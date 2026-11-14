---
type: challenge-playbook
company: "Magiclab Robotics"
slug: Magiclab
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Magiclab Robotics × T03 — Hackathon Playbook

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Brief](Magiclab-T03-1-Brief.md) · [Products and solutions](Magiclab-T03-2-Products-and-Solutions.md)

**Read first:** fit is **2/5**. Magiclab brings mobility, not sustainability content — every concept below gets its T03 value from a sensor pack, a model or a partner arm that **you** add. On-site units are not confirmed; all concepts assume a **MagicDog EDU** (the only MagicDog edition with SDK access). Before H0, confirm edition, SDK access and how a companion computer connects.

## Solution approaches

### Concept 1 — Heat-Loss Hound (indoor energy and air-quality audit)

- **Problem → value:** Leukerbad's hotels, clinics and thermal baths heat large volumes all winter; nobody walks the corridors with a thermal camera every night. A quadruped doing a repeatable route turns one-off audits into a **daily heat-loss, open-window and ventilation map** with a ranked fix list.
- **Hardware:** MagicDog EDU + self-powered sensor pack on the back (low-cost thermal camera, CO2 / temperature / humidity sensor — bring your own or ask organisers) + companion computer (laptop in tether, or a D-Robotics RDK X5 strapped on). Optional: SKYLANDX MetaCam scan as base map; XREAL glasses to show findings in place.
- **Architecture / stack:** Perception — thermal frames + air readings time-stamped against `/odom_chassis` and the Cartographer pose. Planning — waypoint list sent as global goal poses through `magicdog_ros2_sdk` navigation. Control — the robot's built-in motion controller (no gait work). Analytics on laptop: anomaly detection on thermal frames (hot spots on cold walls, cold streaks at windows), CO2 thresholds, heat-map on the saved map, short LLM-written report. Compute: ROS 2 Foxy / Iron on the companion computer wired to the robot.
- **48-hour plan:**
  - **H0–6:** confirm EDU access; bring up SDK (multicast on, CycloneDDS, `ROS_DOMAIN_ID=25`); joystick node works; sensor pack logs to laptop on the bench.
  - **H6–24:** map one corridor with Cartographer; save map; drive 4–6 waypoints autonomously; mount pack; fuse readings with pose.
  - **H24–40:** heat-map overlay, anomaly rules, staged faults (open window, uninsulated hot pipe, crowded room for CO2); report generator; rough kWh / CHF estimate with stated assumptions.
  - **H40–48:** three full dry runs, record backup video, freeze code.
- **3-minute demo script:** (0:00) one line on wasted heat in alpine resorts → (0:30) dog walks the route past a staged open window and a hot pipe → (1:30) live map lights up at both spots → (2:15) report: three ranked fixes with estimated savings → (2:45) how a hotel would run it nightly.
- **Risks and fallbacks:** ROS 2 SDK mismatch with firmware → fall back to `magicdog_sdk` velocity commands and a pre-recorded path, or to joystick teleoperation with autonomous sensing. No thermal camera available → use CO2 / temperature only and call it a ventilation audit. Savings numbers are estimates → label them as such.
- **Judging angles:** innovation medium · technical depth medium (SLAM + sensor fusion) · real-world impact **high and quantifiable** · Leukerbad relevance **very high** (spa and hotel heating).

### Concept 2 — Litter and Waste-Point Scout

- **Problem → value:** Tourist paths and bin stations are checked on fixed schedules. A patrol robot that spots litter and overfull bins lets a small municipal team drive **only where needed** — fewer vehicle trips, cleaner paths.
- **Hardware:** MagicDog EDU (or MagicDog-W if on site: 10 kg payload, 4G uplink) + companion computer. Optional: D-Robotics RDK X5 for on-board low-power detection.
- **Architecture / stack:** Perception — robot colour / depth camera topics → open-source waste-detection model on laptop or RDK; bin fill-level from depth. Planning — patrol waypoints via SLAM navigation; detections projected onto the map. Output — web map with items, classes and a shortest pickup route for staff. Control — built-in controller.
- **48-hour plan:**
  - **H0–6:** SDK bring-up; camera topics on laptop; pick a detection model and test on phone photos.
  - **H6–24:** map the demo area; patrol loop; detection → map pin pipeline.
  - **H24–40:** fill-level estimate, route optimiser, dashboard; tune false positives under venue lighting.
  - **H40–48:** rehearse, backup video.
