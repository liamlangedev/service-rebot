"""Bounded wrist-image checks, not uncalibrated robot-position corrections."""

from __future__ import annotations

import math
from collections.abc import Sequence

from rebot_trash_sorting_agent.types import Detection


def target_feature(
    detections: Sequence[Detection], label: str, image_size: tuple[int, int]
) -> tuple[float, float, float]:
    matches = [detection for detection in detections if detection.label == label and detection.score >= 0.5]
    if len(matches) != 1:
        raise ValueError(f"wrist target {label!r} missing or ambiguous")
    width, height = image_size
    if width <= 0 or height <= 0:
        raise ValueError("invalid wrist image resolution")
    left, top, right, bottom = matches[0].bbox
    feature = (
        (left + right) / (2 * width),
        (top + bottom) / (2 * height),
        max(0.0, right - left) * max(0.0, bottom - top) / (width * height),
    )
    if not all(math.isfinite(value) for value in feature) or feature[2] <= 0:
        raise ValueError("invalid wrist target geometry")
    return feature


def same_stationary_target(
    before: tuple[float, float, float],
    after: tuple[float, float, float],
    max_shift: float = 0.035,
    max_area_ratio: float = 1.6,
) -> bool:
    """Compare views only when the robot has not changed pose."""
    shift = math.hypot(after[0] - before[0], after[1] - before[1])
    ratio = max(before[2], after[2]) / max(min(before[2], after[2]), 1e-9)
    return shift <= max_shift and ratio <= max_area_ratio
