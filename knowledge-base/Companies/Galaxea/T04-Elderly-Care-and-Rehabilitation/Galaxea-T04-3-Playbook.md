---
type: challenge-playbook
company: "Galaxea"
slug: Galaxea
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Galaxea × T04 — Hackathon Playbook

⬆ [Galaxea profile](../Galaxea.md) · [Brief](Galaxea-T04-1-Brief.md) · [Products and solutions](Galaxea-T04-2-Products-and-Solutions.md)

> **Ground rules for all concepts:** (1) confirm at the booth which robot is on site (R1 Pro / R1 Lite / LEMO) and what GPU comes with it — none of this is confirmed; (2) no physical contact between robot and person: hand over onto a tray or with a slow, stationary reach; (3) cap base speed and keep one teammate on the e-stop; (4) teleoperation is the fallback for every autonomous step.

## Solution approaches

### Concept 1 — Tele-care "remote hands" (safest)

- **Problem → value:** Leukerbad clinics and home-care services are short of staff, and guests' relatives live far away. A nurse, physiotherapist or family member remotely operates the robot to fetch, carry, open, tidy — one caregiver covers several rooms; every session is logged as training data.
- **Hardware:** R1 Pro or R1 Lite + teleop rig (leader arms / VR headset — whatever Galaxea brought). Optional: **XREAL** glasses as the operator's head-up camera view.
- **Architecture / stack:** robot cameras → video stream to operator station → teleop commands over ROS 2 (Galaxea SDK) → arms / torso / base. Add a thin assist layer: speed limits near detected persons (LiDAR + head camera), one-button "go to room" via the robot's navigation, two-way audio for the resident. Compute: on-robot + operator laptop; no model training needed.
- **48-hour plan:**
  - H0–6: get teleop running end to end; define 3 care tasks (bring water and medication box, pick up a dropped walking-stick or phone, open curtain / door).
  - H6–24: operator UI (camera views, task buttons, audio), person-distance speed limiter, start recording all sessions in rosbag / LeRobot format.
  - H24–40: user test with a seated "resident"; measure time per task; add network-latency handling; rehearse.
  - H40–48: polish, record backup video, slides with time-saved estimate.
- **3-minute demo script:** resident presses a call button → remote nurse (teammate in another room, on screen) greets them through the robot → robot drives over, picks the dropped phone from the floor, places it on the side table → fetches water bottle and pill box from a shelf → show the recorded dataset counter: "these 40 episodes are tomorrow's autonomy".
- **Risks and fallbacks:** venue Wi-Fi latency → run operator on the same LAN, wired if possible. Teleop rig not on site → ask Galaxea about JoyLo-style or gamepad control; worst case keyboard / gamepad base control plus scripted arm poses.
- **Judging angles:** *impact* — deployable today with a human in the loop, clear staffing story; *technical depth* — moderate (safety layer, data flywheel); *innovation* — low to medium; *Leukerbad* — rehab clinics, remote alpine location, relatives abroad.

### Concept 2 — "Pick it up for me": voice-driven fetch and floor retrieval

- **Problem → value:** bending for a dropped object and reaching high shelves are classic fall triggers. A robot that retrieves on request removes the trigger and keeps people independent after hip or knee surgery (typical Leukerbad rehab patients).
- **Hardware:** R1 Lite (best match to the open data) or R1 Pro; GPU workstation (RTX 3090 / 4090 class, more than 8 GB VRAM) for inference. Optional: **D-Robotics** RDK board as a room camera node for object localisation.
- **Architecture / stack:** microphone → ASR → LLM turns the request into a short instruction and a target location → base navigates to a pre-mapped waypoint → **G0.5 `g05-base` zero-shot** (or `G0Plus_3B-pick_and_place`) executes the grasp from the instruction, served by `scripts/serve_policy.py` off-board with the ROS 2 client from `experiments/r1lite` / `experiments/r1pro` on the robot → drive back → place on tray beside the person → TTS confirmation. Speech and LLM are your own additions; they are not part of the Galaxea stack.
- **48-hour plan:**
  - H0–6: bring up zero-shot G0.5 on the robot; test 10 everyday objects (bottle, glasses case, remote, pill box, phone, slipper) on table and floor; note what fails.
  - H6–24: waypoint navigation + speech front-end; collect **50–100 teleop demos** of the failing cases (floor pick-up, place on tray). If an 80 GB GPU is available, start a G0.5 fine-tune overnight; otherwise train a small diffusion policy (GalaxeaDP / LeRobot).
  - H24–40: integrate the better policy; add grasp-failure detection and retry; teleop takeover button.
  - H40–48: 10-run reliability count, demo rehearsal, backup video.
