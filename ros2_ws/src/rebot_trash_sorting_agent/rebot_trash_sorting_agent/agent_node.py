#!/usr/bin/env python3
"""The agent node: planner, perception, skills and the ROS surface around them.

Topics

    /agent/task        std_msgs/String   submit a task (one line of English)
    /agent/status      std_msgs/String   JSON, 1 Hz plus on every state change
    /agent/events      std_msgs/String   JSON, one per planner/tool event
    /agent/annotated   CompressedImage   the last frame the detector saw, annotated

Services

    /agent/run         RunTask    queue a task; returns immediately
    /agent/stop        Trigger    stop the running task (motion is cancelled too)

A task runs in its own thread, so the node keeps answering services while the arm
moves. Only one task at a time: this robot has one arm.
"""

from __future__ import annotations

import json
import threading
import time
from collections import deque
from typing import Any

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile

from rebot_trash_sorting_agent.agent.events import EventLog
from rebot_trash_sorting_agent.agent.orchestrator import (
    Orchestrator,
    OrchestratorSettings,
)
from rebot_trash_sorting_agent.agent.prompts import system_prompt
from rebot_trash_sorting_agent.agent.tools import TOOLS
from rebot_trash_sorting_agent.config import Config, load_env_files
from rebot_trash_sorting_agent.perception.detector import (
    vocabulary_from_task,
)
from rebot_trash_sorting_agent.perception.height import HeightCamera
from rebot_trash_sorting_agent.perception.scene import (
    CameraClient,
    SceneModel,
)
from rebot_trash_sorting_agent.perception.table_map import TableMap
from rebot_trash_sorting_agent.skills.gripper import GripperClient
from rebot_trash_sorting_agent.skills.motion import MoveItClient
from rebot_trash_sorting_agent.skills.planning_scene import PlanningSceneClient
from rebot_trash_sorting_agent.skills.skills import SkillRunner
from rebot_trash_sorting_agent.types import TaskResult
from rebot_trash_sorting_agent.vlm.json_tools import encode_jpeg
from rebot_trash_sorting_agent.vlm.registry import make_session


class LazyDetector:
    """Build the detector on first use; a missing ultralytics must not stop the node."""

    def __init__(self, settings: dict[str, Any], node: Node) -> None:
        self._settings = dict(settings)
        self._node = node
        self._detector = None
        self._error: str | None = None

    def set_vocabulary(self, words: list[str]) -> None:
        self._settings = dict(self._settings)
        self._settings["classes"] = list(words)
        if self._detector is not None:
            self._detector.set_vocabulary(words)

    @property
    def vocabulary(self) -> list[str]:
        return list(self._settings.get("classes") or ())

    def detect(self, frame: Any):
        if self._error is not None:
            raise RuntimeError(self._error)
        if self._detector is None:
            from .perception.detector import YoloeDetector

            started = time.monotonic()
            try:
                detector = YoloeDetector(self._settings)
                detector.load()
            except Exception as exc:
                self._error = str(exc)
                raise
            self._detector = detector
            self._node.get_logger().info(
                f"detector loaded in {time.monotonic() - started:.1f} s "
                f"({detector.model_path.name}, {len(detector.classes)} prompts)",
            )
        return self._detector.detect(frame)


