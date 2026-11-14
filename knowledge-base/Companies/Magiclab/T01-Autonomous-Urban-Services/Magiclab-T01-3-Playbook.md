---
type: challenge-playbook
company: "Magiclab Robotics"
slug: Magiclab
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Magiclab Robotics × T01 — Hackathon Playbook

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Brief](Magiclab-T01-1-Brief.md) · [Products and solutions](Magiclab-T01-2-Products-and-Solutions.md)

**Before you plan anything (first 30 minutes at the booth):** confirm (1) which robots and **editions** are available — only MagicDog **EDU** and MagicBot Z1 **Development Version** are programmable, (2) that the ROS 2 SLAM / navigation services respond on the unit's firmware, (3) how you connect (Ethernet port, subnet, Wi-Fi option). All concepts below assume a MagicDog EDU; swap in MagicDog-W or T1 if offered. Hardware presence is **not confirmed**.

Naming trap: say "MagicBot Z1" and "MagicDog T1" in full — Unitree has a Z1 arm, AGIBOT a D1 quadruped.

## Solution approaches

### Concept 1 — Corridor Courier (indoor point-to-point delivery)

- **Problem → value:** clinics and spa hotels move small items (medication bags, towels, lab samples, room-service orders) by hand across long corridors. A 16 kg legged runner takes the walk off staff and copes with door sills and a few steps.
- **Hardware:** MagicDog EDU + passive basket or lidded box (≤ **5 kg**). Optional: D-Robotics RDK board or mini PC on the back as ROS 2 computer; phone or tablet as order UI.
- **Architecture / stack:**
  - Perception / localisation: built-in 2D-LiDAR SLAM from `magicdog_ros2_sdk` (`/set_slam_model` 1 to map, `/save_map`, then mode 3 to localise).
  - Planning: your own small "dispatch" node holding named waypoints (reception, room 12, lab); it publishes `/goal_pose` and waits on `/ab_navigation_complete`. Obstacle avoidance by the on-board stack.
  - Control: on-board motion controller. Speech: TTS service for "delivery for room 12" and arrival prompts.
  - Compute: nav on the robot; dispatch + web UI on the wired companion computer or laptop.
- **48-hour plan:**
  - **H0–6:** network up (CycloneDDS, `ROS_DOMAIN_ID=25`), echo `/scan`, joystick drive, map one corridor, save map.
  - **H6–24:** localise on saved map, send goals from CLI, then from the dispatch node; add 3–4 named waypoints, TTS, battery check from `/motion/bms_data`.
  - **H24–40:** order UI (web form or QR per room), delivery confirmation (head-touch topic as "received" button), return-to-base, failure handling (retry, call for help).
  - **H40–48:** 20 repeat runs, record success rate and time, film a backup video, rehearse.
- **3-minute demo script:** (0:00) one-line problem with a clinic corridor picture → (0:30) judge orders an item on a phone → (0:45) helper loads basket, dog announces and leaves → (1:45) arrives, speaks, judge taps head to confirm → (2:15) dog returns; show log of runs, success rate, payload and battery numbers → (2:40) what a T1-class robot adds in production.
- **Risks and fallbacks:** ROS 2 SDK mismatch with firmware → fall back to `magicdog_sdk` high-level velocity commands plus your own waypoint follower on `/scan` or AprilTags from the camera. Tether → backpack computer, or a short demo lane with a managed cable. Localisation drift in glass or crowded areas → pick a walled route.
- **Judging angles:** *Innovation* low–medium; *technical depth* medium (measured reliability is your differentiator); *impact* clear staff-time saving; *Leukerbad* direct fit with rehabilitation clinics and spa hotels.

### Concept 2 — Dorf Guide (multilingual wayfinding dog)

- **Problem → value:** visitors — many elderly, many non-German speakers — ask the same questions: where is the bath entrance, the pharmacy, the bus. A guide robot answers in the guest's language and **walks them there** at their pace.
- **Hardware:** MagicDog EDU (mic array, speaker, depth camera). Optional: XREAL glasses for a staff or visitor overlay of the route; MagicBot Z1 Development Version as a stationary greeter if available.
- **Architecture / stack:**
  - Perception: mic array audio → speech-to-text on laptop; depth camera for checking the guest is still behind (simple person detector on the laptop).
  - Planning: LLM with a small place database (name → map pose, opening hours) picks a destination and generates the spoken answer; your node sends `/goal_pose`, pauses via `/switch_navigate_mode` or zero velocity when the guest falls back.
  - Control: on-board navigation; TTS service for speech (check language support — otherwise play your own synthesised audio).
  - Compute: nav on robot; speech, LLM and person check on laptop or cloud API.
