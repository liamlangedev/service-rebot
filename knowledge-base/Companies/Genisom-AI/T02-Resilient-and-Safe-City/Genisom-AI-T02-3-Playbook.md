---
type: challenge-playbook
company: "Genisom AI"
slug: Genisom-AI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Genisom AI × T02 — Hackathon Playbook

⬆ [Genisom AI profile](../Genisom-AI.md) · [Brief](Genisom-AI-T02-1-Brief.md) · [Products and solutions](Genisom-AI-T02-2-Products-and-Solutions.md)

**Before you commit (first 30 minutes at the booth):** which model is on site, whether you get camera and LiDAR data out of it, and whether the on-robot RoamerX navigation is usable. Every concept below has a path that works with **velocity commands + odometry + your own camera** only, because that is all the public SDK READMEs confirm.

| # | Concept | Ambition | Needs from the robot |
|---|---|---|---|
| 1 | Patrol-and-alert dog | Safest | Velocity control, odometry |
| 2 | First-look scout after an incident | Medium | Same + 3D mapping (on-board LiDAR or SKYLANDX scanner) |
| 3 | Language-tasked search dog | Medium–high | Same + camera feed to a VLM |
| 4 | Mixed-fleet incident command with AR | Most ambitious | Two or more robots, shared map |

## Solution approaches

### Concept 1 — Patrol-and-alert dog
- **Problem → value:** small resorts cannot staff night or off-season patrols of promenades, car parks, clinic grounds and technical rooms. A quadruped walks a fixed loop, spots anomalies (person lying down, blocked escape route, open door, standing water) and sends a geotagged alert with a photo — responders know *what* and *where* before leaving the station.
- **Hardware:** Genisom L2 or M1 if on site (weather-rated); otherwise Genisom L1 EDU indoors or in dry conditions. Optional: USB camera on the payload rail (12 V / USB interfaces); D-Robotics RDK X5 as an on-board inference box.
- **Architecture / stack:**
  - *Perception:* camera frames → open-vocabulary or YOLO-class detector + a small VLM for a one-line incident description. Runs on a laptop over Wi-Fi, or on the L1 EDU's Orin NX / an RDK board.
  - *Planning:* waypoint loop. Option A: the robot's own RoamerX (ask whether route / checkpoint patrol is exposed). Option B: RoamerX Lite on ROS 2 Humble (real-hardware bring-up is marked "TODO" in the repo — budget for it). Option C: odometry + fiducial markers at checkpoints.
  - *Control:* `genisom_L1_sdk` (`SetRemote` velocity, stand, modes) or `genisom_robot_sdk` (M1 / L2, UDP 8082), wrapped in a thin bridge process that your Python or ROS 2 code calls.
  - *Output:* web dashboard with map, live pose, alert cards (photo, time, position, description).
- **48-hour plan:**
  - H0–6: confirm model, take SDK control, read odometry / battery, drive from code. Build the SDK-to-Python (or ROS 2) bridge. Start the detector on recorded phone video.
  - H6–24: waypoint loop working on the real floor (start with Option C). Dashboard skeleton. Camera mounted and streaming.
  - H24–40: integrate detection → alert → dashboard. Add a "go to checkpoint N and look" command. Record a backup video.
  - H40–48: tune three staged anomalies, rehearse, freeze the code.
- **3-minute demo script:** (0:00) one-sentence problem. (0:20) dog starts its loop; dashboard shows pose. (1:00) teammate lies down on the route → dog stops, alert appears with photo and text. (1:40) operator sends the dog to a second checkpoint; a blocked exit is flagged. (2:20) show battery / runtime numbers and how the same loop would run overnight. (2:45) what a real deployment needs next.
- **Risks and fallbacks:** no camera access through the SDK → own USB camera or phone. Navigation unreliable → teleoperate the route and keep detection fully autonomous. Wi-Fi drops → run inference on board. Control-ownership conflict with the phone app → read the SDK's take-control example first and keep one person in charge of the app.
- **Judging angles:** *Innovation* low–medium (well-known pattern). *Technical depth* comes from closing the loop reliably. *Impact* clear and easy to explain. *Leukerbad* night patrol of spa, clinic and car-park areas with few staff.

