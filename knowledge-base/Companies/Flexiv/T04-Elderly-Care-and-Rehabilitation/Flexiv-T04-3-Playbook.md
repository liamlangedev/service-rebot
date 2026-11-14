---
type: challenge-playbook
company: "Flexiv Robotics"
slug: Flexiv
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Flexiv Robotics × T04 — Hackathon Playbook

⬆ [Flexiv Robotics profile](../Flexiv.md) · [Brief](Flexiv-T04-1-Brief.md) · [Products and solutions](Flexiv-T04-2-Products-and-Solutions.md)

**Assumed kit:** one Rizon 4 or 4s + Grav gripper, Hesper controller, wired LAN to your laptop, RDK license active (all ⚠️ unverified — confirm at the booth before committing).

**Ground rules for any body-contact idea**
- Develop on a mannequin, foam roller or silicone limb. Put a person in the loop only with the Flexiv engineers' and organisers' explicit OK.
- Cap contact force, stiffness and speed in software; one team member holds the E-stop at all times.
- Never work near head or neck; never create a pinch point; the person must always be able to pull away.
- Say "wellness / research demo", never "medical device".

**API note:** RDK names below such as Cartesian impedance setting, force-control axis selection and max-contact-wrench limit are from the RDK v1.x / v2.x family as remembered ⚠️ unverified — check the exact calls in the installed version's examples (`intermediate4_non_realtime_cartesian_motion_force_control.py` is the one to open first).

## Solution approaches

### Concept 1 — Spa Hand: contour-following massage with a pressure dial
- **Problem → value:** Leukerbad's spas and clinics depend on scarce therapist hours. A robot that delivers a repeatable, pressure-controlled routine frees therapists for assessment and complex cases. Closest to what Flexiv already proves with Mello, so lowest technical risk.
- **Hardware:** Rizon 4s (or 4) + a soft 3D-printed or silicone massage tip held in Grav or bolted to the flange · one RGB-D camera (RealSense or similar — bring your own) · mannequin torso or foam forearm.
- **Architecture / stack:**
  - Perception: RGB-D camera → open-source body-pose / segmentation on the laptop → pick a region (upper back, forearm, calf) → project a stroke path onto the depth surface.
  - Planning: path as Cartesian waypoints; tool axis normal to the surface; no-go zones (spine line, joints).
  - Control: RDK non-real-time Cartesian motion-force mode — position control along the path, force control on the tool axis (start **5–15 N**), low stiffness sideways, hard cap on contact wrench.
  - UI: tablet slider for pressure, "softer / stop" voice or button; live force plot.
  - Compute: laptop over wired LAN; no GPU strictly needed.
- **48-hour plan:**
  - H0–6: confirm license and RDK version; run display-states and motion-force examples; touch a foam block at constant force.
  - H6–24: hand-taught path (free drive) replayed with force on the tool axis; add pressure slider and force plot; safety caps.
  - H24–40: camera-based path generation and no-go zones; second routine (calf or forearm); comfort feedback loop (pain button lowers force).
  - H40–48: rehearse, record backup video, tune for the demo surface.
- **3-minute demo script:** (0:00) the therapist-shortage story in a spa town → (0:30) camera highlights the region and draws the stroke path on screen → (1:00) robot strokes the mannequin; live force trace sits flat at the set value over bumps → (1:45) judge moves the slider, pressure changes instantly; someone shifts the mannequin, robot follows → (2:20) press "too much": robot backs off → (2:40) what a therapist dashboard and a Mello-class product would add.
- **Risks and fallbacks:** camera calibration eats time → fall back to hand-taught paths (still a valid demo). No wrist F/T sensor → whole-arm sensing at 0.1 N is still sufficient. Human contact not allowed → mannequin only, plus a force-plate "feel it yourself" pad for judges' hands if approved.
- **Judging angles:** innovation medium (Mello exists) — differentiate with personalisation and pain feedback · technical depth: hybrid motion-force control on a sensed surface · impact: therapist time · Leukerbad relevance: **very high**.

