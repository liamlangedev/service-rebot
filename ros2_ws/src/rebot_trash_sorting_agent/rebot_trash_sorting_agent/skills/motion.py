"""MoveIt point-to-point motion.

Everything the arm does goes through ``moveit_msgs/action/MoveGroup`` on
``/move_action``: one goal, plan and execute, collision-checked by MoveIt. Pose
goals are exact (position + orientation constraint on ``gripper_tcp``); joint goals
are used for the named poses and as a fallback when an exact pose is hard to plan.

The action client is non-blocking towards ROS: it waits on threading events so the
node's executor keeps spinning while a motion runs.
"""

from __future__ import annotations

import threading
import time
from typing import Any, Sequence

from ..skills.poses import ToolPose


class MotionError(RuntimeError):
    """A motion could not be planned or executed."""


class MoveItClient:
    def __init__(self, node: Any, cfg: dict[str, Any]) -> None:
        from moveit_msgs.action import MoveGroup
        from moveit_msgs.srv import GetPositionIK
        from rclpy.action import ActionClient
        from rclpy.callback_groups import ReentrantCallbackGroup

        self._node = node
        self._Action = MoveGroup
        self._cfg = dict(cfg)
        self._group = str(cfg.get("group", "arm"))
        self._tip = str(cfg.get("tip_link", "gripper_tcp"))
        self._frame = str(cfg.get("base_frame", "base_link"))
        self._action_name = str(cfg.get("action", "/move_action"))
        self._velocity = float(cfg.get("velocity_scaling", 0.15))
        self._acceleration = float(cfg.get("acceleration_scaling", 0.15))
        self._attempts = int(cfg.get("num_planning_attempts", 8))
        self._planning_time = float(cfg.get("allowed_planning_time", 5.0))
        self._planner_id = str(cfg.get("planner_id", "") or "")
        self._tolerance = float(cfg.get("joint_tolerance", 0.02))
        self._named = {str(k): [float(v) for v in q] for k, q in (cfg.get("named_poses") or {}).items()}

        self._group_cb = ReentrantCallbackGroup()
        self._client = ActionClient(node, MoveGroup, self._action_name, callback_group=self._group_cb)
        self._ik_client = node.create_client(GetPositionIK, "/compute_ik", callback_group=self._group_cb)
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

    def move_named(self, name: str, plan_only: bool = False) -> dict[str, Any]:
        return self.move_to_joints(self.named_pose(name), plan_only=plan_only, label=name)

    def move_to_joints(self, positions: Sequence[float], plan_only: bool = False,
                       label: str = "joints") -> dict[str, Any]:
        from moveit_msgs.msg import Constraints, JointConstraint

        if len(positions) != 6:
            raise MotionError(f"expected 6 joint values, got {len(positions)}")
        goal = self._goal(plan_only)
        constraints = Constraints()
        for index, value in enumerate(positions, start=1):
            constraints.joint_constraints.append(
                JointConstraint(
                    joint_name=f"joint{index}",
                    position=float(value),
                    tolerance_above=self._tolerance,
                    tolerance_below=self._tolerance,
                    weight=1.0,
                )
            )
        goal.request.goal_constraints = [constraints]
        result = self._send(goal, label=label, plan_only=plan_only)
        result["joints"] = [round(float(v), 4) for v in positions]
        return result

    def move_to_pose(self, pose: ToolPose, plan_only: bool = False,
                     label: str = "pose") -> dict[str, Any]:
        goal = self._goal(plan_only)
        goal.request.goal_constraints = [self._pose_constraints(pose)]
        result = self._send(goal, label=label, plan_only=plan_only)
        result["pose"] = pose.summary()
        return result

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

    def _goal(self, plan_only: bool):
        goal = self._Action.Goal()
        request = goal.request
        request.group_name = self._group
        request.num_planning_attempts = self._attempts
        request.allowed_planning_time = self._planning_time
        request.max_velocity_scaling_factor = self._velocity
        request.max_acceleration_scaling_factor = self._acceleration
        if self._planner_id:
            request.planner_id = self._planner_id
        goal.planning_options.plan_only = bool(plan_only or not self._cfg.get("execute", True))
        goal.planning_options.look_around = False
        goal.planning_options.replan = False
        return goal

    def _pose_constraints(self, pose: ToolPose):
        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import (BoundingVolume, Constraints, OrientationConstraint,
                                     PositionConstraint)
        from shape_msgs.msg import SolidPrimitive

        header = self._node.get_clock().now().to_msg()
        message = Pose()
        message.position.x, message.position.y, message.position.z = pose.x, pose.y, pose.z
        (message.orientation.x, message.orientation.y,
         message.orientation.z, message.orientation.w) = pose.quaternion()

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

    def _send(self, goal, label: str, plan_only: bool) -> dict[str, Any]:
        from moveit_msgs.msg import MoveItErrorCodes

        self._cancel.clear()
        if not self._client.wait_for_server(timeout_sec=2.0):
            raise MotionError(f"{self._action_name} is not available (is move_group running?)")

        started = time.monotonic()
        accepted = threading.Event()
        send_future = self._client.send_goal_async(goal)
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
        while not done.wait(timeout=0.1):
            if self._cancel.is_set() and not cancelled:
                handle.cancel_goal_async()
                cancelled = True
            if time.monotonic() - started > 120.0:
                handle.cancel_goal_async()
                raise MotionError(f"{label}: motion did not finish within 120 s")
        self._goal_handle = None

        wrapped = result_future.result()
        code = int(wrapped.result.error_code.val) if wrapped is not None else -1
        elapsed = round(time.monotonic() - started, 3)
        if code != MoveItErrorCodes.SUCCESS:
            raise MotionError(f"{label}: MoveIt error code {code} ({_error_name(code)})")
        return {
            "label": label,
            "planned": bool(goal.planning_options.plan_only),
            "duration_s": elapsed,
            "executed": not goal.planning_options.plan_only,
            "planning_time_s": round(float(wrapped.result.planning_time), 3),
        }


def _to_msg_pose(pose: ToolPose):
    from geometry_msgs.msg import Pose

    message = Pose()
    message.position.x, message.position.y, message.position.z = pose.x, pose.y, pose.z
    (message.orientation.x, message.orientation.y,
     message.orientation.z, message.orientation.w) = pose.quaternion()
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
