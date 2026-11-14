---
type: challenge-playbook
company: "Galaxea"
slug: Galaxea
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Galaxea × T02 — Hackathon Playbook

⬆ [Galaxea profile](../Galaxea.md) · [Brief](Galaxea-T02-1-Brief.md) · [Products and solutions](Galaxea-T02-2-Products-and-Solutions.md)

**Read this first:** Galaxea is a **fit 2/5** for T02. Every concept below keeps the robot **indoors on flat floors** and uses it for what it is good at: two arms operating human-built equipment. Which robots are on site is unconfirmed — check the booth before committing.

## Solution approaches

### Concept 1 — Remote Hands (teleoperated intervention in a hazard room)

- **Problem → value:** After a gas alarm, leak or fire-system trigger, someone has to enter a plant room to close a valve or flip a breaker. Send the robot instead; the human stays outside.
- **Hardware:** R1 Pro or R1 Lite + whatever teleop rig Galaxea brings (VR headset or leader arms). Optional: XREAL glasses as the operator's camera view.
- **Architecture / stack:** Robot cameras (head depth + two wrist) → video stream to operator station → operator commands via Galaxea teleop → ROS 2 Humble arm / gripper / torso / chassis control topics. Add one ROS 2 node that logs every action with timestamps and snapshots into an incident report. Compute: robot on-board for control, laptop for the UI and log.
- **48-hour plan:**
  - **H0–6:** Get teleop working end to end; list the available topics (`ros2 topic list`); build a mock panel (ball valve, rocker switch, door handle, small container).
  - **H6–24:** Operator UI with three camera views and a task checklist; action logger; practise the three interventions until each takes under 60 s.
  - **H24–40:** Add safeguards (speed limit near the panel, dead-man switch, loss-of-link stop); auto-generated incident report (photos before / after).
  - **H40–48:** Rehearse with an operator who has no line of sight to the robot; record a backup video.
- **3-minute demo script:** (0:00) Alarm scenario, operator sits behind a screen. (0:30) Robot drives in, operator closes the valve. (1:30) Flips the breaker, retrieves the sample container. (2:30) Show the generated incident report and state what the human was not exposed to.
- **Risks and fallbacks:** Teleop latency over venue Wi-Fi → use wired LAN or a dedicated router. No R1 available → run the same story on a **LEMO** as a bench-top remote-handling cell (under 50 ms leader-arm latency).
- **Judging angles:** Innovation low–medium; technical depth medium; real-world impact high and easy to explain; Leukerbad relevance: any building with plant rooms — baths, clinics, hotels, cable-car stations.

### Concept 2 — Plant-Room Rounds (semi-autonomous indoor inspection with intervention)