### Concept 2 — Rehab Partner: therapist-taught, assist-as-needed exercise trainer
- **Problem → value:** after stroke, fracture or joint replacement, patients need many repetitions of guided arm movement; therapists can supervise only a few. The robot repeats the therapist's own movement, helps only as much as needed, and produces objective progress data (force, range of motion, smoothness).
- **Hardware:** Rizon 4s (or Rizon 10 for more support force) + a padded handle or forearm cuff gripped by Grav (must release under load — magnetic or friction breakaway). Optional: OriginFlow EMG on the patient's arm; XREAL glasses for the patient.
- **Architecture / stack:**
  - Teach: therapist hand-guides the arm in free drive; record the Cartesian trajectory through RDK.
  - Control: replay as a compliant "virtual tunnel" using joint or Cartesian impedance — soft along the path, stiffer off it. Three modes: **passive** (robot moves the arm), **active-assist** (robot adds help when the patient stalls), **resist** (robot opposes with a set force).
  - Sensing: the arm itself is the sensor — log end-effector force and pose every cycle; compute range of motion, peak force, patient-contributed work, tremor / smoothness index.
  - Adaptation: lower assistance when the patient's contributed force rises (optionally fused with EMG effort).
  - Output: per-session report and trend chart for the therapist; simple game-like visual target for the patient.
  - Compute: laptop; Python non-real-time loop is enough for slow rehab motions.
- **48-hour plan:**
  - H0–6: free drive record + impedance replay of one trajectory, no person attached.
  - H6–24: three modes, force / speed caps, breakaway handle, data logging.
  - H24–40: assist-as-needed adaptation, session report, patient visual; optional EMG or AR add-on.
  - H40–48: test with team members at low force, rehearse, backup video.
- **3-minute demo script:** (0:00) one therapist, twelve patients → (0:30) "therapist" teaches a shoulder-flexion arc by hand in 10 seconds → (1:00) "patient" holds the handle: passive mode, then active-assist — screen shows robot help dropping as the patient pushes → (1:50) resist mode for strengthening → (2:20) auto-generated session report with range-of-motion and effort trend → (2:40) safety design and clinic path.
- **Risks and fallbacks:** person attached to a robot is the main safety issue → handle only (never strapped), low stiffness, small workspace, speed cap; if not permitted, demo with a spring-loaded dummy arm. Jerky non-real-time control → slow the motion or move to the C++ real-time loop if a real-time PC exists. Metrics lack clinical validity → present as engineering measures, not diagnoses.
- **Judging angles:** innovation: teach-by-demonstration plus adaptive assistance on a general-purpose arm · technical depth: impedance shaping, effort estimation · impact: **high** (rehab clinics, ageing population) · Leukerbad relevance: **very high** (rehabilitation clinics in the village).

### Concept 3 — Tele-Physio: remote hands-on therapy with force feedback
- **Problem → value:** mountain villages and home-bound elderly lack specialist access, especially in winter. A therapist at one site guides a patient's limb at another and feels the resistance.
- **Hardware:** **two** Flexiv arms (leader at the therapist, follower at the patient) — only viable if two are available. Fallback leader: a non-Flexiv input device via TDK's device-to-robot mode, or XREAL glasses plus hand tracking (no force feedback).
- **Architecture / stack:**
  - Teleop: `flexiv_tdk` robot-to-robot with force feedback; LAN for the demo, WAN mode if you want to prove distance (needs chrony clock sync on both edge PCs, Ubuntu 22.04+).
  - Safety layer on the follower: workspace box, force and speed caps, dead-man switch on both ends.
  - Add-ons: video call plus live force / range-of-motion overlay for the therapist; record sessions so the follower can replay the exercise alone later (links to Concept 2).
  - Compute: two Linux PCs.
