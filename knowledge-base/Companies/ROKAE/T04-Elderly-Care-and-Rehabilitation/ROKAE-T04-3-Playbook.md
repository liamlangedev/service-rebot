---
type: challenge-playbook
company: "ROKAE Robotics"
slug: ROKAE
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# ROKAE Robotics × T04 — Hackathon Playbook

⬆ [ROKAE Robotics profile](../ROKAE.md) · [Brief](ROKAE-T04-1-Brief.md) · [Products and solutions](ROKAE-T04-2-Products-and-Solutions.md)

**Before anything else (first 30 minutes):** confirm which ROKAE arm your team can use, its xCore version (SDK needs **v3.2.1+**), whether a tool flange adapter or gripper is supplied, and where the e-stop is.

**Safety rules for every concept below:** research prototype, not a medical device · demo on a phantom, mannequin or a healthy volunteer's forearm — never neck, head or spine · low stiffness, capped speed and force · one team member holds the e-stop whenever a person is in reach.

## Solution approaches

### Concept 1 — Assist-as-needed rehab exercise arm (safest)

- **Problem → value:** Upper-limb rehab after stroke, fracture or shoulder surgery needs hundreds of guided repetitions; therapists are scarce. A compliant arm lets one therapist set up an exercise once and the patient repeat it with measured assistance or resistance.
- **Hardware:** xMate SR3 / SR5 (or AR5) clamped to a table, 3D-printed handle on the flange, laptop. Optional: OriginFlow EMG band for effort, XREAL glasses or a tablet for the patient view.
- **Architecture / stack:**
  - *Perception:* robot's own joint and flange state (position, force) — no camera needed for the core loop. Optional webcam + MediaPipe pose for compensation detection (shoulder shrug, trunk lean).
  - *Planning:* therapist records the exercise by **drag teaching**; store the path; per repetition compute lag behind the path and adapt assistance.
  - *Control:* non-real-time path playback plus force-control commands for the first version; upgrade to **real-time Cartesian impedance** (stiffness scheduled along the path, range 0–3000 N/m on SR) if the real-time kernel is ready.
  - *Compute:* laptop, Ubuntu 22.04, xCoreSDK C++ or Python; simple web dashboard (range of motion, repetitions, peak force, session trend).
- **48-hour plan:**
  - *H0–6:* connect SDK, read state, jog, record and replay a dragged path. Print the handle.
  - *H6–24:* compliance along the path, three modes (passive guide / assist / resist), per-repetition metrics, speed and force caps, soft workspace limits.
  - *H24–40:* dashboard, therapist "prescription" screen, optional EMG or pose module, optional LLM session summary for the therapist.
  - *H40–48:* rehearse with three different users, record a backup video, freeze the code.
- **3-minute demo script:** (0:00) one line on the therapist shortage in rehab resorts → (0:30) "therapist" drags the arm through a shoulder-flexion arc, 10 seconds → (1:00) "patient" holds the handle, arm guides gently; patient goes limp and assistance rises; patient pushes and the arm yields → (2:00) dashboard shows range of motion and effort per repetition, plus a generated session note → (2:30) someone pushes the arm off-path to show it stays soft; close with clinic rollout story.
- **Risks and fallbacks:** real-time kernel not ready → stay on non-real-time force commands and drag/playback (still a full demo). No SDK access to force readings → estimate effort from path lag. No arm time → develop against the Gazebo model from rokae_ros2.
- **Judging angles:** *Innovation* — therapist-programmable by demonstration, no code. *Technical depth* — variable impedance, quantified outcomes. *Impact* — multiplies one therapist across several patients. *Leukerbad* — rehab clinics and elderly spa guests are the village's core business.

### Concept 2 — Force-limited massage / physio stroke with body tracking

- **Problem → value:** Massage and manual therapy are labour-intensive and physically hard on therapists. A robot that applies a repeatable, pressure-limited stroke can take over routine warm-up or relaxation passes.
- **Hardware:** SR5 or CR7 (reach), soft silicone roller or ball tool, depth camera (RealSense-class) on a tripod, massage phantom or volunteer forearm / calf. Optional: D-Robotics RDK X5 for on-edge pose estimation.
- **Architecture / stack:**
  - *Perception:* depth camera → body-segment point cloud → surface normals along a chosen muscle line; hand-eye calibration once.
  - *Planning:* generate a surface-following stroke; pressure level chosen by the user (voice or tablet), hard-capped in code.
  - *Control:* hybrid — position along the surface, **constant force along the normal** (force-control commands or Cartesian impedance with a force offset). Stop instantly on force spike or motion of the limb.
  - *Compute:* laptop with GPU for perception; SDK over Ethernet. MoveIt 2 (ROS 2 Humble) for approach and retreat.
