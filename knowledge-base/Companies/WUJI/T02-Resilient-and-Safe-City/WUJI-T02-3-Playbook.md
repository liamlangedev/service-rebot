---
type: challenge-playbook
company: "WUJI"
slug: WUJI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# WUJI × T02 — Hackathon Playbook

⬆ [WUJI profile](../WUJI.md) · [Brief](WUJI-T02-1-Brief.md) · [Products and solutions](WUJI-T02-2-Products-and-Solutions.md)

**Read first:** WUJI = hand + glove + SDK. No arm, no base, no cameras, no autonomy. Hands are dry-lab devices (IP40 / 15–30 °C). Every concept below is an **indoor mock-up** of a hazard task and needs a partner vendor, except Concept 2.

## Solution approaches

### Concept 1 — Remote Hands: hazard-panel teleoperation cell

- **Problem → value:** After a gas alarm, fire or flooding in a technical room (thermal-water plant, cable-car drive room, tunnel substation), someone still has to close a valve, trip a breaker or pull a plug. A glove-driven robot hand does it while the technician stays outside.
- **Hardware:** Wuji Glove + Wuji Hand 2 (or Hand gen 1) · one partner arm (Flexiv Rizon or ROKAE xMate preferred for compliant contact; Dobot CR as alternative) · 1–2 USB cameras · a plywood "hazard panel" with a quarter-turn valve, a rocker / breaker switch, a connector, a door handle.
- **Architecture / stack:**
  - Perception: operator's eyes via camera feed on a monitor (no machine perception needed).
  - Planning: arm moves between **pre-taught poses** ("valve", "breaker", "plug") selected by keyboard or foot pedal, plus small jog offsets. The glove has no wrist position, so do not plan on free-hand arm teleop on day 1.
  - Control: `1.teleop_real.py` from `wuji-sdk` (glove → retargeting → 20 joint commands at 1000 Hz). Set `effort_limit` and soft kp / kd on Hand 2 for gentle contact. Arm through its vendor SDK.
  - Compute: one laptop on the 192.168.1.x subnet for glove + hand; arm controller on a second interface.
- **48-hour plan:**
  - H0–6: secure a hand, a glove and an arm slot; confirm flange adapter; run glove-to-hand teleop on the desk stand; build the panel.
  - H6–24: mount hand on arm; teach arm poses; tune stiffness and effort limits per task; add camera view.
  - H24–40: record every run to MCAP; add a simple operator UI (task buttons, hand temperature / fault status); measure task times.
  - H40–48: rehearse, film a backup video, freeze the code.
- **3-minute demo script:** (0:00) alarm scenario on screen, operator sits behind a partition. (0:30) arm goes to "valve", operator closes it with the glove. (1:15) "breaker" tripped, connector pulled. (2:15) show the recorded session replay and task times versus sending a person in protective gear. (2:45) limits and next steps.
- **Risks and fallbacks:** no adapter plate → hand stays on the desk stand and the panel is brought to the hand. Glove tracking jitter near metal → keep 3 cm clearance, or use webcam + MediaPipe keypoints into the SDK retargeter. Hand 2 fault or overheating → switch to Hand gen 1. Valve too stiff for the 15 N class → use a lever-handle valve.
- **Judging angles:** innovation — human tools operated without a custom gripper; technical depth — compliance tuning, retargeting, logging; impact — keeps staff out of hazard zones; Leukerbad — thermal plant rooms and lift machinery in a valley that road closures can isolate.

### Concept 2 — Gesture and grip command glove for a patrol robot (glove-only)

- **Problem → value:** In noise, darkness or with a radio in the other hand, responders command robots badly by voice or tablet. A glove turns hand signals into robot commands and logs what the responder's hand did.
- **Hardware:** Wuji Glove only · any mobile robot with an open motion API (Unitree Go2, Genisom M1, Magiclab MagicDog) · laptop. No Wuji Hand and no arm needed — the choice if hands are fully booked.
- **Architecture / stack:**
  - Perception: glove joint angles (EMF inverse kinematics) + palm IMU + tactile map.
  - Planning: small classifier (k-NN or a tiny MLP on 20 joint angles) for 6–8 static signals (stop, come, search left / right, sit, return); tactile squeeze as a dead-man confirm.
  - Control: map classes to the robot's high-level velocity / mode API.
  - Compute: laptop; glove is tethered by Ethernet, so the operator carries the laptop or stays at a console.
