"""Start the learned-grasp node under the teleoperation venv's Python (lerobot + torch).

    ros2 launch rebot_trash_sorting_agent grasp_policy.launch.py
    ros2 launch rebot_trash_sorting_agent grasp_policy.launch.py \
        policy_path:=niru-5/act_rebot_grasp_keys_abs mode:=absolute \
        camera_names:="[gripper,front_wide,high_oblique]" \
        camera_topics:="[/wrist_cam/image_raw,/front_cam/image_raw,/far_cam/image_raw]"

ROS must be sourced (rclpy comes from /opt/ros/jazzy on PYTHONPATH); the venv supplies
lerobot. Both are Python 3.12.
"""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration


def _default_python() -> str:
    env = os.environ.get("GRASP_POLICY_PYTHON")
    if env:
        return env
    # the repo root is an ancestor of both the source and the colcon install tree
    for base in Path(__file__).absolute().parents:
        cand = base / "teleoperation" / ".venv" / "bin" / "python"
        if cand.exists():
            return str(cand)
    return "python3"


def _launch(context, *_):
    share = Path(get_package_share_directory("rebot_trash_sorting_agent"))
    params = str(share / "config" / "grasp_policy.yaml")
    cmd = [LaunchConfiguration("python").perform(context), "-m",
           "rebot_trash_sorting_agent.grasp_policy_node", "--ros-args",
           "-r", "__node:=grasp_policy", "--params-file", params]
    for name in ("policy_path", "mode", "device", "camera_names", "camera_topics"):
        value = LaunchConfiguration(name).perform(context)
        if value:
            cmd += ["-p", f"{name}:={value}"]
    return [ExecuteProcess(cmd=cmd, output="screen", name="grasp_policy")]


def generate_launch_description():
    args = [DeclareLaunchArgument("python", default_value=_default_python(),
                                  description="interpreter with lerobot installed")]
    args += [DeclareLaunchArgument(n, default_value="") for n in
             ("policy_path", "mode", "device", "camera_names", "camera_topics")]
    return LaunchDescription(args + [OpaqueFunction(function=_launch)])
