---
type: dev-cheatsheet
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Developer cheat sheet — how to program each platform

> Generated 2026-11-14 15:57 from each company's Developer guide (TL;DR section). Open the full guide for SDK tables, the first-60-minutes checklist and gotchas.

[Start here](00-START-HERE.md)

## AGIBOT

- **X2 humanoid = ROS 2 Humble.** The official SDK is **AimDK_X2** (Python + C++, Ubuntu 22.04). You call ROS 2 services (`/aimdk_5Fmsgs/srv/...`) and publish topics (`/aima/...`). Hello-world is three shell commands: read mode → stand → wave.
- **D1 quadrupeds = plain C++ / Python library, no ROS needed.** `standUp()`, `move(vx, vy, yaw_rate)`, `getRPY()`, plus `sendMotorCmd()` for joint-level control. Each D1 size (Edu/Ultra, Max, MaxPro) has its **own, incompatible** SDK repo.
- **Hands and grippers = `agilink_omnihand_sdk`** (C++ / Python / ROS 2 Humble, Linux and Windows) over USB — works on any vendor's arm.
- **G1 / G2 wheeled manipulators and A2 = no public SDK.** They are driven through **Genie Studio** (commercial platform, "GDK" for real-robot control) and LinkSoul / LinkCraft no-code tools. You need AGIBOT staff.
- **No robot slot? Still productive:** X2 MuJoCo simulation runs on a laptop without a GPU; **Genie Sim** (Isaac Sim, G2 model, ROS 2 + MoveIt) and **GO-1** open weights (about **7 GB** GPU memory for inference) are public.

→ [Full developer guide](Companies/AGIBOT/AGIBOT-Developer-Guide.md) · [Profile](Companies/AGIBOT/AGIBOT.md)

## Binabik AI

- **Workflow, not joint commands:** demonstrate a task once (by hand or teleoperation) → Skill Engine splits it into steps and maps each to a library skill → Binabik Sim varies parts, positions and lighting → the same program runs on the robot. Company claim: "first demonstration to a running robot in **days**", so a 48-hour build only works with skills that already exist in their library.
- **Access is gated:** Studio is "Request access" via the contact form; `docs.binabik.ai` exists but sits behind a login wall. **The on-site engineers are your SDK.**
- **Robots:** publicly named targets are **AgiBot G2** and **Galaxea R1 Pro** (both vendors are on site). Public repos also show work on **Unitree G1** in Isaac Lab simulation (forks, not a product statement).
- **Self-serve today:** `mcp-rosbags` (LLM-queryable ROS 1 / ROS 2 bag analysis, Apache-2.0) and `mcp-lab` (test bench for MCP servers). Both are Python and run on a laptop in minutes, on any vendor's robot data.
- **Decision rule:** build on Binabik only if, within the first 30 minutes, they confirm (a) a robot you can book, (b) Studio / BDK access for your team, (c) the skills you need already exist. Otherwise use the robot vendor's own SDK and keep `mcp-rosbags` as a debugging and demo aid.

→ [Full developer guide](Companies/Binabik-AI/Binabik-AI-Developer-Guide.md) · [Profile](Companies/Binabik-AI/Binabik-AI.md)

## coprod Inc.

