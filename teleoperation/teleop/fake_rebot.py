"""A simulated stand-in for lerobot's RebotB601Follower (no hardware).

Answers the driver calls the real-arm path uses (teleop/fast_loop.py,
teleop/mit_ff.py, teleop/ready_move.py): motors[name].send_mit(q, dq, kp, kd, tau),
_send_joint("gripper", deg), _present_pos(), get_observation(), send_action(),
disconnect(). A 1 kHz physics thread moves a MuJoCo reBot with the motors' own
MIT law, torque = kp (q - q_meas) + kd (dq - dq_meas) + tau, under real gravity
(no fake gravity compensation), so gravity_check, the ready move and the 200 Hz
teleop loop run exactly as they would on the arm.

Units match lerobot's public frame: arm joints in degrees (= degrees of the
MJCF qpos), gripper in the measured degrees of config/gripper_limits.json.
"""
import threading
import time

import mujoco
import numpy as np

from teleop.rebot_model import GRIPPER_MAX, RebotSim
from teleop.rebot_real import JOINT_NAMES


class _FakeMotor:
    def __init__(self, robot, idx):
        self.robot, self.idx = robot, idx

    def send_mit(self, q, dq, kp, kd, tau):
        with self.robot._lock:
            self.robot._frame[self.idx] = (float(q), float(dq), float(kp), float(kd), float(tau))
            self.robot.n_mit_frames += 1

    def disable(self):
        with self.robot._lock:
            self.robot._frame[self.idx] = (0.0, 0.0, 0.0, 0.0, 0.0)  # limp


class _FakeGripperMotor:
    def __init__(self, robot):
        self.robot = robot

    def disable(self):
        self.robot._grip_enabled = False

    def send_mit(self, *a):
        pass


class FakeRebotFollower:
    def __init__(self, config, gripper_limits_deg):
        self.config = config
        self._joint_limits = dict(config.joint_limits)
        self.cameras = {}
        self.calibration = {"fake": True}
        self.open_deg, self.closed_deg = gripper_limits_deg
        self.sim = RebotSim()
        m, d = self.sim.model, self.sim.data
        for a in self.sim.arm_act:  # position servos -> torque motors
            m.actuator_gainprm[a, :] = 0.0
            m.actuator_gainprm[a, 0] = 1.0
            m.actuator_biasprm[a, :] = 0.0
            m.actuator_ctrlrange[a] = m.actuator_forcerange[a]
        m.body_gravcomp[:] = 0.0
        self._tau_max = m.actuator_forcerange[self.sim.arm_act, 1].copy()
        q0 = np.zeros(6)  # calibrated zero = folded "sit-down" pose, like after power-up
        self.sim.reset(q0, self._deg_to_finger(self.open_deg))
        self._lock = threading.Lock()
        # Until the first command the motors hold the start pose softly.
        self._frame = [(float(q), 0.0, 20.0, 2.0, 0.0) for q in q0]
        self._grip_target = self._deg_to_finger(self.open_deg)
        self._grip_enabled = True
        self.n_mit_frames = 0
        self.motors = {n: _FakeMotor(self, i) for i, n in enumerate(JOINT_NAMES)}
        self.motors["gripper"] = _FakeGripperMotor(self)
        self._stop = threading.Event()
        self._thread = None
        self.is_connected = False

    # ---- unit conversion -----------------------------------------------------
    def _deg_to_finger(self, deg):
        closing = (deg - self.open_deg) / (self.closed_deg - self.open_deg)
        return GRIPPER_MAX * (1.0 - float(np.clip(closing, 0.0, 1.0)))

    def _finger_to_deg(self, finger):
        closing = 1.0 - float(np.clip(finger / GRIPPER_MAX, 0.0, 1.0))
        return self.open_deg + closing * (self.closed_deg - self.open_deg)

    # ---- lerobot-like API -------------------------------------------------------
    def connect(self, calibrate: bool = False):
        self.is_connected = True
        self._thread = threading.Thread(target=self._physics, daemon=True)
        self._thread.start()

    @property
    def is_calibrated(self):
        return True

    def _present_pos(self, states=None):
        with self._lock:
            q = self.sim.q_arm.copy()
            finger = self.sim.gripper
        pos = {n: float(np.degrees(v)) for n, v in zip(JOINT_NAMES, q)}
        pos["gripper"] = self._finger_to_deg(finger)
        return pos

    def get_observation(self):
        return {f"{k}.pos": v for k, v in self._present_pos().items()}

    def _send_joint(self, motor_name, position_deg, state=None):
        if motor_name == "gripper":
            lo, hi = self._joint_limits["gripper"]
            self._grip_target = self._deg_to_finger(float(np.clip(position_deg, lo, hi)))
        else:  # position-hold for an arm joint (not used in MIT mode)
            i = JOINT_NAMES.index(motor_name)
            self.motors[motor_name].send_mit(np.radians(position_deg), 0.0, 40.0, 2.5, 0.0)
        return position_deg

    def send_action(self, action):
        for name in JOINT_NAMES:
            if f"{name}.pos" in action:
                self._send_joint(name, action[f"{name}.pos"])
        if "gripper.pos" in action:
            self._send_joint("gripper", action["gripper.pos"])
        return action

    def disconnect(self):
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)
        self.is_connected = False

    # ---- 1 kHz motor + physics loop -------------------------------------------
    def _physics(self):
        sim = self.sim
        m, d = sim.model, sim.data
        nxt = time.perf_counter()
        while not self._stop.is_set():
            with self._lock:
                for _ in range(5):  # 5 x 1 ms per wake-up
                    q, dq = d.qpos[sim.arm_qadr], d.qvel[sim.arm_dadr]
                    f = np.array(self._frame)
                    tau = f[:, 2] * (f[:, 0] - q) + f[:, 3] * (f[:, 1] - dq) + f[:, 4]
                    d.ctrl[sim.arm_act] = np.clip(tau, -self._tau_max, self._tau_max)
                    d.ctrl[sim.grip_act] = self._grip_target if self._grip_enabled else sim.gripper
                    mujoco.mj_step(m, d)
            nxt += 0.005
            sleep = nxt - time.perf_counter()
            if sleep > 0:
                time.sleep(sleep)
            else:
                nxt = time.perf_counter()
