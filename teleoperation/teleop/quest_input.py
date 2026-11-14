"""Meta Quest controller input via OculusReader, plus fake sources for testing.

Every source returns a ControllerSample whose pose is already in the ROBOT
frame (x forward, y left, z up, metres), using the calibration from
tools/calibrate_quest_axes.py when present.
"""
import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CALIBRATION_FILE = ROOT / "config" / "quest_calibration.json"

# Default guess when no calibration exists: OpenXR/OpenGL-style tracking frame
# (x right, y up, z towards the user), user standing behind the robot facing
# the same way. Run tools/calibrate_quest_axes.py to replace it.
DEFAULT_ROBOT_FROM_QUEST = np.array([
    [0.0, 0.0, -1.0],   # robot x (forward) = -quest z
    [-1.0, 0.0, 0.0],   # robot y (left)    = -quest x
    [0.0, 1.0, 0.0],    # robot z (up)      =  quest y
])

# OculusReader button keys per hand.
BUTTON_KEYS = {
    "r": dict(clutch="RG", trigger="rightTrig", reset="A", toggle_rot="B", joystick="rightJS"),
    "l": dict(clutch="LG", trigger="leftTrig", reset="X", toggle_rot="Y", joystick="leftJS"),
}


@dataclass
class ControllerSample:
    valid: bool = False
    pos: np.ndarray = field(default_factory=lambda: np.zeros(3))   # robot frame
    rot: np.ndarray = field(default_factory=lambda: np.eye(3))     # robot frame
    clutch: bool = False      # grip button held -> robot follows the hand
    trigger: float = 0.0      # index trigger 0..1 -> gripper closing
    reset: bool = False       # A / X -> go home
    toggle_rot: bool = False  # B / Y -> toggle orientation tracking
    stamp: float = 0.0


def load_calibration(path: Path = CALIBRATION_FILE) -> np.ndarray:
    if path.exists():
        data = json.loads(path.read_text())
        return np.array(data["robot_from_quest"], dtype=float)
    return DEFAULT_ROBOT_FROM_QUEST.copy()


def to_robot_frame(T_quest: np.ndarray, robot_from_quest: np.ndarray):
    """Converts a 4x4 Quest-frame pose to (pos, rot) in the robot frame.

    Conjugating by the frame change keeps rotations proper even if the Quest
    frame turns out to be left-handed (robot_from_quest with det = -1).
    """
    C = robot_from_quest
    pos = C @ T_quest[:3, 3]
    rot = C @ T_quest[:3, :3] @ C.T
    return pos, rot


class QuestSource:
    """Reads one controller from the Quest through OculusReader (ADB)."""

    def __init__(self, hand: str = "r", ip_address: str | None = None,
                 robot_from_quest: np.ndarray | None = None):
        from oculus_reader.reader import OculusReader  # needs adb + the APK

        self.hand = hand
        self.keys = BUTTON_KEYS[hand]
        self.C = load_calibration() if robot_from_quest is None else robot_from_quest
        self.reader = OculusReader(ip_address=ip_address)

    def raw(self):
        """(4x4 Quest-frame pose or None, buttons dict)."""
        transforms, buttons = self.reader.get_transformations_and_buttons()
        return (transforms or {}).get(self.hand), buttons or {}

    def read(self) -> ControllerSample:
        T, buttons = self.raw()
        if T is None:
            return ControllerSample(valid=False, stamp=time.time())
        pos, rot = to_robot_frame(T, self.C)
        trig = buttons.get(self.keys["trigger"], (0.0,))
        return ControllerSample(
            valid=True, pos=pos, rot=rot,
            clutch=bool(buttons.get(self.keys["clutch"], False)),
            trigger=float(trig[0]) if isinstance(trig, tuple) else float(trig),
            reset=bool(buttons.get(self.keys["reset"], False)),
            toggle_rot=bool(buttons.get(self.keys["toggle_rot"], False)),
            stamp=time.time(),
        )

    def close(self):
        self.reader.stop()


class DemoSource:
    """Scripted fake controller: draws a circle and squeezes the trigger.

    Lets the whole pipeline run without a headset (also used for headless tests).
    """

    def __init__(self, radius: float = 0.08, period: float = 6.0):
        self.radius = radius
        self.period = period
        self.t0 = time.time()

    def read(self, t: float | None = None) -> ControllerSample:
        t = (time.time() - self.t0) if t is None else t
        w = 2 * np.pi / self.period
        pos = np.array([0.0, self.radius * np.sin(w * t), self.radius * (np.cos(w * t) - 1)])
        # Gentle wrist roll about the forward axis.
        a = 0.3 * np.sin(w * t)
        rot = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
        return ControllerSample(valid=True, pos=pos, rot=rot, clutch=t > 0.5,
                                trigger=0.5 * (1 - np.cos(w * t)), stamp=time.time())

    def close(self):
        pass


class ClutchTeleop:
    """Clutch-relative mapping from controller motion to a TCP target.

    While the clutch (grip button) is held, the target moves by the controller's
    displacement since the clutch was pressed (scaled), and rotates by the
    controller's rotation since then. Releasing the clutch freezes the target,
    so you can re-centre your hand, just like lifting a mouse.
    """

    def __init__(self, pos_scale: float = 1.0, track_rotation: bool = True,
                 smoothing: float = 0.3, workspace_lo=(-0.1, -0.5, 0.03),
                 workspace_hi=(0.65, 0.5, 0.75), max_reach: float = 0.62):
        self.pos_scale = pos_scale
        self.track_rotation = track_rotation
        self.smoothing = smoothing  # 0 = no filtering, ->1 = heavy filtering
        self.lo = np.array(workspace_lo)
        self.hi = np.array(workspace_hi)
        self.max_reach = max_reach
        self._engaged = False
        self._prev_toggle = False
        self._ctrl0 = None
        self._target0 = None
        self._filtered = None

    @property
    def engaged(self):
        return self._engaged

    def update(self, s: ControllerSample, target_pos, target_rot):
        """Returns the new (target_pos, target_rot)."""
        if s.toggle_rot and not self._prev_toggle:
            self.track_rotation = not self.track_rotation
            self._engaged = False  # re-anchor so the switch does not cause a jump
            print(f"[teleop] rotation tracking {'ON' if self.track_rotation else 'OFF'}")
        self._prev_toggle = s.toggle_rot

        if not (s.valid and s.clutch):
            self._engaged = False
            return target_pos, target_rot

        if not self._engaged:
            self._engaged = True
            self._ctrl0 = (s.pos.copy(), s.rot.copy())
            self._target0 = (np.array(target_pos), np.array(target_rot))
            self._filtered = None

        p0, R0 = self._ctrl0
        tp0, tR0 = self._target0
        pos = tp0 + self.pos_scale * (s.pos - p0)
        rot = (s.rot @ R0.T) @ tR0 if self.track_rotation else tR0

        if self._filtered is not None and self.smoothing > 0:
            a = self.smoothing
            pos = a * self._filtered + (1 - a) * pos
        self._filtered = pos
        return self._clamp(pos), rot

    def _clamp(self, pos):
        pos = np.clip(pos, self.lo, self.hi)
        shoulder = np.array([0.0, 0.0, 0.14])  # approx. joint2 height
        v = pos - shoulder
        r = np.linalg.norm(v)
        if r > self.max_reach:
            pos = shoulder + v * (self.max_reach / r)
        return pos
