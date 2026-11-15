# rollout: test policies on the real arm, with safety limits

One script, three strategies. It drives the arm directly through lerobot's reBot follower
(no ROS), so it is the quickest way to see what a policy does on the real arm.

| mode | what it tests | default policy |
|---|---|---|
| `full` | the full-task policy (pick the keys, put them in the bin) from the ready pose | `niru-5/act_rebot_sort_v1` |
| `grasp-abs` | grasp-only ACT, absolute: slow 5 s move to a dataset clip's start pose, grasp, stop | `niru-5/act_rebot_grasp_keys_abs` (checkpoint 2000) |
| `grasp-rel` | grasp-only ACT, relative: you place the arm above the keys, it grasps, stops | `niru-5/act_rebot_grasp_keys_rel` |

## First real test, step by step (full ACT, then grasp-rel)

Run everything from the repo root (`steel_team/`, or this worktree until it is merged) in
a normal terminal. The keys are read straight from the terminal, so don't pipe the output.

### 0. Set up once per session

```bash
P=teleoperation/.venv/bin/python
FRONT=/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._KD-USB_Cameras_KD-USB_Cameras-video-index0
WRIST=/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB2.0_CAM1_USB2.0_CAM1-video-index0
HIGH=/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_2ED4DF6F-video-index0
CAMS="--cam front_wide=$FRONT --cam gripper=$WRIST --cam high_oblique=$HIGH"
```

Camera mapping, checked on 2026-11-15 against the dataset views:

| dataset camera | physical camera | device then |
|---|---|---|
| `front_wide` | Sonix KD-USB, far edge of the table, looking back at the arm | /dev/video2 |
| `gripper` | Sonix USB2.0 CAM1 on the wrist | /dev/video4 |
| `high_oblique` | Logitech C920 on the gooseneck | /dev/video6 |

The `/dev/v4l/by-id` paths stay the same across replugs; `/dev/videoN` numbers don't.

1. **Check the cameras.**

   ```bash
   $P rollout/check_cameras.py $CAMS
   ```

   Open `rollout/logs/cameras.jpg` next to `rollout/camera_reference.jpg` (the dataset
   views). Each name should show the same view. The C920 view is framed somewhat
   differently from the dataset's `high_oblique`, and the table now has the yellow tape.
   That is a distribution shift for the 3-camera full ACT. grasp-rel only uses the wrist
   camera.

2. **Check the arm.** Power on, USB-CAN on `/dev/ttyACM0`, `follower.json` in the repo
   root (the script refuses to connect without it, so the motors are never re-zeroed).
   Keep a hand near the power switch for every run.

3. **Optional dry run** without the arm, to see the prompts:
   `$P rollout/rollout.py grasp-rel --fake-hardware --auto-start --arrive-tol-deg 15 --max-lag-deg 40`
   (needs a local copy of rebot_sort_v1 for the fake camera frames; see "Dry run" below).

### A. Full-task ACT

**Scene:** the bin in its usual place, the keys where they were in the demos: on the
table about 30 cm in front of the base and 25 cm to its right (TCP x 0.24-0.37 m,
y -0.22 to -0.30 m in the base frame; compare the `front_wide` view in
`camera_reference.jpg`). Nothing else in the arm's way.

**First run, slow, with a short timeout:**

```bash
$P rollout/rollout.py full $CAMS --max-speed 25 --timeout 20
```

What happens:

1. The policy loads (about 10 s), then the banner prints.
2. The arm moves to the ready pose over at least 5 s (gripper down, 25 cm above the
   table). Press `space` to stop it if anything looks wrong.
3. `Ready. Press a to start the policy, q to quit.` Press **`a`**.
4. The policy runs: it should reach for the keys, close, lift and swing to the bin.
   Press **`space`** at any moment to stop. The arm then holds where it is.
5. It ends after `--timeout` seconds, on a key, or on a safety limit. The reason is
   printed (`policy stopped: ...`).
6. `holding; press q to quit`. Press **`q`**. Torque stays on: support the arm before
   switching the power off.

If the first run looks sane, go faster: drop `--max-speed`, which defaults to 45 deg/s.
The teleop demos moved at up to ~100 deg/s, so the policy will look slow either way.
`--timeout 40` is the default.

### B. Grasp-only ACT, relative (grasp-rel)

**Scene:** the keys anywhere the arm can reach. Its whole point is grasping away from the
demo spot, so start in the demo spot, then move them.

**First run, with the floor above the table** (it stops just before touching, so you see
the approach first):

```bash
$P rollout/rollout.py grasp-rel --cam gripper=$WRIST --max-speed 20 --max-offset 15 --min-tcp-z 0.13
```

What happens:

1. The arm moves to the ready pose (5 s).
2. Placement. The arm is holding. Then:
   - **put a hand under the arm, then press `h`**: torque goes OFF and the arm drops
     into your hand;
   - move the gripper to about **5 cm above the keys**, with the wrist camera looking at
     them and the jaw across the key's narrow side. Keep the wrist angle like the demos:
     tool pointing down with a slight tilt (wrist_flex about 50-70 deg). The policy adds
     its joint changes to this pose, so a very different wrist angle sends it outside
     what it learned. A dry run from 77 deg asked for 98 deg and the joint limit had to
     clamp it;
   - press **`h`** again: torque ON, the arm holds there and the gripper opens.
3. Press **`a`** to start the grasp (or `q` to quit).
4. The policy descends, closes and lifts. It stops by itself when the jaw has closed and
   settled and the TCP has risen 5 cm (`policy stopped: gripped and lifted 5.x cm`), or
   after 10 s, or on `space`. Then it holds.
