---
type: challenge-playbook
company: "WUJI"
slug: WUJI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# WUJI × T01 — Hackathon Playbook

⬆ [WUJI profile](../WUJI.md) · [Brief](WUJI-T01-1-Brief.md) · [Products and solutions](WUJI-T01-2-Products-and-Solutions.md)

**Read first:** WUJI is a **supporting vendor** for T01 (fit 2/5). Every concept below needs a partner arm or robot, and all are **indoor** (hotel, clinic, spa, lift lobby). The winning angle is narrow but real: service robots get stuck wherever the building expects a human hand.

## Solution approaches

### Concept 1 — "Remote hands" tele-assist station (safest)

- **Problem → value:** Delivery and service robots stall at human interfaces (keypads, lift panels, key-card readers). One remote operator wearing a glove takes over the hand for 20 seconds, then autonomy resumes. One operator can back up many robots.
- **Hardware:** Wuji Hand 2 or Wuji Hand on its desk mount or a fixed partner arm · Wuji Glove · webcam at the hand. Optional: XREAL glasses as the operator's view.
- **Architecture / stack:** Glove `hand_skeleton` → SDK `RetargetSession` (21 keypoints → 20 joint angles) → hand joint commands. Camera stream to the operator. A small state machine: AUTONOMOUS → HELP REQUESTED → TELEOP → RESUME. Everything on one Linux or Apple-silicon laptop. No-glove fallback: webcam + MediaPipe world landmarks into the same retargeter.
- **48-hour plan:**
  - H0–6: get hand + glove running with the SDK teleop example; build a mock panel (lift buttons, keypad, card reader).
  - H6–24: operator video view, help-request trigger, MCAP logging of each intervention.
  - H24–40: record interventions and **replay** the most common one (e.g. floor-2 button) autonomously — "the fleet learns from each assist".
  - H40–48: rehearse; measure time-to-resolve per intervention.
- **3-minute demo script:** (1) Robot stand-in reaches the panel and raises "need a hand". (2) Operator across the room puts on the glove, presses the code, taps the key card. (3) Second attempt: the logged intervention replays without the operator. (4) One slide: interventions per robot per day × operator seconds.
- **Risks and fallbacks:** Glove EMF tracking near metal panels (keep ≥ 3 cm; glove stays with the operator, away from the rig) · Hand 2 position mode is Beta → fall back to Hand gen 1 · if no arm, the panel is brought to the hand on a slider.
- **Judging angles:** Innovation — medium · Technical depth — medium · Impact — a practical human-in-the-loop model for service fleets · Leukerbad — older hotels and clinics cannot retrofit every lift and door for robots.

### Concept 2 — "Button and handle" skill module on a force-controlled arm

- **Problem → value:** Give any indoor delivery robot an autonomous skill for lift buttons, door openers and lever handles — the last gap in door-to-door indoor delivery.
- **Hardware:** Wuji Hand (gen 1 preferred: published **15 N** fingertip force) or Hand 2 · Flexiv Rizon or ROKAE xMate arm (force / torque sensing) · RGB-D or wrist camera.
- **Architecture / stack:** Perception: fiducial tag or small detector locates the panel and target button → arm planner moves to a pre-contact pose → hand takes a canned pose (index extended, others curled) → arm pushes along the finger axis until its force sensing reports contact → verify (button light / door opens). Hand poses are recorded once via glove teleop and replayed. Arm vendor SDK + Wuji Python SDK in one process; laptop compute.
- **48-hour plan:**
  - H0–6: adapter plate (STEP in `wuji-description`; 1 × M3 + 2 × M4 pattern) — 3D-print or ask WUJI for a flange; cable routing; e-stop check.
  - H6–24: pose library (press, pinch card, wrap handle); panel localisation; force-guarded press.
  - H24–40: second skill (lever handle or key-card tap); success-rate test over 20 trials.
  - H40–48: polish, record backup video.
- **3-minute demo script:** (1) Operator names a floor. (2) Arm + hand find and press the correct button on a mock panel moved to a new position. (3) Hand picks a key card and taps the reader. (4) Show the trial log and success rate.
- **Risks and fallbacks:** Hand 2 wrist-load limits are unpublished → press with low force, let the arm's force control do the work · adapter plate not ready → clamp the factory base to a bracket · perception flaky → fiducial tags.
- **Judging angles:** Innovation — medium · Technical depth — high (force-guarded contact, hand + arm coordination) · Impact — reusable module · Leukerbad — spa hotels, rehab clinics, multi-storey buildings on steep terrain.

### Concept 3 — Hotel / clinic runner: mobile manipulator with a WUJI hand

- **Problem → value:** A robot delivers towels, parcels or pharmacy bags from reception to a room **through a lift and a door**, with no building retrofit. Frees staff in a seasonal resort.
- **Hardware:** Wheeled dual-arm platform (Galaxea R1 family, Galbot G1 or AGIBOT G1 / G2) with **one** Wuji Hand on one arm, stock gripper on the other · Wuji Glove for tele-assist. Power note: Hand 2 needs 11–13 V DC, up to 20 A adapter rating — confirm the robot can supply it or carry a battery.
- **Architecture / stack:** Partner robot's navigation stack for corridor travel → Concept 2 skill at the lift → handover at the door (hand opens when the recipient pulls; with Hand 2 use back-drivability / joint tracking error as the release cue) → Concept 1 tele-assist when a step fails. Wuji SDK on the robot's onboard Linux PC or a strapped-on laptop; if the robot runs ROS 2 Humble, bridge through a thin Python node instead of `wuji-ros2` (Lyrical only).
- **48-hour plan:**
  - H0–6: secure a platform and WUJI's agreement to mount; power + mount; navigation between two waypoints.
  - H6–24: button press from the mobile base (base positioning error is the hard part); handover behaviour.
  - H24–40: full run reception → lift panel → door; add tele-assist.
  - H40–48: three clean runs filmed; live demo on the shortest reliable route.
