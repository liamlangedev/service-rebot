"""Camera models and 3D geometry (numpy only).

Conventions
-----------
* World frame = robot base frame (metres): x forward, y left, z up.
* Cameras use the OpenCV convention: x right, y down, z forward (into the scene).
* ``T_world_cam`` is a 4x4 camera-to-world transform.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class CameraModel:
    name: str
    K: np.ndarray                    # 3x3 intrinsics
    T_world_cam: np.ndarray          # 4x4 camera-to-world
    width: int
    height: int
    dist: np.ndarray = field(default_factory=lambda: np.zeros(5))

    @property
    def R(self) -> np.ndarray:
        return self.T_world_cam[:3, :3]

    @property
    def center(self) -> np.ndarray:
        return self.T_world_cam[:3, 3]

    def project(self, pts_world: np.ndarray) -> np.ndarray:
        """Nx3 world points -> Nx2 pixels (NaN behind the camera). Ignores distortion."""
        pts = np.atleast_2d(np.asarray(pts_world, float))
        pc = (pts - self.center) @ self.R          # world -> camera (R^T (p - c))
        uv = np.full((len(pc), 2), np.nan)
        front = pc[:, 2] > 1e-6
        proj = (self.K @ pc[front].T).T
        uv[front] = proj[:, :2] / proj[:, 2:3]
        return uv

    def undistort(self, uv) -> np.ndarray:
        """Removes lens distortion from a pixel (no-op for ideal/sim cameras)."""
        if not np.any(self.dist):
            return np.asarray(uv, float)
        import cv2
        pt = np.array([[uv]], np.float64)
        return cv2.undistortPoints(pt, self.K, self.dist, P=self.K)[0, 0]

    def ray(self, uv) -> tuple[np.ndarray, np.ndarray]:
        """Pixel -> (origin, unit direction) in world."""
        u, v = self.undistort(uv)
        d_cam = np.linalg.solve(self.K, np.array([u, v, 1.0]))
        d = self.R @ d_cam
        return self.center.copy(), d / np.linalg.norm(d)

    def to_dict(self) -> dict:
        return {"K": self.K.tolist(), "T_world_cam": self.T_world_cam.tolist(),
                "width": self.width, "height": self.height, "dist": self.dist.tolist()}

    @classmethod
    def from_dict(cls, name: str, d: dict) -> "CameraModel":
        return cls(name, np.array(d["K"], float), np.array(d["T_world_cam"], float),
                   int(d["width"]), int(d["height"]), np.array(d.get("dist", [0] * 5), float))


def intrinsics_from_fovy(fovy_deg: float, width: int, height: int) -> np.ndarray:
    f = 0.5 * height / np.tan(np.radians(fovy_deg) / 2)
    return np.array([[f, 0, width / 2], [0, f, height / 2], [0, 0, 1.0]])


def make_T(R: np.ndarray, t: np.ndarray) -> np.ndarray:
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t
    return T


def ray_plane_z(origin, direction, z: float):
    """Intersection of a ray with the horizontal plane at height z (None if parallel/behind)."""
    if abs(direction[2]) < 1e-9:
        return None
    s = (z - origin[2]) / direction[2]
    return None if s <= 0 else origin + s * direction


def triangulate_rays(origins, directions) -> tuple[np.ndarray, float]:
    """Least-squares point closest to all rays; returns (point, rms distance to rays)."""
    A = np.zeros((3, 3))
    b = np.zeros(3)
    for o, d in zip(origins, directions):
        P = np.eye(3) - np.outer(d, d)
        A += P
        b += P @ o
    p = np.linalg.lstsq(A, b, rcond=None)[0]
    res = [np.linalg.norm((np.eye(3) - np.outer(d, d)) @ (p - o)) for o, d in zip(origins, directions)]
    return p, float(np.sqrt(np.mean(np.square(res))))


def top_down_rotation(yaw: float) -> np.ndarray:
    """Tool frame for a top-down grasp on the reBot.

    The gripper's approach axis is the end_link +x (pointing down here) and the
    fingers slide along end_link +y, which is set to (cos yaw, sin yaw, 0).
    """
    x = np.array([0.0, 0.0, -1.0])
    y = np.array([np.cos(yaw), np.sin(yaw), 0.0])
    return np.column_stack([x, y, np.cross(x, y)])


def wrap_half_pi(a: float) -> float:
    """Wraps an angle to [-pi/2, pi/2): a parallel gripper is symmetric under 180 deg."""
    return (a + np.pi / 2) % np.pi - np.pi / 2


def rot_angle(R1: np.ndarray, R2: np.ndarray) -> float:
    c = (np.trace(R1.T @ R2) - 1) / 2
    return float(np.arccos(np.clip(c, -1, 1)))


def grasp_rotation(approach, finger_dir) -> np.ndarray:
    """Tool frame with the approach axis (end_link +x) along `approach` and the fingers
    sliding as close as possible to the horizontal `finger_dir`."""
    x = np.asarray(approach, float)
    x = x / np.linalg.norm(x)
    y = np.asarray(finger_dir, float) - np.dot(finger_dir, x) * x
    y = y / np.linalg.norm(y)
    return np.column_stack([x, y, np.cross(x, y)])


def tilted_approach(azimuth: float, tilt: float) -> np.ndarray:
    """Downward approach leaning `tilt` rad away from the robot along `azimuth`
    (tilt=0 is straight down). Tilting extends the reach for far objects."""
    return np.array([np.sin(tilt) * np.cos(azimuth), np.sin(tilt) * np.sin(azimuth), -np.cos(tilt)])
