---
type: challenge-playbook
company: "Unitree Robotics"
slug: Unitree
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Unitree Robotics × T02 — Hackathon Playbook

⬆ [Unitree Robotics profile](../Unitree.md) · [Brief](Unitree-T02-1-Brief.md) · [Products and solutions](Unitree-T02-2-Products-and-Solutions.md)

**Assumption for all concepts:** you get a **Go2 EDU** (full SDK, ideally with the Orin module). If you get an As2 / A2 / B2 instead, the same software plan applies and outdoor / snow demos become credible. On-site hardware is not confirmed — settle this in the first 30 minutes.

**First-hour checklist:** confirm variant (EDU?) · Orin fitted? · firmware version · number of batteries and chargers · remote controller / e-stop · allowed test area (stairs, outdoors) · Ethernet access to the robot network (192.168.123.x).

## Solution approaches

### Concept 1 — Night-watch patrol dog (safest)

- **Problem → value:** small resorts cannot staff night patrols of plant rooms, corridors and car parks. A quadruped walks a fixed route, flags anomalies (person lying down, blocked escape route, open door, heat source) and sends an alert with photo and map position.
- **Hardware:** Go2 EDU. Optional: USB thermal camera (bring your own); D-Robotics RDK board as payload computer if no Orin is fitted.
- **Architecture / stack:**
  - Perception: front camera frames (unitree_sdk2_python) → open detector (person / pose) or a VLM call for "what is wrong in this image"; LiDAR `utlidar/cloud` for free-space checks.
  - Planning: waypoint list recorded by driving the route once; either Nav2 + slam_toolbox (community go2_ros2_sdk) or simple odometry-based waypoint following with the built-in obstacle avoidance switched on.
  - Control: high-level sport client (velocity / trajectory commands). No low-level control.
  - Compute: detector on the Orin or a laptop over Wi-Fi; dashboard (web page) on the laptop.
- **48-hour plan:**
  - H0–6: SDK hello-world, drive from Python, pull camera and LiDAR, record a rosbag of the route.
  - H6–24: waypoint patrol loop working; detector running on live frames; alert message format.
  - H24–40: dashboard with map, robot position, alert cards; add 2–3 anomaly types; battery-low return-to-start.
  - H40–48: rehearse 10 full runs, record backup video, freeze code.
