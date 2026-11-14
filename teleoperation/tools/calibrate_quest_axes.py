#!/usr/bin/env python3
"""Step 2: learn how the Quest tracking frame maps onto the robot frame.

Stand where you will teleoperate from, facing the way the robot faces
(robot x = forward, y = left, z = up). Then, holding the controller:

  1. hold it still, press A (or X)        -> origin
  2. move ~20 cm FORWARD, press A         -> forward axis
  3. back to origin, move ~20 cm LEFT, A  -> left axis
  4. back to origin, move ~20 cm UP, A    -> up axis

Writes config/quest_calibration_<source>.json, which sim_teleop.py picks up.
WebXR and OculusReader use different tracking frames, so calibrate each
source you use.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from teleop.quest_input import BUTTON_NAMES, calibration_file, make_quest_source  # noqa: E402


def frame_from_axes(fwd: np.ndarray, left: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Rows = robot x/y/z expressed in Quest coordinates (robot_from_quest).

    Up is trusted most, then forward; left only fixes handedness, so a
    left-handed tracking frame is handled too (det = -1).
    """
    z = up / np.linalg.norm(up)
    x = fwd - z * (fwd @ z)
    x /= np.linalg.norm(x)
    y = np.cross(z, x)
    if y @ left < 0:
        y = -y
    return np.vstack([x, y, z])


def wait_press(src, prompt: str) -> np.ndarray:
    print(prompt)
    while src.read().reset:  # wait for release first
        time.sleep(0.01)
    while True:
        s = src.read()
        if s.valid and s.reset:
            print(f"   recorded {np.round(s.raw[:3, 3], 3)}")
            return s.raw[:3, 3].copy()
        time.sleep(0.01)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["webxr", "oculus"], default="webxr")
    p.add_argument("--relay", default="ws://127.0.0.1:8443/ws")
    p.add_argument("--ip", default=None, help="Quest IP for wireless ADB (oculus)")
    p.add_argument("--hand", choices=["r", "l"], default="r")
    args = p.parse_args()

    src = make_quest_source(args.source, args.hand, args.ip, args.relay,
                            robot_from_quest=np.eye(3))
    key = BUTTON_NAMES[args.hand]["reset"]
    try:
        o = wait_press(src, f"1/4 hold still and press {key}")
        f = wait_press(src, f"2/4 move ~20 cm FORWARD, press {key}") - o
        o2 = wait_press(src, f"   return to start, press {key}")
        l = wait_press(src, f"3/4 move ~20 cm LEFT, press {key}") - o2
        o3 = wait_press(src, f"   return to start, press {key}")
        u = wait_press(src, f"4/4 move ~20 cm UP, press {key}") - o3
    finally:
        src.close()

    for name, v in [("forward", f), ("left", l), ("up", u)]:
        if np.linalg.norm(v) < 0.08:
            sys.exit(f"'{name}' move was only {np.linalg.norm(v) * 100:.1f} cm; redo with ~20 cm.")

    C = frame_from_axes(f, l, u)
    print("robot_from_quest =\n", np.round(C, 3), f"\n det = {np.linalg.det(C):+.2f}")
    print(f" check (cm, expect ~[20,0,0], [0,20,0], [0,0,20]):\n"
          f"  fwd {np.round(C @ f * 100, 1)}\n  left {np.round(C @ l * 100, 1)}\n"
          f"  up {np.round(C @ u * 100, 1)}")
    out = calibration_file(args.source)
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"robot_from_quest": C.tolist(), "hand": args.hand}, indent=2))
    print(f"saved {out}")


if __name__ == "__main__":
    main()
