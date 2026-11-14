---
type: challenge-playbook
company: "Spirit AI"
slug: Spirit-AI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Spirit AI × T02 — Hackathon Playbook

⬆ [Spirit AI profile](../Spirit-AI.md) · [Brief](Spirit-AI-T02-1-Brief.md) · [Products and solutions](Spirit-AI-T02-2-Products-and-Solutions.md)

**Read this first:** Spirit AI is a **2/5** fit for T02. Moz1 is indoor-only (**IP40**, no rain / snow / wet floors, flat floors assumed) and has no hazard sensors. Every concept below uses it for the one thing most T02 hardware lacks: **two arms that can operate things built for humans**. Frame the scene as a dry technical room — pump or plant room, tunnel service room, cable-car machine room, electrical room.

**Hour-0 gate (do this before committing):** confirm with Spirit AI staff that (1) a Moz1 is on site and how many teams share it, (2) the Quest teleop kit and the SDK wheel are available, (3) the navigation Docker stack is installed. If any answer is no, switch vendor.

## Solution approaches

### Concept 1 — Remote Hands: teleoperated intervention in an unsafe room

- **Problem → value:** after a leak, gas alarm or electrical fault, someone must enter to close a valve or trip a breaker. Send the robot; the operator stays outside. Value: no human exposure, minutes instead of waiting for specialist crews.
- **Hardware:** Moz1 + Quest VR teleop kit + wireless emergency stop. Mock panel: a quarter-turn ball valve, a rocker switch or breaker, a large push button, a door handle. Optional: XREAL glasses or a laptop as the operator's video wall.
- **Architecture / stack:**
  - Perception: head RealSense D455 + two wrist D405 streamed to the operator screen (build this yourself from `capture_observation()` frames; video inside the headset is not documented).
  - Planning: the human.
  - Control: stock teleop app (triggers = arms follow, grips = grippers, thumbstick = base, headset = torso).
  - Compute: operator PC cabled to the robot's industrial PC (CAT6); a second laptop for the video dashboard and an intervention log (timestamps, which control was actuated).
