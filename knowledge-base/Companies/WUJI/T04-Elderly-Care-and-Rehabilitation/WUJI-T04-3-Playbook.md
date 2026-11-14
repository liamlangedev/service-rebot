---
type: challenge-playbook
company: "WUJI"
slug: WUJI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# WUJI × T04 — Hackathon Playbook

⬆ [WUJI profile](../WUJI.md) · [Brief](WUJI-T04-1-Brief.md) · [Products and solutions](WUJI-T04-2-Products-and-Solutions.md)

**Read first:** WUJI brings hands and a glove, not a robot. Concepts 1 and 2 need **no partner arm**; 3 and 4 do. Nothing here is a medical device — present every demo as a prototype tested on team members, not patients.

| # | Concept | WUJI hardware | Partner robot needed | Risk |
|---|---|---|---|---|
| 1 | GripCheck — glove hand-function check and exercise game | Glove | No | Low |
| 2 | Mirror Hand — robot hand as exercise partner / tele-therapist | Glove + Hand on a stand | No | Low–medium |
| 3 | Helping Hand — tele-operated dexterous daily-living tasks | Glove + Hand | Yes (arm) | Medium–high |
| 4 | Learned daily-living skill from glove demonstrations | Glove + Hand | Yes (arm) + GPU | High |

## Solution approaches

### Concept 1 — GripCheck: glove-based hand-function check and exercise coach

- **Problem → value:** Hand therapy after stroke, fracture or arthritis relies on short clinic sessions and subjective scoring; home exercise is unmonitored. A glove that scores grip pattern and finger mobility gives patient and therapist an objective trend line.
- **Hardware:** Wuji Glove + laptop with Ethernet. Optional: XREAL glasses as a hands-free display; D-Robotics RDK as a standalone host (SDK supports Linux arm64 — ⚠️ untested on RDK).
- **Architecture / stack:**
  - Perception: `tactile_zones()` (per-finger and palm pressure, 120 FPS), `hand_joint_angles()` / `hand_skeleton()` (120 Hz), IMU (800 Hz).
  - Features: per-finger peak and mean pressure (normalized), left / right or finger-to-finger balance, range of motion per joint, open / close time, tremor band power from the IMU.
  - Logic: 3–4 standard-style tasks (full fist, finger opposition, cylinder grasp, pinch) → score against the user's own baseline → adaptive exercise game (squeeze / stretch to steer).
  - Output: web dashboard (FastAPI + browser) and a one-page session summary; an LLM can phrase the summary but must not diagnose.
  - Compute: laptop only.
- **48-hour plan:**
  - H0–6: book a glove; `wuji doctor`, calibration, stream all channels; log to file. Build pose features on webcam + MediaPipe in parallel (same 21-keypoint format).
  - H6–24: feature extraction, baseline + scoring, one game, dashboard.
  - H24–40: test on 5+ people (include older volunteers if available and willing), tune thresholds, session report, trend view.
  - H40–48: polish, record backup video, rehearse.
- **3-minute demo script:** (0:00) the problem in one sentence with a Leukerbad rehab-clinic framing → (0:30) volunteer puts glove on, live pressure map and skeleton → (1:15) runs two test tasks, score appears vs baseline → (2:00) 30-second game → (2:30) therapist report and week-over-week trend (pre-recorded data) → (2:50) limits and next step.
- **Risks and fallbacks:** glove unavailable or does not fit → webcam + MediaPipe for pose, drop pressure. Normalized pressure only → present relative scores, never newtons. EMF glitches near metal → clear the table, remove rings.
- **Judging angles:** impact and Leukerbad relevance are strong (rehab clinics, older guests); technical depth is moderate — raise it with validated features and a clean longitudinal data model; innovation is moderate (data gloves for rehab exist; the dense palm pressure map is the differentiator).

### Concept 2 — Mirror Hand: robot hand as exercise partner and tele-therapist

- **Problem → value:** Therapists cannot be in every room or every valley. A robot hand on the patient's table physically shows the exercise (driven live by a remote therapist's glove, or replayed), while the patient's own movement is scored. Variant: the healthy hand drives a mirrored robot hand as a 3D take on mirror therapy (an established stroke-rehab technique; the robot variant is a hypothesis, not evidence).
- **Hardware:** Wuji Glove + one Wuji Hand (gen 1 or Hand 2) on a desk stand. Patient side: webcam or a second glove. Optional: XREAL for the patient view.
- **Architecture / stack:**
  - Therapist glove `hand_skeleton()` → `RetargetSession` → hand joint targets (start from the official `1.teleop_real.py`).
  - Mirroring: flip handedness / mirror keypoints before retargeting.
  - Record exercises (joint trajectories) and replay them at reduced speed; Hand 2 in MIT mode with low kp and a low `effort_limit` so it stays soft.
  - Patient tracking: webcam + MediaPipe → compare joint-angle trajectories with the demonstrated exercise (DTW or simple per-joint error) → feedback.
  - Remote link: send the 21 keypoints over WebSocket / WebRTC data channel; compute on two laptops.