- **3-minute demo script:** (1) "Room 12 needs towels." (2) Robot drives, presses the lift button with a finger. (3) Arrives, knocks or rings, hands over. (4) One forced failure → operator glove assist → continues.
- **Risks and fallbacks:** Two vendors' time and hardware needed — highest scheduling risk · base misalignment → fiducials at the panel · if mobile integration slips by H24, drop to Concept 2 on a static arm and show navigation separately.
- **Judging angles:** Innovation — medium-high · Technical depth — high · Impact — high and easy to explain · Leukerbad — strong (hotels, thermal baths, clinics).

### Concept 4 — Learned dexterous service skill (most ambitious)

- **Problem → value:** Replace hand-coded poses with a policy learned from glove demonstrations, so new service tasks (sorting key cards, opening a parcel-locker latch) are taught, not programmed.
- **Hardware:** Wuji Hand(s) on partner arm(s) · Wuji Glove · arm teleop device · head + wrist cameras · **NVIDIA GPU** (CUDA 12).
- **Architecture / stack:** Glove + arm teleop → MCAP / LeRobot episodes → fine-tune with `wuji-openpi` (pi0.5; reference config is dual 7-DoF arms + two hands, 54-D, configurable) or a lighter behaviour-cloning policy → ROS 2 Humble deployment.
- **48-hour plan:** H0–6 teleop rig working · H6–24 collect 50–100 episodes of one task · H24–40 fine-tune and evaluate · H40–48 demo, with teleop as fallback.
- **3-minute demo script:** Show a demonstration, the training curve, then the policy doing the task; compare against scripted replay when the object is moved.
- **Risks and fallbacks:** No published checkpoints or datasets; teleop repo is archived and tied to Tianji arms; training time may exceed the weekend. Fallback: present the data pipeline + scripted replay (Concept 2).
- **Judging angles:** Innovation — high · Technical depth — very high · Impact — long-term · Leukerbad — weak unless the task is local.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| WUJI Hand + Flexiv Rizon or ROKAE xMate | Force-guarded button / handle / card skills (Concept 2) | Medium — adapter plate, two SDKs |
| WUJI Hand + Galaxea R1 / Galbot G1 / AGIBOT G1 | Mobile indoor delivery through lifts and doors (Concept 3) | High — mount, power, base alignment, two teams |
| WUJI Hand + Unitree G1 humanoid | Humanoid concierge with a five-finger hand | High — wrist interface and payload unknown, ⚠️ unverified fit |
| WUJI Glove + Hand + XREAL glasses | Remote operator sees the scene and drives the hand (Concept 1) | Low–medium |
| WUJI Hand + Dobot CR / Nova cobot | Fixed concierge counter: key-card and small-item handover | Medium — no arm-side force sensing assumed; rely on hand compliance |
| WUJI SDK on D-Robotics RDK | Small edge host on the robot instead of a laptop | Low–medium — SDK ships Linux arm64 builds; not tested on RDK, ⚠️ unverified |
| WUJI Glove + OriginFlow EMG | Richer operator-intent data for demonstrations | High, research-grade — skip for T01 |

## Questions to ask the WUJI engineers on site

1. How many hands (gen 1 vs. Hand 2, left / right) and gloves are here, and how is access shared?
2. Which arm flanges did you bring adapters for? Any already mounted on a partner robot on site?
3. Hand 2: what are safe **wrist load, fingertip force and payload** limits for pressing buttons and turning handles? IP rating?
4. Can we read per-joint effort / current for contact detection, and at what rate?
5. Is Hand 2 **position mode** stable on the firmware installed here, or should we stay in MIT mode? Recommended kp / kd for contact tasks?
6. ROS 2: is there a Humble build or Docker image, or should we bridge through the Python SDK?
7. Can Hand 2 run from a mobile robot's battery (11–13 V)? Peak current in practice?
8. Spare soft pads / skins on site, and what happens if we damage a finger?

## Decision rule

- **Pick WUJI for T01 if** your idea hinges on a robot using infrastructure made for human hands (buttons, handles, key cards, handovers) indoors, you have a committed partner arm or mobile platform by H6, and someone on the team can build an adapter plate and merge two SDKs.
- **Avoid if** your core is navigation, outdoor delivery, cleaning or waste logistics, you want a single-vendor robot, or a simple gripper would do the job.

## Sources

- [WUJI company profile (this repo)](../WUJI.md)
- [Wuji Hand 2 (2.2 Beta) product introduction](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md)
- [Wuji Hand 2 mechanical integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration.md)
- [Wuji Hand 2 SDK practice — replaying a thumb opposition](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-practice/opposition-replay.md)
- [Wuji Hand (gen 1) product introduction](https://docs.wuji.tech/docs/en/wuji-hand/v1/overview.md)
- [Wuji Glove product introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md)
- [Wuji SDK — hand retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md)
- [Wuji Docs — English index](https://docs.wuji.tech/_llms/en.txt)
- [GitHub: wuji-ros2](https://github.com/wuji-technology/wuji-ros2)
- [GitHub: wuji-openpi](https://github.com/wuji-technology/wuji-openpi)
- [GitHub: wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop)
- [GitHub: wuji-sdk](https://github.com/wuji-technology/wuji-sdk) · [wuji-description](https://github.com/wuji-technology/wuji-description)
