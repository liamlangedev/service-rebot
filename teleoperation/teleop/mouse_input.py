"""Mouse teleop through the MuJoCo viewer's perturbation ("grab and drag").

Double-click any part of the arm to select it, then:
  Ctrl + right-drag   move the TCP target
  Ctrl + left-drag    rotate the TCP target

The viewer would normally push the selected link with a spring force, which
fights the position servos. Instead we read the drag from the viewer's
MjvPerturb and apply it to the IK target, clutch-style (relative to where the
drag started), and cancel the viewer's force on the arm.
"""
import mujoco
import numpy as np


def _quat2mat(quat):
    mat = np.empty(9)
    mujoco.mju_quat2Mat(mat, quat)
    return mat.reshape(3, 3)


class MouseDragTeleop:
    def __init__(self, model: mujoco.MjModel, root_body: str = "link1"):
        root = model.body(root_body).id
        # Every body in the arm's kinematic subtree (links, gripper, fingers).
        self.arm_bodies = {b for b in range(model.nbody)
                           if b == root or _is_descendant(model, b, root)}
        self._anchor = None  # (active mode, refselpos0, refquat0, target_pos0, target_rot0)

    @property
    def engaged(self):
        return self._anchor is not None

    def update(self, pert: mujoco.MjvPerturb, target_pos, target_rot):
        """Returns the new (target_pos, target_rot)."""
        active = int(pert.active)
        if not active or pert.select not in self.arm_bodies:
            self._anchor = None
            return target_pos, target_rot

        if self._anchor is None or self._anchor[0] != active:
            # New drag (or switched between move and rotate): re-anchor.
            self._anchor = (active, pert.refselpos.copy(), pert.refquat.copy(),
                            np.array(target_pos), np.array(target_rot))

        _, sel0, quat0, pos0, rot0 = self._anchor
        pos, rot = pos0, rot0
        if active & mujoco.mjtPertBit.mjPERT_TRANSLATE:
            pos = pos0 + (pert.refselpos - sel0)
        if active & mujoco.mjtPertBit.mjPERT_ROTATE:
            rot = _quat2mat(pert.refquat) @ _quat2mat(quat0).T @ rot0
        return pos, rot

    def cancel_forces(self, data: mujoco.MjData):
        """Removes the viewer's perturbation force from the arm bodies."""
        data.xfrc_applied[list(self.arm_bodies)] = 0.0


def _is_descendant(model, body, root):
    while body != 0:
        if body == root:
            return True
        body = model.body_parentid[body]
    return False
