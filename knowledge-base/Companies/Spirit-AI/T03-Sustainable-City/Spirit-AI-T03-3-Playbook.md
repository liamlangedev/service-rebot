---
type: challenge-playbook
company: "Spirit AI"
slug: Spirit-AI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Spirit AI × T03 — Hackathon Playbook

⬆ [Spirit AI profile](../Spirit-AI.md) · [Brief](Spirit-AI-T03-1-Brief.md) · [Products and solutions](Spirit-AI-T03-2-Products-and-Solutions.md)

**Read first:** fit is **2/5**. Everything below assumes a **Moz1** with SDK and Quest teleop kit is on site and bookable — ⚠️ unverified. Confirm in the first 30 minutes; if not, take the perception and software parts of Concept 1 to a fixed arm from another vendor.

## Solution approaches

### Concept 1 — Recyclables sorting station (safest)

- **Problem → value:** hotel and café waste arrives mixed; wrong items in a recycling stream spoil the batch. A robot that separates PET, aluminium, glass and residual at the back-of-house point raises recovery without extra staff time.
- **Hardware:** Moz1 (arms only, base parked) · head / wrist RealSense · 4 labelled bins · optional D-Robotics RDK board for the classifier.
- **Architecture / stack:**
  - Perception: RGB-D from RealSense → open-vocabulary detector or small fine-tuned classifier (your own; Spirit AI ships none) → material class + grasp point from depth.
  - Planning: fixed lookup "class → bin pose"; simple top-down grasp; queue of detected items.
  - Control: MozRobot SDK (`MOZ1Robot`, Python, ROS 2 Humble) Cartesian moves, force-limited placing for glass.
  - Compute: laptop on the robot's Ethernet subnet (`172.16.0.x`); classifier on laptop GPU or RDK board.
- **48-hour plan:**
  - H0–6: confirm robot slot, install SDK, run `example_usage.py`, teleop one full sort by hand to prove reach and gripper suitability.
  - H6–24: classifier on 4 classes with real local items; camera-to-arm calibration; scripted pick-and-place for one class.
  - H24–40: all 4 classes, failure recovery (re-grasp, skip), counters and a live "kg / items diverted" dashboard.
  - H40–48: 20-item timed runs, record success rate, backup video, rehearse.
- **3-minute demo script:** 0:00 dump a mixed tray → 0:20 robot classifies (overlay on screen) → 0:30–2:15 sorts 6–8 items, judge throws in a surprise item → 2:15 dashboard shows purity and items per minute → 2:40 one-slide scale-up for a hotel waste room.
- **Risks and fallbacks:** gripper cannot hold crushed cans or glass (not public) → pick items the gripper handles, use a tray for the rest · calibration drift → fixed fiducials · robot time shared → develop against the URDF in simulation, keep VR teleop as live fallback with the classifier still deciding the bin.
- **Judging angles:** *innovation* low–medium · *technical depth* medium (perception + force-aware placing) · *impact* clear metric (stream purity) · *Leukerbad* tourist resort with many hotels and restaurants producing mixed guest waste.

### Concept 2 — Reuse-first bussing table with waste audit

- **Problem → value:** reuse beats recycling. Separate returnables (deposit cups, glass bottles, crockery) from true waste at a café or spa-bistro return point, load reusables into a dishwasher rack, and log what is thrown away so the kitchen can cut waste at source.
- **Hardware:** Moz1 (both arms) · dish rack · two bins · scale under the residual bin (any USB / BLE scale) · optional XREAL glasses for a staff audit view.
- **Architecture / stack:** Concept 1 pipeline plus bimanual steps (one arm steadies the rack, the other places) · item log → small database → dashboard (items reused, waste by category, per hour) · SDK scripted skills; teleop demonstrations recorded for later policy training.
- **48-hour plan:**
  - H0–6: as Concept 1; test rack loading by teleop.
  - H6–24: classes "reusable cup / plate / bottle / waste"; scripted rack placement with force limits.
  - H24–40: audit dashboard, scale integration, surprise-item handling.
  - H40–48: timed runs, video, pitch numbers.
