"""The real arm's MIT-mode controller (teleop/mit_ff.py), simulated in MuJoCo.

On the real reBot each Damiao motor runs, at ~kHz, on the last frame we sent:

    torque = kp (q_cmd - q) + kd (dq_cmd - dq) + tau_ff

and teleop/mit_ff.py builds that frame every control tick (200 Hz) from the
IK output: joint-limit clip, a first-order low-pass on q_cmd, a filtered
finite-difference velocity feed-forward dq_cmd, a clamp of q_cmd to within
MAX_ERR of the measured pose, and a gravity feed-forward tau_ff.

MitSim does exactly the same with the simulated arm: the arm's position
servos become torque motors (same torque limits), the MJCF's fake gravity
compensation is switched off so gravity acts for real, the frame is built by
the same code path and constants as mit_ff.py, and the torque law is evaluated
at every physics step (1 kHz) like the motor's own loop. The gripper keeps
its position servo.

    velocity_ff=False  sends dq_cmd = 0: a plain damped spring, which lags a
                       moving setpoint; compare to see what the feed-forward buys.
"""
import mujoco
import numpy as np

from teleop.mit_ff import DQ_FILTER, DQ_MAX, MAX_ERR_DEG, MIT_KD, MIT_KP, TAU_FF_MAX, MitParams
from teleop.rebot_real import JOINT_NAMES


class MitSim:
    def __init__(self, sim, params: MitParams | None = None, velocity_ff: bool = True,
                 gravity_scale: float = 1.0):
        self.sim = sim
        self.params = params or MitParams()
        self.velocity_ff = velocity_ff
        self.gravity_scale = gravity_scale
        m = sim.model
        self.model, self.data = m, sim.data

        # Position servos -> torque motors: ctrl is now the joint torque [N.m],
        # clipped by the existing force range (the motors' torque limits).
        for a in sim.arm_act:
            m.actuator_gainprm[a, :] = 0.0
            m.actuator_gainprm[a, 0] = 1.0
            m.actuator_biasprm[a, :] = 0.0
            m.actuator_ctrlrange[a] = m.actuator_forcerange[a]
        # Real gravity: the MJCF's gravcomp hides it; our feed-forward handles it.
        m.body_gravcomp[:] = 0.0
        self.tau_max = m.actuator_forcerange[sim.arm_act, 1].copy()

        self._gdata = mujoco.MjData(m)  # for gravity torques, like mit_ff.gravity_torque
        self.kp = np.array([MIT_KP[n] for n in JOINT_NAMES]) * self.params.kp_scale
        self.kd = np.array([MIT_KD[n] for n in JOINT_NAMES]) * self.params.kd_scale
        self.lo, self.hi = m.jnt_range[[m.joint(f"joint{i}").id for i in range(1, 7)]].T
        self.cmd_tau = self.params.cmd_tau
        self.reset()

    def reset(self):
        self._q_filt = None
        self._q_prev = None
        self._dq = np.zeros(6)
        self.q_frame = self.sim.q_arm.copy()  # the frame the "motors" hold
        self.dq_frame = np.zeros(6)
        self.tau_ff = self._gravity(self.sim.q_arm) * self.gravity_scale

    def _gravity(self, q):
        g = self._gdata
        g.qpos[:] = self.data.qpos
        g.qpos[self.sim.arm_qadr] = q
        g.qvel[:] = 0.0
        mujoco.mj_forward(self.model, g)
        return np.clip(g.qfrc_bias[self.sim.arm_dadr], -TAU_FF_MAX, TAU_FF_MAX)

    def set_command(self, q_cmd, dt: float):
        """One control tick: build the motor frame like MitFF.send()."""
        q_cmd = np.clip(np.asarray(q_cmd, dtype=float), self.lo, self.hi)
        if self._q_filt is None:
            self._q_filt = q_cmd.copy()
        a = 1.0 - np.exp(-dt / self.cmd_tau) if self.cmd_tau > 0 else 1.0
        self._q_filt = self._q_filt + a * (q_cmd - self._q_filt)
        q_cmd = self._q_filt.copy()
        if self._q_prev is None:
            self._q_prev = q_cmd.copy()
        raw = np.clip((q_cmd - self._q_prev) / max(dt, 1e-3), -DQ_MAX, DQ_MAX)
        self._dq = DQ_FILTER * self._dq + (1 - DQ_FILTER) * raw
        self._q_prev = q_cmd.copy()

        q_meas = self.sim.q_arm
        max_err = np.radians(MAX_ERR_DEG)
        self.q_frame = np.clip(q_cmd, q_meas - max_err, q_meas + max_err)
        self.dq_frame = self._dq.copy() if self.velocity_ff else np.zeros(6)
        self.tau_ff = self.gravity_scale * self._gravity(q_meas)

    def apply(self):
        """The motors' fast loop: call before every mj_step."""
        d = self.data
        q, dq = d.qpos[self.sim.arm_qadr], d.qvel[self.sim.arm_dadr]
        tau = self.kp * (self.q_frame - q) + self.kd * (self.dq_frame - dq) + self.tau_ff
        d.ctrl[self.sim.arm_act] = np.clip(tau, -self.tau_max, self.tau_max)

    def freeze(self):
        """Hold the current pose (like MitFF.freeze): no motion state left over."""
        q = self.sim.q_arm.copy()
        self._q_filt, self._q_prev, self._dq = q.copy(), q.copy(), np.zeros(6)
        self.q_frame, self.dq_frame = q, np.zeros(6)
