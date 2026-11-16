#!/usr/bin/env bash
# Install the two Python dependencies the agent needs beyond ROS:
#   ultralytics  - local YOLOE detection (pulls torch, which is already here)
#   google-genai - the Gemini planner backend
#
# Installs with --user, so no sudo and nothing outside your home directory.
# Re-running is safe.
#
#   ./scripts/setup_agent.sh          install
#   ./scripts/setup_agent.sh --check  only report what is installed
set -euo pipefail

CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

python3 - <<'PY'
import sys
print(f"python {sys.version.split()[0]}  ({sys.executable})")
PY

check() {
  python3 - "$@" <<'PY'
import importlib, sys
missing = []
for name in sys.argv[1:]:
    try:
        mod = importlib.import_module(name)
        print(f"  ok      {name:14s} {getattr(mod, '__version__', '?')}")
    except Exception:
        missing.append(name)
        print(f"  missing {name}")
sys.exit(0 if not missing else 1)
PY
}

echo "checking python packages:"
if check cv2 numpy yaml torch ultralytics google.genai; then
  echo "everything is installed."
  exit 0
fi

if [[ "$CHECK" == "1" ]]; then
  echo "run without --check to install the missing ones."
  exit 1
fi

echo
echo "installing ultralytics + google-genai with --user (this may take a while)"
python3 -m pip install --user --upgrade ultralytics google-genai

echo
echo "verifying:"
check cv2 numpy yaml torch ultralytics google.genai || {
  echo "something is still missing; see the pip output above" >&2
  exit 1
}

cat <<'EOF'

done. next steps:
  Run the following from ros2_ws/ after sourcing ROS and install/setup.bash:
  1. Set perception.model to existing detector weights in the selected agent.yaml.
  2. Put GEMINI_API_KEY in ros2_ws/.env (or .env from ros2_ws/), with permissions 600.
  3. Set camera devices and enable front_camera in the selected cameras.yaml.
  4. Start arm bringup and camera_node in separate terminals before calibration.
  5. Record five marks once, then click them in both fixed views:
     ros2 run rebot_trash_sorting_agent calibrate_table --config-dir "$PWD/src/rebot_trash_sorting_agent/config" --from-arm --count 5 --joint-states-topic /rebotarm/joint_states
  Intrinsics fall back to configured horizontal FOV automatically.
  For the complete startup order and no-motion verification, follow:
     src/rebot_trash_sorting_agent/README.md
  provider:=mock is NOT a no-motion mode; use run.dry_run: true in agent.yaml.
EOF
