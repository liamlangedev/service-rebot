#!/usr/bin/env bash
# Sets up external dependencies for the steel_team ROS 2 workspace (kept out of git):
#   1. Seeed-Projects/reBotArmController_ROS2 -> src/reBotArmController_ROS2
#   2. Seeed-Projects/reBotArm_control_py     -> third_party/reBotArm_control_py
#   3. Seeed-Projects/reBot-DevArm (sparse)   -> third_party/reBot-DevArm
#   4. motorbridge Python package (for B601-DM USB2CAN hardware)
#   5. Optional: rosdep install (--rosdep)
set -euo pipefail

WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WS_ROOT"

RUN_ROSDEP=0
for arg in "$@"; do
  case "$arg" in
    --rosdep) RUN_ROSDEP=1 ;;
    -h|--help)
      echo "Usage: $0 [--rosdep]"
      echo "  --rosdep   Also run 'rosdep install --from-paths src --ignore-src -r -y'"
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 1
      ;;
  esac
done

mkdir -p src third_party
touch third_party/COLCON_IGNORE

# --- 1. Seeed reBotArmController_ROS2 ---
if [ ! -d src/reBotArmController_ROS2 ]; then
  echo ">> Cloning Seeed-Projects/reBotArmController_ROS2 -> src/reBotArmController_ROS2"
  git clone --depth 1 \
    https://github.com/Seeed-Projects/reBotArmController_ROS2.git \
    src/reBotArmController_ROS2
else
  echo ">> src/reBotArmController_ROS2 already present"
fi

# --- 2. Low-level Python SDK (reBotArm_control_py) ---
# rebotarmcontroller walks parent directories looking for third_party/reBotArm_control_py.
if [ ! -d third_party/reBotArm_control_py ]; then
  echo ">> Cloning Seeed-Projects/reBotArm_control_py -> third_party/reBotArm_control_py"
  git clone --depth 1 \
    https://github.com/Seeed-Projects/reBotArm_control_py.git \
    third_party/reBotArm_control_py
else
  echo ">> third_party/reBotArm_control_py already present"
fi

if [ ! -e src/reBotArmController_ROS2/third_party ]; then
  ln -s ../../third_party src/reBotArmController_ROS2/third_party
fi

# --- 3. Official reBot-DevArm description + Soft Gripper CAD ---
if [ ! -d third_party/reBot-DevArm ]; then
  echo ">> Cloning Seeed-Projects/reBot-DevArm (sparse) -> third_party/reBot-DevArm"
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/Seeed-Projects/reBot-DevArm.git \
    third_party/reBot-DevArm
else
  echo ">> third_party/reBot-DevArm already present"
fi
git -C third_party/reBot-DevArm sparse-checkout set --no-cone \
  '/Rebot_Arm_description/' \
  '/hardware/reBot_B601_DM/3D_Printed_Parts/Soft_Gripper/' \
  '/hardware/reBot_B601_DM/3D_Printed_Parts/01_Finger.step' \
  '/hardware/reBot_B601_DM/3D_Printed_Parts/images/Soft_Finger.png'

# --- 4. motorbridge Python dependency ---
if python3 -c "import motorbridge" >/dev/null 2>&1; then
  echo ">> motorbridge already installed"
else
  echo ">> Installing motorbridge from PyPI"
  python3 -m pip install --user --break-system-packages \
    --index-url https://pypi.org/simple motorbridge
fi

# --- 5. Optional rosdep ---
if [ "$RUN_ROSDEP" -eq 1 ]; then
  if command -v rosdep >/dev/null 2>&1; then
    echo ">> Installing system ROS dependencies via rosdep"
    rosdep install --from-paths src --ignore-src -r -y
  else
    echo "WARN: rosdep not found; install python3-rosdep or apt packages from README.md" >&2
  fi
fi

echo ">> Dependencies ready. Build with:"
echo "   source /opt/ros/\${ROS_DISTRO:-jazzy}/setup.bash"
echo "   colcon build --symlink-install"
echo "   source install/setup.bash"
