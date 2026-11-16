#!/usr/bin/env bash
# Fine-tune lerobot/smolvla_base on a clipped grasp dataset (make_dataset.py), on HF Jobs.
#
#   OBJECT=towel VARIANT=rel EVAL_SPLIT=<...> ./training_gripper/train_smolvla.sh   # gripper camera only
#   OBJECT=towel VARIANT=abs EVAL_SPLIT=<...> ./training_gripper/train_smolvla.sh   # 3 cameras
#
# Cameras are renamed to smolvla_base's camera1/2/3, in the same slots as
# training/smolvla/train.sh (front_wide -> camera1, gripper -> camera2, high_oblique ->
# camera3). The rel datasets have only the gripper camera; SmolVLA skips image keys missing
# from the batch. 8 workers, as in train.sh: the eval DataLoader spawns its own.
# With --policy.path, lerobot ignores --policy.repo_id on remote runs: the model lands in
# <user>/smolvla_rebot_grasp_<object>_<variant>_<date>_<time>. Check its visibility after
# the push (training/RUNS.md: an earlier SmolVLA repo was made public at the final push).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LEROBOT_TRAIN="${LEROBOT_TRAIN:-$REPO_ROOT/teleoperation/.venv/bin/lerobot-train}"
HF_USER="${HF_USER:-niru-5}"
TARGET="${TARGET:-rtx-pro-6000}"
VARIANT="${VARIANT:?set VARIANT=abs or VARIANT=rel}"
OBJECT="${OBJECT:-keys}"
EVAL_SPLIT="${EVAL_SPLIT:?set EVAL_SPLIT from meta/grasp_clips.json}"
NAME="smolvla_rebot_grasp_${OBJECT}_${VARIANT}"

exec "$LEROBOT_TRAIN" \
  --dataset.repo_id="$HF_USER/rebot_grasp_${OBJECT}_${VARIANT}" \
  --dataset.image_transforms.enable=true \
  --dataset.video_backend=torchcodec \
  --dataset.eval_split="$EVAL_SPLIT" \
  --eval_steps=500 \
  --policy.path=lerobot/smolvla_base \
  --policy.repo_id="$HF_USER/$NAME" \
  --policy.private=true \
  --rename_map='{"observation.images.front_wide": "observation.images.camera1", "observation.images.gripper": "observation.images.camera2", "observation.images.high_oblique": "observation.images.camera3"}' \
  --batch_size=64 \
  --num_workers=8 \
  --steps=5000 \
  --save_freq=1000 \
  --policy.scheduler_warmup_steps=300 \
  --policy.scheduler_decay_steps=5000 \
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
