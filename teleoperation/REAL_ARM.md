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
| `rollout_policy.py` | **Run a trained policy** (ACT, SmolVLA, ...) on the arm through the 200 Hz MIT loop |
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

## Run a trained policy

`rollout_policy.py` loads a checkpoint (weights, normalization and camera renaming come from the checkpoint), reads the
cameras and joints, runs the policy at 30 Hz, and the 200 Hz loop interpolates and drives the motors with the same
gains used while recording. No Leap needed. Start with a dry run (no robot, fake images) to check the model loads:

```bash
python rollout_policy.py --policy niru-5/act_rebot_sort_v1 --dry-run
python rollout_policy.py --policy niru-5/smolvla_rebot_sort_v1_2026-11-15_02-15-27 --dry-run
```

Then on the arm (the cameras must be captured at **640x480**, the size of the v1 training data; this is the default here):

```bash
# ACT: language is ignored
python rollout_policy.py --port /dev/tty.usbmodem00000000050C1 --policy niru-5/act_rebot_sort_v1 \
    --duration 30 --n-action-steps 50

# SmolVLA: the prompt matters, use the training wording exactly
python rollout_policy.py --port /dev/tty.usbmodem00000000050C1 \
    --policy niru-5/smolvla_rebot_sort_v1_2026-11-15_02-15-27 \
    --task "pickup the keys and put it in the designated bin" --duration 30
```

Keys: **Right** start / stop early, **Esc** quit, **S** stop in place, **G** resume, **H** ready pose. Each run starts at the ready pose
and returns to it. Other checkpoints of a repo: `--subfolder checkpoints/010500/pretrained_model`.

| Option | Default | Meaning |
|---|---|---|
| `--n-action-steps` | model chunk (ACT 100, SmolVLA 50) | actions executed per policy call; smaller = reacts faster to what it sees |
| `--max-step-deg` | 4 | largest change of any joint target per policy step (4 deg x 30 Hz = 120 deg/s); first safety limit, lower it for the first runs |
| `--device` | auto | cuda > mps > cpu; SmolVLA takes ~0.25 s per chunk on this Mac's MPS |
| `--duration` | 30 | seconds per run; `--runs N` stops after N runs |
| `--mit.*` | the recording values (kp 3, kd 3, wrist 0.4, friction 1.3) | keep equal to what you recorded with |

First runs: put the keys and bin in the training layout, keep a hand on the power switch, start with `--max-step-deg 2`.
The policy can only do what the 640x480-camera, `front_wide` / `gripper` / `high_oblique` data showed it; a different camera
position or crop will degrade it. A dataset recorded with `record_episodes.py` now (16:9, 640x360) does not match these policies.

## Orchestrator: Gemini calls the policy by voice or text

Two processes, so the model is loaded once and every request reuses it:

```bash
# terminal 1: loads the policy and the arm once, serves skills on http://127.0.0.1:8000
python robot_server.py --port /dev/tty.usbmodem00000000050C1 --policy RoboCrafty/smolvla_rebot_merged_V2_15000 \
    --device mps --cam-height 360

# terminal 2: needs a Google AI Studio key in the environment (never commit it)
export GEMINI_API_KEY=...
python orchestrator.py            # then type: "I need a towel" / "clean up the table" / "stop"
```

- `config/skills.json` maps skill names (`bottle`, `towel`, `keys`) to the exact training prompts and the run time.
  Gemini can only pick a name; it cannot write prompts or send joint commands.
- Gemini's tools: `fetch(item)` (runs the skill, blocks, arm returns to ready), `look(camera)` (a camera frame it can see),
  `stop()`. It looks before fetching and after, retries once on failure.
- **Supervision.** `fetch` does not wait for the timer. Before moving, it asks the LLM (with the front camera image) whether the item
  is at the pick-up area; if not, it reports "none left" and the arm stays put. While the skill runs, about every 4 s it sends the
  first and the current frame to the LLM, which answers done / working / stuck / failed. Two "done" in a row end the skill and send
  the arm home; two "stuck", or no arm motion for 10 s, give up with a reason and a suggestion for the user. No automatic retries.
  Edit the plain-language hints (`scene`, per-skill `pickup`) in `config/skills.json` to match your table. `--judge-model` picks a
  smaller, faster model for these checks.
- **Buttons.** STOP (or Esc) ends everything and blocks further robot actions for that request; "Task done" ends the skill and lets
  the assistant wrap up.
- Server API: `GET /skills /status /frame?camera=...`, `POST /run {"skill": ...}`, `POST /stop`. S / G / H still work on the keyboard.
- Test without the robot: `python robot_server.py --fake --http-port 8000`, then run the orchestrator.
- `--model` selects the Gemini model (default `gemini-3.8-flash`; use whichever current model has image input and tool calling).

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