- **48-hour plan:**
  - H0–6: hour-0 gate; get teleop running; build the mock panel at a height the arms reach comfortably; test each control by hand for force and travel.
  - H6–24: practise the three or four interventions; stand up the camera dashboard; move the operator out of line of sight (longer cable or the robot's Wi-Fi hotspot — test which works).
  - H24–40: add operator aids: a checklist overlay, a wrist-camera picture-in-picture, automatic "task done" detection (switch state from the image) written to the log.
  - H40–48: rehearse the run five times, record a backup video, freeze.
- **3-minute demo script:** 0:00 alarm scenario on screen, "room is unsafe, nobody enters" → 0:30 operator behind a screen drives Moz1 through the door → 1:15 closes the valve, flips the breaker, presses alarm reset → 2:15 dashboard shows the logged, timestamped interventions → 2:40 one slide: where this goes in Leukerbad and what the robot cannot do yet.
- **Risks and fallbacks:**
  - Operator cannot work without line of sight → keep a large monitor with all three camera views; accept a visible operator behind a partition.
  - Valve too stiff for the gripper (payload and grip force are not public) → use a lever handle or 3D-print a larger grip.
  - Robot shared between teams → record every milestone on video as you go.
- **Judging angles:** innovation low–medium (teleop is known); technical depth medium only if you add the operator aids; real-world impact clear and easy to explain; Leukerbad relevance: technical rooms of thermal baths, clinics and lift stations are staffed thinly at night and off-season.

### Concept 2 — Night Round: autonomous indoor inspection patrol

- **Problem → value:** routine safety rounds (gauges, escape routes, fire doors, leaks) are skipped when staff are short. A robot does the round and files a report with evidence photos.
- **Hardware:** Moz1 (LiDAR + cameras). Optional: SKYLANDX MetaCam for a reference 3D scan; D-Robotics RDK board for on-edge vision.
- **Architecture / stack:**
  - Perception: head-camera frames at each checkpoint → vision-language model or small detector on a team laptop (gauge in range? door closed? corridor blocked? puddle?).
  - Planning: a fixed list of map-frame poses plus a torso / head posture per checkpoint.
  - Control: navigation Docker stack (LiDAR SLAM + Navigation2); goals sent through the ROS 2 pose-sequence service (`navigation_interfaces`, see the stack's `scripts/example.py`); postures via SDK `reset_robot_positions()`.
  - Compute: navigation on the robot; perception and report on the laptop; Cyclone DDS, `ROS_DOMAIN_ID=33`.
- **48-hour plan:**
  - H0–6: map the demo area with the gamepad (keep people out of the scan), save the map, send one goal from rviz, then one from Python.
  - H6–24: four to six checkpoints with stored poses; image capture at each; first anomaly classifier; JSON report.
  - H24–40: staged anomalies (blocked exit, gauge in the red, open fire door, cone on the floor); web dashboard with map, photos and status; re-run reliability.
  - H40–48: tune speed (docs suggest starting at 50 %), rehearse, record backup.
- **3-minute demo script:** 0:00 show the map and the round → 0:20 robot drives to checkpoint 1, looks, "OK" → 1:00 a judge blocks the escape route with a box → 1:30 robot flags it, photo appears on the dashboard, alert sent → 2:20 summary report → 2:40 limits and next steps.
- **Risks and fallbacks:**
  - Relocalisation fails in a crowded hall → rope off a small area; fall back to gamepad driving between checkpoints with autonomous perception only.
  - Navigation service names are not in the public docs → get them from staff at H0; otherwise click goals in rviz.
  - A quadruped or a camera on a pole does this more cheaply → judges will ask "why a dual-arm humanoid?"; go to Concept 3 for the answer.
- **Judging angles:** innovation low; technical depth medium (navigation + perception + reporting); impact moderate; Leukerbad relevance: clinic and spa technical corridors, hotel back-of-house in low season.

### Concept 3 — Inspect and Act: patrol, detect, then fix with shared autonomy

- **Problem → value:** inspection robots only report; a person still has to go and act. Close the loop: the robot finds the fault and performs the first corrective action, autonomously for scripted cases and by operator takeover for the rest.
- **Hardware:** Moz1 + VR teleop kit. Optional: SKYLANDX MetaCam scan as the digital-twin view; XREAL glasses for the supervisor.
- **Architecture / stack:**
  - Perception: as Concept 2, plus a fiducial marker next to each actuated control to localise it for the arm.
  - Planning: a small state machine — patrol → anomaly → choose action (scripted skill, or "request operator").
  - Control: navigation service for the base; scripted skills as recorded Cartesian trajectories replayed through `send_action()` at the control rate (smooth, no jumps); operator takeover through the teleop app. Only one external controller should command the robot at a time — design an explicit handover.
  - Compute: robot for navigation; laptop for the state machine, perception and dashboard.
- **48-hour plan:**
  - H0–6: hour-0 gate plus the Concept 2 mapping step; decide the two scripted skills (for example push button, pull lever).
  - H6–24: patrol working (Concept 2 core); record and replay skill 1 from a marker-relative pose.
  - H24–40: skill 2; operator-takeover path for a third, harder action (valve turn); incident timeline on the dashboard.
  - H40–48: full-loop rehearsals; cut any skill below 4-in-5 success and show it by teleop instead.
- **3-minute demo script:** 0:00 robot on its round → 0:30 detects "gauge in the red" → 0:50 drives to the panel and presses the shut-off button on its own → 1:30 second anomaly it cannot handle; the dashboard pages the operator → 1:50 operator takes over in VR and closes the valve → 2:30 timeline shows detect → act → verify → 2:45 limits.
- **Risks and fallbacks:**
  - Base stops a few centimetres off, so replayed trajectories miss → correct with the marker pose from the wrist camera, or use large, forgiving targets.
  - Handover between navigation, SDK and teleop is undocumented → ask staff for the supported mode-switch sequence; worst case, restart between phases and narrate it.
  - Too much scope → the fallback is Concept 2 + Concept 1 shown back to back.
- **Judging angles:** innovation medium–high (detect-and-act with human fallback); technical depth high; impact strong for unstaffed facilities; Leukerbad relevance: small municipality, many technical sites, few technicians.

### Concept 4 — Mixed team: rough-terrain scout plus indoor manipulator, with a learned skill

- **Problem → value:** a real incident spans outdoors and indoors. A legged robot or handheld scanner gets eyes on the scene and builds the map; Moz1 does the manipulation where the floor is flat and dry. Stretch goal: the intervention is a learned policy, commanded in language.
- **Hardware:** Moz1 + a quadruped from Unitree or Genisom AI (scout) + SKYLANDX MetaCam (3D map) + operator station. Stretch: cloud GPUs for policy fine-tuning.
- **Architecture / stack:**
  - Perception: scout camera and scan → shared incident map on a laptop; Moz1 cameras for close-range work.
  - Planning: a simple coordinator assigns "look" tasks to the scout and "act" tasks to Moz1 by location.
  - Control: each robot through its own SDK; coordinator talks to both over the venue network. For the stretch goal, record teleop demonstrations of one skill and fine-tune the Pi0.5 / openpi Moz1 adaptation or Spirit v1.5 (needs staff-supplied code or checkpoint, plus data-centre GPUs).
  - Compute: laptop coordinator; cloud for any training; inference host on the robot or a GPU laptop.
- **48-hour plan:**
  - H0–6: secure both robots and confirm time slots; define one message format (location, task, status).
  - H6–24: scout streams images and a pose; Moz1 patrol + one teleop intervention; start collecting demonstrations if doing the stretch.
  - H24–40: coordinator and common dashboard; integrate the 3D scan as a backdrop; go / no-go on the learned skill at H30.
  - H40–48: end-to-end rehearsal; backup video per robot.
- **3-minute demo script:** 0:00 incident call → 0:20 scout crosses rough ground and finds the fault location → 1:00 map updates, task goes to Moz1 → 1:20 Moz1 drives in and performs the intervention (learned, scripted or teleoperated) → 2:20 combined timeline and 3D view → 2:45 what each robot contributed.
- **Risks and fallbacks:**
  - Two vendors, two SDKs, one weekend → keep the link to a single HTTP or ROS message; if it breaks, run the robots in sequence with a human relaying the task.
  - Learned skill does not converge (fine-tuning is specified for **8 × A100**) → replace with the scripted or teleoperated version; say so openly.
  - MetaCam map import into Moz1 navigation is untested (Moz1 relocalisation takes PLY / PCD) → use the scan for visualisation only.
- **Judging angles:** innovation high; technical depth high but fragile; impact strongest story of the four; Leukerbad relevance: snow and slopes outside, technical rooms inside — matches the real terrain split.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Moz1 + Unitree Go2 / B2 or Genisom quadruped | Outdoor or stair scouting plus indoor manipulation (Concept 4) | High — two SDKs; keep the interface to one message |
| Moz1 + SKYLANDX MetaCam | 3D scan of the room as digital-twin view; possible map source (PLY / PCD compatibility ⚠️ unverified) | Low for visualisation, medium–high as a navigation map |
| Moz1 + XREAL glasses | Hands-free supervisor view of camera feeds and incident timeline | Low–medium (display a web dashboard) |
| Moz1 + D-Robotics RDK X5 / S100 | On-edge anomaly detection without a laptop; Spirit AI and D-Robotics already cooperate on the S600 chip (not an RDK board) | Medium |
| Moz1 + OriginFlow EMG capture | Alternative operator input for teleop | High, speculative |
| Moz1 + Binabik AI or coprod stack | Agent layer or common middleware across robots | Unknown — ask both teams; no public Moz1 integration |

## Questions to ask the Spirit AI engineers on site

1. How many Moz1 units are here, and how is robot time shared between teams?
2. Can the Quest teleop run with the operator out of sight — over the robot's Wi-Fi hotspot or a long cable — and does the headset show the camera feed? What latency should we expect?
3. What are the per-arm payload and gripper force, and can Moz1 turn a quarter-turn valve or pull a breaker lever?
4. Does the SDK expose force / torque read-out or impedance settings, or only position streaming?
5. What are the ROS 2 service names and message types for navigation goals, and can we read the robot pose and goal status from Python?
6. What is the supported way to switch between navigation, SDK external-following mode and teleop without restarting?
7. What floor conditions are allowed — door thresholds, ramps, damp concrete — and what is the real battery runtime under arm load?
8. Can you provide a Moz1-ready Spirit v1.5 or Pi0.5 checkpoint and GPU access, or should we plan without a learned policy?

## Decision rule

- **Pick Spirit AI for T02 if** your idea needs a robot to physically operate human-built controls indoors (valves, switches, doors) and you are happy with teleop or scripted skills on a single shared Moz1.
- **Avoid if** your scenario is outdoors, wet, snowy, on stairs or sensor-driven (thermal, gas, mapping at scale) — choose a quadruped or scanning vendor and, at most, add Moz1 as the indoor "hands".

## Sources

- [Docs: Moz1 mechanical structure (DoF, sensors, IP rating, environment)](https://docs.spirit-ai.com/zh/moz1/mechanics.html)
- [Docs: Moz1 safety requirements](https://docs.spirit-ai.com/zh/moz1/safety.html)
- [Docs: Moz1 remote controller](https://docs.spirit-ai.com/zh/moz1/controller.html)
- [Docs: MozRobot SDK quick start](https://docs.spirit-ai.com/zh/sdk/get-started.html)
- [Docs: MozRobot SDK API reference](https://docs.spirit-ai.com/zh/sdk/api.html)
- [Docs: MozRobot SDK examples](https://docs.spirit-ai.com/zh/sdk/examples.html)
- [Docs: SLAM navigation](https://docs.spirit-ai.com/zh/slam-nav/slam_navigation.html)
- [Docs: teleoperation quick start](https://docs.spirit-ai.com/zh/teleop/get-started.html)
- [Spirit AI news: WAIC 2026, Moz2 debut](https://www.spirit-ai.com/en/news/48)
- [Spirit AI company profile in this vault (Spirit v1.5, Pi0.5 adaptation, D-Robotics partnership and their sources)](../Spirit-AI.md)
