---
type: challenge-playbook
company: "OriginFlow"
slug: OriginFlow
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# OriginFlow × T04 — Hackathon Playbook

⬆ [OriginFlow profile](../OriginFlow.md) · [Brief](OriginFlow-T04-1-Brief.md) · [Products and solutions](OriginFlow-T04-2-Products-and-Solutions.md)

**Gate before anything else (first 30 minutes):** ask the OriginFlow team what you can read **live** from the Band. Three possible answers decide your concept:

| What they offer | What you can build |
|---|---|
| Live raw sEMG (+ wrist motion) | Concepts 1 and 2 |
| Live PULSE output (hand pose + force estimate) | Concepts 1, 2 and 3 |
| Recording and file export only | Concept 4, or Concept 1 as an offline analysis |
| Nothing exportable within 48 hours | Do not build on OriginFlow |

No OriginFlow SDK, API or ROS 2 interface is public. All stack descriptions below assume you write a small **bridge node** yourself (read their stream, republish as ROS 2 topics or WebSocket). Test only on healthy team members; make no clinical claims.

## Solution approaches

### Concept 1 — Grip Coach: EMG biofeedback for hand rehabilitation

- **Problem → value:** hand and forearm exercises after injury, stroke or surgery are repetitive and done unsupervised; patients cannot see whether they are activating the right muscles or fatiguing. Live muscle feedback keeps them engaged and gives the therapist an effort log.
- **Hardware:** OriginFlow **Band** + laptop. Optional: **XREAL** glasses as a hands-free display; soft ball or therapy putty as props.
- **Architecture / stack:**
  - Perception: raw 16-channel sEMG → rectified RMS envelope per channel → normalise to the user's maximum voluntary contraction (30-second calibration you build yourself). If PULSE is available, add fingertip-force estimate and finger pose.
  - Logic: exercise state machine (squeeze, hold, release, pinch per finger), rep counter, hold-quality score, fatigue trend from spectral shift across the session.
  - Output: web dashboard (patient view = game bar; therapist view = session report). Compute on the laptop.
- **48-hour plan:**
  - H0–6: confirm stream, write bridge, plot 16 channels live.
  - H6–24: envelope, calibration, rep detection, one exercise end to end.
  - H24–40: three exercises, fatigue trend, session report, optional AR view.
  - H40–48: test on 5 different people, rehearse, record backup video.
- **3-minute demo script:** (0:00) volunteer straps on the Band, 30 s calibration. (0:45) squeezes a ball; bar follows effort, reps counted. (1:30) deliberately "cheats" with a weak squeeze — coach flags it. (2:00) therapist report: reps, peak effort, fatigue curve. (2:30) cost and take-home story.
- **Risks and fallbacks:** no live stream → run the same analysis on recorded files and show it as a post-session report. Noisy signal on some users → fall back to the 4 strongest channels.
- **Judging angles:** innovation moderate; technical depth in signal processing; impact clear and immediately understandable; **Leukerbad relevance high** (rehab clinics, guests continuing therapy in a hotel room). Weakness: no robot — pair with Concept 2 if the track statement requires one.

### Concept 2 — Effort-aware assist arm (assist-as-needed)

- **Problem → value:** robot-guided limb exercises risk the robot doing all the work. Using muscle effort to scale assistance keeps the patient active: the arm helps more when effort drops, less when the patient is working.
- **Hardware:** OriginFlow **Band** + a force-controlled arm on site — **Flexiv Rizon** or **ROKAE xMate** (joint torque sensing) — with a simple hand grip on the flange (hand-held, never strapped).
- **Architecture / stack:**
  - Perception: sEMG effort index (as Concept 1) + the arm's own force / torque reading at the handle.
  - Planning: fixed exercise path (for example a slow forearm reach or wrist arc); assistance gain = function of effort index and tracking error.
  - Control: the arm vendor's impedance / force-control mode through its own SDK, with conservative force and speed limits. Bridge and gain scheduler on a laptop; optional **D-Robotics RDK** as the bridge host.
- **48-hour plan:**
  - H0–6: confirm EMG stream; get the arm moving in compliant mode with vendor engineers; agree safety limits.
  - H6–24: fixed path in impedance mode; effort index live; first gain-scheduling loop.
  - H24–40: tune on several users; add on-screen display of "patient share vs robot share"; fatigue-triggered rest.
  - H40–48: safety review, rehearsal, backup video.
