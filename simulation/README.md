# rebot_sim: the real setup in MuJoCo

## Brief

`rebot_sim` is a MuJoCo replica of the team's real reBot B601-DM workspace, built from
measurements and photos of the setup (`reference_photos/`):

- **Robot:** Seeed's reBot B601-DM model with the teleop servos, gripper and IK, clamped
  on its base plate 38 cm from the right wall and flush with the near wall.
- **Workspace:** a 98 × 84 cm wood table (texture taken from the photos) with 37 cm walls:
  cardboard behind and right of the robot, a black board on the left.
- **Bin:** the white foam bin, 25 × 40 × 12 cm, with two compartments. The drop targets
  are `bin_0` (nearer the robot) and `bin_1`.
- **Cameras:** the same three as on the real setup. `cam_corner` is the Logitech C920 at
  60 cm, `cam_far` is the LeRobot camera at 30 cm, and `wrist` is on the gripper.
- **Objects:** a can (13 × 4.5 cm, 15 g) and a hollow paper cup (11 × 9 cm, 8 g). Mesh
  assets can replace them.

**What it's for:** teleop practice and LeRobot data collection in sim (`--scene real`),
scripted policies and tests (`RealSetupEnv`), and handing the model to other tools
(`export`). The scripted pick-and-place puts the can and the cup into both compartments.
The far compartment is at the edge of the arm's reach with the gripper pointing straight down.

**One source of truth:** all measurements live in `rebot_sim/real_setup.json` and the
builder in `rebot_sim/scene.py`. The teleop apps, the env, the tests and the exports all
build from these two files. When the setup changes, edit the JSON, bump its `version`,
run the tests and push. Everyone gets the new model with `git pull`; the package is
installed editable, so no re-install is needed.

![top-down: sim vs. photo](docs/topdown_sim_vs_photo.jpg)
![cam_corner, cam_far, wrist](docs/cameras.jpg)

## Setup

```bash
cd teleoperation
./scripts/setup_assets.sh   # once: Seeed's reBot model
uv sync                     # installs rebot_sim (editable) into the teleop env
```

After `uv sync`, `import rebot_sim` works in that environment from any directory. Without
the sync, the teleop apps still find the package by its path in the repo.

## Use it

**Teleop and recording.** Add `--scene real`, or pass your own setup JSON instead:

```bash
cd teleoperation
uv run sim_teleop.py --input mouse --scene real
uv run quest_ee_teleop.py --vr --scene real        # sim in the headset; --demo without one
uv run sim_teleop.py --input quest --scene real --record \
    --cameras cam_far,cam_corner,wrist --task "put the can in the bin"
uv run sim_teleop.py --input mouse --scene ~/my_setup.json
```

**From Python (tests, scripted policies, data generation):**

```python
from rebot_sim import RealSetupEnv

env = RealSetupEnv()                        # RealSetupEnv(config="my_setup.json", objects=False)
env.reset(randomize=True, seed=0)           # objects at random spots in spawn_region
can = env.object_pos("can")                 # world position of the can's base
env.move_grasp_to(can + [0, 0, 0.25])       # IK move, gripper pointing down (TOP_DOWN)
env.move_grasp_to(can + [0, 0, 0.06]); env.set_gripper(env.GRIPPER_CLOSED)
env.move_grasp_to(env.bin_pos("bin_0") + [0, 0, 0.30]); env.set_gripper(env.GRIPPER_OPEN)
env.in_bin("can", "bin_0")                  # -> True
rgb = env.render("cam_corner")              # 480x640x3 uint8
env.step(q_arm, gripper)                    # or drive the joints yourself (100 Hz ticks)
```

`RealSetupEnv` subclasses the teleop `RebotSim`, so `model`, `data`, `command()`,
`tcp_pose()` and `q_arm` work too. Lower level: `build_real_setup_spec()` returns the
`MjSpec`, and `apply_real_setup(spec)` adds the scene to your own reBot spec.

**CLI** (run from `simulation/`, or anywhere after `uv sync`):

```bash
uv run --project ../teleoperation python -m rebot_sim info      # version, commit, cameras, bins
uv run --project ../teleoperation python -m rebot_sim view
uv run --project ../teleoperation python -m rebot_sim render --out renders
uv run --project ../teleoperation python -m rebot_sim export out/rebot_real_setup.zip
```

`export` writes a standalone `scene.xml` with all its meshes and the texture, as a folder or
a zip, plus `rebot_sim_info.json` (scene version, commit, frame conventions). Use it for tools
outside this repo; it loads with `mujoco.MjModel.from_xml_path`. Re-export after pulling.
An export is a snapshot, so the JSON and the code stay the source of truth.

**Tests:** run after changing the setup:

```bash
cd simulation && uv run --project ../teleoperation tests/test_scene.py
```