- **48-hour plan:**
  - *H0–6:* SDK up, tool mounted, constant-force press on a foam block working.
  - *H6–24:* camera calibration, surface path from point cloud, stroke on phantom, safety monitors.
  - *H24–40:* pressure levels, voice or tablet control, "too much" stop word, limb-moved re-planning.
  - *H40–48:* tune, rehearse, backup video.
- **3-minute demo script:** problem (0:30) → camera scans forearm, path is drawn on screen (0:45) → robot performs three strokes at "light", then "medium"; live force plot stays inside the band (1:15) → volunteer moves the arm, robot lifts and re-plans (0:30) → business case for spas and clinics.
- **Risks and fallbacks:** calibration eats time → skip vision and drag-teach the stroke on the phantom, keep force control. Unstable contact → lower stiffness, slower stroke, softer tool. Judges worried about safety → run on phantom only and show the force log.
- **Judging angles:** *Innovation* — moderate (ROKAE already lists an AI massage robot application; your edge is perception plus safety logic). *Technical depth* — hybrid force/position on a deformable, moving surface. *Impact* — therapist workload. *Leukerbad* — a thermal-spa resort is the textbook customer.

### Concept 3 — Tele-care touch: remote therapist's hands in a mountain village

- **Problem → value:** Specialists are hours away from alpine villages, and elderly patients travel badly in winter. A force-reflecting remote arm lets a physiotherapist or doctor examine, palpate or guide a movement from elsewhere.
- **Hardware:** SR5 or AR5 as the patient-side arm; operator side = a second ROKAE arm in drag mode (if two are available) or a 6-DoF input (SpaceMouse, VR / XREAL controller, phone IMU). Camera at the patient side. Optional: OriginFlow EMG to map operator grip to contact pressure.
- **Architecture / stack:**
  - *Perception:* patient-side video stream plus flange force stream to the operator.
  - *Planning:* none — direct teleoperation with workspace clamp, velocity scaling and force ceiling.
  - *Control:* real-time **Cartesian impedance** following the operator pose at low stiffness, so contact force stays bounded even if the operator overshoots. Force is shown to the operator as a visual bar, sound, or (two-arm setup) reflected through the leader arm.
  - *Compute:* two laptops linked over the venue network (WebRTC video, small UDP or WebSocket control channel); real-time loop stays local to the patient-side PC.
- **48-hour plan:**
  - *H0–6:* SDK up on patient arm, pose streaming from the input device, clamp limits.
  - *H6–24:* stable impedance following, force display, video link, latency measurement.
  - *H24–40:* watchdog (freeze softly on link loss), session recording, optional AR overlay in XREAL glasses, optional second arm as leader.
  - *H40–48:* run across two rooms, rehearse, backup video.
- **3-minute demo script:** map showing Leukerbad to the nearest hospital (0:20) → "therapist" in another room sees video and force bar, guides the arm to palpate a phantom knee and to lead a patient's hand through a movement (1:30) → pull the network cable: arm goes soft and holds (0:30) → roadmap: tele-ultrasound, which ROKAE arms already do in integrator projects (0:40).
- **Risks and fallbacks:** real-time kernel needed for good feel → fall back to low-rate non-real-time pose targets at reduced speed. Network jitter → same-room demo with an artificial screen wall. Only one arm → SpaceMouse or phone as input.
- **Judging angles:** *Innovation* — bilateral feel with safety by compliance. *Technical depth* — real-time control plus networking and failure handling. *Impact* — access to care in remote regions. *Leukerbad* — one road in, winter closures, elderly guests.

### Concept 4 — Mobile care assistant with compliant handover (most ambitious)

- **Problem → value:** Caregivers spend much of a shift fetching and carrying. A mobile manipulator that brings water, medication boxes or a walking aid and hands them over gently frees time for actual care.
- **Hardware:** Helios if on site; otherwise a ROKAE AR5 / SR3 mounted on or parked beside another vendor's mobile base (Unitree, AGIBOT, Galaxea — check payload and 48 V power). Gripper or WUJI hand, RGB-D camera, Jetson or laptop. Optional: SKYLANDX scan for the room map.
- **Architecture / stack:**
  - *Perception:* open-vocabulary detector for the object and the person's hand; speech-to-text for requests.
  - *Planning:* LLM task planner calling a small skill library (navigate, pick, approach person, handover); MoveIt 2 for arm motion.
  - *Control:* position control for pick; **impedance mode for the handover** — release when the person pulls (force threshold), yield if bumped.
  - *Compute:* Jetson AGX Orin on Helios or a laptop; models local or cloud depending on venue network.
- **48-hour plan:**
  - *H0–6:* confirm platform, power and mounting; SDK and base both drivable from one PC.
  - *H6–24:* pick from a fixed shelf, navigate between two waypoints, force-triggered release.
  - *H24–40:* voice request, person and hand detection, medication-reminder scenario, error recovery.
  - *H40–48:* cut scope to what works three times in a row; backup video.