- **3-minute demo script:** (0:00) problem in one sentence. (0:20) volunteer holds the handle and relaxes — arm carries the motion, screen shows 90% robot. (1:00) volunteer engages — assistance fades, screen shows patient share rising. (1:45) simulated fatigue — arm takes over smoothly and suggests a rest. (2:20) session summary and outlook.
- **Risks and fallbacks:** EMG latency or jitter makes assistance feel unstable → low-pass the effort index and change gain between repetitions rather than inside them. No EMG stream → use the arm's force sensor alone and show EMG as a recorded overlay. Safety: hand-held grip, low force cap, emergency stop within reach, healthy volunteers only.
- **Judging angles:** innovation good (muscle signal closes the loop, not just force); technical depth high (two vendors, real-time control); impact strong for physiotherapy capacity; Leukerbad relevance high.

### Concept 3 — Intent Hand: weak grip in, strong grip out

- **Problem → value:** many elderly people keep motor intent but lose grip strength (arthritis, sarcopenia). A light squeeze detected at the wrist commands a robot hand to do the forceful part — open a bottle, hold a cup, carry a bag.
- **Hardware:** OriginFlow **Band** + **PULSE** output; **WUJI Hand** (20 DoF) or a Unitree Dex hand, mounted on a table stand, a cobot arm (Dobot, ROKAE, Flexiv) or a wheeled mobile manipulator (Galaxea R1, Galbot G1, UniX Wanda).
- **Architecture / stack:**
  - Perception: PULSE hand pose + fingertip-force estimate. Without PULSE: your own 3–4 class gesture classifier on raw sEMG (rest, power grasp, pinch, open), trained per user in minutes.
  - Planning: retarget human finger pose to the robot hand, or map classes to grasp primitives; force estimate sets grip strength with amplification and a hard cap.
  - Control: robot-hand SDK joint or grasp commands; arm stays in a fixed or pre-scripted pose. Compute on a laptop.
- **48-hour plan:**
  - H0–6: confirm PULSE stream format; get the robot hand opening and closing from code.
  - H6–24: classifier or retargeting working; hand mirrors the user with visible latency measured.
  - H24–40: force scaling, three daily-living tasks (bottle, cup, pill box), mount on arm or mobile base if stable.
  - H40–48: reliability runs, rehearsal, backup video.
- **3-minute demo script:** (0:00) volunteer fails to open a tight bottle with a deliberately weak grip. (0:30) puts on the Band; robot hand mirrors finger motion. (1:15) light squeeze → robot holds the bottle firmly while the user twists the cap. (2:00) pinch gesture → robot picks up a pill box and hands it over. (2:40) outlook: same band, any hand.
- **Risks and fallbacks:** no PULSE stream → gesture-class version. Retargeting to 20 DoF too slow → use 3 grasp primitives. Per-user calibration too long → demo with one calibrated team member. Performance on genuinely weak or elderly muscles is untested — say so.
- **Judging angles:** innovation high and very visual; technical depth in decoding and retargeting; impact on independence; Leukerbad relevance medium-high (elderly spa guests). Closest to OriginFlow's own LinkerBot dexterous-hand direction.

### Concept 4 — Caregiver skill capture to robot replay

- **Problem → value:** care tasks depend on how firmly and how gently a skilled person acts, which video alone does not capture. Record a physiotherapist or caregiver with video, motion and muscle-derived force, then have a robot reproduce the motion with a matching force profile.
- **Hardware:** full **OriginKitGen 1.0** (Glass + Band + Space); a force-controlled arm (**Flexiv Rizon** or **ROKAE xMate**) or a wheeled dual-arm robot (Galaxea, Galbot, Spirit AI) for replay; a dummy limb or cushion as the "patient".
- **Architecture / stack:**
  - Capture: 10–20 demonstrations of one task (for example a forearm massage stroke on a dummy, or handing over a cup) → exported video, wrist motion, sEMG / PULSE force.
  - Learning: extract wrist trajectory and a normalised force-over-time profile; fit a simple parametrised skill (path + force setpoint curve). Fine-tuning a vendor VLA on this data is the stretch goal, not the plan.
  - Control: arm follows the path in force-control mode with the learned force curve scaled into a safe range. Compute on a laptop.
