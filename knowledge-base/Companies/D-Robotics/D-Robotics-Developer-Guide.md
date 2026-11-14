---
type: dev-guide
company: "D-Robotics"
slug: D-Robotics
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# D-Robotics — Developer Guide (hackathon edition)

⬆ [D-Robotics profile](D-Robotics.md) · [Product portfolio](D-Robotics-Products.md) · [Roadmap and strategy](D-Robotics-Roadmap-and-Strategy.md)

> D-Robotics sells compute boards, not robots. This guide is therefore about getting **perception / AI running on an RDK board in the first hour** and wiring its output into another vendor's robot. Headings are adapted from the robot template accordingly.

## TL;DR — how you program it

- **It is an Ubuntu ARM64 computer with an AI accelerator (BPU).** SSH in (`sunrise@192.168.127.10`), write Python or C++, use ROS 2. No CUDA, no TensorRT.
- **Fastest path = pre-converted models.** Clone [rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo), run a `download_model.sh` + `main.py` pair, get YOLO detection / pose / segmentation, depth, speech or a small VLM on the BPU in minutes.
- **ROS 2 path = TogetheROS.Bot (TROS).** `sudo apt install tros-humble` adds BPU-accelerated camera, codec, inference and web-render nodes on top of stock ROS 2. Your robot from another vendor then just subscribes to topics.
- **Custom models cost time.** ONNX must be quantized (INT8) and compiled per chip with the OpenExplorer Docker toolchain on an x86 PC (`.bin` for X3 / X5, `.hbm` for S100 / S100P / S600). Budget **half a day** the first time; avoid it if a zoo model is close enough.
- **Robot learning is documented but narrow.** One worked recipe: LeRobot **ACT on SO-100 arms**, inference on RDK S100 / X5 BPU. Pi0 and ACT also appear as model-zoo submodules; treat anything beyond ACT as experimental.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| RDK OS (Ubuntu image) | — | The board itself: drivers, camera, codec, 40-pin header | [RDK X manual](https://developer.d-robotics.cc/rdk_x_doc/en/RDK) · [RDK S manual](https://developer.d-robotics.cc/rdk_s_doc/en/RDK) | System images referenced in TROS docs: **X5 v3.5.0**, **S100 v4.0.5**, **S600 v5.1.0**. Check yours with `cat /etc/version` or `rdkos_info` |
| rdk_model_zoo | Python, C/C++ | BPU inference samples + conversion tutorials | [GitHub](https://github.com/D-Robotics/rdk_model_zoo) | Apache-2.0 · targets **X5, S100, S100P, S600** on `main`; X3 is archive-only (`rdk_x3` branch) · Python API is `hbm_runtime` · X5 needs RDK OS **≥ 3.5.0** |
| TogetheROS.Bot (TROS) | C++, Python | ROS 2 nodes with BPU / codec acceleration | [TROS docs](https://developer.d-robotics.cc/tros_doc/en/tros) · [build entry repo](https://github.com/D-Robotics/robot_dev_config) | apt packages `tros` (Foxy), `tros-humble`, `tros-jazzy` |
| hobot_dnn | C++ | ROS 2 inference framework (`dnn_node`, examples, benchmark) | [GitHub](https://github.com/D-Robotics/hobot_dnn) | Base class for wrapping your own model as a ROS 2 node |
| hobot_mipi_cam / hobot_cv / hobot_codec | C++ | MIPI camera capture, accelerated CV ops, H.264 / H.265 / JPEG codec | [hobot_mipi_cam](https://github.com/D-Robotics/hobot_mipi_cam) · [hobot_cv](https://github.com/D-Robotics/hobot_cv) | Ship inside TROS |
| hobot_stereonet + RDK-Stereo-Camera-SDK | C++ | Learned stereo depth from the RDK stereo cameras | [hobot_stereonet](https://github.com/D-Robotics/hobot_stereonet) · [SDK](https://github.com/D-Robotics/RDK-Stereo-Camera-SDK) | Most-starred perception node in the org; pairs with `stereo_calib`, `dstereo_occnet` (occupancy) |
| D-Robotics LeRobot fork + rdk_LeRobot_tools | Python | Data collection, ACT training, BPU export and deployment for SO-100 arms | [lerobot fork](https://github.com/D-Robotics/lerobot) · [BPU tools](https://github.com/D-Robotics/rdk_LeRobot_tools) | See AI stack below |
| OpenExplorer toolchain | Docker (x86 PC) | ONNX → quantized board model | via [doc center](https://developer.d-robotics.cc/rdk_doc_center/en) | X5 PTQ runs in a CPU Docker; GPU Docker optional for S100 |
| RDK Studio + Moss | Desktop app, TypeScript | Flashing, device manager, terminals, AI coding assistant | [RDK Studio](https://developer.d-robotics.cc/en/rdkstudio) · [moss](https://github.com/D-Robotics/moss) | Supported OS list: see profile; download page linked from the docs is the Windows build |
| rdk-skills / hobot_llamacpp / hobot_chatbot / xiaozhi-in-rdk | Python, C++ | Agent skills, on-board LLM (llama.cpp) and voice-assistant nodes | [rdk-skills](https://github.com/D-Robotics/rdk-skills) · [hobot_llamacpp](https://github.com/D-Robotics/hobot_llamacpp) | Small models only on X5; ⚠️ unverified quality |
| rdk-course-demos ("RDK Classroom") | Markdown + code | 14 beginner lessons: flashing, remote login, camera, audio, codec, 40-pin GPIO / PWM / UART / I2C / SPI, CAN | [GitHub](https://github.com/D-Robotics/rdk-course-demos) | English, organised by `common` / `x5` / `s100`. Best onboarding material |

## Control levels

There is no "robot API" here. Think in three layers:

| Layer | What you get | Use it for |
|---|---|---|
| **High level: perception → ROS 2 topics** | TROS nodes publish detections, poses, depth, speech results; `hobot_render` shows them in a browser | Feeding another vendor's robot (Unitree, AGIBOT, Dobot, Flexiv ...) through that robot's own SDK or ROS 2 bridge. **This is the realistic hackathon mode** |
| **Mid level: board I/O** | 40-pin header (GPIO, PWM, UART, I2C, SPI) and CAN, covered lesson by lesson in RDK Classroom | Driving hobby servos, LEDs, a small custom chassis, reading simple sensors |
| **Low level: real-time MCU cores** | S100 / S100P carry **4x Cortex-R52+**, S600 **6x**, next to the Linux cores, intended for motor loops | Custom actuators (e.g. Leadshine drives or joint modules). MCU SDK, RTOS and loop rates: not checked for this guide; ⚠️ unverified. Do not plan a 48-hour project around it unless a D-Robotics engineer on site commits to help |

- X3 and X5 have **no** real-time MCU; anything time-critical needs an external microcontroller.
- "EDU vs developer edition" does not apply: all boards are open developer kits. Differences are compute tier and RAM only.
- Control rate of a learned policy: the ACT recipe generates a **50-action chunk in about 50 ms** on the BPU and then plays it back, so effective control is chunked, not per-step.

## ROS 2 and middleware

| Item | Detail |
|---|---|
| Install | `sudo apt update && sudo apt install tros-humble` (or `tros` for Foxy on old X3 images, `tros-jazzy`). Fix `Unmet dependencies` with `apt --fix-broken install` |
| Versions shown in the docs | `tros` 2.0.0 (Ubuntu focal) · `tros-humble` 2.2.0 (jammy) · `tros-jazzy` 2.5.0 (the S600 apt source is Ubuntu noble). Yours may be newer: `apt show tros-humble` |
| Install location | under `/opt/tros` (verify with `ls /opt`); source the `setup.bash` inside it before `ros2 ...` (commonly `/opt/tros/humble/setup.bash`, ⚠️ unverified this session) |
| Boards in the TROS feature list | RDK X3, X5, S100, S600 |
| Core packages | `hobot_sensor` (cameras and sensors) · `hobot_dnn` (BPU inference) · `hobot_codec` · `hobot_cv` · `hobot_render` (web / HDMI view) · zero-copy transport · `hobot_image_publisher` · `hobot_tts` · `hobot_audio` · `hobot_vio` |
| Ready-made algorithm nodes ("Boxs") | YOLO v2 / v3 / v5 (v8, v10 on X5 and S100), `hobot_yolo_world` and `hobot_dosod` (open-vocabulary detection), `hobot_clip`, `hobot_llamacpp`, `hobot_xlm`, `hobot_bev`, `hobot_centerpoint`, body tracking, stereo depth |
| App library | [NodeHub](https://developer.d-robotics.cc/en/nodehub): 200+ packaged demos, each with copy-paste launch commands |
| SLAM / Nav | Standard `slam_toolbox` and Nav2 from apt; D-Robotics keeps a `slam_toolbox` fork adapted for X5 / TROS Humble (see simulation repo below) |

Interop tips (general ROS 2 practice, not D-Robotics specific):

- TROS is interface-compatible with stock ROS 2, so the partner robot's ROS 2 messages work as is. Match **ROS 2 distro, `ROS_DOMAIN_ID` and RMW implementation** with the robot you pair with.
- Detection results use D-Robotics' own message package (`ai_msgs`); the consuming machine needs that package built, or write a tiny relay node on the RDK that republishes as `vision_msgs` or a plain `geometry_msgs` target. ⚠️ unverified message names this session; check the NodeHub page of the node you use.

## Simulation and digital twins

D-Robotics has no robot body, so there are no official URDF / MJCF / USD robot assets. What exists:

| Repo | Simulator | Content | Maturity |
|---|---|---|---|
| [drobotics_robosim](https://github.com/D-Robotics/drobotics_robosim) | **Gazebo Classic 11** + ROS 2 Humble | Differential-drive "sweeper" robot (xacro / URDF) with 2D lidar, 16-line 3D lidar, IMU, stereo cameras; 14-room apartment world (SDF); slam_toolbox mapping, Nav2, frontier exploration, coverage planning | Early: single maintainer, README in Chinese, container-based setup, no learned policies, real-hardware port explicitly out of scope, no licence file shown |
| [robot-learning-platform](https://github.com/D-Robotics/robot-learning-platform) | **MuJoCo** (browser, MJX) + Isaac Lab adapter | Web workbench for the 14-servo MicroDuck legged robot + RDK X5: record, train (PPO, BC, ACT, Diffusion Policy; SmolVLA adapter), ONNX export, Sim2Real evaluation, gated deployment | Software parts ready; real X5 latency numbers, joint names and production cloud config still pending. Apache-2.0 |
| Cloud "embodied training field" | not public | Announced Nov 2025 as part of the one-stop cloud platform | 🧪 no public self-serve access found |

Practical advice: simulate with the **body vendor's** assets (Unitree, AGIBOT, Galaxea etc. publish their own) and treat the RDK as the deployment target only. `drobotics_robosim` is useful if you build a home / indoor service robot on a simple diff-drive base (T01, T04).

## AI stack

| Need | What to use | Status |
|---|---|---|
| Detection, segmentation, pose, OBB, classification | Ultralytics YOLO family **YOLOv5u → YOLO26** in the model zoo; YOLOE and YOLOWorld for open-vocabulary / prompt-free | ✅ |
| Depth | `hobot_stereonet` (stereo camera), Depth Anything V2 (S100), YOLO26 Depth | ✅ |
| Segment-anything, features | MobileSAM, EfficientSAM, CLIP, SigLIP, DINOv2 | ✅ |
| Tracking, OCR, lanes | ByteTrack, HobotMot, PaddleOCR, LaneNet | ✅ |
| Speech | Wav2Vec2 ASR, Paraformer, keyword spotting; `sensevoice_ros2`; `hobot_tts` | ✅ |
| On-device language | Gemma4-E2B (VLM chat) and MiniCPM5-2B (text), native C++ samples; `hobot_llamacpp` ROS node | ✅ small models; expect slow token rates on X5 (⚠️ unverified) |
| Locomotion policy | **HIMLoco for Unitree Go2** sample in the model zoo | ✅ sample; relevant because Unitree is on site |
| Imitation learning | LeRobot **ACT** on SO-100 leader / follower arms (Feetech STS3215), two USB cameras, BPU inference on S100 or X5 | ✅ documented end to end on the forum |
| VLA | ACT and **Pi0** as pinned submodules under `samples/vla/`; separate [openpi_runtime](https://github.com/D-Robotics/openpi_runtime) repo. Vendor performance claims for Pi0 and Qwen2.5-VL-7B relate to the **S600** | 🧪 on S100-class boards; do not assume real-time |
| Own foundation model / dataset | none published; D-Robotics provides compute and deployment tooling. Reference dataset for the ACT recipe: `MaCCChhh/rdk_so100_test` on Hugging Face (community) | not public |

ACT recipe in one glance (from the official forum guide):

1. Python 3.10 env, D-Robotics LeRobot fork, `pip install -e ".[feetech]"`.
2. Patch: video codec `libsvtav1` → `libx264`, force MJPG cameras, servo D gain 0.
3. Record **≥ 50 episodes** (about 10 per object position, cameras fixed).
4. Train `--policy.type=act` on a GPU PC: reference run 50k steps, batch 8, **about 4 h** on a TITAN Xp.
5. Verify on CPU, export with `export_bpu_actpolicy.py` (splits into vision encoder + transformer), quantize in the OpenExplorer Docker, copy the output folder to the board, run `bpu_act_control_robot.py`.

Hackathon reality check: steps 3 to 5 consume most of a day. Only start if you have the arms, a training GPU and one person dedicated to it.

## Compute, sensors and connectivity

| Board | AI compute | CPU / RAM | Real-time MCU | Typical role |
|---|---|---|---|---|
| RDK X3 | 5 TOPS | see profile | no | Legacy; model zoo no longer targets it |
| RDK X5 | 10 TOPS | 8x A55, 4 or 8 GB | no | Vision node, small mobile robot brain |
| RDK S100 | 80 TOPS | 6x A78AE, 12 GB | 4x R52+ | Multi-camera perception, ACT, small VLM |
| RDK S100P | 128 TOPS | 6x A78AE, 24 GB | 4x R52+ | Same, more headroom |
| RDK S600 | 560 TOPS (vendor) | 18x A78AE | 6x R52+ | On-device VLA / VLM; unlikely on site |

Network defaults (official docs):

| Item | RDK X5 (image 3.0.0+) | RDK S100 / S600 |
|---|---|---|
| Wired static IP | **192.168.127.10/24** | **eth1: 192.168.127.10/24**, gateway 192.168.127.1 |
| Other ports | USB device ("flash connection") port: **192.168.128.10/24** | eth0: DHCP · S600 also has eth2 / eth3 10GbE |
| SSH | `ssh sunrise@192.168.127.10` | same |
| Default accounts | user `sunrise` / `sunrise` · `root` / `root` | same |
| Serial console | **921600** baud, 8N1, no flow control | same (macOS: `minicom -D /dev/tty.wchusbserial* -b 921600 -8`) |
| Remote desktop | VNC, password `sunrise` | NoMachine (set up via the configuration wizard) |
| Wi-Fi | `sudo nmcli device wifi rescan` then `sudo wifi_connect "SSID" "PASSWD"`; read the address with `ifconfig` | DHCP on wlan0; check with `ifconfig` |

- Laptop setup: set your Ethernet adapter to a static address such as **192.168.127.100/24**, plug straight into the board, `ping 192.168.127.10`.
- Older X3 images (≤ 2.0.0) use 192.168.1.10 instead.
- Cameras: MIPI CSI (X5: 2 ports; S100: 2; S100P: 3; S600: 6), USB UVC cameras, RDK stereo camera modules; GMSL on S100P via add-on board (see profile).
- X5 has a single USB 3 port: two USB cameras on it may need `modprobe uvcvideo quirks=128`.

## First 60 minutes checklist

1. **Ask the D-Robotics desk** which board, image version and camera you are getting, and whether the SD card / eMMC is pre-flashed. If not, flash with RDK Studio.
2. **Power** with the supplied adapter (S100P: 12–20 V, 90 W class; X5: USB-C 5 V supply recommended by the kit). Wait for boot.
3. **Connect**: Ethernet cable laptop ↔ board, laptop at `192.168.127.100/24`, then `ssh sunrise@192.168.127.10`. Fallback: serial console at 921600 baud.
4. **Verify the system**: `cat /etc/version` and `rdkos_info`. Model zoo on X5 wants **≥ 3.5.0**.
5. **Get online**: `sudo wifi_connect "SSID" "PASSWD"`, note the wlan0 address, then **change the default passwords** (`passwd`) because every board on site shares them.
6. **Hello-world inference (no ROS)**:
   ```bash
   git clone https://github.com/D-Robotics/rdk_model_zoo && cd rdk_model_zoo
   cd samples/vision/ultralytics_yolo/model
   bash download_model.sh --platform x5 --family yolo11 --task detect --model-size x
   cd ../runtime/python
   python3 main.py --task detect --platform x5 --family yolo11 --model-size x \
     --test-img ../../test_data/bus.jpg --img-save-path ../../test_data/out.jpg
   ```
   Change `--platform` for S-series boards as the sample README describes; pick a smaller `--model-size` (n or s) for live video.
7. **Read a sensor**: plug in the camera, confirm it with the camera lesson in RDK Classroom (USB: `ls /dev/video*`; MIPI: use the `hobot_mipi_cam` node).
8. **ROS 2 pipeline**: `sudo apt install tros-humble`, source the setup file under `/opt/tros`, then launch a camera + detection + web-render demo from the matching [NodeHub](https://developer.d-robotics.cc/en/nodehub) page and open the board's IP in a browser to see overlays (port given on the NodeHub page).
9. **Bridge to the robot**: on the same network as the partner robot, `ros2 topic list` from both sides; write the 30-line node that turns a detection into that robot's command (velocity, waypoint, gripper trigger).
10. **Decide on custom models now**: if a zoo model is not enough, start the OpenExplorer Docker download on an x86 laptop immediately; it is the long pole.

## Known gotchas and safety

- **Identical static IPs.** Every board defaults to 192.168.127.10. Never put two un-reconfigured boards on one switch; use Wi-Fi / DHCP (eth0 on S-series) or change the static address. (Inference from the documented defaults.)
- **Default passwords** (`sunrise`, `root`) are public. Change them on the shared hackathon network.
- **Models are chip-specific.** An X5 `.bin` will not run on S100 and vice versa (S100 = Nash-E, S100P = Nash-M, S600 = Nash-P artifacts). Download or compile for the exact board.
- **INT8 quantization can cost accuracy**; always compare against the float ONNX on a few of your own images before trusting it.
- **Benchmarks exclude pre / post-processing** and Python is slower than C/C++ (stated in the model zoo). Measure end-to-end FPS yourself.
- **No CUDA.** PyTorch on the board runs on CPU only; anything not converted for the BPU will be slow.
- **TROS / OS version coupling.** TROS 2.x needs a 2.x+ image; `apt update` failures have a dedicated FAQ entry in the manuals.
- **LeRobot recipe quirks:** camera names (`phone`, `laptop`) and 640x480 input are hard-coded; ffmpeg without `libx264` breaks recording; export parameters must match training; Hugging Face downloads can need a proxy in some regions.
- **S100P:** BMI088 IMU on the MCU expansion board unsupported in some OS versions (see profile).
- **Thermals and altitude:** S100P is rated 0–45 °C. Outdoor demos in Leukerbad in November are near or below the lower limit; keep the board in an enclosure, warm it up indoors. X5 under sustained BPU load wants a heatsink / fan. (Practical inference.)
- **No e-stop, no safety rating.** The board is not a safety controller. All motion safety (e-stop, speed limits, force limits) must come from the robot it commands. Keep a human on the robot's own e-stop whenever an RDK-generated command can move hardware; add a watchdog so the robot stops if the RDK topic goes silent.
- **Agent tooling (Moss, OpenClaw, rdk-skills)** can run shell commands on the board; do not let it drive actuators unsupervised.

## Community resources

- [Documentation center](https://developer.d-robotics.cc/rdk_doc_center/en): entry point to X-series, S-series, TROS, accessories and RDK Studio manuals.
- [RDK Classroom code](https://github.com/D-Robotics/rdk-course-demos): English step-by-step lessons for X5 and S100.
- [English forum](https://forum-en.d-robotics.cc/): official guides (e.g. LeRobot ACT) and troubleshooting.
- Discord: used for the Robotics Dream Keeper Challenge; link via the [challenge repo](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter). Contact address listed there: developer@d-robotics.cc.
- [GitHub org](https://github.com/D-Robotics): about **269 repositories**, most active ones updated this week.
- [Official blog](https://en.d-robotics.cc/blog): community project write-ups (arm + AI brain, lidar mapping robot, YOLO benchmarks).
- On site: ask the D-Robotics engineers for a pre-flashed image and the exact NodeHub demo for your camera; that saves the first hour.

Research note: web search was unavailable for part of this guide's preparation; items marked ⚠️ unverified could not be re-checked against the live docs and should be confirmed at the vendor desk.

## Sources

- [D-Robotics GitHub organisation (repository list)](https://github.com/orgs/D-Robotics/repositories?type=all&sort=updated)
- [rdk_model_zoo README](https://github.com/D-Robotics/rdk_model_zoo)
- [hobot_dnn](https://github.com/D-Robotics/hobot_dnn)
- [drobotics_robosim](https://github.com/D-Robotics/drobotics_robosim)
- [robot-learning-platform](https://github.com/D-Robotics/robot-learning-platform)
- [rdk-course-demos (RDK Classroom)](https://github.com/D-Robotics/rdk-course-demos)
- [Robotics Dream Keeper Challenge 2026 Winter](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter)
- [RDK X manual: remote login](https://developer.d-robotics.cc/rdk_x_doc/en/Quick_start/remote_login)
- [RDK S manual: remote login](https://developer.d-robotics.cc/rdk_s_doc/en/Quick_start/remote_login)
- [RDK S series manual](https://developer.d-robotics.cc/rdk_s_doc/en/RDK)
- [Introduction to TogetheROS.Bot](https://developer.d-robotics.cc/tros_doc/en/tros)
- [TROS: installation](https://developer.d-robotics.cc/tros_doc/en/quick_start/install_tros)
- [Forum: LeRobot ACT policy on RDK](https://forum-en.d-robotics.cc/t/lerobot-act-policy-on-rdk/391)
- [D-Robotics blog index](https://en.d-robotics.cc/blog)
- [D-Robotics profile (this folder)](D-Robotics.md)