- **3-minute demo script:** scatter bottles, cans and a full bin → dog patrols → pins appear live with class labels → dashboard shows "2 stops instead of 9" → close with trips saved per week (assumption stated).
- **Risks and fallbacks:** Outdoor snow is untested (no IP rating published; MagicDog-W rated to −5 °C) → run indoors or under cover. Detection unreliable → restrict to 3 classes and bright objects. Navigation flaky → teleoperate the route, keep detection autonomous.
- **Judging angles:** innovation low–medium (known idea) · technical depth medium · impact medium · Leukerbad relevance good (tourist trails, small municipal crew).

### Concept 3 — Fetch-and-Sort Loop (quadruped + partner arm)

- **Problem → value:** Small resorts cannot justify a sorting plant. A mobile carrier that brings mixed recyclables from collection points to **one shared sorting arm** shows a micro-scale circular loop for hotels and clinics.
- **Hardware:** MagicDog EDU with a light basket (≤5 kg) as shuttle + a fixed arm from another vendor (Flexiv Rizon, Dobot CR / Nova or ROKAE xMate) with camera. Use MagicArm R1 instead only if it is on site **and** has a usable SDK (both unconfirmed).
- **Architecture / stack:** Shuttle — SLAM navigation between "collection" and "sorting" goal poses, docking by a fiducial marker seen in the robot camera. Sorting cell — camera → material classifier (PET / aluminium / other) → pick-and-place into bins via the arm vendor's SDK. Coordination — simple ROS 2 or MQTT state machine on one laptop.
- **48-hour plan:**
  - **H0–6:** split team in two (shuttle / cell); both get hardware moving.
  - **H6–24:** shuttle A→B navigation; cell sorts 3 classes from a fixed tray.
  - **H24–40:** handover (arm picks from the basket on the dog's back, or a person tips the basket — decide by H30); counters for kg sorted and purity.
  - **H40–48:** end-to-end runs, backup video.
- **3-minute demo script:** visitor drops items into the basket → dog walks to the cell → arm sorts into three bins → screen shows items sorted, purity and a per-hotel yearly projection.
- **Risks and fallbacks:** two vendors double the integration risk → keep the interface to one "arrived" message. Picking from a moving-then-standing dog is imprecise → human tip-over handover. If the arm fails, present Concept 2 with the shuttle.
- **Judging angles:** innovation medium · technical depth **high** (multi-robot) · impact medium · Leukerbad relevance medium–good.

### Concept 4 — Teach-Once Recycling Humanoid (most ambitious)

- **Problem → value:** Sorting mixed items needs dexterity and adapts poorly to new packaging. Teaching a humanoid by XR teleoperation, then running a learned policy, hints at a sorter that staff can **re-train in an afternoon**.
- **Hardware:** MagicBot Z1 **Development Version** with 11-DoF tactile hands (only if on site and unlocked) + PICO headset for `pico_teleoperate` + GPU workstation. Optional: OriginFlow EMG capture as an alternative demonstration source; WUJI Hand ⚠️ mounting compatibility unverified.
- **Architecture / stack:** Data — teleoperated demonstrations (HDF5 → LeRobot format, following the `magicbot-gen1_pi0_demo` pipeline). Model — LoRA fine-tune of pi0 or MagicW0 checkpoint on a GPU; policy server on workstation; robot runs actions through `magicbot-z1_sdk`. **Caveat:** the published pipeline targets Gen1; adapting it to Z1 is your work.
- **48-hour plan:**
  - **H0–6:** teleoperation working end to end; one item, one bin.
  - **H6–24:** collect 50–100 demos of a two-class sort; start fine-tune overnight.
  - **H24–40:** deploy policy; measure success; add scripted grasp fallback.
  - **H40–48:** rehearse; decide honestly whether to show policy or live teleoperation.
- **3-minute demo script:** 30 s of teaching via headset → policy sorts bottle vs can autonomously → show success rate and "new item taught in N minutes".
- **Risks and fallbacks:** **high** — no Z1 VLA recipe, 2–3 kg arm payload, ~2 h battery, training time. Fallback: live teleoperated sorting framed as the data-collection step, plus a scripted pick for one item.
- **Judging angles:** innovation **high** · technical depth **high** · impact low today (throughput) · Leukerbad relevance low–medium.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| MagicDog EDU + D-Robotics RDK X5 | On-board, low-power sensor fusion and detection; answers the "low-power edge AI" angle | Low–medium (ROS 2 on both; power the board separately) |
| MagicDog EDU + SKYLANDX MetaCam | High-quality 3D building scan as the base for the heat-loss map | Low (offline scan; align to the SLAM map) |
| MagicDog EDU + XREAL glasses | Facility staff see heat leaks or litter pins overlaid in place | Medium (pose alignment between map and glasses) |
| MagicDog EDU + Flexiv / Dobot / ROKAE arm | Fetch-and-sort loop (Concept 3) | Medium–high (two SDKs, handover) |
| MagicBot Z1 dev + OriginFlow | EMG-based demonstrations for sorting policies | High (unproven pairing) |
| MagicDog EDU + Unitree Go2 or Genisom quadruped | Same audit software on two bodies — shows portability | Medium (separate SDKs; share only the analytics layer) |

Naming trap when talking to other teams: MagicBot **Z1** vs Unitree Z1 (arm); MagicBot **D1** vs AGIBOT D1 (quadruped); MagicDog **T1**, Gen1 and the many G1 robots. Use full names.

## Questions to ask the Magiclab Robotics engineers on site

1. Which units are here, and which are **EDU / Development Version** with SDK access unlocked?
2. Does `magicdog_ros2_sdk` (last pushed May 2025) match the firmware on these robots? Is Foxy still required, or is Humble / Jazzy supported?
3. Where does a companion computer plug in — which port for the "data cable to the control board", and is there a **power output** for payloads (voltage, current)?
4. Real payload and runtime with a 2–3 kg sensor pack on the back? Any mounting rails or a backplate drawing?
5. Is MagicDog safe on wet floors, snow or light rain? Any IP rating not shown on the website?
6. Is a MagicArm R1 or MagicHand S01 available to borrow, and what is its SDK or communication interface?
7. Can the navigation stack accept a list of waypoints and report arrival reliably (`/ab_navigation_complete`), and how does it behave around people?
8. Is there a Z1 version of the pi0 / MagicW0 fine-tuning pipeline, or sample teleoperation data?

## Decision rule

- **Pick Magiclab Robotics for T03 if** your idea is "carry sensors along a repeatable indoor route and turn the data into savings", a MagicDog EDU with working ROS 2 navigation is confirmed, and your team can supply the sensing and analytics.
- **Avoid if** your concept depends on manipulation throughput (waste sorting, litter picking), outdoor winter operation, or a ready-made sustainability application — choose an arm or mobile-manipulator vendor and use Magiclab at most as the shuttle.

## Sources

- [Magiclab Robotics company profile (this vault)](../Magiclab.md)
- [MagicDog product page](https://www.magiclab.top/en/dog)
- [MagicDog-W product page](https://www.magiclab.top/en/dog-w)
- [MagicDog-Y1 product page](https://www.magiclab.top/en/dog-y)
- [MagicBot Z1 product page](https://www.magiclab.top/en/z1)
- [MagicArm R1 product page](https://www.magiclab.top/en/magicarm-r1)
- [MagicHand S01 product page](https://www.magiclab.top/en/parts/hand)
- [GitHub — MagiclabRobotics organisation](https://github.com/MagiclabRobotics)
- [GitHub — magicdog_ros2_sdk](https://github.com/MagiclabRobotics/magicdog_ros2_sdk)
- [GitHub — Magic-W0](https://github.com/MagiclabRobotics/Magic-W0)
- [GitHub — magicbot-gen1_pi0_demo](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo)
- [EqualOcean — MagicLab targets European logistics, Slovenia postal partnership (Sep 2026)](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)
