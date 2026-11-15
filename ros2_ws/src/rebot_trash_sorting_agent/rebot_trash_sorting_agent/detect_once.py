#!/usr/bin/env python3
"""One-shot detection check: what does the detector actually see, and where?

Use this before blaming the planner. It prints every detection, its score and - if
the table camera is calibrated - the base_link position the agent would use.

    ros2 run rebot_trash_sorting_agent detect_once
    ros2 run rebot_trash_sorting_agent detect_once --save /tmp/seen.jpg --conf 0.1
    ros2 run rebot_trash_sorting_agent detect_once --image frame.jpg --headless

``--image`` reads a file instead of a camera topic, so a photo from the bench is
enough to test the vocabulary.
"""

from __future__ import annotations

import argparse
import time

import numpy as np

from .config import Config
from .perception.detector import YoloeDetector, annotate
from .perception.table_map import TableMap


def _frame_from_topic(camera: str, config: Config) -> np.ndarray:
    import rclpy
    from rclpy.node import Node

    from .perception.scene import CameraClient

    rclpy.init()
    node = Node("detect_once")
    topic = config.capture_topic(camera)
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
        raise SystemExit(f"no frame on {topic}: is camera_node running?")
    return frame


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--camera", default="table")
    parser.add_argument("--config-dir", default=None)
    parser.add_argument("--image", default=None, help="read this file instead of the camera")
    parser.add_argument("--save", default=None, help="write the annotated frame here")
    parser.add_argument("--conf", type=float, default=None, help="override perception.conf")
    parser.add_argument("--classes", default=None,
                        help="comma-separated vocabulary override, e.g. 'can,cup,bottle'")
    parser.add_argument("--headless", action="store_true", help="never open a window")
    args, _unknown = parser.parse_known_args(argv)

    config = Config.load(args.config_dir)
    settings = dict(config.perception)
    if args.conf is not None:
        settings["conf"] = args.conf
    if args.classes:
        settings["classes"] = [c.strip() for c in args.classes.split(",") if c.strip()]

    if args.image:
        import cv2

        frame = cv2.imread(args.image)
        if frame is None:
            raise SystemExit(f"cannot read image {args.image}")
    else:
        frame = _frame_from_topic(args.camera, config)

    detector = YoloeDetector(settings)
    print(f"model: {detector.model_path}")
    print(f"vocabulary: {', '.join(detector.classes)}   conf >= {detector.conf}")
    started = time.monotonic()
    detections = detector.detect(frame)
    print(f"{len(detections)} detections in {time.monotonic() - started:.2f} s "
          f"(first call includes model load)")

    table_map = TableMap.from_mapping(
        config.table_map(args.camera), float(config.table().get("z", -0.012))
    )
    if table_map is None:
        print("\ntable camera not calibrated: positions are not available "
              "(run calibrate_table)")
    print("\nlabel               score  bbox px                     base x, y")
    for det in detections:
        where = "-"
        if table_map is not None:
            try:
                x, y = table_map.project(det)
                where = f"{x:+.3f}, {y:+.3f}"
            except ValueError:
                where = "outside the plane"
        x1, y1, x2, y2 = det.bbox
        print(f"{det.label:<18s} {det.score:5.2f}  ({x1:6.0f},{y1:6.0f},{x2:6.0f},{y2:6.0f})  {where}")

    annotated = annotate(frame, detections)
    if args.save:
        import cv2

        cv2.imwrite(args.save, annotated)
        print(f"\nsaved {args.save}")
    if not args.headless and not args.image:
        import cv2

        cv2.imshow("detect_once", annotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
