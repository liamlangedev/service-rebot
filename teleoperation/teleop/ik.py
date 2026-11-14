"""Damped-least-squares differential IK for the reBot arm's TCP site.

It runs on a private MjData copy, so it can drive the simulator or (later) the
real arm: give it a target pose plus the last joint command and it returns the
next joint command.
"""
import mujoco
import numpy as np


class DiffIK:
    def __init__(self, model: mujoco.MjModel, site: str, joints: list[str],
                 q_rest: np.ndarray, damping: float = 0.05, rot_weight: float = 0.5,
                 posture_gain: float = 0.05, iters: int = 5,
                 max_joint_vel: float = 2.0, min_rot_weight: float | None = None,
                 pos_tol: tuple[float, float] = (0.003, 0.015)):
        self.model = model
        self.data = mujoco.MjData(model)
        self.site = model.site(site).id
        self.qadr = np.array([model.joint(j).qposadr[0] for j in joints])
        self.dadr = np.array([model.joint(j).dofadr[0] for j in joints])
        self.lo = np.array([model.joint(j).range[0] for j in joints])
        self.hi = np.array([model.joint(j).range[1] for j in joints])
        self.q_rest = np.asarray(q_rest, dtype=float)
        self.damping = damping
        self.rot_weight = rot_weight
        self.posture_gain = posture_gain
        self.iters = iters
        self.max_joint_vel = max_joint_vel
        # Adaptive orientation weight: when the full-weight solution misses the
        # position by more than pos_tol[0] (the requested orientation is out of
        # reach there, e.g. a level tool near the table), the rotation weight is
        # lowered towards min_rot_weight (reached at pos_tol[1]) so the TCP
        # still gets there and the tool tilts as little as needed.
        self.min_rot_weight = min_rot_weight
        self.pos_tol = pos_tol
        self._jacp = np.zeros((3, model.nv))
        self._jacr = np.zeros((3, model.nv))

    def _fk(self, q):
        self.data.qpos[self.qadr] = q
        mujoco.mj_kinematics(self.model, self.data)
        mujoco.mj_comPos(self.model, self.data)
        return (self.data.site_xpos[self.site].copy(),
                self.data.site_xmat[self.site].reshape(3, 3).copy())

    def solve(self, q_prev: np.ndarray, target_pos: np.ndarray,
              target_rot: np.ndarray | None, dt: float):
        """Returns (q_cmd, pos_err_norm, rot_err_norm).

        target_rot=None tracks position only (orientation is left free).
        The step from q_prev is clipped to max_joint_vel * dt.
        """
        q = self._iterate(np.array(q_prev, dtype=float), target_pos, target_rot, self.rot_weight)
        if target_rot is not None and self.min_rot_weight is not None:
            miss = np.linalg.norm(target_pos - self._fk(q)[0])
            lo, hi = self.pos_tol
            if miss > lo:
                a = min(1.0, (miss - lo) / (hi - lo))
                w = (1 - a) * self.rot_weight + a * self.min_rot_weight
                q = self._iterate(np.array(q_prev, dtype=float), target_pos, target_rot, w)

        step = np.clip(q - q_prev, -self.max_joint_vel * dt, self.max_joint_vel * dt)
        q = np.clip(q_prev + step, self.lo, self.hi)
        pos, rot = self._fk(q)
        rot_err = np.linalg.norm(_rot_error(target_rot, rot)) if target_rot is not None else 0.0
        return q, float(np.linalg.norm(target_pos - pos)), float(rot_err)

    def _iterate(self, q, target_pos, target_rot, rot_weight):
        """self.iters damped-least-squares steps from q (no velocity limit)."""
        n = len(q)
        for _ in range(self.iters):
            pos, rot = self._fk(q)
            mujoco.mj_jacSite(self.model, self.data, self._jacp, self._jacr, self.site)
            err_p = target_pos - pos
            if target_rot is not None:
                err_r = _rot_error(target_rot, rot)
                J = np.vstack([self._jacp[:, self.dadr],
                               rot_weight * self._jacr[:, self.dadr]])
                err = np.concatenate([err_p, rot_weight * err_r])
            else:
                J = self._jacp[:, self.dadr]
                err = err_p
            JJt = J @ J.T + (self.damping ** 2) * np.eye(J.shape[0])
            J_pinv = J.T @ np.linalg.solve(JJt, np.eye(J.shape[0]))
            dq = J_pinv @ err
            # Pull towards the rest posture in the Jacobian's null space.
            dq += (np.eye(n) - J_pinv @ J) @ (self.posture_gain * (self.q_rest - q))
            q = np.clip(q + dq, self.lo, self.hi)
        return q

    def fk(self, q):
        return self._fk(np.asarray(q, dtype=float))


def _rot_error(target_rot, rot):
    """Axis-angle vector (world frame) rotating `rot` onto `target_rot`."""
    quat = np.empty(4)
    mujoco.mju_mat2Quat(quat, (target_rot @ rot.T).reshape(-1))
    vel = np.empty(3)
    mujoco.mju_quat2Vel(vel, quat, 1.0)
    return vel
