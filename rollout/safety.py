"""Safety filter applied to every command the rollout sends to the arm.

All values are lerobot degrees (the units of the dataset and of the follower driver).
Layers, in the order they are applied to an arm command:

1. **joint soft limits** - the real arm's limits (teleop.rebot_model.REAL_SOFT_LIMITS_DEG),
   shrunk by a margin.
2. **offset from the anchor** - grasp modes only: no arm joint may move more than
   `max_offset_deg` from the pose the policy started at.
3. **speed** - the command may not move any arm joint faster than `max_speed_deg_s`
   relative to the previous command.
4. **workspace** (forward kinematics) - a command whose TCP would go below the table floor
   or beyond the reach radius is refused: the previous command is repeated instead and
   the rollout stops.

On top of that the driver's own limits stay on: `max_relative_target` (per-command step
from the measured position) and, in pos_vel mode, the motors' velocity cap.

`LagWatch` aborts when the measured arm stays far from the command (blocked, collision).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# real arm limits [deg], joint1..joint6 (teleop/teleop/rebot_model.py REAL_SOFT_LIMITS_DEG)
REAL_SOFT_LIMITS_DEG = np.array([(-150.0, 150.0), (-200.0, 1.0), (-200.0, 1.0),
                                 (-80.0, 90.0), (-90.0, 90.0), (-90.0, 90.0)])


@dataclass
class SafetyLimits:
    max_speed_deg_s: float = 45.0
    max_offset_deg: float | None = None   # from the anchor; None = no limit (full task)
    soft_limit_margin_deg: float = 1.0   # dataset wrist_flex reaches 87 (limit 90)
    #: MuJoCo `tcp` site height floor [m]. That site sits ~14 cm above the fingertips
    #: (it is 0.25 m at the ready pose, where the fingertips are ~0.11 m above the table).
    #: In rebot_sort_v1 grasps happen at 0.144-0.15 m; the teleop *commands* press a little
    #: into the table while closing (1% of action frames are below 0.128, the deepest 0.063
    #: in a tilted grasp), so the floor sits just under the usual grasp height.
    min_tcp_z: float = 0.120
    max_reach_m: float = 0.55             # horizontal TCP distance from the base (dataset max 0.495)
    max_lag_deg: float = 25.0
    lag_time_s: float = 1.0


@dataclass
class Verdict:
    command: np.ndarray                    # 7-D command to send
    clipped: list[str] = field(default_factory=list)  # limits that changed the command
    stop: str | None = None                # reason to stop the rollout, if any


class SafetyFilter:
    def __init__(self, limits: SafetyLimits, rate_hz: float, fk=None):
        self.limits = limits
        self.dt = 1.0 / rate_hz
        self.fk = fk                       # callable q_deg[6] -> (x, y, z) or None
        lo = REAL_SOFT_LIMITS_DEG[:, 0] + limits.soft_limit_margin_deg
        hi = REAL_SOFT_LIMITS_DEG[:, 1] - limits.soft_limit_margin_deg
        self.joint_lo, self.joint_hi = lo, hi
        self.anchor: np.ndarray | None = None

    def set_anchor(self, state: np.ndarray) -> None:
        self.anchor = np.asarray(state, dtype=np.float64).copy()

    def check_pose(self, q_deg: np.ndarray) -> str | None:
        """Why this arm pose is outside the workspace, or None."""
        if self.fk is None:
            return None
        x, y, z = self.fk(q_deg[:6])
        if z < self.limits.min_tcp_z:
            return f"TCP z {z:.3f} m below floor {self.limits.min_tcp_z:.3f} m"
        reach = float(np.hypot(x, y))
        if reach > self.limits.max_reach_m:
            return f"TCP reach {reach:.2f} m beyond {self.limits.max_reach_m:.2f} m"
        return None

    def filter(self, cmd: np.ndarray, prev_cmd: np.ndarray) -> Verdict:
        cmd = np.asarray(cmd, dtype=np.float64).copy()
        prev = np.asarray(prev_cmd, dtype=np.float64)
        clipped: list[str] = []
        arm = cmd[:6]

        new = np.clip(arm, self.joint_lo, self.joint_hi)
        if np.any(new != arm):
            clipped.append("joint_limits")
        arm = new

        if self.limits.max_offset_deg is not None and self.anchor is not None:
            a = self.anchor[:6]
            new = np.clip(arm, a - self.limits.max_offset_deg, a + self.limits.max_offset_deg)
            if np.any(new != arm):
                clipped.append("max_offset")
            arm = new

        step = self.limits.max_speed_deg_s * self.dt
        new = np.clip(arm, prev[:6] - step, prev[:6] + step)
        if np.any(np.abs(new - arm) > 1e-9):
            clipped.append("speed")
        arm = new

        cmd[:6] = arm
        why = self.check_pose(arm)
        if why is not None:
            return Verdict(command=prev.copy(), clipped=clipped + ["workspace"], stop=why)
        return Verdict(command=cmd, clipped=clipped)


class LagWatch:
    """Stop when the measured arm stays more than `max_lag_deg` from the command."""

    def __init__(self, limits: SafetyLimits):
        self.limits = limits
        self._since: float | None = None

    def update(self, t: float, cmd: np.ndarray, measured: np.ndarray) -> str | None:
        lag = float(np.max(np.abs(np.asarray(cmd)[:6] - np.asarray(measured)[:6])))
        if lag <= self.limits.max_lag_deg:
            self._since = None
            return None
        self._since = t if self._since is None else self._since
        if t - self._since >= self.limits.lag_time_s:
            return f"arm lags the command by {lag:.0f} deg for {self.limits.lag_time_s:.1f} s"
        return None


@dataclass(frozen=True)
class GripperUnits:
    """Robot gripper degrees (this arm's calibration) <-> dataset gripper degrees.

    The dataset arm read -365 open / -5 closed; this arm reads (from
    teleoperation/config/gripper_limits.json) 161 open / 507 closed. Both go through the
    opening fraction (1 = open, 0 = closed).
    """

    robot_open: float
    robot_closed: float
    data_open: float = -365.0
    data_closed: float = -5.0

    @staticmethod
    def _frac(v, open_, closed):
        return float(np.clip((v - closed) / (open_ - closed), 0.0, 1.0))

    def opening_robot(self, robot_deg: float) -> float:
        return self._frac(robot_deg, self.robot_open, self.robot_closed)

    def opening_data(self, data_deg: float) -> float:
        return self._frac(data_deg, self.data_open, self.data_closed)

    def to_data(self, robot_deg: float) -> float:
        o = self.opening_robot(robot_deg)
        return self.data_closed + o * (self.data_open - self.data_closed)

    def to_robot(self, data_deg: float) -> float:
        o = self.opening_data(data_deg)
        return self.robot_closed + o * (self.robot_open - self.robot_closed)
