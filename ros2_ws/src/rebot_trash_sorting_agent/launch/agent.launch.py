"""Camera, workspace geometry, agent and dashboard - everything except the arm.

    ros2 launch rebot_trash_sorting_agent agent.launch.py                 # real cameras
    ros2 launch rebot_trash_sorting_agent agent.launch.py provider:=mock dry_run:=true
    ros2 launch rebot_trash_sorting_agent agent.launch.py use_scene:=false

The arm itself is not started here: bring it up with
``rebot_trash_sorting bringup.launch.py`` (or use ``sorting.launch.py`` for both).
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    config_dir = LaunchConfiguration("config_dir")
    config_arg = ["--config-dir", config_dir]

    return LaunchDescription(
        [
            DeclareLaunchArgument("config_dir", default_value="",
                                  description="directory with agent.yaml and friends (default: package share)"),
            DeclareLaunchArgument("provider", default_value="",
                                  description="override vlm.provider: gemini | openai | mock"),
            DeclareLaunchArgument("model", default_value="",
                                  description="override vlm.model, e.g. gemini-3.8-flash"),
            DeclareLaunchArgument("dry_run", default_value="false",
                                  description="plan and measure but never move the arm"),
            DeclareLaunchArgument("max_steps", default_value="0",
                                  description="override the per-task tool-call budget"),
            DeclareLaunchArgument("use_scene", default_value="true",
                                  description="publish the measured table/walls/bin into the planning scene"),
            DeclareLaunchArgument("use_camera_driver", default_value="true",
                                  description="start camera_node for V4L2 devices (false when MuJoCo publishes cameras)"),
            DeclareLaunchArgument("use_mujoco", default_value="true",
                                  description="start MuJoCo 3D view (mirror-only when real cameras are active)"),
            DeclareLaunchArgument("table_camera", default_value="table",
                                  description="camera name from cameras.yaml used by the agent"),
            DeclareLaunchArgument("host", default_value="127.0.0.1",
                                  description="dashboard bind address (do not expose without auth)"),
            DeclareLaunchArgument("port", default_value="8090", description="dashboard port"),
            DeclareLaunchArgument("joint_states_topic", default_value="/joint_states",
                                  description="real arm publishes /rebotarm/joint_states"),

            Node(
                package="rebot_trash_sorting_agent",
                executable="mujoco_sim_node",
                name="mujoco_sim_node",
                output="screen",
                additional_env={"MUJOCO_GL": "egl"},
                parameters=[{"mirror_only": True}],
                remappings=[("/joint_states", LaunchConfiguration("joint_states_topic"))],
                condition=IfCondition(LaunchConfiguration("use_mujoco")),
            ),
            Node(
                package="rebot_trash_sorting_agent",
                executable="camera_node",
                name="camera_node",
                output="screen",
                arguments=config_arg,
                condition=IfCondition(LaunchConfiguration("use_camera_driver")),
            ),
            Node(
                package="rebot_trash_sorting_agent",
                executable="workspace_scene_node",
                name="workspace_scene_node",
                output="screen",
                arguments=config_arg,
                condition=IfCondition(LaunchConfiguration("use_scene")),
            ),
            Node(
                package="rebot_trash_sorting_agent",
                executable="agent_node",
                name="agent_node",
                output="screen",
                arguments=config_arg,
                parameters=[
                    {
                        "provider": LaunchConfiguration("provider"),
                        "model": LaunchConfiguration("model"),
                        "dry_run": ParameterValue(LaunchConfiguration("dry_run"), value_type=bool),
                        "max_steps": ParameterValue(LaunchConfiguration("max_steps"), value_type=int),
                        "table_camera": LaunchConfiguration("table_camera"),
                    }
                ],
                remappings=[("/joint_states", LaunchConfiguration("joint_states_topic"))],
            ),
            Node(
                package="rebot_trash_sorting_agent",
                executable="dashboard_node",
                name="dashboard_node",
                output="screen",
                arguments=config_arg
                + ["--host", LaunchConfiguration("host"), "--port", LaunchConfiguration("port"),
                   "--camera", LaunchConfiguration("table_camera")],
            ),
        ]
    )
