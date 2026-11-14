---
type: challenge-playbook
company: "coprod Inc."
slug: coprod
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# coprod Inc. × T04 — Hackathon Playbook

⬆ [coprod Inc. profile](../coprod.md) · [Brief](coprod-T04-1-Brief.md) · [Products and solutions](coprod-T04-2-Products-and-Solutions.md)

**Before you commit (10 minutes at the booth):** how many axes can we get, is there a motor attached, can we have the `cosystem` package and one working example today, and will a founder help us bring up the bus? If any answer is "no", use coprod only as an add-on or pick another vendor.

**Safety rules for every concept:** prototype, not a medical device. Healthy volunteers or a dummy limb only · hard software torque cap · mechanical end stops · e-stop within reach (co:power power logic) · no Safe Torque Off module exists yet.

All concepts are our proposals — coprod has shown nothing in this domain.

## Solution approaches

### Concept 1 — Rehab Dial (one-axis haptic exercise trainer)
- **Problem → value:** home and clinic exercise for wrist / forearm after stroke or fracture is repetitive and unmeasured. A motorised handle gives adjustable resistance or assistance and an objective log for the therapist.
- **Hardware:** 1× co:act (🧪 if available) **or** co:motion + motor · co:power · bench clamp + 3D-printed handle. Optional: XREAL glasses for a game overlay; D-Robotics RDK for a camera posture check.
- **Architecture / stack:** encoder angle / velocity → Python state machine (guided range of motion = position mode with low gain · resist = torque mode with virtual spring / damper · assist-as-needed = torque grows with tracking lag) → `cosystem` setpoints at up to 1 kHz. Compute: one laptop / mini-PC on real-time Linux as EtherCAT master; dashboard (web UI) on the same machine. Effort metric from commanded torque (measured-torque readback is not public — ask).
- **48-hour plan:** **H0–6** get kit + SDK, spin the axis, verify torque mode and e-stop · **H6–24** three exercise modes, torque cap, handle and mount · **H24–40** dashboard (range of motion, repetitions, smoothness), simple game, session report · **H40–48** tune feel, rehearse, record backup video.
- **3-minute demo script:** 0:00 problem and one patient story · 0:30 volunteer does guided mode · 1:15 switch to resist, then assist-as-needed, live plots · 2:15 therapist view: progress over sessions, exported report · 2:40 path to a low-cost home device for Leukerbad rehab guests.
- **Risks and fallbacks:** no kit / no SDK → run the same control logic on one joint of a force-controlled arm from Flexiv or ROKAE (inference: both offer joint torque control). Jerky feel → lower gains, add damping. No torque readback → use tracking error as effort proxy.
- **Judging angles:** innovation: low (known device class) · technical depth: real-time haptics · impact: measurable home rehab · Leukerbad: rehab clinics and thermal-spa recovery guests.

### Concept 2 — Alpine Rollator (slope-aware walking aid)
- **Problem → value:** on steep streets a rollator runs away downhill and is heavy uphill. Motorised wheels brake automatically downhill, push gently uphill and raise an alarm on a tip-over.
- **Hardware:** 2× co:motion + wheel motors · co:sense · co:power · co:battery · a standard rollator (borrow or buy locally). Motors: ask coprod; Leadshine motors are an option ⚠️ compatibility unverified.
- **Architecture / stack:** co:sense pitch / roll → slope estimate → wheel controller (downhill: speed cap by damping torque · uphill: assist torque proportional to slope · handle release: controlled braking) → `control_vel` / torque commands. IMU roll or shock spike → brake + caregiver alert (phone push). Compute: small Linux PC on the frame. This mirrors the home-page API sample (wheels + IMU + supply voltage).
- **48-hour plan:** **H0–6** kit check, pick motors, bench-run two wheels with IMU · **H6–24** mount wheels and electronics, slope-based assist / brake · **H24–40** tip-over detection, alert app, battery telemetry, ramp tests · **H40–48** indoor ramp demo polish, backup video on a real Leukerbad slope.
- **3-minute demo script:** 0:00 video of a rollator rolling away on a village slope · 0:30 push the aid up a ramp, show assist · 1:15 let go on the downslope, it holds · 2:00 tip it, alert arrives on a phone · 2:30 cost and retrofit story.
- **Risks and fallbacks:** mechanical integration eats the time → demo on a small cart or bench ramp. No user-presence sensing (IO board is roadmap only) → detect push from wheel motion, or add a separate microcontroller. Weather: no IP rating public → demo indoors.
- **Judging angles:** innovation: medium · technical depth: mechatronics + control · impact: fall prevention, independence · Leukerbad: **strong** — steep terrain, snow, many elderly guests.

