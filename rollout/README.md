# rollout: test policies on the real arm, with safety limits

One script, three strategies. It drives the arm directly through lerobot's reBot follower
(no ROS), so it is the quickest way to see what a policy does on the real arm.

```bash
cd steel_team
P=teleoperation/.venv/bin/python
CAMS="--cam front_wide=/dev/video0 --cam gripper=/dev/video2 --cam high_oblique=/dev/video4"

# 1. full-task policy (ACT or SmolVLA trained on rebot_sort_v1), from the ready pose
$P rollout/rollout.py full $CAMS
$P rollout/rollout.py full $CAMS --policy niru-5/smolvla_rebot_sort_v1_2026-11-15_02-15-27

# 2. grasp-only ACT, absolute: drive slowly (5 s) to a dataset clip's start pose, grasp, stop
$P rollout/rollout.py grasp-abs $CAMS --start-episode 27

# 3. grasp-only ACT, relative: place the arm above the keys by hand, press a, grasp, stop
$P rollout/rollout.py grasp-rel --cam gripper=/dev/video2
```

Use the camera devices the datasets were recorded with: `front_wide`, `gripper` (wrist)
and `high_oblique`, all at 640x480, 30 fps. A policy only opens the cameras it needs.

## Keys (terminal, no Enter)

| key | |
|---|---|
| `a` | start the policy (after the approach / placement) |
| `space` or `s` | stop the policy now and hold the pose |
| `q` | quit: the arm keeps holding, torque stays **on** |
| `h` | grasp-rel only, before start: torque off for hand placement, `h` again locks the pose |

Every stop (key, done, timeout, safety) ends in a hold at the current pose, and every
exit leaves torque on. Support the arm before you switch the power off.

## The three strategies

| mode | default policy | starts from | ends when |
|---|---|---|---|
| `full` | `niru-5/act_rebot_sort_v1` | ready pose (5 s move), then `a` | timeout (40 s) or a key |
| `grasp-abs` | `niru-5/act_rebot_grasp_keys_abs` (checkpoint 2000) | ready pose, then the first state of clip `--start-episode` of `niru-5/rebot_grasp_keys_abs` (5 s move), then `a` | gripped and lifted 5 cm, timeout (10 s) or a key |
| `grasp-rel` | `niru-5/act_rebot_grasp_keys_rel` (final) | wherever you put it (`h` to hand-guide), then `a` | gripped and lifted 5 cm, timeout (10 s) or a key |

- **grasp-abs** prints the clip's TCP position (x, y in the base frame) at the start.
  Put the keys under the gripper there, as in that episode. Clips 27-29 (source
  episodes 32-34) were held out from training; 0-26 were trained on.
- **grasp-rel** grasps from wherever you place the gripper. Match the demos: the gripper
  about 5 cm above the keys, the wrist camera seeing them, and the wrist angle like the
  dataset's handoffs (wrist_flex about 50-70 deg). The policy's joint changes are added
  to the start pose: in a dry run started at wrist_flex 77 deg, it asked for 98 deg, which
  the joint limit clamped.
- "Gripped and lifted" means: the policy commanded the jaw closed for 0.2 s, the jaw
  settled, and the TCP then rose `--lift-m` (5 cm). It doesn't check that the keys are in
  the jaw (they close the jaw fully either way). Look at it.

## Safety limits

Applied to every command, in this order (`safety.py`, defaults in brackets):

1. **Joint soft limits:** the real arm's limits minus 1 deg.
2. **Offset from the start pose** (grasp modes, `--max-offset 30` deg per joint): the
   grasp can't wander off.
3. **Speed** (`--max-speed 45` deg/s per joint).
4. **Workspace** (forward kinematics of the command): TCP site height
   `--min-tcp-z 0.125` m and horizontal reach `--max-reach 0.50` m. A command outside is
   refused and the rollout stops and holds. The `tcp` site is about 14 cm above the
   fingertips; dataset grasps happen at 0.144-0.15 m. Raise the floor for the first runs
   (e.g. 0.14) and lower it once the grasp looks right.
5. **Lag** (`--max-lag-deg 25` for 1 s): the arm not following, e.g. blocked, stops the
   rollout.
6. **Timeout** (`--timeout`).

The driver's own limits stay on as well: `--max-step-deg 8` (lerobot
`max_relative_target`, per command from the measured position) and pos_vel control with a
motor speed cap of `--motor-vel-deg 60` deg/s. The calibration file is required, and the
motors are never re-zeroed.

For a first run, tighten everything: `--max-speed 20 --max-offset 15 --min-tcp-z 0.14`.

## Units

- Arm joints are lerobot degrees, the same as the dataset: every rebot_sort_v1 episode
  starts at this repo's ready pose.
- The gripper is mapped through the opening fraction. This arm reads 161 open / 507
  closed (`teleoperation/config/gripper_limits.json`); the dataset arm read -365 / -5.

## Inference speed

Inference runs in a thread on the newest observation. Each 30 Hz tick executes the action
of the latest chunk that belongs to "now". Measured on the dev laptop's CPU:

| policy | cameras | inference | chunk | ok on CPU? |
|---|---|---|---|---|
| act_rebot_grasp_keys_rel | 1 | ~260 ms | 30 (1 s) | yes |
| act_rebot_sort_v1 | 3 | ~820 ms | 100 (3.3 s) | yes |
| act_rebot_grasp_keys_abs | 3 | ~1.1 s | 30 (1 s) | **no**: chunks run out ("chunk ran out" in the log) |

Use `--device cuda` where there is a GPU, especially for grasp-abs and SmolVLA.

## Logs

`rollout/logs/<time>_<mode>.json` holds the summary, events and arguments.
`rollout/logs/<time>_<mode>.npz` holds per tick: `state`, `policy_action`, `command`,
`tcp`, and the limits that clipped the command.

## Dry run without the arm

`--fake-hardware --auto-start` uses the MuJoCo stand-in from `teleop/fake_rebot.py`, with
recorded frames from a rebot_sort_v1 episode as the cameras (open loop: the images don't
react to the arm). The stand-in's motors sag under gravity, so loosen `--arrive-tol-deg 15
--max-lag-deg 40`.

```bash
$P rollout/rollout.py grasp-rel --fake-hardware --auto-start --arrive-tol-deg 15 \
   --max-lag-deg 40 --fake-images-root <local rebot_sort_v1> --fake-episode 32 --fake-start-frame 72
```

Safety tests: `cd rollout && python3 -m pytest -q test_safety.py`.
