"""Tests for the MuJoCo + Gaussian-splat DigitalTwin and joint streaming."""

import pytest

from web_ui.app import PAGE
from web_ui.digital_twin import DigitalTwin


def test_page_includes_digital_twin_stream():
    assert 'id="sim3d"' in PAGE


def test_update_joints_list_and_dict():
    twin = DigitalTwin({"enabled": False})
    snap = twin.update_joints([0.1, -0.2, 0.3, 0.0, 0.4, -0.5, 0.02])
    assert snap["joint_1"] == pytest.approx(0.1)
    assert snap["joint_6"] == pytest.approx(-0.5)
    assert snap["finger_left"] == pytest.approx(0.02)

    snap2 = twin.update_joints({"joint_2": 0.25, "finger_left": 0.01})
    assert snap2["joint_2"] == pytest.approx(0.25)
    assert snap2["finger_left"] == pytest.approx(0.01)
    assert twin.joints_snapshot()["updates"] == 2


def test_digital_twin_renders_with_streamed_joints():
    pytest.importorskip("mujoco")
    pytest.importorskip("torch")
    twin = DigitalTwin({"enabled": True, "web_view": False, "width": 160, "height": 120})
    twin._init_scene()
    try:
        twin.update_joints([0.2, -0.3, 0.4, 0.1, -0.2, 0.0, 0.02])
        jpg = twin._render_once()
        assert jpg is not None and len(jpg) > 500
        assert twin.status()["ready"] is True
    finally:
        if twin._comp is not None:
            twin._comp.close()
