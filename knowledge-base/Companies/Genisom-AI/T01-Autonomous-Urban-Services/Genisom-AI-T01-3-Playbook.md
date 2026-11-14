---
type: challenge-playbook
company: "Genisom AI"
slug: Genisom-AI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Genisom AI × T01 — Hackathon Playbook

⬆ [Genisom AI profile](../Genisom-AI.md) · [Brief](Genisom-AI-T01-1-Brief.md) · [Products and solutions](Genisom-AI-T01-2-Products-and-Solutions.md)

**Before you commit (10 minutes at the booth):** which model is on site (L1 EDU / L1-W / L2 / M1), whether the EDU sensor kit and on-robot RoamerX are included, and whether you can send navigation goals by API. The concepts below state what changes with each answer.

**Common building blocks for all concepts**

| Block | What to use | Note |
|---|---|---|
| Base motion | `genisom_L1_sdk` (L1 series) or `genisom_robot_sdk` GEN2 (M1, L2) — C++, UDP | Write one small ROS 2 node that turns `/cmd_vel` into SDK velocity commands. Take control ownership first (app and SDK arbitrate). |
| Navigation | RoamerX Lite (ROS 2 Humble, Nav2, `/navigate_to_pose`) or the on-robot RoamerX | Lite real-robot bring-up is marked TODO in the README — ask for help early. |
| Simulation | MATRiX + `genisom_model` URDFs | Lets half the team work before robot time. Needs a GPU PC. |
| Compute | On-board Orin NX (L1 EDU) or 86 TOPS unit (L2); laptop over Ethernet / Wi-Fi for LLM calls and dashboard | Keep the safety-critical loop on board; cloud only for language and UI. |
| Safety | Walking pace only, one person holding the app / e-stop, marked demo lane | Legged robot near the public; no pedestrian-safety certification is published. |

## Solution approaches

### Concept 1 — "Bergträger": carry-and-follow porter with autonomous return

- **Problem → value:** Leukerbad guests (many elderly or in rehabilitation) haul luggage, shopping and spa bags up steep lanes and steps; hotels send staff with carts that cannot take stairs. A dog that follows the person with the load and then walks home alone saves staff trips and strain.
- **Hardware:** L2 or M1 Pro (GLUE / UWB following built in) — best case. Fallback L1 EDU with your own follower. Simple cargo basket or strapped crate (stay under **8 kg** on L1, **16 kg** on L2). Optional: D-Robotics RDK X5 for a separate person-tracking camera.
- **Architecture / stack:**
  - Perception: built-in GLUE following if exposed; otherwise depth camera + person detector / tracker on Orin NX, LiDAR for obstacle stop.
  - Planning: follow mode = keep 1.5–2 m behind target; return mode = Nav2 goal to "home" in a pre-built map (or GNSS breadcrumb replay outdoors as a simple fallback).
  - Control: `/cmd_vel` → SDK bridge. Phone web page with two buttons: "Follow me" / "Go home".
- **48-hour plan:**
  - H0–6: confirm robot and API; teleop via SDK; build `/cmd_vel` bridge; mount the basket; start follower in MATRiX.
  - H6–24: following working on the real robot at walking pace; map the demo route; first autonomous return.
  - H24–40: stairs or ramp segment; lost-target behaviour (stop, beep, wait); payload test; web UI.
  - H40–48: 10 full rehearsals, record a backup video, slides.
- **3-minute demo script:** (0:00) guest puts a suitcase-sized bag in the basket and taps "Follow me" → (0:30) walks a lane with a turn and a few steps, dog follows → (1:30) guest unloads, taps "Go home" → (1:45) dog returns alone to the start marker → (2:30) show map, trip log and "staff minutes saved" estimate.
- **Risks and fallbacks:** following API not exposed → own tracker, or UWB / AprilTag on the guest's jacket. Localisation fails → breadcrumb replay of the outbound path. Cold or wet with an L1 → run indoors (hotel corridor + staircase).
- **Judging angles:** innovation moderate; technical depth = tracking + autonomous return on stairs; impact = clear staff-time and accessibility story; Leukerbad relevance **high** (steep spa town, elderly guests).

### Concept 2 — "Stair-mile courier": point-to-point delivery where wheels stop

- **Problem → value:** the last 50 metres in an alpine village are steps, kerbs and snow. Pharmacy items, bakery orders or clinic supplies need a carrier that handles them. A legged courier closes the gap wheeled delivery robots leave.
- **Hardware:** L2 (preferred) or L1 EDU / L1-W. Lidded cargo box with a cheap servo latch on a microcontroller, powered from the robot's 12 V / 24 V expansion port. Optional: SKYLANDX MetaCam to pre-scan the route; a Flexiv, Dobot or ROKAE arm as a fixed loading station.
- **Architecture / stack:**
  - Perception: 3D LiDAR localisation against a point-cloud map (RoamerX: fast_gicp / ndt_omp); depth camera for close obstacles.
  - Planning: Nav2 (NavFn + MPPI) via `/navigate_through_poses`; a small order manager (FastAPI + SQLite) that turns "order → pick-up → drop-off" into waypoint sequences.
  - Control: SDK bridge; box unlocks only after the recipient scans a QR code or enters a PIN on their phone.
  - Compute: nav on board; order manager and dashboard on a laptop.
