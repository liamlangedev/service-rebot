"""Quaternion helpers and the top-down tool orientation.

The SRDF chain tip is ``gripper_tcp``, which sits at the fingertips, 2.858 cm past
``end_link``. At the collision-free ready pose its orientation is a pure +90 deg
rotation about Y::

    q = (x=0, y=0.70711, z=0, w=0.70711)      # tool +x points down (-z)

That is the reference "tool straight down" orientation. A grasp adds a rotation
about the tool's approach axis (``yaw``); a bin release adds a lean about world X
(``tilt``), which is the only way the arm can reach over the rim.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

Quat = tuple[float, float, float, float]  # (x, y, z, w), ROS order

#: tool +x pointing straight down, fingers closing along world y
TOP_DOWN: Quat = (0.0, 0.7071067811865476, 0.0, 0.7071067811865476)


def quat_multiply(a: Quat, b: Quat) -> Quat:
    """a * b: rotate by b first, then by a."""
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
        aw * bw - ax * bx - ay * by - az * bz,
    )


def quat_axis(axis: str, radians: float) -> Quat:
    half = radians / 2.0
    s = math.sin(half)
    v = [0.0, 0.0, 0.0]
    v["xyz".index(axis.lower())] = s
    return (v[0], v[1], v[2], math.cos(half))


def quat_yaw(radians: float) -> Quat:
    return quat_axis("z", radians)


def rotate(q: Quat, v: tuple[float, float, float]) -> tuple[float, float, float]:
    """Rotate vector v by q (no matrix library needed)."""
    x, y, z, w = q
    # v' = q * v * q^-1, expanded
    tx = 2.0 * (y * v[2] - z * v[1])
    ty = 2.0 * (z * v[0] - x * v[2])
    tz = 2.0 * (x * v[1] - y * v[0])
    return (
        v[0] + w * tx + (y * tz - z * ty),
        v[1] + w * ty + (z * tx - x * tz),
        v[2] + w * tz + (x * ty - y * tx),
    )


@dataclass(frozen=True)
class ToolPose:
    """A TCP goal for a top-down-ish grasp, in the base frame."""

    x: float
    y: float
    z: float
    yaw_deg: float = 0.0
    tilt_deg: float = 0.0  # lean about world +x: tips the tool towards +y

    def quaternion(self) -> Quat:
        q = quat_multiply(quat_axis("x", math.radians(self.tilt_deg)), TOP_DOWN)
        if self.yaw_deg:
            q = quat_multiply(quat_yaw(math.radians(self.yaw_deg)), q)
        return q

    def offset(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> "ToolPose":
        return ToolPose(self.x + dx, self.y + dy, self.z + dz, self.yaw_deg, self.tilt_deg)

    def summary(self) -> dict[str, float]:
        return {
            "x": round(self.x, 4),
            "y": round(self.y, 4),
            "z": round(self.z, 4),
            "yaw_deg": round(self.yaw_deg, 1),
            "tilt_deg": round(self.tilt_deg, 1),
        }