They check the measurements (wall, bin and camera heights, robot offset, fields of view),
that the objects rest upright, randomization, a pick-and-place into both bins, camera
renders, the teleop `--scene` flag, and that the export loads standalone.
`examples/pick_place.py` is a template for scripted runs (add `--view` to watch,
`--random --seed N` for random starts).

## Layout

The robot base stays at the world origin, so the IK, teleop and recording code are unchanged.
**+x** points from the robot to the open far edge and **+y** points to the robot's left (the bin side).
The table top is at z = −1.2 cm, the base plate's thickness.

```
                 far edge (open)  84 cm from the near wall
   cam_far ⊗ (36 cm from left, 30 cm high)            ⊗ cam_corner (60 cm high)
 ┌──────────────────────────────────────────────────────┐
 │                                                      │
 │ ┌──────┐                                             │
 │ │bin_1 │ 40 cm                                       │  right wall
 │ │──────│                                             │  (cardboard)
 │ │bin_0 │                                             │
 │ └──────┘ 25 cm                                       │
 │   ↕ 15 cm                     [robot]                │
 └───────────────────────────────────────────────────────┘
  left wall (black)   near wall (cardboard)    ←— 38 cm —→
                    ←——————————— 98 cm ———————————————→
```

All measurements are in **`rebot_sim/real_setup.json`**, in workspace coordinates
(`from_left`, `from_near`, `height` above the table). Edit them there; no code changes are needed.

| Part | Value | Source |
|---|---|---|
| Workspace | 98 × 84 cm | measured |
| Robot (joint-1 axis) | 38 cm from the right wall; plate flush with the near wall (axis 7.5 cm out) | measured |
| Base plate | 19 × 15 × 1.2 cm, black, 2 green clamps | estimated from photo |
| Foam bin | 25 × 40 cm, 15 cm from the near wall, against the left wall | measured |
| Bin height / divider | 12 cm, one divider in the middle → `bin_0`, `bin_1` | measured |
| Bin wall / floor thickness | 2.5 cm / 2 cm | **estimated** |
| `cam_far` | LeRobot camera, far edge, 36 cm from the left, 30 cm high, 100° FOV | measured; aim **estimated** |
| `cam_corner` | Logitech C920 on a gooseneck, far-right corner, 60 cm high, ~75° FOV | measured; aim **estimated** |
| `wrist` | on the gripper, 100° FOV, 8 cm behind and 6 cm above the fingertips | FOV measured; mount spot **estimated** |
| Walls | 37 cm (cardboard near/right, black board left) | measured |
| Can | 13 cm tall, 4.5 cm diameter, 15 g | measured |
| Paper cup | 11 cm tall, 9 cm top diameter (6 cm bottom, estimated), 8 g | measured |
| Table texture | cropped from the top-down photo | `rebot_sim/textures/table_wood.png` |

Named things for scripts and tasks: sites `bin_0` (near compartment), `bin_1` (far
compartment), `can_site` and `cup_site`; cameras `cam_far`, `cam_corner`, `wrist`,
`front` and `overhead_rgb`.

## Objects (placeholders until the real assets arrive)

`objects` in the config lists the pick objects. Three types are built in:

```jsonc
{"name": "can", "type": "can", "from_left": 0.42, "from_near": 0.40,
 "radius": 0.0225, "height": 0.13, "mass": 0.015, "rgba": [0.75, 0.05, 0.05, 1]}
{"name": "cup", "type": "cup", "from_left": 0.70, "from_near": 0.45,       // hollow, open top
 "top_radius": 0.045, "bottom_radius": 0.030, "height": 0.11, "wall": 0.002, "mass": 0.008}
{"name": "coke", "type": "mesh", "file": "assets/coke_can.obj", "scale": 1.0,  // rebot_sim/assets/
 "from_left": 0.42, "from_near": 0.40, "mass": 0.02}
```

Relative paths in a setup JSON resolve against the folder that JSON is in. Mesh objects
collide through their convex hull. A cup mesh would therefore be solid, so
keep the `cup` type for open cups, or split the mesh into convex parts. Every object gets
a free joint and the same contact settings as Seeed's demo objects, which the gripper is
tuned for.

With the tool held straight down, `bin_1` (the far compartment) is at the edge of the
arm's reach at a 30 cm carry height: the IK tilts the tool about 10 cm short of the
centre, and the object still falls in.

## Not modelled yet

- Arm-link collisions: only the gripper palm and fingers collide (that's how Seeed's
  model is set up). The upper arm can pass through the bin walls and the near wall.
- Camera aim: the positions and FOVs are measured, but where each camera points
  (`look_at`) and the wrist mount spot are guesses. Compare `python -m rebot_sim render` output with real
  frames and adjust them. FOVs are read as spec-sheet **diagonal** angles and
  converted to MuJoCo's vertical `fovy` for 4:3 frames (100° → 71°, 75° → 49°);
  give `fovy` directly to override.
- The foam bin's inner steps and inserts, cables, and the clutter beyond the far edge.
