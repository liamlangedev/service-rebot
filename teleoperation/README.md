# reBot Arm teleoperation with a Meta Quest (MuJoCo → real arm)

Teleoperate the Seeed Studio **reBot Arm B601-DM** with a Meta Quest controller (or the
mouse), in MuJoCo first and then on the real arm, and record **LeRobot datasets** whose
format matches the real robot's.

```
Quest browser (WebXR page) ──WebSocket──> vr-teleop-kit relay ─┐
Quest APK (OculusReader)   ──ADB────────────────────────────────┤  controller pose + buttons
Mouse drag in the viewer   ─────────────────────────────────────┘
        │
        ▼  frame calibration (Quest axes -> robot axes)
        ▼  clutch mapping (hold grip = follow the hand) -> TCP target
        ▼  differential IK (6-DoF, joint limits = real arm soft limits)
        ▼
  joint targets ──> MuJoCo reBot B601 (Seeed's official MJCF)      --robot sim
               └──> real arm via LeRobot rebot_b601_follower       --robot real
        │
        └──> LeRobot dataset (shoulder_pan.pos … gripper.pos in degrees + camera videos)
```

| File | What it does |
|---|---|
| `sim_teleop.py` | Main app: input → IK → sim or real arm, viewer, recording |
| `teleop/rebot_model.py` | Loads Seeed's `rebotarm_b601_colored.xml` and adds servos, the gripper, gravity compensation, cameras (`front`, `wrist`, `overhead_rgb`), the target marker and the real arm's joint limits |
| `teleop/ik.py` | Damped-least-squares IK on the `tcp` site |
| `teleop/quest_input.py` | `WebXRSource` (vr-teleop-kit relay), `OculusSource` (OculusReader), clutch mapping, demo source |
| `teleop/mouse_input.py` | Turns a mouse drag on the arm into target motion |
| `teleop/lerobot_mapping.py` | Sim ↔ LeRobot joint names and units |
| `teleop/lerobot_recorder.py` | Writes LeRobot v3 datasets |
| `teleop/real_robot.py` | Real-arm backend using LeRobot's `RebotB601Follower` |
| `tools/quest_stream_check.py` | Checks that poses and buttons arrive from the headset |
| `tools/calibrate_quest_axes.py` | Records forward/left/up moves and writes `config/quest_calibration_<source>.json` |
| `tools/check_setup.py` | One-command check that the setup is complete |
| `TODO.md` | What is done, what needs the headset or the real arm, what is next |
| `scripts/setup_assets.sh` | Fetches the reBot model and OculusReader (not committed) |

## Quick start: one-script Quest end-effector control

With the Quest plugged in over USB (`adb devices` shows it as `device`):

```bash
uv run quest_ee_teleop.py                    # launches the headset app + MuJoCo
uv run quest_ee_teleop.py --ip <quest-ip>    # over Wi-Fi ADB
uv run quest_ee_teleop.py --demo             # no headset: scripted controller
```

Right controller:

