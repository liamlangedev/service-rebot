---
type: dev-guide
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Leadshine Technology Co., Ltd. — Developer Guide (hackathon edition)

⬆ [Leadshine Technology Co., Ltd. profile](Leadshine.md) · [Product portfolio](Leadshine-Products.md) · [Roadmap and strategy](Leadshine-Roadmap-and-Strategy.md)

> Leadshine (雷赛智能, SZSE 002979) is a **component vendor**. The only products with a real programming stack are the **dexterous hands** (DH116 / DH116S / DH2116), built by its subsidiary **Shenzhen Lingqiao Drive and Control Technology** (深圳灵巧驱控, brand "Leadtron"). Everything below is about getting a hand moving in the first hour; joint modules and industrial drives are covered briefly at the end of each section.

| DH116 | DH116S | DH2116 |
|---|---|---|
| ![DH116](assets/leadshine-dh116.jpg) | ![DH116S](assets/leadshine-dh116s.jpg) | ![DH2116](assets/leadshine-dh2116.jpg) |
| 11 DoF / 6 active, 545 g | 11 DoF / 6 active, 359 g | 21 DoF / 16 active, 850 g |

## TL;DR — how you program it

- **One SDK for all hands: `LHandProLib`** — C++ library (namespace `lhplib`) with a C API and a Python `ctypes` wrapper. Current manual **v1.8 (2026-09-16)**, latest package **20261031**. Builds for Linux x86_64 / i386 / aarch64, Windows, macOS arm64.
- **You own the bus, the SDK owns the protocol.** You open EtherCAT / CAN FD / RS485 (or plain CAN on the DH2116), register a *send callback*, and feed received bytes back into the SDK. Ready-made examples exist for every bus in C++ and Python.
- **Control is per joint:** target angle (°) or stroke position (0–10000), speed, and a current limit in per-mille (‰). Modes: position, velocity, torque, and two hybrids. Built-in gestures via `play_gesture`.
- **ROS 2 Humble on Ubuntu 22.04** is the supported robot middleware: a service-based control node, a `/joint_states` bridge for RViz2, tactile topics, C++ and Python demos.
- **Simulation = URDF + MJCF** (Apache-2.0 repo) plus an SDK **dry-run mode**. There is **no AI stack** (no policies, datasets, VLA, LeRobot) and **no public SDK for the PJ3 / HJ2 joint modules**.

## SDKs and interfaces

