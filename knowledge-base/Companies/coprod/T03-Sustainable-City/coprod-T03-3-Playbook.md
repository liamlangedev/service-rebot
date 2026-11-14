---
type: challenge-playbook
company: "coprod Inc."
slug: coprod
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# coprod Inc. × T03 — Hackathon Playbook

⬆ [coprod Inc. profile](../coprod.md) · [Brief](coprod-T03-1-Brief.md) · [Products and solutions](coprod-T03-2-Products-and-Solutions.md)

**Read first:** fit is **1/5**. coprod supplies motor control and power modules, not a robot. Every concept below needs (a) coprod kits actually available on site, (b) SDK access handed over by the team, (c) a real-time Linux host, and (d) mechanics you build yourself. **Confirm all four in the first hour** or switch vendor. Nothing here is a proven coprod use case — these are our proposals.

## Solution approaches

### Concept 1 — Smart sorting gate (safest)

- **Problem → value:** mixed recyclables in hotel and spa bins get contaminated. A camera-driven diverter at the bin opening routes each item to the right fraction; no arm needed.
- **Hardware:** 1–2 × **co:motion** + motor, **co:power**, optional **co:battery**; a chute or mini conveyor from cardboard / 3D print; USB camera; laptop. Optional: **D-Robotics RDK X5** for on-device vision.
- **Architecture / stack:** camera → small image classifier (open model or one trained on 4–5 local classes: PET, alu, glass, paper, residual) → rule-based bin choice → `cosystem` position command to the flap → return. Vision on laptop or RDK; EtherCAT master on the real-time Linux host; log regulator telemetry per cycle.
- **48-hour plan:**
  - **H0–6:** get SDK + one axis spinning from Python; sketch the chute; collect 200+ photos of items.
  - **H6–24:** build the mechanics; train the classifier; closed loop for 2 classes.
  - **H24–40:** extend to 4 classes or a second axis; add a live dashboard (count per fraction, contamination avoided, energy readout if available).
  - **H40–48:** tune speed, rehearse, record a backup video.
- **3-minute demo script:** state the contamination problem (20 s) → judge drops 6 items, gate routes them live (90 s) → dashboard shows counts and power draw (30 s) → show the two-module wiring and the ~20 lines of control code (30 s) → scale-up story (10 s).
- **Risks and fallbacks:** no kit / no SDK → run the same concept on a hobby servo or a Dobot Magician and drop coprod. Classifier weak → reduce to 2 classes with controlled lighting. Jams → wider chute, slower cadence.
- **Judging angles:** innovation low–medium · technical depth medium (perception-to-actuation loop) · impact clear and measurable · **Leukerbad:** tourist resort with many multilingual guests who mis-sort waste.

### Concept 2 — Snow-shedding solar tilt axis

- **Problem → value:** alpine PV loses winter yield under snow cover. A single tilt axis that follows the sun and tips steeply to shed snow recovers production without manual clearing.
- **Hardware:** 1 × **co:motion** + geared motor (or **co:act** if available), **co:sense** on the panel for tilt, **co:power**, **co:battery**; a small PV panel on a hinged frame; a light sensor or the panel's own output read by a separate microcontroller.
- **Architecture / stack:** sun-position calculation (time + location) → target tilt → position control; co:sense quaternion closes the loop on real panel angle; "snow detected" from a camera or from a drop in panel output → shed manoeuvre (steep tilt + short shake in velocity mode). All logic in one Python process on the host.
- **48-hour plan:**
  - **H0–6:** axis moving; frame design; decide the snow-detection signal.
  - **H6–24:** build frame; tilt control with IMU feedback; sun-tracking schedule in fast-forward.
  - **H24–40:** shed routine; simple yield model (fixed vs tracked vs tracked + shed); dashboard.
  - **H40–48:** test with real snow or a stand-in (flour, ice chips) on a tray; rehearse.
- **3-minute demo script:** problem (20 s) → fast-forward day of tracking (40 s) → dump "snow" on the panel, system detects and sheds (60 s) → show measured panel output before / after and the yield estimate (40 s) → modular parts story (20 s).
- **Risks and fallbacks:** hardware has **no published IP or temperature rating** — keep electronics dry and indoors, or under a cover; present as a bench prototype. Detection unreliable → manual trigger button. Motor torque too low → smaller panel, counterweight.
- **Judging angles:** innovation medium · technical depth medium (sensor-in-the-loop control) · impact easy to quantify in kWh · **Leukerbad:** 1,400 m, long snow season, roofs and south slopes.

### Concept 3 — Arm sorting cell with a coprod-driven infeed

- **Problem → value:** a robot arm alone sorts slowly because items arrive in a pile. A controlled infeed (conveyor or turntable) presents items one at a time and doubles as the energy meter for the cell.
- **Hardware:** **co:motion** + motor on a conveyor / turntable, **co:power**; arm from **Dobot** or **Flexiv** with gripper; camera; optional **D-Robotics** board.
- **Architecture / stack:** camera over the belt → detect + classify → Python coordinator: stop or slow the belt via `cosystem` velocity mode → send pick pose to the arm via the arm vendor's SDK → place in bin → resume. The two systems are coupled **in Python only**; the arm is not on coprod's EtherCAT bus.
- **48-hour plan:**
  - **H0–6:** both vendors' "hello world" independently; agree a shared coordinate frame.
  - **H6–24:** belt mechanics; camera-to-arm calibration; stop-and-pick for one class.
  - **H24–40:** multi-class sorting; throughput and energy-per-item metrics.
  - **H40–48:** reliability runs, backup video.
