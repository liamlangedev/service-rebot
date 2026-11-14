---
type: challenge-playbook
company: "D-Robotics"
slug: D-Robotics
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# D-Robotics × T02 — Hackathon Playbook

⬆ [D-Robotics profile](../D-Robotics.md) · [Brief](D-Robotics-T02-1-Brief.md) · [Products and solutions](D-Robotics-T02-2-Products-and-Solutions.md)

**Ground rules for every concept:** D-Robotics supplies the computer and the perception software, never the robot. Use pre-converted models first (Model Zoo, TogetheROS.Bot); treat custom model conversion as optional. Which boards and cameras are actually on site is unconfirmed: ask at H0.

## Solution approaches

### Concept 1 — "Sentinel" edge hazard node (safest)

- **Problem → value:** paths, tunnel portals or slopes closed for avalanche / rockfall risk still get walked into; a control room cannot watch every camera. A self-contained node detects people or new obstacles in a closed zone and raises an alert locally, even with no internet.
- **Hardware:** RDK X5 (8 GB preferred) + RDK Stereo Camera (or any MIPI / USB camera) + PoE module or power bank. Optional: a speaker / light on GPIO for a local warning.
- **Architecture / stack:** camera → `hobot_codec` / `hobot_cv` → YOLO person + object detection (Model Zoo, pre-converted) → ByteTrack → zone logic (polygon + dwell time) in a Python ROS 2 node → optional `hobot_stereonet` for metric distance → alert (snapshot + distance + timestamp) over MQTT / HTTP to a laptop dashboard; `hobot_tts` for a spoken warning. All inference on the X5; laptop only displays.
- **48-hour plan:**
  - H0–6: flash RDK OS, run a Model Zoo YOLO demo on live camera, confirm FPS.
  - H6–24: tracking + zone logic + alert message; simple web dashboard.
  - H24–40: stereo distance, "new static object on path" rule (background change or open-vocabulary prompt), offline buffering and re-send when the link returns.
  - H40–48: enclosure mock-up, rehearse, record backup video.
- **3-minute demo script:** (1) show the node, unplug the network cable; (2) a teammate walks into the taped "closed zone": local voice warning fires, light turns on; (3) re-plug: buffered alert with snapshot and distance appears on the dashboard; (4) drop a box "rock" on the path: obstacle alert; (5) one slide on cost per node and where it would sit in Leukerbad.
- **Risks and fallbacks:** stereo camera not available → mono camera, zone logic in pixels. Obstacle rule flaky → demo person intrusion only. Low light → add a lamp; say so.
- **Judging angles:** modest innovation; solid technical depth if offline-resilience is shown live; strong real-world impact per franc; Leukerbad relevance is direct (closed winter trails, valley road, cable-car stations).

### Concept 2 — Quadruped patrol and inspection payload

- **Problem → value:** routine inspection of tunnels, plant rooms, or thermal-water infrastructure is repetitive and sometimes unsafe; a legged robot with an independent perception payload logs anomalies with a location.
- **Hardware:** RDK X5 + stereo camera as a strap-on payload on a quadruped from another vendor on site (Unitree Go2 / B2, Genisom AI, Magiclab, AGIBOT D1). Robot power or a power bank for the 5 V supply.
- **Architecture / stack:** stereo camera → `hobot_stereonet` depth + `dstereo_occupancy` → detection (YOLO; `hobot_yolo_world` or `hobot_dosod` for text-defined targets such as "puddle", "open door", "person lying down") → anomaly log with pose from the robot's odometry or `hobot_vio` → H.265 stream via `hobot_codec` to the operator. Motion: start with teleoperation through the robot vendor's SDK; add waypoint patrol only if the vendor exposes velocity commands over ROS 2.
- **48-hour plan:**
  - H0–6: confirm with the quadruped vendor how to send velocity commands and read odometry; bring up X5 + camera on the bench.
  - H6–24: mount payload, teleop with live detections overlaid; anomaly log (image, class, pose).
  - H24–40: scripted patrol loop (waypoints or line of markers), report page with a map sketch.
  - H40–48: reliability runs, fallback video.
