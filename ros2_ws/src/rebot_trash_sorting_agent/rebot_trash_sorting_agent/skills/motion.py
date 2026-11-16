"""MoveIt point-to-point motion.

Everything the arm does goes through ``moveit_msgs/action/MoveGroup`` on
``/move_action``: one goal, plan and execute, collision-checked by MoveIt. Pose
goals are exact (position + orientation constraint on ``gripper_tcp``); joint goals
are used for the named poses and as a fallback when an exact pose is hard to plan.

The action client is non-blocking towards ROS: it waits on threading events so the
node's executor keeps spinning while a motion runs.
"""

from __future__ import annotations

import math
import threading
import time
from collections.abc import Callable, Sequence
from typing import Any

from rebot_trash_sorting_agent.skills.poses import ToolPose


class MotionError(RuntimeError):
    """A motion could not be planned or executed."""


class MoveItClient:
    def __init__(self, node: Any, cfg: dict[str, Any]) -> None:
        from moveit_msgs.action import ExecuteTrajectory, MoveGroup
        from moveit_msgs.srv import GetCartesianPath, GetPositionIK
        from rclpy.action import ActionClient
        from rclpy.callback_groups import ReentrantCallbackGroup

        self._node = node
        self._Action = MoveGroup
        self._cfg = {**cfg, **dict(cfg.get("move_group") or {})}
        cfg = self._cfg
        self._group = str(cfg.get("group", "arm"))
        self._tip = str(cfg.get("tip_link", "gripper_tcp"))
        self._frame = str(cfg.get("base_frame", "base_link"))
        self._action_name = str(cfg.get("action", "/move_action"))
        self._velocity = _scaling(cfg.get("velocity_scaling", 0.15))
        self._acceleration = _scaling(cfg.get("acceleration_scaling", 0.15))
        self._speed_profiles = {"default": (self._velocity, self._acceleration)}
        for name, profile in (cfg.get("speed_profiles") or {}).items():
            if name == "default":
                raise ValueError("set default speed with velocity_scaling and acceleration_scaling")
            self._speed_profiles[str(name)] = (
                _scaling(profile.get("velocity_scaling", self._velocity)),
                _scaling(profile.get("acceleration_scaling", self._acceleration)),
            )
        self._speed_profiles.setdefault("travel", self._speed_profiles["default"])
        self._attempts = int(cfg.get("num_planning_attempts", 8))
        self._planning_time = float(cfg.get("allowed_planning_time", 5.0))
        self._planner_id = str(cfg.get("planner_id", "") or "")
        self._tolerance = float(cfg.get("joint_tolerance", 0.02))
        self._named = {str(k): [float(v) for v in q] for k, q in (cfg.get("named_poses") or {}).items()}

        self._group_cb = ReentrantCallbackGroup()
        self._client = ActionClient(node, MoveGroup, self._action_name, callback_group=self._group_cb)
        self._ik_client = node.create_client(GetPositionIK, "/compute_ik", callback_group=self._group_cb)
        self._cartesian_client = node.create_client(
            GetCartesianPath, "/compute_cartesian_path", callback_group=self._group_cb
        )
        self._execute_client = ActionClient(
            node, ExecuteTrajectory, "/execute_trajectory", callback_group=self._group_cb
        )
        self._goal_handle = None
        self._cancel = threading.Event()

        if not self._client.wait_for_server(timeout_sec=5.0):
            node.get_logger().warn(f"{self._action_name} not available yet; motion will fail until it is")

    # ------------------------------------------------------------------ public api
    @property
    def tip_link(self) -> str:
        return self._tip

    def named_pose(self, name: str) -> list[float]:
        if name not in self._named:
            raise MotionError(f"no named pose {name!r} in motion.yaml (have {sorted(self._named)})")
        return list(self._named[name])

    def cancel(self) -> None:
        """Ask the running goal to stop; safe to call from the service thread."""
        self._cancel.set()
        handle = self._goal_handle
        if handle is not None:
            handle.cancel_goal_async()

    def move_named(
        self,
        name: str,
        plan_only: bool = False,
        *,
        speed_profile: str = "default",
        guard: Callable[[], None] | None = None,
    ) -> dict[str, Any]:
        return self.move_to_joints(
            self.named_pose(name), plan_only=plan_only, label=name, speed_profile=speed_profile, guard=guard
        )

    def move_to_joints(
        self,
        positions: Sequence[float],
        plan_only: bool = False,
        label: str = "joints",
        *,
        speed_profile: str = "default",
        guard: Callable[[], None] | None = None,
    ) -> dict[str, Any]:
        from moveit_msgs.msg import Constraints, JointConstraint

        if len(positions) != 6:
            raise MotionError(f"expected 6 joint values, got {len(positions)}")
        goal = self._goal(plan_only, speed_profile)
        constraints = Constraints()
        for index, value in enumerate(positions, start=1):
            constraints.joint_constraints.append(
                JointConstraint(
                    joint_name=f"joint{index}",
                    position=float(value),
                    tolerance_above=self._tolerance,
                    tolerance_below=self._tolerance,
                    weight=1.0,
                ),
            )
        goal.request.goal_constraints = [constraints]
        result = self._send(goal, label=label, plan_only=plan_only, guard=guard)
        result["joints"] = [round(float(v), 4) for v in positions]
        return result

    def move_to_pose(
        self,
        pose: ToolPose,
        plan_only: bool = False,
        label: str = "pose",
        *,
        speed_profile: str = "default",
        guard: Callable[[], None] | None = None,
    ) -> dict[str, Any]:
        goal = self._goal(plan_only, speed_profile)
        goal.request.goal_constraints = [self._pose_constraints(pose)]
        result = self._send(goal, label=label, plan_only=plan_only, guard=guard)
        result["pose"] = pose.summary()
        return result

    def move_cartesian(
        self, pose: ToolPose, plan_only: bool = False, label: str = "cartesian", guard: Callable[[], None] | None = None
    ) -> dict[str, Any]:
        """Plan a complete, orientation-constrained linear path from the current state."""
        from moveit_msgs.action import ExecuteTrajectory
        from moveit_msgs.srv import GetCartesianPath

        cfg = dict(self._cfg.get("cartesian") or {})
        request = GetCartesianPath.Request()
        request.header.frame_id = self._frame
        request.header.stamp = self._node.get_clock().now().to_msg()
        request.start_state.is_diff = True
        request.group_name, request.link_name = self._group, self._tip
        request.waypoints = [_to_msg_pose(pose)]
        request.max_step = float(cfg.get("max_step_m", 0.005))
        max_jump = float(cfg.get("max_joint_step_rad", 0.25))
        if not 0 < request.max_step <= 0.02 or not 0 < max_jump <= 0.5:
            raise MotionError("invalid Cartesian step or joint jump limit")
        request.revolute_jump_threshold = max_jump
        request.prismatic_jump_threshold = 0.01
        request.avoid_collisions = True
        request.path_constraints.orientation_constraints = self._pose_constraints(pose).orientation_constraints
        request.max_velocity_scaling_factor = self._velocity
        request.max_acceleration_scaling_factor = self._acceleration
        request.cartesian_speed_limited_link = self._tip
        request.max_cartesian_speed = float(cfg.get("max_speed_mps", 0.025))
        if not 0 < request.max_cartesian_speed <= 0.1:
            raise MotionError("Cartesian speed must be in (0, 0.1] m/s")
        if guard is not None:
            guard()
        response = self._call_service(self._cartesian_client, request)
        _validate_cartesian(response, max_jump)
        planned = bool(plan_only or not self._cfg.get("execute", True))
        if not planned:
            goal = ExecuteTrajectory.Goal(trajectory=response.solution)
            self._run_action(self._execute_client, goal, label, guard)
        return {
            "label": label,
            "pose": pose.summary(),
            "planned": planned,
            "executed": not planned,
            "fraction": float(response.fraction),
            "cartesian_speed_mps": request.max_cartesian_speed,
        }

    def _call_service(self, client: Any, request: Any, timeout: float = 10.0) -> Any:
        if not client.wait_for_service(timeout_sec=2.0):
            raise MotionError("required MoveIt service is unavailable")
        done = threading.Event()
        future = client.call_async(request)
        future.add_done_callback(lambda _: done.set())
        if not done.wait(timeout):
            future.cancel()
            raise MotionError("MoveIt service timed out")
        response = future.result()
        if response is None:
            raise MotionError("MoveIt service returned no result")
        return response

    def ik_feasible(self, pose: ToolPose, timeout_s: float = 1.5) -> bool:
        """True if MoveIt's IK can solve this pose (used to screen place spots)."""
        from geometry_msgs.msg import PoseStamped

        if not self._ik_client.service_is_ready() and not self._ik_client.wait_for_service(timeout_sec=1.0):
            return True  # no IK service: do not veto a spot we cannot check
        request = self._ik_request_type().Request()
        request.ik_request.group_name = self._group
        request.ik_request.ik_link_name = self._tip
        stamped = PoseStamped()
        stamped.header.frame_id = self._frame
        stamped.pose = _to_msg_pose(pose)
        request.ik_request.pose_stamped = stamped
        request.ik_request.timeout.sec = int(timeout_s)
        request.ik_request.timeout.nanosec = int((timeout_s % 1.0) * 1e9)
        # Kinematic screening only: the planner does the collision checking. Screening
        # with collision checks on would need a seeded robot state and would reject
        # poses that are perfectly reachable but invalid *from the seed*.
        request.ik_request.avoid_collisions = False

        done = threading.Event()
        future = self._ik_client.call_async(request)
        future.add_done_callback(lambda _: done.set())
        if not done.wait(timeout_s + 5.0):
            return True
        response = future.result()
        return bool(response is not None and response.error_code.val == 1)

    # ------------------------------------------------------------------ internals
    @staticmethod
    def _ik_request_type():
        from moveit_msgs.srv import GetPositionIK

        return GetPositionIK

    def _goal(self, plan_only: bool, speed_profile: str = "default"):
        if speed_profile not in self._speed_profiles:
            raise MotionError(f"unknown speed profile {speed_profile!r}")
        velocity, acceleration = self._speed_profiles[speed_profile]
        goal = self._Action.Goal()
        request = goal.request
        request.group_name = self._group
        request.num_planning_attempts = self._attempts
        request.allowed_planning_time = self._planning_time
        request.max_velocity_scaling_factor = velocity
        request.max_acceleration_scaling_factor = acceleration
        if self._planner_id:
            request.planner_id = self._planner_id
        goal.planning_options.plan_only = bool(plan_only or not self._cfg.get("execute", True))
        goal.planning_options.look_around = False
        goal.planning_options.replan = False
        return goal

    def _pose_constraints(self, pose: ToolPose):
        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import BoundingVolume, Constraints, OrientationConstraint, PositionConstraint
        from shape_msgs.msg import SolidPrimitive

        header = self._node.get_clock().now().to_msg()
        message = Pose()
        message.position.x, message.position.y, message.position.z = pose.x, pose.y, pose.z
        (message.orientation.x, message.orientation.y, message.orientation.z, message.orientation.w) = pose.quaternion()

        primitive = SolidPrimitive(type=SolidPrimitive.SPHERE, dimensions=[0.004])
        region = BoundingVolume(primitives=[primitive], primitive_poses=[message])

        position = PositionConstraint(link_name=self._tip, constraint_region=region, weight=1.0)
        orientation = OrientationConstraint(
            link_name=self._tip,
            orientation=message.orientation,
            absolute_x_axis_tolerance=0.05,
            absolute_y_axis_tolerance=0.05,
            absolute_z_axis_tolerance=0.05,
            weight=1.0,
        )
        for item in (position, orientation):
            item.header.frame_id = self._frame
            item.header.stamp = header
        return Constraints(position_constraints=[position], orientation_constraints=[orientation])

    def _run_action(
        self, client: Any, goal: Any, label: str, guard: Callable[[], None] | None = None
    ) -> tuple[Any, float]:
        self._cancel.clear()
        if not client.wait_for_server(timeout_sec=2.0):
            raise MotionError(f"{label}: MoveIt action server unavailable")
        if guard is not None:
            guard()

        started = time.monotonic()
        accepted = threading.Event()
        send_future = client.send_goal_async(goal)
        send_future.add_done_callback(lambda _: accepted.set())
        if not accepted.wait(timeout=10.0):
            raise MotionError(f"{label}: move_group did not answer within 10 s")
        handle = send_future.result()
        if handle is None or not handle.accepted:
            raise MotionError(f"{label}: goal rejected by move_group")
        self._goal_handle = handle

        done = threading.Event()
        result_future = handle.get_result_async()
        result_future.add_done_callback(lambda _: done.set())
        cancelled = False
        failure: Exception | None = None
        cancel_started = 0.0
        try:
            while not done.wait(timeout=0.05):
                if guard is not None and failure is None:
                    try:
                        guard()
                    except Exception as exc:
                        failure = exc
                if time.monotonic() - started > 120.0 and failure is None:
                    failure = MotionError(f"{label}: execution timed out")
                if (self._cancel.is_set() or failure is not None) and not cancelled:
                    handle.cancel_goal_async()
                    cancelled = True
                    cancel_started = time.monotonic()
                if cancelled and time.monotonic() - cancel_started > 3.0:
                    raise MotionError(
                        f"{label}: cancellation not confirmed; stop the robot and inspect before retry"
                    ) from failure
            if failure is not None:
                raise failure
            if cancelled:
                raise MotionError(f"{label}: motion cancelled")
            wrapped = result_future.result()
            if guard is not None:
                guard()
        finally:
            self._goal_handle = None
        code = int(wrapped.result.error_code.val) if wrapped is not None else -1
        elapsed = round(time.monotonic() - started, 3)
        if code != 1:
            raise MotionError(f"{label}: MoveIt error code {code} ({_error_name(code)})")
        return wrapped.result, elapsed

    def _send(self, goal, label: str, plan_only: bool, guard: Callable[[], None] | None = None) -> dict[str, Any]:
        result, elapsed = self._run_action(self._client, goal, label, guard)
        return {
            "label": label,
            "velocity_scaling": goal.request.max_velocity_scaling_factor,
            "acceleration_scaling": goal.request.max_acceleration_scaling_factor,
            "planned": bool(goal.planning_options.plan_only),
            "duration_s": elapsed,
            "executed": not goal.planning_options.plan_only,
            "planning_time_s": round(float(result.planning_time), 3),
        }


