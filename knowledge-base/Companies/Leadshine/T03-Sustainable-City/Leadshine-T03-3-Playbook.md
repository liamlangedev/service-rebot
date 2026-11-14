---
type: challenge-playbook
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Leadshine Technology Co., Ltd. × T03 — Hackathon Playbook

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Brief](Leadshine-T03-1-Brief.md) · [Products and solutions](Leadshine-T03-2-Products-and-Solutions.md)

> **Framing:** Leadshine is a **2/5 supporting-role** vendor for T03. Every concept below uses a Leadshine part as one component; three of four need a host arm from another vendor. Which parts are on site is unconfirmed — check the Leadshine table before committing. All concepts assume **dry, clean objects** (no IP rating is published for the hands).

## Solution approaches

### Concept 1 — "Squeeze-to-sort" material identifier (hand only, no arm)

- **Problem → value:** Mis-sorted recyclables contaminate whole batches. A bench-mounted hand that takes an item from a person, squeezes it gently and classifies the material (rigid glass / deformable PET / crushable aluminium / carton) gives a low-cost sorting assistant for hotel back-of-house or a public recycling point.
- **Hardware:** DH116 with tactile sensors (‑M) or DH116S, clamped to a stand; laptop; USB camera; three or four labelled bins with LED strips. Optional: D-Robotics RDK X5 to run it laptop-free.
- **Architecture / stack:** camera frame → small image classifier or VLM for a first guess → hand closes under a force limit via LHandProLib (Python) → record finger position vs force / motor-current curve → simple classifier (stiffness and spring-back features, fused with vision) → light the correct bin. Compute on the laptop. Rehearse grasp poses in MuJoCo with the MJCF.
- **48-hour plan:**
  - **H0–6:** power and bus bring-up with the Windows GUI; confirm which signals the SDK exposes (position, current, tactile).
  - **H6–24:** scripted squeeze routine; log 20–30 squeezes per material; train the classifier.
  - **H24–40:** add camera fusion, bin LEDs, a tally screen (items sorted, estimated contamination avoided).
  - **H40–48:** robustness pass with unseen items; rehearse the pitch.
- **3-minute demo script:** hand a judge four items → the hand squeezes each → correct bin lights up → show the force curve live → deliberately hand a look-alike (clear PET vs clear glass) that vision alone gets wrong and touch gets right.
- **Risks and fallbacks:** tactile data not exposed in the SDK → use motor current and position only. Hand unavailable with sensors → same fallback. Crushing risk → conservative force limit, test on empties.
- **Judging angles:** innovation (touch as a sorting signal) · technical depth (sensor fusion, measured confusion matrix) · impact (contamination is the real cost in recycling) · Leukerbad (hotels and spa facilities generate mixed guest waste; Switzerland separates PET, glass and aluminium).

### Concept 2 — Dexterous recycling cell (hand on a host arm)

- **Problem → value:** Mixed tourist waste has irregular shapes that defeat suction cups and parallel grippers. A hand-equipped arm sorts a tray of mixed items into fractions without item-specific tooling.
- **Hardware:** DH116 (or DH116S on a low-payload arm) + a host arm — Flexiv Rizon, Dobot CR / Nova or ROKAE xMate — + RGB-D camera. Optional D-Robotics RDK for edge inference.
- **Architecture / stack:** RGB-D → open-vocabulary detector or VLM labels item and material → grasp-type lookup per class (power grasp for bottles, pinch for cans / caps, lateral for cartons) → arm vendor SDK or MoveIt for the reach → LHandPro ROS 2 service node for the grasp sequence → place in bin. Compute on a laptop with GPU; both devices bridged in ROS 2.
- **48-hour plan:**
  - **H0–6:** secure arm + hand; solve flange, cable and power; move each separately.
  - **H6–24:** hand-eye calibration; three grasp primitives; pick one item class end to end.
  - **H24–40:** add classes and bins; add tactile grasp-confirmation and re-grasp; count throughput.
  - **H40–48:** tune for reliability over speed; freeze the code; record a backup video.
