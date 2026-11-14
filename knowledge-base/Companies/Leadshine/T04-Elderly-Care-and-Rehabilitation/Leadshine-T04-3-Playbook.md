---
type: challenge-playbook
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Leadshine Technology Co., Ltd. × T04 — Hackathon Playbook

⬆ [Leadshine Technology Co., Ltd. profile](../Leadshine.md) · [Brief](Leadshine-T04-1-Brief.md) · [Products and solutions](Leadshine-T04-2-Products-and-Solutions.md)

**Read first:** Leadshine brings parts, not robots. Every concept below assumes a dexterous hand (DH116S, DH116 or DH2116) is available to borrow — **confirm at the booth before committing**. Hard safety rule for all concepts: **the robot hand never grips a person** (worm-gear fingers can self-lock, side grip up to 50 N, no medical certification).

**Hour-zero checklist (same for every concept):**
1. Which hand, left or right, which bus (CAN FD / EtherCAT / RS485), tactile variant (-S / -M) or none?
2. Power supply (12–48 V; DH2116 24–60 V) and bus adapter included?
3. Get the SDK, ROS 2 workspace and URDF on a USB stick from the engineers — matching the unit's generation (before / after 2026-02-10).
4. Jog the hand with the Windows LHandPro GUI before writing any code.

## Solution approaches

### Concept 1 — Hand-rehab mirror coach (hand only, safest)

- **Problem → value:** hand and finger exercises after stroke, fracture or arthritis flare-ups are repetitive, and therapists are scarce. A robot hand that *demonstrates* each exercise, mirrors the patient's attempt and logs range of motion makes home or clinic practice measurable. No patient contact.
- **Hardware:** **DH116S** (or DH116) on a desk stand + laptop webcam. Optional: XREAL glasses for an AR overlay of target poses; D-Robotics RDK board as a stand-alone compute unit (SDK supports ARM).
- **Architecture / stack:**
  - Perception: camera hand-landmark tracking (any open-source hand tracker) → finger flexion angles.
  - Planning: map to the **6 active joints** (DH116S ranges: thumb swing 0–91°, thumb flex 0–59°, index / middle / ring 0–72°, little 0–74°); exercise state machine (demo → patient copies → score → next).
  - Control: LHandProLib Python API, or the ROS 2 Humble service node from `lhandpro_ws`; RViz2 / MJCF twin for development without hardware.
  - Compute: one Ubuntu 22.04 laptop.
- **48-hour plan:**
  - H0–6: hardware check with GUI; SDK hello-world; hand tracking running on webcam.
  - H6–24: retargeting to 6 DoF with smoothing and rate limits; 5 exercises (fist, finger opposition, pinch, spread, tendon glide); repetition counter.
  - H24–40: scoring (range of motion vs target, left / right comparison), session report, simple large-print UI with voice prompts; mirror-therapy mode (healthy hand tracked, robot shows the mirrored movement).
  - H40–48: rehearse, record backup video, write the therapist-report slide.
- **3-minute demo script:** (0:00) problem in one sentence + Leukerbad clinic context → (0:30) robot hand demonstrates an exercise, volunteer copies, counter and score update live → (1:30) mirror mode: robot follows the volunteer's hand in real time → (2:15) show the generated progress report → (2:40) what a clinic pilot would need.
- **Risks and fallbacks:** tracking jitter → filter and snap to exercise poses; bus bring-up fails → run the MJCF / RViz2 twin on screen; unit has no ROS 2 package (DH2116) → use the SDK directly.
- **Judging angles:** *Innovation* moderate (robotic mirror therapy at low cost); *Technical depth* retargeting + scoring; *Impact* clear clinical workflow, measurable; *Leukerbad* direct link to local rehabilitation clinics and spa guests.

### Concept 2 — Gentle hand-over assistant (hand + force-controlled arm)

- **Problem → value:** people with weak grip or limited reach need objects (cup, pill box, glasses, phone) brought and handed over safely. The hard part is the hand-over itself: hold securely, release exactly when the person takes it.
- **Hardware:** **DH116-M** (tactile) or DH116S-S / -M on a **Flexiv Rizon** or **ROKAE xMate** arm (both listed with force / torque sensing). Depth camera for object and hand detection.
- **Architecture / stack:**
  - Perception: object detection for 3–4 known items; detect the person's open hand.
  - Planning: grasp primitives per object (power, pinch, hook) + pick → present → wait → release sequence.
  - Control: arm via its vendor SDK; hand via LHandProLib / ROS 2 service; release triggered by tangential-force change at the fingertips (or arm wrist force if the hand has no sensors). Speech in / out for commands and confirmation.
  - Compute: laptop; arm controller as supplied.
