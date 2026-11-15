"""Everything: arm bringup (fake or real) + the agent stack.

    ros2 launch rebot_trash_sorting_agent sorting.launch.py
    ros2 launch rebot_trash_sorting_agent sorting.launch.py use_fake_hardware:=false channel:=/dev/ttyACM0
    ros2 launch rebot_trash_sorting_agent sorting.launch.py use_rviz:=true

``use_fake_hardware:=true`` is the safe default: the real controller is only
started when you ask for it, and ``channel`` is the USB2CAN device.
"""

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def _truthy(text: str) -> bool:
    return text.strip().lower() in ("true", "1", "yes", "on")


def _launch(context, *args, **kwargs):
    del args, kwargs
    fake = _truthy(LaunchConfiguration("use_fake_hardware").perform(context))
    use_mujoco = _truthy(LaunchConfiguration("use_mujoco").perform(context))
    namespace = LaunchConfiguration("arm_namespace").perform(context).strip("/") or "rebotarm"
    joint_states = "/joint_states" if (fake or use_mujoco) else f"/{namespace}/joint_states"
    table_camera = LaunchConfiguration("table_camera").perform(context).strip()
    if use_mujoco and (not table_camera or table_camera == "table"):
        table_camera = "table_sim"

    actions = []
    if use_mujoco:
        actions.append(
            Node(
                package="rebot_trash_sorting_agent",
                executable="mujoco_sim_node",
                name="mujoco_sim_node",
                output="screen",
                additional_env={"MUJOCO_GL": "egl"},
                parameters=[
                    {
                        "randomize": _truthy(LaunchConfiguration("randomize").perform(context)),
                        "seed": int(LaunchConfiguration("seed").perform(context) or 0),
                    },
                ],
            ),
        )

    bringup = GroupAction(
        [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [FindPackageShare("rebot_trash_sorting"), "/launch/bringup.launch.py"],
                ),
                launch_arguments={
                    "use_fake_hardware": LaunchConfiguration("use_fake_hardware"),
                    "use_mujoco": LaunchConfiguration("use_mujoco"),
                    "use_rviz": LaunchConfiguration("use_rviz"),
                    "gripper": LaunchConfiguration("gripper"),
                    "channel": LaunchConfiguration("channel"),
                    "arm_namespace": LaunchConfiguration("arm_namespace"),
                }.items(),
            ),
        ],
    )
    agent = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("rebot_trash_sorting_agent"), "/launch/agent.launch.py"],
        ),
        launch_arguments={
            "config_dir": LaunchConfiguration("config_dir"),
            "provider": LaunchConfiguration("provider"),
            "vlm_model": LaunchConfiguration("vlm_model"),
            "dry_run": LaunchConfiguration("dry_run"),
            "use_camera_driver": "false" if use_mujoco else "true",
            "use_mujoco": "false" if use_mujoco else "true",
            "table_camera": table_camera or "table",
            "host": LaunchConfiguration("host"),
            "port": LaunchConfiguration("port"),
            "joint_states_topic": joint_states,
        }.items(),
    )
    actions.extend([bringup, agent])
    return actions


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_fake_hardware",
                default_value="true",
                description="mock ros2_control hardware (true) or the real arm (false)",
            ),
            DeclareLaunchArgument(
                "use_mujoco",
                default_value="false",
                description="run MuJoCo RealSetupEnv simulation (arm + cam_corner + wrist)",
            ),
            DeclareLaunchArgument("randomize", default_value="false", description="randomize object poses in MuJoCo"),
            DeclareLaunchArgument("seed", default_value="0", description="random seed when randomize:=true"),
            DeclareLaunchArgument("use_rviz", default_value="false"),
            DeclareLaunchArgument("gripper", default_value="soft", choices=["soft", "hard"]),
            DeclareLaunchArgument(
                "channel", default_value="/dev/ttyACM0", description="USB2CAN serial port for the real arm"
            ),
            DeclareLaunchArgument("arm_namespace", default_value="rebotarm"),
            DeclareLaunchArgument("config_dir", default_value=""),
            DeclareLaunchArgument("provider", default_value=""),
            DeclareLaunchArgument("vlm_model", default_value=""),
            DeclareLaunchArgument("dry_run", default_value="false"),
            DeclareLaunchArgument("table_camera", default_value="table"),
            DeclareLaunchArgument("host", default_value="127.0.0.1"),
            DeclareLaunchArgument("port", default_value="8090"),
            OpaqueFunction(function=_launch),
        ],
    )