- **3-minute demo script:** (0:00) state the problem with one local example → (0:30) robot starts patrol autonomously → (1:15) a team member lies down / a box blocks the exit → robot stops, dashboard shows alert with photo and location → (2:15) operator acknowledges, robot resumes → (2:40) cost and scaling slide.
- **Risks and fallbacks:** localisation drift → use AprilTags or short route; Wi-Fi drop → run everything on board; detector false alarms → restrict to 2 well-tested classes; autonomy fails → drive by joystick and keep detection + alerting autonomous.
- **Judging angles:** innovation low–medium; technical depth medium; real-world impact clear (matches Unitree's own deployed inspection use); Leukerbad relevance — off-season hotels, spa plant rooms, clinic corridors at night.

### Concept 2 — First-in scout with live 3D map

- **Problem → value:** after a rockfall, fire alarm or gas warning, responders need to know what is inside before entering. The robot goes first, builds a 3D map, marks people and hazards on it, and streams this to the incident commander.
- **Hardware:** Go2 EDU (or As2 / B2 for outdoors). Optional: SKYLANDX MetaCam for a "before" reference scan; XREAL glasses for the operator view.
- **Architecture / stack:**
  - Perception: L2 LiDAR → Point-LIO (point_lio_unilidar, ROS 1 Noetic in a container) or slam_toolbox 2D map; camera → person detection; detections projected into the map frame.
  - Planning: teleoperation with assisted obstacle avoidance first; add frontier exploration only if time allows.
  - Control: high-level velocity commands from a gamepad or the operator UI.
  - Compute: SLAM on Orin or laptop; viewer in Foxglove or a web 3D viewer; optional AR overlay on XREAL.
- **48-hour plan:**
  - H0–6: LiDAR mapping offline from a recorded bag; teleop from laptop with video.
  - H6–24: live map + pose; victim / hazard markers pinned into the map.
  - H24–40: operator UI (map, video, markers, "safe route" line); optional comparison with a MetaCam reference scan to highlight changes (blocked corridor).
  - H40–48: build the demo "incident room" (dim light, obstacles, a dummy), rehearse.
- **3-minute demo script:** (0:00) alarm scenario → (0:20) robot enters an area the audience cannot see → (0:40) map grows live on the screen → (1:30) dummy found, marker with photo appears → (2:10) UI shows shortest clear route for the rescue team → (2:40) what changes with a B2 (IP67, 4–6 h).
- **Risks and fallbacks:** ROS 1 / ROS 2 bridging eats time → use the community ROS 2 stack with 2D SLAM; LiDAR mapping jitter during trotting → walk slowly; video lag → lower resolution; no AR in time → big-screen viewer only.
- **Judging angles:** innovation medium; technical depth high (SLAM + semantic markers); impact strong for fire and mountain-rescue services; Leukerbad relevance — tunnels and galleries on the access road, underground car parks, spa basements.

### Concept 3 — Infrastructure inspector with change detection

- **Problem → value:** thermal-water pipework, pumps, electrical cabinets and cable-car stations need routine checks. The robot reads gauges, spots leaks, hot spots and missing covers, and compares each visit with a baseline so only changes reach a human.
- **Hardware:** Go2 EDU or As2 / A2; USB thermal camera (own). Optional: SKYLANDX MetaCam scan as the digital-twin baseline; D2 arm on a larger quadruped to point a sensor (only if available).
- **Architecture / stack:**
  - Perception: at each inspection point the robot takes posed RGB (+ thermal) images → VLM prompt for gauge value and anomaly description → compare with stored baseline (value thresholds + image difference).
  - Planning: inspection points as named waypoints with body pose (use the sport client's attitude control to aim the camera).
  - Control: high-level only.
  - Compute: VLM in the cloud or on a laptop GPU; results stored per asset in a small database; report generated automatically.
- **48-hour plan:**
  - H0–6: robot basics; build a mock plant wall (2 gauges, a pipe, a warm object, a cabinet door).
  - H6–24: waypoint + aim + capture pipeline; VLM gauge reading evaluated on 30+ photos.
  - H24–40: baseline versus current comparison, trend chart, auto-generated inspection report; thermal overlay.
  - H40–48: tune reliability, rehearse, prepare the before / after scenario.
- **3-minute demo script:** (0:00) why manual rounds get skipped → (0:30) robot walks to point 1, reads a gauge, value appears → (1:10) team member changes the scene (gauge moved, door open, heat pad on) → second round flags exactly those changes → (2:20) one-page report on screen → (2:40) link to Unitree's deployed inspection line as the scale-up path.
- **Risks and fallbacks:** VLM misreads gauges → use large-dial mock gauges and show confidence; no thermal camera → visual-only anomalies; pose repeatability → AprilTag at each inspection point.
- **Judging angles:** innovation medium (VLM + baseline diff); technical depth medium–high; impact high and easy to quantify; Leukerbad relevance — thermal-spa plant rooms, cable-car stations, clinic building services.

### Concept 4 — Scout plus remote hands (most ambitious)

- **Problem → value:** finding a problem is half the job; someone still has to close the valve or flip the breaker in an unsafe room. A quadruped scouts and maps; a teleoperated humanoid (or an arm) performs the single critical action; the operator stays outside.
- **Hardware:** Go2 EDU (scout) + **G1 EDU with Dex3-1 hands** (remote hands) with an XR headset. Alternatives: quadruped with D2 arm; or a fixed Flexiv / ROKAE arm as the "actuated valve station". Optional: OriginFlow EMG capture as the operator input.
- **Architecture / stack:**
  - Scout: as Concept 2 (map + hazard marker).
  - Remote hands: xr_teleoperate (headset → arm and hand retargeting) with teleimager video streams; G1 walks under its factory controller, hands under operator control.
  - Coordination: shared map and a simple task board ("hazard at X → send G1 → action done").
  - Compute: teleop host PC on the same network; low latency is essential.
- **48-hour plan:**
  - H0–6: split the team — scout stack / teleop stack; get xr_teleoperate running in simulation or on the robot.
  - H6–24: each half works stand-alone (scout finds marker; G1 turns a mock valve under teleop).
  - H24–40: integrate hand-over, shared UI, practise the manipulation task 50+ times.
  - H40–48: rehearse; decide at H40 whether the humanoid part is live or shown as video.
- **3-minute demo script:** (0:00) gas-leak scenario → (0:20) Go2 finds the "leak" and marks it → (1:00) operator puts on headset, G1 walks in → (1:40) G1 closes the valve; dashboard goes green → (2:30) what was autonomous, what was teleoperated, next step.
- **Risks and fallbacks:** two robots double the failure modes; humanoid falls; teleop latency over Wi-Fi; hands may not be fitted. Fallbacks: valve action by a fixed arm; or cut to Concept 2 with a recorded teleop clip.
- **Judging angles:** innovation high; technical depth high; impact strong narrative (remove people from the hazard); Leukerbad relevance — gas, heat and steam hazards in spa and clinic plant rooms. Only attempt with 5+ people and confirmed G1 EDU access.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Go2 EDU + SKYLANDX MetaCam | High-quality reference scan / digital twin; robot data shows changes against it | Low–medium (offline scan, align by hand or tags) |
| Go2 EDU + XREAL glasses | Hands-free operator view: video, map, alerts in AR | Medium (Android / Unity app + stream) |
| Go2 (any variant) + D-Robotics RDK X5 | Payload computer for vision when no Orin is fitted | Low–medium (mount, power, network) |
| Go2 scout + Unitree G1 EDU or other humanoid (AGIBOT, Magiclab) | Scout-then-act story | High |
| Go2 scout + Flexiv Rizon / ROKAE xMate arm | Force-controlled valve / switch actuation at a fixed station | Medium (two separate stacks, message hand-off) |
| Unitree quadruped + Genisom or Magiclab quadruped | Multi-robot, multi-vendor patrol under one dashboard | Medium–high (two SDKs) |
| Go2 + Binabik AI / coprod software | Agent layer or unified stack on top of the Unitree SDK | Not public — ask both teams |

## Questions to ask the Unitree Robotics engineers on site

1. Which exact variants are available to teams (Go2 EDU? As2 X / EDU? B2?) and how many units, batteries and chargers?
2. Is the Orin module fitted, and can we SSH into it and install our own packages / containers?
3. Which firmware is installed, and does it work with unitree_sdk2, unitree_ros2 (Humble) and the community go2_ros2_sdk?
4. Is there an official SLAM / navigation service on the EDU we can call (map, localise, go-to-point), or must we bring our own?
5. Did you bring any inspection payloads — thermal gimbal, gas sensor, D2 arm, charging dock — and can we use them?
6. Can we test on stairs, outdoors and on snow, and which robot is rated for that (As2 IP54, A2 IP56, B2 IP67)?
7. What is the best way to get low-latency video off the robot (teleimager, WebRTC, raw DDS)?
8. Is any part of the commercial inspection software (3D route planning, meter reading) available for the hackathon?

## Decision rule

- **Pick Unitree Robotics for T02 if** your idea needs a robot that reliably walks through real terrain (stairs, slopes, clutter) carrying sensors, you have an **EDU** unit, and your team's value is in perception, mapping or the operator workflow.
- **Avoid if** your concept depends on strong manipulation, on turnkey autonomous navigation without ROS skills in the team, or you can only get a non-EDU unit and nobody wants to rely on an unofficial SDK.

## Sources

- [Unitree — intelligent inspection solution](https://www.unitree.com/mobile/industry/electricity)
- [Unitree — fire rescue solution](https://www.unitree.com/mobile/industry/fireRescue)
- [Unitree Go2](https://www.unitree.com/go2)
- [Unitree B2](https://www.unitree.com/b2)
- [Unitree A2](https://www.unitree.com/A2)
- [Unitree As2](https://www.unitree.com/As2)
- [Unitree GitHub organisation](https://github.com/unitreerobotics)
- [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python)
- [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
- [point_lio_unilidar](https://github.com/unitreerobotics/point_lio_unilidar)
- [go2_ros2_sdk (community, unofficial)](https://github.com/abizovnuralem/go2_ros2_sdk)
- [Unitree Robotics profile (this repository)](../Unitree.md)
