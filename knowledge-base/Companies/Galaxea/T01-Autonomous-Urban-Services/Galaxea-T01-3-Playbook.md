---
type: challenge-playbook
company: "Galaxea"
slug: Galaxea
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Galaxea × T01 — Hackathon Playbook

⬆ [Galaxea profile](../Galaxea.md) · [Brief](Galaxea-T01-1-Brief.md) · [Products and solutions](Galaxea-T01-2-Products-and-Solutions.md)

> **Before you plan:** confirm at the booth (1) which robot is available (R1 Pro, R1 Lite, LEMO), (2) whether a GPU for G0.5 inference is provided, (3) what navigation software is on the robot. The concepts below are written so that each still works if the answer to (3) is "none".
> Topic names, ROS distro and navigation features for the current robots are ⚠️ unverified — the official docs portal could not be read. The legacy R1 exposes chassis velocity as a `Twist` topic; expect the same pattern.

## Solution approaches

### Concept 1 — Order-to-bag service point (safest)

- **Problem → value:** small resort shops, pharmacies and hotel desks are short-staffed off-peak. A robot counter that picks and bags an order placed by phone gives 24-hour pick-up for guests (spa kit, snacks, pharmacy basics, rental accessories).
- **Hardware:** LEMO desktop dual-arm kit, or an R1 Lite / R1 Pro parked at a shelf. No driving needed.
- **Architecture / stack:**
  - Perception: robot cameras → G0.5 (its own target box + trajectory hint) or an open-vocabulary detector for item selection.
  - Planning: tiny order web app → list of items → one language instruction per item ("put the sunscreen in the bag").
  - Control: G0.5 policy server on an off-board GPU (more than 8 GB VRAM) + ROS 2 client on the robot; fallback is a small diffusion / ACT policy trained on your own demos (GalaxeaDP or LeRobot).
- **48-hour plan:**
  - H0–6: get teleop working; fix the scene (shelf, 5–6 items, open bag or tray); test zero-shot G0.5 on each item.
  - H6–24: record 30–60 teleop demos per weak item; convert with GalaxeaLeRobotToolkit; train a small policy overnight.
  - H24–40: order web app + task sequencer + retry logic (re-prompt on failed grasp); measure success rate over 20 orders.
  - H40–48: freeze, rehearse, record a backup video.
- **3-minute demo script:** judge scans QR, orders 3 items → robot picks and bags each while a screen shows the model's subtask text and target box → robot pushes the bag to the hand-over zone → show the success-rate tally and one deliberate disturbance (move an item mid-task).
- **Risks and fallbacks:** zero-shot fails on some items → restrict the catalogue to items that work; bag handling too hard → use a rigid tray; no GPU → teleop-assisted mode with autonomy on the easy items.
- **Judging angles:** mirrors Galaxea's own WRC fulfilment demo (credible); technical depth through measured success rates; impact for seasonal labour shortage; Leukerbad angle: after-hours spa and pharmacy pick-up for guests.

### Concept 2 — Hotel / clinic service runner

- **Problem → value:** staff walk kilometres per shift carrying towels, water, small items between a store room and guest floors. A mobile manipulator fetches the item and brings it to a hand-over point.
- **Hardware:** R1 Pro or R1 Lite. Optional: SKYLANDX MetaCam to pre-scan the corridor; XREAL glasses or a phone for the staff request UI.
- **Architecture / stack:**
  - Perception: chassis LiDAR + IMU for localisation; head / wrist cameras for manipulation.
  - Planning: if the robot ships navigation, use it; otherwise run an open-source 2D SLAM + planner (for example slam_toolbox + Nav2 on ROS 2) publishing to the chassis velocity topic, or fixed waypoints with fiducial markers at the two stations.
  - Control: navigation and manipulation as two separate skills handed over by a simple state machine (go to shelf → pick → go to guest point → hand over → return). G0.5 or a trained policy only for the pick and the hand-over.
  - Compute: navigation on-board; VLA off-board over Wi-Fi.
