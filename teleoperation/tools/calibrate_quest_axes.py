#!/usr/bin/env python3
"""Step 2: learn how the Quest tracking frame maps onto the robot frame.

Stand where you will teleoperate from, facing the way the robot faces
(robot x = forward, y = left, z = up). Then, holding the controller:

  1. hold it still, press A (or X)        -> origin
  2. move ~20 cm FORWARD, press A         -> forward axis
  3. back to origin, move ~20 cm LEFT, A  -> left axis
  4. back to origin, move ~20 cm UP, A    -> up axis

Writes config/quest_calibration.json, which sim_teleop.py picks up. This also
removes any guesswork about OculusReader's axis convention and headset yaw.
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from teleop.quest_input import BUTTON_KEYS, CALIBRATION_FILE, QuestSource  # noqa: E402


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


def wait_press(src: QuestSource, key: str, prompt: str) -> np.ndarray:
    print(prompt)
    while src.raw()[1].get(key, False):  # wait for release first
        time.sleep(0.01)
    while True:
        T, buttons = src.raw()
        if T is not None and buttons.get(key, False):
            print(f"   recorded {np.round(T[:3, 3], 3)}")
            return T[:3, 3].copy()
        time.sleep(0.01)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ip", default=None)
    p.add_argument("--hand", choices=["r", "l"], default="r")
    args = p.parse_args()

    src = QuestSource(hand=args.hand, ip_address=args.ip, robot_from_quest=np.eye(3))
    key = BUTTON_KEYS[args.hand]["reset"]
    try:
        o = wait_press(src, key, f"1/4 hold still and press {key}")
        f = wait_press(src, key, f"2/4 move ~20 cm FORWARD, press {key}") - o
        o2 = wait_press(src, key, f"   return to start, press {key}")
        l = wait_press(src, key, f"3/4 move ~20 cm LEFT, press {key}") - o2
        o3 = wait_press(src, key, f"   return to start, press {key}")
        u = wait_press(src, key, f"4/4 move ~20 cm UP, press {key}") - o3
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
    CALIBRATION_FILE.parent.mkdir(exist_ok=True)
    CALIBRATION_FILE.write_text(json.dumps({"robot_from_quest": C.tolist(),
                                            "hand": args.hand}, indent=2))
    print(f"saved {CALIBRATION_FILE}")


if __name__ == "__main__":
    main()
