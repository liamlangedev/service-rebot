---
type: challenge-playbook
company: "Flexiv Robotics"
slug: Flexiv
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Flexiv Robotics × T02 — Hackathon Playbook

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Brief](Flexiv-T02-1-Brief.md) · [Products and solutions](Flexiv-T02-2-Products-and-Solutions.md)

**Fit 2/5.** Flexiv is the *intervention* half of a T02 system: once something has found the problem, a force-controlled arm can act on it. All concepts below assume a bench-mounted **Rizon 4 / 4s + Grav** indoors and a mock-up panel you build yourself (valve, lever, breaker, connector, bolts). Hardware on site is unconfirmed — check before committing.

**Leukerbad framing that works for every concept (scenario, not a claim about real installations):** the access road is closed by avalanche risk, the technician is stuck in the valley, and a pump room / thermal-water plant room / cable-car machine room needs a valve closed or a breaker reset *now*.

## Solution approaches

### Concept 1 — Touch-test inspector (safest)
- **Problem → value:** Loose bolts, seized valves and slack fittings are invisible to cameras. A force-controlled arm can *feel* them: push, wiggle, turn slightly, and compare the force signature with a healthy baseline → early-warning maintenance for critical equipment.
- **Hardware:** Rizon 4s (or 4) + Grav; mock panel with 4–6 test points, some deliberately faulty. Optional: D-Robotics RDK X5 + camera for locating test points; SKYLANDX MetaCam scan as a 3D backdrop for the report.
- **Architecture / stack:** test-point poses (taught by free-drive or fiducial markers) → Python RDK, `NRT_PRIMITIVE_EXECUTION` for approach and contact, `NRT_CARTESIAN_MOTION_FORCE` for a small controlled push / twist → log external wrench and displacement → stiffness / breakaway-torque features → threshold or simple anomaly score → web dashboard (green / amber / red per asset). All compute on one laptop.
- **48-hour plan:**
  - **H0–6:** licence + Remote mode check, run `basics1`/`basics3` examples, zero the F/T sensor, build the mock panel.
  - **H6–24:** scripted probe routine for one test point; record healthy vs faulty signatures; pick 2–3 robust features.
  - **H24–40:** all test points, dashboard, baseline-vs-today comparison, repeatability runs.
  - **H40–48:** rehearse, record backup video, freeze code.
- **3-minute demo script:** (0:00) the scenario and why cameras miss it → (0:30) robot probes three points, live force plot on screen → (1:30) a judge loosens one bolt → (2:00) robot re-inspects, dashboard flips to red with the measured stiffness drop → (2:40) how it would ride a mobile base on a rota.
- **Risks and fallbacks:** signatures too noisy → use bigger, clearer faults (spring-loaded vs rigid) and average repeated probes. No camera time → fixed taught poses.
- **Judging angles:** *innovation* — tactile inspection is rare at hackathons; *technical depth* — real force data and statistics; *impact* — predictive maintenance of valves and fittings; *Leukerbad* — thermal-water pipework and lift machinery are maintenance-critical.

### Concept 2 — Remote hands for a cut-off plant room
- **Problem → value:** When people cannot or should not enter (gas, flooding, blocked road), a remote operator still needs to turn a valve, flip a breaker or plug in a generator lead. Force feedback and compliance make remote contact safe; fail-safe stop makes it trustworthy.
- **Hardware:** follower Rizon 4 / 4s + Grav at the "plant room" table. Leader: a second Flexiv arm via TDK (if available) **or** fallback input (SpaceMouse / gamepad / phone IMU). Operator view: 2 webcams, optionally XREAL glasses as a head-up display.
- **Architecture / stack:** operator station in another room → network (venue LAN, optionally via a phone hotspot to show WAN) → **with two arms:** `flexiv_tdk` `transparent_cartesian_teleop_lan.py` / `_wan.py` (force feedback; WAN needs chrony clock sync) · **with one arm:** your own loop sending slow Cartesian targets in `NRT_CARTESIAN_MOTION_FORCE` with a force cap, plus one-button assisted skills ("grasp handle", "turn 90°") built from primitives. Video over WebRTC. Loss of connection → robot goes `IDLE`, stops and holds (built in).
- **48-hour plan:**
  - **H0–6:** confirm number of arms and TDK licence; get one teleop path moving the arm; build valve / breaker / plug mock-ups.
  - **H6–24:** stable teleop with force cap; camera streams; first full valve close.
  - **H24–40:** assisted skills, operator UI (force bar, link-quality indicator), link-drop test, timing runs.
  - **H40–48:** rehearse with a non-team operator; backup video.
