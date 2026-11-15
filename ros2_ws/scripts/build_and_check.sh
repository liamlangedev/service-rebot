#!/usr/bin/env bash
# Builds the ROS 2 workspace and runs the environment sanity check.
set -euo pipefail

WS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WS_ROOT"

ROS_SETUP="/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash"
if [ ! -f "$ROS_SETUP" ]; then
  echo "ERROR: ROS 2 setup script not found at $ROS_SETUP" >&2
  exit 1
fi

set +u
# shellcheck disable=SC1090
source "$ROS_SETUP"
set -u

colcon build --symlink-install

set +u
# shellcheck disable=SC1091
source "$WS_ROOT/install/setup.bash"
set -u

ros2 run rebot_trash_sorting check_env
