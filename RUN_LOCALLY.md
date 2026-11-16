# Run the reBot concierge locally (branch `niranjan-rollout`)

A runbook for setting up and running this branch on a new computer, with the trained policy running **on that
computer** (GPU or Apple Silicon) instead of the GPU Space. It is written so that a Claude Code session can follow it step
by step: do the steps in order, check each **Check:** line before moving on, and ask the human before anything that
moves the arm.

What runs:

```
browser :8080  guest page (chat, voice, cameras)     ┐
browser :8080/operator  operator dashboard (issues)  ├─ teleoperation/web_ui.py  ── Claude Opus 5.5 (concierge + camera checks)
                                                     ┘        │ HTTP
                                         teleoperation/robot_server.py :8000 ── arm (serial) + 3 USB cameras
                                                              └─ policy (SmolVLA or XVLA), loaded locally on cuda / mps
```

The guest asks for something ("I'm off to the sauna"), Claude picks an item (towel or bottle), the robot server runs that
item's trained policy, and Claude watches the front camera until the item is in the tray. Problems go to `/operator`.

## 0. Things to know first

| | |
|---|---|
| Models (public, no access needed) | **SmolVLA** `RoboCrafty/smolvla_rebot_merged_V2` (https://huggingface.co/RoboCrafty/smolvla_rebot_merged_V2), 0.45B, chunk 50; the one tested most with the concierge. **XVLA** `niru-5/xvla_rebot_merged_V2` (https://huggingface.co/niru-5/xvla_rebot_merged_V2), 0.9B, chunk 30. |
| Training data | `RoboCrafty/rebot_sort_merged_V2` (public): 640x360 frames from `front_wide`, `gripper`, `high_oblique`; tasks `pick up the bottle and put it in the designated bin` and `pick up the towel and put it in the designated bin` |
| Downloads | Automatic on first use (`--policy <repo>`), into `~/.cache/huggingface/hub`. SmolVLA also pulls its base VLM `HuggingFaceTB/SmolVLM2-500M-Video-Instruct` on first load. To prefetch: `hf download RoboCrafty/smolvla_rebot_merged_V2` |
| GPU Space | `niru-5/rebot-policy-server` is **private** (Niranjan's account) and only needed when the computer is too slow (CPU). This runbook does not use it. |
| Claude API key | Needed for the concierge. Not in git. Put it in `.env` in the repo root (step 2). |
| Python | 3.12 (lerobot 0.7.0 needs >= 3.12) |

**Never do these:**
- Do not run `lerobot-calibrate`, and never press Enter at a prompt that says *"move the reBot B601 to its ZERO POSITION"*.
  That re-zeroes the motors, after which the policies and `config/gripper_limits.json` no longer match. Use step 4.
- Do not end a run by killing the process (`kill`, closing the terminal): the motors go limp and the arm falls. Quit with
  Ctrl-C at the robot server / Esc in rollout_policy, then follow the prompt (it releases torque after a 3 s warning, so
  keep a hand under the arm).
- Do not commit `.env` (it is git-ignored).

## 1. Get the code and the environment

```bash
git clone git@github.com:niru-5/steel_team.git && cd steel_team
git checkout niranjan-rollout
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -r requirements.txt          # lerobot[rebot,dataset,smolvla,xvla]==0.7.0, torch, fastapi, anthropic, ...
```
(No uv: `python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.)

**Check:**
```bash
python -c "import lerobot, motorbridge, torch; print(lerobot.__version__, torch.__version__, 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu'))"
```
prints `0.7.0`, a torch version and `cuda` or `mps`. With `cpu` the policy is too slow for the arm (~30 s per chunk); ask
Niranjan for access to the GPU Space and use `--remote-url https://niru-5-rebot-policy-server.hf.space` (see `teleoperation/REAL_ARM.md`).

If ROS is sourced in the shell (`/opt/ros/...` on `PYTHONPATH`), run Python with `env -u PYTHONPATH` or open a clean shell.

## 2. API key

Create `.env` in the repo root (same folder as this file):
```
ANTHROPIC_API_KEY=sk-ant-...
```
`ANTHROPIC_TOKEN=...` also works. **Check:** `git status` does not list `.env`.

## 3. Check the policy runs on this computer (no robot)

```bash
cd teleoperation
python rollout_policy.py --policy RoboCrafty/smolvla_rebot_merged_V2 --dry-run \
    --task "pick up the towel and put it in the designated bin"
```
**Check:** it ends with `OK: the policy loads and produces 7-dim joint targets.` and the `call 1` / `call 2` lines show
well under 1000 ms (the arm plays a 50-step chunk in ~1.7 s, so inference must be faster than that). On an RTX-class GPU
expect ~100-300 ms; on Apple Silicon (mps) ~250 ms.

The same for XVLA: `--policy niru-5/xvla_rebot_merged_V2`. If XVLA fails on a GPU with a cuDNN error such as
`unable to find an engine` (older GPUs without native bfloat16, e.g. T4 / RTX 20xx), add `--dtype float32`.

## 4. Connect the arm (first time on this computer)

1. Arm powered, USB plugged in. Find the serial port: Linux `ls /dev/ttyACM*` (usually `/dev/ttyACM0`; add the user to
   the `dialout` group if permission is denied), macOS `ls /dev/tty.usbmodem*`.
2. Calibration file without re-zeroing (see "Never do these"):
   ```bash
   python tools/write_calibration.py --port <PORT>
   ```
   **Check:** it prints `wrote ...rebot_b601_follower/None.json`, or `already exists` (fine).
3. `config/gripper_limits.json` is in git and belongs to this arm; leave it.

## 5. Cameras

The robot server needs the three cameras `front_wide` (low front view of the whole table and the white foam tray on the
right), `gripper` (between the gripper fingers) and `high_oblique` (steep view from above). Their OpenCV indices differ
per computer and change when replugged.

- macOS: `config/cameras.json` (indices from the Mac this was recorded on: front_wide 1, gripper 2, high_oblique 3).
- Linux: `config/cameras_linux.json` (Niranjan's Ubuntu laptop: 2 / 4 / 6, with `"fourcc": "MJPG"`; without MJPG the
  USB2 cameras only give 10 fps at 1280x720 and the robot server refuses to start with `failed to set fps=30`).

On a new computer: list the devices (`lerobot-find-cameras opencv`, or on Linux `ls /sys/class/video4linux/*/name`),
grab one frame from each and look at it to tell which is which, then write the indices into a copy of the JSON
(e.g. `config/cameras_<host>.json`) and pass it with `--cameras-file`. Capture must be 1280x720 at 30 fps (16:9, the
frames are downscaled to the policy's 640x360). Close other programs that hold the cameras.

## 6. Run

Terminal 1, robot server (loads the policy and the arm once):
```bash
cd teleoperation
python robot_server.py --port <PORT> --cameras-file config/<cameras file>.json \
    --policy RoboCrafty/smolvla_rebot_merged_V2 --device auto
```
It runs a gravity check, prints the arm's pose and asks **Enter** to move to the ready pose: ask the human to hold the
arm near the ready pose and press Enter themselves. **Check:** it prints `robot ready.`

Terminal 2, concierge web UI (Claude Opus 5.5 by default):
```bash
cd teleoperation
python web_ui.py
```
**Check:** it prints the guest and operator URLs; `curl -s localhost:8080/api/info` lists the skills `bottle` and
`towel` and `"model": "claude-opus-5-5"`.

Open in Chrome (voice needs Chrome or Edge):
- guest page http://localhost:8080/ : type e.g. "I'm heading to the sauna" (towel) or "I'm thirsty" (water)
- operator page http://localhost:8080/operator : issues with reasons and camera snapshots, STOP, Task done, New guest

Put the items in the pick-up area (left/middle of the table) first: a green glass sparkling-water bottle, and the towel
rolled tightly into a teal/green-and-white roll lying on its side. What they look like is described in
`config/skills.json` (`looks_like`, `not_this`); Claude's camera check uses those words, so update them if the objects
change.

Stopping: STOP button (or Esc) in the browser stops a hand-out. To quit: Ctrl-C in terminal 2, then Ctrl-C in terminal 1
and answer its prompt (hand under the arm: torque is released after a 3 s countdown).

## 7. Optional / troubleshooting

| Symptom | Cause / fix |
|---|---|
| Keys S / G / H (and Right / Esc in rollout_policy) do nothing on Linux | Wayland session: the scripts default to `--keys auto`, which then reads keys from the terminal running them; keep that terminal focused |
| Typing in the guest page does nothing | wrong page (the operator page has no chat), or the tab was open before `web_ui.py` restarted: reload with Ctrl+Shift+R |
| Concierge says an item ran out although it is there | the camera check did not recognise it: fix `looks_like` / `not_this` in `config/skills.json` and restart `web_ui.py` |
| `web_ui.py` prints "waiting for the robot server" | start `robot_server.py` first; the UI waits for it |
| `401 invalid x-api-key` on the operator page | the key in `.env` is wrong or revoked |
| Run a policy without the concierge | `python rollout_policy.py --port <PORT> --cameras-file <file> --policy RoboCrafty/smolvla_rebot_merged_V2 --task "pick up the bottle and put it in the designated bin" --duration 60 --max-step-deg 2` (Right arrow starts a run) |
| Test the UI without the arm | `python robot_server.py --fake [--fake-images DIR]` (DIR with `front_wide.jpg`, `gripper.jpg`, `high_oblique.jpg`) and `python web_ui.py --backend demo` (no API key) |

More detail on every script and option: `teleoperation/REAL_ARM.md`.
