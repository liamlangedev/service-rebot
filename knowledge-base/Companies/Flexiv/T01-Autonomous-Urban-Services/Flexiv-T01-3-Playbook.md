---
type: challenge-playbook
company: "Flexiv Robotics"
slug: Flexiv
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Flexiv Robotics × T01 — Hackathon Playbook

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Brief](Flexiv-T01-1-Brief.md) · [Products and solutions](Flexiv-T01-2-Products-and-Solutions.md)

> **Framing:** a Flexiv arm does not move through the city. Every concept below treats it as a **service station** that makes mobile robots (or people) more useful through reliable physical contact. Assumed on-site kit: **Rizon 4 or 4s + Grav gripper**, controlled from a laptop over wired LAN (best guess — confirm at the booth). Primitive names come from the official list; their exact behaviour and parameters must be checked in the docs on site.

## Solution approaches

### Concept 1 — Touch-to-dock parcel hub (safest)
- **Problem → value:** delivery robots park a few centimetres off every time, so loading and unloading them usually needs a human. A force-guided arm that finds the cargo box by touch makes hand-offs fully unattended — hotel-to-clinic pharmacy runs, towel and linen shuttles, guest parcels.
- **Hardware:** Rizon 4 / 4s + Grav on a table. Carrier: any mobile robot with a tray or box (Unitree Go2 / B2 with a basket, or a hand-pushed trolley as stand-in). Optional: one RGB-D camera + D-Robotics RDK X5 for coarse localisation.
- **Architecture / stack:** coarse pose from an AprilTag on the carrier (camera → laptop) → MoveL to a pre-contact pose → **Contact** primitive to touch the box rim on two faces and compute the true offset → GraspComp + MoveL to place the parcel → release. Python RDK, non-real-time mode; small state machine; compute on a laptop. Carrier receives "loaded" over a simple HTTP / ROS 2 message.
- **48-hour plan:**
  - H0–6: confirm RDK license and version, run `basics1_display_robot_states.py`, execute MoveL / Contact from Python, define the safe workspace.
  - H6–24: touch-based box localisation; pick and place of 3 parcel types; tag detection.
  - H24–40: integrate the carrier's arrive / leave signal; 20 consecutive cycles with random parking offsets; error recovery (missed grasp, no contact).
  - H40–48: polish, short dashboard (cycle count, offset corrected), backup video.
- **3-minute demo script:** (0:00) carrier arrives deliberately crooked. (0:30) arm taps the box twice, screen shows measured offset. (1:00) parcel placed, carrier leaves. (1:45) repeat with a judge moving the carrier by hand. (2:30) slide: one hub serves any vendor's robot; Leukerbad clinic-to-hotel use case.
- **Risks and fallbacks:** carrier integration slips → use a trolley pushed by a teammate; tag detection flaky → rely on touch only with a wider search; gripper cannot hold a parcel type → standardise on one tote.
- **Judging angles:** *Innovation* — touch instead of precise vision. *Technical depth* — force-based localisation, repeatability numbers. *Impact* — removes the human from the hand-off. *Leukerbad* — rehab clinics, hotels and baths within a few hundred metres of each other.

### Concept 2 — Constant-force hygiene station for shared surfaces
- **Problem → value:** thermal baths, clinics and lifts have high-touch surfaces (handrails, loungers, ticket screens, walker and wheelchair handles) cleaned by hand many times a day. A robot that wipes with a controlled, logged force gives consistent, auditable cleaning and frees staff.
- **Hardware:** Rizon 4 (IP65) + Grav (IP67) holding a wipe tool or sponge pad; mock-up handrail / lounger section / rollator. Optional: SKYLANDX MetaCam scan of the object for path generation; XREAL glasses to show coverage to an operator.
- **Architecture / stack:** teach the path by hand-guiding (FloatingCartesian) or generate it from a scan → execute with **ForceHybrid / ForceComp** (or Polish) holding roughly 5–15 N normal force → log wrench and pose → coverage map on a laptop. Python RDK non-real-time; optionally ROS 2 `tcp_wrench` topics for logging.
- **48-hour plan:**
  - H0–6: RDK bring-up, tool mount, ZeroFTSensor + Contact on a flat board.
  - H6–24: constant-force wipe on flat, then curved handrail; hand-guided teaching workflow.
  - H24–40: coverage visualisation; UV-marker "before / after" test; second object (rollator handle); person-nearby pause behaviour.
  - H40–48: cleaning report export, demo rehearsal, video.
