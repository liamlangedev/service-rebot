---
type: challenge-playbook
company: "OriginFlow"
slug: OriginFlow
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# OriginFlow × T03 — Hackathon Playbook

⬆ [OriginFlow profile](../OriginFlow.md) · [Brief](OriginFlow-T03-1-Brief.md) · [Products and solutions](OriginFlow-T03-2-Products-and-Solutions.md)

**Read first:** fit is **1/5**. OriginFlow has no robot and **no public SDK, API, ROS 2 driver or export format**. Every concept below is **conditional** on what the booth team offers, and each one needs another vendor's robot to produce a T03 result. Settle the interface question in the first hour (see questions below) or drop OriginFlow from your plan.

| Gate | What you need from the booth | Unlocks |
|---|---|---|
| A | Recordings can be **exported** (video + sEMG and/or PULSE outputs) in a readable format | Concept 1, Concept 3 |
| B | A **live stream** of raw sEMG or PULSE outputs to your laptop | Concept 2, Concept 4 |
| Neither | — | Do not build on OriginFlow for T03 |

## Solution approaches

### Concept 1 — Show-and-sort: teach a recycling cell from one worker's demonstration

- **Problem → value:** resort waste is mixed and changes with the season; reprogramming a sorting robot per item type is slow. A worker wearing the kit sorts for 20 minutes, and the recording becomes labelled training data for the robot's classifier and pick targets.
- **Hardware:** OriginKitGen 1.0 (Glass + Band + Space) · any arm on site with a gripper (Dobot CR / Nova, ROKAE xMate, Flexiv Rizon) · a fixed camera over the table · laptop or D-Robotics RDK.
- **Architecture / stack:**
  - Perception: Glass egocentric video gives item views; the bin each item lands in gives the label. Band grasp events (EMG burst) segment the video into one clip per item — your own thresholding code if only raw sEMG is exported, or PULSE contact output if offered.
  - Planning: small image classifier fine-tuned on those clips (your code); class → bin lookup.
  - Control: the arm vendor's SDK for pick-and-place from the fixed camera. OriginFlow is **offline only** here.
  - Compute: laptop GPU for training; inference on laptop or RDK board.
- **48-hour plan:**
  - H0–6: pass Gate A; record a 2-minute test; confirm you can open the files. In parallel, get the arm doing a scripted pick-and-place.
  - H6–24: record 20–30 minutes of sorting across 4 classes (for example PET, aluminium, glass, residual); auto-segment by grasp events; train classifier.
  - H24–40: integrate classifier with the arm; add a fifth class from a fresh 5-minute demonstration to prove fast re-teaching.
  - H40–48: timing run, accuracy count, demo rehearsal.
- **3-minute demo script:** (0:00) teammate wearing Glass + Band sorts five items of a new class while the screen shows video and EMG grasp markers · (1:00) show the auto-cut clips and a quick fine-tune · (1:45) arm sorts a mixed pile including the new class · (2:30) show accuracy and "minutes of demonstration per new class".
- **Risks and fallbacks:** export not possible → record with a phone or laptop camera and label by hand (OriginFlow drops out). Classifier weak → reduce to 3 visually distinct classes. Fine-tune too slow for live demo → pre-train and show the before/after.
- **Judging angles:** innovation: medium (re-teaching by demonstration) · technical depth: medium · real-world impact: plausible for small sorting stations · Leukerbad relevance: hotel, spa and visitor waste with seasonal peaks (assumption; confirm against the official statement).

### Concept 2 — Hands-busy exception handling for a sorting robot

- **Problem → value:** automated sorters stall or mis-sort on ambiguous items. A worker who is already handling waste resolves each doubt with a wrist gesture, no touchscreen, no stopping. Every decision is logged as a new training label, so interventions fall over time.
- **Hardware:** Band (with Space if required) · arm + camera as in Concept 1 · optional XREAL glasses to show the robot's question in the operator's view.
- **Architecture / stack:**
  - Perception: robot-side classifier with a confidence threshold.
  - Planning: low confidence → pause, show item and top-2 guesses; operator gesture selects bin A, bin B or reject.
  - Input: 3–4 gestures decoded from the Band. Use PULSE pose output if streamed; otherwise train a small per-user classifier on raw 16-channel sEMG windows (your code, a few minutes of data).
  - Control: arm vendor's SDK. Bridge = one small process that turns gesture events into robot commands (write it yourself; no OriginFlow ROS 2 node is documented).
  - Compute: laptop.
