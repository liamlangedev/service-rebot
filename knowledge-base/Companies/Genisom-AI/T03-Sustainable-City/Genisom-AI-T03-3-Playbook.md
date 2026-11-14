---
type: challenge-playbook
company: "Genisom AI"
slug: Genisom-AI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Genisom AI × T03 — Hackathon Playbook

⬆ [Genisom AI profile](../Genisom-AI.md) · [Brief](Genisom-AI-T03-1-Brief.md) · [Products and solutions](Genisom-AI-T03-2-Products-and-Solutions.md)

**Starting point:** a Genisom quadruped is a legged sensor carrier with open power / data rails and a C++ high-level SDK. Every concept below is "walk a route, sense, decide, report" — manipulation only appears where a second vendor supplies the arm. Which Genisom models are on site is ⚠️ unverified; each concept names a fallback.

**Do these three things in the first hour, whatever you build:**
1. Confirm model, firmware and SDK generation (L1 SDK vs GEN2 for M1 / L2).
2. Run the read-only SDK example and print battery telemetry.
3. Ask whether the on-robot RoamerX accepts waypoint goals from your laptop.

## Solution approaches

### Concept 1 — Energy-waste patrol (safest)
- **Problem → value:** Hotels, spas and clinics lose heat through open windows, uninsulated pipes and doors left open; nobody walks the building to check. A robot round finds and geotags the losses so staff fix the biggest ones first.
- **Hardware:** L1 EDU (indoor) or L2 (outdoor facades) · a thermal camera you bring or borrow (USB) — none confirmed from Genisom on site · fallback: on-board RGB / depth camera only.
- **Architecture / stack:**
  - Perception: thermal frames → simple hot-spot / gradient threshold; RGB frames → a VLM or open detector for "open window", "lights on, room empty", "door ajar".
  - Planning: fixed waypoint loop (on-robot RoamerX, or teleop-recorded path replayed with odometry as fallback).
  - Control: high-level velocity commands via `genisom_L1_sdk` or GEN2 SDK over UDP.
  - Compute: Orin NX on the L1 EDU for detection; laptop for dashboard; cloud VLM optional.
  - Output: map with pins, photo evidence, rough ranking (large / medium / small loss). Do not claim kWh savings you cannot measure.
- **48-hour plan:**
  - H0–6: SDK hello-world, camera stream access, mount sensor, pick a 30–50 m loop.
  - H6–24: map the loop, get repeatable waypoint patrol, thermal + RGB detectors working on recorded data.
  - H24–40: integrate live; dashboard; log battery current to report **Wh per patrol**.
  - H40–48: stage 3–4 "planted" faults (open window, warm kettle as pipe leak), rehearse, record backup video.
- **3-minute demo script:** 0:00 problem in one sentence → 0:20 dog starts loop → 1:00 stops at planted heat source, thermal overlay on screen → 1:40 flags open window → 2:15 dashboard with ranked findings and energy used by the patrol → 2:40 scale-up: every hotel corridor in Leukerbad nightly.
- **Risks and fallbacks:** no thermal camera → RGB + VLM only · navigation not ready → teleoperate the route, keep detection autonomous · Wi-Fi congestion → run everything on Ethernet tether / on-board.
- **Judging angles:** innovation: modest · technical depth: sensor fusion + autonomy loop · impact: building energy is a large, measurable cost · Leukerbad: thermal-spa and clinic buildings with year-round heating demand.

### Concept 2 — Litter and bin-fill scout
- **Problem → value:** Collection crews drive fixed rounds whether bins are full or not, and litter on stairs and footpaths is found by chance. A scout robot reports fill levels and litter hot-spots so collection is done on demand — fewer vehicle kilometres.
- **Hardware:** L2 or L1-W preferred outdoors; L1 EDU if dry and above 0 °C · on-board cameras + GNSS · no extra sensor needed.
- **Architecture / stack:**
  - Perception: open-vocabulary detector or VLM on camera frames → litter class and bin state (empty / half / overflowing); depth camera for rough size.
  - Planning: patrol route; findings geotagged with GNSS outdoors or map pose indoors; a small routing script (nearest-neighbour or OR-tools) outputs the pickup order.
  - Control: SDK velocity or RoamerX goals.
  - Compute: on-board for detection, laptop for map and routing.
