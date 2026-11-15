"""MIT-mode joint control with velocity and gravity feed-forward.

    torque = kp (q_cmd - q) + kd (dq_cmd - dq) + tau_gravity(q)

The motor evaluates this at ~kHz from the last frame we send, so the arm
follows a moving setpoint without lag (dq_cmd) and without sagging (tau_g).
Gravity torques come from the MJCF masses, scaled by `gravity_scale`.
"""
from dataclasses import dataclass

import mujoco
import numpy as np

from teleop import gripper_limits
from teleop.rebot_model import ARM_JOINTS, RebotSim
from teleop.rebot_real import JOINT_NAMES

# Lower damping than lerobot's default (kd 12) so the arm is not sluggish;
# the velocity feed-forward supplies the speed. (kp, kd) per joint. A noisy
# dq feed-forward is amplified by kd, so the wrist needs the filter + more damping.
MIT_KP = dict(zip(JOINT_NAMES, [40.0, 40.0, 40.0, 18.0, 18.0, 18.0]))
MIT_KD = dict(zip(JOINT_NAMES, [2.5, 2.5, 2.5, 2.0, 2.0, 2.0]))  # wrist: Seeed's reference values
TAU_FF_MAX = np.array([20.0, 20.0, 20.0, 7.0, 7.0, 7.0])  # below the motors' TMAX
# Largest tracking error we ever command, per joint: it bounds the torque
# (kp * error) when the arm is blocked or pushed, e.g. against the table.
MAX_ERR_DEG = np.array([15.0, 15.0, 15.0, 20.0, 20.0, 20.0])
# Gripper in MIT mode: weak spring, error clamp = grip force (~kp * err = 1.1 N.m).
GRIP_KD, GRIP_DQ_MAX = 1.0, 12.0


@dataclass
class MitParams:
    """Runtime knobs, set on the record_rebot.py command line as --mit.<name>=<value>."""
    grip_mode: str = "force_pos"  # force_pos: firmware torque ratio; impedance: lerobot moving/holding torque limits; mit: our spring
    grip_err_deg: float = 8.0  # max lead of the command over the measured position
    grip_kp: float = 8.0       # grip force limit ~ grip_kp * grip_err_deg(rad) N.m; stiffer kp = closes fully
    kp_scale: float = 1.0      # multiplies the arm kp
    kd_scale: float = 1.0      # multiplies the arm kd
    wrist_scale: float = 1.0   # extra multiplier on wrist (joints 4-6) kp and kd, e.g. 0.4 when kp_scale is 3
    cmd_tau: float = 0.03      # joint-command low-pass time constant [s], 0 = off
    friction_scale: float = 1.0  # multiplies the friction feed-forward; 0 = off, raise until it just stops sticking
    ready_speed: float = 0.6   # ready-move peak speed [rad/s]

# Coulomb-friction feed-forward [N.m], applied along the commanded motion direction.
# Measured dead zone ~ error needed to start moving: lift/elbow ~2 deg at kp 40 (~1.4 N.m).
FRICTION_FF = np.array([0.4, 1.0, 1.0, 0.25, 0.15, 0.12])
FRICTION_VEL = 0.15  # rad/s over which the sign smoothly switches (tanh)
DQ_MAX = 4.0  # rad/s, clip on the velocity feed-forward
DQ_FILTER = 0.6  # low-pass on the finite-difference velocity (0 = none)


