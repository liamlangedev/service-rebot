#!/usr/bin/env python3
"""Table homography for the *simulated* table camera (cameras.yaml -> table_sim).

The MuJoCo bridge (mujoco_sim_node, use_mujoco:=true) publishes the sim's
`cam_corner` as /table_cam. This projects a grid of table points (z = 0 in
base_link) through that camera, exactly as MuJoCo renders it at the bridge's
image size, and fits the pixel -> base_link homography the agent uses.

    python3 scripts/sim_calibrate.py                 # print the cameras.yaml block
    python3 scripts/sim_calibrate.py --width 640 --height 480

Run it with the repo's simulation environment (mujoco + numpy + opencv), e.g.
    uv run --project teleoperation python ros2_ws/src/rebot_trash_sorting_agent/scripts/sim_calibrate.py
Re-run after the sim's camera calibration changes (simulation/rebot_sim/real_setup.json).
"""
import argparse
import sys
from pathlib import Path

import numpy as np


def repo_root() -> Path:
    for p in Path(__file__).resolve().parents:
        if (p / "simulation" / "rebot_sim").is_dir():
            return p
    raise SystemExit("run from inside the steel_team repo")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--camera", default="cam_corner")
    ap.add_argument("--width", type=int, default=640)
    ap.add_argument("--height", type=int, default=480)
    args = ap.parse_args()

    root = repo_root()
    for sub in ("simulation", "teleoperation"):
        sys.path.insert(0, str(root / sub))
    import cv2
    from rebot_sim import RealSetupEnv

    env = RealSetupEnv(objects=False)
    cam = env.data.cam(args.camera)
    R, C = cam.xmat.reshape(3, 3), cam.xpos
    fovy = float(env.model.camera(args.camera).fovy[0])
    f = args.height / 2 / np.tan(np.radians(fovy) / 2)

    px, xy = [], []
    for x in np.linspace(0.05, 0.60, 12):
        for y in np.linspace(-0.35, 0.35, 15):
            pc = R.T @ (np.array([x, y, env.ws.table_z]) - C)   # MuJoCo camera: looks along -z
            if pc[2] >= -1e-6:
                continue
            u = args.width / 2 + f * pc[0] / -pc[2]
            v = args.height / 2 - f * pc[1] / -pc[2]
            if 0 <= u < args.width and 0 <= v < args.height:
                px.append((u, v))
                xy.append((x, y))
    H, _ = cv2.findHomography(np.array(px).reshape(-1, 1, 2), np.array(xy).reshape(-1, 1, 2), 0)
    H /= H[2, 2]
    back = cv2.perspectiveTransform(np.array(px).reshape(-1, 1, 2), H).reshape(-1, 2)
    err_mm = float(np.mean(np.linalg.norm(back - np.array(xy), axis=1)) * 1000)

    rows = [", ".join(f"{v:.11g}" for v in H[i]) for i in range(3)]
    print(f"    fov_deg: {fovy:.2f}")
    print("    table_map:")
    print("      homography:")
    print(f"        [{rows[0]},")
    print(f"         {rows[1]},")
    print(f"         {rows[2]}]")
    print(f"      error_mm: {err_mm:.1f}")
    print(f"      points: {len(px)}")
    print(f"      source: mujoco {args.camera} ({args.width}x{args.height}, scene "
          f"v{env.cfg.get('version')})")


if __name__ == "__main__":
    main()