- **3-minute demo script:** robot walks a short "service corridor"; three planted anomalies (person down, blocked exit, leak mock-up) are detected and appear in a report with photo and position; operator view shows a low-bitrate stream.
- **Risks and fallbacks:** vendor SDK access slower than expected → push the robot by its own remote and keep D-Robotics perception fully autonomous. Open-vocabulary detections unreliable → fall back to fixed YOLO classes (person, backpack, bottle). Vibration blur → lower gait speed.
- **Judging angles:** clear multi-vendor integration (technical depth), believable inspection workflow (impact), tunnels and spa plant rooms give local relevance.

### Concept 3 — Search assistant with on-board scene reports

- **Problem → value:** after an incident, responders need fast answers to "is anyone in there, and what does it look like?" without streaming full video over a weak link. The robot sends short text + one image instead.
- **Hardware:** RDK S100 (preferred, if on site) or RDK X5 8 GB, stereo camera, microphone / speaker; carried by a quadruped or wheeled base from another vendor.
- **Architecture / stack:** detection + `reid` / pose (`mono2d_yolo_pose` on S100) to find and stay with a person → `hobot_llamacpp` VLM (or MiniCPM5-2B sample on S100) to describe the scene on a trigger → `Sensevoice` speech input and `hobot_tts` to talk to the casualty → compact report (text, thumbnail, distance from stereo) to the command laptop. Everything on-board.
- **48-hour plan:**
  - H0–6: benchmark the VLM on the available board (seconds per answer decides the whole concept).
  - H6–24: person-found trigger → VLM report → message pipeline; speech prompt / reply loop.
  - H24–40: integrate on the mobile base, add "posture: standing / lying" from pose, bandwidth meter in the UI.
  - H40–48: rehearse with a fixed scene; pre-compute nothing, but have a recorded run ready.
- **3-minute demo script:** robot enters a dim "room", finds a lying teammate, asks "Can you hear me?", sends: "1 person, lying, responsive, 3.2 m from entrance, exit partly blocked" plus one image; show kilobytes sent versus a video stream.
- **Risks and fallbacks:** VLM too slow or wrong → use templated reports from detector + pose + depth, keep VLM as an optional extra line. Speech recognition language coverage ⚠️ unverified → push-button reply. S100 not on site → X5 with detection-only reports.
- **Judging angles:** highest innovation of the board-only concepts (edge VLM for triage), honest technical depth if latency is shown, strong fit with mountain-rescue reality (poor connectivity).

### Concept 4 — Town-scale alert mesh with robot dispatch (most ambitious)

- **Problem → value:** connect detection to response: several cheap sentinel nodes watch critical points, and an alert automatically sends a robot to verify before people are put at risk.
- **Hardware:** 2–3 RDK X5 sentinel nodes (Concept 1) + one quadruped or wheeled robot with an X5 / S100 payload (Concept 2) + SKYLANDX MetaCam scan as the base map + optional XREAL glasses for the operator.
- **Architecture / stack:** nodes publish alerts with a map coordinate → dispatcher (laptop, ROS 2) picks the goal → robot navigates (vendor navigation, or TROS Navigation2 with SLAM Mapping if a LiDAR is available) → on arrival runs the Concept 2 / 3 perception → result closes the alert on a shared map view.
- **48-hour plan:**
  - H0–6: split the team: nodes / robot / map + UI. Fix the alert message format in the first hour.
  - H6–24: nodes working standalone; robot teleop + perception; map imported and shown.
  - H24–40: dispatch link (alert → goal), first full loop even if the robot leg is teleoperated.
  - H40–48: cut scope to one reliable loop; rehearse.
