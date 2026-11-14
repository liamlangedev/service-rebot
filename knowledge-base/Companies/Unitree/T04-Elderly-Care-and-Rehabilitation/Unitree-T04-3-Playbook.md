---
type: challenge-playbook
company: "Unitree Robotics"
slug: Unitree
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Unitree Robotics × T04 — Hackathon Playbook

⬆ [Unitree Robotics profile](../Unitree.md) · [Brief](Unitree-T04-1-Brief.md) · [Products and solutions](Unitree-T04-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- **No physical contact with the "patient".** Unitree's product pages require a safe distance from humanoids. Use a volunteer team member, not an elderly guest; hand objects over via a table or tray.
- **Confirm the variant first:** only **EDU** units (G1 EDU, R1 EDU, Go2 EDU; Go2 X partly) accept SDK commands.
- Stay on **high-level control**. Low-level joint control switches off the factory balance controller and is where robots fall.
- Time estimates and episode counts below are our planning assumptions, not vendor figures.

## Solution approaches

### Concept 1 — Night-round and fall-response dog (Go2 EDU)

- **Problem → value:** night staff in rehab clinics and care homes cannot watch every corridor. A small quadruped walks a round, spots a person on the floor, talks to them and alerts the caregiver with a photo and location. Relieves night rounds; shortens time-to-help after a fall.
- **Hardware:** Go2 EDU (~15 kg, 4D LiDAR L2, front camera, optional Orin module) + laptop. Optional: small pouch on the back to carry water, a phone or a medication box (payload ~7–8 kg is ample). Optional other vendors: D-Robotics RDK X5 as on-robot perception box; SKYLANDX MetaCam to pre-scan the corridor.
- **Architecture / stack:**
  - Perception: front-camera frames via unitree_sdk2_python (OpenCV example) → open pose-estimation model on laptop or Orin → "person lying on floor for more than N seconds" rule.
  - Planning: waypoint list along a taped route; simple state machine (patrol → approach → check → alert → wait).
  - Control: high-level sport client velocity commands, built-in obstacle avoidance switched on.
  - Interaction: speech recognition + LLM + TTS on the laptop, played through a small Bluetooth speaker on the robot (or the robot's own audio if the on-site engineers confirm the API).
  - Alert: message with snapshot to a caregiver phone or web dashboard.
- **48-hour plan:**
  - H0–6: confirm EDU + network, run sport-client and camera examples, record test video of a person lying down.
  - H6–24: fall detector working on recorded and live video; patrol state machine on a 10 m route.
  - H24–40: approach behaviour, voice check ("Are you OK?"), alert dashboard, false-alarm handling (person sitting, person tying shoes).
  - H40–48: rehearse 10 full runs, record backup video, slides.
- **3-minute demo script:** (0:00) dog patrols corridor past a seated person — no alarm. (0:45) teammate lies down on a mat. (1:00) dog stops at 1.5 m, asks if help is needed; no answer. (1:30) caregiver phone shows photo + location; caregiver answers by voice through the robot. (2:15) second run: person answers "I'm fine" — alarm cancelled. (2:40) numbers: detection time, false alarms in N runs.
- **Risks and fallbacks:** localisation drift → use taped route and short segments, or visual markers. Wi-Fi dropouts → run everything on the on-board Orin. Robot as trip hazard → low speed, stop distance ≥ 1.5 m, lights on. If the unit is not EDU → teleoperate with the remote and run perception on an external camera.
- **Judging angles:** *Innovation* moderate · *Technical depth* perception + autonomy loop on real hardware · *Impact* night staffing is a real care bottleneck · *Leukerbad* rehab clinics and hotels with many elderly guests; the same robot handles stairs and thresholds in old alpine buildings.

### Concept 2 — Humanoid physio coach (G1 EDU, stationary)

- **Problem → value:** rehab patients must repeat exercises many times; therapists are scarce. A humanoid demonstrates each exercise with its own body, a camera counts and scores the patient's repetitions, and the therapist gets a session report. More supervised repetitions per therapist hour.
- **Hardware:** G1 EDU (4-mic array, 5 W speaker, depth camera) standing in place — on a gantry or with a spotter. Optional: OriginFlow EMG sensors on the patient's limb for muscle-activation feedback; XREAL glasses to show the therapist live joint angles. R1 EDU works too (1 h battery).
- **Architecture / stack:**
  - Perception: external webcam or robot camera → open body-pose model on laptop → joint angles, repetition counter, range-of-motion score.
  - Planning: exercise script (3–4 seated upper-body exercises), LLM turns scores into short spoken coaching ("lift the left arm a little higher").
  - Control: upper-body arm trajectories on G1 while the factory controller balances the legs; record trajectories by teleoperation (xr_teleoperate) or keyframes, validate first in unitree_mujoco or unitree_sim_isaaclab.
  - Compute: laptop over Ethernet / Wi-Fi; audio in and out on laptop or robot.
- **48-hour plan:**
  - H0–6: arm-control example running on the real G1; pose model running on a webcam.
  - H6–24: three exercise motions on the robot; repetition counting and range-of-motion scoring; voice loop.
  - H24–40: mirror mode (robot copies the patient's arm pose live), session report page, optional EMG channel.
  - H40–48: tune timing, rehearse, record backup video.
- **3-minute demo script:** (0:00) robot greets the patient by voice and demonstrates shoulder abduction. (0:40) patient follows; screen shows skeleton overlay and rep count. (1:20) patient deliberately under-reaches; robot corrects verbally and re-demonstrates. (2:00) mirror mode for 20 seconds. (2:30) therapist report: reps, range of motion per side, trend.
- **Risks and fallbacks:** robot loses balance during arm motion → slow motions, small amplitudes, gantry. Speech recognition fails in a noisy hall → push-to-talk button or handheld microphone. No arm-control access → use built-in gestures and keep the scoring pipeline as the core.
- **Judging angles:** *Innovation* humanoid embodiment used for what it is uniquely good at · *Technical depth* closed loop from human pose to robot motion and feedback · *Impact* measurable (reps, range of motion) · *Leukerbad* direct match with the village's rehabilitation clinics; a pilot with a local physiotherapist is a strong story.

### Concept 3 — Tele-care avatar with XR (G1 EDU + Dex3-1)

- **Problem → value:** mountain villages have too few caregivers and long travel times. A remote nurse or relative wears an XR headset and uses the robot's hands to fetch a pill box, bring a glass, or check on a person — presence plus hands, not just a video call.
- **Hardware:** G1 EDU with Dex3-1 hands and development computer; XR headset supported by xr_teleoperate (**Apple Vision Pro, PICO 4 Ultra Enterprise or Meta Quest 3** — bring one or ask the organisers; XREAL glasses are not on the supported list); host PC with Ubuntu 20.04 / 22.04. If a G1-D is on site, prefer it (wheeled, cannot fall).
- **Architecture / stack:**
  - Perception: robot head camera streamed to the headset by the image service on the robot.
  - Planning: human in the loop; add "assist" macros (pre-grasp pose, release over tray) triggered by controller buttons.
  - Control: xr_teleoperate maps operator hands to G1 arms and Dex3-1; locomotion by controller in motion mode or robot kept in place.
  - Extras: two-way audio; `--record` to log every session as training data.
- **48-hour plan:**
  - H0–6: xr_teleoperate running in simulation (`--sim`), then on the real robot; check latency on venue Wi-Fi.
  - H6–24: three care tasks rehearsed (pick pill box from shelf → tray; hand over light cup; press a call button); audio link.
  - H24–40: assist macros; operator dashboard with medication schedule; record 30–50 episodes of one task.
  - H40–48: reliability runs, backup video.
- **3-minute demo script:** (0:00) "nurse" in another room puts on the headset. (0:30) through the robot she greets the resident and asks about the evening medication. (1:00) robot picks the correct pill box (≤ 500 g) and places it on the tray in front of the resident. (2:00) she presses the call-light button and says goodbye. (2:30) show the recorded dataset and how it feeds Concept 4.
- **Risks and fallbacks:** network latency → wired host PC, operator in the same room behind a screen. Dex3-1 grasp limit 500 g → light, rigid objects only. Balance while reaching → gantry or fixed stance, no walking near the person. No supported headset → controller-based or keyboard arm macros, or switch to Concept 2.
- **Judging angles:** *Innovation* moderate (teleoperation is known) but strong use case · *Technical depth* full XR-to-humanoid pipeline live · *Impact* multiplies scarce caregivers across remote valleys · *Leukerbad* remote alpine setting is exactly where tele-care pays off.

### Concept 4 — Voice-requested autonomous handover (G1 EDU, learned policy)

- **Problem → value:** many daily requests are small — "bring my glasses", "my pills, please". A robot that hears the request, picks the right object and delivers it to a tray gives independence without a caregiver walking over.
- **Hardware:** as Concept 3, plus a GPU for training (cloud or a workstation on site). Optional: Go2 EDU as courier that carries the item from the G1 station to the resident's room; D-Robotics board for speech at the edge.
- **Architecture / stack:**
  - Data: teleoperate 30–50 episodes per object with xr_teleoperate `--record` (our estimate; the repo gives no number).
  - Learning: convert and train with unitree_lerobot — start with **ACT** (fastest to train); Pi0 / Pi05 / GR00T or UnifoLM-VLA-0 fine-tuning only if GPUs and time allow. Unitree's open "Pour Medicine" and similar G1 datasets can serve as templates, but check that the hand type matches.
  - Planning: speech → LLM → choose among 2–3 trained skills → run policy → verify with camera → speak result.
  - Control: policy inference on host PC with GPU, actions sent via SDK (`eval_g1.py` path).
- **48-hour plan:**
  - H0–6: teleoperation and recording working; fix table, lighting and object positions.
  - H6–24: collect data for skill 1, train ACT overnight, evaluate on robot.
  - H24–40: skill 2 (and 3 if stable), voice + LLM skill selection, optional Go2 courier leg.
  - H40–48: measure success rate over 20 trials, prepare teleop fallback, record backup video.
- **3-minute demo script:** (0:00) resident says "Please bring my pill box." (0:15) robot confirms by voice, policy picks the box and places it on the tray. (1:15) second request, different object. (2:00) optional: Go2 carries the tray pouch to the "room". (2:30) show success rate, data volume, and the path from teleoperated care to autonomous care.
- **Risks and fallbacks:** policy fails outside the training setup → fix positions, mark the table, keep the same light. Training overruns → demo autonomy on one skill and teleoperate the rest (honest hybrid). No GPU → drop to scripted grasps with camera-based object detection.
- **Judging angles:** *Innovation* high (learning from caregiver demonstrations) · *Technical depth* highest: data → training → deployment in 48 h · *Impact* clear route to scalable assistance · *Leukerbad* modest unless tied to a clinic routine (evening medication round).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| G1 EDU + OriginFlow EMG | Rehab coach that sees muscle activation, not just pose; EMG as an input for patients with limited movement | Medium — depends on OriginFlow's data stream format (ask them) |
| Go2 EDU + D-Robotics RDK X5 | Self-contained fall detector on the robot, no Wi-Fi dependency | Low–medium — camera + DDS over Ethernet |
| Go2 EDU + SKYLANDX MetaCam | Pre-scanned 3D map of the clinic floor for route planning | Medium — map format conversion; skip if a taped route suffices |
| Go2 courier + Flexiv Rizon / ROKAE xMate station | Division of labour: force-controlled arm does contact tasks (assisted stretching, massage demo), Go2 does logistics and rounds | Medium — two independent systems linked by a simple message |
| G1 EDU + XREAL glasses | Therapist or caregiver sees patient metrics and robot state hands-free | Low for a display-only overlay; **not** usable as the xr_teleoperate headset |
| G1 EDU + WUJI Hand | 20-DoF hand for finer objects (pills, zips) | High — not in the supported end-effector list of Unitree's teleop / learning repos |
| G1 EDU + Binabik AI | Agentic task layer over Unitree skills | Unknown — ask Binabik whether G1 is supported |
| Go2 EDU + Galaxea / Galbot / UniX wheeled manipulator | Wheeled manipulator does in-room manipulation safely; Go2 covers stairs and corridors | Medium — coordination layer only |

## Questions to ask the Unitree Robotics engineers on site

1. Which exact variants are here — **EDU or not** — and which firmware? Is the development computer (Orin) fitted and reachable by SSH?
2. Which hands are on the G1 units (Dex3-1 with or without tactile, Dex1-1, other)? Are spares available?
3. Is there a gantry or harness for G1, and a wireless e-stop per robot? What is the minimum distance to people you accept for demos?
4. What is the current API for G1 audio: can we play TTS / audio streams through the robot's speaker and read the 4-mic array from our own code?
5. Can we command the G1 arms while the built-in locomotion controller keeps balancing (which mode, which topic), and what speed / torque limits do you recommend near people?
6. Does the Go2 EDU on site expose LiDAR mapping and navigation (SLAM, go-to-point) through the SDK, or only velocity commands and obstacle avoidance?
7. Is a supported XR headset (Vision Pro, PICO 4 Ultra Enterprise, Quest 3) available to borrow, and which xr_teleoperate version matches the robots' firmware?
8. How many batteries and chargers per robot, and can G1 run on external power while standing in place?

## Decision rule

- **Pick Unitree Robotics for T04 if** your idea is no-contact (coach, companion, night rounds, fetch to a tray, tele-care), you get an **EDU** unit, and you want the quickest path from idea to moving robot using open teleoperation and learning tools.
- **Avoid if** your idea needs physical contact or load (lifting, walking support, massage), certified safety near frail people, or more than ~3 kg of manipulation — choose a force-controlled arm or a wheeled manipulator vendor instead and use Unitree only as courier or scout.

## Sources
- [Unitree G1 product page](https://www.unitree.com/g1)
- [Unitree G1-D product page](https://www.unitree.com/G1-D)
- [Unitree Dex3-1 product page](https://www.unitree.com/Dex3-1)
- [Unitree R1 product page](https://www.unitree.com/R1)
- [Unitree Go2 product page (specs taken from the company profile)](https://www.unitree.com/go2)
- [xr_teleoperate repository](https://github.com/unitreerobotics/xr_teleoperate)
- [unitree_lerobot repository](https://github.com/unitreerobotics/unitree_lerobot)
- [unifolm-vla repository](https://github.com/unitreerobotics/unifolm-vla)
- [unitree_sdk2_python repository](https://github.com/unitreerobotics/unitree_sdk2_python)
- [Unitree GitHub organisation](https://github.com/unitreerobotics)
- [Unitree on Hugging Face](https://huggingface.co/unitreerobotics)