- **48-hour plan:**
  - H0–6: confirm export format and that you can take files off Space; pick one task.
  - H6–24: capture sessions; parse data; align video, motion and force.
  - H24–40: skill fitting; replay on the arm against a dummy with a force cap.
  - H40–48: side-by-side visualisation human vs robot, rehearsal.
- **3-minute demo script:** (0:00) therapist wears the kit and performs the stroke on a dummy arm; live timeline shown. (1:00) plot of captured force profile. (1:30) robot reproduces the stroke; measured contact force overlaid on the human curve. (2:30) outlook: a library of care skills captured from Leukerbad therapists.
- **Risks and fallbacks:** export not possible in time → concept is dead, switch to Concept 1 or 2. PULSE gives **fingertip** force estimates, not palm or whole-hand contact force → use it as a relative intensity curve, calibrated against the arm's own force sensor. Too few demos to learn from → hand-script the path and use only the captured force curve.
- **Judging angles:** innovation high (force-aware demonstration data for care); technical depth high; impact is longer-term; Leukerbad relevance good (thermal-spa and physiotherapy know-how). Highest schedule risk of the four.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Band + **Flexiv Rizon** or **ROKAE xMate** | Effort-aware assisted exercise (Concept 2); force-profile replay (Concept 4) | Medium — bridge node + vendor impedance mode |
| Band + PULSE + **WUJI Hand** | Intent-driven assistive grasp with finger-level retargeting (Concept 3) | Medium-high — retargeting to 20 DoF |
| Band + **Unitree Dex hand** on a G1 / H1 | Same as above on a humanoid | High — whole-robot setup on top of decoding |
| Band + **Galaxea R1 / Galbot G1 / UniX Wanda** | Gesture or squeeze as a hands-busy command channel for a fetch-and-carry robot | Medium — class-level commands only |
| Band + **XREAL** glasses | AR exercise feedback in the user's view (Concept 1) | Low-medium — display app only |
| Band + **D-Robotics RDK X5 / S100** | Edge host for the bridge and signal processing, no laptop on the table | Low-medium |
| Full kit + a VLA vendor (**Galaxea G0, Galbot, Spirit AI, AGIBOT GO-1**) | Human demonstrations as fine-tuning data for a care task | High — unlikely to finish in 48 hours |

## Questions to ask the OriginFlow engineers on site

1. Can we read **raw sEMG live** from the Band? Over what transport (BLE, Wi-Fi, USB, via Space), at what sampling rate and bit depth?
2. Can we subscribe to **PULSE output live** (joint angles, fingertip force)? Update rate, end-to-end latency, units?
3. How long is **per-user calibration**, and does it need to be repeated after re-donning the Band?
4. Does the Band work **standalone**, or are Glass and Space required?
5. What is the **export format** of recordings, and can we copy files off Space ourselves during the event?
6. Has PULSE been tried on **older adults or people with reduced hand strength**? Any known failure cases (dry skin, thin forearms, tremor)?
7. Is the force output absolute (newtons) or relative, and what is it calibrated against?
8. Are there any restrictions on publishing demo data or code after the hackathon?

## Decision rule

- **Pick OriginFlow for T04 if** the team confirms a live stream of raw sEMG or PULSE output in the first hour, you want a muscle-signal angle no other vendor offers, and you have someone comfortable with signal processing plus a partner vendor for actuation.
- **Avoid if** there is no real-time access or export, you need a robot platform from a single vendor, or your idea is about mobility, falls, lifting or logistics rather than the hand and forearm.

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost (EN), 2026-05-21 — funding announcement and application areas](https://en.tmtpost.com/post/7997613)
- [QbitAI, 2026-08 — OriginFlow profile (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [36Kr Europe (EN), 2026-08-24 — republished QbitAI profile](https://eu.36kr.com/en/p/3950735048031365)
- [emg2pose — GitHub (facebookresearch)](https://github.com/facebookresearch/emg2pose)
- [generic-neuromotor-interface — GitHub (facebookresearch)](https://github.com/facebookresearch/generic-neuromotor-interface)
- [NinaPro database](https://ninapro.hevs.ch/)
- [OriginFlow company profile (internal)](../OriginFlow.md)
