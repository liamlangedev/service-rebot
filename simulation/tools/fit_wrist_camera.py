"""Fit the wrist camera's mount by matching the gripper silhouette.

In the real wrist frame (reference_photos/cameras/gripper_camera_view.jpeg,
1920x1080) the only dark things are the gripper: the two soft fingers and the
edge of the palm. This renders the sim's gripper (segmentation, so the scene
behind doesn't matter) and searches the camera mount (position and tilt in the
end_link frame), its field of view and the finger opening for the best overlap
(IoU) with that dark mask.

  uv run --project ../teleoperation tools/fit_wrist_camera.py            # fit + report
  uv run --project ../teleoperation tools/fit_wrist_camera.py --write    # update real_setup.json
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SIM))
from rebot_sim import DEFAULT_CONFIG, RealSetupEnv  # noqa: E402

from teleop.rebot_model import _lookat_quat  # noqa: E402

PHOTO = SIM / "reference_photos" / "cameras" / "gripper_camera_view.jpeg"
W, H = 320, 180  # fitting resolution (16:9 like the real 1920x1080 frame)
# Search box: x (along the fingers, tips of the hard fingers at 0), z (away from
# the finger plane), pitch (deg, + = towards the finger axis), fovy, finger opening.
BOUNDS = np.array([[-0.14, -0.03], [0.0, 0.07], [-10, 40], [50, 85], [0.0, 0.05]])


def real_mask() -> np.ndarray:
    img = cv2.resize(cv2.imread(str(PHOTO)), (W, H), interpolation=cv2.INTER_AREA)
    v = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 2]
    mask = (v < 70).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return mask > 0


class Gripper:
    def __init__(self):
        self.env = RealSetupEnv(objects=False)
        self.env.hide_markers()
        m = self.env.model
        root = m.body("end_link").id
        ids = []
        for g in range(m.ngeom):
            b = m.geom_bodyid[g]
            while b not in (0, root):
                b = m.body_parentid[b]
            if b == root and m.geom_contype[g] == 0:  # visual geoms of the gripper
                ids.append(g)
        self.geoms = np.array(ids)
        self.cam = m.camera("wrist").id
        self.r = mujoco.Renderer(m, H, W)
        self.r.enable_segmentation_rendering()
        # Gripper pointing down, high above the table (only its silhouette matters).
        self.env.mirror(np.array([0.0, -1.51, -1.30, 1.36, 0.0, 0.0]), 0.03)

    def mount(self, p):
        x, z, pitch, fovy, _ = p
        pos = np.array([x, 0.0, z])
        look = pos + 0.1 * np.array([np.cos(np.radians(pitch)), 0.0, -np.sin(np.radians(pitch))])
        return pos, look, fovy

    def mask(self, p) -> np.ndarray:
        m, d = self.env.model, self.env.data
        pos, look, fovy = self.mount(p)
        m.cam_pos[self.cam] = pos
        m.cam_quat[self.cam] = _lookat_quat(pos, look, [0, 0, 1])
        m.cam_fovy[self.cam] = fovy
        self.env.mirror(self.env.q_arm, p[4])
        self.r.update_scene(d, camera="wrist")
        seg = self.r.render()
        return (seg[..., 1] == mujoco.mjtObj.mjOBJ_GEOM) & np.isin(seg[..., 0], self.geoms)


def iou(a, b):
    return (a & b).sum() / max((a | b).sum(), 1)


def fit(seed=0, n_random=1500, n_refine=1500):
    rng = np.random.default_rng(seed)
    target = real_mask()
    grip = Gripper()
    lo, hi = BOUNDS[:, 0], BOUNDS[:, 1]
    best_p, best = None, -1.0
    for _ in range(n_random):
        p = lo + rng.random(5) * (hi - lo)
        s = iou(grip.mask(p), target)
        if s > best:
            best_p, best = p, s
    step = (hi - lo) * 0.1
    for i in range(n_refine):  # shrinking random local search
        p = np.clip(best_p + rng.normal(size=5) * step, lo, hi)
        s = iou(grip.mask(p), target)
        if s > best:
            best_p, best = p, s
        if i % 300 == 299:
            step *= 0.5
    return grip, best_p, best, target


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--overlay", default=None, help="save real mask vs fitted sim gripper")
    args = ap.parse_args()
    grip, p, score, target = fit()
    pos, look, fovy = grip.mount(p)
    print(f"IoU {score:.3f}: mount {np.round(pos * 1000, 1)} mm in end_link, pitch {p[2]:.1f} deg, "
          f"fovy {fovy:.1f} deg, finger opening in the photo {p[4] * 1000:.0f} mm")
    if args.overlay:
        sim = grip.mask(p)
        vis = np.zeros((H, W, 3), np.uint8)
        vis[target] = (0, 0, 255)
        vis[sim] = (0, 255, 0)
        vis[target & sim] = (255, 255, 255)
        cv2.imwrite(args.overlay, cv2.resize(vis, (W * 3, H * 3), interpolation=cv2.INTER_NEAREST))
        print(f"overlay -> {args.overlay} (white = both, red = real only, green = sim only)")
    if args.write:
        cfg = json.loads(Path(DEFAULT_CONFIG).read_text())
        wc = cfg["wrist_camera"]
        wc.update({"pos": [round(v, 4) for v in pos], "look_at": [round(v, 4) for v in look],
                   "roll_deg": 0.0, "fovy": round(float(fovy), 1), "aspect": [16, 9],
                   "resolution": [1920, 1080],
                   "_calibrated": f"tools/fit_wrist_camera.py: soft-finger silhouette vs "
                                  f"gripper_camera_view.jpeg (IoU {score:.2f})"})
        Path(DEFAULT_CONFIG).write_text(json.dumps(cfg, indent=2) + "\n")
        print(f"updated {DEFAULT_CONFIG}")


if __name__ == "__main__":
    main()
