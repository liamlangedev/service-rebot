"""MuJoCo + Gaussian-splat digital twin driven by streamed joint values (ROS-free)."""

from __future__ import annotations

from collections.abc import Sequence
import logging
from pathlib import Path
import sys
import threading
import time
from typing import Any

import numpy as np

log = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SIM_DIR = _REPO_ROOT / "simulation"

ARM_JOINT_NAMES = ("joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6")
GRIPPER_JOINT_NAME = "finger_left"


def _ensure_sim_path() -> None:
    sim_str = str(_SIM_DIR)
    if sim_str not in sys.path:
        sys.path.insert(0, sim_str)


class DigitalTwin:
    """Renders the MuJoCo reBot arm + optional Gaussian-splat objects from streamed joints."""

    def __init__(self, cfg: dict[str, Any] | None = None) -> None:
        self.cfg = dict(cfg or {})
        self.enabled = bool(self.cfg.get("enabled", True))
        self.web_view = bool(self.cfg.get("web_view", True))
        self.web_view_port = int(self.cfg.get("web_view_port", 8765))
        self.camera = str(self.cfg.get("camera", "cam_corner"))
        self.width = int(self.cfg.get("width", 480))
        self.height = int(self.cfg.get("height", 360))
        self.fps_target = float(self.cfg.get("fps", 30.0))

        splats_raw = str(self.cfg.get("splats_dir", "simulation/splats"))
        splats_path = Path(splats_raw)
        self.splats_dir = splats_path if splats_path.is_absolute() else (_REPO_ROOT / splats_path)
        self.object_splats: dict[str, str] = {
            str(k): str(v) for k, v in dict(self.cfg.get("objects") or {}).items()
        }

        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

        self._joints: dict[str, float] = {}
        self._joint_stamp = 0.0
        self._joint_updates = 0
        self._dirty = True

        self._jpeg: bytes | None = None
        self._frames = 0
        self._ready = False
        self._error: str | None = None
        self._loaded_splats: list[str] = []

        self._env: Any = None
        self._comp: Any = None
        self._vr: Any = None
        self._mujoco: Any = None

    def start(self) -> None:
        if not self.enabled:
            return
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="digital-twin", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._wake.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        if self._vr is not None:
            try:
                self._vr.stop()
            except Exception:  # noqa: BLE001
                pass
            self._vr = None
        if self._comp is not None:
            try:
                self._comp.close()
            except Exception:  # noqa: BLE001
                pass
            self._comp = None

    def update_joints(self, joints: Sequence[float] | dict[str, float]) -> dict[str, float]:
        """Stream new joint positions (list of 6-7 floats or {name: value} mapping)."""
        parsed: dict[str, float] = {}
        if isinstance(joints, dict):
            for k, v in joints.items():
                parsed[str(k)] = float(v)
        elif isinstance(joints, (list, tuple)):
            names = (*ARM_JOINT_NAMES, GRIPPER_JOINT_NAME)
            for idx, val in enumerate(joints[: len(names)]):
                parsed[names[idx]] = float(val)
        else:
            raise ValueError("joints must be a list of floats or a {name: value} mapping")

        if not parsed:
            raise ValueError("empty joints payload")

        with self._lock:
            self._joints.update(parsed)
            self._joint_stamp = time.monotonic()
            self._joint_updates += 1
            self._dirty = True
            snapshot = dict(self._joints)
        self._wake.set()
        return snapshot

    def joints_snapshot(self) -> dict[str, Any]:
        with self._lock:
            age = None if self._joint_stamp <= 0 else round(time.monotonic() - self._joint_stamp, 3)
            return {
                "joints": dict(self._joints),
                "updates": self._joint_updates,
                "age_s": age,
            }

    def status(self) -> dict[str, Any]:
        with self._lock:
            age = None if self._joint_stamp <= 0 else round(time.monotonic() - self._joint_stamp, 3)
            return {
                "enabled": self.enabled,
                "ready": self._ready,
                "error": self._error,
                "web_view": self.web_view,
                "web_view_port": self.web_view_port,
                "camera": self.camera,
                "splats": list(self._loaded_splats),
                "frames": self._frames,
                "joints": dict(self._joints),
                "joint_updates": self._joint_updates,
                "joint_age_s": age,
            }

    def latest_jpeg(self) -> bytes | None:
        with self._lock:
            return self._jpeg

    def _init_scene(self) -> None:
        import mujoco

        _ensure_sim_path()
        from rebot_sim import RealSetupEnv
        from teleop.vr_view import VRBridge

        env = RealSetupEnv(objects=bool(self.object_splats))
        splat_paths: dict[str, Path] = {}
        for body_name, filename in self.object_splats.items():
            ply_path = self.splats_dir / filename
            if ply_path.is_file():
                splat_paths[body_name] = ply_path
                bid = env.model.body(body_name).id
                env.model.geom_group[env.model.geom_bodyid == bid] = 3
            else:
                log.warning("digital_twin: splat file missing: %s", ply_path)

        vr = None
        if self.web_view:
            vr = VRBridge(env.model, port=self.web_view_port, splats=splat_paths)
            vr.start()
            log.info("Three.js simulation view listening on http://127.0.0.1:%d/", self.web_view_port)

        self._mujoco = mujoco
        self._env = env
        self._vr = vr
        with self._lock:
            self._loaded_splats = sorted(splat_paths.keys())
            self._ready = True
            self._error = None

    def _ensure_compositor(self) -> Any:
        if self._comp is None:
            from rebot_sim.splat_render import SplatCompositor, SplatObject

            splats = {
                name: SplatObject.load(self.splats_dir / self.object_splats[name])
                for name in self._loaded_splats
            }
            self._comp = SplatCompositor(self._env, splats)
        return self._comp

    def _apply_joints(self, joints: dict[str, float]) -> None:
        env = self._env
        if env is None or not joints:
            return
        for name, value in joints.items():
            try:
                jid = env.model.joint(name).id
                adr = int(env.model.jnt_qposadr[jid])
                env.data.qpos[adr] = float(value)
            except Exception:  # noqa: BLE001
                continue
        self._mujoco.mj_forward(env.model, env.data)

    def _render_once(self) -> bytes | None:
        import cv2

        with self._lock:
            joints = dict(self._joints)
            self._dirty = False
        self._apply_joints(joints)
        rgb = self._ensure_compositor().render(camera=self.camera, width=self.width, height=self.height)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        ok, buf = cv2.imencode(".jpg", bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        return buf.tobytes() if ok else None

    def _run(self) -> None:
        try:
            self._init_scene()
        except Exception as exc:  # noqa: BLE001
            log.warning("digital_twin init failed: %s", exc)
            with self._lock:
                self._error = str(exc)
                self._ready = False
            return

        period = 1.0 / max(self.fps_target, 1.0)
        while not self._stop.is_set():
            tick = time.monotonic()
            with self._lock:
                joints = dict(self._joints)
                dirty = self._dirty
                self._dirty = False
            if dirty or self._frames == 0:
                self._apply_joints(joints)
            if self._vr is not None:
                self._vr.publish(self._env.data)
                with self._lock:
                    self._frames += 1
            elif dirty or self._jpeg is None:
                try:
                    encoded = self._render_once()
                    if encoded is not None:
                        with self._lock:
                            self._jpeg = encoded
                            self._frames += 1
                except Exception as exc:  # noqa: BLE001
                    log.warning("digital_twin render failed: %s", exc)
                    with self._lock:
                        self._error = str(exc)
                    self._stop.wait(1.0)
                    continue
            elapsed = time.monotonic() - tick
            wait_s = max(0.01, period - elapsed)
            self._wake.wait(timeout=wait_s)
            self._wake.clear()
