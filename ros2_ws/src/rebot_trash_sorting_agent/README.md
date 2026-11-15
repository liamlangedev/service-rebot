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
2. Calibrate the table camera homography (either by pointing the **closed** gripper tip at 5 table marks with `--from-arm`, or by passing measured `base_link` `--points`):
   ```bash
   # Optional: disable motor torque so you can move the arm by hand.
   # WARNING: the arm will fall under gravity when disabled — be ready to catch/support it!
   ros2 service call /rebotarm/disable std_srvs/srv/Trigger "{}"

   # Recommended: touch each mark with the closed gripper tip, move arm away, then click the marks
   ros2 run rebot_trash_sorting_agent calibrate_table --from-arm --count 5 --joint-states-topic /rebotarm/joint_states

   # Or pass measured base_link (x, y) coordinates directly
   ros2 run rebot_trash_sorting_agent calibrate_table --points "x1,y1;x2,y2;x3,y3;x4,y4"
   ```
3. Launch:
   ```bash
   ros2 launch rebot_trash_sorting_agent sorting.launch.py use_fake_hardware:=false channel:=/dev/ttyACM0
   ```

> **Note:** On shutdown (`Ctrl+C`), the arm bringup/driver (`reBotArmController`) moves the arm to its `safe_home` position (`0, 0, 0, 0, 0, 0` — upright) before disabling the motors. Make sure the workspace above the arm is clear before quitting.
