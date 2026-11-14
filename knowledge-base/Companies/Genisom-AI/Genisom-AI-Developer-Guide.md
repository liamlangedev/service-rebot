---
type: dev-guide
company: "Genisom AI"
slug: Genisom-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Genisom AI — Developer Guide (hackathon edition)

⬆ [Genisom AI profile](Genisom-AI.md) · [Product portfolio](Genisom-AI-Products.md) · [Roadmap and strategy](Genisom-AI-Roadmap-and-Strategy.md)

> **How this guide was built:** every repository under [github.com/zsibot](https://github.com/zsibot/) was opened on 2026-11-14 and its README, docs folder, changelog and example code were read. Numbers below (ports, rates, limits) come from those files. Nothing here was tested on a physical robot — check each step against the unit you are handed. Which robots Genisom brings to Leukerbad is **not confirmed**; the guide covers both SDK families.

![MATRiX simulator](assets/genisom-ai-matrix.jpg)

## TL;DR — how you program it

- **Two robot families, two SDKs, both C++ over UDP.** L1 / L1-W use `genisom_L1_sdk` (JSON over UDP, ports **8081 / 8080**). M1 and L2 use `genisom_robot_sdk` ("GEN2", UDP port **8082**). In both cases the robot's Wi-Fi access point answers at **192.168.234.1**.
- **You command body velocity, not joints.** High-level calls: stand, lie down, posture modes, velocity (`Move` / `MoveVelocity` / `SetRemote`), plus IMU, odometry, joint and battery read-back. Joint-level PD / torque control exists **only for the L1** (shared memory on the robot, **1 kHz**), not for M1 or L2.
- **Control is arbitrated.** Being connected does not mean you may drive. The phone app beats the SDK on M1 / L2; on the L1 you must request SDK control rights first. Close the app before your first motion test.
- **No official ROS 2 driver and no Python package for the current SDKs.** ROS 2 enters through RoamerX Lite (Humble + Nav2). Python enters through the legacy L1 SDK (unmaintained), the documented JSON-over-UDP protocol, or a thin wrapper you write yourself.
- **Start in simulation today.** MATRiX v1.1.2 (MuJoCo + Unreal Engine 5, Linux x86_64) runs L1, L1-W, M1-class and arm-equipped models with built-in locomotion and publishes camera / LiDAR / IMU over Zenoh. Download it early — the runtime is several GB.

## Naming map (read this before opening any repo)

The repos use internal code names, not product names.

| Product | Chinese name | Code names seen in repos | Where |
|---|---|---|---|
| L1 (point-foot) | 钢镚 L1 | `zsl-1`, `xgb` / `xg`, `MODEL_XG`, "ZSL1" | URDF repo, MATRiX, L1 SDK, robot_lab |
| L1-W (wheel-leg) | 钢镚 L1-W | `zsl-1w`, `xgw`, `MODEL_XGW`; high-speed variant `MODEL_XGWHSPD` | URDF repo, MATRiX, L1 SDK |
| L2 | 钢镚 L2 | `DeviceType::L2`, `L2_ULTRA` (wheeled), `L2F`, `L2F_ULTRA` (point-foot); MATRiX `xg2` / `xgw2` and controller names `zsl-2` / `zsl-2w` ⚠️ unverified mapping (inferred from names) | GEN2 SDK, MATRiX |
| M1 | 铜锤 M1 | `DeviceType::M1` (wheeled), `M1F` (point-foot), suffixes `_PRO` (laser), `_ULTRA` (panoramic), `_AIR`; MATRiX `zgws` / `zgwt`, controller name `zsm-1w` ⚠️ unverified mapping (inferred from names) | GEN2 SDK, MATRiX |
| M1 + arm | — | MATRiX `zgwsarm` ⚠️ unverified mapping | MATRiX |
| Organisation | 智身科技 | `zsibot`, `jszr` (in paths and bridge names) | everywhere |

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| `genisom_L1_sdk` ✅ | C++ (README says C++20, changelog says C++17 compiler); prebuilt static lib `libzsibot.a` for x86_64 and aarch64 | L1, L1-W, high-speed L1-W: commands, velocity, stunts, modes, Wi-Fi hotspot; **35 state getters** (IMU, odometry, 4 legs × 4 joints, motor temperature, battery, faults) | [repo](https://github.com/zsibot/genisom_L1_sdk) | MIT · **v1.0.0 (2026-06-22)** · JSON over UDP · robot `192.168.234.1`, send port `8081`, receive port `8080` · heartbeat every 50 ms, link declared dead after 5 s |
| `genisom_L1_sdk` low-level header | C / C++ header (`lowlevel.h`) | L1 joint commands (position, velocity, kp, kd, feed-forward torque) and joint / IMU state through POSIX shared memory `/spline_shm` and `/imu_shm` | [doc](https://github.com/zsibot/genisom_L1_sdk/blob/main/docs/en/api_lowlevel.md) | Shared memory is local to the robot's computer, so the program must **run on the robot**. Update period **1 ms**. Not mentioned in the README — ask the booth whether it is enabled on the loan unit |
| `genisom_robot_sdk` ("GEN2") ✅ | C++17 client library, prebuilt `librobot_sdk.so` (x86_64, aarch64); needs Ubuntu 22.04, CMake 3.8+, Boost 1.74 | **M1 and L2** (12 device types): postures, velocity, position-control mode, lights, obstacle stop, camera bitrate, recharge / undock tasks, dock pairing, LEDs, peripheral power rails | [repo](https://github.com/zsibot/genisom_robot_sdk) | No licence file · changelog up to **v0.2.3**; README compatibility table recommends **v0.2.2** for M1 system v0.3.1 and L2 system v0.0.9 · UDP `8082` default, WebSocket `8081` optional · 12 example programs |
| `genisom_l1_sdk_old` (legacy) | C++ and **Python** (compiled extension, built for a specific CPython version) | L1 / L1-W high-level; **L1 low-level motor control** (`sendMotorCmd`); L1-W has no low-level | [repo](https://github.com/zsibot/genisom_l1_sdk_old) · [online docs](https://zsibot.github.io/genisom_l1_sdk_old/) | BSD-3 · **no longer maintained** · needs an SSH edit of the robot's SDK config (target IP, port `43988`) and a restart · only use if the robot firmware still matches |
| `genisom_roamerx_open` (RoamerX Lite) ✅ | C++, ROS 2 Humble | Mapping (3D PCD + 2D grid), localisation (NDT / GICP), Nav2-based planning (NavFn + MPPI), behaviour trees, waypoint following | [repo](https://github.com/zsibot/genisom_roamerx_open) | BSD-3 · talks to the motion controller over UDP or LCM · **"Hardware Deployment" section of the README is still "TODO"** |
| `matrix` (MATRiX) ✅ | Binary runtime + Python tools | Simulator: robots, sensors, maps, built-in locomotion | [repo](https://github.com/zsibot/matrix) | BSD-3 · release **v1.1.2** (built 2026-09-23), marketed as MATRiX 2.0 · Linux x86_64 |
| `MATRiX_Python_SDK` | Python | Load a MuJoCo scene, run your own controller callback, mirror state to Unreal over UDP | [repo](https://github.com/zsibot/MATRiX_Python_SDK) | No licence stated · state out on UDP `9999`, optional control in on UDP `10001` |
| `MATRiX_Robot_MC` | Binary runtime (Linux x86_64) | Stand-alone locomotion controller for the simulator (same hardware interface as the real robot) | [repo](https://github.com/GENISOM-AI/MATRiX_Robot_MC) | **v0.6.6** · ships **encrypted ONNX policies** — you can run them, not inspect or retrain them |
| `genisom_model` | URDF + meshes | `zsl-1` (L1) and `zsl-1w` (L1-W) only | [repo](https://github.com/zsibot/genisom_model) | BSD-3 · no public URDF for M1 or L2 |
| `genisom_vln` | Python | Language- or image-goal navigation agent (zero-shot) against MATRiX | [repo](https://github.com/zsibot/genisom_vln) | BSD-3 · see AI stack |
| `gawm` | Python | JEPA-style latent world model (research code) | [repo](https://github.com/zsibot/gawm) | MIT · not robot-ready |

## Control levels

| Level | L1 / L1-W (`genisom_L1_sdk`) | M1 / L2 (`genisom_robot_sdk`) |
|---|---|---|
| Body velocity | `SetRemote(joystick[4], buttons[14])` — joystick = forward/back, rotation, left/right, head angle, normalised to ±1. Example code loops every **20 ms** | `Move(left_right, forward_back, yaw)` normalised ±1, or `MoveVelocity(x, y, yaw)` in **m/s and rad/s**. A command stays valid for **1 s**; resend at **10–20 Hz** |
| Speed envelope | Three speed levels (slow / normal / fast); limits not published | Low: **±1.0 m/s** forward, ±0.5 m/s lateral, ±1.5 rad/s. Medium: ±2.0 m/s. High: ±3.0 m/s. Lateral and yaw authority shrink as forward speed rises. `MoveVelocity` is clipped to the active level |
| Postures / modes | Stand, sit, move mode, balance stand, lock, emergency stop, lab mode, entertainment mode | Stand, walk, balance stand, lie down, stair, crawl, crawl-walk, climb, fine gait, slim (narrow passage), same-knee, sand, locked, position-control (`PosControl` + `PosMove` for body pose x/y/z/roll/pitch/yaw) |
| Stunts | Jump, forward jump, back flip, greet, two-leg stand, crawl, climb platform, handstand, unload squat. Most need **lab mode** first. Wheel models cannot jump / flip; point-foot cannot crawl / climb / handstand | Not exposed |
| Model limits | Checked by model type (`MODEL_XG`, `MODEL_XGW`, `MODEL_XGWHSPD`) | Checked by `DeviceType`; unsupported calls return `UnsupportedDeviceOperation`. L2 has **no** slim, same-knee, sand, head-tail reverse or obstacle-stop call; point-foot L2 has no climb or fine gait |
| Joint level | **Yes, L1 only** — per joint: target position, velocity, kp, kd, feed-forward torque; shared memory, 1 ms cycle, on-robot. Legacy SDK FAQ states **500 Hz** low-level and **50 Hz** high-level, and that high- and low-level cannot run at the same time | **No public joint-command API.** Joint position / velocity / torque are read-only |
| State read-back | IMU (quaternion, RPY, accel, gyro), odometry (position, world and body velocity), joints, motor temperature ×16, battery, faults | `RobotState` at **1 Hz** by default; opt-in streams: IMU up to **100 Hz**, motion data (odometry) **50 Hz**, speed **1–50 Hz**, joint state, illuminance 1 Hz, faults on event |
| Tasks | RoamerX control hand-over (`CMD_ROAMERX_CONTROL_RIGHT`) | Autonomous recharge / undock, dock scan and pairing |
| Payload I/O | — | `SetPeriphPower` switches **12 V / 24 V / 48 V** peripheral rails (M1) · LED groups and effects · front / rear fill light · camera bitrate for `camera_front` / `camera_back` |

**What EDU / developer editions unlock (as far as public sources say):**

- **L1 EDU** adds hardware, not a different API: NVIDIA **Jetson Orin NX (up to 100 TOPS)**, built-in 3D LiDAR, depth camera, GNSS and 5G (company product page). The education line also lists an "L1 EDU Navigation Kit" and an "L1 EDU DESK" bench for SDK motion control and ROS 2 mapping / navigation classes.
- **L1 Maker** 🧪 adds component-level assembly and access to the production calibration software.
- ⚠️ unverified: whether low-level joint control is enabled on every L1 firmware or only on EDU units, and whether RoamerX (full version) is pre-installed on the loan robots. Ask the booth.

## ROS 2 and middleware

- **No ROS 2 driver package for either SDK.** The legacy SDK FAQ says plainly that there is no ROS interface. Plan a small bridge node: subscribe to `/cmd_vel`, call `MoveVelocity` (M1 / L2) or `SetRemote` (L1) at 20 Hz, publish IMU / odometry / joint states from the SDK getters.
- **RoamerX Lite** is the official ROS 2 entry point: **Ubuntu 22.04 + ROS 2 Humble**, Nav2 forked into `navigo_*` packages, custom messages in `robots_dog_msgs`, launch file `navigation_bringup.launch.py` with `platform:=GAZEBO | NX_XG3588 | XG3588`, `mc_controller_type:=RL_TRACK_VELOCITY | RL_TRACK_PATH`, `communication_type:=UDP | LCM`. Standard Nav2 actions work (`/navigate_to_pose`, `/navigate_through_poses`).
- **Mapping and localisation services:** `ros2 launch robot_slam slam.launch.py`, then `/slam_state_service` (start = 3, save = 5); localisation loads a PCD map through `/load_map_service`.
- **Middleware seen in the stack:** UDP + JSON (SDKs), LCM (navigation ↔ motion control), Zenoh with ROS 2-compatible CDR messages (simulator), `rmw_zenoh_cpp` with `ROS_DOMAIN_ID=89` in the simulator examples, ZMQ (VLN bridge), POSIX shared memory (low-level control).
- **On the real M1** the navigation computer (`192.168.168.100`) and the motion-control computer (`192.168.168.168`) are separate hosts behind an internal switch. SDK commands go to the motion-control host only.

![RoamerX navigation](assets/genisom-ai-roamerx.jpg)

## Simulation and digital twins

| Item | Detail |
|---|---|
| Simulator | **MATRiX v1.1.2** — MuJoCo dynamics on a dedicated worker (**500 Hz** target) + Unreal Engine 5 rendering; started with `./UeSim.sh` |
| Platform | Linux x86_64 with a working GPU driver (Vulkan); **16 GB RAM** recommended. The product page also claims Windows; the v1.1.2 repo documents Linux only |
| Install | Runtime is a download, not the Git repo. Use the [GitHub release](https://github.com/zsibot/matrix/releases/tag/v1.1.2): fetch **all** `.part-*` files (each under 2 GB) and `SHA256SUMS`, verify, concatenate, extract |
| Robots with built-in locomotion | `xgb`, `xg2`, `xgw`, `xgw2`, `zgws`, `zgwt`, `zgwsarm`. Unitree `go2` / `go2w` assets load but have no built-in controller |
| Driving the sim robot | Gamepad (`/dev/input/js0`; LB+Y stand, LB+B balance stand, LB+RB passive) or UDP JSON on port 7447 — `python3 Tools/matrix_mc_udp_test.py walk --stand-first --forward 0.25 --duration 3` |
| Sensors | RGB, depth, semantic, infrared, fisheye, panorama, gimbal camera, Livox Mid-360, RoboSense Airy, generic LiDAR, IMU, GPS, odometry — chosen through JSON "sensor schemes" (`config_default.json`, `mid360_slam.json`, …) |
| Data out | Zenoh on `tcp/…:7447`, keys under `rt/**` (for example `rt/front_lidar`, `rt/imu`, `rt/odom/mujoco_odom`); inspect with `Tools/zenoh_topic_monitor.py` and `Tools/zenoh_sensor_receiver.py` (Python 3.10+) |
| ROS 2 | Optional — needs a Zenoh-to-ROS 2 bridge (`ue_zenoh_bridge` in the docs); bridge source is not in the public repos ⚠️ unverified availability |
| Maps | Downloaded from inside the launcher (UPDATE LIST → DOWNLOAD): Town10, Venice, Yard, Crowd, House, Office, IROS 2025 flat / sloped courses, 3DGS, Moon |
| Digital twins | 3D Gaussian-splatting scene import is advertised (a `3DGSWorld` map is in the catalogue); the import tool chain is not documented in the repo ⚠️ unverified |
| Own controller in sim | `MATRiX_Python_SDK`: write `controller(state) -> ctrl` in Python against the MuJoCo model, state mirrored to Unreal |
| RL training elsewhere | [fan-ziqi/robot_lab](https://github.com/fan-ziqi/robot_lab) (IsaacLab extension, third party) has rough-terrain velocity tasks for **Zsibot ZSL1** and **ZSL1W**; URDFs in `genisom_model` import into RViz / Gazebo / Isaac |
| Gazebo | RoamerX Lite has a Gazebo launch path (`platform:=GAZEBO`) with single-goal and patrol demos |

## AI stack

| Layer | What exists publicly | Status |
|---|---|---|
| Locomotion policies | Learned controllers ship inside the robot firmware and as **encrypted ONNX** in `MATRiX_Robot_MC`. No open weights, no training code | ✅ usable, closed |
| Navigation | RoamerX Lite (classical: NDT / GICP localisation + Nav2 + MPPI). Full RoamerX on products adds road-network and multi-floor modes | ✅ Lite open |
| End-to-end navigation (GSD / ZSD) | Announced data-driven navigation model | 🧪 no code, no weights |
| Vision-language navigation | `genisom_vln`: zero-shot agent built on UniGoal — builds an occupancy map and scene graph from RGB-D + pose, scores frontiers with an LLM / VLM, plans with Fast Marching. Backends: local **SmolVLM2-256M**, **Ollama** (for example `gemma3:4b`), or a cloud API. Fine-tuned agents folder is empty ("todo") | ✅ sim only; README recommends an RTX 4090-class GPU for local models |
| World model | `gawm` + checkpoints [kikihuang/GA-WM](https://huggingface.co/kikihuang/GA-WM) (tabletop / toy benchmarks) | ✅ research only |
| VLA / manipulation model | A vision-language-action demo on M1 + TA01 arm was shown at WRC 2026; nothing released | 🧪 |
| Agent layer (SomaMind) and PITA models | Announced; no SDK or repo | 🧪 |
| Datasets | **None released** | — |
| Teleoperation | Phone app, gamepad, SDK "remote" role (L1). A VR goal-setting interface appeared in the multi-robot transport demo; not public | partly ✅ |
| Data-collection pipeline | None public. MATRiX has a Zenoh recorder / replayer (`Tools/zenoh_bbox_lidar_recorder.py`) for simulated sensors | — |
| **LeRobot support** | **None found** (no LeRobot dataset, policy or robot config in any Genisom repo) | — |

Practical reading: bring your own perception and reasoning (a VLM over the camera stream, an LLM planner) and let the robot's built-in locomotion and RoamerX do the walking.

## Compute, sensors and connectivity

| Robot | On-board compute | Sensors (per product pages) | Open interfaces | Network |
|---|---|---|---|---|
| L1 | Motion-control computer; RoamerX platform names (`XG3588`) point to an RK3588-class board ⚠️ unverified | HD camera with monocular tracking | **7** interfaces: Ethernet, USB 3.0 / 2.0, 24 V / 12 V power | Wi-Fi AP `192.168.234.1` (DHCP); wired `192.168.168.168` (**no DHCP** — set a static `192.168.168.x` address) |
| L1 EDU | + **Jetson Orin NX, up to 100 TOPS** | + 3D LiDAR (Livox Mid-360 per trade press), depth camera, GNSS | as L1 | + 5G module |
| L1-W | as L1 | as L1 | as L1 | as L1 |
| L2 | **Up to 86 TOPS** | Front wide-angle stereo, 4 fisheye cameras, LiDAR, GNSS; UWB for following (GLUE) | "Full platform extension" — count not published | L2 network layout "to be documented" in the SDK; use site-specific addresses |
| M1 / M1 Pro / M1 Ultra | Two hosts: motion control + navigation | Pro: LiDAR, UWB, microphone, speaker. Ultra: 4 fisheye + front stereo | **15** interfaces; switchable 12 / 24 / 48 V rails; 2 external Ethernet ports | Wi-Fi AP `192.168.234.1`; wired motion host `192.168.168.168`, navigation host `192.168.168.100` |

- **Camera access:** the L1 product page lists a "video stream interface" and the GEN2 SDK only adjusts camera bitrate. The stream URL / protocol is **not documented** in the public repos ⚠️ unverified — ask the booth for the stream address or mount your own USB camera on the open ports.
- **LiDAR access:** no SDK call. On EDU / Pro / Ultra units the point cloud is consumed by the navigation computer; expect ROS 2 topics there ⚠️ unverified topic names.
- **Your own computer on the robot:** power it from the 12 / 24 V port, connect by Ethernet to the internal network, run the SDK locally. The vendor FAQ recommends exactly this to avoid Wi-Fi latency.

## First 60 minutes checklist

**Minute 0–10 — identify and prepare (no robot needed)**

1. Ask the booth: model and variant (L1 / L1 EDU / L1-W / L2 / M1), firmware ("system") version, whether RoamerX is installed, whether an app is paired to the robot, where the emergency stop is.
2. Laptop: Ubuntu 22.04, `sudo apt install build-essential cmake libboost-all-dev`. Run `uname -m` (must be `x86_64` or `aarch64`).
3. Clone the matching SDK: `git clone https://github.com/zsibot/genisom_L1_sdk` (L1 family) or `git clone https://github.com/zsibot/genisom_robot_sdk` (M1 / L2).

**Minute 10–25 — connect and verify (read-only)**

4. Join the robot's Wi-Fi (SSID and password are on the label on the robot's right side), or plug Ethernet and set a static `192.168.168.x` address.
5. Check the route: `ip route get 192.168.234.1` (a failed ping alone proves nothing).
6. **M1 / L2:** `cd example && mkdir -p build && cd build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j"$(nproc)"`, then `./quick_start 192.168.234.1 8082`. Success = SDK / protocol / system versions printed, `[OK] Connected`, `[OK] First robot state received`, clean disconnect. Compare the printed system version with the README compatibility table.
7. **L1 family:** `mkdir build && cd build && cmake .. && make -j"$(nproc)" && make sdk_control`. Start `sdk_control`; confirm `IsConnected()` is true and battery, RPY and joint angles update.

**Minute 25–45 — hello-world motion (clear 3 m around the robot, one person on the stop control)**

8. Close the phone app on every paired phone. On M1 / L2 run `./take_control 192.168.234.1 8082` or `./control …` and press `t`; wait for the ownership ACK with error code 0.
9. **M1 / L2:** in `control`, press `h` for the key map; stand up, then drive. In your own code: `StandUp()` → wait until `RobotState.motion_status` reports walk → `SetSpeed(1)` → loop `MoveVelocity(0.2, 0, 0)` at 20 Hz for 2 s → `LieDown()`.
10. **L1 family:** send `CMD_SDK_CONTROL_RIGHT`, wait until `GetFunctionMode()` reports SDK mode, then `CMD_STAND_UP`, then loop `SetRemote({0.3, 0, 0, 0}, {0})` every 20 ms for 2 s, zero the joystick, `CMD_SIT_DOWN`. Do **not** enter lab mode or trigger stunts indoors.

**Minute 45–60 — read sensors and log**

11. **M1 / L2:** run `./data 192.168.234.1 8082`; in code call `SetImuConfig(50)`, `SetMcConfig(true)`, `SetJointStateConfig(true)` and print inside `OnImuData` / `OnMcData` (copy data out of the callback; never block in it).
12. **L1 family:** poll `GetQuaternion()`, `GetPosition()`, `GetBodyVelocity()`, `GetBatteryInfo()` at 50 Hz and write a CSV.
13. Wrap what you have in a `/cmd_vel` → SDK bridge so the rest of the team can work in ROS 2 or Python.
14. In parallel, one teammate starts the MATRiX download and runs `./UeSim.sh` with the `xgb` robot and the `config_default.json` sensor scheme.

Minimal GEN2 motion sketch (own wording of the documented calls; add the ownership callbacks before using it):

```cpp
robot_sdk::SDKClient client([](const std::error_code&){});
client.Connect("192.168.234.1", "8082", true);
client.StandUp(1000);                 // sync send; then wait for motion_status == WALK
client.SetSpeed(1, 1000);             // low: max 1.0 m/s
for (int i = 0; i < 40; ++i) {        // 2 s at 20 Hz
  client.MoveVelocity(0.2f, 0.0f, 0.0f);
  std::this_thread::sleep_for(std::chrono::milliseconds(50));
}
client.LieDown(1000);
```

## Known gotchas and safety

**Control and safety**

- **App beats SDK (M1 / L2).** If the app connects, your program gets `OnControlLost()` and must stop sending. An app that "releases" control but stays connected still blocks `TakeControl()`. The software emergency stop works for any connected client, owner or not.
- **Legacy L1 SDK: SDK beats gamepad.** While an SDK program runs, the hand controller cannot take over. Keep your own stop key and a person near the robot.
- **Watchdogs differ:** GEN2 velocity command expires after **1 s**; new L1 SDK link drops after **5 s** without heartbeat; legacy L1 goes to damping and lies down after **3 s** without data. A robot that stops mid-stride on a slope can slide.
- **Battery:** the legacy FAQ warns there is **no low-battery protection under SDK control** — the robot may power off while standing. Read battery level in your loop and lie down below a threshold.
- **ACK is not completion.** A returned call or ACK means "received". Posture changes are finished only when `RobotState.motion_status` says so (standing up ends in state *walk*, not *stand up*). Recharge / undock results arrive through task-state callbacks.
- **Callbacks run on the I/O thread.** A synchronous SDK call inside a callback deadlocks.
- **Stunts:** back flip, jump and two-leg stand are one command away on the L1. Not in a crowded hall.
- **Cold:** L1 is rated **0–40 °C**. Leukerbad in mid-November is often below freezing outdoors; use L2 / M1 (−20 °C rated) for outdoor demos.
- **People:** these are industrial outdoor machines with no published contact-safety data. Do not design demos where the robot touches or supports a person (relevant for T04).

**Network**

- Every robot uses the same default AP address. With several units on site, check the SSID before sending motion commands.
- A sports hall with 20 exhibitors is hostile to 2.4 / 5 GHz. Prefer Ethernet or an on-board computer for anything closed-loop.
- VPNs, containers and firewalls on the laptop commonly break the UDP path. Target the **motion-control** host, not the navigation host.
- Wired L1 control on the legacy SDK needs extra on-robot config (`SDK_CLIENT_IP`), which the docs say can stop the remote controller working if the interface has no address at boot. Firmware updates reset these files.

**Versions**

- GEN2 SDK and robot system versions must match the compatibility table. Known bad pair: M1 system v0.3.0 with SDK v0.2.1 (`UpdateCameraBitrate` must not be used).
- GEN2 history removed whole concepts between releases (the "Mode" concept, `DSB()`), so older sample code from the web may not compile.
- The new L1 SDK README does not mention Python; the Python extension lives only in the unmaintained legacy repo and is tied to one CPython version.
- **Joint order differs between SDKs:** new L1 SDK arrays are left-front, right-front, left-rear, right-rear; the legacy SDK uses front-right, front-left, rear-right, rear-left. Euler angles are ZYX. IMU data is raw.

**Simulation and navigation stack**

- RoamerX Lite and `genisom_vln` READMEs still launch MATRiX with `run_sim.sh` / `open_sim_launcher`. Those files **do not exist in MATRiX v1.1.2**; MATRiX's own integration doc says so. Budget time for the Zenoh-to-ROS 2 bridge.
- RoamerX Lite installs a prebuilt `robot-forward` `.deb` for amd64 and gives no real-robot deployment steps. Treat it as a simulation / reference stack unless the booth provides the on-robot version.
- MATRiX starts with **no sensors active** and an **empty map list**. Apply a sensor scheme before spawning the robot and download a map DLC first. Map DLC mirrors are partly on Baidu Netdisk, which is slow from Europe.
- MATRiX point clouds are labelled `frame_id=map` although the points are sensor-local.
- GPU LiDAR needs NVIDIA CUDA / OptiX; otherwise switch each LiDAR to `"backend": "cpu"`. There is no supported Docker image.
- Never run the built-in and the external motion controller together.
- No URDF / MJCF for M1 or L2 outside the MATRiX runtime package.

## Community resources

- **GitHub:** [github.com/zsibot](https://github.com/zsibot/) — issues on each repo are the public support channel (MATRiX has issue templates, a contributing guide and a security policy). MATRiX is the most active repo (about **450 stars**, last push 2026-09-23); GEN2 SDK last push 2026-10-27.
- **Official pages:** [Open Source](https://www.genisomai.com/en/opensource) (links to repos and firmware upgrade packages for L1, L1-W and M1) · [Download Center](https://www.genisomai.com/en/download.html) (manual categories exist; no files were listed when checked).
- **Legacy docs site:** [zsibot.github.io/genisom_l1_sdk_old](https://zsibot.github.io/genisom_l1_sdk_old/) — still the best description of the L1 network setup, state machine and FAQ.
- **Programmes:** Genisom EAI Academy (courses, simulation, competitions; no public URL found) and the **Gravity** programme (robots and resources for researchers and developers, application by form) — see [Education and research](https://www.genisomai.com/en/education-research).
- **Chat:** WeChat assistant QR code in the MATRiX README (Chinese-language community). No Discord, forum or Slack found.
- **Third party:** [fan-ziqi/robot_lab](https://github.com/fan-ziqi/robot_lab) for IsaacLab training on the L1 / L1-W.
- **Competition references:** IROS 2025 and 2026 legged-robot challenge teams (University of Manchester on L1, NTU Singapore on M1 with arm) built full autonomy stacks on these SDKs; MATRiX ships the IROS 2025 course maps.
- **At the event:** the booth engineers are the fastest route to firmware versions, stream addresses and the on-robot RoamerX build — none of which are public.

## Sources

- [GitHub organisation zsibot](https://github.com/zsibot/)
- [genisom_L1_sdk — README (English)](https://github.com/zsibot/genisom_L1_sdk/blob/main/README_en.md)
- [genisom_L1_sdk — API reference](https://github.com/zsibot/genisom_L1_sdk/blob/main/docs/en/api.md)
- [genisom_L1_sdk — low-level API](https://github.com/zsibot/genisom_L1_sdk/blob/main/docs/en/api_lowlevel.md)
- [genisom_L1_sdk — communication protocol](https://github.com/zsibot/genisom_L1_sdk/blob/main/docs/protocol/protocol.md)
- [genisom_L1_sdk — changelog](https://github.com/zsibot/genisom_L1_sdk/blob/main/CHANGELOG.md)
- [genisom_robot_sdk — README](https://github.com/zsibot/genisom_robot_sdk)
- [genisom_robot_sdk — changelog](https://github.com/zsibot/genisom_robot_sdk/blob/main/CHANGELOG.md)
- [genisom_robot_sdk — API capability matrix](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_api_capability_en.md)
- [genisom_robot_sdk — SDKClient API](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_client_api_en.md)
- [genisom_robot_sdk — control ownership](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_control_ownership_en.md)
- [genisom_robot_sdk — motion states and command delivery](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_state_en.md)
- [genisom_robot_sdk — network architecture](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_network_en.md)
- [genisom_robot_sdk — data types (speed levels, power rails)](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_type_en.md)
- [genisom_robot_sdk — callback reference](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_callback_en.md)
- [genisom_robot_sdk — troubleshooting](https://github.com/zsibot/genisom_robot_sdk/blob/main/docs/en/sdk_troubleshooting_en.md)
- [genisom_l1_sdk_old — README](https://github.com/zsibot/genisom_l1_sdk_old)
- [genisom_l1_sdk_old — deployment guide](https://github.com/zsibot/genisom_l1_sdk_old/blob/main/docs/en/deploy.md)
- [genisom_l1_sdk_old — FAQ](https://github.com/zsibot/genisom_l1_sdk_old/blob/main/docs/en/faq.md)
- [genisom_l1_sdk_old — architecture](https://github.com/zsibot/genisom_l1_sdk_old/blob/main/docs/en/architecture.md)
- [genisom_roamerx_open — README](https://github.com/zsibot/genisom_roamerx_open)
- [matrix — README](https://github.com/zsibot/matrix)
- [matrix — Getting Started](https://github.com/zsibot/matrix/blob/main/docs/Getting_Started.md)
- [matrix — Motion Control](https://github.com/zsibot/matrix/blob/main/docs/Motion_Control.md)
- [matrix — Controller Guide](https://github.com/zsibot/matrix/blob/main/docs/Controller_Guide.md)
- [matrix — Robots and Maps](https://github.com/zsibot/matrix/blob/main/docs/Robots_and_Maps.md)
- [matrix — Sensor Schemes](https://github.com/zsibot/matrix/blob/main/docs/Sensor_Schemes.md)
- [matrix — RoamerX Lite integration](https://github.com/zsibot/matrix/blob/main/docs/RoamerX_Lite_Integration.md)
- [matrix — Release Notes v1.1.2](https://github.com/zsibot/matrix/blob/main/docs/Release_Notes.md)
- [matrix — Docker support status](https://github.com/zsibot/matrix/blob/main/docs/Docker_Tutorial.md)
- [matrix — Tools index](https://github.com/zsibot/matrix/blob/main/Tools/README.md)
- [GENISOM-AI/MATRiX_Robot_MC](https://github.com/GENISOM-AI/MATRiX_Robot_MC)
- [MATRiX_Python_SDK — README](https://github.com/zsibot/MATRiX_Python_SDK)
- [genisom_model — README](https://github.com/zsibot/genisom_model)
- [genisom_vln — README](https://github.com/zsibot/genisom_vln)
- [genisom_vln — development guide](https://github.com/zsibot/genisom_vln/blob/main/docs/guide.md)
- [zsibot/gawm](https://github.com/zsibot/gawm)
- [fan-ziqi/robot_lab](https://github.com/fan-ziqi/robot_lab)
- [Genisom AI — Official Open Source page](https://www.genisomai.com/en/opensource)
- [Genisom AI — Download Center](https://www.genisomai.com/en/download.html)
- [Genisom L1 product page](https://www.genisomai.com/en/product-robot/L1)
- [Genisom L2 product page](https://www.genisomai.com/en/product-robot/L2)
- [Genisom M1 product page](https://www.genisomai.com/en/product-robot/M1)
- [Genisom L1 Maker product page](https://www.genisomai.com/en/product-robot/L1maker)
- [MATRiX product page](https://www.genisomai.com/en/product-robot/MATRiX)
- [Education and research ecosystem](https://www.genisomai.com/en/education-research)
- [Education and research solutions](https://www.genisomai.com/en/solutions)
