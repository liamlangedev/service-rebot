"""One control tick from controller sample to joint command, shared by sim and real.

  EEController (A/B, grip clutch, precision, gripper, roll)
    -> wrist pivot: hand rotations become wrist-joint rotations (the reBot's
       wrist axes sit 12-23 cm behind the fingertips; rotating about the
       fingertips would swing the whole arm)
    -> wrist-limit guard: a rotation that needs a wrist joint past its limit is
       held back (the gripper waits at the limit until your hand comes back)
       instead of being reached by folding the shoulder/elbow
    -> dev/roboCrafy's singularity-guarded IK on the fingertip (grasp) point
    -> runaway brake: the target never gets more than 5 cm ahead of the arm

Seen on the real arm without the pivot and the guard: wrist_flex sat at its
+90 deg limit 45% of the time while the elbow folded to -160 deg.
"""
import numpy as np

from teleop.ee_control import EEController, orthonormalize, wrist_pivot_shift
from teleop.ik import DiffIK
from teleop.rebot_model import ARM_JOINTS, GRASP_SITE
from teleop.rebot_real import JOINT_NAMES, guarded_solve

RUNAWAY_M = 0.05                 # target further than this from the arm -> snap back
WRIST_JOINTS = (3, 4, 5)         # wrist_flex, wrist_yaw, wrist_roll
WRIST_MARGIN = np.radians(3.0)   # "at the limit" band


def wrist_at_limit(ik, q_prev, q_new):
    """Index of a wrist joint in its limit band that is not moving out of it."""
    for j in WRIST_JOINTS:
        d_new = min(q_new[j] - ik.lo[j], ik.hi[j] - q_new[j])
        d_old = min(q_prev[j] - ik.lo[j], ik.hi[j] - q_prev[j])
        if d_new < WRIST_MARGIN and d_new <= d_old + 1e-4:
            return j
    return None


class ArmStep:
    def __init__(self, ctrl_cfg, model, q_start, gripper_m, q_rest, args, log=print):
        self.ik = DiffIK(model, GRASP_SITE, ARM_JOINTS, q_rest=q_rest,
                         max_joint_vel=args.max_joint_vel,
                         min_rot_weight=None if args.strict_rotation else 0.05)
        self.q = np.array(q_start, dtype=float)
        pos, rot = self.ik.fk(self.q)
        self.ctrl = EEController(ctrl_cfg, pos, rot, gripper=gripper_m, hand=args.hand, log=log)
        if getattr(args, "wrist_pivot", True):
            self.ctrl.pivot_fn = lambda ro, rn: wrist_pivot_shift(self.ik, self.q, ro, rn)
        self.wrist_guard = getattr(args, "wrist_guard", True)
        self.log = log
        self.blocked = False
        self.wrist_limited = None
        self.rot_debt = np.eye(3)  # hand rotation held back at a wrist limit
        self.pos_err = 0.0
        self.rot_err = 0.0

    def update(self, s, dt: float):
        """One tick. Returns (q_cmd rad, finger opening m)."""
        prev_rot = np.array(self.ctrl.target[1])
        target_pos, target_rot, finger = self.ctrl.update(s, dt)
        if not self.ctrl.moving:
            self.rot_debt = np.eye(3)
        want = orthonormalize(np.asarray(target_rot) @ prev_rot.T @ self.rot_debt)
        if self.wrist_guard and not np.allclose(want, np.eye(3), atol=1e-9):
            base_pos = self.ctrl.pivot_correct(target_pos, target_rot, prev_rot)  # undo tick
            try_rot = orthonormalize(want @ prev_rot)
            try_pos = self.ctrl.pivot_correct(base_pos, prev_rot, try_rot)
            q, pe, re, blocked = guarded_solve(self.ik, self.q, try_pos, try_rot, dt)
            j = wrist_at_limit(self.ik, self.q, q)
            if j is None:
                target_pos, target_rot, self.rot_debt = try_pos, try_rot, np.eye(3)
                self.wrist_limited = None
            else:
                target_pos, target_rot, self.rot_debt = base_pos, prev_rot, want
                q, pe, re, blocked = guarded_solve(self.ik, self.q, target_pos, target_rot, dt)
                if self.wrist_limited != j:
                    self.log(f"[arm] {JOINT_NAMES[j]} at its limit: rotation waits there "
                             "until you rotate back")
                self.wrist_limited = j
            self.ctrl.target = (np.asarray(target_pos), np.asarray(target_rot))
        else:
            q, pe, re, blocked = guarded_solve(self.ik, self.q, target_pos, target_rot, dt)
        if blocked and not self.blocked:
            self.log("[arm] IK step refused: it would move into a singularity (arm holds)")
        self.blocked = blocked
        self.q = q
        self.pos_err, self.rot_err = pe, re
        if self.ctrl.moving:  # (a deliberate far target, e.g. "go home", is allowed)
            arm_pos, _ = self.ik.fk(q)
            if np.linalg.norm(np.asarray(target_pos) - arm_pos) > RUNAWAY_M:
                self.ctrl.resync(arm_pos, target_rot)
        return q, finger

    def reset_to(self, q, gripper_m=None):
        """Re-anchor on a joint configuration (disarms)."""
        self.q = np.array(q, dtype=float)
        pos, rot = self.ik.fk(self.q)
        self.ctrl.disarm(" (resync)")
        self.ctrl.resync(pos, rot, gripper_m)
        self.rot_debt = np.eye(3)
