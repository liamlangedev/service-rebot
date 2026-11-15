# Real reBot B601 arm: Leap Motion teleoperation and dataset recording

Hand (Ultraleap Leap) → clutch → IK → joint targets → 200 Hz MIT control loop (velocity, gravity and friction
feed-forward) → Damiao motors. Recorded as LeRobot datasets for ACT / VLA training.
Run everything from this folder with the repo's root venv (`steel_team/.venv`: lerobot[rebot], mujoco, scipy, pynput, leap).

## Files

| File | Purpose |
|---|---|
| `record_episodes.py` | **Main recorder.** Right = start/save, Left = discard, Esc = finish. `--resume` appends |
| `record_rebot.py` | Same idea through stock `lerobot-record` (fewer features; prefer `record_episodes.py`) |
| `go_ready.py` | Move the arm to the ready pose (gripper pointing down), then hold |
| `push_dataset.py` | Upload a local dataset to the Hugging Face Hub |
| `sim_teleop.py` | Same Leap/IK pipeline in MuJoCo (`--input leap`); use it to check hand axes safely |
| `tools/measure_gripper.py` | Measure the gripper's real open/closed angles → `config/gripper_limits.json` |
| `tools/probe_cameras.py` | Check which camera modes really work |
| `teleop/fast_loop.py` | 200 Hz control thread, S/G/H keys, controlled park at exit |
| `teleop/mit_ff.py` | MIT torque control: gains, gravity + friction feed-forward, gripper modes, `--mit.*` options |
| `teleop/lerobot_leap.py`, `teleop/leap_input.py` | Leap → clutch → IK teleoperator (`--teleop.type=leap_ik`) |
| `teleop/rebot_real.py` | Ready pose, singularity guard, helpers |
| `config/gripper_limits.json` | Measured gripper range (per arm, not portable) |
| `config/cameras.json` | Camera names → OpenCV indices, capture and saved resolution |

## One-time setup (per arm / per machine)

1. **Arm calibration** (arm in the B601 zero pose; sets the motor zeros): `lerobot-calibrate --robot.type=rebot_b601_follower --robot.port=<PORT>`.
   Anyone who plugs the arm into another computer and runs calibration re-zeros it: redo steps 1 and 2 afterwards.
2. **Gripper range.** lerobot's default gripper range (-270..0) is wrong for this arm. Measure the real one (torque is off, move it by hand):
   `python tools/measure_gripper.py --port <PORT>`. `record_*` and `go_ready.py` refuse to run without `config/gripper_limits.json`.
3. **Cameras.** Find indices with `lerobot-find-cameras opencv`, edit `config/cameras.json`
   (currently `front_wide`=1, `gripper`=2, `high_oblique`=3). Indices change when you replug.
   Cameras **capture 1280x720 (16:9) and are downscaled to 640x360** before saving. 4:3 modes such as 640x480 crop ~25% off the sides.
   Check modes: `python tools/probe_cameras.py`. Give the terminal camera permission in macOS.
4. **Leap**: install the Ultraleap service; the visualizer should show ~110 fps. `leap` and `libLeapC.6.dylib` must be in the venv.
5. Serial port on macOS: `/dev/tty.usbmodem00000000050C1` (Linux: `/dev/ttyACM0`, add yourself to `dialout`; pynput needs X11, not Wayland).
6. macOS: the terminal needs Accessibility permission (pynput keys, space clutch).

## Try it in simulation first

```bash
python sim_teleop.py --input leap
```

## Move to the ready pose

```bash
python go_ready.py --port /dev/tty.usbmodem00000000050C1
```
Hold the arm near the ready pose by hand, run it, press Enter. It does a smooth joint-space move (not Cartesian: the folded
start pose is near a singularity), then keeps holding until Ctrl-C. `--no-hold` exits right after.

## Record a dataset

```bash
python record_episodes.py --port /dev/tty.usbmodem00000000050C1 \
  --repo-id RoboCrafty/rebot_sort_v2 --task "pick up the keys and put them in the bin" \
  --episodes 50 --fps 30 --max-episode-s 30 \
  --teleop.scale=1.5 --mit.kp_scale=3 --mit.kd_scale=3 --mit.wrist_scale=0.4 --mit.friction_scale=1.3
```
Add `--resume` to append to an existing dataset (`--episodes` is then the **total**). Keep the `--task` text identical across sessions.
At start it runs a gravity-compensation sign check, then asks for Enter before moving to the ready pose.