- **48-hour plan:**
  - H0–6: glove streaming, per-user calibration; robot API hello-world.
  - H6–24: collect gesture data (MCAP), train classifier, add confirm logic.
  - H24–40: run a short "search the corridor" course; add event log.
  - H40–48: rehearse; measure recognition accuracy and false triggers.
- **3-minute demo script:** responder signals the quadruped through a mock search course without speaking; squeeze-to-confirm prevents accidental commands; show the log and accuracy numbers.
- **Risks and fallbacks:** tether limits walking range → present as a console or vehicle-mounted operator. Humidity limit (< 55 % RH) and metal sensitivity → keep it indoors. Weak WUJI differentiation (a camera could do gestures) → emphasise tactile confirm and no line of sight.
- **Judging angles:** innovation — moderate; technical depth — modest; impact — practical operator interface; Leukerbad — mountain-rescue style hand signals in poor visibility. Lowest risk, lowest ceiling.

### Concept 3 — Mobile Remote Hands with AR operator view

- **Problem → value:** The hazard is not next to the robot. A mobile platform carries the hand to the cabinet or valve; the operator sees the scene in AR and works through the glove.
- **Hardware:** Wuji Glove + Wuji Hand 2 · mobile manipulator or humanoid with a free wrist (Galaxea R1 family, AGIBOT G1 / G2, Unitree G1 / H1, Spirit AI Moz1, UniX Wanda — whichever team will allow an end-effector swap) · XREAL glasses for the camera view · optional SKYLANDX MetaCam scan of the room as a 3D context map.
- **Architecture / stack:**
  - Perception: robot head / wrist camera stream to XREAL; pre-scanned 3D model for orientation.
  - Planning: base driven by the vendor's teleop or navigation; arm by vendor teleop or pre-taught poses; fingers by glove.
  - Control: Wuji SDK or `wuji-ros2` node on the robot's onboard computer or a tethered laptop; hand needs a 12 V rail and Ethernet on the robot.
  - Compute: robot onboard PC + operator laptop on one network.
- **48-hour plan:**
  - H0–6: agree with the partner vendor on mounting, power and network; bench teleop.
  - H6–24: mechanical and electrical integration; camera to glasses; drive-and-reach test.
  - H24–40: full mission run (drive in → open cabinet → flip switch → drive out); log everything.
  - H40–48: rehearse; backup video.
- **3-minute demo script:** operator in glasses and glove at a desk; robot drives into the "sealed" area, opens a cabinet door and isolates a circuit; split screen shows operator hand and robot hand.
- **Risks and fallbacks:** end-effector swap refused or adapter missing → fall back to Concept 1 on a fixed arm placed on a cart. Network latency over Wi-Fi → keep hand control on the robot's onboard PC and send only glove data. Weight and power budget on the wrist (800 g + cabling) → check with the vendor first.
- **Judging angles:** innovation — multi-vendor remote-presence system; technical depth — high integration; impact — closest to a real response robot; Leukerbad — remote expert operates local equipment when the access road is closed.

### Concept 4 — Teach once by teleop, repeat when the link drops

- **Problem → value:** Teleoperation fails when communication fails. Record the operator's valve-closing or breaker-trip demonstration and let the robot repeat it autonomously on link loss.
- **Hardware:** as Concept 1 (fixed arm + hand + glove) plus a wrist or scene camera; NVIDIA GPU machine only for the stretch goal.
- **Architecture / stack:**
  - Perception: fiducial marker (AprilTag) on the panel to re-locate the target; camera on the arm.
  - Planning: baseline = **trajectory replay** of recorded arm poses and hand joint trajectories, re-anchored to the marker, with compliant kp / kd. Stretch = fine-tune pi0.5 with `wuji-openpi` (needs LeRobot v2.1 data, CUDA 12 GPU, no checkpoints provided — unlikely to converge in 48 h).
  - Control: heartbeat between operator PC and robot PC; on timeout switch from teleop to stored skill, then to a safe open-hand pose.
  - Compute: laptop for baseline; GPU workstation for the stretch.
- **48-hour plan:**
  - H0–6: Concept 1 basics.
  - H6–24: reliable teleop; record 20–50 demonstrations per skill to MCAP together with arm states.
  - H24–40: replay with marker re-anchoring; heartbeat and mode switch; success-rate test with the panel moved a few centimetres.
  - H40–48: rehearse the cable-pull moment; backup video.