- **3-minute demo script:** tip a tray of 6–8 mixed items → robot sorts them → a judge adds an unseen object → show the detector label and chosen grasp on screen → close with picks per minute and success rate.
- **Risks and fallbacks:** no mechanical adapter → 3D-print or bolt a plate (ask organizers for a workshop early). Integration overruns → fall back to Concept 1 on the bench with the arm doing a fixed hand-over motion. Judges ask "why not a gripper?" → have the irregular-object cases ready.
- **Judging angles:** innovation (moderate) · technical depth (multi-vendor ROS 2 integration, grasp selection) · impact (tool-free sorting of mixed streams) · Leukerbad (resort waste peaks with seasonal tourism).

### Concept 3 — Teleoperated e-waste disassembly with data capture

- **Problem → value:** Reuse and repair are blocked by manual disassembly cost. Teleoperating a dexterous hand to open a small device (remove a battery cover, pull a battery, unplug a connector) shows a path to remote or learned disassembly and produces demonstration data.
- **Hardware:** DH2116 (21 DoF) or DH116 + host arm (Flexiv Rizon preferred for force control) + XREAL glasses for hand tracking, or OriginFlow EMG capture as the operator interface.
- **Architecture / stack:** operator hand pose (XREAL spatial SDK or EMG) → retargeting to hand joints (use the URDF) → LHandProLib streaming commands; arm follows wrist pose through the arm SDK. Log synchronized video + joint data per episode. Stretch goal: replay or a small imitation policy for one sub-step.
- **48-hour plan:**
  - **H0–6:** hand bring-up; confirm command rate over CAN FD; get a tracking stream from the XR or EMG device.
  - **H6–24:** retargeting for thumb-index pinch and power grasp; arm teleoperation with safety limits.
  - **H24–40:** practise one disassembly task on a dummy device; record 20+ episodes.
  - **H40–48:** replay the best episode autonomously; prepare the dataset summary slide.
- **3-minute demo script:** operator with glasses removes a battery from a device live → show the recorded episode replayed by the robot → show the dataset (episodes, duration) and what it would take to automate.
- **Risks and fallbacks:** retargeting 16 active joints is slow to tune → drop to DH116 (6 active). Latency too high → scripted keyframes with operator trigger. Never use real lithium cells that could be punctured — use dummy packs.
- **Judging angles:** innovation (high) · technical depth (teleoperation, retargeting, data pipeline) · impact (circular economy) · Leukerbad (weak — frame as remote repair for places far from service centres).

### Concept 4 — Self-metering efficient actuator for a resource-saving mechanism

- **Problem → value:** Many resource savings are one moving part away: a cover that closes over warm water, a flap that diverts a waste stream, a panel that follows the sun. Build one mechanism with an integrated joint and report the energy it uses versus the energy or water it saves.
- **Hardware:** PJ3 joint module (PJ3-60 at 9.5 N·m or PJ3-75 at 14 N·m rated) or a Leadshine integrated servo with Modbus RTU / CANopen, if available; D-Robotics RDK board as controller; inline power meter; temperature or light sensor; 3D-printed or plywood mechanics.
- **Architecture / stack:** sensor reading → rule or small model decides when to move → CAN FD (PJ3) or Modbus RTU (integrated motor) command from the RDK → log position, temperature-rise port and measured power → dashboard of energy in vs savings out.
- **48-hour plan:**
  - **H0–6:** get the PJ3 protocol document and a working "move to angle" example **from Leadshine staff**. No protocol by H6 → abandon this concept.
  - **H6–24:** build the mechanism; closed-loop moves; power logging.
  - **H24–40:** sensing and decision logic; measure a before / after scenario on a scale model.
  - **H40–48:** dashboard, repeatability runs, pitch.