- **48-hour plan:**
  - H0–6: confirm two arms and TDK license; run a TDK example on LAN.
  - H6–24: follower safety envelope; handle / cuff; therapist dashboard.
  - H24–40: record-and-replay of a taught session; optional WAN test between two rooms or over a phone hotspot.
  - H40–48: rehearse; fix latency fallbacks; backup video.
- **3-minute demo script:** (0:00) winter road closed, physio cannot reach the patient → (0:30) therapist station and patient station at opposite ends of the stage → (1:00) therapist moves the leader, follower guides the patient's arm; patient resists and the therapist feels it → (1:50) dashboard shows force and range live → (2:20) therapist leaves; robot replays the prescribed exercise → (2:45) reach: one therapist, many valleys.
- **Risks and fallbacks:** two arms not available → drop to Concept 2 with a "remote prescription" story. TDK licensing or setup delays → LAN-only, or unilateral teleop without force feedback. Network latency on venue Wi-Fi → wired LAN.
- **Judging angles:** innovation **high** · technical depth: bilateral teleop, transparency vs stability · impact: rural and alpine care access · Leukerbad relevance: high (remote alpine location).

### Concept 4 — Learned bedside helper: feeding or handover assistance from therapist demonstrations
- **Problem → value:** people with weak grip or tremor need help with eating, drinking and reaching items; caregivers spend hours on this. A fixed bedside or table-mounted arm that hands over objects and assists with feeding restores some independence.
- **Hardware:** Rizon 4 / 4s + Grav Enhanced (cup, bottle, pill box) or Grav holding a spoon · 2–3 RGB-D cameras · GPU laptop. Optional: a mobile robot from another vendor (Galaxea R1, Unitree) bringing items to the station; Binabik or your own LLM agent for speech.
- **Architecture / stack:**
  - Data: teleoperate or hand-guide demonstrations; record with Flexiv Trainer as LeRobot-format episodes.
  - Policy: train a small imitation policy (diffusion or ACT-style via LeRobot tooling) for one skill — e.g. scoop-and-present, or pick-and-hand-over.
  - Safety shell (classical, not learned): mouth / hand region from a face or hand detector defines an approach line; final approach is force-limited and compliant; **the person comes to the spoon**, the robot stops short; release on a gentle pull detected by force sensing.
  - Interaction: voice or button request ("water", "tablets"); confirmation before motion.
  - Compute: GPU laptop for training and inference; RDK for execution.
- **48-hour plan:**
  - H0–6: scripted (non-learned) pick-and-hand-over with pull-to-release — this is the fallback demo.
  - H6–24: data collection (50–100 demos of one skill), start training; voice / button interface.
  - H24–40: policy on the robot inside the safety shell; second object; failure recovery.
  - H40–48: rehearse; decide honestly between learned and scripted for the live run.
