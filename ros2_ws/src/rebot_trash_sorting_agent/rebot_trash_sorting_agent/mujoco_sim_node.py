#!/usr/bin/env python3
"""MuJoCo simulation bridge for ``rebot_trash_sorting_agent``.

Runs ``rebot_sim.RealSetupEnv`` in a dedicated physics/render thread and exposes
the exact ROS 2 interface that MoveIt and the agent expect from the arm and
cameras:

* ``/joint_states`` (``sensor_msgs/JointState``) with real simulated gripper
  position and actuator effort so ``GripperClient``'s position + torque checks
  work identically to hardware.
* ``/rebotarm_controller/follow_joint_trajectory`` (``FollowJointTrajectory``)
* ``/gripper_controller/follow_joint_trajectory`` (``FollowJointTrajectory``)
* ``/table_cam/image_raw`` + ``camera_info`` (from ``cam_corner``)
* ``/wrist_cam/image_raw`` + ``camera_info`` (from ``wrist``)
"""

from __future__ import annotations

import math
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
import threading
import time
from pathlib import Path
from typing import Any

import numpy as np
import rclpy
from control_msgs.action import FollowJointTrajectory
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo, Image, JointState

ARM_JOINTS = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
ALL_JOINTS = [*ARM_JOINTS, "finger_left", "finger_right", "gripper_joint1", "gripper_joint2"]
READY_QPOS = np.array([0.0, -1.51, -1.30, 1.36, 0.0, 0.0], dtype=float)
READY_GRIPPER = 0.025


def _find_repo_root() -> Path:
    env_root = os.environ.get("REBOT_REPO_ROOT", "").strip()
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if (p / "simulation" / "rebot_sim").is_dir():
            return p
    here = Path(__file__).resolve()
    for parent in (here, *here.parents):
        if (parent / "simulation" / "rebot_sim").is_dir():
            return parent
    cwd = Path.cwd().resolve()
    for parent in (cwd, *cwd.parents):
        if (parent / "simulation" / "rebot_sim").is_dir():
            return parent
    raise RuntimeError(
        "Could not locate simulation/rebot_sim; set REBOT_REPO_ROOT to the repo root"
    )


def _camera_info(frame_id: str, width: int, height: int, fovy_deg: float) -> CameraInfo:
    info = CameraInfo()
    info.header.frame_id = frame_id
    info.width = width
    info.height = height
    fy = (height / 2.0) / max(math.tan(math.radians(fovy_deg) / 2.0), 1e-6)
    fx = fy
    cx = width / 2.0
    cy = height / 2.0
    info.k = [fx, 0.0, cx, 0.0, fy, cy, 0.0, 0.0, 1.0]
    info.p = [fx, 0.0, cx, 0.0, 0.0, fy, cy, 0.0, 0.0, 0.0, 1.0, 0.0]
    info.distortion_model = "plumb_bob"
    info.d = [0.0, 0.0, 0.0, 0.0, 0.0]
    return info


def _duration_to_sec(dur: Any) -> float:
    return float(dur.sec) + float(dur.nanosec) * 1e-9


def _interpolate_trajectory(points: list[Any], names: list[str], t: float) -> np.ndarray:
    """Linearly interpolate a JointTrajectory at elapsed time ``t`` [s]."""
    if not points:
        return np.zeros(len(names), dtype=float)
    if len(points) == 1 or t <= _duration_to_sec(points[0].time_from_start):
        return np.array(points[0].positions[: len(names)], dtype=float)
    for i in range(1, len(points)):
        t1 = _duration_to_sec(points[i].time_from_start)
        if t <= t1:
            t0 = _duration_to_sec(points[i - 1].time_from_start)
            p0 = np.array(points[i - 1].positions[: len(names)], dtype=float)
            p1 = np.array(points[i].positions[: len(names)], dtype=float)
            alpha = (t - t0) / max(t1 - t0, 1e-6)
            return p0 + np.clip(alpha, 0.0, 1.0) * (p1 - p0)
    return np.array(points[-1].positions[: len(names)], dtype=float)