- **3-minute demo script:** (0:00) "road closed, gas smell in the pump room" → (0:20) operator, visibly elsewhere, grasps and closes the valve; force bar on screen → (1:30) flips the breaker with a one-button assist → (2:00) pull the network cable: robot freezes safely; reconnect and resume → (2:40) numbers: task time, peak force, latency.
- **Risks and fallbacks:** only one arm or no TDK licence → single-arm fallback above (no haptics, but visual force bar). Venue Wi-Fi jitter → wired LAN; present WAN as tested-once evidence. Operator struggles with depth → add a wrist camera and the assists.
- **Judging angles:** *innovation* — shared-autonomy assists on top of teleop; *technical depth* — force-limited control and fail-safe behaviour; *impact* — keeps staff out of hazardous spaces; *Leukerbad* — one road in, real closure risk.

### Concept 3 — Say it, approve it, done: semi-autonomous valve and breaker operator
- **Problem → value:** In an incident the duty officer has no time to joystick a robot. They say "isolate line 2"; the system finds the right valve, shows its plan, and executes after one click — the arm's force control handles the misalignment that vision leaves.
- **Hardware:** Rizon 4 / 4s + Grav; RGB-D camera (wrist or fixed); labelled mock panel with several valves / breakers. Optional: D-Robotics RDK X5 for on-edge detection; XREAL for plan overlay.
- **Architecture / stack:** speech / text → LLM maps the request to an asset ID and a skill from a fixed whitelist → perception (fiducials first; open-vocabulary detector + depth as stretch) gives a coarse pose → MoveIt (`flexiv_ros2`) or RDK primitives for the approach → contact primitive to seat on the handle, compliant turn until torque rises or the angle is reached → verify by camera + final torque → incident log. LLM in the cloud or on a laptop GPU; control on the laptop.
- **48-hour plan:**
  - **H0–6:** robot bring-up; camera-to-robot calibration; panel with markers.
  - **H6–24:** two skills (turn valve, flip breaker) working from marker poses, with force-based success checks.
  - **H24–40:** LLM command layer with whitelist + human approval screen; marker-free detection if time allows; failure recovery (retry / ask human).
  - **H40–48:** scripted scenario, rehearsal, backup video.
- **3-minute demo script:** (0:00) alarm on the dashboard → (0:20) operator speaks the command; UI highlights the chosen valve and plan → (0:45) approve; arm closes the valve, torque curve shows the hard stop → (1:45) judge shifts the panel a few centimetres; system still succeeds → (2:30) audit log and "what if the link drops" answer.
- **Risks and fallbacks:** calibration eats the day → fixed camera + markers only. LLM picks the wrong asset → whitelist, confirmation step and readable labels. Handle slips → printed handle adapter or Grav finger pads.
- **Judging angles:** *innovation* — language-to-safe-contact pipeline; *technical depth* — perception + force verification; *impact* — faster isolation of utilities; *Leukerbad* — small municipal crews covering many plant rooms.

### Concept 4 — Scout and fixer: multi-vendor incident response (most ambitious)
- **Problem → value:** End-to-end response: a legged scout finds and localises the fault in a 3D map; a fixed or wheeled "fixer" arm performs the intervention; one dashboard shows both. Demonstrates a city-scale pattern: many cheap scouts, a few capable hands.
- **Hardware:** Unitree Go2 / B2 or Genisom quadruped (scout) + SKYLANDX MetaCam (3D map) + Flexiv Rizon 4 / 4s + Grav (fixer; on an FMR 300 only if one is on site) + optional XREAL operator view.
- **Architecture / stack:** scout patrol → anomaly detected (thermal / visual cue or a mock gauge reading) → location pinned in the MetaCam map → task dispatched over a simple message bus (ROS 2 or MQTT) → Flexiv cell runs the Concept 3 skill (or Concept 2 teleop) → result written back to the map / twin. Each vendor's stack stays separate; integrate only at the message level.
- **48-hour plan:**
  - **H0–6:** split the team per robot; agree the message schema (asset ID, pose, action, status) before coding.
  - **H6–24:** each half works standalone: scout detects and reports; arm executes one skill.
  - **H24–40:** connect through the bus; shared dashboard; two full end-to-end runs.
  - **H40–48:** rehearse; record each half separately as backup.
