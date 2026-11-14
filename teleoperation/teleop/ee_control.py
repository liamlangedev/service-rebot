"""Quest controller -> end-effector target, shared by the sim and the real arm.

Right controller (left: X/Y instead of A/B):
  A                    arm robot control
  B                    stop and disarm (the target freezes, the arm holds)
  hold grip            move the target with your hand (position, and rotation
                       unless track_rotation=False); release = hold
  thumbstick up/down   open / close the gripper (further = faster)
  thumbstick l/r       roll the gripper about its pointing axis
  index trigger        precision mode: hand motion and stick rates x precision_scale
"""
from dataclasses import dataclass

import mujoco
import numpy as np

from teleop.quest_input import ClutchTeleop, ControllerSample
from teleop.rebot_model import GRIPPER_MAX


def rodrigues(v):
    """Rotation matrix of the axis-angle vector v."""
    a = np.linalg.norm(v)
    if a < 1e-12:
        return np.eye(3)
    k = v / a
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K


def rotvec(R):
    """Axis-angle vector of the rotation matrix R."""
    quat, vel = np.empty(4), np.empty(3)
    mujoco.mju_mat2Quat(quat, np.ascontiguousarray(R, dtype=float).reshape(-1))
    mujoco.mju_quat2Vel(vel, quat, 1.0)
    return vel


def rot_x(a):
    return np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])


class GripClutchMapper:
    """Grip-clutched, incremental hand -> TCP-target mapping.

    While moving, every tick adds the hand's motion since the previous tick
    (times `gain`) to the target, so changing the gain (precision mode) or
    releasing the grip never makes the target jump.
    """

    def __init__(self, workspace: ClutchTeleop, track_rotation: bool = True,
                 smoothing: float = 0.3):
        self.workspace = workspace
        self.track_rotation = track_rotation
        self.smoothing = smoothing
        self._prev = None  # (filtered hand position, hand rotation) of the last tick

    def reset(self):
        self._prev = None

    def update(self, s: ControllerSample, moving: bool, gain: float, target_pos, target_rot):
        if not (s.valid and moving):
            self._prev = None
            return target_pos, target_rot
        if self._prev is None:  # grip just pressed: anchor here, no motion yet
            self._prev = (s.pos.copy(), s.rot.copy())
            return target_pos, target_rot
        p_prev, R_prev = self._prev
        p_f = self.smoothing * p_prev + (1 - self.smoothing) * s.pos
        pos = self.workspace.clamp(np.asarray(target_pos) + gain * (p_f - p_prev))
        rot = np.asarray(target_rot)
        if self.track_rotation:
            dR = s.rot @ R_prev.T
            if gain != 1.0:
                dR = rodrigues(gain * rotvec(dR))
            rot = dR @ rot
        self._prev = (p_f, s.rot.copy())
        return pos, rot


@dataclass
class EEConfig:
    scale: float = 1.0
    precision_scale: float = 0.25
    grip_speed: float = 0.06    # m/s of finger travel at full stick (0.05 m = full)
    roll_speed: float = 1.5     # rad/s at full stick
    deadzone: float = 0.3
    track_rotation: bool = True


class EEController:
    """Controller state machine: arm/disarm, grip clutch, precision, gripper, roll."""

    def __init__(self, cfg: EEConfig, target_pos, target_rot, gripper: float = GRIPPER_MAX,
                 hand: str = "r", log=print):
        self.cfg = cfg
        self.start_btn, self.stop_btn = ("A", "B") if hand == "r" else ("X", "Y")
        self.log = log
        self.mapper = GripClutchMapper(ClutchTeleop(), track_rotation=cfg.track_rotation)
        self.target = (np.array(target_pos, float), np.array(target_rot, float))
        self.gripper = float(gripper)  # finger opening [m], 0 = closed .. GRIPPER_MAX
        self.armed = self.moving = self.precise = False
        self._prev_a = self._prev_b = False
        self.last_sample = ControllerSample()

    def _stick(self, v):
        dz = self.cfg.deadzone
        if abs(v) <= dz:
            return 0.0
        return float(np.sign(v) * (abs(v) - dz) / (1.0 - dz))

    def status_text(self) -> str:
        if not self.armed:
            return f"DISARMED - press {self.start_btn}"
        if not self.moving:
            return "ARMED - hold grip to move"
        return "MOVING" + (" (precision)" if self.precise else "")

    def disarm(self, reason: str = ""):
        if self.armed:
            self.log(f"[teleop] DISARMED{reason}")
        self.armed = self.moving = self.precise = False
        self.mapper.reset()

    def resync(self, target_pos, target_rot, gripper: float | None = None):
        """Re-anchor on where the arm actually is (after a stop / external move)."""
        self.target = (np.array(target_pos, float), np.array(target_rot, float))
        if gripper is not None:
            self.gripper = float(gripper)
        self.mapper.reset()

    def update(self, s: ControllerSample, dt: float):
        """One control tick. Returns (target_pos, target_rot, gripper_m)."""
        self.last_sample = s
        a, b = s.reset, s.toggle_rot  # A/B (X/Y on the left hand)
        if a and not self._prev_a and not self.armed:
            self.armed = True
            self.log(f"[teleop] {self.start_btn}: ARMED (hold grip to move)")
        if b and not self._prev_b and self.armed:
            self.disarm(f" ({self.stop_btn}): arm holds its pose")
        self._prev_a, self._prev_b = a, b

        moving = self.armed and s.valid and s.clutch
        precise = moving and s.trigger > 0.5
        changed = moving != self.moving or precise != self.precise
        self.moving, self.precise = moving, precise
        if changed and self.armed:
            self.log(f"[teleop] {self.status_text()}")

        gain = self.cfg.scale * (self.cfg.precision_scale if precise else 1.0)
        pos, rot = self.mapper.update(s, moving, gain, *self.target)

        if self.armed and s.valid:
            rate = self.cfg.precision_scale if s.trigger > 0.5 else 1.0
            # stick up (+y) opens, down closes; left/right rolls the gripper about
            # its pointing axis (tool x), right = clockwise seen from behind.
            self.gripper = float(np.clip(
                self.gripper + self._stick(s.joystick[1]) * rate * self.cfg.grip_speed * dt,
                0.0, GRIPPER_MAX))
            roll = self._stick(s.joystick[0]) * rate * self.cfg.roll_speed * dt
            if roll:
                rot = np.asarray(rot) @ rot_x(roll)
        self.target = (pos, rot)
        return pos, rot, self.gripper
