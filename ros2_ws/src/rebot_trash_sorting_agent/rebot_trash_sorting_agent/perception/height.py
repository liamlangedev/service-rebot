"""Metric front-view height from calibrated table marks and a known footprint.

This is a coarse upright-object model, not stereo reconstruction. The top is
approximated by a disk spanning the measured footprint; occlusion and overhangs
can invalidate that approximation.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from rebot_trash_sorting_agent.types import Detection, WorldObject


@dataclass
class HeightCamera:
    projection: np.ndarray
    image_size: tuple[int, int]
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.projection = np.asarray(self.projection, dtype=float).reshape(3, 4)
        if not np.isfinite(self.projection).all() or np.linalg.matrix_rank(self.projection) != 3:
            raise ValueError("height camera needs a finite rank-3 projection matrix")
        if len(self.image_size) != 2 or min(self.image_size) <= 0:
            raise ValueError("height calibration needs a positive image width and height")

    @classmethod
    def fit_table(
        cls,
        pixels: Sequence[Sequence[float]],
        table_points: Sequence[Sequence[float]],
        table_z: float,
        image_size: tuple[int, int],
        camera_matrix: Sequence[Sequence[float]] | np.ndarray,
        distortion: Sequence[float] = (),
    ) -> HeightCamera:
        import cv2

        uv = np.asarray(pixels, dtype=float)
        xy = np.asarray(table_points, dtype=float)
        intrinsic = np.asarray(camera_matrix, dtype=float).reshape(3, 3)
        coefficients = np.asarray(distortion, dtype=float).reshape(-1)
        if xy.ndim != 2 or xy.shape[1] != 2 or uv.shape != (len(xy), 2) or len(xy) < 4:
            raise ValueError("height calibration needs at least 4 matching pixel/XY points")
        if not np.isfinite(xy).all() or not np.isfinite(uv).all() or not np.isfinite(intrinsic).all():
            raise ValueError("calibration points must be finite")
        if np.linalg.matrix_rank(xy - xy.mean(axis=0)) < 2:
            raise ValueError("degenerate table calibration; spread marks over X and Y")
        if intrinsic[0, 0] <= 0 or intrinsic[1, 1] <= 0 or not np.isclose(intrinsic[2, 2], 1):
            raise ValueError("camera_matrix needs positive focal lengths and bottom-right value 1")
        xyz = np.column_stack((xy, np.full(len(xy), table_z)))
        ok, rotation_vector, translation = cv2.solvePnP(
            xyz,
            uv,
            intrinsic,
            coefficients if coefficients.size else None,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )
        if not ok:
            raise ValueError("could not recover camera pose from table points")
        rotation, _ = cv2.Rodrigues(rotation_vector)
        model = cls(
            intrinsic @ np.column_stack((rotation, translation)),
            image_size,
            {"camera_matrix": intrinsic.reshape(-1).tolist(), "distortion": coefficients.tolist()},
        )
        residuals = np.linalg.norm(model.project(xyz) - uv, axis=1)
        model.meta.update(error_px=float(residuals.mean()), max_error_px=float(residuals.max()), points=len(xyz))
        return model

    @classmethod
    def from_mapping(cls, data: dict[str, Any] | None) -> HeightCamera | None:
        if not data:
            return None
        return cls(
            np.asarray(data["projection"]),
            tuple(data["image_size"]),
            {key: value for key, value in data.items() if key not in ("projection", "image_size")},
        )

    def to_mapping(self) -> dict[str, Any]:
        return {**self.meta, "projection": self.projection.reshape(-1).tolist(), "image_size": list(self.image_size)}

    def project(self, points: Sequence[Sequence[float]] | np.ndarray) -> np.ndarray:
        xyz = np.asarray(points, dtype=float).reshape(-1, 3)
        projected = (self.projection @ np.column_stack((xyz, np.ones(len(xyz)))).T).T
        if np.any(projected[:, 2] <= 1e-9):
            raise ValueError("point is on or behind the camera plane")
        pixels = projected[:, :2] / projected[:, 2:3]
        if self.meta.get("distortion") and np.any(self.meta["distortion"]):
            import cv2

            intrinsic = np.asarray(self.meta["camera_matrix"]).reshape(3, 3)
            rays = (np.linalg.inv(intrinsic) @ np.column_stack((pixels, np.ones(len(pixels)))).T).T
            distorted, _ = cv2.projectPoints(
                rays, np.zeros(3), np.zeros(3), intrinsic, np.asarray(self.meta["distortion"])
            )
            pixels = distorted.reshape(-1, 2)
        return pixels

    def matches(self, obj: WorldObject, detection: Detection, margin_px: float) -> float | None:
        if obj.label != detection.label:
            return None
        try:
            horizontal, vertical = self.project([[obj.x, obj.y, obj.z]])[0]
        except ValueError:
            return None
        left, top, right, bottom = detection.bbox
        if not (
            left - margin_px <= horizontal <= right + margin_px
            and top + 0.4 * detection.height_px <= vertical <= bottom + margin_px
        ):
            return None
        return abs(horizontal - (left + right) / 2) / max(right - left, 1.0)

    def height(
        self,
        obj: WorldObject,
        detection: Detection,
        min_height_m: float = 0.005,
        max_height_m: float = 0.35,
    ) -> float | None:
        """Fit the top silhouette of an upright disk with the measured footprint width."""
        if min_height_m <= 0 or max_height_m <= min_height_m:
            raise ValueError("height limits must satisfy 0 < min < max")
        top = min((point[1] for point in detection.polygon), default=detection.bbox[1])
        angles = np.linspace(0, 2 * np.pi, 32, endpoint=False)
        radius = max(0.0, obj.width_m / 2)
        rim = np.column_stack((obj.x + radius * np.cos(angles), obj.y + radius * np.sin(angles), np.full(32, obj.z)))

        def top_row(height: float) -> float:
            points = rim.copy()
            points[:, 2] += height
            return float(self.project(points)[:, 1].min())

        low, high = min_height_m, max_height_m
        try:
            bottom_row, upper_row = top_row(low), top_row(high)
            if bottom_row - upper_row < 5.0 or not upper_row <= top <= bottom_row:
                return None
            for _ in range(30):
                middle = (low + high) / 2
                if top_row(middle) > top:
                    low = middle
                else:
                    high = middle
        except ValueError:
            return None
        return (low + high) / 2

    def estimate_heights(
        self,
        objects: Sequence[WorldObject],
        detections: Sequence[Detection],
        image_size: tuple[int, int],
        *,
        match_margin_px: float = 20.0,
        ambiguity_margin: float = 0.15,
        min_height_m: float = 0.005,
        max_height_m: float = 0.35,
    ) -> dict[int, float]:
        if tuple(image_size) != tuple(self.image_size):
            raise ValueError(f"front camera resolution {image_size} differs from calibration {self.image_size}")
        proposals: dict[int, tuple[int, float]] = {}
        for object_index, obj in enumerate(objects):
            matches = []
            for detection_index, detection in enumerate(detections):
                score = self.matches(obj, detection, match_margin_px)
                if score is not None:
                    matches.append((score, detection_index))
            matches.sort()
            if not matches or (len(matches) > 1 and matches[1][0] - matches[0][0] < ambiguity_margin):
                continue
            detection_index = matches[0][1]
            height = self.height(obj, detections[detection_index], min_height_m, max_height_m)
            if height is not None:
                proposals[object_index] = (detection_index, height)
        return {
            object_index: height
            for object_index, (detection_index, height) in proposals.items()
            if sum(other_index == detection_index for other_index, _ in proposals.values()) == 1
        }
