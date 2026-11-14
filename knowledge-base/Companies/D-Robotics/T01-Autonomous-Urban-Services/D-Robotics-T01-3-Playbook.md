---
type: challenge-playbook
company: "D-Robotics"
slug: D-Robotics
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# D-Robotics × T01 — Hackathon Playbook

⬆ [D-Robotics profile](../D-Robotics.md) · [Brief](D-Robotics-T01-1-Brief.md) · [Products and solutions](D-Robotics-T01-2-Products-and-Solutions.md)

> D-Robotics is the on-board computer, not the robot. Every concept below names the mobility partner you still need. Confirm in the first hour which boards, cameras and audio boards are on the D-Robotics table, and which base you can borrow. Integration with other vendors' robots is described as a plan, not as something verified.

## Solution approaches

### Concept 1 — Street-keeper smart camera (no robot needed)

- **Problem → value:** a small resort has few municipal staff and long walking routes. A cheap edge camera that spots litter, overflowing bins, blocked paths or unshovelled snow and files a geo-tagged ticket saves patrol rounds.
- **Hardware:** RDK X5 + MIPI or USB camera (optionally RDK X5 PoE Module for a single-cable install). Optional: mount the same unit on any robot or on a handcart to show it "patrolling".
- **Architecture / stack:** camera → `mono2d_trash_detection` or open-vocabulary `hobot_dosod` on the BPU → small ROS 2 node that debounces detections and writes tickets → web dashboard on a laptop. Optional `hobot_llamacpp` VLM to write a one-line description per ticket. All compute on the X5.
- **48-hour plan:**
  - **H0–6:** flash board, run the stock detection demo with web view, pick 3–4 target classes.
  - **H6–24:** ticket logic, dashboard, photo evidence; collect test scenes around the venue.
  - **H24–40:** add VLM caption or a second camera; tune thresholds; optional ride on a partner robot.
  - **H40–48:** freeze, record backup video, rehearse.
- **3-minute demo script:** show a clean scene (no ticket) → drop a cup and a bag → ticket appears with photo, class and location → clear it, ticket closes → show power draw and cost per unit.
- **Risks and fallbacks:** custom classes need extra DOSOD deployment steps → fall back to the stock garbage model or COCO classes. Snow / ice detection has no ready model → present it as roadmap, do not fake it.
- **Judging angles:** impact and Leukerbad relevance are strong (tourism image, small crew); innovation and technical depth are modest. Low risk, low ceiling.

### Concept 2 — Follow-me porter for guests and staff

- **Problem → value:** steep streets, many elderly spa guests, luggage and laundry to move between bus stop, hotels and clinics. A robot that follows one person and carries the load removes strain without needing a map.
- **Hardware:** RDK X5 + camera (stereo camera if available) on a borrowed base: quadruped (Unitree Go2 / B2, AGIBOT D1, Genisom, Magiclab) or a wheeled platform. Basket or strap for payload.
- **Architecture / stack:** camera → `body_tracking` (person detection + tracking → `/cmd_vel`) with `reid` to stay locked on the same guest → safety node (stop on lost target, depth-based minimum distance from `hobot_stereonet`) → bridge node translating `/cmd_vel` to the base's velocity API. Perception on the X5; locomotion stays on the robot's own controller.
- **48-hour plan:**
  - **H0–6:** run `body_tracking` in its Gazebo mode and on the bench with web view; in parallel get the base moving from a teleop velocity command.
  - **H6–24:** write the `/cmd_vel` bridge with speed limits and a dead-man stop; first follow test in a corridor.
  - **H24–40:** add re-ID so crossing people do not steal the lock; add stop distance from depth; add "start / stop following" by gesture or voice command (`sensevoice_ros2` command words).
  - **H40–48:** payload test with a suitcase, backup video, rehearse.
- **3-minute demo script:** guest says "follow me" → robot follows across the hall carrying a bag → second person walks between them, robot keeps its target → guest stops, robot stops at a set distance → guest says "stop", robot stays.
- **Risks and fallbacks:** base SDK access denied or slow → use a small wheeled kit or a teleoperated base with the X5 only issuing commands. Re-ID unstable → single-person tracking with a clear demo area. Camera mount shake on a quadruped → lower speed, wider lens.
- **Judging angles:** clear real-world impact and Leukerbad story (elderly guests, slopes); technical depth from re-ID + depth safety on a 10 TOPS board; innovation medium.

