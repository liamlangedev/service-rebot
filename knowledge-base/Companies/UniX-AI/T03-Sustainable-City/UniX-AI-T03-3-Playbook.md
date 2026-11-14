---
type: challenge-playbook
company: "UniX AI"
slug: UniX-AI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# UniX AI × T03 — Hackathon Playbook

⬆ [UniX AI profile](../UniX-AI.md) · [Brief](UniX-AI-T03-1-Brief.md) · [Products and solutions](UniX-AI-T03-2-Products-and-Solutions.md)

**Read this first:** UniX AI is a **2/5 fit** for T03. There is no public SDK, so every concept below is built around an **adapter layer** with three possible levels. Find out which one you get in the first hour, then pick the concept.

| Access level you are given | What you can build |
|---|---|
| **A — Skills only** (vendor triggers pre-loaded skills) | Concept 1 with operator-triggered motions; your value is perception, logic and impact data |
| **B — Skill / motion calls** (navigate-to, pick, place, or Cartesian targets from your code) | Concepts 1–3 properly autonomous |
| **C — Demonstration teaching** (record demos, train a new skill with UniFlex) | Concept 4 becomes realistic |

Whether levels B and C exist is **not public** — ⚠️ unverified.

## Solution approaches

### Concept 1 — Hotel-floor sorting station (safest)

- **Problem → value:** Guests and housekeeping throw mixed waste into one bag; sorting at the source (PET, aluminium, glass, paper, residual) raises recycling quality. A robot sorting point on a hotel floor or in a spa back-office does it without extra staff time.
- **Hardware:** Wanda 2.0 or Panther with UniPicker Pro · fixed RGB / RGBD camera over the table (your own) · laptop · 4–5 labelled bins. Optional: D-Robotics RDK board to run the classifier at low power.
- **Architecture / stack:**
  - Perception: external camera → object detection + material classification on laptop / edge board (your own model; no UniX model is available).
  - Planning: simple state machine — pick the nearest item, look up class → bin, queue the move.
  - Control: adapter to the robot — level B: send pick pose and bin target; level A: display the decision and have the vendor skill or operator execute it.
  - Output: live dashboard with items per stream and contamination rate.
- **48-hour plan:**
  - H0–6: confirm access level; fix table, camera and bin layout; collect 200–300 photos of real hackathon waste.
  - H6–24: train / tune classifier; first end-to-end pick → correct bin for 3 object types.
  - H24–40: extend to 5 streams, add "unknown → residual" rule, dashboard, 20-item endurance run.
  - H40–48: freeze, rehearse, record a backup video.
- **3-minute demo script:** (0:00) tip a mixed bag onto the table → (0:20) screen shows detections and chosen bins → (0:30–2:15) robot sorts 6–8 items while the counter updates → (2:15) judge drops in an unseen item; system routes it or sends it to residual → (2:40) impact slide: what one station per hotel floor would divert.
- **Risks and fallbacks:** grasp failures on flat or transparent items → restrict to bottles, cans, cartons, cups · no programmatic control → operator-in-the-loop with your perception deciding · robot not available enough hours → develop against recorded video.
- **Judging angles:** innovation low–medium (sorting robots exist) · technical depth medium (perception + integration) · real-world impact clear and measurable · Leukerbad relevance good (hotels, spa, clinics produce steady small-volume mixed waste).

### Concept 2 — Reuse loop for spa and hotel (cups, bottles, towels)

- **Problem → value:** Single-use cups and half-used amenities are thrown away; a robot that **collects, checks and returns reusables** (cups, glass bottles, trays) and **restocks only what is missing** cuts waste and purchasing.
- **Hardware:** Panther preferred (floor-level reach, omnidirectional base) or Wanda 2.0 · crate or trolley for collected items · external or on-robot camera.
- **Architecture / stack:**
  - Perception: detect reusable items on tables / return shelves; classify clean-looking vs. reject; count amenities on a shelf versus a target list.
  - Planning: route over 2–3 collection points (robot navigation, LiDAR map), then to a drop-off; restock list derived from the count.
  - Control: navigate-to and pick / place calls (needs level B); compute on laptop.
- **48-hour plan:**
  - H0–6: confirm navigation and pick calls exist; map a small arena with 3 stations.
  - H6–24: item detector; single-station collect → crate.
  - H24–40: multi-station round; restock-by-difference logic; log of items reused.
  - H40–48: polish, timing, backup video.
- **3-minute demo script:** robot drives to a "spa lounge" table, collects two reusable cups and a bottle, skips a single-use item, drives to the amenity shelf, adds only the missing item, then the screen shows "items kept in the loop today".
- **Risks and fallbacks:** navigation API not exposed → run a static two-table version · two-handed tray handling too hard → single items only · level A only → fall back to Concept 1.
- **Judging angles:** innovation medium (reuse, not just recycling) · technical depth medium–high (mobile manipulation) · impact credible for hospitality · Leukerbad relevance strong (thermal baths and hotels).

### Concept 3 — Energy and resource audit round with simple fixes

- **Problem → value:** In hotels and clinics, heat and power are lost to open windows above running radiators, lights and devices left on in empty rooms, dripping taps. A robot already doing service rounds can **detect, log and fix the simple cases**.
- **Hardware:** Wanda 2.0 (long **8–16 h** runtime suits rounds) · optional thermal camera or temperature / CO₂ sensor on a small edge board that you mount (D-Robotics RDK) · optional SKYLANDX scan for a 3D map to pin findings on.
- **Architecture / stack:**
  - Perception: camera images → vision model flags "window open", "light on, room empty", "tap running"; optional sensor readings.
  - Planning: patrol waypoints; rule engine ranks findings by estimated loss; decide "fix" or "report".
  - Control: navigation calls; arm action for one reachable fix (press a light switch, push a window shut, close a tap) — needs level B. Reporting to a web dashboard.