- **One Python package, `cosystem`** (C++ core, Python bindings): scan the EtherCAT bus, get a handle per device, set a mode, write targets, read telemetry. 🧪 Preview only — not on PyPI, not on GitHub.
- **Low-level and joint-centric.** You command **torque, velocity or position per axis** and tune gains yourself. There is no navigation, manipulation, skill or behaviour layer.
- **Hard real time over EtherCAT:** **1 kHz** typical loop, **< 20 µs** jitter, distributed clocks, on a **real-time Linux** host that you (or coprod) supply.
- **Simulation = one browser demo.** The co:dodo simulator (MuJoCo in WebAssembly, **200 Hz** physics, **50 Hz** ONNX policy) runs with no install, but there is no published URDF / MJCF / USD and no training repo.
- **AI stack = none.** No pretrained manipulation policy, VLA, dataset or teleop pipeline. Bring your own brain (laptop, another vendor's robot, or a D-Robotics RDK board) and use coprod as the actuation layer.

→ [Full developer guide](Companies/coprod/coprod-Developer-Guide.md) · [Profile](Companies/coprod/coprod.md)

## D-Robotics

- **It is an Ubuntu ARM64 computer with an AI accelerator (BPU).** SSH in (`sunrise@192.168.127.10`), write Python or C++, use ROS 2. No CUDA, no TensorRT.
- **Fastest path = pre-converted models.** Clone [rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo), run a `download_model.sh` + `main.py` pair, get YOLO detection / pose / segmentation, depth, speech or a small VLM on the BPU in minutes.
- **ROS 2 path = TogetheROS.Bot (TROS).** `sudo apt install tros-humble` adds BPU-accelerated camera, codec, inference and web-render nodes on top of stock ROS 2. Your robot from another vendor then just subscribes to topics.
- **Custom models cost time.** ONNX must be quantized (INT8) and compiled per chip with the OpenExplorer Docker toolchain on an x86 PC (`.bin` for X3 / X5, `.hbm` for S100 / S100P / S600). Budget **half a day** the first time; avoid it if a zoo model is close enough.
- **Robot learning is documented but narrow.** One worked recipe: LeRobot **ACT on SO-100 arms**, inference on RDK S100 / X5 BPU. Pi0 and ACT also appear as model-zoo submodules; treat anything beyond ACT as experimental.

→ [Full developer guide](Companies/D-Robotics/D-Robotics-Developer-Guide.md) · [Profile](Companies/D-Robotics/D-Robotics.md)

## Dobot Robotics

- **Arms = plain TCP sockets.** Every 6-axis arm on V4 firmware (CRA, CRAF, CR 30H, Nova 2 / 5, Magician E6) takes ASCII commands such as `MovJ(...)` on port **29999** and streams a 1,440-byte state packet every **8 ms** on port **30004**. No licence, no vendor runtime; Python wrapper is one file (`dobot_api.py`).
- **Streaming control tops out at about 33 Hz.** `ServoJ` / `ServoP` (joint / Cartesian target following) are the "real-time" interface; Dobot recommends a **30 ms** call interval (minimum point time 0.02 s). There is **no public joint-torque command** for the arms.
- **ROS 2 Humble is first-class.** `DOBOT_6Axis_ROS2_V4` (MIT, V4.6.5) ships URDF / Xacro, MoveIt configs and Gazebo launch files for **12 models** including Nova 2, Nova 5, E6, CR5 and CR30H.
- **Learning stack is thin but real.** Official LeRobot-format dataset + ACT checkpoint for CR5A (simulation), X-Trainer teleop / HDF5 recorder, Isaac Gym RL frameworks for Atom and the quadruped, DobotTrack VLA weights. The flagship models (**KONGYI / DobotWAM, DOBOT-VLA, ROM-1**) are closed.
- **Legged and humanoid robots use DDS + RPC, not the arm protocol.** Atom: CycloneDDS at about **833 Hz** plus RPC from the on-board PC2. Rover X1: gRPC high level (works over Wi-Fi) and CycloneDDS low level (wired only).

→ [Full developer guide](Companies/Dobot/Dobot-Developer-Guide.md) · [Profile](Companies/Dobot/Dobot.md)

## Flexiv Robotics

- **One SDK, two generations.** Everything goes through **Flexiv RDK** (C++ / Python, Apache-2.0). **RDK v1.9.x** drives **Rizon / AICO** (robot software v3.11.x); **RDK v2.x** drives **Enlight / MICO** (robot software v3E.x). The two APIs are **not interchangeable** — ask the booth which arm and which robot software version you have before installing anything.
- **Fast path for 48 hours:** Python + **non-real-time (NRT) primitives and Cartesian motion-force commands**. No real-time kernel, works from Linux, macOS or Windows, tolerates up to **1000 ms** round-trip latency (even wireless LAN).
- **Full power:** **1 kHz** real-time streaming of joint torque, joint position / impedance or Cartesian motion + force. Needs the **Professional** RDK licence, **wired LAN**, **< 1 ms** round-trip latency and Linux or macOS.
- **ROS 2:** `flexiv_ros2` (Humble / Jazzy) with ros2_control, MoveIt and a fake-hardware mode. It exposes joint position / joint impedance — for force-controlled contact use the RDK directly.
- **AI:** no pretrained Flexiv policy or VLA is public. The supported pipeline is **Flexiv Trainer**: leader-follower teleop → **LeRobot-format** episodes → train → rollout. It needs a leader arm *and* a follower arm.

→ [Full developer guide](Companies/Flexiv/Flexiv-Developer-Guide.md) · [Profile](Companies/Flexiv/Flexiv.md)

## Galaxea

- **R1 Pro / R1 Lite = ROS 2 Humble on Ubuntu 22.04**, running on the robot's own **Jetson AGX Orin 32 GB**. The vendor stack ("ATC ROS2 SDK", latest **V2.5.0**, 30 Oct 2026) is pre-installed; you start it with `galaxea --sdk start --feature-pkg R1ProBody` and then simply publish / subscribe: commands on `/motion_target/*`, feedback on `/hdas/*`.
- **Three control levels are openly documented**: Cartesian end-effector pose and chassis twist (high), joint-position targets with velocity limits (mid), and per-motor `p_des / v_des / kp / kd / t_ff` impedance commands (low). The public docs show no "EDU unlock" gate for low-level access.
- **LEMO = the same idea on a small box**: RK3588 controller, ROS 2 Humble workspace (`galaxea_lemo`), browser dashboard on port **8000**, 200 Hz arm control, leader arms for teleop. **A1Z alone = a plain Python SDK** over SocketCAN (250 Hz loop, gravity compensation, FK / IK), no ROS required.
- **AI is server / client**: a GPU machine (more than **8 GB VRAM**, RTX 4090 recommended) runs the **G0.5** policy server; a thin robot-side client streams camera + joint observations over WebSocket and executes the returned action chunks. Weights are public but **non-commercial**.
- **Data path is LeRobot-format end to end**: teleoperate (VR headset or leader arms) → record MCAP / rosbag / HDF5 → convert with `GalaxeaLeRobotToolkit` → fine-tune G0.5, π0.5, SmolVLA or a diffusion policy → deploy with the same client.

→ [Full developer guide](Companies/Galaxea/Galaxea-Developer-Guide.md) · [Profile](Companies/Galaxea/Galaxea.md)

## Galbot

- **One official SDK: GalbotSDK** (C++ and Python, Apache-2.0, **V1.10.0, 2026-09-22**). `from galbot_sdk.g1 import GalbotRobot`, call `init()`, then blocking or streaming commands. No ROS needed.
- **Two ways to run code:** on the robot's Orin over SSH (lowest friction, works over Wi-Fi) or from an Ubuntu laptop over a **wired link through Galbot's Ethernet adapter board** (PC `192.168.1.99`, HPU `192.168.1.88`, XCU `192.168.1.66`).
- **SDK and robot firmware must match:** SDK 1.10.x needs robot system **GBS 1.18.x**. Check with `galbot_sdk check-version` before anything else.
- **Navigation only works after you build a map** of the venue (push the robot around by hand, via a web tool on the robot). A robot without a map can sit in `ABNORMAL` mode and refuse all commands.
- **Bring your own model:** the SDK has a documented pattern for VLA / RL policies — synchronized camera + joint observation in, **23-D joint action chunks out at 20 Hz** (tutorial example 5). Data collection uses the TM01 leader arms and converts to **LeRobot** format.

→ [Full developer guide](Companies/Galbot/Galbot-Developer-Guide.md) · [Profile](Companies/Galbot/Galbot.md)

## Genisom AI

- **Two robot families, two SDKs, both C++ over UDP.** L1 / L1-W use `genisom_L1_sdk` (JSON over UDP, ports **8081 / 8080**). M1 and L2 use `genisom_robot_sdk` ("GEN2", UDP port **8082**). In both cases the robot's Wi-Fi access point answers at **192.168.234.1**.
- **You command body velocity, not joints.** High-level calls: stand, lie down, posture modes, velocity (`Move` / `MoveVelocity` / `SetRemote`), plus IMU, odometry, joint and battery read-back. Joint-level PD / torque control exists **only for the L1** (shared memory on the robot, **1 kHz**), not for M1 or L2.
- **Control is arbitrated.** Being connected does not mean you may drive. The phone app beats the SDK on M1 / L2; on the L1 you must request SDK control rights first. Close the app before your first motion test.
- **No official ROS 2 driver and no Python package for the current SDKs.** ROS 2 enters through RoamerX Lite (Humble + Nav2). Python enters through the legacy L1 SDK (unmaintained), the documented JSON-over-UDP protocol, or a thin wrapper you write yourself.
- **Start in simulation today.** MATRiX v1.1.2 (MuJoCo + Unreal Engine 5, Linux x86_64) runs L1, L1-W, M1-class and arm-equipped models with built-in locomotion and publishes camera / LiDAR / IMU over Zenoh. Download it early — the runtime is several GB.

→ [Full developer guide](Companies/Genisom-AI/Genisom-AI-Developer-Guide.md) · [Profile](Companies/Genisom-AI/Genisom-AI.md)

## Leadshine Technology

- **One SDK for all hands: `LHandProLib`** — C++ library (namespace `lhplib`) with a C API and a Python `ctypes` wrapper. Current manual **v1.8 (2026-09-16)**, latest package **20261031**. Builds for Linux x86_64 / i386 / aarch64, Windows, macOS arm64.
- **You own the bus, the SDK owns the protocol.** You open EtherCAT / CAN FD / RS485 (or plain CAN on the DH2116), register a *send callback*, and feed received bytes back into the SDK. Ready-made examples exist for every bus in C++ and Python.
- **Control is per joint:** target angle (°) or stroke position (0–10000), speed, and a current limit in per-mille (‰). Modes: position, velocity, torque, and two hybrids. Built-in gestures via `play_gesture`.
- **ROS 2 Humble on Ubuntu 22.04** is the supported robot middleware: a service-based control node, a `/joint_states` bridge for RViz2, tactile topics, C++ and Python demos.
- **Simulation = URDF + MJCF** (Apache-2.0 repo) plus an SDK **dry-run mode**. There is **no AI stack** (no policies, datasets, VLA, LeRobot) and **no public SDK for the PJ3 / HJ2 joint modules**.

→ [Full developer guide](Companies/Leadshine/Leadshine-Developer-Guide.md) · [Profile](Companies/Leadshine/Leadshine.md)

## Magiclab Robotics

- **One SDK per robot, C++20 with Python 3.10 bindings**, BSD-3-Clause, on GitHub (`magicdog_sdk`, `magicbot-z1_sdk`, `magicbot-gen1_sdk`, `magicdog-w_sdk`, `magicdog-y1_sdk`). You build it on **your own Ubuntu 22.04 laptop**; Mac and Windows are not supported, and the robot's on-board PC is not a development environment.
- **Wired Ethernet is the supported path.** Laptop on the robot's subnet (**MagicDog: 192.168.55.10, robot at 192.168.55.200**; **Z1: 192.168.54.111**), plus a **multicast route** on that interface. Without the route most calls fail.
- **Two control levels**: high-level (stand, gaits, trick actions, joystick-style velocity, SLAM / navigation) and low-level (per-joint commands with gains, state at **500 Hz**).
- **SDK access is edition-locked**: MagicDog **EDU** and Z1 **Development Version** only. The phone app and the SDK **cannot control the robot at the same time**.
- **AI stack is "bring your own"**: no vendor VLA is exposed through the robot SDK. What is open: Magic-W0 weights (manipulation, GPU needed), a pi0 recipe for Gen1, and an RL → MuJoCo → real pipeline for Z1 locomotion. For a 48-hour build, plan on **high-level SDK + your own perception / LLM on a laptop**.

→ [Full developer guide](Companies/Magiclab/Magiclab-Developer-Guide.md) · [Profile](Companies/Magiclab/Magiclab.md)

## Omnicor AI

- **You do not program OmniCor directly (as far as is public).** The stated workflow is: you bring a **trained model + a target hardware platform**, they deliver a deployment that fits your **power, speed and memory** limits.
- **It sits at the inference layer**, not the robot-control layer: below your policy / agent code, above the chip. Robot motion still goes through the robot vendor's SDK (AgiBot, Galbot, Unitree, ...).
- **Two named building blocks:** **OC Agent** (agentic deployment environment, software) and **OC Node** (in-house compute platform, hardware). Interfaces, APIs and specs for both: **not public**.
- **Models they say they deploy:** Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek (LLMs) and **OpenVLA, pi0.5** (robot VLAs). All are third-party open models you can already run yourself.
- **Hackathon play:** prototype with the open model on a laptop GPU first, then ask OmniCor to move it **on-board / offline**. Decide in the first hour whether their path fits in 48 h; if not, keep your laptop as the inference server.

→ [Full developer guide](Companies/Omnicor-AI/Omnicor-AI-Developer-Guide.md) · [Profile](Companies/Omnicor-AI/Omnicor-AI.md)

## OriginFlow

- **No public device SDK, API, docs portal or ROS 2 package** for OriginKitGen 1.0 (Glass + Band + Space). Live access to raw sEMG or PULSE outputs depends on what the team hands out on site — **ask first, commit second**.
- **There is one real public developer asset:** the gated Hugging Face dataset **OriginData preview sample** — **100.62 h, 7,717 episodes, 10.87M frames**, LeRobot v3.0 Parquet + MP4, with stereo egocentric video, 21-joint 3D hand pose, head SLAM pose, **per-finger force estimates (mN)** and language annotations.
- **Raw 16-channel sEMG and IMU are not listed among the released columns** — the public data is the *derived* layer (pose, force), not the muscle signal.
- **PULSE, CHORD, ORACLE and Fusion2Force have no public weights, API or model card.** You cannot run them yourself unless OriginFlow provides a runtime on site.
- **Any robot motion is your own bridge code** to another vendor's SDK (WUJI, Unitree, Flexiv, ROKAE, Dobot ...). Budget half a day for that bridge and a clutch / dead-man mechanism.

→ [Full developer guide](Companies/OriginFlow/OriginFlow-Developer-Guide.md) · [Profile](Companies/OriginFlow/OriginFlow.md)

## ROKAE Robotics

- **One SDK for every arm: xCore SDK** (C++, Python, C#, Android/Java), Apache-2.0, on GitHub under `RokaeRobot`. It talks to the xCore controller over **TCP/IP**; the real-time channel uses **UDP**.
- **Python = high-level only.** Point-to-point and linear moves, jog, drag teaching, force-control setup, I/O, registers. Enough for most 48-hour builds (pick-and-place, compliant contact, massage-style demos).
- **C++ = everything, including 1 kHz real-time mode** with five controller modes on xMate cobots: joint position, Cartesian position, joint impedance, Cartesian impedance, **direct torque**. Needs a wired direct link and ideally a PREEMPT_RT Linux PC.
- **ROS 2 Humble package (`rokae_ros2`)** with `ros2_control`, MoveIt 2 configs per model, URDF/xacro and Gazebo — the fastest way to get planning plus simulation without touching the SDK.
- **No downloadable AI models or datasets.** ROKAE supplies force-controlled hardware and control software; bring your own policy and perception, plus an external PC (the arm controller has no GPU).

→ [Full developer guide](Companies/ROKAE/ROKAE-Developer-Guide.md) · [Profile](Companies/ROKAE/ROKAE.md)

## SKYLANDX

- **There is nothing to `pip install`.** No public SDK, API reference, ROS package or GitHub org. Your first task is to ask SKYLANDX staff for the API / Rosbridge document and a unit with the interface enabled.
- **Live path (robot integration):** the scanner exposes a **WebSocket interface that speaks the Rosbridge protocol** — point clouds, images, IMU and pose, no custom driver. Supported ROS versions, topics and message types: not public.
- **Offline path (always works, no API needed):** scan → process in MetaCam Studio (Windows) or MetaCam Cloud (browser) → export **LAS / PCD / PLY / RCP / E57** point cloud, **OBJ** mesh, **PLY** 3DGS, **JPEG** panoramas → load into your own tools. Plan around this path; treat the live path as a bonus.
- **C01 LiDAR = raw sensor:** UDP point packets + 200 Hz IMU, 12–30 V. You bring the SLAM (advertised as plug-and-play with mainstream open-source algorithms). No public driver or packet spec.
- **It never moves a robot.** Output is pose, map and (optionally) navigation commands; another vendor's robot does the motion. Scanning itself is one button; the engineering is in what you do with the data.

→ [Full developer guide](Companies/SKYLANDX/SKYLANDX-Developer-Guide.md) · [Profile](Companies/SKYLANDX/SKYLANDX.md)

## Spirit AI

- **One Python SDK, on top of ROS 2 Humble.** `mozrobot` (Python ≥ 3.10, Ubuntu 22.04, x86_64 or aarch64) gives you `connect → enable_external_following_mode → capture_observation / send_action`. Commands are dictionaries of joint or Cartesian **position** targets plus a base **velocity**, streamed at **120 Hz**.
- **No public torque or impedance API.** The robot is force-controlled internally (joint torque sensors, collision detection), but the SDK exposes position streaming only. Force and impedance settings live in the HMI (MovaXHelper).
- **Fastest path to a working demo: VR teleop + scripted SDK skills + Nav2 goals.** Quest teleop, a data-collection app and a Dockerised lidar SLAM / Nav2 stack ship with the robot.
- **The learning path is π0.5 first, Spirit v1.5 second.** The docs give a full openpi (`pi05_moz`) fine-tune and deploy recipe for Moz1; the Spirit v1.5 repo only documents RoboChallenge inference and multi-GPU fine-tuning, with **no Moz1 config**.
- **Several pieces are gated by after-sales support:** the openpi adaptation, the sample dataset, the Isaac Sim asset pack and the navigation package. Ask the Spirit AI staff on site for them on day 1.

→ [Full developer guide](Companies/Spirit-AI/Spirit-AI-Developer-Guide.md) · [Profile](Companies/Spirit-AI/Spirit-AI.md)

## Unitree Robotics

- **One SDK for everything:** `unitree_sdk2` (C++) or `unitree_sdk2_python`. Both speak **CycloneDDS 0.10.2** over **Ethernet** on the robot's `192.168.123.x` network. Examples exist for Go2, Go2-W, B2, B2-W, A2, As2, G1, H1, H1-2, H2 and R1.
- **Two levels:** high-level clients (walk at a velocity, stand, sit, obstacle avoidance) work in minutes; low-level joint control (`LowCmd` position / velocity / torque + gains) requires switching off the factory controller and is where robots fall. **For 48 hours: stay high-level for legs, spend your time on perception, arms and task logic.**
- **ROS 2 is native, not a bridge:** `unitree_ros2` exposes the same DDS topics as ROS 2 topics (**Humble on Ubuntu 22.04 recommended**).
- **Check the variant first:** only **EDU** models (and partly Go2 X / As2 X) are open to the SDK. Go2 Air / Pro and the base G1 / R1 are not meant for secondary development.
- **Fastest path to a manipulation demo on G1:** `xr_teleoperate` (XR headset teleop + recording) → `unitree_lerobot` (convert, train ACT / Diffusion / Pi0 / Pi05 / GR00T) → `eval_g1.py`. Simulate the same pipeline in `unitree_sim_isaaclab`.

→ [Full developer guide](Companies/Unitree/Unitree-Developer-Guide.md) · [Profile](Companies/Unitree/Unitree.md)

## UniX AI

- **No self-serve route exists publicly.** No SDK download, API reference, URDF or forum. Your interface is whatever the UniX booth team hands you on day 1.
- **Most realistic mode: skill composition.** Wanda 2.0 and Panther ship with pre-loaded "L4-level" applications (tea service, tidying, wiping, guiding, restocking, waste sorting were all demoed publicly). Plan to **trigger existing skills + navigation goals from your own laptop** and add your own perception / LLM / UI layer on top.
- **Second mode: teach a skill by demonstration.** The UniFlex stack is an imitation-learning framework (semantic keypoints + trajectory imitation). Whether hackathon teams get the teaching / teleoperation tool is **not public — ask**.
- **Only Martian (biped) officially promises APIs**: "high-/low-level API interfaces" for secondary development, CAN FD bus, OTA. Languages, rates and docs are not public, and Martian is the least likely robot to be on site.
- **Decision rule:** if within the first hour the booth cannot show you (a) a way to send a command from your laptop and (b) a way to read at least one sensor or robot state, treat UniX as a **demo actor in a multi-vendor system**, not as your development platform.

→ [Full developer guide](Companies/UniX-AI/UniX-AI-Developer-Guide.md) · [Profile](Companies/UniX-AI/UniX-AI.md)

## WUJI

- **One SDK for everything:** `pip install wuji-sdk` (Python, CPython 3.8–3.14) or the C package. Same API pattern for Hand 2, Hand gen 1 and Glove: `device.{resource}().{get|set|subscribe|publish}()`.
- **Joint level only:** you send 20 joint targets at up to **1 kHz**. Hand 2 defaults to **MIT mode** (position + velocity + current feed-forward, per-joint kp / kd); whole-hand **position mode is Beta** and needs firmware **v3.0.0**. There is no grasp planner, no perception, no skill library.
- **Wired, static IP:** Hand 2 and Glove talk Ethernet on `192.168.1.x` (no DHCP); Hand gen 1 is USB. Budget one wired NIC (or a switch) per team laptop.
- **Fastest demo = glove teleop:** `examples/python/retargeting/1.teleop_real.py` mirrors a Wuji Glove onto a hand; official estimate **45 min** from unboxing. No glove free? Any source of 21 MediaPipe keypoints (webcam, VR headset) feeds the same `RetargetSession`.
- **Develop without hardware:** `wuji-description` has URDF / MJCF / MJX / USD for all hand revisions; a MuJoCo viewer check takes **10 min**. ROS 2 drivers (`wuji-ros2`) exist but target **Ubuntu 26.04 + ROS 2 Lyrical** only.

→ [Full developer guide](Companies/WUJI/WUJI-Developer-Guide.md) · [Profile](Companies/WUJI/WUJI.md)

## XREAL

- **Three stacks, do not mix them up:** (1) no code — glasses are a **USB-C DisplayPort monitor**; (2) **XREAL SDK 3.1.0** — a **Unity (C#)** package for One series / Air 2 Ultra, app runs on an **Android host** (Beam Pro or Samsung S24 / S25); (3) **Android XR** (Unity 6.5 + OpenXR) — **AURA only**.
- **Check the glasses model before you plan features.** Per the official compatibility table: **One series + XREAL Eye = 6DoF head pose + RGB camera, but no hand tracking, planes, image tracking, depth mesh or anchors.** Those need **Air 2 Ultra** (XREAL SDK) or **AURA** (Android XR).
- **Fastest 48-hour route:** render your operator UI (RViz, web dashboard, camera feed) on a laptop or robot computer and show it in the glasses. Zero SDK work, works in 5 minutes.
- **No official ROS 2 package, no Python / C++ / Unreal SDK, no simulation assets, no robot models.** Robot integration = your Unity app talks to ROS 2 over a bridge (ROS-TCP-Connector, rosbridge WebSocket or plain UDP).
- **Hard gotchas:** do **not** update the host to **Android 16**; turn off **Samsung DeX**; 6DoF on One + Eye needs the **latest glasses firmware**; the host's USB-C port is occupied by the glasses, so debug over **wireless ADB**.

→ [Full developer guide](Companies/XREAL/XREAL-Developer-Guide.md) · [Profile](Companies/XREAL/XREAL.md)