- **3-minute demo script:** scale model (for example a warm-water basin with an automatic insulating cover) → trigger closes the cover → live graph of heat loss with and without → show actuator energy per cycle next to the saving.
- **Risks and fallbacks:** closed protocol is the main risk → swap in any hobby servo or another vendor's motor and keep the measurement story (Leadshine then drops out of the build). Mechanical build time is easy to underestimate.
- **Judging angles:** innovation (low–moderate) · technical depth (measured energy balance) · impact (quantified saving) · Leukerbad (**strong** — thermal baths and heated pools at 1,400 m lose heat; any measured saving speaks to local operators).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| DH116 + Flexiv Rizon | Force-controlled reach + multi-finger grasp for mixed waste or disassembly | **Medium–high**: custom flange, two SDKs, ROS 2 bridge |
| DH116S + Dobot CR / Nova or ROKAE xMate | Lighter hand on a common cobot for a sorting cell | **Medium**: flange and payload check; cobot SDKs are mature |
| DH116 / DH2116 + XREAL glasses | Hand-tracking teleoperation for disassembly demos | **Medium**: retargeting code is on you |
| DH2116 + OriginFlow EMG capture | Muscle-signal teleoperation and demonstration data | **High**: two young stacks, calibration time |
| Any hand + D-Robotics RDK X5 | Low-power edge inference and hand control without a laptop (SDK lists ARM support) | **Low–medium**: CAN FD / RS485 adapter and driver on ARM |
| Hand on AGIBOT / Galaxea / Galbot mobile manipulator | Mobile litter or sorting robot | **High**: replacing a stock end-effector in 48 hours is unrealistic unless the vendor already supports it ⚠️ unverified |
| PJ3 + coprod modular hardware | Custom mechanism from modular parts | **Unknown**: depends on PJ3 protocol access and coprod interfaces |

## Questions to ask the Leadshine Technology Co., Ltd. engineers on site

1. Which hands are available to teams (DH116, DH116S, DH2116; left / right; with or without tactile sensors), how many, and with which bus (CAN FD, RS485, EtherCAT)?
2. What supply voltage and peak current does the hand need, and do you provide the power supply and a USB-to-CAN FD adapter?
3. Does the Python SDK expose **raw tactile readings and motor current** at a usable rate, and can I set a grasp-force limit per finger?
4. Do you have a mounting adapter for the Flexiv, Dobot or ROKAE flange, or the flange drawing so we can print one?
5. Can you hand over the latest SDK, ROS 2 package and URDF / MJCF on a USB stick (post-2026-02-10 generation), and which ROS 2 distribution is tested?
6. Is there an IP rating or cleaning guidance for the hand — can it touch damp or dirty items?
7. For PJ3 / HJ2: is there a CAN FD protocol document and a minimal example we may use this weekend, and what is the idle and typical power draw?
8. Are any integrated servo motors, low-voltage drives or iW wheel modules on site?

## Decision rule

- **Pick Leadshine Technology Co., Ltd. for T03 if** your idea hinges on grasping or feeling irregular objects (sorting, disassembly, reuse), you have already secured a host arm, and a Leadshine engineer has confirmed hand availability, power, bus adapter and mounting within the first hours.
- **Avoid if** you need a complete robot, outdoor or wet operation, environmental sensing, or a ready autonomy stack — or if a suction cup or two-finger gripper would do the job.

## Sources

Fetched in this pass (2026-11-14):
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html)
- [PJ3 series product page](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html)
- [Leadshine solutions overview](https://www.leadshine.com/solutions.html)
- [Leadshine logistics industry solution page](https://www.leadshine.com/solution/logistics-industry.html)
- [Leadshine integrated motors category page](https://www.leadshine.com/products/integrated-motor.html)

Carried over from the company profile (not re-fetched in this pass):
- [Leadshine company profile (internal)](../Leadshine.md)
- [DH116S series product page](https://en.leadshine.com/robots/dextrous-hands/dh116s-series.html)
- [DH2116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [DH116S LHandPro ROS2 example project description (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [DH116 / DH116P user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf)
- [Store: DH116-R1 dexterous hand (price)](https://store.leadshine.com/products/dh116-r1-dexterous-hand)

Note: track-specific web search was unavailable in this pass (search quota exhausted); concepts are the author's proposals, not Leadshine reference designs.
