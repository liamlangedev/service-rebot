"""lerobot teleoperator: Ultraleap hand -> clutch -> IK -> reBot joint targets.

Registered as `--teleop.type=leap_ik`. Outputs absolute joint positions in
degrees (`shoulder_pan.pos` ... `gripper.pos`), the same layout as the
rebot_b601_follower action, so the recorded dataset needs no conversion.
The arm must already be at the ready pose (run go_ready.py first).
"""
import time
from dataclasses import dataclass

import numpy as np

from lerobot.teleoperators.config import TeleoperatorConfig
from lerobot.teleoperators.teleoperator import Teleoperator

from teleop.ik import DiffIK
from teleop.leap_input import LeapSource
from teleop.quest_input import ClutchTeleop
from teleop.rebot_model import ARM_JOINTS, TCP_SITE, RebotSim
from teleop.rebot_real import (GRIPPER_OPEN_DEG, READY_QPOS, JOINT_NAMES,
                               gripper_from_closing, guarded_solve, q_to_action)


@TeleoperatorConfig.register_subclass("leap_ik")
@dataclass(kw_only=True)
class LeapIKConfig(TeleoperatorConfig):
    scale: float = 1.0
    track_rotation: bool = False
    yaw_offset_deg: float = 0.0
    max_joint_vel: float = 2.5  # rad/s, IK output limit


class LeapIK(Teleoperator):
    config_class = LeapIKConfig
    name = "leap_ik"

    def __init__(self, config: LeapIKConfig):
        super().__init__(config)
        self.config = config
        self._source = None

    @property
    def action_features(self) -> dict:
        return {f"{n}.pos": float for n in [*JOINT_NAMES, "gripper"]}

    @property
    def feedback_features(self) -> dict:
        return {}

    @property
    def is_connected(self) -> bool:
        return self._source is not None

    @property
    def is_calibrated(self) -> bool:
        return True

    def calibrate(self) -> None:
        pass

    def configure(self) -> None:
        pass

    def connect(self, calibrate: bool = True) -> None:
        model = RebotSim().model
        self._ik = DiffIK(model, TCP_SITE, ARM_JOINTS, q_rest=READY_QPOS,
                          max_joint_vel=self.config.max_joint_vel)
        self._teleop = ClutchTeleop(pos_scale=self.config.scale,
                                    track_rotation=self.config.track_rotation)
        self._q = READY_QPOS.copy()
        self._target = self._ik.fk(self._q)
        self._gripper = GRIPPER_OPEN_DEG
        self._t = time.perf_counter()
        self._source = LeapSource(yaw_offset_deg=self.config.yaw_offset_deg)

    def get_action(self) -> dict[str, float]:
        now = time.perf_counter()
        dt = float(np.clip(now - self._t, 1e-3, 0.1))
        self._t = now

        s = self._source.read()
        pos, rot = self._teleop.update(s, *self._target)
        self._target = (pos, rot)
        # With rotation tracking off, `rot` stays at the ready orientation, so the
        # IK holds the tool pointing down instead of letting it tilt as the arm extends.
        self._q, _, _, _ = guarded_solve(self._ik, self._q, pos, rot, dt)
        if s.valid:
            self._gripper = gripper_from_closing(s.trigger)
        return q_to_action(self._q, self._gripper)

    def send_feedback(self, feedback) -> None:
        pass

    def disconnect(self) -> None:
        if self._source is not None:
            self._source.close()
            self._source = None