- **3-minute demo script:** (0:00) UV lamp shows a marked, "dirty" rail. (0:20) staff member teaches a new path by guiding the arm for 15 s. (0:50) robot wipes; live force plot stays flat over the curve. (2:00) UV lamp shows the result; coverage report appears. (2:30) scaling story: same skill on a mobile base for overnight rounds.
- **Risks and fallbacks:** curved-surface tracking unstable → slow down, reduce to flat + gently curved; wet tools near electronics → dry microfibre and UV marker only; "it is stationary" criticism → show the object arriving (rollator returned to a cleaning bay) rather than the robot travelling.
- **Judging angles:** *Innovation* — auditable force-logged cleaning. *Technical depth* — hybrid force / position control on unknown curvature. *Impact* — hygiene labour in care and spa facilities. *Leukerbad* — public thermal baths and rehabilitation clinics.

### Concept 3 — Autonomous plug-in charging point for service fleets
- **Problem → value:** e-bikes, mobility scooters and service robots only become autonomous if recharging needs no human. An arm that finds the socket by feel and plugs in removes the last manual step.
- **Hardware:** Rizon 4s + Grav; a mock charging inlet on a mobile robot or e-bike / scooter mock-up; one camera for coarse inlet detection (D-Robotics RDK X5 or laptop). Carrier from Unitree or another on-site vendor (optional).
- **Architecture / stack:** coarse inlet pose from a fiducial or small detector → approach → **SearchHole → CheckPiH → InsertComp / Mate** → verify by force signature and a charge-contact signal → unplug on request. Python RDK; simulate first in Isaac Sim using the Rizon 4 + Grav cable-insertion reference workflow as a template; RL policy only as a stretch goal.
- **48-hour plan:**
  - H0–6: bring-up; 3D-print or source plug holder and inlet; rigid fixture test of InsertComp.
  - H6–24: insertion with ±10 mm / ±5° offsets; unplug; cable management.
  - H24–40: coarse vision; integrate a parked vehicle or robot; 30-trial success-rate table.
  - H40–48: failure handling (abort on force limit), demo script, video.
