---
type: challenge-playbook
company: "Magiclab Robotics"
slug: Magiclab
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Magiclab Robotics × T02 — Hackathon Playbook

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Brief](Magiclab-T02-1-Brief.md) · [Products and solutions](Magiclab-T02-2-Products-and-Solutions.md)

**Before anything else (first 30 minutes):** confirm which units are hackable (MagicDog **EDU**, Z1 **Development Version**, Y1?), connect by Ethernet on **192.168.55.x** with multicast on, and check that `ros2 topic list` shows `/scan` with CycloneDDS and `ROS_DOMAIN_ID=25`. All concepts below assume a MagicDog EDU; swap in Y1 or MagicDog-W if you get one.

## Solution approaches

### Concept 1 — Night-watch patrol dog (safest)

- **Problem → value:** small resorts cannot staff night rounds of plant rooms, garages, lift stations and corridors. A dog that walks a fixed round and reports only what changed saves a human round and shortens detection time.
- **Hardware:** MagicDog EDU; team laptop; optional **D-Robotics RDK X5** on the back for on-board inference.
- **Architecture / stack:**
  - Perception: `/scan` + RGB / RGB-D topics from `magicdog_ros2_sdk`; a vision-language model or small detector on the laptop for "person on floor", "blocked exit", "door open", "water on floor".
  - Planning: built-in SLAM (`/set_slam_model`, `/save_map`), waypoint list sent to `/goal_pose`, wait on `/ab_navigation_complete`.
  - Control: built-in navigation; stand / sit / gait through `magicdog_sdk` high-level API.
  - Output: web dashboard with map, position (`/tracked_pose`), photo and a one-line incident card.
- **48-hour plan:**
  - H0–6: network, SDK build, teleop walk, record a map of the demo area.
  - H6–24: waypoint patrol loop; image capture at each waypoint; first anomaly detector.
  - H24–40: dashboard, incident cards, voice announcement through the robot audio service; repeat runs.
  - H40–48: freeze code, rehearse, record a backup video.
- **3-minute demo script:** (0:00) the problem in one sentence → (0:30) dog starts its round on its own → (1:15) a teammate lies down or blocks an exit → (1:45) dog stops, announces, incident card appears with photo and map pin → (2:30) show the night's log and what a real deployment would cost in rounds saved.
- **Risks and fallbacks:** ROS 2 SDK does not match firmware → drive waypoints by timed velocity commands through `magicdog_sdk` and keep the detection pipeline. Localisation drift → shorten the route, add distinct landmarks. Wi-Fi drop → run everything over the cable with a walking operator.
- **Judging angles:** innovation low–medium; technical depth medium (full autonomy loop); impact clear; Leukerbad relevance: thermal-bath plant rooms, underground parking, hotel corridors in low season.

### Concept 2 — Infrastructure round with baseline comparison

- **Problem → value:** inspection of pipes, pumps, cable-car or tunnel equipment is about spotting change (leak, heat, missing cover, ice). Comparing each visit with a stored baseline turns a walking robot into a maintenance tool.
- **Hardware:** MagicDog EDU (or Y1 if available, with its thermal / gas payload options); a USB thermal camera or gas sensor you bring; **SKYLANDX** MetaCam for the 3D baseline scan.
- **Architecture / stack:**
  - Perception: per-waypoint RGB (+ thermal) capture; gauge reading and change detection by a vision-language model on the laptop; image alignment against baseline shots.
  - Planning: same waypoint navigation as Concept 1; inspection points defined in the MetaCam 3D model and mapped to robot map coordinates by hand-picked reference points.
  - Control: built-in navigation; body pitch / height via high-level motion to aim the camera.
  - Compute: laptop; extra sensor read by an RDK X5 or a laptop USB port, powered separately.
- **48-hour plan:**
  - H0–6: as Concept 1, plus a MetaCam scan of the area.
  - H6–24: patrol loop; baseline image set; extra sensor mounted and logging.
  - H24–40: change detection, gauge reading, findings pinned in the 3D model.
  - H40–48: stage two faults, rehearse, backup video.
