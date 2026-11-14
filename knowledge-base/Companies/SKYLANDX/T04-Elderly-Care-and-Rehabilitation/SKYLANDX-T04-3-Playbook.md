---
type: challenge-playbook
company: "SKYLANDX"
slug: SKYLANDX
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# SKYLANDX × T04 — Hackathon Playbook

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Brief](SKYLANDX-T04-1-Brief.md) · [Products and solutions](SKYLANDX-T04-2-Products-and-Solutions.md)

> **Read first:** SKYLANDX is a **2/5** fit — a mapping layer, not a care robot. Concept 1 works with the scanner alone; Concepts 2–4 need another vendor's robot. No SDK is public, so every concept below has an **offline-export path** (PLY / PCD / OBJ files) that does not depend on live API access. Thresholds and processing times quoted as targets are our planning assumptions, not SKYLANDX specs.

## Solution approaches

### Concept 1 — Discharge-ready home twin (fall-hazard and accessibility audit)

- **Problem → value:** before a rehab patient goes home, an occupational therapist should check the home for fall hazards — a visit that costs hours of travel in an alpine valley. One 10-minute walk-through with a scanner by a relative or Spitex nurse → measured 3D twin → automatic hazard list + remote walk-through for the therapist.
- **Hardware:** MetaCam Air 2 (or MetaCam Lite) + laptop. No robot needed.
- **Architecture / stack:**
  - *Perception:* scan → MetaCam Studio export (PLY / PCD) + Skyland Cloud 3DGS.
  - *Analysis (laptop, Python + Open3D):* fit floor plane → height-above-floor map → flag steps / thresholds, loose low objects on walking routes, narrow passages; slice at hip height → 2D occupancy grid → plan bed → bathroom → kitchen routes with a rollator / wheelchair footprint; report minimum clearance per route.
  - *Output:* web report with hazard markers on the point cloud / 3DGS (cloud viewer or SuperSplat), ranked fix list. Thresholds come from a configurable norm profile (e.g. Swiss barrier-free building standard SIA 500 — check the actual values with a therapist; do not hard-code from memory).
  - *Optional:* an LLM turns the hazard list into a plain-language letter for the family.
- **48-hour plan:**
  - H0–6: get a scanner, scan one room, confirm you can export a point cloud to your laptop; request sample data as backup.
  - H6–24: floor fit, height map, threshold / clutter detection, occupancy grid + footprint path planning on scan #1.
  - H24–40: stage a "before / after" room (rug, cable, chair in the path, then cleared); second scan; report UI; 3DGS viewer link.
  - H40–48: tune false positives, rehearse, record a backup video.
- **3-minute demo script:** (0:00) persona: 78-year-old leaving a Leukerbad rehab clinic after hip surgery. (0:30) time-lapse of the 5-minute scan. (1:00) open the twin; hazards light up: threshold, rug edge, 62 cm gap beside the bed. (1:45) rollator route to the bathroom turns red → remove the chair → re-scan result turns green. (2:30) therapist view in the browser + generated fix list.
- **Risks and fallbacks:** cloud 3DGS too slow → show the colorized point cloud only. Soft objects (rugs, cables) are near the < 1 cm noise floor → use the panorama images + a vision model for rug / cable detection, geometry for steps and widths. No scanner slot → use SKYLANDX sample data.
- **Judging angles:** *Innovation* — moderate (measured audit instead of a paper checklist). *Technical depth* — geometry pipeline + path planning with real footprints. *Impact* — fall prevention and faster discharge are easy to explain. *Leukerbad* — rehab clinics discharging to remote valley homes; also applicable to spa-hotel rooms for elderly guests.

### Concept 2 — Map-once ward for an assistive mobile manipulator

