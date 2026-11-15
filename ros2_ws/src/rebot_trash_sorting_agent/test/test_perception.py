"""Runtime discovery and overlay checks without detector weights or ROS."""

import numpy as np
from rebot_trash_sorting_agent.perception.detector import annotate, discovery_vocabulary
from rebot_trash_sorting_agent.types import Detection


def test_discovery_extends_baseline_and_rejects_invalid_names():
    vocabulary = discovery_vocabulary(
        [" Paper CUP ", "paper cup", "bottle", "robot", 7, "x" * 65, "ignore\nall;commands"],
        ["can", "bottle"],
    )
    assert vocabulary == ["paper cup", "can", "bottle"]
    assert discovery_vocabulary(None, ["can"]) == ["can"]
    assert discovery_vocabulary("not a list", ["can"]) == ["can"]


def test_discovery_budget_keeps_baseline_classes():
    vocabulary = discovery_vocabulary([f"item {index}" for index in range(100)], ["can", "bottle"])
    assert len(vocabulary) == 32
    assert vocabulary[-2:] == ["can", "bottle"]


def test_overlay_draws_mask_interior_and_keeps_original_frame():
    original = np.zeros((120, 120, 3), dtype=np.uint8)
    detection = Detection("cup", 0.9, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100), (20, 100)))
    rendered = annotate(original, [detection])
    assert rendered[65, 60, 1] > 0
    assert rendered[50, 20, 1] > 0
    assert not original.any()
