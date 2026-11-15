"""Ultraleap hand tracking as a ControllerSample source.

Same interface as QuestSource, so ClutchTeleop/DiffIK work unchanged.
  * clutch   = left-hand fist (with hysteresis) or the spacebar
  * trigger  = gripper closing, from the thumb-index distance of the driving hand
The right hand drives; a lone hand is used only while the spacebar is held.
"""
import math
import threading
import time

import numpy as np
from scipy.spatial.transform import Rotation

from teleop.quest_input import ControllerSample

# Leap (x right, y up, z towards user) -> robot (x forward, y left, z up).
ROBOT_FROM_LEAP = np.array([[0.0, 0.0, -1.0],
                            [-1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0]])

FINGER_DIST_OPEN = 80.0    # mm
FINGER_DIST_CLOSED = 25.0  # mm
GRIP_CLOSED_DEADZONE = 0.2
GRIP_OPEN_DEADZONE = 0.1
GRAB_ON, GRAB_OFF = 0.9, 0.6
CLUTCH_RELEASE_DELAY = 0.3  # a fist that opens or leaves view for less than this keeps the clutch engaged
STALE_S = 0.15  # no tracking frame for this long -> sample is invalid (arm holds)


class LeapSource:
    def __init__(self, yaw_offset_deg: float = 0.0, use_keyboard: bool = True):
        import leap  # needs the Ultraleap service and libLeapC

        self._yaw = Rotation.from_euler("z", yaw_offset_deg, degrees=True).as_matrix()
        self._lock = threading.Lock()
        self._sample = ControllerSample(valid=False)
        self._fist = False
        self._fist_lost_t = None
        self._space = False
        self._kb = None

        outer = self

        class _Listener(leap.Listener):
            def on_tracking_event(self, event):
                outer._on_tracking(event)

        self._conn = leap.Connection()
        self._conn.add_listener(_Listener())
        self._ctx = self._conn.open()
        self._ctx.__enter__()

        if use_keyboard:
            from pynput import keyboard
            self._kb = keyboard.Listener(
                on_press=lambda k: self._key(k, True), on_release=lambda k: self._key(k, False))
            self._kb.start()

    def _key(self, key, down):
        from pynput import keyboard
        if key == keyboard.Key.space:
            self._space = down

    def _on_tracking(self, event):
        left = next((h for h in event.hands if str(h.type) == "HandType.Left"), None)
        right = next((h for h in event.hands if str(h.type) == "HandType.Right"), None)
        closed = left is not None and left.grab_strength > (GRAB_OFF if self._fist else GRAB_ON)
        now = time.time()
        if closed:
            self._fist, self._fist_lost_t = True, None
        elif self._fist:
            # Left-hand tracking drops out briefly; only release after a sustained loss.
            self._fist_lost_t = self._fist_lost_t or now
            if now - self._fist_lost_t > CLUTCH_RELEASE_DELAY:
                self._fist, self._fist_lost_t = False, None

        hand = right
        if hand is None and len(event.hands) == 1 and self._space:
            hand = event.hands[0]
        if hand is None:
            with self._lock:
                self._sample = ControllerSample(valid=False, stamp=time.time())
            return

        C = self._yaw @ ROBOT_FROM_LEAP
        p = hand.palm.position
        o = hand.palm.orientation
        pos = C @ (np.array([p.x, p.y, p.z]) / 1000.0)
        rot = C @ Rotation.from_quat([o.x, o.y, o.z, o.w]).as_matrix() @ C.T

        a = hand.digits[0].distal.next_joint
        b = hand.digits[1].distal.next_joint
        dist = math.dist((a.x, a.y, a.z), (b.x, b.y, b.z))
        openness = (dist - FINGER_DIST_CLOSED) / (FINGER_DIST_OPEN - FINGER_DIST_CLOSED)
        openness = (openness - GRIP_CLOSED_DEADZONE) / (1 - GRIP_CLOSED_DEADZONE - GRIP_OPEN_DEADZONE)
        openness = float(np.clip(openness, 0.0, 1.0))

        with self._lock:
            self._sample = ControllerSample(
                valid=True, pos=pos, rot=rot, clutch=self._fist or self._space,
                trigger=1.0 - openness, stamp=time.time())

    def read(self) -> ControllerSample:
        with self._lock:
            s = self._sample
        if s.valid and time.time() - s.stamp > STALE_S:
            return ControllerSample(valid=False, stamp=time.time())
        return s

    def close(self):
        if self._kb is not None:
            self._kb.stop()
        self._ctx.__exit__(None, None, None)
