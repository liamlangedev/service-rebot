"""Relative (handoff-anchored) joint representation used by the variant-B grasp policy.

The anchor is the 7-D state (lerobot degrees) at the moment the classical stack hands the
arm to the policy. The six arm joints are expressed as offsets from it; the gripper stays
absolute, because "open"/"closed" means the same thing everywhere on the table.

The ROS node keeps a copy of these three functions (ros2_ws/.../grasp_policy/relative.py);
keep them in sync.
"""

from __future__ import annotations

import numpy as np

ARM = slice(0, 6)


def to_relative(x: np.ndarray, anchor: np.ndarray) -> np.ndarray:
    """State or action (…, 7) -> relative to the anchor (arm joints only)."""
    out = np.array(x, dtype=np.float32, copy=True)
    out[..., ARM] -= np.asarray(anchor, dtype=np.float32)[ARM]
    return out


def from_relative(x: np.ndarray, anchor: np.ndarray) -> np.ndarray:
    """Relative action (…, 7) -> absolute lerobot degrees."""
    out = np.array(x, dtype=np.float32, copy=True)
    out[..., ARM] += np.asarray(anchor, dtype=np.float32)[ARM]
    return out
