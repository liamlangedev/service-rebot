---
type: challenge-playbook
company: "Spirit AI"
slug: Spirit-AI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Spirit AI × T04 — Hackathon Playbook

⬆ [Spirit AI profile](../Spirit-AI.md) · [Brief](Spirit-AI-T04-1-Brief.md) · [Products and solutions](Spirit-AI-T04-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- Assumes a **Moz1** with Quest VR teleop kit and MozRobot SDK is on site — ⚠️ unverified. Confirm in the first 30 minutes.
- The Moz1 manual asks for **≥ 2 m** distance during commissioning and excludes people with chronic illnesses from the operating area. Design for **hand-over via table or tray**, an actor as the "resident", and an E-stop holder at all times.
- Public SDK = joint / Cartesian position targets at up to 120 Hz + camera and state readout. No documented force or impedance commands.
- Voice I/O, LLM and perception run on your laptop (Ubuntu 22.04, ROS 2 Humble, Ethernet to the robot); Moz1 has no documented microphone or speaker.

## Solution approaches

### Concept 1 — Tele-care avatar (caregiver in VR, robot in the room)

- **Problem → value:** one night-shift caregiver covers many rooms; many requests are small (pass the water, pick up the dropped remote). A remote caregiver or relative does them through Moz1 without walking over — and every session becomes training data.
- **Hardware:** Moz1 + Quest VR teleop kit. Optional: XREAL glasses as a lightweight caregiver monitor view.
- **Architecture / stack:** head D455 + wrist D405 video → operator in Quest → shipped teleop app (relative / Cartesian modes) → Moz1. Add a small request queue web app (resident taps a tablet or speaks; speech-to-text on a laptop) and automatic episode logging per task type.
- **48-hour plan:**
  - H0–6: get teleop running, measure latency, pick 3 chores (bring bottle, pick object off low table, clear tray).
  - H6–24: request-queue app; practise chores until each takes < 60 s; log episodes.
  - H24–40: add one "assist macro" through the SDK (for example auto-return to home pose or auto-place on tray) so it is not pure teleop.
  - H40–48: rehearse with an actor; record backup video.
- **3-minute demo script:** resident asks for water by voice → request appears on caregiver screen → caregiver in VR picks the bottle and places it on the bedside tray → macro returns the arms home → show the episode counter and explain "after N episodes this chore runs by itself".
- **Risks and fallbacks:** teleop latency on venue Wi-Fi → use the wired link; operator fatigue → limit to 2 chores; no remote-network teleop → operator sits behind a screen in the same hall.
- **Judging angles:** innovation medium (data-flywheel framing) · technical depth low–medium · real-world impact high (staff shortage) · Leukerbad relevance: rehab clinics with night shifts and seasonal staff.

### Concept 2 — Bedside fetch: "bring me my evening medication and water"

- **Problem → value:** residents with limited mobility need small items many times a day; reaching and walking for them is a fall risk. The robot brings the right item to a hand-over table and confirms what it brought.
- **Hardware:** Moz1 (`dualarm` or `wholebody_without_base`), a shelf with 4–6 labelled items (medication boxes, bottle, glasses case). Optional: D-Robotics RDK board running the detector.
- **Architecture / stack:** speech-to-text + LLM on laptop turns the request into `{item, destination}` → detection from wrist D405 / head D455 (ArUco or large printed labels first; open-vocabulary detector as upgrade) → grasp pose from RealSense depth → Cartesian waypoints through `send_action()` → place on tray → spoken confirmation and a log line for the caregiver ("20:02 evening box delivered").
- **48-hour plan:**
  - H0–6: SDK connection, run the Cartesian example, calibrate camera-to-gripper, fix the shelf layout.
  - H6–24: reliable pick and place of one box with markers; add the bottle; add voice front end.
  - H24–40: wrong-item check (re-read label before placing), medication schedule logic, caregiver log page, teleop takeover button.
  - H40–48: 20 timed runs, tune, record backup.
- **3-minute demo script:** actor says the request → robot names the item it understood → picks the correct box among look-alikes → places box and bottle on the tray → logs the delivery; second request is deliberately for a medication not due yet → robot declines and notifies the caregiver.
- **Risks and fallbacks:** grasp failures with two-finger grippers → use rigid boxes with a fixed grasp face; depth noise → markers and fixed shelf slots; SDK access shared → rehearse motions in MuJoCo with the URDF.
- **Judging angles:** innovation medium · technical depth medium (perception-to-Cartesian loop, safety logic) · impact high (medication adherence, fall prevention) · Leukerbad relevance: clinic and hotel guests recovering from surgery.

### Concept 3 — Night round: room-to-room delivery and trip-hazard check

- **Problem → value:** night rounds eat caregiver time; objects on the floor cause falls. Moz1 drives a waypoint round, delivers items to each room's table and reports hazards or a person on the floor.
- **Hardware:** Moz1 in `wholebody` mode with its Livox MID-360S. Optional: Unitree Go2 as a fast scout, D-Robotics RDK X5 as a fixed fall-detection camera node, SKYLANDX MetaCam for a venue scan (map format compatibility ⚠️ unverified).
- **Architecture / stack:** `run_mapping.sh` → saved map → `run_nav.sh` (Nav2 + relocalisation) → waypoint list through the navigation ROS service (CycloneDDS) → at each stop run the Concept 2 place skill → head camera frames to a person-pose / floor-object detector on the laptop → alert to a caregiver dashboard.
- **48-hour plan:**
  - H0–6: map a mock "ward" of 3 stations when the hall is quiet (moving people leave ghost obstacles); first Nav2 goal.
  - H6–24: scripted round with 3 waypoints; tray place at each stop.
  - H24–40: hazard and lying-person detection, dashboard, external trigger (scout or fixed camera calls Moz1 to a room).
  - H40–48: full-loop rehearsals at reduced speed; backup video.
- **3-minute demo script:** dashboard shows the round → Moz1 drives to room 1 and places a bottle → at room 2 it flags an object on the floor with a photo → a fall alert from the camera node diverts it to room 3, where it stops at a safe distance and opens a caregiver video view.
- **Risks and fallbacks:** navigation defaults are conservative (10 % speed; docs suggest 50 % for first runs) and base tops out at **0.5 m/s** → keep the route short; crowded hall breaks localisation → fence off a lane; combining Nav2 and arm control in one session untested → fall back to driving by controller and automate only the arm part.
- **Judging angles:** innovation medium–high (multi-robot trigger) · technical depth high (SLAM + manipulation + perception) · impact high · Leukerbad relevance: small clinics and hotels with thin night staffing.

### Concept 4 — Learned care skill from caregiver demonstrations

- **Problem → value:** care chores vary too much to script. Show that a caregiver can teach one chore (clear a meal tray, fill a weekly pill organiser with large mock pills) by VR demonstration and the robot repeats it.
- **Hardware:** Moz1 + Quest VR; cloud GPUs. Optional: OriginFlow EMG capture as an extra demonstration signal (integration ⚠️ unverified), D-Robotics S600 for on-board inference (port announced May 2026, availability on site ⚠️ unverified).
- **Architecture / stack:** teleop data collection → fine-tune Pi0.5 with the documented `pi05_moz` config (policy server + robot client, Docker) or Spirit v1.5 (MIT, fine-tune spec **8× A100 80 GB**) → run through the teleop app's inference mode → scripted fallback from Concept 2.
- **48-hour plan:**
  - H0–6: ask Spirit AI for the adapted openpi source, a base checkpoint and GPU access. **No checkpoint or GPUs by H6 → drop to Concept 2.**
  - H6–24: collect 100–200 short demonstrations of one narrow task; start training.
  - H24–40: evaluate, collect corrective demos, retrain once.
  - H40–48: measure success rate over 20 trials; prepare honest numbers.
- **3-minute demo script:** 20-second clip of a caregiver teaching in VR → live autonomous run of the chore → disturb the scene once → show the measured success rate and the scripted fallback.
- **Risks and fallbacks:** training time and GPU access are the whole risk; closed Spirit v1.6 (the model behind the WAIC pill-sorting demo) is not available to teams; fallback is teleop + scripted skills presented as the data pipeline.
- **Judging angles:** innovation high · technical depth high · impact medium (one chore) · Leukerbad relevance medium.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Moz1 + D-Robotics RDK X5 | Off-board fall / person detection node that calls the robot; keeps the laptop free | Low–medium (ROS 2 on both sides; check DDS domain 33) |
| Moz1 + Unitree Go2 | Quadruped scouts rooms quickly, Moz1 follows with the manipulation job | Medium (two stacks, shared dashboard only) |
| Moz1 + XREAL glasses | Caregiver sees robot camera and task queue hands-free | Low (video and web view) |
| Moz1 + OriginFlow EMG | Resident triggers "fetch" by muscle signal when speech is hard; or richer demonstration data | Medium–high (⚠️ unverified interfaces) |
| Moz1 + Flexiv Rizon or ROKAE xMate | Fixed force-controlled arm handles the contact-rich rehab exercise; Moz1 does logistics | Medium (two independent cells, one story) |
| Moz1 + WUJI Hand | Fine pill and utensil handling | High (mechanical and control integration, not realistic in 48 h) |
| Moz1 + Binabik AI / Genisom SomaMind | Agent layer for task planning over the SDK skills | Unknown (⚠️ unverified) |

## Questions to ask the Spirit AI engineers on site

1. Which robot and how many units are here, and how is robot time shared between teams?
2. Can we get the MozRobot SDK wheel, the navigation Docker bundle and the `pi05_moz` openpi source today — and is there English documentation?
3. Does any API expose joint torques, end-effector force or impedance / compliance settings, or is collision sensitivity only adjustable in the HMI?
4. What are the arm payload, gripper stroke and grip force, and battery runtime? Can the grippers reach the floor?
5. Can Nav2 navigation and SDK arm control run in the same session, and can teleop run over the venue network from another room?
6. Is a Moz1-ready Spirit v1.5 (or Pi0.5) checkpoint available, and do you provide GPU access for fine-tuning during the event?
7. What distance and speed limits do you require when an actor plays the resident near the robot?
8. Is there a microphone, speaker or head-control interface we can use?

## Decision rule

- **Pick Spirit AI for T04 if** your idea is care logistics — fetch, deliver, tidy, tele-care — on flat indoor floors, you have someone fluent in ROS 2 and Python (ideally reading Chinese), and you can secure robot time early.
- **Avoid if** your idea needs physical contact with a person (physio, massage, transfers), programmable force control, legged or outdoor mobility, or a guaranteed robot per team.

## Sources

- [Spirit AI news: WAIC 2026 demos and Moz2 debut](https://www.spirit-ai.com/en/news/48)
- [Spirit AI product page](https://www.spirit-ai.com/en/product)
- [Docs: Moz1 mechanics](https://docs.spirit-ai.com/zh/moz1/mechanics.html)
- [Docs: Moz1 safety](https://docs.spirit-ai.com/zh/moz1/safety.html)
- [Docs: MozRobot SDK quick start](https://docs.spirit-ai.com/zh/sdk/get-started.html)
- [Docs: MozRobot SDK API reference](https://docs.spirit-ai.com/zh/sdk/api.html)
- [Docs: MozRobot SDK examples](https://docs.spirit-ai.com/zh/sdk/examples.html)
- [Docs: SLAM navigation](https://docs.spirit-ai.com/zh/slam-nav/slam_navigation.html)
- [Docs: Pi0.5 adaptation (via profile research)](https://docs.spirit-ai.com/zh/open-resources/pi.html)
- [GitHub: Spirit-AI-Team/spirit-v1.5](https://github.com/Spirit-AI-Team/spirit-v1.5)
- [Spirit AI company profile (internal)](../Spirit-AI.md)