- **3-minute demo script:** tray comes back from a "guest" → robot racks cup and plate, bins napkin, sets bottle aside → dashboard updates → show the weekly waste report a kitchen manager would get.
- **Risks and fallbacks:** rack placement precision → wide-slot rack, tilt-tolerant placing · wet or greasy items → dry props only (docs warn about humidity; gripper wet-grip not public) · bimanual timing → single-arm version.
- **Judging angles:** *innovation* medium (audit data, not just sorting) · *technical depth* medium · *impact* waste prevention + reuse, measurable · *Leukerbad* spa bistros and clinics with canteens; mirrors the company's own WAIC dishwasher demo, so staff can help.

### Concept 3 — Energy-saver patrol (windows, radiators, lights)

- **Problem → value:** in an alpine winter, heat lost through tilted windows, radiators left on full and lights in empty rooms is avoidable energy. A robot on a night round of corridors and meeting rooms finds and fixes these, and reports what it could not fix.
- **Hardware:** Moz1 whole-body with base · optional SKYLANDX MetaCam scan for the floor map · optional thermal camera (bring your own) · mock-up panel with a radiator thermostat valve, light switch and window handle.
- **Architecture / stack:** map + waypoints via the docs' SLAM navigation section (contents not reviewed — confirm maturity) → at each stop, detector finds valve / switch / handle state → force-controlled turn or press through the SDK → event log with estimated kWh saved (state your assumptions).
- **48-hour plan:**
  - H0–6: verify navigation works at the venue and what API it exposes; build the mock-up panel.
  - H6–24: state detection for 3 fixtures; teleop-recorded then scripted manipulation of each.
  - H24–40: chain 2–3 waypoints; report generation.
  - H40–48: reliability runs; decide live-navigation versus stationary panel demo.
- **3-minute demo script:** robot drives to the panel → turns the thermostat from 5 to 2, switches the light off, pushes the window handle closed → report appears with "3 fixes, estimated saving" → map view of a hotel floor.
- **Risks and fallbacks:** navigation not usable in time → panel-only demo with the base parked · window handles need more force or reach than available (specs not public) → restrict to valve and switch · savings estimate challenged → present it as an assumption-based estimate, not a measurement.
- **Judging angles:** *innovation* medium–high · *technical depth* high (navigation + contact-rich manipulation; echoes the CATL plugging skill) · *impact* direct energy story · *Leukerbad* strong — hotels and clinics with long heating seasons.

### Concept 4 — Learned sorting policy on low-power edge compute (most ambitious)

- **Problem → value:** hand-scripted sorting breaks on new items. Train a policy from teleop demonstrations and run it on an efficient edge board to show that general-purpose sorting does not need a GPU workstation.
- **Hardware:** Moz1 · Quest teleop kit · cloud GPUs (bring your own budget) · D-Robotics board for inference (which board is on site and whether Spirit v1.5 runs on it ⚠️ unverified — the published port is to the Sunrise S600).
- **Architecture / stack:** collect 50–150 demonstrations with the collection app → fine-tune either the Pi0.5 / openpi `pi05_moz` adaptation (source from Spirit AI staff) or Spirit v1.5 (public repo; recommended **8× A100 80 GB**) → policy server + robot client → Concept 1 scripted pipeline kept as the safety net.
- **48-hour plan:**
  - H0–6: get the adaptation source and data format from staff; book GPUs; build Concept 1 baseline in parallel.
  - H6–24: data collection in shifts; start the first fine-tune by H18.
  - H24–40: evaluate on the robot; second fine-tune if needed; try edge deployment.
  - H40–48: side-by-side scripted versus learned on unseen items; freeze.
