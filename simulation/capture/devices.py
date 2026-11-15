"""USB cameras and the arm's serial port: discovery, roles, and frame streams.

The role -> device map lives in capture/devices.json (per machine, not committed),
written by the device UI (capture/device_ui.py). Devices are stored by stable
ids (/dev/v4l/by-id, /dev/serial/by-id on Linux) so the roles survive replugging.
"""
from __future__ import annotations

import glob
import json
import os
import platform
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np

CAPTURE_DIR = Path(__file__).resolve().parent
SIM_DIR = CAPTURE_DIR.parent
if str(SIM_DIR) not in sys.path:
    sys.path.insert(0, str(SIM_DIR))

DEVICES_FILE = CAPTURE_DIR / "devices.json"
ROLES = ["cam_corner", "cam_far", "wrist"]
FULL_RES = (1920, 1080)


@dataclass
class Device:
    key: str     # stable id shown to the user
    path: str    # what to open (device path or camera index)
    label: str   # human-readable name


# ----------------------------------------------------------------- discovery
def list_cameras() -> list[Device]:
    if platform.system() == "Linux":
        return _list_cameras_linux()
    # macOS / Windows: OpenCV indices (opening is the only way to probe).
    out = []
    for i in range(8):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            out.append(Device(f"index:{i}", str(i), f"camera index {i}"))
        cap.release()
    return out


def _list_cameras_linux() -> list[Device]:
    by_id = {os.path.realpath(p): p for p in glob.glob("/dev/v4l/by-id/*")}
    by_path = {os.path.realpath(p): p for p in glob.glob("/dev/v4l/by-path/*")}
    out = []
    for sys_dir in sorted(glob.glob("/sys/class/video4linux/video*"),
                          key=lambda p: int(p.rsplit("video", 1)[1])):
        dev = "/dev/" + os.path.basename(sys_dir)
        try:  # each USB camera has several nodes; index 0 is the image stream
            if Path(sys_dir, "index").read_text().strip() != "0":
                continue
            name = Path(sys_dir, "name").read_text().strip()
        except OSError:
            continue
        stable = by_id.get(dev) or by_path.get(dev) or dev
        out.append(Device(stable, dev, f"{name} ({dev})"))
    return out


def list_serial_ports() -> list[Device]:
    out, seen = [], set()
    for p in sorted(glob.glob("/dev/serial/by-id/*")):
        real = os.path.realpath(p)
        seen.add(real)
        out.append(Device(p, real, f"{os.path.basename(p)} ({real})"))
    for pat in ("/dev/ttyACM*", "/dev/ttyUSB*", "/dev/tty.usbmodem*", "/dev/tty.usbserial*",
                "/dev/cu.usbmodem*"):
        for p in sorted(glob.glob(pat)):
            if os.path.realpath(p) not in seen:
                out.append(Device(p, p, p))
    return out


def resolve(dev: dict) -> str:
    """Current device path for a stored device (stable link if it still exists)."""
    key, path = dev.get("key", ""), dev.get("path", "")
    if key.startswith("/dev/") and os.path.exists(key):
        return os.path.realpath(key)
    return path


# ----------------------------------------------------------------- device map
def load_devices(path: Path = DEVICES_FILE) -> dict | None:
    return json.loads(path.read_text()) if path.exists() else None


def save_devices(cameras: dict[str, Device], arm: Device | None, path: Path = DEVICES_FILE):
    data = {"cameras": {role: asdict(d) for role, d in cameras.items()},
            "arm": asdict(arm) if arm else None,
            "saved": time.strftime("%Y-%m-%d %H:%M:%S")}
    path.write_text(json.dumps(data, indent=2) + "\n")
    return data


# ----------------------------------------------------------------- streams
class CameraStream:
    """Background reader that always holds the newest frame (BGR)."""

    def __init__(self, path: str, size=FULL_RES, fps: int = 30):
        src = int(path) if path.isdigit() else path
        api = cv2.CAP_V4L2 if platform.system() == "Linux" and not path.isdigit() else cv2.CAP_ANY
        self.cap = cv2.VideoCapture(src, api)
        if not self.cap.isOpened():
            raise RuntimeError(f"cannot open camera {path}")
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.path = path
        self._frame, self._t = None, 0.0
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            ok, frame = self.cap.read()
            if ok:
                with self._lock:
                    self._frame, self._t = frame, time.time()
            else:
                time.sleep(0.02)

    def read(self, fresh_after: float | None = None, timeout: float = 3.0) -> np.ndarray:
        """Newest frame; with fresh_after, waits for one captured after that time."""
        t_end = time.time() + timeout
        while time.time() < t_end:
            with self._lock:
                if self._frame is not None and (fresh_after is None or self._t > fresh_after):
                    return self._frame.copy()
            time.sleep(0.01)
        raise TimeoutError(f"no frame from camera {self.path}")

    @property
    def size(self) -> tuple[int, int]:
        return (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def close(self):
        self._stop.set()
        self._thread.join(timeout=1.0)
        self.cap.release()


class SimCameraHub:
    """Stand-in cameras for --fake: one thread renders the sim cameras of a
    RealSetupEnv (an OpenGL context belongs to the thread that made it).
    Change env.data only while holding `hub.lock`."""

    def __init__(self, env, cameras: list[str], size=FULL_RES, period: float = 0.1):
        self.env, self.cameras, self.size, self.period = env, cameras, size, period
        self.lock = threading.Lock()
        self._frames: dict[str, tuple[np.ndarray, float]] = {}
        self._cond = threading.Condition()
        self._stop = threading.Event()
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        import mujoco
        renderer = mujoco.Renderer(self.env.model, height=self.size[1], width=self.size[0])
        while not self._stop.is_set():
            for cam in self.cameras:
                with self.lock:
                    renderer.update_scene(self.env.data, camera=cam)
                rgb = renderer.render()
                with self._cond:
                    self._frames[cam] = (cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), time.time())
                    self._cond.notify_all()
            time.sleep(self.period)
        renderer.close()

    def read(self, cam, fresh_after=None, timeout=3.0):
        t_end = time.time() + timeout
        with self._cond:
            while True:
                f = self._frames.get(cam)
                if f is not None and (fresh_after is None or f[1] > fresh_after):
                    return f[0].copy()
                left = t_end - time.time()
                if left <= 0:
                    raise TimeoutError(f"no frame from sim camera {cam}")
                self._cond.wait(left)

    def stream(self, cam) -> "SimCameraStream":
        return SimCameraStream(self, cam)

    def close(self):
        self._stop.set()


class SimCameraStream:
    def __init__(self, hub: SimCameraHub, camera: str):
        self.hub, self.camera, self.path = hub, camera, f"sim:{camera}"

    def read(self, fresh_after: float | None = None, timeout: float = 3.0) -> np.ndarray:
        return self.hub.read(self.camera, fresh_after, timeout)

    @property
    def size(self):
        return self.hub.size

    def close(self):
        pass


def open_streams(devices: dict, size=FULL_RES) -> dict[str, CameraStream]:
    streams = {}
    for role, dev in devices["cameras"].items():
        streams[role] = CameraStream(resolve(dev), size)
    return streams