- **3-minute demo script:** pile on the belt (20 s) → cell sorts 8–10 items (100 s) → metrics screen: items/min, purity, energy (30 s) → why a cheap modular axis beats a second arm (30 s).
- **Risks and fallbacks:** two SDKs and two support teams → split the team early. Belt slip / timing → stop-and-go instead of on-the-fly picking. coprod kit unavailable → hand-fed tray; the cell still works.
- **Judging angles:** innovation medium · technical depth high (multi-vendor integration) · impact strong (closest to a real sorting cell) · **Leukerbad:** small-scale sorting for hotels and clinics far from large recycling plants.

### Concept 4 — Torque-aware unscrewing tool for repair and disassembly (most ambitious)

- **Problem → value:** e-waste and broken appliances are shredded because opening them is manual work. A torque-controlled spindle that finds, loosens and removes screws is the first step to automated repair / parts harvesting.
- **Hardware:** **co:act** (or co:motion + small geared motor) as a screwdriver spindle with bit holder, **co:power**; mounted on a **Flexiv** or **Dobot** arm; camera for screw detection.
- **Architecture / stack:** camera → screw-head detection (classical circle detection or small detector) → arm moves the tool above the screw (arm SDK) → spindle engages in torque-limited mode, detects break-loose from the torque / velocity profile, counts turns to release → log torque curve per screw (stuck, stripped, OK). Requires torque or current read-back from the API — ⚠️ unverified.
- **48-hour plan:**
  - **H0–6:** confirm co:act availability and torque read-back; **if either is missing, drop this concept**.
  - **H6–24:** tool mount and bit coupling; manual-position unscrewing with torque logging.
  - **H24–40:** vision-guided positioning on one known device (e.g. an old router or power-tool housing).
  - **H40–48:** run 4–6 screws reliably; rehearse.
- **3-minute demo script:** e-waste problem (20 s) → robot finds and removes 3 screws, live torque plot on screen (100 s) → lid comes off, reusable parts shown (30 s) → roadmap to full disassembly (30 s).
- **Risks and fallbacks:** highest of the four — unreleased actuator, bit alignment, cam-out. Fallback: fixed jig with human positioning, robot only does the torque-aware unscrewing. Second fallback: pivot to Concept 3.
- **Judging angles:** innovation high · technical depth high (contact-rich control) · impact high but long-term · **Leukerbad:** weak direct link; frame it as circular economy for remote valleys with costly waste transport.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| coprod + **D-Robotics** (RDK X5) | Low-power on-device vision deciding, coprod actuating (Concept 1) | Low–medium — network link between RDK and the EtherCAT host; whether the master can run on the RDK itself is ⚠️ unverified |
| coprod + **Leadshine** | Motors / joint modules for co:motion to drive | Medium — electrical and encoder compatibility must be checked on site ⚠️ unverified |
| coprod + **Dobot** | Cobot or desktop arm picks, coprod runs infeed axis (Concept 3) | Medium — two SDKs coupled in Python |
| coprod + **Flexiv** | Force-controlled arm + coprod spindle for disassembly (Concept 4) | High — tool mounting, two real-time systems |
| coprod + **Unitree** / **AGIBOT** mobile robot | Custom add-on axis (hatch, sampler, tilt mount) on a mobile platform | High — power, mounting and a second control PC on the robot |

If your idea is a mobile or arm-centric T03 solution, the other vendor is the platform and coprod is optional.

## Questions to ask the coprod Inc. engineers on site

1. How many **co:motion + motor** sets can one team get today, and is any **co:act** available?
2. Can we get the **cosystem** package, a working example (wheel base or single axis) and docs right now? Which OS / kernel / network card does the EtherCAT master need?
3. Does the API expose **measured current, torque and bus power** per axis and per co:power submodule, and at what rate?
4. Does the brake submodule only dissipate regenerative energy, or can it return energy to the battery?
5. Which motors do you have matched to co:motion on site, and what are the voltage / current limits?
6. Is there a **ROS 2** bridge today, or Python / C++ only?
7. Can a third-party analog or digital sensor be read on the bus before the IO board ships, or must we use a separate microcontroller?
8. What are the environmental limits (temperature, moisture) — can anything go outdoors at 1,400 m in November?

## Decision rule

- **Pick coprod Inc. for T03 if** your idea is a small custom mechanism (1–3 axes), your team has mechatronics skills, and coprod confirms kits + SDK + an engineer for you within the first hour.
- **Avoid if** you need a finished robot, perception or autonomy out of the box, outdoor operation, or cannot afford to lose half a day on bring-up.

## Sources
- [coprod — official site (API sample, system specs)](https://coprod.co/)
- [coprod — products and roadmap](https://coprod.co/products.html)
- [coprod — systems](https://coprod.co/systems.html)
- [coprod — co:found programme](https://coprod.co/cofound.html)
- [Venture Kick — coprod receives CHF 40,000 (2 Apr 2026)](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)
- [coprod company profile (internal, general research)](../coprod.md)
