---
type: challenge-playbook
company: "OriginFlow"
slug: OriginFlow
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# OriginFlow × T01 — Hackathon Playbook

⬆ [OriginFlow profile](../OriginFlow.md) · [Brief](OriginFlow-T01-1-Brief.md) · [Products and solutions](OriginFlow-T01-2-Products-and-Solutions.md)

**Gate before anything else (first 30 minutes):** ask the OriginFlow team which of these they can give you. Your concept choice follows directly.

| What the booth offers | Concepts open to you |
|---|---|
| Live **raw sEMG + wrist motion** stream | 1, 2 |
| Live **PULSE** output (hand pose / fingertip force) | 1, 2, 3 |
| Only recorded files, exported by staff | 4 (weak), or drop OriginFlow |
| Nothing exportable | Do not build on OriginFlow for T01 |

Every concept needs a robot from another vendor. OriginFlow has no public SDK; all stack details on their side are assumptions to confirm.

## Solution approaches

### Concept 1 — Muscle remote for a porter / delivery robot

- **Problem → value:** Hotel porters, clinic staff and municipal workers in Leukerbad have gloved or full hands, and wind or street noise defeats voice and touchscreens. A wristband under the sleeve lets them command a carrier robot (follow, stop, wait here, return to base) with small hand gestures.
- **Hardware:** OriginFlow **Band** (+ Space if required) · a carrier: Unitree Go2 / B2, Genisom or AGIBOT D1 quadruped with a basket, or a wheeled platform · laptop or D-Robotics RDK for the classifier.
- **Architecture / stack:**
  - Perception: raw 16-channel sEMG + wrist motion → sliding windows → amplitude features → small per-user classifier (4–5 gestures + rest), with a hold-to-confirm rule to reject accidental triggers.
  - Planning: tiny state machine (IDLE / FOLLOW / WAIT / RETURN) on the laptop.
  - Control: the robot vendor's **high-level** SDK (velocity / follow / go-to commands). Do not touch low-level control.
  - Compute: laptop; no OriginFlow model needed.
- **48-hour plan:**
  - H0–6: confirm stream, write a reader, log 10 minutes of labelled gestures from one operator; in parallel get the robot moving from a keyboard.
  - H6–24: train classifier, add debounce, wire the state machine to the robot; first end-to-end run.
  - H24–40: add person-following or waypoint return from the robot vendor's stack; test with winter gloves and a loaded basket; record backup video.
  - H40–48: rehearse, freeze code, build one slide with confusion matrix and latency.
- **3-minute demo script:** (0:00) worker with ski gloves carries two towel stacks, cannot touch a phone → (0:30) fist-hold: robot starts following → (1:15) open-hand: robot stops at a "room door", worker loads the basket → (1:45) double pinch: robot returns to the "laundry" waypoint alone → (2:30) show live EMG traces, gesture accuracy and why voice / touch fail outdoors.
- **Risks and fallbacks:** no raw stream → use wrist-motion only, or fall back to a phone-IMU gesture and present the Band as the intended sensor (honestly labelled). Misfires → fewer gestures (2–3) and longer hold time. Band shift → re-record 2 minutes before the pitch.
- **Judging angles:** innovation medium (new input channel for service robots) · technical depth medium · real-world impact good (keeps staff in the loop cheaply) · Leukerbad relevance high (gloves, cold, hotel and clinic logistics on steep streets).

### Concept 2 — Effort-aware load handover

- **Problem → value:** Delivery and maintenance robots hand heavy items to people. Use forearm muscle activation as a signal that the human has taken the load (or is straining), so the robot releases at the right moment or offers to carry more.
- **Hardware:** Band · any arm or mobile manipulator with a gripper (Galaxea R1, Galbot G1, AGIBOT G1 / G2, Dobot or ROKAE cobot on a cart; Flexiv Rizon if you also want measured force on the robot side).
- **Architecture / stack:** sEMG envelope → calibrated "effort level" per user → release / hold logic fused with the robot's own gripper or wrist force reading if available → vendor SDK gripper commands. Laptop compute.
- **48-hour plan:** H0–6 stream + effort calibration (rest vs holding 1 kg / 3 kg). H6–24 handover logic on a static arm. H24–40 add the delivery leg (robot brings item to a table / person) and a strain alert. H40–48 rehearse.
- **3-minute demo script:** robot brings a crate → person grips → robot releases only when muscle effort confirms the grip → repeat with a heavier crate, system flags strain and the robot keeps carrying instead.
- **Risks and fallbacks:** effort signal is noisy across users → single demo operator, two-level threshold only. If the robot has a force sensor, let it be the primary trigger and show EMG as confirmation.
- **Judging angles:** innovation medium-high · technical depth medium · impact: worker ergonomics in logistics · Leukerbad: luggage, spa laundry and supply handling with an older workforce and guests.

### Concept 3 — EMG remote-assist for a stuck service robot

- **Problem → value:** Service robots fail on the "last metre": a door handle, a lift button, a parcel locker. A remote operator wearing the Band takes over only the hand for a few seconds, with squeeze strength following estimated grip force, then autonomy resumes.
- **Hardware:** Band + **PULSE** live output (required) · **WUJI Hand** or a Unitree Dex hand on an arm, or a mobile manipulator's gripper (1-DoF mapping is enough) · XREAL glasses or a monitor for the robot's camera view.
- **Architecture / stack:**
  - Perception: PULSE hand pose + fingertip-force estimate; robot camera to operator.
  - Planning: autonomy state machine with an explicit "ask for help" state and hand-back.
  - Control: retarget pose to the hand's joint targets (or open / close + force level for a gripper); arm positioning by the robot's own planner or a simple preset approach pose.
  - Compute: PULSE wherever OriginFlow runs it; bridge and retargeting on your laptop.
