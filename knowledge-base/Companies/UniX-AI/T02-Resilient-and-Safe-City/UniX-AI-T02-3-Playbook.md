---
type: challenge-playbook
company: "UniX AI"
slug: UniX-AI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# UniX AI × T02 — Hackathon Playbook

⬆ [UniX AI profile](../UniX-AI.md) · [Brief](UniX-AI-T02-1-Brief.md) · [Products and solutions](UniX-AI-T02-2-Products-and-Solutions.md)

**Read first:** UniX AI has **no public SDK**. Every concept below is designed so the "brain" runs on **your laptop** and the robot is driven through whatever the on-site engineers expose: (a) skill / waypoint calls, (b) camera and LiDAR streams, or (c) only their teleoperation system. Spend the first hour finding out which. All concepts are **indoor, flat-floor**.

## Solution approaches

### Concept 1 — Night fire-safety round (safest)

- **Problem → value:** Hotels, baths and clinics must keep extinguishers in place, fire doors closing and escape routes clear; checks are manual and skipped at night. A robot that does the round and files evidence gives continuous compliance with no extra staff. This mirrors UniX AI's own published Security use case, so the vendor team can help.
- **Hardware:** Wanda 2.0 (or Panther) with UniPicker Pro. Optional: D-Robotics RDK board as a carried perception node.
- **Architecture / stack:**
  - Perception: head RGB / RGBD frames → open detector or VLM on laptop ("extinguisher present?", "door fully closed?", "corridor blocked?", "unattended object?").
  - Planning: mission file of checkpoints (pose + check type) → simple state machine.
  - Control: vendor navigation to waypoints; vendor skill or taught demonstration for "push door open, release, watch it close"; fallback teleop.
  - Output: web dashboard with floor plan, pass / fail per checkpoint, photo evidence, timestamp.
- **48-hour plan:**
  - H0–6: confirm interfaces; map one corridor; get a camera stream on the laptop; define 4–5 checkpoints.
  - H6–24: perception checks working on still frames; waypoint patrol loop; dashboard skeleton.
  - H24–40: fire-door test (push, release, time the closing from video); fault injection (remove extinguisher, wedge door, drop a box in the exit path).
  - H40–48: full-loop rehearsals, record a backup video, polish report.
- **3-minute demo script:** (0:00) the problem in one sentence + a wedged-open fire door photo. (0:30) robot starts round, passes checkpoint 1. (1:00) judge removes the extinguisher → robot flags it live on the dashboard. (1:40) robot pushes the fire door, door fails to close → alert. (2:20) show the generated inspection report; (2:40) scale story: 8–16 h battery, every night, every floor.
- **Risks and fallbacks:** no nav API → engineer or teammate teleoperates between checkpoints, perception and reporting stay autonomous. Door manipulation unreliable → robot only observes door state. No camera stream → mount a phone / USB camera on the robot.
- **Judging angles:** *Innovation* — inspection that manipulates, not only looks. *Technical depth* — closed loop from perception to evidence. *Impact* — measurable compliance gain. *Leukerbad* — fits spa hotels and rehab clinics directly.

### Concept 2 — Teleoperated first-look responder with AI co-pilot

- **Problem → value:** When an alarm goes off in a plant room (chemical store for pool treatment, boiler, electrical room), the first person in takes the risk. A robot already in the building goes first; a remote operator sees, assesses and performs one simple action (close a valve, hit a stop button, retrieve an item).
- **Hardware:** Wanda 2.0 or Panther + UniX AI's proprietary teleoperation system. Optional: XREAL glasses for the operator view; a USB gas / temperature sensor carried in one gripper.
- **Architecture / stack:**
  - Perception: camera streams to operator + VLM overlay on laptop that labels hazards (spill, smoke, person down, valve state) and suggests next step.
  - Planning: operator decides; co-pilot produces a checklist and an auto-written incident log.
  - Control: vendor teleoperation for arms and base; autonomous drive to the room door if waypoint navigation is available.
- **48-hour plan:**
  - H0–6: hands-on with the teleop rig; measure latency; pick the intervention (lever valve or emergency-stop button mock-up).
  - H6–24: build the mock plant room; video stream to laptop; hazard-labelling overlay.
  - H24–40: operator training runs; incident log generation; XREAL view if time allows.
  - H40–48: timed rehearsals; backup video.
- **3-minute demo script:** alarm sounds → robot drives to the room → operator (in another room, visible on screen) sees overlay "liquid on floor, valve open" → closes the valve with the gripper → co-pilot reads back the incident summary.
- **Risks and fallbacks:** teleop rig not on site or not shareable → reduce to autonomous "go, look and report" with no intervention. Remote link poor → operate on local network and say so.
- **Judging angles:** *Innovation* — dual-use: service robot by day, responder on alarm. *Technical depth* — shared autonomy. *Impact* — removes the human from first entry. *Leukerbad* — thermal-bath technical rooms and small volunteer response teams.

### Concept 3 — Disruption mode: the hotel robot becomes the evacuation helper

- **Problem → value:** An alpine village can be isolated by road closure, storm or power failure, with few staff and many elderly guests. Service robots already in the building switch role: check rooms and corridors, guide guests to the assembly point, carry a first-aid kit or blankets, and keep a headcount for the incident lead.
- **Hardware:** Wanda 2.0 (voice via 6-mic array and speaker; 12 kg payload). Optional: second robot from any vendor for a multi-robot story.
- **Architecture / stack:**
  - Perception: person detection and simple "person on floor" check from head camera; speech in / out through a laptop LLM (multilingual: DE / FR / EN).
  - Planning: LLM-based mission agent with a mode switch ("normal service" → "incident"), room list, priority for rooms flagged as mobility-impaired.
  - Control: waypoint navigation; pick-and-carry skill for the kit; teleop fallback.
  - Output: incident board — rooms checked, people found, who needs help.