Status of "official": Leadshine has **no GitHub organisation**. The public release channel is a personal GitHub account of the SDK developer (`sorrowfeng`, Shenzhen). Its release notes point to the **same Feishu wiki page** that Leadshine's official manuals link as the "SDK download page", so it is treated here as the vendor's working channel — but confirm with staff on site.

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| **LHandProLib SDK** (release mirror) | C++17 core, C API, Python wrapper | DH116, DH116 V2, DH116S (6 active DoF), DH2116 (16 active DoF), generic per-axis mode (up to 30 axes) | [sorrowfeng/LHandProLib-Releases](https://github.com/sorrowfeng/LHandProLib-Releases/releases) | ✅ Binary library + headers + example sources. **Core source is private** — Leadshine's "open-source SDK" wording means open examples, not an open library. Each release ships an English and a Chinese SDK manual. |
| **LHandPro** host GUI ("upper computer") | Qt desktop app | Jogging, homing, gestures, teaching, tactile view, 3D preview, firmware OTA, node-ID / baud-rate setup | [sorrowfeng/LHandPro-Releases](https://github.com/sorrowfeng/LHandPro-Releases/releases) | ✅ **v1.4.5 (2026-10-31)**: Windows x64, macOS arm64 (.dmg, not notarized), Linux x86_64 / aarch64 (.deb / .tar.gz, built for Ubuntu 22.04). Earlier versions were Windows-only. |
| **`lhandpro_ws`** — official ROS 2 example | C++ / Python | DH116 / DH116S over EtherCAT (SOEM) | Zip linked from the user manuals (Feishu); build notes: [ROS2 example PDF](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf) | ✅ Packages: `lhandpro_description`, `lhandpro_interfaces`, `lhandpro_service`, `sequence_demo_cpp`, `sequence_demo_py`. File names in the manuals: `lhandpro_ws_116_2026_02_10.zip`, `lhandpro_ws_DH116S_2026_1_6.zip`. |
| **`hand_control_ws`** — newer ROS 2 workspace | C++17 / Python | Any LHandProLib hand over CAN FD, RS485 or EtherCAT; one or several hands | [sorrowfeng/hand_control_ws](https://github.com/sorrowfeng/hand_control_ws) | 🧪 White-labelled successor of `lhandpro_ws` (README in Chinese). Adds YAML bus/hand topology, real-time state topic, tactile topic, multi-hand. Check that `thirdparty/lib` contains the SDK binaries; otherwise copy them from the SDK package. |
| **`leadtron_hand_descriptions`** | URDF / MJCF / Python tools | Models for DH116, DH116S, DH116 V2.0 (left + right) | [sorrowfeng/leadtron_hand_descriptions](https://github.com/sorrowfeng/leadtron_hand_descriptions) | ✅ **Apache-2.0**. Includes mesh, launch and config folders; DH116 V2.0 ships an interactive MuJoCo script `sim_hand.py`. |
| **`RaspberryPiDemo`** | Python | Hand on a Raspberry Pi over CAN FD / EtherCAT / RS485 | [sorrowfeng/RaspberryPiDemo](https://github.com/sorrowfeng/RaspberryPiDemo) | 🧪 Motion sequences, grasp cycles, GPIO triggers, **data-glove input over UDP**. Contains a full Python wrapper class (`PyLHandProLib`). SDK binaries are not in the repo. |
| **`gsusb-canfd`** | C++17 / Python (PyPI `gsusb-canfd`) | USB-CAN FD adapters (candleLight / gs_usb type) from userspace | [sorrowfeng/gsusb-canfd](https://github.com/sorrowfeng/gsusb-canfd) | ✅ **MIT**. Default CAN FD backend of the ROS 2 workspace and the Pi demo; no kernel driver, works on Windows / macOS / Linux. |
| DH116 "deployment kit" (older bundle) | — | DH116: SDK 20251128, URDF 2025-11-24, ROS 2 source, `Protocol.xlsx`, EtherCAT ESI `LSLQ_DH116.xml`, STEP/DXF | [carolyang823 repo](https://github.com/carolyang823/Leadshine-Cost-Effective-Dexterous-Hand-DH116-Designed-for-Humanoid-Robots-) | ⚠️ unverified as official; **old generation** (pre-2026-02-10 hardware). Useful mainly because it contains the protocol spreadsheet and PDF manuals in one place. |
| Bus protocol documents | xlsx / Feishu doc | EtherCAT PDO map, CAN FD and RS485 frame formats | Feishu wiki links inside the manuals | Feishu pages redirect scripts to a login page; open in a browser or ask staff for a copy. |
| PJ3 / HJ2 joint modules | — | — | [PJ3](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html) · [HJ2](https://www.leadshine.com/robots/integrated-actuators/hj2-series.html) | **No public SDK, ROS 2 driver, object dictionary or protocol document found.** Buses: EtherCAT or CAN FD. Protocol must come from Leadshine staff. |
| Industrial servo / stepper drives | vendor Windows tools | EL7 / EL8 / ELD3 / EM3E / CS3E … | [Download centre](https://www.leadshine.com/downloads.html) | EtherCAT models follow CiA 402 over CoE (per the first-pass profile), so a generic EtherCAT master can drive them. Unlikely to be useful in 48 hours. One community ROS 2 package exists for EM2RS steppers: [openvmp/stepper_driver_em2rs](https://github.com/openvmp/stepper_driver_em2rs) (2023, third party). |

**Feishu wiki pages linked from the manuals** (same space for all three hands): [host tool downloads](https://zcnrg1e5hv0a.feishu.cn/wiki/LxWzwOGdVi31Z1kKYe3cQ8PkneT) · [SDK downloads](https://zcnrg1e5hv0a.feishu.cn/wiki/LyKNwGTU4i82ZKkHf6mcW8iWnRh) · [URDF & MJCF downloads](https://zcnrg1e5hv0a.feishu.cn/wiki/P8j6wreHCiWFgZk4YIAcvPpxnBf) · [CAN FD protocol for DH116(S)](https://zcnrg1e5hv0a.feishu.cn/wiki/HtaywawGLiQCJokG196ckLwrn8f).

## Control levels

There is **no EDU / developer edition** — every hand exposes the same interface. What differs per model is the bus and the sensor option.

| Level | What you call | Units / range | Notes |
|---|---|---|---|
| **Scripted** | `play_gesture(gesture_id, velocity, current)`; GUI teaching; sequence demos | velocity in counts/s, current in ‰ | Gesture IDs are defined in firmware / GUI — ask staff or read them in the GUI. |
| **Joint position** (default) | `set_target_angle(id, deg)` or `set_target_position(id, 0…10000)` → `move_motors(id)` | degrees, or stroke counts (0 = open, 10000 = full stroke) | `id = 0` broadcasts to all joints. Read limits with `get_limit_target_angle`. |
| **Speed and force limit** | `set_angular_velocity(id, deg/s)` / `set_position_velocity(id, counts/s)`, `set_max_current(id, ‰)` | example values in vendor code: **200 °/s**, **20000 counts/s**, **1000 ‰** | Sent only when changed; `apply_motion_params()` forces an immediate update. `set_max_current` is your grip-force limiter. |
| **Control mode** | `set_control_mode(id, mode)` | `LCM_POSITION`, `LCM_VELOCITY`, `LCM_TORQUE`, `LCM_VEL_TOR`, `LCM_POS_TOR`, `LCM_HOME` | Torque = motor-current control; the FOC current loop itself runs inside the hand and is not exposed. |
| **Feedback** | `get_now_angle / position / angular_velocity / current / status / alarm`, `get_position_reached`, `get_torque_reached` | — | Alarm types: position error, over-speed, over-current, overload, over/under-voltage, encoder, stall. |
| **Tactile** | `set_sensor_enable(1)`, `set_finger_pressure_reset()`, `get_finger_pressure`, `get_finger_normal_force[_ex]`, `get_finger_tangential_force[_ex]`, `get_finger_force_direction[_ex]`, `get_finger_proximity[_ex]` | N, degrees (0–360), proximity 0–1 | 11 sites: 5 fingertips + 5 finger pads + palm (`LSS_FINGER_1_1` … `LSS_HAND_PALM`). Only on -M / -S variants. |
| **Device config** | node ID, CAN FD arbitration / data baud rate, RS485 baud rate, SDO read/write, firmware OTA | — | Saved to the drive; changing them mid-event can lock you out of the bus. |

**Joint numbering (6-DoF hands, `LAC_DOF_6`, `LAC_DOF_6_V2`, `LAC_DOF_6_S`):** 1 thumb abduction · 2 thumb flexion · 3 index · 4 middle · 5 ring · 6 pinky.

| Active joint | DH116 range | DH116S range |
|---|---|---|
| Thumb side swing | 0–60° | 0–91° |
| Thumb flexion | 0–30° | 0–59° |
| Index / middle / ring | 0–80° | 0–72° |
| Little finger | 0–80° | 0–74° |

**DH2116 (`LAC_DOF_16`):** 5 fingers × 3 motors + 1 extra thumb axis. Per finger, motors 1 and 2 work differentially (their mean bends joint 2, their difference swings joint 1 by ±20°), motor 3 drives joints 3 and 4 together. Motor commands run **0–4095**. Mapping from the manual: `M1 − M2 = θ1 · 4095/90`, `(M1 + M2)/2 = θ2 · 4095/90`, `M3 = θ3 · 4095/75`. Motors 1 and 2 constrain each other, so not every combination is reachable.

**Rates (what the vendor code actually does — no kHz loop is documented):**

| Path | Rate / timing | Source |
|---|---|---|
| EtherCAT example: TPDO polling loop | every **10 ms** (100 Hz) | SDK manual example |
| SDK inter-frame delay | unified at **10 ms** | SDK v1.8 changelog |
| RS485 shared bus | one transaction window per **30 ms** by default (whole bus, all hands) | SDK manual |
| ROS 2 `realtime_state` topic | **100 Hz** default | `hand_control_ws` config |
| ROS 2 tactile topic | **50 Hz** default; one frame = 55 bus reads — lower it if the bus cannot keep up | `hand_control_ws` README |
| CAN FD bit rates | **1 Mbps** arbitration / **5 Mbps** data (defaults in vendor config) | `hand_control_ws` config |

The "100 MHz EtherCAT" in the DH116 manual means a 100 Mbit/s link, not a 100 MHz control loop. Practical expectation: **~100 Hz joint commands and state**, fine for grasping and teleoperation, not for high-bandwidth finger impedance control.

**Joint modules and drives:** PJ3 / HJ2 offer EtherCAT or CAN FD, but torque / position / MIT-style modes, rates and object dictionaries are **not published** ⚠️. Industrial EtherCAT drives use standard CiA 402 modes.

## ROS 2 and middleware

| Item | Official example `lhandpro_ws` | Newer `hand_control_ws` |
|---|---|---|
| Environment | Ubuntu 22.04, ROS 2 Humble, `colcon` | Same; C++17, CMake ≥ 3.8 |
| Buses | EtherCAT (bundled SOEM master) | CAN FD (gs_usb userspace default, SocketCAN optional), RS485, EtherCAT (SOEM) |
| Control interface | ROS 2 **services** mapped 1:1 to SDK calls | Services under `/hand_control/…` (`set_enable`, `home_motors`, `set_angle`, `set_position`, `set_max_current`, `move_motors`, `control_motors`, `play_gesture`, `get_now_*`, …) |
| State | `lhandpro_state_publisher` → `/joint_states` | `/hand_control/realtime_state` (`HandJointState`) → `hand_state_publisher` → `/joint_states` |
| Tactile | not in the example | `/hand_control/<hand>/tactile_state` (`TactileState`: pressure, normal force, tangential force, direction, proximity per site) |
| Multi-hand | no | yes — same bus with different IDs, or separate buses; names like `/hand_control/left/…`, `/hand_control/right/…` |
| Visualisation | `ros2 launch lhandpro_description display_lhandpro.launch.py` (RViz2 mirrors the real hand) | `ros2 launch hand_control_description display.launch.py` (single hand only) |
| Demos | `sequence_demo_py`, `sequence_demo_cpp` | plus `tactile_demo_py`, `tactile_demo_cpp` |

- **Not provided:** `ros2_control` hardware interface, MoveIt configuration, ROS 1 packages, DDS-level API, Isaac ROS integration. For arm + hand planning you write a thin action wrapper around the services yourself.
- **DH2116:** no ROS 2 example was found in the manual's download list (SDK, STEP, URDF and protocol only). The newer workspace is hand-type driven (`hand_type: LAC_DOF_6_S` in YAML); whether `LAC_DOF_16` works out of the box is ⚠️ unverified.
- **No ROS? Use the SDK directly** — Python on Windows / macOS / Linux needs no middleware.

## Simulation and digital twins

| Asset | Models | Where | Notes |
|---|---|---|---|
| URDF | DH116, DH116S, DH116 V2.0, left and right | [leadtron_hand_descriptions](https://github.com/sorrowfeng/leadtron_hand_descriptions) | Passive finger joints are coupled with `<mimic>` — a **linear** approximation (mid-stroke error up to about 3.8° on DH116). |
| MJCF (MuJoCo) | same | same repo | Coupling modelled with `equality joint polycoef` (quadratic, closer to the real linkage). DH116 V2.0 folder has `sim_hand.py` for interactive MuJoCo control. |
| URDF for DH2116 | DH2116 | `DH2116_URDF_Files_2026_3_16.zip`, linked in the DH2116 manual (Feishu) | MJCF for DH2116 not found ⚠️. |
| STEP / CAD | all three hands | linked in the manuals | Use for designing the wrist flange adapter. |
| Passive-vs-active joint tables | DH116, DH116S | spreadsheets linked in the manuals; formulas also in the description repo READMEs | Needed if you retarget human hand poses. |
| RViz2 twin | DH116 / DH116S | both ROS 2 workspaces | Mirrors the physical hand from `/joint_states`. |
| **SDK dry-run mode** | all | `set_dry_run_mode(true)` | Generates bus frames without hardware; `initial()` does not time out and `move_motors` skips the homing check. Good for coding before you get a hand. |

- **Not found:** Isaac Sim / Isaac Lab USD assets, Gazebo worlds, Genesis or Webots models, contact-rich tactile simulation. MJCF can be imported into Isaac Lab or converted yourself.
- Joint names in the models: active `finger11`, `finger12`, `finger21`, `finger31`, `finger41`, `finger51`; passive `finger13`, `finger22`, `finger32`, `finger42`, `finger52`.

## AI stack

**Leadshine offers none.** Plain statement of what exists and what does not:

| Topic | Status |
|---|---|
| Pretrained manipulation policies, VLA / foundation models | ❌ none published |
| Datasets | ❌ none published |
| LeRobot / Hugging Face integration | ❌ none found |
| Teleoperation | 🧪 Building blocks only: an optional **data glove ("6248XL Super Sensing Data Gloves", accessory "for data acquisition")** listed in the DH116S manual; a glove example in the SDK package (per the 20261031 release notes); glove input over UDP in the Raspberry Pi demo; "glove linkage" and camera-based hand / gesture detection inside the LHandPro GUI (per release notes). No documented end-to-end teleop pipeline. |
| Data collection | DIY: record `/hand_control/realtime_state` and `tactile_state` with `ros2 bag`, or log from the SDK (`log_on`, `log_save`). |
| "Adaptive grasping algorithms", "multi-modal machine-learning tactile sensor" | Vendor wording for firmware features and the sensor type; no model or training code is released. |
| Higher-level motion intelligence | 🔭 A July 2026 investor note says the company is starting R&D on the robot "cerebellum" (motion-control layer). No product. |

**Practical hackathon recipe (our suggestion, not a vendor feature):** webcam → MediaPipe Hands (or an XR headset's hand tracking) → map finger curl to the **6 active joints** → `set_target_position` at 20–50 Hz with a low `set_max_current`. Only six numbers per hand are needed, which makes retargeting and imitation learning unusually simple.

## Compute, sensors and connectivity

**Compute:** none on board. The hand is a bus slave; you bring a laptop or an SBC (x86_64, ARM64 such as Raspberry Pi or Jetson-class boards, Apple-silicon Mac, Windows PC).

| Item | DH116 | DH116S | DH2116 |
|---|---|---|---|
| DoF (active) | 11 (6) | 11 (6) | 21 (16) |
| Drive | brushless coreless motor + worm gear | same, miniaturised | brushless coreless + trapezoidal screw |
| Size / weight | 545 g ± 10 g | 147.54 × 73.53 × 26.35 mm, **359 g ± 10 g** | 218 × 119 × 80.5 mm, **850 g ± 10 g** |
| Supply | **12–48 V**, 2.5 A | **12–48 V**, idle 0.1 A, max 2.0 A | **24–60 V**, idle 0.16 A, rated 1 A, max 5 A (at 24 V) |
| Buses (by model code) | CAN FD (`DH116-…`) or EtherCAT (`DH116EC-…`); RS485 mentioned | CAN FD (`DH116S-…`), EtherCAT (`DH116SEC-…`), RS485 (`DH116SRS-…`) | CAN 1 Mbps, CAN FD 1 / 5 Mbps, RS485 up to 5 Mbps (no EtherCAT listed) |
| Tactile option | `-M`: multi-modal (normal, tangential, proximity) | `-S`: piezoresistive; `-M`: multi-modal; fingers + palm | not documented in the manual |
| Load / speed | hook grip ≤ 30 kg, lateral grip ≤ 50 N, open-close ≥ 0.5 s | hook grip 15 kg, side grip 50 N, open-close 0.4 s | recommended load 5 kg, max five-finger grip 150 N (product page: 94 N), open-close 0.6 s |
| Repeatability | ±0.2 mm | ±0.2 mm | ±0.6 mm |
| Life | 1 million grasp cycles (claim) | 1 million cycles, 3-year design life | 300,000 cycles, 2-year design life |
| Environment | −10…40 °C table value (precautions say 0–40 °C) | −10…45 °C, IP30 | — |
| In the box / accessories | — | options: variable PSU (KJS-1509), 0.5 m EtherCAT cable, MINI USB-CANFD-I adapter, data glove | M9 debug cable + **PCAN-USB** module |

**Tactile resolution (DH116S manual):** palm normal force 0.1 N over 0–25 N; fingers normal force 0.01 N over 0–20 N; tangential force 0.01 N with direction 0–360° at 1° resolution.

**Wiring**

| Hand | Pins / wire colours |
|---|---|
| DH116 (CAN FD) | red VDC · green GND · yellow CANH · black CANL |
| DH116 (EtherCAT) | red VDC · green GND · brown RX+ · white RX− · yellow TX+ · black TX− |
| DH116S | pins 1, 2 VDC · pins 5, 6 GND · pin 3 CANH / 485+ · pin 4 CANL / 485− (CAN FD or RS485, one or the other) |

**Host adapters:** CAN FD via a gs_usb / candleLight-type USB adapter (vendor examples reference USB ID `a8fa:8598`, "CANFD Analyser") or any SocketCAN interface; standard CAN on Windows via PCAN; RS485 via any USB-serial adapter (vendor default 500 000 baud in ROS config); EtherCAT via a spare wired Ethernet port.

## First 60 minutes checklist

1. **Identify the unit (5 min).** Read the label: `DH116` / `DH116S` / `DH2116`, `EC` or `RS` in the code (bus), `L` / `R`, `-M` / `-S` (tactile). Ask whether it was built **before or after 2026-02-10** and which adapter, cable and power supply come with it.
2. **Get the software from staff on a USB stick (5 min)** — or download: SDK package and manual from the [SDK releases](https://github.com/sorrowfeng/LHandProLib-Releases/releases), GUI from the [LHandPro releases](https://github.com/sorrowfeng/LHandPro-Releases/releases), models from [leadtron_hand_descriptions](https://github.com/sorrowfeng/leadtron_hand_descriptions). Do not rely on the Feishu links working on hackathon Wi-Fi.
3. **Power and wire (5 min).** Power off first. 24 V bench supply with current limit about 2.5 A (DH116 / DH116S) or 5 A (DH2116). Connect the bus per the wiring table. Keep fingers clear.
4. **Verify with the GUI (10 min).** Start LHandPro, select the bus and adapter, connect, check firmware version and serial number, **home** the hand, jog each joint, play a preset gesture. If the GUI cannot connect, code will not either — fix node ID / baud rate / adapter driver here.
5. **Linux permissions (5 min).**
   - CAN FD (userspace gs_usb): install the udev rule shipped in the workspace (`99-hand-control-usb.rules`), then re-plug the adapter. `LIBUSB_ERROR_ACCESS` means the rule is missing.
   - RS485: `sudo usermod -aG dialout $USER`, then log in again.
   - EtherCAT: `sudo setcap cap_net_raw,cap_net_admin+ep <service binary>`.
6. **Hello-world motion, ROS 2 route (15 min).** Ubuntu 22.04 + Humble:
   ```bash
   cd hand_control_ws && source /opt/ros/humble/setup.bash
   colcon build --symlink-install && source install/setup.bash
   # edit src/hand_control_service/config/service.yaml: bus type, address, hand_type
   ros2 launch hand_control_service service.launch.py
   ros2 service list | grep hand_control        # then: enable, home, move
   ros2 service call /hand_control/set_enable hand_control_interfaces/srv/SetEnable "{joint_id: 0, enable: 1}"
   ros2 service call /hand_control/set_position hand_control_interfaces/srv/SetPosition "{joint_id: 3, position: 5000}"
   ros2 service call /hand_control/move_motors hand_control_interfaces/srv/MoveMotors "{joint_id: 0}"
   ```
   Call the `home_motors` service before the first move (look up its type with `ros2 service type`). With the official `lhandpro_ws` instead: `colcon build`, copy `libLHandProLib.so` to `/usr/local/lib`, `sudo ldconfig`, `ros2 launch lhandpro_service lhandpro.launch.py`, then `ros2 launch sequence_demo_py sequence.launch.py`.
7. **Hello-world motion, SDK route (alternative).** Run the bus example from `share/LHandProLib/examples/` (`CANFD_cpp`, `RS485_cpp`, `EtherCAT_cpp`, or the `*_python` folders). The call order is always: register send callback → feed receive data → `initial(mode[, node_id])` → `set_control_mode(0, LCM_POSITION)` → `set_enable(0, 1)` → `home_motors(0)` → `set_target_angle(i, deg)` + `set_angular_velocity(i, 200)` + `set_max_current(i, 1000)` → `move_motors()`.
8. **Read sensors (5 min).** `ros2 topic echo /hand_control/realtime_state` and `ros2 topic hz …` (expect about 100 Hz). Tactile: set `tactile_enabled: true` in the YAML, call `set_finger_pressure_reset`, then `ros2 topic echo /hand_control/hand/tactile_state`. SDK route: `get_now_angle`, `get_now_current`, `get_finger_normal_force`.
9. **Start the twin (5 min).** `ros2 launch hand_control_description display.launch.py` — RViz2 should follow the real hand. No hardware yet? Load the MJCF in MuJoCo or enable SDK dry-run and keep coding.
10. **Lock in a safe default.** Decide a conservative `set_max_current` (start at 300–500 ‰) and speed for anything near people, and write them into your launch config before building further.

## Known gotchas and safety

**Version and configuration traps**

- **Generation split at 2026-02-10 (DH116):** the manual lists separate "old version" SDK, URDF, ROS 2 project, GUI and protocol files for units made earlier. Mixing generations is the most likely cause of a hand that connects but behaves wrongly.
- **Hand type must match:** `LAC_DOF_6` (DH116), `LAC_DOF_6_V2` (DH116 V2), `LAC_DOF_6_S` (DH116S), `LAC_DOF_16` (DH2116). Over EtherCAT the SDK auto-detects type, side, firmware and serial via SDO; on other buses set it yourself.
- **Homing first:** motion calls return `LER_NOT_HOME` until `home_motors` has run, unless you explicitly allow `set_move_no_home(1)`.
- **Units are unusual:** current in **per-mille**, stroke position **0–10000**, DH2116 motor commands **0–4095**, speed in °/s or counts/s depending on the call.
- **`LER_KEY_FUNC_UNINIT` from `initial()`** = send callback not registered. Sensor values frozen = you stopped feeding received frames into the SDK.
- **ROS 2 parameters must be floats:** `tactile_publish_rate_hz: 50` (integer) crashes the node; write `50.0`.
- **EtherCAT NIC index:** the official example hard-codes the network interface index in `hand_control_service.cpp`; change it and rebuild. The newer workspace takes it from YAML (`channel`).
- **CAN FD driver conflict:** the userspace gs_usb backend and the Linux kernel `gs_usb` driver cannot both hold the adapter. Use one or the other (the workspace has a build switch for SocketCAN; clean-rebuild after switching).
- **RS485 is half-duplex and slow:** about 33 transactions per second for the whole bus by default; two hands on one port need the SDK's `RS485SharedBus`, not two polling loops.
- **Duplicate ROS nodes** (after Ctrl+C) make the RViz model jump between two states — check `ros2 topic info -v /joint_states` shows one publisher.
- **The ROS 2 PDF suggests a third-party one-line installer for ROS**; use the standard `apt` install instead.
- **Documentation inconsistencies** (do not quote blindly in your pitch): DH116S weight 359 g (manual) vs 379 g (trade-show material) vs "< 380 g" (store); DH116S load 15 kg hook grip (manual table) vs 10 kg "light-load handling" (manual text); DH2116 grip 150 N (manual) vs 94 N (product page); robot overview page says CANopen where the manuals say CAN FD.

**Safety**

- The hands are strong: DH116 hook-grip load up to 30 kg and 50 N lateral grip. **Pinch hazard** — keep `set_max_current` low and add a software stop (`stop_motors`) on a key.
- **Worm-gear fingers are self-locking.** Do not force them by hand; they do not back-drive and reset on power-up. This also means a hand that loses power **keeps gripping** — plan how to release an object or a person's finger.
- No functional-safety features (STO, certified force limiting) are documented for the hands; they are components, not certified for contact with patients. For T04 demos use dummies or keep contact forces minimal and supervised.
- Power off before plugging or unplugging; do not open the housing or remove the tamper label; avoid dust, moisture and oil (DH116S is IP30); stop and let it cool if it gets hot.
- Avoid collisions of the fingers with the arm or table — plan arm paths with the hand's open envelope.
- macOS GUI build is ad-hoc signed and not notarized (Gatekeeper prompt). Firmware OTA exists in the GUI — **do not flash firmware on a loaned unit** without staff.

## Community resources

| Resource | Link | Use |
|---|---|---|
| SDK releases + manuals (EN / CN) | [LHandProLib-Releases](https://github.com/sorrowfeng/LHandProLib-Releases/releases) | API reference, changelog, packages |
| GUI releases | [LHandPro-Releases](https://github.com/sorrowfeng/LHandPro-Releases/releases) | bring-up tool |
| ROS 2 workspace | [hand_control_ws](https://github.com/sorrowfeng/hand_control_ws) | services, topics, multi-hand configs, troubleshooting section |
| URDF / MJCF | [leadtron_hand_descriptions](https://github.com/sorrowfeng/leadtron_hand_descriptions) | simulation, RViz |
| Embedded Python demo | [RaspberryPiDemo](https://github.com/sorrowfeng/RaspberryPiDemo) | reference Python wrapper, sequences, glove input |
| User manuals (PDF) | [DH116 / DH116P](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf) · [DH116S](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf) · [DH2116](https://store.leadshine.com/cdn/shop/files/DH2116_Series_Dexterous_Hand_User_Manual.pdf) | specs, pinouts, download links |
| Downloads (drives, PLCs) | [leadshine.com/downloads](https://www.leadshine.com/downloads.html) | manuals, tuning software, 3D models |
| Contacts | sales@leadshine.com · North America: sales@leadshineusa.com · China robot-components hotline 400-155-8078 | pre-sales and support |

- **No forum, Discord, developer portal or official GitHub organisation** was found. Repositories above have near-zero stars — there is no community to ask; **the Leadshine / Leadtron engineers on site are the support channel**.
- Questions worth asking them first: protocol documents for your bus; gesture ID list; whether a `ros2_control` driver or DH2116 ROS 2 package exists internally; PJ3 / HJ2 protocol and control modes; spare adapter and flange drawings.

## Sources

- [Leadshine profile in this knowledge base (first pass)](Leadshine.md)
- [DH116 / DH116P user manual (PDF, Leadshine store)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf)
- [DH116S user manual (PDF, Leadshine store)](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf)
- [DH2116 user manual (PDF, Leadshine store)](https://store.leadshine.com/cdn/shop/files/DH2116_Series_Dexterous_Hand_User_Manual.pdf)
- [DH116S LHandPro ROS2 example project description (PDF, Leadshine store)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [LHandProLib SDK releases and SDK manual v1.8 (GitHub release mirror)](https://github.com/sorrowfeng/LHandProLib-Releases/releases)
- [LHandProLib release 20261031 (links the Feishu SDK page)](https://github.com/sorrowfeng/LHandProLib-Releases/releases/tag/20261031)
- [LHandPro GUI releases (GitHub release mirror)](https://github.com/sorrowfeng/LHandPro-Releases/releases)
- [hand_control_ws ROS 2 workspace README](https://github.com/sorrowfeng/hand_control_ws)
- [leadtron_hand_descriptions (URDF / MJCF, Apache-2.0)](https://github.com/sorrowfeng/leadtron_hand_descriptions)
- [RaspberryPiDemo README and Python wrapper](https://github.com/sorrowfeng/RaspberryPiDemo)
- [gsusb-canfd README](https://github.com/sorrowfeng/gsusb-canfd)
- [DH116 deployment kit repository (third-party upload)](https://github.com/carolyang823/Leadshine-Cost-Effective-Dexterous-Hand-DH116-Designed-for-Humanoid-Robots-)
- [openvmp/stepper_driver_em2rs (third-party ROS 2 package)](https://github.com/openvmp/stepper_driver_em2rs)
- [DH2116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [Leadshine robot components overview](https://www.leadshine.com/robot/index.html)
- [PJ3 series product page](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html)
- [HJ2 series product page](https://www.leadshine.com/robots/integrated-actuators/hj2-series.html)
- [Leadshine offices and contacts](https://en.leadshine.com/contact/contact_leadshine_offices.html)
- [Leadshine Chinese site — robot core components](https://www.leisai.com/product_1073.html)
- [Investor research note, July 2026 (10jqka)](https://stock.10jqka.com.cn/20260723/c678395454.shtml)
- [WeChat: Leadshine tactile dexterous hand on CCTV, Aug 2026](https://mp.weixin.qq.com/s/BzrqQMtciwjRFgLOlOiouQ)