- **48-hour plan:**
  - H0–6: confirm arm + hand availability, flange adapter (3D-print if needed), power and cable routing; both devices moving independently.
  - H6–24: grasp primitives tuned on real objects; pick-and-present trajectory; read tactile data.
  - H24–40: pull-to-release logic, speed limits near the person, voice loop, "medication time" reminder scenario.
  - H40–48: reliability runs (target 9 / 10), demo rehearsal, backup video.
- **3-minute demo script:** (0:00) spoken request "bring my pills" → (0:30) robot picks the pill box, presents it at a fixed safe zone → (1:10) volunteer takes it; hand releases on pull, not before → (1:40) repeat with a cup; show the live force plot → (2:20) safety rules and limits.
- **Risks and fallbacks:** no flange adapter → clamp-mount and reduce payload; no tactile variant → use arm force sensing or a timed release with spoken confirmation; **IP30** → dry, empty containers only; never present objects toward the face.
- **Judging angles:** *Innovation* tactile release on a low-cost hand; *Technical depth* multi-vendor integration + force logic; *Impact* daily-living assistance; *Leukerbad* hotel / clinic room service for guests with limited mobility.

### Concept 3 — Muscle-signal (EMG) controlled assistive hand

- **Problem → value:** amputees and people with paresis train for months to control a prosthesis or assistive gripper. A bench "prosthesis trainer" lets them practise muscle-signal control with a realistic five-finger hand and gives therapists objective feedback.
- **Hardware:** **DH2116** (finger-level realism) or DH116S + **OriginFlow** EMG capture (see its profile for what is available). Optional XREAL display for feedback.
- **Architecture / stack:**
  - Perception: forearm EMG stream → gesture / intent classifier (4–6 classes: rest, fist, pinch, point, open, tripod), calibrated per user in about 2 minutes.
  - Planning: intent → grasp primitive, with proportional closing from signal amplitude.
  - Control: LHandProLib (DH2116: motor commands 0–4095, mapping in the manual); game-like training tasks with scoring.
  - Compute: laptop.
- **48-hour plan:**
  - H0–6: confirm EMG data access (format, rate, SDK) and hand control separately.
  - H6–24: per-user calibration + classifier; map classes to hand poses; latency measurement.
  - H24–40: proportional control, training game (pick the right grip for a shown object), accuracy and latency dashboard.
  - H40–48: test on 3 different people, rehearse, backup video.
- **3-minute demo script:** (0:00) who needs this → (0:30) volunteer calibrates live (shortened) → (1:10) hand follows muscle intent: open, pinch, fist → (1:50) training game with score → (2:30) accuracy / latency numbers and next steps.
- **Risks and fallbacks:** EMG stream not accessible in real time → fall back to camera hand tracking (Concept 1 pipeline) and present EMG as recorded data; classifier unstable → reduce to 3 classes; DH2116 unavailable → use DH116S with 6 DoF.
- **Judging angles:** *Innovation* high (cross-vendor human-machine interface); *Technical depth* signal processing + ML + control; *Impact* prosthetics and neuro-rehab training; *Leukerbad* rehab-clinic use case.

### Concept 4 — Bench-top single-joint rehab exerciser with a PJ3 module (most ambitious)

- **Problem → value:** wrist, elbow or ankle mobilisation needs slow, repeatable assisted motion. A compact actuator with adjustable assistance / resistance could become a low-cost exerciser.
- **Hardware:** one **PJ3** module (PJ3-60, 9.5 N·m rated, is the sensible size) + 3D-printed handle and base + USB-CAN adapter + emergency stop cutting power. Optional EMG or camera feedback.
- **Architecture / stack:** joint position / velocity / current feedback → assist-as-needed controller (follow a slow trajectory, yield when resistance exceeds a limit) → session logging. Control over CAN FD using Leadshine's protocol. Compute: laptop.
- **Go / no-go gate (H0–2):** proceed **only if** Leadshine engineers provide the protocol document, confirm a torque / current control mode and backdrivability, and lend an adapter. No public SDK exists. Otherwise switch to Concept 1.
- **48-hour plan:**
  - H0–6: gate check; spin the module; read position and current.
  - H6–24: mechanical fixture; torque-limited trajectory mode; hard software limits on angle, speed and torque.
  - H24–40: assist-as-needed and resistance modes; logging and progress chart.
  - H40–48: safety review, rehearsal, video.