- **48-hour plan:**
  - H0–6: confirm navigation access; build a mock room (lamp, window frame or door, switch).
  - H6–24: detection of 2–3 waste conditions; waypoint patrol with logging.
  - H24–40: one physical fix (light switch is the easiest); dashboard with map and estimated savings (state your assumptions).
  - H40–48: rehearse; backup video.
- **3-minute demo script:** robot enters the mock room, screen flags "light on, nobody present" and "window open"; robot presses the switch; dashboard shows the finding closed and the open window sent to staff with a photo.
- **Risks and fallbacks:** fine manipulation of switches fails → report-only mode with a pointing gesture · savings numbers are estimates → label them as such and show the method · weak link to the robot's arms → combine with Concept 1 as a "resource steward" doing both.
- **Judging angles:** innovation medium–high (humanoid as building-energy auditor) · technical depth medium · impact depends on honest numbers · Leukerbad relevance strong (heating-heavy alpine hotels and clinics).

### Concept 4 — Teach-by-demonstration circular micro-hub (most ambitious)

- **Problem → value:** A small town cannot justify a sorting plant or a repair shop per building. A general-purpose robot that **learns a new circular task from a few demonstrations** — sort a new material, unscrew a cap, separate a battery from a device, fold towels for reuse — makes decentralised reuse viable.
- **Hardware:** Wanda 2.0 or Panther · optional outdoor feeder: a quadruped (Unitree Go2 or Genisom) bringing collected litter to the indoor hub · optional Flexiv arm for the force-sensitive disassembly step · optional OriginFlow capture for demonstrations.
- **Architecture / stack:**
  - Perception: classifier as in Concept 1 plus a "new item" trigger.
  - Learning: record demonstrations with the vendor's tooling and train a UniFlex skill — **only if level C exists** (not public).
  - Planning: task planner (your own LLM layer, or UniCortex if exposed) chains sort → pre-process → hand over.
  - Control: learned skill on robot; orchestration on laptop.
- **48-hour plan:**
  - H0–6: get a firm yes / no on demonstration teaching and training time per skill. If no, drop to Concept 1 or 2 immediately.
  - H6–24: baseline sorter running (Concept 1); record demos for one new skill.
  - H24–40: train and test the new skill; integrate optional second robot hand-over.
  - H40–48: reliability runs; backup video of the best take.
- **3-minute demo script:** show the 10-minute teaching session as a time-lapse, then the robot performing the newly taught step on an unseen item, then the full chain: item arrives → sorted → pre-processed → placed in the reuse crate.
- **Risks and fallbacks:** teaching tooling not offered or too slow → present Concept 1 with a design for the learning step · learned skill unreliable → show success rate honestly and keep a scripted motion as backup · multi-robot hand-over adds failure points → make it optional.
- **Judging angles:** innovation high · technical depth high · impact long-term (adaptable circular automation for small communities) · Leukerbad relevance medium–high (small alpine municipality, seasonal waste peaks from tourism).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| UniX AI + **D-Robotics** RDK board | Material classifier and sensor logging on a low-power edge board; supports the "low-power edge AI" angle | Low — independent of robot access |
| UniX AI + **Unitree** or **Genisom AI** quadruped | Outdoor litter collection (quadruped) feeding the indoor sorting station (Wanda / Panther) | Medium–high — two stacks, hand-over point needed |
| UniX AI + **SKYLANDX** MetaCam | 3D scan of the building to place audit findings and plan routes | Low–medium — offline map, loose coupling |
| UniX AI + **Flexiv** Rizon | Humanoid fetches and sorts; force-controlled arm does disassembly or repair | Medium — fixed cell beside the robot, simple hand-over |
| UniX AI + **XREAL** glasses | Staff see sorting decisions or audit findings in AR and confirm exceptions | Low–medium — UI only |
| UniX AI + **OriginFlow** | Human-motion capture as demonstration data for a new skill | High — depends on UniX teaching tooling (not public) |

## Questions to ask the UniX AI engineers on site

1. Which robots are here (Wanda 2.0, Panther, Martian) and how many hours per team?
2. What can our code call: pre-loaded skills, navigate-to-pose, Cartesian or joint arm targets, gripper commands? Over what interface (ROS 2, Python, HTTP)?
3. Is the **waste-sorting skill** from CES 2026 installed on these units, and can we change its classes and bin positions?
4. Can we record demonstrations and train a new UniFlex skill here? How many demos and how long does training take?
5. Can we read camera, RGBD and LiDAR streams and the navigation map from an external laptop?
6. What are the gripper's opening width and limits with thin, wet or transparent items?
7. What is the robot's power draw and charging method? (Needed for any energy-footprint claim.)
8. What safety rules apply — speed limits, e-stop, required operator presence?

## Decision rule

- **Pick UniX AI for T03 if** your idea is an *indoor* hotel / spa / clinic story (sorting, reuse, restocking, energy audit), you bring your own perception and logic, and the booth confirms at least skill or motion calls from your code.
- **Avoid if** you need outdoor operation, a documented SDK from hour zero, measured energy data, or high-throughput sorting — choose a vendor with an open arm or quadruped stack and use UniX AI, at most, as the demo's service-robot front end.

## Sources
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [Panther product page](https://www.unix-group.ai/Panther)
- [UniPicker Pro product page](https://www.unix-group.ai/UniPicker)
- [Press release, 2 Jan 2026: Wanda series at CES 2026 (via Webull / PR Newswire)](https://www.webull.com/news/14134140025406464)
- [Press release, 8 Apr 2026: Panther launch (via TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [WRC 2026 live report, 20 Aug 2026 (iTiger)](https://www.itiger.com/news/1101359561)