- **48-hour plan:**
  - H0–6: pass Gate B; measure stream rate and latency; record gesture data from two teammates.
  - H6–24: gesture classifier with a rest class and a hold-to-confirm rule; robot sorter with confidence output.
  - H24–40: close the loop; log interventions; retrain once to show the intervention rate dropping.
  - H40–48: robustness with a second user (recalibration time matters), rehearsal.
- **3-minute demo script:** (0:00) robot sorts easy items alone · (0:40) ambiguous item: robot pauses, operator with full hands flicks the wrist, item goes to the right bin · (1:30) repeat with reject gesture · (2:10) chart: interventions per 20 items before and after retraining.
- **Risks and fallbacks:** no live stream → keyboard or foot pedal stands in (OriginFlow drops out). False triggers → require a held gesture and limit to 2 gestures. Calibration per user is long → one designated operator for the demo.
- **Judging angles:** innovation: medium-high (muscle-signal human-in-the-loop) · technical depth: medium-high · real-world impact: keeps humans in charge of edge cases · Leukerbad relevance: small municipal or hotel sorting points with few staff (assumption).

### Concept 3 — Force-aware disassembly for repair and reuse

- **Problem → value:** reuse beats recycling, but dismantling devices or equipment (small electronics, battery packs, rental-gear fittings) is contact-rich and hard to automate. Capture how hard a skilled person grips, twists and pries, and use that to set force limits on a force-controlled arm so it opens the item without breaking reusable parts.
- **Hardware:** OriginKitGen 1.0 with PULSE force output · **Flexiv Rizon** or **ROKAE xMate** 7-DoF with torque sensing · gripper or screwdriver tool · fixed camera.
- **Architecture / stack:**
  - Perception: Glass video for step order; fixed camera for fastener or part location (simple detection or fiducials).
  - Planning: hand-written step sequence taken from the recorded demonstration (unscrew, pry, lift).
  - Control: the arm's force / impedance mode via its vendor SDK. Per-step force ceiling and contact threshold derived from the **relative** grip-effort profile of the human demonstration (scale it against the arm's own force sensor; PULSE force is an estimate, not a calibrated Newton value).
  - Compute: laptop; OriginFlow used offline (Gate A), or live for a side-by-side display (Gate B).
- **48-hour plan:**
  - H0–6: pass Gate A; pick **one** object with 3–4 steps; record 10 demonstrations.
  - H6–24: script the sequence on the arm with conservative force limits; extract per-step effort peaks from the recordings.
  - H24–40: tune limits from the human profile; compare breakage or success against fixed-limit baseline.
  - H40–48: repeatability runs, demo rehearsal.
- **3-minute demo script:** (0:00) human dismantles the item wearing the kit; live effort curve on screen · (0:50) the per-step effort profile turned into robot force limits · (1:20) arm performs the same disassembly · (2:20) recovered parts in a "reuse" tray; success-rate table.
- **Risks and fallbacks:** PULSE force not exported → use raw sEMG amplitude envelope as a relative effort proxy. Effort-to-force mapping is weak → present it as step segmentation and ordering only, and tune limits from the arm's own sensor. Scope creep → one object, one tool.
- **Judging angles:** innovation: high (muscle-derived force priors for circular-economy tasks) · technical depth: high · real-world impact: repair and parts recovery · Leukerbad relevance: winter-sports rental gear and hospitality equipment repair (assumption; pick the object to match the official statement).

### Concept 4 — EMG-teleoperated hand for unsortable or hazardous items

