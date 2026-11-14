---
type: challenge-playbook
company: "SKYLANDX"
slug: SKYLANDX
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# SKYLANDX × T02 — Hackathon Playbook

⬆ [SKYLANDX profile](../SKYLANDX.md) · [Brief](SKYLANDX-T02-1-Brief.md) · [Products and solutions](SKYLANDX-T02-2-Products-and-Solutions.md)

> **Ground rules for planning:** (1) Which SKYLANDX hardware is on site is unconfirmed — assume a MetaCam Air 2 and verify in the first hour. (2) File export (PLY / PCD / LAS / E57, OBJ, 3DGS PLY) is the only integration path you can count on; live Rosbridge / API access depends on what the SKYLANDX engineers hand out. (3) Concepts 1–2 need no vendor API; concepts 3–4 do.

## Solution approaches

### Concept 1 — Hazard Delta: scan, re-scan, show what changed

- **Problem → value:** After a rockfall, avalanche, quake or water ingress, operators must know quickly what moved or is blocked in a tunnel, gallery, plant room or cable-car station. A 10-minute walk-through scan compared against a baseline gives an objective, cm-level damage and blockage map instead of photos and guesswork.
- **Hardware:** MetaCam Air 2 (handheld) + laptop. Nothing else.
- **Architecture / stack:**
  - Perception: on-device SLAM → colorized point cloud; MetaCam Go coverage check.
  - Processing: MetaCam Studio (optimize, align, export PLY / LAS). Fine alignment with ICP in Open3D.
  - Analysis: cloud-to-cloud or M3C2 distance (CloudCompare CLI or Open3D), threshold at a few cm, cluster changed points, compute volume and position per cluster, classify as "added / removed / deformed".
  - Output: web report with 3D heat map, ranked change list, "exit blocked" flag where a change cluster cuts a walkable corridor. Compute: laptop only.
- **48-hour plan:**
  - H0–6: get scanner + software access; baseline scan of the chosen site; export and load in Open3D. Start coding on SKYLANDX sample data in parallel.
  - H6–24: stage changes (boxes as debris, moved barrier, closed door); second scan; registration + distance pipeline; first heat map.
  - H24–40: clustering, volume estimate, blocked-route logic, web viewer; test repeatability with a no-change re-scan to set the noise floor.
  - H40–48: rehearse the live run end to end; record a backup video; freeze.
- **3-minute demo script:** 0:00 show baseline twin → 0:30 teammate "causes" an incident (debris, blocked exit) → 0:45 live walk-through scan with coverage view on the phone → 1:45 run pipeline → 2:15 heat map + list ("0.4 m³ new material at exit B, route blocked") → 2:45 how this scales to a road gallery or cable-car station.
- **Risks and fallbacks:** processing slower than the demo slot → pre-process a second "after" scan and show live capture separately · SLAM drift creates false changes → use control points / overlap-rich paths and report the measured noise floor · no Studio licence → request raw export from staff or use Skyland Cloud.
- **Judging angles:** innovation medium (known method, sharp packaging) · technical depth: registration, noise floor, volumetrics · impact: faster reopening of infrastructure · Leukerbad: rockfall / avalanche galleries, thermal plant rooms, lift stations.

### Concept 2 — Responder Twin: pre-incident 3D plan with AR guidance

- **Problem → value:** Fire brigade, mountain rescue and clinic staff rarely have current 3D plans of the building they enter. A scanned twin with exits, shut-off valves, hazards and safe routes cuts orientation time, especially for guests and elderly evacuees in spa and clinic buildings.
- **Hardware:** MetaCam Air 2 + laptop; optional **XREAL** glasses for an in-situ overlay; optional **D-Robotics RDK** as a local server if connectivity is poor.
- **Architecture / stack:**
  - Capture: one scan → point cloud + OBJ mesh + 3DGS (Skyland Cloud).
  - Planning: slice the cloud into a floor-level occupancy grid, extract walkable space, A* evacuation routes; re-plan when a corridor is marked blocked (pairs with Concept 1 output).
  - Semantics: detect doors, extinguishers, signage in the 360° panoramas with an off-the-shelf detector and project into 3D; manual tagging as fallback.
  - Presentation: browser viewer (3DGS for realism, point cloud for measurement); XREAL view showing route arrows — localization in the twin by markers / manual alignment unless SKYLANDX relocalization is made available.
- **48-hour plan:**
  - H0–6: scan one floor or wing; submit to Cloud for 3DGS; check turnaround.
  - H6–24: occupancy grid + routing; panorama detection; viewer skeleton.
  - H24–40: blocked-route re-planning; AR overlay or tablet walkthrough; annotate assets.
  - H40–48: scripted scenario, backup video.