class MujocoSimNode(Node):
    def __init__(self) -> None:
        super().__init__("mujoco_sim_node")
        self.declare_parameter("randomize", False)
        self.declare_parameter("seed", 0)
        self.declare_parameter("fps", 30.0)
        self.declare_parameter("show_viewer", False)
        self.declare_parameter("web_view", True)
        self.declare_parameter("web_view_port", 8765)
        self.declare_parameter("table_camera_name", "cam_corner")
        self.declare_parameter("wrist_camera_name", "wrist")
        self.declare_parameter("sim_camera_name", "front")
        self.declare_parameter("table_topic", "/table_cam")
        self.declare_parameter("wrist_topic", "/wrist_cam")
        self.declare_parameter("sim_topic", "/sim_view")
        self.declare_parameter("width", 640)
        self.declare_parameter("height", 480)

        self._randomize = bool(self.get_parameter("randomize").value)
        self._seed = int(self.get_parameter("seed").value)
        self._fps = max(1.0, float(self.get_parameter("fps").value))
        self._show_viewer = bool(self.get_parameter("show_viewer").value)
        self._web_view = bool(self.get_parameter("web_view").value)
        self._web_view_port = int(self.get_parameter("web_view_port").value)
        self._table_cam = str(self.get_parameter("table_camera_name").value)
        self._wrist_cam = str(self.get_parameter("wrist_camera_name").value)
        self._sim_cam = str(self.get_parameter("sim_camera_name").value)
        self._width = int(self.get_parameter("width").value)
        self._height = int(self.get_parameter("height").value)

        table_base = str(self.get_parameter("table_topic").value).rstrip("/")
        wrist_base = str(self.get_parameter("wrist_topic").value).rstrip("/")
        sim_base = str(self.get_parameter("sim_topic").value).rstrip("/")

        self._cb = ReentrantCallbackGroup()

        self._joint_pub = self.create_publisher(JointState, "/joint_states", 20)
        self._table_pub = self.create_publisher(Image, f"{table_base}/image_raw", 10)
        self._table_info_pub = self.create_publisher(CameraInfo, f"{table_base}/camera_info", 10)
        self._wrist_pub = self.create_publisher(Image, f"{wrist_base}/image_raw", 10)
        self._wrist_info_pub = self.create_publisher(CameraInfo, f"{wrist_base}/camera_info", 10)
        self._sim_pub = self.create_publisher(Image, f"{sim_base}/image_raw", 10)
        self._sim_info_pub = self.create_publisher(CameraInfo, f"{sim_base}/camera_info", 10)

        self._state_lock = threading.Lock()
        self._arm_target = READY_QPOS.copy()
        self._grip_target = READY_GRIPPER
        self._latest_q_arm = READY_QPOS.copy()
        self._latest_grip = READY_GRIPPER
        self._latest_grip_effort = 0.0
        self._table_info: CameraInfo | None = None
        self._wrist_info: CameraInfo | None = None
        self._sim_info: CameraInfo | None = None

        self._ready_event = threading.Event()
        self._init_error: Exception | None = None
        self._stop_event = threading.Event()
        self._sim_thread = threading.Thread(
            target=self._sim_loop, name="mujoco_sim", daemon=True
        )
        self._sim_thread.start()
        self._ready_event.wait(timeout=15.0)
        if self._init_error is not None:
            raise self._init_error

        self._arm_server = ActionServer(
            self,
            FollowJointTrajectory,
            "/rebotarm_controller/follow_joint_trajectory",
            execute_callback=self._execute_arm,
            goal_callback=self._accept_goal,
            cancel_callback=self._accept_cancel,
            callback_group=self._cb,
        )
        self._grip_server = ActionServer(
            self,
            FollowJointTrajectory,
            "/gripper_controller/follow_joint_trajectory",
            execute_callback=self._execute_gripper,
            goal_callback=self._accept_goal,
            cancel_callback=self._accept_cancel,
            callback_group=self._cb,
        )
        self._js_timer = self.create_timer(0.02, self._publish_joint_states, callback_group=self._cb)
        self.get_logger().info(
            f"MuJoCo sim ready (table={self._table_cam}, wrist={self._wrist_cam}, "
            f"randomize={self._randomize})"
        )

    # ------------------------------------------------------------------ sim thread
    def _sim_loop(self) -> None:
        env = None
        try:
            repo_root = _find_repo_root()
            for sub in ("simulation", "teleoperation"):
                path = str(repo_root / sub)
                if path not in sys.path:
                    sys.path.insert(0, path)
            from rebot_sim import RealSetupEnv

            env = RealSetupEnv(control_hz=100)
            env.reset(
                q_arm=READY_QPOS,
                gripper=READY_GRIPPER,
                randomize=self._randomize,
                seed=self._seed,
            )
            table_fovy = float(env.model.camera(self._table_cam).fovy[0])
            wrist_fovy = float(env.model.camera(self._wrist_cam).fovy[0])
            sim_fovy = float(env.model.camera(self._sim_cam).fovy[0])
            self._table_info = _camera_info(
                "table_cam_optical_frame", self._width, self._height, table_fovy
            )
            self._wrist_info = _camera_info(
                "wrist_cam_optical_frame", self._width, self._height, wrist_fovy
            )
            self._sim_info = _camera_info(
                "sim_view_optical_frame", self._width, self._height, sim_fovy
            )
            vr = None
            if self._web_view:
                try:
                    from teleop.vr_view import VRBridge

                    vr = VRBridge(env.model, port=self._web_view_port)
                    vr.start()
                    self.get_logger().info(
                        f"interactive 3D web view on http://127.0.0.1:{self._web_view_port}/"
                    )
                except Exception as exc:  # noqa: BLE001
                    self.get_logger().warn(f"3D web view unavailable: {exc}")
                    vr = None
            viewer = None
            if self._show_viewer and os.environ.get("DISPLAY"):
                try:
                    import mujoco.viewer

                    viewer = mujoco.viewer.launch_passive(env.model, env.data)
                    viewer.cam.azimuth = 135.0
                    viewer.cam.elevation = -28.0
                    viewer.cam.distance = 1.45
                    viewer.cam.lookat[:] = [0.28, 0.12, 0.12]
                except Exception as exc:  # noqa: BLE001
                    self.get_logger().warn(f"MuJoCo viewer unavailable: {exc}")
                    viewer = None
            self._ready_event.set()
        except Exception as exc:  # noqa: BLE001
            self._init_error = exc
            self._ready_event.set()
            return

        dt = env.control_dt
        render_period = 1.0 / self._fps
        next_render = time.monotonic()

        try:
            while not self._stop_event.is_set():
                t0 = time.monotonic()
                with self._state_lock:
                    q_cmd = self._arm_target.copy()
                    g_cmd = float(self._grip_target)

                env.step(q_arm=q_cmd, gripper=g_cmd)
                q_meas = env.q_arm
                g_meas = env.gripper
                g_effort = float(env.data.actuator_force[env.grip_act])

                with self._state_lock:
                    self._latest_q_arm = q_meas
                    self._latest_grip = g_meas
                    self._latest_grip_effort = g_effort

                now = time.monotonic()
                if vr is not None:
                    vr.publish(env.data)
                if now >= next_render:
                    next_render = now + render_period
                    self._render_and_publish(env)
                    if viewer is not None and viewer.is_running():
                        viewer.sync()

                sleep_s = dt - (time.monotonic() - t0)
                if sleep_s > 0:
                    time.sleep(sleep_s)
        finally:
            if vr is not None:
                try:
                    vr.close()
                except Exception:  # noqa: BLE001
                    pass
            if viewer is not None:
                try:
                    viewer.close()
                except Exception:  # noqa: BLE001
                    pass
            if env is not None:
                env.close()

    def _render_and_publish(self, env: Any) -> None:
        stamp = self.get_clock().now().to_msg()
        for cam_name, img_pub, info_pub, info in (
            (self._table_cam, self._table_pub, self._table_info_pub, self._table_info),
            (self._wrist_cam, self._wrist_pub, self._wrist_info_pub, self._wrist_info),
            (self._sim_cam, self._sim_pub, self._sim_info_pub, self._sim_info),
        ):
            rgb = env.render(cam_name, width=self._width, height=self._height)
            bgr = np.ascontiguousarray(rgb[:, :, ::-1])
            msg = Image()
            msg.header.stamp = stamp
            msg.header.frame_id = info.header.frame_id if info else f"{cam_name}_optical_frame"
            msg.height = int(bgr.shape[0])
            msg.width = int(bgr.shape[1])
            msg.encoding = "bgr8"
            msg.is_bigendian = 0
            msg.step = int(bgr.shape[1] * 3)
            msg.data = bgr.tobytes()
            img_pub.publish(msg)
            if info is not None:
                info.header.stamp = stamp
                info_pub.publish(info)

    # ------------------------------------------------------------------ ros
    def _publish_joint_states(self) -> None:
        with self._state_lock:
            q_arm = self._latest_q_arm.copy()
            grip = self._latest_grip
            effort = self._latest_grip_effort
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(ALL_JOINTS)
        msg.position = [*q_arm.tolist(), grip, -grip, 0.0, 0.0]
        msg.effort = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, effort, 0.0, 0.0, 0.0]
        self._joint_pub.publish(msg)

    def _accept_goal(self, _goal_request: Any) -> GoalResponse:
        return GoalResponse.ACCEPT

    def _accept_cancel(self, _goal_handle: Any) -> CancelResponse:
        return CancelResponse.ACCEPT

    def _execute_arm(self, goal_handle: Any) -> FollowJointTrajectory.Result:
        traj = goal_handle.request.trajectory
        joint_names = list(traj.joint_names)
        points = list(traj.points)
        result = FollowJointTrajectory.Result()
        if not points:
            goal_handle.succeed()
            return result

        index_map = [joint_names.index(j) if j in joint_names else -1 for j in ARM_JOINTS]
        total_s = _duration_to_sec(points[-1].time_from_start)
        started = time.monotonic()

        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result
            elapsed = time.monotonic() - started
            pos = _interpolate_trajectory(points, joint_names, elapsed)
            with self._state_lock:
                cmd = self._arm_target.copy()
                for arm_i, traj_i in enumerate(index_map):
                    if traj_i >= 0 and traj_i < len(pos):
                        cmd[arm_i] = float(pos[traj_i])
                self._arm_target = cmd
            if elapsed >= total_s:
                break
            time.sleep(0.01)

        # Let the position servo settle briefly.
        time.sleep(0.08)
        goal_handle.succeed()
        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        return result

    def _execute_gripper(self, goal_handle: Any) -> FollowJointTrajectory.Result:
        traj = goal_handle.request.trajectory
        joint_names = list(traj.joint_names)
        points = list(traj.points)
        result = FollowJointTrajectory.Result()
        if not points:
            goal_handle.succeed()
            return result

        grip_idx = joint_names.index("finger_left") if "finger_left" in joint_names else 0
        total_s = _duration_to_sec(points[-1].time_from_start)
        started = time.monotonic()

        while rclpy.ok():
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
                return result
            elapsed = time.monotonic() - started
            pos = _interpolate_trajectory(points, joint_names, elapsed)
            if grip_idx < len(pos):
                with self._state_lock:
                    self._grip_target = float(np.clip(pos[grip_idx], 0.0, 0.05))
            if elapsed >= total_s:
                break
            time.sleep(0.01)

        time.sleep(0.15)
        goal_handle.succeed()
        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        return result

    def destroy_node(self) -> bool:
        self._stop_event.set()
        if self._sim_thread.is_alive():
            self._sim_thread.join(timeout=2.0)
        return super().destroy_node()


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = MujocoSimNode()
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
