"""Real reBot B601-DM backend through LeRobot's `rebot_b601_follower` driver.

The teleop loop keeps producing the same thing as in simulation (6 joint
targets + finger opening); this converts them to LeRobot's degree actions and
reads the measured pose back so the MuJoCo scene mirrors the real arm.

Needs `uv sync --extra lerobot` (includes lerobot[rebot] / motorbridge).
UNTESTED ON HARDWARE so far: start slow (see README "Real arm").
"""
from pathlib import Path

import numpy as np

from teleop.lerobot_mapping import lerobot_to_sim, sim_to_lerobot, to_action_dict


class RealRebot:
    def __init__(self, port: str, robot_id: str = "follower",
                 calibration_dir: str | Path | None = None, max_step_deg: float = 5.0):
        from lerobot.robots.rebot_b601_follower import (
            RebotB601Follower, RebotB601FollowerRobotConfig)

        # calibration_dir/<robot_id>.json, e.g. the team's steel_team/follower.json
        config = RebotB601FollowerRobotConfig(
            port=port, id=robot_id, motor_family="dm",
            calibration_dir=Path(calibration_dir) if calibration_dir else None,
            max_relative_target=max_step_deg)
        self.robot = RebotB601Follower(config)
        self.robot.connect(calibrate=False)

    def read(self) -> tuple[np.ndarray, float]:
        """Measured (q_arm rad, finger m) in the simulator's convention."""
        return lerobot_to_sim(self.robot.get_observation())

    def send(self, q_arm: np.ndarray, finger_m: float):
        self.robot.send_action(to_action_dict(sim_to_lerobot(q_arm, finger_m)))

    def close(self):
        # LeRobot disables torque on disconnect: support the arm first.
        self.robot.disconnect()
