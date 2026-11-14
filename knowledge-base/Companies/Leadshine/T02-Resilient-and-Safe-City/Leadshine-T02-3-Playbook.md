---
type: challenge-playbook
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Leadshine Technology Co., Ltd. × T02 — Hackathon Playbook

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Brief](Leadshine-T02-1-Brief.md) · [Products and solutions](Leadshine-T02-2-Products-and-Solutions.md)

**Read this first:** Leadshine is an **add-on** for T02 (fit 2/5). Every concept below needs a host robot or arm from another vendor. Secure that host **before** committing. What Leadshine brings on site is not confirmed — check the table for hand variant (CAN FD or EtherCAT, left or right, tactile or not), flange and power supply.

## Solution approaches

### Concept 1 — Remote hands for the hazard zone (fixed station)
- **Problem → value:** after a gas alarm, flood or fire in a technical room (pump room of a thermal bath, cable-car machine room, tunnel service niche) someone must close a valve or trip a breaker. A teleoperated hand does it; the responder stays outside.
- **Hardware:** Leadshine **DH116** (EtherCAT or CAN FD; tactile -M if available) on a cobot arm from Flexiv, ROKAE or Dobot; webcam or depth camera at the scene; laptop. Mock "infrastructure panel": ball valve, rocker breaker, lever, door handle.
- **Architecture / stack:**
  - Perception: scene camera stream to operator; optional hand `/joint_states` twin in RViz2.
  - Planning: operator-in-the-loop. Arm moved by gamepad or pre-taught waypoints (host arm's SDK); hand driven by **grasp presets** (hook, power, lateral pinch) first, then continuous control from webcam hand tracking mapped to the six active joints.
  - Control: `lhandpro_service` (ROS 2 Humble, Ubuntu 22.04) or LHandProLib Python directly. Tactile / current values shown as a contact bar on the operator UI.
  - Compute: one laptop; operator UI on a second machine over Wi-Fi to show real separation.
- **48-hour plan:**
  - H0–6: get SDK archive from Leadshine staff; jog the hand in the Windows GUI; run `sequence_demo_py`; mount on arm (flange adapter).
  - H6–24: grasp presets as ROS 2 services; arm waypoints for each panel element; first full valve turn by teleop.
  - H24–40: operator UI (video + contact bar + preset buttons); hand-tracking input; link-loss behaviour (hand holds grip — self-locking — arm stops).
  - H40–48: rehearse, time the run, record a backup video.
- **3-minute demo script:** 0:00 alarm scenario on screen → 0:30 operator at a separate desk approaches panel → 1:00 closes valve (quarter turn) → 1:40 flips breaker → 2:10 pulls lever / opens door handle, contact bar visible → 2:40 unplug network: hand keeps grip, system reports safe state.
- **Risks and fallbacks:** flange or bus adapter missing → clamp the hand on a fixed stand and bring the panel to it. Hand tracking jittery → stay on preset buttons. Wrist torque of the arm too low for the valve → use a lever-handle valve.
- **Judging angles:** impact (keeps people out of danger), Leukerbad relevance (spa and cable-car technical rooms, road closures delaying specialists), technical depth modest, innovation modest.

### Concept 2 — Rehearse-then-execute with a hand digital twin
- **Problem → value:** in an incident you get one attempt. The operator first rehearses the manipulation in simulation on a twin of the panel, then the validated sequence is replayed on the real hand with contact checks.
- **Hardware:** as Concept 1. Optional: **SKYLANDX** scan of the room for the twin backdrop; **XREAL** glasses as the operator display.
- **Architecture / stack:**
  - Perception: fiducial markers on the panel for pose; tactile / proximity (-M) for contact confirmation.
  - Planning: Leadshine **MJCF** hand model in MuJoCo plus simple panel geometry; operator records a grasp sequence in sim; sequence exported as joint targets.
  - Control: replay through `lhandpro_service`; abort if expected contact does not appear or current exceeds a threshold.
  - Compute: laptop (sim + ROS 2).
- **48-hour plan:**
  - H0–6: hardware bring-up as Concept 1; load MJCF in MuJoCo and confirm joint order matches the real hand.
  - H6–24: sim panel, recording tool, sim-to-real replay for one element.
  - H24–40: contact-check logic, marker-based pose correction, second and third element.
  - H40–48: polish split-screen (sim left, real right), backup video.
- **3-minute demo script:** 0:00 scenario → 0:30 rehearse valve closing in sim → 1:15 "execute" — real hand repeats it, twin mirrors live → 2:00 deliberately shift the panel: contact check fails, system aborts and re-plans → 2:40 summary.
- **Risks and fallbacks:** MJCF and firmware generation mismatch (use resources dated ≥ 2026-02-10) → fall back to RViz2 twin with URDF and recorded real sequences. Sim contact unrealistic → use sim for kinematic rehearsal only.
- **Judging angles:** innovation and technical depth higher (digital twin, verified execution); impact credible for infrastructure operators.

### Concept 3 — Mobile first responder that can use its hand
- **Problem → value:** a robot enters the building, maps it, finds the shut-off and operates it — "see and act" instead of inspection only.
- **Hardware:** DH116 or lighter **DH116S** on a mobile manipulator or humanoid from another vendor (Galaxea, Galbot, AGIBOT, Unitree, Spirit AI, UniX AI — whichever allows an end-effector swap); SKYLANDX MetaCam for the 3D map; D-Robotics board if on-board compute for the hand is needed.
- **Architecture / stack:**
  - Perception: host robot's cameras; object detector for valve / breaker; 3D scan for situational awareness.
  - Planning: host robot's navigation and arm stack; the hand is one extra ROS 2 node called at the end of the approach.
  - Control: `lhandpro_service` on the host computer or a companion board; power from the robot's rail (hand accepts 12–48 V, 2.5 A).
- **48-hour plan:**
  - H0–6: confirm with **both** vendors that the wrist flange, power and data connection are feasible. If not confirmed by H6, drop to Concept 1.
  - H6–24: mount, power, hand node running on the robot; teleoperated drive-and-grasp.
  - H24–40: detection-triggered grasp presets; map overlay; one full mission.
  - H40–48: reliability runs, backup video.
- **3-minute demo script:** 0:00 map of the "building" → 0:30 robot drives to the panel → 1:20 hand closes the valve → 2:10 robot carries a 5 kg bag out using hook grip → 2:40 map with marked actions.
- **Risks and fallbacks:** mechanical / electrical integration with an unfamiliar host is the main risk; humanoid arms may lack wrist torque. Fallback: mobile base carries a fixed mini-station from Concept 1.
- **Judging angles:** strongest real-world story and multi-vendor integration; Leukerbad relevance (first look after avalanche or rockfall cuts access). Leadshine's part is small — be clear about who contributed what.

### Concept 4 — Custom PJ3-driven rescue mechanism (only with Leadshine staff support)
- **Problem → value:** a purpose-built actuator unit — for example a pan-tilt sensor mast or a door / hatch opener — where a standard robot is overkill.
- **Hardware:** PJ3-60 / 75 / 97 joint modules (9.5 / 14 / 44 N·m rated), 3D-printed or aluminium brackets, CAN FD adapter, D-Robotics board; possibly coprod modular hardware.
- **Architecture / stack:** sensor (camera or thermal, own supply) → simple tracking logic → position / torque commands over CAN FD. **Protocol is not public** — everything depends on Leadshine handing over documentation or sample code.
- **48-hour plan:** H0–6 obtain protocol and spin one module, or stop. H6–24 mechanics. H24–40 closed-loop behaviour. H40–48 demo hardening.
- **3-minute demo script:** mechanism tracks a simulated hazard (heat source or moving person), then performs one forceful action (opens a weighted hatch).
- **Risks and fallbacks:** no protocol by H6 → abandon. Missing specs (voltage, speed, IP) → ask before designing.
- **Judging angles:** technical depth; weakest storytelling unless tied to a concrete Leukerbad hazard.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| DH116 + Flexiv Rizon / ROKAE xMate arm | Force-sensitive arm + strong hand for valves and levers (Concepts 1–2) | **Medium** — flange adapter, separate hand control node |
| DH116 + Dobot cobot | Same, simpler arm | **Medium** |
| DH116 / DH116S + wheeled dual-arm robot (Galaxea, Galbot, AGIBOT G1, UniX AI) | Mobile "see and act" responder (Concept 3) | **High** — wrist swap, power, both vendors must agree |
| Hand + XREAL glasses | Operator sees video and hand twin hands-free | **Low–medium** — display only is easy; hand-tracking input is more work |
| Hand + OriginFlow EMG | Operator's muscle signals drive grasp presets | **Medium–high** — depends on OriginFlow's output API (not verified) |
| Hand + SKYLANDX MetaCam | 3D scan of the incident room as twin backdrop | **Low** — offline scan, no real-time coupling needed |
| Hand or PJ3 + D-Robotics RDK board | On-robot compute for the hand node | **Medium** — confirm LHandProLib ARM build and bus adapter |

## Questions to ask the Leadshine Technology Co., Ltd. engineers on site
1. Which hands are available to loan — DH116, DH116S, DH2116; CAN FD or EtherCAT; left or right; tactile (-M) or not — and how many?
2. Can we get the **current SDK, ROS 2 workspace, URDF / MJCF and protocol sheets on a USB stick** now (matching the firmware of the loan units)?
3. What flange / mounting pattern does the hand have, and do you have adapter plates for Flexiv, ROKAE, Dobot, Unitree or AGIBOT wrists?
4. For CAN FD units: which USB-CAN FD adapter does the SDK support on Linux? For EtherCAT units: any NIC restrictions?
5. Which feedback can we read per finger and at what rate — position, current, force, tactile, proximity? Can we set a grip-force or current limit?
6. What happens on communication loss or power loss — does the hand hold position (self-locking), and how do we release it safely?
7. Is there an existing teleoperation or hand-retargeting demo (glove, camera) we can reuse?
8. For PJ3 / HJ2: is there a protocol document, sample code or ROS 2 driver, and what are supply voltage, peak torque and IP rating?

## Decision rule
- **Pick Leadshine Technology Co., Ltd. for T02 if** you already have a host arm or mobile manipulator secured and your concept's key moment is a robot operating human-made controls (valve, breaker, handle) by remote control or after an autonomous approach — indoors.
- **Avoid if** you need a self-contained platform for patrol, mapping, search or outdoor hazard monitoring, cannot spare half a day for mounting and bus bring-up, or would depend on the joint modules without confirmed protocol support.

## Sources
- [Leadshine company profile (internal, general research)](../Leadshine.md)
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html)
- [DH116 / DH116P user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf)
- [DH116S LHandPro ROS2 example project description (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [DH2116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [PJ3 series product page](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html)
- [FAIR plus 2026 recap (Leadshine store blog)](https://store.leadshine.com/blogs/news/leadshine-dexterous-hands-and-joint-modules-shine-at-the-shenzhen-fair-plus-2026)
- [WAIC 2026 recap (Leadshine news)](https://en.leadshine.com/newsEvent/details/leadshine-successfully-concludes-waic-2026,-showcasing-next-generation-robotics-solutions.html)
