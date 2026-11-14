---
type: challenge-playbook
company: "WUJI"
slug: WUJI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# WUJI × T03 — Hackathon Playbook

⬆ [WUJI profile](../WUJI.md) · [Brief](WUJI-T03-1-Brief.md) · [Products and solutions](WUJI-T03-2-Products-and-Solutions.md)

**Read first:** WUJI is a **2/5 fit** for T03. It has no sustainability track record and no arm. The concepts below are the credible niches: tasks on objects **made for human fingers**, where a gripper fails, plus human-demonstration capture. All use **clean, dry mock items** (hands are IP40 / beta, pads and cables are fragile). Official T03 directions these map to: T03.1 smart waste sorting, T03.6 smart recycling and resource optimization, T03.3 energy-efficient robotic systems.

## Solution approaches

### Concept 1 — "Hands that teach": disassembly demonstration recorder (glove only, hand as mirror)

- **Problem → value:** Repair and disassembly for reuse are manual because every product is different. Recording *how* a skilled person does it (finger poses + **526-point** pressure map) is the missing dataset for automating it. Value: a reusable, labelled demonstration set and a live grip-effort view per step.
- **Hardware:** Wuji Glove (1–2). Optional: Wuji Hand on a desk stand mirroring the operator live. Optional: webcam for step video. No arm needed.
- **Architecture / stack:** glove streams (tactile, fingertip poses, skeleton, IMU) → Wuji SDK on a laptop → `TopicRecorder` to one **MCAP per episode** → small Python step-segmenter (pressure peaks + pose change) → dashboard (time per step, peak force per step, parts recovered). Mirror path: glove skeleton → `RetargetSession` → hand joint targets.
- **48-hour plan:**
  - H0–6: borrow glove, install SDK, verify streams, test tracking next to your actual items (metal check).
  - H6–24: recording script with episode start / stop, 3 item types (for example remote control, small power adapter, plastic bottle with cap and label), 10 episodes each.
  - H24–40: step segmentation, dashboard, live hand mirror.
  - H40–48: rehearse, record backup video, write impact estimate.
- **3-minute demo script:** 0:00 problem (repair is unscalable without data) → 0:30 operator disassembles one item with glove, hand mirrors it, pressure map live → 1:45 dashboard shows auto-segmented steps and the stored episode → 2:30 how this dataset feeds a robot policy; numbers recorded so far.
- **Risks and fallbacks:** EMF tracking degrades within 3 cm of metal → choose mostly plastic items, or rely on tactile + IMU; no hand available → show the skeleton in a 3-D viewer or MuJoCo with `wuji-description` models.
- **Judging angles:** innovation medium (data angle is fresh for T03) · technical depth medium · impact indirect (enabler, not a robot doing work — say so) · Leukerbad: repair-café / hotel maintenance framing. **Weakness:** thin "robot acts on the world" element.

### Concept 2 — Teleoperated reuse cell: human fingers, robot hand, scripted arm

- **Problem → value:** Small e-waste and multi-material packaging need finger-level work (unclip a cover, pull a battery, peel a connector) before parts can be reused or recycled cleanly. A teleoperated dexterous cell keeps the worker away from the item and logs every action as training data for later autonomy.
- **Hardware:** Wuji Glove + Wuji Hand (gen 1 for known force limits, Hand 2 for compliance) + partner arm (Flexiv Rizon, ROKAE xMate or Dobot CR). Fixture or vice to hold the item. Camera over the bench. Optional XREAL glasses as the operator's remote view.
- **Architecture / stack:** fingers: glove skeleton → `RetargetSession` → hand (Hand 2 in position mode, as in the official teleop examples). Arm: **pre-taught poses** stepped by a foot pedal or key (do not attempt full arm teleop on day 1; the glove tracks fingers, not a global wrist pose — confirm with WUJI). Logging: MCAP for hand + glove, plus arm joint log and video. Compute: one laptop; arm on its own controller.
- **48-hour plan:**
  - H0–6: secure arm + hand slots, mount hand (adapter flange, cable slack, payload check), glove → hand teleop working on the desk.
  - H6–24: teach 5–8 arm poses around the fixture; complete one item end-to-end by teleop; add recording.
  - H24–40: second item type, sorted output bins with a counter, operator view; stretch: replay a recorded finger trajectory autonomously for one step.
  - H40–48: reliability runs, backup video, impact slide.