class AgentNode(Node):
    def __init__(self) -> None:
        super().__init__("agent_node")
        self.declare_parameter("config_dir", "")
        self.declare_parameter("provider", "")
        self.declare_parameter("vlm_model", "")
        self.declare_parameter("dry_run", False)
        self.declare_parameter("max_steps", 0)
        self.declare_parameter("table_camera", "table")

        loaded = load_env_files()
        self._config = Config.load(self._str_param("config_dir") or None)
        self._apply_overrides()
        for path in loaded:
            self.get_logger().info(f"loaded environment from {path}")

        self._state = "idle"
        self._task = ""
        self._result: TaskResult | None = None
        self._busy = threading.Event()
        self._orchestrator: Orchestrator | None = None
        self._runner: SkillRunner | None = None
        self._worker: threading.Thread | None = None
        self._events_tail: deque[dict[str, Any]] = deque(maxlen=60)
        self._holding: dict[str, Any] = {}
        self._cb = ReentrantCallbackGroup()

        self._table_name = self._str_param("table_camera") or "table"
        self._table_cfg = self._config.camera(self._table_name)
        self._table_topic = self._config.capture_topic(self._table_name)
        self._table_map = TableMap.from_mapping(
            self._config.table_map(self._table_name),
            float(self._config.table().get("z", -0.012)),
        )
        self._wrist_name = next(
            (c["name"] for c in self._config.camera_list if c["name"] == "wrist"),
            next((c["name"] for c in self._config.camera_list if c["name"] != self._table_name), None),
        )

        self._scene = SceneModel(
            merge_radius=float(self._config.perception.get("merge_radius", 0.05)),
        )
        timeout = float(self._config.run.get("capture_timeout_s", 5.0))
        self._camera = CameraClient(self, self._table_topic, timeout_s=timeout)
        self._wrist_camera = (
            CameraClient(self, self._config.capture_topic(self._wrist_name), timeout_s=timeout)
            if self._wrist_name
            else None
        )
        self._detector = LazyDetector(self._config.perception, self)
        front_cfg = next(
            (
                camera
                for camera in self._config.camera_list
                if camera["name"] == "front_camera" and camera.get("enabled", True)
            ),
            None,
        )
        self._front_camera = (
            CameraClient(self, self._config.capture_topic("front_camera"), timeout_s=timeout) if front_cfg else None
        )
        front_map = self._config.table_map("front_camera") if front_cfg else None
        self._height_camera = HeightCamera.from_mapping((front_map or {}).get("height_camera"))
        self._motion = MoveItClient(self, self._config.motion)
        scene_cfg = dict(self._config.motion.get("planning_scene") or {})
        self._planning_scene = (
            PlanningSceneClient(self, self._motion, scene_cfg, self._config.places)
            if scene_cfg.get("enabled", False)
            else None
        )
        self._gripper = GripperClient(self, dict(self._config.motion.get("gripper") or {}))

        self._status_pub = self.create_publisher(
            __import__("std_msgs.msg", fromlist=["String"]).String,
            "/agent/status",
            10,
        )
        self._event_pub = self.create_publisher(
            __import__("std_msgs.msg", fromlist=["String"]).String,
            "/agent/events",
            50,
        )
        from sensor_msgs.msg import CompressedImage

        self._annotated_pub = self.create_publisher(CompressedImage, "/agent/annotated", 5)
        self._status_pub_qos = QoSProfile(
            depth=1,
            history=HistoryPolicy.KEEP_LAST,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
        )

        from rebot_trash_sorting_agent_msgs.srv import RunTask
        from std_msgs.msg import Empty, String
        from std_srvs.srv import Trigger

        self.create_subscription(String, "/agent/task", self._on_task_topic, 10, callback_group=self._cb)
        self.create_subscription(Empty, "/agent/cancel", lambda _: self._stop("topic"), 10, callback_group=self._cb)
        self.create_service(RunTask, "/agent/run", self._on_run, callback_group=self._cb)
        self.create_service(Trigger, "/agent/stop", self._on_stop, callback_group=self._cb)
        self.create_timer(1.0, self._publish_status, callback_group=self._cb)

        self._log_startup()
        self._publish_status()

    # ------------------------------------------------------------------ setup
    def _str_param(self, name: str) -> str:
        value = self.get_parameter(name).value
        return str(value).strip() if value is not None else ""

    def _apply_overrides(self) -> None:
        provider = self._str_param("provider").lower()
        model = self._str_param("vlm_model")
        max_steps = int(self.get_parameter("max_steps").value or 0)
        dry_run = bool(self.get_parameter("dry_run").value)
        if provider or model or max_steps or dry_run:
            vlm = self._config.vlm
            self._config.vlm = type(vlm)(
                provider=provider or vlm.provider,
                model=model or vlm.model,
                tool_mode=vlm.tool_mode,
                api_key_env=vlm.api_key_env,
                base_url=vlm.base_url,
                thinking_level=vlm.thinking_level,
                max_output_tokens=vlm.max_output_tokens,
                temperature=vlm.temperature,
                timeout_s=vlm.timeout_s,
                retries=vlm.retries,
                max_steps=max_steps or vlm.max_steps,
                history_images=vlm.history_images,
            )
        if dry_run:
            self._config.run["dry_run"] = True

    def _log_startup(self) -> None:
        vlm = self._config.vlm
        self.get_logger().info(
            f"planner: {vlm.provider}/{vlm.model} ({vlm.tool_mode} tools, max {vlm.max_steps} steps)",
        )
        self.get_logger().info(f"camera: {self._table_topic}")
        if self._table_map is None:
            self.get_logger().warn(
                "table camera is NOT calibrated: run "
                "'ros2 run rebot_trash_sorting_agent calibrate_table' before picking",
            )
        else:
            self.get_logger().info(f"table map: {self._table_map.describe()}")
        if self._config.run.get("dry_run"):
            self.get_logger().warn("dry run: no motion will be executed")
        if vlm.provider != "mock" and not self._config.api_key():
            self.get_logger().error(
                f"no API key in ${vlm.api_key_env}: set it in ros2_ws/.env or export it",
            )

    # ------------------------------------------------------------------ inputs
    def _on_task_topic(self, msg: Any) -> None:
        accepted, message = self.start_task(str(msg.data))
        if not accepted:
            self.get_logger().warn(f"task rejected: {message}")

    def _on_run(self, request: Any, response: Any) -> Any:
        accepted, message = self.start_task(str(request.task))
        response.accepted = accepted
        response.message = message
        return response

    def _on_stop(self, _request: Any, response: Any) -> Any:
        response.success = self._stop("service")
        response.message = "stopping the running task" if response.success else "idle"
        return response

    # ------------------------------------------------------------------ task control
    def start_task(self, task: str) -> tuple[bool, str]:
        task = (task or "").strip()
        if not task:
            return False, "empty task"
        if self._busy.is_set():
            return False, f"busy with: {self._task}"
        self._busy.set()
        self._task = task
        self._result = None
        self._state = "running"
        self._publish_status()
        self._worker = threading.Thread(target=self._run_task, args=(task,), name="agent_task", daemon=True)
        self._worker.start()
        return True, "task accepted"

    def _stop(self, source: str) -> bool:
        if not self._busy.is_set():
            return False
        self.get_logger().warn(f"stop requested ({source})")
        if self._runner is not None:
            self._runner.cancel()
        if self._orchestrator is not None:
            self._orchestrator.cancel()
        try:
            self._motion.cancel()
        except Exception:  # noqa: BLE001 - stopping must not raise
            pass
        self._state = "stopping"
        self._publish_status()
        return True

    def _run_task(self, task: str) -> None:
        runs_dir = (self._config.agent.get("logging") or {}).get("runs_dir")
        events = EventLog(runs_dir, echo=self._publish_event)
        self._events_tail.clear()
        self._scene.clear()
        try:
            vocabulary = vocabulary_from_task(
                task,
                self._config.perception.get("classes") or (),
            )
            self._detector.set_vocabulary(vocabulary)
            self.get_logger().info(
                f"task vocabulary ({len(vocabulary)}): {', '.join(vocabulary[:8])}"
                + (" ..." if len(vocabulary) > 8 else ""),
            )
            session = make_session(
                self._config.vlm,
                system_prompt(self._config, [c["name"] for c in self._config.camera_list]),
                TOOLS,
                api_key=self._config.api_key(),
            )
            runner = SkillRunner(
                places=self._config.places,
                motion_cfg=self._config.motion,
                scene=self._scene,
                camera=self._camera,
                detector=self._detector,
                motion=self._motion,
                gripper=self._gripper,
                events=events,
                table_map=self._table_map,
                plan_only=bool(self._config.run.get("dry_run", False)),
                wrist_camera=self._wrist_camera,
                front_camera=self._front_camera,
                height_camera=self._height_camera,
                baseline_classes=self._config.perception.get("classes") or (),
                holding=self._holding,
                planning_scene=self._planning_scene,
                annotated_sink=self._publish_annotated,
            )
            self._runner = runner
            self._orchestrator = Orchestrator(
                session=session,
                tools=TOOLS,
                runner=runner,
                events=events,
                settings=OrchestratorSettings(
                    max_steps=self._config.vlm.max_steps,
                    timeout_s=float(self._config.run.get("task_timeout_s", 240.0)),
                ),
                scene=self.scene_text,
                capture=self.capture_jpeg,
            )
            result = self._orchestrator.run(task)
        except Exception as exc:  # noqa: BLE001 - e.g. missing API key or SDK
            result = TaskResult(task=task, success=False, summary="agent could not start", steps=0, error=str(exc))
            events.emit("task_error", error=str(exc))
        finally:
            self._runner = None
            self._orchestrator = None
            self._busy.clear()

        self._result = result
        self._state = "stopped" if result.stopped else ("done" if result.success else "failed")
        self._publish_status()
        log = self.get_logger().info if result.success else self.get_logger().warn
        log(f"task {self._state}: {result.summary or result.error or ''}")

    # ------------------------------------------------------------------ data for the planner
    def scene_text(self) -> str:
        lines = []
        if self._table_map is None:
            lines.append(
                "TABLE CAMERA NOT CALIBRATED: positions are unavailable until scripts/calibrate_table.py has been run.",
            )
        else:
            error = self._table_map.error_mm
            lines.append(
                "table camera calibrated" + (f" (reprojection error {error:.1f} mm)" if error is not None else ""),
            )
        lines.append("objects from the last camera view:")
        lines.append(self._scene.summary_text())
        lines.append("active detector classes: " + ", ".join(self._detector.vocabulary))
        held = self._holding.get("object")
        lines.append(f"gripper holding: {held.label if held else 'nothing confirmed'}")
        return "\n".join(lines)

    def capture_jpeg(self) -> bytes | None:
        frame = self._camera.wait_fresh(1.5)
        if frame is None:
            return None
        return encode_jpeg(
            frame,
            max_side=int(self._config.perception.get("max_side", 1024)),
            quality=int(self._config.perception.get("jpeg_quality", 85)),
        )

    def _publish_annotated(self, data: bytes) -> None:
        from sensor_msgs.msg import CompressedImage

        message = CompressedImage()
        message.header.stamp = self.get_clock().now().to_msg()
        message.header.frame_id = str(self._table_cfg.get("frame_id") or "table_cam")
        message.format = "jpeg"
        message.data = data
        self._annotated_pub.publish(message)

    def _publish_event(self, event: dict[str, Any]) -> None:
        from std_msgs.msg import String

        self._events_tail.append(event)
        message = String()
        message.data = json.dumps(event, separators=(",", ":"), default=str)
        self._event_pub.publish(message)

    # ------------------------------------------------------------------ status
    def _publish_status(self) -> None:
        from std_msgs.msg import String

        status = {
            "state": self._state,
            "task": self._task,
            "busy": self._busy.is_set(),
            "provider": self._config.vlm.provider,
            "model": self._config.vlm.model,
            "dry_run": bool(self._config.run.get("dry_run", False)),
            "calibrated": self._table_map is not None,
            "camera": self._table_topic,
            "frames": self._camera.frames_received,
            "wrist_frames": self._wrist_camera.frames_received if self._wrist_camera else 0,
            "front_frames": self._front_camera.frames_received if self._front_camera else 0,
            "height_calibrated": self._height_camera is not None,
            "detector_classes": self._detector.vocabulary,
            "holding": self._holding["object"].label if self._holding else None,
            "objects": self._scene.as_summaries(),
            "events": list(self._events_tail)[-12:],
            "updated": round(time.time(), 3),
        }
        if self._result is not None:
            status["result"] = self._result.summary_dict()
        message = String()
        message.data = json.dumps(status, separators=(",", ":"), default=str)
        self._status_pub.publish(message)


def main(argv: list[str] | None = None) -> None:
    rclpy.init(args=argv)
    node = AgentNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node._stop("shutdown")  # noqa: SLF001 - graceful stop of a running task
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