- **48-hour plan:**
  - H0–6: interfaces; map corridor + "assembly point"; voice loop on laptop.
  - H6–24: room-sweep mission, person detection, headcount board.
  - H24–40: guide-me behaviour at walking pace; kit delivery; mode-switch trigger.
  - H40–48: rehearsals with volunteers as guests.
- **3-minute demo script:** robot serving tea → alert "road closed, power cut" → mode switch → sweeps two "rooms", finds a guest, speaks German, guides them out, delivers a kit; board updates live.
- **Risks and fallbacks:** audio access blocked → use a clip-on Bluetooth speaker-mic. Navigation flaky in crowds → mark a taped lane.
- **Judging angles:** *Innovation* — resilience from assets already deployed. *Impact* — elderly guests, staff shortage. *Leukerbad* — strongest local story of the four. *Depth* — moderate; relies on integration quality.

### Concept 4 — Indoor-outdoor incident team (most ambitious)

- **Problem → value:** Real incidents span outside and inside. A quadruped scouts terrain and stairs, a scanner builds the 3D picture, and the UniX robot is the **hands** indoors. One incident agent assigns tasks across robots.
- **Hardware:** Wanda 2.0 / Panther (manipulation) + Unitree Go2 or Genisom quadruped (scout) + SKYLANDX MetaCam (3D map) + optional XREAL (commander view).
- **Architecture / stack:**
  - Perception: MetaCam scan → shared map; quadruped camera → hazard detections pinned to the map.
  - Planning: laptop incident agent turns detections into tasks ("door blocked at B2 → send manipulator").
  - Control: each robot through its own vendor interface; a thin task bridge per robot (HTTP or ROS 2 where available).
- **48-hour plan:**
  - H0–6: confirm all three vendor interfaces; agree one coordinate frame.
  - H6–24: scan the venue; each robot reaches a named map location independently.
  - H24–40: one end-to-end hand-off: scout finds obstruction → manipulator clears it.
  - H40–48: rehearse the single hand-off until reliable; cut everything else.
- **3-minute demo script:** 3D map on screen → quadruped finds a blocked exit → task appears → UniX robot arrives, moves the box → map turns green.
- **Risks and fallbacks:** three closed or semi-closed stacks in 48 h is the main risk. Fallback: drop to two robots, or human-in-the-loop dispatch.
- **Judging angles:** *Innovation* and *technical depth* highest; *impact* — realistic multi-agency picture; *Leukerbad* — outdoor hazard + indoor care setting.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| UniX Wanda / Panther + **Unitree Go2 / B2** or **Genisom M1 / L1** | Outdoor and stair scouting plus indoor manipulation | High (two stacks, shared map) |
| + **SKYLANDX MetaCam** | Fast 3D scan / digital twin of the building for patrol routes and incident view | Low–medium (offline scan, export map) |
| + **XREAL** glasses | Operator or incident-commander view for teleoperation | Medium (video and overlay only) |
| + **D-Robotics RDK X5 / S100** | Independent on-robot perception node if UniX compute is closed | Low–medium |
| + **OriginFlow** EMG capture | Alternative teleoperation input for arm control | High, ⚠️ unverified compatibility |
| + **Binabik AI** / **coprod** | Vendor-neutral agent or interoperability layer across robots | Unknown — ask both teams |

## Questions to ask the UniX AI engineers on site

1. Which robots are here, and which can teams drive themselves versus engineer-operated only?
2. What does "fully open software and hardware interfaces" mean today: ROS 2 topics, a Python / HTTP API, or neither? Any docs you can share?
3. Can we send **navigation goals** (map pose or named waypoint) and read robot pose from an external laptop?
4. Can we get **live camera, depth and LiDAR streams** off the robot? At what rate, over what transport?
5. Is the **remote teleoperation system** here? What is the operator hardware, and can we record teleop sessions?
6. Are the Security skills (patrol, fire-cabinet check, fire-door test, corridor anomaly detection) installed on these units and callable?
7. Can we teach a **new skill by demonstration** within the event, and how many demonstrations and hours does that take?
8. Safety limits: maximum slope and threshold height, behaviour on connection loss, emergency stop, and may we mount an external sensor or carry a payload?

## Decision rule

- **Pick UniX AI for T02 if** your idea is indoor building safety or response that needs **arms and long runtime** (fire-safety rounds, teleoperated intervention, evacuation assistance) and the on-site team confirms at least waypoint navigation plus a camera stream — or commits an engineer to your team.
- **Avoid if** your concept needs outdoor terrain, stairs, snow, weatherproofing or a documented low-level API from hour one — choose a quadruped vendor and use UniX only as the indoor manipulator, if at all.

## Sources
- [UniX AI — Security Service application page](https://www.unix-group.ai/Security)
- [UniX AI — Applications page (teleoperation, open interfaces claim)](https://www.unix-group.ai/Applications)
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [Panther product page](https://www.unix-group.ai/Panther)
- [Martian product page](https://www.unix-group.ai/Martian)
- [UniPicker Pro product page](https://www.unix-group.ai/UniPicker)
- [36Kr Japan, 21 Dec 2025: shipments and sectors](https://36kr.jp/449686/)
- [Panther launch release, 8 Apr 2026 (TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [UniX AI company profile (this repo)](../UniX-AI.md)
