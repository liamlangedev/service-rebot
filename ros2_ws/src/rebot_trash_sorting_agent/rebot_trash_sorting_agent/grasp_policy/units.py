"""ROS joint units <-> the units the policy was trained in (rebot_sort_v1, lerobot degrees).

Arm: the dataset's six joints are lerobot degrees of joint1..joint6 in the same zero and
sign as the URDF (checked: every dataset episode starts at motion.yaml's `ready` pose,
[0, -1.51, -1.30, 1.36, 0, 0] rad, to within 0.5 deg). So deg = degrees(rad).

Gripper: raw gripper degrees depend on each arm's calibration (the dataset arm reads
-365 open / -5 closed; this repo's arm, re-measured 2026-11-15, -370 / 0), so the gripper goes through a
normalised opening: ROS finger_left metres -> fraction open -> dataset degrees.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

ARM_JOINTS = ("joint1", "joint2", "joint3", "joint4", "joint5", "joint6")


@dataclass(frozen=True)
class GripperMap:
    ros_open_m: float = 0.05
    ros_closed_m: float = 0.0
    data_open_deg: float = -365.0
    data_closed_deg: float = -5.0

    def opening(self, finger_m: float) -> float:
        """finger_left metres -> 0 (closed) .. 1 (open), clipped."""
        span = self.ros_open_m - self.ros_closed_m
        return float(np.clip((finger_m - self.ros_closed_m) / span, 0.0, 1.0))

    def to_data(self, finger_m: float) -> float:
        o = self.opening(finger_m)
        return self.data_closed_deg + o * (self.data_open_deg - self.data_closed_deg)

    def to_ros(self, data_deg: float) -> float:
        span = self.data_open_deg - self.data_closed_deg
        o = float(np.clip((data_deg - self.data_closed_deg) / span, 0.0, 1.0))
        return self.ros_closed_m + o * (self.ros_open_m - self.ros_closed_m)

    def data_is_closed(self, data_deg: float, threshold: float = 0.3) -> bool:
        """A command below `threshold` opening counts as 'close'."""
        span = self.data_open_deg - self.data_closed_deg
        return (data_deg - self.data_closed_deg) / span < threshold


def ros_to_data(arm_rad: np.ndarray, finger_m: float, gmap: GripperMap) -> np.ndarray:
    """(6 arm joints [rad], finger_left [m]) -> 7-D dataset state [deg]."""
    out = np.empty(7, dtype=np.float32)
    out[:6] = np.degrees(np.asarray(arm_rad, dtype=np.float64))
    out[6] = gmap.to_data(finger_m)
    return out


def data_to_ros(action: np.ndarray, gmap: GripperMap) -> tuple[np.ndarray, float]:
    """7-D dataset action [deg] -> (6 arm joints [rad], finger_left [m])."""
    action = np.asarray(action, dtype=np.float64)
    return np.radians(action[:6]), gmap.to_ros(float(action[6]))
