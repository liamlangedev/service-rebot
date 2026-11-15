# rebot_trash_sorting_agent

VLM-orchestrated pick-and-place agent for the Seeed reBot Arm B601-DM (`classic_real`).

## Environment

Build the workspace first; see the [workspace setup](../../README.md). All commands
below run from `ros2_ws/`, not the repository root. In **each terminal**, source the
environment and select the same source config directory:

```bash
source /opt/ros/${ROS_DISTRO:-jazzy}/setup.bash
source install/setup.bash
export AGENT_CONFIG="$PWD/src/rebot_trash_sorting_agent/config"
```

Check the optional detector/planner Python dependencies with:

```bash
bash src/rebot_trash_sorting_agent/scripts/setup_agent.sh --check
```

Set the detector weights path in `agent.yaml` (`perception.model`); the dependency
check does not download or validate weights. For Gemini, put `GEMINI_API_KEY=...`
in `ros2_ws/.env` (gitignored). No key is needed with `provider:=mock`, but the mock
planner can still call motion tools: it is not a no-motion mode.

## Configure the Cameras

Edit [config/cameras.yaml](config/cameras.yaml). Use stable `/dev/v4l/by-id/...`
device paths for `table`, `front_camera`, and `wrist`. The front-camera device is
a placeholder and `enabled` defaults to `false`; set the correct device and
`enabled: true` before capture or calibration. Disable any absent cameras.

Keep mounts, focus/zoom, and capture resolution fixed after calibration. The
front camera should see object bases and tops from an oblique or side view, not
straight down. Its configured **horizontal** `fov_deg` is used to approximate
intrinsics automatically when `camera_matrix` is null. A supplied calibrated
`camera_matrix` (3x3 K, nine row-major values) always takes precedence; provide
matching OpenCV `distortion` coefficients if available. No extra flag is needed.
The legacy `--allow-approximate-intrinsics` flag is still accepted.

## Calibrate Both Fixed Views

### 1. Start the Arm and Cameras

For arm-based point recording, start real arm bringup in terminal 1. This starts
the driver, gripper bridge, and MoveIt, but **not** the cameras or agent:

```bash
ros2 launch rebot_trash_sorting bringup.launch.py \
   use_fake_hardware:=false channel:=/dev/ttyACM0 use_rviz:=false
```

In terminal 2, start only the configured camera streams:

```bash
ros2 run rebot_trash_sorting_agent camera_node --config-dir "$AGENT_CONFIG"
```

Leave both running. In terminal 3, check that joint states and both image topics
are publishing before calibration:

```bash
ros2 topic list
ros2 topic hz /rebotarm/joint_states
```

Stop the `hz` command with Ctrl+C when readings appear. The default fixed image
topics are `/table_cam/image_raw` and `/front_camera/image_raw`.

### 2. Record Once, Click Twice

Place five marks spread over the reachable table area, visible in both cameras.
Use the **closed** gripper tip to record each mark once. If disabling the motors
for hand positioning, **support the arm before disabling: it can fall under
gravity**. Do not send agent tasks while calibrating.

```bash
# Optional, only while physically supporting the arm
ros2 service call /rebotarm/disable std_srvs/srv/Trigger "{}"

ros2 run rebot_trash_sorting_agent calibrate_table \
   --config-dir "$AGENT_CONFIG" \
   --from-arm --count 5 --joint-states-topic /rebotarm/joint_states
```

Follow the prompts: touch marks 1-5, move the arm out of both views, click marks
1-5 in the table image, then click the **same marks in the same order** in the
front image. Press Enter after each complete click set. `--count` controls the
number of recorded marks with `--from-arm`; five is the default. Adjust
`places.yaml` table Z to match the physical setup before calibrating.

Alternatively, supply measured `base_link` X/Y coordinates in metres. This does
not need a running arm, only the camera node:

```bash
ros2 run rebot_trash_sorting_agent calibrate_table \
   --config-dir "$AGENT_CONFIG" \
   --points "0.16,-0.15;0.30,-0.15;0.16,0.15;0.30,0.15;0.23,0.00"
```

These are example coordinates, not measurements of your marks. For table-only
calibration add `--camera table`; this does not calibrate front-camera height.
For headless operation add `--pixels "u1,v1;..."` and
`--front-pixels "u1,v1;..."` in the same order. Without images, the script uses
the resolutions in `cameras.yaml`. Optional `--image` and `--front-image` use
saved images instead of live capture, at the intended runtime resolution.

### 3. Check What Was Saved