- **3-minute demo script:** (0:00) a resident with tremor at breakfast → (0:30) "water please": robot picks the cup, presents it, releases on gentle pull → (1:10) spoon presentation stops short of the face (mannequin head or volunteer at distance); push the spoon aside and the robot yields → (1:50) show the demonstration-to-policy pipeline in 20 seconds → (2:20) failure handling and caregiver alert → (2:45) path to a mobile base.
- **Risks and fallbacks:** policy not robust in 48 h (most likely risk) → run the scripted handover and show the learned skill as video. Near-face motion not allowed → mannequin head. Trainer setup friction (cameras, GPU, teleop device) → hand-guided demos with your own logger.
- **Judging angles:** innovation **high** (learning + force-safe shell) · technical depth **high** · impact: daily-living independence · Leukerbad relevance: medium-high (care homes, clinic wards).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Flexiv Rizon + **OriginFlow** EMG | Muscle-effort signal for assist-as-needed rehab (Concept 2); biofeedback display | Medium — depends on OriginFlow's real-time streaming API ⚠️ unverified |
| Flexiv Rizon + **XREAL** AR glasses | Patient sees the target path and score; therapist sees force overlay | Low–medium — glasses as a display for your own app |
| Flexiv Rizon + **D-Robotics** RDK X5 / S100 | Edge pose estimation and person detection without a GPU laptop. Naming trap: D-Robotics "RDK" is a board, Flexiv "RDK" is an SDK | Low–medium |
| Flexiv Rizon + **Galaxea / Galbot / Spirit AI / UniX AI** wheeled manipulator or **Unitree** quadruped | Mobile robot fetches and delivers; Flexiv station does the delicate human-contact part | High — two stacks, hand-off choreography |
| Flexiv Rizon + **WUJI** Hand | Dexterous, hand-like contact (kneading, object handover) | High — mechanical adapter, payload budget (4 kg), separate controller ⚠️ unverified |
| Flexiv Rizon + **SKYLANDX** MetaCam | 3D scan of a room or body surface for path planning | Medium — offline scan is easy, live use is not |
| Flexiv Rizon + **Binabik AI** / **Genisom** agent stack | Speech and task-level agent on top of force skills | Unknown — no Flexiv integration public ⚠️ unverified |
| Two Flexiv arms (TDK) | Tele-physio with force feedback (Concept 3) | Medium — needs two arms and TDK set-up |

## Questions to ask the Flexiv Robotics engineers on site
1. Which arms and grippers are here, how many, and is there a **Mello** or **Enlight L** we can touch or program?
2. Is the **RDK license** activated on each robot, which RDK version, and do you provide a real-time Ubuntu PC?
3. What are your rules for **robot-on-human contact** during the hackathon, and which safety limits (force, speed, workspace) can we set and lock?
4. Which RDK calls do you recommend for constant-force contact along a path, and how do we cap the contact wrench?
5. Can free drive record a trajectory we can replay with variable impedance, and at what rate can Python read force and pose?
6. How does Mello sense the body (camera, depth, force only), and is any of that software available to us?
7. Is **TDK** licensed on these robots, and are two arms available for leader-follower teleop?
8. Can we mount a custom end-effector (flange pattern, tool mass / inertia update), and is a wrist F/T sensor fitted?

## Decision rule
- **Pick Flexiv Robotics for T04 if** your idea's core is safe, measurable physical contact with a person or delicate handover — massage, guided or resisted exercise, tele-physio, feeding — and you can work at a fixed station with your own camera and laptop.
- **Avoid if** you need a robot that moves through a home or clinic, talks to residents, detects falls, or lifts people — or if the booth cannot confirm an activated RDK license in the first hour.

## Sources
- [Flexiv — Robot Station / System page (Mello, Mico, AICO, Mobile Manipulator)](https://www.flexiv.com/product/robot-system)
- [Flexiv — Rizon product page](https://www.flexiv.com/product/rizon)
- [Flexiv — Enlight product page](https://www.flexiv.com/product/enlight)
- [Flexiv — "Flexiv to Showcase the Future of Adaptive Robotics at Hannover Messe 2026" (2026-04-16)](https://www.flexiv.com/news/Flexiv%20to%20Showcase%20the%20Future%20of%20Adaptive%20Robotics%20at%20Hannover%20Messe%202026)
- [Robotics 24/7 — Hannover Messe 2026: Flexiv showcases the future of adaptive robotics](https://www.robotics247.com/article/hannover-messe-2026-flexiv-showcases-the-future-of-adaptive-robotics)
- [GitHub — flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk)
- [GitHub — flexiv_rdk Python examples](https://github.com/flexivrobotics/flexiv_rdk/tree/main/example_py)
- [GitHub — flexiv_tdk](https://github.com/flexivrobotics/flexiv_tdk)
- [GitHub — flexiv_trainer (via company profile)](https://github.com/flexivrobotics/flexiv_trainer)
- [Flexiv RDK manual v2.x](https://www.flexiv.com/software/rdk/manual/v2.x/index.html)
- [Flexiv Robotics company profile (this vault)](../Flexiv.md)
