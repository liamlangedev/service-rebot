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
2. Calibrate the table camera homography:
   ```bash
   ros2 run rebot_trash_sorting_agent calibrate_table --points "x1,y1;x2,y2;x3,y3;x4,y4"
   ```
3. Launch:
   ```bash
   ros2 launch rebot_trash_sorting_agent sorting.launch.py use_fake_hardware:=false channel:=/dev/ttyACM0
   ```
