"""python3 -m pytest rollout/test_safety.py"""

import numpy as np
import pytest

from safety import GripperUnits, LagWatch, SafetyFilter, SafetyLimits

GRASP = np.array([-40.0, -120.0, -95.0, 58.0, 0.0, -40.0, 161.0])


def test_speed_cap_limits_each_tick():
    f = SafetyFilter(SafetyLimits(max_speed_deg_s=30.0), rate_hz=30.0)
    v = f.filter(GRASP + np.r_[10, 0, 0, 0, 0, 0, 0], GRASP)
    assert v.command[0] == pytest.approx(GRASP[0] + 1.0)
    assert "speed" in v.clipped and v.stop is None


def test_offset_from_anchor():
    f = SafetyFilter(SafetyLimits(max_speed_deg_s=1e6, max_offset_deg=20.0), rate_hz=30.0)
    f.set_anchor(GRASP)
    v = f.filter(GRASP + np.r_[0, 0, 0, 0, 0, 50, 0], GRASP)
    assert v.command[5] == pytest.approx(GRASP[5] + 20.0)
    assert "max_offset" in v.clipped


def test_joint_soft_limits():
    f = SafetyFilter(SafetyLimits(max_speed_deg_s=1e6), rate_hz=30.0)
    cmd = GRASP.copy()
    cmd[3] = 120.0  # joint4 limit is 90 - margin 1
    assert f.filter(cmd, cmd).command[3] == pytest.approx(89.0)


def test_workspace_floor_refuses_and_repeats_previous():
    fk = lambda q: (0.3, -0.2, 0.10 if q[1] < -130 else 0.15)  # noqa: E731
    f = SafetyFilter(SafetyLimits(max_speed_deg_s=1e6, min_tcp_z=0.125), rate_hz=30.0, fk=fk)
    low = GRASP.copy()
    low[1] = -135
    v = f.filter(low, GRASP)
    assert v.stop and "floor" in v.stop
    np.testing.assert_array_equal(v.command, GRASP)


def test_gripper_is_not_touched_by_arm_limits():
    f = SafetyFilter(SafetyLimits(max_speed_deg_s=1.0), rate_hz=30.0)
    cmd = GRASP.copy()
    cmd[6] = 507.0
    assert f.filter(cmd, GRASP).command[6] == 507.0


def test_lag_watch_needs_persistence():
    w = LagWatch(SafetyLimits(max_lag_deg=10.0, lag_time_s=1.0))
    far = GRASP + np.r_[20, 0, 0, 0, 0, 0, 0]
    assert w.update(0.0, far, GRASP) is None
    assert w.update(0.5, far, GRASP) is None
    assert w.update(0.6, GRASP, GRASP) is None   # recovered: timer resets
    assert w.update(1.0, far, GRASP) is None
    assert "lags" in w.update(2.1, far, GRASP)


def test_gripper_units_this_arm_vs_dataset():
    g = GripperUnits(robot_open=161.0, robot_closed=507.0)
    assert g.to_data(161.0) == pytest.approx(-365.0)
    assert g.to_data(507.0) == pytest.approx(-5.0)
    assert g.to_robot(-5.0) == pytest.approx(507.0)
    assert g.to_robot(g.to_data(300.0)) == pytest.approx(300.0)
    assert g.opening_data(-5.0) == 0.0 and g.opening_robot(161.0) == 1.0
