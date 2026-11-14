---
type: challenge-playbook
company: "coprod Inc."
slug: coprod
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# coprod Inc. × T02 — Hackathon Playbook

⬆ [coprod Inc. profile](../coprod.md) · [Brief](coprod-T02-1-Brief.md) · [Products and solutions](coprod-T02-2-Products-and-Solutions.md)

**Read first:** coprod is a parts-and-control-bus vendor with **fit 2/5** for this track. Every concept below assumes (a) coprod staff give you the `cosystem` SDK and sit with you for bring-up, and (b) enough kits exist. Confirm both before H0. All coprod hardware is 🧪 pre-order or coming soon; no IP rating, no safety certification.

## Solution approaches

### Concept 1 — Resilience monitor: power and tilt health node (no motion)
- **Problem → value:** Critical equipment (a cable-car drive cabinet, a pump station, a patrol robot) fails silently when power sags or the structure shifts. A node that logs bus health and tilt at 1 kHz and raises an alert gives operators early warning.
- **Hardware:** co:power + co:battery + co:sense on one EtherCAT line; host laptop with real-time Linux. Optional: **D-Robotics RDK** as the dashboard / alert computer.
- **Architecture / stack:** co:sense (quaternion, accel, gyro) and co:power telemetry → `cosystem` Python read loop → simple threshold and spectral anomaly detection (your code) → web dashboard and alert message. Compute on the host PC.
- **48-hour plan:** H0–6 get SDK, read IMU and power data · H6–24 logging, thresholds, dashboard · H24–40 mock-up (IMU on a tilting pole or shaking plate; mains-cut switch-over to battery) · H40–48 rehearse, record backup video.
- **3-minute demo script:** show live traces → pull mains plug, node stays up on battery and flags "on backup" → tilt or hit the pole, alarm fires with time-stamp → show log replay.
- **Risks and fallbacks:** telemetry fields may be limited → fall back to IMU-only alarm. Battery switch-over behaviour unknown → ask first; otherwise demo fault detection only.
- **Judging angles:** low innovation, modest depth; impact story is early warning for rockfall barriers or lift pylons around Leukerbad — but be honest that a wired EtherCAT IMU is a lab stand-in for a field sensor.

