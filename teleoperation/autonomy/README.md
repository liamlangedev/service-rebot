# Prompt → robot: `autonomy/`

Type a sentence, and the reBot B601-DM does it: *"sort the cans into the yellow bin and the
bottles into the blue bin"*. There is no task-specific training. A language model **plans once**,
deterministic code **executes and checks** each step, and the model is called again only if
something unexpected fails.

```
 "put everything in the place zone"
        │
        ▼
 PLANNER  rules (instant, offline) ─or─ Claude (anything else)        ← sees the object list + top image
        │  compiles the prompt into a TASK GRAPH (typed JSON, validated before anything moves)
        ▼
 EXECUTOR walks the graph:  select_next → pick($current) → place(zone) → back to select_next …
        │  each skill returns ok / a failure code; edges branch on it; "replan" asks Claude again
        ▼
 SKILLS   look · select_next · pick · place · check · home · say · run_policy (learned, optional)
        │
   ┌────┴──────────────┬───────────────────────────┐
 PERCEPTION          MOTION                      SAFETY (every trajectory, before sending)
 2 fixed cameras  →  IK (MuJoCo model) →         joint limits (follower.json), workspace box,
 triangulate 3D      min-jerk / straight lines   fingertips never below the table,
 wrist camera     →  tilted grasps for far       speed cap, tracking-error abort, Ctrl+C E-stop
 re-centres (mm)     objects                     (holds pose, no torque-off)
        │                  │
        └──── SimArm (MuJoCo physics) ─or─ RealArm (LeRobot rebot_b601_follower) ────┘
```