- **Problem → value:** some waste (broken glass, sharps, leaking batteries) should not be touched by people and defeats simple grippers. An operator's wrist signals drive a dexterous hand remotely; every teleoperated grasp is logged as training data.
- **Hardware:** Band + PULSE hand-pose stream · **WUJI Hand** (20 DoF) or Unitree Dex hand on an arm or on a Galaxea / Galbot mobile manipulator · camera feed to the operator.
- **Architecture / stack:** PULSE joint estimates → your retargeting code → hand vendor's joint interface; arm positioned by a separate input or pre-set poses; laptop compute. No published OriginFlow-to-WUJI mapping exists (their announced hand partner, LinkerBot, is not on site).
- **48-hour plan:** H0–6: pass Gate B and confirm PULSE streams joint angles at usable latency · H6–24: retarget 3 grasp types (pinch, power, tripod) · H24–40: pick-and-drop of 5 awkward items · H40–48: rehearsal, log replay.
- **3-minute demo script:** operator behind a screen closes their hand; the robot hand mirrors it and lifts a "hazardous" item into a sealed bin; show logged episodes as future training data.
- **Risks and fallbacks:** highest-risk concept: two undocumented interfaces plus retargeting. Fallback: reduce to open / close / pinch on a parallel gripper, which is Concept 2 with a different story.
- **Judging angles:** innovation: high · technical depth: high · real-world impact: worker safety more than sustainability, so it may sit better in T02 · Leukerbad relevance: low.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| OriginKitGen 1.0 + Dobot CR / Nova or Magician | Concept 1 show-and-sort on an easy-to-script cobot | **Medium** — offline data only; hinges on export |
| Band + any arm + XREAL glasses | Concept 2 gesture-resolved sorting with the robot's question shown in view | **Medium-high** — live stream + your gesture decoder + your bridge |
| OriginKitGen 1.0 + Flexiv Rizon or ROKAE xMate (torque-sensing) | Concept 3 force-aware disassembly | **High** — effort-to-force mapping is unproven |
| Band + PULSE + WUJI Hand | Concept 4 EMG teleoperation of a dexterous hand | **Very high** — retargeting from scratch |
| OriginKitGen 1.0 + Galaxea / Galbot / Spirit AI VLA stacks | Human demonstrations as extra data for a vision-language-action policy | **Very high** — no documented data format match; unrealistic in 48 hours ⚠️ unverified |
| Any combo + D-Robotics RDK | Low-power edge inference for the classifier (fits the "low-power edge AI" angle) | **Low-medium** — independent of OriginFlow |

## Questions to ask the OriginFlow engineers on site

1. Can we **take recordings away**? In which format (video container, sEMG as CSV / HDF5, timestamps)?
2. Is there a **live stream** of raw sEMG and of PULSE outputs (UDP, WebSocket, ROS 2)? At what rate and latency?
3. Does PULSE output **per-finger force** or only a relative effort value? In what units, and how accurate after calibration?
4. How long is **per-user calibration**, and does it survive taking the Band off and on?
5. Does the Band work **standalone**, or are Glass and Space required?
6. Does it work with **work gloves, wet or dirty hands**, and in the cold?
7. Can you run **ORACLE** on our recording to get task segments, or is that internal only?
8. How many kits can one team borrow, and will an engineer stay with us during integration?

## Decision rule

- **Pick OriginFlow for T03 if** you already have a robot from another vendor doing sorting or disassembly, the booth confirms export or a live stream within the first hour, and you want a human-skill or human-in-the-loop story on top.
- **Avoid if** you need the vendor to provide the robot, the autonomy or a documented API, or if your T03 idea is about energy, water, monitoring or mobility — OriginFlow adds nothing there.

## Sources

- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost (EN), 2026-05-21 — funding, industrial and home-service scenarios](https://en.tmtpost.com/post/7997613)
- [36Kr Europe (EN), 2026-08-24 — profile: Band, PULSE, CHORD, ORACLE, roadmap](https://eu.36kr.com/en/p/3950735048031365)
- [QbitAI (Chinese), 2026-08-22 — original profile](https://www.qbitai.com/2026/08/477094.html)
- [facebookresearch/emg2pose (GitHub)](https://github.com/facebookresearch/emg2pose)
- [facebookresearch/generic-neuromotor-interface (GitHub)](https://github.com/facebookresearch/generic-neuromotor-interface)
- [OriginFlow company profile (internal)](../OriginFlow.md)
