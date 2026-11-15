"""Web UI stream, confidence overlay, and status tests (ROS-free)."""

from types import SimpleNamespace

import numpy as np
import pytest

from web_ui.app import PAGE, DashboardApp
from web_ui.types import Detection


def test_page_contains_three_camera_streams():
    assert 'src="/stream"' in PAGE
    assert 'src="/front_stream"' in PAGE
    assert 'src="/wrist_stream"' in PAGE


def test_render_cache_tracks_mask_and_box_changes():
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    stream = SimpleNamespace(frames_received=1, latest=lambda max_age_s=5.0: frame)
    app = SimpleNamespace(
        _bboxes_enabled=True,
        _jpeg_cache={},
        _stream_for=lambda _name: stream,
        _encode=lambda image: image.tobytes(),
    )
    first = Detection("can", 0.8, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100)))
    second = Detection("can", 0.8, (30, 40, 90, 90), ((30, 40), (90, 40), (90, 90)))
    original = DashboardApp._camera_jpeg(app, "front", [first])
    changed = DashboardApp._camera_jpeg(app, "front", [second])
    assert original != changed


@pytest.mark.parametrize("camera", ["table", "front", "wrist"])
@pytest.mark.parametrize("confidence, visible", [(0.49, False), (0.5, True), (0.51, True)])
def test_display_confidence_threshold(camera, confidence, visible):
    frame = np.zeros((120, 120, 3), dtype=np.uint8)
    stream = SimpleNamespace(frames_received=1, latest=lambda max_age_s=5.0: frame)
    app = SimpleNamespace(
        _bboxes_enabled=True,
        _jpeg_cache={},
        _stream_for=lambda _name: stream,
        _encode=lambda image: image.tobytes(),
    )
    detection = Detection("can", confidence, (20, 30, 100, 100), ((20, 30), (100, 30), (100, 100)))
    rendered = DashboardApp._camera_jpeg(app, camera, [detection])
    assert (rendered != frame.tobytes()) is visible
