---
type: challenge-playbook
company: "SKYLANDX"
slug: SKYLANDX
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# SKYLANDX × T01 — Hackathon Playbook

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Brief](SKYLANDX-T01-1-Brief.md) · [Products and solutions](SKYLANDX-T01-2-Products-and-Solutions.md)

**Ground rules for every concept below**

- SKYLANDX supplies the **map and the pose**; a second vendor supplies the robot. Secure that robot first.
- On-site SKYLANDX hardware and API access are **not confirmed**. Concept 1 needs only a scanner and file export; each later concept adds one more dependency on the booth engineers.
- Do the scan in **hour 1** — it is the one asset every concept needs and it takes minutes.

## Solution approaches

### Concept 1 — Scan-once delivery map (safest)

- **Problem → value:** Service robots lose their first day to mapping each new building. One 10-minute walk with a handheld scanner gives a hotel, clinic or spa a delivery-ready map; the robot runs room-service / linen / medication-cart routes the same afternoon.
- **Hardware:** MetaCam Air 2 (handheld; MetaCam Lite also works indoors) + MetaCam Go + MetaCam Studio (Windows laptop). Carrier: any on-site robot with its own 2D navigation — Unitree Go2 / B2, or a wheeled base from AGIBOT, Galaxea, Galbot, Spirit AI or UniX AI.
- **Architecture / stack:**
  - Perception: offline. Scan → Studio (clean, remove people) → export **PCD / PLY**.
  - Map conversion (your code, laptop): Open3D — crop to a height band above the floor, project to a 2D occupancy grid (PGM + YAML), mark stairs / no-go zones by hand.
  - Planning + control: the carrier robot's own stack (Nav2 or vendor navigation) localizes with **its own** LiDAR against the SKYLANDX-derived map. No SKYLANDX API needed at run time.
  - Mission layer: small web app — pick destination, robot drives, notifies on arrival.
- **48-hour plan:**
  - H0–6: borrow scanner, scan the route (two passes), export; confirm the carrier robot accepts an external map.
  - H6–24: conversion script; first localized drive on the imported map; waypoints for 3 destinations.
  - H24–40: mission web app, arrival confirmation, re-scan of a second area to prove "new site in 15 minutes".
  - H40–48: timing measurements (scan-to-first-delivery), rehearsal, backup video.
- **3-minute demo script:** (0:00) Hand a judge the scanner, walk 20 m of corridor live, show the point cloud growing on the phone. (0:45) Show the pre-made map from the same pipeline. (1:15) Tap "Deliver to room 3" — robot drives with a payload. (2:30) Slide: scan-to-delivery time vs. conventional robot-driven mapping.
- **Risks and fallbacks:** Carrier robot rejects external maps → use the map only as the operator's planning view and let the robot build its own SLAM map aligned by 3 landmarks. Scale / frame mismatch → align with two measured reference points. Studio unavailable → ask SKYLANDX staff to export for you.
- **Judging angles:** Innovation — modest (clean workflow, not new science). Technical depth — map conversion + cross-vendor localization. Impact — cuts commissioning cost for small operators. Leukerbad — many small hotels and clinics that cannot afford robot integrators.

### Concept 2 — GNSS-free courier with a live localization payload

- **Problem → value:** A resort delivery route crosses outdoor lanes (GNSS, sometimes poor between buildings and rock faces) and indoor / covered sections (no GNSS). One sensor that gives continuous pose across both removes the classic hand-over failure.
- **Hardware:** MetaCam Air 2 on **MetaCam Hub** (or an improvised mount) riding a quadruped — Unitree Go2 / B2, AGIBOT D1, Magiclab MagicDog or Genisom M1 / L1. Optional: D-Robotics RDK X5 as on-robot bridge computer.
- **Architecture / stack:**
  - Perception: MetaCam runs SLAM on-device; RTK anchors outdoor segments. Stream pose (+ downsampled cloud) over the **Rosbridge WebSocket** to the bridge computer (roslibpy client, or rosbridge directly into ROS).
  - Planning: Nav2 on the bridge computer — global plan on the Concept 1 map, local costmap from the robot's own sensors or the MetaCam cloud flattened with pointcloud_to_laserscan.
  - Control: velocity commands to the quadruped through that vendor's SDK. Relocalization in the saved map at start-up (SKYLANDX feature — confirm how it is triggered).
- **48-hour plan:**
  - H0–6: get the Rosbridge endpoint, topic list and message types from SKYLANDX; print pose on a laptop. **Go / no-go gate at H6** — if no live pose, drop to Concept 1.
  - H6–24: mount, measure the sensor-to-base transform, pose → `/tf`; teleoperated run logging pose indoors and outdoors.
  - H24–40: close the loop with Nav2; indoor → outdoor → indoor route; relocalization after restart.
  - H40–48: reliability runs, pose-drift plot, demo polish.
