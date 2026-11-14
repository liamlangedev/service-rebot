---
type: challenge-playbook
company: "Galbot"
slug: Galbot
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Galbot × T01 — Hackathon Playbook

⬆ [Galbot profile](../Galbot.md) · [Brief](Galbot-T01-1-Brief.md) · [Products and solutions](Galbot-T01-2-Products-and-Solutions.md)

**Assumptions (confirm in the first 30 minutes):** a **Galbot G1** with grippers is on site ⚠️ unconfirmed; GalbotSDK V1.10.0 high-level navigation and arm planning are usable; G1 works **indoors on flat floor only**. All concepts keep G1 inside one building and one floor.

**Rule for every concept:** build the scripted version first (fixed shelf poses, known items), then swap in learned grasping and free-form language only if time remains.

## Solution approaches

### Concept 1 — Alpine Service Point (robot concierge kiosk)

- **Problem → value:** small hotels, spa receptions and the tourist office cannot staff a desk 24/7. A robot that answers questions and hands out physical items (towel, water, bus card, OTC item, rental key) extends service hours without extra staff. Mirrors Galbot's Space Capsule, which already runs at 170+ locations.
- **Hardware:** Galbot G1 + a 2-3 level shelf + a hand-over counter. Optional: XREAL glasses for a staff "what the robot sees / next action" view.
- **Architecture / stack:**
  - Perception: G1 head and wrist cameras; item localisation by shelf slot + fiducial markers first, open-vocabulary grasp (GraspVLA on an external GPU, ~9 GB) as upgrade.
  - Planning: speech-to-text → LLM with a small tool set (`answer`, `fetch(item)`, `guide_to(place)`) → task state machine.
  - Control: SDK point-to-point navigation between "counter" and "shelf" waypoints; SDK whole-body motion planning for pick and hand-over; wrist F/T to detect the guest taking the item.
  - Compute: SDK client on the robot or a laptop on the same network; LLM and grasp model off-board.
- **48-hour plan:**
  - H0–6: SDK hello-world, map the area, save waypoints, drive between them, open / close gripper.
  - H6–24: scripted pick of 3 items from fixed slots; hand-over with force trigger; voice loop with canned intents.
  - H24–40: LLM tool calling, multilingual replies (DE / FR / EN), inventory count, optional GraspVLA for unknown items.
  - H40–48: 20 full dry runs, record backup video, freeze code.
- **3-minute demo script:** (0:00) guest asks in German for a bottle of water and where the thermal bath entrance is → (0:30) robot answers, drives to shelf, picks → (1:30) hands over, releases on pull → (2:00) judge asks for an item that is out of stock → robot offers an alternative → (2:30) show dashboard: orders served, stock left.
- **Risks and fallbacks:** grasp fails → fixed slots + trays with handles; speech fails in a noisy hall → tablet buttons; navigation drifts → shorten the route to 2 m.
- **Judging angles:** impact (24/7 service in a staff-short resort) · technical depth (language → mobile manipulation, force-aware hand-over) · Leukerbad relevance (multilingual spa and hotel guests) · innovation is moderate, since it is close to Galbot's existing product.

### Concept 2 — Click-and-collect micro-hub (order picking into lockers)

- **Problem → value:** village pharmacy and mini-market close early; guests and residents order by phone and collect later. Robot picks orders after hours into numbered totes or lockers. Maps onto Galbot's instant-retail warehouse work (100+ sites).
- **Hardware:** G1 + shelf with 8-12 SKUs + 3 totes or locker bays. Optional: D-Robotics RDK X5 camera box at the lockers to verify contents; SKYLANDX MetaCam to scan the stockroom once.
- **Architecture / stack:**
  - Perception: SKU lookup table (slot → item), barcode / label check with the wrist camera, tote verification from a fixed camera.
  - Planning: web order form → order queue → batch planner (which arm, which order of picks).
  - Control: SDK navigation between shelf and lockers; SDK arm planning; suction or gripper depending on package.
  - Compute: order server and vision on a laptop; robot runs SDK control.
- **48-hour plan:**
  - H0–6: SDK bring-up, map, waypoints, single pick-and-place.
  - H6–24: order web page + queue; pick 2-item order into a tote; verification camera.
  - H24–40: dual-arm use (hold tote with one arm, pick with the other), error recovery (re-grasp, skip and flag), restock mode.
  - H40–48: timing runs, metrics screen (picks per hour, error rate), backup video.
