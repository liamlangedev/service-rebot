# steel_team ROS 2 Workspace (`rebot_trash_sorting`)

ROS 2 colcon workspace for the **Seeed Studio reBot Arm B601-DM** vision-guided trash sorting pipeline.

External Seeed repositories are kept out of git and fetched via [`scripts/setup_deps.sh`](scripts/setup_deps.sh), following the official [reBot Arm B601-DM ROS 2 Integration Wiki](https://wiki.seeedstudio.com/rebot_arm_b601_dm_ros2_integration/).

## 1. System Prerequisites (Ubuntu 24.04 + ROS 2 Jazzy / Ubuntu 22.04 + Humble)

If `conda` is active, deactivate it before building so ROS 2 uses system Python:

```bash
conda deactivate
```

Install system ROS 2 packages if not already present:

```bash
source /opt/ros/${ROS_DISTRO:-jazzy}/setup.bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions python3-pip python3-rosdep git \
  ros-${ROS_DISTRO}-control-msgs \
  ros-${ROS_DISTRO}-trajectory-msgs \
  ros-${ROS_DISTRO}-tf-transformations \
  ros-${ROS_DISTRO}-robot-state-publisher \
  ros-${ROS_DISTRO}-rviz2 \
  ros-${ROS_DISTRO}-pinocchio \
  ros-${ROS_DISTRO}-cv-bridge \
  ros-${ROS_DISTRO}-moveit \
  ros-${ROS_DISTRO}-ros2-control \
  ros-${ROS_DISTRO}-ros2-controllers \
  ros-${ROS_DISTRO}-xacro
```

## 2. Fetch External Dependencies & Build

```bash
cd ros2_ws
./scripts/setup_deps.sh            # clones reBotArmController_ROS2, reBotArm_control_py, reBot-DevArm + motorbridge
# Optional: ./scripts/setup_deps.sh --rosdep

source /opt/ros/${ROS_DISTRO:-jazzy}/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## 3. Verify & Launch

```bash
# Check rebot_trash_sorting + OpenCV/cv_bridge + rebotarm_msgs linkage
ros2 run rebot_trash_sorting check_env

# Default: fake hardware + MoveIt 2 + RViz (MotionPlanning panel + interactive target ball)
ros2 launch rebot_trash_sorting bringup.launch.py

# Real B601-DM hardware + MoveIt 2 + RViz
ros2 launch rebot_trash_sorting bringup.launch.py use_fake_hardware:=false channel:=/dev/ttyACM0
# (In another terminal, enable the motors before clicking Execute in RViz:
#  ros2 service call /rebotarm/enable std_srvs/srv/Trigger)
```
