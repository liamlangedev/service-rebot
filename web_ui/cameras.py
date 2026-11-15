"""Direct OpenCV/V4L2 camera capture for the 3-camera live feed (ROS-free)."""

from __future__ import annotations

import logging
import threading
import time
from typing import Any

import numpy as np

log = logging.getLogger(__name__)


class CameraStream:
    """Continuously captures frames from one configured V4L2/OpenCV device."""

    def __init__(self, cfg: dict[str, Any]) -> None:
        self.name = str(cfg.get("name") or "camera")
        self.device = cfg.get("device", 0)
        self.width = int(cfg.get("width", 1280))
        self.height = int(cfg.get("height", 720))
        self.fps_target = float(cfg.get("fps", 15))
        self.fourcc = str(cfg.get("fourcc") or "").strip()
        self.warmup_s = float(cfg.get("warmup_s", 1.0))

        self._lock = threading.Lock()
        self._frame: np.ndarray | None = None
        self._stamp = 0.0
        self._frames = 0
        self._failures = 0
        self._fps = 0.0
        self._cap: Any = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name=f"cam-{self.name}", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:  # noqa: BLE001
                pass
            self._cap = None

    def _open(self) -> None:
        import cv2

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
        cap.set(cv2.CAP_PROP_FPS, self.fps_target)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self._cap = cap
        actual = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        log.info("%s: %r -> %dx%d @%.0f fps", self.name, self.device, actual[0], actual[1], cap.get(cv2.CAP_PROP_FPS))

    def _run(self) -> None:
        try:
            self._open()
        except Exception as exc:  # noqa: BLE001
            log.warning("%s: open failed (%s)", self.name, exc)
            return

        period = 1.0 / max(self.fps_target, 1.0)
        if self.warmup_s > 0:
            end = time.monotonic() + self.warmup_s
            while time.monotonic() < end and not self._stop.is_set():
                self._cap.read()
                time.sleep(0.02)

        while not self._stop.is_set():
            tick = time.monotonic()
            ok, frame = self._cap.read()
            if ok and frame is not None:
                now = time.monotonic()
                with self._lock:
                    if self._stamp > 0:
                        dt = now - self._stamp
                        if dt > 0:
                            inst = 1.0 / dt
                            self._fps = inst if self._fps == 0 else 0.85 * self._fps + 0.15 * inst
                    self._frame = frame
                    self._stamp = now
                    self._frames += 1
                    self._failures = 0
            else:
                self._failures += 1
                if self._failures >= 10:
                    log.warning("%s: %d consecutive read failures; reopening", self.name, self._failures)
                    try:
                        self._cap.release()
                        time.sleep(0.5)
                        self._open()
                    except Exception as exc:  # noqa: BLE001
                        log.warning("%s: reopen failed (%s)", self.name, exc)
                        time.sleep(1.0)
            elapsed = time.monotonic() - tick
            if elapsed < period:
                self._stop.wait(period - elapsed)

    @property
    def frames_received(self) -> int:
        with self._lock:
            return self._frames

    @property
    def fps(self) -> float:
        with self._lock:
            return self._fps

    def age_s(self) -> float:
        with self._lock:
            if self._stamp <= 0:
                return float("inf")
            return time.monotonic() - self._stamp

    def latest(self, max_age_s: float | None = None) -> np.ndarray | None:
        with self._lock:
            if self._frame is None:
                return None
            if max_age_s is not None and time.monotonic() - self._stamp > max_age_s:
                return None
            return self._frame.copy()

    def wait(self, timeout_s: float = 5.0) -> np.ndarray | None:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            frame = self.latest(max_age_s=2.0)
            if frame is not None:
                return frame
            time.sleep(0.05)
        return None

    def wait_fresh(self, timeout_s: float = 2.0) -> np.ndarray | None:
        start = self.frames_received
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if self.frames_received > start:
                return self.latest(max_age_s=1.0)
            time.sleep(0.02)
        return self.latest(max_age_s=1.0)


class CameraRig:
    """Manages all enabled cameras (table, wrist, front) from ``cameras.yaml``."""

    def __init__(self, camera_configs: list[dict[str, Any]]) -> None:
        self.streams: dict[str, CameraStream] = {
            str(cfg.get("name")): CameraStream(cfg)
            for cfg in camera_configs
            if cfg.get("enabled", True) and cfg.get("name")
        }

    def start(self) -> None:
        for stream in self.streams.values():
            stream.start()

    def stop(self) -> None:
        for stream in self.streams.values():
            stream.stop()

    def get(self, name: str) -> CameraStream | None:
        return self.streams.get(name)

    def snapshot_frames(self, max_age_s: float = 2.0) -> dict[str, np.ndarray]:
        frames: dict[str, np.ndarray] = {}
        for name, stream in self.streams.items():
            frame = stream.latest(max_age_s=max_age_s)
            if frame is not None:
                frames[name] = frame
        return frames