- **48-hour plan:**
  - H0–6: robot bring-up; record a LiDAR bag of the route; run RoamerX Lite in Gazebo / MATRiX with the same waypoint logic.
  - H6–24: map + localisation on the robot; first A → B run; build box and latch.
  - H24–40: order app, QR unlock, stairs segment, pedestrian stop-and-wait behaviour, live map dashboard.
  - H40–48: reliability runs, timing numbers, backup video.
- **3-minute demo script:** (0:00) judge orders on a phone → (0:20) staff (or fixed arm) loads the box, robot departs → (0:40) route with stairs and a person stepping in front (robot waits) → (2:00) arrival, QR scan, lid opens → (2:20) robot heads back; dashboard shows the trip and battery.
- **Risks and fallbacks:** RoamerX Lite hardware bring-up stalls → use the on-robot RoamerX through the app for navigation and keep your work on order logic and the box; or line / AprilTag following for the route. Latch fails → open tray. Map drift outdoors → shorten the route, add GNSS on open sections.
- **Judging angles:** innovation = legged last-metre logistics; technical depth = full pipeline (map, localise, plan, secure hand-over); impact = measurable trips per charge (L2: about 20 km range claimed); Leukerbad relevance high (pharmacy / clinic / chalet runs in winter).

### Concept 3 — "Ask-the-dog" guide: language-directed wayfinding and escort

- **Problem → value:** visitors and clinic patients need to find baths, clinics, bus stops and trailheads; signage is hard for people with low vision or limited mobility. The robot takes a spoken or typed request in the guest's language and leads at their pace.
- **Hardware:** M1 Pro (microphone + speaker built in) or L2; fallback L1 EDU + USB speakerphone. Optional: XREAL glasses for an overlay of the route and robot status; OriginFlow EMG band as a hands-free "stop / go" input ⚠️ unverified integration effort.
- **Architecture / stack:**
  - Perception: speech-to-text on the laptop or cloud; rear-facing camera / depth (or UWB) to measure distance to the guest.
  - Planning: LLM maps the request to one of N named waypoints ("thermal bath entrance", "reception") with tool calls; Nav2 executes; a pace controller slows or stops when the guest falls behind. Stretch: open-vocabulary goals with `genisom_vln` (needs a CUDA GPU; shown in MATRiX only).
  - Control: SDK bridge; spoken updates ("stairs ahead, eight steps").
- **48-hour plan:**
  - H0–6: bring-up; waypoint list of the venue; LLM tool schema; VLN baseline running in MATRiX on a GPU PC.
  - H6–24: map + named waypoints on the robot; voice in → goal out; basic leading.
  - H24–40: pace adaptation, multilingual prompts (DE / FR / EN), hazard announcements, optional AR view.
  - H40–48: rehearsals with a non-team "guest"; backup video.
- **3-minute demo script:** (0:00) judge asks in German for a destination → (0:15) robot confirms aloud and starts → (0:45) judge slows down, robot waits → (1:30) robot announces stairs, climbs, arrives → (2:15) second request typed in English with a vague goal ("somewhere to sit") resolved by the LLM.
- **Risks and fallbacks:** noisy hall breaks speech recognition → phone text input. LLM latency or no connectivity → small local model or fixed intent list. VLN on real robot is unproven → keep it as a simulator segment in the demo.
- **Judging angles:** innovation = natural-language interface on a legged guide; technical depth = LLM-to-Nav2 tool use + human-pace control; impact = accessibility and tourism; Leukerbad relevance high. Note overlap with T04 — frame it as a public service, not a care device.

### Concept 4 — "Legged relay": multi-robot delivery with arm hand-over and a fleet dispatcher

- **Problem → value:** real city logistics needs more than one robot: something loads, something carries over hard terrain, something hands over. Show a small heterogeneous fleet run by one dispatcher.
- **Hardware:** one or two Genisom dogs (any model) as terrain carriers + a manipulator from another vendor (Galaxea R1, Galbot G1, AGIBOT G1, or a fixed Flexiv / Dobot / ROKAE arm) for loading and hand-over. If the booth has an **M1 + TA01** and exposes its API, use it for the hand-over instead.
- **Architecture / stack:**
  - Perception: each robot localises in a shared map; AprilTag docking marker at the hand-over station for the last 30 cm.
  - Planning: central dispatcher (task queue, assignment by battery / payload / terrain class) → per-robot Nav2 goals; simulate extra dogs in MATRiX (multi-robot supported) so the dashboard shows a larger fleet than the physical one.
  - Control: Genisom SDK bridge per dog; the arm vendor's own SDK for pick and place; simple state machine for the hand-over handshake.
