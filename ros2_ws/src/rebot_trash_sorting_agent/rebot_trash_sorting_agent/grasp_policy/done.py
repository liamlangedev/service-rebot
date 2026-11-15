"""Decide when the learned grasp is finished: the jaw has closed and the TCP has lifted.

Fed once per control tick. The two phases:

1. **gripped** - the policy has commanded "close" for `closed_ticks` consecutive ticks
   and the measured finger has stopped moving (spread over the last `settle_ticks`
   readings below `settle_m`). The TCP height at that moment is the lift reference.
2. **lifted** - the TCP is `lift_m` above that reference.

It does not judge whether something is actually held: for thin objects (keys) the jaw
closes fully either way. The caller gets the finger position and can apply its own
torque/position check (``GripperClient.check_hold`` in the classical stack).
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass
class DoneConfig:
    closed_ticks: int = 6       # 0.2 s of "close" commands at 30 Hz
    settle_ticks: int = 6
    settle_m: float = 0.0008    # finger spread over the settle window [m]
    lift_m: float = 0.05


@dataclass
class GraspDone:
    cfg: DoneConfig = field(default_factory=DoneConfig)
    closed_for: int = 0
    gripped: bool = False
    z_grip: float | None = None
    finger_at_grip: float | None = None
    lifted_m: float = 0.0
    _fingers: deque = field(default_factory=deque)

    def update(self, close_cmd: bool, finger_m: float, tcp_z: float) -> bool:
        """Returns True once gripped and lifted."""
        self._fingers.append(float(finger_m))
        while len(self._fingers) > self.cfg.settle_ticks:
            self._fingers.popleft()
        if not self.gripped:
            self.closed_for = self.closed_for + 1 if close_cmd else 0
            settled = (len(self._fingers) == self.cfg.settle_ticks
                       and max(self._fingers) - min(self._fingers) <= self.cfg.settle_m)
            if self.closed_for >= self.cfg.closed_ticks and settled:
                self.gripped = True
                self.z_grip = float(tcp_z)
                self.finger_at_grip = float(finger_m)
            return False
        self.lifted_m = float(tcp_z) - float(self.z_grip)
        return self.lifted_m >= self.cfg.lift_m

    @property
    def phase(self) -> str:
        if not self.gripped:
            return "closing" if self.closed_for else "approaching"
        return "lifting"
