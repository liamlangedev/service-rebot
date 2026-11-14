---
type: challenge-playbook
company: "OriginFlow"
slug: OriginFlow
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# OriginFlow × T02 — Hackathon Playbook

⬆ [OriginFlow profile](../OriginFlow.md) · [Brief](OriginFlow-T02-1-Brief.md) · [Products and solutions](OriginFlow-T02-2-Products-and-Solutions.md)

**Before anything else (first 15 minutes):** OriginFlow has **no public SDK, API or export format**. Go to their table and find out which of these you get. It decides which concept is possible.

| What the team offers | Concepts open to you |
|---|---|
| File export only (video + sEMG + motion) | Concept 1 |
| Live **raw sEMG** stream | Concepts 1, 2 |
| Live **PULSE** output (hand pose + fingertip force) | Concepts 1, 2, 3 |
| Nothing self-service | Drop OriginFlow for T02 |

OriginFlow is never the robot. Every concept needs a second vendor for anything that moves.

## Solution approaches

### Concept 1 — Inspection black box (wearable task log to auto-report)

- **Problem → value:** Inspection rounds on cable cars, thermal-water pipes or avalanche barriers are documented by hand, after the fact. A worn recorder that produces a time-stamped, searchable report makes rounds auditable and lets a less experienced technician replay an expert's procedure.
- **Hardware:** OriginKitGen 1.0 (Glass + Band + Space) on one technician. Optional: SKYLANDX MetaCam scan of the same site to place findings in a 3D map.
- **Architecture / stack:** capture (kit, local recording) → export → your laptop: segment the session using sEMG effort bursts and wrist motion as "hands-on" markers → run a vision-language model of your choice on the matching video segments to describe each action and flag anomalies → generate a checklist-style report. No robot control, no live stream needed. Compute on a laptop.
- **48-hour plan:**
  - **H0–6:** confirm export works and the format is readable; record one 5-minute mock inspection.
  - **H6–24:** parser, sEMG / motion segmentation, video-clip extraction, VLM captioning.
  - **H24–40:** report generator, second and third recordings on a mock rig (valve, bolt, cable clamp), optional 3D map anchoring.
  - **H40–48:** freeze, rehearse, pre-compute one full report as backup.
- **3-minute demo script:** (0:00) the pain: paper inspection logs. (0:30) technician wears kit, tightens a clamp, checks a valve, skips one step. (1:30) report appears: steps, timestamps, effort trace, the skipped step flagged. (2:30) how it scales to a real maintenance crew.
- **Risks and fallbacks:** no export within 48 h → concept dead, switch vendor. sEMG adds little over video → present it honestly as the "hands-on effort" channel. Fallback: pre-recorded session.
- **Judging angles:** innovation low-medium; technical depth medium; real-world impact medium (auditability of safety-critical maintenance); Leukerbad relevance good (cable cars, thermal infrastructure, protective structures).

### Concept 2 — Silent gesture command for a scout quadruped

- **Problem → value:** A responder on steep, snowy ground has gloves on, hands on poles or a stretcher, and radio noise. Decoding a handful of wrist / finger gestures from muscle signals gives a command channel that needs no free hand, no voice and no camera view of the hand (inference: EMG should work in darkness or smoke; not demonstrated by OriginFlow).
- **Hardware:** Band (plus Glass for the mission log). A quadruped from Unitree, Genisom AI or Magiclab via its own high-level SDK. Optional: D-Robotics RDK as an on-robot bridge; XREAL glasses to show the dog's camera to the operator.
- **Architecture / stack:** raw sEMG stream → laptop: band-pass, windowing, per-user classifier for 5 to 8 gestures (stop, follow, go ahead, scan, return, confirm) → command arbiter with a mandatory **confirm gesture and a dead-man stop** → quadruped high-level velocity / mode commands through the robot vendor's SDK. Robot autonomy (obstacle avoidance, gait) stays on the robot.
- **48-hour plan:**
  - **H0–6:** verify the live sEMG stream and its rate; get the quadruped moving from a keyboard through the same command interface.
  - **H6–24:** record gesture data from one operator; train and test the classifier; wire gestures to robot commands.
  - **H24–40:** robustness: re-don the band, test with gloves and a jacket, add confirm / timeout logic, add video feed to the operator.
  - **H40–48:** scripted mock-rescue run, backup video, measure and report accuracy.
- **3-minute demo script:** (0:00) responder with both hands on a stretcher. (0:30) fist-twist sends the dog ahead; pinch triggers a scan; open-hand stops it instantly. (1:45) dog finds the "casualty" marker, operator sees the feed. (2:30) confusion matrix and false-trigger rate, honestly shown.
- **Risks and fallbacks:** no raw stream → not possible. Classifier drifts after re-donning → quick 60-second recalibration routine. Glove / cold degrade signal → demo indoors, state the limit. Fallback input: wrist-motion (IMU) gestures only.
- **Judging angles:** innovation medium-high (EMG field interface); technical depth medium; impact medium; Leukerbad relevance high (mountain rescue, avalanche terrain).

### Concept 3 — Force-aware remote hand for hazardous manipulation