5. **`q`** to quit. Torque stays on, and the keys stay in the gripper.

With `--min-tcp-z 0.13` the run usually ends with
`safety: TCP z 0.12x m below floor 0.130 m` just above the keys. That's expected on the
first run: it shows the approach is aimed right. Then run with the default floor (0.120)
so it can actually grasp:

```bash
$P rollout/rollout.py grasp-rel --cam gripper=$WRIST --max-speed 30 --max-offset 20
```

Then move the keys: 5, 10 and 15 cm away from the demo spot, rotated 45 and 90 deg.
Place the arm above them each time.

### C. After each run

Every run writes `rollout/logs/<time>_<mode>.json` (outcome, events, arguments) and an
`.npz` (per tick: state, policy action, sent command, TCP, which limit clipped). The JSON
`reason` tells you why it stopped. Keep the logs of interesting runs.

### Troubleshooting

| message | meaning / what to do |
|---|---|
| `calibration ... not found` | run from the repo root, or pass `--calibration-dir` |
| `policy needs cameras [...]` | add the missing `--cam NAME=DEVICE` |
| `refusing to move to ...` / `TCP z ... below floor` | the pose is outside the workspace limits. For grasps: the floor did its job (see above) |
| `arm lags the command by N deg` | the arm is blocked or much slower than commanded; check for contact. `--max-lag-deg` |
| `chunk ran out before the next inference` | inference is slower than the action chunk (grasp-abs on CPU); use `--device cuda` |
| `did not reach the ready pose (residual N deg)` | the arm ended more than `--arrive-tol-deg` (5) away; look at what stopped it |
| arm limp after quitting | the motors need commands; the script holds until `q`. Restart it or support the arm |

## Keys (terminal, no Enter)

| key | |
|---|---|
| `a` | start the policy (after the approach / placement) |
| `space` or `s` | stop the policy now and hold the pose |
| `q` | quit: the arm keeps holding, torque stays **on** |
| `h` | grasp-rel only, before start: torque off for hand placement, `h` again locks the pose |

## grasp-abs

```bash
$P rollout/rollout.py grasp-abs $CAMS --start-episode 27 --device cuda
```

It prints the clip's TCP position (x, y in the base frame); put the keys under the
gripper there. It then goes ready pose -> the clip's first pose (5 s, `--approach-s`) ->
waits for `a` -> grasps -> stops once gripped and lifted. Clips 27-29 (source episodes
32-34) were held out from training; 0-26 were trained on. It needs `--device cuda` or a
fast CPU: 3-camera inference takes ~1.1 s on the dev laptop, longer than its 1 s chunks.

## Safety limits

Applied to every command, in this order (`safety.py`, defaults in brackets):

1. **Joint soft limits:** the real arm's limits minus 1 deg.
2. **Offset from the start pose** (grasp modes, `--max-offset 30` deg per joint).
3. **Speed** (`--max-speed 45` deg/s per joint, from one command to the next).
4. **Workspace** (forward kinematics of the command): TCP site height
   `--min-tcp-z 0.120` m and horizontal reach `--max-reach 0.55` m. A command outside is
   refused, and the rollout stops and holds.
   - The `tcp` site is about 14 cm above the fingertips. Dataset grasps happen at a site
     height of 0.144-0.15 m. While closing, the teleop commands pressed a little into the
     table (1% of action frames are below 0.128 m), so 0.120 allows a normal grasp and
     stops anything deeper.
   - The dataset's farthest reach is 0.495 m.
5. **Lag** (`--max-lag-deg 25` held for 1 s) stops the rollout.
6. **Timeout** (`--timeout`, 40 s full, 10 s grasps).

The driver's own limits stay on: `--max-step-deg 8` (lerobot `max_relative_target`, per
command from the measured position) and pos_vel control with a motor speed cap of
`--motor-vel-deg 60` deg/s. Every stop ends in a hold; every exit leaves torque on.

## Units

- Arm joints are lerobot degrees, as in the dataset: every rebot_sort_v1 episode starts
  at this repo's ready pose.
- The gripper is mapped through the opening fraction. This arm reads 161 open / 507
  closed (`teleoperation/config/gripper_limits.json`); the dataset arm read -365 / -5.

## Inference speed

Inference runs in a thread on the newest observation. Each 30 Hz tick executes the action
of the latest chunk that belongs to "now". Measured on the dev laptop's CPU:

| policy | cameras | inference | chunk | ok on CPU? |
|---|---|---|---|---|
| act_rebot_grasp_keys_rel | 1 | ~260 ms | 30 (1 s) | yes |
| act_rebot_sort_v1 | 3 | ~820 ms | 100 (3.3 s) | yes |
| act_rebot_grasp_keys_abs | 3 | ~1.1 s | 30 (1 s) | **no** ("chunk ran out" in the log) |

## Dry run without the arm

`--fake-hardware --auto-start` uses the MuJoCo stand-in (`teleop/fake_rebot.py`), with
recorded frames from a rebot_sort_v1 episode as the cameras (open loop: the images don't
react to the arm). Its motors sag under gravity, so loosen the arrival and lag checks:

```bash
hf download RoboCrafty/rebot_sort_v1 --repo-type dataset --local-dir /tmp/rebot_sort_v1
$P rollout/rollout.py grasp-rel --fake-hardware --auto-start --arrive-tol-deg 15 --max-lag-deg 40 \
   --fake-images-root /tmp/rebot_sort_v1 --fake-episode 32 --fake-start-frame 72
```

Safety tests: `cd rollout && python3 -m pytest -q test_safety.py`.