- **Problem → value:** Routine checks of gauges, indicator lamps, extinguishers and escape routes are skipped when staff are short or during an incident. The robot does the round, flags anomalies, and can act on simple ones.
- **Hardware:** R1 Pro or R1 Lite. Optional: D-Robotics RDK X5 as an edge box for detection; SKYLANDX MetaCam to build the reference map.
- **Architecture / stack:** Waypoint list → navigation (Galaxea's stack if it is exposed; otherwise recorded teleop paths replayed through chassis commands) → at each stop, torso and head pose a camera at the target → a vision-language model reads the gauge / lamp / presence → rules decide "OK / warn / act" → for "act", hand over to a teleoperator (Concept 1). Compute: VLM on a laptop GPU or a cloud API; robot control on-board.
- **48-hour plan:**
  - **H0–6:** Confirm navigation access. If absent, decide immediately on the path-replay fallback. Set up 4–5 inspection stops.
  - **H6–24:** Camera-pose routine per stop; VLM prompts with structured JSON output; anomaly rules; dashboard.
  - **H24–40:** Inject faults (gauge out of range, missing extinguisher, blocked exit) and tune; add teleop escalation.
  - **H40–48:** Three full rounds without intervention; backup video.
- **3-minute demo script:** (0:00) Dashboard shows the round. (0:30) Robot visits two normal stops. (1:15) Third stop: gauge out of range → alert. (1:45) Operator takes over and closes the valve. (2:30) Report with photos and timeline.
- **Risks and fallbacks:** Navigation not exposed → path replay over a 5–10 m course. VLM misreads → use large-print gauges and coloured lamps, show the confidence value honestly.
- **Judging angles:** Innovation medium; technical depth medium–high (perception + navigation + manipulation); impact high for facility operators; Leukerbad relevance: thermal-bath and clinic technical rooms.

### Concept 3 — Scout and Fixer (multi-robot response)

- **Problem → value:** One robot cannot both reach the problem and fix it. A legged scout covers rough ground and finds the fault; the Galaxea robot performs the manipulation where the floor allows.
- **Hardware:** R1 Pro (fixer) + a quadruped from Unitree, Genisom, AGIBOT or Magiclab (scout) + SKYLANDX MetaCam (shared 3D map). Optional: XREAL for the incident commander.
- **Architecture / stack:** MetaCam scan → shared map / simple digital twin → scout patrols and detects an anomaly (thermal or visual) → publishes a task with a pose to a small coordinator (ROS 2 topic or MQTT) → R1 drives to the nearest reachable point and executes the intervention (teleop, or the learned skill from Concept 4) → status back to the twin. Compute: coordinator and UI on a laptop; each robot keeps its own controller.
- **48-hour plan:**
  - **H0–6:** Split the team by robot. Agree on one message format (task id, pose, type, status). Each side gets its robot moving.
  - **H6–24:** Scout detection + task publishing; R1 intervention (start from Concept 1); common frame alignment (use fiducial markers, not full map fusion).
  - **H24–40:** End-to-end hand-over; commander view; failure handling.
  - **H40–48:** Rehearse the full chain five times; backup video.
- **3-minute demo script:** (0:00) Map and scenario. (0:30) Scout finds the "leak". (1:15) Task appears, R1 moves in. (1:45) R1 closes the valve. (2:30) Twin shows "resolved"; explain how it scales.
- **Risks and fallbacks:** Two vendor stacks in 48 h is the main risk → keep the interface to one message; if frame alignment fails, place the R1 at a fixed station. If one robot is unavailable, the other half still demos alone.
- **Judging angles:** Innovation high; technical depth high; impact high; Leukerbad relevance strong if the scout part is shown on stairs or outdoors.

### Concept 4 — One-Shot Skill for Responders (learned autonomous intervention)

- **Problem → value:** Teleoperation needs a trained operator and a good link. If the robot can execute "close the red valve" or "press the emergency stop" by itself, a dispatcher only has to give the order — and it keeps working when the link is poor.
- **Hardware:** R1 Lite or R1 Pro; LEMO + A1Z-T as a second data-collection rig if available. Off-board RTX-class GPU.
- **Architecture / stack:** Collect 50–100 teleop demos per skill (rosbag / MCAP) → convert with GalaxeaLeRobotToolkit → train GalaxeaDP (diffusion policy) or fine-tune G0.5 if an 80 GB-class GPU is provided → deploy with EFMNode at 15 Hz → language or button trigger from the dispatcher UI → operator can interrupt and take over by teleop.
- **48-hour plan:**
  - **H0–6:** Confirm GPU availability and teleop recording; pick **one** skill; fix the scene (lighting, panel position).
  - **H6–24:** Record demos with varied start poses; first training run overnight.
  - **H24–40:** Evaluate, collect corrections, retrain; add the take-over path; try a second skill only if the first exceeds about 70% success.
  - **H40–48:** Measure success over 20 trials and put the number on the slide; backup video.
- **3-minute demo script:** (0:00) Dispatcher types the command. (0:20) Robot executes the skill autonomously, twice from different start poses. (1:30) Someone disturbs the scene; robot recovers or operator takes over. (2:15) Success rate, number of demos, training time.
- **Risks and fallbacks:** Policy does not converge → fall back to Concept 1 with the learned skill shown as a partial result. No big GPU → diffusion policy only, or zero-shot G0.5 on a simple pick.
- **Judging angles:** Innovation medium–high; technical depth high; impact medium (single skill); Leukerbad relevance moderate.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| R1 + quadruped (Unitree Go2 / B2, Genisom, AGIBOT D1, Magiclab) | Scout finds, R1 fixes (Concept 3) | High — two stacks; keep to one shared message |
| R1 + SKYLANDX MetaCam | Reference 3D map of the site for the dashboard or digital twin | Low–medium — offline scan, display only |
| R1 + XREAL glasses | Head-worn operator or commander view of robot cameras | Medium — video streaming to the glasses |
| R1 + D-Robotics RDK X5 / S100 | Edge detection (gauges, people, smoke) without a laptop | Medium — ROS 2 image bridge |
| R1 Pro + WUJI Hand | Dexterous operation of knobs, keys, small switches | High — mechanical and driver integration ⚠️ unverified compatibility |
| LEMO + OriginFlow EMG capture | Alternative operator input for remote handling | High — research-grade |
| R1 + Binabik AI or Genisom SomaMind agent layer | Task-level orchestration of "inspect, decide, act" | Unknown — depends on their SDKs |

## Questions to ask the Galaxea engineers on site

1. Which robots are here (R1 Pro, R1 Lite, LEMO, Nexo), how many, and how are time slots shared?
2. Is the navigation stack open to us — can we build a map and send waypoint goals over ROS 2, or only velocity commands to the chassis?
3. Which teleop rigs did you bring (VR, leader arms, whole-body), and what latency should we expect over the venue network? Can we teleoperate from another room?
4. What are the floor limits: maximum slope, door-threshold height, wet floors? Is there any IP rating?
5. Where is the e-stop, is there a wireless one, and can we set speed and force limits in software?
6. How much torque or grip force can the arm and gripper apply — enough to turn a quarter-turn ball valve or pull a breaker?
7. Is fine-tuning compute provided for G0.5 (80 GB-class GPU), or should we plan for a small diffusion policy?
8. Can we mount our own sensor (thermal camera, gas sensor) and power it from the robot?

## Decision rule

- **Pick Galaxea for T02 if** your idea is an indoor intervention — a robot that operates valves, switches, doors or containers so a person does not have to enter — and you either accept teleoperation as the core or have a second vendor covering mobility and sensing.
- **Avoid if** your idea needs outdoor or rough-terrain movement, wide-area patrol or mapping, ruggedised hardware, or a vendor with a proven safety or inspection record.

## Sources
- [Galaxea blog — WRC 2026 (23 Aug 2026)](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)
- [GitHub — OpenGalaxea organisation](https://github.com/OpenGalaxea)
- [GitHub — OpenGalaxea/EFMNode](https://github.com/OpenGalaxea/EFMNode)
- [GitHub — awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers)
- [Galaxea company profile (this repo)](../Galaxea.md)
