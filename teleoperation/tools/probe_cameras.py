#!/usr/bin/env python3
"""Check the cameras in config/cameras.json: which resolutions really reach 30 fps, and save one frame each.

  python tools/probe_cameras.py            # run from a terminal that has camera permission
  python tools/probe_cameras.py --index 4  # probe any other index
"""
import argparse
import json
import time
from pathlib import Path

import cv2

CONFIG = Path(__file__).resolve().parents[1] / "config" / "cameras.json"
MODES = [(640, 480), (640, 360), (848, 480), (1280, 720)]

p = argparse.ArgumentParser()
p.add_argument("--index", type=int, action="append", help="probe these indices instead of the config")
p.add_argument("--fps", type=int, default=30)
args = p.parse_args()

cams = {f"index{i}": i for i in args.index} if args.index else json.loads(CONFIG.read_text())["cameras"]
out = CONFIG.parent.parent / "outputs" / "probe"
out.mkdir(parents=True, exist_ok=True)
for name, idx in cams.items():
    for w, h in MODES:
        cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION) if hasattr(cv2, "CAP_AVFOUNDATION") else cv2.VideoCapture(idx)
        if not cap.isOpened():
            print(f"{name} (index {idx}): cannot open (camera permission for this terminal?)")
            break
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        cap.set(cv2.CAP_PROP_FPS, args.fps)
        for _ in range(5):
            cap.read()
        t0, n, frame = time.time(), 0, None
        while time.time() - t0 < 2.0:
            ok, fr = cap.read()
            if ok:
                n, frame = n + 1, fr
        got = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        cap.release()
        verdict = "OK" if n / 2.0 >= args.fps - 3 and got == (w, h) else "no"
        print(f"{name:14s} idx {idx}  {w}x{h}: got {got[0]}x{got[1]}, {n / 2.0:4.1f} fps  {verdict}")
        if frame is not None and (w, h) == (640, 480):
            cv2.imwrite(str(out / f"{name}.png"), frame)