- **3-minute demo script:** operator starts closing the valve, a team member unplugs the network cable, the robot finishes the job alone and reports status when the link returns.
- **Risks and fallbacks:** replay is brittle to panel pose → keep the marker and limit offsets; no robot-side touch sensing → rely on compliance, not force thresholds (docs advise against using joint current as force). If autonomy fails, demo Concept 1 and show replay in simulation with the MJCF model.
- **Judging angles:** innovation — shared autonomy for degraded communication; technical depth — highest; impact — resilience is literally the track title; Leukerbad — alpine valleys lose connectivity in storms.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| WUJI hand + **Flexiv Rizon** | Force-controlled arm for compliant valve turning and door opening | Medium: adapter plate, two SDKs on one PC |
| WUJI hand + **ROKAE xMate** (7-DoF, joint torque sensing) | Same role; hand-guided teaching of arm poses | Medium |
| WUJI hand + **Dobot CR / Nova** | Simple position-controlled carrier with easy pose teaching | Low–medium |
| WUJI hand + **Unitree G1 / H1** or **AGIBOT** humanoid | Humanoid with a 20-DoF hand for a mobile response story | High: wrist mount, power, vendor approval |
| WUJI hand + **Galaxea R1** / **Galbot G1** / **Spirit AI Moz1** | Wheeled dual-arm base that drives the hand to the task | High: end-effector swap |
| WUJI glove + **Unitree Go2** / **Genisom M1** / **MagicDog** | Gesture-commanded patrol or search robot (Concept 2) | Low: software only |
| WUJI teleop + **XREAL** glasses | Head-up camera view for the operator | Low–medium: video streaming app |
| WUJI teleop + **SKYLANDX MetaCam** | 3D scan of the room as operator context / digital twin | Low if used as a pre-scan |
| WUJI glove + **OriginFlow** EMG | Two-channel operator input (pose + muscle effort) for grip-strength commands | Medium, research-style ⚠️ unverified compatibility |
| WUJI hand + **D-Robotics RDK** | Onboard host for the hand SDK on a mobile robot (SDK supports Linux arm64) | Medium ⚠️ not tested by WUJI as far as public docs show |

## Questions to ask the WUJI engineers on site

1. How many Hand 2, Hand gen 1 and glove units are available per team, and for how many hours?
2. Which arm flange adapters did you bring, and for which vendors' arms on site? Can we get the STEP file for a printed plate?
3. Which firmware is on the Hand 2 units — is position mode (firmware v3.0.0+) available, or MIT mode only?
4. What kp / kd and `effort_limit` values do you recommend for turning a valve and flipping a switch? What fingertip force can Hand 2 safely deliver?
5. What happens to the hand if the Ethernet link or the host process dies — hold, relax or fault? Is there a command watchdog?
6. How do you recommend getting wrist pose for arm teleoperation with the glove (which tracker and mount)? Did you bring any?
7. How long can Hand 2 hold a loaded grasp before thermal derating, and how do we read temperature?
8. Is a tactile Hand 2 or any ruggedised / sealed version planned, and has any customer used the hands for remote operation in hazardous areas?

## Decision rule

**Pick WUJI for T02 if** your idea is teleoperated or taught manipulation of human-scale controls in a staged indoor hazard scene, and you have secured a partner arm (or mobile manipulator) plus a mounting adapter in the first six hours.

**Avoid if** your idea is patrol, mapping, monitoring, outdoor or wet operation, heavy-force rescue, or anything that must run autonomously out of the box — WUJI adds cost and integration risk without solving those.

## Sources

- [WUJI company profile (this repo)](../WUJI.md)
- [Wuji Glove quick start (incl. glove-to-hand teleoperation)](https://docs.wuji.tech/docs/en/wuji-glove/latest/getting-started.md)
- [Wuji Glove introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md)
- [Wuji Hand 2 (2.2 Beta) overview](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md)
- [Wuji Hand 2 user notice / usage constraints](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md)
- [Wuji Hand 2 mechanical integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration.md)
- [Wuji Hand 2 joint states and control](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/joint-control.md)
- [Wuji Hand 2 effort and MIT parameters](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/effort-and-mit.md)
- [Wuji Hand (gen 1) overview](https://docs.wuji.tech/docs/en/wuji-hand/v1/overview.md)
- [Wuji SDK data recording](https://docs.wuji.tech/docs/en/wuji-sdk/latest/data-recording.md)
- [Wuji SDK hand retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md)
- [GitHub: wuji-sdk](https://github.com/wuji-technology/wuji-sdk) · [wuji-ros2](https://github.com/wuji-technology/wuji-ros2) · [wuji-description](https://github.com/wuji-technology/wuji-description) · [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop) · [wuji-openpi](https://github.com/wuji-technology/wuji-openpi)
