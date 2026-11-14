"""One arm interface, two backends: SimArm (MuJoCo physics) and RealArm (LeRobot driver).

Skills only call the methods of ``Arm``: they never know which backend runs. Motion is
planned here (IK + min-jerk time scaling), checked by ``Safety`` and then streamed by the
backend at a fixed rate.
"""
from __future__ import annotations

import time

import mujoco
import numpy as np

from autonomy.geometry import top_down_rotation
from autonomy.safety import EStopped, Safety, SafetyError
from teleop.ik import DiffIK
from teleop.rebot_model import ARM_JOINTS, GRIPPER_MAX, HOME_QPOS, TCP_SITE, RebotSim

# The fingertips sit 10.5 cm beyond the `tcp` site along the approach axis (end_link
# +x); the middle of the finger pads is about 9 cm beyond it.
TIP_OFFSET = 0.105
PAD_OFFSET = 0.090

# Folded back and turned aside so the fixed cameras see the whole table.
OBSERVE_QPOS = np.radians([120.0, -90.0, -60.0, 0.0, 0.0, 0.0])


class Arm:
    rate = 100.0

    def __init__(self, sim: RebotSim, safety: Safety, max_joint_vel: float):
        self.sim = sim
        self.safety = safety
        self.max_joint_vel = max_joint_vel
        m = sim.model
        # Precise offline IK (no posture pull) for goal poses; the teleop IK is tuned
        # for smooth streaming instead.
        self._ik = DiffIK(m, TCP_SITE, ARM_JOINTS, q_rest=HOME_QPOS, damping=0.02,
                          posture_gain=0.0, iters=1)
        self._ik_rest = DiffIK(m, TCP_SITE, ARM_JOINTS, q_rest=HOME_QPOS, iters=1)
        self.q_cmd = None
        self.grip_cmd = GRIPPER_MAX

    # ---- backend hooks --------------------------------------------------------------
    @property
    def q(self) -> np.ndarray:
        raise NotImplementedError

    @property
    def gripper(self) -> float:
        """Measured finger opening [m] (0 closed .. GRIPPER_MAX open)."""
        raise NotImplementedError

    def _stream(self, qs: list[np.ndarray], grips: list[float]):
        raise NotImplementedError

    def close(self):
        pass

    # ---- kinematics -----------------------------------------------------------------
    def fk(self, q=None):
        return self._ik.fk(self.q if q is None else q)

    def fk_tip(self, q):
        pos, rot = self.fk(q)
        return pos, pos + TIP_OFFSET * rot[:, 0]

    def solve_ik(self, pos, rot, q_seed=None, tol_mm=1.0, tol_deg=1.0):
        """Returns (q, ok). Tries the seed first, then a few standard seeds."""
        seeds = [self.q if q_seed is None else q_seed, HOME_QPOS,
                 np.radians([0, -100, -100, 60, 0, 0])]
        best = None
        for seed in seeds:
            q = np.array(seed, float)
            for _ in range(60):          # pull towards a comfortable posture first
                q, ep, er = self._ik_rest.solve(q, pos, rot, 1.0)
            for _ in range(200):
                q, ep, er = self._ik.solve(q, pos, rot, 1.0)
                if ep * 1000 < tol_mm and np.degrees(er) < tol_deg:
                    return q, True
            if best is None or ep < best[1]:
                best = (q, ep)
        return best[0], False

    # ---- motion ---------------------------------------------------------------------
    def move_joints(self, q_goal, gripper: float | None = None, speed: float = 1.0):
        q0 = self.q_cmd if self.q_cmd is not None else self.q
        q_goal = np.asarray(q_goal, float)
        g0 = self.grip_cmd
        g1 = g0 if gripper is None else float(np.clip(gripper, 0, GRIPPER_MAX))
        vmax = self.max_joint_vel * speed
        dist = float(np.max(np.abs(q_goal - q0)))
        T = max(0.3, 1.875 * dist / vmax)        # min-jerk peak velocity = 1.875 * mean
        n = max(2, int(T * self.rate))
        s = np.linspace(0, 1, n)
        s = 10 * s**3 - 15 * s**4 + 6 * s**5
        qs = [q0 + si * (q_goal - q0) for si in s]
        grips = [g0 + si * (g1 - g0) for si in s]
        self.safety.check_trajectory(qs, self.fk_tip)
        self._stream(qs, grips)

    def move_tcp(self, pos, rot, linear: bool = False, speed: float = 1.0, step: float = 0.01):
        """Moves the TCP to (pos, rot). linear=True follows a straight Cartesian line."""
        pos = np.asarray(pos, float)
        if not linear:
            q_goal, ok = self.solve_ik(pos, rot)
            if not ok:
                raise SafetyError(f"pose {np.round(pos, 3)} is not reachable")
            return self.move_joints(q_goal, speed=speed)
        q = self.q_cmd if self.q_cmd is not None else self.q
        p0, _ = self.fk(q)
        n = max(2, int(np.ceil(np.linalg.norm(pos - p0) / step)) + 1)
        waypoints = []
        for i, a in enumerate(np.linspace(0, 1, n)[1:]):
            q, ok = self.solve_ik(p0 + a * (pos - p0), rot, q_seed=q)
            if not ok:
                raise SafetyError(f"straight line to {np.round(pos, 3)} is not reachable")
            waypoints.append(q)
        q_start = self.q_cmd if self.q_cmd is not None else self.q
        vmax = self.max_joint_vel * speed * 0.5
        qs, grips = [], []
        prev = q_start
        for q in waypoints:
            k = max(1, int(np.ceil(np.max(np.abs(q - prev)) / (vmax / self.rate))))
            for a in np.linspace(0, 1, k + 1)[1:]:
                qs.append(prev + a * (q - prev))
                grips.append(self.grip_cmd)
            prev = q
        self.safety.check_trajectory(qs, self.fk_tip)
        self._stream(qs, grips)

    def set_gripper(self, width: float, settle: float = 0.6) -> float:
        """Commands the finger opening [m] and returns the measured one after settling."""
        q = self.q_cmd if self.q_cmd is not None else self.q
        g0, g1 = self.grip_cmd, float(np.clip(width, 0, GRIPPER_MAX))
        n = int(settle * self.rate)
        ramp = np.linspace(0, 1, max(2, n // 2))
        grips = [g0 + a * (g1 - g0) for a in ramp] + [g1] * (n - len(ramp))
        self._stream([q] * len(grips), grips)
        return self.gripper

    def observe_pose(self):
        """Moves out of the fixed cameras' view."""
        self.move_joints(OBSERVE_QPOS)

    def home(self):
        self.move_joints(HOME_QPOS)


class SimArm(Arm):
    """MuJoCo physics backend (also what tests and demos without hardware use)."""

    def __init__(self, safety: Safety, viewer: bool = False, max_joint_vel: float = 1.5,
                 realtime: bool | None = None):
        sim = RebotSim()
        super().__init__(sim, safety, max_joint_vel)
        self.n_sub = max(1, round(1.0 / self.rate / sim.model.opt.timestep))
        self.viewer = None
        self.realtime = viewer if realtime is None else realtime
        if viewer:
            import mujoco.viewer
            self.viewer = mujoco.viewer.launch_passive(sim.model, sim.data)
            self.viewer.cam.lookat[:] = [0.35, 0.0, 0.15]
            self.viewer.cam.distance = 1.2
        self.sim.reset(OBSERVE_QPOS)
        self.q_cmd = OBSERVE_QPOS.copy()
        self.settle(0.5)

    @property
    def q(self):
        return self.sim.q_arm

    @property
    def gripper(self):
        return self.sim.gripper

    def settle(self, seconds: float):
        q = self.q_cmd if self.q_cmd is not None else self.q
        self._stream([q] * int(seconds * self.rate), [self.grip_cmd] * int(seconds * self.rate))

    def _stream(self, qs, grips):
        m, d = self.sim.model, self.sim.data
        t_next = time.perf_counter()
        for i, (q, g) in enumerate(zip(qs, grips)):
            if self.safety.stopped:
                raise EStopped("E-stop during motion")
            self.sim.command(q, g)
            self.q_cmd, self.grip_cmd = np.array(q), float(g)
            for _ in range(self.n_sub):
                mujoco.mj_step(m, d)
            if self.viewer is not None and i % 2 == 0:
                if not self.viewer.is_running():
                    self.safety.estop("viewer closed")
                self.viewer.sync()
            if self.realtime:
                t_next += 1.0 / self.rate
                time.sleep(max(0.0, t_next - time.perf_counter()))

    def close(self):
        if self.viewer is not None:
            self.viewer.close()


class RealArm(Arm):
    """reBot B601-DM through LeRobot's rebot_b601_follower (UNTESTED ON HARDWARE).

    Streams joint targets at 50 Hz, mirrors the measured pose into MuJoCo (for FK and
    the wrist-camera pose), aborts if the arm stops tracking, and holds position on
    E-stop instead of disabling torque (the arm would fall).
    """
    rate = 50.0

    def __init__(self, safety: Safety, port: str, robot_id: str = "follower",
                 calibration_dir=None, max_joint_vel: float = 0.6, max_step_deg: float = 5.0):
        from teleop.real_robot import RealRebot
        sim = RebotSim()
        super().__init__(sim, safety, max_joint_vel)
        self.robot = RealRebot(port, robot_id, calibration_dir, max_step_deg)
        q, g = self.robot.read()
        self.q_cmd, self.grip_cmd = q.copy(), g
        self.sim.mirror(q, g)
        print(f"[real] connected, q = {np.round(np.degrees(q), 1)} deg, gripper {g * 1000:.1f} mm")

    @property
    def q(self):
        q, g = self.robot.read()
        self.sim.mirror(q, g)
        return q

    @property
    def gripper(self):
        return self.robot.read()[1]

    def _stream(self, qs, grips):
        dt = 1.0 / self.rate
        t_next = time.perf_counter()
        lim = np.radians(self.safety.cfg.max_tracking_error_deg)
        for q, g in zip(qs, grips):
            if self.safety.stopped:
                self._hold()
                raise EStopped("E-stop during motion")
            self.robot.send(np.asarray(q), float(g))
            self.q_cmd, self.grip_cmd = np.array(q), float(g)
            q_meas, g_meas = self.robot.read()
            self.sim.mirror(q_meas, g_meas)
            if np.max(np.abs(q_meas - q)) > lim:
                self._hold()
                raise SafetyError("arm is not tracking the command (blocked or collision?)")
            t_next += dt
            time.sleep(max(0.0, t_next - time.perf_counter()))

    def _hold(self):
        q, g = self.robot.read()
        self.robot.send(q, g)
        self.q_cmd, self.grip_cmd = q, g

    def close(self):
        print("[real] disconnecting: LeRobot disables torque, SUPPORT THE ARM")
        self.robot.close()


__all__ = ["Arm", "SimArm", "RealArm", "top_down_rotation", "TIP_OFFSET", "PAD_OFFSET",
           "OBSERVE_QPOS"]
