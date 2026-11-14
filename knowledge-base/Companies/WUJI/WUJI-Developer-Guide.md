---
type: dev-guide
company: "WUJI"
slug: WUJI
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# WUJI — Developer Guide (hackathon edition)

⬆ [WUJI profile](WUJI.md) · [Product portfolio](WUJI-Products.md) · [Roadmap and strategy](WUJI-Roadmap-and-Strategy.md)

> **Scope:** WUJI is a component vendor: two 20-DoF hands (Wuji Hand gen 1, Wuji Hand 2) and a tactile + pose glove (Wuji Glove). There is no arm, base or on-board computer. Everything below is about driving the hand joints and reading the glove from your own PC. All facts are from the official docs (docs.wuji.tech, state of **2026-11-10**) and the `wuji-technology` GitHub repos unless marked.

## TL;DR — how you program it

- **One SDK for everything:** `pip install wuji-sdk` (Python, CPython 3.8–3.14) or the C package. Same API pattern for Hand 2, Hand gen 1 and Glove: `device.{resource}().{get|set|subscribe|publish}()`.
- **Joint level only:** you send 20 joint targets at up to **1 kHz**. Hand 2 defaults to **MIT mode** (position + velocity + current feed-forward, per-joint kp / kd); whole-hand **position mode is Beta** and needs firmware **v3.0.0**. There is no grasp planner, no perception, no skill library.
- **Wired, static IP:** Hand 2 and Glove talk Ethernet on `192.168.1.x` (no DHCP); Hand gen 1 is USB. Budget one wired NIC (or a switch) per team laptop.
- **Fastest demo = glove teleop:** `examples/python/retargeting/1.teleop_real.py` mirrors a Wuji Glove onto a hand; official estimate **45 min** from unboxing. No glove free? Any source of 21 MediaPipe keypoints (webcam, VR headset) feeds the same `RetargetSession`.
- **Develop without hardware:** `wuji-description` has URDF / MJCF / MJX / USD for all hand revisions; a MuJoCo viewer check takes **10 min**. ROS 2 drivers (`wuji-ros2`) exist but target **Ubuntu 26.04 + ROS 2 Lyrical** only.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| ✅ **Wuji SDK** (`wuji-sdk`) | Python (primary), C11 | Hand 2, Hand gen 1, Glove: discovery, connect, streams, joint commands, parameters, MCAP recording, retargeting | [repo](https://github.com/wuji-technology/wuji-sdk) · [docs](https://docs.wuji.tech/docs/en/wuji-sdk/latest/introduction.md) | MIT. Linux x86_64 / arm64 (glibc ≥ 2.17 Python, ≥ 2.31 C), macOS 11+ Apple silicon, Windows 10 21H2+ / 11 x64. C package also for Android aarch64. Current release **v2026.11.9** |
| ✅ **Wuji CLI** (`wuji`) | Binary (terminal) | Scan, ping, get / set parameters, subscribe, live viewer, glove calibration, health check, logs, firmware upgrade | [docs](https://docs.wuji.tech/docs/en/wuji-cli/latest/introduction.md) · [repo](https://github.com/wuji-technology/wuji-cli) | Install: `curl -fsSL https://get.wuji.tech/cli \| bash` (Linux / macOS), `irm https://get.wuji.tech/cli.ps1 \| iex` (PowerShell). `--json` / `--jsonl` output for scripts |
| ✅ CLI agent skills | Skill bundle | Lets an AI coding agent run the CLI (scan, calibrate, doctor, logs, upgrade, viz) | [CLI getting started](https://docs.wuji.tech/docs/en/wuji-cli/latest/getting-started.md) | `npx --yes skills add wuji-technology/wuji-cli -g`. Docs warn: the agent can write parameters and move hardware — review before it runs |
| ✅ **wuji-ros2** | C++ / ROS 2 | `wuji_hand2_driver` (states, commands, services), `wuji_glove_driver` (data only), `wuji_msgs`, `wuji_bringup`, `wuji_tools` | [repo](https://github.com/wuji-technology/wuji-ros2) · [Hand 2 guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/ros2-integration.md) · [Glove guide](https://docs.wuji.tech/docs/en/wuji-glove/latest/ros2-integration.md) | MIT. **ROS 2 Lyrical on Ubuntu 26.04**, x86_64 / aarch64. Source build; release notes also mention the apt package `ros-lyrical-wuji-bringup` |
| ✅ **wuji-description** | URDF, MJCF, MJX, USD, STEP | Models of Hand gen 1, Hand 2.1, Hand 2.2 and the glove hand skeleton | [repo](https://github.com/wuji-technology/wuji-description) · [loading guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/model-integration.md) | MIT. ROS 2 packages `wuji_hand2_1_description`, `wuji_hand2_2_description` |
| ✅ SDK retargeting (`RetargetSession`) | Python, C | 21 keypoints (MediaPipe order, metres) → 20 joint angles for Hand or Hand 2 | [docs](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md) | Built into the SDK; needs only `numpy`. Wheels with retargeting: Linux x86_64 / aarch64 and macOS arm64 — **not Windows, not Intel Mac** |
| ✅ **wuji-mjlab** | Python (mjlab, PPO) | RL: in-hand cube reorientation (both generations), pen spinning (Hand 2), sim-to-real bridge | [repo](https://github.com/wuji-technology/wuji-mjlab) | Apache-2.0. Linux x86_64, NVIDIA GPU, CUDA 12.8, **pixi only** |
| ✅ **wuji-isaaclab** | Python (Isaac Lab 2.3.2, rsl_rl) | Cube reorientation for Hand 2 in Isaac Sim 5.1 | [repo](https://github.com/wuji-technology/wuji-isaaclab) | Apache-2.0. glibc ≥ 2.35, NVIDIA driver ≥ 580.65.06 |
| ✅ **wuji-openpi** | Python (JAX), ROS 2 Humble | Fine-tune and deploy pi0 / pi0.5 on single- or dual-arm + Wuji Hand rigs | [repo](https://github.com/wuji-technology/wuji-openpi) | Apache-2.0 fork of Physical Intelligence openpi. Linux x86_64, CUDA 12, Python 3.11+, `uv` |
| ✅ **toporetarget** | Python | Human hand-object motion → Wuji Hand reference motion (CPU only) | [repo](https://github.com/wuji-technology/toporetarget) | MIT. Research code (CoRL 2026 paper) |
| ✅ wuji-hand-teleop | ROS 2 Humble, Docker | Glove → hands, HTC Vive Tracker / PICO 4 → arms, stereo video to headset, MCAP capture | [repo](https://github.com/wuji-technology/wuji-hand-teleop) | MIT. README: **not actively maintained**; reference arms are Tianji 7-DoF |
| Legacy: `wujihandpy`, `wujihandros2`, Wuji Studio, HMI, Upgrader, `wuji-retargeting` | Python / ROS 2 / desktop | Hand gen 1 tooling | [archived docs](https://docs.wuji.tech/docs/en/archived.md) | Superseded by SDK + CLI. `pip install wujihandpy` still works for gen 1 (Ubuntu 22.04 / 24.04) |

**Low-level transport:** Hand 2 and Glove use a proprietary UDP protocol (Hand 2 port **50001**; glove examples in the docs show both `:50000` and `:50001`, so use the address `wuji devices` prints); Hand gen 1 uses a proprietary USB 2.0 protocol. No public CAN, EtherCAT, Modbus or raw-protocol spec was found — the SDK is the supported entry point.

## Control levels

| Level | Available? | Detail |
|---|---|---|
| Task / skill API (grasp, pinch, handover) | ✗ none | You write grasps as joint trajectories, teleoperate, or learn them |
| Grasp planning / perception | ✗ none | Bring your own camera and planner |
| Retargeting (human hand → 20 joints) | ✅ | `RetargetSession.for_hand(HandModel.WujiHand2, side=Handedness.Right)`, then `session.step(keypoints)` |
| Joint position targets | ✅ | Hand 2: MIT mode with kp / kd, or position mode (Beta). Hand gen 1: position control only |
| Joint impedance (MIT) | ✅ Hand 2 | `τ = kp·(q_d − q) + kd·(dq_d − dq) + τ_ff`; set with `hand.mit_params().set((kp, kd))` or a list of 20 |
| Current feed-forward | ✅ Hand 2 | `JointCommand(position, velocity, effort)`; `effort` is **current in A** in MIT mode |
| True joint-torque control / external force sensing | ✗ | `joint_states.effort` is measured current (MIT) or an estimated net torque in N·m (position mode). Docs say **do not** use it to judge contact force on 2.2 units |
| Firmware / motor-driver access | ✗ | Closed firmware; upgrades via `wuji upgrade` |

**Rates and numbers (Hand 2):**

| Item | Value |
|---|---|
| Device control loop | **1000 Hz × 20 axes** (one message carries all 20 joints) |
| Command publish rate | up to **1 kHz** (`hand.joint_command().publish()`) |
| `joint_states` stream | **1000 Hz** native; lower it with `sub.set_rate(hz)` |
| IMU stream | **100 Hz** (angular velocity + acceleration, no orientation) |
| GET queries | keep at or below **100 Hz** |
| Conservative MIT start values | `effort_limit = 0.5 A` for first tests; gentle hold at `kp = 3.0`, `kd = 0.05`, `effort_limit = 1.5 A` |
| Factory MIT defaults on new units | kp = 5.0, kd = 0.1 (per the solutions register; check the SDK log line printed on connect) |
| Position mode (Beta) | needs firmware **v3.0.0**; limits in **N·m**, default **300 %** of each joint's rated torque; command low-pass default **40 Hz**; mode resets to MIT after every power cycle |
| Joint order | thumb 0–3, index 4–7, middle 8–11, ring 12–15, pinky 16–19 (`{finger}_S1..S4`) |
| Units | rad, rad/s; angles only from `joint_states` |

**Hand gen 1:** position control, 1000 Hz × 20 axes, USB. It is **not back-drivable** — never force the fingers by hand. Driven by the unified SDK on Linux and Apple-silicon macOS (not Windows), or by the older `wujihandpy` (`hand.finger(1).joint(0).write_joint_target_position(1.57)`).

**Editions:** no EDU / developer / pro tiers are published. Every unit exposes the same SDK. What differs is the **hardware revision**:

| Revision | How to tell | What you get |
|---|---|---|
| Hand 2.2 Beta | serial positions 5–7 = `A01` | current firmware line (v3.0.0 on 2026-11-10), 11–13 V input, position mode (Beta), soft-pad link in the models. Built-in feed-forward compensation only on units shipped from October 2026 |
| Hand 2.1 Beta | serial `A00` | **12 V only**, firmware frozen at v1.2.4, newer SDK features (including position mode) unavailable; use `model_revision:=1` in ROS 2 |
| Hand gen 1 | USB device | position control, self-locking joints, optional paired tactile glove (`hand.is_tactile_attached()`) |

## ROS 2 and middleware

- **Official target:** Ubuntu **26.04** + ROS 2 **Lyrical**, x86_64 or aarch64. If your laptop runs Humble or Jazzy, either use a container with host networking or skip ROS and bridge the Python SDK into your own node (about 30 lines: subscribe `joint_states`, publish `JointCommand`).
- **Build:** clone `wuji-ros2`, run `scripts/install_hand2_descriptions.sh`, `rosdep install`, `colcon build --cmake-args -DBUILD_TESTING=OFF`. The build downloads the C SDK (v2026.10.12); offline builds pass `-DWUJI_SDK_ROOT=<path>`.
- **Find devices:** `ros2 run wuji_tools wuji_list`.

| Hand 2 interface (namespace-relative) | Type | Notes |
|---|---|---|
| `joint_states` (pub) | `sensor_msgs/msg/JointState` | position rad, velocity rad/s, `effort` = **current in A** |
| `joint_diagnostics` (pub) | `wuji_msgs/msg/JointDiagnosticsArray` | status words, fault codes, voltage, temperature |
| `imu` (pub) | `sensor_msgs/msg/Imu` | no orientation (`orientation_covariance[0] = -1`) |
| `joint_commands` (sub) | `sensor_msgs/msg/JointState` | named subset or 20 values in fixed order. **Unlisted joints are driven to zero** |
| `set_enabled`, `clear_faults` | `wuji_msgs/srv/…` | 20-entry mask |
| `set_effort_limit(s)`, `set_mit_params` | `wuji_msgs/srv/…` | current limits in A; 20 kp / kd values |
| `emergency_stop` | `std_srvs/srv/Trigger` | not latched: stop publishing afterwards |

- **Launch:** `ros2 launch wuji_bringup hand2_view.launch.py serial_number:=… hand_side:=… model_revision:=2 namespace:=hand` (view only, never enables), `hand2.launch.py … auto_enable:=true` (control), then `ros2 run wuji_bringup hand2_wave_demo --ros-args -r __ns:=/hand` (100 Hz wave).
- **Glove driver:** `ros2 launch wuji_bringup glove.launch.py serial_number:=… namespace:=glove`. 10 topics: `joint_angles`, `emf_poses`, `tip_poses`, `hand_skeleton`, `imu/palm`, `tactile`, `tactile/residual`, `tactile/binary`, `tactile/zones`, `tactile/points` (PointCloud2). All **best-effort** QoS — a reliable subscriber receives nothing. The glove driver holds an **exclusive** connection (no `wuji viz` in parallel).
- **TF:** the hand model root is `l_mount` / `r_mount` (the arm flange mount). Your arm stack must publish the transform from its tool flange to that frame.
- **DDS:** if RViz shows no TF or demos get no data, check namespace and `ROS_DOMAIN_ID`, then try `rmw_cyclonedds_cpp`.
- **Other middleware:** the SDK "bridge" (`enable_bridge=True`, default) lets several SDK processes — also on other hosts — share one device. `wuji-hand-teleop` and `wuji-openpi` use **ROS 2 Humble** inside Docker with their own topic layout, separate from `wuji-ros2`.

## Simulation and digital twins

| Asset | Format | How to load | Notes |
|---|---|---|---|
| Hand 2.2 | MJCF | `python -m mujoco.viewer --mjcf=hand2/hand2_2/body/mjcf/right.xml` | MuJoCo 2.3+. 20 revolute joints; collision = convex hull per link, 27 colliding links |
| Hand 2.2 | USD | `hand2/hand2_2/body/usd/{left,right}/wujihand2_2.usd` | Isaac Sim 2024.x+; keep the whole `usd/` folder (layered asset) |
| Hand 2.2 | URDF (+ ROS variant) | `urdf-viz hand2/hand2_2/body/urdf/right.urdf` or RViz via `wuji_bringup` | URDF is the source of truth for the mount frame |
| Hand 2.1, Hand gen 1 | URDF, MJCF, MJX, USD | same repo, per-revision folders | bare, cover and glove variants |
| Glove hand skeleton | URDF (21 DoF) + EMF module STL | `urdf-viz glove/body/urdf/right.urdf` | for checking frames and data mapping |
| CAD | STEP, A3 drawings | palm mounting interface, flange mount (69 g), full hand | re-download if fetched before 2026-11-10 (STEP files were corrected) |

- **Actuator names in the models:** `{l,r}_{THJ|FFJ|MFJ|RFJ|LFJ}{0-3}`. The mapping between SDK labels `S1..S4` and model actuators `J0..J3` is **not published yet** — verify joint by joint in the viewer before trusting a sim-to-real script.
- **Limits:** rigid-body only; fingertip soft pads are separate rigid links, no deformable simulation. Joint limits in the models match the real hand and are mirrored left / right.
- **RL environments:** `wuji-mjlab` (MuJoCo Warp, tasks Cube Reorient and PenSpin) and `wuji-isaaclab` (`Wuji-Hand2-Reorient-v0`). Both export ONNX; the mjlab repo carries the sim-to-real deployment stack.
- **Live digital twin:** `wuji viz` opens a Rerun web viewer where a 3D hand follows the real joint states (Hand 2) or shows skeleton + tactile matrix (Glove). One viewer page per session.

## AI stack

| Piece | Status | What exists | Hackathon reality |
|---|---|---|---|
| WUJI foundation model / VLA weights | ✗ not published | none | Do not plan on a WUJI checkpoint |
| VLA fine-tuning | ✅ `wuji-openpi` | pi0 / pi0.5 supervised fine-tuning, policy server (WebSocket / ROS 2), reference config `pi05_wuji_multi_54d` (7 + 7 arm, 20 + 20 hand = **54-D**); arm count and DoF are config values | Needs CUDA 12 GPU, upstream `pi05_base` weights and your own demos (WUJI's report used 200 per skill). Tight for 48 h |
| LeRobot | ◐ dataset format only | `wuji-openpi` trains on **LeRobot v2.1** datasets converted from ROS 2 MCAP; expected keys `observation.state`, `observation.images.cam_high`, `cam_left_wrist`, `cam_right_wrist`, `action` | No native LeRobot robot / teleoperator plugin for Wuji devices was found. The README describes the conversion step but check the repo for the converter before you rely on it |
| Pretrained RL policies | ✅ | `wuji-mjlab` release **v2026.10.22**: cube-reorient checkpoints per hand and five pen-spin sets (`model.pt`, `policy.onnx`), 40 motion clips, jig CAD | Replays need the camera + tag rig from the repo; a show piece, not a track solution |
| Retargeting | ✅ | SDK `RetargetSession`; `toporetarget` for contact-preserving object manipulation references | The practical "AI" most teams will use |
| Teleoperation | ✅ | Glove → hand (`1.teleop_real.py`, Python and C); hand + arm via `wuji-hand-teleop` (unmaintained) | Hand-only teleop works in under an hour; arm teleop means integrating a partner arm yourself |
| Data collection | ✅ | `TopicRecorder` → **MCAP** (LZ4), multi-device, episodes, live metrics and alerts; glove raw data can be re-solved offline | Record `joint_states` + glove streams with device-side UTC-synced timestamps |
| Egocentric data model | ✅ (research) | MINT: video → two-hand motion, weights and annotations for 1,021 h of video | See [papers](WUJI-Papers-and-Research.md); not needed for a first build |

Minimal recording pattern (Python): `recorder = TopicRecorder(compression="lz4")`, `recorder.record(hand.joint_states().subscribe())`, `handle = await recorder.start("./data/episode_001.mcap")`; start again with a new path for the next episode.

## Compute, sensors and connectivity

| Item | Hand 2 (2.2 Beta) | Hand gen 1 | Glove |
|---|---|---|---|
| On-board application compute | none | none | none (acquisition board on the forearm) |
| Host | your PC / Jetson-class board; WUJI benchmarks on Jetson AGX Orin | same | same |
| Data link | **RJ45 Ethernet 100BASE-TX**, static IP | **USB 2.0** (USB-C) | RJ45 via USB-C-to-Ethernet power adapter |
| Default address | left `192.168.1.110`, right `192.168.1.111`, port 50001 | — (USB) | left `192.168.1.100`, right `192.168.1.101` |
| Power | **11–13 V DC**, ≥ 200 W, XT30; 12 V 20 A adapter supplied | 12–20 V DC, XT30, ≥ 10 A, 420 W transient | USB 5 V / 1 A |
| Sensors | joint position, velocity, current; per-joint temperature and voltage (diagnostics); IMU 100 Hz. **No tactile, no camera** | joint state; optional tactile glove accessory | 526-point tactile matrix 120 FPS; 5 EMF 6-DoF trackers 120 Hz; IMU 800 Hz |
| Derived streams | — | — | tactile zones, binary contact, residual, 3D tactile point cloud, fingertip poses, 21-DoF joint angles, 21-keypoint skeleton, fused IMU |
| Wireless | none | none | none |
| Time base | device timestamps synced to host UTC by the SDK (NTP-style exchange) | host-stamped | device-stamped, synced |
| Status light | blue breathing = self-check, white breathing = ready, solid white = enabled, red slow flash = fault, solid red = critical (power-cycle) | blue solid = firmware update in progress | see glove docs |

- **Multi-client:** several SDK programs can share a device by default (visualiser + recorder + your app). The CLI falls back to read-only when another session owns the device.
- **Telemetry:** the SDK uploads anonymous usage data by default; disable with `WUJI_TELEMETRY_DISABLE=1`.
- **Docker:** official image recipe in `wuji-sdk/docker` (Ubuntu 22.04, Python 3.10); run with `--network host` and mount `~/.wuji` for calibration data.

## First 60 minutes checklist

1. **Ask WUJI staff (2 min):** which hand revision (gen 1, 2.1 or 2.2), which firmware, left or right, which flange adapters, and whether you may upgrade firmware yourself. Read the serial number: 4th character `J` = left, `K` = right.
2. **Sim check, no hardware (10 min):** `git clone --depth 1 https://github.com/wuji-technology/wuji-description.git && pip install mujoco && python -m mujoco.viewer --mjcf=wuji-description/hand2/hand2_2/body/mjcf/right.xml`. Done when 20 joints render.
3. **Install (5 min):** `python -m pip install wuji-sdk numpy`; `curl -fsSL https://get.wuji.tech/cli | bash`; verify with `python -c "from wuji_sdk import SdkManager"`.
4. **Wire Hand 2 (5 min):** RJ45 to your laptop, XT30 to the hand first, then plug in the adapter. Wait for blue → white breathing (under 30 s). Clear the finger workspace.
5. **Network (5 min):** set your wired NIC to `192.168.1.50/24` (Linux: `sudo ip addr add 192.168.1.50/24 dev <iface>`). `ping 192.168.1.111` (right) or `.110` (left).
6. **Verify (3 min):** `wuji devices` then `wuji ping` — note serial, firmware, IP. With several hands on one switch always pass `--sn`.
7. **Connect and health-check (5 min):**
   `hand = SdkManager.instance().connect(sn="<SN>", device_name="hand")`; `print(hand.online_joints_count().get())` must print **20**; subscribe `hand.joint_diagnostics()` and decode any `error_code_current` with `WujiHand2.describe_error(code)`.
8. **Hello-world motion (10 min):** `hand.effort_limit().set(1.5)`; `hand.mit_params().set((3.0, 0.05))`; `hand.enable()`; read the current pose from `hand.joint_states().subscribe()`; then publish `JointCommand(position, 0.0, 0.0)` × 20 through `hand.joint_command().publish()` at 200 Hz, interpolating to zero over 1.5 s. Never send a step change. The official script is in the [Hand 2 quick start](https://docs.wuji.tech/docs/en/wuji-hand/latest/quick-start.md); ready-made motions: `examples/python/wuji_hand_2/7.mit_sweep.py` (tiny single-joint sweep) and `8.position_mode.py`.
9. **Read sensors (5 min):** `wuji viz --sn <SN>` for the live 3D view; in code, `sub = hand.joint_states().subscribe(); frame = sub.recv()` (position, velocity, current) and `hand.imu().subscribe()`.
10. **Glove (10 min, if you have one):** wire the acquisition board (mind the USB-C label orientation), `ping 192.168.1.101`, put the glove on with fingers relaxed, `wuji doctor`, then `sub = glove.hand_skeleton().subscribe()` and `glove.tactile().subscribe()`. Run `python examples/python/retargeting/1.teleop_real.py` (press Enter for the default SDK user; set `SIDE` for a left hand).
11. **Stop cleanly:** `hand.disable()`; `manager.disconnect_all()`; power down only when the hand is at rest. Emergency: `hand.emergency_stop()`.

Hand gen 1 variant of steps 4–8: plug USB-C + power, on Linux add the udev rule from the [gen-1 SDK guide](https://docs.wuji.tech/docs/en/wujihandpy/latest/introduction.md), connect with `manager.connect(sn=<usb device sn>, device_name="wuji_hand")` after filtering `manager.scan()` by `TransportType.Usb`.

## Known gotchas and safety

- **Beta hardware.** Hand 2.1 and 2.2 are prototypes: docs give **no guarantee** on durability, drop, thermal behaviour or load values, and ask you not to run long high-load tests. Treat the hand as borrowed lab equipment.
- **No safety-rated function.** Thermal derating, over-current stop and soft limits protect the device, not people. Keep hands away from moving fingers; do not grasp fragile or valuable objects.
- **High kp + big step = full-speed fingers.** Always ramp targets and start with a low `effort_limit`.
- **Teleop example needs new firmware.** Since 2026-11-10 the SDK teleop examples switch Hand 2 to position mode first; on firmware older than v3.0.0 the mode switch fails and the example exits. Either upgrade (`wuji upgrade`, never cut power) or pin an SDK / example version that matches the firmware.
- **Mode confusion.** `effort` and `effort_limit` are **A** in MIT mode and **N·m** in position mode; limits are not converted when you switch. Control mode resets to MIT at power-up.
- **ROS 2 driver has no command watchdog.** Stopping your publisher does not stop the hand; a named `joint_commands` message drives unlisted joints to zero; `emergency_stop` is not latched.
- **Comms loss.** With firmware v2.1.0+ a dropped link while enabled stops the motors and raises a fault; you must call `enable()` again. No hot-plugging of power or Ethernet.
- **Static IP collisions.** All left hands ship as `.110`, all right hands as `.111`, gloves `.100` / `.101`. Two teams on one switch will collide — change the device IP (SDK device operations) or keep each rig on its own NIC. `connect(handedness=…)` raises `AmbiguousHandedness` when two same-side devices are visible.
- **Queue lag in teleop.** `sub.recv()` returns the oldest unread frame; drain to the latest frame each loop or use callbacks.
- **Glove tracking.** EMF degrades within **3 cm** of metal and near magnets (robot flanges, tools, laptops); the SDK warns when confidence stays below 0.85. Humidity < 55 % RH. The built-in default hand model is currently more reliable than per-user calibration — start with the default SDK user.
- **Thermal.** Hand 2 derates total current above **85 °C** MCU temperature and stops above 100 °C; the housing gets hot. Room temperature 15–30 °C is the specified range — fine in the arena, not outdoors in November.
- **Environment.** Dry, clean, indoor only (gen 1 is IP40; Hand 2 has no published rating). Keep the skin and soft pads fitted: the finger flex cables underneath are fragile.
- **Platform holes.** Windows: no gen-1 hand, no retargeting, reduced examples. macOS: Apple silicon only, allow local-network access for the terminal. ROS 2: Lyrical only.
- **Connector change announced.** The XT30 + RJ45 layout and voltage range "will change in later versions" — do not design a permanent mount around them.
- **Fault help:** `wuji doctor`, `wuji logs export`, SDK log at `~/.wuji/logs/`, and `describe_error(code)`.

## Community resources

| Resource | Link | Use |
|---|---|---|
| Developer docs (EN / ZH, with `llms.txt` index for AI assistants) | [docs.wuji.tech](https://docs.wuji.tech) · [index](https://docs.wuji.tech/_llms/en.txt) | Everything above, per product |
| Release notes (fortnightly) | [release notes](https://docs.wuji.tech/docs/en/release-notes.md) | Check which firmware / SDK pair you have |
| GitHub organisation | [wuji-technology](https://github.com/wuji-technology) | SDK examples, ROS 2, models, RL, VLA |
| SDK examples | [examples/python](https://github.com/wuji-technology/wuji-sdk/tree/main/examples/python) · [examples/c](https://github.com/wuji-technology/wuji-sdk/tree/main/examples/c) | Numbered scripts per device |
| Video guides | [docs videos page](https://docs.wuji.tech/docs/en/videos.md) · [YouTube @WUJI_TECH](https://www.youtube.com/@WUJI_TECH/videos) | Glove calibration tutorial, demos |
| Support | support@wuji.tech (attach a `wuji logs export` bundle) | Hardware faults |
| Sales / partnership | sales@wuji.tech | After the hackathon |
| Forum / Discord | not found | Ask the WUJI engineers on site |

Related in this pack: [solutions and projects](WUJI-Solutions-and-Projects.md) · [papers and research](WUJI-Papers-and-Research.md).

## Sources

- [Wuji Docs — English index](https://docs.wuji.tech/_llms/en.txt)
- [Wuji SDK overview](https://docs.wuji.tech/docs/en/wuji-sdk/latest/introduction.md) · [installation and environment](https://docs.wuji.tech/docs/en/wuji-sdk/latest/quick-start.md) · [device discovery and connection](https://docs.wuji.tech/docs/en/wuji-sdk/latest/device-connection.md) · [data recording](https://docs.wuji.tech/docs/en/wuji-sdk/latest/data-recording.md) · [time synchronization](https://docs.wuji.tech/docs/en/wuji-sdk/latest/time-sync.md) · [hand retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md) · [Docker deployment](https://docs.wuji.tech/docs/en/wuji-sdk/latest/docker-deployment.md) · [best practices](https://docs.wuji.tech/docs/en/wuji-sdk/latest/advanced.md)
- [Wuji Hand 2 quick start](https://docs.wuji.tech/docs/en/wuji-hand/latest/quick-start.md) · [control guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/control-guide.md) · [user notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md) · [electrical and network integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/electrical-network-integration.md) · [ROS 2 integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/ros2-integration.md) · [model assets and loading](https://docs.wuji.tech/docs/en/wuji-hand/latest/model-integration.md) · [data streams overview](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference.md) · [effort and MIT parameters](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/effort-and-mit.md) · [position control practice](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-practice/position-mode.md) · [maintenance](https://docs.wuji.tech/docs/en/wuji-hand/latest/maintenance.md) · [troubleshooting](https://docs.wuji.tech/docs/en/wuji-hand/latest/troubleshooting.md) · [version identification and compatibility](https://docs.wuji.tech/docs/en/wuji-hand/latest/version-compatibility.md)
- [Wuji Hand (gen 1) user notice](https://docs.wuji.tech/docs/en/wuji-hand/v1/user-notice.md) · [Wuji Hand SDK (wujihandpy) getting started](https://docs.wuji.tech/docs/en/wujihandpy/latest/introduction.md)
- [Wuji Glove quick start](https://docs.wuji.tech/docs/en/wuji-glove/latest/getting-started.md) · [data streams overview](https://docs.wuji.tech/docs/en/wuji-glove/latest/sdk-data-reference/index.md) · [ROS 2 integration](https://docs.wuji.tech/docs/en/wuji-glove/latest/ros2-integration.md)
- [Wuji CLI overview](https://docs.wuji.tech/docs/en/wuji-cli/latest/introduction.md) · [getting started](https://docs.wuji.tech/docs/en/wuji-cli/latest/getting-started.md) · [live visualization](https://docs.wuji.tech/docs/en/wuji-cli/latest/visualization.md)
- [Wuji Docs release notes](https://docs.wuji.tech/docs/en/release-notes.md)
- GitHub: [wuji-sdk](https://github.com/wuji-technology/wuji-sdk) ([Python examples README](https://github.com/wuji-technology/wuji-sdk/blob/main/examples/python/README.md)) · [wuji-ros2](https://github.com/wuji-technology/wuji-ros2) · [wuji-description](https://github.com/wuji-technology/wuji-description) · [wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab) · [wuji-isaaclab](https://github.com/wuji-technology/wuji-isaaclab) · [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) · [toporetarget](https://github.com/wuji-technology/toporetarget) · [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop)
- In this pack: [WUJI profile](WUJI.md) · [product portfolio](WUJI-Products.md) · [solutions and projects](WUJI-Solutions-and-Projects.md) (revision batches, default kp / kd, repo status carried over from their sources)
