---
type: challenge-playbook
company: "Galaxea"
slug: Galaxea
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Galaxea × T03 — Hackathon Playbook

⬆ [Galaxea profile](../Galaxea.md) · [Brief](Galaxea-T03-1-Brief.md) · [Products and solutions](Galaxea-T03-2-Products-and-Solutions.md)

**Before you commit (first 30 minutes):** confirm at the booth (1) which robots are bookable — LEMO, R1 Lite or R1 Pro, (2) which teleop rig, (3) what GPU is available for training and inference. Concepts 1 and 4 assume LEMO or a fixed arm pair; Concepts 2 and 3 assume an R1.

**Rule for all concepts:** keep the "what is this object?" decision in a separate vision model (VLM or small classifier) and use the Galaxea robot for the motion. That gives a working demo even if policy training underperforms.

## Solution approaches

### Concept 1 — Hotel-scale recyclables sorting cell (safest)

- **Problem → value:** Hotels, spas and clinics produce small mixed waste streams that are too small for industrial sorting and too tedious for staff. A desktop cell sorts PET, aluminium, glass and paper at the source → higher recycling purity, a measurable kg-diverted number.
- **Hardware:** LEMO (or two A1Z arms, or a parked R1 using only its arms) + top camera + 4 bins. Optional: Leadshine stepper + drive for a mini conveyor; D-Robotics RDK X5 running the material classifier.
- **Architecture / stack:**
  - Perception: top camera → VLM or fine-tuned small classifier → class + pick point.
  - Planning: state machine "detect → pick → drop in bin(class)"; second arm singulates or holds a bag open.
  - Control: option A scripted Cartesian picks through the SDK; option B small ACT / diffusion policy per class trained on 50–100 teleop demos in LeRobot format; option C G0.5 with a language prompt per item.
  - Compute: classifier on edge board, policy on a laptop / workstation GPU.
- **48-hour plan:**
  - H0–6: robot access, teleop working, bins and mock waste (clean, dry), camera calibration.
  - H6–24: classifier on 4 classes; scripted pick baseline; record 50–100 demos in parallel.
  - H24–40: train and compare learned policy vs scripted; add counter dashboard (items, estimated kg, purity).
  - H40–48: 20-item endurance runs, failure handling (re-grasp, "unknown" bin), rehearsal.
- **3-minute demo script:** tip a mixed tray onto the table → robot sorts 8–10 items live → dashboard shows class, count and purity → judge drops in an unseen item → robot routes it or sends it to "unknown" → close with yearly extrapolation for one hotel (state assumptions).
- **Risks and fallbacks:** transparent PET and crushed cans are hard to grasp → pre-select gripper-friendly items (uncrushed bottles, rigid cans); policy fails → scripted picks; LEMO not on site → use R1 arms from a fixed position.
- **Judging angles:** innovation medium · technical depth medium (learned vs scripted comparison helps) · impact clear and measurable · Leukerbad relevance high (tourism waste peaks, small decentralised sites).

### Concept 2 — Table clearing with source separation (mobile)

- **Problem → value:** In breakfast rooms and spa cafés, everything on a table goes in one bin. A mobile dual-arm robot clears the table and separates reusable dishes, recyclables and food waste on the spot → less residual waste, less staff time.
- **Hardware:** R1 Lite or R1 Pro + a cart with three containers. Optional: XREAL glasses for a staff "what goes where" overlay; SKYLANDX MetaCam to map the room.
- **Architecture / stack:**
  - Perception: head + wrist cameras → VLM labels each item as reuse / recycle / organic / residual.
  - Planning: per-item language instruction ("put the can in the blue bin").
  - Control: G0.5 `g05-base` zero-shot first; fine-tune or train a small policy on about 20–50 demos per item family (the G0 paper reports table bussing fine-tuned from 20 demos). Deployment through the GalaxeaVLA policy server + ROS 2 client or EFMNode.
  - Navigation: fixed table and cart poses; use the vendor navigation stack only if it works out of the box.
  - Compute: off-board RTX-class GPU.
