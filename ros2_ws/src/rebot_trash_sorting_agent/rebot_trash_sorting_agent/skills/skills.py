"""Composable perception, motion, grasp and place skills for the planner.

``pick_and_place`` is one long, boring, verifiable sequence:

    look -> (optional wrist correction) -> above -> down -> close -> check
         -> lift -> above the destination -> release -> retreat

Every step either returns a measurement or raises :class:`SkillError`, so the
planner always gets a concrete reason ("closed on nothing", "no reachable grasp")
instead of a boolean. Nothing here talks to the robot directly: motion and
gripper objects are injected, which is what makes the dry-run mode and the unit
tests possible.
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable, Sequence
from typing import Any

from rebot_trash_sorting_agent.perception.detector import discovery_vocabulary
from rebot_trash_sorting_agent.skills.grasp import (
    GraspPlan,
    plan_grasp,
)
from rebot_trash_sorting_agent.skills.place import resolve_place
from rebot_trash_sorting_agent.skills.poses import ToolPose
from rebot_trash_sorting_agent.types import (
    PlaceTarget,
    ToolResult,
    WorldObject,
)


class SkillError(RuntimeError):
    """A skill refused or failed; the message goes back to the planner."""


class TaskCancelled(SkillError):
    pass


Detect = Callable[[Any], Sequence[Any]]
AnnotateSink = Callable[[bytes], None]


class SkillRunner:
    def __init__(
        self,
        *,
        places: dict[str, Any],
        motion_cfg: dict[str, Any],
        scene: Any,
        camera: Any,
        detector: Any,
        motion: Any,
        gripper: Any,
        events: Any,
        table_map: Any = None,
        plan_only: bool = False,
        wrist_camera: Any = None,
        annotated_sink: AnnotateSink | None = None,
        front_camera: Any = None,
        height_camera: Any = None,
        baseline_classes: Sequence[str] = (),
        holding: dict[str, Any] | None = None,
    ) -> None:
        self.places = places
        self.motion_cfg = motion_cfg
        self.scene = scene
        self.camera = camera
        self.detector = detector
        self.motion = motion
        self.gripper = gripper
        self.events = events
        self.table_map = table_map
        self.plan_only = bool(plan_only)
        self.wrist_camera = wrist_camera
        self.annotated_sink = annotated_sink
        self.front_camera = front_camera
        self.height_camera = height_camera
        self.baseline_classes = list(baseline_classes)
        self.holding = holding if holding is not None else {}
        self._cancelled = False

        self._grasp_cfg = dict(motion_cfg.get("grasp") or {})
        self._place_cfg = dict(motion_cfg.get("place") or {})
        self._wrist_cfg = dict(motion_cfg.get("wrist_correction") or {})
        self._table_z = float((places.get("table") or {}).get("z", -0.012))

    # ------------------------------------------------------------------ control
    def cancel(self) -> None:
        self._cancelled = True

    def reset(self) -> None:
        self._cancelled = False

    def _check_cancel(self) -> None:
        if self._cancelled:
            raise TaskCancelled("stopped by the operator")

    # ------------------------------------------------------------------ dispatch
    def __call__(self, name: str, arguments: dict[str, Any]) -> ToolResult:
        started = time.monotonic()
        try:
            handlers = {
                "list_objects": lambda: self.list_objects(arguments.get("classes")),
                "detect_objects": lambda: self.list_objects(arguments.get("classes")),
                "pick_and_place": lambda: self.pick_and_place(
                    str(arguments.get("object", "")),
                    arguments.get("destination"),
                ),
                "move_above_object": lambda: self.move_above_object(
                    str(arguments.get("object", "")),
                    float(arguments.get("clearance_m", 0.10)),
                ),
                "move_to_pose": lambda: self.move_to_pose(
                    ToolPose(
                        float(arguments["x"]),
                        float(arguments["y"]),
                        float(arguments["z"]),
                        float(arguments.get("yaw_deg", 0)),
                        float(arguments.get("tilt_deg", 0)),
                    ),
                ),
                "grasp_object": lambda: self.grasp_object(
                    str(arguments.get("object", "")),
                    bool(arguments.get("lift", True)),
                ),
                "place_object": lambda: self.place_object(arguments.get("destination")),
                "open_gripper": lambda: self.command_gripper(True),
                "close_gripper": lambda: self.command_gripper(False),
                "move_home": self.move_home,
            }
            handler = handlers.get(name)
            if handler is None:
                raise SkillError(f"unknown skill {name!r}")
            payload = handler()
        except TaskCancelled as exc:
            return ToolResult(name, {"error": str(exc), "cancelled": True}, True)
        except SkillError as exc:
            return ToolResult(name, {"error": str(exc)}, True)
        except Exception as exc:  # noqa: BLE001 - a driver error must reach the planner as data
            return ToolResult(name, {"error": f"{type(exc).__name__}: {exc}"}, True)
        payload.setdefault("elapsed_s", round(time.monotonic() - started, 2))
        return ToolResult(name, payload, False)

    # ------------------------------------------------------------------ list_objects
    def list_objects(self, classes: Any = None) -> dict[str, Any]:
        if classes is not None:
            vocabulary = discovery_vocabulary(classes, self.baseline_classes)
            if vocabulary:
                self.detector.set_vocabulary(vocabulary)
                self.events.emit("detector_vocabulary", classes=vocabulary)
        frame = self._grab(self.camera)
        if frame is None:
            raise SkillError(
                "no camera frame: is camera_node running and is cameras.yaml device correct?",
            )
        detections = self._detect(frame)
        objects = self.scene.update(detections, self.table_map)
        height_note = self._update_heights(objects)
        self._publish_annotated(frame, detections)
        pixels = [
            {
                "label": detection.label,
                "score": round(detection.score, 3),
                "bbox": list(detection.bbox),
                "polygon": [
                    list(point) for point in detection.polygon[:: max(1, math.ceil(len(detection.polygon) / 64))]
                ],
            }
            for detection in detections
        ]
        vocabulary = list(getattr(self.detector, "vocabulary", ()))

        if self.table_map is None:
            return {
                "calibrated": False,
                "objects": [],
                "detections": pixels,
                "classes": vocabulary,
                "summary": (
                    "the table camera is not calibrated, so pixels cannot be turned into "
                    "robot positions; run scripts/calibrate_table.py before picking"
                ),
            }
        return {
            "calibrated": True,
            "visible": len(objects),
            "height_estimation": height_note,
            "detections": pixels,
            "classes": vocabulary,
            "objects": self.scene.as_summaries(),
            "summary": _objects_sentence(objects),
        }

    # ------------------------------------------------------------------ pick_and_place
    def pick_and_place(self, label: str, destination: str | None = None) -> dict[str, Any]:
        grasped = self.grasp_object(label)
        if self.plan_only:
            grasped["destination"] = destination
            grasped["summary"] = f"dry run: would pick {label} and place at {destination or 'a free spot'}"
            return grasped
        placed = self.place_object(destination)
        placed["steps"] = grasped["steps"] + placed["steps"]
        placed["attempts"] = grasped["attempts"]
        placed["notes"] = grasped["notes"] + placed["notes"]
        return placed

    def _object(self, label: str) -> WorldObject:
        if self.table_map is None:
            raise SkillError("table camera is not calibrated; cannot target an object reliably")
        label = (label or "").strip()
        if not label:
            raise SkillError("no object label given")
        visible = [obj for obj in self.scene.all() if obj.state == "visible"]
        matches = [obj for obj in visible if obj.label.lower() == label.lower()]
        if not matches:
            matches = [obj for obj in visible if label.lower() in obj.label.lower()]
        if len(matches) != 1:
            raise SkillError(
                f"need exactly one visible object matching {label!r}; found {len(matches)}. "
                "Detect again or clarify the target",
            )
        self._check_cancel()
        return matches[0]

    def move_above_object(self, label: str, clearance_m: float = 0.10) -> dict[str, Any]:
        if not math.isfinite(clearance_m) or not 0.02 <= clearance_m <= 0.25:
            raise SkillError("clearance_m must be between 0.02 and 0.25 metres")
        obj = self._object(label)
        plan = plan_grasp(obj, self.motion_cfg, self._table_z)
        pose = ToolPose(
            obj.x,
            obj.y,
            max(plan.pre_grasp.z, obj.z + (obj.height_m or 0) + clearance_m),
            plan.grasp.yaw_deg,
        )
        result = self.move_to_pose(pose)
        result.update(
            object=obj.label,
            summary=f"{'dry run: would move' if self.plan_only else 'moved'} above {obj.label}; gripper unchanged",
        )
        return result

    def move_to_pose(self, pose: ToolPose) -> dict[str, Any]:
        self._check_cancel()
        values = (pose.x, pose.y, pose.z, pose.yaw_deg, pose.tilt_deg)
        limits = dict(self.motion_cfg.get("tool_limits") or {})
        if not all(math.isfinite(value) for value in values):
            raise SkillError("pose coordinates and angles must be finite")
        if (
            pose.z < self._table_z + float(limits.get("min_height_m", 0.002))
            or pose.z > self._table_z + float(limits.get("max_height_m", 0.60))
            or math.hypot(pose.x, pose.y) > float(limits.get("max_radius_m", 0.65))
        ):
            raise SkillError("requested pose is outside configured tool_limits")
        if not self.motion.ik_feasible(pose):
            raise SkillError("requested tool pose has no IK solution")
        result = self.motion.move_to_pose(
            pose,
            plan_only=self.plan_only,
            label="requested tool pose",
            speed_profile="default" if self.holding else "travel",
        )
        return {
            "success": True,
            "dry_run": self.plan_only,
            "pose": pose.summary(),
            "motion": result,
            "summary": "pose planned" if self.plan_only else "tool moved to requested pose",
        }

    def command_gripper(self, opening: bool) -> dict[str, Any]:
        self._check_cancel()
        if self.plan_only:
            return {
                "success": True,
                "dry_run": True,
                "summary": f"dry run: would {'open' if opening else 'close'} gripper",
            }
        result = self.gripper.open() if opening else self.gripper.close()
        if opening:
            held = self.holding.get("object")
            if held is not None:
                self.scene.remove(held.label)
            self.holding.clear()
        elif result.get("holding") and not self.holding:
            self.holding.update(object=WorldObject("unknown object", 0, 0, self._table_z), close=result)
        return {
            "success": True,
            "gripper": result,
            "holding": bool(result.get("holding")) if not opening else False,
            "summary": "gripper opened" if opening else "gripper closed; inspect holding result",
        }

    def grasp_object(self, label: str, lift: bool = True) -> dict[str, Any]:
        if self.holding:
            raise SkillError("gripper already holds an object; place it or explicitly open the gripper first")
        obj = self._object(label)

        notes: list[str] = []
        if obj.state == "remembered":
            notes.append(
                f"{obj.label} was last seen {obj.age_s:.1f} s ago and is not visible now; the position may be stale",
            )

        plans, grasp_notes = self._reachable_grasps(obj)
        notes.extend(grasp_notes)

        dx, dy, wrist_note = self._wrist_correction(obj)
        if wrist_note:
            notes.append(wrist_note)
            if dx or dy:
                plans = [plan.offset(dx=dx, dy=dy) for plan in plans]

        first = plans[0]
        plan = {
            "object": obj.label,
            "at": {"x": round(obj.x, 4), "y": round(obj.y, 4)},
            "grasp": first.grasp.summary(),
            "pre_grasp": first.pre_grasp.summary(),
            "candidates": [candidate.summary() for candidate in first.candidates],
            "dry_run": self.plan_only,
        }
        if self.plan_only:
            return {
                "success": True,
                "dry_run": True,
                "plan": {**plan, "all_candidates": [p.summary() for p in plans]},
                "notes": notes,
                "summary": f"dry run: would pick {obj.label} at ({obj.x:.3f}, {obj.y:.3f})",
            }

        steps: list[dict[str, Any]] = []
        attempts: list[dict[str, Any]] = []
        chosen: GraspPlan | None = None
        close: dict[str, Any] = {}
        hold: dict[str, Any] = {}
        for candidate_plan in plans:
            self._check_cancel()
            steps.append(
                self.motion.move_to_pose(candidate_plan.pre_grasp, label="above object", speed_profile="travel")
            )
            # Open here: it drops nothing important (we are above the target) and it gives
            # the torque monitor a free-air baseline before the close.
            self.gripper.open()
            self._check_cancel()
            steps.append(self.motion.move_to_pose(candidate_plan.grasp, label="grasp"))
            self._check_cancel()

            close = self.gripper.close()
            if not close.get("holding"):
                attempts.append({"grasp": candidate_plan.grasp.summary(), "close": _grasp_payload(close)})
                # Retreat with the jaws still closed: if the torque test missed a soft
                # object, it comes up rather than being knocked off the table by an
                # opening jaw.
                self.motion.move_to_pose(candidate_plan.pre_grasp, label="retreat after empty grasp")
                self.gripper.open()
                continue

            self.holding.update(object=obj, plan=candidate_plan, close=close)
            self._check_cancel()
            if lift:
                steps.append(self.motion.move_to_pose(candidate_plan.lift, label="lift"))

            # A grasp that survives the close can still slide out on the way up. Torque
            # and finger position are re-read here; either dropping is a slip.
            hold = self.gripper.check_hold(close)
            self.events.emit("grasp_hold", object=obj.label, **hold)
            if hold["slipped"] or not hold["holding"]:
                attempts.append({"grasp": candidate_plan.grasp.summary(), "close": _grasp_payload(close), "hold": hold})
                self.gripper.open()
                self.holding.clear()
                continue

            chosen = candidate_plan
            break

        if chosen is None:
            raise SkillError(
                f"could not hold {obj.label} after {len(attempts)} grasp attempt(s) ({_attempts_sentence(attempts)}); it is probably not where "
                "the detector thought, too wide for the jaw, or out of reach",
            )

        self.holding.update(hold=hold)
        return {
            "success": True,
            "object": obj.label,
            "holding": True,
            "lifted": lift,
            "grasp": _grasp_payload(close),
            "grasp_plan": chosen.summary(),
            "hold": hold,
            "attempts": attempts,
            "steps": steps,
            "notes": notes,
            "summary": f"grasped {obj.label}{' and lifted it' if lift else ''}; still holding, not placed",
        }

    def place_object(self, destination: str | None = None) -> dict[str, Any]:
        self._check_cancel()
        if not self.holding:
            raise SkillError("no held object; grasp an object before placing")
        obj = self.holding["object"]
        chosen = self.holding.get("plan")
        close = self.holding.get("close", {})
        hold = self.holding.get("hold", {})
        exclude = [other for other in self.scene.all() if other.label != obj.label]
        target, release, approach, place_notes = self._reachable_place(destination, objects=exclude)
        notes = list(place_notes)
        if self.plan_only:
            return {
                "success": True,
                "dry_run": True,
                "object": obj.label,
                "destination": target.name,
                "pose": release.summary(),
                "summary": f"dry run: would place {obj.label} at {target.name}",
            }
        steps: list[dict[str, Any]] = []

        if approach is not None:
            self._check_cancel()
            steps.append(self.motion.move_to_pose(approach, label=f"above {target.name}"))
        self._check_cancel()
        steps.append(self.motion.move_to_pose(release, label=f"release at {target.name}"))

        self.gripper.open()
        self.holding.clear()
        retreat = release.offset(dz=0.12)
        self._safe_retreat(retreat)
        self.scene.remove(obj.label)

        if self.motion_cfg.get("place", {}).get("return_home_after_pick"):
            try:
                self.move_home()
            except Exception:  # noqa: BLE001 - the pick already succeeded
                notes.append("could not return home after release")

        return {
            "success": True,
            "object": obj.label,
            "destination": target.name,
            "grasp": {key: close.get(key) for key in ("position", "torque", "torque_delta")},
            "grasp_plan": chosen.summary() if chosen else None,
            "hold": hold,
            "attempts": [],
            "released_at": {"x": round(release.x, 4), "y": round(release.y, 4), "z": round(release.z, 4)},
            "steps": steps,
            "notes": notes,
            "summary": (
                f"picked {obj.label} and released it at {target.name} "
                f"(x={release.x:.3f}, y={release.y:.3f}, z={release.z:.3f})"
            ),
        }

    # ------------------------------------------------------------------ move_home
    def move_home(self) -> dict[str, Any]:
        if self.plan_only:
            return {
                "success": True,
                "dry_run": True,
                "joints": self.motion.named_pose("home"),
                "summary": "dry run: would go home",
            }
        result = self.motion.move_named("home", speed_profile="default" if self.holding else "travel")
        return {"success": True, "motion": result, "summary": "arm is at the home pose"}

    # ------------------------------------------------------------------ planning
    def _reachable_grasps(self, obj: WorldObject) -> tuple[list[GraspPlan], list[str]]:
        """Grasp candidates that have IK, in the order they should be attempted."""
        plan = plan_grasp(obj, self.motion_cfg, self._table_z)
        pre_clear = float(self._grasp_cfg.get("pre_grasp_clearance", 0.12))
        lift_clear = float(self._grasp_cfg.get("lift_clearance", 0.10))
        max_attempts = max(1, int(self._grasp_cfg.get("max_attempts", 3)))
        notes = list(plan.notes)

        plans: list[GraspPlan] = []
        for candidate in plan.candidates:
            grasp = ToolPose(candidate.x, candidate.y, candidate.z, candidate.yaw_deg)
            if not self.motion.ik_feasible(grasp):
                continue
            if obj.height_m:
                pre_heights = [
                    max(pre_clear, self._table_z + obj.height_m + 0.04 - grasp.z),
                    max(0.03, self._table_z + obj.height_m + 0.015 - grasp.z),
                ]
            else:
                pre_heights = [pre_clear]
            pre_grasp = None
            for clearance in pre_heights:
                cand_pre = grasp.offset(dz=clearance)
                if self.motion.ik_feasible(cand_pre):
                    pre_grasp = cand_pre
                    break
            if pre_grasp is not None:
                lift = grasp.offset(dz=lift_clear)
                plans.append(
                    GraspPlan(
                        label=obj.label,
                        pre_grasp=pre_grasp,
                        grasp=grasp,
                        lift=lift,
                        candidates=[candidate],
                    ),
                )
        if not plans:
            raise SkillError(
                f"no reachable grasp for {obj.label} at ({obj.x:.3f}, {obj.y:.3f}): "
                f"IK failed for all {len(plan.candidates)} candidate poses. Move the object "
                "closer to the arm (x 0.16-0.34 m, |y| < 0.26 m) or rotate it.",
            )
        skipped = len(plan.candidates) - len(plans)
        if skipped:
            notes.append(f"{skipped} of {len(plan.candidates)} grasp candidates skipped: no IK")
        if len(plans) > max_attempts:
            notes.append(f"trying the first {max_attempts} of {len(plans)} reachable candidates")
            plans = plans[:max_attempts]
        return plans, notes

    def _reachable_place(
        self,
        destination: str | None,
        objects: Sequence[WorldObject] = (),
    ) -> tuple[PlaceTarget, ToolPose, ToolPose | None, list[str]]:
        targets = resolve_place(
            destination,
            self.places,
            self.motion_cfg,
            objects=objects,
            ik_check=self.motion.ik_feasible,
        )
        notes: list[str] = []
        approach_clear = float(self._place_cfg.get("approach_clearance", 0.10))
        for target in targets:
            release = ToolPose(target.x, target.y, target.z, target.yaw_deg, target.tilt_deg)
            if not self.motion.ik_feasible(release):
                notes.append(f"{target.name}: release pose is out of reach")
                continue
            approach = release.offset(dz=approach_clear)
            if not self.motion.ik_feasible(approach):
                notes.append(f"{target.name}: no reachable approach pose, descending directly")
                approach = None
            if target.kind == "table" and destination and destination not in ("table", ""):
                notes.append(f"{destination} unreachable; used a free spot on the table instead")
            return target, release, approach, notes
        raise SkillError(
            "no reachable place target: " + ("; ".join(notes) if notes else "nothing configured"),
        )

    def _update_heights(self, objects: Sequence[WorldObject]) -> str:
        for obj in objects:
            obj.height_m = None
        if self.front_camera is None or self.height_camera is None:
            return "front_camera not configured or height pose not calibrated; using fallback grasp heights"
        if not objects:
            return "no visible objects"
        frame = self._grab(self.front_camera, fresh_timeout=1.5)
        if frame is None:
            return "no fresh front_camera frame; using fallback grasp heights"
        detections = self._detect(frame)
        cfg = dict(self.motion_cfg.get("height_estimation") or {})
        try:
            estimates = self.height_camera.estimate_heights(
                objects,
                detections,
                (frame.shape[1], frame.shape[0]),
                match_margin_px=float(cfg.get("match_margin_px", 20.0)),
                min_height_m=float(cfg.get("min_height_m", 0.005)),
                max_height_m=float(cfg.get("max_height_m", 0.35)),
            )
        except ValueError as exc:
            self.events.emit("height_rejected", reason=str(exc))
            return f"front_camera height rejected: {exc}; using fallback grasp heights"
        for index, height in estimates.items():
            objects[index].height_m = height
            self.events.emit("object_height", object=objects[index].label, height_m=round(height, 4))
        source = (
            "approximate FOV intrinsics"
            if self.height_camera.meta.get("approximate_intrinsics")
            else "calibrated intrinsics"
        )
        return f"front_camera: estimated {len(estimates)}/{len(objects)} heights ({source})"

    # ------------------------------------------------------------------ wrist correction
    def _wrist_correction(self, obj: WorldObject) -> tuple[float, float, str | None]:
        if not self._wrist_cfg.get("enabled", False) or self.wrist_camera is None:
            return 0.0, 0.0, None
        frame = self._grab(self.wrist_camera, fresh_timeout=1.5)
        if frame is None:
            return 0.0, 0.0, "wrist camera gave no frame; grasping without the second view"
        detections = self._detect(frame)
        if not detections:
            return 0.0, 0.0, "wrist view found nothing; grasping without the second view"
        same = [d for d in detections if d.label == obj.label] or detections
        best = max(same, key=lambda d: d.score)
        height, width = frame.shape[:2]
        u, v = best.centre_px
        du, dv = u - width / 2.0, v - height / 2.0
        m_per_px = float(self._wrist_cfg.get("m_per_px", 0.00025))
        u_to_base = list(self._wrist_cfg.get("u_to_base", [0.0, 1.0]))
        v_to_base = list(self._wrist_cfg.get("v_to_base", [1.0, 0.0]))
        dx = m_per_px * (u_to_base[0] * du + v_to_base[0] * dv)
        dy = m_per_px * (u_to_base[1] * du + v_to_base[1] * dv)
        limit = float(self._wrist_cfg.get("max_offset_m", 0.04))
        dx, dy = max(-limit, min(limit, dx)), max(-limit, min(limit, dy))
        if abs(dx) < 0.002 and abs(dy) < 0.002:
            return 0.0, 0.0, "wrist view agrees with the table camera"
        return (
            dx,
            dy,
            (
                f"wrist correction {1000 * dx:+.0f} mm x, {1000 * dy:+.0f} mm y from a "
                f"{best.label} at ({u:.0f}, {v:.0f}) px"
            ),
        )

    # ------------------------------------------------------------------ helpers
    def _grab(self, camera: Any, fresh_timeout: float | None = None) -> Any:
        if camera is None:
            return None
        try:
            wait_fresh = getattr(camera, "wait_fresh", None)
            if wait_fresh is not None:
                return wait_fresh(fresh_timeout if fresh_timeout is not None else 2.0)
            return camera.wait()
        except Exception as exc:  # noqa: BLE001 - broken camera must not kill the task
            self.events.emit("camera_error", error=str(exc))
            return None

    def _detect(self, frame: Any) -> list[Any]:
        try:
            return list(self.detector.detect(frame))
        except Exception as exc:
            raise SkillError(f"detector failed: {exc}") from exc

    def _publish_annotated(self, frame: Any, detections: Sequence[Any]) -> None:
        if self.annotated_sink is None:
            return
        try:
            from ..perception.detector import annotate
            from ..vlm.json_tools import encode_jpeg

            self.annotated_sink(encode_jpeg(annotate(frame, detections), max_side=960, quality=80))
        except Exception:  # noqa: BLE001 - the dashboard image is a nicety
            pass

    def _safe_retreat(self, pose: ToolPose) -> None:
        try:
            self.motion.move_to_pose(pose, label="retreat", speed_profile="default" if self.holding else "travel")
        except Exception as exc:  # noqa: BLE001 - never hide the original failure
            self.events.emit("retreat_failed", error=str(exc), pose=pose.summary())


def _grasp_payload(result: dict[str, Any]) -> dict[str, Any]:
    """The handful of fields worth keeping from one failed attempt."""
    return {key: result.get(key) for key in ("position", "torque", "torque_delta", "holding", "slipped")}


def _attempts_sentence(attempts: Sequence[dict[str, Any]]) -> str:
    parts = []
    for index, attempt in enumerate(attempts, start=1):
        grasp = attempt.get("grasp") or {}
        pinch = grasp.get("pinch_m")
        where = f"at pinch {float(pinch) * 100:.1f} cm" if pinch is not None else "no pinch height"
        parts.append(f"try {index} {where}: {_grasp_numbers(attempt.get('close') or {})}")
    return "; ".join(parts) or "no measurements"


def _grasp_numbers(result: dict[str, Any]) -> str:
    """One line for the operator: what the fingers and the motor actually did."""
    parts = []
    position = result.get("position")
    if position is not None:
        parts.append(f"finger {position * 1000:.1f} mm")
    torque = result.get("torque")
    if torque is not None:
        delta = result.get("torque_delta")
        parts.append(
            f"torque {torque:.3f} N m" + (f" ({delta:+.3f} above free air)" if delta is not None else ""),
        )
    elif result.get("torque_available") is False:
        parts.append("no torque telemetry")
    return ", ".join(parts) or "no measurements"


def _objects_sentence(objects: Sequence[WorldObject]) -> str:
    if not objects:
        return "no objects are visible on the table"
    counts: dict[str, int] = {}
    for obj in objects:
        counts[obj.label] = counts.get(obj.label, 0) + 1
    parts = [f"{count} x {label}" if count > 1 else label for label, count in counts.items()]
    return "visible: " + ", ".join(parts)
