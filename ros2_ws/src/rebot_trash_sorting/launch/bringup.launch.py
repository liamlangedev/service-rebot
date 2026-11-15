"""Unified MoveIt 2 + RViz bringup for reBot Arm B601-DM (fake or real hardware)."""

from importlib.machinery import SourceFileLoader
import os
import signal

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    EmitEvent,
    IncludeLaunchDescription,
    OpaqueFunction,
    RegisterEventHandler,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown, matches_action
from launch.events.process import SignalProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "on")


def _launch_setup(context, *args, **kwargs):
    del args, kwargs
    use_fake_hardware = _parse_bool(
        LaunchConfiguration("use_fake_hardware").perform(context)
    )
    use_mujoco = _parse_bool(
        LaunchConfiguration("use_mujoco").perform(context)
    )
    gripper = LaunchConfiguration("gripper").perform(context).strip().lower()
    if gripper not in ("soft", "hard"):
        raise ValueError(f"Invalid gripper={gripper!r}; expected 'soft' or 'hard'")
    arm_namespace = LaunchConfiguration("arm_namespace").perform(context).strip("/") or "rebotarm"

    moveit_pkg_share = get_package_share_directory("rebotarm_moveit_config")
    sorting_pkg_share = get_package_share_directory("rebot_trash_sorting")

    moveit_launch_common = SourceFileLoader(
        "moveit_launch_common",
        os.path.join(moveit_pkg_share, "launch", "moveit_launch_common.py"),
    ).load_module()

    initial_positions_file = os.path.join(
        sorting_pkg_share, "config", "initial_positions.yaml"
    )
    urdf_file = os.path.join(sorting_pkg_share, "urdf", "rebotarm.urdf.xacro")
    srdf_file = os.path.join(sorting_pkg_share, "config", "rebotarm.srdf")
    hw_controllers_file = os.path.join(
        sorting_pkg_share, "config", "moveit_hardware_controllers.yaml"
    )

    moveit_config = (
        MoveItConfigsBuilder("rebotarm", package_name="rebotarm_moveit_config")
        .robot_description(
            file_path=urdf_file,
            mappings={
                "initial_positions_file": initial_positions_file,
                "gripper": gripper,
            },
        )
        .robot_description_semantic(file_path=srdf_file)
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .joint_limits(file_path="config/joint_limits.yaml")
        .trajectory_execution(
            file_path=(
                "config/moveit_controllers.yaml"
                if (use_fake_hardware or use_mujoco)
                else hw_controllers_file
            )
        )
        .planning_scene_monitor(
            publish_robot_description=True,
            publish_robot_description_semantic=True,
        )
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )
    moveit_config = moveit_launch_common.apply_rviz_urdf_compat(moveit_config)
    moveit_params = moveit_launch_common.moveit_parameters(moveit_config)

    if not use_fake_hardware and not use_mujoco and arm_namespace != "rebotarm":
        ctrl_mgr = moveit_params.get("moveit_simple_controller_manager", {})
        if "rebotarm" in ctrl_mgr:
            ctrl_mgr[arm_namespace] = ctrl_mgr.pop("rebotarm")
            ctrl_mgr["controller_names"] = [arm_namespace, "gripper_controller"]

    joint_states_remapping = (
        [] if (use_fake_hardware or use_mujoco) else [("/joint_states", f"/{arm_namespace}/joint_states")]
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
        remappings=joint_states_remapping,
    )

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_params],
        remappings=joint_states_remapping,
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rviz_config")],
        condition=IfCondition(LaunchConfiguration("use_rviz")),
        parameters=[moveit_params],
        remappings=joint_states_remapping,
    )

    if use_mujoco:
        return [
            robot_state_publisher_node,
            move_group_node,
            rviz_node,
            RegisterEventHandler(
                OnProcessExit(
                    target_action=move_group_node,
                    on_exit=[EmitEvent(event=Shutdown(reason="move_group exited"))],
                )
            ),
        ]

    if use_fake_hardware:
        ros2_controllers_path = os.path.join(
            moveit_pkg_share, "config", "ros2_controllers.yaml"
        )
        ros2_control_node = Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[moveit_config.robot_description, ros2_controllers_path],
            output="screen",
        )
        spawners = [
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    controller_name,
                    "--controller-manager",
                    "/controller_manager",
                ],
            )
            for controller_name in (
                "joint_state_broadcaster",
                "rebotarm_controller",
                "gripper_controller",
            )
        ]
        return [
            robot_state_publisher_node,
            ros2_control_node,
            *spawners,
            move_group_node,
            rviz_node,
            RegisterEventHandler(
                OnProcessExit(
                    target_action=move_group_node,
                    on_exit=[
                        EmitEvent(
                            event=SignalProcess(
                                signal_number=signal.SIGINT,
                                process_matcher=matches_action(ros2_control_node),
                            )
                        )
                    ],
                )
            ),
            RegisterEventHandler(
                OnProcessExit(
                    target_action=ros2_control_node,
                    on_exit=[
                        EmitEvent(event=Shutdown(reason="ros2_control_node exited"))
                    ],
                )
            ),
        ]

    hardware_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("rebotarm_bringup"), "launch", "driver.launch.py"]
            )
        ),
        launch_arguments={
            "model": "dm",
            "channel": LaunchConfiguration("channel"),
            "arm_namespace": arm_namespace,
        }.items(),
    )

    hardware_gripper_bridge = Node(
        package="rebot_trash_sorting",
        executable="hardware_gripper_bridge",
        name="hardware_gripper_bridge",
        output="screen",
        parameters=[{"arm_namespace": arm_namespace}],
    )

    return [
        hardware_driver,
        hardware_gripper_bridge,
        robot_state_publisher_node,
        move_group_node,
        rviz_node,
        RegisterEventHandler(
            OnProcessExit(
                target_action=move_group_node,
                on_exit=[EmitEvent(event=Shutdown(reason="move_group exited"))],
            )
        ),
    ]


def generate_launch_description() -> LaunchDescription:
    default_rviz = PathJoinSubstitution(
        [FindPackageShare("rebot_trash_sorting"), "rviz", "moveit.rviz"]
    )
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_fake_hardware",
                default_value="true",
                description="Use mock ros2_control hardware (true) or real B601-DM driver (false)",
            ),
            DeclareLaunchArgument(
                "use_mujoco",
                default_value="false",
                description="Use MuJoCo simulation bridge instead of ros2_control/real driver",
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
                description="Start RViz with the MoveIt MotionPlanning panel and target ball",
            ),
            DeclareLaunchArgument(
                "gripper",
                default_value="soft",
                choices=["soft", "hard"],
                description="Gripper finger variant: 'soft' (Fin-Ray TPU, default) or 'hard' (stock rigid)",
            ),
            DeclareLaunchArgument(
                "channel",
                default_value="/dev/ttyACM0",
                description="USB2CAN serial port when use_fake_hardware:=false",
            ),
            DeclareLaunchArgument(
                "arm_namespace",
                default_value="rebotarm",
                description="Controller ROS namespace when use_fake_hardware:=false",
            ),
            DeclareLaunchArgument(
                "rviz_config",
                default_value=default_rviz,
                description="RViz configuration file",
            ),
            OpaqueFunction(function=_launch_setup),
        ]
    )