- **3-minute demo script:** (0:00) judge places an order on a phone → (0:20) robot picks two items into tote 3 → (1:40) locker camera confirms, phone shows pickup code → (2:10) inject an error (item missing) → robot flags it and substitutes → (2:40) throughput numbers.
- **Risks and fallbacks:** small or shiny packages → choose boxy items, use suction; dual-arm coordination too slow → single arm + fixed tote stand.
- **Judging angles:** real-world impact and a measurable KPI · credible because Galbot already runs this commercially · Leukerbad relevance (after-hours pharmacy for elderly guests) · innovation lower unless verification and recovery are shown well.

### Concept 3 — Facility upkeep patrol (inspect, tidy, report)

- **Problem → value:** lobbies, changing areas and corridors need constant small upkeep: misplaced towels, bottles left behind, blocked exits, missing supplies. A patrol robot that **fixes what it can and reports the rest** covers the "maintain" part of T01. Galbot's own inspection kit is only planned, so this is new work.
- **Hardware:** G1 + collection bin on site. Optional: SKYLANDX MetaCam for a reference 3D scan to compare against; XREAL for the facility manager's task list.
- **Architecture / stack:**
  - Perception: patrol waypoints; at each stop a vision-language model compares the camera view with a "should look like this" reference and lists anomalies.
  - Planning: classify each anomaly as *pick up* (light object, reachable), *restock* or *report only*; write a ticket with photo and map position.
  - Control: SDK navigation for the route; open-vocabulary grasp (GraspVLA if integrated) or scripted pick for known object types; drop in bin.
  - Compute: VLM off-board; Orin handles SDK and streaming.
- **48-hour plan:**
  - H0–6: SDK bring-up, map, 4-stop patrol loop.
  - H6–24: anomaly detection per stop, ticket dashboard with photos.
  - H24–40: pick-up of two object classes (bottle, towel) from table height; report-only for everything else.
  - H40–48: run the loop repeatedly with planted objects; backup video.
- **3-minute demo script:** (0:00) show clean reference → (0:20) judge leaves a bottle and blocks a doorway with a chair → (0:40) robot patrols, picks up the bottle, bins it → (1:50) flags the chair as "cannot fix", ticket appears with photo → (2:30) dashboard: 2 found, 1 fixed, 1 escalated.
- **Risks and fallbacks:** floor-level and soft objects are hard → keep objects on tables, towels on hooks; VLM false alarms → restrict to a short anomaly list; no grasp model on G1 → report-only patrol plus one scripted pick.
- **Judging angles:** innovation (acts, not only inspects) · technical depth (VLM anomaly reasoning + manipulation) · impact (housekeeping load in spas and clinics) · Leukerbad relevance (thermal baths, rehab clinics).

### Concept 4 — Indoor-to-outdoor relay (G1 loads, quadruped delivers)

- **Problem → value:** last-mile in an alpine village means snow, slopes and stairs, where wheeled robots stop. Split the job: **G1 picks and loads indoors, a quadruped carries outdoors.** Shows a whole delivery chain, with Galbot doing the part it is proven at.
- **Hardware:** G1 + Unitree Go2 / B2 or Genisom M1 / L1 with a top-mounted open box. Optional: SKYLANDX scan for a shared map; D-Robotics board on the quadruped for docking markers.
- **Architecture / stack:**
  - Perception: G1 locates the quadruped's box by fiducial marker at a fixed docking spot; quadruped uses its own vendor navigation outdoors.
  - Planning: a small dispatcher (order → G1 pick → quadruped at dock → load → depart → delivered) over a shared message bus (plain HTTP or MQTT is enough).
  - Control: GalbotSDK navigation and arm planning on G1; the quadruped's own SDK for locomotion. No shared autonomy stack needed.
  - Compute: dispatcher on a laptop; each robot keeps its own stack.
- **48-hour plan:**
  - H0–6: both robots under SDK control separately; agree on the dock spot and message format.
  - H6–24: G1 pick + place into a static box; quadruped drives dock → door → drop point.
  - H24–40: join them: marker-based alignment, load confirmation by camera, dispatcher, phone order.
  - H40–48: end-to-end runs, outdoor leg filmed in real snow as backup, indoor-only live version ready.
