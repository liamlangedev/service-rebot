"""Meta Quest controller input, plus a scripted fake source for testing.

Two ways to get controller poses off the headset:

  WebXRSource   (default) the vr-teleop-kit relay: a web page in the Quest
                browser streams WebXR poses over a WebSocket. Nothing to
                install on the headset.
  OculusSource  OculusReader: an APK on the headset, read over ADB.

Every source returns a ControllerSample whose pose is already in the ROBOT
frame (x forward, y left, z up, metres), using the per-source calibration
from tools/calibrate_quest_axes.py when present.
"""
import json
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"

# Default guess when no calibration exists: OpenXR/WebXR-style tracking frame
# (x right, y up, z towards the user), operator standing behind the robot
# facing the same way. vr-teleop-kit uses the same default (DEFAULT_R_CALIB).
# Run tools/calibrate_quest_axes.py to replace it.
DEFAULT_ROBOT_FROM_QUEST = np.array([
    [0.0, 0.0, -1.0],   # robot x (forward) = -quest z
    [-1.0, 0.0, 0.0],   # robot y (left)    = -quest x
    [0.0, 1.0, 0.0],    # robot z (up)      =  quest y
])

HANDS = {"r": "right", "l": "left"}

# OculusReader button keys per hand.
OCULUS_KEYS = {
    "r": dict(clutch="RG", trigger="rightTrig", reset="A", toggle_rot="B", record="RJ"),
    "l": dict(clutch="LG", trigger="leftTrig", reset="X", toggle_rot="Y", record="LJ"),
}

# WebXR "xr-standard" gamepad button indices (same on both hands).
XR_TRIGGER, XR_GRIP, XR_STICK, XR_A_X, XR_B_Y = 0, 1, 3, 4, 5

BUTTON_NAMES = {"r": dict(reset="A", toggle_rot="B"), "l": dict(reset="X", toggle_rot="Y")}


@dataclass
class ControllerSample:
    valid: bool = False
    pos: np.ndarray = field(default_factory=lambda: np.zeros(3))   # robot frame
    rot: np.ndarray = field(default_factory=lambda: np.eye(3))     # robot frame
    clutch: bool = False      # grip button held -> robot follows the hand
    trigger: float = 0.0      # index trigger 0..1 -> gripper closing
    reset: bool = False       # A / X -> go home
    toggle_rot: bool = False  # B / Y -> toggle orientation tracking
    record: bool = False      # joystick click -> start / save an episode
    raw: np.ndarray | None = None  # 4x4 pose in the Quest's own frame
    stamp: float = 0.0


def calibration_file(source: str) -> Path:
    return CONFIG_DIR / f"quest_calibration_{source}.json"


def load_calibration(source: str) -> np.ndarray:
    path = calibration_file(source)
    if path.exists():
        return np.array(json.loads(path.read_text())["robot_from_quest"], dtype=float)
    return DEFAULT_ROBOT_FROM_QUEST.copy()


def to_robot_frame(T_quest: np.ndarray, robot_from_quest: np.ndarray):
    """Converts a 4x4 Quest-frame pose to (pos, rot) in the robot frame.

    Conjugating by the frame change keeps rotations proper even if the Quest
    frame turns out to be left-handed (robot_from_quest with det = -1).
    """
    C = robot_from_quest
    pos = C @ T_quest[:3, 3]
    rot = C @ T_quest[:3, :3] @ C.T
    return pos, rot


class _QuestSource:
    """Shared conversion from a raw Quest reading to a ControllerSample."""
    name = ""

    def __init__(self, hand: str, robot_from_quest: np.ndarray | None):
        self.hand = hand
        self.C = load_calibration(self.name) if robot_from_quest is None else robot_from_quest

    def _raw(self):
        """(4x4 Quest-frame pose or None, dict of clutch/trigger/reset/toggle_rot/record)."""
        raise NotImplementedError

    def read(self) -> ControllerSample:
        T, b = self._raw()
        if T is None:
            return ControllerSample(valid=False, stamp=time.time())
        pos, rot = to_robot_frame(T, self.C)
        return ControllerSample(valid=True, pos=pos, rot=rot, raw=T, stamp=time.time(), **b)


class WebXRSource(_QuestSource):
    """Subscribes to `xr_frame` messages from the vr-teleop-kit relay.

    Start the relay first (`uv run vr-teleop-relay`), open its page in the
    Quest browser and press "Start Teleop".
    """
    name = "webxr"

    def __init__(self, hand: str = "r", url: str = "ws://127.0.0.1:8443/ws",
                 robot_from_quest: np.ndarray | None = None):
        super().__init__(hand, robot_from_quest)
        from websockets.sync.client import connect

        self._ws = connect(url, open_timeout=5)
        self._latest = None
        self._lock = threading.Lock()
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def _listen(self):
        hand = HANDS[self.hand]
        try:
            for raw in self._ws:
                if not self._running:
                    break
                msg = json.loads(raw)
                if msg.get("type") != "xr_frame":
                    continue
                ctrl = (msg.get("controllers") or {}).get(hand)
                if ctrl is not None:
                    with self._lock:
                        self._latest = (ctrl, time.time())
        except Exception as e:  # connection closed / relay stopped
            if self._running:
                print(f"[webxr] relay connection lost: {e}")

    def _raw(self):
        with self._lock:
            latest = self._latest
        if latest is None or time.time() - latest[1] > 0.5:  # stale: page closed
            return None, {}
        ctrl, _ = latest
        x, y, z, w = ctrl["orientation"]  # WebXR sends xyzw
        R = np.empty(9)
        mujoco.mju_quat2Mat(R, np.array([w, x, y, z], dtype=float))
        T = np.eye(4)
        T[:3, :3] = R.reshape(3, 3)
        T[:3, 3] = ctrl["position"]
        btn = ctrl.get("buttons") or []

        def pressed(i):
            return bool(btn[i]["p"]) if len(btn) > i else False

        return T, dict(clutch=pressed(XR_GRIP),
                       trigger=float(btn[XR_TRIGGER]["v"]) if btn else 0.0,
                       reset=pressed(XR_A_X), toggle_rot=pressed(XR_B_Y),
                       record=pressed(XR_STICK))

    def close(self):
        self._running = False
        self._ws.close()