- **3-minute demo script:** "Bring my pills" (0:15) → robot drives to shelf, picks box (1:00) → approaches seated person at low speed, offers the box, releases on a gentle pull (0:45) → person bumps the arm, it yields (0:20) → caregiver time-saved claim and next steps (0:40).
- **Risks and fallbacks:** highest integration risk (two vendors, power, mounting, calibration). Fallback 1: static arm at a "care station" doing pick and compliant handover only. Fallback 2: base delivers, human loads. Helios weight (160 kg) near people → low speed and a marked keep-out zone.
- **Judging angles:** *Innovation* — force-aware handover in an LLM-planned task. *Technical depth* — full perception-to-control chain. *Impact* — caregiver relief. *Leukerbad* — clinics, hotels and care residences with staff shortages.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| ROKAE arm + **OriginFlow** EMG | Measure patient effort or intent; adapt assistance; show muscle activation next to robot force | Low–medium (independent data stream, fuse on the laptop) |
| ROKAE arm + **XREAL** glasses | AR exercise guidance for the patient or remote view for the therapist | Medium (separate Android XR app, share state over WebSocket) |
| ROKAE arm + **D-Robotics** RDK X5 / S100 | Pose estimation and body tracking at the edge, no GPU laptop needed | Low–medium (ROS 2 on both sides; check Humble compatibility) |
| ROKAE arm + **WUJI** Hand | Dexterous grasp and gentle handover of small objects (pill box, cup) | Medium–high (flange adapter, power, second SDK) |
| ROKAE arm + **Unitree / AGIBOT / Galaxea** mobile base | Mobile fetch-and-carry when no Helios is available | High (mounting, 48 V supply, calibration) |
| ROKAE arm + **SKYLANDX** MetaCam | Fast 3D map of the room or care station for planning | Medium (offline scan, export to planner) |
| ROKAE arm + **Binabik AI** / **Spirit AI** / **Galbot** models | Agent or VLA layer on top of a force-controlled arm | High and ⚠️ unverified — depends on whether their stack supports third-party arms |
| ROKAE HSA joints + **Leadshine** / **coprod** parts | Custom rehab device (for example a one-joint elbow trainer) | High — not advised for 48 hours |

## Questions to ask the ROKAE Robotics engineers on site

1. Which arms are here (SR3 / SR5 / CR / AR5), how many, and what xCore version do they run (SDK needs v3.2.1+)?
2. Is real-time mode (1 kHz joint / Cartesian impedance, direct torque) licensed and enabled on these units, and does the **Python** SDK expose it or only C++?
3. Do you have a PC with a real-time kernel already set up that we can borrow, or an image we can flash?
4. How do we read external force / joint torque estimates from the SDK, and at what rate?
5. What are the software limits we can set for human contact — maximum TCP speed, force, power, collision-detection sensitivity — and do they hold in real-time mode?
6. What changes for AR arms (SDK 0.7.x-AR): stiffness range, redundancy / elbow control, dual-arm coordination?
7. Is a gripper, flange adapter or force-controlled tool supplied, and is tool-payload identification automatic?
8. Can you share details of the AI massage or remote-ultrasound integrations (control mode used, force levels, safety concept) and whether ROKAE has any rehab or nursing project in progress?

## Decision rule

- **Pick ROKAE Robotics for T04 if** your idea is a contact-rich arm task (rehab exercise, massage / physio, tele-examination, compliant handover), an SR / CR / AR arm is confirmed on site, and someone on the team is comfortable with Linux and C++ or Python.
- **Avoid if** you need mobility, fall detection, companionship or a ready-made VLA / agent stack, if no ROKAE arm is free for your team, or if nobody can own the safety limits for human contact.

## Sources
- [ROKAE Robotics company profile (internal)](../ROKAE.md)
- [ROKAE — SR cobots](https://www.rokae.com/en/product/show/349/SR-Cobots.html)
- [ROKAE — Humanoid Force-Controlled Arm AR](https://www.rokae.com/en/product/show/595/Humanoid-Force-Controlled-Arm-AR.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html) (specs via company profile)
- [ROKAE — Healthcare case index](https://www.rokae.com/en/case/206/Healthcare.html)
- [ROKAE docs — xCore SDK introduction](https://docs.rokae.com/en/docs/SDK/SDK_Intro)
- [ROKAE docs — SDK index](https://docs.rokae.com/en/docs/SDK)
- [GitHub — ROKAE Robotics org](https://github.com/RokaeRobot)
- [GitHub — xCoreSDK-CPP](https://github.com/RokaeRobot/xCoreSDK-CPP)
- [GitHub — xCoreSDK-Python](https://github.com/RokaeRobot/xCoreSDK-Python)
- [GitHub — rokae_ros2](https://github.com/RokaeRobot/rokae_ros2)
