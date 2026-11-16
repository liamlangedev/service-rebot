"""Frame subscriptions and the rolling scene model.

``CameraClient`` keeps the latest RGB frame from one topic. ``SceneModel`` turns
detections into base-frame objects, merges repeats, and remembers what has left the
view so the planner can be told "visible" versus "remembered".
"""

from __future__ import annotations

import math
import time
from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np

from rebot_trash_sorting_agent.perception.table_map import TableMap
from rebot_trash_sorting_agent.ros_image import imgmsg_to_bgr
from rebot_trash_sorting_agent.types import Detection, WorldObject


class CameraClient:
    """Latest frame from ``<topic>`` as a BGR array."""

    def __init__(self, node: Any, topic: str, timeout_s: float = 5.0) -> None:
        from sensor_msgs.msg import Image

        self._node = node
        self.topic = topic
        self._frame: np.ndarray | None = None
        self._stamp = 0.0
        self._timeout_s = timeout_s
        self._frames = 0
        self._sub = node.create_subscription(Image, topic, self._on_image, 10)

    def _on_image(self, msg: Any) -> None:
        try:
            self._frame = imgmsg_to_bgr(msg)
            self._stamp = time.monotonic()
            self._frames += 1
        except Exception as exc:  # noqa: BLE001 - a malformed frame must not kill the node
            self._node.get_logger().warn(f"{self.topic}: bad frame ({exc})")

    # ------------------------------------------------------------------ api
    @property
    def frames_received(self) -> int:
        return self._frames

    def latest(self, max_age_s: float | None = None) -> np.ndarray | None:
        if self._frame is None:
            return None
        if max_age_s is not None and time.monotonic() - self._stamp > max_age_s:
            return None
        return self._frame

    def wait(self, timeout_s: float | None = None) -> np.ndarray | None:
        timeout_s = self._timeout_s if timeout_s is None else timeout_s
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            frame = self.latest(max_age_s=2.0)
            if frame is not None:
                return frame
            time.sleep(0.05)
        return None

    def wait_fresh(self, timeout_s: float = 2.0) -> np.ndarray | None:
        """Block until a frame arrives that was captured *after* this call.

        ``latest()`` happily returns a two-second-old image; a perception step that
        claims to "look now" should not.
        """
        start = self._frames
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self._frames > start:
                return self.latest(max_age_s=1.0)
            time.sleep(0.02)
        return self.latest(max_age_s=1.0)