- **3-minute demo script:** show the 3D twin with inspection points → dog walks the round → a staged fault (warm object, moved valve handle, puddle) → the finding appears on the twin with before / after images and a suggested work order.
- **Risks and fallbacks:** twin-to-map alignment takes too long → show findings on the 2D occupancy map. Thermal camera integration fails → RGB-only change detection. Mount shakes → capture only while standing still.
- **Judging angles:** innovation medium; technical depth high (multi-sensor, twin); impact strong for operators; Leukerbad relevance: thermal-water pipes and pumps, Gemmi and Torrent lift stations, road tunnels (framing, not a tested site).

### Concept 3 — First-look scout for a closed path

- **Problem → value:** after a rockfall, avalanche or flood warning, someone has to check a closed path or building before responders go in. A remote-operated dog gives eyes, ears and a small payload drop without exposing a person.
- **Hardware:** MagicDog EDU, or **MagicDog-W** for its 4G link, or **Y1** for real outdoor use; **XREAL** glasses for the operator; small payload (radio, first-aid pouch, under 5 kg).
- **Architecture / stack:**
  - Perception: live camera stream; person detection; mic array for a "call out and listen" check; optional SKYLANDX scan carried in.
  - Planning: operator-in-the-loop — shared autonomy with built-in obstacle avoidance mode (`/switch_navigate_mode` 1) and velocity input.
  - Control: high-level velocity commands from a gamepad; video and telemetry overlay in the glasses.
  - Compute: laptop as operator station; robot streams over Wi-Fi (or 4G on the W).
- **48-hour plan:**
  - H0–6: teleop with video latency measured; payload mount.
  - H6–24: operator HUD in XREAL; person detection overlay; two-way audio.
  - H24–40: breadcrumb map of the route, "found person" marker, payload-drop routine (sit and tilt, or simple release).
  - H40–48: obstacle course rehearsal; backup video.
- **3-minute demo script:** operator sits with back to the course → dog enters a cluttered "closed" zone → HUD flags a person → operator talks through the robot, drops the pouch → route and victim position exported for the rescue team.
- **Risks and fallbacks:** video latency too high → lower resolution, cable tether. Glasses integration slips → laptop screen HUD. Outdoor snow demo fails → run indoors on a rubble mock-up and state limits honestly.
- **Judging angles:** innovation medium; technical depth medium; impact high and easy to explain; Leukerbad relevance very high (avalanche and rockfall closures) — but the EDU has no weather rating, so pitch it as a prototype of a Y1-class deployment.

### Concept 4 — Dog-and-humanoid incident team (most ambitious)

- **Problem → value:** an incident needs both detection and people management. A patrol dog finds the hazard; a humanoid stands at the junction and redirects guests, as Magiclab's traffic robot did at the Wuxi Marathon.
- **Hardware:** MagicDog EDU + **MagicBot Z1 Development Version**; laptop as coordinator.
- **Architecture / stack:**
  - Perception: dog as in Concept 1; Z1 uses its cameras for a simple "person approaching" trigger.
  - Planning: a coordinator service (LLM with a small tool set) turns an incident card into tasks: dog holds position at hazard, Z1 walks to a preset spot, gestures and speaks multilingual directions.
  - Control: dog via ROS 2 nav; Z1 via `magicbot-z1_sdk` high-level motion, pre-recorded arm gestures and audio.
  - Compute: all on laptop; both robots on one network.
- **48-hour plan:**
  - H0–6: both SDKs running; Z1 walk, gesture and speak tests.
  - H6–24: Concept 1 patrol loop; Z1 gesture library (stop, go left, go right).
  - H24–40: coordinator, incident-to-task logic, language switching (DE / FR / EN).
  - H40–48: timing rehearsal; backup video.