### Concept 2 — Fail-safe actuated barrier or valve
- **Problem → value:** During flood, avalanche warning or gas alarm, a road barrier, flood gate or shut-off valve must move reliably even when mains power is gone, and must stop safely if someone is in the way.
- **Hardware:** 1× co:motion + motor and encoder (from coprod's kit or **Leadshine**), co:power, co:battery, co:sense; 3D-printed or plywood barrier mock-up. co:act instead of co:motion + motor if units exist.
- **Architecture / stack:** trigger (button, simulated sensor feed, or camera event from a **D-Robotics RDK**) → state machine on host PC → `cosystem` position / velocity command at 1 kHz → torque monitoring for obstruction detection → controlled stop via co:motion braking; power state from co:power.
- **48-hour plan:** H0–6 spin one axis under SDK control, confirm e-stop behaviour · H6–24 build mechanism, tune gains, obstruction detection from torque · H24–40 outage scenario on battery, dashboard, trigger integration · H40–48 rehearse.
- **3-minute demo script:** alarm triggers → barrier closes → hand blocks it, axis detects contact and yields → mains cut, barrier still operates on battery → e-stop pressed, controlled halt → dashboard shows event log.
- **Risks and fallbacks:** no spare motor or wrong encoder interface → ask coprod for a complete motor + controller set. Torque sensing too noisy → use position-error threshold. Mechanism breaks → keep a bare-shaft demo with a pointer arm.
- **Judging angles:** clear real-world story (road closure on the Leukerbad access road, thermal-water shut-off); technical depth in fail-safe behaviour; innovation moderate. Do not claim certified safety — Safe Torque Off is not yet available.

### Concept 3 — Stabilised inspection head on a quadruped
- **Problem → value:** Inspecting tunnels, bridges or lift stations with a legged robot gives shaky, poorly aimed sensor data. An actively stabilised, steerable head improves scan and image quality and lets an operator look where the robot cannot turn.
- **Hardware:** 2× co:motion axes (pan / tilt) or 2× co:act, co:sense on the head, co:power + co:battery; carrier **Unitree Go2 / B2** or **Genisom AI** quadruped; payload camera or **SKYLANDX MetaCam** (check mass against your motor torque).
- **Architecture / stack:** co:sense orientation → 1 kHz stabilisation loop (your controller via `cosystem`) → co:motion torque / position; carrier robot driven through its own SDK; operator view and pointing commands over Wi-Fi to a small on-board PC running the EtherCAT master. Mapping done by the payload's own software.
- **48-hour plan:** H0–6 two axes moving, IMU read, confirm on-board PC can run the master · H6–24 gimbal mechanics and stabilisation on the bench · H24–40 mount on quadruped, walk test, operator UI · H40–48 inspection run on a mock structure, backup video.
- **3-minute demo script:** side-by-side video, stabilised vs fixed camera, while the dog walks over rough ground → operator points head at a "crack" marker → show resulting scan or image and health telemetry.
- **Risks and fallbacks:** on-board real-time Linux host not available → tether to a laptop on a cart. Payload too heavy → use a light camera. Mounting on the carrier not permitted → hand-carry rig to show stabilisation.
- **Judging angles:** good technical depth (1 kHz stabilisation on a custom bus), solid multi-vendor integration; Leukerbad relevance through tunnel, gallery and cable-car inspection.

### Concept 4 — Force-reflecting teleoperated tool for hazardous areas
- **Problem → value:** After a gas leak, fire or rockfall, someone must turn a valve, flip a breaker or probe debris. A leader-follower joint pair with force feedback lets an operator feel the task from a safe distance.
- **Hardware:** 2–4 backdrivable axes — ideally **co:act** (10 Nm continuous / 25 Nm peak, 16:1), else co:motion with low-ratio motors; co:power, co:battery; follower mounted on a quadruped or wheeled base from another vendor; operator view on **XREAL** glasses (optional).
- **Architecture / stack:** bilateral position-torque coupling between leader and follower joints in one 1 kHz EtherCAT loop (your controller on `cosystem`); camera stream to operator; carrier robot driven separately. All real-time control on one host — leader and follower share a wired bus, so "remote" means cable length unless you add your own network bridge.
- **48-hour plan:** H0–6 two axes, torque mode verified, confirm co:act availability · H6–24 1-DoF bilateral coupling stable, valve-wheel end effector · H24–40 second DoF or mount on carrier, video link · H40–48 task rehearsal and safety limits.
- **3-minute demo script:** operator turns leader knob, follower turns a real valve → valve hits end stop, operator feels it → blocked valve shows torque limit and alert → e-stop halts both sides.
- **Risks and fallbacks:** co:act not available (likely) → 1-DoF demo on co:motion + motor. Unstable coupling → drop to unilateral control with torque shown on screen. Wired-only link weakens the "remote" claim → state it as a prototype of the joint-level technology.
- **Judging angles:** highest innovation and technical depth; aligns with coprod's planned teleop platform (inference); impact for hazardous-area intervention. Highest chance of running out of time.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| coprod + **Unitree** Go2 / B2 (or **Genisom AI** / **Magiclab** quadruped) | Custom actuated payload (gimbal, probe, tool) on a proven carrier | High — mechanical mount, separate power, separate SDKs, host PC for EtherCAT |
| coprod + **SKYLANDX** MetaCam | Stabilised or steerable 3D-scan head | Medium–high — payload mass vs. torque unknown; scanner software stays independent |
| coprod + **D-Robotics** RDK | Camera-based trigger or dashboard next to the control host | Medium — RDK as a separate perception node; whether it can run the EtherCAT master is ⚠️ unverified |
| coprod + **Leadshine** | Motors / joint modules for co:motion to drive | Medium — encoder interface must match (BiSS, SSI, SPI, Hall, incremental); compatibility ⚠️ unverified |
| coprod + **XREAL** | Operator view for teleoperated tool | Medium — video link only; no coprod integration exists |
| coprod + **Flexiv** / **ROKAE** arm | Usually pointless — those arms already provide force control | — |

## Questions to ask the coprod Inc. engineers on site

1. How many co:motion axes, motors, co:sense, co:power and co:battery units can one team get, and are any co:act units here?
2. Can we get the `cosystem` package and examples now? Which OS, kernel and network card does the EtherCAT master need — and can it run on a small on-board computer?
3. Is there a ROS 2 bridge today, or only the Python / C++ API?
4. What are the current, voltage and continuous-power limits of co:motion and co:power, and the battery capacity and voltage?
5. What exactly happens on e-stop and on bus loss — and what can we configure? Does co:power support switch-over from external supply to battery without dropping the bus?
6. Which telemetry fields are readable (bus voltage, current, temperature, fault codes) and at what rate?
7. Is torque control accurate enough for contact detection or bilateral teleoperation without a torque sensor?
8. Any environmental limits (temperature, moisture, vibration) we should respect if we mount it on a walking robot?

## Decision rule

- **Pick coprod Inc. for T02 if** your idea hinges on one or two custom, torque-controlled axes with defined fail-safe behaviour, your team has mechatronics and real-time Linux skills, and a coprod engineer commits to help with bring-up in the first six hours.
- **Avoid if** you need a mobile robot, perception, mapping or autonomy out of the box, outdoor-rated hardware, or cannot get SDK access and a confirmed kit count before starting.

## Sources
- [coprod — official site (home, API sample, system specs)](https://coprod.co/)
- [coprod — products and roadmap](https://coprod.co/products.html)
- [coprod — systems (co:dodo, planned systems)](https://coprod.co/systems.html)
- [coprod Inc. profile (general research, incl. Venture Kick and startup.ch facts)](../coprod.md)