- **3-minute demo script:** map on screen with three node icons; one node turns red (intrusion / obstacle); robot leaves its dock, arrives, confirms "person present" or "false alarm"; the icon turns green; state the end-to-end time.
- **Risks and fallbacks:** autonomous navigation is the weak link → teleoperate the drive, keep alert → verification logic automatic. Map alignment slips → use a hand-drawn floor plan. Too many parts → ship Concept 1 + a teleoperated verifier.
- **Judging angles:** system-level thinking and digital-twin angle, strongest "city-scale" story; risk is breadth over depth, so show one loop working end to end.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| RDK X5 + Unitree Go2 / B2 | Patrol / search payload on a proven quadruped; Model Zoo even lists a Go2 locomotion policy sample (offline inference only) | Medium: depends on Unitree SDK access for velocity + odometry |
| RDK X5 + Genisom AI or Magiclab quadruped | Same as above with a different carrier | Medium to high: SDK openness unknown, ask first |
| RDK X5 nodes + SKYLANDX MetaCam | Alerts pinned on a real 3D scan of the site (digital-twin view) | Low to medium: export map, register node positions by hand |
| RDK X5 / S100 + XREAL glasses | Hands-free operator view of alerts and robot camera | Medium: simple web / video view is easy, spatial anchoring is not |
| RDK S100 + Spirit AI Moz1 | Spirit AI is a named Sunrise S600 customer, so the teams may already know each other's stack | Unknown: ask both booths |
| RDK X5 + Leadshine motors | DIY pan-tilt or gate / barrier actuator triggered by detections | Medium: CAN FD / PWM available on X5, drive protocol to confirm |
| RDK X5 + Flexiv / ROKAE / Dobot arm | Vision-guided valve turning or switch pressing for "keep infrastructure running" | High: arm SDK + calibration in 48 h is tight |

## Questions to ask the D-Robotics engineers on site

1. Which boards, how many, and which cameras (stereo module, IMU variant) can teams borrow today?
2. Which pre-converted detection model gives the best FPS on RDK X5 for person detection at 640 px, and what FPS should we expect with `hobot_stereonet` running alongside?
3. Is there any ready model for fire, smoke or fallen-person detection, or must we train and convert? How long does an OpenExplorer conversion of a custom YOLO take in practice, and can you do it with us?
4. How fast is the VLM node (`hobot_llamacpp`) on X5 8 GB versus MiniCPM5-2B on S100 (seconds per image answer)?
5. Does `hobot_yolo_world` / `hobot_dosod` accept new text prompts at runtime, or are vocabularies fixed at conversion time?
6. Has anyone run TROS on top of a Unitree Go2 (velocity commands, odometry, DDS settings)? Is the HIMLoco sample usable on a real robot?
7. What is the real power draw of X5 under load and its operating temperature range, for an outdoor battery node?
8. Which languages does the Sensevoice speech node support on the board (German, French, English)?

## Decision rule

- **Pick D-Robotics for T02 if** your idea is perception-centric (detect, measure, map, report), must run offline at the edge on little power, and you either build a fixed sensor node or have already secured another vendor's mobile robot.
- **Avoid if** you need a complete robot from one vendor, rugged outdoor hardware, thermal or gas sensing, or you plan to train a custom model and nobody on the team has time for the conversion toolchain.

## Sources

- [D-Robotics company profile (this repo)](../D-Robotics.md)
- [RDK X5 product page](https://en.d-robotics.cc/rdkx5)
- [D-Robotics accessories page](https://en.d-robotics.cc/accessories)
- [Introduction to TogetheROS.Bot (feature and board table)](https://developer.d-robotics.cc/tros_doc/en/tros)
- [rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo)
- [rdk_model_zoo samples](https://github.com/D-Robotics/rdk_model_zoo/tree/main/samples)
- [hobot_stereonet](https://github.com/D-Robotics/hobot_stereonet)
- [D-Robotics GitHub org](https://github.com/D-Robotics)
- [Robotics Dream Keeper Challenge 2026 Winter](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter)
- [Kyodo PR Wire: USD 400M Series C (17 Sep 2026)](https://kyodonewsprwire.jp/release/202609176168)
