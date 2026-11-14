---
type: dev-guide
company: "Unitree Robotics"
slug: Unitree
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Unitree Robotics — Developer Guide (hackathon edition)

⬆ [Unitree Robotics profile](Unitree.md) · [Product portfolio](Unitree-Products.md) · [Roadmap and strategy](Unitree-Roadmap-and-Strategy.md)

> Research note: the official docs portal (support.unitree.com) is a JavaScript app that could not be read in this run, and web search was unavailable. Everything below comes from the official GitHub READMEs and Hugging Face org unless marked ⚠️ unverified (= from prior knowledge of the official docs, confirm at the booth).

## TL;DR — how you program it

- **One SDK for everything:** `unitree_sdk2` (C++) or `unitree_sdk2_python`. Both speak **CycloneDDS 0.10.2** over **Ethernet** on the robot's `192.168.123.x` network. Examples exist for Go2, Go2-W, B2, B2-W, A2, As2, G1, H1, H1-2, H2 and R1.
- **Two levels:** high-level clients (walk at a velocity, stand, sit, obstacle avoidance) work in minutes; low-level joint control (`LowCmd` position / velocity / torque + gains) requires switching off the factory controller and is where robots fall. **For 48 hours: stay high-level for legs, spend your time on perception, arms and task logic.**
- **ROS 2 is native, not a bridge:** `unitree_ros2` exposes the same DDS topics as ROS 2 topics (**Humble on Ubuntu 22.04 recommended**).
- **Check the variant first:** only **EDU** models (and partly Go2 X / As2 X) are open to the SDK. Go2 Air / Pro and the base G1 / R1 are not meant for secondary development.
- **Fastest path to a manipulation demo on G1:** `xr_teleoperate` (XR headset teleop + recording) → `unitree_lerobot` (convert, train ACT / Diffusion / Pi0 / Pi05 / GR00T) → `eval_g1.py`. Simulate the same pipeline in `unitree_sim_isaaclab`.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| unitree_sdk2 | C++ | All current robots; example folders: `go2`, `go2w`, `b2`, `b2w`, `a2`, `as2`, `g1`, `h1`, `h2`, `r1`, `wireless_controller`, `state_machine` | [GitHub](https://github.com/unitreerobotics/unitree_sdk2) | BSD-3. Pre-built for **Ubuntu 20.04, x86_64 + aarch64, GCC 9.4**. Install to `/opt/unitree_robotics` (other repos expect it there) |
| unitree_sdk2_python | Python ≥ 3.8 | Same API as C++; examples: `go2`, `go2w`, `b2`, `b2w`, `a2`, `as2`, `g1`, `h1`, `h1_2`, `h2`, `r1`, `motionSwitcher`, `obstacles_avoid`, `vui_client`, `wireless_controller` | [GitHub](https://github.com/unitreerobotics/unitree_sdk2_python) | `pip3 install -e .`; needs `cyclonedds==0.10.2`. Quickest for a hackathon |
| unitree_ros2 | C++ / ROS 2 | Go2, B2, H1 (examples also for G1, H1-2): state, sport requests, low-level commands, LiDAR cloud | [GitHub](https://github.com/unitreerobotics/unitree_ros2) | Foxy (20.04) or **Humble (22.04, recommended)** |
| unitree_ros | C++ / ROS 1 | URDF files and Gazebo-era simulation packages for all robots | [GitHub](https://github.com/unitreerobotics/unitree_ros) | BSD-3. Mainly useful as the **URDF source** |
| xr_teleoperate | Python 3.10 | Teleoperation of G1 (23 / 29 DoF), H1, H1-2, H2, R1 arms + Dex1-1, Dex3-1, Inspire, BrainCo hands from Apple Vision Pro, PICO 4 Ultra Enterprise, Meta Quest 3 | [GitHub](https://github.com/unitreerobotics/xr_teleoperate) | Formerly `avp_teleoperate`. Records imitation-learning episodes |
| teleimager | Python | Multi-camera image server (ZeroMQ / WebRTC) used by teleop and sim | [GitHub](https://github.com/unitreerobotics/teleimager) | Runs on the robot's development computer |
| unitree_lerobot | Python 3.10 | LeRobot fork: data conversion, training and real-robot evaluation for G1 (+ Z1 configs) | [GitHub](https://github.com/unitreerobotics/unitree_lerobot) | Policies documented: ACT, Diffusion, Pi0, Pi05, GR00T |
| unitree_robotskills | Python ≥ 3.10 | Agent "skills" (camera → LLM reasoning → bounded SDK2 motion tools) for **G1-D** and **R1-D** | [GitHub](https://github.com/unitreerobotics/unitree_robotskills) | Apache-2.0. Navigation skill uses MCP. Read its `docs/safety.md` first |
| D2-Arm · r1-7a_sdk · R1-7A | Python / C++ | D2 arm materials; R1-7a arm low-level SDK; single / dual-arm teleop with recording | [GitHub org](https://github.com/unitreerobotics) | New in Nov 2026, few users yet |
| unilidar_sdk2 · point_lio_unilidar | C++ | 4D LiDAR L2 driver; Point-LIO odometry / mapping for Unitree LiDARs | [GitHub org](https://github.com/unitreerobotics) | Use for SLAM on a stand-alone L1 / L2 |
| unitree_actuator_sdk · Unitree-Motor-Assistant | C++ / Qt | Stand-alone joint motors (GO-M8010-6 etc.) | [GitHub org](https://github.com/unitreerobotics) | Only if you build your own mechanism |
| z1_sdk / z1_controller / z1_ros | C++ / Python | Z1 arm | not confirmed in this run | ⚠️ unverified — older line, check repo activity before committing |

## Control levels

| Level | What you send | Typical rate | Robots / editions | Use it when |
|---|---|---|---|---|
| **High-level (sport / loco service)** | Requests to the on-board motion service via a client class (Go2 `SportClient`, G1 loco client): velocity move, stand up / down, balance stand, attitude, trajectory follow, special motions; plus obstacle-avoidance switch, volume / light (`vui_client`), front camera | Request / response; velocity commands a few tens of Hz ⚠️ unverified | Go2 EDU (X: partial), As2 X / EDU, A2, B2, G1 EDU, R1 EDU, H1 / H2 | Always start here. Legs stay under the factory controller |
| **Upper-body overlay (humanoids)** | Arm joint targets on topic `rt/arm_sdk` while the factory controller keeps balance and walks | Teleop loop default **30 Hz** in `xr_teleoperate` | G1 EDU, H1-2, H2, R1 EDU | Manipulation while standing or walking ("motion mode"; only **Regular mode, R1+X**, is supported, not Running mode R2+A) |
| **Low-level (joint)** | `LowCmd` per motor: target q, dq, feed-forward torque, kp, kd; motor mode `0x01` = FOC, `0x00` = stop. Read `LowState` (motors, IMU, BMS) | Examples run around **500 Hz** ⚠️ unverified (D2 arm page states 500 Hz) | EDU editions only | Custom RL policies or whole-body control. You must first release the built-in motion service (app or `motionSwitcher` example); on G1 enter **debug mode with L2+R2** while the robot hangs in zero-torque mode |

Key consequences:

- With the motion service off, **`sportmodestate` is no longer published** on the real robot — your policy needs its own state estimation.
- Low-level and high-level commands **conflict** if both are active; the SDK README tells you to disable sport mode first.
- Message families differ: **`unitree_go` IDL** for Go2, Go2-W, B2, B2-W, H1; **`unitree_hg` IDL** for G1, H1-2, As2 (and other newer humanoids). Code copied from a Go2 example will not run on a G1 unchanged.

## ROS 2 and middleware

- **Middleware:** CycloneDDS **0.10.2**. Real robots use **DDS domain 0**; Unitree simulators use **domain 1** on loopback so both can coexist.
- **ROS 2 setup:** clone `unitree_ros2`, build its `cyclonedds_ws` (Humble users can skip compiling CycloneDDS itself), put your interface name into `setup.sh`, then `source ~/unitree_ros2/setup.sh`. `setup_local.sh` = loopback for simulation.
- **Topics you will use** (ROS 2 names; DDS names carry an `rt/` prefix):

| Topic | Content |
|---|---|
| `/sportmodestate` (`/lf/sportmodestate` = low-frequency copy) | Position, velocity, gait, foot data |
| `/lowstate` (`/lf/lowstate`) | Motor states, IMU, battery, power |
| `/lowcmd` | Low-level motor commands |
| `/api/sport/request` | High-level sport requests (`unitree_api::msg::Request`) |
| `/wirelesscontroller` | Remote joystick and keys |
| `/utlidar/cloud` | Go2 LiDAR point cloud (frame `utlidar_lidar`) |

- **No official Nav2 / SLAM bring-up package** was found in the repos read. Plan to wire `utlidar/cloud` + odometry into your own stack (Point-LIO is published for Unitree LiDARs), or use the robot's built-in obstacle avoidance and keep navigation simple.

## Simulation and digital twins

| Asset / repo | Engine | Robots | Notes |
|---|---|---|---|
| [unitree_mujoco](https://github.com/unitreerobotics/unitree_mujoco) | MuJoCo (C++ and Python simulators) | go2, go2w, b2, b2w, h1, g1, h2, as2 | Publishes the **same `LowCmd` / `LowState` DDS topics** as the robot → identical code in sim and real (switch domain 1 / `lo` to domain 0 / your NIC). **Low-level only** — the high-level sport service is not simulated. Python: `pip3 install mujoco pygame`, `python3 ./unitree_mujoco.py` |
| [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) | Isaac Sim **6.2.0** / Isaac Lab **3.0.0** (branch for 4.5–5.1) | G1 29-DoF (Dex1, Dex3, Inspire), H1-2, **G1-D**, **R1-D** | Pick-place, stacking, drawer and whole-body "move cylinder" tasks. Same DDS + image-server interface as the real robot, so `xr_teleoperate` connects directly. Replay and augment recorded data (lighting / camera changes) |
| [unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab) | Isaac Lab 2.3.0 / Isaac Sim 5.1.0 | Go2, H1, G1 29-DoF | RL training (`./unitree_rl_lab.sh -t --task Unitree-G1-29dof-Velocity`), MuJoCo sim2sim, then `./g1_ctrl --network <nic>` on the robot |
| [unitree_rl_mjlab](https://github.com/unitreerobotics/unitree_rl_mjlab) | mjlab (MuJoCo, GPU) | Go2, A2, As2, G1 (23 / 29 DoF), R1, H1-2, H2 | Velocity and **motion-imitation** tasks; exports `policy.onnx`; documented G1 deploy path |
| unitree_rl_gym | Isaac Gym (legacy) | Go2, H1, G1 | 3.7k stars but last updated Jul 2025; prefer rl_lab / rl_mjlab |
| unitree_ros (URDF) · unitree_model (USD, Hugging Face) | — | Whole range | URDF recommended for Isaac Sim ≥ 5.0; USD via the `unitree_model` dataset |

Hackathon advice: a 48-hour event is too short to train and safely deploy a new locomotion policy. Use simulation to **test task logic and teleop pipelines**, not to replace the factory gait.

## AI stack

| Layer | What exists | Status | Notes |
|---|---|---|---|
| Locomotion policies | Factory controllers on every robot; RL training repos above | ✅ | Factory gait already handles stairs and slopes |
| Teleoperation | `xr_teleoperate` (Vision Pro, PICO 4 Ultra Enterprise, Quest 3; hand tracking or controllers) | ✅ | Example: `python teleop_hand_and_arm.py --input-mode=hand --arm=G1_29 --ee=dex3 --record` (`--sim` for Isaac Lab). Keys: `r` start, `s` start / stop episode, `q` quit |
| Data pipeline | `unitree_lerobot`: edit / sort episodes → `convert_unitree_json_to_lerobot.py` → train → `eval_g1.py` (real), `eval_g1_sim.py` (sim), `replay_robot.py` | ✅ | Robot types: `Unitree_G1_Dex1`, `_Dex3`, `_Brainco`, `_Inspire`, `_Dex1_Sim`, Z1 single / dual. README is inconsistent about LeRobot dataset v2 vs v3 — check before converting |
| Policies trainable out of the box | **ACT, Diffusion, Pi0, Pi05, GR00T** (via `unitree_lerobot`) | ✅ | Pi0-family needs gated `paligemma` access on Hugging Face |
| UnifoLM-WMA-0 | World-model-action model (Base, Dual checkpoints) | ✅ open | Repo `unifolm-world-model-action`; non-commercial licence (see profile) |
| UnifoLM-VLA | VLA for humanoid manipulation (`UnifoLM-VLA-Base`, `-Libero`, `UnifoLM-VLM-Base` 8B) | ✅ open | Repo `unifolm-vla`; reported as one policy covering 12 G1 manipulation categories |
| **UnifoLM-WLA-1.0** | Newest foundation model: **6B parameters**, ~**2,500 h** real-robot data, **64 tasks** (table-top + whole-body); `UnifoLM-ER-1` / `-ER-Flow` (4B) reasoning modules | ✅ open, **Apache-2.0** (weights 11–28 Sep 2026) | Repo `unifolm-wla`; grippers and five-finger hands; GPU requirements not stated on the README |
| Datasets | **246 datasets** on Hugging Face: `G1_Dex1_*`, `G1_Dex3_*`, `G1_Brainco_*` table-top tasks (≈100–400 episodes each) and `G1_WBT_SMPL_*` whole-body teleop | ✅ | LeRobot format; good for fine-tuning without collecting from zero |
| LLM agents | `unitree_robotskills`: observe → reason → act → verify loop with skills as folders (`SKILL.md` + tools); MCP for navigation | ✅ (G1-D / R1-D only) | Pattern is portable to Go2 / G1 by writing your own bounded tools on SDK2 |
| NVIDIA GR00T | H2 Plus reference humanoid; **G1 reference workflow** announced for GitHub / Hugging Face | 🧪 (announced 1 Jun 2026; release status not checked) | Use GR00T fine-tuning through `unitree_lerobot` today |
| Upstream LeRobot G1 support | Native Unitree G1 robot class in Hugging Face LeRobot | ⚠️ unverified | Check the LeRobot docs if you prefer upstream over the Unitree fork |

Realistic 48-hour ML scope: **20–50 teleop demos of one short task → ACT fine-tune → on-robot eval**. Bring or borrow a GPU laptop (the Orin module is for inference, not training).

## Compute, sensors and connectivity

| Item | Detail |
|---|---|
| Robot network | Internal Ethernet subnet **`192.168.123.0/24`** |
| Your laptop | Static IPv4 on the wired NIC, e.g. **`192.168.123.99`** (ROS 2 README) or `.222` (rl_mjlab README), netmask `255.255.255.0`, no gateway |
| G1 development computer ("PC2") | **`192.168.123.164`** — runs teleimager; WebRTC preview at `https://192.168.123.164:60001` |
| Other fixed addresses | G1 locomotion computer `.161`, Go2 EDU expansion dock `.18`, G1 LiDAR `.120` — ⚠️ unverified, avoid these addresses for your laptop |
| Interface argument | Every example takes your NIC name (`python3 example/high_level/read_highstate.py enp2s0`); find it with `ifconfig` / `ip a` |
| On-board compute | Platform controller (closed) + user computer: Orin-class module on Go2 / R1 / G1 EDU (40–100 TOPS options), Intel i7 on A2 / B2 / H2, Jetson Thor option on H2-X (see profile) |
| Sensors via SDK | Go2: L2 4D LiDAR cloud, front camera, IMU, foot force. G1: depth camera + 3D LiDAR, IMU; G1+ / R1 / H2: stereo cameras. Hands: joint state, optional tactile arrays |
| Laptop OS | **Ubuntu 22.04 x86_64** is the safe choice (20.04 for the pre-built C++ SDK). macOS / Windows: use a VM or Docker with a bridged wired NIC, or SSH into the on-board computer — native support ⚠️ unverified |
| Wi-Fi / app | Consumer control goes through the Unitree app and remote; SDK traffic is expected over Ethernet. Running your code on the on-board computer avoids a tether |

## First 60 minutes checklist

1. **Ask the booth (5 min):** exact model and edition (EDU?), firmware version, whether the Orin / dev PC is fitted and its login, which hands, number of batteries, where the remote and e-stop are.
2. **Laptop prep (10 min):** Ubuntu 22.04; `git clone https://github.com/unitreerobotics/unitree_sdk2_python && cd unitree_sdk2_python && pip3 install -e .` If it fails with "Could not locate cyclonedds", build CycloneDDS `releases/0.10.x`, `export CYCLONEDDS_HOME=~/cyclonedds/install`, retry.
3. **No robot yet? (parallel):** `pip3 install mujoco pygame`, run `unitree_mujoco/simulate_python/unitree_mujoco.py` and its `test/test_unitree_sdk2.py`; set `USE_JOYSTICK = 0` if no gamepad.
4. **Cable up:** Ethernet from laptop to the robot's port; set static IP `192.168.123.99/24`; `ping 192.168.123.164` (G1 PC2) or the address the booth gives you.
5. **Verify DDS (read-only):** `python3 example/high_level/read_highstate.py <nic>` (Go2) — you should see position / velocity streaming. On ROS 2: `source ~/unitree_ros2/setup.sh && ros2 topic list && ros2 topic echo /sportmodestate`.
6. **Clear 2 m around the robot; one person holds the remote.**
7. **Hello-world motion (Go2):** open `example/high_level/sportmode_test.py`, enable only `StandUpDown()`, run it with `<nic>`; then try `VelocityMove()` at low speed.
8. **Hello-world motion (G1):** start with the remote (stand, Regular mode R1+X), then run a `g1` high-level example from the SDK; arms: use the `rt/arm_sdk`-based examples or `xr_teleoperate` with `--sim` first.
9. **Read sensors:** `example/front_camera/camera_opencv.py <nic>` (needs a display, ESC to quit); LiDAR: `ros2 topic echo /utlidar/cloud --once` or view in RViz.
10. **Move your code on board:** SSH to the development computer, clone your repo there, confirm the same script runs untethered.
11. **Decide scope:** if steps 5–9 worked in under an hour, build on high-level control + perception. Do not open low-level control unless your idea truly needs it.

## Known gotchas and safety

| Gotcha | What to do |
|---|---|
| **Edition lock** | Air / Pro Go2 and base G1 / R1 are not SDK platforms. Confirm EDU before you design around the SDK |
| **CycloneDDS version** | Must be 0.10.x. Do not source ROS 2 in the shell where you compile CycloneDDS; Humble users skip that build |
| **Wrong NIC** | No data usually means the wrong interface name in `setup.sh` or the example argument, or a firewall / VPN on the laptop |
| **Sim and real on one network** | Simulators use DDS domain 1, robots domain 0 — keep them apart; `unitree_sim_isaaclab` warns about collisions if a real robot shares the network |
| **Go vs HG messages** | Go2 code does not run on G1 / As2 without switching IDL (`unitree_go` → `unitree_hg`) |
| **Low-level control** | Release the motion service first; G1: hang the robot, zero-torque → **L2+R2** debug mode; close the on-board control program before running `g1_ctrl`. Test in MuJoCo with `--network=lo` before the real robot |
| **Teleop exit** | In `xr_teleoperate`, bring arms near the start pose before quitting; both joysticks pressed = soft e-stop (damping). `--motion` cannot be combined with `--ee dex1_internal` |
| **Examples that change settings** | Obstacle-avoidance and VUI examples toggle avoidance, volume and lights — reset afterwards for the next team |
| **Humanoid falls** | Use a gantry / tether when testing new code on G1 / H1 / H2; damping mode drops the robot gently but it still goes down. Keep bystanders (and any elderly test users) out of reach |
| **E-stop** | Remote-based stop / damping mode is the standard; the H2 Plus release mentions an on-remote emergency stop. A separate wireless hard e-stop is not confirmed — ask the booth ⚠️ unverified |
| **Security** | Researchers published a wormable Bluetooth exploit (Sept 2025; Go2, B2, G1, H1) and reported undisclosed telemetry on the G1. Use the wired link, keep robots off open venue Wi-Fi, and do not store personal data on them |
| **Battery** | Go2 1–2 h (EDU long-life 2–4 h), G1 ~2 h, R1 ~1 h — plan demo runs and charging rotation |
| **Model licences** | UnifoLM-WMA-0 is non-commercial; UnifoLM-WLA-1.0 and `unitree_robotskills` are Apache-2.0; SDKs are BSD-3 |

## Community resources

- **Official GitHub org** — 59 repositories; most active in Nov 2026: `unitree_ros`, `unitree_sdk2`, `teleimager`, `unitree_sim_isaaclab`. [github.com/unitreerobotics](https://github.com/unitreerobotics)
- **Hugging Face org** — 8 models, 246 datasets, robot USD models. [huggingface.co/unitreerobotics](https://huggingface.co/unitreerobotics)
- **Docs portal** — [support.unitree.com/home/en/developer](https://support.unitree.com/home/en/developer) (open in a real browser; per-robot quick start, network setup, service API tables).
- **Open-source index and platforms** — [unitree.com/opensource](https://www.unitree.com/opensource); it also links UnifoLM (unifolm.com), UniStore, UniUni and UniPlatform (contents not checked).
- **Learning material** — `unitree_guide` (quadruped control textbook code), `Qmini` (open-source small biped), `kinect_teleoperate` (camera-based humanoid teleop), all in the official org.
- **Community projects for non-EDU Go2** (WebRTC-based ROS 2 drivers such as `go2_ros2_sdk`) exist but are unofficial and firmware-dependent — ⚠️ unverified, not checked in this run.
- **GitHub issues** on `xr_teleoperate`, `unitree_sdk2` and `unitree_ros` are the de-facto forum; search there before debugging alone.

## Sources

- [Unitree profile in this repo (specs, editions, licences)](Unitree.md)
- [Unitree GitHub organisation](https://github.com/unitreerobotics)
- [Unitree GitHub — repositories sorted by stars](https://github.com/orgs/unitreerobotics/repositories?type=all&q=&sort=stargazers)
- [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) · [examples folder](https://github.com/unitreerobotics/unitree_sdk2/tree/main/example)
- [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) · [examples folder](https://github.com/unitreerobotics/unitree_sdk2_python/tree/master/example)
- [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
- [unitree_mujoco](https://github.com/unitreerobotics/unitree_mujoco)
- [unitree_rl_lab](https://github.com/unitreerobotics/unitree_rl_lab)
- [unitree_rl_mjlab](https://github.com/unitreerobotics/unitree_rl_mjlab)
- [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)
- [xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate)
- [unitree_lerobot](https://github.com/unitreerobotics/unitree_lerobot)
- [unifolm-wla](https://github.com/unitreerobotics/unifolm-wla)
- [unitree_robotskills](https://github.com/unitreerobotics/unitree_robotskills)
- [Unitree on Hugging Face](https://huggingface.co/unitreerobotics)
- [Unitree official open-source page](https://www.unitree.com/opensource)
- [PR Newswire — Unitree H2 Plus / NVIDIA Isaac GR00T reference humanoid (1 Jun 2026)](https://tools.prnewswire.com/en-us/live/20823/release/20260601EN72140)
- [Notebookcheck — Unitree household / elder-care plans, UnifoLM-VLA-0](https://www.notebookcheck.net/Beyond-kung-fu-Unitree-plans-humanoid-robot-for-household-chores-and-elder-care-by-2030.1255707.0.html)
- [Wikipedia — Unitree Robotics (security findings)](https://en.wikipedia.org/wiki/Unitree_Robotics)
