#!/usr/bin/env python3
"""Step 1: check that controller poses and buttons stream from the Quest.

  uv run tools/quest_stream_check.py                     # WebXR relay (default)
  uv run tools/quest_stream_check.py --source oculus     # OculusReader over USB
  uv run tools/quest_stream_check.py --source oculus --ip 192.168.1.42

Prints update rate, raw Quest-frame position, the same position in the robot
frame (using the calibration for that source if present), and the buttons.
Move the controller forward/left/up: the robot-frame x/y/z should increase.
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from teleop.quest_input import calibration_file, make_quest_source  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["webxr", "oculus"], default="webxr")
    p.add_argument("--relay", default="ws://127.0.0.1:8443/ws")
    p.add_argument("--ip", default=None, help="Quest IP for wireless ADB (oculus)")
    p.add_argument("--hand", choices=["r", "l"], default="r")
    args = p.parse_args()

    src = make_quest_source(args.source, args.hand, args.ip, args.relay)
    cal = calibration_file(args.source)
    print("calibration:", cal if cal.exists() else "default guess")
    last_raw, n_updates, t0 = None, 0, time.time()
    try:
        while True:
            s = src.read()
            if s.valid and (last_raw is None or not np.array_equal(s.raw, last_raw)):
                n_updates += 1
                last_raw = s.raw.copy()
            time.sleep(0.005)
            if time.time() - t0 < 0.25:
                continue
            hz = n_updates / (time.time() - t0)
            n_updates, t0 = 0, time.time()
            if not s.valid:
                print(f"{hz:5.1f} Hz  no '{args.hand}' controller pose yet "
                      f"(page open and 'Start Teleop' pressed? controller awake?)")
                continue
            print(f"{hz:5.1f} Hz  raw={np.round(s.raw[:3, 3], 3)}  robot={np.round(s.pos, 3)}  "
                  f"grip={s.clutch!s:5} trig={s.trigger:.2f} home={s.reset!s:5} "
                  f"rot={s.toggle_rot!s:5} rec={s.record!s:5}")
    except KeyboardInterrupt:
        pass
    finally:
        src.close()


if __name__ == "__main__":
    main()
