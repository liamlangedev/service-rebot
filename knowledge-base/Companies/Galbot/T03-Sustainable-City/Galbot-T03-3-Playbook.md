---
type: challenge-playbook
company: "Galbot"
slug: Galbot
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Galbot × T03 — Hackathon Playbook

⬆ [Galbot profile](../Galbot.md) · [Brief](Galbot-T03-1-Brief.md) · [Products and solutions](Galbot-T03-2-Products-and-Solutions.md)

**Assumptions to confirm at the booth before committing:** the robot on site is a **Galbot G1** with grippers; GalbotSDK is usable at least at high level; you may attach a laptop with a GPU. Everything below is indoor, flat-floor work. Galbot has no sustainability reference of its own, so the sustainability logic and metrics are yours to build.

## Solution approaches

### Concept 1 — Recyclables sorting station (safest)

- **Problem → value:** Hotels, spas and clinics produce mixed recyclables (PET, glass, aluminium, cartons) that staff sort by hand or not at all. A robot station sorts them and reports weight and count per stream, so the building sees its diversion rate.
- **Hardware:** Galbot G1 parked at a table, 4–5 labelled bins within reach (floor level is reachable). Optional: D-Robotics RDK X5 with a fixed camera over the table as a low-power classifier; kitchen scale under each bin for kg per stream.
- **Architecture / stack:**
  - Perception: overhead or head camera → open-vocabulary detector or a vision-language model on a laptop classifies each item by material.
  - Planning: simple state machine (detect → choose bin → pick → place → log). Grasp pose from the G1's built-in grasp skill if exposed through the SDK; otherwise top-down grasps from wrist depth, or GraspVLA served from a laptop (about 9 GB VRAM, about 200 ms per step).
  - Control: GalbotSDK high-level arm motion; base stays still.
  - Compute: classifier on laptop or RDK X5; dashboard on the laptop.
- **48-hour plan:**
  - H0–6: SDK hello-world (move arm, open gripper, read cameras). Fix table, bins, lighting. Choose 15–20 test items.
  - H6–24: detection + material label working on live camera; first scripted pick and place into one bin.
  - H24–40: all bins; error recovery (regrasp, "unknown" bin); dashboard with counts, kg and an estimated CO2 figure with stated assumptions.
  - H40–48: 20 clean runs, film a backup video, rehearse.
- **3-minute demo script:** tip a bag of mixed items on the table → robot sorts 6–8 items into the right bins while the screen shows label and confidence → judge hands over an unseen item → robot handles it or puts it in "unknown" → show the dashboard total.
- **Risks and fallbacks:** grasp skill not exposed → fixed top-down grasps on rigid items only. Transparent PET and crushed cans are hard for depth cameras → use the RGB label and pre-set grasp heights. Dirty or wet waste → out of scope, say so.
- **Judging angles:** innovation low to medium (known use case); technical depth medium; impact easy to quantify; Leukerbad relevance good for hotels and thermal baths with many guests.

### Concept 2 — Near-expiry shelf audit and rescue

- **Problem → value:** Food and medicines are thrown away because nobody notices they are about to expire. The robot audits shelves, pulls near-expiry items and moves them to a "use first / donate" shelf. Waste avoided is the metric.
- **Hardware:** Galbot G1 (mobile), a mock shop or clinic store shelf with 20–30 packaged items, a rescue shelf or tote.
- **Architecture / stack:**
  - Perception: wrist or head camera close-ups → OCR or vision-language model reads expiry dates and product names; shelf slots tracked in a small database.
  - Planning: first-expired-first-out rules decide leave / move forward / rescue. Navigation between shelf and rescue point through the SDK's navigation functions on a pre-built map.
  - Control: SDK high-level pick and place; uses the same skills as Galbot's retail inventory-check and restocking work.
  - Compute: OCR / VLM on laptop; rules and database on laptop.
- **48-hour plan:**
  - H0–6: map the area, test navigation to two waypoints, test picking boxes from a shelf.
  - H6–24: expiry-date reading pipeline on photos, then live; shelf database.
  - H24–40: full loop audit → pick → carry → place; report page (items saved, value, kg).
  - H40–48: reliability runs, backup video.
- **3-minute demo script:** show shelf with mixed dates → robot scans a row, screen lists dates → robot removes two near-expiry items and places them on the rescue shelf → report shows what was saved and what expires next week.
- **Risks and fallbacks:** small or curved date print is unreadable → add QR labels encoding the date and present OCR as the stretch goal. Tight shelf picking fails → use open-front trays with spacing. Navigation unavailable → place both shelves within arm reach.
- **Judging angles:** innovation medium; technical depth medium to high (perception + mobile manipulation); impact credible for retail, pharmacies and clinic stores; Leukerbad relevance: rehabilitation clinics and small alpine shops with seasonal demand swings.

### Concept 3 — Night energy patrol that acts

- **Problem → value:** Heated buildings waste energy through lights left on, open windows and doors, and unread meters. Most inspection robots only report. A G1 can also act: press a switch, close a door, read a meter.
- **Hardware:** Galbot G1; optional USB thermal camera or temperature / CO2 sensor on the robot; optional SKYLANDX MetaCam scan for a 3D map of the venue.
- **Architecture / stack:**
  - Perception: LiDAR navigation on a mapped route; cameras + vision-language model answer checklist questions per waypoint (light on? window open? meter value?).
  - Planning: waypoint list with a checklist; act if safe, otherwise report.
  - Control: SDK navigation between waypoints; arm motions for switch and door, using wrist force sensors to limit contact force.
  - Compute: VLM on laptop or cloud; route logic on laptop.
