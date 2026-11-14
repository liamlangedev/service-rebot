---
type: challenge-playbook
company: "Flexiv Robotics"
slug: Flexiv
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Flexiv Robotics × T03 — Hackathon Playbook

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Brief](Flexiv-T03-1-Brief.md) · [Products and solutions](Flexiv-T03-2-Products-and-Solutions.md)

**Assumptions (verify at the booth in the first 30 minutes):** one Rizon 4 / 4s with a Grav gripper, RDK licence active, wired LAN to your laptop. No camera, no mobile base, no pretrained model supplied. Flexiv has no sustainability deployments — the domain logic is yours; the arm contributes **touch**.

**Design principle for all concepts:** use force as a *sensor*, not only as a safety feature. That is the one thing other arms on site do less well, and it is what judges will remember.

## Solution approaches

### Concept 1 — Touch-verified recyclables sorter (safest)

- **Problem → value:** Mixed tourist waste (PET, aluminium cans, glass, cartons) is mis-sorted because cameras confuse look-alike materials. A gentle squeeze tells them apart: fewer contaminated recycling batches, higher recovery. Fits Swiss separate-collection habits and hotel back-of-house in Leukerbad.
- **Hardware:** Rizon 4 / 4s + Grav (or Grav Enhanced for round items) · one USB / depth camera above the table (bring your own) · 3–4 labelled bins. Optional: D-Robotics RDK X5 for on-edge vision.
- **Architecture / stack:**
  - Perception: overhead camera → small detector (open-vocabulary or YOLO fine-tuned on a public waste dataset) → pick pose via table-plane calibration.
  - Planning: simple state machine in Python (detect → pick → squeeze test → classify → place).
  - Control: `flexivrdk` non-real-time primitives for moves and contact; gripper closes at 2–3 force levels while you log finger width → stiffness feature; arm wrench gives weight. Fuse vision class + stiffness + weight with a tiny classifier.
  - Compute: laptop; no GPU needed if the detector is small.
- **48-hour plan:**
  - H0–6: RDK connection, run example programs, gripper open/close with force, camera-to-robot calibration.
  - H6–24: pick-and-place loop on 4 object classes; record squeeze curves for ~20 objects per class.
  - H24–40: fusion classifier, confusion matrix **vision-only vs. vision + touch**, bin-full counter, simple dashboard (kg recovered, estimated CO2e avoided using a cited factor).
  - H40–48: robustness runs, video backup, pitch.
- **3-minute demo script:** (0:00) show two look-alike items a camera confuses (clear PET vs. glass bottle). (0:30) robot picks each, squeezes, sorts correctly; live plot of the squeeze curve. (1:30) judge throws in an unseen item. (2:15) show accuracy delta and the dashboard. (2:45) scale-up slide: same logic on a faster parallel robot at a sorting line.
- **Risks and fallbacks:** grasp failures on crumpled items → restrict to 4 rigid classes; vision calibration drift → fixed fiducial on the table; if the camera fails entirely → pure touch sorting from a fixed pick point still demos the core idea.
- **Judging angles:** *Innovation* — multimodal material ID by touch. *Technical depth* — measured accuracy gain. *Impact* — contamination is the real cost driver in recycling. *Leukerbad* — hotels and thermal baths generate concentrated PET / glass streams.

### Concept 2 — Force-guided charger plug-in for e-bikes / EVs

- **Problem → value:** Shared e-bikes, rental EVs and service robots sit uncharged or hog chargers. An arm that plugs and unplugs lets one charger serve several vehicles in sequence — fewer chargers, better use of off-peak or solar power. E-bike and EV rental is realistic in a car-light resort.
- **Hardware:** Rizon 4s + Grav holding a real connector (Type 2 mock or e-bike charger plug) · socket mounted on a board you can move by a few centimetres · optional camera for coarse localisation. Cross-vendor: a quadruped or wheeled robot as the "vehicle" that parks imprecisely.
- **Architecture / stack:**
  - Perception: coarse socket pose from a fiducial or camera (±1–2 cm is enough).
  - Planning: approach pose → contact → search → insert → verify → retract.
  - Control: built-in contact / hole-search / compliant-insertion primitives; verify seating from the force profile and insertion depth. The NVIDIA Isaac cable-insertion workflow (Rizon 4 + Grav) is the conceptual template; do **not** try to reproduce RL training in 48 h.
  - Scheduling layer (the "sustainable" part): a small script that decides which vehicle charges when, using a mock solar / tariff signal.
  - Compute: laptop.