- **3-minute demo script:** 0:00 "a responder who has never been here" → 0:30 fly through the photorealistic twin → 1:00 click "fire in room X": routes recompute, nearest extinguisher and shut-off highlighted → 2:00 put on glasses / tablet and follow the arrows in the real corridor → 2:40 capture cost: one person, minutes per floor.
- **Risks and fallbacks:** Cloud 3DGS slow or unavailable → show colorized point cloud / mesh · AR registration unstable → tablet view with a "you are here" marker · permission to scan clinic or hotel areas → use the hackathon venue.
- **Judging angles:** innovation medium-high (routing + AR on a measured twin) · technical depth: geometry-to-navigation pipeline · impact: clear user (responders, facility managers) · Leukerbad: clinics, thermal baths, hotels with elderly guests.

### Concept 3 — No-Entry Patrol: quadruped carries the scanner into the hazard zone

- **Problem → value:** Sending a person to check a gallery after rockfall, a flooded basement or a plant room with a suspected leak is the dangerous step. A legged robot with a mapping payload does the first look and returns a measured 3D picture.
- **Hardware:** MetaCam Air 2 + **MetaCam Hub** on a quadruped — **Unitree Go2 / B2**, **Genisom M1 / L1**, **Magiclab MagicDog** or **AGIBOT D1** (check payload and mounting with that vendor). Optional **D-Robotics RDK** on the robot for detection.
- **Architecture / stack:**
  - Perception: MetaCam SLAM → live pose + point cloud over the Rosbridge WebSocket (roslibpy or rosbridge client) to an operator laptop.
  - Planning: teleoperation first; then waypoint following in the baseline map using MetaCam relocalization for pose and the robot vendor's SDK for velocity commands.
  - Control: robot's own locomotion controller. SKYLANDX's navigation-command output only if staff enable it.
  - Analysis: Concept 1 change detection on the patrol scan; optional camera-based detection (person, leak, open door) pinned to map coordinates.
  - Compute: SLAM on the MetaCam, robot control on the robot, analysis on the laptop.
- **48-hour plan:**
  - H0–6: confirm Hub + API access and a carrier robot; mount; stream pose to the laptop. **Go / no-go at H6** — without live pose, fall back to "robot carries, scan is processed afterwards".
  - H6–24: teleop patrol with live map in the operator view; baseline scan of the route.
  - H24–40: relocalize in the baseline; semi-autonomous waypoint run; change detection on the patrol data.
  - H40–48: reliability runs, backup video, operator UI polish.
- **3-minute demo script:** 0:00 "zone closed, nobody enters" → 0:20 robot walks in, live 3D map grows on screen → 1:20 robot returns; delta map shows new debris and a blocked passage with volume → 2:10 operator marks a safe route → 2:40 same kit works in a tunnel with no GNSS.
- **Risks and fallbacks:** API / Hub not available → strap the handheld unit to the robot, process offline · vibration degrades SLAM → slow gait, damped mount · Wi-Fi drops in the zone → log on device, sync on return · two vendors' support needed at once → book both early.
- **Judging angles:** innovation high (cross-vendor, human removed from risk) · technical depth: live SLAM bridge + relocalization · impact: matches SKYLANDX's own "no human entry" use case · Leukerbad: galleries, steep icy access, plant rooms.

### Concept 4 — First-Look Explorer: autonomous mapping and victim pinning in an unknown space

- **Problem → value:** In the first minutes of an incident nobody has a map. A robot that explores on its own, builds the 3D map and marks people and hazards in it gives the incident commander a shared picture before teams go in.
- **Hardware:** as Concept 3, plus an RGB (ideally thermal — not from SKYLANDX) camera and **D-Robotics RDK X5 / S100** for on-board detection. Optional second robot or handheld unit to show map merging.
- **Architecture / stack:**
  - Perception: MetaCam pose + cloud stream → rolling occupancy / elevation map.
  - Planning: frontier-based exploration on the occupancy map; goals sent to the robot's navigation or velocity interface; MetaCam navigation outputs if granted.
  - Detection: person / hazard detector on the RDK; detections ray-cast into the map frame.
  - Command view: web dashboard with live map, robot track, pins, coverage percentage; finished scan pushed to Skyland Cloud for the 3DGS twin.
- **48-hour plan:**
  - H0–6: same go / no-go as Concept 3 (live pose + cloud is mandatory here).
  - H6–24: occupancy mapping from the stream; teleop + detection pins working end to end.
  - H24–40: frontier exploration in a small staged area (cardboard "rubble", mannequin or volunteer); dashboard.
  - H40–48: constrain the arena until it runs 3 times in a row; backup video.
