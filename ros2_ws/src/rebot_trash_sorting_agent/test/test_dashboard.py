"""Dashboard vocabulary and overlay checks without starting ROS nodes."""

import json
import threading
import time
from types import SimpleNamespace

import numpy as np
import pytest

pytest.importorskip("rclpy")

from rebot_trash_sorting_agent.dashboard_node import PAGE, DashboardNode
from rebot_trash_sorting_agent.types import Detection


def test_dashboard_accepts_agent_vocabulary_and_invalidates_previous_overlays():
    node = SimpleNamespace(
        _lock=threading.Lock(),
        _perception_cfg={"classes": ["can"]},
        _table_dets=[object()],
        _wrist_dets=[object()],
        _front_dets=[object()],
        _jpeg_cache={"table": object()},
    )
    DashboardNode._on_status(node, SimpleNamespace(data=json.dumps({"detector_classes": ["wrapper", "can"]})))
    assert node._perception_cfg["classes"] == ["wrapper", "can"]
    assert not node._table_dets and not node._wrist_dets and not node._front_dets
    assert not node._jpeg_cache


def test_render_cache_tracks_mask_and_box_changes_even_with_same_label_and_score():
    node = SimpleNamespace(_jpeg_cache={}, _encode=lambda image, age: image.tobytes())
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    first = Detection("can", 0.8, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100)))
    second = Detection("can", 0.8, (30, 40, 90, 90), ((30, 40), (90, 40), (90, 90)))
    original = DashboardNode._render_stream(node, "front", frame, 0, 1, [first], 15, "idle")
    changed = DashboardNode._render_stream(node, "front", frame, 0, 1, [second], 15, "idle")
    assert original != changed
    assert 'src="/front_stream"' in PAGE


@pytest.mark.parametrize("camera", ["table", "front", "wrist"])
@pytest.mark.parametrize("confidence, visible", [(0.49, False), (0.5, True), (0.51, True)])
def test_display_confidence_threshold(camera, confidence, visible):
    node = SimpleNamespace(_jpeg_cache={}, _encode=lambda image, age: image.tobytes())
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    detection = Detection("can", confidence, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100)))
    rendered = DashboardNode._render_stream(node, camera, frame, 0, 1, [detection], 15, "idle")
    assert (rendered != frame.tobytes()) is visible


def test_table_feed_does_not_reuse_unfiltered_agent_annotation():
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    node = SimpleNamespace(
        _lock=threading.Lock(),
        _jpeg=b"unfiltered agent annotation",
        _jpeg_stamp=time.monotonic(),
        _frame=frame,
        _frame_stamp=time.monotonic(),
        _frame_seq=1,
        _frame_fps=15,
        _bboxes_enabled=True,
        _table_dets=[],
        _status={},
        _render_stream=lambda *args: frame.tobytes(),
    )
    assert DashboardNode.jpeg(node) == frame.tobytes()
