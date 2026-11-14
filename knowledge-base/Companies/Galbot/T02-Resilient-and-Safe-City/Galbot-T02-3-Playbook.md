---
type: challenge-playbook
company: "Galbot"
slug: Galbot
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Galbot × T02 — Hackathon Playbook

⬆ [Galbot profile](../Galbot.md) · [Brief](Galbot-T02-1-Brief.md) · [Products and solutions](Galbot-T02-2-Products-and-Solutions.md)

**Read first:** Galbot is a **2/5** fit for T02. Every concept below keeps the G1 **indoors on flat floors** and uses what it is actually good at: unattended operation, navigation between known points, and hands. Assumed on-site hardware is a G1 with grippers (not confirmed). Exact SDK call names are in the docs shipped inside the GalbotSDK repo; check them at H0.

## Solution approaches

### Concept 1 — Indoor safety-round robot ("inspect and report")

- **Problem → value:** Hotels, spas and clinics need recurring safety rounds (escape routes clear, extinguishers present, doors closed, leaks on the floor). A robot does the round at night and files a dated photo report with flagged anomalies.
- **Hardware:** Galbot G1. Optional: D-Robotics RDK board with an added thermal or gas sensor carried in the gripper or on the torso (G1 has neither).
- **Architecture / stack:** SDK mapping + localization → list of checkpoints → point-to-point navigation → head / torso camera snapshots → VLM (cloud or team laptop GPU) answers a per-checkpoint checklist → JSON report + web dashboard. Compute: navigation on the robot's AGX Orin; VLM off-board.
- **48-hour plan:**
  - H0–6: get SDK connected, build the map, drive to 2 waypoints, pull a camera frame.
  - H6–24: checkpoint list, VLM checklist prompts, anomaly schema, simple dashboard.
  - H24–40: staged anomalies (box in front of exit, extinguisher removed, wet-floor patch), tune prompts, add voice alert.
  - H40–48: three clean end-to-end runs, record backup video.
- **3-minute demo script:** (0:00) show the map and route → (0:30) robot visits checkpoint A, reports "OK" → (1:15) judge places a box in front of the exit sign → (1:45) robot flags it, dashboard shows photo + location → (2:30) show the full night-round report.
- **Risks and fallbacks:** navigation unreliable in a crowded hall → shorten to 2 checkpoints or reposition by teleop / joystick and keep the perception pipeline. VLM latency → cache prompts, use a smaller local model.
- **Judging angles:** innovation low (quadrupeds do this elsewhere); technical depth medium; impact real for small operators; Leukerbad relevance: spa hotels and rehab clinics with night-time staffing gaps.

### Concept 2 — Unattended emergency supply point

- **Problem → value:** When a resort is cut off or staff are stretched (storm, road closure, power incident), a robot-run point keeps handing out first-aid kits, medication packs, blankets and torches 24/7 and logs what went to whom.
- **Hardware:** Galbot G1 + a shelf. Optional: XREAL glasses for a remote pharmacist / coordinator approving requests.
- **Architecture / stack:** request by voice or tablet → item lookup → navigate to shelf → grasp (GraspVLA if available on the robot, otherwise fixed shelf slots + SDK motion planning + wrist depth camera) → hand-over using wrist F/T to detect the take → inventory log. Compute on board; speech / LLM off-board.
- **48-hour plan:**
  - H0–6: confirm grasp path with Galbot engineers (GraspVLA preloaded or scripted picks); pick one item from one slot.
  - H6–24: 4–6 items, hand-over detection, request interface, inventory state.
  - H24–40: "disruption mode" logic (rationing rules, priority requests, low-stock alert), remote approval view.
  - H40–48: reliability runs, backup video.
- **3-minute demo script:** (0:00) scenario: valley road closed, clinic short-staffed → (0:30) judge asks for a first-aid kit, robot picks and hands over → (1:30) second request for a restricted item triggers remote approval → (2:15) dashboard shows stock, log and low-stock alert.
- **Risks and fallbacks:** grasp failures on soft or shiny items → rigid boxes with known slots. No GraspVLA on the robot → scripted picks. This concept overlaps T01 / T04; frame it clearly around disruption and continuity.
- **Judging angles:** innovation medium; technical depth medium–high; impact credible because it reuses Galbot's **proven** pharmacy / warehouse pattern; Leukerbad relevance: many elderly guests and clinics in a mountain resort.

### Concept 3 — Inspect and act (a robot that fixes what it finds)

- **Problem → value:** Inspection robots usually only report. A robot with arms can perform the first response step: press an emergency stop, close a door or valve, move an obstacle off an escape route, place a warning cone.
- **Hardware:** Galbot G1. Optional: XREAL for operator confirmation; SKYLANDX MetaCam for a prior 3D scan of the space.
- **Architecture / stack:** Concept 1 pipeline → anomaly classified into an action type → operator confirms (human in the loop) → SDK whole-body planning to a pre-taught action, with wrist F/T for contact tasks (push button, pull handle) → verify with a second camera check.
- **48-hour plan:**
  - H0–6: Concept 1 minimum (navigate + snapshot).
  - H6–24: two manipulation primitives (press button, move a light box) with force thresholds.
  - H24–40: link detection → confirmation → action → verification; add a third primitive if stable.
  - H40–48: rehearse, cut anything flaky.