- **3-minute demo script:** (0:00) scooter / robot parks roughly. (0:30) camera gives a rough target, arm spirals and finds the socket — force plot on screen. (1:15) plug seats, LED turns on. (1:45) judge shifts the vehicle, repeat. (2:30) numbers: success rate, tolerated offset, cycle time.
- **Risks and fallbacks:** connector jams → chamfered custom plug, lower insertion force; cable drags the arm off path → short, supported cable; vision fails → fixed parking guide plus wider search pattern. Use low-voltage (USB / 12 V) only — no mains connectors.
- **Judging angles:** *Innovation* — tactile plug-in without precise docking. *Technical depth* — measured tolerance envelope, sim-to-real path. *Impact* — unattended fleet charging. *Leukerbad* — e-bike tourism and mobility scooters for elderly guests on steep streets. (Flexiv's own EV-charging work is ⚠️ unverified — do not cite it as a reference.)

### Concept 4 — Roaming service manipulator with a learned skill (most ambitious)
- **Problem → value:** an indoor robot that travels between service points and does one contact task at each (restock a shelf, collect used towels, press a lift button) — the full "move + maintain" loop.
- **Hardware:** only credible if a Flexiv mobile platform (Mobile Manipulator, AICO or FMR 300) is on site **and** its base can be commanded. Otherwise split the roles: roaming done by Galaxea R1 / Galbot G1 / Unitree, contact task done by a fixed Rizon station.
- **Architecture / stack:** laser-SLAM navigation on the base (vendor API) → dock at station → arm cancels docking error by touch (Contact) → task skill, either primitives or a policy trained with **Flexiv Trainer** (teleop demos via flexiv_tdk → LeRobot-format episodes → policy) → task planner (LLM / VLM on a laptop GPU) picks the next station.
- **48-hour plan:**
  - H0–6: verify base API, map the demo area, confirm teleop hardware for data collection.
  - H6–24: navigation between 2–3 stations; scripted contact skill at one station; start collecting 50+ demos for one learned skill.
  - H24–40: train and evaluate the policy; keep the scripted version as default; add the planner.
  - H40–48: end-to-end runs, freeze, video.
- **3-minute demo script:** (0:00) spoken or typed request "restock towels at station B". (0:20) base navigates. (1:00) arm touches off, performs the task. (2:00) second station with the learned skill, or scripted fallback. (2:40) recap of the architecture.
- **Risks and fallbacks:** base not available or not controllable (public AMR SDK covers SEER AMRs only) → drop to Concept 1 or 3; policy does not converge → scripted primitives; two-vendor integration → agree on a one-message interface (arrived / done) on day 1.
- **Judging angles:** *Innovation* — touch-calibrated mobile manipulation plus a learned skill. *Technical depth* — highest, also highest risk. *Impact* — closest to a real urban-service robot. *Leukerbad* — hotel and clinic back-of-house logistics.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Flexiv Rizon + Unitree Go2 / B2 | Quadruped carries goods over steep or snowy streets; arm loads / unloads / plugs it in at each end | Low–medium (one "arrived / done" message; carrier needs a box) |
| Flexiv Rizon + D-Robotics RDK X5 | Edge vision for coarse target pose, arm refines by touch | Low |
| Flexiv Rizon + SKYLANDX MetaCam | 3D scan of object or room → wipe paths, digital twin for the pitch | Medium (scan-to-robot-frame registration) |
| Flexiv Rizon + Galaxea R1 / Galbot G1 | Roaming manipulator hands items to a precise fixed station | Medium–high (two stacks) |
| Flexiv Rizon + XREAL glasses | Operator sees force, coverage or task status in AR; remote supervision story | Medium |
| Flexiv Rizon + WUJI Hand | Dexterous end-effector for buttons, handles, bags | High (mechanical flange, power, separate control loop) ⚠️ unverified compatibility |
| Flexiv Rizon + Binabik AI / coprod stack | Agent layer or common middleware over several robots | Unknown — ask both teams |

## Questions to ask the Flexiv Robotics engineers on site

1. Which exact robots and end-effectors are here, and is any **mobile base** (FMR 300, AICO, Mobile Manipulator) available to teams?
2. Is the **RDK license** active on each robot, which robot software / RDK version is installed (v1.x or v2.x), and which primitives are licensed — including the vision-guidance ones?
3. Do you provide a laptop with a real-time kernel, or should we stay in non-real-time mode? What update rate is safe from Python?
4. What are the recommended parameters and force limits for Contact, SearchHole / InsertComp and ForceHybrid for a plug-in or wipe task, and what are the safety limits when people stand nearby?
5. How is an FMR 300 or AICO base commanded today, given the public AMR SDK lists SEER AMR integration only?
6. What leader device does flexiv_tdk teleoperation need, and is one here for collecting Flexiv Trainer demos?
7. Can the arm be mounted on a table or cart we supply, and what are the power requirements for the controller?
8. Are there existing customer references in commercial or public services we may cite in our pitch?

## Decision rule

- **Pick Flexiv Robotics for T01 if** your idea's hard part is physical contact at a service point (loading, plugging, wiping, handing over) and you can pair it with another vendor's mobile robot or present it as fixed infrastructure.
- **Avoid if** your idea is mainly about navigating streets or buildings, needs outdoor or legged mobility, or must be a single self-contained robot from one vendor.

## Sources
- [Flexiv — Primitives list](https://www.flexiv.com/software/primitives)
- [Flexiv — Robot System page (Mico, AICO, Mello, Mobile Manipulator)](https://www.flexiv.com/product/robot-system)
- [Flexiv RDK manual v2.x](https://www.flexiv.com/software/rdk/manual/v2.x/index.html)
- [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk)
- [GitHub — flexiv_ros2](https://github.com/flexivrobotics/flexiv_ros2)
- [GitHub — flexiv_amr_sdk](https://github.com/flexivrobotics/flexiv_amr_sdk)
- [GitHub — flexiv_trainer](https://github.com/flexivrobotics/flexiv_trainer)
- [Automated Warehouse — Flexiv launches its first self-developed AMR (2025-12-04)](https://www.automatedwarehouseonline.com/flexiv-launches-its-first-self-developed-amr/)
- [Robotics 24/7 — Hannover Messe 2026: Flexiv showcases the future of adaptive robotics](https://www.robotics247.com/article/hannover-messe-2026-flexiv-showcases-the-future-of-adaptive-robotics)
- [Flexiv Robotics company profile (arm / gripper specs, NVIDIA Isaac workflow, teleop and Trainer details)](../Flexiv.md)
