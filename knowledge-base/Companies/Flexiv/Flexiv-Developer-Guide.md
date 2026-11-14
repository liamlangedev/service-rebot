---
type: dev-guide
company: "Flexiv Robotics"
slug: Flexiv
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Flexiv Robotics — Developer Guide (hackathon edition)

⬆ [Flexiv Robotics profile](Flexiv.md) · [Product portfolio](Flexiv-Products.md) · [Roadmap and strategy](Flexiv-Roadmap-and-Strategy.md)

## TL;DR — how you program it

- **One SDK, two generations.** Everything goes through **Flexiv RDK** (C++ / Python, Apache-2.0). **RDK v1.9.x** drives **Rizon / AICO** (robot software v3.11.x); **RDK v2.x** drives **Enlight / MICO** (robot software v3E.x). The two APIs are **not interchangeable** — ask the booth which arm and which robot software version you have before installing anything.
- **Fast path for 48 hours:** Python + **non-real-time (NRT) primitives and Cartesian motion-force commands**. No real-time kernel, works from Linux, macOS or Windows, tolerates up to **1000 ms** round-trip latency (even wireless LAN).
- **Full power:** **1 kHz** real-time streaming of joint torque, joint position / impedance or Cartesian motion + force. Needs the **Professional** RDK licence, **wired LAN**, **< 1 ms** round-trip latency and Linux or macOS.
- **ROS 2:** `flexiv_ros2` (Humble / Jazzy) with ros2_control, MoveIt and a fake-hardware mode. It exposes joint position / joint impedance — for force-controlled contact use the RDK directly.
- **AI:** no pretrained Flexiv policy or VLA is public. The supported pipeline is **Flexiv Trainer**: leader-follower teleop → **LeRobot-format** episodes → train → rollout. It needs a leader arm *and* a follower arm.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| `flexiv_rdk` | C++, Python (`pip install flexivrdk`) | Arm states, RT + NRT motion / force, primitives, plans, gripper, tools, digital I/O, dynamics (Jacobian, mass matrix, gravity) | [repo](https://github.com/flexivrobotics/flexiv_rdk) · [manual v2.x](https://www.flexiv.com/software/rdk/manual/v2.x/index.html) · [manual v1.x](https://www.flexiv.com/software/rdk/manual/v1.x/index.html) | ✅ Linux (Ubuntu 22.04+), macOS 12+, Windows 10+, QNX. Python 3.10 / 3.12 (3.14 on Linux). PyPI latest = **2.1.0**; latest v1 = **1.9.4.1** |
| `flexiv_rdk_csharp` | C# | Same as RDK | [org](https://github.com/flexivrobotics) | ✅ |
| `flexiv_ros2` | C++ (ROS 2) | ros2_control hardware interface, MoveIt config, Grav gripper actions | [repo](https://github.com/flexivrobotics/flexiv_ros2) | ✅ Humble (22.04) and Jazzy (24.04); `-v1` branches for Rizon |
| `flexiv_description` | xacro / URDF | Robot models for RViz and simulators | [repo](https://github.com/flexivrobotics/flexiv_description) | ✅ Rizon 4 / 4s / 10 / 10s, Enlight-L, MICO, AICO variants |
| `flexiv_tdk` | C++, Python (`pip install flexivtdk`) | Robot-to-robot or device-to-robot teleoperation with force feedback, LAN or WAN | [repo](https://github.com/flexivrobotics/flexiv_tdk) | ✅ Ubuntu 22.04+ only; needs real-time privileges |
| `flexiv_trainer` | Python (web UI) | Teleop data collection, LeRobot datasets, policy training, rollout and evaluation | [repo](https://github.com/flexivrobotics/flexiv_trainer) | ✅ Ubuntu 22.04+, Python 3.12 / 3.14, GPU recommended |
| `flexiv_drdk` | C++, Python | Synchronised dual-robot control | [org](https://github.com/flexivrobotics) | ✅ Linux only |
| `flexiv_ddk` | C++, Python (+ C#) | Data Distribution Kit: stream robot data (up to 1 kHz) for logging | [org](https://github.com/flexivrobotics) | ✅ Linux, Windows |
| `flexiv_pdk` + `flexiv_composer_studio` | Python / web | Motion planning and scan-path authoring for workcells | [org](https://github.com/flexivrobotics) | ✅ |
| `flexiv_amr_sdk`, `flexiv_amr_ros2` | C++ | FMR 300 mobile base | [org](https://github.com/flexivrobotics) | ✅ binaries + headers |
| `isaac_sim_ws`, `flexiv_sim_plugin` | Python, C++ | Flexiv robots in NVIDIA Isaac Sim, driven by Elements Studio + RDK | [repo](https://github.com/flexivrobotics/isaac_sim_ws) | ✅ Ubuntu 22.04 / 24.04, x86_64 |
| Flexiv Elements (tablet) / Elements Studio (desktop) | Graphical | No-code programs, settings, licence install, free drive, simulated robot | not a public download ⚠️ unverified | Needed for setup even if you only use the RDK |
| `flexiv_aidk` | C++, Python | "Noema Edge" AI vision kit | [org](https://github.com/flexivrobotics) | Last updated 2024-03 — treat as legacy |

## Control levels

| Level | RDK mode | What you send | Rate / latency | Licence |
|---|---|---|---|---|
| Plans | `NRT_PLAN_EXECUTION` | Name of a program authored in Elements | one-shot | Standard |
| Primitives | `NRT_PRIMITIVE_EXECUTION` | Built-in skills with parameters (move, contact, force-hold and similar) | one-shot; poll `primitive_states()` | Standard |
| NRT Cartesian | `NRT_CARTESIAN_MOTION_FORCE` | Target pose and / or wrench; robot interpolates | slow-periodic, **< 1000 ms** latency OK | Standard ⚠️ unverified (manual lists "NRT functions" under Standard) |
| NRT joint | `NRT_JOINT_POSITION`, `NRT_JOINT_IMPEDANCE` | Joint targets; robot interpolates | slow-periodic | Standard ⚠️ unverified |
| RT Cartesian | `RT_CARTESIAN_MOTION_FORCE` | Pose + wrench stream to the unified motion-force controller | **1 kHz**, **< 1 ms** | **Professional** |
| RT joint | `RT_JOINT_POSITION`, `RT_JOINT_IMPEDANCE` | Joint position stream | **1 kHz**, **< 1 ms** | **Professional** |
| RT torque | `RT_JOINT_TORQUE` | Joint torques (gravity, friction, Coriolis compensated by the robot) | **1 kHz**, **< 1 ms** | **Professional** |

- There is **no "EDU" edition**. What you can do is decided by the **RDK licence tier installed on the robot** (Standard vs Professional), purchased through Flexiv sales and installed via Elements.
- State feedback is **1 kHz in every mode**, including NRT.
- In RT modes the robot checks command timeliness at 1 kHz; late commands fault the robot. A real-time Linux kernel is optional but recommended (Ubuntu Pro real-time kernel on 22.04 / 24.04).
- Position modes are much stiffer than impedance modes — for anything touching a person or object, prefer impedance or Cartesian motion-force.
- Rule of thumb: a learned policy at 10–30 Hz fits **NRT Cartesian**; only custom controllers (haptics, admittance, torque-level RL) need RT.

## ROS 2 and middleware

| Your robot | Branch | RDK | Distro |
|---|---|---|---|
| Rizon 4 / 4s / 10 / 10s, AICO 1 / 2 | `humble-v1` or `jazzy-v1` | v1.x | Humble (22.04) / Jazzy (24.04) |
| Enlight-L / LL, MICO Core / Plus / Ultra | `humble` or `jazzy` (default) | v2.x | Humble / Jazzy |

- Packages: `flexiv_bringup`, `flexiv_hardware`, `flexiv_controllers`, `flexiv_gripper`, `flexiv_moveit_config`, `flexiv_msgs`, `flexiv_test_nodes`.
- Driver (v2 branch): `ros2 launch flexiv_bringup flexiv.launch.py robot_sn:=<SN> robot_type:=Enlight-L` · options `rdk_control_mode:=joint_position|joint_impedance`, `load_gripper:=true`, `use_fake_hardware:=true`. The `-v1` branches use different launch file names — read that branch's README.
- MoveIt: `flexiv_moveit.launch.py robot_sn:=<SN>` (also works with fake hardware).
- Grav gripper: `move` (width, velocity, max force) and `grasp` (force) actions.
- Build cost: you must build RDK from source into `~/rdk_install` first, then `colcon build`. Budget **30–45 min** on a fresh machine.
- Limits: fake hardware just mirrors commands to states (no physics); MICO Ultra's mobile base is not in ros2_control; ROS 1 bridge (`flexiv_ros`) is unmaintained since 2024.

## Simulation and digital twins

| Asset / tool | Status | Notes |
|---|---|---|
| URDF + meshes (`flexiv_description`) | ✅ | Docker one-liner viewer: `./scripts/visualize_flexiv.sh robot_type:=Rizon4 gui:=True`. The RDK manual describes the robot description as **kinematics-only** — do not trust inertia for dynamics sims |
| USD assets + Isaac Sim bridge (`isaac_sim_ws`) | ✅ | Isaac Sim **6.x** on the `v2.x` branch (Elements Studio v3E.2); workspace v1.4.0 for Elements Studio v3.11.2; v1.3 for Isaac Sim 4.5 / 5.0. Simulated arm runs the **same force controller** and accepts the same RDK code |
| Elements Studio simulated robot | ✅ | Lightest "digital twin": develop RDK code against it, then point the same script at the real serial number |
| NVIDIA Isaac Lab reference workflow (Rizon 4 + Grav cable insertion) | 🧪 | Announced 2026-09-24 (Isaac Lab + Isaac ROS + FoundationPose + cuMotion). Public repo location not confirmed ⚠️ unverified |
| MJCF (MuJoCo) / Gazebo package | not public | No official asset found; convert the URDF yourself and add your own inertias |

- Isaac bridge gotchas: container must use **host networking**; calibration step needs internet; sample `pick_place` / stacking tasks are marked not working.
- Realistic for 48 h: RViz + fake hardware for motion planning; skip Isaac unless a teammate already has Isaac Sim 6 and Elements Studio installed.

## AI stack

| Item | Status | Detail |
|---|---|---|
| Pretrained policies / VLA from Flexiv | not public | Bring your own model |
| Flexiv Trainer | ✅ | Local web UI (`flexiv-trainer-server` → `http://127.0.0.1:8000/`): record teleop → merge → train → rollout → evaluate |
| Dataset format | ✅ | **LeRobot** layout: `observation.state`, `action`, `observation.images.<name>`; TCP orientation stored as rotation-6D. LeRobot version not stated |
| Cameras | ✅ | Intel RealSense, Orbbec (Gemini 305 / 330); up to **3** cameras single-arm, **5** dual-arm. Orbbec needs Python 3.12 and `pip install --no-deps 'pyorbbecsdk2>=2.1'` + udev rules |
| Policies | ✅ / 🧪 | "B-Spline Diffusion" named (its converter is experimental and cannot yet run through the standard executor); other policy families via plugins |
| Rollout | ✅ | Chunked execution, planner ticks at dataset rate (often **10 Hz**); operator can take over with the leader arm; optional safety envelope (workspace box, force limit) — **off by default** |
| Teleoperation | ✅ | `flexiv_tdk`: robot-to-robot with force feedback, LAN or WAN. Trainer setup = 1 leader + 1 follower Rizon (2 + 2 for dual-arm) |
| Upstream LeRobot robot class | ⚠️ unverified | Not found; Trainer writes the format itself |
| Public datasets with Flexiv arms | ⚠️ unverified | None published by Flexiv in the repos checked |

If only **one arm** is on site, Trainer's teleop path is out. Alternatives: kinesthetic teaching via free drive (record `states()` at 1 kHz), or perception + classical force primitives — usually the quicker win.

## Compute, sensors and connectivity

- **Compute:** the control box runs the controller and RDK server. Your code and any GPU inference run on **your own laptop / PC** over Ethernet. No user-accessible on-board GPU ⚠️ unverified.
- **Built-in sensing:** joint torque sensing in all 7 joints; `s` models add a wrist F/T sensor. TCP wrench, joint torques, poses available at 1 kHz. **No built-in camera** — bring a RealSense or similar.
- **Robot address by serial number**, not IP: e.g. `Rizon4-123456` or `Enlight-L-123456` (no spaces). It is printed on the robot / shown in Elements.

| Control box port | Robot IP | Laptop setting |
|---|---|---|
| User Port 1 | **192.168.2.100** (static) | Static `192.168.2.x`, mask `255.255.255.0`, no gateway |
| User Port 2 | DHCP client | Put robot and laptop on the same router |
| General Port | **192.168.100.1** (robot is DHCP server) | Automatic (DHCP) |

- Direct cable: laptop **MTU must be 1500** (`ip link show <if>`).
- Firewall: disable or whitelist your program, otherwise discovery fails.
- RT control: wired only, ping **< 1 ms**, > 5 MiB/s. NRT: wired or wireless, < 1000 ms, > 1 MiB/s.

## First 60 minutes checklist

1. **Ask the booth (5 min):** arm model and serial number · robot software version (v3.11.x → RDK 1.9.x; v3E.x → RDK 2.x) · licence tier (Standard or Professional) · is "Remote Mode = Ethernet" already enabled · which gripper · where the E-stop is.
2. **Install (5 min):** `python3.12 -m pip install numpy spdlog flexivrdk==<matching version>`. Plain `pip install flexivrdk` gives **2.1.0**, which will refuse a Rizon. Clone the matching tag of `flexiv_rdk` for the examples.
3. **Cable up (5 min):** Ethernet to **General Port** (laptop on DHCP) or User Port 1 (static 192.168.2.x). Check MTU 1500, firewall off, `ping 192.168.100.1` (or `192.168.2.100`).
4. **Remote mode (5 min):** Auto/Manual slide switch on the motion bar **up (Auto)**; in Elements choose **AUTO (REMOTE)**. If Remote Mode was only just enabled in Settings, the robot needs a power cycle.
5. **Read-only test (5 min):** `python3.12 basics1_display_robot_states.py <robot-sn>` — confirms discovery, version match and licence. Push the arm gently and watch the wrench values change.
6. **Hello-world motion (15 min):** clear faults → enable → wait until operational → switch to primitive mode → run a home primitive → stop. Sketch (v1.x-style names; confirm against the examples of your installed version ⚠️):
   ```python
   import time, flexivrdk
   robot = flexivrdk.Robot("Rizon4-123456")
   if robot.fault(): robot.ClearFault()
   robot.Enable()
   while not robot.operational(): time.sleep(1)
   robot.SwitchMode(flexivrdk.Mode.NRT_PRIMITIVE_EXECUTION)
   robot.ExecutePrimitive("Home", dict())
   # poll robot.primitive_states() until the target is reached, then:
   robot.Stop()
   ```
7. **Read sensors (5 min):** `robot.states()` → joint positions, TCP pose, external TCP wrench (field names differ between v1.x and v2.x; in v2.x `states()` returns a map per joint group with `tcp_wrench`).
8. **Gripper (5 min):** run the gripper example; expect the jaws to open and close on initialisation — keep fingers and objects clear.
9. **First contact skill (10 min):** run the primitive-execution and Cartesian motion-force examples (move until contact, hold a few newtons). This is the building block for massage, insertion, wiping and handover demos.
10. **Decide:** stay on RDK Python (recommended) or invest ~45 min in the ROS 2 build if you need MoveIt collision-aware planning.

## Known gotchas and safety

- **Version lock:** RDK checks robot software at connect and errors on mismatch. Pin the pip version; do not upgrade robot firmware at a hackathon.
- **Licence wall:** with a Standard licence, RT streaming and dynamics calls fail. Find out before designing a torque-level controller.
- **Elements vs RDK is exclusive:** in Remote mode Elements cannot jog, run projects or free-drive. Use the RDK free-drive call, or flip the switch down to Manual (then re-enter Auto (Remote) via the prompt).
- **Toggling the Auto/Manual switch drops RDK control** until you re-select AUTO (REMOTE) in Elements.
- **E-stop:** after releasing it and re-enabling, brakes take several seconds to release — check `operational()` before commanding, and `fault()` before enabling.
- **Critical faults** (torque, velocity, position, TCP-force, power limit) cut drive power and engage brakes; `ClearFault()` takes about **30 s** (hot reset; older units need a power cycle). **Minor faults** clear in < 3 s.
- **Joint-limit violation** puts the robot in a recovery state: move the joint back with Elements; `ClearFault()` alone will not help.
- **Connection loss:** the robot stops automatically; RDK supports hot reconnection.
- **Real-time scheduler** (`Scheduler`) needs root or `rtprio 99` in `/etc/security/limits.conf`; TDK and Trainer teleop need the same.
- **Windows:** C++ examples exit silently if the install `bin` folder is not on `PATH`.
- **Human contact (T04 demos):** the arm can output **150–350 N** at the TCP depending on model. Use impedance / low force limits, low speed, a soft end-effector, keep the head and neck out of the workspace, one person on the E-stop. Trainer's safety envelope is off until you set it. Follow the vendor's safety briefing — it overrides anything here.

## Community resources

- [RDK manual v2.x](https://www.flexiv.com/software/rdk/manual/v2.x/index.html) (Enlight / MICO) and [v1.x](https://www.flexiv.com/software/rdk/manual/v1.x/index.html) (Rizon / AICO): setup, control modes, error handling, FAQ.
- [flexiv_rdk examples](https://github.com/flexivrobotics/flexiv_rdk) — `basics*` and `intermediate*` series in C++ and Python; GitHub Issues is the public support channel.
- [flexivrobotics GitHub org](https://github.com/flexivrobotics) — 27 repos, most updated within the last month.
- Primitive reference: shipped with Elements / robot documentation; the public `primitives` repo dates from 2022 and may be outdated.
- Public forum / Discord: none found. On site, the Flexiv engineers at the booth are the fastest resource.

## Sources

- [GitHub — flexiv_rdk README](https://github.com/flexivrobotics/flexiv_rdk)
- [GitHub — flexivrobotics organisation repositories](https://github.com/orgs/flexivrobotics/repositories?type=all)
- [GitHub — flexiv_ros2 README](https://github.com/flexivrobotics/flexiv_ros2)
- [GitHub — flexiv_description README](https://github.com/flexivrobotics/flexiv_description)
- [GitHub — isaac_sim_ws README](https://github.com/flexivrobotics/isaac_sim_ws)
- [GitHub — flexiv_tdk README](https://github.com/flexivrobotics/flexiv_tdk)
- [GitHub — flexiv_trainer README](https://github.com/flexivrobotics/flexiv_trainer)
- [Flexiv RDK manual v2.x — index](https://www.flexiv.com/software/rdk/manual/v2.x/index.html)
- [Flexiv RDK manual v2.x — Control Modes](https://www.flexiv.com/software/rdk/manual/v2.x/control_modes.html)
- [Flexiv RDK manual v2.x — Activate RDK Server (licence tiers)](https://www.flexiv.com/software/rdk/manual/v2.x/activate_rdk_server.html)
- [Flexiv RDK manual v2.x — Connect User Computer](https://www.flexiv.com/software/rdk/manual/v2.x/connect_user_computer.html)
- [Flexiv RDK manual v2.x — Enter and Exit Remote Mode](https://www.flexiv.com/software/rdk/manual/v2.x/enter_and_exit_remote_mode.html)
- [Flexiv RDK manual v2.x — System Requirements](https://www.flexiv.com/software/rdk/manual/v2.x/system_requirements.html)
- [Flexiv RDK manual v2.x — Key Features](https://www.flexiv.com/software/rdk/manual/v2.x/key_features.html)
- [Flexiv RDK manual v2.x — Error Handling](https://www.flexiv.com/software/rdk/manual/v2.x/error_handling.html)
- [Flexiv RDK manual v2.x — FAQ](https://www.flexiv.com/software/rdk/manual/v2.x/faq.html)
- [Flexiv RDK manual v2.x — Robot Software Compatibility](https://www.flexiv.com/software/rdk/manual/v2.x/robot_software_compatibility.html)
- [Flexiv RDK manual v1.x — Robot Software Compatibility](https://www.flexiv.com/software/rdk/manual/v1.x/robot_software_compatibility.html)
- [PyPI — flexivrdk release history](https://pypi.org/project/flexivrdk/)
- [Robotics 24/7 — Flexiv Rizon 4 now supported in NVIDIA Isaac (2026-09-24)](https://www.robotics247.com/article/flexix-rizon-4-adaptive-robot-now-supported-in-nvidia-isaac/Flexiv_Robotics)
