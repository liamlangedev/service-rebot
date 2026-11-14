---
type: challenge-playbook
company: "SKYLANDX"
slug: SKYLANDX
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# SKYLANDX × T03 — Hackathon Playbook

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Brief](SKYLANDX-T03-1-Brief.md) · [Products and solutions](SKYLANDX-T03-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- SKYLANDX measures; it does not act. Each concept names who does the acting.
- **Safe data path = file export** (LAS / PLY / E57 from MetaCam Studio) into your own Python. Treat the live Rosbridge stream as a bonus until an engineer on site hands you documentation.
- On-site hardware is not confirmed (best guess: MetaCam Air 2 + apps). Confirm units, software licences and cloud access in the first hour.
- Local-relevance statements about Leukerbad are our interpretation of the event context, not SKYLANDX claims.

## Solution approaches

### Concept 1 — Fill-level twin: collect and clear only when needed (safest)

- **Problem → value:** Waste containers, wood-chip or grit stores and snow depots are emptied or refilled on fixed schedules. Measuring real volume lets a small mountain town cut truck trips (fuel, noise, cost) and plan capacity.
- **Hardware:** MetaCam Air 2 (handheld) + laptop. Optional: XREAL glasses to show the result on site.
- **Architecture / stack:**
  - Perception: walk-through scan → MetaCam Studio alignment and export (LAS / PLY). Studio's own stockpile-volume tool gives a reference number.
  - Analysis: Open3D or CloudCompare — align scan A and scan B, ground-plane fit, 2.5D volume and difference map.
  - Decision: simple rule or route optimizer ("visit only sites above 70 % fill"), estimated km and CO₂ avoided with stated assumptions.
  - Compute: laptop; Skyland Cloud only for the shareable 3D view.
- **48-hour plan:**
  - H0–6: get a scanner, scan one test pile, confirm export and file sizes, write the volume script on sample data.
  - H6–24: scan 3–5 real sites (or mock piles) at two points in time; build alignment + difference pipeline.
  - H24–40: dashboard (map, fill %, trend, trip plan); validate one volume against a tape-measure estimate.
  - H40–48: polish, upload one scene to the cloud viewer, rehearse.
- **3-minute demo script:** (1) 20 s problem: fixed-schedule trucks. (2) Live 60 s scan of a pile of boxes / snow in front of the jury. (3) Show before / after difference map and volume in litres. (4) Dashboard: which sites to visit today, trips saved. (5) 3D scene in a browser.
- **Risks and fallbacks:** processing slower than expected → pre-process all scans, show live capture only as preview. Snow or wet surfaces return poorly → use cardboard, wood chips or gravel. No Studio licence on your laptop → ask staff to export for you.
- **Judging angles:** innovation low–medium; technical depth medium (registration, error bars); impact clear and quantifiable; Leukerbad relevance high (winter road service, tourist-season waste peaks).

### Concept 2 — Retrofit twin: where does this building waste energy?

- **Problem → value:** Old hotels and chalets are costly to audit. A 15-minute scan yields envelope areas, window shares and room volumes; add thermal images and you get a ranked list of retrofit measures.
- **Hardware:** MetaCam Air 2 or MetaCam Lite (indoor). **A thermal camera is required and is not a SKYLANDX product** — bring or borrow one. Optional: XREAL for an AR overlay of hot spots.
- **Architecture / stack:**
  - Perception: scan → point cloud + panoramas → plane segmentation (walls, floor, ceiling, windows) in Open3D.
  - Fusion: register thermal photos to the scan by manual tie points (do not attempt automatic calibration in 48 h).
  - Model: simple steady-state heat-loss estimate per surface (area × assumed U-value × temperature difference); rank measures by saved kWh. State every assumption on screen.
  - Output: 3DGS / point-cloud viewer with coloured loss map; RCP / E57 hand-off to an architect.
- **48-hour plan:**
  - H0–6: scan one room, prove plane extraction and area numbers against a tape measure.
  - H6–24: scan the target space (venue room, corridor, façade); capture thermal images; tie-point registration.
  - H24–40: heat-loss calculator, ranking, viewer.
  - H40–48: sanity checks, demo run.
- **3-minute demo script:** (1) Scan the demo room live for 45 s. (2) Show auto-extracted wall / window areas. (3) Overlay thermal hot spots. (4) "Top three measures, estimated saving" card. (5) Export to a BIM-ready file.
- **Risks and fallbacks:** glass and mirrors corrupt geometry → mark windows manually. No thermal camera → geometry-only audit (window-to-wall ratio, volume to heat) and say so. Numbers are estimates → present ranges, not single values.
- **Judging angles:** innovation medium; technical depth medium–high (multi-modal fusion); impact high (building heat dominates alpine energy use — *our framing*); Leukerbad relevance high (hotel and clinic stock, thermal-water heat).

### Concept 3 — Autonomous resource round: a quadruped that re-scans and reports change

- **Problem → value:** Audits only save resources if they are repeated. A legged robot carrying the scanner walks the same route weekly and flags what changed: stock levels, snow load, blocked recycling points, new damage.
- **Hardware:** MetaCam Air 2 + MetaCam Hub (⚠️ availability on site unconfirmed) on a quadruped — Unitree Go2 / B2, Genisom AI M1 / L1, Magiclab MagicDog or AGIBOT D1. Edge compute: D-Robotics RDK X5 or a laptop.
- **Architecture / stack:**
  - Integration depth 1 (payload only) is the realistic target: the robot uses its own navigation or teleoperation; MetaCam records.
  - Stretch — depth 2: subscribe to MetaCam pose and point cloud over the Rosbridge WebSocket (roslibpy) and feed the robot's stack; use relocalization against the first scan.
  - Analysis: same difference pipeline as Concept 1, run automatically after each round; alert list + 3D viewer.
- **48-hour plan:**
  - H0–6: secure robot + scanner + mount; check mass (619 g) against the robot's payload; first teleoperated scan.
  - H6–24: repeatable route (robot's own waypoint mode or teleop); two rounds with a staged change in between; ask SKYLANDX for stream access.
  - H24–40: automatic alignment + change report; if stream access arrived, live pose on a map.
  - H40–48: reliability runs, backup video.
- **3-minute demo script:** (1) Robot walks a short loop with the scanner. (2) Team moves / removes material. (3) Second loop. (4) Screen shows the change map and "minus 0.4 m³ at station B" alert. (5) One sentence on weekly rounds for depots, plant rooms, forest paths.
- **Risks and fallbacks:** no Hub → improvised rigid mount (tape and 3D print), accept vibration. No stream docs → stay at depth 1 with file export. Robot unavailable → push the scanner on a trolley and keep the story. Two vendors to coordinate → assign one person per vendor from hour 0.
- **Judging angles:** innovation medium–high; technical depth high (multi-vendor integration, registration); impact medium–high; Leukerbad relevance high (steep, snowy terrain suits legs).

### Concept 4 — Real2Sim sorting cell or protection-forest carbon plot (most ambitious, pick one)

- **Problem → value:**
  - *4a Sorting cell:* scan a real waste / recycling station into a 3DGS + mesh twin so a manipulator's sorting policy can be developed and tested in simulation before touching the real cell.
  - *4b Forest plot:* scan a forest plot under the canopy, extract stems and diameters, estimate biomass and stored carbon, repeat to track change.
- **Hardware:** MetaCam Air 2 (4b: MetaCam Pro if offered). 4a adds an arm or mobile manipulator from Flexiv, Dobot, ROKAE, Galbot or Galaxea.
- **Architecture / stack:**
  - 4a: scan → OBJ mesh + 3DGS PLY (Skyland Cloud) → convert to your simulator's format yourself (no USD / Isaac export is mentioned) → policy or scripted pick-and-place in sim → run on the real arm using the scan as the world model.
  - 4b: scan → ground classification (PDAL) → stem detection and diameter (3DFin) → allometric biomass estimate (cite the equation you use) → compare with swissSURFACE3D canopy data.
- **48-hour plan:**
  - H0–6: capture the scene / plot; prove the conversion (4a) or stem extraction (4b) on one small scan.
  - H6–24: full capture; simulator scene or plot metrics.
  - H24–40: sim-to-real run (4a) or carbon report + repeat-scan comparison (4b).
  - H40–48: demo hardening.
- **3-minute demo script:** 4a — split screen: splat twin, simulated sort, real arm repeating it. 4b — fly through the scanned plot, stems light up with diameters, carbon total and uncertainty appear.
- **Risks and fallbacks:** 4a — cloud 3DGS time unknown, mesh quality may be too rough for physics → use simple collision boxes fitted to the point cloud. 4b — November weather, snow cover and daylight; scanner IP rating not public → scan a few trees near the venue only. Both: high integration load, weak if the team is under four people.
- **Judging angles:** innovation high; technical depth high; impact medium (4a indirect) to high (4b measurable carbon); Leukerbad relevance medium (4a) / high (4b, mountain forests).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| SKYLANDX + Unitree / Genisom AI / Magiclab quadruped | Autonomous repeat scans of depots, plant rooms, slopes | Medium (mount + teleop) · High (live pose into robot stack) |
| SKYLANDX + D-Robotics RDK | On-robot Rosbridge client, change detection at the edge, low-power story | Medium |
| SKYLANDX + XREAL | AR overlay of volume, fill level or heat-loss results on site | Medium (alignment of scan frame to glasses frame is manual) |
| SKYLANDX + Flexiv / Dobot / ROKAE arm | Scan gives cell geometry; arm sorts or disassembles | High (scan is offline; arm still needs its own live camera) |
| SKYLANDX + Galbot / Galaxea / Spirit AI mobile manipulator | Prior map + relocalization for a robot that collects or sorts | High |
| SKYLANDX + Binabik AI / coprod | Scan as the shared world model inside a modular robot stack | Unknown — ask both teams |

## Questions to ask the SKYLANDX engineers on site

1. Which units are available to teams (Air 2, Lite, Pro, C01, Hub), how many, and for how long per booking?
2. Can we get MetaCam Studio on our own laptops and a Skyland Cloud account this weekend? How long does a 3DGS job take for a 5-minute scan?
3. Is the Rosbridge WebSocket open to hackathon teams? Which topics, message types and ROS versions (ROS 2?), and is there a sample client?
4. Does Studio expose volume and scan-to-scan difference tools we can script, or only through the GUI?
5. What are the IP rating and operating-temperature limits — can we scan in snow, drizzle or near steam?
6. How well does the scanner handle snow, water and glass surfaces, and what scanning pattern do you recommend for a pile or a tree stand?
7. For robot mounting: Hub mass, power input, connector, and which robots on site have already been tested with it?
8. Can relocalization against an earlier scan be triggered through the API, and what accuracy should we expect between two rounds?

## Decision rule

- **Pick SKYLANDX for T03 if** your idea is about *measuring and tracking* a physical resource (volume, area, building geometry, biomass, change over time) and you can write the analysis yourself from exported point clouds — ideally with a quadruped as carrier.
- **Avoid if** your idea needs a robot to physically sort, collect, charge or repair, needs thermal / air / water sensing from the same device, or cannot tolerate an undocumented API.

## Sources
- [SKYLANDX — MetaCam Air 2](https://skylandx.com/metacam-air-2/)
- [SKYLANDX — MetaCam Pro](https://skylandx.com/metacam-pro/)
- [SKYLANDX — Software platforms](https://skylandx.com/software-platforms/)
- [SKYLANDX — Spatial Perception Robots](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Industry: AEC](https://skylandx.com/industry/aec/)
- [SKYLANDX — Industry: Industrial facilities](https://skylandx.com/industry/industrial-facilities/)
- [SKYLANDX — Industry: Surveying](https://skylandx.com/industry/surveying/)
- [SKYLANDX company profile (this vault)](../SKYLANDX.md)
- Third-party tools named above (reachability checked): [Open3D](https://github.com/isl-org/Open3D) · [CloudCompare](https://www.cloudcompare.org/) · [PDAL](https://pdal.io/) · [roslibpy](https://github.com/gramaziokohler/roslibpy) · [3DFin](https://github.com/3DFin/3DFin) · [swissSURFACE3D](https://www.swisstopo.admin.ch/en/height-model-swisssurface3d)