def _validate_cartesian(response: Any, max_jump: float) -> None:
    if response.error_code.val != 1 or not math.isfinite(response.fraction) or response.fraction < 1.0 - 1e-6:
        raise MotionError(f"Cartesian path incomplete (fraction={response.fraction}); refusing execution")
    trajectory = response.solution.joint_trajectory
    points = trajectory.points
    if len(points) < 2 or not trajectory.joint_names:
        raise MotionError("Cartesian path is empty or has no timed motion")
    previous_time = -1.0
    previous_positions = None
    for point in points:
        elapsed = point.time_from_start.sec + point.time_from_start.nanosec * 1e-9
        if elapsed < 0 or elapsed <= previous_time or len(point.positions) != len(trajectory.joint_names):
            raise MotionError("Cartesian trajectory has invalid timing or joint dimensions")
        if not all(math.isfinite(value) for value in (*point.positions, *point.velocities, *point.accelerations)):
            raise MotionError("Cartesian trajectory contains nonfinite values")
        if previous_positions is not None and any(
            abs(new - old) > max_jump for new, old in zip(point.positions, previous_positions)
        ):
            raise MotionError("Cartesian trajectory contains a joint jump")
        previous_time, previous_positions = elapsed, point.positions


def _scaling(value: Any) -> float:
    scale = float(value)
    if not math.isfinite(scale) or not 0.0 < scale <= 1.0:
        raise ValueError("motion speed scaling must be finite and in (0, 1]")
    return scale