class OculusSource(_QuestSource):
    """Reads one controller from the Quest through OculusReader (ADB + APK)."""
    name = "oculus"

    def __init__(self, hand: str = "r", ip_address: str | None = None,
                 robot_from_quest: np.ndarray | None = None):
        super().__init__(hand, robot_from_quest)
        from oculus_reader.reader import OculusReader  # needs adb + the APK

        self.keys = OCULUS_KEYS[hand]
        self.reader = OculusReader(ip_address=ip_address)

    def _raw(self):
        transforms, buttons = self.reader.get_transformations_and_buttons()
        T = (transforms or {}).get(self.hand)
        buttons = buttons or {}
        trig = buttons.get(self.keys["trigger"], (0.0,))
        return T, dict(
            clutch=bool(buttons.get(self.keys["clutch"], False)),
            trigger=float(trig[0]) if isinstance(trig, tuple) else float(trig),
            reset=bool(buttons.get(self.keys["reset"], False)),
            toggle_rot=bool(buttons.get(self.keys["toggle_rot"], False)),
            record=bool(buttons.get(self.keys["record"], False)),
        )

    def close(self):
        self.reader.stop()


def make_quest_source(kind: str, hand: str = "r", ip: str | None = None,
                      relay_url: str = "ws://127.0.0.1:8443/ws",
                      robot_from_quest: np.ndarray | None = None):
    if kind == "webxr":
        return WebXRSource(hand, relay_url, robot_from_quest)
    return OculusSource(hand, ip, robot_from_quest)


class DemoSource:
    """Scripted fake controller: draws a circle and squeezes the trigger.

    Lets the whole pipeline run without a headset (also used for headless tests).
    """

    def __init__(self, radius: float = 0.08, period: float = 6.0):
        self.radius = radius
        self.period = period
        self.t0 = time.time()

    def read(self, t: float | None = None) -> ControllerSample:
        t = (time.time() - self.t0) if t is None else t
        w = 2 * np.pi / self.period
        pos = np.array([0.0, self.radius * np.sin(w * t), self.radius * (np.cos(w * t) - 1)])
        # Gentle wrist roll about the forward axis.
        a = 0.3 * np.sin(w * t)
        rot = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
        return ControllerSample(valid=True, pos=pos, rot=rot, clutch=t > 0.5,
                                trigger=0.5 * (1 - np.cos(w * t)), stamp=time.time())

    def close(self):
        pass


class ClutchTeleop:
    """Clutch-relative mapping from controller motion to a TCP target.

    While the clutch (grip button) is held, the target moves by the controller's
    displacement since the clutch was pressed (scaled), and rotates by the
    controller's rotation since then. Releasing the clutch freezes the target,
    so you can re-centre your hand, just like lifting a mouse.
    """

    def __init__(self, pos_scale: float = 1.0, track_rotation: bool = True,
                 smoothing: float = 0.3, workspace_lo=(-0.1, -0.5, 0.03),
                 workspace_hi=(0.65, 0.5, 0.75), max_reach: float = 0.62):
        self.pos_scale = pos_scale
        self.track_rotation = track_rotation
        self.smoothing = smoothing  # 0 = no filtering, ->1 = heavy filtering
        self.lo = np.array(workspace_lo)
        self.hi = np.array(workspace_hi)
        self.max_reach = max_reach
        self._engaged = False
        self._prev_toggle = False
        self._ctrl0 = None
        self._target0 = None
        self._filtered = None

    @property
    def engaged(self):
        return self._engaged

    def update(self, s: ControllerSample, target_pos, target_rot):
        """Returns the new (target_pos, target_rot)."""
        if s.toggle_rot and not self._prev_toggle:
            self.track_rotation = not self.track_rotation
            self._engaged = False  # re-anchor so the switch does not cause a jump
            print(f"[teleop] rotation tracking {'ON' if self.track_rotation else 'OFF'}")
        self._prev_toggle = s.toggle_rot

        if not (s.valid and s.clutch):
            self._engaged = False
            return target_pos, target_rot

        if not self._engaged:
            self._engaged = True
            self._ctrl0 = (s.pos.copy(), s.rot.copy())
            self._target0 = (np.array(target_pos), np.array(target_rot))
            self._filtered = None

        p0, R0 = self._ctrl0
        tp0, tR0 = self._target0
        pos = tp0 + self.pos_scale * (s.pos - p0)
        rot = (s.rot @ R0.T) @ tR0 if self.track_rotation else tR0

        if self._filtered is not None and self.smoothing > 0:
            a = self.smoothing
            pos = a * self._filtered + (1 - a) * pos
        self._filtered = pos
        return self._clamp(pos), rot

    def _clamp(self, pos):
        pos = np.clip(pos, self.lo, self.hi)
        shoulder = np.array([0.0, 0.0, 0.14])  # approx. joint2 height
        v = pos - shoulder
        r = np.linalg.norm(v)
        if r > self.max_reach:
            pos = shoulder + v * (self.max_reach / r)
        return pos