- **Problem → value:** a fetch-and-carry or medication-delivery robot loses hours on mapping each new ward. Scan the ward once, give the robot a metric prior map with named places ("room 3 bedside", "nurse station"), and spend the 48 hours on the care task itself.
- **Hardware:** MetaCam Air 2 + a wheeled dual-arm robot on site (Galaxea R1 family, Galbot G1, UniX AI Wanda or Spirit AI Moz1 — whichever team you can partner with). Optional: MetaCam Hub to mount the scanner on the robot.
- **Architecture / stack:**
  - *Path A (offline, safe):* point cloud → 2D occupancy grid (slice at the robot's LiDAR height) → load into the robot's own navigation stack (e.g. Nav2 map + the robot's localizer) → semantic waypoints picked in the 3D twin.
  - *Path B (live, needs staff support):* MetaCam on the robot streams pose over the Rosbridge-protocol WebSocket → bridge into the robot's TF / odometry. Relocalization against the prior scan is an official claim; how to trigger it is undocumented.
  - *Task layer:* the robot vendor's manipulation stack / VLA for pick and hand-over; voice or tablet request UI. Compute: robot onboard + laptop.
- **48-hour plan:**
  - H0–6: secure a robot partner; scan the demo area; confirm the robot's map format and coordinate conventions.
  - H6–24: occupancy-grid export and alignment with the robot's localizer; first waypoint navigation.
  - H24–40: one care task end-to-end (bring water bottle / medication box from station to bedside); add named places from the twin.
  - H40–48: reliability runs, fallback teleop for the grasp, video.
- **3-minute demo script:** (0:00) show the 3D twin with named places. (0:30) "Bring Mrs. M. her water" → robot plans on the scanned map. (1:15) robot drives, hands over. (2:15) move to a second, never-driven room: only a new scan was needed.
- **Risks and fallbacks:** frame / scale mismatch between scan and robot localizer → fall back to the robot's own SLAM map and use the SKYLANDX twin for the semantic layer and visualization only. No Hub or live API → Path A. The SKYLANDX contribution can look thin next to the robot — make "map once, deploy in a new ward in 30 minutes" the measured headline.
- **Judging angles:** *Innovation* — deployment speed, not a new robot skill. *Technical depth* — cross-vendor map hand-over. *Impact* — caregiver relief. *Leukerbad* — clinics and hotels with many similar rooms.

### Concept 3 — Night-round hazard patrol with change detection

- **Problem → value:** many falls happen at night on the way to the toilet; corridors collect wheelchairs, laundry carts and cables during the day. A robot carrying a scanner patrols after lights-out, compares against the "safe" baseline twin, and alerts staff to new obstacles and blocked exits.
- **Hardware:** MetaCam Air 2 on a quadruped or wheeled base (Unitree Go2, Genisom, AGIBOT D1, or a wheeled manipulator) via MetaCam Hub — or carried by hand to prove the pipeline first.
- **Architecture / stack:** baseline scan (day 1) → patrol scan → register both clouds (ICP in Open3D) → cloud-to-cloud distance → cluster new objects on or near the floor inside the walking corridor → classify with panorama crops + a vision model → push alert with location on the twin. Robot navigation uses the host robot's stack; SKYLANDX's "indoor safety patrol" use case is the official precedent (for cracks / leaks, not care).
- **48-hour plan:**
  - H0–6: baseline scan of a corridor; export; hand-carried second scan with staged obstacles.
  - H6–24: registration + change detection + floor-zone filter; alert UI.
  - H24–40: mount on a robot (if Hub + robot available); patrol route; live or post-patrol processing.
  - H40–48: thresholds, demo choreography, video.
- **3-minute demo script:** (0:00) baseline twin of the corridor, all green. (0:30) teammate leaves a rollator and a cable in the corridor. (1:00) robot (or operator) patrols. (2:00) dashboard shows two red markers with photos and "exit route narrowed to X cm". (2:40) staff clears, re-check green.
- **Risks and fallbacks:** post-processing takes too long for a "live" feel → use real-time preview / live point-cloud stream if staff provide it, else present as a nightly batch report. Robot mounting not possible → hand-carried patrol still proves the pipeline. People in the scan create false changes → patrol empty corridors. Quadrupeds near frail residents are a safety and acceptance issue — say so and prefer a slow wheeled base.
- **Judging angles:** *Innovation* — change detection on care corridors. *Technical depth* — registration, clustering, multi-modal classification. *Impact* — fall prevention, emergency-exit compliance. *Leukerbad* — clinics and hotels with night staffing shortages.

### Concept 4 — Real2Sim rehab room for assistive-robot rehearsal

- **Problem → value:** you cannot test a new assistive behaviour around frail patients. Turn the real therapy room into a simulation scene (LiDAR-measured mesh for physics, 3DGS for photorealistic camera views), rehearse and evaluate the robot's navigation / approach behaviour there, then run the same task in the real room.
- **Hardware:** MetaCam Air 2 or Lite + GPU laptop + one robot with a simulator model (e.g. Unitree G1 / Go2, Galaxea R1, AGIBOT — confirm with the vendor which simulation assets exist).
- **Architecture / stack:** scan → OBJ mesh (collision) + 3DGS PLY (rendering) → convert into your simulator (conversion is manual; no USD / Isaac export from SKYLANDX) → run the vendor's navigation or VLA policy in the twin → score safety metrics (minimum distance to bed / patient zone, path clearance, success rate) → replay in the real room. This is SKYLANDX's officially stated Real2Sim direction, including residential interiors.
- **48-hour plan:**
  - H0–6: scan; get mesh + 3DGS; pick the simulator the robot vendor already supports.
  - H6–24: mesh clean-up and import; robot spawns and navigates in the twin.
  - H24–40: evaluation harness with 2–3 care scenarios (approach bedside, pass a rollator user, dock at a chair); real-room run of one scenario.
  - H40–48: sim-vs-real side-by-side video.
- **3-minute demo script:** (0:00) split screen: real room / twin. (0:40) run 20 simulated bedside approaches, show the failure heat-map. (1:30) adjust the policy / parameters, failures drop. (2:10) the real robot performs the same approach in the real room.
- **Risks and fallbacks:** mesh quality or import eats the weekend → fall back to point-cloud-derived occupancy grid for 2D navigation rehearsal. 3DGS rendering inside the simulator is advanced → use it only as a visual layer in the video. Highest risk concept; do not start it without a GPU laptop and a simulator-savvy teammate.
- **Judging angles:** *Innovation* — highest of the four. *Technical depth* — strong. *Impact* — indirect (safer deployment). *Leukerbad* — scene is a real local rehab room.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| SKYLANDX + Galaxea / Galbot / UniX AI / Spirit AI | Prior map + named places for fetch-and-carry or medication delivery (Concept 2) | Medium — map format and frame alignment |
| SKYLANDX + Unitree Go2 / Genisom / AGIBOT D1 | Robot-carried night-round scan (Concept 3) | Medium–high — needs MetaCam Hub or a custom mount, power, live data |
| SKYLANDX + XREAL | AR overlay of hazards or a walking-therapy route in the scanned room; remote therapist "visits" the twin | High — aligning the glasses' tracking frame with the scan is unsolved out of the box |
| SKYLANDX + D-Robotics RDK | Edge box running the audit / change-detection pipeline next to the scanner | Low–medium — file hand-over; live stream needs API access |
| SKYLANDX + Binabik AI / Genisom SomaMind | Agent layer that reasons over a scene graph built from the twin ("where is a safe place to put the walker?") | High — scene-graph extraction is yours to build |
| SKYLANDX + Flexiv / ROKAE / Dobot arm | Scan gives the fixed arm's workcell geometry (bed, chair) for collision-aware physio / assist motions | Medium — static scene only; the person is not in the scan |
| SKYLANDX + OriginFlow | Twin of the therapy room as the context for EMG-captured rehab exercises | High, loosely coupled — little technical synergy |

## Questions to ask the SKYLANDX engineers on site

1. Which units are available to teams (Air 2, Lite, Air 3, C01, MetaCam Hub), how many, and for how long per slot?
2. Can we get the Rosbridge-protocol WebSocket endpoint documentation today — topics, message types, rates, ROS 1 vs ROS 2?
3. How long does a ~100 m² indoor scan take to process into a colorized point cloud and into a 3DGS scene, and does it need the venue internet?
4. Can a second scan be relocalized into the coordinate frame of the first automatically (for change detection), and is that exposed to us?
5. Do exports include camera poses and panoramas so we can run our own vision models and project detections into 3D?
6. Is there a way to export a 2D floor plan / occupancy grid directly, or do we slice the point cloud ourselves?
7. How does the SLAM handle people walking through the scene, glass doors, mirrors and wet shiny bathroom tiles?
8. Where is cloud data stored and can faces be blurred — what can we tell a clinic about privacy?

## Decision rule

- **Pick SKYLANDX for T04 if** your idea is about the *environment* of care — a home or ward safety audit, a prior map that gets another vendor's assistive robot working fast, or a simulation twin — and you can work from exported files without a documented SDK.
- **Avoid if** your idea needs to physically help or monitor a person (manipulation, force-controlled contact, fall detection, exoskeleton, EMG), or if nobody on the team is comfortable with point-cloud processing.

## Sources
- [SKYLANDX — Robotics & Physical AI (industry page)](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Spatial Perception Robots](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — MetaCam Air 2](https://skylandx.com/metacam-air-2/)
- [SKYLANDX — MetaCam Lite](https://skylandx.com/metacam-lite/)
- [SKYLANDX — C01 LiDAR](https://skylandx.com/c01-slam-lidar/)
- [SKYLANDX — Software platforms](https://skylandx.com/software-platforms/)
- [SKYLANDX — Game & XR (industry page)](https://skylandx.com/industry/game-xr/)
- [SKYLANDX company profile (this repo)](../SKYLANDX.md)
- Third-party tools (links checked, pages not analysed in depth): [Open3D](https://github.com/isl-org/Open3D) · [CloudCompare](https://www.cloudcompare.org/) · [rosbridge_suite](https://github.com/RobotWebTools/rosbridge_suite) · [Nav2](https://github.com/ros-navigation/navigation2) · [SuperSplat](https://github.com/playcanvas/supersplat)
- Note: web search was unavailable during this write-up (budget exhausted); findings rest on official SKYLANDX pages fetched on 2026-11-14 and the company profile.