- **3-minute demo script:** dog patrols → detects smoke-machine haze or a blocked corridor → coordinator dispatches Z1 → Z1 takes position, signals and tells visitors the alternative route → dashboard shows the whole timeline.
- **Risks and fallbacks:** two robots double the integration risk → Z1 stays at a fixed post (no walking). Z1 on site is the base edition (no SDK) → drop to Concept 1 and use a screen or speaker as the "marshal".
- **Judging angles:** innovation high; technical depth high (multi-robot orchestration); impact plausible for events and evacuations; Leukerbad relevance: guest guidance at baths and lift stations during closures.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| MagicDog EDU + **SKYLANDX** MetaCam | 3D baseline / digital twin that the 2D-LiDAR dog cannot build itself | Low–medium (offline scan, manual alignment) |
| MagicDog EDU + **D-Robotics** RDK X5 | On-dog detection and extra sensor hub (thermal, gas) without a laptop link | Medium (power, mount, ROS 2 bridge) |
| MagicDog + **XREAL** glasses | Heads-up operator view for remote scouting | Medium |
| MagicDog + **Unitree** Go2 or **Genisom** quadruped | Mixed-fleet patrol under one dispatcher; shows vendor-neutral design | Medium–high (two SDKs) |
| MagicBot Z1 dev + **Binabik AI** agent OS | Faster task orchestration on the humanoid | Unknown — ask both teams ⚠️ unverified |
| MagicBot Gen1 + **OriginFlow** EMG capture | Gesture or muscle-signal teleoperation for hazardous tasks | High; Gen1 availability doubtful |

Naming trap when talking to other teams: MagicBot **Z1** is not the Unitree Z1 arm; MagicBot **D1** is not the AGIBOT D1 quadruped.

## Questions to ask the Magiclab Robotics engineers on site

1. Which units here are **EDU / Development Version**, and is low-level control unlocked?
2. Does `magicdog_ros2_sdk` (last pushed May 2025) match the firmware on these robots? Which ROS 2 distro do you run on site?
3. Can I send velocity commands and navigation goals at the same time as reading sensors, and what is the correct topic for manual velocity (`/vel_app`)?
4. Does built-in SLAM work on **slopes and stairs** with the 2D LiDAR, and how large a map is practical?
5. What power and data ports can I use for an add-on sensor or compute board on the MagicDog (voltage, current limit, mount points)?
6. Is a **Y1 or T1** available for a supervised outdoor run, with thermal or gas payload? What speed limits apply?
7. What is the wireless range and video latency for remote operation, and does the MagicDog-W 4G link work with a Swiss SIM?
8. Is the dog safe to run on wet or snowy ground, and who is liable if it falls?

## Decision rule

- **Pick Magiclab Robotics for T02 if** you want an autonomous patrol or inspection demo and a MagicDog EDU (or better, Y1) with a working ROS 2 SLAM / nav stack is confirmed in the first hour.
- **Avoid if** your idea needs manipulation, proven outdoor ruggedness on a small robot, aerial coverage, or if only PRO / base editions without SDK access are on site.

## Sources

- [Magiclab Robotics profile (this repo)](../Magiclab.md)
- [MagicDog product page](https://www.magiclab.top/en/dog)
- [MagicDog-W product page](https://www.magiclab.top/en/dog-w)
- [MagicDog-Y1 product page](https://www.magiclab.top/en/dog-y)
- [GitHub — magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk)
- [GitHub — magicdog_sdk](https://github.com/MagiclabRobotics/magicdog_sdk)
- [GitHub — magicdog-y1_sdk](https://github.com/MagiclabRobotics/magicdog-y1_sdk)
- [GitHub — pico_teleoperate](https://github.com/MagiclabRobotics/pico_teleoperate)
- [QbitAI — MagicLab at WRC 2026 (Chinese)](https://www.qbitai.com/2026/08/477155.html)
- [EqualOcean — MagicLab targets European logistics (IFA 2026)](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)