- **48-hour plan:**
  - H0–6: run glove → hand teleop from the official example; confirm which hand generation you get.
  - H6–24: record / replay library of 5 exercises; mirroring; patient-side tracking and similarity score.
  - H24–40: remote link between two laptops, latency check, soft-gain tuning, UI.
  - H40–48: polish, backup video, rehearse.
- **3-minute demo script:** (0:00) "one therapist, many patients, steep valley" → (0:30) therapist across the room moves gloved hand, robot hand follows → (1:10) patient copies, live similarity score → (1:50) therapist leaves, robot replays the prescribed set, patient continues → (2:30) mirror-mode in 15 seconds → (2:45) limits.
- **Risks and fallbacks:** no hand available → render the hand in MuJoCo from `wuji-description` (works fully in simulation). Retargeting artefacts on thumb → restrict to exercises that look right. Hand overheating on long runs → short sets, pauses.
- **Judging angles:** innovation is higher than Concept 1 (physical demonstration + tele-care); technical depth from retargeting, compliant control and trajectory comparison; impact story is tele-rehab for mountain regions.

### Concept 3 — Helping Hand: tele-operated dexterous assistance for daily living

- **Problem → value:** Many daily tasks that defeat weak or arthritic hands are dexterity tasks: bottle caps, pill organisers, blister packs, zips. A remote caregiver wearing a glove operates a robot hand to do them — one caregiver can serve several residents without travelling.
- **Hardware:** Wuji Glove + Wuji Hand on a partner arm — Flexiv Rizon or ROKAE xMate (force-controlled, good near people), or Dobot CR / Nova. Check flange adapter, payload (Hand 2 is 800 g with cables) and 12 V / 20 A power routing. Camera for the operator view.
- **Architecture / stack:**
  - Fingers: glove → `RetargetSession` → hand (1000 Hz joint interface).
  - Arm: keep it simple — hand-guide and store 4–6 poses (above pill box, above bottle, handover zone) and let the operator switch between them, with small jog offsets. Full wrist-pose teleop needs an external tracker (the archived `wuji-hand-teleop` used Vive Tracker / PICO 4) and is a time sink.
  - Safety: arm in low-speed collaborative mode with force limits; handover only by placing objects on a tray, not hand-to-hand.
  - Compute: one laptop (WUJI SDK) + arm controller; ROS 2 optional (`wuji-ros2` targets ROS 2 Lyrical — check before committing).
- **48-hour plan:**
  - H0–6: secure arm + hand + adapter; mount; move both from one script.
  - H6–24: finger teleop on the arm, taught arm poses, operator camera view; pick two tasks that work (for example open a flip-top pill box, lift a cup).
  - H24–40: reliability runs (target 8 / 10), operator UI, e-stop routine, optional remote link.
  - H40–48: polish, backup video, rehearse.
- **3-minute demo script:** (0:00) resident cannot open the pill organiser → (0:30) caregiver "at another site" puts on the glove → (0:50) arm moves to the box, fingers open the lid and pick the day's compartment → (1:50) arm places it on the tray, resident takes it → (2:20) second task or log of "medication given" → (2:45) path to autonomy (Concept 4).
- **Risks and fallbacks:** no adapter or no arm slot → fall back to Concept 2 on a stand. No tactile on the robot hand and no force estimate from current → choose rigid, light, cheap objects; avoid anything fragile (the user notice says so). Hand 2 beta faults → use gen 1 (position control, 15 N fingertip).
- **Judging angles:** strongest "robot helps a person" visual; technical depth from multi-vendor integration; impact is caregiver relief; be ready for the question "why a 20-DoF hand instead of a gripper" — answer with the cap / lid / blister tasks.

### Concept 4 — Learned daily-living skill from glove demonstrations

- **Problem → value:** Tele-operation does not scale; show that the same rig can learn one daily-living task from a few dozen demonstrations and then run it on request.
- **Hardware:** Concept 3 rig + wrist / scene cameras + a GPU machine (on-site workstation or cloud).
- **Architecture / stack:** collect 50–100 demonstrations with the Concept 3 teleop (record hand joint states with `TopicRecorder` to MCAP, plus arm states and camera frames with your own logger, synchronised on timestamps) → train a small imitation policy (ACT or diffusion policy), or fine-tune pi0 / pi0.5 with `wuji-openpi` if GPU time allows → run with a voice or button trigger and a tele-op takeover fallback.
- **48-hour plan:**
  - H0–6 and H6–24: as Concept 3, but lock the task and camera setup by H12 and start collecting by H18.
  - H24–40: train, evaluate, collect more where it fails; keep teleop demo working in parallel.
  - H40–48: decide honestly: autonomous run if ≥ 60% success, otherwise show teleop + learned sub-skill.
