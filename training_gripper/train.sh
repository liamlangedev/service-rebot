#!/usr/bin/env bash
# Small ACT on the clipped grasp datasets (see make_dataset.py), on HF Jobs.
#
#   VARIANT=rel ./training_gripper/train.sh     # relative actions, gripper camera only
#   VARIANT=abs ./training_gripper/train.sh     # absolute actions, 3 cameras
#   TARGET=local VARIANT=rel ./training_gripper/train.sh --steps=50   # local smoke test
#
# 8 workers: the eval DataLoader spawns its own workers at each eval, and 16+16 hit the
# process limit on rtx-pro-6000 (crash at step 500, "CPU dispatcher tracer already initlized").
#
# EVAL_SPLIT must match the held-out clips written by make_dataset.py
# (meta/grasp_clips.json -> eval_split.<variant>).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEROBOT_TRAIN="${LEROBOT_TRAIN:-$REPO_ROOT/teleoperation/.venv/bin/lerobot-train}"
HF_USER="${HF_USER:-niru-5}"
TARGET="${TARGET:-rtx-pro-6000}"
VARIANT="${VARIANT:?set VARIANT=abs or VARIANT=rel}"
EVAL_SPLIT="${EVAL_SPLIT:?set EVAL_SPLIT from meta/grasp_clips.json}"
NAME="act_rebot_grasp_keys_${VARIANT}"

exec "$LEROBOT_TRAIN" \
  --dataset.repo_id="$HF_USER/rebot_grasp_keys_${VARIANT}" \
  --dataset.image_transforms.enable=true \
  --dataset.video_backend=torchcodec \
  --dataset.eval_split="$EVAL_SPLIT" \
  --eval_steps=500 \
  --policy.type=act \
  --policy.repo_id="$HF_USER/$NAME" \
  --policy.private=true \
  --policy.chunk_size=30 \
  --policy.n_action_steps=30 \
  --policy.optimizer_lr=3e-5 \
  --policy.optimizer_lr_backbone=3e-5 \
  --batch_size=64 \
  --num_workers=8 \
  --steps=5000 \
  --save_freq=1000 \
  --save_checkpoint_to_hub=true \
  --log_freq=100 \
  --job_name="$NAME" \
  --job.target="$TARGET" \
  --trackio.enable=true \
  --trackio.space_id="${TRACKIO_SPACE:-$HF_USER/rebot-training}" \
  --trackio.private=true \
  --job.timeout=4h \
  --job.detach=true \
  "$@"