- **3-minute demo script:** (0:00) Map view with live robot pose. (0:30) Robot leaves the hall, crosses the doorway to outside, GNSS/RTK status changes on screen while the pose track stays continuous. (1:45) Robot returns through a different door and stops at a drop point within a taped 30 cm box. (2:30) Drift plot + "no beacons, no QR codes, no infrastructure".
- **Risks and fallbacks:** API not handed over → Concept 1. Wi-Fi point-cloud bandwidth → stream pose only, use the robot's own obstacle sensing. Quadruped vibration degrades SLAM → slower gait, damped mount. Snow / wet weather (Air 2 is IP5X) → keep the outdoor leg under cover or short; rain cover that does not block the LiDAR.
- **Judging angles:** Innovation — seamless indoor / outdoor localization as a bolt-on. Technical depth — real-time cross-vendor integration, frame calibration. Impact — delivery without installing infrastructure. Leukerbad — steep lanes, covered passages, winter conditions (−20 °C rated).

### Concept 3 — Public-space upkeep patrol (change detection → work orders)

- **Problem → value:** Municipal crews find blocked paths, overflowing or displaced bins, damaged railings and snow / debris build-up by walking around. A robot repeating a route and comparing today's 3D scan with a reference turns that into an automatic, located task list.
- **Hardware:** MetaCam Air 2 handheld (reference + "today" scans) or robot-mounted as in Concept 2; Skyland Cloud for the 3DGS viewer. Optional: a wheeled manipulator (Galaxea R1, Galbot G1, AGIBOT G1) to act on one finding.
- **Architecture / stack:**
  - Perception: two scans of the same route, both exported as PCD; panoramic JPEGs kept for evidence.
  - Analysis (laptop): Open3D — register scans (RTK / landmarks + ICP), cloud-to-cloud distance, cluster changes above a threshold, classify by size / height (obstacle on path, missing object, volume change). Optional VLM on the panorama crop to label the finding.
  - Output: map-pinned work orders (position, photo, estimated volume) in a simple dashboard; optionally dispatch the robot to the location to verify or clear.
- **48-hour plan:**
  - H0–6: reference scan of a loop (indoor hall + outdoor forecourt); stage 4–5 changes (moved bin, cone on path, box, "snow" pile); second scan.
  - H6–24: registration + diff pipeline; first change list; tune thresholds against false positives (people, parked items).
  - H24–40: dashboard; photo crops; volume estimate; robot-mounted repeat run if Concept 2's link works.
  - H40–48: precision / recall on staged changes, demo flow.
- **3-minute demo script:** (0:00) 3D twin of the route. (0:30) A judge moves an object on the route; quick re-scan of that segment. (1:30) Dashboard flags the change with position, photo and size. (2:15) Work order sent; robot (or person) goes to the pin.
- **Risks and fallbacks:** Processing too slow for a live re-scan → pre-record the "today" scan and re-scan only a 10 m segment live. Too many false positives from people → scan in quiet moments, filter small / transient clusters. No robot mount → handheld walk still demonstrates the full value chain; state clearly which part is automated.
- **Judging angles:** Innovation — maintenance by 3D differencing rather than cameras alone. Technical depth — registration, change clustering, volume estimation. Impact — fewer inspection walks, documented upkeep. Leukerbad — snow clearing, tourist-season wear, small municipal team.

### Concept 4 — Step-free route twin for guide and delivery robots (most ambitious)

- **Problem → value:** In a steep village with many elderly and rehabilitation guests, the shortest path is often not usable by a wheeled robot, a wheelchair or a rollator. A LiDAR twin can be analysed for slope, steps and kerb height to compute a **traversability graph**; the same graph drives a delivery robot, a guide robot and a human wayfinding view.
- **Hardware:** MetaCam Air 2 with RTK for the outdoor scan (MetaCam Pro only if SKYLANDX offers one for longer streets); Skyland Cloud 3DGS; a wheeled robot (delivery) or quadruped (guide); XREAL glasses for the wayfinding overlay; C01 LiDAR + FAST-LIO as on-robot localization if a unit and driver are available.
- **Architecture / stack:**
  - Perception: georeferenced scan → ground segmentation → per-cell slope, step height and clear width (Open3D + numpy).
  - Planning: cost graph with profiles (wheeled robot, quadruped, wheelchair); A* per profile; export waypoints to the robot's Nav stack.
  - Control: carrier robot executes the profile-specific route; localization from Concept 2's live pose or the robot's own stack.
  - Human interface: route drawn in the 3DGS web twin and, stretch goal, as an AR path in XREAL glasses.
- **48-hour plan:**
  - H0–6: scan a route with at least one stair, one ramp and one kerb; export.
  - H6–24: traversability analysis and profile-based routing; validate slopes against a manual measurement.
  - H24–40: robot executes the "wheeled" route and avoids the stairs; twin viewer with routes; AR overlay if time allows.
  - H40–48: comparison of shortest vs. step-free route, demo.
