# reBot Arm teleoperation with a Meta Quest (MuJoCo first)

Teleoperate the Seeed Studio **reBot Arm B601-DM** with a Meta Quest controller,
in MuJoCo first, so the same pipeline can later drive the real arm with confidence.

```
Quest controller ──ADB──> OculusReader ──> frame calibration ──> clutch mapping
     (APK on headset)       (pose+buttons)   (Quest -> robot axes)   (TCP target)
                                                                        │
              MuJoCo reBot B601  <── joint position targets <── differential IK
              (Seeed's official MJCF)       (100 Hz, rate-limited)
```

| File | What it does |
|---|---|
| `scripts/setup_assets.sh` | Fetches Seeed's official reBot MJCF/meshes and the OculusReader Quest 3 fork, plus its APK |
| `teleop/rebot_model.py` | Loads Seeed's `rebotarm_b601_colored.xml` and adds position servos, the coupled gripper, gravity compensation and the target marker |
| `teleop/ik.py` | Damped-least-squares IK on the `tcp` site, with joint-limit clipping, a posture bias and a joint-velocity limit |
| `teleop/quest_input.py` | OculusReader wrapper, Quest-to-robot frame conversion, clutch teleop mapping, scripted demo source |
| `sim_teleop.py` | Main app: Quest / mouse / demo input, MuJoCo viewer, optional `.npz` recording |
| `tools/quest_stream_check.py` | Checks that poses and buttons arrive from the headset |
| `tools/calibrate_quest_axes.py` | Records forward/left/up moves and writes `config/quest_calibration.json` |

## 1. Setup (PC)

```bash
sudo apt install android-tools-adb      # OculusReader talks to the Quest over ADB
./scripts/setup_assets.sh               # robot model + OculusReader + APK (not committed)
uv sync
```

## 2. Setup (Quest, once)

1. Make a free developer organization at <https://developer.oculus.com/manage/organizations/create/>.
2. In the Meta Horizon phone app, open the headset settings and turn on **Developer Mode**.
3. Connect the Quest over USB-C, put it on, and accept **Allow USB debugging** (tick *Always allow*).
4. Run `adb devices`. The headset should show as `device`, not `unauthorized`.

The first OculusReader run installs and launches the APK on the headset automatically.

**Wireless (optional):** with USB still plugged in, run `adb tcpip 5555` and
`adb shell ip route` to get the headset's IP. Unplug, then pass `--ip <quest-ip>`
to every command below.

## 3. Workflow

```bash
# a) Check that data streams (expect ~60-70 Hz, values change as you move)
uv run tools/quest_stream_check.py

# b) Calibrate axes: stand behind the robot's position, facing its +x direction
uv run tools/calibrate_quest_axes.py

# c) Teleoperate the simulated arm
uv run sim_teleop.py --input quest --no-rotation   # start position-only
uv run sim_teleop.py --input quest                 # then with orientation
```

No headset? Use `--input mouse` and drag the green target: double-click it, then
Ctrl+right-drag to move it and Ctrl+left-drag to rotate it. Up/Down arrows open and
close the gripper. `--input demo` runs a scripted controller motion instead.

### Quest controls (right hand; `--hand l` uses X/Y)

| Input | Action |
|---|---|
| **Grip (hold)** | Clutch. The arm follows your hand only while it is held. Release it to re-centre your hand, like lifting a mouse. |
| **Trigger** | Close the gripper (proportional) |
| **A** | Send the arm home |
| **B** | Toggle orientation tracking |

Useful flags: `--scale 0.5` gives finer motion, `--max-joint-vel 1.0` is gentler,
and `--record session.npz` logs the command and target streams.

## 4. Sim-to-real notes

- **Same commands as the real arm.** The loop outputs 6 joint position targets at
  100 Hz, rate-limited to `--max-joint-vel`. The real arm takes exactly that through
  Seeed's [reBotArm_control_py](https://github.com/Seeed-Projects/reBotArm_control_py)
  (`RebotArm().groups["arm"].send_pos_vel(q, vlim)`). The plan is a `RealBackend`
  that replaces `sim.command()`; nothing upstream of it needs to change.
- **Joint names and limits** come from Seeed's model (`joint1`..`joint6`), so they
  match the SDK's URDF.
- **Gripper units differ.** The sim uses finger travel in metres (0–0.05). The
  real SDK gripper motor takes radians, so a mapping is needed for the real arm.
- **Gravity.** The sim uses actuator gravity compensation to mimic the stiff
  POS_VEL loop on the Damiao motors. The real arm will have more lag and
  compliance, so start it with `--max-joint-vel 0.5` and `--scale 0.5`.
- **Model variant.** This uses the **DM** (Damiao) model. For the RS (RobStride)
  variant, point `DM_MJCF` in `teleop/rebot_model.py` at `RS/mjcf/rs_arm.xml`;
  its actuators would need a check.

## Credits

- Robot model: Seeed Studio [reBot-DevArm](https://github.com/Seeed-Projects/reBot-DevArm) (CERN-OHL-W)
- Quest reader: [OculusReader](https://github.com/rail-berkeley/oculus_reader),
  using the Quest 3 fork [jborbik/oculus_reader](https://github.com/jborbik/oculus_reader) (Apache-2.0)

## 5. Ultraleap + real arm (lerobot)

**Current instructions for the real arm, recording and safety are in [REAL_ARM.md](REAL_ARM.md); the commands below are the first version.**

Run these with the root `steel_team/.venv` (lerobot, leap, mujoco). Left fist or Space = clutch,
right hand drives, thumb-index pinch = gripper.

```bash
python sim_teleop.py --input leap            # 1. try it in the simulator first
python go_ready.py --port /dev/tty.usbmodem00000000050C1   # 2. MoveJ to gripper-down ready pose
python record_rebot.py --robot.type=rebot_b601_follower \
  --robot.port=/dev/tty.usbmodem00000000050C1 --robot.max_relative_target=3 \
  --teleop.type=leap_ik --dataset.repo_id=<user>/rebot_leap \
  --dataset.single_task="pick up the cube"  # 3. record
```

`teleop/rebot_real.py` holds the ready pose and the singularity guard (steps that reduce the
Jacobian's smallest singular value below a threshold are refused). Check `GRIPPER_OPEN_DEG` /
`GRIPPER_CLOSED_DEG` there against your gripper.
