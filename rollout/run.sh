#!/usr/bin/env bash
# Rollout launcher with this cell's cameras and the guide's first-run settings.
#
#   rollout/run.sh cameras                 # grab one frame per camera -> rollout/logs/cameras.jpg
#   rollout/run.sh full                    # full-task ACT, first run (slow, 20 s)
#   rollout/run.sh grasp-rel-approach      # grasp-rel, floor above the table: approach only
#   rollout/run.sh grasp-rel               # grasp-rel, real grasp
#   rollout/run.sh grasp-abs               # grasp-abs (held-out clip 27; add --device cuda)
#   rollout/run.sh dry-run                 # grasp-rel on the MuJoCo stand-in, no arm
#
# Anything after the mode is passed on to rollout.py and overrides the defaults below,
# e.g. `rollout/run.sh full --max-speed 45 --timeout 40` or `... --policy <repo>`.
# Camera devices can be overridden with FRONT=, WRIST=, HIGH= in the environment.
# Runs from any directory; works the same when called from zsh.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY="${PY:-$ROOT/teleoperation/.venv/bin/python}"

FRONT="${FRONT:-/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._KD-USB_Cameras_KD-USB_Cameras-video-index0}"
WRIST="${WRIST:-/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB2.0_CAM1_USB2.0_CAM1-video-index0}"
HIGH="${HIGH:-/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_2ED4DF6F-video-index0}"

ALL_CAMS=(--cam "front_wide=$FRONT" --cam "gripper=$WRIST" --cam "high_oblique=$HIGH")
WRIST_CAM=(--cam "gripper=$WRIST")

mode="${1:-}"
[[ -n "$mode" ]] && shift
case "$mode" in
  cameras)
    exec "$PY" rollout/check_cameras.py "${ALL_CAMS[@]}" "$@" ;;
  full)
    exec "$PY" rollout/rollout.py full "${ALL_CAMS[@]}" --max-speed 25 --timeout 20 "$@" ;;
  grasp-rel-approach)
    exec "$PY" rollout/rollout.py grasp-rel "${WRIST_CAM[@]}" \
      --max-speed 20 --max-offset 15 --min-tcp-z 0.13 "$@" ;;
  grasp-rel)
    exec "$PY" rollout/rollout.py grasp-rel "${WRIST_CAM[@]}" --max-speed 30 --max-offset 20 "$@" ;;
  grasp-abs)
    exec "$PY" rollout/rollout.py grasp-abs "${ALL_CAMS[@]}" --start-episode 27 "$@" ;;
  dry-run)
    src="${DATASET_ROOT:-$HOME/.cache/rebot_sort_v1}"
    if [[ ! -f "$src/meta/info.json" ]]; then
      echo "downloading RoboCrafty/rebot_sort_v1 to $src (about 900 MB, once)"
      "$ROOT/teleoperation/.venv/bin/hf" download RoboCrafty/rebot_sort_v1 --repo-type dataset --local-dir "$src"
    fi
    exec "$PY" rollout/rollout.py grasp-rel --fake-hardware --auto-start --arrive-tol-deg 15 \
      --max-lag-deg 40 --fake-images-root "$src" --fake-episode 32 --fake-start-frame 72 "$@" ;;
  *)
    sed -n '2,13p' "${BASH_SOURCE[0]}"
    exit 2 ;;
esac
