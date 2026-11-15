#!/usr/bin/env python3
"""Fit the table-plane homography: image pixels -> base_link metres.

This is the *only* calibration the agent needs. No intrinsics, no hand-eye, no
depth: an object standing on the table touches a known plane, so four or more
known points on that plane are enough to place every detection.

Procedure

1. Put four or more marks on the table at known base-frame coordinates (masking
   tape crosses are fine). Pick them spread over the reachable area, not clustered.
2. Measure their (x, y) in base_link - x straight ahead of the arm, y to its left -
   and pass them with ``--points`` in the order you will click them.
3. Run this, click the same points in the same order, press Enter.

    ros2 run rebot_trash_sorting_agent calibrate_table \
        --points "0.15,-0.20;0.45,-0.20;0.15,0.20;0.45,0.20;0.30,0.00"

For a headless machine pass the pixel coordinates too and no window opens:

    ... --pixels "412,610;1010,608;395,240;1020,236"

The result goes to ``config/calibration.yaml`` (not cameras.yaml), so hand-written
comments in the config survive every recalibration. It is printed as well, so it
can be pasted into ``cameras.yaml -> table_map`` if you prefer.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

from .config import Config
from .perception.table_map import TableMap


def _parse_pairs(text: str, label: str) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for chunk in (text or "").replace(";", " ").replace("\n", " ").split():
        parts = chunk.split(",")
        if len(parts) != 2:
            raise SystemExit(f"{label}: expected 'a,b' pairs, got {chunk!r}")
        out.append((float(parts[0]), float(parts[1])))
    return out


def _grab_frame(camera: str, config_dir: str | None) -> np.ndarray:
    """Take one frame from the camera topic (needs camera_node running)."""
    import rclpy
    from rclpy.node import Node

    from .perception.scene import CameraClient

    config = Config.load(config_dir)
    topic = config.capture_topic(camera)
    rclpy.init()
    node = Node("calibrate_table")
    client = CameraClient(node, topic, timeout_s=10.0)
    node.get_logger().info(f"waiting for a frame on {topic}")
    deadline = time.monotonic() + 10.0
    frame = None
    while time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=0.1)
        frame = client.latest(max_age_s=2.0)
        if frame is not None:
            break
    node.destroy_node()
    rclpy.shutdown()
    if frame is None:
        raise SystemExit(
            f"no frame on {topic}: is camera_node running? "
            "(ros2 launch rebot_trash_sorting_agent agent.launch.py)"
        )
    return frame


def _click_points(image: np.ndarray, expected: int) -> list[tuple[float, float]]:
    import cv2

    points: list[tuple[float, float]] = []
    window = "calibrate_table - click points, Enter=accept, r=reset, Esc=abort"

    def on_mouse(event, x, y, _flags, _param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < expected:
            points.append((float(x), float(y)))
            print(f"  point {len(points)}: pixel ({x}, {y})")

    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window, on_mouse)
    while True:
        canvas = image.copy()
        for index, (x, y) in enumerate(points, start=1):
            cv2.circle(canvas, (int(x), int(y)), 6, (0, 0, 255), -1)
            cv2.putText(canvas, str(index), (int(x) + 9, int(y) - 9),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(canvas, f"{len(points)}/{expected} points", (12, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2, cv2.LINE_AA)
        cv2.imshow(window, canvas)
        key = cv2.waitKey(30) & 0xFF
        if key in (13, 10, 32) and points:
            break
        if key in (ord("r"), ord("R")):
            points.clear()
        if key == 27:
            cv2.destroyAllWindows()
            raise SystemExit("aborted")
    cv2.destroyAllWindows()
    return points


def _write(out: Path, camera: str, table_map: TableMap) -> None:
    import yaml

    data: dict = {}
    if out.is_file():
        try:
            data = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            data = {}
    data[camera] = table_map.to_mapping()
    out.parent.mkdir(parents=True, exist_ok=True)
    header = (
        "# Written by calibrate_table.py. One homography per camera:\n"
        "# [u, v, 1] * H -> [x, y, 1] in metres on the table plane (z = places.yaml table.z).\n"
        "# Regenerate after moving the camera; this file is disposable.\n"
    )
    out.write_text(header + yaml.safe_dump(data, sort_keys=False, default_flow_style=False),
                   encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--camera", default="table", help="camera name from cameras.yaml")
    parser.add_argument("--config-dir", default=None)
    parser.add_argument("--points", required=True,
                        help="base_link coordinates 'x,y;x,y;...' in click order (metres)")
    parser.add_argument("--pixels", default=None,
                        help="skip the window: 'u,v;u,v;...' in the same order")
    parser.add_argument("--image", default=None, help="use this still instead of the live topic")
    parser.add_argument("--out", default=None, help="default: <config_dir>/calibration.yaml")
    parser.add_argument("--max-error-mm", type=float, default=10.0,
                        help="refuse to save above this mean reprojection error")
    parser.add_argument("--force", action="store_true", help="save even above the error limit")
    args, _unknown = parser.parse_known_args(argv)

    config = Config.load(args.config_dir)
    table_z = float(config.table().get("z", -0.012))
    table_points = _parse_pairs(args.points, "--points")
    if len(table_points) < 4:
        raise SystemExit("need at least 4 table points (6-8 spread out is better)")

    if args.image:
        import cv2

        image = cv2.imread(args.image)
        if image is None:
            raise SystemExit(f"cannot read image {args.image}")
    else:
        image = _grab_frame(args.camera, args.config_dir)

    if args.pixels:
        pixels = _parse_pairs(args.pixels, "--pixels")
    else:
        print(f"click {len(table_points)} points on the table, in the order of --points:")
        for index, (x, y) in enumerate(table_points, start=1):
            print(f"  {index}: x={x:+.3f} y={y:+.3f}")
        pixels = _click_points(image, len(table_points))

    if len(pixels) != len(table_points):
        raise SystemExit(f"got {len(pixels)} pixels for {len(table_points)} table points")

    table_map = TableMap.fit(pixels, table_points, table_z)
    errors = []
    print("\npoint   pixel            base (measured)   reprojected       error")
    for index, ((u, v), (x, y)) in enumerate(zip(pixels, table_points), start=1):
        px, py = table_map.pixel_to_base(u, v)
        error = 1000.0 * ((px - x) ** 2 + (py - y) ** 2) ** 0.5
        errors.append(error)
        print(f"{index:5d}   ({u:6.1f},{v:6.1f})  ({x:+.3f},{y:+.3f})   "
              f"({px:+.3f},{py:+.3f})  {error:6.1f} mm")
    mean = float(np.mean(errors))
    print(f"\nmean reprojection error: {mean:.1f} mm")
    if mean > args.max_error_mm and not args.force:
        raise SystemExit(
            f"mean error {mean:.1f} mm exceeds --max-error-mm {args.max_error_mm:.1f}: "
            "re-measure the points, or pass --force if the marks themselves are rough"
        )

    table_map.meta.update(error_mm=round(mean, 2), camera=args.camera, points=len(pixels))
    out = Path(args.out).expanduser() if args.out else config.directory / "calibration.yaml"
    _write(out, args.camera, table_map)
    print(f"\nsaved {out}")
    print("restart agent_node (or the launch file) to pick it up")


if __name__ == "__main__":
    main()