### Keys

| Key | Action |
|---|---|
| **Right** | start an episode; again to save it |
| **Left** | discard the current episode |
| **Esc** | finish and write the dataset |
| **S** | stop in place (holds the arm, torque on) |
| **G** | resume after stop (release and re-press the clutch) |
| **H** | go to the ready pose |
| **Space** (held) or **left fist** | clutch: the arm follows the right hand only while engaged |
| right hand thumb-index pinch | gripper |

After every episode the arm returns to ready by itself. Episodes are encoded while recording, so saving is near-instant.
At exit it holds the arm, asks for Enter, lowers it slowly to the folded rest pose and then releases torque (`--park yes|ask|no`).
Ctrl-C at that prompt exits immediately and the arm goes limp: support it.

### Options

| Option | Default | Meaning |
|---|---|---|
| `--teleop.scale` | 1.5 | hand-to-robot motion gain |
| `--teleop.smoothing` | 0.85 | hand filter (higher = smoother, laggier) |
| `--teleop.track_rotation` / `--no-teleop.track_rotation` | on | follow hand rotation |
| `--teleop.max_joint_vel` / `--teleop.max_wrist_vel` | 2.5 / 1.5 rad/s | IK speed limits |
| `--teleop.max_rot_vel` | 2.0 rad/s | how fast the orientation target may turn (rejects Leap spikes) |
| `--teleop.gripper_vel` | 2000 deg/s | gripper command slew limit |
| `--mit.kp_scale`, `--mit.kd_scale` | 1.0 | multiply the arm gains (big joints kp 40 / kd 2.5 before scaling) |
| `--mit.wrist_scale` | 1.0 | extra multiplier on wrist kp/kd |
| `--mit.friction_scale` | 1.0 | stiction compensation (0 = off); too high = hunting/buzz |
| `--mit.cmd_tau` | 0.03 s | joint-command low-pass |
| `--mit.grip_mode` | `force_pos` | `force_pos` (firmware torque ratio), `impedance`, `mit` |
| `--gripper-torque-ratio` | 0.03 | `force_pos` squeeze force (fraction of peak torque) |
| `--camera NAME=INDEX` | from json | override one camera |
| `--save-width/--save-height` | 640 / 360 | recorded image size |

## What is recorded

`action` = the joint-position targets the 200 Hz loop last sent (degrees, 6 joints + gripper, raw motor frame).
`observation.state` = measured joint angles, same names. Images: one video per camera. The action leads the state by roughly 50-100 ms.
Inference must go through the same 200 Hz MIT loop (same gains and feed-forward), not plain lerobot `send_action`.

## Push to the Hub

```bash
python push_dataset.py RoboCrafty/rebot_sort_v2      # private; --public for public
```
Run again after `--resume` sessions. Needs `hf auth login`.

## Safety and troubleshooting

- Keep a hand near the power switch. There is no collision detection: only software joint limits, the 15-20° command-error clamp
  (bounds torque to roughly kp x error), the TCP workspace box and a singularity guard.
- **Never end a run by killing the process**: the motors go limp and the arm falls. Use Esc, or S then Ctrl-C and support the arm.
- Gripper positions are far outside the measured range, or the gripper does not move: someone re-zeroed the motors. Re-run `tools/measure_gripper.py`.
- Camera `Timed out waiting for frame`: another process may still hold the cameras (`ps aux | grep record_`), or USB bandwidth is too high
  (use separate ports). Startup retries 4 times; stale frames are reused for up to 3 s.
- `[fast_loop] N Hz` should stay near 200. A collapse means the laptop is starved (low battery power mode, heavy encoding): plug it in.
- A log of commanded vs measured joints is written to `/tmp/fast_loop_log.npz` on a clean exit.
- Dataset folder `~/.cache/huggingface/lerobot/<repo-id>`: an existing one needs `--resume` or a new `--repo-id`.
- Motor gains in firmware (`pos_vel` mode) are unrelated: this pipeline uses MIT mode, which needs none of them.