### Concept 3 — Spa-hotel delivery runner (map-based navigation)

- **Problem → value:** towels, medication, room service and parcels move all day between reception, rooms and treatment areas. Autonomous point-to-point delivery frees care and hotel staff.
- **Hardware:** RDK X5 or S100 on a base that provides **LiDAR and odometry** (quadruped or wheeled mobile manipulator from another vendor). Optional: SKYLANDX MetaCam to capture the venue quickly; XREAL glasses as operator view.
- **Architecture / stack:** LiDAR + odometry from the base → `slam_toolbox` map → Nav2 on the RDK (both `apt` packages, supported on X3 / X5 / S100) → `/cmd_vel` bridge → base. Add-ons: `mono2d_body_detection` to slow down near people, `hobot_tts` to announce arrival, simple web page to order a delivery to a named waypoint.
- **48-hour plan:**
  - **H0–6:** reproduce the official Nav2 + TurtleBot3 Gazebo guide with Nav2 running on the RDK. Confirm the base exposes scan, odom and TF over ROS 2.
  - **H6–24:** map one corridor loop with `slam_toolbox`; tune Nav2 footprint and speed limits for the real base.
  - **H24–40:** waypoint ordering UI, arrival announcement, person-aware slow-down.
  - **H40–48:** run 10 repeat deliveries, log success rate, record backup video.
- **3-minute demo script:** order "towels to room 2" on a phone → robot plans and drives → pauses for a crossing person → announces arrival → returns to base; show the map and the success-rate log.
- **Risks and fallbacks:** this is the concept with the most integration risk: the official guide is **simulation only**, and real TF / odometry tuning eats time. Fallback 1: use the base vendor's own navigation and keep the RDK for perception, voice and ordering. Fallback 2: drop to Concept 2 with fixed "stations".
- **Judging angles:** technical depth high if it runs reliably; impact strong for clinics and hotels; innovation low unless combined with Concept 4.

### Concept 4 — Offline multilingual concierge-and-inspection robot

- **Problem → value:** an alpine resort serves guests in several languages and has patchy connectivity outdoors. A robot that patrols, answers questions about what it sees, guides guests and reports maintenance issues, all without cloud, is a service and a maintenance tool in one.
- **Hardware:** **RDK S100** (80 TOPS, 12 GB) + camera + RDK audio board and speaker, on a mobile base (as in Concept 2 or 3). X5 works with smaller VLMs.
- **Architecture / stack:** microphone → `sensevoice_ros2` (offline ASR) → intent node → `hobot_llamacpp` VLM (InternVL3 family; up to 8B on S100) with the current camera frame → `hobot_tts` reply. In parallel `hobot_dosod` flags maintenance items and logs tickets (Concept 1). Motion: follow-me (Concept 2) or waypoints (Concept 3). Everything on the board; optional `hobot_xlm` LLM on S100 for longer answers.
- **48-hour plan:**
  - **H0–6:** bring up ASR, TTS and the VLM node separately; measure response time and pick the model size that stays usable.
  - **H6–24:** chain voice → VLM → voice; write prompts for wayfinding and "what is wrong here" inspection.
  - **H24–40:** mount on the base, add motion mode, add ticket log; test in noise.
  - **H40–48:** script three reliable interactions, record backup video.
