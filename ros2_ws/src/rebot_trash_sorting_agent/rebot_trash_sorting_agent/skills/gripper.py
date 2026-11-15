"""Parallel-jaw gripper through ``/gripper_controller/follow_joint_trajectory``.

The jaw is one prismatic joint (``finger_left``, 0 = closed .. 0.05 m = open). On
the real arm a bridge node turns this trajectory into the DM gripper's motor
command, on fake hardware it is an ordinary ros2_control JTC, so the same code
drives both.

Two independent signals decide whether a grasp worked:

* **position** - a parallel jaw that stops meaningfully above the command has
  something between its fingers;
* **torque** - the DM motors publish motor torque in ``/joint_states.effort``.
  Position alone cannot tell a soft object from a slip; torque can.

Torque is *not* calibrated to newtons (that needs a force gauge). It is used as a
delta above the free-air reading taken just before closing, with one configurable
threshold - ``holding_torque_delta_nm``. On mock hardware ``effort`` is exactly
0, which is treated as "no telemetry" so the fake-hardware smoke test still works.
"""

from __future__ import annotations

import math
import statistics
import threading
import time
from collections import deque
from typing import Any


class GripperError(RuntimeError):
    """The gripper could not be commanded."""


def judge_holding(position: float | None, closed_m: float, torque: float | None,
                  baseline_torque: float, gap_m: float, torque_delta_nm: float) -> bool:
    """Did the close end on an object?

    Position must show the finger stopped early **and**, when torque telemetry
    exists, the motor must be pushing harder than it was in free air. Without
    torque telemetry the position test alone decides (mock hardware).
    """
    if position is None or not math.isfinite(position):
        return False
    if position - closed_m <= gap_m:
        return False
    if torque is None:
        return True
    return abs(torque - baseline_torque) >= torque_delta_nm


def judge_slip(position: float | None, torque: float | None, reference: dict[str, Any],
               position_drop_m: float, torque_drop_nm: float) -> bool:
    """Did the hold change since the close (object sliding out of the jaw)?"""
    if position is None or not math.isfinite(position):
        return False
    ref_position = reference.get("position")
    if ref_position is not None and ref_position - position > position_drop_m:
        return True
    ref_torque = reference.get("torque")
    if torque is not None and ref_torque is not None and ref_torque - torque > torque_drop_nm:
        return True
    return False