- **48-hour plan:**
  - H0–6: zero-shot G0.5 pick-and-place test on real tableware; decide zero-shot vs fine-tune.
  - H6–24: teleop data for the weak items; VLM routing logic; bin layout.
  - H24–40: integrate the loop for one table; add second table only if stable.
  - H40–48: timing runs, recovery behaviours, rehearsal.
- **3-minute demo script:** table with cup, plate, can, napkin, apple core (mock) → robot clears five items into three containers → screen shows the VLM decision per item → end with separation rate over all rehearsal runs.
- **Risks and fallbacks:** zero-shot fails on local objects → restrict to 4–5 rigid items; navigation unreliable → park the robot at the table; no fine-tune GPU → small ACT policy or scripted grasps.
- **Judging angles:** innovation medium · technical depth high if the VLA runs live · impact moderate · Leukerbad relevance high (hotels, clinics, thermal baths).

### Concept 3 — Night energy patrol for hotel and clinic rooms

- **Problem → value:** Empty rooms with lights on, windows tilted open and thermostats high waste heating energy — a real cost at 1,400 m in winter. A robot patrols unoccupied rooms, detects waste states, fixes the simple ones physically and logs the rest → retrofit-free building automation for old buildings.
- **Hardware:** R1 Pro (floor-to-2 m reach for switches, thermostats, window handles) or R1 Lite. Optional: SKYLANDX MetaCam for a fast 3D map; D-Robotics board for low-power detection; a temperature / CO2 sensor on the robot.
- **Architecture / stack:**
  - Perception: VLM checklist per room (lights on? window open? radiator valve setting?).
  - Planning: waypoint list per room → action per finding.
  - Control: scripted or teleop-learned primitives for "press switch" and "turn thermostat dial"; the Open-World Dataset includes an air-conditioner adjustment task, so G0.5 may handle panel interaction zero-shot ⚠️ unverified — test early.
  - Reporting: dashboard with findings, actions and estimated kWh saved (state the assumptions).
- **48-hour plan:**
  - H0–6: build a mock wall (light switch, thermostat dial, window handle); test reach and zero-shot behaviour.
  - H6–24: VLM state detection; one reliable primitive (light switch).
  - H24–40: second primitive (thermostat); two-waypoint patrol; dashboard.
  - H40–48: full patrol runs and rehearsal.
- **3-minute demo script:** robot drives to mock room A → reports "light on, thermostat at 5" → switches the light off and turns the dial down → drives to room B → flags an open window it cannot close → dashboard shows the night's savings estimate.
- **Risks and fallbacks:** fine manipulation of small switches fails → larger rocker switches, or detect-and-report only for hard items; navigation fails → rooms side by side on one wall; savings numbers challenged → show the calculation openly.
- **Judging angles:** innovation high · technical depth medium · impact plausible but needs honest numbers · Leukerbad relevance high (old hotel stock, heating-dominated energy use).

### Concept 4 — Dual-arm disassembly for repair and reuse (most ambitious)

- **Problem → value:** Small electronics and rental equipment are thrown away because disassembly is manual and slow. One arm holds, the other unscrews and separates battery, board and housing → enables repair, battery-safe recycling and parts reuse.
- **Hardware:** LEMO with A1Z-T leader arms (force-controlled, ±0.1 mm) + a powered screwdriver end effector or bit holder. Optional: WUJI Hand for clips and connectors; Flexiv Rizon for high-force prying; OriginFlow EMG capture to record expert human demonstrations.
- **Architecture / stack:**
  - Perception: top camera → screw detection and device-type recognition.
  - Planning: per-device disassembly sequence (hand-written for one device).
  - Control: teleop-learned unscrew primitive (the published LEMO example is screw insertion and fastening — the reverse motion) + scripted part removal and sorting; shared autonomy: human teleoperates the hard step, robot repeats the easy ones.
  - Compute: workstation GPU for policy; classical vision is enough for screws.
- **48-hour plan:**
  - H0–6: pick one device with 4 large, visible screws; build a fixture; fit the tool.
  - H6–24: teleop the full sequence; record 50+ unscrew demos; screw detector.
  - H24–40: automate unscrew + lift cover; keep battery removal teleoperated if needed.
  - H40–48: repeatability runs, sort parts into bins, rehearsal.