- **Problem → value:** Closing a valve or flipping a breaker in a gas-filled or flooded plant room should not need a person inside. Vision-only teleoperation lacks grip force; PULSE estimates fingertip force along with hand pose, so the remote hand can squeeze as hard as the operator does.
- **Hardware:** Band + PULSE. WUJI Hand or a Unitree Dex hand on a Flexiv Rizon or ROKAE xMate force-controlled arm. Optional: XREAL for the remote camera view.
- **Architecture / stack:** PULSE stream (hand pose + fingertip force) → retargeting node (human joint angles to the robot hand's joints; force estimate to grip-force or current limit) → hand SDK. Arm pose from a separate source (Band wrist motion gives orientation only): a 6-DoF controller, AR-glasses hand tracking or pre-taught waypoints. Arm in compliant mode so contact is safe. Compute on a laptop.
- **48-hour plan:**
  - **H0–6:** confirm PULSE output is streamable, its rate and latency; move the robot hand from a script.
  - **H6–24:** retargeting, open / close / pinch mirroring; arm waypoints to the valve.
  - **H24–40:** force mapping with clamps and rate limits; valve-turn and breaker-flip trials.
  - **H40–48:** rehearse one task end to end; record backup.
- **3-minute demo script:** (0:00) "plant room is unsafe". (0:30) operator outside flexes fingers, robot hand mirrors. (1:15) arm moves to the valve, operator grips and turns; force bar shows operator estimate versus robot grip. (2:30) limits and next steps.
- **Risks and fallbacks:** PULSE not exposed, or too laggy → fall back to Concept 2 style discrete grasp commands (open, power grasp, pinch). Force estimate noisy → use it as three levels (light, medium, firm). Two extra vendor integrations in 48 h is a lot — fix the task to one object.
- **Judging angles:** innovation high; technical depth high; impact medium-high; Leukerbad relevance medium (thermal-water and utility plant rooms).

### Concept 4 — Show once, robot repeats (shut-off skill capture)

- **Problem → value:** During a disruption the one person who knows the shut-off procedure may not be reachable. Capture the expert doing it once with the kit, and let a mobile manipulator replay it.
- **Hardware:** OriginKitGen 1.0 for capture; a wheeled dual-arm robot on site (Galaxea, Galbot, AGIBOT G-series, Spirit AI or UniX AI) for execution.
- **Architecture / stack:** kit recording → hand trajectory + grip events (from PULSE or your own decoding) → keyframe extraction → retarget to the robot's end-effector waypoints and gripper commands → execute with the robot vendor's own motion API. Honest scope: **scripted keyframe replay on one fixed rig**, not a learned policy — OriginFlow's cross-embodiment transfer is not available to you.
- **48-hour plan:** **H0–6** confirm export and pose output; **H6–24** keyframe extraction and retargeting in simulation or on the robot; **H24–40** real-robot replay on one valve rig; **H40–48** rehearse.
- **3-minute demo script:** expert performs the shut-off wearing the kit; pipeline view of extracted keyframes; robot repeats it; say clearly what was scripted.
- **Risks and fallbacks:** highest risk of the four — needs export, pose output and a robot integration. Fallback: Concept 1 report plus a manually taught robot replay.
- **Judging angles:** innovation high; technical depth high if it works; impact medium; Leukerbad relevance medium.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Band + Unitree / Genisom AI / Magiclab quadruped | Hands-busy gesture command of a scout robot (Concept 2) | **Medium** — own classifier + a thin command bridge; needs raw sEMG stream |
| Band + PULSE + WUJI Hand (or Unitree Dex hand) + Flexiv / ROKAE arm | Force-aware remote manipulation (Concept 3) | **High** — three vendors, retargeting, separate arm tracking |
| OriginKitGen 1.0 + SKYLANDX MetaCam | Inspection log anchored in a 3D scan of the site (Concept 1) | **Low-medium** — off-line fusion by timestamp / manual anchoring |
| Band + XREAL glasses | Operator sees the robot feed while commanding by gesture | **Low-medium** — display only |
| Band + D-Robotics RDK | Edge inference / bridge node on the robot instead of a laptop | **Medium** — only worth it if the classifier is small |
| OriginKitGen 1.0 + Galaxea / Galbot / AGIBOT wheeled dual-arm | Human demonstration to scripted robot replay (Concept 4) | **High** |

## Questions to ask the OriginFlow engineers on site

1. Can we get a **live stream of raw 16-channel sEMG** from the Band? Transport (UDP, WebSocket, BLE, serial), sampling rate, latency?
2. Is **PULSE output** (hand pose, fingertip force) streamable in real time, and at what rate? Which hand model / joint convention?
3. How long is **per-user calibration**, and how well does it survive taking the Band off and on?
4. What **export format** do recordings use, how fast can we get files, and may we keep and publish the data?
5. Does the Band work **standalone**, or must Glass and Space be present?
6. Has the Band been tested **over or under gloves, in cold or with wet skin**? Any IP rating?
7. Has anyone on your team driven a **robot hand or robot** live from the Band? Can we reuse that bridge?
8. How many kits are available per team, and is an engineer available to help with integration overnight?

## Decision rule

- **Pick OriginFlow for T02 if** the team confirms a live sEMG or PULSE stream in the first hour **and** you already have a robot from another vendor whose high-level commands you can drive — then EMG becomes a distinctive operator interface for hazardous or hands-busy work.
- **Avoid if** you need a robot, mapping or autonomy from your main vendor, if only staff-run capture is offered, or if nobody on your team can train a small signal classifier in a day.

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost (EN), 2026-05-21 — funding and commercial scenarios](https://en.tmtpost.com/post/7997613)
- [36Kr Europe (EN), 2026-08-24 — OriginFlow profile, PULSE / WAIC demo](https://eu.36kr.com/en/p/3950735048031365)
- [QbitAI, 2026-08-22 — OriginFlow profile (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [emg2pose — GitHub (facebookresearch)](https://github.com/facebookresearch/emg2pose)
- [generic-neuromotor-interface — GitHub (facebookresearch)](https://github.com/facebookresearch/generic-neuromotor-interface)
- [OriginFlow company profile (internal)](../OriginFlow.md)