- **48-hour plan:**
  - **H0–6:** same bring-up as Concept 1; test audio in and out; confirm TTS languages.
  - **H6–24:** map venue area, define 5–6 destinations, working "take me to X" by typed command; speech loop on laptop.
  - **H24–40:** pace adaptation (stop and wait, "shall I slow down?"), three languages, graceful "I cannot go there, here are directions" answer for off-map places.
  - **H40–48:** noise testing in the hall, fixed fallback phrases, rehearsal.
- **3-minute demo script:** judge asks in French or Italian for a location → dog answers, sets off → presenter deliberately stops; dog waits and prompts → arrival announcement with opening hours → slide: destinations, languages, response latency.
- **Risks and fallbacks:** hall noise breaks speech recognition → push-to-talk on a phone. TTS limited to Chinese / English ⚠️ unverified → play audio from the companion computer's speaker. Guest tracking unreliable → timed check-ins instead of vision.
- **Judging angles:** *Innovation* medium; *technical depth* medium (speech + nav + human-pace loop); *impact* tourism and accessibility; *Leukerbad* very high — multilingual resort with elderly guests.

### Concept 3 — Village Upkeep Scout (patrol that files maintenance tickets)

- **Problem → value:** a small municipality cannot inspect every path, bin, lamp and handrail daily. A patrolling robot turns a walk into geotagged tickets (overflowing bin, blocked path, ice patch, broken light) for the works crew.
- **Hardware:** MagicDog EDU or MagicDog-W (4G, longer runtime). Optional: SKYLANDX MetaCam scan as a prior 3D map and as the "digital twin" the tickets are pinned on; D-Robotics RDK board for on-dog vision inference.
- **Architecture / stack:**
  - Perception: camera frames → vision-language model or small detector (laptop / RDK) classifying issue types; pose from `/tracked_pose`.
  - Planning: looped waypoint patrol through `/goal_pose`; on detection, stop, capture, create ticket (image, class, map pose, time).
  - Control: on-board nav. Output: web dashboard with map pins and a "resolved" workflow.
  - Compute: detection off-board; dashboard on laptop.
- **48-hour plan:**
  - **H0–6:** bring-up, map a loop, camera stream to laptop.
  - **H6–24:** patrol loop running unattended; detection of 2–3 staged issue types (full bin, obstacle on path, spill).
  - **H24–40:** ticket dashboard, duplicate suppression, simple priority rule; optional MetaCam map overlay.
  - **H40–48:** staged course with three "faults", repeat runs, metrics (detections, false alarms).
- **3-minute demo script:** show the empty dashboard → dog patrols a taped "street" with a full bin and a blocked path → tickets appear live with photo and map pin → presenter clears one fault, next lap closes the ticket → cost framing: one robot lap vs. one staff round.
- **Risks and fallbacks:** detector unreliable → restrict to two visually obvious classes or fiducial-tagged assets. Outdoor demo not possible (no IP rating, snow) → indoor mock street. Overlap with T02 (safety patrol) — keep the story on **maintenance service**, not security.
- **Judging angles:** *Innovation* medium; *technical depth* medium–high (autonomy + perception + data product); *impact* municipal operations; *Leukerbad* good — winter path upkeep, small works crew.

### Concept 4 — Concierge and Runner (humanoid front desk + quadruped delivery)

- **Problem → value:** hospitality and care sites need both a face that takes requests and legs that carry them out. A humanoid host takes the order and hands the item to a quadruped runner — a two-robot service chain with no staff in the loop.
- **Hardware:** MagicBot Z1 **Development Version** (arm payload **2–3 kg**) + MagicDog EDU with an open basket. Optional substitute for the hand-over: a fixed Flexiv Rizon or Dobot cobot loading the basket (more reliable than humanoid grasping); OriginFlow or PICO teleoperation as operator fallback.
- **Architecture / stack:**
  - Perception: Z1 cameras or an external camera for item and basket position (fiducials recommended).
  - Planning: shared dispatch service (your own) with states *order → dog docks at pickup pose → load → deliver → return*; LLM dialogue on the Z1 side.
  - Control: Z1 arm motions via `magicbot-z1_sdk` (scripted pick-and-place of one known item); dog via ROS 2 nav as in Concept 1.
  - Compute: two wired control laptops on separate subnets (Z1 on 192.168.54.x, dog on 192.168.55.x) plus one dispatcher.