- **3-minute demo script:** 0:00 unknown room, lights low → 0:15 "explore" pressed, robot maps on its own, coverage counter climbs → 1:30 person detected, pin drops in 3D with coordinates → 2:10 commander view: route to the victim through mapped free space → 2:40 limits and next steps stated honestly.
- **Risks and fallbacks:** autonomy not stable → supervised autonomy (operator clicks goals) · no live stream → degrade to Concept 3 fallback · detection false positives → confirm step by operator · scope creep is the main risk; cut multi-robot first.
- **Judging angles:** innovation highest · technical depth: exploration, 3D detection fusion, multi-vendor integration · impact: search-and-rescue first response · Leukerbad: avalanche / rockfall incidents, underground parking, tunnels.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| SKYLANDX MetaCam Air 2 + Unitree Go2 / B2 | Legged no-entry mapping patrol; Unitree SDK for motion, MetaCam for pose / map | Medium — mount + Rosbridge client; high if you want closed-loop autonomy |
| SKYLANDX + Genisom M1 / L1, Magiclab MagicDog or AGIBOT D1 | Same as above on an alternative quadruped if Unitree units are booked | Medium–high — depends on that vendor's SDK and payload mount |
| SKYLANDX + XREAL | Responder AR: routes, hazards and change heat map overlaid on the real corridor | Medium — aligning the glasses to the scan frame is the hard part |
| SKYLANDX + D-Robotics RDK X5 / S100 | On-robot detection (people, leaks) fused into the 3D map; local server without cloud | Low–medium |
| SKYLANDX scan + any mobile manipulator (Galaxea R1, Galbot G1, AGIBOT G1 / G2, Spirit AI Moz1, UniX AI Wanda) | Prior map for navigation so the robot can act on a finding (close a valve, clear an object) | High — map format conversion and that robot's navigation stack |
| SKYLANDX + Binabik AI | Agent layer that turns "inspect gallery 2 and report changes" into scan / compare / report steps | Unknown — depends on Binabik's interfaces |
| SKYLANDX C01 LiDAR + Leadshine / coprod custom platform | Build-your-own inspection rover with open SLAM | High — only if a C01 is on site and the team has ROS depth |

## Questions to ask the SKYLANDX engineers on site

1. Which units can teams borrow (Air 2, Air 3, Lite, Pro, C01, MetaCam Hub), how many, and for how long?
2. Can we get the Rosbridge WebSocket documentation now — topics, message types, rates, ROS 1 vs ROS 2, and is the pose stream available during capture?
3. Is relocalization against a previous scan available to us through the API, and what does it need (same device, map file format)?
4. Is the navigation-command output usable this weekend, and has it been run on any robot present here (Unitree Go2 / B2, others)?
5. How long does processing take for a 10-minute scan — in MetaCam Studio and for 3DGS in the Cloud — and do teams get licences / accounts?
6. What are the IP rating, operating temperature range and battery runtime of the Air 2? Can it scan outdoors in snow at around 0 °C?
7. What is the Air 2 LiDAR range and what drift should we expect in a long feature-poor corridor or tunnel without RTK?
8. Does Studio or Cloud have any scan-to-scan comparison, and can you share sample before / after datasets or a pre-scan of the venue?

## Decision rule

- **Pick SKYLANDX for T02 if** your idea is about knowing the state of a place — mapping, change / damage detection, digital twin for responders, GPS-denied localization — and you can deliver value from exported scans even if the live API never arrives.
- **Avoid if** you need a robot that acts by itself from hour 0, a documented open SDK, or hazard sensing beyond geometry and colour (thermal, gas, through-snow); then use SKYLANDX only as a mapping add-on to another vendor's platform.

## Sources
- [SKYLANDX — Robotics & Physical AI (MetaCam Hub, Rosbridge, APIs, relocalization, export formats)](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Spatial Perception Robots (GPS-denied exploration, safety patrols, platforms)](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — MetaCam Air 2](https://skylandx.com/metacam-air-2/)
- [SKYLANDX — MetaCam Pro](https://skylandx.com/metacam-pro/)
- [SKYLANDX — C01 LiDAR](https://skylandx.com/c01-slam-lidar/)
- [SKYLANDX — Software platforms](https://skylandx.com/software-platforms/)
- [SKYLANDX — Case studies: Industrial inspection](https://skylandx.com/case-studies-industrial-inspection)
- [SKYLANDX — Case studies: Surveying](https://skylandx.com/case-studies-surveying)
- [SKYLANDX company profile (this vault)](../SKYLANDX.md)
- Third-party tools named above ([Open3D](https://www.open3d.org/), [CloudCompare](https://www.cloudcompare.org/), [rosbridge_suite](https://github.com/RobotWebTools/rosbridge_suite), [roslibpy](https://github.com/gramaziokohler/roslibpy)) are cited from general knowledge; they were not re-checked in this pass because the web-search quota was exhausted.
