#!/usr/bin/env python3
"""Publish the measured cell geometry into MoveIt's planning scene.

MoveIt only knows the robot and the SRDF. The table, the three cell walls and the
bin are *physical* objects that are not in any URDF, so without this node the
planner happily plans the forearm through the wall - which is exactly what the
old ``ready`` pose did (16 mm into ``wall_near``).

The geometry is the measured cell from ``places.yaml``. Boxes are applied as a
planning-scene diff through ``/apply_planning_scene`` and re-applied on a timer, so
restarting move_group does not silently lose the walls.
"""

from __future__ import annotations

import argparse
from typing import Any

import rclpy
from rclpy.node import Node

from .config import Config

BOX_NAMES = {
    "table": "cell_table",
    "walls": "wall",
    "bin": "bin",
}


class WorkspaceSceneNode(Node):
    def __init__(self, config: Config) -> None:
        super().__init__("workspace_scene_node")
        self.declare_parameter("frame_id", "base_link")
        self.declare_parameter("reapply_s", 10.0)
        self._frame = str(self.get_parameter("frame_id").value or "base_link")
        self._boxes = build_boxes(config.places)
        self._applied = False
        self._warned = False

        from moveit_msgs.msg import PlanningScene
        from moveit_msgs.srv import ApplyPlanningScene
        from std_srvs.srv import Trigger

        self._Apply = ApplyPlanningScene
        self._Scene = PlanningScene
        self._client = self.create_client(ApplyPlanningScene, "/apply_planning_scene")
        self.create_service(Trigger, "/workspace_scene/apply", self._on_apply)
        period = float(self.get_parameter("reapply_s").value or 10.0)
        self.create_timer(max(period, 1.0), self._tick)
        self.get_logger().info(
            f"workspace: {len(self._boxes)} collision boxes in {self._frame} "
            f"({', '.join(name for name, _ in self._boxes)})"
        )

    # ------------------------------------------------------------------ scene
    def _scene(self):
        from geometry_msgs.msg import Pose
        from moveit_msgs.msg import CollisionObject
        from shape_msgs.msg import SolidPrimitive

        scene = self._Scene()
        scene.is_diff = True
        for name, (centre, size) in self._boxes:
            obj = CollisionObject()
            obj.header.frame_id = self._frame
            obj.id = name
            obj.operation = CollisionObject.ADD
            primitive = SolidPrimitive()
            primitive.type = SolidPrimitive.BOX
            primitive.dimensions = list(size)
            pose = Pose()
            pose.position.x, pose.position.y, pose.position.z = centre
            pose.orientation.w = 1.0
            obj.primitives = [primitive]
            obj.primitive_poses = [pose]
            scene.world.collision_objects.append(obj)
        return scene

    def _tick(self) -> None:
        if self._applied:
            return
        if not self._client.service_is_ready():
            if not self._client.wait_for_service(timeout_sec=0.1) and not self._warned:
                self.get_logger().info("waiting for /apply_planning_scene (is move_group up?)")
                self._warned = True
            return
        self.apply()

    def apply(self) -> bool:
        request = self._Apply.Request()
        request.scene = self._scene()
        future = self._client.call_async(request)
        future.add_done_callback(self._done)
        return True

    def _done(self, future: Any) -> None:
        try:
            response = future.result()
            ok = bool(response is not None and response.success)
        except Exception as exc:  # noqa: BLE001 - a failed apply is retried by the timer
            ok = False
            self.get_logger().warn(f"planning scene apply failed: {exc}")
        if ok:
            if not self._applied:
                self.get_logger().info("workspace geometry applied to the planning scene")
            self._applied = True
            self._warned = False
        else:
            self.get_logger().warn("planning scene apply rejected; will retry")

    def _on_apply(self, _request: Any, response: Any) -> Any:
        self._applied = False
        self._tick()
        response.success = True
        response.message = f"{len(self._boxes)} boxes submitted"
        return response


def build_boxes(places: dict[str, Any]) -> list[tuple[str, tuple[tuple[float, float, float], tuple[float, float, float]]]]:
    """``[(id, (centre, size))]`` from the ``[x0, x1, y0, y1, z0, z1]`` boxes."""
    out: list[tuple[str, tuple[tuple[float, float, float], tuple[float, float, float]]]] = []

    def add(name: str, box) -> None:
        try:
            x0, x1, y0, y1, z0, z1 = (float(v) for v in box[:6])
        except (TypeError, ValueError):
            return
        centre = ((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)
        size = (abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))
        if min(size) <= 0.0:
            return
        out.append((name, (centre, size)))

    table = places.get("table") or {}
    if table.get("box"):
        add("cell_table", table["box"])
    for name, box in (places.get("walls") or {}).items():
        add(f"wall_{name}", box)
    for name, box in ((places.get("bin") or {}).get("boxes") or {}).items():
        add(f"bin_{name}", box)
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", default=None)
    args, ros_args = parser.parse_known_args(argv)

    rclpy.init(args=ros_args)
    node = WorkspaceSceneNode(Config.load(args.config_dir))
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