- **3-minute demo script:** 0:00 one-line problem → 0:20 operator (standing apart) opens the item, extracts the battery or board, drops parts into "reuse" and "recycle" bins → 2:00 show logged episode and the one step that already replays without the human → 2:30 metric: parts recovered per item, minutes per item, path to autonomy.
- **Risks and fallbacks:** mounting eats the first day → fall back to hand on a stand with items handed in by a person; Hand 2 position mode (Beta) unstable → use gen 1; fragile clips need more than fingertip force → pre-loosen and say so; glove near metal → webcam + MediaPipe keypoints as alternative input to the same retargeting call.
- **Judging angles:** innovation good (dexterous circular-economy cell) · technical depth good (retargeting, multi-device sync, data pipeline) · impact plausible but must be argued per item · Leukerbad: a remote alpine village ships waste down the valley; local repair / pre-sorting of hotel and clinic e-waste is a reasonable framing (your claim to substantiate).

### Concept 3 — Multi-material separator: vision + grasp primitives (autonomous)

- **Problem → value:** Many recyclables are rejected or down-cycled because materials are still joined: metal lid on a glass jar, cap on a bottle, sleeve on a container. Separation is a twist / pinch / peel task, which is where a multi-finger hand beats a gripper.
- **Hardware:** Wuji Hand (gen 1: **15 N** fingertip, max grasp diameter **100 mm**) or Hand 2 on a partner arm; a second arm with a simple gripper or a fixed clamp to hold the container; RGB-D camera; vision on a laptop GPU or D-Robotics RDK board.
- **Architecture / stack:** camera → detector / classifier (item class + pose) → task selector (which primitive) → arm motion to pre-grasp (vendor SDK or MoveIt) → hand **grasp primitives** written as joint-target sequences (power grasp, tripod pinch, cap-twist with re-grasp) → verify by joint effort / position readback → drop into the correct stream bin.
- **48-hour plan:**
  - H0–6: mount hand, hand-eye calibration, one power grasp from a fixed pose.
  - H6–24: tune the cap-twist primitive on one jar size by hand-coded trajectories (use teleop to find good finger poses, then freeze them); detector for 3–4 classes.
  - H24–40: integrate detect → pick → clamp → twist → sort; success-rate logging.
  - H40–48: narrow to the items that work, demo polish, energy-per-item measurement.
- **3-minute demo script:** 0:00 show a jar with lid = contaminated stream → 0:20 robot detects, clamps, unscrews, sorts lid and jar separately; repeat with a bottle → 2:00 success rate over N trials and energy per item → 2:30 what scales (more primitives, learned from glove demos).
- **Risks and fallbacks:** cap torque exceeds what fingers deliver (Hand 2 forces unpublished) → pre-loosen caps or switch to snap lids; re-grasp twist unreliable → rotate with the arm wrist while the hand only holds; one arm only → fixed clamp; perception late → fixed item positions.
- **Judging angles:** innovation high · technical depth high · impact clear and countable (items correctly separated) · Leukerbad: glass and packaging volume from hotels and restaurants. Completeness is the risk — scope to **one** item family.

### Concept 4 — Retrofit-free energy round: a robot hand for human interfaces (most ambitious)

- **Problem → value:** Old hotel and clinic buildings waste heat through radiators left on, windows tilted open and lights on in empty rooms. Smart-building retrofits are costly; a mobile robot that operates the **existing** knobs, handles and switches needs no retrofit. Sustainability metric: kWh avoided per round (estimate, state assumptions).
- **Hardware:** Wuji Hand on a wheeled dual-arm mobile manipulator (Galaxea R1 family, Galbot G1, AGIBOT G1 / G2 or similar on site), its cameras; optional thermal camera. Mock-up wall with a radiator thermostat head, window handle and light switch.
- **Architecture / stack:** navigation and arm motion from the host robot's stack → detector for fixture type and state → per-fixture hand primitive (wrap-and-twist for thermostat head, hook-and-turn for handle, single-finger press for switch), compliant with Hand 2 MIT gains → log each action and estimated saving. Compute on the host robot or a laptop.
- **48-hour plan:**
  - H0–6: confirm a host robot will accept a third-party hand (mechanical + power + network); if not, switch to a fixed arm in front of the mock-up.
  - H6–24: build mock-up wall; three primitives working from fixed poses.
  - H24–40: perception of fixture state; base repositioning between fixtures (or manual repositioning).
  - H40–48: run-through, savings model, video.