### Concept 2 — First-look scout after an incident
- **Problem → value:** after a rockfall, avalanche, flood or partial collapse, the first question is "what changed and is it safe to send people?". The robot walks in, captures the scene in 3D and highlights differences against a baseline scan, so the incident lead decides from a map instead of sending a person.
- **Hardware:** Genisom M1 or L2 (rated to −20 °C; the M1 page shows snow, ice and shallow-water tests). L1 EDU works for an indoor mock-up. Plus SKYLANDX MetaCam for the baseline scan (and as the mapping sensor if robot LiDAR data is not accessible).
- **Architecture / stack:**
  - *Perception:* baseline point cloud of the area (MetaCam, before). Second cloud after the "incident" (robot LiDAR through RoamerX mapping, or MetaCam strapped to the robot — check weight against the **8 / 16 / 30 kg** payload of L1 / L2 / M1).
  - *Processing:* register the two clouds (ICP / GICP), compute cloud-to-cloud distance, cluster changes, label them (new obstacle, missing structure, blocked passage). Laptop with GPU optional.
  - *Planning / control:* teleoperated or waypoint drive through the SDK; operator sees the robot camera.
  - *Output:* 3D viewer with change heat-map + a short auto-generated situation report.
- **48-hour plan:**
  - H0–6: confirm LiDAR access or the MetaCam route. Scan the demo area as baseline. Drive the robot from code.
  - H6–24: second scan pipeline end to end on a laptop (record → export → register → diff). Build the staged "incident" (boxes, a barrier, a tipped shelf).
  - H24–40: viewer and report. Speed up the loop so scan-to-map takes minutes. Rehearse the drive.
  - H40–48: polish, backup dataset, demo run-throughs.
- **3-minute demo script:** (0:00) the question responders ask. (0:20) show the baseline twin. (0:40) "incident" happens; robot is sent in while people stay back. (1:30) new scan arrives; changed regions light up red; blocked route is marked. (2:20) situation report on screen. (2:40) how this maps to a road gallery or cable-car station.
- **Risks and fallbacks:** live registration too slow → pre-record the "after" scan and replay it while the robot drives. No LiDAR access → MetaCam on the robot or hand-carried for the baseline only, with camera-based change detection on the robot. Slippery or uneven mock-up terrain → keep it on flat ground and argue terrain capability from the published ratings.
- **Judging angles:** *Innovation* medium (digital-twin diff for responders). *Technical depth* 3D registration and change detection. *Impact* keeps responders out of unstable areas. *Leukerbad* rockfall, avalanche and flood risk on mountain access routes and infrastructure.

