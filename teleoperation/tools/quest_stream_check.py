#!/usr/bin/env python3
"""Step 1: check that controller poses and buttons stream from the Quest.

  uv run tools/quest_stream_check.py            # USB
  uv run tools/quest_stream_check.py --ip 192.168.1.42

Prints update rate, raw Quest-frame position, the same position in the robot
frame (using config/quest_calibration.json if present), and pressed buttons.
Move the controller forward/left/up: the robot-frame x/y/z should increase.
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from teleop.quest_input import CALIBRATION_FILE, QuestSource  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ip", default=None)
    p.add_argument("--hand", choices=["r", "l"], default="r")
    args = p.parse_args()

    src = QuestSource(hand=args.hand, ip_address=args.ip)
    print("calibration:", CALIBRATION_FILE if CALIBRATION_FILE.exists() else "default guess")
    last_T, n_updates, t0 = None, 0, time.time()
    try:
        while True:
            T, buttons = src.raw()
            if T is not None and (last_T is None or not np.array_equal(T, last_T)):
                n_updates += 1
                last_T = T.copy()
            time.sleep(0.01)
            if time.time() - t0 < 0.25:
                continue
            hz = n_updates / (time.time() - t0)
            n_updates, t0 = 0, time.time()
            if T is None:
                print(f"{hz:5.1f} Hz  no '{args.hand}' controller pose yet "
                      f"(is the controller awake / app in front?)")
                continue
            s = src.read()
            pressed = [k for k, v in buttons.items() if v is True]
            print(f"{hz:5.1f} Hz  raw={np.round(T[:3, 3], 3)}  robot={np.round(s.pos, 3)}  "
                  f"grip={s.clutch!s:5} trig={s.trigger:.2f}  pressed={pressed}")
    except KeyboardInterrupt:
        pass
    finally:
        src.close()


if __name__ == "__main__":
    main()
