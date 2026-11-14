---
type: dev-guide
company: "Magiclab Robotics"
slug: Magiclab
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Magiclab Robotics — Developer Guide (hackathon edition)

⬆ [Magiclab Robotics profile](Magiclab.md) · [Product portfolio](Magiclab-Products.md) · [Roadmap and strategy](Magiclab-Roadmap-and-Strategy.md)

> Scope: what you need to get a MagicDog EDU or MagicBot Z1 Development Version moving and sensing in the first hour. Facts come from the official GitHub READMEs, changelogs, example scripts and the docs centre, read on 2026-11-14. Web search was unavailable in this run, so there are **no forum or third-party gotchas** here — only what the vendor itself documents.

## TL;DR — how you program it

- **One SDK per robot, C++20 with Python 3.10 bindings**, BSD-3-Clause, on GitHub (`magicdog_sdk`, `magicbot-z1_sdk`, `magicbot-gen1_sdk`, `magicdog-w_sdk`, `magicdog-y1_sdk`). You build it on **your own Ubuntu 22.04 laptop**; Mac and Windows are not supported, and the robot's on-board PC is not a development environment.
- **Wired Ethernet is the supported path.** Laptop on the robot's subnet (**MagicDog: 192.168.55.10, robot at 192.168.55.200**; **Z1: 192.168.54.111**), plus a **multicast route** on that interface. Without the route most calls fail.
- **Two control levels**: high-level (stand, gaits, trick actions, joystick-style velocity, SLAM / navigation) and low-level (per-joint commands with gains, state at **500 Hz**).
- **SDK access is edition-locked**: MagicDog **EDU** and Z1 **Development Version** only. The phone app and the SDK **cannot control the robot at the same time**.
- **AI stack is "bring your own"**: no vendor VLA is exposed through the robot SDK. What is open: Magic-W0 weights (manipulation, GPU needed), a pi0 recipe for Gen1, and an RL → MuJoCo → real pipeline for Z1 locomotion. For a 48-hour build, plan on **high-level SDK + your own perception / LLM on a laptop**.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| `magicdog_sdk` | C++20, Python 3.10 | MagicDog **EDU**: high- and low-level motion, sensors, audio (incl. streaming ASR), display / expression, state monitor, SLAM + navigation | [GitHub](https://github.com/MagiclabRobotics/magicdog_sdk) | Changelog top entry **v1.2.1-hotfix1** (Dec 2025), needs firmware ≥ **MagicDog 20251129**. Repo pushed Sep 2026 and already contains a gRPC-only mode the changelog does not list. |
| `magicbot-z1_sdk` | C++20, Python 3.10 | MagicBot Z1 **Development Version**: high-level, low-level, **hybrid** motion, sensors, audio, monitor, SLAM + navigation, hand tactile state | [GitHub](https://github.com/MagiclabRobotics/magicbot-z1_sdk) | **v1.2.6** (12 Aug 2026), needs firmware ≥ **MagicBot-Z1 20260708-v1.1.2**. Most actively maintained repo. PDF manual in `doc/en`. |
| `magicbot-gen1_sdk` | C++, Python | MagicBot Gen1 (docs list an extra upper-body motion service) | [GitHub](https://github.com/MagiclabRobotics/magicbot-gen1_sdk) | Not read in detail ⚠️ unverified |
| `magicdog-w_sdk`, `magicdog-y1_sdk` | C++, Python | MagicDog-W, MagicDog-Y1 | [W](https://github.com/MagiclabRobotics/magicdog-w_sdk) · [Y1](https://github.com/MagiclabRobotics/magicdog-y1_sdk) | Same layout as `magicdog_sdk`; details not read ⚠️ unverified |
| `magicdog_ros2_sdk` | ROS 2 (C++) | MagicDog EDU sensors as topics / services, SLAM and navigation. **No motion control** in this repo. | [GitHub](https://github.com/MagiclabRobotics/magicdog_ros2_sdk) | **Frozen**: docs say it "will no longer be updated". Last push May 2025. |
| `magicdog_motion_sdk` | C++ over **LCM** | Older pure motion SDK (high- and low-level) used by the ROS 2 path | [GitHub](https://github.com/MagiclabRobotics/magicdog_motion_sdk) | Last push May 2025; prefer `magicdog_sdk` |
| `magiclab_deploy` | Python | Runs an ONNX locomotion policy + ONNX odometry model on a real Z1 through the low-level SDK | [GitHub](https://github.com/MagiclabRobotics/magiclab_deploy) | Keyboard (SSH) or gamepad; has an aarch64 / Jetson helper script |
| `pico_teleoperate` | Python | PICO 4 Ultra whole-body teleoperation of **Gen1** | [GitHub](https://github.com/MagiclabRobotics/pico_teleoperate) | Needs PICO headset + 3 body trackers; last push Aug 2025 |
| `motor_tool` | C++ | Not documented; name suggests a joint-module utility ⚠️ unverified | [GitHub org](https://github.com/MagiclabRobotics) | — |

Build recipe (identical for dog and Z1, from the READMEs):

```bash
# deps: GCC >= 11.4, CMake >= 3.16, Eigen3, python3.10 (Z1 also OpenCV >= 4.5)
git clone https://github.com/MagiclabRobotics/magicdog_sdk.git && cd magicdog_sdk
mkdir build && cd build
cmake .. -DBUILD_EXAMPLES=ON -DCMAKE_INSTALL_PREFIX=/opt/magic_robotics/magicdog_sdk
make -j8 && sudo make install
export PYTHONPATH=/opt/magic_robotics/magicdog_sdk/lib:$PYTHONPATH
export LD_LIBRARY_PATH=/opt/magic_robotics/magicdog_sdk/lib:$LD_LIBRARY_PATH
```

Python modules: `magicdog_python`, `magicbot_z1_python`. Entry object in both: `MagicRobot()`.

## Control levels

| Level | What you get | Key calls (Python) | Rate / timing |
|---|---|---|---|
| **High-level** | Built-in controller keeps balance. Gaits (recovery stand, balance stand, stair gait on MagicDog), trick actions (MagicDog: lie down, shake head …; Z1: greetings, handshakes, welcome, hug, salute, clap …), joystick-style velocity command, head pose on MagicDog | `robot.set_motion_control_level(ControllerLevel.HIGH_LEVEL)` → `robot.get_high_level_motion_controller()` → `set_gait(GaitMode.…)`, `JoystickCommand` | RPC calls, default timeout **5 s**; long gaits need a larger timeout argument (examples use 10 000 ms) |
| **SLAM / navigation** (high-level) | Mapping, relocalisation, go-to-pose on a grid map, odometry stream | `switch_to_location()`, `activate_nav_mode(NavMode.GRID_MAP)`, `init_pose()`, `set_nav_target()`, `get_nav_task_status()`, pause / resume / cancel | Added in SDK v1.2.0 (Nov 2025) for both MagicDog and Z1 |
| **Hybrid** (Z1 only) | Added in v1.2.5 (Jun 2026). Appears to combine the built-in locomotion with your own joint commands ⚠️ unverified — read `hybrid_motion_example.py` | — | — |
| **Low-level** | Per-joint command structs (operation mode, `kp`, `kd`, targets) per group; joint state, body IMU and (Z1) state-estimator topics. **You own balance.** | `ControllerLevel.LowLevel` → `get_low_level_motion_controller()` → `subscribe_leg_state()`, `publish_leg_command()` … | State reported at **500 Hz**; suggested command rate **500 Hz** (example loop: 2 ms) |

- Z1 joint groups in the deployment repo: **12 leg**, **10 arm**, **1 waist**, **2 head** joints. Low-level examples put joints in operation mode `200` first.
- Enum spelling differs between SDKs: MagicDog Python uses `ControllerLevel.HIGH_LEVEL`, Z1 Python uses `ControllerLevel.HighLevel`. Copy from the matching example.
- **What the editions unlock**: all of the above is only reachable on MagicDog **EDU** and Z1 **Development Version**. Base / PRO units have no secondary-development access (see profile). Whether low-level mode is enabled on the hackathon units is a booth question.
- Recommendation for 48 hours: stay **high-level**. Low-level on a biped means a gantry, a safety person and a tested policy.

## ROS 2 and middleware

- **Native middleware is not ROS**: the SDK uses **LCM (UDP multicast) + gRPC + ZMQ + UDP**. On Z1, LiDAR point clouds and camera images moved to ZMQ in v1.2.1.
- **MagicDog gRPC-only mode** (docs quick start): `robot.initialize_grpc_only("192.168.55.10", features, "192.168.55.200")` with `SdkFeature.HIGH_LEVEL_MOTION | SdkFeature.SLAM_NAVIGATION`. No multicast route needed, and the docs say it is the mode to use over the robot's AP / WiFi. Limited to the features you enable; whether sensor streams work in this mode was not confirmed ⚠️ unverified — assume they need the default (multicast) mode.
- **ROS 2 for MagicDog EDU** (`magicdog_ros2_sdk`): ROS 2 **Foxy** on Ubuntu 20.04 (recommended) or **Iron** on 22.04, CycloneDDS, `ROS_DOMAIN_ID=25`. Topics include `/tof`, `/ultra`, `/head_touch_state`, battery, voice, RealSense depth, fisheye, binocular camera, LiDAR. It needs `magicdog_motion_sdk` for movement. **Frozen and built on end-of-life distros** — expect to fight it.
- **ROS 2 for humanoids**: no official package found. `magicbot-z1_description` is a ROS package (has `package.xml`, `launch`, `rviz`), which covers visualisation only.
- **Fastest ROS 2 route**: write a thin `rclpy` node that wraps the Python SDK (`cmd_vel` → joystick command, SDK sensor callbacks → ROS topics). Python **3.10** matches ROS 2 Humble on Ubuntu 22.04.

## Simulation and digital twins

| Asset / repo | Robot | Format / simulator | Link | Notes |
|---|---|---|---|---|
| `magicbot-z1_description` | Z1 | URDF + **MJCF** + meshes, RViz launch | [GitHub](https://github.com/MagiclabRobotics/magicbot-z1_description) | BSD-3 |
| `magicbot-gen1_description` | Gen1 | Robot description | [GitHub](https://github.com/MagiclabRobotics/magicbot-gen1_description) | BSD-3 |
| `magicdog_description`, `magicdog-w_description` | MagicDog, MagicDog-W | URDF | [dog](https://github.com/MagiclabRobotics/magicdog_description) · [W](https://github.com/MagiclabRobotics/magicdog-w_description) | BSD-3 |
| `magiclab_rl_lab` | Z1 (12-DoF legs) | **Isaac Lab 2.3.0 / Isaac Sim 5.1.0**, rsl_rl; task `Magiclab-Z1-12dof-Velocity` | [GitHub](https://github.com/MagiclabRobotics/magiclab_rl_lab) | Apache-2.0. The clone URL in its README has a typo; use the org URL. |
| `magiclab_mujoco` | Z1 (12-DoF) | **MuJoCo** sim-to-sim runner | [GitHub](https://github.com/MagiclabRobotics/magiclab_mujoco) | Check a policy before the real robot |
| `magicbot-mimic` | Z1 (23 DoF) | Isaac Lab 2.1.0 / Isaac Sim 4.5.0 motion tracking (BeyondMimic port) + MuJoCo sim-to-sim; task `Tracking-Flat-Z1-v0` | [GitHub](https://github.com/MagiclabRobotics/magicbot-mimic) | MIT |
| `Magiclab_GMR` | Z1 (24 driven joints) | Human motion (BVH LAFAN1 / Nokov, SMPL-X) → Z1 trajectory, MuJoCo viewer | [GitHub](https://github.com/MagiclabRobotics/Magiclab_GMR) | MIT; robot ID in code is `dreame_z1` |

- **USD assets, Gazebo worlds, quadruped RL environments**: none published (not public).
- Joint counts differ between repos (12 / 23 / 24). Match the model to the unit in front of you.
- Realistic in 48 hours: MuJoCo viewer for motion preview. Training a new policy in Isaac Lab is a multi-hour GPU job plus sim-to-real risk.

## AI stack

| Item | Status | What it is | Useful at the hackathon? |
|---|---|---|---|
| **Magic-W0** ([code](https://github.com/MagiclabRobotics/Magic-W0), [weights](https://huggingface.co/XuhuaX/Magic-W0)) | ✅ open (MIT code; weights released 30 Oct 2026) | "World–action" manipulation model; pre-trained + RoboDojo fine-tuned checkpoints; Python 3.11, NVIDIA GPU; shared 34-D state–action interface | Only if you have a GPU and a manipulator with demos to fine-tune on. Published evaluation uses the RoboDojo simulator, **not** a MagicBot SDK adapter. |
| **Inference** ([code](https://github.com/MagiclabRobotics/Inference)) | ✅ open (Apache-2.0, Sep 2026) | Real-time VLA runtime: policy server (WebSocket) + robot client, JAX / TensorRT backends. Reference hardware is **two Agilex Piper arms**, not a MagicLab robot. | Good pattern for running a slow policy next to a fast control loop |
| **magicbot-gen1_pi0_demo** ([code](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo)) | ✅ open (Apache-2.0) | pi0 (openpi) fine-tuning recipe for Gen1 dual-arm dexterous manipulation; converts collected **HDF5 → LeRobot v2.0** datasets | Only if a Gen1 with hands is hackable on site |
| **pico_teleoperate** | ✅ open | Data collection by PICO 4 Ultra teleoperation of Gen1 | Needs PICO hardware (not an on-site vendor) |
| **Locomotion policies** | ✅ pipeline open | `magiclab_rl_lab` → `magiclab_mujoco` → `magiclab_deploy` (ONNX). Policy files are referenced by config; whether trained weights ship in the repo was not checked ⚠️ unverified | Risky for 48 hours |
| **Magic-VLA K02, Magic-Mix, Magic-Brain** | 🧪 | Company models / agent framework described in press and articles | **No public weights or code** found |
| **Datasets** | — | No public MagicLab dataset found | — |
| **LeRobot** | — | No official LeRobot robot driver found; only the dataset-format conversion above | — |
| **Voice** | ✅ | Audio service in the SDK; MagicDog gained streaming ASR and expression control in v1.2.1 | Cheap win for interaction demos |

Practical recipe: run a VLM / LLM agent on your laptop, feed it SDK camera frames, and let it call a **small tool set** (go-to-pose, stand, trick action, speak). MagicLab's own September 2026 article describes the same split — a VLM agent that points at the target, and a policy that executes.

## Compute, sensors and connectivity

| Topic | MagicDog EDU | MagicBot Z1 Development Version |
|---|---|---|
| Laptop IP (wired) | **192.168.55.10** (any 192.168.55.X) | **192.168.54.111** (any 192.168.54.X) |
| Robot IP | **192.168.55.200** (on-board computer) | not captured — see the Z1 quick start |
| Multicast | `sudo ifconfig <if> multicast` and `sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev <if>` | same |
| Wireless development | FAQ: **not supported**. Quick start: gRPC-only mode can work over the robot AP (high-level and navigation only). | FAQ: **not supported** |
| Sensor streams in SDK | IMU, laser scan, RGB-D colour / depth + camera info, binocular left / right, head touch, ultrasonic | body IMU, joint states, LiDAR point cloud, cameras (via ZMQ), hand tactile / force state (v1.2.6) |
| Extra video | Fisheye `rtsp://192.168.12.1:8080/`, 4K `rtsp://192.168.12.1:8082/` (from the FAQ; test with `ffplay`) | GST video streaming not supported in the current software |
| SDK logs | `/tmp/logs/magicdog_sdk.log`, config `/tmp/magicdog_mjrrt.yaml` | `/tmp/logs/magicbot_z1_sdk.log`, config `/tmp/magicbot_z1_mjrrt.yaml` |

- **On-board compute**: the vendor states the on-board PC runs its own services and is not a development environment. Bring a laptop (Ubuntu 22.04, x86_64). The Z1 deployment repo references **aarch64** SDK libraries and a Jetson script, so a Jetson companion computer is workable.
- **Sensors must be switched on before subscribing** on MagicDog: `robot.open_channel_switch()`, then `open_laser_scan()`, `open_rgbd_camera()`, `open_binocular_camera()` on the sensor controller. On Z1 the docs give `OpenLidar` as the example.
- Hardware specs (LiDAR type, compute TOPS, battery) are in the [profile](Magiclab.md).

## First 60 minutes checklist

1. **Ask the booth (5 min)**: Is this an **EDU / Development Version**? Which **firmware version**? Is low-level mode allowed? Where is the Ethernet port, and what is the **e-stop**? Who is the safety person?
2. **Prepare the laptop (10 min)**: Ubuntu 22.04, `sudo apt install build-essential cmake libeigen3-dev python3-dev` (Z1: also `libopencv-dev`). Add `* - rtprio 98` to `/etc/security/limits.conf`; set `net.core.rmem_max`, `rmem_default`, `wmem_max`, `wmem_default` to `20971520` in `/etc/sysctl.conf`, then `sudo sysctl -p`.
3. **Pick the SDK tag that matches the firmware (5 min)**: read `CHANGELOG.md` in the repo; each release names its minimum firmware. Clone and build with `-DBUILD_EXAMPLES=ON` (recipe above).
4. **Connect (5 min)**: Ethernet to the robot. Set the laptop to `192.168.55.10/24` (MagicDog) or `192.168.54.111/24` (Z1). `ping 192.168.55.200` for MagicDog. Add the multicast route and confirm with `ip route | grep 224.0.0.0`.
5. **Close the phone app** — app and SDK cannot both control the robot.
6. **Verify with the monitor example (5 min)**: `python3 example/python/monitor_example.py` → robot state report. If it hangs, read the SDK log in `/tmp/logs/`.
7. **Hello-world motion (10 min)**: clear 2 m around the robot, then run `example/python/high_level_motion_example.py` (keyboard menu: recovery stand → balance stand → a trick → joystick walk). Minimal MagicDog version:
   ```python
   import magicdog_python as magicdog
   robot = magicdog.MagicRobot()
   assert robot.initialize("192.168.55.10")          # or initialize_grpc_only(...)
   robot.connect()
   robot.set_motion_control_level(magicdog.ControllerLevel.HIGH_LEVEL)
   ctl = robot.get_high_level_motion_controller()
   ctl.set_gait(magicdog.GaitMode.GAIT_STAND_R)       # recovery stand
   ```
8. **Read sensors (10 min)**: `sensor_example.py` → open the channel switch, enable the camera / LiDAR, subscribe and save one RGB frame and one scan. Keep callbacks short (copy the data, return).
9. **Map the room (10 min, optional)**: `slam_example.py` to build a map, then `navigation_example.py`: `switch_to_location()` → `activate_nav_mode(GRID_MAP)` → `init_pose()` → `set_nav_target()`. Navigation will not start until relocalisation has succeeded.
10. **Freeze your setup**: note SDK tag, firmware, IPs and the working example in your team notes before building on top.

## Known gotchas and safety

| Gotcha | Symptom | Fix |
|---|---|---|
| SDK tag does not match firmware | SDK "becomes unavailable", topics silent | Use the release named for your firmware in `CHANGELOG.md`; do not self-update firmware during the event |
| Multicast route missing | `Failed to disable SDK`, LCM init failure, no sensor / audio data | Re-add the route (it is lost on cable re-plug); the docs give a NetworkManager dispatcher script to automate it |
| App still connected | Commands ignored or fighting | Close the app; one controller at a time |
| RPC `Deadline Exceeded` | Long gait or skill call fails after 5 s | Pass a larger timeout to that call |
| Stale `/tmp/*_mjrrt.yaml` | Topics misbehave after switching SDK versions in one boot | Delete the file or reboot the laptop |
| Blocking in callbacks | Message backlog, lag, odd errors | Hand data to a queue; process elsewhere |
| Small socket buffers | Unstable topic rates | Apply the `sysctl` values above |
| Docker / WiFi interfaces (ROS 2 path) | DDS discovery fails | Turn WiFi off and `sudo ifconfig docker0 down` |
| ROS 2 docs typo | `rmw_cyclonedx-cpp` in the docs page | The package is `rmw_cyclonedds_cpp` (as in the repo README) |
| Python version | `ImportError` on the binding | Bindings are built for **Python 3.10**; rebuild if your interpreter differs. Bundled binaries built on 22.04 fail on older glibc. |
| Wireless | FAQ says wired only; quick start mentions gRPC-only over AP | Treat wireless as best-effort; keep a cable on hand |
| Conflicting DoF counts | URDF / policy does not match the robot | Check the variant (Z1 12 / 23 / 24 joints across repos) |

Safety:

- **E-stop**: no hardware e-stop procedure was found in the pages read. Ask the vendor before the first motion. On the Z1 remote, **Home + Start** takes control and **Home + Back** releases it; in `magiclab_deploy`, **Space** (keyboard) or **LB + RB** (gamepad) is the software emergency stop.
- **Low-level mode disables the built-in balance controller.** Z1 low-level work belongs on the hanger / gantry. When the older MagicDog motion SDK client exits, the robot is set to `PureDamper` — expect it to sink to the ground.
- Exit low-level cleanly: the Z1 example switches back to balance stand before quitting.
- Vendor notes that speed, payload and endurance are lab values; snow, ice and wet thermal-bath floors are untested — walk the route with a spotter first.
- Licences: SDKs and descriptions are BSD-3; Magic-W0 is MIT but its training-time teacher models carry their own terms; `magiclab_mujoco` and `magiclab_deploy` state no licence.

## Community resources

- [GitHub org](https://github.com/MagiclabRobotics) — 22 public repos; issues are the only public support channel found. Community is small (single-digit to low double-digit stars per repo), so do not expect searchable answers.
- [Docs centre](https://support.magiclab.top/) — per-robot guides (MagicDog, MagicDog-W, MagicDog-Y1, Gen1, Z1) with C++ API, Python API, examples and FAQ. English pages live under `/en/docs/...`.
- SDK PDF manuals — in each SDK repo under `doc/en`.
- Research pages and model articles — see [Roadmap and strategy](Magiclab-Roadmap-and-Strategy.md).
- Forum, Discord or Slack: none found.
- Best resource on site: the MagicLab engineers at the booth. Bring the firmware and edition questions from step 1.

## Sources

- [GitHub — MagiclabRobotics organisation (repository list)](https://github.com/MagiclabRobotics)
- [GitHub — magicdog_sdk (README, CHANGELOG, Python examples)](https://github.com/MagiclabRobotics/magicdog_sdk)
- [GitHub — magicbot-z1_sdk (README, CHANGELOG, Python examples)](https://github.com/MagiclabRobotics/magicbot-z1_sdk)
- [GitHub — magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk)
- [GitHub — magicdog_motion_sdk](https://github.com/MagiclabRobotics/magicdog_motion_sdk)
- [GitHub — magiclab_rl_lab](https://github.com/MagiclabRobotics/magiclab_rl_lab)
- [GitHub — magiclab_mujoco](https://github.com/MagiclabRobotics/magiclab_mujoco)
- [GitHub — magiclab_deploy](https://github.com/MagiclabRobotics/magiclab_deploy)
- [GitHub — magicbot-mimic](https://github.com/MagiclabRobotics/magicbot-mimic)
- [GitHub — Magiclab_GMR](https://github.com/MagiclabRobotics/Magiclab_GMR)
- [GitHub — magicbot-z1_description](https://github.com/MagiclabRobotics/magicbot-z1_description)
- [GitHub — pico_teleoperate](https://github.com/MagiclabRobotics/pico_teleoperate)
- [GitHub — magicbot-gen1_pi0_demo](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo)
- [GitHub — Magic-W0](https://github.com/MagiclabRobotics/Magic-W0)
- [GitHub — Inference](https://github.com/MagiclabRobotics/Inference)
- [MagicLab Docs Center](https://support.magiclab.top/)
- [Docs — MagicDog quick start](https://support.magiclab.top/en/docs/dog/quick_start_reference)
- [Docs — MagicDog FAQ](https://support.magiclab.top/en/docs/dog/FAQ)
- [Docs — MagicDog ROS2 SDK user guide](https://support.magiclab.top/en/docs/dog/ros2_sdk)
- [Docs — MagicBot Z1 SDK overview](https://support.magiclab.top/en/docs/human-z1/overview_reference)
- [Docs — MagicBot Z1 FAQ](https://support.magiclab.top/en/docs/human-z1/FAQ)
- [Docs — MagicBot Z1 remote control](https://support.magiclab.top/en/docs/human-z1/remote-control)
- [MagicLab news — In-Context Visual Guidance with Magic-Brain](https://www.magiclab.top/en/news/65)
