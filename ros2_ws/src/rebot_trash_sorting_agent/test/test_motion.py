"""MoveIt request configuration checks without a ROS graph or hardware."""

from types import SimpleNamespace

import pytest

pytest.importorskip("rclpy")
pytest.importorskip("moveit_msgs")

from rebot_trash_sorting_agent.skills.motion import MoveItClient


@pytest.fixture
def make_client(monkeypatch):
    monkeypatch.setattr(
        "rclpy.action.ActionClient",
        lambda *args, **kwargs: SimpleNamespace(
            wait_for_server=lambda **kwargs: True,
        ),
    )
    node = SimpleNamespace(create_client=lambda *args, **kwargs: object())
    return lambda cfg: MoveItClient(node, cfg)


def test_nested_move_group_settings_reach_request(make_client):
    client = make_client(
        {
            "velocity_scaling": 0.1,
            "named_poses": {"home": [0.0] * 6},
            "joint_tolerance": 0.03,
            "move_group": {
                "group": "test_arm",
                "velocity_scaling": 0.3,
                "acceleration_scaling": 0.2,
                "execute": False,
                "allowed_planning_time": 2.0,
                "num_planning_attempts": 3,
            },
        },
    )
    goal = client._goal(False)
    assert goal.request.group_name == "test_arm"
    assert goal.request.max_velocity_scaling_factor == pytest.approx(0.3)
    assert goal.request.max_acceleration_scaling_factor == pytest.approx(0.2)
    assert goal.request.allowed_planning_time == pytest.approx(2.0)
    assert goal.request.num_planning_attempts == 3
    assert goal.planning_options.plan_only
    assert client.named_pose("home") == [0.0] * 6
    assert client._tolerance == pytest.approx(0.03)


def test_flat_config_remains_supported(make_client):
    client = make_client({"velocity_scaling": 0.25, "acceleration_scaling": 0.18})
    goal = client._goal(False)
    assert goal.request.max_velocity_scaling_factor == pytest.approx(0.25)
    assert goal.request.max_acceleration_scaling_factor == pytest.approx(0.18)
    assert not goal.planning_options.plan_only


def test_travel_profile_does_not_change_subsequent_default_goals(make_client):
    client = make_client(
        {
            "move_group": {
                "velocity_scaling": 0.15,
                "acceleration_scaling": 0.15,
                "speed_profiles": {"travel": {"velocity_scaling": 0.3, "acceleration_scaling": 0.2}},
            }
        }
    )
    travel = client._goal(True, "travel")
    assert travel.request.max_velocity_scaling_factor == pytest.approx(0.3)
    assert travel.request.max_acceleration_scaling_factor == pytest.approx(0.2)
    assert travel.planning_options.plan_only
    precise = client._goal(False)
    assert precise.request.max_velocity_scaling_factor == pytest.approx(0.15)
    assert precise.request.max_acceleration_scaling_factor == pytest.approx(0.15)


def test_legacy_config_without_travel_profile_keeps_default_speed(make_client):
    client = make_client({"velocity_scaling": 0.12})
    assert client._goal(False, "travel").request.max_velocity_scaling_factor == pytest.approx(0.12)


@pytest.mark.parametrize("value", [0, -0.1, 1.1, float("nan"), float("inf")])
@pytest.mark.parametrize("key", ["velocity_scaling", "acceleration_scaling"])
def test_invalid_scales_fail_before_creating_a_goal(make_client, value, key):
    with pytest.raises(ValueError, match="scaling"):
        make_client({"move_group": {key: value}})
    with pytest.raises(ValueError, match="scaling"):
        make_client({"move_group": {"speed_profiles": {"travel": {key: value}}}})


def test_public_pose_and_named_moves_forward_speed_profiles(make_client):
    from rebot_trash_sorting_agent.skills.poses import ToolPose

    client = make_client(
        {
            "named_poses": {"home": [0.0] * 6},
            "move_group": {
                "speed_profiles": {"travel": {"velocity_scaling": 0.3, "acceleration_scaling": 0.2}},
            },
        }
    )
    goals = []
    client._send = lambda goal, **kwargs: goals.append(goal) or {}
    client._pose_constraints = lambda pose: __import__("moveit_msgs.msg", fromlist=["Constraints"]).Constraints()
    client.move_to_pose(ToolPose(0.2, 0, 0.2), speed_profile="travel")
    client.move_named("home", speed_profile="travel")
    client.move_to_pose(ToolPose(0.2, 0, 0.05))
    assert [goal.request.max_velocity_scaling_factor for goal in goals] == pytest.approx([0.3, 0.3, 0.15])
