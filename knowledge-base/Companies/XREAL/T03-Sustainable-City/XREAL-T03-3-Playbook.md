---
type: challenge-playbook
company: "XREAL"
slug: XREAL
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# XREAL × T03 — Hackathon Playbook

⬆ [XREAL profile](../XREAL.md) · [Brief](XREAL-T03-1-Brief.md) · [Products and solutions](XREAL-T03-2-Products-and-Solutions.md)

> **Read first:** XREAL is an add-on (fit **2/5**). Every concept below needs another vendor's robot as the core. The glasses must earn their place by making the human part of the loop faster, hands-free or more convincing on stage. Items marked ⚠️ are unverified and must be checked at the booth before you commit.

## Solution approaches

### Concept 1 — Sorting-cell HUD with human-in-the-loop labels (safest)

- **Problem → value:** robot waste sorters fail on unusual or dirty items; mis-sorts contaminate recycling streams. A hands-free operator resolves only the uncertain cases, and each correction becomes a labelled training sample → the cell improves while it runs.
- **Hardware:** any One-series glasses (One Pro / 1 Pro+ / 1S) as a **USB-C display** on the laptop. Robot: Dobot CR / Nova, Flexiv Rizon or ROKAE xMate arm with a camera over a mock conveyor / bin table. Optional D-Robotics RDK board for on-edge inference.
- **Architecture / stack:**
  - Perception: overhead camera → your detector / classifier (off-the-shelf open-vocabulary detector or a VLM call) on laptop or RDK.
  - Planning: confidence threshold → auto-sort, or queue for the human.
  - Control: the arm vendor's SDK for pick-and-place.
  - XREAL part: a full-screen web / Qt dashboard rendered on the laptop, shown in the glasses (no XREAL SDK). Confirm / override by voice, foot pedal or keyboard clicker.
  - Compute: laptop; glasses only display.
- **48-hour plan:**
  - H0–6: verify glasses work as a display on your laptop port; get the arm picking one object; choose 4 waste classes.
  - H6–24: detector + threshold logic; dashboard with item crop, top-2 classes, big confirm / swap prompt; log corrections.
  - H24–40: retrain or re-prompt with the logged corrections; measure accuracy before / after; tune HUD legibility.
  - H40–48: rehearse, record backup video, build one slide with the numbers.
- **3-minute demo script:** (0:00) mixed waste on the table, arm sorts the obvious items alone → (1:00) an odd item appears, HUD shows "PET 48% / Alu 41%", operator says "alu", arm sorts → (2:00) show the correction log and the before / after accuracy → (2:40) pass the glasses to a juror.
- **Risks and fallbacks:** laptop port without DisplayPort Alt Mode → use Beam Pro screen mirroring or a normal monitor. Jurors cannot see the HUD → mirror it on a screen.
- **Judging angles:** innovation low–medium; technical depth from the learning loop; impact = fewer contaminated streams; Leukerbad relevance = hotels and clinics produce mixed guest waste with seasonal staff who need help.

### Concept 2 — "Look-and-sort" wearable camera that directs a robot

- **Problem → value:** staff or guests hold an item and do not know the right stream (Swiss separate collection has many). The glasses recognise what the wearer is looking at, show the stream, and a mobile manipulator takes the item to the correct container — the human never walks to the recycling point.
- **Hardware:** **One Pro + XREAL Eye + Beam Pro**. Robot: Galaxea R1 Lite / Galbot G1 / UniX Wanda (mobile manipulator), or a fixed arm for a reduced version.
- **Architecture / stack:**
  - Perception: Unity app on Beam Pro reads Eye RGB frames (`RGBCamera` sample, YUV_420_888) → JPEG over Wi-Fi to a laptop → VLM / classifier returns stream + confidence.
  - Planning: laptop maps stream → target bin pose; sends a fetch-and-drop task to the robot.
  - Control: robot vendor stack for navigation and grasp.
  - XREAL part: head-locked label + coloured bin icon; optional spatial anchor on each bin so an arrow points to it.
  - Compute: Beam Pro (UI, frame grab), laptop (models), robot computer (motion).
- **48-hour plan:**
  - H0–6: **gate** — build and run `HelloMR` and `RGBCamera` on the provided host; if this is not working by H6, drop to Concept 1.
  - H6–24: frame upload + classification round trip (target < 2 s); robot handover pose and one drop-off.
  - H24–40: overlay polish, 5–6 item types, anchors on bins, error states.
  - H40–48: rehearse with fixed lighting; backup video.
