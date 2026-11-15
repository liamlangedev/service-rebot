"""ChArUco board: spec, printable image, detection, and where it lies on the table.

The board lies flat on the table, its edges parallel to the walls, printed side
up and the text margin towards the near wall. `near_left` in real_setup.json
(`charuco` section) is the workspace position of the pattern's outer corner
nearest the left wall and the near wall:

        far edge
      +-----------+
      |  pattern  |   x (columns) -> towards the right wall
      +-----------+   y (rows)    -> towards the near wall
      ^ near_left = (from_left, from_near) of this corner
        near wall (robot)

Make the printable board (A4 PDF, exact size):  python -m rebot_sim.charuco board.pdf
Print at 100 % ("actual size"), measure one square and put it in `square` if it differs.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class BoardSpec:
    squares_x: int = 7
    squares_y: int = 5
    square: float = 0.035   # m, as printed (measure it!)
    marker: float = 0.026   # m
    dictionary: str = "DICT_5X5_100"
    near_left: tuple[float, float] | None = None  # (from_left, from_near) when on the table

    @classmethod
    def from_config(cls, cfg: dict | None) -> "BoardSpec":
        cfg = dict(cfg or {})
        keep = {k: v for k, v in cfg.items() if k in cls.__dataclass_fields__}
        if "near_left" in keep and keep["near_left"] is not None:
            keep["near_left"] = tuple(keep["near_left"])
        return cls(**keep)

    @property
    def size(self) -> tuple[float, float]:
        """Pattern size (x along columns, y along rows) [m]."""
        return self.squares_x * self.square, self.squares_y * self.square

    def board(self) -> "cv2.aruco.CharucoBoard":
        d = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, self.dictionary))
        return cv2.aruco.CharucoBoard((self.squares_x, self.squares_y), self.square,
                                      self.marker, d)

    def image(self, px_per_square: int = 200) -> np.ndarray:
        """Pattern image without margin (its edges are the pattern's edges)."""
        # Drawn from the board definition (marker corners from getObjPoints) because
        # CharucoBoard.generateImage fails for most exact sizes in OpenCV 4.13.
        p = px_per_square
        board = self.board()
        img = np.full((self.squares_y * p, self.squares_x * p), 255, np.uint8)
        marker_px = round(self.marker / self.square * p)
        has_marker = set()
        for mid, corners in zip(board.getIds().reshape(-1), board.getObjPoints()):
            c = np.asarray(corners).reshape(4, 3)[:, :2] / self.square * p
            x0, y0 = np.round(c.min(axis=0)).astype(int)
            mk = cv2.aruco.generateImageMarker(board.getDictionary(), int(mid), marker_px, None, 1)
            img[y0:y0 + marker_px, x0:x0 + marker_px] = mk
            has_marker.add((int(c[:, 0].mean() // p), int(c[:, 1].mean() // p)))
        for j in range(self.squares_y):
            for i in range(self.squares_x):
                if (i, j) not in has_marker:
                    img[j * p:(j + 1) * p, i * p:(i + 1) * p] = 0
        return img

    def to_workspace(self, obj_pts: np.ndarray) -> np.ndarray:
        """Board object points (OpenCV board frame, z = 0) -> workspace
        (from_left, from_near, height) for a board lying on the table."""
        if self.near_left is None:
            raise ValueError("charuco.near_left not set: where does the board lie?")
        _, h = self.size
        p = np.asarray(obj_pts, float).reshape(-1, 3)
        return np.column_stack([self.near_left[0] + p[:, 0],
                                self.near_left[1] + (h - p[:, 1]),
                                np.full(len(p), 0.0005)])  # printed sheet thickness


@dataclass
class Detection:
    corners: np.ndarray   # (N, 2) pixels
    ids: np.ndarray       # (N,)
    obj: np.ndarray       # (N, 3) board-frame points [m]

    def __len__(self):
        return len(self.ids)

    def spans_2d(self, spec: "BoardSpec", min_corners: int = 6) -> bool:
        """Enough corners, not all in one row/column (a pose needs a 2-D spread)."""
        cols = spec.squares_x - 1
        return (len(self.ids) >= min_corners and len(set(self.ids // cols)) >= 2
                and len(set(self.ids % cols)) >= 2)


def detect(spec: BoardSpec, image_bgr: np.ndarray, min_corners: int = 6) -> Detection | None:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY) if image_bgr.ndim == 3 else image_bgr
    board = spec.board()
    detector = cv2.aruco.CharucoDetector(board)
    corners, ids, _, _ = detector.detectBoard(gray)
    if ids is None or len(ids) < min_corners:
        return None
    obj, img = board.matchImagePoints(corners, ids)
    return Detection(img.reshape(-1, 2), ids.reshape(-1), obj.reshape(-1, 3))


def draw(image_bgr: np.ndarray, det: Detection | None) -> np.ndarray:
    out = image_bgr.copy()
    if det is not None:
        cv2.aruco.drawDetectedCornersCharuco(out, det.corners.reshape(-1, 1, 2).astype(np.float32),
                                             det.ids.reshape(-1, 1), (0, 255, 0))
    return out


def calibrate_intrinsics(spec: BoardSpec, views: list[Detection], image_size: tuple[int, int]):
    """Lens calibration from many views of the board (moved around in front of
    the camera). Returns (K, dist, rms_px)."""
    obj = [v.obj.astype(np.float32) for v in views]
    img = [v.corners.astype(np.float32) for v in views]
    rms, K, dist, _, _ = cv2.calibrateCamera(obj, img, image_size, None, None)
    return K, dist.reshape(-1), float(rms)


def solve_pose(det: Detection, world_pts: np.ndarray, K: np.ndarray, dist: np.ndarray):
    """Camera pose from known 3D points of the detected corners.
    Returns (R_world_from_cv, cam_pos_world, rms_px) with OpenCV camera axes
    (x right, y down, z forward)."""
    ok, rvec, tvec = cv2.solvePnP(world_pts.astype(np.float64), det.corners.astype(np.float64),
                                  K, dist, flags=cv2.SOLVEPNP_ITERATIVE)
    if not ok:
        raise RuntimeError("solvePnP failed")
    rvec, tvec = cv2.solvePnPRefineLM(world_pts.astype(np.float64),
                                      det.corners.astype(np.float64), K, dist, rvec, tvec)
    proj, _ = cv2.projectPoints(world_pts.astype(np.float64), rvec, tvec, K, dist)
    rms = float(np.sqrt(np.mean(np.sum((proj.reshape(-1, 2) - det.corners) ** 2, axis=1))))
    R_cv_from_world = cv2.Rodrigues(rvec)[0]
    R = R_cv_from_world.T
    return R, (-R @ tvec).reshape(3), rms


def write_printable(spec: BoardSpec, path: str, dpi: int = 300) -> str:
    """A4 landscape PDF (or PNG) with the pattern at its exact physical size."""
    from PIL import Image, ImageDraw
    a4 = (round(297 / 25.4 * dpi), round(210 / 25.4 * dpi))
    w, h = (round(v / 0.0254 * dpi) for v in spec.size)
    if w > a4[0] - 100 or h > a4[1] - 100:
        raise ValueError("pattern does not fit on A4; use a smaller square")
    pattern = Image.fromarray(spec.image()).resize((w, h), Image.NEAREST)
    page = Image.new("L", a4, 255)
    x0, y0 = (a4[0] - w) // 2, (a4[1] - h) // 2
    page.paste(pattern, (x0, y0))
    ImageDraw.Draw(page).text(
        (x0, y0 + h + 20),
        f"ChArUco {spec.squares_x}x{spec.squares_y} {spec.dictionary}, square "
        f"{spec.square * 1000:.0f} mm, marker {spec.marker * 1000:.0f} mm. Print at 100%. "
        "This edge faces the near wall (robot).", fill=0)
    page.save(path, resolution=dpi)
    return f"pattern {spec.size[0] * 100:.1f} x {spec.size[1] * 100:.1f} cm on A4"


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "charuco_board.pdf"
    print(f"wrote {out}: {write_printable(BoardSpec(), out)}")
