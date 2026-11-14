---
type: challenge-playbook
company: "ROKAE Robotics"
slug: ROKAE
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# ROKAE Robotics × T01 — Hackathon Playbook

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Brief](ROKAE-T01-1-Brief.md) · [Products and solutions](ROKAE-T01-2-Products-and-Solutions.md)

> **Before you pick a concept:** ask what ROKAE has on site (⚠️ unverified). Concepts 1–3 need only one small xMate cobot (SR3 / SR5 / CR7). Concept 4 needs a Helios.
> **Common stack facts:** `xCoreSDK` (C++ / Python / C#, Apache-2.0), real-time C++ up to **1 kHz** with Cartesian impedance; `rokae_ros2` on ROS 2 **Humble** / Ubuntu 22.04 with MoveIt 2 configs; controller must run xCore **v3.2.1+**. The cobot controller has no GPU — vision and planning run on your laptop or an edge board.

## Solution approaches

### Concept 1 — Unattended resort service kiosk (safest)

- **Problem → value:** small resorts cannot staff every desk around the clock. A robot kiosk hands out pre-ordered items (rental-locker key, bath towel pack, lift pass, pharmacy pick-up, hot drink) at any hour → longer service hours without extra staff. Builds directly on ROKAE's coffee / unmanned-catering cases.
- **Hardware:** xMate **SR5** (or SR3 / CR7) on a table · gripper (ask ROKAE; else Flexiv Grav or a simple parallel gripper) · RGB-D or USB camera · laptop. Optional: D-Robotics RDK X5 for on-device detection, XREAL glasses as the operator view.
- **Architecture / stack:** phone or QR order → small web app → task queue → camera detects item slot and guest hand-over zone (fiducials or a light detector) → MoveIt 2 (`rokae_ros2`) or taught waypoints via Python SDK → **Cartesian impedance hand-over** (release when the guest pulls, sensed as external force). Compute on laptop.
- **48-hour plan:**
  - **H0–6:** arm powered, SDK hello-world, gripper I/O, drag-teach one pick-and-hand-over path.
  - **H6–24:** order app, shelf with 4–6 slots, vision for slot occupancy, parametrised picks.
  - **H24–40:** force-based hand-over, speed limits and safety zone, error recovery (empty slot, dropped item), multilingual prompts (DE / FR / EN).
  - **H40–48:** 20 uninterrupted cycles, video backup, pitch.
- **3-minute demo script:** judge scans QR and orders "towel + locker key" → arm picks, presents, releases on a gentle pull → second judge blocks the arm by hand; arm yields and resumes → show the dashboard: orders served, cycle time, items left.
- **Risks and fallbacks:** no gripper supplied → 3D-print a hook / tray tool; vision flaky → fixed slots with fiducials; MoveIt setup slow → pure taught waypoints.
- **Judging angles:** *innovation* low-to-medium · *technical depth* in force-based hand-over · *impact* clear staffing story · *Leukerbad* off-hours spa / hotel / rental service.

### Concept 2 — Robotic hand-off dock for delivery robots (cross-vendor)

- **Problem → value:** delivery robots still need a human to load and unload them. A fixed arm at a "micro-hub" (hotel lobby, pharmacy, bakery) loads the right parcel into a quadruped or wheeled robot's cargo box → an end-to-end, human-free last-100-metres chain.
- **Hardware:** xMate **SR5 / CR7** (hub arm) + a delivery carrier from another vendor on site (Unitree Go2 / B2, AGIBOT D1, Genisom M1 / L1, Magiclab MagicDog) with a cargo box + camera at the hub. Optional: SKYLANDX MetaCam map of the venue for the carrier's route.
- **Architecture / stack:** order service assigns parcel + carrier → carrier navigates (its own stack) and parks at the dock → hub camera localises the cargo box (fiducial on the box, 6-DoF pose) → MoveIt 2 plans pick-from-shelf and place-in-box → **impedance-controlled insertion** tolerates centimetre-level parking error → "loaded" message releases the carrier. ROS 2 Humble topics or plain MQTT / HTTP between systems.
- **48-hour plan:**
  - **H0–6:** split team (arm / carrier / orchestration); arm picks from a shelf; carrier drives A→B by teleop.
  - **H6–24:** fiducial box localisation, compliant place; carrier waypoint navigation; message contract agreed and mocked.
  - **H24–40:** full loop with 3 parcels and 2 destinations; handle mis-parking (re-detect, or ask the carrier to re-dock).
  - **H40–48:** reliability runs, timing metrics, film a clean run.
- **3-minute demo script:** tablet order "pharmacy bag to Room 2" → quadruped trots to the dock → arm finds the box, loads the bag, taps the lid closed → quadruped delivers across the hall → show the log: zero human touches.
- **Risks and fallbacks:** carrier navigation unreliable → teleoperate the drive and keep the dock autonomous (the ROKAE part is the novel bit); box pose noisy → mechanical docking guide; two-vendor networking → single laptop as the bridge.
- **Judging angles:** *innovation* medium-high (closes a gap most delivery demos skip) · *technical depth* multi-robot handshake + compliant placement · *impact* real last-mile bottleneck · *Leukerbad* steep, car-light village where legged carriers make sense and the hubs are hotels and clinics.

### Concept 3 — Contact-rich facility upkeep cell (wipe, press, turn)

- **Problem → value:** public touchpoints (handrails, lift buttons, door handles, ticket machines, spa lockers) need frequent cleaning and operation; most service robots avoid contact. A force-controlled arm wipes curved surfaces with constant pressure and operates buttons / handles built for humans → hygiene and maintenance automation.
- **Hardware:** xMate **CR7** (IP67 arm, good for wet work) or SR5 · wiping tool with sponge on the flange · RGB-D camera · mock-up panel (handrail section, lift button panel, lever handle). Mobility optional: push-cart mount, a CMR if present, or another vendor's wheeled base.
- **Architecture / stack:** RGB-D point cloud → surface segmentation and coverage path → **real-time C++ Cartesian impedance** (low stiffness along the surface normal, target contact force ~5–10 N) at up to 1 kHz → coverage and force log as a "cleaning certificate". Button pressing: detect the button, approach, stop on force threshold.
- **48-hour plan:**
  - **H0–6:** real-time mode running; constant-force contact on a flat board; safety limits.
  - **H6–24:** point cloud → path on a curved rail; button detection and force-terminated press.
  - **H24–40:** lever-handle turn with compliance; coverage visualisation; UV-marker or dry-erase "dirt" for a visible before / after.
  - **H40–48:** tune, repeat, record.
- **3-minute demo script:** judge scribbles on the handrail → robot scans, wipes it clean with constant pressure → presses a lift button and turns a handle → screen shows the force trace and coverage map → judge pushes the arm mid-wipe; it complies, then continues.
- **Risks and fallbacks:** real-time networking issues (the docs have a troubleshooting section — use wired Ethernet, a dedicated NIC) → fall back to the SDK's non-real-time force-control commands; perception path weak → drag-teach the path and keep force control live.
- **Judging angles:** *innovation* medium · *technical depth* highest of the four (plays to ROKAE's core strength) · *impact* hygiene in clinics and spas · *Leukerbad* thermal baths and rehab clinics with heavy touch-surface traffic.

### Concept 4 — Helios hotel concierge and runner (most ambitious; only if Helios is on site)

- **Problem → value:** a mobile dual-arm robot fetches and delivers inside a hotel or clinic (luggage tag, towel, water, forgotten medication), opening doors and using the lift itself → one robot covers delivery plus light upkeep.
- **Hardware:** **Helios** (2 × 7-DoF arms at 5 kg, omni base 1.5 m/s, 2 × 3D LiDAR, head stereo camera, Orin / Thor compute, ~4 h runtime) with grippers. Optional: XREAL glasses for staff tasking; a second vendor's VLA only if ROKAE's interface allows external arm commands.
- **Architecture / stack:** speech or app request → LLM task planner (cloud or laptop) → skill library (navigate-to, pick, place, hand-over, press-button) → Helios SLAM navigation + arm control through its **ROS 2 / Python SDK** → on-board Jetson for perception. Interface details are not public — the first hours are discovery with ROKAE engineers.
- **48-hour plan:**
  - **H0–6:** get API access, map the hall, drive point-to-point, move one arm from code. **Go / no-go at H6:** if navigation or arm control is not scriptable, drop to Concept 1–3.
  - **H6–24:** pick from a table, hand-over skill, speech / app front end.
  - **H24–40:** chain a 3-step errand; add a lift-button or door-push skill; recovery behaviours.
  - **H40–48:** rehearse one errand until it works 4 of 5 times.
- **3-minute demo script:** "Helios, bring a towel to the guest at table 3" → drives to the shelf, picks, navigates around a person, hands over compliantly → on the way back presses a (mock) lift button → dashboard shows the plan and executed skills.
- **Risks and fallbacks:** undocumented API, 160 kg robot in a crowd (keep speed low, marshal the route), limited robot time shared between teams → pre-record a full run early; reduce to navigate + hand-over only.
- **Judging angles:** *innovation* medium (common concept, rarely shown working) · *technical depth* high if autonomous · *impact* strong hospitality / care staffing story · *Leukerbad* hotels and rehab clinics with elderly guests.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| ROKAE SR / CR + **Unitree / AGIBOT / Genisom / Magiclab quadruped** (separate robots) | Hub-and-carrier delivery (Concept 2) | **Low–medium** — message-level only |
| ROKAE SR + **D-Robotics RDK X5 / S100** | On-device detection next to the arm; no laptop in the kiosk | **Low** — SDK supports aarch64 Linux; check Ubuntu version match |
| ROKAE SR / AR + **WUJI Hand** | Dexterous operation of human interfaces (handles, switches) | **Medium** — flange adapter, power, separate hand SDK |
| ROKAE SR + **Flexiv Grav gripper** | Reliable grasping if ROKAE brings no gripper | **Low–medium** — mechanical adapter + I/O |
| ROKAE arm + **SKYLANDX MetaCam** | Fast 3D scan of the venue or of a surface to clean | **Low** — offline map / point cloud hand-off |
| ROKAE arm + **XREAL glasses** | AR operator view, remote supervision of an unattended kiosk | **Medium** — custom app |
| ROKAE **SR3** mounted on another vendor's wheeled base (Galaxea, coprod, AGIBOT) | A true mobile manipulator | **High** — mechanics, 48 VDC power, e-stop, calibration; needs both vendors' consent |
| ROKAE arm + **Galbot / Spirit AI / Galaxea VLA** | Learned grasping policy on a ROKAE arm | **High** — models are embodiment-specific; not a 48-hour bet |

## Questions to ask the ROKAE Robotics engineers on site

1. Which robots, controllers and **xCore firmware version** are here — and which SDK version (0.7.x, 0.7.x-AR, 0.8.x) matches them?
2. Is a **gripper, camera and flange adapter** included? Which gripper protocol (digital I/O, RS485)?
3. Is **real-time mode** (1 kHz, Cartesian impedance / torque) enabled on these units, and what network setup do you recommend?
4. Does the **Python SDK** expose real-time or force-control commands, or is that C++ only?
5. Is a Helios or CMR on site? If so: what is the **navigation and arm API** (ROS 2 topics / actions, Python calls), and can we send our own goals?
6. Can an SR arm run from a **48 VDC battery** on another vendor's base, and what is the peak current?
7. Which **safety settings** (collision sensitivity, speed and force limits, virtual walls) can we change ourselves for a demo with visitors nearby?
8. Is there any **iNex / VLA model or teleoperation data tool** we can try this weekend?

## Decision rule

- **Pick ROKAE Robotics for T01 if** your idea has a contact-rich manipulation step at its core (hand-over, loading, wiping, pressing, opening) and you are happy with a fixed station or with pairing it with another vendor's mobile robot — or a Helios is on site and its API is confirmed open by hour 6.
- **Avoid if** your concept is mainly outdoor navigation, street delivery, snow / terrain mobility or fleet routing, or if you need a ready-made service robot or pretrained policy out of the box.

## Sources
- [ROKAE Robotics profile (internal)](../ROKAE.md)
- [ROKAE — SR cobots](https://www.rokae.com/en/product/show/349/SR-Cobots.html)
- [ROKAE — xMate CR](https://www.rokae.com/en/product/show/545/xMateCR.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE — Mobile Manipulator CMR](https://www.rokae.com/en/product/show/599/Mobile-Manipulator-CMR.html)
- [ROKAE — Commercial Services application cases](https://www.rokae.com/en/case/208/Commercial-Services.html)
- [ROKAE SDK docs](https://docs.rokae.com/en/docs/SDK)
- [GitHub — RokaeRobot organisation](https://github.com/RokaeRobot)
- [GitHub — RokaeRobot/xCoreSDK-CPP](https://github.com/RokaeRobot/xCoreSDK-CPP)
- [GitHub — RokaeRobot/rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)
- [TechNode Global (PR Newswire) — Schaeffler Helios deployment, Oct 2026](https://technode.global/?p=996114)