- **3-minute demo script:** Concept 3 story, then "now without the caregiver": press the button, policy runs; show success rate and one failure honestly; takeover by glove.
- **Risks and fallbacks:** highest risk — data pipeline and training time usually overrun 48 hours; no WUJI checkpoints exist to start from. Fallback is Concept 3 exactly as built.
- **Judging angles:** top technical depth and innovation if it works; weakest reliability. Only for teams with prior imitation-learning experience.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Wuji Glove + XREAL AR glasses | AR-guided therapy: ghost target hand, pressure heat-map and score in view | Medium (stream from laptop to glasses app) |
| Wuji Glove + OriginFlow EMG | Muscle activity + ground-truth finger pose and pressure: fatigue / effort metrics, or an EMG → hand-pose decoder driving a Wuji Hand (prosthesis-style demo) | Medium–high (depends on OriginFlow's SDK — ⚠️ unverified) |
| Wuji Hand + Flexiv Rizon / ROKAE xMate | Compliant arm + dexterous hand for lids, pill boxes, cups | High (adapter, power, two SDKs) |
| Wuji Hand + Dobot CR / Nova | Same as above with a simpler cobot | Medium–high |
| Wuji Glove + Galaxea R1 / Galbot G1 / UniX Wanda | Glove as an intuitive teleop input for an existing mobile manipulator's own grippers (map pinch aperture) | Medium |
| Wuji Hand on a humanoid (Unitree, AGIBOT) | Dexterous hand on a walking platform | Very high — avoid unless adapters and drivers already exist on site |
| WUJI stack + D-Robotics RDK | Laptop-free bedside unit running the glove app | Low–medium (Linux arm64 wheels exist; ⚠️ untested) |

## Questions to ask the WUJI engineers on site

1. How many gloves and hands are here, which sides and generations, and how is access booked?
2. Does the glove fit small or stiff hands? Is there a liner or a cleaning procedure between users?
3. Is the EMF tracker safe to use on people with pacemakers or other implants, and how badly do rings, wheelchair frames or bed rails disturb it?
4. Can a person with limited finger range complete hand-model and tactile calibration, or can we use a default / therapist-made model?
5. Is there a mapping from the normalized tactile value (0–1) to newtons, and can tactile streams be recorded to MCAP?
6. Which arm flange adapters did you bring, and how should the 12 V / 20 A supply be routed along an arm?
7. For Hand 2: recommended kp / kd and `effort_limit` values for a soft, people-adjacent demo, and how long can it run before thermal derating?
8. Do glove calibration and the CLI work on macOS / Windows today, or should we plan for a Linux laptop? Is there a Docker image for ROS 2 Lyrical?
9. Does WUJI have any healthcare or rehab customers, or plans in that direction?

## Decision rule

- **Pick WUJI for T04 if** your idea is about the hand itself — measuring, coaching or remotely lending hand function — and you can get a glove early; add a partner arm only if you have integration experience and a confirmed adapter.
- **Avoid if** you need a mobile, whole-body or lifting assistant, autonomous behaviour out of the box, or anything that must touch or support a person with force.

## Sources

- [WUJI profile (this repo)](../WUJI.md)
- [Wuji Glove product introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md)
- [Wuji Glove — tactile data reference](https://docs.wuji.tech/docs/en/wuji-glove/latest/sdk-data-reference/tactile.md)
- [Wuji Glove — hand tracking data reference](https://docs.wuji.tech/docs/en/wuji-glove/latest/sdk-data-reference/hand-tracking.md)
- [Wuji Glove — calibration and configuration](https://docs.wuji.tech/docs/en/wuji-glove/latest/calibration.md)
- [Wuji Hand 2 — user notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md)
- [Wuji Hand 2 — effort and MIT parameters](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/effort-and-mit.md)
- [Wuji SDK — hand retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md)
- [Wuji SDK — data recording](https://docs.wuji.tech/docs/en/wuji-sdk/latest/data-recording.md)
- [Wuji Docs — English index](https://docs.wuji.tech/_llms/en.txt)
- [GitHub: wuji-technology](https://github.com/wuji-technology) ([wuji-sdk](https://github.com/wuji-technology/wuji-sdk), [wuji-description](https://github.com/wuji-technology/wuji-description), [wuji-ros2](https://github.com/wuji-technology/wuji-ros2), [wuji-openpi](https://github.com/wuji-technology/wuji-openpi), [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop))
