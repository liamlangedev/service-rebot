"""Offline check of the ROS node's PolicyRunner on dataset frames (no ROS, no robot).

    teleoperation/.venv/bin/python training_gripper/smoke_runner.py \
        --policy niru-5/act_rebot_sort_v1 --mode absolute --dataset <local rebot_sort_v1 root> \
        [--episode 32] [--start-before-close 60]

Starts the runner at a frame before the close (the handoff), feeds it the recorded frames
open-loop, and prints its first actions next to the recorded ones. Large disagreement at
the handoff frame means a unit, camera or mode mismatch, not a bad policy.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "ros2_ws" / "src" / "rebot_trash_sorting_agent"))

from rebot_trash_sorting_agent.grasp_policy.runner import PolicyRunner, RunnerConfig  # noqa: E402
from segments import find_grasp  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--policy", required=True)
    p.add_argument("--mode", default="absolute")
    p.add_argument("--dataset", required=True)
    p.add_argument("--episode", type=int, default=32)
    p.add_argument("--start-before-close", type=int, default=60)
    p.add_argument("--n-steps", type=int, default=10)
    a = p.parse_args()

    from lerobot.datasets.lerobot_dataset import LeRobotDataset

    ds = LeRobotDataset("RoboCrafty/rebot_sort_v1", root=a.dataset, video_backend="pyav",
                        return_uint8=True, episodes=[a.episode])
    states = np.stack([ds.hf_dataset[i]["observation.state"].numpy() for i in range(len(ds))])
    actions = np.stack([ds.hf_dataset[i]["action"].numpy() for i in range(len(ds))])
    g = find_grasp(a.episode, actions)
    t0 = g.t_close - a.start_before_close

    runner = PolicyRunner(RunnerConfig(policy_path=a.policy, mode=a.mode, n_steps=a.n_steps))
    print("policy cameras:", runner.camera_names, "chunk", runner.chunk_size)
    runner.start(states[t0])
    errs = []
    for t in range(t0, min(g.t_close + 40, len(ds)), runner.n_steps):
        item = ds[t]
        imgs = {c: item[f"observation.images.{c}"].permute(1, 2, 0).numpy()
                for c in runner.camera_names}
        tic = time.perf_counter()
        pred, clipped = runner.predict(states[t], imgs)
        ms = (time.perf_counter() - tic) * 1000
        rec = actions[t:t + len(pred)]
        err = np.abs(pred[: len(rec)] - rec).mean(0)
        errs.append(err)
        print(f"t={t - g.t_close:+4d} {ms:6.0f} ms  |pred-rec| arm "
              f"{np.round(err[:6], 1)} grip {err[6]:.0f}  pred grip {pred[-1, 6]:.0f} "
              f"rec grip {rec[-1, 6]:.0f}{' CLIPPED' if clipped else ''}")
    print("mean abs error per joint:", np.round(np.mean(errs, 0), 1))


if __name__ == "__main__":
    main()
