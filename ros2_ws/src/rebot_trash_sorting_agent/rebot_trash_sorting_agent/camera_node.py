#!/usr/bin/env python3
"""Capture the RGB cameras and publish ``<topic>/image_raw`` + ``camera_info``.

There is no camera driver in this repository, so this node is the driver: it opens
each device in ``cameras.yaml`` with OpenCV/V4L2, in its own thread, and republishes
frames as ``sensor_msgs/Image`` (bgr8). Device selection is a config line, so moving
a camera from ``/dev/video0`` to ``/dev/video2`` or to a stable
``/dev/v4l/by-id/...`` path never needs a code change.

Nothing here knows about detection, homographies or the robot: it is a camera
driver and nothing else. ``scripts/calibrate_table.py`` and the agent subscribe.
"""

from __future__ import annotations

import argparse
import math
import threading
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from .config import Config
from .ros_image import bgr_to_imgmsg


class CameraStream:
    def __init__(self, node: Node, cfg: dict) -> None:
        import cv2
        from sensor_msgs.msg import CameraInfo, Image

        self._cv2 = cv2
        self._node = node
        self._cfg = cfg
        self.name = str(cfg.get("name") or "camera")
        base = str(cfg.get("topic") or f"/{self.name}_cam").rstrip("/")
        self.topic = f"{base}/image_raw"
        self.info_topic = f"{base}/camera_info"
        self.device = cfg.get("device", 0)
        self.width = int(cfg.get("width", 1280))
        self.height = int(cfg.get("height", 720))
        self.fps = float(cfg.get("fps", 15))
        self.fourcc = str(cfg.get("fourcc") or "").strip()
        self.warmup_s = float(cfg.get("warmup_s", 1.0))
        self.frame_id = str(cfg.get("frame_id") or f"{self.name}_optical_frame")

        self._bridge = None
        self._Image = Image
        self.image_pub = node.create_publisher(Image, self.topic, qos_profile_sensor_data)
        self.info_pub = node.create_publisher(CameraInfo, self.info_topic, qos_profile_sensor_data)
        self._info = self._camera_info(float(cfg.get("fov_deg", 75.0)))

        self._cap = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self.frames = 0
        self.failures = 0

    # ------------------------------------------------------------------ device
    def _open(self) -> None:
        cv2 = self._cv2
        device = self.device
        if isinstance(device, str) and device.isdigit():
            device = int(device)
        backend = cv2.CAP_V4L2 if isinstance(device, int) or str(device).startswith("/dev/") else cv2.CAP_ANY
        cap = cv2.VideoCapture(device, backend)
        if not cap.isOpened():
            raise RuntimeError(f"{self.name}: cannot open {self.device!r}")
        if self.fourcc:
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.fourcc[:4].ljust(4)))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv2.CAP_PROP_FPS, self.fps)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self._cap = cap
        actual = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self._node.get_logger().info(
            f"{self.name}: {self.device!r} -> {actual[0]}x{actual[1]} "
            f"@{cap.get(cv2.CAP_PROP_FPS):.0f} fps on {self.topic}"
        )
        if actual[0] and abs(actual[0] - self.width) > 1:
            # K was built from the requested size; keep them consistent.
            self.width, self.height = actual
            self._info = self._camera_info(float(self._cfg.get("fov_deg", 75.0)))

    def _camera_info(self, fov_deg: float):
        from sensor_msgs.msg import CameraInfo

        info = CameraInfo()
        info.header.frame_id = self.frame_id
        info.width, info.height = self.width, self.height
        focal = (self.width / 2.0) / max(math.tan(math.radians(fov_deg) / 2.0), 1e-6)
        info.k = [focal, 0.0, self.width / 2.0, 0.0, focal, self.height / 2.0, 0.0, 0.0, 1.0]
        info.p = [focal, 0.0, self.width / 2.0, 0.0, 0.0, focal, self.height / 2.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        info.distortion_model = "plumb_bob"
        info.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        return info

    # ------------------------------------------------------------------ loop
    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, name=f"{self.name}_capture", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def _run(self) -> None:
        period = 1.0 / self.fps if self.fps > 0 else 0.0
        next_open = 0.0
        while not self._stop.is_set():
            if self._cap is None:
                if time.monotonic() < next_open:
                    time.sleep(0.1)
                    continue
                try:
                    self._open()
                    time.sleep(self.warmup_s)
                    # Throw away the first frames: auto-exposure settles here.
                    for _ in range(3):
                        self._cap.read()
                except Exception as exc:  # noqa: BLE001 - a missing camera must not kill the node
                    self.failures += 1
                    if self.failures % 10 == 1:
                        self._node.get_logger().error(str(exc))
                    self._cap = None
                    next_open = time.monotonic() + 3.0
                    continue

            started = time.monotonic()
            ok, frame = self._cap.read()
            if not ok or frame is None:
                self.failures += 1
                self._node.get_logger().warn(f"{self.name}: frame grab failed; reopening")
                self._cap.release()
                self._cap = None
                next_open = time.monotonic() + 1.0
                continue

            stamp = self._node.get_clock().now().to_msg()
            try:
                message = bgr_to_imgmsg(frame, stamp=stamp, frame_id=self.frame_id)
            except Exception as exc:  # noqa: BLE001
                self._node.get_logger().warn(f"{self.name}: image encode failed ({exc})")
                continue
            self.image_pub.publish(message)
            self._info.header.stamp = stamp
            self.info_pub.publish(self._info)
            self.frames += 1

            if period:
                time.sleep(max(0.0, period - (time.monotonic() - started)))


class CameraNode(Node):
    def __init__(self, config: Config, names: list[str] | None = None) -> None:
        super().__init__("camera_node")
        wanted = list(names or [c["name"] for c in config.camera_list])
        self.streams = [
            CameraStream(self, config.camera(name))
            for name in wanted
            if config.camera(name).get("enabled", True)
        ]
        for stream in self.streams:
            stream.start()
        self.get_logger().info(f"publishing {', '.join(s.topic for s in self.streams)}")

    def destroy_node(self) -> bool:
        for stream in self.streams:
            stream.stop()
        return super().destroy_node()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", default=None, help="directory holding cameras.yaml")
    parser.add_argument("--camera", action="append", help="only start this camera (repeatable)")
    args, ros_args = parser.parse_known_args(argv)

    rclpy.init(args=ros_args)
    config = Config.load(args.config_dir)
    node = CameraNode(config, args.camera)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