- **3-minute demo script:** seated person drops glasses case, says "please pick up my glasses" → robot answers, drives over, lowers torso, picks from the floor, places it on the lap tray → "bring my water from the shelf" → high-shelf fetch → show success statistics and the one-tap handover to a remote caregiver when the policy is unsure.
- **Risks and fallbacks:** zero-shot grasp fails on small or flat objects → restrict to 4–5 reliable objects, use fine-tuned policy, or teleop takeover (Concept 1). No fine-tune GPU → small policy or the pick-and-place checkpoint. Navigation not exposed → fixed base position within arm reach.
- **Judging angles:** *innovation* — VLA in a care setting is new for this vendor (no public care work exists); *technical depth* — high (VLA deployment, fine-tune, failure recovery); *impact* — direct fall-prevention story; *Leukerbad* — post-surgery rehab guests in hotel and clinic rooms.

### Concept 3 — Learned care-prep station: medication and meal trays

- **Problem → value:** caregivers lose time on repetitive preparation (weekly pill organisers, meal trays, opening packaging for people with weak grip). A dual-arm station does the preparation; a human verifies. Frees staff time for people.
- **Hardware:** **LEMO** desktop dual-arm kit with A1Z-T leader arms (or the R1's two arms parked at a table). Optional: R1 delivers the finished tray to the room; **WUJI** hand only if a real pinch grasp for pills is needed (integration unproven).
- **Architecture / stack:** 3 fisheye cameras → learned bimanual policy (LEMO Studio collect-train-deploy, or LeRobot / GalaxeaDP) → arm control. A vision check (separate small model or classical colour / count check) verifies the compartment contents before release; an LLM reads the "prescription" (a mock schedule) and selects which sub-policy to run. Use candy or coloured beads in containers large enough for a parallel gripper — never real medication.
- **48-hour plan:**
  - H0–6: fix the workspace (jig the tray, lighting); pick 2 sub-tasks: (a) move a dose cup into the right day slot, (b) open a screw-top bottle or peel a yoghurt lid with two arms.
  - H6–24: collect **about 100 demos per sub-task** with the leader arms (the Stanford BRS work used about 100–140 per task); train first policies; build the verification camera check.
  - H24–40: iterate on failure cases with more demos; chain sub-tasks from the mock schedule; add the "human confirms" screen.
  - H40–48: reliability run (20 trials), demo rehearsal.
- **3-minute demo script:** nurse scans a mock schedule → station fills Monday–Wednesday slots, opens a bottle bimanually → verification screen shows green / red per slot → nurse confirms → (optional) R1 carries the tray to the "room".
- **Risks and fallbacks:** small-object grasping with parallel grippers → use cups / blister-size boxes instead of single pills. Policy unreliable → narrow to one sub-task and show verification catching the errors. LEMO not on site → same task with R1 arms at a table.
- **Judging angles:** *technical depth* — bimanual learned skills with verification; *impact* — measurable caregiver minutes saved, human stays accountable; *innovation* — medium; *Leukerbad* — clinic and care-home back-office.

### Concept 4 — Night-round fall responder (most ambitious, multi-vendor)

- **Problem → value:** falls at night are found late. A sensing layer detects a fall or a person out of bed; the Galaxea robot goes to the room, opens a telepresence line, brings phone / blanket / water and clears the floor of obstacles while help is on the way. It does **not** lift the person.
- **Hardware:** R1 Pro or R1 Lite as the responder; **D-Robotics** RDK X5 as fixed fall-detection camera nodes (or a **Unitree** Go2 as a roaming scout); **XREAL** glasses for the on-call nurse; optional **OriginFlow** EMG band as a wearable "I need help" gesture trigger.
- **Architecture / stack:** RDK node runs pose estimation → fall / inactivity event over ROS 2 or MQTT → orchestrator (LLM agent with a fixed playbook) → R1 navigates to the room waypoint → person-aware approach with a hard stop distance → two-way audio / video to the nurse → nurse picks an action: "bring blanket", "clear path", "fetch phone" → G0.5 or a fine-tuned policy executes; teleop takeover at any time. Compute: detection on RDK, VLA on GPU workstation, orchestration on a laptop.
- **48-hour plan:**
  - H0–6: split the team — detection node, robot navigation, manipulation skill. Agree on one message schema.
  - H6–24: fall detector working on the RDK; robot drives to an alarm waypoint; one manipulation skill (blanket or phone fetch) by teleop, demos recorded.
  - H24–40: end-to-end alarm → arrival → call → action; add stop-distance safety and the nurse UI; train the skill policy if time allows.
  - H40–48: timed runs (alarm to arrival, alarm to human contact), rehearsal, backup video.
- **3-minute demo script:** lights dimmed, teammate "falls" → alarm on nurse's AR glasses within seconds → robot arrives, stops at a safe distance, nurse talks through it → robot fetches the phone from the table and a blanket, moves a chair out of the paramedics' path → timeline slide: detection, arrival, contact.
- **Risks and fallbacks:** three integrations in 48 h → cut the scout dog first, then the AR view (use a tablet), then autonomy (teleop the manipulation). Blanket handling is hard → fetch phone / water instead.
- **Judging angles:** *innovation* and *impact* — high, system-level; *technical depth* — multi-robot, multi-vendor orchestration; *Leukerbad* — small clinics and hotels with thin night staffing, long ambulance times in a mountain valley.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Galaxea R1 + **D-Robotics** RDK | Edge fall / pose / gesture detection that triggers robot tasks | Low–medium (ROS 2 messages) |
| Galaxea R1 + **XREAL** | Caregiver AR view and tele-care supervision | Medium (video stream + simple app) |
| Galaxea R1 + **OriginFlow** | EMG gesture or effort signal as input for people who cannot speak or press buttons; rehab effort logging | Medium–high (signal decoding is the unknown) |
| Galaxea R1 + **Unitree** Go2 | Dog patrols corridors, R1 manipulates on arrival | High (two robot stacks) |
| Galaxea R1 (logistics) + **Flexiv** Rizon (contact) | Flexiv arm does the force-controlled physio / massage contact; R1 fetches towels, equipment, water | Medium (loose coupling, two demos in one story) |
| Galaxea LEMO + **WUJI** hand | Fine pinch for pills, buttons, zips | High (mechanical + control integration unproven) |
| Galaxea R1 + **Binabik AI** | Agentic task layer on top of robot skills | Unknown — ask both teams whether an adapter exists |
| Galaxea R1 + **SKYLANDX** MetaCam | Fast 3D scan of the "apartment" for a navigation map / digital twin | Low–medium (offline map import) |

## Questions to ask the Galaxea engineers on site

1. Which robots are here (R1 Pro, R1 Lite, LEMO, Nexo), how many units, and how are they shared between teams?
2. Which teleop devices did you bring (leader arms, VR, JoyLo), and can we record to LeRobot format out of the box?
3. Is there a GPU with 80 GB VRAM on site for G0.5 fine-tuning? If not, which policy do you recommend training in under 6 hours, and how many demos does it need?
4. Does `g05-base` zero-shot pick objects from the **floor** and hand them to a person, or only tabletop? Which objects fail?
5. Is navigation (mapping, go-to-waypoint, obstacle avoidance) exposed through the SDK, and which ROS 2 distro and topics do we use for base, torso and arms?
6. What safety functions exist near people: joint torque sensing, collision detection, speed and force limits, software e-stop? What stand-off distance do you require?
7. Can we mount extra hardware (microphone, speaker, tray, call button) and draw power from the robot?
8. Does Galaxea have any care, hospital or rehabilitation pilots or plans it can talk about (none are public)?

## Decision rule

- **Pick Galaxea for T04 if** your idea is assistive *manipulation* around a person — fetch, floor pick-up, tidy, tray prep, tele-care — and you want to show a learned or VLA-driven skill rather than scripted motion, with teleop as a safety net.
- **Avoid if** your idea needs physical contact or load-bearing support for a person (lifting, gait aid, massage, physio), outdoor or stair mobility, or a path to commercial use without a separate model licence — or if the booth cannot confirm a robot and GPU for your team within the first hour.

## Sources
- [Galaxea blog — Stanford x Galaxea household robotics (BRS)](https://galaxea-dynamics.com/blogs/robotics-applications/stanford-galaxea-brs-household-robotics)
- [BEHAVIOR Robot Suite project page](https://behavior-robot-suite.github.io)
- [GitHub — OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA)
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics)
- [Hugging Face — Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset)
- [Galaxea legacy user guide — R1](https://userguide-galaxea.github.io/Product_User_Guide/Introducing_Galaxea_Robot/product_info/R1)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)
- [Galaxea company profile (internal, general research)](../Galaxea.md)
