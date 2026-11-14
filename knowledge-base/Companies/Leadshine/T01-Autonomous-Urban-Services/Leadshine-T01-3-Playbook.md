---
type: challenge-playbook
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Leadshine Technology Co., Ltd. × T01 — Hackathon Playbook

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Brief](Leadshine-T01-1-Brief.md) · [Products and solutions](Leadshine-T01-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- Leadshine is the **end-effector or a sub-mechanism**; the robot, navigation and compute come from another vendor.
- **Hour 0 gate:** confirm with Leadshine staff which hand variant is available (bus type, left / right, tactile or not), its flange, its power supply and the bus adapter. If no hand can be lent, drop Leadshine for this track.
- Keep the hand **indoors** — no IP rating is published.
- Hand API details below (per-finger position / force targets, ROS 2 service node) follow Leadshine's public description; verify against the SDK you are handed.

## Solution approaches

### Concept 1 — Hand-over station for hotel and spa deliveries

- **Problem → value:** delivery robots carry items but cannot load themselves or hand things to guests. A fixed arm with a five-finger hand picks mixed items (towel roll, bottle, key-card sleeve, small parcel) and loads a courier robot or hands them to a person — removing the staff step at a hotel or thermal-bath reception.
- **Hardware:** **DH116** (or DH116S) on a fixed cobot — Dobot CR, ROKAE xMate or Flexiv Rizon. Optional: a Unitree Go2 or other mobile robot with a basket as the courier. One RGB-D camera.
- **Architecture / stack:** camera → object detection + a small table of pre-set grasp types per item class (power grasp, pinch, tripod) → arm motion via the arm vendor's SDK or MoveIt 2 → hand grasp via LHandProLib (Python) or the LHandPro ROS 2 service node. Compute on a laptop; orders entered through a simple web form.
- **48-hour plan:**
  - H0–6: mount hand, power up, jog fingers in the Windows GUI, run the SDK demo from Linux.
  - H6–24: four grasp presets working on four item types; arm pick-and-place to a fixed drop pose.
  - H24–40: order queue, hand-over to a person (release on pull detected through finger current or tactile, if available), courier robot docking position.
  - H40–48: reliability runs, fallback video, pitch.
- **3-minute demo script:** guest orders "towel + water" on a phone → arm picks both with different grasps → loads courier basket → courier leaves → second order is handed directly to a judge.
- **Risks and fallbacks:** flange mismatch (3D-print an adapter plate in H0–6) · release-on-pull unreliable (fall back to a timed release or a button) · no courier robot (hand-over to a person only).
- **Judging angles:** modest innovation; solid technical depth if grasp selection is perception-driven; clear real-world impact for hotels and clinics short of staff; Leukerbad relevance through the spa / hotel setting.

### Concept 2 — The last 10 metres: lifts, doors and room hand-over

- **Problem → value:** indoor delivery robots normally need lift and door retrofits (network modules, automatic openers). A mobile manipulator with a human-like hand uses the building as it is: presses the lift button, pushes down a lever handle, knocks, hands over the parcel. Value: delivery in old alpine hotels and clinics **without building retrofits**.
- **Hardware:** **DH116** on a wheeled dual-arm robot (Galaxea R1 family, AGIBOT G1 / G2 or Galbot G1) or on a Unitree G1 humanoid arm. Host robot's cameras and navigation.
- **Architecture / stack:** host navigation to pre-mapped waypoints → camera detects button panel / handle (fiducial marker as a safe fallback) → arm approach via host SDK → hand: index-finger extension pose for buttons, hook grasp for lever handles, power grasp for the parcel, all via LHandProLib / ROS 2 → simple state machine (py_trees or SMACH) on the host computer or a laptop.
- **48-hour plan:**
  - H0–6: hardware gate, hand mounted and commanded from the host's computer; pick the exact door and lift panel (or build a mock panel).
  - H6–24: button press and lever-handle skills as stand-alone routines with marker-based alignment.
  - H24–40: chain navigate → press → wait → enter → door → hand-over; replace markers with learned detection only if time allows.
  - H40–48: 10 consecutive runs, record backup video, pitch.
- **3-minute demo script:** robot receives "room 12" → drives to the mock lift panel, presses the call button → drives to a door, opens it by the handle → offers the parcel; judge takes it and the hand releases.
- **Risks and fallbacks:** door too heavy for the host arm (use a light mock door) · finger alignment on small buttons (use a larger mock panel; compliance from force-position control helps) · no access to the host robot's arm API (fall back to Concept 1).
- **Judging angles:** strong real-world story (retrofit-free delivery), good technical depth (navigation + manipulation chain), high Leukerbad relevance (older buildings, clinics, many elderly guests who cannot come down to reception).

### Concept 3 — Public-space upkeep with human tools

- **Problem → value:** maintenance robots are usually single-purpose machines. A hand that uses **human tools** — spray bottle, cloth, litter of any shape, dispenser refills — lets one robot disinfect handrails, wipe tables and pick up litter in a spa lobby or station hall.
- **Hardware:** **DH2116** (16 active DoF, for trigger pulling) or **DH116-M** with tactile sensors, on a mobile manipulator or a cobot on a cart. RGB-D camera. Optional XREAL glasses for a teleoperated first pass and operator view.
- **Architecture / stack:** camera → surface / litter detection → task planner picks tool and grasp → arm wiping trajectory (force-controlled arm such as Flexiv Rizon or ROKAE xMate makes wiping easy) → hand: hold bottle with three fingers, pull trigger with index finger; pinch or power grasp for litter. Optional: a hosted vision-language model to choose the grasp type from an image. Compute on a laptop.
- **48-hour plan:**
  - H0–6: hardware gate; test whether the hand can actually pull the spray trigger — decide DH2116 vs DH116 immediately.
  - H6–24: three skills in isolation: spray, wipe, pick litter.
  - H24–40: detection-driven sequencing; tactile or current feedback to confirm a grasp.
  - H40–48: timed runs, video, pitch.
- **3-minute demo script:** robot approaches a handrail section → sprays → swaps to cloth and wipes → spots a cup and a crumpled bag on the floor → picks both with different grasps → drops them in a bin.
- **Risks and fallbacks:** trigger force or geometry beyond the hand (use a pump-top bottle pressed with the palm) · liquid near an unsealed hand (use water, spray away from the hand, cover with a glove only if Leadshine agrees) · DH2116 bring-up takes too long (DH116 with litter picking and wiping only).
- **Judging angles:** highest innovation of the hand concepts (tool use), strong technical depth, hygiene relevance for thermal baths and rehabilitation clinics.

### Concept 4 — PJ3-powered self-unloading cargo module

- **Problem → value:** a quadruped or wheeled base can reach a doorstep over steps and slopes but cannot drop its load without a person. A tilting cargo bed or lidded parcel box driven by one or two **PJ3** joint actuators makes any mobile base a self-unloading courier for steep village streets.
- **Hardware:** **PJ3-60 or PJ3-75** (9.5 / 14 N·m rated) + printed or laser-cut tray, on a Unitree Go2 / B2 or another vendor's base. Battery or host power rail, CAN FD adapter.
- **Architecture / stack:** host navigation to drop point → trigger over ROS 2 topic → small node sends position / velocity commands to the PJ3 over CAN FD → tilt, confirm unload (current or a simple switch), return. Compute on the host or a D-Robotics RDK board.
- **48-hour plan:**
  - H0–6: **hard gate — obtain the PJ3 CAN FD protocol or a library from Leadshine staff and spin one actuator.** No protocol by H6 means abandon this concept.
  - H6–24: build the tray mechanism, closed-loop tilt with soft limits.
  - H24–40: mount on the base, integrate with navigation, tune for payload.
  - H40–48: outdoor-style ramp test, video, pitch.
- **3-minute demo script:** parcel loaded → robot walks a ramp or steps to a marked doorstep → bed tilts and parcel slides into a drop box → robot reports delivery and returns.
- **Risks and fallbacks:** no public SDK (highest risk) · supply voltage mismatch with the host rail (ask before designing) · mechanical build eats the schedule (fallback: a hobby servo for the lid and keep PJ3 as a stated upgrade path — which weakens the Leadshine story).
- **Judging angles:** hardware creativity and alpine relevance are high; software depth is lower; risk is the highest of the four.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| DH116 + Galaxea R1 / AGIBOT G1-G2 / Galbot G1 | Mobile manipulation for lifts, doors, hand-over (Concept 2). Leadshine reports AGIBOT as a customer, so ask whether a mounted example exists. | High — flange, power, bus, host arm API |
| DH116 or DH116S + Dobot CR / ROKAE xMate / Flexiv Rizon | Fixed hand-over or tool-use station (Concepts 1, 3); force-controlled arms simplify wiping and button pressing | Medium — adapter plate + separate hand bus to a laptop |
| DH116S + Unitree G1 humanoid | Lighter hand on a humanoid arm for concierge-style demos | High — payload and wrist interface must be checked first |
| Hand + D-Robotics RDK board | SDK supports ARM, so the hand node can run on the robot instead of a tethered laptop | Low to medium — ⚠️ unverified on that specific board |
| Hand + XREAL glasses | Operator view / teleoperated fallback when autonomy fails in the demo | Medium — you write the mapping |
| Hand vs WUJI Hand (20 DoF) | Alternative on site: more dexterity, different stack. Choose Leadshine for load capacity and price, WUJI for fine manipulation | n/a — pick one |
| PJ3 + Unitree Go2 / B2 | Self-unloading cargo module (Concept 4) | High — depends on protocol access |
| Hand-equipped robot + SKYLANDX scan | Fast 3D map of the venue for navigation to doors and lifts | Low for the map, host-dependent for use |

## Questions to ask the Leadshine Technology Co., Ltd. engineers on site

1. Which hands can teams borrow — DH116, DH116S or DH2116; CAN FD, RS485 or EtherCAT; left or right; with tactile sensors?
2. What supply voltage and peak current does the hand need, and do you provide the power supply and the USB-to-CAN FD adapter?
3. What is the mounting flange pattern, and do you have adapter plates for any arm or humanoid at this event?
4. Which ROS 2 distribution is the LHandPro package built for, and does it cover DH116 and DH2116 or only DH116S?
5. Can the SDK command fingertip force directly, and what is the control and feedback rate over CAN FD?
6. Is there a splash or dust rating, and what is the minimum operating temperature? Can the hand wear a glove?
7. For PJ3 / iW: can you share the CAN FD protocol or a Python library today, and what voltage do they run on?
8. Is any robot at this event already fitted with Leadshine hands or joint modules?

## Decision rule

- **Pick Leadshine Technology Co., Ltd. for T01 if** you already have access to an arm or mobile manipulator from another vendor, your idea hinges on a contact task (button, handle, hand-over, tool use), and a hand plus adapter is confirmed available in the first hour.
- **Avoid if** you need mobility or autonomy out of the box, your task is outdoors in snow or wet, or you have nobody on the team comfortable with mechanical mounting and CAN bus bring-up.

## Sources

- [Leadshine company profile (this vault) — specs, prices and developer-stack summary](../Leadshine.md)
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html)
- [DH116S series product page](https://www.leadshine.com/robots/dextrous-hands/dh116s-series.html)
- [DH2116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [PJ3 series product page](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html)
- [ELD3 series product page](https://www.leadshine.com/products/servo/servo-drive/eld3-series.html)
- [Logistics industry solution page](https://www.leadshine.com/solution/logistics-industry.html)
- [Automate 2026 recap (Leadshine news)](https://www.leadshine.com/newsEvent/details/automate-2026-concludes-successfully-%7C-leadshine-drives-global-industrial-automation-and-humanoid-robotics-innovation-with-core-motion-control-technologies.html)
- [WAIC 2026 recap (Leadshine news)](https://en.leadshine.com/newsEvent/details/leadshine-successfully-concludes-waic-2026,-showcasing-next-generation-robotics-solutions.html)
