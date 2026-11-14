"""Glue between the MuJoCo model (radians, joint1..6) and lerobot's reBot B601
follower (degrees, named joints), plus the safe "ready" pose and guards."""
import mujoco
import numpy as np

JOINT_NAMES = ["shoulder_pan", "shoulder_lift", "elbow_flex",
               "wrist_flex", "wrist_yaw", "wrist_roll"]

# Gripper pointing straight down in front of the base, TCP ~(0.25, 0, 0.25) m.
# Found with DiffIK; the Jacobian is well conditioned here (sigma_min ~0.15),
# unlike the folded start pose.
READY_QPOS = np.array([0.0, -1.51, -1.30, 1.36, 0.0, 0.0])

# Gripper joint, degrees in lerobot's public frame (range -270..0); verified on the arm.
GRIPPER_OPEN_DEG = -270.0
GRIPPER_CLOSED_DEG = 0.0


def q_to_action(q: np.ndarray, gripper_deg: float) -> dict[str, float]:
    action = {f"{n}.pos": float(np.degrees(v)) for n, v in zip(JOINT_NAMES, q)}
    action["gripper.pos"] = float(gripper_deg)
    return action


def obs_to_q(obs: dict) -> np.ndarray:
    return np.radians([obs[f"{n}.pos"] for n in JOINT_NAMES])


def gripper_from_closing(closing: float) -> float:
    """closing: 0 = open, 1 = closed -> gripper degrees."""
    closing = float(np.clip(closing, 0.0, 1.0))
    return GRIPPER_OPEN_DEG + closing * (GRIPPER_CLOSED_DEG - GRIPPER_OPEN_DEG)


def joint_space_path(q_from: np.ndarray, q_to: np.ndarray, max_speed: float, rate: float):
    """Straight line in joint space (MoveJ) at the speed of the slowest-limited
    joint, with a smooth start/stop. Yields one waypoint per tick."""
    dist = float(np.max(np.abs(q_to - q_from)))
    n = max(2, int(np.ceil(dist / max_speed * rate * 1.5)))
    for i in range(1, n + 1):
        s = i / n
        s = s * s * (3 - 2 * s)  # smoothstep
        yield q_from + s * (q_to - q_from)


def sigma_min(ik, q: np.ndarray) -> float:
    """Smallest singular value of the TCP position Jacobian (m/rad)."""
    ik._fk(q)
    mujoco.mj_jacSite(ik.model, ik.data, ik._jacp, ik._jacr, ik.site)
    return float(np.linalg.svd(ik._jacp[:, ik.dadr], compute_uv=False)[-1])


def guarded_solve(ik, q_prev, target_pos, target_rot, dt, min_sigma: float = 0.04):
    """ik.solve, but refuses steps that move deeper into a singularity."""
    q, pe, re = ik.solve(q_prev, target_pos, target_rot, dt)
    s_new = sigma_min(ik, q)
    if s_new < min_sigma and s_new < sigma_min(ik, q_prev):
        return np.asarray(q_prev, dtype=float).copy(), pe, re, True
    return q, pe, re, False
