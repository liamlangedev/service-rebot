---
type: challenge-playbook
company: "Dobot Robotics"
slug: Dobot
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Dobot Robotics × T03 — Hackathon Playbook

⬆ [Dobot Robotics profile](../Dobot.md) · [Brief](Dobot-T03-1-Brief.md) · [Products and solutions](Dobot-T03-2-Products-and-Solutions.md)

> **Before anything else (15 min at the booth):** which arms are free, which end-effectors (suction, gripper), controller firmware (need **V4.4.0.0+** for the V4 repos), and whether a camera and conveyor are available. All concepts below assume the hardware is a best guess, not a confirmed list.

## Solution approaches

### Concept 1 — Recyclables sorting cell with an energy receipt (safest)

- **Problem → value:** Guests in a resort mis-sort waste; contaminated recycling gets burned. A small cell re-sorts mixed light recyclables (PET, alu cans, cartons, batteries) and reports diversion rate and **energy used per item**, so the automation's own footprint is visible.
- **Hardware:** Magician E6 (750 g, 450 mm) or MG400 (500 g, faster, top-down only) + suction cup or gripper + any USB / RealSense camera above the tray. Optional: D-Robotics RDK X5 for on-device inference; Dobot mini conveyor if on site.
- **Architecture / stack:**
  - Perception: fixed overhead camera → detector (YOLO-family fine-tuned on a public litter dataset, or a VLM for zero-shot material label) → pixel-to-table transform via a 4-point homography or hand-eye calibration.
  - Planning: pick highest-confidence item → fixed bin pose per class; low-confidence items go to a "human check" bin.
  - Control: `TCP-IP-Python-V4` (MovJ / MovL + digital output for suction) for E6; `TCP-IP-4Axis-Python` for MG400.
  - Compute: laptop, or RDK X5 for a low-power edge story. Dashboard in a browser.
  - Energy: use rated power from Dobot (E6 130 W, MG400 150 W) or a plug-in power meter for measured Wh.
- **48-hour plan:**
  - H0–6: arm moving from Python; camera mounted; table calibration; scripted pick-place of one object.
  - H6–24: detector on 4–5 classes; closed loop pick → sort; suction reliability per material.
  - H24–40: dashboard (counts, contamination, Wh per item); uncertain-item bin; run 100-item endurance test.
  - H40–48: freeze code, film a backup video, rehearse.
- **3-minute demo script:** (0:00) dump a mixed handful on the tray → (0:20) robot sorts while the dashboard counts → (1:30) judge throws in an odd item; it goes to "human check" → (2:10) show Wh per item and yearly extrapolation for one hotel → (2:40) what scales: bigger arm, conveyor, same code.
- **Risks and fallbacks:** suction fails on crumpled items → use a gripper or restrict classes; detector weak → colour / shape rules or fiducial-tagged items; calibration drift → clamp the camera, re-run the 4-point routine.
- **Judging angles:** innovation low-to-medium (well-trodden); technical depth medium; impact clear and quantified; Leukerbad relevance: hotel and spa waste streams, seasonal tourist peaks.

### Concept 2 — Second-life triage station for batteries and small electronics

- **Problem → value:** Loose batteries and small devices in residual waste are a fire risk and a lost resource. A station **inspects, tests and grades** each item into reuse / repair / recycle / hazardous — the pattern Dobot's Breezy reference uses for refurbished electronics.
- **Hardware:** Nova 2 or Nova 5 (or CR3A / Magician E6) + gripper + two cameras (overhead, close-up) + a simple test fixture (contact pads to an ADC on an Arduino or D-Robotics RDK board for voltage). Optional: XREAL glasses to show the operator each item's grade.
- **Architecture / stack:**
  - Perception: detect item → close-up image → VLM / OCR reads chemistry and label, flags swelling or damage.
  - Test: arm places the cell on the fixture; microcontroller reads open-circuit voltage; result joins the image verdict.
  - Planning: rule table (chemistry + voltage + damage → bin). Log every item to a CSV "material passport".
  - Control: V4 Python or ROS 2 Humble + MoveIt (`DOBOT_6Axis_ROS2_V4`) if you need collision-aware motion around the fixture.
  - Compute: laptop; VLM local or cloud.
- **48-hour plan:**
  - H0–6: arm + gripper + fixture mechanical mock-up; voltage read over serial.
  - H6–24: pick → present to close-up camera → place on fixture → bin; label reading on 3 battery types.
  - H24–40: damage / swelling check, passport log, dashboard; add one small-device class (e.g. earbuds case) if time.
  - H40–48: rehearse, backup video.
