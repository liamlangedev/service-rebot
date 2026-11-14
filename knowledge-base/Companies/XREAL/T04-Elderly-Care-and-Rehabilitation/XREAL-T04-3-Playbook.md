---
type: challenge-playbook
company: "XREAL"
slug: XREAL
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# XREAL × T04 — Hackathon Playbook

⬆ [XREAL profile](../XREAL.md) · [Brief](XREAL-T04-1-Brief.md) · [Products and solutions](XREAL-T04-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- XREAL is the **human interface**; the robot comes from another vendor. Start the robot work first, add glasses second.
- Check your hardware at H0: **One series + Eye = 6DoF head pose + RGB camera only** (no hands / planes / anchors). Hand tracking needs **Air 2 Ultra** or **AURA**.
- All concepts are hackathon prototypes, not medical devices. Test on team members, keep "patients" seated or spotted, manage the cable.

## Solution approaches

### Concept 1 — Therapist HUD for a robot-assisted exercise (safest)
- **Problem → value:** a physiotherapist guiding a robot-assisted exercise must watch the patient, not a monitor. A heads-up view of force, range and rep count keeps eyes and hands on the patient.
- **Hardware:** any One-series glasses (One Pro / 1S / 1 Pro+) plugged into a laptop over USB-C. Robot: a force-controlled arm (Flexiv Rizon or ROKAE xMate) holding a handle the "patient" pushes or pulls. Optional: OriginFlow EMG.
- **Architecture / stack:** arm force / position (vendor SDK) → small Python service computes reps, range of motion, peak force, asymmetry → web dashboard (large fonts, high contrast, dark background because black is transparent in optical see-through) → shown in the glasses as an external display; the glasses' own 3DoF mode pins the screen in space. **No XREAL SDK.** Compute on the laptop.
- **48-hour plan:**
  - H0–6: confirm glasses work as a display on your laptop port; get the arm streaming force / pose.
  - H6–24: compliant exercise mode on the arm (resistance level, safe limits); metrics service; first dashboard.
  - H24–40: HUD layout tuned for see-through; session report export; voice or foot-pedal control so hands stay free.
  - H40–48: rehearse with a volunteer; record a backup video through the glasses.
- **3-minute demo script:** (0:00) the therapist's problem; (0:30) volunteer does guided arm exercise, therapist wears glasses while the same HUD is mirrored on a big screen for judges; (1:30) raise resistance by voice, HUD flags asymmetry / fatigue; (2:15) auto-generated session report; (2:40) how it scales in a rehab clinic.
- **Risks and fallbacks:** laptop port lacks DisplayPort Alt Mode → use a phone / Beam Pro or another laptop. Judges cannot see inside glasses → always mirror. Arm safety → low force limits, emergency stop in hand.
- **Judging angles:** innovation — modest; technical depth — lives in the arm's force control; impact — real workflow pain for therapists; Leukerbad — rehabilitation clinics are the town's core business.

### Concept 2 — Captions and prompts for hard-of-hearing guests with a companion robot
- **Problem → value:** hearing loss makes care instructions and robot speech hard to follow. Glasses show live subtitles (optionally translated — spa guests speak German, French, English, Italian) plus simple prompts such as medication or exercise reminders, while a robot delivers the item or demonstrates the movement.
- **Hardware:** One-series glasses + Beam Pro or phone / laptop as host. Robot: a wheeled service robot or humanoid on site (UniX AI Wanda, AGIBOT, Unitree G1, Galaxea R1) for delivery or demonstration.
- **Architecture / stack:** microphone → open speech-to-text model on the laptop → optional translation → caption overlay rendered as a browser page → glasses as display. Robot task queue (reminder → fetch → hand over) publishes status lines into the same overlay. No XREAL SDK required; an existing third-party app (XRAI Glass) already proves captioning on XREAL glasses, but build your own overlay so robot events can be merged in.
- **48-hour plan:**
  - H0–6: speech-to-text running locally with acceptable delay; caption page readable in the glasses.
  - H6–24: robot delivery or demonstration behaviour (scripted is fine); event bus between robot and overlay.
  - H24–40: translation toggle, speaker labels ("Nurse", "Robot"), reminder schedule, large-text mode.
  - H40–48: noise test in the hall with a close-talk microphone; rehearse.
- **3-minute demo script:** (0:00) guest cannot follow the nurse; (0:30) glasses on, captions appear live, mirrored for judges; (1:10) switch to another language; (1:40) reminder fires, robot brings the pill box and its spoken message is captioned; (2:30) privacy and deployment notes.
- **Risks and fallbacks:** hall noise ruins transcription → lapel microphone, push-to-talk. Network down → keep the model local. Robot navigation fails → hand-over from a fixed position.
- **Judging angles:** innovation — merging robot state into an accessibility overlay; technical depth — moderate; impact — high and easy to understand; Leukerbad — multilingual elderly spa guests.

### Concept 3 — Head-pose rehab coach with a robot partner
- **Problem → value:** home or clinic exercises for neck mobility, balance and sit-to-stand are rarely measured. The glasses' 6DoF head pose measures them without extra sensors and shows targets in the room; a robot acts as demonstrator, spotter or resistance partner.
- **Hardware:** One Pro (or 1S ⚠️ check Eye support) + **XREAL Eye** + Beam Pro / Samsung S24–S25. Or Air 2 Ultra / AURA for richer tracking. Robot: Flexiv / ROKAE arm as a moving target or support handle, or a humanoid that mirrors the exercise.
- **Architecture / stack:** Unity app with XREAL SDK 3.1.0 → head pose at each frame → exercise logic in C# (neck rotation range, sway during standing, head-height curve for sit-to-stand counting) → world-placed visual targets and progress ring → pose and scores sent over UDP / WebSocket (or ROS-TCP-Connector) to the robot computer → robot adapts pace, position or resistance. Compute: Android host for AR, laptop for the robot.
- **48-hour plan:**
  - H0–6: build and deploy the SDK HelloMR sample; confirm 6DoF with Eye; log head pose to file.
  - H6–24: three exercises with scoring; pose stream to the robot; robot reacts to one signal (e.g. slows down when sway rises).
  - H24–40: calibration step, large simple UI, session summary; first-person recording for the demo.
  - H40–48: tracking robustness test in venue lighting; rehearse; backup video.
- **3-minute demo script:** (0:00) unmeasured exercises; (0:30) volunteer follows floating targets for neck rotation, live angle on the mirror screen; (1:15) sit-to-stand next to the robot arm offering a support handle, counter and sway score update; (2:00) robot eases the pace when sway rises; (2:30) therapist report and limits.
- **Risks and fallbacks:** exercise metrics from head pose are **your own design, not clinically validated** — say so. 6DoF drift or loss in a bright, crowded hall → fall back to 3DoF rotation-only exercises. Unity / Android build problems → fall back to Concept 1 display mode with a webcam pose estimator.
- **Judging angles:** innovation — glasses as both sensor and display; technical depth — AR app + robot loop; impact — measurable home rehab; Leukerbad — thermal-spa rehab and elderly guests.

### Concept 4 — Remote caregiver tele-assist through the glasses (most ambitious)
- **Problem → value:** relatives and nurses cannot be in every room. A remote caregiver sees the resident's home through a robot and performs simple fetch-and-hand-over tasks, or sees the resident's own view to coach them.
- **Hardware:** **Air 2 Ultra or AURA** (hand tracking) for the operator; if only One + Eye is available, use head pose for camera control plus a gamepad for the arms. Robot: wheeled dual-arm mobile manipulator (Galaxea R1, AGIBOT G1 / G2, Galbot G1, Spirit AI Moz1). Optional second pair of One + Eye on the resident for first-person streaming.
- **Architecture / stack:** robot head-camera video → operator glasses (video panel in Unity or plain display mode) · operator head pose → robot head / camera pan-tilt · hand joints (XR Hands) → wrist targets and gripper open / close via the robot vendor's teleop or inverse-kinematics API · speed and force limits enforced on the robot side. Resident view: SDK first-person streaming sample. Compute: Android host or AURA puck for the operator, robot computer for control.
- **48-hour plan:**
  - H0–6: confirm which glasses and which robot teleop interface exist; video from robot to glasses; head pose out of Unity.
  - H6–24: head-to-camera control; one arm following a hand or gamepad; gripper control.
  - H24–40: one full task (pick up a water bottle, hand it over); latency tuning; safety limits; optional resident-view stream.
  - H40–48: rehearse the task ten times; record the best run.
- **3-minute demo script:** (0:00) the staffing gap; (0:30) operator at one table puts on glasses and looks around through the robot; (1:10) picks up a bottle and hands it to the "resident"; (2:10) switch to the resident's first-person view for a coaching moment; (2:40) path to assisted autonomy using recorded demonstrations.
- **Risks and fallbacks:** highest integration load — two vendors, real-time loop. No hand-tracking glasses on site → gamepad arms. Latency or Wi-Fi problems → wired link, lower resolution. Robot teleop API closed → use the vendor's own teleop and keep the glasses for the view and head control only.
- **Judging angles:** innovation — light glasses instead of a VR headset for care tele-operation; technical depth — high; impact — remote care for alpine villages; Leukerbad — steep, snowbound access makes remote presence valuable.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| XREAL + Flexiv Rizon or ROKAE xMate | Therapist HUD over force-controlled exercise or massage data | **Low** (display mode) |
| XREAL + OriginFlow | EMG muscle-activation biofeedback in the wearer's view | **Low–medium** (depends on OriginFlow data output — ask) |
| XREAL + UniX AI Wanda / AGIBOT / Unitree humanoid | Captions, reminders and robot status for hard-of-hearing residents | **Low–medium** |
| XREAL (One + Eye) + any arm | Head-pose-measured exercises with a robot partner | **Medium** (Unity + pose bridge) |
| XREAL (Air 2 Ultra / AURA) + Galaxea R1 / AGIBOT G1 / Galbot G1 | Hand-tracked tele-assist for fetch and hand-over | **High** |
| XREAL + WUJI Hand | Hand-tracking-to-dexterous-hand mirroring for hand-rehab demos | **High** (needs hand-tracking glasses + retargeting) |
| XREAL + D-Robotics RDK | Edge board runs vision / speech, glasses show the result | **Medium** (board video output to USB-C needs an adapter ⚠️ check) |
| XREAL + SKYLANDX MetaCam | Pre-scanned room model for placing guidance content | **Medium–high** (alignment between scan and glasses is manual) |

## Questions to ask the XREAL engineers on site

1. Exactly which glasses, how many, and which hosts (Beam Pro, Samsung S24 / S25) are available to teams — any **Air 2 Ultra or AURA**?
2. Does XREAL Eye give 6DoF on **1S and 1 Pro+**, or only on One / One Pro?
3. Can the RGB camera and 6DoF tracking run at the same time on One + Eye, and at what resolution and frame rate?
4. Is there any hand-tracking path on One + Eye (beta firmware or SDK build), or is it strictly Air 2 Ultra / AURA?
5. How does the first-person-view streaming sample send video (protocol, receiver, typical latency), and can it reach a Linux robot computer?
6. Is there a way to get head pose on a **laptop** (Windows / Linux) without the Android host — for example over USB from the X1 chip?
7. Do you have prescription inserts or fit options on site for testers who wear glasses?
8. Do you know of any healthcare, accessibility or rehab pilots using XREAL glasses that we may cite?

## Decision rule

- **Pick XREAL for T04 if** your core robot build is already on another vendor and a hands-free view for the therapist, caregiver or patient makes the demo clearer — and you can live with display mode or head pose only.
- **Avoid if** you need the vendor to provide physical assistance, hand or body tracking on One-series hardware, ROS 2-native tooling, or you have no Unity / Android skills and want more than a screen.

## Sources
- [XREAL profile (general research)](../XREAL.md)
- [XREAL docs — device and feature compatibility](https://docs.xreal.com/XREALDevices/Compatibility)
- [XREAL docs — Sample Code (SDK 3.1.0)](https://docs.xreal.com/Sample%20Code)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XREAL docs — Frequently Asked Questions](https://docs.xreal.com/Frequently%20Asked%20Questions)
- [Android Developers — Develop with Unity for Android XR](https://developer.android.com/develop/xr/unity)
- [XRAI Glass — compatible AR glasses](https://xrai.glass/ar-glasses/)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/abs/2604.08534)