With `--config-dir "$AGENT_CONFIG"`, both table homographies and the front-camera
height pose are written to `$AGENT_CONFIG/calibration.yaml`, preserving other
camera entries. Runtime must use that same config directory. Without
`--config-dir`, calibration tries to update source config when found and the
installed config directory. Existing non-null inline `table_map` entries in
`cameras.yaml` take precedence over this file; keep the real fixed-camera entries
null when using the calibration script.

Calibration rejects excessive table error (default mean 10 mm) or front pose
error (default maximum 5 pixels). `--force` bypasses these error thresholds, not
geometry checks. A small error on the table does **not** prove that height above
the table is accurate: validate several known object heights, particularly when
using FOV-derived intrinsics. Recalibrate after moving a camera or changing its
focus/zoom or resolution.

## Run the Real Pipeline

For the first check, set `run.dry_run: true` in
[config/agent.yaml](config/agent.yaml). The current `dry_run:=true` launch override
does not persist into the run configuration, so do not rely on that flag alone.
Dry-run skips skill motion execution; it is not a hardware interlock.

If terminal 1's arm bringup is still running, leave it running. Stop **only** the
standalone camera node in terminal 2 to release the devices, then start the agent
stack there. It restarts the cameras and loads the new calibration, without
starting another driver or MoveIt instance:

```bash
ros2 launch rebot_trash_sorting_agent agent.launch.py \
   config_dir:="$AGENT_CONFIG" \
   joint_states_topic:=/rebotarm/joint_states use_mujoco:=false
```

Open **http://127.0.0.1:8090/** for the table/wrist streams, task box, and STOP
button. There is currently no front-camera dashboard stream; the image is
published on `/front_camera/image_raw` and consumed for height estimation.

Check the reported dry-run state, then submit a task from another sourced terminal:

```bash
ros2 topic echo /agent/status --once
ros2 topic pub --once /agent/task std_msgs/msg/String '{data: "Put the can in the bin"}'
```

After `list_objects`, status objects include `height_m` in metres above the table.
The tool's `height_estimation` result reports how many heights were obtained or
why fallback was used. The estimate assumes an upright object and approximates
its top with a circular footprint. Occlusion, overhangs, unusual shapes, and
uncertain X/Y can produce inaccurate heights. Missing or ambiguous detections,
resolution mismatch, or unavailable height calibration use the configured
`grasp.pinch_heights_m` fallback; `height_m` is then null for that observation.
Measured heights instead use `grasp.height_fractions` (currently 60%, then 40%)
for candidate pinch heights, adjusted by the configured TCP-to-pinch offset.

Once observations and planned poses are checked, stop the agent stack, set
`run.dry_run: false`, and restart it. Re-enable the supported arm before requesting
motion if you disabled its motors during calibration:

```bash
ros2 service call /rebotarm/enable std_srvs/srv/Trigger "{}"
```

For subsequent starts, when **no** separate arm, camera, or agent processes are
running, the equivalent all-in-one command is:

```bash
ros2 launch rebot_trash_sorting_agent sorting.launch.py \
   config_dir:="$AGENT_CONFIG" use_fake_hardware:=false channel:=/dev/ttyACM0
```

The combined real-hardware launch also starts the MuJoCo mirror and therefore
needs its simulation dependencies. It is not a second arm controller. For a
ROS-only run without that mirror, use the split bringup/agent commands above.
Never run combined and split bringup together. Use `arm_namespace` on bringup and
the matching joint-state topic on calibration/agent if not using `rebotarm`.

**Safety:** custom table/wall/bin and target collision publishers were removed.
MoveIt retains robot self-collision checks but cannot avoid unmodelled obstacles.
Restart `move_group` if old scene objects are still present. The agent STOP button
is software cancellation, not a hardware emergency stop. On driver shutdown,
the controller moves to its upright `safe_home` position before disabling motors;
clear the swept workspace before stopping arm bringup.

## Simulation

With the simulation dependencies/assets installed and `run.dry_run` set as desired:

```bash
ros2 launch rebot_trash_sorting_agent sorting.launch.py \
   config_dir:="$AGENT_CONFIG" use_mujoco:=true
```

This uses simulated arm/camera topics, disables the USB camera driver, and selects
`table_sim` with its stored table map. It does not command the real driver. The
simulator publishes table and wrist images but **not** `front_camera`, so this
mode does not validate the new front-camera height path and uses fallback grasp
heights when no front images are available. The wrist correction is still the
existing fixed-scale X/Y heuristic, not a calibrated height estimate.

Open **http://127.0.0.1:8090/**. Optional launch flags are
`randomize:=true seed:=1`, `provider:=mock`, and `use_rviz:=true`. Submit tasks via
the dashboard or `/agent/task` as above. Stop any real pipeline before launching
simulation because the default topics and dashboard port are shared.