- **3-minute demo script:** (0:00) why batteries in waste matter → (0:20) robot picks an AA, reads label, tests voltage: "reuse" → (1:00) a button cell: "recycle" → (1:30) a damaged Li-ion pouch mock-up: "hazardous", routed to a sand box → (2:10) passport log and totals → (2:40) link to Breezy-style refurbishment at scale.
- **Risks and fallbacks:** real damaged Li-ion cells are a **safety hazard — use dummies**; small round cells are hard to grasp → V-groove tray and suction; label reading unreliable → fall back to size / shape class plus voltage.
- **Judging angles:** innovation medium-high; technical depth medium-high (multi-sensor decision); impact strong (fire prevention, reuse); Leukerbad relevance: remote valley, costly waste transport, many seasonal devices (rental gear, hotel electronics).

### Concept 3 — Off-grid reusable-cup return kiosk

- **Problem → value:** Events, ski huts and spas burn through single-use cups. A battery-powered kiosk accepts reusable cups, checks them (clean enough / damaged / foreign object), stacks them for washing and credits a deposit — proving a robot cell can run on a small DC supply.
- **Hardware:** Nova 2 (2 kg, typical **100 W**, controller takes **30–60 V DC**) + gripper + camera; a 48 V battery pack (ask the organisers or Dobot what is allowed) with a power meter. Optional: Unitree or Galaxea mobile robot to carry full stacks away; D-Robotics board for edge vision.
- **Architecture / stack:**
  - Perception: camera at the drop slot → classifier (cup OK / dirty / not a cup).
  - Planning: state machine — accept, stack by type, reject, "stack full" signal.
  - Control: V4 Python; collision level set conservatively because the public stands close; I/O for a slot light or lock.
  - Compute: edge board; QR code on screen for the deposit credit (mock payment only).
  - Energy: log battery Wh per 100 cups.
- **48-hour plan:**
  - H0–6: confirm DC supply option with Dobot engineers; if not approved, run on the standard supply and meter it. Scripted grasp and stack.
  - H6–24: classifier; stacking with height tracking; reject path.
  - H24–40: deposit UI, energy log, enclosure / reach limits for safety.
  - H40–48: public-style dry run with strangers, backup video.
- **3-minute demo script:** (0:00) judge drops a cup → (0:15) robot inspects, stacks, screen credits deposit → (0:50) drop a dirty cup and a non-cup: sorted and rejected → (1:40) show live watt draw and "cups per kWh" → (2:20) cost and waste avoided for one season.
- **Risks and fallbacks:** DC / battery operation may not be permitted on site → mains + power meter keeps the energy story; transparent cups confuse depth cameras → use RGB and a backlit slot; public interaction → physical barrier and low speed.
- **Judging angles:** innovation medium; technical depth medium; impact tangible and easy to grasp; Leukerbad relevance high (spas, mountain restaurants, events).

### Concept 4 — Learned disassembly for repair and reuse (most ambitious)

- **Problem → value:** Repair and material recovery fail at the manual step: opening a device, removing the battery, separating parts. Teach that step by teleoperation and let a policy repeat it.
- **Hardware:** X-Trainer (2 × Nova 2, leader handles, RGB + depth) — only if it is on site with booth support. Optional: Flexiv Rizon or ROKAE xMate for a force-controlled unscrewing step; WUJI hand for fine manipulation; OriginFlow for extra demonstration capture.
- **Architecture / stack:**
  - Data: teleoperate 50–100 episodes of one narrow task (e.g. open a battery compartment and lift the cell out of a fixed-pose device) with `dobot_xtrainer`.
  - Learning: imitation policy (ACT-style or diffusion). **Which policies Dobot's stack supports is not public — ask on site**; otherwise export episodes and train with an open framework.
  - Control: 25 Hz end-to-end interface on the X-Trainer; scripted pre- and post-steps (present device, drop parts into bins) via V4 API.
  - Compute: a GPU workstation or cloud GPU for training; inference on a laptop GPU.
- **48-hour plan:**
  - H0–6: get teleop working; fix the task, fixture and camera views; record 10 test episodes; confirm the training pipeline end-to-end on those.
  - H6–24: collect the full dataset; first training run overnight.
  - H24–40: evaluate, collect corrective episodes, retrain; add scripted sorting of removed parts.
  - H40–48: measure success rate over 20 trials; prepare teleop fallback demo.
