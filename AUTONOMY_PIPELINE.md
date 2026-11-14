# reBot B601-DM: prompt → autonomous task (final plan)

Updated 2026-11-14 18:15. Judging Round 1 is **Mon 16 Nov 13:00** (4 min pitch + 2 min Q&A,
scored on technical quality, innovation, real-world value, completeness). About 43 h left.

**Hardware:** reBot B601-DM, **three RGB cameras, no depth: two fixed (top + side) and one
wrist**, an Ubuntu laptop for the arm, and the Mac for development.

> **Status (14 Nov, 22:15):** implemented in `teleoperation/autonomy/` on branch `autonomy-pipeline`.
> Runs end-to-end in MuJoCo (prompt → graph → pick / place / sort / stack, 16 tests). How to run it and
> the real-arm bring-up steps: `teleoperation/autonomy/README.md`. Not yet run on the real arm.

## 1. Decisions

| Decision | Choice | Why |
|---|---|---|
| Overall approach | **LLM planner + scripted skills**, no training required | End-to-end VLAs reach about 30–40 % with 50 demos on cheap arms ([source](https://justintiensmith.github.io/vla-research/2026/04/10/are-vlas-overhyped-first-results-on-a-real-robot.html)) |
| 3D without depth | **Triangulation** from the two fixed cameras (gives height too), table plane as fallback, + **wrist-camera alignment** before each grasp | About 4 mm from the fixed cameras in sim; the wrist camera corrects the rest to < 1 mm |
| GaP (graph-as-policy) | **Borrow the idea, not the code**: the planner compiles a validated skill graph, code executes it | GaP needs an RTX 4090 + depth cameras and only has Franka / UR connectors |
| Codebase | **Our own stack**: `teleop/ik.py` + `RealRebot` + new `autonomy/` package | Agent Claw (Seeed) needs a depth camera and the RS arm, so we'd be rewriting most of it. We only borrow its ideas |
| Reference design | Google [robotics-pointing-sample](https://github.com/google-gemini/robotics-pointing-sample): SO-101, no depth, homography, Gemini pointing | Same setup as ours |
| Planner / verifier | **Claude** (tool use) as the orchestrator; **Gemini Robotics-ER 2** for pointing and success checks (Google Cloud sandbox) | Either can do both. Keep one as backup |
| Detector | Gemini ER pointing (open-vocab, no setup). Fallback: YOLOE / OWLv2 locally | Pointing returns a pixel directly |
| Learned policy | **Optional**, only for one task scripting can't do (ACT or SmolVLA, trained on the cloud GPU) | Not on the critical path |
| Demo | **T3 "Waste sorter"**: *"sort the cans, PET bottles and glass into the right bins"* | Official track example, flat-table objects, clear real-world value |

## 2. Architecture

```
  User: "sort the cans and bottles into the right bins"   (text, optional Whisper voice)
                     │
  ┌──────────────────▼───────────────────┐
  │ PLANNER  (Claude tool use)           │  sees: table-camera image + object list
  │ prompt → steps → one tool call each  │  per step: call skill → read result →
  │ re-plans on failure, max 2 retries   │  next step / retry / ask user
  └──────────────────┬───────────────────┘   LLM is called per STEP, never per control tick
                     │
  ┌──────────────────▼─────────────────────────────────────────────────┐
  │ SKILL API (deterministic Python, every motion goes through safety)  │
  │  look() → list of {name, pixel, table_xy}                           │
  │  pick(object)  place(zone)  pick_and_place(object, zone)  home()    │
  │  open_gripper()  close_gripper()  verify(question)                  │
  │  [optional] run_policy(task)   ← learned ACT/SmolVLA skill          │
  └───┬──────────────────┬──────────────────────┬───────────────────────┘
      │                  │                      │
  PERCEPTION         MOTION                  VERIFICATION
  table cam →        IK (teleop/ik.py,       1. gripper width after close
  detector →         <1 mm in sim) →            (fully closed = missed)
  homography →       min-jerk trajectory     2. re-look with the table cam
  table (x, y)       → safety → arm          3. Gemini ER / Claude:
  wrist cam →                                   "is the can in the blue bin?"
  centre object
      │                  │
      └────────┬─────────┘
       SAFETY: workspace box, joint soft limits (follower.json),
       speed cap, max_relative_target 5°, E-stop key
               │
       RealRebot (LeRobot rebot_b601_follower, motor_family=dm)
               │                              │
         reBot B601-DM                 MuJoCo mirror (sim_teleop)
```

### The pick skill, step by step

1. **Coarse (table camera).** The detector gives the object's pixel. Use the **bottom-centre**
   of the box (the point touching the table) so tall objects don't suffer from parallax. The
   homography maps that pixel to table (x, y).
2. **Hover.** IK moves the gripper about 12 cm above (x, y), pointing down, gripper open.
3. **Fine (wrist camera).** Detect the object in the wrist image and nudge the arm in x/y until
   it sits at the calibrated "aligned" pixel (usually 2–4 iterations, ±3 px). This step fixes
   calibration error.
4. **Descend** to `table_z + grasp_height[class]` (e.g. can 6 cm, bottle 8 cm). Rotate
   wrist_roll to the object's short axis if the box is elongated.
5. **Close**, then check gripper width. Fully closed means a miss: lift, `look()` again, retry
   (max 2).
6. **Lift** to the hover height. `place(zone)` = hover over the bin's fixed (x, y), open,
   return home.

## 3. Calibration (do once, then never move the cameras or table)

| What | How | Time |
|---|---|---|
| Arm zero | `lerobot-calibrate --robot.type=rebot_b601_follower --robot.motor_family=dm --robot.id=follower` in the sit-down pose, gripper closed | 10 min |
| Sim ↔ real check | Put the arm in 3–4 poses; the MuJoCo mirror must match (signs, zero) | 15 min |
| Table homography | Touch the table with the gripper tip at 6–9 spread-out points; record FK (x, y) + pixel; `cv2.findHomography` | 15 min |
| Table height | FK z of the gripper tip touching the table | 1 min |
| Wrist "aligned" pixel | Closed gripper centred over an object by hand → record where the object appears in the wrist image | 5 min |
| Bin positions | Touch each bin centre, save its (x, y) | 5 min |

Save everything in `autonomy/calibration.json`.

## 4. Code layout (new, beside `teleop/`)

```
steel_team/teleoperation/
  teleop/                     existing: ik.py, real_robot.py, rebot_model.py, lerobot_mapping.py
  autonomy/
    arm.py                    one interface, two backends: SimArm (MuJoCo) / RealArm (RealRebot)
    safety.py                 workspace box, limits, speed cap, E-stop
    calibrate.py              homography + table z + wrist pixel + bins → calibration.json
    perception.py             detect(image, name) → pixel; Gemini pointing or YOLOE/OWLv2
    skills.py                 look, pick, place, pick_and_place, home, verify
    planner.py                Claude tool-use loop (+ Gemini ER fallback), logs a trace
    app.py                    CLI / small web UI: prompt in, live cameras + trace out
```

Everything runs against **SimArm first** (the MuJoCo sim already has `overhead_rgb` and `wrist`
cameras), then the same code switches to `--robot real`.

## 5. Timeline

| When | Main track (critical) | Side track |
|---|---|---|
| **Sat 18–22** | Real-arm bring-up: calibrate, sim↔real check, first slow moves (TODO.md "Needs the real arm"). Mount both cameras for good | Write `autonomy/` in sim: arm, safety, skills with the sim's cameras |
| **Sat 22–Sun 02** | Calibration script on the real arm; `pick` with fixed coordinates (no vision) | Perception: Gemini pointing + homography in sim |
| **Sun 02–08** | Sleep in shifts | (optional) Quest-record demos for a learned skill, train on the cloud |
| **Sun 08–13** | Real pick with vision + wrist alignment. **Milestone: "pick up the can" ≥ 8/10** | Planner (Claude tools) working in sim |
| **Sun 13–19** | Planner on the real arm: multi-object sorting into bins, verify + retry | Web UI showing camera + trace |
| **Sun 19–Mon 08** | Freeze scene and lighting. 30 end-to-end trials, fix the top failure, measure success rate. **Record a backup video** | Pitch slides |
| **Mon 08–13** | Rehearse: live demo + backup video + numbers | |

**Go/no-go checkpoints**
- **Sun 08:00:** the real arm must do a fixed-coordinate pick. If not, demo in **MuJoCo** with
  the same planner + skills, and show the real arm doing teleop.
- **Sun 13:00:** vision pick ≥ 8/10. If not, narrow the scope to one object type and bigger bins.
- The learned policy joins only if it reaches **≥ 70 %** in 10 trials by Sun 19:00.

## 6. Risks

1. **The real arm has never run.** Calibration writes the motor zero. **The arm drops when torque
   turns off on exit**, so someone holds it. No hot-plugging XT30. On Linux:
   `sudo apt remove brltty`, `chmod 666 /dev/ttyACM*`.
2. **Calibration drift.** A bumped camera or table means every grasp misses. Tape everything
   down and re-check the homography each morning.
3. **Gripper force.** The DM default `gripper_torque_ratio` is 0.07. Tune it on day 1 so it
   holds a can.
4. **Tall objects and parallax.** Use the bottom-centre of the box; wrist alignment fixes the rest.
5. **LLM latency (2–15 s per turn).** Call it per step only. Common commands can skip the LLM
   (template parsing).
6. **Lighting changes the detector.** Fix the lighting at the demo spot; test there.

## 7. Pitch story (4 min)

1. Problem: waste sorting is dull, dirty work, and robots need retraining for every new item.
2. Our answer: **no task-specific training.** Language model + vision + geometry = say what you
   want, and it does it.
3. Live demo: one spoken or typed prompt sorts 3–4 items, with the plan + check trace on screen.
4. Numbers: success rate over N trials, time per item, and that a new object needs zero
   retraining (just say its name).
5. Next step: add a learned skill for hard grasps (the Quest teleop + LeRobot recording is
   already built).

## Links

- Gemini pointing → SO-101 (no depth): https://github.com/google-gemini/robotics-pointing-sample
- Gemini Robotics-ER docs: https://aistudio.google.com/docs/robotics-overview
- LeRobot reBot docs: https://huggingface.co/docs/lerobot/rebot_b601
- Seeed DM getting started: https://wiki.seeedstudio.com/rebot_b601_dm_getting_started/
- Agent Claw (ideas: skill API, traces, retries, safety): https://github.com/TheMoonAstronaut/wrc
- Seeed kinematics/control: https://github.com/Seeed-Projects/reBotArm_control_py
- Google Cloud sandbox: email chalemba@google.com with team name + number of hackers