- **3-minute demo script:** (0:00) robot on patrol → (0:40) finds a box blocking the exit, asks operator → (1:00) operator confirms, robot moves it → (1:50) finds an "alarm" light, presses the mock stop button → (2:30) before / after report.
- **Risks and fallbacks:** contact tasks need tuning → keep to one robust primitive and fall back to Concept 1 for the rest. Safety near judges → slow speeds, clear zone.
- **Judging angles:** innovation medium–high (intervention, not only observation); technical depth high (navigation + perception + force-aware manipulation); impact strong; Leukerbad relevance: plant rooms in spas and clinics.

### Concept 4 — Mixed responder team: quadruped scouts, G1 is the indoor base

- **Problem → value:** One robot type cannot cover an alpine incident. A quadruped scouts terrain the G1 cannot reach; the G1 stays in the shelter or control room and does the handling: loads supplies onto the dog, swaps its payload, hands items to people.
- **Hardware:** Galbot G1 + a quadruped (Unitree Go2 / B2, Genisom AI M1 / L1 or AGIBOT D1) + optional SKYLANDX MetaCam for the shared map.
- **Architecture / stack:** shared task board (simple message bus on a laptop) → quadruped runs its own vendor stack for outdoor / stairs legs → docking pose at a marked station → G1 detects the dog's payload tray (fiducial marker) and loads the requested item → dashboard tracks the mission. Each robot keeps its own on-board compute.
- **48-hour plan:**
  - H0–6: prove each robot alone (G1 pick; dog walks a route).
  - H6–24: docking station, tray detection, load primitive.
  - H24–40: mission logic end to end, map overlay.
  - H40–48: rehearsal; decide whether the dog leg is live or pre-recorded.
- **3-minute demo script:** (0:00) incident call: person needs a first-aid kit up a stairway → (0:30) G1 picks the kit and loads the dog → (1:30) dog climbs stairs / leaves the hall → (2:15) dashboard shows delivery confirmed and the next task queued.
- **Risks and fallbacks:** two vendor stacks in 48 h is the main risk → hand-coded handshake over a shared laptop; if docking fails, a human places the dog at the station. Needs two hardware slots.
- **Judging angles:** innovation high; technical depth high; impact high; Leukerbad relevance strongest of the four (steep terrain, snow, stairs handled by the dog).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| G1 + Unitree / Genisom AI / AGIBOT D1 quadruped | Outdoor and stair coverage plus indoor handling (Concept 4) | High: two stacks, docking |
| G1 + SKYLANDX MetaCam | Fast 3D scan of the venue as inspection map / digital-twin backdrop | Medium: map formats differ; may stay visual only |
| G1 + XREAL glasses | Remote operator sees robot camera and approves actions | Medium: video stream + simple UI |
| G1 + D-Robotics RDK X5 + external sensor | Adds thermal / gas sensing that G1 lacks | Low–medium: separate node, Wi-Fi to dashboard |
| G1 + WUJI Hand | Finer manipulation (switches, valves) | High: mounting and control not confirmed for G1 |
| Galbot open code (Click-and-Traverse, OpenWBT) on a Unitree humanoid | Cluttered-scene traversal or whole-body teleop without Galbot hardware | Medium–high: check robot version compatibility |

## Questions to ask the Galbot engineers on site

1. Which robot is here (G1, G1 Lite, ET1), and which SDK / robot-environment version does it run (SDK V1.10.0 expects V1.18)?
2. Is low-level control unlocked, and can we stream RGB, depth and LiDAR point clouds to a laptop over the venue network?
3. How do we build and save a map, and how reliable is point-to-point navigation in a crowded hall?
4. Is GraspVLA (or the retail picking stack) preloaded and callable, or do we script grasps ourselves?
5. Is there any teleoperation or remote-takeover tool for G1 we can use as a fallback?
6. Can we read the wrist force/torque sensors in real time for contact tasks (button press, hand-over detection)?
7. Is any part of the planned Site Inspection kit available as a preview?
8. What are the safety rules for running the G1 near the public (speed limits, e-stop, supervision)?

## Decision rule

- **Pick Galbot for T02 if** your idea happens indoors on flat floors and needs a robot that can both navigate and use its hands (inspect-and-act, emergency supply point), or you want it as the handling station in a multi-robot team.
- **Avoid if** your idea needs outdoor mobility, stairs, snow, hazard sensors or a ready-made inspection / rescue stack; choose a quadruped vendor instead.

## Sources
- [Galbot company profile (this repo)](../Galbot.md)
- [Galbot G1 product page](http://www.galbot.com/g1/)
- [Galbot developer portal (kits, tiers, SDK capabilities)](https://developer.galbot.com/?lang=en)
- [GalbotSDK README](https://raw.githubusercontent.com/GalaxyGeneralRobotics/GalbotSDK/HEAD/README.md)
- [GitHub org GalaxyGeneralRobotics](https://github.com/GalaxyGeneralRobotics)
- [Click-and-Traverse repo](https://github.com/GalaxyGeneralRobotics/Click-and-Traverse)
- [GraspVLA paper (arXiv 2505.03233)](https://arxiv.org/abs/2505.03233)
- [NavFoM project page](https://pku-epic.github.io/NavFoM-Web)