- **48-hour plan:**
  - H0–6: SDK, camera stream, choose a route with 3–5 bins.
  - H6–24: detector prompt / fine-tune on photos you take on site; geotag pipeline.
  - H24–40: patrol integration, map UI, "pickup list" generator, compare route length full-round vs on-demand.
  - H40–48: rehearsal with staged litter; backup video.
- **3-minute demo script:** dog walks route → live detections on screen → map fills with pins → "today's pickup list: 2 of 5 bins, 4 litter spots" → route-length comparison.
- **Risks and fallbacks:** detector false positives in snow → restrict classes, show confidence · GNSS poor between buildings → use LiDAR localisation · outdoor not permitted → indoor mock street.
- **Judging angles:** innovation: medium · technical depth: perception + routing · impact: clear emissions and labour argument · Leukerbad: tourist footpaths, stairs and steep lanes that sweepers cannot reach.

### Concept 3 — Scout-and-pick team (cross-vendor)
- **Problem → value:** Closing the loop from "found" to "removed and sorted". The quadruped covers terrain cheaply; a manipulator only moves when there is something to pick.
- **Hardware:** Genisom dog as scout · a mobile manipulator from another vendor (Galaxea R1, Galbot G1 or AGIBOT G1) or a fixed arm cell (Dobot / Flexiv) as the sorting station · if the booth confirms an **M1 + TA01 arm**, a single-vendor version becomes possible (TA01 specs not public).
- **Architecture / stack:**
  - Dog: Concept 2 pipeline publishes `{class, pose, photo}` over a shared message bus (ROS 2 topic or plain MQTT / HTTP).
  - Manipulator: receives the task, navigates, grasps with its own VLA / grasp model, drops into the correct bin.
  - Shared frame: one common map (SKYLANDX scan or the dog's LiDAR map) or fiducial markers to align the two robots.
  - Compute: each robot runs its own stack; a laptop hosts the task queue.
- **48-hour plan:**
  - H0–6: agree the message format; both sub-teams get hello-world on their robot.
  - H6–24: dog detection + pose; arm picks 3 object classes from a known spot.
  - H24–40: frame alignment, end-to-end hand-off, sorting rule (PET / can / paper).
  - H40–48: reduce to the most reliable 2 objects; rehearse; backup video.
- **3-minute demo script:** dog finds a can and a bottle → tasks appear in queue → manipulator drives over, picks, sorts → counter shows items recovered and manipulator distance saved versus blind search.
- **Risks and fallbacks:** two robots = two failure chains; frame alignment drifts → use AprilTags · manipulator unavailable → dog carries a collection basket to a fixed arm cell, or a human does the pick and you demo the dispatch · high integration load: needs 4+ people.
- **Judging angles:** innovation: heterogeneous team · technical depth: high · impact: full workflow · Leukerbad: works on mixed terrain where a single wheeled robot cannot.

### Concept 4 — Language-tasked resource auditor with scan-to-sim twin (most ambitious)
- **Problem → value:** Facility managers want to ask "where are we wasting heat / water / light on level 2?" and get an evidence-backed answer, without programming routes.
- **Hardware:** L1 EDU or L2 · SKYLANDX MetaCam scan of the venue · optional thermal camera · optional XREAL glasses to view findings in place.
- **Architecture / stack:**
  - Twin: scan → 3DGS scene → import into MATRiX (3DGS import is a listed feature; the exact workflow is ⚠️ unverified — test it early).
  - Tasking: LLM turns the question into a checklist of places and objects; `genisom_vln` baseline (zero-shot, VLM-based) or plain waypoint navigation takes the robot there.
  - Rehearsal: run the whole mission in MATRiX first (it simulates RGB, infrared, depth, LiDAR).
  - Report: findings written back onto the twin; natural-language summary.
  - Compute: VLN baseline recommends a strong GPU for local models; use Ollama on a laptop GPU or a cloud API. Real-robot use of the VLN repo is not documented.
- **48-hour plan:**
  - H0–6: scan the space; install MATRiX and run the stock demo; SDK hello-world.
  - H6–24: scene import attempt (hard stop at H16 — fall back to a stock map); LLM checklist → waypoint list; detectors from Concept 1.
  - H24–40: sim mission end to end, then the same mission on the robot.
  - H40–48: polish the split-screen sim / real story; backup video.
- **3-minute demo script:** type a question → plan appears → split screen: simulated run and real dog doing the same route → findings pinned on the twin → spoken summary.
- **Risks and fallbacks:** 3DGS import or VLN on hardware fails → keep LLM-to-waypoints and show the twin as a viewer only · scope creep → Concept 1 is the built-in fallback.
- **Judging angles:** innovation: high · technical depth: sim-to-real + language tasking · impact: lowers the skill needed to run audits · Leukerbad: one twin of a spa or clinic building reused for energy, water and maintenance.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Genisom dog + **D-Robotics RDK** board | Low-power sensor / inference box on the dog's power rail; "low-power edge AI" story with measured watts | Low–medium (USB / Ethernet; check supply voltage and current) |
| Genisom dog + **SKYLANDX MetaCam** | Fast 3D map of the venue for localisation, twin and findings overlay | Medium (map format conversion to PCD / 3DGS) |
| Genisom dog + **Galaxea / Galbot / AGIBOT G1** mobile manipulator | Scout finds, manipulator picks and sorts (Concept 3) | High (two stacks, shared frame) |
| Genisom dog + **Dobot / Flexiv** fixed arm | Dog as carrier bringing items to a sorting cell | Medium (hand-off fixture; dog has no arm to unload) |
| Genisom dog + **XREAL** glasses | Technician sees heat-leak pins in place | Medium (pose alignment) |
| Genisom dog + **Unitree Z1** or other small arm on an M1 | Single mobile unit that picks | High (mounting, power, payload balance; only if M1 is on site) |

## Questions to ask the Genisom AI engineers on site
1. Which models and how many units are here — L1 EDU, L2, M1? Is a **TA01 arm** available?
2. Do you have a **thermal, gas or air-quality payload** with you, and how do we read it?
3. Can we send waypoint / patrol goals to the **on-robot RoamerX** from our laptop (API, ROS 2 action, or app only)?
4. Is there a **Python or ROS 2 wrapper** for the L1 SDK / GEN2 SDK, even unofficial?
5. How do we get the **camera, depth and LiDAR streams** (protocol, resolution, latency) onto our own computer or the Orin NX?
6. What are the **current limits** on the 12 V / 24 V rails, and where can we mount a 1–2 kg sensor box?
7. May the robot go **outdoors on snow** here? What do you advise for the L1 below 0 °C?
8. Is a **charging dock** on site, and does the recharge task work on these units?

## Decision rule
- **Pick Genisom AI for T03 if** your idea is monitoring or auditing on foot-accessible terrain (energy loss, bins and litter, water or air sensing), you are comfortable with C++ / ROS 2, and you can bring or borrow the sustainability sensor.
- **Avoid if** your core idea needs grasping (sorting, disassembly, EV plugs) and you cannot secure a second vendor's arm, or you need a Python-first, ready-made application stack.

## Sources
- [Genisom AI company profile (internal research doc)](../Genisom-AI.md)
- [Genisom L2 product page](https://www.genisomai.com/en/product-robot/L2)
- [Genisom L1 product page](https://www.genisomai.com/en/product-robot/L1)
- [Genisom M1 product page](https://www.genisomai.com/en/product-robot/M1)
- [MATRiX product page](https://www.genisomai.com/en/product-robot/MATRiX)
- [Industry page — Industrial Inspection](https://www.genisomai.com/en/industry/industrial-inspection)
- [Industry page — Emerging Applications](https://www.genisomai.com/en/industry/emerging-applications)
- [GENISOM AI at WAIC 2026 (company news, 2026-07-19)](https://www.genisomai.com/en/newsdetail/GENISOM-AI-at-WAIC-2026)
- [genisom_L1_sdk](https://github.com/zsibot/genisom_L1_sdk)
- [genisom_robot_sdk](https://github.com/zsibot/genisom_robot_sdk)
- [genisom_roamerx_open](https://github.com/zsibot/genisom_roamerx_open)
- [genisom_vln](https://github.com/zsibot/genisom_vln)
- [matrix (MATRiX simulator)](https://github.com/zsibot/matrix)