- **48-hour plan:**
  - H0–6: confirm navigation and mapping work on site; pick 4–5 waypoints in the venue.
  - H6–24: checklist perception per waypoint; meter reading.
  - H24–40: one or two physical actions (rocker switch, push a door closed); report with estimated kWh saved and assumptions.
  - H40–48: full patrol runs, backup video.
- **3-minute demo script:** robot drives to waypoint 1, reads a meter → waypoint 2, sees a light on in an empty room and switches it off → waypoint 3, flags an open window on the report → show the patrol log.
- **Risks and fallbacks:** Galbot's own "site inspection" kit is only planned, so everything is custom. Switch pressing is fiddly → 3D-print a large paddle over the switch, or fall back to report-only plus a smart plug. Window closing is too risky → report only.
- **Judging angles:** innovation medium to high (inspect and act); technical depth high; impact depends on honest kWh estimates; Leukerbad relevance strong (thermal baths, hotels and clinics with high heating loads in winter).

### Concept 4 — Outdoor-to-indoor circular loop (most ambitious, multi-vendor)

- **Problem → value:** Collection and sorting are separate, manual steps. A quadruped collects recyclables or returned items along a route and brings them to an indoor G1 station that sorts, logs and prepares reuse.
- **Hardware:** Galbot G1 (indoor station) + a quadruped from Unitree, Genisom or Magiclab with a basket (outdoor / corridor leg) + optional D-Robotics RDK X5 smart-bin camera + optional XREAL glasses as operator view.
- **Architecture / stack:**
  - Perception: quadruped uses its own navigation; G1 station as in Concept 1.
  - Planning: a small dispatcher (laptop) assigns pick-up points and tells the G1 when a delivery has arrived.
  - Control: each robot through its own vendor SDK; hand-over through a passive tray or basket, no robot-to-robot grasping.
  - Compute: dispatcher and dashboard on one laptop on the same network.
- **48-hour plan:**
  - H0–6: secure both robots; prove each alone (G1 pick and place, quadruped waypoint run).
  - H6–24: Concept 1 station working; quadruped route with basket.
  - H24–40: hand-over at a docking tray; dispatcher messages; shared dashboard.
  - H40–48: end-to-end runs; decide early whether to demo linked or as two segments.
- **3-minute demo script:** person drops bottles in the quadruped's basket → quadruped walks to the station → G1 unloads and sorts → dashboard shows the route, items and totals.
- **Risks and fallbacks:** two SDKs and two vendor teams in 48 h is the main risk → fall back to Concept 1 with a human carrying the basket. Hand-over alignment → fixed docking marks on the floor.
- **Judging angles:** innovation high; technical depth high; impact is a full city loop; Leukerbad relevance strong because the quadruped covers the terrain the G1 cannot.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| G1 + D-Robotics RDK X5 | Low-power always-on classifier over the bin or table; robot wakes only when needed | Low (camera + network message) |
| G1 + Unitree Go2 / Genisom / Magiclab quadruped | Outdoor or multi-floor collection feeding the indoor sorting station | High (two SDKs, hand-over) |
| G1 + SKYLANDX MetaCam | Fast 3D scan of the venue for the energy patrol route and a digital twin of the building | Medium (map format conversion ⚠️ unverified) |
| G1 + Flexiv Rizon | G1 fetches and presents parts, force-controlled arm does unscrewing or disassembly for repair and reuse | Medium to high |
| G1 + WUJI Hand | Dexterous handling of small e-waste parts; G1 accepts swappable end effectors, but mounting and drivers for a third-party hand are ⚠️ unverified | High |
| G1 + XREAL glasses | Operator sees labels, confidence and can correct the robot's sorting decision | Low to medium |

## Questions to ask the Galbot engineers on site

1. Which robots are here (G1, G1 Lite, ET1), how many, and can a team reserve one for 48 hours?
2. Which SDK and robot environment version is installed (SDK V1.10.0 expects V1.18), and is low-level control unlocked?
3. Is a ready grasp skill (GraspVLA or the retail picking stack) callable through the SDK with a text or box prompt? What input does it need?
4. Is the "material sorting" kit available in any preview form for the hackathon?
5. Is on-site mapping and navigation available to us, and how long does mapping a new room take?
6. Which end effectors are here (gripper, suction cup, dexterous hand), and can we swap them ourselves?
7. May we attach an external GPU laptop and USB sensors, and what network setup do you recommend?
8. What are the safe force and speed limits near people, and who resets the robot after an emergency stop?

## Decision rule

- **Pick Galbot for T03 if** your idea is an indoor pick-and-sort or shelf task with rigid items under 5 kg, a G1 is confirmed available, and the Galbot team confirms a callable grasp skill or you are ready to script grasps.
- **Avoid if** your idea is outdoors, needs environmental sensing, EV charging or heavy lifting as its core, or depends on a domain reference from the vendor.

## Sources
- [Galbot G1 product page](http://www.galbot.com/g1/)
- [Galbot developer portal (kits and tiers)](https://developer.galbot.com/?lang=en)
- [GalbotSDK README](https://raw.githubusercontent.com/GalaxyGeneralRobotics/GalbotSDK/HEAD/README.md)
- [GraspVLA repository (PKU-EPIC)](https://github.com/PKU-EPIC/GraspVLA)
- [CnEVPost, 2026-06-24: CATL teams with Galbot](https://cnevpost.com/2026/06/24/catl-galbot-scale-humanoid-robots-battery-factories/)
- [Galbot company profile in this repo](../Galbot.md)