- **3-minute demo script:** show an unseen item defeating the scripted baseline → learned policy sorts it → power meter on the inference box next to a GPU-workstation figure → open-model slide (MIT).
- **Risks and fallbacks:** training does not converge in time (likely) → present Concept 1 with the collected dataset and an honest partial result · no Moz1 embodiment config in the public repo → depend on staff · edge port unavailable → run inference on a laptop GPU and drop the low-power claim.
- **Judging angles:** *innovation* high · *technical depth* very high · *impact* generalisation + compute efficiency · *Leukerbad* indirect.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Moz1 + **D-Robotics** RDK board | Classifier (and possibly policy) on a low-power board; credible "efficient edge AI" angle backed by the published S600 partnership | Low for a vision classifier over ROS 2; high / uncertain for VLA inference |
| Moz1 + **SKYLANDX** MetaCam | Fast 3D map of the venue or a hotel floor for the patrol concept | Medium — map format into Moz1 navigation is unknown |
| Moz1 + **XREAL** glasses | Staff see sort decisions, audit data or remaining fixes as an overlay | Low — reads your dashboard data, no robot coupling |
| Moz1 + **OriginFlow** EMG capture | Alternative demonstration source for the learned-policy concept | High — no known link to Spirit AI's data pipeline |
| Sorting software + **Flexiv** / **ROKAE** / **Dobot** arm | Same Concept 1 on a fixed cell if no Moz1 slot; cheaper per sorted item, stronger sustainability case | Medium — re-do calibration and motion layer |
| Moz1 + **Unitree** / **AGIBOT** quadruped | Quadruped collects litter or bins outdoors, Moz1 sorts indoors | High — two stacks, hand-over point; only with a large team |

## Questions to ask the Spirit AI engineers on site

1. Is a Moz1 available to teams, how many, and how are time slots allocated? Is a simulation-only path supported?
2. What gripper is fitted — stroke, max grip force, and can it hold a glass bottle or a crushed can? What is the per-arm payload?
3. Can we get the MozRobot SDK wheel, the API reference and an English summary today? Which SDK version matches the robot's firmware?
4. Does the SDK expose Cartesian moves with force limits, and base navigation goals, or is navigation only available through the HMI / app?
5. Can you share the `pi05_moz` adaptation source and a sample dataset? What data format does the collection app write?
6. Is there a Spirit v1.5 or v1.6 checkpoint for Moz1 we may run for pick-and-place, and on what compute? Any on-site GPU?
7. Does Spirit v1.5 run on any D-Robotics board present here, and at what rate and power draw?
8. What are the robot's runtime per charge and typical power draw? (Needed for any energy-per-item claim.)

## Decision rule

- **Pick Spirit AI for T03 if** a Moz1 slot and SDK access are confirmed in the first hour, your idea is indoor dual-arm sorting, reuse or fixture manipulation, and you are happy to bring your own perception and sustainability metrics.
- **Avoid if** your concept is outdoors, needs published payload / runtime / energy numbers, depends on fine-tuning a VLA without cloud GPUs, or would be served equally well by a fixed arm — a cobot cell makes the stronger efficiency case.

## Sources

- [Spirit AI news: WAIC 2026, Moz1 + Spirit v1.6 demos, Moz2 debut](https://www.spirit-ai.com/en/news/48)
- [Spirit AI news: CATL battery-pack line deployment](https://www.spirit-ai.com/en/news/23)
- [Spirit AI news: D-Robotics partnership, Spirit v1.5 on Sunrise S600](https://www.spirit-ai.com/en/news/45)
- [Spirit AI news: Bosch China partnership](https://www.spirit-ai.com/en/news/29)
- [Docs: MozRobot SDK quick start](https://docs.spirit-ai.com/zh/sdk/get-started.html)
- [Docs: Moz1 product introduction](https://docs.spirit-ai.com/zh/moz1/product-intro.html)
- [Docs: Pi0.5 adaptation](https://docs.spirit-ai.com/zh/open-resources/pi.html)
- [GitHub: Spirit-AI-Team/spirit-v1.5](https://github.com/Spirit-AI-Team/spirit-v1.5)
- [Spirit AI company profile (this repo)](../Spirit-AI.md)