- **3-minute demo script:** unplug the network cable on stage → guest asks a question in German or English about the scene → robot answers aloud → robot is led past a spilled-litter spot and reports it → dashboard shows the ticket.
- **Risks and fallbacks:** VLM latency and answer quality on edge hardware (speed not verified) → shorten prompts, use a smaller model, or pre-compute for scripted questions. Language coverage of the ASR / TTS models ⚠️ unverified → test on day 1; fall back to English. Audio board not on site → USB microphone path needs checking with the engineers.
- **Judging angles:** innovation and Leukerbad relevance highest (offline, multilingual, tourism + maintenance); technical depth high; reliability is the weak point.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| RDK X5 + Unitree Go2 / B2 (or AGIBOT D1, Genisom, Magiclab quadruped) | Follow-me porter or patrol on stairs and slopes | Medium: `/cmd_vel` bridge to the robot's velocity API; check SDK access level on site |
| RDK X5 / S100 + Galaxea R1 or Galbot G1 | Delivery with hand-over or litter pick-up; RDK as extra perception node | High: two stacks; keep the RDK to detection + voice |
| RDK X5 + SKYLANDX MetaCam | Fast 3D capture of the venue for the pitch and for planning routes | Low for visuals; converting the scan to a Nav2 map is ⚠️ unverified |
| RDK X5 + Leadshine drives or coprod modules | Custom wheeled cart driven over CAN FD / PWM from the X5 | High: mechanical build inside 48 hours |
| RDK S100 + Spirit AI Moz1 | Spirit AI is a reported Sunrise S600 customer; ask whether their robot already speaks to RDK tooling | Unknown: ask both teams |
| RDK X5 + XREAL glasses | Operator sees detections / tickets hands-free | Low to medium: stream the TROS web view |

## Questions to ask the D-Robotics engineers on site

1. Which boards, cameras (stereo model?) and audio boards can teams borrow, and how many?
2. Is there an image with TROS, `body_tracking`, `reid`, `hobot_stereonet` and Nav2 pre-installed, or do we `apt install` over the venue network?
3. Has anyone here already bridged an RDK to a Unitree, AGIBOT or other on-site robot? Any example node for `/cmd_vel`?
4. Does Nav2 on the X5 keep up with a real 2D LiDAR plus one BPU model, or should we move to the S100?
5. What does the Stereo OCC package output (grid size, range), and can it feed a Nav2 costmap directly?
6. Which languages do the shipped SenseVoice and TTS models handle (German, French, Italian)? Can we use a USB microphone instead of the audio board?
7. How long does converting a custom YOLO model take with OpenExplorer, and can you do one conversion with us on day 1?
8. What response time should we expect from InternVL3-2B on the X5 and InternVL3-8B on the S100?

## Decision rule

- **Pick D-Robotics for T01 if** you already have (or can borrow) a mobile base and need a cheap, offline, ROS 2 native perception / voice / follow-me brain that you fully control, or if your idea works as a fixed smart sensor.
- **Avoid if** you need a complete robot out of the box, proven real-world Nav2 without integration work, or outdoor operation in snow and sub-zero temperatures during the demo.

## Sources
- [D-Robotics RDK X5 product page](https://en.d-robotics.cc/rdkx5)
- [D-Robotics accessories page](https://en.d-robotics.cc/accessories)
- [TogetheROS.Bot documentation index (feature support list)](https://developer.d-robotics.cc/tros_doc/en/tros)
- [TROS app: Navigation2](https://developer.d-robotics.cc/tros_doc/en/apps/navigation2)
- [TROS app: SLAM mapping](https://developer.d-robotics.cc/tros_doc/en/apps/slam)
- [TROS: body detection and tracking](https://developer.d-robotics.cc/tros_doc/en/boxs/body/mono2d_body_detection)
- [GitHub: body_tracking](https://github.com/D-Robotics/body_tracking)
- [GitHub: reid](https://github.com/D-Robotics/reid)
- [GitHub: hobot_stereonet](https://github.com/D-Robotics/hobot_stereonet)
- [GitHub: hobot_llamacpp](https://github.com/D-Robotics/hobot_llamacpp)
- [GitHub: hobot_dosod](https://github.com/D-Robotics/hobot_dosod)
- [GitHub: sensevoice_ros2](https://github.com/D-Robotics/sensevoice_ros2)
- [GitHub: mono2d_trash_detection](https://github.com/D-Robotics/mono2d_trash_detection)
- [Kyodo PR Wire: Series C release (17 Sep 2026)](https://kyodonewsprwire.jp/release/202609176168)
- [CNX Software: RDK S100P review](https://www.cnx-software.com/2026/08/31/d-robotics-rdk-s100p-a-128-tops-alternative-to-nvidia-jetson-orin-nx-16gb-with-cortex-a78ae-r52-cores/)
