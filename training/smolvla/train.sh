#!/usr/bin/env bash
# Fine-tune lerobot/smolvla_base on RoboCrafty/rebot_sort_v1 on HF Jobs.
#
#   ./training/smolvla/train.sh                 # submit to HF Jobs (rtx-pro-6000) and detach
#   TARGET=local ./training/smolvla/train.sh    # run on this machine instead
#   ./training/smolvla/train.sh --steps=1000    # extra args are appended (override anything)
#
# smolvla_base was pretrained with cameras named camera1/2/3, so ours are renamed to match.
# Our 7-DoF state/action is zero-padded to max_state_dim/max_action_dim (32) by the policy.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LEROBOT_TRAIN="${LEROBOT_TRAIN:-$REPO_ROOT/teleoperation/.venv/bin/lerobot-train}"
HF_USER="${HF_USER:-niru-5}"
TARGET="${TARGET:-rtx-pro-6000}"

exec "$LEROBOT_TRAIN" \
  --dataset.repo_id=RoboCrafty/rebot_sort_v1 \
  --dataset.image_transforms.enable=true \
  --dataset.video_backend=torchcodec \
  --policy.path=lerobot/smolvla_base \
  --policy.repo_id="$HF_USER/smolvla_rebot_sort_v1" \
  --rename_map='{"observation.images.front_wide": "observation.images.camera1", "observation.images.gripper": "observation.images.camera2", "observation.images.high_oblique": "observation.images.camera3"}' \
  --batch_size=128 \
  --num_workers=16 \
  --steps=10000 \
  --save_freq=2500 \
  --policy.scheduler_warmup_steps=500 \
  --policy.scheduler_decay_steps=15000 \
  --save_checkpoint_to_hub=true \
  --log_freq=100 \
  --job_name=smolvla_rebot_sort_v1 \
  --job.target="$TARGET" \
  --trackio.enable=true \
  --trackio.space_id="${TRACKIO_SPACE:-$HF_USER/rebot-training}" \
  --trackio.private=true \
  --job.timeout=24h \
  --job.detach=true \
  "$@"
