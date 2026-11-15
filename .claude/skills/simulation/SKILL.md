---
name: simulation
description: Work with the MuJoCo replica of the real reBot B601 workspace (simulation/rebot_sim): run or view it, teleop or record in it, script tests and policies with RealSetupEnv, change the measured setup or objects, recalibrate cameras, run capture sessions on the real hardware, or build Gaussian-splat datasets. Use for any task touching simulation/, `--scene real`, or the sim's cameras, gripper or geometry.
---

# The reBot simulation (simulation/rebot_sim)

A MuJoCo model of the team's real cell, calibrated against the real cameras and the arm.
Docs: `simulation/README.md` (overview, layout, calibration) and `simulation/capture/README.md`
(real-hardware sessions). Run from `simulation/` with the teleop environment:
`uv run --project ../teleoperation python …`. Set `MUJOCO_GL=egl` when headless.

## One source of truth

- `simulation/rebot_sim/real_setup.json`: every measurement (workspace coords: `from_left`,
  `from_near`, `height` above the table), the cameras, the bin, the objects and the ChArUco
  board. It has a `version`; bump it when the setup changes.
- `simulation/rebot_sim/scene.py`: builds the scene on top of the teleop robot model.
- `teleoperation/teleop/rebot_model.py`: the robot itself, with servos, IK sites and the soft
  gripper (default).
- Everything else builds from these files: teleop `--scene real`, `RealSetupEnv`, the tests,
  `export`, and the ROS MuJoCo bridge (`ros2_ws/.../mujoco_sim_node.py`). Never hard-code
  geometry elsewhere.

## Conventions that matter

- **World frame** = robot `base_link`: origin on joint 1 at table height, **table top z = 0**,
  +x towards the open far edge, +y towards the bin. The black base plate (20 × 14 × 1.4 cm) is
  part of the robot mesh. Don't add another.
- **Gripper:** Seeed's soft (Fin-Ray) fingers. Their tips reach 2.86 cm past the hard ones;
  at the ready pose `[0, -1.51, -1.30, 1.36, 0, 0]` the fingertips are 11 cm above the table.
  Sites: `fingertip` (= ROS `gripper_tcp`), `grasp` (pinch point, 2 cm behind the tip),
  `tcp` (palm).
- **Bin:** 25 × 40 × 12 cm, two compartments `bin_0` (near) and `bin_1` (far). Its robot-side
  edge is at y = 0.30 (corrected from the arm's table homography).
- **Cameras:** `cam_corner` (C920 on a gooseneck, fovy 43.3°), `cam_far` (LeRobot camera,
  fovy 66°), `wrist` (on the gripper, fovy 63.6°, **1920×1080**). The fovy values are vertical,
  for 16:9 frames. `front` and `overhead_rgb` are extra sim-only views.

## Common commands

```bash
python -m rebot_sim info | view | render --out renders | export out.zip
tests/test_scene.py                          # run after any change to the setup or code
examples/pick_place.py --obj can --bin bin_0 --view
cd ../teleoperation && uv run sim_teleop.py --input mouse --scene real
uv run quest_ee_teleop.py --vr --scene real  # Quest; --demo without a headset
uv run sim_teleop.py --input quest --scene real --record --cameras cam_corner,wrist
```

From Python: `from rebot_sim import RealSetupEnv`. It has `reset(randomize=True, seed=…)`,
`object_pos`, `move_grasp_to(pos, TOP_DOWN)`, `set_gripper`, `in_bin`,
`render(cam)` (at the camera's real resolution by default), `step(q_arm, gripper)` and
`hide_markers()`.

## Changing the setup

- **New measurements:** edit `real_setup.json`, bump `version`, run the tests, regenerate
  `docs/` images with `tools/compare_cameras.py`.
- **New objects:** add an `objects` entry: `can`, `roll` (cylinder lying along x), `cup`
  (hollow) or `mesh`. Relative paths
  resolve against the JSON's folder. Mesh collisions use the convex hull, so open containers
  need the `cup` type.
- **Camera moved:** with the board, run a capture session (below) with `--write`. Without it,
  `tools/calibrate_cameras.py` fits landmarks plus the arm's table homography, and
  `tools/fit_wrist_camera.py` fits the gripper silhouette. Then update the ROS sim homography
  with `ros2_ws/src/rebot_trash_sorting_agent/scripts/sim_calibrate.py`.

## Real hardware (simulation/capture)

1. `python -m capture.device_ui`: assign camera roles and the arm port, and calibrate lenses
   with the ChArUco board (print it with `python -m rebot_sim.charuco board.pdf`).
2. `python -m capture.capture_session --name s1 --write`: the arm holds poses, all cameras are
   captured, real-vs-sim comparisons are written, cameras are calibrated from the board, and it
   pauses 3 min for the phone video.
3. `python -m capture.prepare_splat_dataset s1 --media … --repo-id …`: uploads an HF dataset.
   It prints an `hf jobs run … nerfstudio … train_splat.sh` command for Gaussian-splat training.
   Plain phone videos work too (`--standalone`, plus `--object/--pose/--length/--diameter`
   for one object).

## Scanned objects (Gaussian splats) in the sim

- `tools/crop_object_splat.py splats/<x>/splat.ply --object …/object.json --out …`: cuts the
  object out of its trained splat, scales it to metres from the measured length, base at the
  origin, z up. Check the `.png` it writes.
- `tools/splat_in_sim.py [--video]`: adds the objects with physics proxies (`can`/`roll`) to a
  copy of the setup and renders each camera with the splats composited in
  (`rebot_sim/splat_render.py`: CPU torch rasteriser, depth-tested against MuJoCo, proxies
  hidden in geom group 3). Seconds per frame on CPU: fine for stills, slow for video.
- Transparent bottles reconstruct poorly (refraction makes ghost shells); textured, opaque
  objects work best. Splats live in `simulation/splats/` (gitignored) and on the Hub
  (`niru-5/rebot_splat_<name>_splat`).

Every tool has `--fake`, which runs against a simulated arm and cameras, so test there before
touching hardware. The real arm keeps torque on while holding; warn the user to support it
before releasing.

## Pitfalls

- MuJoCo caches assets by file name: generated textures are named by content hash, so keep it that way.
- An OpenGL context belongs to its thread: render each env from one thread (see `SimCameraHub`).
- OpenCV 4.13's `CharucoBoard.generateImage` fails at most sizes, so `charuco.py` draws the board itself.
- The ROS soft-gripper collision mesh must not be used in MuJoCo: its hull fills the jaw.
