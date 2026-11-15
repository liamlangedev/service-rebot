"""Robot, cameras and kinematics for the rollouts.

The arm is driven through lerobot's reBot B601 follower, set up like
teleoperation/go_ready.py: pos_vel control (the motors cap joint speed), a per-command
step limit (`max_relative_target`), the measured gripper range, never re-zeroing, and
torque left on at exit so the arm does not drop.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "teleoperation"))
sys.path.insert(0, str(REPO / "ros2_ws" / "src" / "rebot_trash_sorting_agent"))

JOINTS = ["shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_yaw",
          "wrist_roll", "gripper"]
READY_DEG = np.degrees([0.0, -1.51, -1.30, 1.36, 0.0, 0.0])


def to_action(cmd7: np.ndarray) -> dict[str, float]:
    return {f"{n}.pos": float(v) for n, v in zip(JOINTS, cmd7)}


def state_of(obs: dict) -> np.ndarray:
    return np.array([obs[f"{n}.pos"] for n in JOINTS], dtype=np.float64)


def connect_robot(args, cameras: dict[str, str]):
    """Real follower (or the MuJoCo stand-in with --fake-hardware). Returns (robot, gripper limits)."""
    from lerobot.robots.rebot_b601_follower import RebotB601Follower, RebotB601FollowerRobotConfig
    from lerobot.robots.rebot_b601_follower.motor_family import ArmControlMode

    from teleop import gripper_limits

    limits = gripper_limits.load()
    if limits is None:
        sys.exit("gripper range not measured: run teleoperation/tools/measure_gripper.py first")
    lo, hi = gripper_limits.bounds(limits)
    calib = Path(args.calibration_dir) / f"{args.robot_id}.json"
    if not args.fake_hardware and not calib.exists():
        sys.exit(f"calibration {calib} not found; not connecting (lerobot would re-zero the motors)")

    cam_cfgs = {}
    if not args.fake_hardware:
        from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
        for name, dev in cameras.items():
            index = int(dev) if dev.isdigit() else Path(dev)
            cam_cfgs[name] = OpenCVCameraConfig(index_or_path=index, fps=30, width=640, height=480)

    config = RebotB601FollowerRobotConfig(
        port=args.port, id=args.robot_id, calibration_dir=Path(args.calibration_dir),
        joint_limits={"gripper": (lo, hi)}, max_relative_target=args.max_step_deg,
        control_mode=ArmControlMode.POS_VEL, pos_vel_velocity=args.motor_vel_deg,
        cameras=cam_cfgs, disable_torque_on_disconnect=False)
    if args.fake_hardware:
        from teleop.fake_rebot import FakeRebotFollower
        robot = FakeRebotFollower(config, limits)
        print("FAKE HARDWARE: MuJoCo stand-in, nothing physical moves")
    else:
        robot = RebotB601Follower(config)
    robot.connect(calibrate=False)
    return robot, limits


def set_torque(robot, on: bool) -> None:
    """Torque off lets the arm be moved by hand; on re-arms it (holding where it is)."""
    if not hasattr(robot, "disable_torque"):
        print("(fake hardware: torque toggle ignored)")
        return
    if on:
        robot.configure()
    else:
        robot.disable_torque()


class Fk:
    """TCP position [m] of the MuJoCo `tcp` site for lerobot joint degrees."""

    def __init__(self):
        from teleop.rebot_model import RebotSim
        self.sim = RebotSim(scene="real")

    def __call__(self, q_deg) -> tuple[float, float, float]:
        import mujoco
        self.sim.data.qpos[self.sim.arm_qadr] = np.radians(np.asarray(q_deg)[:6])
        mujoco.mj_forward(self.sim.model, self.sim.data)
        p = self.sim.tcp_pose()[0]
        return float(p[0]), float(p[1]), float(p[2])


class FakeCameras:
    """Dry-run camera source: replays one recorded episode's frames in real time."""

    def __init__(self, repo_id: str, root: str | None, episode: int, start_frame: int,
                 names: list[str]):
        from lerobot.datasets.lerobot_dataset import LeRobotDataset
        self.ds = LeRobotDataset(repo_id, root=root, episodes=[episode], video_backend="pyav",
                                 return_uint8=True)
        self.names = names
        self.start = start_frame
        self.t0 = time.monotonic()

    def read(self) -> dict[str, np.ndarray]:
        i = min(self.start + int((time.monotonic() - self.t0) * 30), len(self.ds) - 1)
        item = self.ds[i]
        return {n: item[f"observation.images.{n}"].permute(1, 2, 0).numpy() for n in self.names}