### Concept 3 — Language-tasked search dog
- **Problem → value:** a missing guest or patient (think elderly spa or clinic visitor) has to be found fast in a building or grounds. The incident lead types or says "find a person in a red jacket near the lower entrance"; the dog searches, confirms with a photo and opens a two-way voice link or plays a reassurance message.
- **Hardware:** Genisom L1 EDU (Orin NX, depth camera) or L2 / M1 Pro (the Pro variant lists voice dialogue and broadcasting). Optional: OriginFlow or XREAL for the operator interface; a USB speaker / microphone on the payload rail.
- **Architecture / stack:**
  - *Perception:* camera → VLM for goal matching and scene description; person detector for robust "person found". Start from [genisom_vln](https://github.com/zsibot/genisom_vln) (UniGoal-based zero-shot baseline; supports SmolVLM2, Ollama models or a cloud VLM).
  - *Planning:* frontier exploration or a room-by-room waypoint list; the VLM picks the next room from a text map.
  - *Control:* SDK velocity commands through the same bridge as Concept 1.
  - *Compute:* VLM on a GPU laptop or a cloud API; detector on board.
  - *Sim first:* develop in MATRiX while waiting for robot time; the VLN repo targets MATRiX directly.
- **48-hour plan:**
  - H0–6: run genisom_vln in MATRiX on one laptop; in parallel take SDK control of the real robot and get camera frames.
  - H6–24: port the perception → goal loop to the real robot with a simple room-waypoint explorer. Person detector live.
  - H24–40: voice or text mission input, "found" event with photo and position, audio message to the person. Dashboard.
  - H40–48: three rehearsed search missions with different descriptions; backup video.
- **3-minute demo script:** (0:00) missing-person scenario. (0:20) operator gives the description in plain language. (0:40) dog explores; screen shows what the VLM "thinks". (1:40) person found; photo and location pushed; dog sits and plays the message. (2:20) second query with a different target to show it is not scripted. (2:45) limits and next steps.
- **Risks and fallbacks:** VLM latency or hallucination → gate every "found" with the person detector and operator confirmation. Sim-to-real port of the VLN stack takes too long → keep VLN in MATRiX as the "brain" demo and run detector-only search on the real robot. Exploration unreliable → fixed room list.
- **Judging angles:** *Innovation* high (language-driven search on a legged robot). *Technical depth* VLM + navigation integration. *Impact* faster location of vulnerable people. *Leukerbad* many elderly guests and clinic patients; also overlaps with T04.

### Concept 4 — Mixed-fleet incident command with AR
- **Problem → value:** in a real incident several robots from different makers will be on scene. Show one command view where a responder wearing AR glasses sees every robot's pose, video and findings on a shared map and assigns sectors with a gesture or voice.
- **Hardware:** one or two Genisom quadrupeds + a second vendor's robot (Unitree Go2 or Magiclab MagicDog) + XREAL glasses for the operator. Optional SKYLANDX scan as the shared map.
- **Architecture / stack:**
  - *Common layer:* a small ROS 2 (or plain MQTT / WebSocket) fleet bus with a per-vendor adapter: Genisom adapter wraps the C++ SDK; each robot publishes pose, battery and detections and accepts "go to" or velocity goals.
  - *Perception:* each robot runs the Concept 1 detector.
  - *Planning:* sector assignment (simple area split) + re-assignment when a robot reports low battery or a fault (Genisom SDKs expose battery and fault data).
  - *Operator view:* XREAL app or web view rendered to the glasses: map, robot icons, alert cards.
  - *Sim:* MATRiX supports multi-robot simulation — use it to test the coordination logic.
- **48-hour plan:**
  - H0–6: agree on the message schema; one person per vendor adapter; confirm a shared coordinate frame (fiducials or a common scan).
  - H6–24: both robots report pose on one map and accept goals. Coordination logic running in simulation.
  - H24–40: AR / web command view; sector assignment and battery-triggered hand-over on real robots.
  - H40–48: one clean scripted scenario, backup video, rehearsal.
- **3-minute demo script:** (0:00) why mixed fleets matter. (0:20) operator puts on the glasses; two robots appear on the map. (0:50) operator assigns sectors; both start. (1:40) one robot flags a casualty; the other is redirected to bring a first-aid pouch or act as a relay. (2:20) simulated low battery → automatic hand-over. (2:45) how more vendors plug in.
- **Risks and fallbacks:** shared localisation is the hard part → use fiducials and a small arena. Two SDKs to learn → drop to one real robot plus simulated teammates in MATRiX. AR app not ready → tablet view.
- **Judging angles:** *Innovation* high (vendor-neutral response fleet). *Technical depth* highest of the four. *Impact* interoperability is a real gap for civil protection. *Leukerbad* a small municipality would pool whatever equipment partners bring.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Genisom quadruped + SKYLANDX MetaCam | Baseline 3D scan as prior map / digital twin; change detection after an incident | Low–medium (offline point clouds; live on-robot mount is harder) |
| Genisom quadruped + D-Robotics RDK X5 / S100 | On-board detection without depending on Wi-Fi or on access to the robot's own compute | Low (USB camera + Ethernet / 12 V from the payload interfaces) |
| Genisom quadruped + XREAL glasses | Hands-free operator view: robot video, map and alerts | Medium (stream + simple overlay app) |
| Genisom quadruped + Unitree Go2 or Magiclab MagicDog | Vendor-neutral fleet coordination | High (two SDKs, shared localisation) |
| Genisom quadruped + OriginFlow EMG input | Gesture-based control when hands are gloved or busy | Medium–high (unknown API; ask OriginFlow) |
| Genisom scout + Galaxea / Galbot / AGIBOT mobile manipulator | Scout finds the problem, manipulator acts (close a valve, hand over supplies) | High (two-stage mission, indoor flat floor only for the manipulator) |
| Binabik AI or coprod stack + Genisom robot | Agent / orchestration layer on top of the Genisom SDK | Unknown — confirm with those teams that a C++ / UDP robot can be wrapped quickly |

## Questions to ask the Genisom AI engineers on site
1. Which models and how many units are here (L1, L1 EDU, L1-W, L2, M1)? Any spare batteries or a charging dock?
2. Can we read **camera frames and LiDAR point clouds** from our own code? Through which interface (ROS 2 topics on the on-board computer, RTSP, SDK callbacks)?
3. Is the on-robot RoamerX (full version) installed, and can we send it map / waypoint / patrol goals programmatically? Has anyone run RoamerX Lite on real hardware?
4. Do we get shell access to the on-board computer (Orin NX on L1 EDU, the L2 compute)? Can we install our own packages?
5. Does the current SDK offer Python bindings or low-level joint control, or only the high-level C++ API?
6. What are the velocity limits and the safe way to take and release control from the phone app? Is there a hardware or software emergency stop we must use?
7. May we run the robot outdoors here (snow, wet ground, sub-zero)? Any limits you want us to respect for the L1's 0–40 °C / IP54 rating?
8. Are any payloads available — thermal camera, speaker / microphone, light, UWB tag for following? Mounting rail dimensions and available power (12 V / 24 V, current limit)?

## Decision rule
- **Pick Genisom AI for T02 if** you want a rugged legged platform for a patrol, scout or search mission, your team is comfortable wrapping a C++ / UDP SDK, and the booth confirms either sensor-stream access or you bring your own camera.
- **Avoid if** your idea needs manipulation, joint-level control, a ready-made thermal / gas payload, or a Python-first robot API on day one — or if only L1-class units are on site and your demo must run outdoors in snow.

## Sources
- [Genisom AI — Emergency Response industry page](https://www.genisomai.com/en/industry/emergency-response)
- [Genisom AI — Security Patrol industry page](https://www.genisomai.com/en/industry/security-patrol)
- [Genisom AI — Industrial Inspection industry page](https://www.genisomai.com/en/industry/industrial-inspection)
- [Genisom M1 product page](https://www.genisomai.com/en/product-robot/M1)
- [Genisom L2 product page](https://www.genisomai.com/en/product-robot/L2)
- [genisom_L1_sdk (GitHub)](https://github.com/zsibot/genisom_L1_sdk)
- [genisom_robot_sdk (GitHub)](https://github.com/zsibot/genisom_robot_sdk)
- [genisom_roamerx_open (GitHub)](https://github.com/zsibot/genisom_roamerx_open)
- [genisom_vln (GitHub)](https://github.com/zsibot/genisom_vln)
- [matrix — MATRiX simulator (GitHub)](https://github.com/zsibot/matrix)
- [GENISOM AI at IROS 2026 (PR Newswire, 2026-10-01)](https://www.prnewswire.com/news-releases/genisom-ai-showcases-embodied-intelligence-and-debuts-worlds-first-industry-grade-educational-quadruped-at-iros-2026-302896049.html)
- [Genisom AI company profile (this repository)](../Genisom-AI.md)
