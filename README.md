# steel_team: reBot B601 pick-and-place

Leukerbad hackathon project. A Seeed Studio **reBot Arm B601-DM** sorts objects (cans, paper
cups, keys) into a foam bin. We teleoperate it with a Meta Quest, record LeRobot datasets, train
policies on Hugging Face Jobs, and run a VLM-driven ROS 2 agent. A calibrated MuJoCo replica of
the real cell sits underneath all of it.

```
              ┌────────────────────────── simulation/ (MuJoCo replica of the cell) ─────────────────────────┐
              │  calibrated cameras · soft gripper · measured table, walls, bin · capture + splat tools      │
              └───────▲──────────────────────────────▲──────────────────────────────────▲──────────────────┘
                      │ --scene real                   │ RealSetupEnv                        │ mujoco_sim_node
 Quest / mouse ──► teleoperation/ ──► LeRobot datasets ──► training/ (ACT, SmolVLA on HF Jobs)  ros2_ws/ (agent)
                      │                                                                               │
                      └──────────────────────────── real reBot arm + 3 cameras ◄──────────────────────┘
```

## Repository

| Folder | What it is | Start here |
|---|---|---|
| [`teleoperation/`](teleoperation/README.md) | Quest (WebXR, OculusReader) and mouse teleop of the arm, in MuJoCo and on the real arm. Records LeRobot datasets in the real arm's format. | `uv run quest_ee_teleop.py --scene real` |
| [`simulation/`](simulation/README.md) | `rebot_sim`: the measured, camera-calibrated MuJoCo cell, with the `RealSetupEnv` scripting API, tests, export, real-hardware capture sessions (ChArUco calibration) and Gaussian-splat datasets. | `python -m rebot_sim view` |
| [`training/`](training/README.md) | ACT and SmolVLA trained with lerobot on HF Jobs; [`RUNS.md`](training/RUNS.md) logs every run. | `./training/act/train.sh` |
| [`ros2_ws/`](ros2_ws/README.md) | ROS 2 workspace: arm bringup and MoveIt (`rebot_trash_sorting`), and the VLM pick-and-place agent with dashboard and MuJoCo bridge (`rebot_trash_sorting_agent`). | `ros2 launch rebot_trash_sorting_agent sorting.launch.py use_mujoco:=true` |
| `follower.json` | LeRobot calibration of the real follower arm (joint ranges). Real-arm tools refuse to connect without it. | |

## Quick start

```bash
# Teleop + simulation environment (MuJoCo, lerobot, Quest input)
cd teleoperation && ./scripts/setup_assets.sh && uv sync --extra lerobot

# Drive the arm in the simulated cell (mouse; --input quest for the headset)
uv run sim_teleop.py --input mouse --scene real

# Quest with the sim inside the headset; add --real-robot for the real arm
uv run quest_ee_teleop.py --vr --scene real

# Record a sim dataset with the real cameras' names and resolutions
uv run sim_teleop.py --input quest --scene real --record --cameras cam_corner,wrist --task "put the can in the bin"

# Check the simulation
cd ../simulation && uv run --project ../teleoperation tests/test_scene.py
```

Secrets: copy `.env.example` to `.env` and set `HF_TOKEN` (`.env` is gitignored). The ROS agent
reads `GEMINI_API_KEY` from `ros2_ws/.env`.

## The real cell (as modelled)

- **Arm:** reBot B601-DM with Seeed's **soft (Fin-Ray) gripper**, 38 cm from the right wall,
  base plate flush with the near wall. Robot frame = `base_link`, table top at z = 0.
- **Workspace:** 98 × 84 cm wood table, 37 cm cardboard and black walls, open far edge.
- **Bin:** white foam, 25 × 40 × 12 cm, two compartments (`bin_0` near, `bin_1` far).
- **Cameras:**
  - Logitech C920 on a gooseneck (`cam_corner`, the ROS table camera, calibrated to the arm by
    a table homography);
  - a LeRobot camera on the far edge (`cam_far`);
  - a wrist camera on the gripper (1920×1080).

Details, measurements and how they were calibrated: [`simulation/README.md`](simulation/README.md).

## Policies

Trained on [RoboCrafty/rebot_sort_v1](https://huggingface.co/datasets/RoboCrafty/rebot_sort_v1)
(35 episodes, 30 fps, 3 cameras):

- [ACT](https://huggingface.co/niru-5/act_rebot_sort_v1) (from scratch);
- [SmolVLA](https://huggingface.co/niru-5/smolvla_rebot_sort_v1_2026-11-15_02-15-27)
  (fine-tuned `smolvla_base`).

Results and suggested checkpoints are in [`training/RUNS.md`](training/RUNS.md). Run policies at
30 Hz.

## Working with Claude Code

- [`CLAUDE.md`](CLAUDE.md): repo rules. Feature work goes in worktrees under
  `.claude/worktrees/` and reaches `main` through PRs; merged worktrees are deleted.
- Project skills in `.claude/skills/`:
  - [`simulation`](.claude/skills/simulation/SKILL.md): running, scripting, recalibrating and
    capturing with the sim;
  - [`training`](.claude/skills/training/SKILL.md): submitting, monitoring and evaluating HF
    Jobs training runs.

## Credits

Robot model and CAD (including the soft gripper): Seeed Studio
[reBot-DevArm](https://github.com/Seeed-Projects/reBot-DevArm) (CERN-OHL-W).
Dataset format and real-arm driver: [LeRobot](https://github.com/huggingface/lerobot).
WebXR relay: [vr-teleop-kit](https://github.com/Dream-Machines-Robotics/vr-teleop-kit).
Physics: [MuJoCo](https://mujoco.org).