- **3-minute demo script:** (0:00) map on screen, scout walking → (0:40) scout flags a leaking / overheated valve; pin appears → (1:10) task dispatched; arm closes the valve → (2:10) map pin turns green; timeline of the incident → (2:40) scaling story.
- **Risks and fallbacks:** two robot queues and two vendor stacks → highest schedule risk; if integration slips, present Concept 2 or 3 with a pre-recorded scout segment. Avoid mounting the arm on a quadruped (weight, power, controller — not a 48-hour job).
- **Judging angles:** *innovation* — heterogeneous fleet; *technical depth* — cross-vendor orchestration; *impact* — full detect-to-fix loop; *Leukerbad* — legged scout suits steep, snowy access while the arm stays in the sheltered plant room.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Flexiv arm + Unitree / Genisom quadruped | Scout finds, arm fixes (message-level hand-off) | Medium — two stacks, no physical coupling |
| Flexiv arm + SKYLANDX MetaCam | Interventions and touch-test results pinned into a 3D scan / twin | Low–medium — offline scan, manual registration |
| Flexiv arm + XREAL glasses | Head-up operator view for teleop: camera feed, force bar, plan overlay | Low — treat glasses as a display; medium if using the spatial SDK |
| Flexiv arm + D-Robotics RDK X5 | Edge vision (valve / gauge detection) next to the robot, no cloud needed | Low–medium |
| Flexiv arm + OriginFlow EMG capture | Gesture / muscle-signal input for hands-busy teleop | High — unproven pairing ⚠️ unverified |
| Flexiv arm + WUJI Hand | Dexterous manipulation of knobs and small switches | High — mechanical and control integration; skip unless vendors help |
| Flexiv FMR 300 / AICO (if present) + Rizon | Indoor "drive up and service" robot | Medium — AMR SDK + RDK; availability unlikely |

## Questions to ask the Flexiv Robotics engineers on site

1. Which arms and how many are here (Rizon 4, 4s, 10, Enlight L)? Is an FMR 300 or AICO base on site?
2. Is the **RDK licence** active on each robot, and which RDK version is installed? Is a **TDK licence** included?
3. For TDK: can we do robot-to-robot teleop with two arms here, and which leader *devices* are supported if only one arm is free?
4. Which primitives are available on these units for contact and compliant turning (approach-until-contact, force-hold, screw / rotate)? Is there a list for this firmware?
5. What force / speed / workspace safety limits are configured, and can we set our own Cartesian force caps and safety planes?
6. Is a real-time Ubuntu PC provided, or should we stay in non-real-time modes?
7. Can we mount a wrist camera (flange ISO 9409-1-50-4-M6) and is there a recommended bracket / calibration routine?
8. How many hours of robot time can one team book, and is there an Elements Studio / Isaac simulation set-up for off-robot development?

## Decision rule

- **Pick Flexiv Robotics for T02 if** your idea's key moment is *physical contact with infrastructure* (turn, plug, press, probe) done remotely or semi-autonomously indoors, and you are happy to build the mock-up and bring your own perception — or you are the "fixer" half of a multi-vendor team.
- **Avoid if** your idea needs outdoor or rough-terrain mobility, wide-area sensing, search-and-rescue or patrol, or you want one vendor to cover the whole T02 story — choose a quadruped or mapping vendor and treat Flexiv as optional.

## Sources
- [Flexiv — Rizon product page](https://www.flexiv.com/product/rizon)
- [Flexiv — Robot System page (Mico, AICO, Mello, Mobile Manipulator)](https://www.flexiv.com/product/robot-system)
- [Flexiv RDK manual — Control modes](https://www.flexiv.com/software/rdk/manual/v2.x/control_modes.html)
- [Flexiv RDK manual — Loss of connection](https://www.flexiv.com/software/rdk/manual/v2.x/loss_of_connection.html)
- [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk)
- [GitHub — flexiv_rdk Python examples](https://github.com/flexivrobotics/flexiv_rdk/tree/main/example_py)
- [GitHub — flexiv_tdk](https://github.com/flexivrobotics/flexiv_tdk)
- [GitHub — flexiv_tdk Python examples](https://github.com/flexivrobotics/flexiv_tdk/tree/main/example_py)
- [GitHub — flexiv_ros2](https://github.com/flexivrobotics/flexiv_ros2)
- [Flexiv Robotics company profile (local)](../Flexiv.md)