- **48-hour plan:**
  - H0–6: secure both vendors' hardware slots; agree on the map frame and hand-over station; dispatcher skeleton with simulated robots.
  - H6–24: dog waypoint navigation + tag docking; arm pick-and-place into the box on a parked dog.
  - H24–40: end-to-end relay; mixed real + simulated fleet in the dashboard; failure handling (re-assign task on timeout).
  - H40–48: rehearse the single best sequence; backup video.
- **3-minute demo script:** (0:00) two orders appear in the dispatcher → (0:20) arm loads the dog at the station → (0:40) dog takes the stairs route while a simulated second dog serves another order on screen → (1:50) dog docks at the drop-off; recipient or second arm unloads → (2:30) dispatcher view: tasks done, energy used, re-assignment after an injected failure.
- **Risks and fallbacks:** two vendor queues and two SDKs double the integration risk → fixed arm instead of a mobile manipulator; human hand-over if the arm slips. Docking accuracy → larger funnel-shaped box. If time runs out, fall back to Concept 2 plus the simulated fleet.
- **Judging angles:** innovation and technical depth highest (heterogeneous fleet, sim + real); impact = scalable service model; Leukerbad relevance moderate to high (hotel-to-chalet supply chain in winter).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Genisom dog + **SKYLANDX MetaCam** | Fast, accurate 3D pre-scan of the route as the navigation map | Low–medium (map format conversion to PCD; frame alignment) |
| Genisom L1 (base) + **D-Robotics RDK X5** | On-board perception compute and ROS 2 where no EDU kit is fitted | Medium (power from expansion port, Ethernet to robot, own sensors) |
| Genisom dog + **Flexiv / Dobot / ROKAE** fixed arm | Automated loading / unloading station | Medium (docking accuracy, handshake logic) |
| Genisom dog + **Galaxea R1 / Galbot G1 / AGIBOT G1** | Wheeled manipulator indoors, legged carrier outdoors — relay | High (two mobile platforms, shared map, two SDKs) |
| Genisom dog + **XREAL** glasses | Operator or guest AR view of route, status and camera | Low–medium (stream data to an Android XR app) |
| Genisom dog + **Unitree Z1** arm on the back | Mobile manipulation without TA01 | High ⚠️ unverified (mounting, power, payload on L1 is only 8 kg) |
| Genisom dog + **Binabik AI** / **coprod** stacks | Agent layer or modular interop on top of the dog | Unknown — ask both sides |

## Questions to ask the Genisom AI engineers on site

1. Which models and how many units are here, and how are robot hours allocated per team?
2. Can we send **navigation goals and saved waypoints by API** on the on-robot RoamerX (L2 / M1 / L1 EDU), or only through the app?
3. Is **GLUE following** triggerable and tunable (distance, speed) from the SDK? Do you have UWB tags to lend?
4. Is there a **Python binding or ROS 2 driver** for the current SDKs, or a ready `/cmd_vel` bridge? Is low-level joint control available on L1?
5. How do we read the **LiDAR point cloud and camera streams** on the EDU kit — ROS 2 topics on the Orin NX, or raw drivers?
6. What is the status of RoamerX Lite on real hardware (README says TODO)? Can you give us the `robot-forward` package and a working launch file for this robot?
7. What are the real limits for this weekend: max payload with a box on top, stairs with payload, snow / sub-zero use for the L1 family, runtime per battery and spare batteries / charger?
8. Is an **M1 + TA01 arm** available, and does TA01 have an API we can use?

## Decision rule

- **Pick Genisom AI for T01 if** your idea is about moving things or people's loads across stairs, slopes or snow, you have at least one C++ / ROS 2 developer, and the booth confirms an L2, M1 or sensor-equipped L1 EDU with usable navigation access.
- **Avoid if** your concept depends on manipulation, on a Python-only high-level API, or on smooth indoor service where a wheeled dual-arm platform does the whole job by itself.

## Sources

- [Genisom AI profile (internal)](../Genisom-AI.md)
- [Genisom L2 product page](https://www.genisomai.com/en/product-robot/L2)
- [Genisom L1-W product page](https://www.genisomai.com/en/product-robot/L1-W)
- [Genisom M1 product page](https://www.genisomai.com/en/product-robot/M1)
- [GENISOM AI at WAIC 2026 (company news, 2026-07-19)](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WAIC-2026)
- [GENISOM AI at WRC 2026 (company news, 2026-08-23)](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WRC-2026)
- [IROS 2026 press release via TNGlobal (2026-10-01)](https://technode.global/prnasia/genisom-ai-showcases-embodied-intelligence-and-debuts-worlds-first-industry-grade-educational-quadruped-at-iros-2026/)
- [genisom_roamerx_open (GitHub)](https://github.com/zsibot/genisom_roamerx_open)
- [genisom_robot_sdk (GitHub)](https://github.com/zsibot/genisom_robot_sdk)
- [genisom_L1_sdk (GitHub)](https://github.com/zsibot/genisom_L1_sdk)
- [genisom_vln (GitHub)](https://github.com/zsibot/genisom_vln)
- [matrix (GitHub)](https://github.com/zsibot/matrix)
