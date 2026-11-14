---
type: dev-guide
company: "AGIBOT"
slug: AGIBOT
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# AGIBOT — Developer Guide (hackathon edition)

⬆ [AGIBOT profile](AGIBOT.md) · [Product portfolio](AGIBOT-Products.md) · [Roadmap and strategy](AGIBOT-Roadmap-and-Strategy.md)

> **Read this first:** what AGIBOT brought to Leukerbad is **not confirmed**. Identify the exact unit before you plan — the nameplate decides everything. An **X2 EDU has no cameras, no LiDAR, no on-board developer computer, no hands and no voice module**; an **X2 Ultra** has all of them. A **D1 Pro** dog has no SDK; a **D1 Edu / Ultra** does. All facts below were read on 2026-11-14 from the official SDK docs (AimDK_X2 **v1.1.0**) and the AgibotTech GitHub READMEs unless flagged.

## TL;DR — how you program it

- **X2 humanoid = ROS 2 Humble.** The official SDK is **AimDK_X2** (Python + C++, Ubuntu 22.04). You call ROS 2 services (`/aimdk_5Fmsgs/srv/...`) and publish topics (`/aima/...`). Hello-world is three shell commands: read mode → stand → wave.
- **D1 quadrupeds = plain C++ / Python library, no ROS needed.** `standUp()`, `move(vx, vy, yaw_rate)`, `getRPY()`, plus `sendMotorCmd()` for joint-level control. Each D1 size (Edu/Ultra, Max, MaxPro) has its **own, incompatible** SDK repo.
- **Hands and grippers = `agilink_omnihand_sdk`** (C++ / Python / ROS 2 Humble, Linux and Windows) over USB — works on any vendor's arm.
- **G1 / G2 wheeled manipulators and A2 = no public SDK.** They are driven through **Genie Studio** (commercial platform, "GDK" for real-robot control) and LinkSoul / LinkCraft no-code tools. You need AGIBOT staff.
- **No robot slot? Still productive:** X2 MuJoCo simulation runs on a laptop without a GPU; **Genie Sim** (Isaac Sim, G2 model, ROS 2 + MoveIt) and **GO-1** open weights (about **7 GB** GPU memory for inference) are public.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| **AimDK_X2** v1.1.0 (2026-05-11) ✅ | Python, C++17 on ROS 2 Humble | X2 Ultra, X2 Ultra (new version), X2 EDU: motion modes, walking, upper body, joints, hands, voice, face screen, LEDs, sensors, SLAM / navigation (optional) | [docs](https://x2-aimdk.agibot.com/en/latest/) | SDK package is downloaded from the floating toolbar on the docs site, or copied from the robot. **SDK version must match robot firmware.** |
| X2 RL Deploy extras (`x2_rl_deploy`) ✅ | C++, ONNX Runtime | Run your own RL locomotion policy (ONNX) on the X2 or in MuJoCo | [docs](https://x2-aimdk.agibot.com/en/latest/rl_contents.html) | Separate download ("Extras" on the docs toolbar). PS5 gamepad mapping included. |
| X2 Sim + MC (`sim_mujoco-x86`, `mc-x86`) ✅ | binaries + ROS 2 | X2 physics simulation with the real motion controller in the loop | [docs](https://x2-aimdk.agibot.com/en/latest/sim_contents.html) | x86_64, Ubuntu 22.04, **no GPU required**, Docker recommended. |
| `agibot_x2_urdf` ✅ | URDF, MJCF | X2 Ultra, X2 Ultra (new version, incl. OmniHand and OmniPicker variants), X2 EDU models | [GitHub](https://github.com/AgibotTech/agibot_x2_urdf) | Mulan PSL v2. Pick the folder by nameplate (see checklist). |
| LinkSoul **AgentSDK** (`linksoul-agentsdk` 1.4.0a0) + sample ✅ | Python ≥ 3.10 | Cloud conversation agent on the robot: ASR text in, your LLM / knowledge base / skills out | [sample code](https://github.com/AgibotTech/agibot_agentsdk_sample_code) | Sample is a **hospital triage robot** (intent routing, knowledge base, whitelisted skills, Chinese and English). SDK wheel is installed offline; needs `appId` / `appSecret` from the LinkSoul platform. |
| `agibot_D1_Edu-Ultra` ✅ | C++, Python 3 | D1 Edu / D1 Ultra (model codes ZSL-1, wheel-legged ZSL-1W; a ZSM-1W API file is also present): high-level gaits, low-level motors, IMU | [GitHub](https://github.com/AgibotTech/agibot_D1_Edu-Ultra) | BSD-3-Clause. Pre-built `.so` for x86_64 and aarch64. Ubuntu 22.04, GCC 11+, Eigen3, Boost. |
| `Agibot_D1_Max` ("RobotSDK") ✅ | C++ | D1 Max: high-level control and state data | [GitHub](https://github.com/AgibotTech/Agibot_D1_Max) | README lists high-level control only. Has an SDK-version × system-version compatibility table and a raw protocol PDF. |
| `Agibot_D1_MaxPro` ✅ | C++ only | D1 MaxPro: high-level motion, low-level motor / joint control, video, point cloud, odometry, charging state | [GitHub](https://github.com/AgibotTech/Agibot_D1_MaxPro) | Chinese README. Recommended host: **Ubuntu 20.04 x86**. High-level needs no ROS; **low-level needs ROS 1**. URDF in repo. |
| `agilink_omnihand_sdk` v1.1.11 ✅ | C++, Python, ROS 2 Humble | OmniHand 2025, OmniHand Pro 2025, OmniHand 3 Lite, OmniHand 3 Ultra-M, OmniPicker 3, OmniHand Dex UMI; kinematics API for two models | [GitHub](https://github.com/AgibotTech/agilink_omnihand_sdk) | Mulan PSL v2. Linux x64 / aarch64 and Windows x64. USB; run `setup_udev.sh` once. |
| `agilink_omniglove_sdk` ✅ | C | OmniGlove teleoperation glove | [GitHub](https://github.com/AgibotTech/agilink_omniglove_sdk) | Mulan PSL v2. Linux (DIRECT and UDP) and Windows (DIRECT only). |
| Hand URDFs, toolbox, firmware ✅ | URDF, tools | `agilink_omnihand_description`, `agilink_omnihand_3_lite_s_description`, `agilink_omnihand_toolbox` (HMI, data collection, firmware update) | [AgibotTech org](https://github.com/AgibotTech) | Active in November 2026. |
| `genie_sim` (Genie Sim 3.x) ✅ | Python, ROS 2 | Simulated Genie G2 (and reference arms) — benchmark, teleop, data generation, scene generation | [GitHub](https://github.com/AgibotTech/genie_sim) | `geniesim` CLI; Docker image with Isaac Sim 6.2; needs an NVIDIA GPU. |
| `A3-A3U-robot-model`, `A3_Ultra_usd` ✅ | URDF, MJCF, SRDF, USD | A3 and A3 Ultra models (static assets only, no controllers) | [GitHub](https://github.com/AgibotTech/A3-A3U-robot-model) | SRDF for MoveIt only on the A3 Ultra variants. |
| `sonic_for_a3` 🧪 | C++, Python | Whole-body tracking controller and XR teleoperation for A3 / A3 Ultra | [GitHub](https://github.com/AgibotTech/sonic_for_a3) | Port of NVIDIA SONIC. Apache-2.0. Safety gantry strongly recommended by the repo. |
| GO-1 / GO-1 Air ✅ | Python (PyTorch) | VLA manipulation policy: fine-tune, local or server inference | [GitHub](https://github.com/OpenDriveLab/AgiBot-World) | CC BY-NC-SA 4.0 (non-commercial). Built on LeRobot datasets. |
| Genie Studio 2.0 / GDK ✅ (commercial) | web platform | G-series robots: data collection, training, sim evaluation, deployment, task orchestration, fleet monitoring | [Genie Studio](https://genie.agibot.com/en/geniestudio) | No public API reference; access by contacting AGIBOT. |
| X1 stack (`agibot_x1_infer`, `_train`, `_hardware`) ✅ | C++, Python | Open-source X1 humanoid: RL training, inference, drivers | [GitHub](https://github.com/AgibotTech/agibot_x1_infer) | Built on AGIBOT's open-source **AimRT** middleware. Reference only — not a robot you will find on site. |

**No public SDK found for:** A2 / A2 Ultra / A2 Lite (configuration tools only), A3 (product page claims open interfaces; only models and the SONIC port are public), G1 / G2 / G2 Air / G2 Max, C5 cleaning robot. ⚠️ unverified whether AGIBOT hands out private SDKs at events.

## Control levels

### X2 (AimDK) — what each level gives you

| Level | Interface | Rate / limits | Use it for |
|---|---|---|---|
| Motion mode | service `SetMcAction` / `GetMcAction` | on demand; returns a reject code (bad posture, safety level, starting up …) | Zero-torque `PASSIVE_DEFAULT` → damping `DAMPING_DEFAULT` → position stand `JOINT_DEFAULT` → balanced stand `STAND_DEFAULT` → walking `LOCOMOTION_DEFAULT` → off-road `LOCOMOTION_STEP`; also `HEAD_ONLY`, `UPPERBODY_REMOTE_SPLIT` |
| Preset and authored motions | `SetMcPresetMotion`, LinkCraft actions | discrete; `interrupt` flag decides pre-emption | Wave (ID 1002 in the docs example), gestures, motions authored in LinkCraft |
| Walking velocity | topic `/aima/mc/locomotion/velocity` (forward, lateral, yaw) | publish at **50 Hz**; **open loop** — no trajectory or end-point accuracy | Teleop, simple approach behaviours. Default LOW speed mode caps forward speed at **0.8 m/s** (MEDIUM 1.2, HIGH 1.8, off-road 2.0 m/s) |
| Navigation (optional module) | `/aima/te/pnc_task_request`, SLAM commands on `/integrated_command` | needs a built map + relocalization; obstacle avoidance on/off | Point-to-point goals. **Must be enabled by AGIBOT after-sales** |
| Upper body | topic `/mc/upper_body_command` in `UPPERBODY_REMOTE_SPLIT` mode | **50 Hz**; stamp must be within **200 ms** of receive time | Head (2) + arms (14) + hands in one message while the robot keeps balancing — the right level for teleop and manipulation |
| Joint (low level) | `/aima/hal/joint/{head,arm,waist,leg}/command` with position, velocity, effort, stiffness, damping | state feedback **500 Hz** (head 333 Hz); **no timeout or fail-safe** | Position / velocity / **torque** control per joint; whole-body research |
| Hand (low level) | `/aima/hal/joint/hand/command` | needs `aima em stop-app mc` on PC1 first | Independent hand / gripper control |
| Full takeover | developer mode `Develop_MC` via `MigrateSystemState` | you send data straight to the EtherCAT layer | Your own RL policy (see X2 RL Deploy) |

Other developer modes: `Develop_Nav` (disables AGIBOT navigation, mapping, planning, perception so you can run your own), `Develop_Audio_ROS` and `Develop_Audio_Linux` (raw microphone stream for your own voice stack). Switch back to `Ready` or reboot when done.

**Input-source arbitration:** register your own source name with `SetMcInputSource` and put it in every command. The handheld remote (priority 80) and the phone app (60) outrank most SDK sources — if the robot ignores you, someone is holding the remote. Query with `GetCurrentInputSource`.

### What each X2 edition unlocks

| | X2 Neo | X2 EDU | X2 Ultra | X2 Ultra (new version, nameplate "-N") |
|---|---|---|---|---|
| SDK access | ❌ (product page: not supported) | ✅ | ✅ | ✅ |
| On-board developer computer | — | ❌ none — external PC over Ethernet | ✅ Jetson Orin NX 16 GB | ✅ Jetson Orin NX 16 GB |
| Container development on robot | — | ❌ | ✅ | ✅ |
| Perception sensors | interaction camera only | ❌ none (no LiDAR, cameras, touch, GNSS) | ✅ full suite | ✅ full suite |
| Head joints | 1 | ❌ not supported | yaw only | yaw + pitch |
| Hands / gripper (end-effector API) | ❌ | ❌ | ✅ OmniHand 2025, OmniPicker | ✅ |
| Built-in voice / interaction module | ✅ | ❌ | ✅ | ✅ |
| Controllable body joints (derived from SDK joint tables) | — | **29** (waist 3, arms 14, legs 12) | **30** | **31** |

### D1 quadrupeds

| Model | High level | Low level | Sensors via SDK |
|---|---|---|---|
| D1 Edu / Ultra | `standUp`, `lieDown`, `passive` (damping), `move(vx, vy, yaw_rate)` (up to ±3 m/s, ±1 m/s, ±3 rad/s), `jump`, `frontJump`, `backflip`, `shakeHand`, two-leg stand, `attitudeControl` | `sendMotorCmd` — per joint target position, velocity, kp, kd, feed-forward torque; shared-memory interface updates every **1 ms** | IMU quaternion / RPY / acceleration / gyro, body position and velocity, battery, per-joint angle, speed, torque |
| D1 Max | high-level client (state machine documented in repo) | not listed in README | state data stream (demo `./data <ip> 8082`) |
| D1 MaxPro | high-level TCP client, crawl mode, auto-docking | motor / joint control (ROS 1 required) | odometry, joint state, IMU acceleration, alerts, charging state, point cloud, front / rear camera via RTSP |
| D1 Pro | ❌ no SDK | ❌ | — |

On the D1 MaxPro the README states that under SDK control **the robot's own controller does not intervene or change state for you** — every state is yours to manage.

## ROS 2 and middleware

- **X2:** ROS 2 **Humble** on Ubuntu 22.04. Messages live in `aimdk_msgs`; services are named `/aimdk_5Fmsgs/srv/<Name>`; topics under `/aima/hal/...` (hardware), `/aima/mc/...` (motion control), `/aima/hds/...` (diagnostics), `/aima/sm/system_state` (1 Hz).
- **QoS matters:** most command and state topics are `BEST_EFFORT`; several sensor topics are `RELIABLE + TRANSIENT_LOCAL`. A subscriber with the wrong QoS silently receives nothing — copy the QoS from the docs tables or the examples.
- **DDS:** do not edit the robot's DDS configuration. Nodes started outside an SSH shell (for example from a systemd **user** service — system-level services are not available) must first `source /home/agi/.aima/env/bashrc`.
- **RMW:** the simulation guide exports `RMW_IMPLEMENTATION=rmw_fastrtps_cpp`; the RL-deploy guide installs `rmw-cyclonedds-cpp`. Follow the guide you are using and keep all terminals consistent.
- **Visualization:** Foxglove, RSView or RViz (docs section "Data Visualization").
- **Standard messages:** cameras use `sensor_msgs/Image`, `CompressedImage`, `CameraInfo`; LiDAR `PointCloud2`; IMU `Imu`; GNSS `NavSatFix`; SLAM maps use `nav_msgs/MapMetaData`.
- **D1 dogs:** no ROS in the Edu / Ultra / Max SDKs (UDP / TCP client library); D1 MaxPro low level uses **ROS 1**. Wrap them in your own ROS 2 node if you need Nav2.
- **Hands:** ROS 2 Humble packages ship inside the OmniHand SDK (`source ros2/setup.bash`).
- **Genie Sim:** `geniesim_ros` runs physics, rendering and the robot natively in ROS 2 with **MoveIt** and **ros2_control** on one shared `sim_time` (container built as "Isaac Sim 6.2 + Jazzy").
- **AimRT:** AGIBOT's own open-source C++ runtime (used by the X1 stack and the A3 MuJoCo sim in `sonic_for_a3`); ROS 2-compatible. You do not need it for the X2 SDK.
- **Link-U OS 1.0** 🧪 (Chinese name "Lingqu OS"): AGIBOT's robot operating system, in partner trial; announced to be **fully open source by end of 2026** via the OpenAtom Foundation. Not something you can install this weekend.

## Simulation and digital twins

| Tool | Robots | Engine | What you need | Good for |
|---|---|---|---|---|
| **X2 Sim + MC** ✅ | X2 | MuJoCo + the real motion-control binary + AimDK | x86_64, Ubuntu 22.04, 16 GB RAM, **no GPU**; Docker or local | Test the exact same `ros2 run py_examples ...` code before touching the robot |
| **X2 RL Deploy** ✅ | X2 | MuJoCo | ROS 2 Humble, ONNX Runtime 1.23.2, PS5 gamepad | Drop in your own ONNX locomotion policy |
| `agibot_x2_urdf` ✅ | X2 Ultra / new / EDU | MuJoCo viewer, any URDF tool | `pip3 install mujoco` | Kinematics, reach checks, custom sim |
| A3 / A3 Ultra models ✅ | A3, A3 Ultra | MuJoCo (MJCF), RViz, MoveIt (SRDF), Isaac (USD) | — | Planning studies; no controller included |
| `sonic_for_a3` 🧪 | A3 / A3 Ultra | MuJoCo (AimRT) | GPU for training | Whole-body tracking, XR teleop in sim; policy controls **29 joints at 50 Hz** |
| D1 models ✅ | D1 Edu / Ultra, D1 MaxPro | Isaac Sim and MuJoCo (per product page); URDF folder in the MaxPro repo | — | Gait and payload tests. URDF location for Edu / Ultra not seen in the repo README ⚠️ unverified |
| **Genie Sim 3.x** ✅ | Genie **G2** (tier 1); Franka FR3, UR5, ALOHA, Piper, ARX (reference) | Isaac Sim 6.2 (PhysX or Newton backend) | NVIDIA GPU, Docker, Python 3.12 | Manipulation benchmark (**200+ tasks**), LLM scene generation, 3DGS scene reconstruction, VR / keyboard teleop, synthetic data |
| GenieSim Assets ✅ | — | USD assets | Hugging Face / ModelScope | **5,140** objects for retail, industry, catering, home, office scenes |
| Genie Sim World ✅ | — | spatial world model | separate CUDA environment | Photorealistic 3D scene from one panorama photo — a quick "digital twin" of a room |
| GE-Sim 2.0 / Genie Envisioner ✅ | G1 / G2 | learned video world model | high-end GPU | Policy evaluation in a neural simulator (research) |

Genie Sim ships `AGENTS.md` and `SKILL.md` recipes so an AI coding assistant can drive the simulator directly — a real time-saver in a 48-hour build.

## AI stack

| Layer | What exists | Access | Hackathon reality |
|---|---|---|---|
| Manipulation VLA | **GO-1**, **GO-1 Air** ✅ | open weights + fine-tune code (non-commercial) | Inference about **7 GB** GPU memory; action-expert-only fine-tune about **24 GB**; full fine-tune about **70 GB**. Policy-server mode lets a laptop GPU serve a robot. |
| | **GO-2** ✅ | inside Genie Studio only | Needs AGIBOT staff and a G-series robot |
| | **GO-3 Preview** 🧪 (2026-10-29) | not released; open-source announced for end of 2026 | Not usable now |
| | **ACoT-VLA** ✅ (CVPR 2026) | open code, Apache-2.0 | Research baseline behind GO-2's action chain-of-thought |
| Locomotion | X2 built-in controller ✅; your own ONNX policy via `x2_rl_deploy` ✅; X1 RL training code ✅; SONIC port for A3 🧪; BFM / GCFM motion models 🧪 (not public) | mixed | Use the built-in walker; do not train locomotion in 48 hours |
| Interaction | LinkSoul cloud agent + AgentSDK ✅; on-robot TTS / ASR / audio services ✅; **WITA-Omni** 🧪 (full-duplex, 100+ languages claimed) not public | LinkSoul account needed | Fastest path to a talking robot: `PlayTts` service + your own LLM, or the AgentSDK sample |
| Event / memory agent | **LIFE / RoboBeats** ✅ | open code (Apache-2.0), runs on any webcam | "Tell me when X happens" on a video stream — robot-agnostic |
| Skill tools | LinkCraft (video → motion), SkillForge (X2 pick-and-place training, limited trials), Genie Master agent framework 🧪 | AGIBOT tools | Ask staff; not self-serve |
| Datasets | AgiBot World Alpha / Beta (G1), **AgiBot World 2026** (G2, **LeRobot v2.1** format), AgiBot Digital World (sim), GenieSim3.0-Dataset (10,000+ h synthetic), Challenge 2025 / 2026 sets | Hugging Face `agibot-world` | CC BY-NC-SA 4.0. Beta / Alpha are gated (accept terms); download per task |

- **LeRobot support:** the GO-1 code base is built on **LeRobot dataset v2.1**; a LIBERO → LeRobot conversion script is included, and AgiBot World data is converted with the community `any4lerobot` tool. AgiBot World 2026 is already published in LeRobot v2.1 format.
- **Teleoperation and data collection:** `UPPERBODY_REMOTE_SPLIT` mode (X2), AGIBOT VR Kit, OmniGlove SDK, OmniHand toolbox (data collection), MEgo robot-free kit 🧪, Genie Sim teleop (VR or keyboard), `sonic_for_a3` XR retargeting. The org also hosts `IsaacCapture`, a copy of NVIDIA's Isaac Capture teleop / egocentric capture stack.
- **Genie Studio** (per its public page): data-collection templates, training with third-party models (RDT, Pi0, OpenVLA, GR00T) and GO-1, simulation evaluation, one-click deployment. Version 2.0 (2026-10-26) adds Flywheel (data + training), Agent (drag-and-drop task orchestration) and Monitor (fleet operations).

See [Papers and research](AGIBOT-Papers-and-Research.md) for the papers and licences behind each model.

## Compute, sensors and connectivity

### X2 (from the AimDK hardware pages)

| Item | X2 Ultra / Ultra (new version) | X2 EDU |
|---|---|---|
| Motion-control computer (PC1) | RK3588 — **off limits for your code** (`10.0.1.40`) | RK3588 — off limits (`10.0.1.40`) |
| Developer computer (PC2) | **Jetson Orin NX 16 GB**, 157 TOPS, 8-core A78AE, 512 GB storage (`10.0.1.41`) | none |
| Interaction computer (PC3) | yes (voice, face, head touch) | none |
| LiDAR | RoboSense **E1R**, 120° × 90°, 10 Hz point cloud (`PointXYZIRT`), 200 Hz IMU | — |
| RGB-D | Orbbec **Gemini 335**, 1280 × 720 RGB + depth at 30 Hz; depth in mm; **depth is not aligned to RGB** since v1.1.0 | — |
| Stereo RGB (head front) | 2064 × 1552 (new version 2048 × 1536), 10 Hz, FOV 156° × 120° | — |
| Rear RGB | same sensor class, 10 Hz; partly blocked by the neck handle; rotated 90° on the new version | — |
| Interaction RGB | up to 2608 × 1960, FOV 110° × 80° | — |
| IMU | chest + torso at **500 Hz** | chest + torso |
| Other | head touch (100 Hz), GNSS `NavSatFix` at 1 Hz, mic array, speaker, face screen, LED strip | not stated in the docs |
| USB | Ultra: 2 × Type-A + 2 × Type-C; new version: 3 × Type-C only | 1 × Type-C (RK3588 side) |
| Ethernet | 2 × GbE (reach Orin NX and RK3588) | 1 × GbE |
| Power out | 12 V / 3 A and 48 V / 5 A (XT30) | same |
| Mobile network | 5G SIM slot | none |

- **USB side matters:** a device plugged into an RK3588 port is invisible to code on the Orin NX. Use the Orin NX ports.
- **Camera bandwidth:** raw streams are about **80–90 MB/s each** — subscribe only on the Orin NX; across machines use the `/compressed` topics.
- **Network:** wired — set your PC to `10.0.1.2/24`; robot hotspot — jump host at `192.168.88.88`. SSH credentials come from AGIBOT technical support.

### D1 and others (short)

| Robot | Compute and links (from SDK READMEs and product pages) |
|---|---|
| D1 Edu / Ultra | Robot at `192.168.234.1` (Wi-Fi, DHCP) or `192.168.168.168` (Ethernet, static). Expansion: Ethernet, USB, power, SBUS, UART. No LiDAR or depth camera as standard. |
| D1 Max | Wi-Fi `192.168.234.1`; Orin NX 16 GB, 2 × LiDAR, RTK on board (product page). |
| D1 MaxPro | Wi-Fi `192.168.12.1`, Ethernet `192.168.144.3`, Type-C `192.168.55.1`; front / rear video at `rtsp://192.168.144.3:8554/camf` and `/camb`. |
| A2 Ultra | Jetson Orin 64 GB + 16-core CPU (product page). |
| A3 Ultra | 700 TOPS embedded computer (product page). |
| G1 | Jetson AGX Orin 64 GB (product page). |

Full spec tables: [Product portfolio](AGIBOT-Products.md).

## First 60 minutes checklist

### A. X2 Ultra or X2 EDU

1. **Read the nameplate** on the back of the neck: ends in "X2 Ultra", "X2 Ultra -N" (new version) or "X2 EDU". This picks your URDF folder (`X2_URDF-v1.3.0` for Ultra, `v1.4.0` for the other two) and tells you whether sensors and an on-board computer exist.
2. **Ask AGIBOT staff for:** firmware version, the matching SDK package, SSH credentials, and whether the navigation / SLAM module is enabled. Ask where the remote controller is and who holds it.
3. **Connect by cable.** Plug into the rear SDK Ethernet port, set your PC to static `10.0.1.2`, mask `255.255.255.0`. Ping `10.0.1.41` (Ultra developer computer) or `10.0.1.40` (EDU). Wi-Fi is for debugging only.
4. **Choose where code runs.** Ultra: SSH into the Orin NX and use the **podman container** (`podman exec -it aimdk-dev bash`) — container-only becomes mandatory from v1.2.0. EDU: your own Ubuntu 22.04 + ROS 2 Humble laptop with the SDK in `~/aimdk`.
5. **Build:** `source /opt/ros/humble/setup.bash && cd ~/aimdk && colcon build && source install/local_setup.bash`.
6. **Verify the link:** `ros2 run py_examples get_mc_action` → expect a mode name such as `PASSIVE_DEFAULT` and status `100`. If nothing: `ros2 topic list`, then `ros2 topic echo /aima/sm/system_state`.
7. **Stand up** (robot upright, both feet flat, spotter ready): `ros2 run py_examples set_mc_action JD`, then `ros2 run py_examples set_mc_action SD`.
8. **Hello-world motion:** `ros2 run py_examples preset_motion_client` → arm area `2` (right arm), preset ID `1002` → the robot waves.
9. **Read sensors:** `ros2 topic hz /aima/hal/imu/chest/state` (expect about 500 Hz) and `ros2 topic echo /aima/hal/joint/arm/state --once`. On an Ultra also check `/aima/hal/sensor/lidar_chest_front/lidar_pointcloud` and `/aima/hal/sensor/rgbd_head_front/rgb_image/compressed` in Foxglove or RViz.
10. **Walk slowly:** register your input source, then `ros2 run py_examples mc_locomotion_velocity` at low speed in a clear area. Try `ros2 run py_examples upper_body_control` for arm motion.
11. **Make it talk** (Ultra only): call the `PlayTts` service; for your own speech stack switch the agent to `only_voice` or use `Develop_Audio_ROS`.

### B. D1 Edu / Ultra

1. Confirm it is **Edu or Ultra** (a Pro has no SDK) and that the battery is well charged.
2. Join the robot's Wi-Fi (SSID and password on the label on the robot's right side) or cable in with a static `192.168.168.x` address.
3. SSH into the robot (login details are in the repo's `docs/deploy.md`) and set `target_ip` in `/opt/export/config/sdk_config.yaml` to **your PC's IP**; for cable or non-default subnets also set `SDK_CLIENT_IP` in the motion-control start script. **Reboot the robot.**
4. On your PC (Ubuntu 22.04): `git clone https://github.com/AgibotTech/agibot_D1_Edu-Ultra`, then `cd demo/zsl-1/python/examples` and set `initRobot("<your IP>", 43988, "192.168.234.1")`.
5. Run `python3 highlevel_demo.py` → verify with `checkConnection()`, then `standUp()`.
6. Hello-world motion: `move(0.2, 0, 0)` for two seconds, `move(0, 0, 0)`, `shakeHand()`, `lieDown()`.
7. Read sensors: `getRPY()`, `getBodyGyro()`, battery level, joint angles.
8. Only then try `lowlevel_demo` — with the dog on a stand.

### C. No robot yet

1. X2: download `sim_mujoco-x86` + `mc-x86` + the SDK from the docs toolbar, run the Docker deployment, and repeat steps A6–A10 in simulation.
2. Manipulation: `pip install -e source/geniesim_cli/` → `geniesim docker build` → `geniesim docker up` → `geniesim doctor` (needs an NVIDIA GPU and a large download — start it early).
3. Perception or agent work: clone `LIFE` and run the webcam demo, or the AgentSDK hospital-triage sample with your own knowledge base.

## Known gotchas and safety

- **Never build or run your code on the X2 motion-control computer** (PC1, `10.0.1.40`) — explicitly prohibited; warranty and support are void if you do.
- **Low-level joint commands have no watchdog.** If your node dies, the last command stays active. Publish at a fixed rate and send a safe pose or zero command on exit. Keep the robot on a gantry or have a spotter for any joint-level or RL work.
- **Do not launch many ROS nodes at once while the robot is standing or walking** (limit: about 2 nodes per second). A burst of DDS discovery traffic can starve the motion controller and the robot can **fall**. Start everything in zero-torque or damping mode first.
- **Balanced stand needs both feet on the ground** before `STAND_DEFAULT`. Low battery can leave the legs unpowered ("legs don't respond, arms move slowly").
- **The remote controller wins.** SDK velocity commands are dropped while the remote is active and until its source times out (1 s after the last non-zero command).
- **Do not use or modify built-in input sources** (`rc`, `app_proxy`, `vr`, `interaction`, `pnc`, and especially `linkswarm`).
- **Preset motions only work in Stable Stand.** Old mode names from before v0.8 (`ZERO_TORQUE_DEFAULT`, `RUN_DEFAULT`, `JOINT_FREEZE`, `STAND_BODY_CONTROL`, `SOFT_EMERGENCY_STOP`) must not be used — many blog examples still show them.
- **SDK ↔ firmware mismatch** is the most likely first-hour failure. Same for the D1 Max (compatibility table in the README) and D1 MaxPro.
- **Navigation, SLAM and vision are not plug-and-play:** SLAM / navigation are optional modules that need after-sales activation; the vision interface page is still "to be enabled". Plan your own perception on the Orin NX.
- **Depth ≠ RGB pixels** since v1.1.0: register depth to colour yourself with the `/tf_static` transform and both `CameraInfo` messages. RGB and depth frames are not time-synchronized.
- **`cv_bridge` crash on the robot** (`Assertion failed: s >= 0`): link against the Ubuntu OpenCV, not the NVIDIA one.
- **Data loss:** firmware up / downgrades reformat the disks; never store work in `$HOME/aimdk*`; a factory reset wipes `$HOME`. Push to git often.
- **Container build pulls from mirrors in mainland China** (NJU, Aliyun, Tsinghua). From Leukerbad this may be slow or blocked — check reachability first or ask staff for a pre-built image.
- **X2 payload is small:** about 1 kg per arm over the full range. Design tasks around light objects.
- **X2 walking speed limits are per speed mode**; off-road mode (`LOCOMOTION_STEP`) cannot be selected through the speed-mode service — it is entered as a motion mode.
- **D1 under SDK control has no low-battery protection** (repo FAQ): it can cut power while moving. Watch the battery.
- **D1 config resets:** after a firmware or controller update the `sdk_config.yaml` edits are lost; deleting the IP line stops the motion service from starting; setting `SDK_CLIENT_IP` can disable the remote if the network comes up late.
- **D1 temperature rating:** Pro / Edu are rated from **0 °C** — November evenings in Leukerbad can be colder. D1 Max / MaxPro are rated to −20 °C.
- **Public networks:** AGIBOT advises against putting robot and dev PC on a shared or public network. Use a direct cable or a private router, not the venue Wi-Fi.
- **Licences:** GO-1, datasets and world models are **non-commercial** (CC BY-NC-SA 4.0). Fine for the hackathon, a problem for a start-up pitch — say so if asked.

## Community resources

| Resource | What you get | Link |
|---|---|---|
| AimDK_X2 docs (English and Chinese) | Interface reference, Python and C++ examples, FAQ, changelog, feedback form | [x2-aimdk.agibot.com](https://x2-aimdk.agibot.com/en/latest/) |
| AgibotTech GitHub | SDKs, URDFs, simulators, research code (about 35 public repos, many updated this month) | [github.com/AgibotTech](https://github.com/AgibotTech) |
| Hugging Face `agibot-world` | GO-1 weights, datasets, sim assets, world models | [huggingface.co/agibot-world](https://huggingface.co/agibot-world) |
| OpenDriveLab AgiBot-World | GO-1 code, dataset tooling, issue tracker | [GitHub](https://github.com/OpenDriveLab/AgiBot-World) |
| AGIBOT open platform | LinkSoul / AgentSDK docs and downloads (JavaScript-only site, could not be read in this pass) | [open.agibot.com](https://open.agibot.com/) |
| Product manuals and open-source downloads | PDF manuals, brochures, app downloads | [agibot.com/DOCS/OS](https://www.agibot.com/DOCS/OS) |
| AGILINK hands site | Hand and gripper product pages | [agilink-ai.com](https://www.agilink-ai.com) |
| RoboColiseum | Public Genie Sim benchmark leaderboard | [robocoliseum.ai](https://robocoliseum.ai/) |
| AimRT | Middleware docs (X1 / A3 sim) | [aimrt.org](https://aimrt.org/) |
| AgiBot World Challenge | Annual competition (IROS 2025, ICRA 2026) with baselines and data | [challenge data](https://huggingface.co/datasets/agibot-world/AgiBotWorldChallenge-2026) |

AGIBOT states its ecosystem covers **255 universities, 511 companies and 80,000+ developers** (Innovation Day, 2026-10-29, company figure). No public Discord or forum was found in this pass ⚠️ unverified. On site, the AGIBOT (or Minth Group / partner) engineers are the real support channel — SSH credentials, firmware-matched SDKs and optional modules all go through them.

## Sources

- [AimDK_X2 documentation — home and table of contents (v1.1.0)](https://x2-aimdk.agibot.com/en/latest/)
- [AimDK_X2 — Get the SDK](https://x2-aimdk.agibot.com/en/latest/get_sdk/index.html)
- [AimDK_X2 — Quick Start: development modes and network](https://x2-aimdk.agibot.com/en/latest/quick_start/prerequisites.html)
- [AimDK_X2 — Develop in a Container](https://x2-aimdk.agibot.com/en/latest/quick_start/container_dev.html)
- [AimDK_X2 — Build the SDK and run an example](https://x2-aimdk.agibot.com/en/latest/quick_start/run_example.html)
- [AimDK_X2 — On-board Computer](https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/onboard_computer.html)
- [AimDK_X2 — User Debug Interfaces](https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/user_debug_interface.html)
- [AimDK_X2 — Secondary Development Interfaces](https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/SDK_interface.html)
- [AimDK_X2 — Sensor Overview](https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/sensor_fov.html)
- [AimDK_X2 — Motion Mode Switching](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/modeswitch.html)
- [AimDK_X2 — Locomotion Control](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/locomotion.html)
- [AimDK_X2 — MC Control Signal Configuration](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/MC_control.html)
- [AimDK_X2 — Upper Body Control](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/upper_body_control.html)
- [AimDK_X2 — End Effector Control](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/endeffector.html)
- [AimDK_X2 — Joint Control](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/joint_control.html)
- [AimDK_X2 — Sensor Interfaces](https://x2-aimdk.agibot.com/en/latest/Interface/hal/sensor.html)
- [AimDK_X2 — SLAM (optional)](https://x2-aimdk.agibot.com/en/latest/Interface/perception/SLAM.html)
- [AimDK_X2 — Navigation (optional)](https://x2-aimdk.agibot.com/en/latest/Interface/perception/navigation.html)
- [AimDK_X2 — Voice Control](https://x2-aimdk.agibot.com/en/latest/Interface/interactor/voice.html)
- [AimDK_X2 — LinkSoul Cloud Interaction](https://x2-aimdk.agibot.com/en/latest/Interface/interactor/linksoul.html)
- [AimDK_X2 — System Modes and Developer Modes](https://x2-aimdk.agibot.com/en/latest/Interface/system_state/index.html)
- [AimDK_X2 — Python examples](https://x2-aimdk.agibot.com/en/latest/example/Python.html)
- [AimDK_X2 — FAQ](https://x2-aimdk.agibot.com/en/latest/faq/index.html)
- [AimDK_X2 — Temporary Transitional Solutions](https://x2-aimdk.agibot.com/en/latest/faq/temp_works.html)
- [AimDK_X2 — Boundaries and Disclaimer](https://x2-aimdk.agibot.com/en/latest/end_notes.html)
- [AimDK_X2 — X2 RL Deployment](https://x2-aimdk.agibot.com/en/latest/rl_contents.html)
- [AimDK_X2 — X2 MuJoCo Motion-Control Simulation](https://x2-aimdk.agibot.com/en/latest/sim_contents.html)
- [AimDK_X2 — Changelog](https://x2-aimdk.agibot.com/en/latest/changelog.html)
- [GitHub — AgibotTech organisation](https://github.com/AgibotTech)
- [GitHub — AgibotTech/agibot_x2_urdf](https://github.com/AgibotTech/agibot_x2_urdf)
- [GitHub — AgibotTech/agibot_D1_Edu-Ultra (README, docs/deploy.md, docs/api_zsl-1.md, docs/api_lowlevel.md, docs/faq.md)](https://github.com/AgibotTech/agibot_D1_Edu-Ultra)
- [GitHub — AgibotTech/Agibot_D1_Max](https://github.com/AgibotTech/Agibot_D1_Max)
- [GitHub — AgibotTech/Agibot_D1_MaxPro](https://github.com/AgibotTech/Agibot_D1_MaxPro)
- [GitHub — AgibotTech/agilink_omnihand_sdk](https://github.com/AgibotTech/agilink_omnihand_sdk)
- [GitHub — AgibotTech/agilink_omniglove_sdk](https://github.com/AgibotTech/agilink_omniglove_sdk)
- [GitHub — AgibotTech/agibot_agentsdk_sample_code](https://github.com/AgibotTech/agibot_agentsdk_sample_code)
- [GitHub — AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)
- [GitHub — AgibotTech/genie_sim_robot_model](https://github.com/AgibotTech/genie_sim_robot_model)
- [GitHub — AgibotTech/A3-A3U-robot-model](https://github.com/AgibotTech/A3-A3U-robot-model)
- [GitHub — AgibotTech/sonic_for_a3](https://github.com/AgibotTech/sonic_for_a3)
- [GitHub — AgibotTech/IsaacCapture](https://github.com/AgibotTech/IsaacCapture)
- [GitHub — AgibotTech/agibot_x1_infer](https://github.com/AgibotTech/agibot_x1_infer)
- [GitHub — OpenDriveLab/AgiBot-World (GO-1 README)](https://github.com/OpenDriveLab/AgiBot-World)
- [Hugging Face — agibot-world organisation](https://huggingface.co/agibot-world)
- [Genie Studio product page](https://genie.agibot.com/en/geniestudio)
- [AGIBOT — Genie Studio 2.0 launch (2026-10-26)](https://www.agibot.com/article/231/detail/130.html)
- [AGIBOT — Innovation Day 2026: Link-U OS 1.0, ecosystem figures (2026-10-29)](https://www.agibot.com/article/231/detail/131.html)
- [AGIBOT — GO-3 Preview (2026-10-29)](https://www.agibot.com/article/231/detail/133.html)
- [AGIBOT — X2 product page](https://www.agibot.com/products/X2)
- [AGIBOT company profile (first pass)](AGIBOT.md) · [Product portfolio](AGIBOT-Products.md) · [Papers and research](AGIBOT-Papers-and-Research.md)
