"""Conversion between the MuJoCo model and LeRobot's `rebot_b601_follower`.

LeRobot (lerobot>=0.7, robots/rebot_b601_follower) talks to the real arm in
"public joint degrees": one `<name>.pos` value per motor, zero at the
calibrated zero pose (the folded "sit-down" pose, gripper closed). Its DM
soft limits match the team's follower.json.

The MJCF joints share that zero pose and sign convention (joint2/joint3 are
negative-only in both), so arm joints map as degrees(qpos). The gripper motor
runs 0 (closed) .. -270 deg (open); we map it linearly onto the simulated
finger travel 0 .. GRIPPER_MAX m.

Verify on hardware before trusting it: read `get_observation()` with the arm
in a few poses and compare against `lerobot_to_sim()` in the viewer.
"""
import numpy as np

from teleop.rebot_model import GRIPPER_MAX

ROBOT_TYPE = "rebot_b601_follower"
JOINT_NAMES = ["shoulder_pan", "shoulder_lift", "elbow_flex",
               "wrist_flex", "wrist_yaw", "wrist_roll", "gripper"]
FEATURE_NAMES = [f"{n}.pos" for n in JOINT_NAMES]
GRIPPER_OPEN_DEG = -270.0


def sim_to_lerobot(q_arm: np.ndarray, finger_m: float) -> np.ndarray:
    """MuJoCo (6 joint rad, finger m) -> 7 LeRobot values in degrees."""
    grip = GRIPPER_OPEN_DEG * np.clip(finger_m / GRIPPER_MAX, 0.0, 1.0)
    return np.concatenate([np.degrees(q_arm), [grip]])


def lerobot_to_sim(values) -> tuple[np.ndarray, float]:
    """7 LeRobot values (array, or dict keyed by FEATURE_NAMES) -> (q_arm rad, finger m)."""
    if isinstance(values, dict):
        values = [values[k] for k in FEATURE_NAMES]
    values = np.asarray(values, dtype=float)
    return np.radians(values[:6]), GRIPPER_MAX * float(np.clip(values[6] / GRIPPER_OPEN_DEG, 0, 1))


def to_action_dict(values: np.ndarray) -> dict[str, float]:
    return {k: float(v) for k, v in zip(FEATURE_NAMES, values)}
