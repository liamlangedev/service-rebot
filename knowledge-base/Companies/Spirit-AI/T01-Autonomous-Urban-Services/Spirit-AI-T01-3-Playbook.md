---
type: challenge-playbook
company: "Spirit AI"
slug: Spirit-AI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Spirit AI × T01 — Hackathon Playbook

⬆ [Spirit AI profile](../Spirit-AI.md) · [Brief](Spirit-AI-T01-1-Brief.md) · [Products and solutions](Spirit-AI-T01-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- Assume **Moz1**, one unit, **indoors only** (IP40; the manual forbids rain, snow and open-air use). Whether it is on site, with the nav stack and SDK installed, is ⚠️ unverified — confirm in the first hour.
- Build order that survives bad luck: **navigation first** (vendor stack), **manipulation second** (scripted via SDK), **teleop as the fallback** for any step, **learned policy last**.
- The SDK returns RGB images only (per docs), so use **fiducial markers (e.g. AprilTags) on trays, bins and hand-over points** to get poses cheaply; that marker approach is our suggestion, not a vendor feature.
- Keep a person on the wireless emergency stop and stay at the low speed settings until mapped routes are proven.

## Solution approaches

### Concept 1 — Corridor room-service runner (safest)

- **Problem → value:** Leukerbad hotels and rehab clinics move towels, water, parcels and spa items along corridors all day with scarce staff. A robot that takes an item from reception to a numbered door frees staff for guests.
- **Hardware:** Moz1 (LiDAR base, two grippers, head camera). Optional: a tray or tote with a marker; a laptop as dispatcher.
- **Architecture / stack:**
  - Perception: Livox MID-360S LiDAR SLAM for localisation; head-camera RGB + marker detection for the hand-over pose.
  - Planning: tiny dispatcher (web form or chat) → ordered list of saved waypoints → vendor ROS 2 navigation service (pose sequence).
  - Control: Navigation2-based stack drives the base; MozRobot SDK plays a pre-recorded or interpolated Cartesian trajectory for pick and present.
  - Compute: nav Docker on the robot PC; dispatcher and marker detection on a laptop on the robot network.
- **48-hour plan:**
  - **H0–6:** confirm access, map one corridor while it is empty, save 4–5 waypoints, drive a loop with the vendor test script.
  - **H6–24:** dispatcher → nav service; scripted pick-from-tray and present-to-person; arrival announcement (speaker or phone).
  - **H24–40:** chain 2–3 deliveries; handle "nobody took the item" (timeout, return to base); run 10 full trials and log success.
  - **H40–48:** freeze code, record a backup video, rehearse.
- **3-minute demo script:** (0:00) "Room 12 wants towels" entered on a phone → (0:20) Moz1 picks the tote at "reception" → (1:00) drives the corridor, passes a via-point → (1:45) stops at the door marker, presents the tote, waits for removal → (2:20) returns and takes the next order → (2:40) show the trial log and the staff-minutes saved.
- **Risks and fallbacks:** nav tarball unavailable → drive the base by SDK velocity commands between markers, or by joystick; grasp unreliable → carry the item on a fixed tray and only do the hand-over gesture; robot time cut short → rehearse trajectories with the URDF in simulation.
- **Judging angles:** *Innovation* modest; *technical depth* in reliable nav + manipulation integration and measured success rate; *impact* clear labour case; *Leukerbad* direct fit for hotels and clinics.

### Concept 2 — Lobby and spa tidy patrol

- **Problem → value:** public indoor areas (lobbies, spa lounges, breakfast rooms) accumulate cups, cans and paper between cleaning rounds. A patrol robot that spots and bins items keeps spaces presentable. Mirrors Spirit AI's own WAIC tidy demo, so on-site staff know the task family.
- **Hardware:** Moz1. Optional: **D-Robotics RDK** board as an on-robot detection node (⚠️ unverified integration effort).
- **Architecture / stack:**
  - Perception: open-vocabulary or pre-trained object detector on `cam_high` RGB (laptop GPU or RDK); wrist camera for final alignment.
  - Planning: patrol = looped waypoint list; on detection, state machine *approach → align → grasp → go to bin → drop → resume*.
  - Control: nav service for patrol and bin trips; SDK Cartesian moves for a top-down grasp on a table of known height.
  - Compute: detector off-robot or on RDK; state machine on laptop.
- **48-hour plan:**
  - **H0–6:** mapping and patrol loop; pick two object classes (can, paper cup) and one table height.
  - **H6–24:** detector → table-plane position estimate → scripted grasp; bin waypoint and drop.
  - **H24–40:** sorting twist (cans vs paper into two bins); robustness to object position; count items per patrol.
  - **H40–48:** rehearse with judges placing the litter themselves.
- **3-minute demo script:** (0:00) judge places a can and a cup on a lounge table → (0:20) Moz1 on patrol detects them → (0:50) picks the can → (1:30) drives to the recycling bin, drops it → (2:10) returns for the cup → (2:40) dashboard: items collected, classes, patrol time.
- **Risks and fallbacks:** pose from RGB only is fragile → fix the table height and use a marker on the table edge for calibration; grasp fails → switch that single step to VR teleop and present it as supervised autonomy; detector latency → stop-and-look instead of detecting while moving.
- **Judging angles:** *Innovation* in autonomous upkeep with sorting (links to T03); *depth* in perception-to-grasp loop; *impact* cleaning labour; *Leukerbad* spa and hotel public areas.

### Concept 3 — Snow-to-door relay (multi-vendor)

- **Problem → value:** in an alpine village the hard part of delivery is the street (snow, slopes, steps); the fiddly part is indoors (reception, shelves, room doors). Split the job: a quadruped does the outdoor leg, Moz1 does the indoor handling.
- **Hardware:** Moz1 indoors + one quadruped with a cargo basket (**Unitree Go2 / B2**, **Genisom**, **MagicDog** or **AGIBOT D1** — whichever team you can pair with). Optional: **SKYLANDX MetaCam** scan of the hand-over zone.
- **Architecture / stack:**
  - Perception: quadruped's own navigation outside; marker on the quadruped's basket for Moz1 to localise the parcel.
  - Planning: shared job board (simple MQTT or HTTP service) with states *outdoor en route → at dock → transferred → delivered*.
  - Control: Moz1 nav to the entrance dock, SDK pick from the basket, nav to destination shelf or door.
  - Compute: job board on a laptop; each robot keeps its own stack — integrate at the message level only.
- **48-hour plan:**
  - **H0–6:** agree the hand-over spot and basket geometry with the quadruped team; Moz1 mapping.
  - **H6–24:** each robot's leg works alone; job board messages defined and tested with mocks.
  - **H24–40:** physical hand-over: quadruped parks at a floor marker, Moz1 picks from the basket; end-to-end runs.
  - **H40–48:** timing polish, backup video of the outdoor leg (weather may not cooperate at demo time).
- **3-minute demo script:** (0:00) order placed → (0:15) video or live view of the quadruped crossing snow → (0:50) it parks at the entrance dock → (1:10) Moz1 arrives, picks the parcel from the basket → (1:50) delivers it to a labelled pharmacy-pickup shelf or room door → (2:30) job board shows the full chain with timestamps.
- **Risks and fallbacks:** two robots double the failure modes → keep the interface to one parked pose and one marker; quadruped parking error → widen the basket and let Moz1 servo on the marker; no quadruped partner → a human courier plays the outdoor leg and you demo Concept 1.
- **Judging angles:** *Innovation* in heterogeneous hand-over; *depth* in cross-vendor orchestration; *impact* realistic last-mile split; *Leukerbad* strongest story of the four (snow outside, guests inside).

### Concept 4 — Language-tasked service agent with a learned skill (most ambitious)

- **Problem → value:** service work is varied ("bring two waters to the lounge and clear the table"). A language interface that composes navigation and manipulation skills is the direction Spirit AI itself demonstrates with Spirit v1.6.
- **Hardware:** Moz1 + Quest VR teleop kit; GPU access (A100-class for Spirit v1.5 inference per the README); optional **Binabik AI** agent layer or **D-Robotics** edge board (both ⚠️ unverified integration).
- **Architecture / stack:**
  - Perception: head and wrist RGB into the policy; detector for task grounding.
  - Planning: LLM task planner → calls a small skill library (`go_to(place)`, `pick(object)`, `place(target)`, `hand_over()`).
  - Control: most skills scripted (Concept 1–2); **one** skill learned — either a vendor-supplied Spirit checkpoint or the docs' Pi0.5 / openpi Moz1 adaptation fine-tuned on demonstrations you teleoperate.
  - Compute: policy server on a GPU machine or cloud, robot client on the robot network (the docs describe this server–client split for Pi0.5).
- **48-hour plan:**
  - **H0–6:** ask staff which checkpoint they can run on this robot; secure GPU; get Concept 1 navigation working regardless.
  - **H6–24:** skill library with scripted implementations; LLM planner producing valid skill sequences; start collecting teleop demonstrations for one skill.
  - **H24–40:** fine-tune and test the learned skill **only if** GPU and data are in hand by H24; otherwise keep it scripted and invest in planner robustness and replanning after failure.
  - **H40–48:** fix the demo to three spoken or typed instructions that work repeatedly.
- **3-minute demo script:** (0:00) judge types a free-form request → (0:15) planner shows the skill sequence on screen → (0:30) Moz1 navigates, picks, delivers → (1:45) judge moves the object mid-task; robot re-detects and replans → (2:30) show which steps were scripted and which were learned — be explicit.
- **Risks and fallbacks:** Spirit v1.5 fine-tuning is specified for **8× A100** → do not plan on it; no Moz1 checkpoint available → scripted skills behind the same planner interface; network latency to a remote policy server → run the learned skill only when stationary.
- **Judging angles:** *Innovation* and *depth* highest; *impact* generalisable service agent; *Leukerbad* multi-purpose helper for small hotels that cannot buy one robot per task. Highest risk of an empty-handed demo.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Moz1 + quadruped (Unitree Go2 / B2, Genisom, MagicDog, AGIBOT D1) | Outdoor leg on snow and slopes, indoor handling by Moz1 (Concept 3) | Medium — message-level only, one physical hand-over pose |
| Moz1 + D-Robotics RDK X5 / S100 | On-robot detection or voice node without a laptop; the two firms announced a partnership in May 2026 (Spirit v1.5 on Sunrise S600) | Low for a ROS 2 perception node; running Spirit v1.5 on the boards actually on site ⚠️ unverified |
| Moz1 + SKYLANDX MetaCam | Fast 3D scan of the venue for the pitch or a digital twin; the Moz1 relocaliser reads .ply / .pcd, so an external map *might* be usable (inference, ⚠️ unverified) | Low for visualisation; high-risk as a nav map |
| Moz1 + XREAL glasses | Staff see the robot's job queue and camera view; "summon" or approve hand-overs hands-free | Low–medium (app on the glasses talks to your dispatcher) |
| Moz1 + Binabik AI | Agentic task layer over your skill library (Concept 4) | Unknown — depends on their Moz1 / ROS 2 adapter |
| Moz1 + WUJI Hand | Dexterous end effector instead of two-finger gripper | High — mechanical and bus integration; not a 48-hour job |

## Questions to ask the Spirit AI engineers on site

1. Which robot is here, how many units, and how is robot time shared between teams?
2. Is the **SLAM navigation stack** (`nav_stack`, Docker image, `navigation_interfaces`) installed on this unit, and can we get the tarball and example script?
3. Can the nav stack drive the base **while** the MozRobot SDK commands the arms and torso — or do we have to switch modes between driving and manipulating?
4. What are the **payload per arm**, reach, and battery runtime? Can it traverse door thresholds or ramps, and at what slope?
5. Can we read **depth** from the D455 / D405 alongside the SDK (or via ROS 2 topics), and is a hand–eye calibration available?
6. Is there a ready **Moz1 checkpoint** (Spirit v1.5, v1.6 or the Pi0.5 adaptation) for pick-and-place or hand-over that we can call, and on what compute?
7. Is English documentation or an SDK cheat sheet available for the event?
8. What speed and safety settings do you require for demos near the public?

## Decision rule

- **Pick Spirit AI for T01 if** your idea lives entirely indoors (hotel, clinic, shop, lobby), needs both driving and two-arm handling, and you have confirmed robot access plus the navigation stack by the end of hour 1.
- **Avoid if** your concept needs outdoor mobility, stairs, a fleet, or a policy trained during the weekend — or if you cannot tolerate sharing a single robot.

## Sources
- [Docs: Moz1 SLAM navigation](https://docs.spirit-ai.com/zh/slam-nav/slam_navigation.html)
- [Docs: Moz1 mechanical structure](https://docs.spirit-ai.com/zh/moz1/mechanics.html)
- [Docs: MozRobot SDK API reference](https://docs.spirit-ai.com/zh/sdk/api.html)
- [Docs: MozRobot SDK data format](https://docs.spirit-ai.com/zh/sdk/data-format.html)
- [Docs: MozRobot SDK examples](https://docs.spirit-ai.com/zh/sdk/examples.html)
- [Docs: Moz1 safety requirements](https://docs.spirit-ai.com/zh/moz1/safety.html)
- [Spirit AI news: WAIC 2026, Moz1 demos and Moz2 debut](https://www.spirit-ai.com/en/news/48)
- [Spirit AI news: D-Robotics partnership](https://www.spirit-ai.com/en/news/45)
- [GitHub: Spirit-AI-Team/spirit-v1.5](https://github.com/Spirit-AI-Team/spirit-v1.5)
- [Spirit AI company profile (Pi0.5 adaptation, teleop kit, general research)](../Spirit-AI.md)