- **48-hour plan:**
  - H0–6: RDK up; 3D-print or clamp a plug holder; first manual insertion in free-drive to learn forces.
  - H6–24: scripted insertion with deliberate ±15 mm / few-degree offsets; log success rate.
  - H24–40: unplug, multi-socket sequence, charging scheduler + dashboard.
  - H40–48: 20-trial reliability run, video, pitch.
- **3-minute demo script:** (0:00) the problem in one sentence. (0:20) judge shifts the socket board; robot finds and mates the plug by feel. (1:20) force trace on screen shows search and seating. (1:50) robot moves the plug from "vehicle A" to "vehicle B" when the scheduler says so. (2:30) numbers: success rate, chargers saved per fleet.
- **Risks and fallbacks:** real Type 2 plugs need high insertion force (Rizon 4s tops out at 150 N; Rizon 4 at 200 N) → use an e-bike or low-force connector; plug slips in the gripper → rigid adapter bolted to the flange; no live mains voltage on the demo socket — ever.
- **Judging angles:** *Technical depth* — contact-rich insertion with measured tolerance. *Impact* — charger utilisation. *Leukerbad* — e-bike rental and hotel parking. *Honesty* — say clearly this is not a Flexiv product.

### Concept 3 — Repair-not-replace: constant-force refurbishing cell

- **Problem → value:** Rental skis, snowboards, wooden furniture and fittings are discarded when the surface is worn. Consistent robot refinishing extends life and cuts scrap from over-sanding. Builds on Flexiv's most proven application (shutter sanding, polishing).
- **Hardware:** Rizon 4 (Rizon 10 if available for higher push force) + hand sanding block / abrasive pad / wax scraper clamped in Grav or bolted to the flange · a worn ski or wooden panel. Optional: SKYLANDX MetaCam to scan the part.
- **Architecture / stack:**
  - Perception: either teach the surface by free-drive (three corner points) or use a scan; detect worn zones with a camera before / after.
  - Planning: raster path over the surface (own code or `flexiv_pdk` scan-path tools).
  - Control: constant normal force along the path via force primitives; record the force map and passes per zone → "digital repair record".
  - Compute: laptop.
- **48-hour plan:**
  - H0–6: RDK up, tool mount, contact + constant-force stroke on a flat board.
  - H6–24: curved surface (ski tip), raster path, force logging.
  - H24–40: before / after camera comparison, adaptive passes only where worn (saves abrasive and time), repair report.
  - H40–48: polish demo, dust control, pitch.
- **3-minute demo script:** (0:00) worn ski, cost and CO2e of a new pair (cited). (0:30) robot finds the surface by touch, runs constant-force passes; live force map. (1:45) before / after image; only worn zones were treated. (2:20) repair passport and life-extension estimate.
- **Risks and fallbacks:** dust and noise indoors → use non-woven pads, wax scraping or wipe-cleaning instead of sanding; powered sander unavailable → manual block is enough to show force control; venue may forbid abrasives — ask organisers early.
- **Judging angles:** *Impact* — circular economy with a local product (ski rental). *Technical depth* — force map, adaptive passes. *Innovation* — moderate; strengthen with the repair passport.

### Concept 4 — Feel-your-way disassembly for reuse (most ambitious)

- **Problem → value:** Small e-waste (power-tool and e-bike battery packs, routers, chargers) is shredded because manual disassembly is too costly; cells and boards could be reused. A robot that unscrews, unclips and unplugs by feel raises recovery of reusable parts.
- **Hardware:** Rizon 4s + Grav (plus a small electric screwdriver triggered by controller digital output) · camera · **dummy** battery housing with no live cells. Cross-vendor: WUJI hand for clips and cables; second Flexiv arm if two are free (leader–follower teleop data via Flexiv Trainer).
- **Architecture / stack:**
  - Perception: detect screws / connectors (small detector), coarse pose only.
  - Planning: an LLM or behaviour tree sequences skills (locate screw → engage → unscrew → lift lid → unplug connector → sort parts).
  - Control: each skill is a force primitive with success checks from torque / force; optional learned skill (ACT-style via Flexiv Trainer, LeRobot data) for the one step that resists scripting.
  - Compute: laptop + GPU if you train a policy.
- **48-hour plan:**
  - H0–6: RDK up; pick one product and freeze the scope to **three skills**.
  - H6–24: scripted unscrew and lid lift with force checks.
  - H24–40: connector unplug (scripted or learned), part sorting, skill sequencer.
  - H40–48: end-to-end runs, failure recovery, pitch.
