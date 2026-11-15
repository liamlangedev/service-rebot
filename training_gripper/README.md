# training_gripper: a learned grasp inside the classical pick

The classical stack (`ros2_ws`, MoveIt) gets the gripper above the object, but the grasp
itself often fails. This folder tests whether a small policy trained **only on the grasp**
can do that last part: classical motion brings the arm to a handoff pose, the policy
descends, closes and lifts, and control returns to the classical stack once the object is
gripped and lifted.

Only keys for now (`RoboCrafty/rebot_sort_v1` is keys only). Other objects come after the
idea works.

```
classical: detect -> above object -> open -> handoff pose (5 cm above grasp)
                                                   │
               grasp_policy_node  ~/grasp ─────────┘  policy at 30 Hz until
                                                      jaw closed + TCP up 5 cm
                                                   │
classical: hold check -> place in bin  ◄───────────┘
```

## What the data says (`analyze_grasps.py`)

- The gripper action is about -365 open and -5 closed. Each episode has one sustained
  close, at a median of 5.8 s.
- All grasps happen in one patch of the table (shoulder_pan -36 to -53 deg). A policy with
  absolute joint actions can only grip there.
- 2.5 s before the close, the TCP is 5-7 cm above the grasp height. The last approach is
  short: mostly XY alignment and wrist roll.
- After the close, the TCP rises 5 cm in 0.9-1.4 s, then swings to the bin.
- The jaw closes fully on keys (state -5 while holding). A position-based "is something
  held" check can't confirm a key grasp.
- The joint zero and sign match the URDF: every episode starts at motion.yaml's `ready`
  pose to within 0.5 deg. The MuJoCo `tcp` site is about 14 cm above the fingertips
  (z = 0.25 m at `ready`, where the SRDF `gripper_tcp` is at 0.11 m).

## Datasets (`make_dataset.py`)

Each clip runs from `pre` frames before the close until the TCP has risen 5 cm (FK), plus
6 frames. Episodes with fumbled closes, a reopen before the lift, or no lift are dropped:
0, 1, 7, 10 and 13. That leaves 30 episodes. The last 3 (32, 33, 34) are held out for
eval loss.

| | `niru-5/rebot_grasp_keys_abs` (A) | `niru-5/rebot_grasp_keys_rel` (B) |
|---|---|---|
| Clips | 1 per grasp (pre = 75 frames) | 4 per grasp (pre = 75, 60, 45, 30): handoff-timing augmentation |
| Cameras | front_wide, gripper, high_oblique | gripper (wrist) only |
| State / action | absolute lerobot degrees | arm joints minus the clip's first state (`anchor_state`); gripper absolute |
| Question it answers | does clipping alone give a working grip, in the training patch? | does a local grip transfer to new key positions? |

Both datasets are private.

```bash
hf download RoboCrafty/rebot_sort_v1 --repo-type dataset --local-dir <src>
teleoperation/.venv/bin/python training_gripper/make_dataset.py --src <src> --out <dir> --plan-only
teleoperation/.venv/bin/python training_gripper/make_dataset.py --src <src> --out <dir> --push
```

## Training (`train.sh`)

Small ACT: chunk 30 (1 s), batch 64, 5k steps, lr 3e-5, eval loss on the held-out clips
every 500 steps. Models are private.

```bash
EVAL_SPLIT=<from meta/grasp_clips.json> VARIANT=rel ./training_gripper/train.sh
EVAL_SPLIT=<...>                        VARIANT=abs ./training_gripper/train.sh
```

Runs are logged in [`training/RUNS.md`](../training/RUNS.md).

## ROS node (`ros2_ws/src/rebot_trash_sorting_agent`)

- `grasp_policy_node`: `~/grasp` (`std_srvs/Trigger`, blocking), `~/cancel`, and
  `~/status` (JSON). It runs the policy in chunks of 10 actions, each sent as one
  `FollowJointTrajectory` goal (the previous goal is cancelled first). It stops when the
  jaw has been commanded closed and has settled, and the TCP (TF `base_link` ->
  `gripper_tcp`) has risen `lift_m` (5 cm). It then holds the arm where it is and does
  **not** reopen the gripper.
  - It fails on timeout (8 s), cancel or error, and holds the arm in those cases too.
  - Arm joints are clamped to within 45 deg of the handoff pose.
- `grasp_policy/`: units, relative anchoring, done detector and runner. These are pure
  Python with unit tests (`test/test_grasp_policy.py`).
- It runs under the teleop venv's Python (lerobot) with ROS sourced:
  `ros2 launch rebot_trash_sorting_agent grasp_policy.launch.py`. Parameters are in
  `config/grasp_policy.yaml`.
- Classical side: set `learned_grasp.enabled: true` in `config/motion.yaml`.
  `pick_and_place` then goes pre-grasp -> open -> handoff (grasp + 5 cm) -> `~/grasp`,
  then runs its hold check and the place. A failed attempt retreats up, opens, and tries
  the next candidate.

### Check on the hardware before the first run

1. **Gripper map.** `gripper_ros_*` / `gripper_data_*` map finger_left metres to the
   dataset's gripper degrees through the opening fraction. The dataset arm read -365 open
   / -5 closed. This repo's arm reads -370 / 0 in lerobot degrees
   (`teleoperation/config/gripper_limits.json`, re-measured 2026-11-15; the earlier
   161 / 507 was stale). Check it against the arm before trusting the gripper.
2. **Wrist camera.** The dataset's `gripper` camera is 640x480. ROS `/wrist_cam` is
   1920x1080, centre-cropped to 4:3 and resized. Compare a frame side by side with a
   dataset frame: same mount, same field of view?
3. **Arm controller.** The action name is `/rebotarm_controller/follow_joint_trajectory`
   in the MuJoCo bridge. Set `arm_action` if the hardware controller is called something
   else.
4. **First motion with `max_offset_deg` small** (e.g. 15) and a hand on the e-stop.

## Test protocol

About 5 trials per cell; record success (gripped and lifted, keys still in the jaw at
the bin).

| Keys at | classical only | full ACT (`act_rebot_sort_v1`) | A (abs) | B (rel) |
|---|---|---|---|---|
| training patch (~(0.30, -0.26)) | | | | |
| +5 cm | | | | |
| +10 cm | | | | |
| +15 cm | | | | |
| rotated 45 deg | | | | |
| rotated 90 deg | | | | |

The full-task ACT baseline needs no training. Launch the node with
`policy_path:=niru-5/act_rebot_sort_v1 mode:=absolute` and all three cameras.

## Offline check

`smoke_runner.py` feeds recorded frames to `PolicyRunner` (the node's inference path)
from a handoff frame and compares predicted with recorded actions. It catches unit,
camera and mode mismatches without a robot.