- **3-minute demo script:** (0:00) the repair bottleneck → (0:20) 15 seconds of live teleoperation: "this is how we taught it" → (0:45) autonomous run on a fresh device → (1:45) parts dropped into battery / plastic / PCB bins → (2:15) success rate, hours of data, what a second task would cost.
- **Risks and fallbacks:** undocumented training stack → switch to scripted motion with a fixture; policy success below 50% → show a shared-autonomy mode (human teleoperates the hard 5 seconds); no GPU → cloud; again **no real Li-ion cells**.
- **Judging angles:** innovation high; technical depth high; impact strong for circular economy; Leukerbad relevance moderate (repair cafés, rental equipment) — weaker than Concepts 1–3.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Dobot E6 / MG400 + **D-Robotics** RDK X5 | Sorting cell with all inference on a low-power board: credible "low-energy edge AI" claim | Low — camera and model on the board, TCP/IP to the arm |
| Dobot Nova + **Unitree** Go2 / B2 or **Galaxea** R1 | Fixed sorting / return station fed or emptied by a mobile robot (litter or cup logistics) | Medium–high — two stacks, handover pose, scheduling |
| Dobot arm + **Flexiv** Rizon or **ROKAE** xMate | Dobot does fast pick-and-place; the force-controlled arm does unscrewing or prying for disassembly | Medium — shared workspace, two APIs |
| Dobot X-Trainer + **WUJI** Hand / **OriginFlow** | Finer manipulation or richer human demonstration data for disassembly | High — custom mounting and data alignment |
| Dobot arm + **SKYLANDX** MetaCam | 3D scan of a waste room or depot to place and size the cell (digital-twin slide) | Low — offline, presentation value only |
| Dobot arm + **XREAL** glasses | Operator sees class, confidence and grade overlaid; human handles the uncertain bin | Medium |
| Dobot arm + **Leadshine** drives | Build your own conveyor or carousel feeder | Medium — mechanical build time |

## Questions to ask the Dobot Robotics engineers on site

1. Which arms, how many, and which end-effectors (suction cup, electric gripper, camera) can teams actually use for 48 hours?
2. Is the controller firmware **V4.4.0.0 or later**, and is remote TCP/IP mode already enabled? What is each robot's IP?
3. For MG400: is conveyor tracking via the encoder input usable from the 4-axis Python API, and is a conveyor on site?
4. What is the fastest supported streaming interface (ServoJ / ServoP rate) for closed-loop visual servoing on E6 and Nova?
5. Can a Nova controller be run from a 48 V battery pack here, and what is the measured idle versus moving power draw?
6. X-Trainer: which policies does your pipeline train out of the box (ACT, diffusion, other), what is the episode data format, and what GPU do you recommend?
7. Is there a hand-eye calibration tool (DobotCameraCalibrate) you recommend for a third-party USB or RealSense camera?
8. Do you have any waste-sorting, refurbishment (Breezy) or EV-charging demo code or integrator contacts you can share, and is Kongyi DobotWAM accessible to teams in any form?

## Decision rule

- **Pick Dobot Robotics for T03 if** your idea is a fixed cell that sorts, inspects or grades small objects (under about 750 g on desktop arms, up to 5 kg on Nova 5 / CR5A) and you want the robot part done on day 1 so the 48 hours go into perception, metrics and the sustainability case.
- **Avoid if** the idea needs mobility, outdoor or wet operation, heavy objects, or true force control — or if you are counting on a ready-made waste / energy solution from the vendor; there is none.

## Sources

- [Magician E6 product page](https://www.dobot-robots.com/products/education/magician-e6.html)
- [MG400 product page](https://www.dobot-robots.com/products/desktop-four-axis/mg400.html)
- [Nova series product page](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html)
- [CRA series product page](https://www.dobot-robots.com/products/cra-series/dobot-cra-series.html)
- [X-Trainer product page](https://www.dobot-robots.com/products/humanoid-robots/x-trainer.html)
- [Bin picking / sorting application page](https://www.dobot-robots.com/applications/sorting.html)
- [Case study: Breezy refurbishment, Poland](https://www.dobot-robots.com/insights/case-studies/dobot-powers-breezys-robotic-solutions-to-transform-refurbishment-in-poland.html)
- [Dobot-Arm on GitHub (repository list)](https://github.com/Dobot-Arm?tab=repositories)
- [TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- [DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)
- [TCP-IP-4Axis-Python](https://github.com/Dobot-Arm/TCP-IP-4Axis-Python)
- [dobot_xtrainer](https://github.com/Dobot-Arm/dobot_xtrainer)
- [Dobot company profile (internal)](../Dobot.md)
