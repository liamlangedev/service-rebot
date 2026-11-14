#!/usr/bin/env bash
# Fetches the third-party pieces this project needs (kept out of git):
#   1. Seeed's official reBot Arm B601 description (MJCF + meshes) -> assets/reBot-DevArm
#   2. OculusReader, Quest 3 fork, plus its APK (stored in Git LFS) -> third_party/oculus_reader
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p assets third_party

# --- 1. reBot Arm description (sparse checkout, only the arm description) ---
if [ ! -d assets/reBot-DevArm ]; then
  echo ">> Fetching reBot Arm description from Seeed-Projects/reBot-DevArm"
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/Seeed-Projects/reBot-DevArm.git assets/reBot-DevArm
  git -C assets/reBot-DevArm sparse-checkout set Rebot_Arm_description
else
  echo ">> assets/reBot-DevArm already present (delete it to re-fetch)"
fi

# --- 2. OculusReader (Quest 3 fork) ---
if [ ! -d third_party/oculus_reader ]; then
  echo ">> Fetching OculusReader (jborbik fork, Quest 3 support)"
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 \
    https://github.com/jborbik/oculus_reader.git third_party/oculus_reader
else
  echo ">> third_party/oculus_reader already present"
fi

# The APK lives in Git LFS; download the real binary if we only have the pointer file.
APK=third_party/oculus_reader/oculus_reader/APK/teleop-debug.apk
if [ ! -s "$APK" ] || head -c 100 "$APK" | grep -q "git-lfs"; then
  echo ">> Downloading OculusReader APK"
  curl -fL -o "$APK" \
    https://media.githubusercontent.com/media/jborbik/oculus_reader/main/oculus_reader/APK/teleop-debug.apk
fi

echo ">> Done. Next: uv sync"
