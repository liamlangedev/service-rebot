import numpy as np
import pytest

from rebot_trash_sorting_agent.grasp_policy.done import DoneConfig, GraspDone
from rebot_trash_sorting_agent.grasp_policy.relative import from_relative, to_relative
from rebot_trash_sorting_agent.grasp_policy.units import GripperMap, data_to_ros, ros_to_data


def test_gripper_map_ends_and_roundtrip():
    g = GripperMap()
    assert g.to_data(0.05) == pytest.approx(-365.0)
    assert g.to_data(0.0) == pytest.approx(-5.0)
    assert g.to_data(0.2) == pytest.approx(-365.0)  # clipped
    for m in (0.0, 0.01, 0.025, 0.05):
        assert g.to_ros(g.to_data(m)) == pytest.approx(m)
    assert g.data_is_closed(-5.0) and g.data_is_closed(-60.0)
    assert not g.data_is_closed(-365.0) and not g.data_is_closed(-200.0)


def test_gripper_map_other_calibration_direction():
    # this repo's arm: open 161 deg, closed 507 deg (opposite sign convention)
    g = GripperMap(data_open_deg=161.0, data_closed_deg=507.0)
    assert g.to_data(0.05) == pytest.approx(161.0)
    assert g.data_is_closed(500.0) and not g.data_is_closed(170.0)


def test_ready_pose_matches_dataset_start():
    # every rebot_sort_v1 episode starts at about [0, -86.6, -74.5, 77.7, -0.2, 0] deg
    ready_rad = np.array([0.0, -1.51, -1.30, 1.36, 0.0, 0.0])
    state = ros_to_data(ready_rad, 0.05, GripperMap())
    np.testing.assert_allclose(state[:6], [0.0, -86.6, -74.5, 77.7, 0.0, 0.0], atol=0.6)
    arm, finger = data_to_ros(state, GripperMap())
    np.testing.assert_allclose(arm, ready_rad, atol=1e-6)
    assert finger == pytest.approx(0.05)


def test_relative_roundtrip_keeps_gripper_absolute():
    anchor = np.array([-40, -110, -80, 55, 0, -30, -365], dtype=np.float32)
    action = np.array([[-41, -115, -85, 57, 1, -35, -5]], dtype=np.float32)
    rel = to_relative(action, anchor)
    np.testing.assert_allclose(rel[0, :6], [-1, -5, -5, 2, 1, -5])
    assert rel[0, 6] == -5
    np.testing.assert_allclose(from_relative(rel, anchor), action)


def _run(done, ticks):
    for close, finger, z in ticks:
        if done.update(close, finger, z):
            return True
    return False


def test_done_needs_close_settle_and_lift():
    done = GraspDone(DoneConfig(closed_ticks=3, settle_ticks=3, settle_m=0.001, lift_m=0.05))
    approach = [(False, 0.045, 0.10)] * 5
    closing = [(True, f, 0.02) for f in (0.04, 0.03, 0.02, 0.012)]
    settled = [(True, 0.011, 0.02)] * 3
    assert not _run(done, approach + closing + settled)
    assert done.gripped and done.z_grip == pytest.approx(0.02)
    assert not _run(done, [(True, 0.011, 0.05)])
    assert done.phase == "lifting"
    assert _run(done, [(True, 0.011, 0.071)])
    assert done.lifted_m == pytest.approx(0.051)


def test_done_not_fooled_by_lifting_open_jaw():
    done = GraspDone(DoneConfig(closed_ticks=3, settle_ticks=3, lift_m=0.05))
    assert not _run(done, [(False, 0.045, 0.02 + 0.01 * i) for i in range(20)])
    assert not done.gripped


def test_done_resets_close_count_when_policy_reopens():
    done = GraspDone(DoneConfig(closed_ticks=3, settle_ticks=2, settle_m=0.001))
    _run(done, [(True, 0.01, 0.02), (True, 0.01, 0.02), (False, 0.01, 0.02), (True, 0.01, 0.02)])
    assert not done.gripped and done.closed_for == 1
