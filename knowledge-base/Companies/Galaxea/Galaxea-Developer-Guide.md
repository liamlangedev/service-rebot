---
type: dev-guide
company: "Galaxea"
slug: Galaxea
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Galaxea — Developer Guide (hackathon edition)

⬆ [Galaxea profile](Galaxea.md) · [Product portfolio](Galaxea-Products.md) · [Roadmap and strategy](Galaxea-Roadmap-and-Strategy.md)

> Scope: the platforms a team can realistically touch at Leukerbad — **R1 Pro / R1 Lite** (wheeled dual-arm), **LEMO** (desktop dual-arm) and the **A1Z** arm — plus the **G0.5** model stack. Everything below was checked on 2026-11-14 against the official docs portal and the two GitHub organisations. Which units are actually on site is not confirmed — ask the booth first.

## TL;DR — how you program it

- **R1 Pro / R1 Lite = ROS 2 Humble on Ubuntu 22.04**, running on the robot's own **Jetson AGX Orin 32 GB**. The vendor stack ("ATC ROS2 SDK", latest **V2.5.0**, 30 Oct 2026) is pre-installed; you start it with `galaxea --sdk start --feature-pkg R1ProBody` and then simply publish / subscribe: commands on `/motion_target/*`, feedback on `/hdas/*`.
- **Three control levels are openly documented**: Cartesian end-effector pose and chassis twist (high), joint-position targets with velocity limits (mid), and per-motor `p_des / v_des / kp / kd / t_ff` impedance commands (low). The public docs show no "EDU unlock" gate for low-level access.
- **LEMO = the same idea on a small box**: RK3588 controller, ROS 2 Humble workspace (`galaxea_lemo`), browser dashboard on port **8000**, 200 Hz arm control, leader arms for teleop. **A1Z alone = a plain Python SDK** over SocketCAN (250 Hz loop, gravity compensation, FK / IK), no ROS required.
- **AI is server / client**: a GPU machine (more than **8 GB VRAM**, RTX 4090 recommended) runs the **G0.5** policy server; a thin robot-side client streams camera + joint observations over WebSocket and executes the returned action chunks. Weights are public but **non-commercial**.
- **Data path is LeRobot-format end to end**: teleoperate (VR headset or leader arms) → record MCAP / rosbag / HDF5 → convert with `GalaxeaLeRobotToolkit` → fine-tune G0.5, π0.5, SmolVLA or a diffusion policy → deploy with the same client.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| **ATC ROS2 SDK V2.5.0** (R1 Pro / R1 Lite, 2026 models) | ROS 2 Humble (C++ / Python nodes), CLI `galaxea` | Whole robot: arms, grippers, torso, chassis, cameras, LiDAR, IMU, BMS | [Docs — Get the SDK](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/development/r1pro_get_sdk) | ✅ Binary `.run` installer, pre-installed in `~/galaxea`. **V2.5.0 supports 2026 models only**; 2025 models stay on V2.2.1 / V2.3.1 (the changelog pages disagree on which) |
| `galaxea_a1z` | Python ≥ 3.10 | A1Z 6-DoF arm + optional G1Z gripper | [GitHub](https://github.com/userguide-galaxea/galaxea_a1z) | ✅ MIT. SocketCAN on Linux; `gs_usb` user-space backend on macOS / Windows; Pinocchio gravity compensation, FK / IK, teach-and-play |
| `galaxea_lemo` | ROS 2 Humble + Python | LEMO platform: dual-arm teleop, 3 cameras, MCAP recording, web dashboard, policy client | [GitHub](https://github.com/userguide-galaxea/galaxea_lemo) | ✅ Ships as a precompiled runtime package plus `lemo-server/` for the GPU machine. Custom licence |
| `a1z-t` | Python 3.11 | Production A1Z-T leader arms → A1Z followers | [GitHub](https://github.com/userguide-galaxea/a1z-t) | ✅ Needs CPython 3.11 exactly (ships 3.11 bytecode) |
| `OpenA1Z-T` | Python 3.11 | 3D-printed open-hardware leader arm → A1Z | [GitHub](https://github.com/userguide-galaxea/OpenA1Z-T) | ✅ MIT, includes assembly guide |
| `a1z_data_collection` | Python 3.11 | One-command teleop + recording (joints + USB cameras) to HDF5 | [GitHub](https://github.com/userguide-galaxea/a1z_data_collection) | ✅ MIT. `main` = A1Z-T hardware, branch `legacy/open-a1z-t` = open hardware |
| `a1z_lerobot` | Python | LeRobot `Robot` adapter (`--robot.type=a1z`), training + rollout | [GitHub](https://github.com/userguide-galaxea/a1z_lerobot) | ✅ MIT. Scripts for SmolVLA and π0.5; sync or RTC async inference. README is Chinese only |
| `a1z_g05_deployment` | Python | Collect → LeRobot v2.1 → **G0.5 LoRA / full fine-tune** → PC inference on A1Z | [GitHub](https://github.com/userguide-galaxea/a1z_g05_deployment) | ✅ LoRA needs about **24 GB VRAM**, full fine-tune about 80 GB |
| `a1z_pi05_deployment` | Python (JAX openpi) | Same pipeline for **π0.5** | [GitHub](https://github.com/userguide-galaxea/a1z_pi05_deployment) | 🧪 Reference adaptation: dual-arm LoRA + online inference verified, task success not yet evaluated (per README) |
| `GalaxeaVLA` | Python 3.10, PyTorch 2.7.1 / CUDA 12.8 | **G0.5** model, policy server, fine-tuning; robot clients for R1 Lite, R1 Pro, SO-100/101, DROID / Franka | [GitHub](https://github.com/OpenGalaxea/GalaxeaVLA) | ✅ G0.5 Community License (non-commercial). About 820 GitHub stars |
| `EFMNode` | Python 3.10, ROS 2 Humble | On-robot deployment node for R1 Lite / R1 Pro; Docker image with `glx discovery` / `glx run` CLI; optional TensorRT | [GitHub](https://github.com/OpenGalaxea/EFMNode) | ✅ From the G0 Plus era (last push Feb 2026) |
| `GalaxeaLeRobotToolkit` | Python 3.10 + ROS 2 Humble | Converts rosbag / MCAP → LeRobot dataset | [GitHub](https://github.com/OpenGalaxea/GalaxeaLeRobotToolkit) | ✅ Apache-2.0. Needs `hdas_msg` built with colcon |
| `GalaxeaLeRobot`, `GalaxeaLerobot3.0` | Python | LeRobot forks (fixes; faster data generation and merge tools) | [GitHub](https://github.com/OpenGalaxea/GalaxeaLeRobot) · [3.0 fork](https://github.com/OpenGalaxea/GalaxeaLerobot3.0) | ✅ Apache-2.0 |
| `GalaxeaDP` | Python 3.10 | Diffusion-policy baseline (sim pipeline, joint or EE control) | [GitHub](https://github.com/OpenGalaxea/GalaxeaDP) | ✅ README badge MIT, repo metadata Apache-2.0 |
| `GalaxeaManipSim` | Python 3.10 | Simulation benchmark for R1 / R1 Pro / R1 Lite | [GitHub](https://github.com/OpenGalaxea/GalaxeaManipSim) | ✅ 30+ environments, 17 tasks |
| `robot_descriptions` | URDF / meshes / launch | A1, A1X, A1Y, A1Z, LEMO, R1, R1 Lite 2025 / 2026, R1 Pro 2025 / 2026 | [GitHub](https://github.com/userguide-galaxea/robot_descriptions) | ✅ ROS package names were renamed (for example `r1pro_urdf` → `r1pro_g1z_2026_description`) |
| `USD`, `CAD_files` | USD, STEP | Robot USD files; flanges, wrist-camera mounts (D405 / D435i / GMSL), arm bases | [USD](https://github.com/userguide-galaxea/USD) · [CAD](https://github.com/userguide-galaxea/CAD_files) | ✅ Use the CAD files to print custom fingers or sensor mounts |
| Legacy: `A1_SDK`, `R1-T_SDK`, `Tabletop_Teleoperation_SDK`, `Galaxea_Lab` | mixed | 2024-era A1 arm, R1 teleop, Isaac Lab fork | [userguide-galaxea org](https://github.com/userguide-galaxea) | Last pushed 2024 – early 2025; only relevant if an original R1 / A1 is on site |

## Control levels

**R1 Pro (2026) — topics confirmed in the official interface docs.** R1 Lite uses the same topic names with 6-element arm vectors and 3-element torso vectors.

| Level | Interface | Message | Limits and notes |
|---|---|---|---|
| Task | Navigation goal: action `/system_manager/navi/action` | `system_manager_msg/action/NavigationTask` (pose in `map` frame) | 🧪 **Paid add-on**. Laser SLAM, localisation **100 Hz**, accuracy under **0.05 m**, max **0.6 m/s**, obstacle bypass 10–20 Hz. Indoor only, area up to 100 m², ceiling up to 5 m |
| High | Arm end-effector pose: `/motion_target/target_pose_arm_left` / `_right` | `geometry_msgs/PoseStamped` | Pose of `gripper_link` relative to `torso_link4`. **Both arms must receive a target** before IK solves. Launch `teleoperation_ros2 vr_teleoperation_whole_body_launch.py independent_mode:=true`, then call service `/switch_control_mode_vr` with `use_vr_mode: false` |
| High | Chassis velocity: `/motion_target/target_speed_chassis` | `geometry_msgs/TwistStamped` | vx, vy within **±1.5 m/s**, ω within **±3 rad/s**; acceleration limits via `/motion_target/chassis_acc_limit` (max 2.5 / 1.0 / 1.0). Brake: `/motion_target/brake_mode` (`std_msgs/Bool`) |
| High | Gripper: `/motion_target/target_position_gripper_left` / `_right` | `sensor_msgs/JointState` | `position` 0–100 (0 closed, 100 open; stroke 0–100 mm) |
| Mid | Arm joints: `/motion_target/target_joint_state_arm_left` / `_right` | `sensor_msgs/JointState` | 7 positions (rad) + per-joint max velocity; ceilings {3, 3, 3, 3, 5, 5, 5}; acceleration and jerk limits are 1.5 × the velocity limit |
| Mid | Torso joints: `/motion_target/target_joint_state_torso` | `sensor_msgs/JointState` | 4 positions; velocity ceiling 1.5 per joint |
| Low | Per-motor command: `/motion_control/control_arm_left` / `_right`, `control_gripper_*`, `control_torso`, `control_chassis` | `hdas_msg/MotorControl` | Fields `p_des`, `v_des`, `kp`, `kd`, `t_ff`, `mode` — MIT-style impedance / feed-forward torque. Vendor-recommended A2 arm gains: kp 2.0, kd 25.0 per joint ("adjust with caution") |
| Feedback | `/hdas/feedback_arm_left`, `/hdas/feedback_arm_right`, `/hdas/feedback_torso`, `/hdas/feedback_chassis`, `/hdas/feedback_gripper_*` | `sensor_msgs/JointState` | Position, velocity, effort (arm torque). Torso feedback **200 Hz** (since V2.3.0). Error codes on `/hdas/feedback_status_*` |
| State estimate | `/motion_control/pose_ee_arm_left`, `/motion_control/pose_ee_arm_right`, `/motion_control/pose_floating_base` | `geometry_msgs/PoseStamped` | Published by the state estimator started with `moca_launch.py` |

**Rates you can plan with**

| Loop | Rate | Source |
|---|---|---|
| A1Z Python SDK control loop | **250 Hz** default | A1Z API docs |
| LEMO arm control | **200 Hz** default (`ctrl_hz`), leader polling 2000 Hz | `galaxea_lemo` README |
| R1 chassis command example | published at 200 Hz | R1 Pro command examples |
| Cameras | 30 Hz (head 1920×1536, wrist 1280×720); LEMO default 15 Hz | Docs, V2.3.0 changelog |
| LiDAR | 10 Hz | Navigation guide |
| VLA policy on robot | 15 Hz control, 16–32-step action chunks; G0 Tiny on Orin with TensorRT up to **10 Hz** | EFMNode, GalaxeaVLA README |

**A1Z low level (Python):** the motor firmware runs `τ = kp·(q_target − q) + kd·(q̇_target − q̇) + τ_ff`; the SDK adds Pinocchio gravity torque every cycle. Default gains kp `[30, 30, 30, 20, 5, 5]`, kd `[1, 1, 1, 0.5, 0.5, 0.5]`; torque limits `[70, 70, 70, 27, 10, 10]` Nm. Modes: zero-force floating (drag-teach) and position hold.

**What editions unlock.** No separate "EDU" firmware tier was found in the public docs; the low-level topics above are documented for the standard product. What *is* gated:

| Item | Gate |
|---|---|
| Autonomous navigation package | Paid add-on (trial via sales) |
| EHI tablet interface (live camera view, task claiming during data collection) | Purchased separately; 2026 R1 models only |
| EDP cloud data platform | Account from after-sales; **100 GB free** per robot / teleop kit purchased |
| LEMO human-takeover during inference | "Under development"; not on LEMO Standard, standard on COMBO / COMBO PLUS |
| G0.5 commercial use | Separate commercial licence |

## ROS 2 and middleware

- **Distro / OS:** ROS 2 **Humble**, Ubuntu **22.04 LTS**, JetPack 6.2 on the Orin (since V2.4.0). LEMO runs Ubuntu 22.04 ARM64 + Humble on the RK3588.
- **Modules (R1 Pro):**

| Module | Role | Launch |
|---|---|---|
| `HDAS` | Drivers: arms, torso, chassis, IMU, BMS, remote controller | `ros2 launch HDAS r1pro.py` |
| `moca_adapter` (renamed from `mobiman` in V2.3.0) | Joint, gripper, torso, chassis control + state estimator | `ros2 launch moca_adapter moca_launch.py` |
| `signal_camera` | Camera drivers | `signal_camera.py` |
| `livox_ros_driver2` | LiDAR (launch file `msg_MID360_launch.py`) | — |
| `hdas_msg` | Custom messages (`MotorControl`, `FeedbackStatus`) | build it on your laptop to decode bags |

- **Start / stop (SDK V2.4.0 and later):** `galaxea --sdk info` (lists feature packages, for example `R1ProBody`), `galaxea --sdk start --feature-pkg R1ProBody --use-discovery-service`, `galaxea --sdk stop`. Options: `--use-domain-id 5`, `--localhost-only`. Single modules: `galaxea --sdk start navigation`. Health: `galaxea --primary-check` (hardware self-check), `galaxea --sys monitor`.
- **Older start path (still in several doc pages):** `./robot_startup.sh boot ../sessions.d/ATCStandard/R1PROBody.d/` from `~/galaxea/install/startup_config/share/startup_config/script/` (tmux sessions); VR teleop session `R1PROVRTeleop.d`; navigation session `ATCNavigation/R1PROVRTeleopNAV.d`.
- **Discovery:** the stack uses a **Fast DDS discovery server** (port 11811). To see topics from your laptop, copy `super_client_configuration_file.xml`, set the robot IP in `<address>`, and `export FASTRTPS_DEFAULT_PROFILES_FILE=<path>`; if `ros2 topic list` is empty, `ros2 daemon stop && ros2 daemon start`.
- **Isolation:** by default ROS 2 talks to every host on the LAN. On a hall network shared by 20 vendors set `ROS_DOMAIN_ID` (docs example: 72) or `ROS_LOCALHOST_ONLY=1`. LEMO defaults to `ros_domain_id: 26`.
- **LEMO graph:** `Leader → g4_spi → teleop_bridge → /motion_target/* → arm_bridge → SDK → CAN → motors`, with an optional `policy_client` injecting targets. Launch: `ros2 launch lemo lemo.launch.py` (arguments: `arm:=left|right|both`, `start_camera`, `start_recording`, `start_policy`, `ctrl_hz`).
- **TF:** complete TF tree including wrist GMSL camera links since V2.4.1; LiDAR extrinsics from `~/galaxea/calib/robot_calibration.json` on `/tf_static`; URDF / SRDF auto-loaded from `/opt/galaxea/body/hardware.json`.

## Simulation and digital twins

| Asset | What you get | Status |
|---|---|---|
| [GalaxeaManipSim](https://github.com/OpenGalaxea/GalaxeaManipSim) | 30+ environments / 17 tasks for R1, R1 Pro, R1 Lite; scripted demo generation (`collect_demos`), replay with `bimanual_joint_position` or `bimanual_relaxed_ik` controllers, export to LeRobot | ✅ Linux + CUDA; last push Aug 2025 |
| [GalaxeaDP](https://github.com/OpenGalaxea/GalaxeaDP) | Diffusion-policy training and closed-loop sim evaluation on the above | ✅ |
| Isaac Sim tutorial (`galaxea_isaac_tutorial`) | R1 Pro in **Isaac Sim 4.5**: torso, chassis, target-following and whole-body demo scripts | ✅ documented for the 2025 R1 Pro; repo link is given inside the [simulation guide](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2025/function_guide/simulation/r1pro_simulation_guide) |
| [Galaxea_Lab](https://github.com/userguide-galaxea/Galaxea_Lab) | Isaac Lab fork (Isaac Sim 4.0) with the original R1 | Legacy (2024) |
| [robot_descriptions](https://github.com/userguide-galaxea/robot_descriptions) · [USD](https://github.com/userguide-galaxea/USD) | URDFs for every current robot incl. R1 Pro 2026, R1 Lite 2026, LEMO, A1Z (with / without G1Z); USD files | ✅ import into MuJoCo, Isaac, PyBullet, Pinocchio |
| G0.5 evaluation harnesses in GalaxeaVLA | LIBERO (`scripts/run/eval_libero.sh`), RoboTwin 2.0, plus checkpoints for DROID and RoboDojo | ✅ |
| [BEHAVIOR-1K fork](https://github.com/OpenGalaxea/BEHAVIOR-1K) | Household benchmark where the R1 Pro is the reference robot | ✅ fork, pushed Aug 2026 |

No vendor-hosted "digital twin" cloud product was found. Third-party sims that support Galaxea robots (GSWorld, MoMaGen, General Motion Retargeting) are listed in the [awesome list](https://github.com/OpenGalaxea/awesome-galaxea-developers).

## AI stack

**Models**

| Model | Size / base | Where | Use at a hackathon |
|---|---|---|---|
| **G0.5** `g05-base` | Autoregressive VLA on a Qwen3.5 2B backbone; about 11 GB per checkpoint | [HF OpenGalaxea/G05](https://huggingface.co/OpenGalaxea/G05) | ✅ Zero-shot on **R1 Lite and R1 Pro**; starting point for fine-tuning |
| G0.5 variants | `g05-so101`, `g05-droid`, `g05-libero`, `g05-robotwin20`, `g05-robodojo` | same org | ✅ SO-100/101 arms, Franka (DROID), sim benchmarks |
| G0 Plus 3B (`G0Plus_3B-base`, `-pick_and_place`) | Legacy line | [HF OpenGalaxea/G0-VLA](https://huggingface.co/OpenGalaxea/G0-VLA) | ✅ "Pick up anything" checkpoint; code at legacy commit `13a16a9` |
| G0 Tiny 250M | SmolVLM2 backbone, trained on about 1k h of R1 Pro VR teleop | same | ✅ Runs **on the R1 Pro's Orin** via TensorRT (demos: fold towels, hand over gift) |
| G0.5 Tiny | Listed in the EDP model catalogue | — | ⚠️ unverified — no public weights found |
| Third-party via EDP "one-click post-training" | π0, π0-FAST, π0.5, LingBot-VLA, LingBot-VA, DreamZero | [EDP page](https://www.galaxea-ai.com/en/edp.html) | 🧪 Needs an EDP account |

**G0.5 mechanics worth knowing**

- Shared **27-D action space**: `left_control(9) | left_gripper(1) | right_control(9) | right_gripper(1) | lower_body(7)`; the model emits optional reasoning (`Subtask`, `BBox`, `Trace`, `ActionHint`) before action tokens.
- Deployment = `scripts/serve_policy.py` (R1 Lite) or `scripts/serve_policy_mem.py` (R1 Pro, multi-frame memory) on the GPU box, then `experiments/r1pro/run.py --config config.toml` on the robot. Transport: **WebSocket + msgpack**; the client has no torch dependency. The task sentence comes from an instruction file.
- Fine-tune: `bash scripts/run/finetune.sh <num_gpu> r1lite|r1pro|r1pro_wbc` (joint-space or whole-body variant with torso). **Full fine-tune needs more than 70 GB VRAM** per GPU; the A1Z repo adds **LoRA at about 24 GB**.
- Reported by the vendor: 82.5% zero-shot on DROID, 98.9% LIBERO, 93.3% RoboTwin 2.0, 76.7% average after real-world fine-tuning on R1 Lite / R1 Pro (self-reported).

**Datasets**

| Dataset | Content | Licence / format |
|---|---|---|
| [Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) | **500+ h** real mobile manipulation, one embodiment, subtask language labels; homes, kitchens, retail, offices | RLDS + LeRobot; licence ⚠️ unverified (see profile) |
| [R1Pro_Pick_and_Place_Cube](https://huggingface.co/datasets/OpenGalaxea/R1Pro_Pick_and_Place_Cube) | Small R1 Pro example set | LeRobot |
| [G05-LIBERO-Dataset](https://huggingface.co/datasets/OpenGalaxea/G05-LIBERO-Dataset) | LIBERO data in the G0.5 layout | LeRobot |
| Fine-tune demo sets | `G0Plus_Finetune_LeRobot_Datasets_Demo` inside the G0-VLA repo | LeRobot |

**Teleoperation and data collection**

| Method | Platform | Notes |
|---|---|---|
| VR | R1 Pro, R1 Lite | Meta Quest 3 / 3S (app V0.2.2) and PICO 4 Ultra Enterprise (app V0.3.2). Upper-body and whole-body modes; robot and headset on the same LAN |
| Leader arms (isomorphic) | LEMO / A1Z via A1Z-T; R1 Lite via its "-T" leader kit (2025 and 2026 docs); R1 Pro leader kit documented for the 2025 model only | A1Z-T buttons: right = start / stop teleop, left = start / stop recording, both = discard episode |
| LEMO Studio / web dashboard | LEMO | Live joints + 3 camera previews, episode browse / replay / download; episodes saved as MCAP under `~/GalaxeaDataset/<date>/<name>_RAW/` |
| On-robot recording | R1 series | `./scripts/record.sh` (EFMNode) or `ros2 bag record ... -s mcap`; convert with `GalaxeaLeRobotToolkit` |
| EDP cloud | R1 series, LEMO | Task configuration, upload, visualisation, annotation, training, OTA deployment at `edp.galaxea-ai.com` |

**LeRobot support:** yes, first-class — official forks, a converter, a registered `a1z` robot type, and a LeRobot inference backend in the LEMO server (`bash server_setup.sh --backend lerobot`).

## Compute, sensors and connectivity

| | R1 Pro (2026) | R1 Lite (2026) | LEMO |
|---|---|---|---|
| Computer | NVIDIA **Jetson AGX Orin 32 GB** (200 TOPS), 1 TB SSD | Jetson AGX Orin 32 GB, 1 TB SSD (some doc pages still say "NUC") | **RK3588** (6 TOPS NPU), 8 GB RAM, 64 GB eMMC |
| DoF | **26** (2 × 7 arm, 2 grippers, 4 torso, 6 chassis) | **23** (2 × 6 arm, 2 grippers, 3 torso, 6 chassis) | **14** incl. grippers (2 × 6-DoF A1Z) |
| Payload per arm | 3.5 kg rated / **5 kg** peak at 0.6 m | 3 kg rated / 5 kg peak at 0.6 m | 3 kg rated / 5 kg peak |
| Reach / workspace | 0–2000 mm vertical, 716 mm radius (861 mm with gripper) | Arm 600 mm extended | 2370 × 900 × 912 mm dual-arm envelope |
| Size / mass | 1700 mm, **126 kg** with battery | 1560 mm max, **96 kg** | 18–20 kg, 1040 × 565 × 592 mm |
| Battery | 48 V, 35 Ah, **1680 Wh** | 48 V, 15 Ah, 720 Wh (or mains) | 24 V / 30 A adapter |
| Cameras | Head: 2 × mono 1920×1536 at 30 fps (118° × 92°). Wrist (optional): 2 × depth 1280×720 (7–50 cm) or 2 × fisheye 196° | Platform stereo 1280×720; 2 × wrist depth | 3 synchronised views (top + 2 wrist), hardware-triggered |
| LiDAR / IMU | 1 × 360° × 59° LiDAR (40 m at 10% reflectivity); IMUs in chest and chassis | 1 × 360° LiDAR | — |
| Network / I/O | 4 × GbE, Wi-Fi 6 (AX210), BT 5.2, USB 3.0, HDMI; aux power 24 V / 12 A and 5 V / 3 A | Wi-Fi 6 (AX201), BT 5.2, 4 USB, Type-C, 2 HDMI | 2 × GbE, Wi-Fi 6E, HDMI 2.1 ×2, USB 3.0 |
| Bus | CAN FD to motors | CAN FD | CAN (1 Mbps on A1Z) |
| Login | `ssh nvidia@<ip>`, password `nvidia` | `ssh r1lite@<ip>`, password `nvidia` | monitor + keyboard for first setup |

- The official R1 Pro 2026 spec sheet (126 kg, 4-DoF torso) differs from the reseller figures quoted in the profile (96 kg, 3-DoF torso) — trust the docs portal or `cat /opt/galaxea/body/hardware.json` on the actual unit.
- The driver docs still list five chassis RGB camera topics, while the 2026 navigation guide states the 2026 chassis is LiDAR-only. Check `ros2 topic list` on site.
- Off-board GPU: any Linux x86_64 box with an NVIDIA card; the LEMO script `ethernet_setup.sh` builds a direct cable link (server `192.168.88.1`, robot `192.168.88.2`, policy port 8765).

## First 60 minutes checklist

**Path A — R1 Pro / R1 Lite**

1. **Safety first (5 min).** Find the red E-stop (rear top of chassis). Turn on the RC transmitter with all four switches (SWA–SWD) **up** = stopped. Clear a 1.5 m radius.
2. **Power on.** Rocker switch (rear bottom of chassis), then the round soft switch (hold about 3 s). E-stop must be released before power-on.
3. **Connect.** Get the robot IP from the Galaxea staff, then `ssh nvidia@<ip>` (R1 Lite: `ssh r1lite@<ip>`).
4. **Isolate ROS.** In every shell: `export ROS_DOMAIN_ID=<number agreed with the booth>`.
5. **Check and start the stack.** `galaxea --sdk info` → `galaxea --primary-check` → `galaxea --sdk start --feature-pkg R1ProBody --use-discovery-service` (on an R1 Lite use the package name that `--sdk info` prints). (On older images: `bash ~/canfd.sh`, then `robot_startup.sh boot ...` as above.)
6. **Verify feedback.** `source ~/galaxea/sdk/setup.bash`, then `ros2 topic hz /hdas/feedback_arm_left` and `ros2 topic echo /hdas/feedback_arm_left --once`. Battery: `ros2 topic echo /hdas/bms --once`.
7. **Hello-world motion (gripper — the safest joint).**
   `ros2 topic pub --once /motion_target/target_position_gripper_left sensor_msgs/msg/JointState "{position: [100]}"` then `[0]`.
8. **Move an arm slowly.** Read the current 7 joint angles, then publish them back with one joint changed by 0.1 rad and a low velocity limit:
   `ros2 topic pub --once /motion_target/target_joint_state_arm_left sensor_msgs/msg/JointState "{position: [q1,q2,q3,q4,q5,q6,q7], velocity: [0.3,0.3,0.3,0.3,0.3,0.3,0.3]}"`.
9. **Drive the base.** RC switches to host-control pattern (**down-down-up-up**), then
   `ros2 topic pub -r 50 /motion_target/target_speed_chassis geometry_msgs/msg/TwistStamped "{twist: {linear: {x: 0.1}}}"`; Ctrl-C to stop, then `ros2 topic pub --once /motion_target/brake_mode std_msgs/msg/Bool "{data: true}"`.
10. **Read sensors.** Cameras: `/hdas/camera_head/left_raw/image_raw_color/compressed`, `/hdas/camera_wrist_left/color/image_raw/compressed`. LiDAR: `/hdas/lidar_chassis_left`. IMU: `/hdas/imu_chassis`, `/hdas/imu_torso`. View from a laptop with `rqt_image_view` after setting the discovery-server profile.
11. **Record a test bag.** `ros2 bag record /hdas/feedback_arm_left /hdas/feedback_arm_right /hdas/camera_head/left_raw/image_raw_color/compressed -s mcap` for 10 s; confirm it converts with `GalaxeaLeRobotToolkit`.
12. **Try zero-shot G0.5 (if a GPU box is available).** Server: `python scripts/serve_policy_mem.py --ckpt_path checkpoints/g05-base/checkpoints/model_state_dict.pt --host 0.0.0.0 --port 8080 --device cuda --action_steps 16 eval_embodiment=galaxea_r1pro` (plus the overrides in the README). Robot: set the server address in `experiments/r1pro/config.toml`, `python run.py --config config.toml`. Keep a hand on the E-stop.

**Path B — LEMO / A1Z**

1. Clamp the base plate, check fasteners, locate the E-stop button and the pause remote.
2. Power the CCU (long-press), attach monitor / keyboard once to join Wi-Fi; note the IP.
3. On the CCU: `source ~/lemo_1.x.x.x/install/setup.bash && ros2 launch lemo lemo.launch.py`.
4. Open `http://<lemo-ip>:8000` — confirm both arms report joints and all three cameras preview.
5. Teleop: right A1Z-T button to enable, move slowly, left button to record one episode, left again to save.
6. Bare A1Z without the CCU: `sudo ip link set can0 type can bitrate 1000000 && sudo ip link set can0 up`, `pip install -e galaxea_a1z`, then `python examples/gravity_comp.py --gravity_factor 0.3` (raise to 1.0 once the direction is right) and `python examples/position_hold.py --q_target_deg 0,30,-20,-15,0,0 --speed 0.5`.
7. Read state in Python: `robot = get_a1z_robot(can_channel="can0", zero_gravity_mode=False); robot.start(); robot.get_joint_state()`; move with `robot.move_joints(target, speed)`.
8. Inference: on the GPU box `bash server_setup.sh --backend lerobot` (or `g05`), edit `deploy/serve.env.local`, `bash deploy/start_serve.sh`; on LEMO set `policy.server_url` in `/etc/lemo/machine.yaml` and relaunch with `start_policy:=true`.

## Known gotchas and safety

- **E-stop does not cut power on the R1 Pro**, and after an E-stop while running you must cycle the *hard* switch before the robot works again. RC switch SWD down is also an E-stop that requires a restart.
- **Arms drop on power-off.** The docs state the R1 Lite joint motors have no brakes; for both robots hold the arms (or park them) before powering down.
- **Starting the pose controller moves both arms** to a default posture — start with arms hanging naturally and people clear.
- **Chassis commands need the RC on but not in RC-control mode**; the base only moves while you keep publishing.
- **ROS 2 cross-talk** on a shared network can make someone else's node drive your robot. Set a domain ID or localhost-only mode before launching anything.
- **Default credentials (`nvidia` / `nvidia`) and an unauthenticated LEMO dashboard on `0.0.0.0:8000`** — use the vendor's private router, or set `DASHBOARD_TOKEN`.
- **Version traps:** V2.5.0 is for 2026 hardware only; `mobiman` was renamed `moca` in V2.3.0, so older tutorials and third-party code use stale package names; URDF package names changed too.
- **Doc inconsistencies:** the driver table labels `/hdas/camera_wrist_left/...` as the *right* wrist camera and vice versa — cover a lens to confirm. The R1 Pro "Command Example" page is Chinese-only even on the English site.
- **Python versions:** G0.5 and the ROS client need **3.10** (do not create a second venv inside `experiments/r1pro`, it would pull a newer Python that breaks `rclpy`); A1Z teleop / collection need **3.11**. Keep separate environments.
- **A1Z:** start gravity compensation at factor 0.3; check the 120 Ω CAN termination; joint 3's sign is opposite to the URDF; an over-threshold gravity torque triggers a software emergency stop.
- **Navigation limits:** indoor, static environment, map area up to 100 m², cover the route twice while mapping, keep the robot 45 cm from obstacles at goals; mapping runs in a vendor Docker image you must obtain from sales.
- **EDP auto-upload deletes local recordings after a successful upload** once credentials are configured — do not enable it on hall Wi-Fi unless you mean to.
- **Compute reality:** full G0.5 fine-tuning does not fit a 24 GB card. Plan for zero-shot, LoRA (A1Z repo), or a small policy (SmolVLA / diffusion / ACT) on 30–100 demos.
- **Licences:** G0.5 code and weights are non-commercial; the A1Z SDK and teleop tools are MIT; `a1z_g05_deployment` / `a1z_pi05_deployment` use a Galaxea A1Z licence agreement. Fine for the hackathon, check before productising.
- **Mechanical envelope:** wheeled base on flat floors only; 126 kg (R1 Pro) on a sports-hall floor — check ramps and thresholds; the docs give no IP rating, so no snow or wet surfaces.

## Community resources

| Resource | Link | Use it for |
|---|---|---|
| Documentation centre (EN / 中文) | [docs.galaxea-dynamics.com](https://docs.galaxea-dynamics.com/home/en/) | Per-robot guides, interface tables, changelog, FAQ |
| SDK changelog | [V2.5.0 notes](https://docs.galaxea-dynamics.com/Changelog/en/v2.5.0) | What changed between images |
| Product / SDK GitHub org | [userguide-galaxea](https://github.com/userguide-galaxea) | A1Z, LEMO, URDF, CAD, USD |
| Model / data GitHub org | [OpenGalaxea](https://github.com/OpenGalaxea) | G0.5, toolkits, sim |
| Community project index | [awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers) | 30+ papers and competition entries built on Galaxea robots (BEHAVIOR Robot Suite, π0.5 on R1 Lite, ICRA 2025 WBCD winner on A1X, …) |
| Hugging Face | [OpenGalaxea](https://huggingface.co/OpenGalaxea) | Checkpoints and datasets |
| G0.5 project page | [opengalaxea.github.io/G05](https://opengalaxea.github.io/G05/) | Videos, benchmark tables |
| Support | support@galaxea-dynamics.com · product@galaxea-ai.com | Vendor support (office hours Mon–Fri 10:00–18:00 GMT+8 — on site, ask the booth instead) |
| Video channels | [YouTube @Galaxea_youtube](https://www.youtube.com/@Galaxea_youtube) · [Bilibili](https://space.bilibili.com/3546640453471155) | Setup and demo videos |
| Programmes | [Developer discount](https://galaxea-dynamics.com/pages/developer-discount) · [Education discount](https://galaxea-dynamics.com/pages/education-discount) | LEMO / A1Z only |

No official Discord or forum was found; GitHub issues on `GalaxeaVLA` are the public Q&A channel.

## Sources

- [Galaxea documentation centre](https://docs.galaxea-dynamics.com/home/en/)
- [R1 Pro 2026 — About / specifications](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/)
- [R1 Pro 2026 — Unboxing guide](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/openbox/r1pro_openbox_ros2)
- [R1 Pro 2026 — Quick start](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/getting_started/quick_start/r1pro_quick_start)
- [R1 Pro 2026 — Remote controller guide](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/getting_started/controller/r1pro_controller_guide)
- [R1 Pro 2026 — Demo](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/getting_started/demo/r1pro_demo_ros2)
- [R1 Pro 2026 — Get the SDK](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/development/r1pro_get_sdk)
- [R1 Pro 2026 — Command examples](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/development/r1pro_py_template)
- [R1 Pro 2026 — ROS 2 communication](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/development/r1pro_ros2_com)
- [R1 Pro 2026 — Software architecture](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/software_interface/r1pro_software_topo)
- [R1 Pro 2026 — Driver interface](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/software_interface/r1pro_driver)
- [R1 Pro 2026 — Motion control interface](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/software_interface/r1pro_motion_control)
- [R1 Pro 2026 — Interface startup example](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/software_interface/r1pro_launch)
- [R1 Pro 2026 — VR teleoperation](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/teleop/vr_teleop/r1pro_vr_guide_ros2)
- [R1 Pro 2026 — Autonomous navigation guide](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/function_guide/navigation/r1pro_navigation_guide)
- [R1 Pro 2026 — Open-source STP files](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2026/getting_started/r1pro_stp_opensource)
- [R1 Pro 2025 — Simulation platform guide](https://docs.galaxea-dynamics.com/R1Pro/en/docs/2025/function_guide/simulation/r1pro_simulation_guide)
- [R1 Lite 2026 — About / specifications](https://docs.galaxea-dynamics.com/R1Lite/en/docs/2026/)
- [R1 Lite 2026 — Unboxing guide](https://docs.galaxea-dynamics.com/R1Lite/en/docs/2026/openbox/r1lite_openbox)
- [R1 Lite 2026 — Motion control interface](https://docs.galaxea-dynamics.com/R1Lite/en/docs/2026/software_interface/r1lite_motion_control/)
- [LEMO — About](https://docs.galaxea-dynamics.com/LEMO/en/docs/)
- [LEMO — Usage workflow](https://docs.galaxea-dynamics.com/LEMO/en/docs/usage_workflow/lemo_usage_workflow)
- [LEMO — A1Z-T teleoperation device](https://docs.galaxea-dynamics.com/LEMO/en/docs/lemo_a1zt_teleop/)
- [LEMO — Developer tools](https://docs.galaxea-dynamics.com/LEMO/en/docs/tools/lemo_tools)
- [A1Z — Launch SDK](https://docs.galaxea-dynamics.com/A1Z/en/docs/development/a1z_get_sdk)
- [A1Z — Software API](https://docs.galaxea-dynamics.com/A1Z/en/docs/software_api/a1z_api)
- [Tools — EDP platform configuration](https://docs.galaxea-dynamics.com/Tools/en/docs/edp_setup)
- [Tools — ROS 2 discovery service](https://docs.galaxea-dynamics.com/Tools/en/docs/ros2_discovery_service)
- [SDK changelog V2.5.0](https://docs.galaxea-dynamics.com/Changelog/en/v2.5.0) · [V2.4.1](https://docs.galaxea-dynamics.com/Changelog/en/v2.4.1) · [V2.4.0](https://docs.galaxea-dynamics.com/Changelog/en/v2.4.0) · [V2.3.0](https://docs.galaxea-dynamics.com/Changelog/en/v2.3.0)
- [GitHub — OpenGalaxea organisation](https://github.com/OpenGalaxea)
- [GitHub — OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA)
- [GitHub — GalaxeaVLA R1 Pro client README](https://github.com/OpenGalaxea/GalaxeaVLA/tree/main/experiments/r1pro)
- [GitHub — OpenGalaxea/EFMNode](https://github.com/OpenGalaxea/EFMNode)
- [GitHub — OpenGalaxea/GalaxeaLeRobotToolkit](https://github.com/OpenGalaxea/GalaxeaLeRobotToolkit)
- [GitHub — OpenGalaxea/GalaxeaManipSim](https://github.com/OpenGalaxea/GalaxeaManipSim)
- [GitHub — OpenGalaxea/GalaxeaDP](https://github.com/OpenGalaxea/GalaxeaDP)
- [GitHub — OpenGalaxea/awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers)
- [GitHub — userguide-galaxea organisation](https://github.com/userguide-galaxea)
- [GitHub — userguide-galaxea/galaxea_a1z](https://github.com/userguide-galaxea/galaxea_a1z)
- [GitHub — userguide-galaxea/galaxea_lemo](https://github.com/userguide-galaxea/galaxea_lemo)
- [GitHub — userguide-galaxea/a1z-t](https://github.com/userguide-galaxea/a1z-t)
- [GitHub — userguide-galaxea/OpenA1Z-T](https://github.com/userguide-galaxea/OpenA1Z-T)
- [GitHub — userguide-galaxea/a1z_data_collection](https://github.com/userguide-galaxea/a1z_data_collection)
- [GitHub — userguide-galaxea/a1z_lerobot](https://github.com/userguide-galaxea/a1z_lerobot)
- [GitHub — userguide-galaxea/a1z_g05_deployment](https://github.com/userguide-galaxea/a1z_g05_deployment)
- [GitHub — userguide-galaxea/a1z_pi05_deployment](https://github.com/userguide-galaxea/a1z_pi05_deployment)
- [GitHub — userguide-galaxea/robot_descriptions](https://github.com/userguide-galaxea/robot_descriptions)
- [GitHub — userguide-galaxea/CAD_files](https://github.com/userguide-galaxea/CAD_files)
- [GitHub — userguide-galaxea/Galaxea_Lab](https://github.com/userguide-galaxea/Galaxea_Lab)
- [Hugging Face — OpenGalaxea](https://huggingface.co/OpenGalaxea)
- [Galaxea — EDP (Embodied Development Platform)](https://www.galaxea-ai.com/en/edp.html)
- [Galaxea store — LEMO / support centre](https://galaxea-dynamics.com/pages/galaxea-support-center)
- [Galaxea store — Developer discount](https://galaxea-dynamics.com/pages/developer-discount)
