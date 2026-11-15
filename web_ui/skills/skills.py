"""ROS-free skill runner: local detection + VLA policy delegation."""

from __future__ import annotations

from collections.abc import Callable, Sequence
import time
from typing import Any

from ..perception.detector import annotate, discovery_vocabulary
from ..perception.scene import SceneModel
from ..types import Detection, ToolResult, WorldObject
from .vla_policy import VLAError, VLAPolicyClient

AnnotateSink = Callable[[Any, list[Detection]], None]


class SkillError(RuntimeError):
    """A skill could not run or complete safely."""


class CancelledError(SkillError):
    """Raised when a running skill is cancelled by the operator."""


class SkillRunner:
    """Executes planner tool calls without ROS: perception + VLA policy."""

    def __init__(
        self,
        places: dict[str, Any],
        scene: SceneModel,
        camera: Any,
        detector: Any,
        vla: VLAPolicyClient,
        events: Any,
        *,
        table_map: Any = None,
        cameras: dict[str, Any] | None = None,
        plan_only: bool = False,
        baseline_classes: Sequence[str] = (),
        annotated_sink: AnnotateSink | None = None,
    ) -> None:
        self.places = places
        self.scene = scene
        self.camera = camera
        self.cameras = dict(cameras or {})
        self.detector = detector
        self.vla = vla
        self.events = events
        self.table_map = table_map
        self.plan_only = bool(plan_only)
        self.baseline_classes = list(baseline_classes)
        self.annotated_sink = annotated_sink
        self._cancelled = False
        self._last_detections: list[Detection] = []

    def cancel(self) -> None:
        self._cancelled = True
        self.vla.cancel()

    def reset_cancel(self) -> None:
        self._cancelled = False
        self.vla.reset()

    def _check_cancel(self) -> None:
        if self._cancelled:
            raise CancelledError("cancelled by operator")

    def __call__(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        try:
            self._check_cancel()
            payload = self._dispatch(name, arguments)
            return ToolResult(name, payload, False)
        except CancelledError as exc:
            return ToolResult(name, {"error": str(exc), "cancelled": True}, True)
        except (SkillError, VLAError) as exc:
            return ToolResult(name, {"error": str(exc)}, True)
        except Exception as exc:  # noqa: BLE001
            self.events.emit("skill_crash", skill=name, error=str(exc))
            return ToolResult(name, {"error": f"{type(exc).__name__}: {exc}"}, True)

    def _dispatch(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        if name == "detect_objects":
            return self.detect_objects(args.get("classes"))
        if name == "list_objects":
            return self.list_objects(args.get("classes"))
        if name == "run_vla_policy":
            return self.run_vla_policy(
                instruction=str(args.get("instruction", "")).strip(),
                obj_label=args.get("object"),
                destination=args.get("destination"),
            )
        raise SkillError(f"unknown tool {name!r}")

    def _grab(self, cam: Any, fresh_timeout: float = 2.0):
        if cam is None:
            return None
        frame = cam.wait_fresh(timeout_s=fresh_timeout)
        return frame if frame is not None else cam.latest()

    def _detect(self, frame: Any) -> list[Detection]:
        if self.detector is None:
            return []
        return list(self.detector.detect(frame))

    def _apply_classes(self, classes: Any) -> list[str]:
        if self.detector is None:
            return []
        if classes is not None:
            vocab = discovery_vocabulary(classes, self.baseline_classes)
            if vocab:
                self.detector.set_vocabulary(vocab)
        return list(getattr(self.detector, "classes", ()) or ())

    def detect_objects(self, classes: Any = None) -> dict[str, Any]:
        self._check_cancel()
        vocab = self._apply_classes(classes)
        frame = self._grab(self.camera)
        if frame is None:
            raise SkillError("no camera frame available")

        detections = self._detect(frame)
        self._last_detections = detections
        if self.annotated_sink is not None:
            self.annotated_sink(frame, detections)

        visible = (
            self.scene.update(detections, self.table_map, (frame.shape[1], frame.shape[0]))
            if self.table_map is not None
            else []
        )
        return {
            "vocabulary": vocab,
            "count": len(detections),
            "detections": [
                {"label": d.label, "score": round(d.score, 2), "bbox": [round(v, 1) for v in d.bbox]}
                for d in detections
            ],
            "objects": [o.summary() for o in visible],
            "summary": f"detected {len(detections)} object(s)",
        }

    def list_objects(self, classes: Any = None) -> dict[str, Any]:
        info = self.detect_objects(classes)
        visible = self.scene.visible()
        remembered = [o for o in self.scene.all() if o.state == "remembered"]
        return {
            **info,
            "visible": [o.summary() for o in visible],
            "remembered": [o.summary() for o in remembered],
            "summary": f"{len(visible)} visible, {len(remembered)} remembered",
        }

    def run_vla_policy(
        self,
        instruction: str,
        obj_label: str | None = None,
        destination: str | None = None,
    ) -> dict[str, Any]:
        self._check_cancel()
        if not instruction:
            raise SkillError("instruction is required")

        frames: dict[str, Any] = {}
        for cam_name, cam in self.cameras.items():
            frame = self._grab(cam, fresh_timeout=1.5)
            if frame is not None:
                frames[cam_name] = frame
        if not frames and self.camera is not None:
            frame = self._grab(self.camera, fresh_timeout=1.5)
            if frame is not None:
                frames["table"] = frame

        self.events.emit(
            "vla_start",
            instruction=instruction,
            object=obj_label,
            destination=destination,
            cameras=sorted(frames.keys()),
        )
        result = self.vla.execute(
            instruction,
            frames,
            target=obj_label,
            destination=destination,
            dry_run=self.plan_only,
        )
        self.events.emit("vla_done", instruction=instruction, ok=bool(result.get("success", True)))
        return result