- **3-minute demo script:** (0:00) pile of e-waste, what is lost by shredding. (0:30) robot unscrews, opens, unplugs and sorts cell pack / PCB / housing into three trays. (2:00) show force traces used as success checks and one live recovery from a failed step. (2:30) value recovered per unit.
- **Risks and fallbacks:** scope explosion → demo a single product; teleop needs a second Flexiv arm → fall back to free-drive teaching and scripted skills; **never** open real lithium packs at the venue.
- **Judging angles:** *Innovation and depth* — highest of the four. *Impact* — battery reuse is a recognised bottleneck. *Leukerbad* — weaker; link to e-bike fleets and regional recycling.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Flexiv arm + **D-Robotics RDK X5** | Low-power edge vision for the sorter (strengthens the "low-power AI" angle). Naming trap: D-Robotics "RDK" is a board, Flexiv "RDK" is an SDK | Low — camera node publishes detections over LAN / ROS 2 |
| Flexiv arm + **Unitree Go2 / Genisom quadruped** | Quadruped collects or carries litter to a fixed sorting station; or acts as the "vehicle" for plug-in charging | Medium — hand-off point and timing only, no shared control |
| Flexiv arm + **Galaxea / Galbot / AGIBOT wheeled manipulator** | Mobile robot fetches bins or parts, Flexiv does the contact-critical step | Medium–high — two stacks, coordinate via simple messages |
| Flexiv arm + **SKYLANDX MetaCam** | 3D scan of a part or room to plan refinishing paths or map waste points | Medium — offline scan → point cloud → path |
| Flexiv arm + **XREAL glasses** | Operator sees class, confidence and force trace over the workcell; nice for the demo | Low–medium — display-only overlay |
| Flexiv arm + **WUJI Hand** | Dexterous unclipping and cable handling for disassembly | High — mechanical adapter, power, separate SDK; flange fit ⚠️ unverified |
| Flexiv arm + **Leadshine drive / motor** | Small conveyor or turntable for a continuous sorting line, triggered by controller I/O | Medium — mechanical build time is the cost |

## Questions to ask the Flexiv Robotics engineers on site

1. Which arms and grippers are here, how many, and how is robot time shared between teams?
2. Is the RDK licence activated, which RDK / robot software version is installed, and which primitives are available on it (contact, hole search, compliant insertion, surface following)?
3. Can the Grav gripper report finger width and measured grip force fast enough to build a squeeze-stiffness signal? What is the update rate?
4. Is a camera module, calibration tool or example hand-eye calibration available, or do we bring everything?
5. May we mount our own tool on the flange (sanding block, screwdriver, plug holder)? Are adapter plates and the tool-payload setup procedure available?
6. Can we use the controller's digital I/O to trigger an external device (conveyor, screwdriver, light)? What voltage / wiring?
7. Is a real-time Linux laptop provided for 1 kHz control, or should we stay with non-real-time primitives?
8. Has Flexiv done EV-charging, recycling or disassembly projects that are not public? Any reference parameters for connector insertion forces?

## Decision rule

- **Pick Flexiv Robotics for T03 if** your idea's hard part is *physical contact with uncertain objects* (sorting by feel, plug-in, refinishing, disassembly), you can supply your own camera and vision model, and a stationary indoor cell is acceptable.
- **Avoid if** your concept needs mobility, outdoor or sub-zero operation, a ready-made AI model, or is mainly about sensing, energy data or building automation — choose a mobile platform or an edge-AI vendor instead.

## Sources

- [Flexiv — Rizon product page](https://www.flexiv.com/product/rizon)
- [Flexiv — Grav product page](https://www.flexiv.com/product/grav)
- [Flexiv — Robot System page](https://www.flexiv.com/product/robot-system)
- [Flexiv — user cases](https://www.flexiv.com/partner/case)
- [Flexiv — Automated Shutter Sanding Solution case](https://www.flexiv.com/partner/case/Flexiv's_Automated_Shutter_Sanding_Solution)
- [Flexiv — polishing story](https://www.flexiv.com/story/polish)
- [Flexiv RDK manual](https://www.flexiv.com/software/rdk/manual/v2.x/index.html)
- [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk)
- [GitHub — flexiv_trainer](https://github.com/flexivrobotics/flexiv_trainer)
- [GitHub — flexivrobotics organisation](https://github.com/flexivrobotics)
- [Robotics 24/7 — Flexiv Rizon 4 now supported in NVIDIA Isaac (2026-09-24)](https://www.robotics247.com/article/flexix-rizon-4-adaptive-robot-now-supported-in-nvidia-isaac/Flexiv_Robotics)
- [Flexiv Robotics profile (internal, general research)](../Flexiv.md)