- **48-hour plan:**
  - H0–6: drive the base from your own node; record a LiDAR bag; decide SLAM vs markers by hour 6.
  - H6–24: reliable A → B → A driving at low speed with obstacle stop; in parallel collect pick and hand-over demos.
  - H24–40: integrate the state machine; add request UI and speech or screen feedback; 10 end-to-end runs.
  - H40–48: tune, cap speed, rehearse in the actual demo space.
- **3-minute demo script:** "guest" requests a towel and a water bottle → robot picks both at the shelf → drives 10–15 m, stops for a person stepping in its path → hands over at chest height → returns; dashboard shows map, state and trip time.
- **Risks and fallbacks:** localisation drift → fiducial markers at stations; Wi-Fi drop → on-board G0 Tiny (R1 Pro Orin) or scripted grasp; crowded venue → roped-off lane; pick fails → items pre-loaded in a tray on the torso, demo focuses on delivery + hand-over.
- **Judging angles:** full "move + deliver" loop on one robot; clear real-world fit for Leukerbad's hotels and rehab clinics; honest metrics (trip time, success out of 10).

### Concept 3 — Public-area upkeep robot

- **Problem → value:** spa lounges, breakfast rooms and lobbies need constant tidying: left-behind cups, used towels, wet table tops. A robot that patrols and resets a zone frees staff for guests.
- **Hardware:** R1 Lite (closest to the dataset: wiping, cleaning and arranging tasks were recorded on it) or R1 Pro.
- **Architecture / stack:**
  - Perception: G0.5 with language prompts per chore ("put the towel in the basket", "wipe the table").
  - Planning: patrol list of 2–3 fixed stations; at each one a vision-language check ("is anything out of place?") selects the chore prompt.
  - Control: G0.5 fine-tuned on your demos if an 80 GB-class GPU is available, otherwise a small policy per chore; base moves between stations by waypoint.
- **48-hour plan:**
  - H0–6: choose two chores; test zero-shot; set up stations.
  - H6–24: 50+ demos per chore with varied object positions; start training.
  - H24–40: station patrol + chore selection + evaluation with randomised clutter.
  - H40–48: polish and rehearse; prepare before / after photos.
- **3-minute demo script:** judge messes up a table (towel, two cups, spill) → robot arrives, bins the cups, baskets the towel, wipes → moves to station 2 and reports "nothing to do" → summary screen of chores done.
- **Risks and fallbacks:** deformable towels are hard → rigid items only; wiping quality poor → present it as "collect and sort", drop wiping; patrol unreliable → single station.
- **Judging angles:** "maintain the city" covered with manipulation, not just driving; technical depth in learned policies and language-driven chore choice; Leukerbad relevance: thermal-bath and hotel housekeeping load.

### Concept 4 — Indoor-outdoor delivery relay (most ambitious)

- **Problem → value:** village delivery in Leukerbad means snow, slopes and steps outside, shelves and bags inside. No single robot does both. Galaxea packs and loads; a quadruped carries the parcel through the street.
- **Hardware:** R1 Pro or R1 Lite (pack and load) + a quadruped from Unitree, Genisom or Magiclab with a cargo box (outdoor leg). Optional: D-Robotics RDK board on the quadruped for perception.
- **Architecture / stack:**
  - Dispatcher: one order service assigns "pack" to the Galaxea robot and "carry" to the quadruped; shared message bus (ROS 2 or plain MQTT / HTTP if the two stacks differ).
  - Galaxea side: Concept 1 picking + a learned "place parcel into the box on the dog" skill; docking by fiducial marker on the cargo box.
  - Quadruped side: vendor navigation or teleop-assisted route to the recipient.
- **48-hour plan:**
  - H0–6: prove the two robots can exchange one message; fix box geometry and docking pose.
  - H6–24: packing skill and loading skill demos; quadruped route with payload.
  - H24–40: end-to-end relay with order tracking page.
  - H40–48: rehearse; record the outdoor leg on video in case of weather or venue limits.