- **3-minute demo script:** place device in fixture → robot locates and removes 4 screws → second arm lifts the cover → battery goes to a safe bin, housing to plastics → show time vs manual and which steps were autonomous.
- **Risks and fallbacks:** no suitable screwdriver tool → use large thumb-screws or a 3D-printed bit holder; cam-out and stuck screws → shared-autonomy mode; too ambitious → reduce to "remove cover and sort two parts".
- **Judging angles:** innovation high · technical depth high (contact-rich, bimanual) · impact strong circular-economy story · Leukerbad relevance medium (ski and e-bike rental equipment, hotel electronics).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Galaxea LEMO + D-Robotics RDK X5 | Material classifier on a few watts; credible "low-power edge AI" story | Low — camera + network message to the arm controller |
| Galaxea LEMO + Leadshine drive and motor | Mini conveyor feeding the sorting cell → continuous throughput | Medium — mechanical build and speed sync |
| Galaxea R1 + SKYLANDX MetaCam | Fast 3D map of rooms for the energy patrol | Medium — map format and localisation hand-over ⚠️ unverified |
| Galaxea R1 / LEMO + XREAL glasses | Operator overlay for exceptions ("unknown item") or remote assist | Low to medium — separate app, loose coupling |
| Galaxea arms + WUJI Hand | Clips, connectors and soft items in disassembly | High — mounting, wiring and control in 48 h is risky |
| Unitree Go2 (outdoor scout) + Galaxea R1 (indoor sorter) | Quadruped finds and reports litter outdoors; R1 sorts what is brought in | High — two stacks; keep the hand-over manual |
| Galaxea LEMO + OriginFlow | Human expert demonstrations as extra training signal | High — research-grade, unproven pipeline |

## Questions to ask the Galaxea engineers on site

1. Which robots can teams book (LEMO, R1 Lite, R1 Pro), how many units, and in what time slots?
2. Is there an 80 GB-class GPU for G0.5 fine-tuning, or should we plan zero-shot / small policies only?
3. Which G0.5 checkpoint and deployment path is pre-installed — GalaxeaVLA policy server or EFMNode — and how do we pass a language instruction at runtime?
4. Does LEMO Studio export LeRobot-format data and can it run our own ACT / diffusion policy?
5. What Cartesian and force-control APIs are exposed for scripted picks (rate, frames, force limits)?
6. Which end effectors are fitted, what are the gripper stroke and force, and may we mount a custom tool (screwdriver bit, bag holder)?
7. Is autonomous navigation on the R1 usable out of the box in the venue, or should we stay at fixed positions?
8. Any restrictions on handling liquids, food or dirty items near the robot?

## Decision rule

- **Pick Galaxea for T03 if** your idea is an indoor manipulation task — sorting, clearing, disassembly or switch / dial operation — and you want to teach it by teleoperation with a vision model deciding what goes where.
- **Avoid if** the idea is outdoors, sensing- or analytics-driven, needs rough-terrain mobility, or depends on a proven sustainability product rather than a platform you program yourself.

## Sources
- [Galaxea profile (general research)](../Galaxea.md)
- [Galaxea blog — LEMO launch (9 Nov 2026)](https://galaxea-dynamics.com/blogs/robotics-insights-news/two-arms-one-platform-galaxea-launches-lemo)
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics)
- [GitHub — OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA)
- [GitHub — OpenGalaxea/EFMNode](https://github.com/OpenGalaxea/EFMNode)
- [GitHub — OpenGalaxea/GalaxeaLeRobotToolkit](https://github.com/OpenGalaxea/GalaxeaLeRobotToolkit)
- [GitHub — OpenGalaxea/GalaxeaManipSim](https://github.com/OpenGalaxea/GalaxeaManipSim)
- [Hugging Face — Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset)
- [arXiv 2509.00576 — Galaxea Open-World Dataset and G0 dual-system VLA](https://arxiv.org/html/2509.00576v1)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)
