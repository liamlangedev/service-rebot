"""Shared value types for the agent stack.

Nothing in this module imports rclpy: everything here is pure Python so it can be
unit-tested without a ROS graph.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

# --------------------------------------------------------------------------- perception


@dataclass(frozen=True)
class Detection:
    """One detector result, in image pixels."""

    label: str
    score: float
    bbox: tuple[float, float, float, float]  # x1, y1, x2, y2
    polygon: tuple[tuple[float, float], ...] = ()  # mask outline; bbox corners if unavailable
    #: pixel to project onto the table plane; the mask's contact point by default
    contact_px: tuple[float, float] | None = None

    @property
    def centre_px(self) -> tuple[float, float]:
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    @property
    def width_px(self) -> float:
        return self.bbox[2] - self.bbox[0]

    @property
    def height_px(self) -> float:
        return self.bbox[3] - self.bbox[1]

    def bottom_mid_px(self) -> tuple[float, float]:
        """Base centre estimate: midpoint of the mask's left/right base extremes.

        The lowest point of a standing object is its *near* tangent, so projecting
        it through a table homography biases the target towards the camera by about
        the object's radius. The left and right silhouette extremes in the same
        bottom band straddle the base, so their midpoint is much closer to the
        vertical axis - for a can or a cup it is within a few millimetres. A box
        still has a half-depth bias here, which is what the optional wrist view is
        for.
        """
        if self.contact_px is not None:
            return self.contact_px
        if self.polygon:
            y_max = max(p[1] for p in self.polygon)
            band = max(3.0, 0.20 * max(self.height_px, 1.0))
            points = [p for p in self.polygon if p[1] >= y_max - band]
            if len(points) >= 2:
                left = min(points, key=lambda p: p[0])
                right = max(points, key=lambda p: p[0])
                return ((left[0] + right[0]) / 2.0, (left[1] + right[1]) / 2.0)
        x1, _, x2, y2 = self.bbox
        return ((x1 + x2) / 2.0, y2)


@dataclass
class WorldObject:
    """A detection lifted onto the table plane, in the robot base frame."""

    label: str
    x: float
    y: float
    z: float
    score: float = 0.0
    width_px: float = 0.0
    state: Literal["visible", "remembered"] = "visible"
    age_s: float = 0.0
    seen_count: int = 1
    #: width of the visible bottom edge, projected onto the table plane. There is no
    #: per-class size table: this is measured from the mask on every detection.
    width_m: float = 0.0
    #: direction of that bottom edge in the base frame, degrees. The jaw closes
    #: perpendicular to it, which is the natural way to take a box across its depth.
    yaw_deg: float = 0.0
    #: monotonic stamp of the last frame that contained this object (bookkeeping only)
    last_seen: float = 0.0
    height_m: float | None = None

    @property
    def xy(self) -> tuple[float, float]:
        return (self.x, self.y)

    def summary(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "state": self.state,
            "x": round(self.x, 4),
            "y": round(self.y, 4),
            "z": round(self.z, 4),
            "width_m": round(self.width_m, 4),
            "height_m": round(self.height_m, 4) if self.height_m is not None else None,
            "yaw_deg": round(self.yaw_deg, 1),
            "age_s": round(self.age_s, 1),
            "seen_count": self.seen_count,
            "score": round(self.score, 3),
        }


# --------------------------------------------------------------------------- grasping


@dataclass(frozen=True)
class GraspCandidate:
    """A top-down grasp, in the robot base frame."""

    x: float
    y: float
    z: float  # TCP height (table_z + grasp_height)
    yaw_deg: float  # rotation of the fingers about the tool axis
    width_m: float  # expected object width across the fingers
    score: float
    label: str = ""
    #: height above the table where the fingers should pinch
    pinch_m: float = 0.0

    def summary(self) -> dict[str, Any]:
        return {
            "x": round(self.x, 4),
            "y": round(self.y, 4),
            "z": round(self.z, 4),
            "yaw_deg": round(self.yaw_deg, 1),
            "width_m": round(self.width_m, 4),
            "pinch_m": round(self.pinch_m, 4),
            "score": round(self.score, 3),
        }


@dataclass(frozen=True)
class PlaceTarget:
    """Where an object is released."""

    name: str
    x: float
    y: float
    z: float  # TCP height at release
    kind: Literal["table", "bin"] = "table"
    tilt_deg: float = 0.0  # lean of the tool towards +y (needed to clear the bin rim)
    yaw_deg: float = 0.0

    def summary(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "x": round(self.x, 4),
            "y": round(self.y, 4),
            "z": round(self.z, 4),
            "tilt_deg": round(self.tilt_deg, 1),
        }


# --------------------------------------------------------------------------- VLM / tools


@dataclass(frozen=True)
class TextPart:
    text: str


@dataclass(frozen=True)
class ImagePart:
    data: bytes
    mime_type: str = "image/jpeg"

    def __post_init__(self) -> None:
        if not self.data:
            raise ValueError("ImagePart needs non-empty image bytes")


VLMContent = str | Sequence[TextPart | ImagePart]


@dataclass(frozen=True)
class ToolSchema:
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema object

    def to_summary(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "parameters": self.parameters}


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]
    call_id: str | None = None


@dataclass(frozen=True)
class ToolResult:
    name: str
    payload: dict[str, Any]
    is_error: bool = False

    def to_json(self) -> str:
        import json

        return json.dumps(
            {"tool": self.name, "ok": not self.is_error, "result": self.payload},
            separators=(",", ":"),
            default=str,
        )


@dataclass
class LLMResponse:
    """One planner turn."""

    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    request_id: str | None = None
    raw: Any = None

    @property
    def first_call(self) -> ToolCall | None:
        return self.tool_calls[0] if self.tool_calls else None


@dataclass
class TaskResult:
    task: str
    success: bool
    summary: str
    steps: int
    stopped: bool = False
    error: str | None = None

    def summary_dict(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "success": self.success,
            "summary": self.summary,
            "steps": self.steps,
            "stopped": self.stopped,
            "error": self.error,
        }


def as_text(content: VLMContent) -> str:
    """Flatten VLM content to text (images become a marker)."""
    if isinstance(content, str):
        return content
    out: list[str] = []
    for part in content:
        out.append(part.text if isinstance(part, TextPart) else "[image]")
    return " ".join(out)


def image_parts(content: VLMContent) -> Iterable[ImagePart]:
    if isinstance(content, str):
        return ()
    return [p for p in content if isinstance(p, ImagePart)]
