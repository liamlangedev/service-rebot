"""Pixel -> base_link projection through a table-plane homography.

With one RGB camera and no depth, the only honest way to place an object is to use
the fact that it stands on a known plane. ``H`` maps image pixels to metres on that
plane, so the contact point at the bottom of a mask projects to the object's
footprint and the object's top does not.

``H`` is fitted from >= 4 measured points (``scripts/calibrate_table.py``) and lives
in ``cameras.yaml``. Nothing here imports ROS.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import time
from typing import Any, Iterable, Sequence

import numpy as np

from ..types import Detection


@dataclass
class TableMap:
    #: 3x3 homography, [u, v, 1] -> [x, y, 1] in metres
    homography: np.ndarray
    table_z: float
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        h = np.asarray(self.homography, dtype=float)
        if h.shape != (3, 3):
            raise ValueError(f"homography must be 3x3, got {h.shape}")
        if abs(np.linalg.det(h)) < 1e-12:
            raise ValueError("homography is singular")
        self.homography = h / h[2, 2] if abs(h[2, 2]) > 1e-12 else h

    # ------------------------------------------------------------------ construction
    @classmethod
    def from_mapping(cls, data: dict[str, Any] | None, table_z: float) -> "TableMap | None":
        if not data:
            return None
        raw = data.get("homography") if isinstance(data, dict) else None
        if raw is None:
            return None
        flat = np.asarray(raw, dtype=float).reshape(-1)
        if flat.size != 9:
            raise ValueError("cameras.yaml: table_map.homography must hold 9 numbers")
        meta = {k: v for k, v in dict(data).items() if k != "homography"}
        return cls(flat.reshape(3, 3), float(table_z), meta)

    @classmethod
    def fit(cls, pixels: Sequence[Sequence[float]], points: Sequence[Sequence[float]],
            table_z: float) -> "TableMap":
        """Least-squares homography from >= 4 pixel/base pairs."""
        uv = np.asarray(pixels, dtype=float).reshape(-1, 2)
        xy = np.asarray(points, dtype=float).reshape(-1, 2)
        if uv.shape != xy.shape:
            raise ValueError(f"got {len(uv)} pixels but {len(xy)} points")
        if len(uv) < 4:
            raise ValueError("need at least 4 correspondences")
        h, _ = _cv2_find_homography(uv, xy)
        if h is None:
            h = _dlt_homography(uv, xy)
        return cls(h, table_z, {"points": int(len(uv)), "created": _timestamp()})

    # ------------------------------------------------------------------ projection
    def pixel_to_base(self, u: float, v: float) -> tuple[float, float]:
        p = self.homography @ np.array([float(u), float(v), 1.0])
        if abs(p[2]) < 1e-12:
            raise ValueError(f"point ({u}, {v}) maps to infinity")
        return (float(p[0] / p[2]), float(p[1] / p[2]))

    def base_to_pixel(self, x: float, y: float) -> tuple[float, float]:
        inv = np.linalg.inv(self.homography)
        p = inv @ np.array([float(x), float(y), 1.0])
        if abs(p[2]) < 1e-12:
            raise ValueError(f"point ({x}, {y}) maps to infinity")
        return (float(p[0] / p[2]), float(p[1] / p[2]))

    def project(self, detection: Detection) -> tuple[float, float]:
        u, v = detection.bottom_mid_px()
        return self.pixel_to_base(u, v)

    def footprint(self, detection: Detection, band_fraction: float = 0.20,
                  min_band_px: float = 4.0) -> tuple[float, float]:
        """``(width_m, edge_angle_deg)`` of the base silhouette.

        The bottom band of the mask is the only part of the silhouette that is
        certainly near the table plane, so it is the only part the homography can
        measure without depth. Its left and right extremes straddle the object's
        base (the lowest point is only the near tangent), and projecting each end at
        its own row gives the visible width at the base and the direction of that
        edge. For a can or a cup the width is close to the diameter; for a box it is
        the visible side, which is the dimension the jaws close across.

        No class table is involved: a can and a bottle use the same measurement.
        ``width_m`` is an upper bound on the jaw opening needed; ``edge_angle_deg``
        is the direction of the base edge in the base frame (jaws close
        perpendicular to it).
        """
        y_max = float(detection.bbox[3])
        if detection.polygon:
            y_max = max(y_max, max(p[1] for p in detection.polygon))
        band = max(float(min_band_px), float(band_fraction) * max(detection.height_px, 1.0))
        if detection.polygon:
            points = [(float(u), float(v)) for u, v in detection.polygon
                      if v >= y_max - band]
        else:
            points = []
        if len(points) >= 2:
            left = min(points, key=lambda p: p[0])
            right = max(points, key=lambda p: p[0])
            lo, lo_v = left
            hi, hi_v = right
        else:
            lo, hi = float(detection.bbox[0]), float(detection.bbox[2])
            lo_v = hi_v = y_max
        if hi - lo < 1.0:
            return 0.0, 0.0
        x1, y1 = self.pixel_to_base(lo, lo_v)
        x2, y2 = self.pixel_to_base(hi, hi_v)
        width = math.hypot(x2 - x1, y2 - y1)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        # The edge is a line, not a direction: +180 deg is the same grasp.
        angle = ((angle + 90.0) % 180.0) - 90.0
        return width, angle

    def reprojection_error_mm(self, pixels: Iterable[Sequence[float]],
                              points: Iterable[Sequence[float]]) -> float:
        errs = []
        for (u, v), (x, y) in zip(pixels, points):
            px, py = self.pixel_to_base(u, v)
            errs.append(1000.0 * ((px - x) ** 2 + (py - y) ** 2) ** 0.5)
        return float(np.mean(errs)) if errs else float("nan")

    # ------------------------------------------------------------------ io
    def to_mapping(self) -> dict[str, Any]:
        data: dict[str, Any] = {"homography": [round(float(v), 8) for v in self.homography.reshape(-1)]}
        data.update(self.meta)
        return data

    @property
    def error_mm(self) -> float | None:
        value = self.meta.get("error_mm")
        return float(value) if value is not None else None

    def describe(self) -> dict[str, Any]:
        return {
            "table_z": round(self.table_z, 4),
            "error_mm": self.error_mm,
            "points": self.meta.get("points"),
            "created": self.meta.get("created"),
        }


def _cv2_find_homography(uv: np.ndarray, xy: np.ndarray) -> tuple[np.ndarray | None, float]:
    try:
        import cv2
    except ImportError:  # pragma: no cover - cv2 is a ROS dependency, present at runtime
        return None, float("nan")
    h, _ = cv2.findHomography(uv.reshape(-1, 1, 2), xy.reshape(-1, 1, 2), method=0)
    return (h if h is not None else None), float("nan")


def _dlt_homography(uv: np.ndarray, xy: np.ndarray) -> np.ndarray:
    """Normalised DLT, used when OpenCV is unavailable (tests, tooling)."""
    a, b = _normalise(uv), _normalise(xy)
    rows = []
    for (u, v), (x, y) in zip(a[0], b[0]):
        rows.append([-u, -v, -1.0, 0.0, 0.0, 0.0, x * u, x * v, x])
        rows.append([0.0, 0.0, 0.0, -u, -v, -1.0, y * u, y * v, y])
    _, _, vt = np.linalg.svd(np.asarray(rows))
    h = vt[-1].reshape(3, 3)
    h = np.linalg.inv(b[1]) @ h @ a[1]
    return h / h[2, 2]


def _normalise(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    centre = points.mean(axis=0)
    shifted = points - centre
    scale = np.sqrt(2.0) / max(np.mean(np.linalg.norm(shifted, axis=1)), 1e-12)
    t = np.array([[scale, 0.0, -scale * centre[0]], [0.0, scale, -scale * centre[1]], [0.0, 0.0, 1.0]])
    homogeneous = np.column_stack([points, np.ones(len(points))])
    transformed = (t @ homogeneous.T).T
    return transformed[:, :2] / transformed[:, 2:3], t


def _timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")
