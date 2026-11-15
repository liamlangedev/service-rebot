"""Camera calibration math shared by the device UI and the capture session.

Lens (intrinsics) files: rebot_sim/calibration/<role>.json, from the device UI's
board calibration. Poses: from a ChArUco board at a known spot on the table
(fixed cameras), or board + arm forward kinematics (wrist camera, hand-eye).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from capture.devices import SIM_DIR  # noqa: F401  (sets sys.path)
from rebot_sim.scene import PKG_DIR

CALIB_DIR = PKG_DIR / "calibration"
CV_TO_MJ = np.diag([1.0, -1.0, -1.0])  # OpenCV cam (x right, y down, z fwd) -> MuJoCo (y up, z back)


# ----------------------------------------------------------------- intrinsics
def K_from_fovy(fovy_deg: float, size: tuple[int, int]) -> np.ndarray:
    w, h = size
    f = h / 2 / np.tan(np.radians(fovy_deg) / 2)
    return np.array([[f, 0, w / 2], [0, f, h / 2], [0, 0, 1.0]])


def fovy_from_K(K: np.ndarray, size: tuple[int, int]) -> float:
    return float(np.degrees(2 * np.arctan(size[1] / 2 / K[1, 1])))


def save_intrinsics(role: str, K, dist, size, rms, n_views) -> Path:
    CALIB_DIR.mkdir(parents=True, exist_ok=True)
    path = CALIB_DIR / f"{role}.json"
    path.write_text(json.dumps({
        "role": role, "image_size": list(size), "K": np.asarray(K).tolist(),
        "dist": np.asarray(dist).reshape(-1).tolist(), "rms_px": rms, "views": n_views,
        "fovy_deg": fovy_from_K(np.asarray(K), size),
        "saved": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=2) + "\n")
    return path


def load_intrinsics(role: str, size: tuple[int, int], fallback_fovy: float):
    """(K, dist, source) scaled to `size`; falls back to the sim's pinhole."""
    path = CALIB_DIR / f"{role}.json"
    if path.exists():
        d = json.loads(path.read_text())
        K = np.array(d["K"], float)
        sx, sy = size[0] / d["image_size"][0], size[1] / d["image_size"][1]
        K[0] *= sx
        K[1] *= sy
        return K, np.array(d["dist"], float), f"lens calibration ({path.name})"
    return K_from_fovy(fallback_fovy, size), np.zeros(5), "sim fovy (no lens calibration yet)"


# ----------------------------------------------------------------- poses
def lookat_R(pos, target, up=(0, 0, 1.0)) -> np.ndarray:
    """MuJoCo camera orientation (columns x, y, z; looks along -z) at pos facing target."""
    z = np.asarray(pos, float) - np.asarray(target, float)
    z /= np.linalg.norm(z)
    x = np.cross(up, z)
    x /= np.linalg.norm(x)
    return np.column_stack([x, np.cross(z, x), z])


def lookat_roll(R_mj: np.ndarray, pos: np.ndarray, plane_z: float | None = None,
                up=(0, 0, 1.0), dist: float = 0.3):
    """Express a camera orientation as (look_at point, roll_deg), the way
    rebot_sim.scene._camera_quat rebuilds it."""
    fwd = -R_mj[:, 2]
    t = dist
    if plane_z is not None and fwd[2] < -1e-3:
        t = (plane_z - pos[2]) / fwd[2]
    target = pos + t * fwd
    L = lookat_R(pos, target, up)
    roll = np.degrees(np.arctan2(R_mj[:, 0] @ L[:, 1], R_mj[:, 0] @ L[:, 0]))
    return target, float(roll)


def rot_angle_deg(Ra: np.ndarray, Rb: np.ndarray) -> float:
    c = (np.trace(Ra.T @ Rb) - 1) / 2
    return float(np.degrees(np.arccos(np.clip(c, -1, 1))))


def mean_rotation(Rs: list[np.ndarray]) -> np.ndarray:
    U, _, Vt = np.linalg.svd(sum(Rs))
    R = U @ Vt
    if np.linalg.det(R) < 0:
        U[:, -1] *= -1
        R = U @ Vt
    return R


def fixed_camera_entry(ws, R_mj_world, C_world, fovy_deg) -> dict:
    """real_setup.json camera fields from a world-frame pose."""
    target, roll = lookat_roll(R_mj_world, C_world, plane_z=ws.table_z)
    pos_ws, look_ws = ws.from_world(C_world), ws.from_world(target)
    return {"from_left": round(pos_ws[0], 4), "from_near": round(pos_ws[1], 4),
            "height": round(pos_ws[2], 4), "look_at": [round(v, 4) for v in look_ws],
            "roll_deg": round(roll, 2), "fovy": round(fovy_deg, 2)}


def wrist_camera_entry(R_mj_ee, t_ee, fovy_deg) -> dict:
    target, roll = lookat_roll(R_mj_ee, t_ee, dist=0.1)
    return {"pos": [round(v, 4) for v in t_ee], "look_at": [round(v, 4) for v in target],
            "roll_deg": round(roll, 2), "fovy": round(fovy_deg, 2)}
