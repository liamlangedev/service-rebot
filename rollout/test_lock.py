"""Locking after hand placement must hold the new pose, never pull the arm back.

python3 -m pytest rollout/test_lock.py
"""

import numpy as np
import pytest

import rollout as R
from safety import GripperUnits

J = R.robot_io.JOINTS
READY = np.r_[0.0, -86.5, -74.5, 77.93, 0.0, 0.0, -366.0]
PLACED = np.r_[-20.0, -100.0, -80.0, 63.2, 0.0, -15.0, -366.0]   # where the hand left it


class MockArm:
    """Reports the pre-torque-off pose for its first `stale` readings; clamps every
    command to 8 deg (arm) / 40 deg (gripper) from where it really is, like the driver."""

    def __init__(self, stale: int):
        self.true = PLACED.copy()
        self.stale = stale
        self.largest_move = 0.0

    def get_observation(self):
        q = READY if self.stale > 0 else self.true
        self.stale -= 1
        return {f"{n}.pos": float(v) for n, v in zip(J, q)}

    def send_action(self, action):
        goal = np.array([action[f"{n}.pos"] for n in J])
        lim = np.r_[[8.0] * 6, 40.0]
        sent = np.clip(goal, self.true - lim, self.true + lim)
        self.largest_move = max(self.largest_move, float(np.max(np.abs(sent[:6] - self.true[:6]))))
        return {f"{n}.pos": float(v) for n, v in zip(J, sent)}


def make_session(stale: int):
    s = object.__new__(R.Session)
    s.robot = MockArm(stale)
    s.grip = GripperUnits(robot_open=-370.38, robot_closed=-0.01)
    s.events = []
    s.event = s.events.append
    return s


@pytest.mark.parametrize("stale", [0, 2, 6])
def test_lock_holds_the_placed_pose(stale):
    s = make_session(stale)
    target = s.lock_here()
    np.testing.assert_allclose(target[:6], PLACED[:6])
    assert target[6] == pytest.approx(-370.38)          # gripper opens on lock
    # a stale target may be sent once and clamped, but it is replaced before the hold loop
    assert any("stale" in e for e in s.events) == (stale > 0)