class GripperClient:
    def __init__(self, node: Any, cfg: dict[str, Any]) -> None:
        from control_msgs.action import FollowJointTrajectory
        from rclpy.action import ActionClient
        from rclpy.callback_groups import ReentrantCallbackGroup
        from sensor_msgs.msg import JointState

        self._node = node
        self._Action = FollowJointTrajectory
        self._action_name = str(cfg.get("action", "/gripper_controller/follow_joint_trajectory"))
        self._joint = str(cfg.get("joint", "finger_left"))
        self._open_m = float(cfg.get("open_m", 0.045))
        self._closed_m = float(cfg.get("closed_m", 0.0))
        self._close_s = float(cfg.get("close_seconds", 1.2))
        self._open_s = float(cfg.get("open_seconds", 0.8))
        self._gap_m = float(cfg.get("holding_gap_m", 0.004))
        self._timeout_s = float(cfg.get("timeout_s", 5.0))

        self._torque_enabled = bool(cfg.get("torque_monitor", True))
        self._torque_delta = float(cfg.get("holding_torque_delta_nm", 0.15))
        self._slip_position = float(cfg.get("slip_position_drop_m", 0.003))
        self._slip_torque = float(cfg.get("slip_torque_drop_nm", 0.10))
        self._sample_s = float(cfg.get("sample_s", 0.35))

        self._group = ReentrantCallbackGroup()
        self._client = ActionClient(
            node, FollowJointTrajectory, self._action_name, callback_group=self._group
        )
        self._history: deque[tuple[float, float, float | None]] = deque(maxlen=400)
        self._baseline: float | None = None
        self._lock = threading.Lock()
        self._sub = node.create_subscription(
            JointState, "/joint_states", self._on_state, 20, callback_group=self._group
        )
        if not self._client.wait_for_server(timeout_sec=3.0):
            node.get_logger().warn(
                f"{self._action_name} not available yet; gripper moves will fail until it is"
            )

    # ------------------------------------------------------------------ state
    def _on_state(self, msg: Any) -> None:
        try:
            index = list(msg.name).index(self._joint)
        except ValueError:
            return
        if index >= len(msg.position):
            return
        position = float(msg.position[index])
        torque: float | None = None
        if self._torque_enabled and index < len(msg.effort):
            value = float(msg.effort[index])
            # Mock hardware reports exact zeros: that is "no telemetry", not "no force".
            if math.isfinite(value) and abs(value) > 1e-6:
                torque = value
        with self._lock:
            self._history.append((time.monotonic(), position, torque))

    def _window(self, duration_s: float) -> list[tuple[float, float | None]]:
        cutoff = time.monotonic() - max(duration_s, 0.05)
        with self._lock:
            samples = [(p, t) for ts, p, t in self._history if ts >= cutoff]
        return samples

    def _median(self, duration_s: float | None = None) -> tuple[float | None, float | None]:
        samples = self._window(duration_s if duration_s is not None else 0.5)
        if not samples:
            return None, None
        positions = [p for p, _ in samples]
        torques = [t for _, t in samples if t is not None]
        position = statistics.median(positions) if positions else None
        torque = statistics.median(torques) if torques else None
        return position, torque

    def position(self, max_age_s: float = 2.0) -> float | None:
        position, _ = self._median(max_age_s)
        return position

    def torque(self, max_age_s: float = 2.0) -> float | None:
        _, torque = self._median(max_age_s)
        return torque

    @property
    def baseline_torque(self) -> float:
        return float(self._baseline or 0.0)

    @property
    def torque_available(self) -> bool:
        return self.torque() is not None

    @property
    def is_open(self) -> bool:
        value = self.position()
        return value is not None and value > 0.5 * self._open_m

    # ------------------------------------------------------------------ commands
    def open(self, plan_only: bool = False) -> dict[str, Any]:
        result = self.command(self._open_m, self._open_s, label="gripper_open",
                              plan_only=plan_only)
        if plan_only:
            return result
        time.sleep(min(self._sample_s, 0.3))
        position, torque = self._median(self._sample_s)
        if torque is not None:
            self._baseline = torque
        result.update(position=_round(position), torque=_round(torque),
                      baseline_torque=_round(self._baseline))
        return result

    def close(self, plan_only: bool = False) -> dict[str, Any]:
        """Close to ``closed_m``, then measure whether the jaw ended up on an object."""
        if not plan_only and self._baseline is None:
            # No open() this session: take the free-air reading now, before pushing.
            _, torque = self._median(0.4)
            self._baseline = torque
        result = self.command(self._closed_m, self._close_s, label="gripper_close",
                              plan_only=plan_only)
        if plan_only:
            result["holding"] = True
            return result

        time.sleep(self._sample_s)
        position, torque = self._median(self._sample_s)
        holding = judge_holding(position, self._closed_m, torque, self.baseline_torque,
                                self._gap_m, self._torque_delta)
        result.update(
            holding=holding,
            position=_round(position),
            torque=_round(torque),
            baseline_torque=_round(self._baseline),
            gap_m=_round(None if position is None else position - self._closed_m),
            torque_delta=_round(None if torque is None else torque - self.baseline_torque),
            blocked=bool(result.get("blocked", False)),
        )
        if torque is None:
            result["note"] = "no torque telemetry; holding is decided by finger position alone"
        elif position is None:
            result["note"] = "no /joint_states position for finger_left; cannot confirm a grasp"
        return result

    def check_hold(self, reference: dict[str, Any], sample_s: float | None = None) -> dict[str, Any]:
        """Re-measure the grasp after a lift and report a slip in either signal."""
        duration = self._sample_s if sample_s is None else sample_s
        time.sleep(min(duration, 0.4))
        position, torque = self._median(duration)
        slipped = judge_slip(position, torque, reference, self._slip_position, self._slip_torque)
        return {
            "holding": not slipped and judge_holding(
                position, self._closed_m, torque, self.baseline_torque,
                self._gap_m * 0.5, self._torque_delta * 0.5,
            ),
            "slipped": slipped,
            "position": _round(position),
            "torque": _round(torque),
            "reference_position": reference.get("position"),
            "reference_torque": reference.get("torque"),
            "torque_available": torque is not None,
        }

    def command(self, target_m: float, seconds: float, label: str = "gripper",
                plan_only: bool = False) -> dict[str, Any]:
        from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

        target = max(0.0, float(target_m))
        if plan_only:
            return {"label": label, "target_m": round(target, 4), "executed": False}

        if not self._client.wait_for_server(timeout_sec=self._timeout_s):
            raise GripperError(f"{self._action_name} is not available")

        trajectory = JointTrajectory(joint_names=[self._joint])
        point = JointTrajectoryPoint()
        point.positions = [target]
        point.velocities = [0.0]
        point.time_from_start.sec = int(seconds)
        point.time_from_start.nanosec = int((seconds % 1.0) * 1e9)
        trajectory.points = [point]

        goal = self._Action.Goal()
        goal.trajectory = trajectory

        started = time.monotonic()
        accepted = threading.Event()
        send_future = self._client.send_goal_async(goal)
        send_future.add_done_callback(lambda _: accepted.set())
        if not accepted.wait(timeout=self._timeout_s + 2.0):
            raise GripperError(f"{label}: gripper action server did not answer")
        handle = send_future.result()
        if handle is None or not handle.accepted:
            raise GripperError(f"{label}: gripper goal rejected (is the controller active?)")

        done = threading.Event()
        result_future = handle.get_result_async()
        result_future.add_done_callback(lambda _: done.set())
        if not done.wait(timeout=max(self._timeout_s, seconds + 3.0)):
            handle.cancel_goal_async()
            raise GripperError(f"{label}: gripper motion timed out")

        wrapped = result_future.result()
        code = int(getattr(wrapped.result, "error_code", 0)) if wrapped is not None else -1
        blocked = False
        if code != 0:
            # A JTC reports a blocked close as a path/goal tolerance violation. That is
            # not a fault: it is the object. The real bridge does not report it at all.
            blocked = label == "gripper_close" and code in (-4, -5)
            if not blocked:
                text = str(getattr(wrapped.result, "error_string", "") or "").strip()
                raise GripperError(f"{label}: gripper error {code}" + (f" ({text})" if text else ""))

        return {
            "label": label,
            "target_m": round(target, 4),
            "duration_s": round(time.monotonic() - started, 3),
            "executed": True,
            "blocked": blocked,
        }


def _round(value: float | None, digits: int = 4) -> float | None:
    return None if value is None else round(float(value), digits)