- **3-minute demo script:** (0:00) wearer picks up a coffee capsule, label appears "Aluminium → bin 3" → (0:45) robot arrives, takes it, drops it → (1:45) repeat with a tricky item (composite packaging) and show the model's explanation → (2:30) tally of items diverted.
- **Risks and fallbacks:** Eye frame latency / resolution unknown ⚠️ → fall back to the Beam Pro's own camera or a clip-on USB webcam. Unity Android build problems → use the FPV streaming sample or a phone app. Robot grasp unreliable → hand the item into a tray on the robot.
- **Judging angles:** innovation medium (wearable perception + robot logistics); depth in the cross-device pipeline; impact = higher sorting quality without training people; Leukerbad relevance = multilingual tourists and spa guests.

### Concept 3 — Energy X-ray: robot-collected building data pinned in AR

- **Problem → value:** heat loss, over-heated rooms and stale air are invisible; audits are slow and end up in PDFs nobody reads. A robot patrols and logs temperature / CO2 / humidity (and optionally thermal images); the facility manager walks the building and sees the readings **anchored where they were measured**, with the worst spots highlighted.
- **Hardware:** **One Pro + Eye + Beam Pro** (6DoF + spatial anchors), or AURA / Air 2 Ultra if available. Robot: Unitree Go2 or a wheeled base carrying a sensor pack on a D-Robotics RDK X5. Optional SKYLANDX MetaCam for a 3D scan of the space.
- **Architecture / stack:**
  - Perception: robot SLAM pose + sensor samples → time-stamped (x, y, z, value) points.
  - Planning: simple waypoint patrol; anomaly scoring (e.g. deviation from set-point, CO2 above threshold).
  - Control: robot vendor navigation.
  - Registration: one printed marker at a known robot-map pose; XREAL image tracking gives the glasses-to-map transform (limit: 1 tracked image at a time).
  - XREAL part: Unity scene with persistent anchors, colour-coded spheres / heat ribbons, a "top 3 actions" panel.
  - Compute: robot / RDK (logging), laptop (aggregation + REST endpoint), Beam Pro (rendering).
- **48-hour plan:**
  - H0–6: sensor pack logging to CSV; `Anchors` + `BasicImageTracking` samples running on the glasses.
  - H6–24: robot patrol of one corridor + two rooms; marker-based registration; first points visible in AR.
  - H24–40: anomaly scoring, estimated savings per fix (state your assumptions), UI polish.
  - H40–48: create a visible anomaly for the demo (open window, space heater); rehearse.
- **3-minute demo script:** (0:00) robot finishes a patrol lap → (0:40) wearer looks at the marker, the room fills with data points → (1:20) walk to the red cluster by the window, panel shows the reading and suggested action → (2:10) close the window, robot re-measures, point turns green → (2:40) summary slide.
- **Risks and fallbacks:** registration drift → keep the demo area small and re-scan the marker. 6DoF on the available model not working → show the same data as a head-locked mini-map (3DoF) or on a tablet. No thermal camera → temperature / CO2 points are enough.
- **Judging angles:** innovation medium–high (robot as mobile sensor, AR as the report); depth in multi-frame registration; impact = actionable energy savings; Leukerbad relevance = heating-intensive alpine hotels, clinics and thermal-bath buildings (inference from the venue, not a cited figure).

### Concept 4 — Teach-by-showing for repair and disassembly (most ambitious)

- **Problem → value:** reuse and repair need dexterous disassembly that is uneconomic to program per product. A technician wearing glasses demonstrates opening a device once; head pose, egocentric video and (if available) hand joints are recorded, and a robot arm replays or learns the task — the pattern used in the ActiveGlasses research with Air 2 Ultra.
- **Hardware:** Air 2 Ultra or **AURA** (hand tracking), else One Pro + Eye (hand tracking ⚠️ unverified) with a separate camera. Robot: Flexiv Rizon (force control for unscrewing / prying) or ROKAE 7-DoF xMate; optional WUJI Hand; optional OriginFlow EMG capture for grip intent.
- **Architecture / stack:**
  - Perception: glasses 6DoF head pose + 26-joint hand pose (XR Hands) streamed via UDP / WebSocket to a laptop; RGB from Eye or an external camera.
  - Planning: retarget wrist trajectory + grip events to the arm frame; start with direct replay, attempt a small imitation policy only if time allows.
  - Control: arm vendor Cartesian / impedance interface.
  - XREAL part: recording UI, live "ghost" of the planned robot path over the workpiece, step checklist.
  - Compute: laptop (retargeting, training), Beam Pro or AURA puck (capture).