- **3-minute demo script:** (0:00) need → (0:30) passive mobilisation: the handle moves a **dummy limb or test weight** → (1:20) a team member holds the handle with torque capped low to show yield-on-resistance → (2:10) session chart → (2:40) path to a certified device.
- **Risks and fallbacks:** protocol not available → no demo; unknown backdrivability and no certified safety functions → keep torque limits very low, hardware e-stop, mechanical end stops, **demo on a dummy first**; judges may see it as off-the-shelf motor control → emphasise the adaptive controller and data.
- **Judging angles:** *Innovation* moderate; *Technical depth* high if force control works; *Impact* large market but long regulatory path; *Leukerbad* rehab clinics.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| DH116S + camera only | Mirror coach (Concept 1) | **Low** — one device, one SDK |
| DH116-M + Flexiv Rizon or ROKAE xMate | Force-aware hand-over, simple feeding-aid or dressing-aid motions | **Medium** — flange adapter, two SDKs, cable routing |
| DH hand + OriginFlow EMG | Muscle-controlled assistive hand / prosthesis trainer | **Medium** — depends on real-time EMG access |
| DH hand + XREAL glasses | AR-guided therapy overlay, or first-person tele-care view | **Medium** — separate app; loose coupling over network |
| DH hand + Galaxea R1 / AGIBOT G1 / Unitree G1 (host robot) | Mobile fetch-and-hand-over, medication round | **High** — replacing a host robot's end-effector in 48 h is risky; only if the vendors already have an adapter and driver |
| DH hand + D-Robotics RDK X5 | Self-contained edge unit (no laptop) | **Low–medium** — SDK lists ARM support; verify the Linux build runs |
| DH hand + Dobot desktop / CR arm | Low-cost reach for table-top demos | **Medium** — check payload (hand 359–850 g plus object) |
| PJ3 + coprod modular hardware | Custom assistive joint or fixture | **High** — no public PJ3 protocol |

Note: WUJI also offers a dexterous hand on site — compare availability, SDK maturity and tactile options before choosing.

## Questions to ask the Leadshine Technology Co., Ltd. engineers on site

1. Which hands can teams borrow (model, left / right, bus, tactile -S / -M), how many, and for how long?
2. Can you give us the current LHandProLib SDK, ROS 2 workspace and URDF / MJCF on a USB stick — and which generation does this unit need?
3. Does the SDK expose **per-finger force / current limits** and raw tactile values at what update rate? Is there a compliant or torque-limited grip mode?
4. Are the fingers self-locking when powered off? How do we open the hand in an emergency?
5. Do you have a flange adapter for the arms on site (Flexiv, ROKAE, Dobot, Unitree, AGIBOT), and a suitable power supply and USB-CAN FD adapter?
6. Is there a ROS 2 package for the DH2116, and is the data glove (6248XL) available with a real-time interface?
7. For PJ3: can you share the CAN FD protocol, confirm torque / current control mode, backdrivability and peak torque, and lend a module with an adapter?
8. Has any customer used your hands or joints in care, rehabilitation, prosthetics or exoskeletons that we may cite?

## Decision rule

- **Pick Leadshine Technology Co., Ltd. for T04 if** a hand is confirmed available with SDK and power in the first hour, and your idea centres on the *hand itself* (therapy mirroring, hand-over, EMG control) — alone on a desk or on a force-controlled arm from another vendor.
- **Avoid if** you need a complete robot, mobility, autonomy or patient-contact force control out of the box, or if your plan depends on the PJ3 / HJ2 joint modules without a protocol in hand.

## Sources

- [Leadshine company profile](../Leadshine.md)
- [DH116S user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf)
- [DH116 / DH116P user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf)
- [DH2116 user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH2116_Series_Dexterous_Hand_User_Manual.pdf)
- [DH116S LHandPro ROS2 example project description (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html)
- [DH116S series product page](https://en.leadshine.com/robots/dextrous-hands/dh116s-series.html)
- [DH2116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [PJ3 series product page](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html)
- [FAIR plus 2026 recap (Leadshine store blog)](https://store.leadshine.com/blogs/news/leadshine-dexterous-hands-and-joint-modules-shine-at-the-shenzhen-fair-plus-2026)
- [Leadshine at CES 2026 — supply-chain release (PR Newswire Asia)](https://en.prnasia.com/releases/global/leadshine-achieves-great-success-at-ces-2026-entering-us-and-european-robotics-supply-chain-518892.shtml)