- **3-minute demo script:** (0:00) order from a "chalet" on a phone → (0:20) G1 picks a pharmacy bag → (1:10) places it in the quadruped's box, confirms → (1:30) quadruped leaves, video cut or live feed of it crossing snow / stairs → (2:30) recipient takes the bag, order closes on screen.
- **Risks and fallbacks:** two SDKs and two teams of vendor engineers → fix interfaces on day 1; docking misalignment → mechanical funnel on the box; outdoor leg fails live → pre-recorded outdoor clip plus live indoor hand-off.
- **Judging angles:** innovation (heterogeneous relay) · technical depth (multi-robot orchestration) · impact (true last-mile) · strongest Leukerbad fit of the four, and the highest delivery risk.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| G1 + Unitree Go2 / B2 or Genisom quadruped | Indoor pick and load, outdoor carry over snow and stairs (Concept 4) | **High** — two SDKs, docking, dispatcher |
| G1 + SKYLANDX MetaCam | Fast 3D scan of the venue for a digital twin or anomaly baseline | **Low-medium** — offline scan; using it for G1 localisation is not documented ⚠️ |
| G1 + XREAL glasses | Staff AR view of robot task queue, tickets, teleop assist | **Medium** — separate app, talks to your own backend |
| G1 + D-Robotics RDK X5 | Cheap smart camera at locker, shelf or door for verification | **Low** — standalone vision node over network |
| G1 + WUJI Hand | Dexterous handling (keys, cards, door handles) | **High** — mechanical and SDK integration on G1 not documented ⚠️ |
| G1 + Binabik AI | Agent layer orchestrating several robots | **Unknown** — depends on Binabik's G1 support; ask both |
| G1 + ET1 (if both on site) | ET1 greets at the door, G1 fetches | **Medium** — ET1 developer access unclear ⚠️ |

## Questions to ask the Galbot engineers on site

1. Which robots are here (G1, G1 Lite, ET1?), how many, and which end effectors (gripper, suction, dexterous hand)?
2. Which robot environment version is installed — does it match **SDK V1.10.0 / GBS 1.18** — and is low-level control unlocked for hackathon teams?
3. Is a grasping model (GraspVLA or the retail picking stack) preloaded and callable, or do we bring our own perception?
4. How do we build and save a map and named waypoints, and how long does mapping a 50 m² area take?
5. Is the welcome / guide kit (knowledge base, persona, speech) available to us, and which languages do speech recognition and synthesis support (German, French)?
6. Can the SDK run from our laptop over the network, and is there any ROS 2 bridge for topics and TF?
7. What are the safety limits and procedures: speed cap near people, e-stop, who must supervise, allowed floor surfaces and slopes?
8. Do we get Pro-tier features (cloud simulation, one-click deployment) during the event, and are SimReady shelf scenes available?

## Decision rule

- **Pick Galbot for T01 if** your idea is an indoor service point where a robot must **pick real items from shelves and hand them to people** (kiosk, pharmacy, click-and-collect, upkeep), and the booth confirms a G1 with working navigation and a callable grasp stack.
- **Avoid if** your idea needs outdoor driving, snow, stairs, loads above 10 kg, or a ready-made open navigation model — or if no G1 is on site.

## Sources
- [Galbot company profile (this repo)](../Galbot.md)
- [Galbot G1 product page](http://www.galbot.com/g1/)
- [Galbot developer portal](https://developer.galbot.com/?lang=en)
- [GalbotSDK repository](https://github.com/GalaxyGeneralRobotics/GalbotSDK)
- [GitHub org GalaxyGeneralRobotics](https://github.com/GalaxyGeneralRobotics)
- [GraspVLA repository (PKU-EPIC)](https://github.com/PKU-EPIC/GraspVLA)
- [UrbanVLA repository](https://github.com/GalaxyGeneralRobotics/UrbanVLA)
- [NavFoM project page](https://pku-epic.github.io/NavFoM-Web)
- [Guiyang government: robotic tourism-retail capsules](https://fgw.english.guiyang.gov.cn/2026-01/26/c_1157846.htm)
- [eWeek, 2026-06-17: humanoid robot to run a 24-hour store in Hong Kong](https://www.eweek.com/news/hong-kong-humanoid-robot-store-apac-china/)
