#!/usr/bin/env python3
"""Sanity-check node verifying ROS 2, OpenCV/cv_bridge, and reBotArm dependencies."""

from __future__ import annotations

from pathlib import Path
import subprocess
import time

from ament_index_python.packages import PackageNotFoundError, get_package_share_directory
from control_msgs.action import FollowJointTrajectory, GripperCommand as GripperCommandAction
import cv2
from cv_bridge import CvBridge
import numpy as np
import rclpy
from rclpy.node import Node
from rebotarm_msgs.action import MoveToPose
from rebotarm_msgs.msg import ArmStatus, JointMotorState
from rebotarm_msgs.srv import GripperCommand, MoveToPoseIK, SetGripper


def _find_workspace_root() -> Path | None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "third_party" / "reBotArm_control_py").is_dir():
            return parent
    return None


class EnvCheckNode(Node):
    def __init__(self) -> None:
        super().__init__("rebot_trash_sorting_check_env")
        self.declare_parameter("arm_namespace", "rebotarm")
        self.declare_parameter("table_camera_topic", "/table_cam/image_raw")
        self.declare_parameter("wrist_camera_topic", "/wrist_cam/image_raw")

    def run_checks(self) -> bool:
        ns = str(self.get_parameter("arm_namespace").value).strip("/")
        table_topic = str(self.get_parameter("table_camera_topic").value)
        wrist_topic = str(self.get_parameter("wrist_camera_topic").value)

        # Verify cv_bridge + OpenCV round-trip
        bridge = CvBridge()
        dummy = np.zeros((64, 64, 3), dtype=np.uint8)
        msg = bridge.cv2_to_imgmsg(dummy, encoding="bgr8")
        restored = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        assert restored.shape == dummy.shape

        self.get_logger().info(
            f"OpenCV {cv2.__version__} + cv_bridge OK | "
            f"rebotarm_msgs ({MoveToPose.__name__}, {MoveToPoseIK.__name__}, "
            f"{SetGripper.__name__}, {GripperCommand.__name__}, "
            f"{ArmStatus.__name__}, {JointMotorState.__name__}) OK | "
            f"control_msgs ({FollowJointTrajectory.__name__}, {GripperCommandAction.__name__}) OK"
        )

        for pkg in ("rebotarm_bringup", "rebotarm_moveit_config", "rebot_trash_sorting"):
            try:
                share = get_package_share_directory(pkg)
                self.get_logger().info(f"Package '{pkg}' share -> {share}")
            except PackageNotFoundError:
                self.get_logger().error(f"Package '{pkg}' not found in ament index")
                return False

        sorting_share = Path(get_package_share_directory("rebot_trash_sorting"))
        xacro_file = sorting_share / "urdf" / "rebotarm.urdf.xacro"
        for variant in ("soft", "hard"):
            res = subprocess.run(
                ["xacro", str(xacro_file), f"gripper:={variant}"],
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode != 0:
                self.get_logger().error(
                    f"xacro failed for gripper:={variant}: {res.stderr.strip()}"
                )
                return False
            if 'lower="-1.57" upper="1.57"' not in res.stdout or 'name="joint6"' not in res.stdout:
                self.get_logger().error("joint6 [-1.57, 1.57] limit missing in URDF")
                return False
        self.get_logger().info(
            "URDF xacro verified for both gripper:=soft and gripper:=hard (joint6 in [-1.57, 1.57])"
        )

        ws_root = _find_workspace_root()
        if ws_root is not None:
            devarm_dm = ws_root / "third_party" / "reBot-DevArm" / "Rebot_Arm_description" / "DM"
            self.get_logger().info(
                f"Workspace third_party found at {ws_root / 'third_party'} "
                f"(reBot-DevArm DM description present: {devarm_dm.is_dir()})"
            )
        else:
            self.get_logger().warn(
                "third_party/reBotArm_control_py not found in parent directories; "
                "run ./scripts/setup_deps.sh before launching hardware bringup."
            )

        # Briefly spin to discover live graph topics
        deadline = time.monotonic() + 0.5
        while time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)

        topics = dict(self.get_topic_names_and_types())
        self.get_logger().info(
            f"Target namespace '/{ns}' | "
            f"/{ns}/joint_states live={f'/{ns}/joint_states' in topics} | "
            f"{table_topic} live={table_topic in topics} | "
            f"{wrist_topic} live={wrist_topic in topics}"
        )
        return True


def main() -> None:
    rclpy.init()
    node = EnvCheckNode()
    try:
        ok = node.run_checks()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
