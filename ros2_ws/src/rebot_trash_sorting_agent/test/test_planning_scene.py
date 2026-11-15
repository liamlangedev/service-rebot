"""Primitive scene lifecycle and carried-object clearance tests."""

from types import SimpleNamespace

import pytest

pytest.importorskip("moveit_msgs")

from moveit_msgs.msg import CollisionObject, PlanningScene
from rebot_trash_sorting_agent.skills.planning_scene import PlanningSceneClient
from rebot_trash_sorting_agent.skills.poses import ToolPose
from rebot_trash_sorting_agent.types import WorldObject


def scene_client():
    updates = []

    def call(client, request):
        if hasattr(request, "scene"):
            updates.append(request.scene)
            return SimpleNamespace(success=True)
        return SimpleNamespace(scene=PlanningScene())

    motion = SimpleNamespace(_cfg={}, tip_link="gripper_tcp", _call_service=call)
    node = SimpleNamespace(create_client=lambda *args, **kwargs: object())
    scene = PlanningSceneClient(
        node,
        motion,
        {"static_boxes": {"table": [-1.0, 1.0, -1.0, 1.0, -0.04, 0.0]}},
        {"table": {"z": 0}, "bin": {"rim_z": 0.12}},
    )
    return scene, updates


def test_scene_has_all_objects_and_only_target_finger_contact():
    scene, updates = scene_client()
    obj = WorldObject("can", 0.2, 0.0, 0.0, width_m=0.05, height_m=0.15)
    neighbour = WorldObject("cup", 0.3, 0.0, 0.0, width_m=0.08, height_m=0.1)
    scene.sync([obj, neighbour])
    assert len(updates[-1].world.collision_objects) == 3
    scene.allow_target_contact(obj)
    matrix = updates[-1].allowed_collision_matrix
    assert "observed_1" not in matrix.entry_names
    assert set(matrix.entry_names) == {"observed_0", "finger_left_link", "finger_right_link"}
    scene.attach(obj, ToolPose(0.2, 0.0, 0.08))
    assert updates[-1].world.collision_objects[0].operation == CollisionObject.REMOVE
    attached = updates[-1].robot_state.attached_collision_objects[0]
    assert attached.link_name == "gripper_tcp"
    assert attached.object.header.frame_id == "gripper_tcp"
    carried = scene.carry_pose(ToolPose(0.2, 0.0, 0.1), [neighbour])
    centre, _ = scene.held.at(carried)
    assert centre[2] - scene.held.height / 2 >= 0.16 - 1e-6
    scene.detach(carried)
    assert not scene._attached and scene.held is None
    assert updates[-1].robot_state.attached_collision_objects[0].object.operation == CollisionObject.REMOVE


def test_scene_failure_refuses_to_claim_geometry_was_applied():
    from rebot_trash_sorting_agent.skills.motion import MotionError

    scene, _ = scene_client()
    scene.motion._call_service = lambda *args: SimpleNamespace(success=False)
    with pytest.raises(MotionError, match="rejected"):
        scene.sync([])
    assert not scene._ids


def test_tilted_release_clears_surface_using_entire_object():
    import math

    from rebot_trash_sorting_agent.skills.poses import rotate

    scene, _ = scene_client()
    obj = WorldObject("bottle", 0.2, 0.0, 0.0, width_m=0.06, height_m=0.25)
    scene.sync([obj])
    scene.allow_target_contact(obj)
    scene.attach(obj, ToolPose(0.2, 0.0, 0.18))
    release = scene.release_pose(ToolPose(0.2, 0.425, 0.17, tilt_deg=40), 0.12)
    centre, orientation = scene.held.at(release)
    axis = rotate(orientation, (0.0, 0.0, 1.0))
    extent = abs(axis[2]) * scene.held.height / 2 + math.sqrt(max(0, 1 - axis[2] ** 2)) * scene.held.radius
    assert centre[2] - extent >= 0.135 - 1e-6