class MitFF:
    def __init__(self, robot, params: MitParams | None = None):
        self.robot = robot
        self.params = params or MitParams()
        sim = RebotSim()
        self.model = sim.model
        self.model.body_gravcomp[:] = 0.0  # the MJCF fakes gravity comp; we want the real torque
        self.data = mujoco.MjData(self.model)
        self.qadr, self.dadr = sim.arm_qadr, sim.arm_dadr
        self.gravity_scale = 0.0
        self._q_prev = None
        self._dq = np.zeros(6)
        w = np.array([1.0, 1.0, 1.0] + [self.params.wrist_scale] * 3)
        self.kp = np.array([MIT_KP[n] for n in JOINT_NAMES]) * self.params.kp_scale * w
        self.kd = np.array([MIT_KD[n] for n in JOINT_NAMES]) * self.params.kd_scale * w
        self._g_prev, self._g_dq = None, 0.0
        self._grip_tripped = False
        self._q_filt = None
        self.cmd_tau = self.params.cmd_tau

    def gravity_torque(self, q: np.ndarray) -> np.ndarray:
        self.data.qpos[self.qadr] = q
        self.data.qvel[:] = 0.0
        mujoco.mj_forward(self.model, self.data)
        return np.clip(self.data.qfrc_bias[self.dadr], -TAU_FF_MAX, TAU_FF_MAX)

    def send(self, action: dict, q_meas_deg: dict, dt: float) -> None:
        q_cmd = np.radians([action[f"{n}.pos"] for n in JOINT_NAMES])
        lo = np.radians([self.robot._joint_limits[n][0] for n in JOINT_NAMES])
        hi = np.radians([self.robot._joint_limits[n][1] for n in JOINT_NAMES])
        q_cmd = np.clip(q_cmd, lo, hi)
        if self._q_filt is None:
            self._q_filt = q_cmd.copy()
        # First-order low-pass on the command: removes jitter before it reaches kp and the velocity term.
        a = 1.0 - np.exp(-dt / self.cmd_tau) if self.cmd_tau > 0 else 1.0
        self._q_filt = self._q_filt + a * (q_cmd - self._q_filt)
        q_cmd = self._q_filt.copy()
        if self._q_prev is None:
            self._q_prev = q_cmd.copy()
        raw = np.clip((q_cmd - self._q_prev) / max(dt, 1e-3), -DQ_MAX, DQ_MAX)
        self._dq = DQ_FILTER * self._dq + (1 - DQ_FILTER) * raw
        self._q_prev = q_cmd.copy()

        q_meas = np.radians([q_meas_deg[n] for n in JOINT_NAMES])
        max_err = np.radians(MAX_ERR_DEG)
        q_cmd = np.clip(q_cmd, q_meas - max_err, q_meas + max_err)
        tau = self.gravity_scale * self.gravity_torque(q_meas)
        tau = tau + self.gravity_scale * self.params.friction_scale * FRICTION_FF * np.tanh(self._dq / FRICTION_VEL)
        tau = np.clip(tau, -TAU_FF_MAX, TAU_FF_MAX)
        for i, name in enumerate(JOINT_NAMES):
            self.robot.motors[name].send_mit(
                float(q_cmd[i]), float(self._dq[i]), float(self.kp[i]), float(self.kd[i]), float(tau[i]))
        if "gripper.pos" in action:
            self._send_gripper(action["gripper.pos"], q_meas_deg["gripper"], dt)

    def freeze(self, pose_deg: dict) -> None:
        """Forget the motion state so the next command is a plain hold at `pose_deg`."""
        self._q_filt = np.radians([pose_deg[f"{n}.pos"] for n in JOINT_NAMES])
        self._q_prev = self._q_filt.copy()
        self._dq = np.zeros(6)
        self._g_prev, self._g_dq = pose_deg["gripper.pos"], 0.0

    def _send_gripper(self, cmd_deg: float, meas_deg: float, dt: float) -> None:
        limits = gripper_limits.load()
        if limits is None:
            return  # never move an unmeasured gripper
        lo, hi = gripper_limits.bounds(limits)
        phys_lo, phys_hi = sorted(limits)
        if not (phys_lo - 15.0 <= meas_deg <= phys_hi + 15.0):
            if not self._grip_tripped:
                self.robot.motors["gripper"].disable()
                print(f"[gripper] position {meas_deg:.0f} deg is outside the measured range "
                      f"{phys_lo:.0f}..{phys_hi:.0f}: gripper torque disabled.")
                self._grip_tripped = True
            return
        cmd = float(np.clip(cmd_deg, lo, hi))
        if self.params.grip_mode in ("force_pos", "impedance"):
            self.robot._send_joint("gripper", cmd)  # firmware loop: speed limit + torque ratio
            return
        if self._g_prev is None:
            self._g_prev = cmd
        raw = np.clip(np.radians(cmd - self._g_prev) / max(dt, 1e-3), -GRIP_DQ_MAX, GRIP_DQ_MAX)
        self._g_dq = 0.3 * self._g_dq + 0.7 * raw
        self._g_prev = cmd
        cmd = float(np.clip(cmd, meas_deg - self.params.grip_err_deg, meas_deg + self.params.grip_err_deg))
        self.robot.motors["gripper"].send_mit(
            float(np.radians(cmd)), 0.0, self.params.grip_kp, GRIP_KD, 0.0)
