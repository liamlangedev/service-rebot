---
type: challenge-playbook
company: "Dobot Robotics"
slug: Dobot
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Dobot Robotics × T04 — Hackathon Playbook

⬆ [Dobot Robotics profile](../Dobot.md) · [Brief](Dobot-T04-1-Brief.md) · [Products and solutions](Dobot-T04-2-Products-and-Solutions.md)

**Before you commit (first 30 minutes at the Dobot booth):** which arm models, how many, firmware **V4.4.0.0+**?, which gripper, is a **CRAF** (force sensor) or **X-Trainer** on site?

**Setup that applies to every concept:** laptop on the robot subnet (192.168.5.x, robot default 192.168.5.1), robot in TCP/IP mode, ports 29999 + 30004 free, `TCP-IP-Python-V4` cloned. ROS 2 route needs Ubuntu 22.04 + Humble.

**Safety rules for a care demo:** low `SpeedFactor`, most sensitive `SetCollisionLevel`, safe wall / work zone between arm and person, E-stop in a team member's hand, no approach to a real person's head or neck — use a mannequin or a team member's forearm. None of these arms is a certified medical device.

## Solution approaches

### Concept 1 — Rehab motion coach (no-contact, safest)

- **Problem → value:** home or clinic exercise sessions lack supervision between therapist visits. A therapist drag-teaches an upper-limb exercise once; the arm replays it as a moving target the patient follows by hand, and a camera scores repetitions, range of motion and smoothness. Therapist gets a progress report.
- **Hardware:** Nova 5 (or CR5A / Magician E6) + a bright target on the flange + webcam + laptop. Optional: XREAL glasses for an AR overlay, OriginFlow EMG for muscle-activation feedback.
- **Architecture / stack:** *Teach* — `StartDrag`, sample `GetPose` into a waypoint list, `StopDrag`. *Replay* — `MovL` / `ServoP` at a speed scaled to the patient. *Perception* — body / hand pose estimation from the webcam on the laptop CPU (for example MediaPipe); compute hand-to-target distance and joint angles. *Adaptation* — slow down or shrink the trajectory when the patient lags. *UI* — web dashboard with rep count and range-of-motion trend. All compute local.
- **48-hour plan:**
  - H0–6: connect, move, drag-teach and replay one trajectory; pose estimation running on the webcam.
  - H6–24: camera-to-robot calibration; target-tracking score; adaptive speed loop.
  - H24–40: therapist UI (record, name, assign exercises), session report, voice prompts.
  - H40–48: three polished exercises, rehearsal, backup video.
- **3-minute demo script:** (1) "therapist" grabs the arm and teaches a shoulder-flexion arc in 20 s. (2) "patient" follows the target; live score on screen. (3) patient tires, arm slows and reduces range automatically. (4) show the weekly report a Leukerbad clinic therapist would see.
- **Risks and fallbacks:** camera calibration drift → score in image space only. Drag mode unavailable over the API on site firmware → teach via DobotStudio Pro and export points.
- **Judging angles:** innovation medium; technical depth in the adaptive loop; impact high (therapist time is the bottleneck); **Leukerbad:** direct fit with local rehabilitation clinics and spa guests doing post-surgery exercise.

### Concept 2 — Voice-driven bedside fetch and medication handover