This is the **graph-as-policy** idea from [GaP](https://github.com/graph-robots/graph-as-policy)
(CoRL 2026), cut down to what fits our arm, our cameras and 40 hours. See "Why not GaP itself" below.

## Quick start (simulation, no hardware, no API key)

```bash
cd teleoperation
./scripts/setup_assets.sh                 # once: fetches the reBot model
uv sync --extra autonomy                  # anthropic, opencv-headless, pytest
uv run python -m autonomy.app "put the red cube in the place zone"
uv run python -m autonomy.app "put everything in the place zone"
uv run python -m autonomy.app "put the red cube on the blue block"
uv run python -m autonomy.app             # interactive: type prompts one after another
uv run pytest tests -q                    # 15 tests, about 20 s
```

To watch the arm, add `--viewer`. On macOS, the MuJoCo viewer needs `mjpython`:
`uv run mjpython -m autonomy.app "…" --viewer`.

Every run saves `runs/<timestamp>/run.json` (prompt, graph, every skill call with timing and
result) and the final camera images. These are useful for the pitch ("N trials, X % success, Y s
per object").

### Which prompts need Claude?

| Prompt shape | Planner | Latency |
|---|---|---|
| `put / move / place X in / on / into Y` | rules | ~0 s |
| `sort / put all / everything X into Y [and Z into W …]` | rules | ~0 s |
| `pick up X` | rules | ~0 s |
| anything else: *"tidy up, but leave the cup"*, *"make room next to the box"*, *"which one is the can?"* | Claude (`claude-opus-5-5`) | a few seconds per plan |

`--planner auto` (the default) tries the rules first and only calls Claude when they don't parse the
sentence. Claude needs `ANTHROPIC_API_KEY`. Use `--effort low` for faster plans, and `--plan-only` to
print the graph without moving.

### Detectors (`--detector`)

| Name | What it is | Use when |
|---|---|---|
| `color` (default) | HSV colour blobs with masks, which give the grasp angle | Demo with coloured objects. Offline and instant |
| `claude` | Claude vision, open vocabulary ("crushed can", "PET bottle") | Real waste items. Needs `ANTHROPIC_API_KEY` |
| `gemini` | Gemini Robotics-ER pointing (`GEMINI_API_KEY`, `GEMINI_ER_MODEL`) | Open vocabulary, specialised for pointing. Not tested yet |
| `oracle` | Ground truth from MuJoCo | Sim only: separates motion bugs from vision bugs |

## How the 3 cameras are used

| Camera | Role | Job |
|---|---|---|
| top (fixed) | `scene` | Sees the whole table. Gives the object list and the image the planner sees |
| side (fixed) | `scene` | Second view: **triangulation gives x, y and height** with no depth camera |
| wrist | `wrist` | At the hover pose, re-centres over the object (the "wrist camera: corrected by N mm" lines) and refines the grasp angle |

In sim, `overhead_rgb + front` triangulate objects to within about 4 mm, and the wrist camera
brings that to under 1 mm. With only one fixed camera it still works: it intersects the camera ray
with the table plane at an assumed height, and the wrist camera fixes the rest.

**Placement:** mount the top camera 70–90 cm above the table, looking down. Put the side camera
30–45° off the table plane from the front or side. Both must see the whole work area, and the
arm's *observe pose* (folded behind the base) must stay out of their view. Tape everything down;
moving a camera after calibration breaks every grasp.

## Real arm bring-up (in order)

The real arm has **never run** this code. Go slowly, keep one person on the power switch, and
support the arm when the program exits, because LeRobot turns torque off.

1. Arm basics from `teleoperation/README.md`: `lerobot-calibrate`, then the sim↔real joint check
   with `sim_teleop.py --robot real`.
2. `cp autonomy/config/real.example.json autonomy/config/real.json`, then set the port and the
   camera `device` numbers. `uv run python -m autonomy.calibrate list-cameras` saves a snapshot
   per device.
3. Calibrate (writes `autonomy/config/calibration.json`):
   ```bash
   uv run python -m autonomy.calibrate make-sheet                 # print aruco_sheet.png at 100 %
   uv run python -m autonomy.calibrate intrinsics --camera top --board 9x6 --square 0.025
   uv run python -m autonomy.calibrate intrinsics --camera side --board 9x6 --square 0.025
   uv run python -m autonomy.calibrate intrinsics --camera wrist --board 9x6 --square 0.025
   uv run python -m autonomy.calibrate markers     # jog the fingertips onto each marker (keyboard)
   uv run python -m autonomy.calibrate extrinsics  # fixed cameras from the markers
   uv run python -m autonomy.calibrate wrist       # wrist-camera mount from 5 hover poses
   uv run python -m autonomy.calibrate check       # reprojection error + overlay images
   ```
   Copy the printed `table_z` into `real.json → world.table_z`, then measure the bin centres
   (jog onto them) and put them under `zones`.
4. Dry run: `uv run python -m autonomy.app --config autonomy/config/real.json --plan-only "…"`.
5. First moves: `--config autonomy/config/real.json`. It asks before each graph. Keep
   `safety.max_joint_vel` at 0.6 rad/s until pick works 8 times out of 10.
6. Tune: the gripper force (`gripper_torque_ratio` in LeRobot) so it holds a can, `grasp.hover`,
   and per-object grasp height.

## Learned skills: the "latest solutions" for this arm

Seeed documents ACT, **SmolVLA**, **π0 / π0.5** and **GR00T N1.7** for the B601-DM through
LeRobot ([Seeed policy guide](https://wiki.seeedstudio.com/robotics/hands_on_algorithm_switching/),
[GR00T on reBot](https://wiki.seeedstudio.com/fine_tune_gr00t_n1.7_for_rebot_arm_and_deploy_on_robotics_j601/),
[LeRobot reBot docs](https://huggingface.co/docs/lerobot/rebot_b601)). All of them need
**demonstrations per task** (our Quest teleop + LeRobot recording already produce those) and a GPU
to fine-tune. They do not follow arbitrary new prompts on a new arm out of the box.

So they are **one skill in the graph**, not the whole system: `run_policy(text=…)` hands control
to a trained policy for the one motion that scripting can't do (for example, pour or open a lid),
the same pattern as GaP's `steered_policy` example. To plug one in, pass
`SkillContext(policies={"open the lid": runner})`, where `runner(arm, rig, text) -> bool` runs the
LeRobot policy loop.

## Why not GaP itself

GaP's concept is exactly what we need, and this package copies it: language → validated skill
graph → deterministic execution → re-plan on failure. Its code doesn't fit our hardware this
weekend ([GaP README](https://github.com/graph-robots/graph-as-policy),
[connectors doc](https://github.com/graph-robots/graph-as-policy/blob/main/docs/source/real-robots/connectors.md)):

- It needs **one RTX 4090 (≥ 24 GB, Linux)**, plus SAM3 / Grounding DINO / cuRobo weights.
- Real-robot connectors exist **only for Franka (full motion) and UR + ZED (perception only)**.
  A reBot connector would mean writing its msgpack bridge, URDF kinematics and RGB-D camera
  plumbing first.
- Its skills assume **depth cameras**. On real robots its checkpoints (postconditions) are skipped,
  and the release is a beta.

The door stays open: `arm.py` and `cameras.py` already provide what a GaP connector has to expose
(joint and Cartesian moves, IK, gripper, camera images with poses). A reBot connector for GaP
would be a thin adapter over them, not a rewrite.

## Files

| File | What it does |
|---|---|
| `app.py` | CLI: prompt → plan → confirm (real) → execute → re-plan → save the trace |
| `planner.py` | `RulePlanner`, `ClaudePlanner` (structured JSON graph, validation-fix loop, re-plan), `AutoPlanner` |
| `graph.py` | Graph JSON schema, `validate()`, `execute()` with loop and step limits |
| `skills.py` | The skills, grasp planning (tilts for far objects), wrist visual servoing, grasp check by finger opening |
| `world.py` | Multi-camera fusion (triangulation / table plane), object ids, zones, free-spot search |
| `perception.py` | Detectors: colour, Claude, Gemini ER, sim oracle |
| `cameras.py` | `SimCameraRig` (MuJoCo) and `RealCameraRig` (OpenCV + calibration.json, wrist pose from FK) |
| `arm.py` | `SimArm` / `RealArm`, IK, min-jerk and straight-line motion |
| `safety.py` | Limits, workspace, table floor, speed, E-stop |
| `calibrate.py` | Camera discovery, ArUco sheet, intrinsics, marker touch-points, extrinsics, wrist hand-eye, check |
| `config/` | `sim.json`, `real.example.json` |
| `../tests/test_autonomy.py` | Geometry, perception, validation, planners (with a fake Claude), 3 end-to-end sim tasks, calibration solvers |

## Status: what is tested and what is not

- **Tested in sim:** perception on 3 cameras, pick and place, sort-all loop, stacking, graph
  validation, the Claude planner's request shape and fix loop (against a fake client), and the
  calibration maths.
- **Not tested:** anything on the real arm or real cameras; live Claude and Gemini calls (no API
  keys on the dev machine); `calibrate.py` on hardware.
- **Known limits:** no collision checking against objects (only table, limits and workspace).
  The colour detector only knows colours. The default wrist-camera mount comes from the sim model
  until `calibrate wrist` runs.
