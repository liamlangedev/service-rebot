"""Render each sim camera next to its real frame (reference_photos/cameras).

  uv run --project ../teleoperation tools/compare_cameras.py --out docs/camera_compare.jpg

Each row: real frame | sim render | sim render with the real frame's edges in red.
The arm pose differs between the photos and the sim, so compare the static scene
(walls, table edges, bin, base plate).
"""
import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

SIM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SIM))
from rebot_sim import RealSetupEnv, TOP_DOWN  # noqa: E402

PHOTOS = {"cam_corner": "corner_camera_view.jpeg", "cam_far": "center_camera_view.jpeg",
          "wrist": "gripper_camera_view.jpeg"}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="camera_compare.jpg")
    p.add_argument("--width", type=int, default=640)
    args = p.parse_args()
    w = args.width
    h = w * 9 // 16

    env = RealSetupEnv(objects=False)
    env.hide_markers()
    env.reset()
    rows = []
    for cam, photo in PHOTOS.items():
        if cam == "wrist":  # gripper down, a few cm above the table, like the photo
            env.move_grasp_to(np.array([0.30, 0.0, env.ws.table_z + 0.09]), TOP_DOWN,
                              speed=0.5, settle=0.5)
        real = cv2.resize(cv2.imread(str(SIM / "reference_photos" / "cameras" / photo)), (w, h))
        sim = cv2.cvtColor(env.render(cam, w, h), cv2.COLOR_RGB2BGR)
        edges = cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(real, cv2.COLOR_BGR2GRAY), (5, 5), 0),
                          40, 120)
        over = sim.copy()
        over[cv2.dilate(edges, np.ones((2, 2), np.uint8)) > 0] = (0, 0, 255)
        for im, label in ((real, f"real {cam}"), (sim, "sim"), (over, "sim + real edges")):
            cv2.putText(im, label, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        rows.append(np.hstack([real, sim, over]))
    env.close()
    cv2.imwrite(args.out, np.vstack(rows))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