- **48-hour plan:**
  - **H0–6:** split team — dog bring-up (Concept 1 path) and Z1 SDK bring-up (stand, wave, speak, one arm trajectory).
  - **H6–24:** dog delivers reliably between two poses; Z1 executes a repeatable place-into-basket motion with a fixed item position.
  - **H24–40:** dispatcher links both; docking accuracy (the dog must stop within the arm's reach — use a mechanical guide or fiducial); dialogue.
  - **H40–48:** end-to-end runs; decide by H40 whether the hand-over is autonomous, teleoperated or done by a cobot.
- **3-minute demo script:** guest asks the Z1 for an item → Z1 confirms, dog trots to the counter → Z1 places item in basket → dog delivers and announces → both return to idle; close with the architecture slide showing the same dispatcher scaling to more runners.
- **Risks and fallbacks:** highest risk of the four. Z1 Development Version may not be available or manipulation may be too imprecise → replace hand-over with a cobot or a human "loader" and keep the Z1 as talking host. Dog docking error larger than arm tolerance → funnel-shaped basket. Two SDKs and two networks → start integration by H24 at the latest.
- **Judging angles:** *Innovation* high (heterogeneous team); *technical depth* high; *impact* plausible for hotels and clinics; *Leukerbad* good story, but only if it runs live.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| MagicDog EDU + **D-Robotics** RDK X5 | Untethered ROS 2 companion computer on the dog; on-board vision inference | Medium — ROS 2 distro and DDS match with the dog's Foxy-era stack must be tested ⚠️ |
| MagicDog + **SKYLANDX** MetaCam | Fast 3D scan of the venue as prior map / digital twin for route planning and ticket pins | Medium — dog localises in its own 2D map; alignment is manual |
| MagicDog + **XREAL** glasses | Operator or visitor AR view of robot status, route, incoming delivery | Low–medium — app talks to your dispatcher, not to the robot |
| MagicDog + **Flexiv** / **Dobot** / **ROKAE** arm | Automatic loading and unloading station (parcel locker, pharmacy counter) | Medium — fixed station, fiducial docking |
| MagicDog + **Galaxea** / **Galbot** / **UniX AI** wheeled manipulator | Manipulator picks and packs, quadruped does stairs and rough ground | High — two autonomy stacks, hand-over |
| MagicDog vs. **Unitree** Go2 / **Genisom** quadruped | Alternative base with the same concept; choose by SDK maturity and on-site support | n/a — decide early, do not mix |
| MagicBot Z1 + **Binabik AI** agent OS | Higher-level task agent on a humanoid | Unknown — ask both teams whether an adapter exists ⚠️ unverified |

## Questions to ask the Magiclab Robotics engineers on site

1. Which units are available to teams, and which **edition** (MagicDog EDU? Z1 Development Version?) — is low-level control unlocked?
2. Does `magicdog_ros2_sdk` (SLAM, `/goal_pose`, navigation modes) work on the firmware of these units, and on which ROS 2 distro? Does it also run on MagicDog-W?
3. Can we connect **wirelessly**, or must a computer be wired to the control board? Is there a payload power outlet (voltage, current) for a backpack computer?
4. How large a map can the built-in SLAM handle, and does it survive ramps, glass walls and moving crowds? Any multi-floor support?
5. Which languages does the TTS service support, and can we play arbitrary audio and read the microphone array stream?
6. What is the safe continuous payload on the back, where are the mounting points, and what happens to gait stability at 5 kg?
7. Is there any access to Magic-VLA K02, the fleet scheduling system or the T1 gripper interface during the event?
8. What are the limits for outdoor use this weekend (wet ground, snow, temperature), and who covers damage?

## Decision rule

- **Pick Magiclab Robotics for T01 if** a MagicDog EDU (or W / T1) with working ROS 2 navigation is confirmed at the booth and your idea is a navigation-centred service — delivery runner, guide, patrol-and-report — that stays indoors or on dry ground.
- **Avoid if** your concept needs robust manipulation, all-weather street operation or a well-documented community stack, or if only PRO / base editions without SDK access are on site.

## Sources
- [MagicDog product page](https://www.magiclab.top/en/dog)
- [MagicDog-W product page](https://www.magiclab.top/en/dog-w)
- [GitHub — magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk)
- [GitHub — magicdog_sdk](https://github.com/MagiclabRobotics/magicdog_sdk)
- [GitHub — magicbot-z1_sdk](https://github.com/MagiclabRobotics/magicbot-z1_sdk)
- [QbitAI — MagicLab at WRC 2026 (Chinese)](https://www.qbitai.com/2026/08/477155.html)
- [EqualOcean — MagicLab targets European logistics, Slovenia postal partnership](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)
- [Magiclab Robotics profile](../Magiclab.md)