- **48-hour plan:** H0–6 confirm PULSE stream rate and latency; get hand / gripper SDK moving. H6–24 retargeting (start with 1-DoF grasp + force scaling, then fingers). H24–40 integrate with one scripted service task (open a door, pick a parcel) and the help-request flow. H40–48 rehearse; record video.
- **3-minute demo script:** robot drives to a door / locker and stops, "help needed" appears → operator across the room closes their hand, robot hand mirrors it and squeezes harder as the operator does → handle turned / parcel taken → operator relaxes, robot continues its route.
- **Risks and fallbacks:** no PULSE stream → fall back to Concept 1 gestures mapped to open / close presets. Latency too high → slow, deliberate grasps only. Finger retargeting unstable → gripper open / close with three force levels.
- **Judging angles:** innovation high (force-aware EMG takeover) · technical depth high · impact: realistic human-in-the-loop path to deployment · Leukerbad: one remote operator could assist robots across hotels and clinics.

### Concept 4 — Teach-by-doing skill capture for housekeeping robots

- **Problem → value:** Hotels and clinics need robots to learn local tasks (strip a bed, load a linen cart, set a tray). Record staff doing the task with OriginKitGen and use the data to teach a mobile manipulator.
- **Hardware:** full **OriginKitGen 1.0** · a mobile manipulator with a data-driven stack (Galaxea with G0, Galbot, AGIBOT with GO-1, Spirit AI Moz1).
- **Architecture / stack:** capture → export (format unknown) → your own alignment of human hand trajectory to robot end-effector → fine-tune or condition the vendor's policy. Human-to-robot transfer is an open research problem and OriginFlow describes it as a plan, not a product.
- **48-hour plan:** H0–6 confirm export and format; record 30–50 demos of one task. H6–24 parse data, segment, visualise video + EMG + estimated force. H24–40 attempt transfer to one primitive (grasp force profile or pick sequence); otherwise script the robot with parameters taken from the human data. H40–48 rehearse.
- **3-minute demo script:** show capture of a housekeeper task → synchronised timeline (video, wrist, muscle) → robot performs the same primitive using parameters extracted from the recording → pitch the scaling path via capture services.
- **Risks and fallbacks:** highest risk; most likely outcome is a data pipeline + visualisation, not a learned policy. Be explicit about what is learned versus scripted.
- **Judging angles:** innovation high on paper · technical depth depends on how real the transfer is · impact long-term · Leukerbad: local hospitality workforce as the teachers.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Band + Unitree Go2 / B2 (or Genisom, AGIBOT D1) | Gesture-commanded porter / delivery quadruped (Concept 1) | Low–medium, if raw stream exists |
| Band + Flexiv Rizon / ROKAE xMate | Handover with muscle effort on the human side and measured force on the robot side (Concept 2) | Medium |
| Band + PULSE + WUJI Hand | Force-aware EMG teleoperation of a dexterous hand (Concept 3) | High; needs PULSE stream and retargeting |
| Band + Galaxea / Galbot / AGIBOT mobile manipulator | Remote-assist for a service robot's failed grasp | Medium–high |
| Glass / OriginKitGen + XREAL | Operator sees robot view while the kit records the operator | Medium; two head-worn devices may conflict |
| Band + D-Robotics RDK | Classifier on an edge board carried by the robot instead of a laptop | Low–medium |
| OriginKitGen + SKYLANDX MetaCam | Demonstrations anchored in a 3D scan of the site | High; little 48-hour payoff |

## Questions to ask the OriginFlow engineers on site

1. Can we read **raw 16-channel sEMG and wrist motion live**? Over what transport (UDP, WebSocket, BLE, USB), at what sampling rate?
2. Is **PULSE** running on site, and can we subscribe to its hand-pose and fingertip-force output? What is the end-to-end latency?
3. How long is per-user calibration, and how badly does accuracy drop if the Band is re-seated or another person wears it?
4. Does the Band work **standalone**, or are Glass and Space mandatory?
5. What is the recording **export format**, and can we copy files ourselves during the event?
6. Battery life and wireless range of the Band; any limits in cold or with sleeves over it?
7. How many kits can one team hold for the full 48 hours?
8. Has anyone already retargeted PULSE output to a dexterous hand (for example in the LinkerBot work), and is that mapping code shareable?

## Decision rule

- **Pick OriginFlow for T01 if** you already have a robot from another vendor, the booth confirms a live stream within the first hour, and your story is human-in-the-loop service work (hands-busy command, remote assist, effort-aware handover).
- **Avoid if** you need autonomy, navigation or manipulation from your main vendor, or if no real-time interface is offered — then OriginFlow adds risk without adding capability.

## Sources
- [OriginFlow official site](https://www.originflow.ai/)
- [TMTPost (EN), 2026-05-21](https://en.tmtpost.com/post/7997613)
- [QbitAI, 2026-08 (Chinese)](https://www.qbitai.com/2026/08/477094.html)
- [facebookresearch/emg2pose (GitHub)](https://github.com/facebookresearch/emg2pose)
- [facebookresearch/generic-neuromotor-interface (GitHub)](https://github.com/facebookresearch/generic-neuromotor-interface)
- [OriginFlow company profile (this repo)](../OriginFlow.md)

Note: the concepts are this guide's proposals, not OriginFlow offerings; other vendors' capabilities are indicative — check each vendor's own profile.