class SceneModel:
    """Visible and remembered objects in the base frame."""

    def __init__(self, merge_radius: float = 0.05, ttl_s: float = 45.0) -> None:
        self.merge_radius = float(merge_radius)
        self.ttl_s = float(ttl_s)
        self._objects: list[WorldObject] = []
        self._last_update = 0.0

    # ------------------------------------------------------------------ updates
    def update(
        self,
        detections: Iterable[Detection],
        table_map: TableMap | None,
        stamp: float | None = None,
    ) -> list[WorldObject]:
        now = time.monotonic() if stamp is None else stamp
        self._last_update = now
        fresh: list[WorldObject] = []
        for det in detections:
            if table_map is None:
                continue
            x, y = table_map.project(det)
            width, yaw = table_map.footprint(det)
            fresh.append(
                WorldObject(
                    label=det.label,
                    x=x,
                    y=y,
                    z=table_map.table_z,
                    score=det.score,
                    width_px=det.width_px,
                    width_m=width,
                    yaw_deg=yaw,
                ),
            )

        matched: set[int] = set()
        for obj in fresh:
            match = self._match(obj)
            if match is None:
                obj.last_seen = now
                obj.age_s = 0.0
                self._objects.append(obj)
                matched.add(id(obj))
            else:
                # exponential smoothing: a single noisy frame must not move the target
                alpha = 0.6
                match.x = alpha * obj.x + (1 - alpha) * match.x
                match.y = alpha * obj.y + (1 - alpha) * match.y
                match.score = obj.score
                match.width_px = obj.width_px or match.width_px
                match.height_m = None
                if obj.width_m > 0.0:
                    match.width_m = (
                        alpha * obj.width_m + (1 - alpha) * match.width_m if match.width_m > 0.0 else obj.width_m
                    )
                match.yaw_deg = _blend_angle(match.yaw_deg, obj.yaw_deg, alpha)
                match.seen_count += 1
                match.age_s = 0.0
                match.state = "visible"
                match.last_seen = now
                matched.add(id(match))

        for obj in self._objects:
            if id(obj) in matched:
                continue
            obj.age_s = now - obj.last_seen
            obj.state = "remembered" if obj.age_s <= self.ttl_s else "stale"
        self._objects = [o for o in self._objects if o.state != "stale"]
        return self.visible()

    def _match(self, obj: WorldObject) -> WorldObject | None:
        best = None
        best_dist = self.merge_radius
        for candidate in self._objects:
            if candidate.label != obj.label:
                continue
            dist = float(np.hypot(candidate.x - obj.x, candidate.y - obj.y))
            if dist <= best_dist:
                best, best_dist = candidate, dist
        return best

    # ------------------------------------------------------------------ reading
    def visible(self) -> list[WorldObject]:
        return [o for o in self._objects if o.state == "visible"]

    def all(self) -> list[WorldObject]:
        return list(self._objects)

    def find(self, label: str) -> WorldObject | None:
        """Visible first, then remembered; substring match as a fallback."""
        text = (label or "").strip().lower()
        if not text:
            return None
        for pool in (self.visible(), self.all()):
            for obj in pool:
                if obj.label.lower() == text:
                    return obj
            for obj in pool:
                if text in obj.label.lower() or obj.label.lower() in text:
                    return obj
        return None

    def remove(self, label: str) -> bool:
        """Forget an object that has been picked up (so it cannot be picked twice)."""
        before = len(self._objects)
        self._objects = [o for o in self._objects if o.label.lower() != label.strip().lower()]
        return len(self._objects) != before

    def clear(self) -> None:
        """Clear cached objects so the next task runs a fresh detection."""
        self._objects.clear()
        self._last_update = 0.0

    def summary_text(self, limit: int = 8) -> str:
        objects = self.all()[:limit]
        if not objects:
            return "- nothing detected yet"
        lines = []
        for obj in objects:
            lines.append(
                f"- {obj.label}: state={obj.state}, x={obj.x:.3f}, y={obj.y:.3f}, "
                f"width={obj.width_m:.3f} m, yaw={obj.yaw_deg:.0f} deg, seen={obj.seen_count}x"
                + (f", height={obj.height_m:.3f} m" if obj.height_m is not None else ""),
            )
        return "\n".join(lines)

    def as_summaries(self) -> list[dict[str, Any]]:
        return [o.summary() for o in self.all()]

    @property
    def last_update(self) -> float:
        return self._last_update


def _blend_angle(old_deg: float, new_deg: float, alpha: float) -> float:
    """Exponential smoothing for a line orientation (period 180 deg)."""
    old = math.radians(2.0 * old_deg)
    new = math.radians(2.0 * new_deg)
    return 0.5 * math.degrees(
        math.atan2(
            alpha * math.sin(new) + (1.0 - alpha) * math.sin(old),
            alpha * math.cos(new) + (1.0 - alpha) * math.cos(old),
        ),
    )


def combine(detections: Sequence[Detection]) -> list[Detection]:
    """Merge the same object seen under two vocabulary labels.

    YOLOE is prompt-based, so a "blue bottle" prompt and a "bottle" prompt can both
    fire on one bottle. Sorting by score and merging high-IoU boxes keeps the more
    confident label and drops the duplicate, regardless of the wording.
    """
    seen: list[Detection] = []
    for det in sorted(detections, key=lambda d: d.score, reverse=True):
        if any(_iou(det.bbox, other.bbox) > 0.75 for other in seen):
            continue
        seen.append(det)
    return seen


def _iou(a: Sequence[float], b: Sequence[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    x1, y1 = max(ax1, bx1), max(ay1, by1)
    x2, y2 = min(ax2, bx2), min(ay2, by2)
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0
