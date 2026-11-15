#!/usr/bin/env python3
"""Upload a local LeRobot dataset to the Hugging Face Hub (private by default).

  python push_dataset.py RoboCrafty/rebot_sort_v1
  python push_dataset.py RoboCrafty/rebot_sort_v1 --public

Run it again after `record_episodes.py --resume` to upload the new episodes.
Needs `hf auth login` once.
"""
import argparse

from huggingface_hub import HfApi

from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.utils.constants import HF_LEROBOT_HOME

p = argparse.ArgumentParser()
p.add_argument("repo_id")
p.add_argument("--public", action="store_true")
args = p.parse_args()

private = not args.public
HfApi().create_repo(args.repo_id, repo_type="dataset", private=private, exist_ok=True)
# explicit root: otherwise LeRobot treats the dataset as a Hub download and looks it up remotely first
dataset = LeRobotDataset(args.repo_id, root=HF_LEROBOT_HOME / args.repo_id)
print(f"pushing {dataset.meta.total_episodes} episodes ({dataset.meta.total_frames} frames)")
dataset.push_to_hub(private=private)