- **Problem → value:** people with limited mobility ask caregivers for small things all day (glass, glasses, remote, pill box). A bedside arm hands over named objects and runs a medication schedule with confirmation logging.
- **Hardware:** Nova 5 or Nova 2 (E6 works for items under 750 g) + gripper + RGB-D or RGB camera + laptop with GPU. Optional: D-Robotics RDK X5 for on-device perception; a Unitree or Galaxea base to bring items from another room.
- **Architecture / stack:** speech-to-text → target phrase → open-vocabulary detection (Dobot's `voice_txt_command` shows Whisper + Grounding DINO + tracking) → table-plane grasp pose → `MovJ` / `MovL` pick → move to a fixed handover pose → release on a button, voice "got it", or a collision-level nudge. Scheduler triggers pill-box delivery; log each handover for the caregiver.
- **48-hour plan:**
  - H0–6: arm + gripper I/O working; pick from fixed positions; speech-to-text running.
  - H6–24: detection → hand-eye calibration → top-down grasps of 4–5 known objects.
  - H24–40: handover logic, medication scheduler, caregiver log page, error speech ("I can't see the cup").
  - H40–48: robustness tuning on the demo table, rehearsal.
- **3-minute demo script:** (1) "Bring me my glasses" → pick and handover. (2) 10:00 reminder fires → pill box delivered, user confirms, log updates. (3) ask for an object that is absent → clear spoken failure. (4) caregiver view on a phone.
- **Risks and fallbacks:** open-vocabulary detection too slow without a GPU → fiducial markers or a small fixed-class detector. Grasp failures → fixed object slots on a tray. Weak venue internet → keep all models local.
- **Judging angles:** innovation low–medium; technical depth medium; impact clear and easy to explain; **Leukerbad:** hotel and clinic rooms with elderly guests and thin night staffing.

### Concept 3 — Assisted feeding arm

- **Problem → value:** people with tremor or weak arms need a helper for every meal. A robot that scoops and presents food on request returns independence and frees caregiver time.
- **Hardware:** Nova 2 / Nova 5 or Magician E6 + spoon mount (3D-printed) + camera facing the user + bowl in a fixed holder.
- **Architecture / stack:** face and mouth-open detection on the laptop → fixed scoop motion (drag-taught) → `MovL` to a presentation pose that stops **10–15 cm short of the face**; the user leans in. Trigger by voice, mouth-open gesture or a large button. Speed capped; safe wall in front of the face plane. Optional bite-count log for nutrition tracking.
- **48-hour plan:**
  - H0–6: spoon mount, drag-teach scoop, replay reliably.
  - H6–24: face tracking → presentation pose follows head position within limits.
  - H24–40: triggers (voice, gesture, button), pause-on-turn-away, bite log.
  - H40–48: test with soft food and with a mannequin head; rehearse.
- **3-minute demo script:** (1) user says "next bite" → scoop → spoon waits in front of the mouth. (2) user turns to talk → arm holds back. (3) head moves → presentation pose adapts. (4) show the meal log.
- **Risks and fallbacks:** near-face motion is the main safety concern → mannequin for the live demo, human only on video. Scooping varies with food → use one food type. Spilling → presentation orientation locked level.
- **Judging angles:** innovation medium (known research problem, rarely built in 48 h); technical depth in the safety design; impact very tangible; **Leukerbad:** rehabilitation clinics with neurological and post-stroke patients.

### Concept 4 — Force-controlled physio assistant (needs CRAF; most ambitious)

- **Problem → value:** manual therapy and assisted stretching are physically tiring for therapists and hard to dose consistently. A therapist demonstrates a stroke or assisted movement; the robot reproduces it with a set contact force and backs off when the patient tenses.
- **Hardware:** **CR5AF** (flange 6-axis force sensor) + soft silicone end-effector + depth camera. Optional: OriginFlow EMG on the patient's forearm to modulate intensity; XREAL for the therapist's view. Without a CRAF, do not attempt contact — fall back to Concept 1.
- **Architecture / stack:** teach path by force-guided drag (<2 N start force) → depth camera re-registers the path on the limb → `EnableFTSensor`, `SixForceHome`, `FCForceMode` with `FCSetForce` and `FCSetForceLimit` along the tool axis while the path runs → monitor `GetForce`; EMG or a hand-held "stop" switch scales force down or retracts. Exact force-command semantics need a booth walkthrough ⚠️ unverified.
- **48-hour plan:**
  - H0–6: confirm CRAF and force API with Dobot engineers; constant-force press on a foam block.
  - H6–24: taught stroke on a mannequin arm at constant force; force logging and hard limits.
  - H24–40: depth-based path re-registration; EMG or switch-based intensity control; therapist UI for force presets.
  - H40–48: tests on a team member's forearm at low force, rehearsal, backup video.
- **3-minute demo script:** (1) therapist teaches a forearm stroke by hand. (2) robot repeats it at 5 N, live force plot. (3) patient tenses → force drops and arm retracts. (4) move the arm → path re-registers.
- **Risks and fallbacks:** no CRAF on site (likely) → partner with Flexiv or ROKAE force-controlled arms, or drop to Concept 1. Force loop unstable on soft tissue → lower stiffness, slower path, foam phantom for the live demo.
- **Judging angles:** innovation and technical depth highest; impact credible given thermal-spa and physiotherapy culture; **Leukerbad:** strongest local story (spa massage and rehab), also the highest safety scrutiny from judges.

**If an X-Trainer is on site:** consider a tele-care variant — a remote caregiver teleoperates two Nova 2 arms to help with a bimanual task (open a pill bottle, pour water), then train a policy from the recorded demos. Check the software stack with Dobot first; public documentation is thin.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Dobot arm + OriginFlow EMG | Muscle-activation feedback for rehab scoring or intensity control | Medium — depends on OriginFlow's streaming API |
| Dobot arm + XREAL AR glasses | AR overlay of the exercise path for the patient, or therapist view | Medium — separate app, loose coupling over network |
| Dobot arm + D-Robotics RDK X5 | On-device perception, no laptop at the bedside | Low–medium — Python TCP client runs anywhere |
| Dobot arm on Unitree Go2 / B2 or Galaxea base | Mobile fetch between rooms | High — mounting, power (Nova's 30–60 V DC helps), no ready integration |
| Dobot arm + WUJI Hand | Dexterous handover, opening containers | High — mechanical and control integration |
| Dobot (non-force) arm + Flexiv Rizon | Dobot does fetch / presentation, Flexiv does contact tasks | Medium — two independent cells, shared orchestrator |
| Dobot arm + Unitree / AGIBOT humanoid | Humanoid does rounds and fall checks, arm is the bedside station | High — only as a loosely coupled story |

## Questions to ask the Dobot Robotics engineers on site

1. Which arms are here, how many per team, and is controller firmware V4.4.0.0 or later?
2. Is a CRAF (force-sensor) arm available? If so, which `FC*` commands work and what are the force range and update rate?
3. What rate do `ServoJ` / `ServoP` accept, and does the 30004 feedback port expose joint currents or estimated external torque?
4. Does `StartDrag` work over TCP/IP on these units, and can we record a dragged trajectory from Python or only in DobotStudio Pro?
5. Which collision level number is the most sensitive, and what contact force does it correspond to on Nova 5?
6. Which grippers and cameras are available, and how are they wired (tool I/O, RS485)?
7. Does Dobot have a reference massage / physiotherapy application or integrator we can look at, and is any model certified as a medical device?
8. Is X-Trainer here, and which training pipeline (policy type, data format) does it ship with?

## Decision rule

- **Pick Dobot Robotics for T04 if** your idea is a fixed-base bedside or therapy-table task (exercise coaching, handover, feeding), you want a simple Python API and teach-by-demonstration, and a Nova 5 / CR5A / E6 is confirmed on site.
- **Avoid if** your idea needs mobility, patient lifting, or contact-force control and no CRAF is available — go to a force-controlled arm vendor (Flexiv, ROKAE) or a mobile manipulator instead.

## Sources
- [Dobot Robotics profile (this repo)](../Dobot.md)
- [Dobot Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html)
- [Dobot CRAF series](https://www.dobot-robots.com/products/cra-series/dobot-craf-series.html)
- [Dobot CRA series](https://www.dobot-robots.com/products/cra-series/dobot-cra-series.html)
- [Dobot Healthcare industry page](https://www.dobot-robots.com/industries/medical.html)
- [TCP-IP-Python-V4 (GitHub)](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- [dobot_api.py in TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4/blob/main/dobot_api.py)
- [DOBOT_6Axis_ROS2_V4 (GitHub)](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)
- [voice_txt_command (GitHub)](https://github.com/Dobot-Arm/voice_txt_command)
- [dobot_xtrainer (GitHub)](https://github.com/Dobot-Arm/dobot_xtrainer)