- **3-minute demo script:** 0:00 "empty room, heating on, window tilted" → 0:20 robot turns the thermostat down, closes the window, switches the light off → 2:00 log and estimated kWh per room per night → 2:30 why a hand (works with any existing fixture) and robot energy cost vs saving.
- **Risks and fallbacks:** integration on a mobile robot not allowed or too slow (likely) → fixed-arm mock-up demo; a gripper could do some of this → emphasise fixture variety and show at least one fixture a gripper cannot handle; net-energy question → measure hand and arm power.
- **Judging angles:** innovation high · real-world impact strong narrative for an alpine spa town with heated buildings · technical depth depends on how much is autonomous · highest integration risk of the four.

**Stretch for any concept — learned skill:** `wuji-openpi` (pi0 / pi0.5) is a real path but ships **no checkpoints or data**, expects a dual-arm rig, an NVIDIA GPU and a ROS 2 Humble deployment chain. Within 48 hours a replayed trajectory or a small imitation policy on one fixed step is more realistic than VLA fine-tuning.

**Energy figure for the pitch (any concept):** put a DC power meter on the hand's 12 V supply, or on gen 1 integrate per-joint current × bus voltage from the SDK as an approximation. Gen 1 static draw is **12 W** (official); Hand 2 typical draw is not published.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| WUJI Glove + Hand + **Flexiv Rizon** | Force-controlled arm + dexterous hand: compliant disassembly cell (Concepts 2, 3) | Medium — custom adapter plate, payload check, two SDKs |
| WUJI Glove + Hand + **ROKAE xMate** or **Dobot CR** | Same cell on a more conventional cobot | Medium |
| WUJI Hand + **Galaxea R1 / Galbot G1 / AGIBOT G1-G2** | Mobile dexterous manipulation for the energy round (Concept 4) | High — third-party end effector on a vendor robot; needs vendor approval |
| WUJI + **D-Robotics RDK** | Low-power edge vision for item classification (supports the "low energy" story); SDK has Linux arm64 builds, hand control from an RDK board ⚠️ unverified | Low–medium |
| WUJI Glove + **XREAL** glasses | Remote operator view for teleoperated cell | Low–medium |
| WUJI Glove + **OriginFlow** (EMG capture) | Richer human-demonstration dataset: muscle activity + tactile + pose (Concept 1) | Medium — time sync between two capture systems |
| WUJI Hand + **Unitree Z1** or other light arm | Compact demo cell | Medium–high — check payload: hand alone is about 0.6–0.9 kg |

## Questions to ask the WUJI engineers on site

1. Which units are here (Hand gen 1, Hand 2, gloves, left / right) and how is access booked?
2. Which flange adapters did you bring, and which arms on site have you already mounted the hand on?
3. Hand 2: what fingertip force, payload and wrist load / shock limits should we design for? What must we never do?
4. Can the hand twist a jar lid or bottle cap? Is there an example of a re-grasp or twist primitive?
5. Does the glove give a wrist pose usable for arm teleoperation, or fingers only? How does tracking behave next to metal parts in practice?
6. For glove → Hand 2 teleop, is position mode (Beta) stable enough, or do you recommend MIT mode with specific `kp` / `kd`?
7. Can the pads / skin be protected (thin over-glove) or cleaned if they touch dusty or sticky items?
8. Is there a ROS 2 Humble / Jazzy Docker image, and can you share any base checkpoint or demo dataset for `wuji-openpi`?

## Decision rule

- **Pick WUJI for T03 if** your idea hinges on finger-level manipulation of objects made for human hands (disassembly, cap / lid separation, knobs and handles), you have secured a partner arm in the first hours, and you are happy with a teleoperated or semi-autonomous demo on clean mock items.
- **Avoid if** you want bulk waste sorting, litter picking, outdoor or wet work, environmental monitoring, or a single-vendor autonomous robot — a gripper arm, quadruped or mobile manipulator from another vendor gets you there faster.

## Sources

- [WUJI profile (this repo)](../WUJI.md)
- [T03 track overview (this repo)](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
- [Wuji Docs — English index](https://docs.wuji.tech/_llms/en.txt)
- [Wuji Hand 2 (2.2 Beta) product introduction](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md)
- [Wuji Hand 2 mechanical integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration.md)
- [Wuji Hand 2 effort and MIT parameters](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/effort-and-mit.md)
- [Wuji Hand (gen 1) product introduction](https://docs.wuji.tech/docs/en/wuji-hand/v1/overview.md)
- [Wuji Glove product introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md)
- [Wuji SDK hand retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md)
- [Wuji SDK data recording](https://docs.wuji.tech/docs/en/wuji-sdk/latest/data-recording.md)
- [GitHub: wuji-technology repositories](https://github.com/orgs/wuji-technology/repositories)
- [GitHub: wuji-openpi](https://github.com/wuji-technology/wuji-openpi)