| Input | Action |
|---|---|
| **A** | Start mimicking: the gripper follows your hand's position **and** rotation |
| **B** | Stop mimicking: the arm holds its pose (A again resumes from your hand's new spot) |
| **Thumbstick left / right** | Close / open the gripper (hold; further = faster) |

Keyboard in the viewer: Home sends the arm home, Up/Down open/close the gripper.
Tune with `--scale 0.5` (finer motion), `--grip-speed`, `--max-joint-vel`.
Full setup and check steps: [QUEST_EE_TELEOP.md](QUEST_EE_TELEOP.md).

## 1. Setup

```bash
./scripts/setup_assets.sh       # reBot MJCF + meshes, OculusReader (+ APK)
uv sync                         # sim + Quest input
uv sync --extra lerobot         # + LeRobot recording and the real-arm driver (CPU torch)
```

Recording uses CPU torch to keep the download small. Install CUDA torch on the
machine you train on.

### Check the setup

```bash
uv run --extra lerobot tools/check_setup.py     # or: uv run tools/check_setup.py
```

This needs no headset or robot. It checks the model assets, builds the model, tests
the IK, runs 2 s of headless teleop, and reports on the Quest pieces (relay,
OculusReader + APK, adb + connected devices, axis calibration), LeRobot,
`motorbridge` and `follower.json`. **FAIL** means the simulator won't run. **WARN**
marks something needed only for one mode (headset, recording, real arm). Expected
on a fresh machine: `Quest axis calibration` stays WARN until you run
`tools/calibrate_quest_axes.py` with the headset.

## 2. Try it without a headset

```bash
uv run sim_teleop.py --input mouse
```

**Mouse:** double-click any part of the arm (the gripper is easiest) so it is highlighted.
Then **Ctrl + right-drag** moves the gripper and **Ctrl + left-drag** rotates it. The
arm follows through the IK. Plain dragging only moves the camera. Double-click empty
space to deselect.

**Keyboard:** Up/Down opens and closes the gripper, Home sends the arm home, End
starts or saves an episode, and Delete discards the current episode. Avoid Backspace,
which is the viewer's own reset.

`--input demo` runs a scripted motion.

## 3. Quest via WebXR (default, nothing to install on the headset)

This uses the relay and web page from
[vr-teleop-kit](https://github.com/Dream-Machines-Robotics/vr-teleop-kit)
(installed by `uv sync`). Their IK is DK1-specific, so we use only the relay and
page and feed the poses into our reBot IK.

1. Turn on Developer Mode on the Quest (Meta Horizon phone app → Devices → headset),
   plug in USB-C and accept "Allow USB debugging" in the headset.
2. Run:
   ```bash
   uv run vr-teleop-relay                   # terminal 1, serves http://localhost:8443
   adb reverse tcp:8443 tcp:8443            # forward the Quest's localhost over USB
   ```
3. In the Quest browser, open `http://localhost:8443/` and press **Start Teleop**.
4. In terminal 2:
   ```bash
   uv run tools/quest_stream_check.py       # poses streaming? (~72 Hz)
   uv run tools/calibrate_quest_axes.py     # once: map Quest axes to robot axes
   uv run sim_teleop.py --input quest --no-rotation   # start position-only
   uv run sim_teleop.py --input quest                 # then with orientation
   ```

For Wi-Fi instead of USB, see vr-teleop-kit's README (LAN HTTPS with a self-signed
cert), then pass `--relay wss://<pc-ip>:8443/ws`.

**OculusReader fallback:** run `sudo apt install android-tools-adb` first, then add
`--input oculus` (and `--source oculus` for the tools). The first run installs the
APK. Calibration is stored separately per source.

### Quest controls (right hand; `--hand l` uses X/Y)

| Input | Action |
|---|---|
| **Grip (hold)** | Clutch: the arm follows your hand while held; release to re-centre |
| **Trigger** | Close the gripper (proportional) |
| **A** | Send the arm home |
| **B** | Toggle orientation tracking |
| **Thumbstick click** | Start / save a recording episode |

Useful flags: `--scale 0.5` for finer motion, `--max-joint-vel 1.0` for gentler motion.

## 4. Record LeRobot datasets

```bash
uv run sim_teleop.py --input quest --record --task "pick up the red cube"
```

Each episode goes: start (thumbstick click or End) → do the task → save (same
button). Save resets the scene for the next episode. Delete discards the current
episode. Datasets go to `datasets/<name>_<timestamp>/` (`--dataset-root` overrides).

The format matches what `lerobot-record` produces with the real arm
(`robot_type = rebot_b601_follower`), so sim and real data can be mixed:

| Feature | Content |
|---|---|
| `observation.state` | measured `shoulder_pan.pos`, `shoulder_lift.pos`, `elbow_flex.pos`, `wrist_flex.pos`, `wrist_yaw.pos`, `wrist_roll.pos`, `gripper.pos` (deg) |
| `action` | the commanded values, same names and units |
| `observation.images.{front,wrist,overhead_rgb}` | 640×480 videos (`--cameras` to choose) |

25 fps by default (`--fps`; it must divide the 100 Hz control rate). Rename the
cameras to match your real camera names before mixing datasets. Push to the Hub with
`LeRobotDataset(repo_id, root=...).push_to_hub()`.

## 5. Real arm (untested on hardware so far)

```bash
uv run sim_teleop.py --input quest --robot real --port /dev/ttyACM0
```

- Uses LeRobot's `rebot_b601_follower` driver with the team's `follower.json`
  calibration (repo root, `--robot-id follower`). The MuJoCo window mirrors the
  measured arm pose.
- Starts from the measured pose, so nothing moves until you hold the grip.
- Safety defaults: 50 Hz, joint speed ≤ 0.5 rad/s, and ≤ 5° change per command
  (`--max-step-deg`).
- **Torque is disabled on exit (LeRobot default). Support the arm before quitting.**
- First check the joint mapping in `teleop/lerobot_mapping.py`: with the arm in a
  few poses, the mirrored sim pose must match the real one. The gripper's 0 to −270°
  mapping onto finger travel is an assumption.

## Sim-to-real notes

- Sim joint ranges are clipped to the real arm's LeRobot soft limits, so recorded
  actions are valid on hardware.
- Gravity: the sim uses actuator gravity compensation to mimic the stiff Damiao loop.
- The model is the **DM** variant. For RS, point `DM_MJCF` at `RS/mjcf/rs_arm.xml`
  and change `motor_family` in `teleop/real_robot.py`.
- vr-teleop-kit's own IK assumes a near-spherical wrist. The reBot's joint 4 and 5
  axes are 78 mm apart, which is why we use a full 6-DoF IK instead.

## Credits

- Robot model: Seeed Studio [reBot-DevArm](https://github.com/Seeed-Projects/reBot-DevArm) (CERN-OHL-W)
- WebXR relay and page: [vr-teleop-kit](https://github.com/Dream-Machines-Robotics/vr-teleop-kit) (Apache-2.0)
- Quest reader: [OculusReader](https://github.com/rail-berkeley/oculus_reader), Quest 3 fork
  [jborbik/oculus_reader](https://github.com/jborbik/oculus_reader) (Apache-2.0)
- Real-arm driver and dataset format: [LeRobot](https://github.com/huggingface/lerobot) (Apache-2.0)
