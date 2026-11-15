#!/usr/bin/env bash
# Baseline ACT on RoboCrafty/rebot_sort_v1, trained from scratch on HF Jobs.
#
#   ./training/act/train.sh                     # submit to HF Jobs (a100-large) and detach
#   TARGET=local ./training/act/train.sh        # run on this machine instead
#   ./training/act/train.sh --steps=1000        # extra args are appended (override anything)
#
# Monitor with `hf jobs ps` / `hf jobs logs <id>`.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LEROBOT_TRAIN="${LEROBOT_TRAIN:-$REPO_ROOT/teleoperation/.venv/bin/lerobot-train}"
HF_USER="${HF_USER:-niru-5}"
TARGET="${TARGET:-a100-large}"

exec "$LEROBOT_TRAIN" \
  --dataset.repo_id=RoboCrafty/rebot_sort_v1 \
  --dataset.image_transforms.enable=true \
  --dataset.video_backend=torchcodec \
  --policy.type=act \
  --policy.repo_id="$HF_USER/act_rebot_sort_v1" \
  --policy.chunk_size=100 \
  --policy.n_action_steps=100 \
  --batch_size=32 \
  --num_workers=10 \
  --steps=40000 \
  --save_freq=5000 \
  --save_checkpoint_to_hub=true \
  --log_freq=200 \
  --job_name=act_rebot_sort_v1 \
  --job.target="$TARGET" \
  --trackio.enable=true \
  --trackio.space_id="${TRACKIO_SPACE:-$HF_USER/rebot-training}" \
  --trackio.private=true \
  --job.timeout=24h \
  --job.detach=true \
  "$@"
