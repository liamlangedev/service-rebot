# rebot_trash_sorting_agent

VLM-orchestrated pick-and-place agent for the Seeed reBot Arm B601-DM (`classic_real`).

## Quick start (simulation)

Run from the repository root:

```bash
source /opt/ros/jazzy/setup.bash && source ros2_ws/install/setup.bash && ros2 launch rebot_trash_sorting_agent sorting.launch.py use_mujoco:=true
```

Then open **http://127.0.0.1:8090/** in your browser for the interactive 3D MuJoCo view, table camera (`cam_corner`), wrist camera, task box, and STOP button.

Optional simulation flags:
- `randomize:=true seed:=1` — randomize object positions on the table
- `provider:=mock` — run without calling the Gemini API
- `dry_run:=true` — plan without moving the simulated arm

You can also submit a task from the CLI:

```bash
ros2 topic pub --once /agent/task std_msgs/msg/String '{data: "Put the can in the bin"}'
```

## Quick start (real hardware)

1. Put `GEMINI_API_KEY=...` in `ros2_ws/.env` (gitignored).
2. In `config/cameras.yaml`, set the `front_camera` device and `enabled: true`.
   Calibrate both fixed views: record five table marks once, then click the same
   five marks in the same order in the table view and again in the front view.
   Start the camera topics before running calibration. Camera mounts, focus and
   capture resolution must stay fixed after calibration.
   ```bash
   # Optional: disable motor torque so you can move the arm by hand.
   # WARNING: the arm will fall under gravity when disabled — be ready to catch/support it!
   ros2 service call /rebotarm/disable std_srvs/srv/Trigger "{}"

   # Touch five marks once; then click five points in each camera image
   ros2 run rebot_trash_sorting_agent calibrate_table --from-arm --count 5 --joint-states-topic /rebotarm/joint_states

   # Or pass measured base_link (x, y) coordinates directly
   ros2 run rebot_trash_sorting_agent calibrate_table --points "x1,y1;x2,y2;x3,y3;x4,y4"

   # Single-camera calibration remains available
   ros2 run rebot_trash_sorting_agent calibrate_table --camera table --from-arm --count 5
   ```
   Front-camera height uses the same marks and a calibrated `camera_matrix`
   (3x3 K, nine row-major values) plus optional OpenCV `distortion` coefficients
   from `cameras.yaml`. Without intrinsics only XY is saved. To explicitly try
   approximate height from the configured **horizontal** `fov_deg`, add
   `--allow-approximate-intrinsics` to the calibration command. Validate those
   heights against measured objects before allowing grasps; low table-plane
   reprojection error alone does not establish height accuracy.

   Both maps and the front height pose are saved to `config/calibration.yaml`.
   Restart the agent after calibration. `list_objects` reports `height_m` in metres
   above the table; grasp heights use `grasp.height_fractions` of this measurement.
   Missing/ambiguous front detections, changed resolution, or unavailable calibration
   fall back to `grasp.pinch_heights_m`, with a reason in `height_estimation`.
   The estimate assumes an upright object with an approximately circular footprint;
   overhangs, occlusion, and non-upright objects can produce inaccurate heights.
   For headless calibration supply `--pixels` and `--front-pixels` (and optionally
   `--image` / `--front-image`); coordinates must match each configured resolution.
3. Launch:
   ```bash
   ros2 launch rebot_trash_sorting_agent sorting.launch.py use_fake_hardware:=false channel:=/dev/ttyACM0
   ```

> **Note:** On shutdown (`Ctrl+C`), the arm bringup/driver (`reBotArmController`) moves the arm to its `safe_home` position (`0, 0, 0, 0, 0, 0` — upright) before disabling the motors. Make sure the workspace above the arm is clear before quitting.

Custom table/wall/bin and target collision publishers are not included. MoveIt
retains robot self-collision checks but cannot avoid unmodelled scene obstacles.
Restart `move_group` to discard any previously published obstacles.
