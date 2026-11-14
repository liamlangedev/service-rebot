---
type: challenge-playbook
company: "UniX AI"
slug: UniX-AI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# UniX AI × T01 — Hackathon Playbook

⬆ [UniX AI profile](../UniX-AI.md) · [Brief](UniX-AI-T01-1-Brief.md) · [Products and solutions](UniX-AI-T01-2-Products-and-Solutions.md)

> **Before you commit (first 30 minutes):** UniX AI publishes **no SDK, ROS 2 packages or docs**. Every concept below assumes the on-site engineers give you at least a thin hook: *trigger a named skill*, *send the base to a waypoint*, *read status*. Concepts are ordered by how little access they need. Which robot is on site (Wanda 2.0 most likely, Panther possible) is ⚠️ unverified.

| Access level you get | What is realistic |
|---|---|
| A — Skills only, triggered by vendor staff or a tablet | Concept 1 with a human pressing "go" (weak) |
| B — Scriptable skill trigger + waypoint navigation + status | Concepts 1, 2, 3 |
| C — B plus camera / LiDAR streams or demonstration recording | Concepts 3 and 4 at full depth |

## Solution approaches

### Concept 1 — Spa-resort concierge and guide

- **Problem → value:** Leukerbad hotels, baths and clinics serve many older, multilingual guests with thin staffing in the off-hours. A robot that answers questions and walks guests to the right place frees reception staff.
- **Hardware:** Wanda 2.0 (or Panther). Optional: XREAL glasses as a staff supervision view.
- **Architecture / stack:**
  - Perception: your own speech-to-text on a laptop (robot's 6-mic array if audio is exposed, otherwise an external microphone or a phone / QR web page).
  - Planning: LLM router on the laptop with a small venue knowledge base (opening hours, rooms, pool rules) → outputs one of a fixed set of intents: `answer`, `guide_to(place)`, `fetch(item)`.
  - Control: robot's own navigation and pre-loaded reception / guiding skills, called through whatever hook UniX exposes.
  - Compute: laptop (cloud LLM if venue Wi-Fi holds; keep a small local model as backup).
- **48-hour plan:**
  - H0–6: confirm access level; map the demo area with the vendor; define 5–8 named waypoints; write the intent schema.
  - H6–24: speech in / out in DE, FR, EN; LLM router with venue facts; first end-to-end "guide me to X".
  - H24–40: add one manipulation hand-over (e.g. hand a towel or brochure); error handling ("I did not understand", blocked path); 20 full dry runs.
  - H40–48: freeze code, rehearse, record a backup video.
- **3-minute demo script:** (0:00) guest asks in German where the thermal pool is → (0:30) robot answers and leads the way → (1:30) second guest asks in English for a towel → robot fetches and hands it over → (2:30) show the staff dashboard with the request log and one slide on staffing impact.
- **Risks and fallbacks:** no skill API → run navigation from the vendor tablet and keep your voice + LLM layer as the visible contribution. Noisy hall → use the QR / phone interface. Wi-Fi down → local model and canned answers.
- **Judging angles:** innovation — modest; technical depth — language grounding to robot skills; impact — clear staffing case; Leukerbad relevance — **high** (multilingual spa tourism, elderly guests).

### Concept 2 — On-demand amenity and parcel runner

- **Problem → value:** Small deliveries inside a hotel or clinic (water, towels, medication bags, parcels from reception) eat staff time. A dual-arm robot can pick the item itself instead of waiting to be loaded like a tray robot.
- **Hardware:** Wanda 2.0 or Panther with UniPicker Pro. Optional: D-Robotics RDK X5 with a camera as a fixed "stock shelf" station that confirms the right item was taken.
- **Architecture / stack:**
  - Perception: on-robot perception for grasping; optional shelf camera (your code) for item verification.
  - Planning: web order page (QR code per room or table) → order queue → your dispatcher picks the next job and the route (stock point → destination waypoint).
  - Control: robot skills `pick(item)`, `go_to(waypoint)`, `hand_over / place`.
  - Compute: laptop runs the order page, queue and dashboard.
- **48-hour plan:**
  - H0–6: confirm which items the robot already grasps reliably; pick 3 SKUs; set up shelf and two delivery points.
  - H6–24: order page + queue + dispatcher; first full delivery of one item.
  - H24–40: multi-order queue, status feedback to the guest's phone, failure recovery (grasp retry, "item out of stock"); measure time per delivery.
  - H40–48: rehearse; prepare a metric slide (deliveries per hour, success rate over N runs).
- **3-minute demo script:** (0:00) judge scans QR and orders a water bottle → (0:20) robot picks from shelf → (1:20) drives to the judge's table, hands over → (2:00) second order already queued, dashboard shows the queue and measured success rate → (2:40) one slide: where this runs in Leukerbad.
- **Risks and fallbacks:** elevator riding is claimed on the application page but needs building integration — **stay on one floor**. Grasp failures → restrict to SKUs the pre-loaded skills handle. No pick skill for your items → ask whether a new skill can be taught by demonstration; otherwise staff-loaded hand-over.
- **Judging angles:** innovation — pick-and-deliver in one robot; technical depth — dispatcher + verification loop; impact — measurable; Leukerbad relevance — hotels and rehabilitation clinics.

### Concept 3 — Facility upkeep round with a digital logbook

- **Problem → value:** Public interiors (bath changing areas, lobbies, restrooms, corridors) need constant small upkeep: wipe surfaces, restock amenities, collect and sort litter, check that equipment is in place. Today it is a paper checklist.
- **Hardware:** Panther preferred (reaches the floor, omnidirectional); Wanda 2.0 works for table-height tasks. Optional: SKYLANDX MetaCam to scan the venue once and show the round on a 3D model.
- **Architecture / stack:**
  - Perception: robot head cameras if streams are exposed (access level C), otherwise an external camera; a vision-language model on the laptop classifies each checkpoint ("dispenser empty", "litter on floor", "fire-equipment cabinet complete").
  - Planning: round = ordered list of checkpoints; per checkpoint the VLM result selects a skill (wipe, restock, pick up and sort) or files a ticket for humans.
  - Control: pre-loaded skills shown publicly — wiping, amenity restocking, waste sorting; the official security page also describes fire-equipment cabinet checks.
  - Compute: laptop; logbook as a simple web dashboard with photos and timestamps.
- **48-hour plan:**
  - H0–6: confirm camera access and which upkeep skills are loaded; build a 4-checkpoint mock-up (table, amenity shelf, bin area, equipment cabinet).
  - H6–24: checkpoint classifier with 20–30 photos per state; logbook; first automatic "see problem → run skill".
  - H24–40: full round without intervention; add ticket hand-off for problems the robot cannot fix; optional 3D map overlay.
  - H40–48: rehearse with staged faults; backup video.
- **3-minute demo script:** (0:00) show a messy mock-up and the empty logbook → (0:20) robot starts its round, wipes the table → (1:10) finds litter, sorts it into the right bin → (1:50) sees the empty amenity shelf, restocks → (2:20) flags a missing item it cannot fix; ticket appears → (2:40) logbook view and impact slide.
- **Risks and fallbacks:** no camera stream → mount your own camera on the robot or at each checkpoint. A skill is missing → swap that checkpoint to "detect and report". Long skill durations → pre-cut the demo to three checkpoints.
- **Judging angles:** innovation — closed loop from inspection to action; technical depth — VLM-to-skill grounding and audit trail; impact — maintenance labour and hygiene evidence; Leukerbad relevance — thermal baths and clinics with strict hygiene routines.

### Concept 4 — Street-to-room relay (multi-vendor)

- **Problem → value:** Leukerbad is steep and snowy; a wheeled indoor humanoid cannot leave the building, and an outdoor robot cannot open a cupboard or hand over an item. Chain them: an outdoor robot covers the street leg, the UniX robot does the indoor last 50 metres.
- **Hardware:** Wanda 2.0 or Panther (indoor leg) + a quadruped from another vendor on site, e.g. Unitree Go2 / B2 with a carry box (outdoor leg). Optional: SKYLANDX MetaCam for a shared map, D-Robotics board as the hand-over station sensor.
- **Architecture / stack:**
  - Perception: each robot uses its own navigation; a fixed hand-over station at the entrance (marker + camera) detects arrival.
  - Planning: your orchestrator on a laptop holds the job state machine: `outdoor_transit → arrived_at_station → indoor_pick → indoor_deliver → confirmed`.
  - Control: quadruped via its public SDK; UniX robot via the exposed skill hook (`pick from box`, `go_to`, `hand_over`).
  - Compute: laptop; simple message bus (MQTT or plain HTTP) between the two robot adapters.
- **48-hour plan:**
  - H0–6: secure both robots and both vendor contacts; agree the hand-over geometry (box height within Wanda's reach); freeze the state machine.
  - H6–24: each leg works alone; station detection works.
  - H24–40: full relay; timeouts and recovery (parcel not found, robot late); tracking page for the recipient.
  - H40–48: rehearse 10 full relays; backup video of the outdoor leg in real snow or on a real slope.
- **3-minute demo script:** (0:00) order placed, tracking page opens → (0:20) quadruped arrives at the "entrance" with the parcel (outdoor clip shown in parallel) → (1:00) UniX robot picks the parcel from the box → (1:50) delivers to the "room door" and hands over → (2:30) tracking page shows confirmed; slide on the Leukerbad route.
- **Risks and fallbacks:** two vendors = two access negotiations; if the UniX hook is missing, the idea still works with a human-triggered indoor skill but loses its autonomy claim. Hand-over grasp is the weak point — use a rigid box with a fixed, easy-to-grasp parcel. If time runs out, demo the indoor leg live and the outdoor leg on video.
- **Judging angles:** innovation — **highest** (heterogeneous fleet, terrain-matched robots); technical depth — orchestration and hand-over; impact — realistic last-mile model for steep alpine resort towns; Leukerbad relevance — **high**.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| UniX robot + Unitree Go2 / B2 | Outdoor leg on slopes and snow, indoor manipulation and hand-over (Concept 4) | High — two robots, orchestrator, hand-over station |
| UniX robot + SKYLANDX MetaCam | Fast 3D scan of the venue for a digital twin, route display or checkpoint planning | Low–medium — offline use is easy; feeding the map into the robot depends on map-format access (not public) |
| UniX robot + D-Robotics RDK X5 | External perception node (shelf check, hand-over station, checkpoint camera) without touching robot internals | Low — independent device, talks to your laptop |
| UniX robot + XREAL glasses | Staff see robot tasks, queue and alerts in AR; possible teleoperation view if UniX exposes its remote-control channel | Medium — AR app is your own work; teleop link not public |
| UniX robot + Binabik AI | Agentic task layer above the robot's skills | Unknown — depends on both sides' interfaces; ask both teams |
| Panther + WUJI Hand | Dexterous manipulation (Panther page says dexterous-hand compatible) | High — mechanical and control interface not public; not a 48-hour job without vendor help |

## Questions to ask the UniX AI engineers on site

1. Which robots are here (Wanda 2.0, Panther), how many, and how many team-hours can each team book?
2. What can we call from our own code: named skills, waypoint navigation, status / result feedback? Over what interface (ROS 2, Python, HTTP, tablet only)?
3. Which pre-loaded skills are installed on these units — guiding, delivery, pick-and-place, wiping, restocking, waste sorting — and on which objects are they reliable?
4. Can we read camera, LiDAR and microphone streams, and can we play audio through the robot?
5. Can we teach a new skill by demonstration (UniFlex) during the event? How many demos and how long does training take?
6. How is the map built and can we define our own waypoints? Is the area limited to one floor?
7. What are the limits for slope, door thresholds and wet floors, and what safety rules apply when the public is nearby (speed cap, e-stop, supervisor)?
8. Is teleoperation available as a fallback, and which languages does the built-in voice interaction support?

## Decision rule

- **Pick UniX AI for T01 if** your idea is an **indoor** service task (concierge, guiding, in-building delivery, upkeep) and the on-site team confirms at least a scriptable skill + waypoint hook — then your value is the application layer, and the robot's proven hotel / reception skills do the hard manipulation.
- **Avoid if** you need outdoor mobility, stairs or snow, low-level control, simulation or open models — or if access turns out to be "vendor presses the button"; then use UniX only as the indoor partner in a multi-vendor relay.

## Sources
- [UniX AI official site](https://www.unix-group.ai)
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [Panther product page](https://www.unix-group.ai/Panther)
- [Reception & Guiding application page](https://www.unix-group.ai/Reception-Guiding)
- [Household & Hotel application page](https://www.unix-group.ai/Household-Hotel)
- [Security Service application page](https://www.unix-group.ai/Security)
- [Retail application page](https://www.unix-group.ai/lspicture/1852/detail/51)
- [Press release, 2 Jan 2026: Wanda 2.0 at CES 2026 (via Webull / PR Newswire)](https://www.webull.com/news/14134140025406464)
- [Press release, 8 Apr 2026: Panther launch (TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [WRC 2026 live report, 20 Aug 2026 (iTiger)](https://www.itiger.com/news/1101359561)
- [UniX AI company profile (this repo)](../UniX-AI.md)
