"""Conservative observed-object geometry and target-contact lifecycle for MoveIt."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from rebot_trash_sorting_agent.skills.motion import MotionError
from rebot_trash_sorting_agent.skills.poses import ToolPose, quat_multiply, rotate
from rebot_trash_sorting_agent.types import WorldObject


@dataclass
class HeldGeometry:
    centre: tuple[float, float, float]
    orientation: tuple[float, float, float, float]
    radius: float
    height: float

    def at(self, pose: ToolPose) -> tuple[tuple[float, float, float], tuple[float, float, float, float]]:
        if isinstance(pose, ToolPose):
            position, quaternion = (pose.x, pose.y, pose.z), pose.quaternion()
        else:
            position = (pose.position.x, pose.position.y, pose.position.z)
            quaternion = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)
        offset = rotate(quaternion, self.centre)
        return (
            tuple(value + delta for value, delta in zip(position, offset)),
            quat_multiply(quaternion, self.orientation),
        )

    def clearance_pose(self, pose: ToolPose, surface_z: float, margin: float) -> ToolPose:
        centre, orientation = self.at(pose)
        axis = rotate(orientation, (0.0, 0.0, 1.0))
        extent = abs(axis[2]) * self.height / 2 + math.sqrt(max(0.0, 1 - axis[2] ** 2)) * self.radius
        return pose.offset(dz=max(0.0, surface_z + margin - (centre[2] - extent)))


class PlanningSceneClient:
    def __init__(self, node: Any, motion: Any, cfg: dict[str, Any], places: dict[str, Any]) -> None:
        from moveit_msgs.srv import ApplyPlanningScene, GetPlanningScene, GetPositionFK
        from rclpy.callback_groups import ReentrantCallbackGroup

        self.motion = motion
        self.cfg = cfg
        self.places = places
        self.frame = str((motion._cfg).get("base_frame", "base_link"))
        self.tip = motion.tip_link
        self.touch_links = list(cfg.get("touch_links") or ["finger_left_link", "finger_right_link"])
        group = ReentrantCallbackGroup()
        self.apply_client = node.create_client(ApplyPlanningScene, "/apply_planning_scene", callback_group=group)
        self.get_client = node.create_client(GetPlanningScene, "/get_planning_scene", callback_group=group)
        self.fk_client = node.create_client(GetPositionFK, "/compute_fk", callback_group=group)
        self._ids: set[str] = set()
        self._objects: dict[int, Any] = {}
        self._target: Any = None
        self._attached = False
        self.held: HeldGeometry | None = None

    def _apply(self, scene: Any) -> None:
        from moveit_msgs.srv import ApplyPlanningScene

        response = self.motion._call_service(self.apply_client, ApplyPlanningScene.Request(scene=scene))
        if not response.success:
            raise MotionError("planning scene update rejected; refusing motion")

    def current_pose(self):
        from moveit_msgs.msg import PlanningSceneComponents
        from moveit_msgs.srv import GetPlanningScene, GetPositionFK

        request = GetPlanningScene.Request()
        request.components.components = PlanningSceneComponents.ROBOT_STATE
        state = self.motion._call_service(self.get_client, request).scene.robot_state
        fk = GetPositionFK.Request(robot_state=state, fk_link_names=[self.tip])
        fk.header.frame_id = self.frame
        response = self.motion._call_service(self.fk_client, fk)
        if response.error_code.val != 1 or len(response.pose_stamped) != 1:
            raise MotionError("cannot read current tool pose for attached-object release")
        return response.pose_stamped[0].pose

    def _cylinder(self, obj: WorldObject, identifier: str):
        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import CollisionObject
        from shape_msgs.msg import SolidPrimitive

        padding = float(self.cfg.get("padding_m", 0.01))
        height = float(obj.height_m or self.cfg.get("unknown_height_m", 0.25))
        width = float(obj.width_m or self.cfg.get("unknown_width_m", 0.10))
        if not all(math.isfinite(value) for value in (obj.x, obj.y, obj.z, padding, height, width)):
            raise MotionError("nonfinite observed collision geometry")
        if height <= 0 or width <= 0 or padding < 0:
            raise MotionError("invalid observed collision dimensions")
        shape = SolidPrimitive(type=SolidPrimitive.CYLINDER, dimensions=[height + padding, width / 2 + padding])
        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = obj.x, obj.y, obj.z + (height + padding) / 2 + 0.001
        pose.orientation.w = 1.0
        collision = CollisionObject(id=identifier, operation=CollisionObject.ADD)
        collision.header.frame_id = self.frame
        collision.primitives, collision.primitive_poses = [shape], [pose]
        return collision

    def sync(self, objects: Sequence[WorldObject]) -> None:
        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import CollisionObject, PlanningScene
        from shape_msgs.msg import SolidPrimitive

        scene = PlanningScene(is_diff=True)
        for name, bounds in (self.cfg.get("static_boxes") or {}).items():
            if len(bounds) != 6 or not all(math.isfinite(float(value)) for value in bounds):
                raise MotionError(f"invalid static collision bounds for {name}")
            lower, upper = bounds[::2], bounds[1::2]
            sizes = [float(hi - lo) for lo, hi in zip(lower, upper)]
            if min(sizes) <= 0:
                raise MotionError(f"invalid static collision size for {name}")
            pose = Pose()
            pose.position.x, pose.position.y, pose.position.z = [(hi + lo) / 2 for lo, hi in zip(lower, upper)]
            pose.orientation.w = 1.0
            collision = CollisionObject(id=f"cell_{name}", operation=CollisionObject.ADD)
            collision.header.frame_id = self.frame
            collision.primitives = [SolidPrimitive(type=SolidPrimitive.BOX, dimensions=sizes)]
            collision.primitive_poses = [pose]
            scene.world.collision_objects.append(collision)
        new_objects = {id(obj): self._cylinder(obj, f"observed_{index}") for index, obj in enumerate(objects)}
        new_ids = {collision.id for collision in new_objects.values()}
        if self._attached and self._target is not None:
            raise MotionError("cannot replace observed scene while carrying; retain the grasp-time scene")
        for identifier in self._ids - new_ids:
            scene.world.collision_objects.append(CollisionObject(id=identifier, operation=CollisionObject.REMOVE))
        scene.world.collision_objects.extend(new_objects.values())
        self._apply(scene)
        self._ids, self._objects = new_ids, new_objects

    def allow_target_contact(self, obj: WorldObject, allow: bool = True) -> None:
        from moveit_msgs.msg import AllowedCollisionEntry, PlanningScene, PlanningSceneComponents
        from moveit_msgs.srv import GetPlanningScene

        target = self._objects.get(id(obj)) if allow else self._target
        if target is None:
            raise MotionError("target is absent from the synchronized planning scene")
        request = GetPlanningScene.Request()
        request.components.components = PlanningSceneComponents.ALLOWED_COLLISION_MATRIX
        matrix = self.motion._call_service(self.get_client, request).scene.allowed_collision_matrix
        for name in [target.id, *self.touch_links]:
            if name not in matrix.entry_names:
                matrix.entry_names.append(name)
                for entry in matrix.entry_values:
                    entry.enabled.append(False)
                matrix.entry_values.append(AllowedCollisionEntry(enabled=[False] * len(matrix.entry_names)))
        target_index = matrix.entry_names.index(target.id)
        for link in self.touch_links:
            link_index = matrix.entry_names.index(link)
            matrix.entry_values[target_index].enabled[link_index] = bool(allow)
            matrix.entry_values[link_index].enabled[target_index] = bool(allow)
        self._apply(PlanningScene(is_diff=True, allowed_collision_matrix=matrix))
        self._target = target

    def attach(self, obj: WorldObject, grasp: ToolPose) -> None:
        import copy

        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import AttachedCollisionObject, CollisionObject, PlanningScene, RobotState

        if self._target is None or self._objects.get(id(obj)) is not self._target:
            raise MotionError("contact target must be selected before attachment")
        collision = copy.deepcopy(self._target)
        world_pose = collision.primitive_poses[0]
        quaternion = grasp.quaternion()
        inverse = (-quaternion[0], -quaternion[1], -quaternion[2], quaternion[3])
        centre = rotate(
            inverse, (world_pose.position.x - grasp.x, world_pose.position.y - grasp.y, world_pose.position.z - grasp.z)
        )
        held = HeldGeometry(
            centre, inverse, collision.primitives[0].dimensions[1], collision.primitives[0].dimensions[0]
        )
        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = centre
        pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w = inverse
        collision.header.frame_id = self.tip
        collision.primitive_poses = [pose]
        scene = PlanningScene(is_diff=True, robot_state=RobotState(is_diff=True))
        scene.world.collision_objects = [CollisionObject(id=collision.id, operation=CollisionObject.REMOVE)]
        scene.robot_state.attached_collision_objects = [
            AttachedCollisionObject(
                link_name=self.tip,
                object=collision,
                touch_links=self.touch_links,
            )
        ]
        self._apply(scene)
        self._attached, self.held = True, held

    def detach(self, release: ToolPose) -> None:
        import copy

        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import AttachedCollisionObject, CollisionObject, PlanningScene, RobotState

        if not self._attached or self.held is None or self._target is None:
            raise MotionError("no attached geometry to detach")
        collision = copy.deepcopy(self._target)
        centre, orientation = self.held.at(release)
        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = centre
        pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w = orientation
        collision.primitive_poses = [pose]
        scene = PlanningScene(is_diff=True, robot_state=RobotState(is_diff=True))
        scene.robot_state.attached_collision_objects = [
            AttachedCollisionObject(
                link_name=self.tip,
                object=CollisionObject(id=collision.id, operation=CollisionObject.REMOVE),
            )
        ]
        scene.world.collision_objects = [collision]
        self._apply(scene)
        self._attached, self.held = False, None

    def carry_pose(self, pose: ToolPose, objects: Sequence[WorldObject]) -> ToolPose:
        if self.held is None:
            raise MotionError("carry clearance requires attached object geometry")
        top = max(
            [
                float((self.places.get("table") or {}).get("z", 0.0)),
                float((self.places.get("bin") or {}).get("rim_z", 0.12)),
            ]
            + [float(obj.z + (obj.height_m or self.cfg.get("unknown_height_m", 0.25))) for obj in objects]
        )
        return self.held.clearance_pose(pose, top, float(self.cfg.get("carry_clearance_m", 0.04)))

    def release_pose(self, pose: ToolPose, surface_z: float) -> ToolPose:
        if self.held is None:
            raise MotionError("release clearance requires attached object geometry")
        return self.held.clearance_pose(pose, surface_z, float(self.cfg.get("release_clearance_m", 0.015)))
