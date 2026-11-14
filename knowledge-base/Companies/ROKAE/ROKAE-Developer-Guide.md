---
type: dev-guide
company: "ROKAE Robotics"
slug: ROKAE
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# ROKAE Robotics — Developer Guide (hackathon edition)

⬆ [ROKAE Robotics profile](ROKAE.md) · [Product portfolio](ROKAE-Products.md) · [Roadmap and strategy](ROKAE-Roadmap-and-Strategy.md)

> Research note: built from ROKAE's official docs portal and official GitHub account (fetched 2026-11-14). Open web search was not available for this pass, so community / third-party assets (MuJoCo, Isaac, LeRobot ports) could not be checked — they are marked accordingly.

## TL;DR — how you program it

- **One SDK for every arm: xCore SDK** (C++, Python, C#, Android/Java), Apache-2.0, on GitHub under `RokaeRobot`. It talks to the xCore controller over **TCP/IP**; the real-time channel uses **UDP**.
- **Python = high-level only.** Point-to-point and linear moves, jog, drag teaching, force-control setup, I/O, registers. Enough for most 48-hour builds (pick-and-place, compliant contact, massage-style demos).
- **C++ = everything, including 1 kHz real-time mode** with five controller modes on xMate cobots: joint position, Cartesian position, joint impedance, Cartesian impedance, **direct torque**. Needs a wired direct link and ideally a PREEMPT_RT Linux PC.
- **ROS 2 Humble package (`rokae_ros2`)** with `ros2_control`, MoveIt 2 configs per model, URDF/xacro and Gazebo — the fastest way to get planning plus simulation without touching the SDK.
- **No downloadable AI models or datasets.** ROKAE supplies force-controlled hardware and control software; bring your own policy and perception, plus an external PC (the arm controller has no GPU).

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| xCoreSDK-CPP | C++ (CMake ≥ 3.12) | All xCore robots: xMate cobots, AR 7-DoF arms, NB/XB industrial arms. Non-real-time motion, real-time mode, PC-side planner, kinematics/dynamics model (`xMateModel`) | [GitHub](https://github.com/RokaeRobot/xCoreSDK-CPP) | Ubuntu 18.04 / 20.04 / 22.04 (x86_64, aarch64), Windows 10/11 (MSVC 14.1+). Repo has headers + examples; **prebuilt libs come from the Releases page** and go in `lib/`. README references **v0.7.1**, controller **xCore ≥ 3.2.1** |
| xCoreSDK-Python | Python **3.8–3.12** | Same robots, **non-real-time only**: motion queue, jog, drag, force control, I/O, registers, RL projects | [GitHub](https://github.com/RokaeRobot/xCoreSDK-Python) | **Not on pip.** Clone, then extract the matching release archive (win / linux-x86_64 / linux-aarch64) into `Release/`. First script: `example/base_example.py` |
| xCoreSDK-CSharp | C# | Same scope as Python | [GitHub](https://github.com/RokaeRobot/xCoreSDK-CSharp) | Windows only |
| xCoreSDK-Android | Java | Same scope as Python | [GitHub account](https://github.com/RokaeRobot) | Last updated 2023 — treat as stale |
| rokae_ros2 | C++ / ROS 2 Humble | xMate SR / CR / ER / Pro, AR arms, several NB/XB arms | [GitHub](https://github.com/RokaeRobot/rokae_ros2) · [manual](https://docs.rokae.com/en/docs/ROS2) | `ros2_control` hardware interface, MoveIt 2, Gazebo, driver services (movej / movel / IK / DI-DO / drag) |
| xCorePlugin-client / -controller | C++ | Extensions to the pendant software and controller | [GitHub account](https://github.com/RokaeRobot) | Not needed for a hackathon build |
| Arc-welding SDK | C++ / Python / C# | Welding process package | [SDK docs](https://docs.rokae.com/en/docs/SDK) | Only relevant with the welding robot |
| Helios "ROS 2 + Python SDK" | — | Wheeled dual-arm robot | [Helios page](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html) | Listed on the product page; **no public repo or docs found** — ask ROKAE staff on site |
| iNex | — | Whole-body controller for wheeled humanoids / dual-arm systems | not public | 🧪 Described in ROKAE news only; no public API |

Doc versions on the portal: **0.7.x**, **0.7.x-AR** (humanoid arm) and **0.8.x**. C++ changelog: v0.7.0 (2026.1), v0.7.1 (2026.3), v0.7.2 (2026.6, for xCore 3.2.2). **Match SDK version to the controller firmware on the robot you are given.**

Robot classes (pick by model; the SDK checks the class against the connected robot):

| Class | Use for |
|---|---|
| `xMateRobot` | 6-axis cobots (SR, CR, …) |
| `xMateErProRobot` | 7-axis arms — ER Pro **and AR series** |
| `xMateCr5Robot` | CR5 (5-axis) |
| `StandardRobot` | 6-axis industrial NB / XB |

## Control levels

| Level | Interface | Rate | What you get | Requirements |
|---|---|---|---|---|
| Pendant / no-code | RobotAssist HMI, drag teaching, RL programs | — | Teach points, run programs, calibrate tool/load and force sensor | None |
| High-level (non-real-time) | Python / C# / C++ SDK, ROS 2 driver services | Command queue, not cyclic | `MoveAbsJ`, `MoveJ`, `MoveL`, `MoveC`, `MoveCF`, `MoveSP`; jog; drag and path replay (xMate only); collision detection; force-control setup (`fcInit` / `fcStart`, Cartesian or joint stiffness, desired force); DI/DO, registers, RS-485 | Any OS above; switch or direct cable both work |
| Trajectory streaming | ROS 2 `ros2_control` + MoveIt 2 | Real-robot controllers default to **1000 Hz** update | `follow_joint_trajectory`, MoveIt planning, RViz | Ubuntu 22.04 + Humble; RT kernel recommended |
| Low-level real-time | **C++ only** (`RtMotionControl`) | **up to 1 kHz** | xMate cobots: joint position, Cartesian position, joint impedance, Cartesian impedance, **direct torque**. 6-axis industrial arms: joint + Cartesian position only | Direct cable to the controller's control LAN port, no switch; whole loop (network round trip + your code + robot) **under 1 ms**; timeout configurable 1–4 ms in `xcoresdk_config.json` |

- **EDU / developer editions:** the docs state no separate licence or paid option for real-time mode. Whether the on-site units have it enabled — ⚠️ unverified, ask staff.
- **AR arms in real-time mode:** the AR FAQ documents **joint position and Cartesian position** demos. Impedance / torque modes on AR are not documented there — ⚠️ unverified.
- **Published torque-mode limits** (docs list only these models):

| Model | Axes | Max torque | Max torque rate |
|---|---|---|---|
| xMate ER3 Pro / ER7 Pro | 1–4 | **85 Nm** | 1500 Nm/s |
| | 5–7 | **36 Nm** | 1000 Nm/s |
| xMate3 / xMate7 | 1–3 | **85 Nm** | 1500 Nm/s |
| | 4–6 | **36 Nm** | 1000 Nm/s |

Recommendation for 48 hours: **stay in Python non-real-time + built-in force control** unless your idea really needs a custom control law. Real-time mode costs half a day of RT-kernel and network tuning.

## ROS 2 and middleware

| Item | Detail |
|---|---|
| Package | `rokae_ros2` v0.1.1 — [repo](https://github.com/RokaeRobot/rokae_ros2) |
| Supported stack | **ROS 2 Humble on Ubuntu 22.04 x86_64** only (other distros "may be incompatible") |
| Sub-packages | `rokae_hardware` (ros2_control SystemInterface + drivers), `rokae_description` (URDF/xacro, meshes), `rokae_msgs`, `rokae_<model>_moveit_config`, `rokae_gazebo` |
| `robot_type` values | SR3 / SR4 / SR5 · CR7 / CR12 / CR18 / CR20 / CR35 · ER3 / ER7 · Pro3 / Pro7 · AR3L / AR3R / AR5L / AR5R (+ variants) · XB / NB industrial models |
| Dual-arm wheeled platform | **RViz visualisation only** — no control, MoveIt or Gazebo |
| Topics | `/joint_states`, `/rokae_driver/joint_states`, `/rokae_driver/cartesian_pose` |
| Driver services (`/rokae_driver/…`, 7-axis: `/rokae_driver7/…`) | `movej`, `movel`, `movec`, `jog_control`, `drag_control`, `calculate_fk`, `calculate_ik`, `get/set_di`, `get/set_do`, `read/write_register`, `get_robot_info` |
| Actions | `/move_action`, `/execute_trajectory`, `/position_joint_trajectory_controller/follow_joint_trajectory` |

Launch lines from the manual:

```bash
# MoveIt with fake hardware (no robot needed)
ros2 launch rokae_hardware rokae_moveit_launch.py robot_type:=SR4 use_fake_hardware:=true
# MoveIt on the real arm
ros2 launch rokae_hardware rokae_moveit_launch.py robot_type:=SR5 use_fake_hardware:=false robot_ip:=<robot> local_ip:=<your NIC>
# Driver only (services + state topics)
ros2 launch rokae_hardware rokae_driver.launch.py robot_ip:=<robot> local_ip:=<your NIC>
```

No force/torque or impedance topics are listed in the ROS 2 manual — for contact tasks call the SDK directly or wrap it in your own node.

## Simulation and digital twins

| Asset | Status | Where |
|---|---|---|
| URDF / xacro + meshes | ✅ official | `rokae_description` in [rokae_ros2](https://github.com/RokaeRobot/rokae_ros2) |
| Gazebo (via `gazebo_ros2_control`) | ✅ official | `rokae_gazebo`: `empty.world`, `obstacles.world`, record / replay scripts, unified `gazebo_moveit.launch.py mode:=sim|real` |
| MoveIt 2 fake hardware | ✅ official | `use_fake_hardware:=true` |
| MuJoCo MJCF | not found in official repos | Convert the URDF yourself; community models ⚠️ unverified |
| Isaac Sim / Isaac Lab USD | not found in official repos | Import the URDF; ⚠️ unverified |
| RokaeStudio offline programming | ✅ vendor tool | [Download center](https://www.rokae.com/en/service/190/Download-Center.html) (some downloads need a MyROKAE login) |
| Helios / Human.X simulation assets | not public | — |

## AI stack

| Topic | What exists publicly |
|---|---|
| Pretrained policies / VLA | **None downloadable.** WRC 2026 demos used a self-developed "embodied skill model" with imitation learning + human-in-the-loop RL (USB insertion, reported 95–99 % success) — not released |
| Foundation-model interface | iNex is described as exposing interfaces for teleoperation devices and model training 🧪 — no public docs |
| Datasets | not public |
| Teleoperation / data collection | Shown with third-party kit: IO-AI TeleXperience, **Wuji Hand**, motion capture, exoskeleton gloves. No ROKAE-published pipeline. Helios lists gamepad control only |
| LeRobot support | No official integration found. Practical route: write a small LeRobot robot class around the Python SDK (`jointPos()` for state, `MoveAbsJ` queue for actions) — expect low action rates in non-real-time mode |
| Built-in "skills" worth using | Drag teaching + path replay, Cartesian / joint impedance, desired-force control, collision detection with selectable reaction (stop or compliant) |

Fastest learning pipeline for a weekend: kinesthetic demos by **drag teaching** (`enableDrag`), log `jointPos()` and camera frames on your PC, train a small imitation policy, execute through the motion queue. **WUJI is on site** — the same hand ROKAE used in its own teleoperation demo.

## Compute, sensors and connectivity

| Item | Detail |
|---|---|
| Arm controller | xCore controller (compact MSC / MAC units for SR / AR). No GPU — runs motion control only |
| Your PC | Linux x86_64 or aarch64 (Jetson and Raspberry Pi 3B+/4/5 work if glibc ≥ 2.27), or Windows 10/11 |
| Default network | Direct-connect port: static **192.168.0.160**. Set your PC to the same subnet, e.g. 192.168.0.22. A second port is for router / switch networks (docs warn this can make motion unstable) |
| Other IPs seen in docs | ROS 2 manual examples use 192.168.2.160 (SR5) and 192.168.21.10 (industrial) — **read the actual IP from the pendant** |
| Protocol | TCP for commands, UDP for real-time state/commands; `connectToRobot(remoteIP, localIP)` — the local IP is needed for the real-time/state stream |
| Built-in sensing | Joint torque sensors on xMate / AR: `jointTorque()`, external force via `getEndTorque(...)`; DI/DO; RS-485 on some controllers |
| Not included | Camera, gripper, GPU — plan your own (D-Robotics RDK board or a laptop for perception) |
| Helios (if on site) | Compute option: Orin NX 8 GB, AGX Orin 64 GB or Thor T5000. 2× 3D LiDAR, head stereo camera, IMU; optional fisheye / chest / wrist cameras, mic array. Wi-Fi 2.4/5 GHz, Bluetooth, optional 5G; HDMI, USB 2.0, RJ45 debug ports. ~4 h runtime |

## First 60 minutes checklist

1. **Ask ROKAE staff (5 min):** exact model, controller firmware version (xCore 3.x), robot IP, which SDK version they recommend, whether real-time mode is allowed, where the e-stop is.
2. **Safety setup:** clear the workspace, e-stop within reach, confirm tool and **payload mass / centre of mass are entered on the pendant** (wrong load data makes force control drift).
3. **Cable:** PC straight into the robot's direct-connect port. Set a static IP on the same subnet (default robot IP 192.168.0.160). `ping` it.
4. **Get the SDK:** `git clone https://github.com/RokaeRobot/xCoreSDK-Python`, download the matching release archive from the repo's Releases page, extract into `Release/`. Python 3.8–3.12.
5. **Verify:** edit the IP in `example/base_example.py` and run it from `example/`. It should connect and print robot info / state.
6. **Hello-world motion (slow speed first).** Documented call order — take exact enum names and argument shapes from `base_example.py`:
   - create the right class (`xMateRobot` for 6-axis, `xMateErProRobot` for 7-axis/AR) and `connectToRobot(...)`
   - `setOperateMode(` automatic `)` → `setPowerState(` on `)`
   - `setMotionControlMode(` NrtCommandMode `)`
   - `moveReset()` → `moveAppend(` MoveAbsJ / MoveL command(s) `)` → `moveStart()`
   - `stop()` to halt; power off when done
7. **Read sensors:** `jointPos()`, `posture(...)`, `jointTorque()`, `getEndTorque(...)`. Push gently on the flange and watch the values change.
8. **Try compliance:** `enableDrag(...)` and move the arm by hand, then `disableDrag()`. For contact tasks: `fcInit` → `setControlType` → `setCartesianStiffness` / `setCartesianDesiredForce` → `fcStart` … `fcStop`.
9. **Enable collision detection** before any demo near people: `enableCollisionDetection(sensitivity, behaviour, fallback)`.
10. **ROS 2 route instead (optional):** on Ubuntu 22.04 + Humble, build `rokae_ros2`, run the fake-hardware MoveIt launch first, then the real launch with `robot_ip` and `local_ip`.

## Known gotchas and safety

| Gotcha | What to do |
|---|---|
| Python has **no real-time mode**, no PC-side planner, no `xMateModel` | Use C++ for 1 kHz loops or dynamics |
| SDK not installable via pip; repo ships without binaries | Download the release archive that matches OS, CPU and Python version |
| SDK / firmware mismatch | README requires xCore ≥ 3.2.1 for v0.7.1; AR FAQ still references an older AR-specific pair (controller 3.0.1.6.AR…, SDK v0.5.1.ar) — confirm versions with staff |
| Real-time mode over a switch or Wi-Fi | Use a direct cable; docs recommend a **Realtek NIC over Intel**, `performance` CPU governor, PREEMPT_RT kernel |
| 1 kHz callback overruns | No printing, file I/O, sleeping, sockets or allocation in the loop; raise the timeout (1–4 ms) or network tolerance if packets drop |
| After switching to real-time mode the robot stays powered and comes up in automatic mode after restart | Be aware before rebooting next to people |
| Torque mode: sag, float or drift | Almost always wrong payload / COM or an uncalibrated force sensor. Calibrate (pendant or `calibrateForceSensor`), set `setGravityDirection` for side mounts. Controller adds gravity + friction compensation to your commanded torque |
| Torque jumps at start | Ramp from small values; respect torque and torque-rate limits |
| Noisy `getEndTorque` | Compute external torque from `tau_m` minus model gravity (and Coriolis when moving) |
| State values all zero or lagging in C++ | Request the field in `startReceiveRobotState`, use the same period in `updateRobotState`, flush stale packets first |
| AR arms | Use the 7-axis class; shipped Cartesian demo is written for 6-axis and will not run unchanged; left and right side-mount parameters differ; set automatic + real-time mode **before** power-on; call `setDefaultConfOpt(false)` if IK/FK fails |
| ROS 2 | Humble / 22.04 only; 6-axis vs 7-axis SDK type is switched manually in `rokae_hardware_interface`; check the pendant's RCI setting and packet loss on the real robot; test with fake hardware first |
| Helios DoF | Product page says 42 in the text and 23 in the spec table (news says 43) — confirm before planning whole-body tasks |
| Human contact (T04) | Collision detection and impedance reduce risk but these are **not certified medical devices**. Low stiffness, low speed, e-stop in the operator's hand, test on a dummy first |

## Community resources

| Resource | Link | Note |
|---|---|---|
| Docs portal (SDK, xCore manual, ROS 2, plugins, downloads) | [docs.rokae.com/en](https://docs.rokae.com/en/) | English pages exist; some sub-page URLs and comments are Chinese |
| C++ real-time troubleshooting (network, torque, AR) | [torque control FAQ](https://docs.rokae.com/en/docs/SDK/cpp/%E5%AE%9E%E6%97%B6%E6%A8%A1%E5%BC%8F%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/cpp_rt_torque_control) · [AR FAQ](https://docs.rokae.com/en/docs/SDK/cpp/%E5%AE%9E%E6%97%B6%E6%A8%A1%E5%BC%8F%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/cpp_rt_ar_special) | Best source of practical gotchas |
| GitHub issues | [RokaeRobot](https://github.com/RokaeRobot) | Small community: xCoreSDK-CPP ~46 stars, a handful of open issues |
| Forum / Discord | not found | The on-site ROKAE engineers are the realistic support channel |

## Sources

- [ROKAE documentation hub](https://docs.rokae.com/en/)
- [xCore SDK landing page](https://docs.rokae.com/en/docs/SDK)
- [SDK introduction (platforms, real-time modes, language support)](https://docs.rokae.com/en/docs/SDK/SDK_Intro)
- [SDK quick start (network, build, RT kernel)](https://docs.rokae.com/en/docs/SDK/quick_start)
- [SDK FAQ](https://docs.rokae.com/en/docs/SDK/sdk_faq)
- [C++ SDK introduction (version history)](https://docs.rokae.com/en/docs/SDK/cpp/cpp_Intro)
- [Python SDK introduction](https://docs.rokae.com/en/docs/SDK/python/py_Intro)
- [Python SDK API description](https://docs.rokae.com/en/docs/SDK/python/py_API)
- [C++ real-time mode — torque control issues](https://docs.rokae.com/en/docs/SDK/cpp/%E5%AE%9E%E6%97%B6%E6%A8%A1%E5%BC%8F%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/cpp_rt_torque_control)
- [C++ real-time mode — AR models](https://docs.rokae.com/en/docs/SDK/cpp/%E5%AE%9E%E6%97%B6%E6%A8%A1%E5%BC%8F%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98/cpp_rt_ar_special)
- [ROS 2 package manual](https://docs.rokae.com/en/docs/ROS2)
- [Rokae xMate ROS 2 user manual](https://docs.rokae.com/en/docs/ROS2/rokae%20ros2%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C)
- [GitHub — RokaeRobot account](https://github.com/RokaeRobot)
- [GitHub — xCoreSDK-CPP](https://github.com/RokaeRobot/xCoreSDK-CPP)
- [GitHub — xCoreSDK-Python](https://github.com/RokaeRobot/xCoreSDK-Python)
- [GitHub — rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE news — WRC 2026 full-stack development platform](https://www.rokae.com/en/news/show/2604/WRC-2026:-ROKAE-Unveils-a-Ready-to-Use-Full-Stack-Development-Platform-for-Embodied-Intelligence,-Advancing-Physical-AI-Infrastructure-Development.html)
- [ROKAE download center](https://www.rokae.com/en/service/190/Download-Center.html)
