---
type: dev-guide
company: "Galbot"
slug: Galbot
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Galbot — Developer Guide (hackathon edition)

⬆ [Galbot profile](Galbot.md) · [Product portfolio](Galbot-Products.md) · [Roadmap and strategy](Galbot-Roadmap-and-Strategy.md)

Scope: this guide is about the **G1** (the robot most likely on site). S1 uses the same SDK with its own docs folder. **ET1 has no public SDK or docs** (not in the SDK model list) — ask the booth.

## TL;DR — how you program it

- **One official SDK: GalbotSDK** (C++ and Python, Apache-2.0, **V1.10.0, 2026-09-22**). `from galbot_sdk.g1 import GalbotRobot`, call `init()`, then blocking or streaming commands. No ROS needed.
- **Two ways to run code:** on the robot's Orin over SSH (lowest friction, works over Wi-Fi) or from an Ubuntu laptop over a **wired link through Galbot's Ethernet adapter board** (PC `192.168.1.99`, HPU `192.168.1.88`, XCU `192.168.1.66`).
- **SDK and robot firmware must match:** SDK 1.10.x needs robot system **GBS 1.18.x**. Check with `galbot_sdk check-version` before anything else.
- **Navigation only works after you build a map** of the venue (push the robot around by hand, via a web tool on the robot). A robot without a map can sit in `ABNORMAL` mode and refuse all commands.
- **Bring your own model:** the SDK has a documented pattern for VLA / RL policies — synchronized camera + joint observation in, **23-D joint action chunks out at 20 Hz** (tutorial example 5). Data collection uses the TM01 leader arms and converts to **LeRobot** format.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| **GalbotSDK** ✅ | C++, Python 3.8–3.14 | G1, S1 (and "G3"): joints, end-effectors, base, sensors, audio, planning, navigation, perception | [GitHub](https://github.com/GalaxyGeneralRobotics/GalbotSDK) | Apache-2.0. Ubuntu 20.04–24.04 (22.04 recommended), x86_64 PC / aarch64 robot. Docs ship inside the repo: `cd docs && python3 -m http.server 8000`, open `/g1/en/` |
| GalbotSDK Docker image ✅ | — | Same as above, containerised | `docker pull galbot/galbot_sdk:1.10.0`, then `docker/run.sh` | Useful if your laptop is not Ubuntu 20–24. Still needs the wired network setup |
| `galbot_one_golf_description` ✅ | ROS 2 (colcon), xacro | G1 model only: URDF, MJCF, USD | [GitHub](https://github.com/GalaxyGeneralRobotics/galbot_one_golf_description) | "Galbot One Golf" is the G1's internal name (the robot's own config uses `galbot_one_golf.urdf`). Apache-2.0 |
| `galbot_s1_description` ✅ | — | S1 model: URDF, MJCF, USD | [GitHub](https://github.com/GalaxyGeneralRobotics/galbot_s1_description) | Apache-2.0 |
| `galbot-mcap2lerobot` ✅ | Python | Converts G1 MCAP recordings to LeRobot v2.1 datasets | [GitHub](https://github.com/GalaxyGeneralRobotics/galbot-mcap2lerobot) | MIT. 23-D state/action, 4 cameras at 30 FPS |
| GraspVLA ✅ | Python | Open-vocabulary grasp policy (model server) | [GitHub](https://github.com/PKU-EPIC/GraspVLA) | Research release; G1 adapter not public (see AI stack) |
| Developer platform ✅ | Web | Docs, AI doc assistant; paid: online sim, one-click deploy | [developer.galbot.com](https://developer.galbot.com/?lang=en) | Free tier covers SDK, docs, digital models, 5 assistant queries/day |

SDK modules, as organised in the examples: `galbot_robot` (state, joints, grippers, base, sensors, audio, e-stop), `galbot_motion` (IK/FK, Jacobian, collision checking, motion planning, obstacles, tool attach), `galbot_navigation` (goals, waypoints, relocalisation), `galbot_perception` (stereo depth example), plus six end-to-end `tutorials`.

## Control levels

| Level | What you get | Key calls (Python names) | Rate / limits |
|---|---|---|---|
| **High-level** | Whole-body motion planning with self and environment collision checks, straight-line moves, multi-waypoint plans; autonomous navigation with dynamic obstacle avoidance | `motion_plan`, `move_line`, `motion_plan_multi_waypoints`, `combine_plan`; `navigate_to_goal`, `navigate_through_waypoints`, `set_navigation_target` | Blocking or non-blocking calls. Navigation needs an applied map |
| **Mid-level** | Joint-space position and trajectory control, Cartesian end-effector pose control, gripper / suction cup / dexterous-hand commands, torso height | `set_joint_positions`, `execute_joint_trajectory`, `set_end_effector_commands`, `set_gripper_command`, `set_suction_cup_command`, `set_leg_height` | `set_joint_positions(pos, groups, joints, is_blocking, max_speed, timeout_s)` returns a `ControlStatus` |
| **Low-level / real-time** | Streaming joint or end-effector commands for your own closed loop (VLA, RL); open-loop base velocity | `set_joint_commands`, `set_joint_commands_batch`, `set_end_effector_command`, `set_base_velocity`, `navigate_with_velocity` | Tutorial example streams at **20 Hz**, chunks of 30 actions. Maximum supported rate: not stated in the docs |
| **Business modules** | Packaged SPS sorting and bin-handling flows | — | **Locked: require unlocking through Galbot sales.** Ask the booth if they are enabled |

- **Torque / current control:** not described in the SDK overview (it lists position, trajectory, Cartesian pose and base velocity). Treat as unavailable ⚠️ unverified.
- **Real-time end-effector commands** need `using_wbc = true` in the robot config on the XCU plus a launcher restart — a booth-engineer job, not yours.
- **Editions:** there is no separate "EDU" hardware edition in public material. What differs is the developer subscription (Free / Pro ¥50,000 / Enterprise ¥200,000 per robot per year), which gates online simulation, one-click deployment and support — not the SDK API itself.
- **G1 joint groups** (order used by the VLA example and datasets): `leg` 5 · `head` 2 · `left_arm` 7 · `left_gripper` 1 · `right_arm` 7 · `right_gripper` 1 = **23 dimensions**.

## ROS 2 and middleware

- **The robot does not run on ROS 2.** GalbotSDK talks to Galbot's own middleware ("embosa", discovery server on the HPU, port 11888), configured through `embosa_ip_config.json`.
- **ROS 2 is used only for robot description:** `galbot_one_golf_description` builds with `colcon` and has an RViz launch (`ros2 launch galbot_one_golf_description display.launch.py`).
- **No official ROS 2 runtime bridge is published.** If you need Nav2, MoveIt or ROS-based tools from another vendor, write a thin Python node that wraps the SDK calls you need (publish joint states and camera images, subscribe to `cmd_vel` → `set_base_velocity`). Budget 2–4 hours.
- Recordings are **MCAP files with protobuf messages** and ROS-style topic names (for example `/front_head_camera/left_color/image_raw`), so Foxglove-type tooling can read them.
- Debug tool on the robot: `/data/galbot/bin/embosa_topic_tool` (topic rates).

## Simulation and digital twins

| Asset | Format | Where | Notes |
|---|---|---|---|
| G1 full model | URDF (wheeled and fixed-base presets), xacro sources | `galbot_one_golf_description/urdf` | Regenerate variants with `scripts/create_description.py`; single components via `xacro/component.xacro` |
| G1 for MuJoCo | MJCF: wheeled base, fixed base, **virtual planar base** (x, y, yaw velocity actuators) | `mjcf/` | The planar-base variant is the quickest way to test mobile manipulation logic |
| G1 for Isaac Sim | USD, entry point `usd/galbot_one_golf.usda` | `usd/` | Gripper collision hulls and fingertip friction (1.5) are authored; includes example scenes |
| S1 model | URDF, MJCF, USD | `galbot_s1_description` | — |
| Scenes and objects | SimReady assets | On request (paid tiers get priority) | Not downloadable publicly |
| Online simulation | Browser | Developer platform, **Pro tier and above** | Not available on the free tier |

- **No official Isaac Lab, Gazebo or MuJoCo task repositories for G1 are public.** You get robot assets, not ready-made environments.
- Gripper TCP: translation `(0.13996, 0, 0)` from the gripper base, identical across xacro / URDF / MJCF / USD.
- The robot's own IK, planner and controller read joint limits from the same `galbot_one_golf.urdf`, so the public model is a faithful reference for limits.

## AI stack

| Item | Status | What it is | Hackathon usability |
|---|---|---|---|
| **GraspVLA** | ✅ open (weights on Hugging Face, model server, sim playground, real-world controller) | Grasping VLA pretrained on the synthetic SynGrasp-1B set (240 categories, 10,000+ objects); zero-shot open-vocabulary grasping | Runs as a **network model server**: about **9 GB GPU memory, ~200 ms** per inference on an L40s-class GPU. You need an external GPU machine. A ready-made G1 client is **not public** ⚠️ unverified — ask whether the booth robot has it preloaded |
| **SynGrasp-1B** | ✅ released 2026-08-19 | Billion-frame synthetic grasp dataset + training framework | Too large to train on in 48 h; useful for reference only |
| SDK VLA pattern (tutorial example 5) | ✅ | `get_synced_observation` (time-aligned image + joint state) → your model → `set_joint_commands` stream | The supported route for any policy you train or bring (ACT, Diffusion Policy, pi-style, your own) |
| **TM01 leader arms** | ✅ product (availability on site unknown) | Leader-follower teleop for whole-body G1 control and data recording: 2 x 7 DoF, ≥100 Hz sampling, ≤20 ms mapping delay, USB | The official demonstration-collection path. Buttons on the handles start, segment, fail-mark and cancel episodes |
| **LeRobot support** | ✅ | `galbot-mcap2lerobot` converts recordings to LeRobot **v2.1** (use LeRobot's own script to go to v3.0) | Match dataset version to LeRobot code: v2.1 ↔ lerobot 0.3.x, v3.0 ↔ 0.4+ |
| Perception service | ✅ | Built-in perception incl. a FoundationStereo depth example (`galbot_perception`) | Needs GBS 1.15.16+ and a config switch on the HPU |
| GroceryVLA, TrackVLA, NavFoM, AstraBrain-WAM / Dex | 🧪 in products / papers | Retail picking, person following, navigation, world-action model | No public weights or API found. Do not plan on them unless the booth provides access |
| Humanoid-GPT (AstraBrain-WBC 0.5), OpenTrack, OpenWBT, LATENT | ✅ open | Humanoid whole-body tracking / teleop research code | Target **bipedal humanoids (Humanoid-GPT: Unitree G1)**, not the wheeled Galbot G1. Relevant if you pair with a Unitree humanoid |
| UrbanVLA | ✅ repo public (ICRA 2026) | VLA for urban micromobility navigation | Research code; not a G1 SDK feature |

Practical recommendation for 48 hours: use the **built-in planner + your own perception** (open-vocabulary detector on the head or wrist camera → grasp pose → `motion_plan` / `move_line`) as the baseline, and treat any learned policy as an upgrade.

## Compute, sensors and connectivity

| Item | Detail |
|---|---|
| Compute architecture | Two ARM64 units. **HPU** ("brain"): NVIDIA Jetson AGX Orin 64 GB (275 TOPS); AGX Thor 128 GB also supported since SDK 1.10.0. **XCU** ("cerebellum"): real-time motor and whole-body control (service name SingoriX) |
| Where services live | HPU: localisation, navigation, planning, perception. XCU: control, chassis, mode management |
| Sensors exposed by the SDK | Head stereo camera, left/right wrist cameras (colour, depth, infrared), LiDAR point cloud, IMU, wrist force/torque (raw or calibrated wrench), ultrasonic, battery (BMS), odometry, microphone stream and speaker |
| Camera data used in datasets | 4 streams at 30 FPS, 480x640: head left, head right, left wrist, right wrist |
| Wired laptop link | Through the **Ethernet adapter board** (RJ45 → robot's dedicated port on the back). Laptop static IP **192.168.1.99/24**; fixed robot IPs **HPU 192.168.1.88**, **XCU 192.168.1.66**. Then run `./configure_embosa_ip.sh` (choose G-series) |
| Wi-Fi | The robot joins Wi-Fi from its screen; read the HPU IP there. The XCU is not on Wi-Fi — reach it by SSH from the HPU |
| SSH | User `galbot` on the HPU. Default passwords (HPU, XCU, mapping web tool) are printed in the SDK docs under Robot-Side Deployment and Troubleshooting; the booth may have changed them |
| Paths on the robot | SDK libs `/data/galbot/lib`; put your code in `/userdata`; service logs `/userdata/log/<service>/`; SDK logs `~/galbot_sdk_log/` |
| Laptop OS | Native Ubuntu, Windows + WSL2 (mirrored networking), VMware (bridged) are documented. **macOS is not** — Mac users should SSH into the HPU and run Python there |

## First 60 minutes checklist

1. **Ask the booth (5 min):** GBS version on the robot, which end-effectors are mounted (factory default config is left gripper + right suction cup), whether a venue map exists, whether an Ethernet adapter board and TM01 are available, and current login details.
2. **Get the SDK (5 min):** `git clone https://github.com/GalaxyGeneralRobotics/GalbotSDK.git`, then serve the docs locally (`cd docs && python3 -m http.server 8000`, open `http://localhost:8000/g1/en/`).
3. **Pick a run mode (10 min):**
   - Fastest: robot-side. `./deploy_to_robot.sh` (asks for HPU user, IP, password), then `scp your_app.py galbot@<robot-ip>:/userdata` and run it over SSH.
   - Laptop-side: wire up, set `192.168.1.99/24`, `./configure_embosa_ip.sh`, `./install.sh`, `./install_python_deps.sh`, `source ~/.bashrc`.
4. **Verify versions (2 min):** `galbot_sdk check-version` (add `--robot-ip <ip>` if needed). SDK 1.10.x ↔ GBS 1.18.x. On a mismatch, use the SDK release that matches the robot rather than re-flashing a shared robot.
5. **Verify robot state (5 min):** red e-stop on the back released (twist clockwise), mode is `WORKING_MODE` (`/data/bin/sys_tool`, key `q`, on the XCU). Battery above 25 %.
6. **Read before you move (5 min):** run `get_joint_positions.py`, `get_camera_data.py`, `get_force_sensor_data.py`, `get_lidar_data.py`, `get_bms_information.py` from the `galbot_robot` examples.
7. **Hello-world motion (10 min):** clear **2 m** around the robot, one person on the e-stop, run `tutorials/example1_galbot_control_started.py` (arms rise into a heart pose and return). Then `set_gripper_command.py`.
8. **Base and navigation (15 min):** `get_set_base_velocity.py` for a short open-loop move. If no map exists, build one now (web mapping tool at `http://<HPU-IP>:8000`, push the robot around at walking pace with the e-stop pressed, save, apply, switch back to Working mode), then run `navigate_to_goal.py`.
9. **Manipulation baseline:** `tutorials/example6_pick_and_place.py` and `example2_arm_manipulation.py` are the templates to adapt.

## Known gotchas and safety

| Gotcha | What to do |
|---|---|
| **E-stop** | Hardware: red button on the robot's back, self-locking, twist clockwise to release; power stays on, motion is locked. Software (SDK 1.10.0+): `emergency_stop()` / `resume_from_emergency_stop()`; allow about 10 s to stabilise after resuming |
| Robot ignores commands | Check in this order: e-stop released → mode not `ABNORMAL` → versions match → `singorix` running on XCU. Quick recovery: `systemctl restart launcher` on XCU and HPU |
| `ABNORMAL` mode on a fresh robot | Usually no map, so localisation cannot start. Map first, then restart the launcher on the HPU |
| Mode switching | Working ↔ Deployment switches require the e-stop **released**, which briefly powers the motors. Keep people clear |
| Chassis will not move | Below **25 % charge** the base enters protection stop. Charge early; a full charge takes about 3.5 h |
| Python `.append()` on SDK objects silently does nothing | List attributes return copies. Build a plain Python list and assign it (`traj.points = points`). Symptom: `ControlStatus.INVALID_INPUT`, no motion |
| `set_config()` returns SUCCESS but nothing changes | Settings apply only **after a device restart**. One invalid key rejects the whole batch |
| Works on the robot, fails from the laptop | embosa IP config is wrong or was reset on reboot (`enable_modify_embosa_cfg=false` in `/data/config/system.cfg` on both units keeps it). `get info failed` / `PUBLISH FAIL` in SDK logs point here |
| End-effector commands fail | Robot config must match the mounted tools (`right_suction_cup` vs `right_gripper`). Booth engineer edits `robot_config.toml` and restarts the launcher |
| Joint stuck at a limit | Hold the teach button on the wrist and drag the arm back inside limits; press and release the e-stop to clear |
| Speaker silent | Audio service (`galbot_vtn`) can be disabled in `/data/config/launcher.cfg` on the HPU |
| Camera streams unstable | Lower resolution in the camera `.cfg` files when several sensors run at once (takes effect after reboot) |
| `numpy has no typeDict` | `pip install --upgrade scipy` |
| Teleop with TM01 | Never put the leader arms down while the robot is following. Do not drive or brake fast with the torso at full height (tip-over risk) |
| Environment limits | Wheeled base, IP54, 0–40 °C: **indoor, flat floors only**. No stairs, snow or slopes |
| Licence / access limits | Business modules locked; online sim and one-click deploy are paid; GraspVLA-family product models are not exposed through the SDK |

## Community resources

- **Docs:** inside the SDK repo (`docs/g1/en`, `docs/g1/zh`), and online at the developer platform (login for the AI assistant). English docs are complete for G1.
- **Support:** GitHub issues on GalbotSDK; developer e-mail `developer@galbot.com`; Chinese-language chat groups (free tier is community-only, no SLA).
- **Training:** "Galaxy Pioneer" bootcamps (2-, 3- and 7-day) are tied to paid tiers.
- **Community size:** small. GalbotSDK has about 70 GitHub stars and no visible third-party ROS wrappers or forum, so expect to rely on the booth engineers and the bundled examples.
- **Research code with larger communities:** OpenTrack, OpenWBT, LATENT, Humanoid-GPT (each roughly 500–800 stars) — but these target bipedal humanoids.

## Sources

- [GalbotSDK repository and README](https://github.com/GalaxyGeneralRobotics/GalbotSDK)
- [GalbotSDK CHANGELOG](https://raw.githubusercontent.com/GalaxyGeneralRobotics/GalbotSDK/HEAD/CHANGELOG.md)
- [GalbotSDK G1 docs (English, in-repo): overview, installation, version compatibility, troubleshooting, routine operations, tutorials, set_config reference](https://github.com/GalaxyGeneralRobotics/GalbotSDK/tree/HEAD/docs/g1/en)
- [GalbotSDK tutorial example 5 (VLA execution)](https://raw.githubusercontent.com/GalaxyGeneralRobotics/GalbotSDK/HEAD/docs/g1/en/python/tutorials/example5_execute_vla.py)
- [galbot_one_golf_description](https://github.com/GalaxyGeneralRobotics/galbot_one_golf_description)
- [galbot_s1_description](https://github.com/GalaxyGeneralRobotics/galbot_s1_description)
- [galbot-mcap2lerobot](https://github.com/GalaxyGeneralRobotics/galbot-mcap2lerobot)
- [GitHub org GalaxyGeneralRobotics](https://github.com/GalaxyGeneralRobotics)
- [GraspVLA repository](https://github.com/PKU-EPIC/GraspVLA)
- [GraspVLA paper (arXiv 2505.03233)](https://arxiv.org/abs/2505.03233)
- [Humanoid-GPT repository](https://github.com/GalaxyGeneralRobotics/Humanoid-GPT)
- [OpenTrack repository](https://github.com/GalaxyGeneralRobotics/OpenTrack)
- [Galbot developer platform](https://developer.galbot.com/?lang=en)
- [TM01 leader-follower arm manual (Chinese)](https://developer.galbot.com/docs/tm01/1.4.0/zh/tm01)
