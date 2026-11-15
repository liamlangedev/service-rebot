#!/usr/bin/env python3
"""Grab one frame from each camera and save a labelled grid, to check which device is
which dataset camera before a rollout.

    teleoperation/.venv/bin/python rollout/check_cameras.py            # all /dev/v4l/by-id cameras
    teleoperation/.venv/bin/python rollout/check_cameras.py --cam front_wide=/dev/video2 \
        --cam gripper=/dev/video4 --cam high_oblique=/dev/video6        # the mapping you will use

Compare the output (rollout/logs/cameras.jpg) with rollout/camera_reference.jpg, which
shows the three dataset views (episode 32 of rebot_sort_v1).
"""

from __future__ import annotations

import argparse
import glob
from pathlib import Path

import cv2
import numpy as np


def grab(dev: str) -> np.ndarray | None:
    cap = cv2.VideoCapture(int(dev) if dev.isdigit() else dev)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    frame = None
    for _ in range(15):  # let exposure settle
        ok, f = cap.read()
        frame = f if ok else frame
    cap.release()
    return frame


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cam", action="append", metavar="NAME=DEVICE")
    p.add_argument("--out", default=str(Path(__file__).resolve().parent / "logs" / "cameras.jpg"))
    a = p.parse_args()
    cams = dict(c.split("=", 1) for c in a.cam) if a.cam else {
        Path(d).name.replace("usb-", "")[:28]: d
        for d in sorted(glob.glob("/dev/v4l/by-id/*-video-index0"))}
    tiles = []
    for name, dev in cams.items():
        f = grab(dev)
        ok = f is not None
        f = cv2.resize(f, (320, 240)) if ok else np.zeros((240, 320, 3), np.uint8)
        cv2.putText(f, name, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        cv2.putText(f, str(Path(dev).resolve()), (6, 232), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                    (0, 255, 255), 1)
        tiles.append(f)
        print(f"{name:30s} {dev} -> {Path(dev).resolve()}  {'ok' if ok else 'NO FRAME'}")
    while len(tiles) % 2:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + 2]) for i in range(0, len(tiles), 2)]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(a.out, np.vstack(rows))
    print("saved", a.out)


if __name__ == "__main__":
    main()
