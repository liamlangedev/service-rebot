"""Records teleop episodes as a LeRobot dataset (LeRobotDataset v3 format).

The layout matches what `lerobot-record` produces with the real arm
(robot.type=rebot_b601_follower), so sim and real episodes are interchangeable:

  observation.state               [7] measured shoulder_pan.pos .. gripper.pos (deg)
  action                          [7] commanded shoulder_pan.pos .. gripper.pos (deg)
  observation.images.<camera>     HxWx3 video, one per camera
  task                            language instruction for the episode

See teleop/lerobot_mapping.py for the joint/gripper conversion.
"""
from pathlib import Path

import mujoco
import numpy as np

from teleop.lerobot_mapping import FEATURE_NAMES, ROBOT_TYPE, sim_to_lerobot


class LeRobotRecorder:
    def __init__(self, model: mujoco.MjModel, repo_id: str, root: Path, fps: int,
                 task: str, cameras: list[str], height: int = 480, width: int = 640):
        from lerobot.datasets.lerobot_dataset import LeRobotDataset

        self.task = task
        self.cameras = cameras
        self.renderer = mujoco.Renderer(model, height, width)
        features = {
            "observation.state": {"dtype": "float32", "shape": (len(FEATURE_NAMES),),
                                  "names": FEATURE_NAMES},
            "action": {"dtype": "float32", "shape": (len(FEATURE_NAMES),),
                       "names": FEATURE_NAMES},
        }
        for cam in cameras:
            features[f"observation.images.{cam}"] = {
                "dtype": "video", "shape": (height, width, 3),
                "names": ["height", "width", "channels"]}

        root = Path(root)
        if root.exists():
            raise FileExistsError(
                f"{root} already exists; pick a new --dataset-root or delete it.")
        self.dataset = LeRobotDataset.create(
            repo_id=repo_id, fps=fps, root=root, robot_type=ROBOT_TYPE,
            features=features, use_videos=True, image_writer_threads=4)
        self.recording = False
        self.n_frames = 0
        self.n_episodes = 0

    def start(self):
        self.recording = True
        self.n_frames = 0
        print(f"[record] episode {self.n_episodes} started")

    def add_frame(self, data: mujoco.MjData, q_meas, gripper_meas, q_cmd, gripper_cmd):
        frame = {
            "observation.state": sim_to_lerobot(q_meas, gripper_meas).astype(np.float32),
            "action": sim_to_lerobot(q_cmd, gripper_cmd).astype(np.float32),
            "task": self.task,
        }
        for cam in self.cameras:
            self.renderer.update_scene(data, cam)
            frame[f"observation.images.{cam}"] = self.renderer.render().copy()
        self.dataset.add_frame(frame)
        self.n_frames += 1

    def save(self):
        self.recording = False
        if self.n_frames == 0:
            print("[record] empty episode, nothing saved")
            return
        self.dataset.save_episode()
        print(f"[record] saved episode {self.n_episodes} ({self.n_frames} frames)")
        self.n_episodes += 1

    def discard(self):
        self.recording = False
        self.dataset.clear_episode_buffer()
        print(f"[record] discarded episode ({self.n_frames} frames)")

    def close(self):
        if self.recording:
            self.save()
        self.dataset.finalize()
        self.renderer.close()
        print(f"[record] dataset at {self.dataset.root} "
              f"({self.n_episodes} episodes)")
