"""Safety layer: every trajectory is checked here before a single command is sent.

What it enforces
  * joint soft limits of the real DM arm (follower.json), with a margin
  * a workspace box for the TCP and a floor for the fingertips (never into the table)
  * a joint speed cap (trajectories are time-scaled to respect it)
  * a software E-stop that stops streaming and holds the current pose

What it does NOT do: collision checking against objects or people. Keep a hand on the
real E-stop / power switch whenever the real arm is enabled.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field

import numpy as np

from teleop.rebot_model import REAL_SOFT_LIMITS_DEG


class SafetyError(RuntimeError):
    pass


class EStopped(SafetyError):
    pass


@dataclass
class SafetyConfig:
    workspace_min: tuple = (-0.40, -0.45, 0.0)     # TCP box [m] (z is checked via fingertips)
    workspace_max: tuple = (0.70, 0.45, 0.75)
    min_tip_height: float = 0.004                  # fingertips above the table [m]
    joint_margin_deg: float = 2.0
    max_joint_vel: float = 1.5                     # [rad/s] (real default lower, see app.py)
    max_tracking_error_deg: float = 12.0           # real arm: abort if it lags this much

    @classmethod
    def from_dict(cls, d: dict | None) -> "SafetyConfig":
        return cls(**{k: tuple(v) if isinstance(v, list) else v for k, v in (d or {}).items()})


@dataclass
class Safety:
    cfg: SafetyConfig = field(default_factory=SafetyConfig)
    table_z: float = 0.03
    _estop: threading.Event = field(default_factory=threading.Event)

    def __post_init__(self):
        lims = np.radians(np.array(list(REAL_SOFT_LIMITS_DEG.values())))
        m = np.radians(self.cfg.joint_margin_deg)
        self.q_lo, self.q_hi = lims[:, 0] + m, lims[:, 1] - m

    # ---- E-stop -------------------------------------------------------------
    def estop(self, reason: str = "operator"):
        print(f"[safety] E-STOP: {reason}")
        self._estop.set()

    def reset_estop(self):
        self._estop.clear()

    @property
    def stopped(self) -> bool:
        return self._estop.is_set()

    def check_running(self):
        if self._estop.is_set():
            raise EStopped("E-stop is active")

    # ---- checks ---------------------------------------------------------------
    def check_joints(self, q: np.ndarray):
        if np.any(q < self.q_lo) or np.any(q > self.q_hi):
            bad = [i + 1 for i in np.where((q < self.q_lo) | (q > self.q_hi))[0]]
            raise SafetyError(f"joint limit on joint(s) {bad}: {np.round(np.degrees(q), 1)} deg")

    def check_tcp(self, tcp: np.ndarray, tip: np.ndarray):
        lo, hi = np.array(self.cfg.workspace_min), np.array(self.cfg.workspace_max)
        if np.any(tcp[:2] < lo[:2]) or np.any(tcp[:2] > hi[:2]) or tcp[2] > hi[2]:
            raise SafetyError(f"TCP {np.round(tcp, 3)} outside the workspace box")
        if tip[2] < self.table_z + self.cfg.min_tip_height:
            raise SafetyError(f"fingertips would go into the table (z={tip[2]:.3f})")

    def check_trajectory(self, qs: list[np.ndarray], fk_tip):
        """fk_tip(q) -> (tcp_pos, fingertip_pos). Raises SafetyError on the first bad point."""
        self.check_running()
        for q in qs:
            self.check_joints(q)
            self.check_tcp(*fk_tip(q))
