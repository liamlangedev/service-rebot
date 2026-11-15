#!/usr/bin/env python3
"""Bridges MoveIt's finger_left FollowJointTrajectory [0..0.05 m] to /rebotarm/gripper/command [rad]."""

from __future__ import annotations

from pathlib import Path
import threading
import time

from ament_index_python.packages import PackageNotFoundError, get_package_share_directory
from control_msgs.action import FollowJointTrajectory, GripperCommand
import rclpy
from rclpy.action import ActionClient, ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
import yaml

_MAX_FINGER_LEFT_M = 0.05


def _load_default_dm_gripper_limits() -> tuple[float, float]:
    try:
        cfg_path = (
            Path(get_package_share_directory("rebotarm_bringup"))
            / "config"
            / "rebotarm_hardware.yaml"
        )
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        limits = (
            data.get("models", {})
            .get("dm", {})
            .get("overrides", {})
            .get("gripper", {})
            .get("position_limits", {})
        )
        return float(limits.get("open", -5.0)), float(limits.get("close", 0.0))
    except (PackageNotFoundError, OSError, ValueError, TypeError):
        return -5.0, 0.0


class HardwareGripperBridgeNode(Node):
    def __init__(self) -> None:
        super().__init__("hardware_gripper_bridge")
        default_open, default_close = _load_default_dm_gripper_limits()

        self.declare_parameter("arm_namespace", "rebotarm")
        self.declare_parameter("gripper_open_rad", default_open)
        self.declare_parameter("gripper_closed_rad", default_close)
        self.declare_parameter("max_effort", 1.5)

        ns = str(self.get_parameter("arm_namespace").value).strip("/") or "rebotarm"
        self._cb_group = ReentrantCallbackGroup()

        self._gripper_client = ActionClient(
            self,
            GripperCommand,
            f"/{ns}/gripper/command",
            callback_group=self._cb_group,
        )
        self._trajectory_server = ActionServer(
            self,
            FollowJointTrajectory,
            "/gripper_controller/follow_joint_trajectory",
            execute_callback=self._execute_callback,
            goal_callback=self._goal_callback,
            cancel_callback=self._cancel_callback,
            callback_group=self._cb_group,
        )
        self.get_logger().info(
            f"Bridging /gripper_controller/follow_joint_trajectory [0..{_MAX_FINGER_LEFT_M} m] "
            f"-> /{ns}/gripper/command [{default_close:.2f}..{default_open:.2f} rad]"
        )

    def _goal_callback(self, goal_request: FollowJointTrajectory.Goal) -> GoalResponse:
        if "finger_left" not in goal_request.trajectory.joint_names:
            self.get_logger().warn("Rejecting gripper trajectory without 'finger_left'")
            return GoalResponse.REJECT
        if not goal_request.trajectory.points:
            self.get_logger().warn("Rejecting empty gripper trajectory")
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def _cancel_callback(self, _goal_handle) -> CancelResponse:
        return CancelResponse.ACCEPT

    def _finger_m_to_motor_rad(self, finger_m: float) -> float:
        open_rad = float(self.get_parameter("gripper_open_rad").value)
        close_rad = float(self.get_parameter("gripper_closed_rad").value)
        ratio = max(0.0, min(1.0, float(finger_m) / _MAX_FINGER_LEFT_M))
        return close_rad + ratio * (open_rad - close_rad)

    def _send_gripper_goal(self, target_rad: float, max_effort: float):
        cmd_goal = GripperCommand.Goal()
        cmd_goal.command.position = target_rad
        cmd_goal.command.max_effort = max_effort

        accepted_event = threading.Event()
        send_future = self._gripper_client.send_goal_async(cmd_goal)
        send_future.add_done_callback(lambda _: accepted_event.set())

        if not accepted_event.wait(timeout=2.0):
            return None, FollowJointTrajectory.Result.INVALID_GOAL, "Timed out sending goal to hardware gripper"

        client_goal_handle = send_future.result()
        if client_goal_handle is None or not client_goal_handle.accepted:
            return None, FollowJointTrajectory.Result.INVALID_GOAL, "Hardware gripper rejected goal (is the arm enabled?)"

        return client_goal_handle, FollowJointTrajectory.Result.SUCCESSFUL, ""

    def _execute_callback(self, goal_handle) -> FollowJointTrajectory.Result:
        result = FollowJointTrajectory.Result()
        traj = goal_handle.request.trajectory
        idx = traj.joint_names.index("finger_left")
        max_effort = float(self.get_parameter("max_effort").value)

        if not self._gripper_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("Hardware gripper action server not available")
            goal_handle.abort()
            result.error_code = FollowJointTrajectory.Result.PATH_TOLERANCE_VIOLATED
            result.error_string = "Hardware gripper action server not available"
            return result

        started = time.monotonic()
        client_goal_handle = None
        for point in traj.points:
            pt_time = float(point.time_from_start.sec) + float(point.time_from_start.nanosec) * 1e-9
            while time.monotonic() - started < pt_time:
                if goal_handle.is_cancel_requested:
                    if client_goal_handle is not None:
                        client_goal_handle.cancel_goal_async()
                    goal_handle.canceled()
                    result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                    return result
                time.sleep(min(0.02, max(0.0, pt_time - (time.monotonic() - started))))

            if goal_handle.is_cancel_requested:
                if client_goal_handle is not None:
                    client_goal_handle.cancel_goal_async()
                goal_handle.canceled()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result

            if client_goal_handle is not None:
                client_goal_handle.cancel_goal_async()

            target_rad = self._finger_m_to_motor_rad(float(point.positions[idx]))
            client_goal_handle, err_code, err_str = self._send_gripper_goal(target_rad, max_effort)
            if client_goal_handle is None:
                goal_handle.abort()
                result.error_code = err_code
                result.error_string = err_str
                return result

        done_event = threading.Event()
        result_future = client_goal_handle.get_result_async()
        result_future.add_done_callback(lambda _: done_event.set())

        while not done_event.wait(timeout=0.02):
            if goal_handle.is_cancel_requested:
                client_goal_handle.cancel_goal_async()
                goal_handle.canceled()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result

        goal_handle.succeed()
        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        return result


def main() -> None:
    rclpy.init()
    node = HardwareGripperBridgeNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