- **3-minute demo script:** (0:00) Twin with two routes: shortest (stairs) vs. step-free. (0:40) Switch profile wheelchair → quadruped: the route changes. (1:15) Wheeled robot delivers along the step-free route past the stairs. (2:15) Visitor view (web or glasses) following the same path. (2:45) Scaling: one scan session per district.
- **Risks and fallbacks:** Outdoor scan blocked by weather (IP5X) or too feature-poor → do it in and around the venue (entrance ramp + steps). Ground segmentation noisy → restrict to hand-drawn corridors and compute slope only there. AR too much → web twin only. Robot integration slips → show planning + a teleoperated run along the computed route, labelled as such.
- **Judging angles:** Innovation — one geometric twin serving robots and people. Technical depth — terrain analysis, multi-profile planning, multi-vendor execution. Impact — accessibility data most towns do not have. Leukerbad — the strongest local story (steep terrain, rehab guests, tourism).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| SKYLANDX Air 2 (handheld) + any robot with 2D navigation | Prior map for delivery (Concept 1) | **Low** — files only |
| SKYLANDX Air 2 + MetaCam Hub + Unitree Go2 / B2 | Live GNSS-free pose on a legged courier (Concept 2) | **Medium–high** — depends on Rosbridge access and mount |
| SKYLANDX C01 + D-Robotics RDK X5 + any base | Self-built LiDAR-inertial localization with open-source LIO | **High** — UDP driver / packet spec needed ⚠️ |
| SKYLANDX scan + Galaxea R1 / Galbot G1 / AGIBOT G1 | Navigate to a mapped spot, then manipulate (bin, parcel hand-over) | **Medium** — map import + the vendor's manipulation stack |
| SKYLANDX 3DGS twin + XREAL glasses | Wayfinding / operator view in the twin | **Medium** — 3DGS PLY viewer on Android XR is your problem ⚠️ |
| SKYLANDX twin + Binabik AI or Genisom SomaMind agent stack | Language-level tasking ("take this to the spa reception") grounded in a real map | **Medium–high** — interfaces of those stacks not verified here ⚠️ |
| SKYLANDX scan + coprod modular hardware | Custom delivery base with a ready map | **High** — two early-stage stacks |

## Questions to ask the SKYLANDX engineers on site

1. Which units can teams borrow, how many, and for how long — Air 2, C01, MetaCam Hub?
2. Can we get the **Rosbridge WebSocket** details today: IP / port, topic names, message types, rates, coordinate frames? ROS 1 or ROS 2 on the other end?
3. How do we trigger **relocalization** in a previously saved map, and can the device output pose in that map's frame live?
4. Is the "navigation command" output available to us, or partner-only? What does it output (velocity, waypoints)?
5. For the C01: is there a ROS driver or a UDP packet specification, and which open-source LIO have you tested it with?
6. MetaCam Hub: mechanical pattern, power input and data connector — will it fit a Unitree Go2 / B2 payload rail?
7. How long do Studio export and Cloud 3DGS take for a 10-minute scan, and do teams get accounts? Is there an offline path if the venue network is slow?
8. Has the Air 2 been used in snow or light rain, and what do you recommend given IP5X?

## Decision rule

- **Pick SKYLANDX for T01 if** your idea lives or dies on navigation in a real building or street (delivery, patrol, guiding), you already have a carrier robot from another vendor, and you can get either file exports (enough for Concept 1) or the live pose stream within the first 6 hours.
- **Avoid if** your concept is manipulation- or interaction-centred, you want one vendor and one SDK, or the booth cannot confirm a loaner unit and API access at kickoff.

## Sources
- [SKYLANDX — MetaCam Air 2 brochure (PDF, official)](https://skylandx.com/wp-content/uploads/MetaCam_Air_2_EN.pdf)
- [SKYLANDX — C01 LiDAR brochure (PDF, official)](https://skylandx.com/wp-content/uploads/EN_C01_LiDAR_BROCHURE.pdf)
- [SKYLANDX — Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Spatial Perception Robots](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — Software platforms](https://skylandx.com/software-platforms/)
- [SKYLANDX company profile (this vault)](../SKYLANDX.md)
- Open-source repositories (existence checked 2026-11-14; fit with SKYLANDX data untested): [roslibpy](https://github.com/gramaziokohler/roslibpy) · [rosbridge_suite](https://github.com/RobotWebTools/rosbridge_suite) · [Nav2](https://github.com/ros-navigation/navigation2) · [Open3D](https://github.com/isl-org/Open3D) · [pointcloud_to_laserscan](https://github.com/ros-perception/pointcloud_to_laserscan) · [FAST-LIO](https://github.com/hku-mars/FAST_LIO)