def _to_msg_pose(pose: ToolPose):
    from geometry_msgs.msg import Pose

    message = Pose()
    message.position.x, message.position.y, message.position.z = pose.x, pose.y, pose.z
    (message.orientation.x, message.orientation.y, message.orientation.z, message.orientation.w) = pose.quaternion()
    return message


_ERRORS = {
    -1: "FAILURE",
    -2: "PLANNING_FAILED",
    -3: "INVALID_MOTION_PLAN",
    -4: "MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE",
    -5: "CONTROL_FAILED",
    -6: "UNABLE_TO_AQUIRE_SENSOR_DATA",
    -7: "TIMED_OUT",
    -10: "START_STATE_IN_COLLISION",
    -11: "START_STATE_VIOLATES_PATH_CONSTRAINTS",
    -12: "GOAL_IN_COLLISION",
    -13: "GOAL_VIOLATES_PATH_CONSTRAINTS",
    -14: "GOAL_CONSTRAINTS_VIOLATED",
    -15: "INVALID_GROUP_NAME",
    -16: "INVALID_GOAL_CONSTRAINTS",
    -17: "INVALID_ROBOT_STATE",
    -18: "INVALID_LINK_NAME",
    -19: "INVALID_OBJECT_NAME",
    -21: "FRAME_TRANSFORMATION",
    -22: "INVALID_LINK_MODEL_TYPE",
    -23: "UNKNOWN",
    -31: "NO_IK_SOLUTION",
}


def _error_name(code: int) -> str:
    return _ERRORS.get(code, "UNKNOWN")