- **48-hour plan:**
  - H0–6: **gate** — confirm which device gives hand joints and at what rate; stream poses to the laptop.
  - H6–24: calibration glasses ↔ robot base (marker); replay one demonstrated motion in free space.
  - H24–40: one real task (e.g. remove a battery cover with two screws pre-loosened); ghost-path overlay.
  - H40–48: narrow to the most reliable step; rehearse; backup video.
- **3-minute demo script:** (0:00) technician demonstrates the step on device A → (1:00) overlay shows the captured path, operator approves → (1:30) robot repeats it on device B → (2:30) show recovered parts sorted for reuse and the time per unit.
- **Risks and fallbacks:** hand tracking unavailable or noisy → use the phone-as-3DoF-controller or a tracked tool with a marker. Policy learning does not converge → present direct replay honestly. Contact-rich steps fail → pre-loosen fasteners.
- **Judging angles:** innovation high; technical depth high (calibration, retargeting, force control); impact = scalable circular-economy labour; Leukerbad relevance moderate (local repair of rental ski / e-bike / clinic equipment as a story).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| XREAL (display only) + Dobot / ROKAE arm | Concept 1 sorting HUD | **Low** — no XREAL SDK |
| XREAL One Pro + Eye + Galaxea / Galbot / UniX mobile manipulator | Concept 2 look-and-sort with robot delivery | Medium — Unity app + HTTP bridge + robot task API |
| XREAL + Unitree Go2 + D-Robotics RDK X5 | Concept 3 sensor patrol with AR report | Medium — marker registration between robot map and glasses |
| XREAL + SKYLANDX MetaCam | Pre-scanned 3D model to align overlays or show a mini digital twin | Medium — export / alignment of the scan |
| XREAL (Air 2 Ultra / AURA) + Flexiv Rizon (+ WUJI Hand) | Concept 4 demonstration capture and replay | **High** — calibration, retargeting, safety |
| XREAL + OriginFlow | Egocentric video + EMG as a richer demonstration dataset | High — two capture stacks to synchronise |
| XREAL + Binabik AI / coprod | Glasses as the operator front-end of their agent / modular stack | Unknown — ask both teams |

## Questions to ask the XREAL engineers on site

1. Exactly which glasses, how many, and which hosts (Beam Pro, Samsung S24 / S25) are available to teams — and are any AURA units here?
2. On One series + XREAL Eye: is **hand tracking** supported, or only 6DoF? Does Eye + 6DoF also work on 1 Pro+ and 1S?
3. What resolution, frame rate and latency do Eye RGB frames have through the SDK, and can 6DoF tracking and RGB capture run at the same time?
4. Is the **UVC mode** from the docs FAQ usable to read the Eye camera directly on a Linux laptop or a Jetson / RDK board (no Unity)?
5. Is there any way to get head pose on a PC / Linux host without an Android device?
6. On AURA: can a third-party app access camera frames, and can it call Gemini with them, or is that system-only?
7. Do you have a ready Unity project (anchors + RGB camera + networking) or a ROS 2 / WebSocket bridge example we can start from?
8. Are the provided hosts on Android 15 or older (docs warn against Android 16), and are the glasses already on the firmware needed for 6DoF?

## Decision rule

- **Pick XREAL for T03 if** your core robot is from another vendor, your story has a human operator, teacher or auditor in the loop, and one teammate can own Unity / Android — or you only need a no-code HUD.
- **Avoid if** you want a single-vendor build, an autonomous outdoor system, or nobody on the team has shipped a Unity Android build before (then use the glasses purely as a display, or not at all).

## Sources
- [XREAL company profile (this repo)](../XREAL.md)
- [XREAL developer docs — SDK overview (3.1.0)](https://docs.xreal.com/)
- [XREAL SDK 3.1.0 release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.1.0)
- [XREAL docs — Getting Started with XREAL SDK](https://docs.xreal.com/Getting%20Started%20with%20XREAL%20SDK)
- [XREAL docs — Sample Code](https://docs.xreal.com/Sample%20Code)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XREAL docs — Image Tracking](https://docs.xreal.com/Image%20Tracking/intro)
- [XREAL docs — Frequently Asked Questions](https://docs.xreal.com/Frequently%20Asked%20Questions)
- [GitHub — nreal-ai organisation](https://github.com/nreal-ai)
- [Android Developers — Develop with Unity for Android XR](https://developer.android.com/develop/xr/unity)
- [GitHub — Unity-Technologies/ROS-TCP-Connector](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/pdf/2604.08534) (via profile)