- **3-minute demo script:** order placed → R1 bags the items → quadruped docks → R1 loads the box → quadruped walks out (live or video for the outdoor part) → recipient confirms on phone.
- **Risks and fallbacks:** two vendor stacks in 48 hours is the main risk → keep the interface to one "ready / loaded / delivered" message; loading skill unreliable → fixed-height shelf hand-off instead of placing onto the robot; no quadruped slot → a human courier closes the loop and the demo falls back to Concept 1.
- **Judging angles:** strongest innovation and Leukerbad story (alpine last mile); shows system thinking across vendors; technical depth is in the hand-off.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Galaxea R1 + Unitree / Genisom / Magiclab quadruped | indoor pack-and-load + outdoor last leg (Concept 4) | High — two stacks, physical docking |
| Galaxea R1 + SKYLANDX MetaCam | fast 3D scan of the venue as a prior map or digital twin for the dashboard | Medium — map format conversion ⚠️ unverified |
| Galaxea R1 / LEMO + XREAL glasses | hands-free staff UI: see robot state, approve or correct tasks | Low to medium — separate app talking to your order service |
| Galaxea R1 + D-Robotics RDK | extra on-board perception node (person detection, marker tracking) without loading the main computer | Medium — ROS 2 bridge |
| LEMO + Galaxea R1 | LEMO as fixed packing cell, R1 as runner between cell and guest | Medium — one vendor, shared tooling |
| Galaxea R1 + WUJI Hand | dexterous end-effector for bags, zips, handles | High — mechanical and driver work; not advised in 48 hours |
| Galaxea R1 + Binabik AI or coprod stack | higher-level agent / orchestration layer over Galaxea skills | Unknown — ask both booths |

## Questions to ask the Galaxea engineers on site

1. Which robots can teams actually use (R1 Pro, R1 Lite, LEMO), how many, and in what time slots?
2. Does the robot ship with mapping, localisation and path planning? If yes, what is the API; if no, which topics give LiDAR, odometry and velocity command, and which ROS 2 distro?
3. Is a GPU provided for G0.5 inference, and is any 80 GB-class GPU available for fine-tuning — or should we plan for a small policy?
4. Which G0.5 checkpoint works best zero-shot on the unit here, and does its action space drive the chassis or only arms and torso?
5. What teleop rig is on site (leader arms, VR), and how many demos per task do you recommend for a reliable pick-and-place?
6. What are the safe limits: max base speed around people, e-stop behaviour, thresholds or ramps the base can cross?
7. Can we mount a tray, basket or marker on the robot, and what payload is safe on the torso or chassis?
8. Is the dark-store fulfilment software from WRC 2026 (order intake, sequencing) available in any form, or only the model?

## Decision rule

- **Pick Galaxea for T01 if** your idea is an indoor service task that needs two arms on a mobile base — pick, pack, carry, hand over, tidy — and you are comfortable with a teleop-data-and-policy workflow and have a GPU.
- **Avoid if** your concept depends on outdoor driving, snow, slopes or stairs, on proven off-the-shelf autonomous navigation, or if you cannot get confirmed robot time and compute in the first hours.

## Sources
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics)
- [PR Newswire — Galaxea AI at WRC 2026](https://en.prnasia.com/story/545003-0.shtml)
- [Galaxea blog — G0.5](https://galaxea-dynamics.com/blogs/developer-hub/galaxea-g05-a-new-generation-embodied-foundation-model-for-robotics)
- [GitHub — OpenGalaxea/GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA)
- [GitHub — OpenGalaxea organisation](https://github.com/OpenGalaxea)
- [GitHub — OpenGalaxea/awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers)
- [GitHub — userguide-galaxea organisation](https://github.com/userguide-galaxea)
- [Hugging Face — Galaxea Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset)
- [Galaxea legacy user guide — R1 software guide](https://userguide-galaxea.github.io/Product_User_Guide/Guide/R1/Software_Guide/)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)
- [Galaxea company profile (this repo)](../Galaxea.md)