### Concept 3 — Intent-driven assist joint (EMG + actuator)
- **Problem → value:** weak patients cannot start a movement alone; assistance that triggers on their own muscle intent trains recovery better than passive motion.
- **Hardware:** 1× co:act or co:motion + motor · co:power · arm rest with elbow / wrist hinge · **OriginFlow** EMG capture (⚠️ real-time streaming and SDK access unverified — check their profile and booth).
- **Architecture / stack:** EMG envelope → intent detector (threshold or small classifier) → assist torque profile that fades as the user contributes → `cosystem` torque setpoints. Encoder gives range and speed for the log. Compute: laptop as EtherCAT master; EMG processing in a separate process.
- **48-hour plan:** **H0–6** verify both vendors' data paths independently · **H6–24** hinge rig, torque-mode assist with manual trigger, EMG onset detection offline · **H24–40** close the loop, assist-as-needed, safety limits, dashboard · **H40–48** calibration routine under one minute, rehearsal.
- **3-minute demo script:** 0:00 why intent matters · 0:30 strap on, 30-second calibration · 1:00 user thinks "lift", joint helps; show EMG and torque traces · 2:00 reduce assistance live as the user "recovers" · 2:30 roadmap: home device, more joints.
- **Risks and fallbacks:** EMG stream not accessible in real time → trigger from encoder micro-motion instead. Two immature SDKs at once → freeze Concept 1 as the safe core and add EMG last.
- **Judging angles:** innovation: high · technical depth: bio-signal + real-time control · impact: neuro-rehab · Leukerbad: rehab clinics.

### Concept 4 — Mirror and tele-rehab pair (bilateral two-axis link)
- **Problem → value:** therapists are scarce in mountain regions. Two coupled handles let the healthy hand drive the affected one (mirror therapy), or let a therapist feel and guide a patient from elsewhere.
- **Hardware:** 2× co:act or co:motion + motor · co:power · two handles. Optional: XREAL glasses for the therapist view.
- **Architecture / stack:** leader and follower on one EtherCAT bus → bilateral position-force coupling at 1 kHz (the deterministic bus is what makes this stable) → scaling and safety limits. Stretch: split across two hosts over the network with position-only coupling plus damping to tolerate delay.
- **48-hour plan:** **H0–6** two axes running, unilateral follow · **H6–24** bilateral coupling, scaling, limits · **H24–40** mirror-therapy mode, session logging, optional network split · **H40–48** stability margins, rehearsal.
- **3-minute demo script:** 0:00 therapist shortage · 0:30 mirror mode: left hand moves right hand · 1:15 judge holds the follower and feels resistance mirrored back · 2:00 remote mode across the room / network · 2:30 link to coprod's planned teleoperation platform.
- **Risks and fallbacks:** needs two axes — may exceed available kit → fall back to Concept 1. Coupling instability → lower stiffness, add damping. Network delay → show local link only.
- **Judging angles:** innovation: medium-high · technical depth: **highest** (bilateral control) · impact: tele-care reach · Leukerbad: remote valley, clinic-to-home follow-up.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| coprod axis + **OriginFlow** EMG | Intent-triggered assistance (Concept 3) | High — two early-stage SDKs |
| coprod axis + **XREAL** glasses | AR exercise game / therapist overlay | Low — only shares data over the network |
| coprod axis + **D-Robotics** RDK | Camera posture check, voice prompts, on-device UI | Medium — whether an RDK can also host the EtherCAT master is ⚠️ unverified |
| coprod wheels + IMU on a rollator + **SKYLANDX** scan | Slope map of Leukerbad paths to pre-set assist levels | Medium, mostly offline |
| coprod add-on axis on a mobile manipulator (**Galaxea**, **Galbot**, **UniX AI**) | Custom actuated tray, lift or dispenser for a care robot | High — mechanical and two control stacks; rarely worth it in 48 h |
| **Flexiv** / **ROKAE** arm as main robot, coprod co:sense on the patient side | Arm does physio motion, IMU measures limb response | Medium — wired IMU limits placement |

## Questions to ask the coprod Inc. engineers on site
1. How many co:motion axes (and any co:act units) can one team have, and do they come with motors and a power supply?
2. Can we install the `cosystem` package today, and is there an example for torque mode / impedance control?
3. Can the API read back **measured torque or motor current**, and at what rate?
4. What does the host need — which Linux, real-time kernel, network card? Does it run on a laptop?
5. What happens on e-stop with co:power — is torque removed or is braking controlled? What is the safe way to cap torque?
6. How backdrivable is co:act when unpowered and in zero-torque mode?
7. Is there a ROS 2 bridge today?
8. Will a founder sit with us for bus bring-up in the first six hours?

## Decision rule
- **Pick coprod Inc. for T04 if** your idea is a custom one- or two-axis device (exercise trainer, assist joint, powered rollator), your team has mechatronics and real-time control skills, and coprod confirms kit + SDK + hands-on support in the first hour.
- **Avoid if** you need a ready robot, perception or AI out of the box, want to touch real patients, or cannot get hardware and software in hand by H2.

## Sources
- [coprod — official site (API sample, system specs)](https://coprod.co/)
- [coprod — products and roadmap](https://coprod.co/products.html)
- [coprod — systems (co:dodo, planned systems)](https://coprod.co/systems.html)
- [Venture Kick — coprod receives CHF 40,000 (2 Apr 2026)](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)
- [coprod Inc. company profile (internal)](../coprod.md)
