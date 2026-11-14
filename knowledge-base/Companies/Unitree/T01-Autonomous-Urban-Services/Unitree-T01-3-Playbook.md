---
type: challenge-playbook
company: "Unitree Robotics"
slug: Unitree
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Unitree Robotics × T01 — Hackathon Playbook

⬆ [Unitree Robotics profile](../Unitree.md) · [Brief](Unitree-T01-1-Brief.md) · [Products and solutions](Unitree-T01-2-Products-and-Solutions.md)

**Before anything else (first 30 minutes):** confirm you have a **Go2 EDU** (not Air / Pro), whether an Orin module is fitted, how many batteries and chargers you get, and where you are allowed to run. Everything below assumes Go2 EDU unless stated. Hardware on site is not confirmed.

**Common base stack for all concepts**

| Layer | Choice |
|---|---|
| Robot link | Ethernet to the robot, CycloneDDS; unitree_sdk2_python or unitree_ros2 (ROS 2 Humble, Ubuntu 22.04) |
| Motion | High-level sport API (velocity commands); keep the factory obstacle avoidance on; never use low-level joint control |
| Sensing | LiDAR cloud on `utlidar/cloud`, front camera via SDK; add a USB camera if needed |
| Mapping / navigation | slam_toolbox + Nav2 (community go2_ros2_sdk has this wired) or point_lio_unilidar for odometry |
| Compute | On-board Orin if fitted; otherwise a laptop on the Ethernet tether or a backpack mini-PC; cloud LLM / VLM only where Wi-Fi is reliable |
| Safety | Speed cap ≤ 1 m/s near people, spotter holding the remote, taped demo lane |

## Solution approaches

### Concept 1 — Stair-capable courier ("Bergbote")
- **Problem → value:** Leukerbad's hotels, clinics and pharmacy are linked by stairs, ramps and steep lanes that stop wheeled delivery robots. A legged courier moves small items (medication, room service, lab samples, lost property) door to door.
- **Hardware:** Go2 EDU + light lidded cargo box (≤ 5 kg loaded, well inside the ~7–8 kg payload). Optional: Go2-W for speed on flat stretches; SKYLANDX MetaCam to pre-scan the venue; D-Robotics RDK X5 as a cheap extra perception computer.
- **Architecture / stack:** LiDAR → slam_toolbox map → Nav2 global / local planner → `cmd_vel` bridged to sport velocity requests. Named waypoints ("reception", "room 12") in a YAML file. Task layer: small web app or chat bot creates jobs; QR code or PIN on a phone confirms pickup and drop-off; robot speaks status through its speaker. Stairs: switch to a stair gait segment with a scripted straight-line traverse rather than asking Nav2 to plan on stairs.
- **48-hour plan:**
  - **H0–6:** SDK hello-world, teleop from laptop, record a rosbag of the route, build the box.
  - **H6–24:** map the demo area, tune Nav2 footprint and speeds, waypoint-to-waypoint runs on flat ground, job web app.
  - **H24–40:** stair segment, handover confirmation, voice prompts, 10 full dry runs, battery-swap routine.
  - **H40–48:** freeze code, film a backup video, rehearse the pitch.
- **3-minute demo script:** (0:00) judge orders an item on a phone → (0:20) staff loads the box, scans QR → (0:30) robot navigates the lane, climbs a short staircase → (1:45) arrives, announces itself, judge scans to confirm → (2:00) dashboard shows trip log, time and battery → (2:15) slide: cost per trip versus staff time, routes in Leukerbad where wheels fail.
- **Risks and fallbacks:** localisation loss in crowds → add AprilTags at waypoints; stairs unreliable → demo a ramp and show stairs under manual control; Nav2 not ready → line-following or tag-to-tag navigation; box shifts → lower the centre of mass, strap it.
- **Judging angles:** *Innovation* modest; *technical depth* in mixed flat / stair navigation; *impact* clear and measurable; *Leukerbad relevance* high (steep, stepped town, clinics).

### Concept 2 — Public-space upkeep patrol ("Dorf-Check")
- **Problem → value:** a small municipality cannot inspect every path daily. A robot walks a fixed round and reports icy patches, full bins, blocked paths, broken lights or litter as geotagged tickets for the works crew.
- **Hardware:** Go2 EDU (camera + LiDAR). Optional: As2 / As2-W if available (IP54, −20 °C, ~3 h); SKYLANDX MetaCam for a reference 3D map; XREAL glasses for the crew's ticket view.
- **Architecture / stack:** same navigation base on a recorded patrol loop → at each checkpoint capture images → vision-language model (cloud, or a small detector on Orin for bins / litter) classifies "OK / issue + type" → ticket with photo, map position and severity pushed to a web dashboard. LiDAR map differencing flags new obstacles on the path.
- **48-hour plan:**
  - **H0–6:** teleop, pick 6–8 checkpoints, define 4 issue types you can stage reliably.
  - **H6–24:** patrol loop navigation; image capture; VLM prompt and JSON schema; dashboard.
  - **H24–40:** staged issues (tipped bin, cone on path, "ice" mat), false-positive tuning, map-change detection.
  - **H40–48:** rehearse, record backup run, prepare a before / after map.
- **3-minute demo script:** (0:00) show the empty dashboard → (0:15) robot starts its round → (0:45) finds an overflowing bin, ticket appears with photo → (1:15) detects a blocked path and reroutes → (1:45) crew member closes a ticket on phone or AR glasses → (2:15) slide: kilometres of path per battery, hours saved, winter-safety angle.
- **Risks and fallbacks:** VLM latency or no internet → local detector with fixed classes; navigation fails → walk the round under teleop and keep the perception pipeline autonomous (still a valid demo); lighting → fixed checkpoint poses and the robot's front light.
- **Judging angles:** *Innovation* in turning a robot dog into a municipal sensor; *technical depth* in perception + change detection; *impact* on winter safety and maintenance cost; *Leukerbad relevance* high (ice, snow, tourist paths). Overlaps with T02 — pitch it as service upkeep, not emergency response.

### Concept 3 — Follow-me porter and guide ("Gepäck-Hund")
- **Problem → value:** guests, many elderly, arrive by bus and walk uphill with luggage to hotels and thermal baths. A robot carries the bag, guides them along the accessible route, and adapts to their pace.
- **Hardware:** Go2 EDU or Go2-W with a luggage rack (bag ≤ 7 kg); As2-W if available (~16 kg, built-in side-follow). Optional: G1 / G1+ EDU as a stationary greeter at the start point; XREAL glasses for a staff dispatcher.
- **Architecture / stack:** person tracking (camera detector + LiDAR cluster) → follow / lead controller holding 1–1.5 m distance → route from the Nav2 map in "lead" mode, pure tracking in "follow" mode. Speech-to-text and an LLM for multilingual destination requests ("Thermalbad", "Hotel X") with text-to-speech on the robot speaker. Pace adaptation: slow down when the tracked person falls behind; stop and announce at stairs, offering the step-free route.
- **48-hour plan:**
  - **H0–6:** teleop, rack build, person detector running on the camera stream.
  - **H6–24:** follow mode robust to one occluding passer-by; voice destination intent; map with 3 destinations.
  - **H24–40:** lead mode with pace adaptation, re-acquisition after losing the person, multilingual prompts (DE / FR / EN).
  - **H40–48:** rehearse with a real suitcase and a volunteer; backup video.
- **3-minute demo script:** (0:00) guest says "take me to the thermal bath" in German → (0:15) bag goes on the rack, robot confirms destination → (0:30) leads the way, slows when the guest lags → (1:30) pauses at stairs, offers the ramp route → (2:00) arrival, guest takes bag, robot returns to base → (2:20) slide: accessibility and tourism value.
- **Risks and fallbacks:** tracking the wrong person → coloured vest or AprilTag on the guest; speech fails in noise → phone / tablet destination picker; rack makes the robot unstable → lighter bag, lower mount, slower gait.
- **Judging angles:** *Innovation* in pace-adaptive guiding; *technical depth* in tracking + navigation + dialogue; *impact* on accessibility; *Leukerbad relevance* very high (elderly spa guests, steep lanes). Also arguable under T04.

### Concept 4 — Multi-robot service relay (most ambitious)
- **Problem → value:** real urban logistics crosses domains — an indoor hub, an outdoor stepped route, a handover at the door. One robot type cannot do it all; a relay of specialists can.
- **Hardware:** indoor manipulator loads the parcel — Unitree G1-D Flagship if present, otherwise another vendor's unit (Galbot G1, Galaxea R1, or a fixed Flexiv Rizon / Dobot / ROKAE arm as a loading station) → Go2 EDU / Go2-W carries it over stairs and outdoors → recipient handover. Optional XREAL glasses as dispatcher console.
- **Architecture / stack:** central dispatcher (simple job queue + state machine over MQTT or ROS 2) assigns pick, load, carry and handover steps. Loading station: marker-based docking of the dog under the arm, scripted or teleoperated pick-and-place into the box. Courier: Concept 1 stack. Use separate DDS domain IDs so the robots do not collide on the network.
- **48-hour plan:**
  - **H0–6:** split into courier and loading sub-teams; agree the interface (docking pose, box geometry, job messages).
  - **H6–24:** courier navigation A → B; arm places a fixed parcel into a fixed box; dispatcher skeleton.
  - **H24–40:** docking accuracy, end-to-end relay, failure states (parcel missed, robot late).
  - **H40–48:** three clean end-to-end runs or cut scope to a scripted handover; backup video.
- **3-minute demo script:** (0:00) order placed → (0:20) arm or G1-D picks the parcel and loads the docked dog → (1:00) dog leaves, climbs steps, crosses the "street" → (2:00) recipient confirms → (2:15) dispatcher view shows both robots' states → (2:30) slide: how the relay scales to a town.
- **Risks and fallbacks:** two-vendor integration slips → teleoperate the loading step (xr_teleoperate for Unitree humanoids) and keep the courier autonomous; docking imprecise → funnel-shaped box and AprilTag; network clashes → wired links, fixed IPs, domain IDs.
- **Judging angles:** *Innovation* and *technical depth* highest; *impact* as a system blueprint; *Leukerbad relevance* medium-high; delivery risk highest — only for teams of four or more with ROS 2 experience.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Go2 EDU + SKYLANDX MetaCam | Pre-scanned, accurate 3D map of the venue to localise against; nice visual for the pitch | Low–medium (map format conversion) |
| Go2 EDU + D-Robotics RDK X5 | Extra on-board perception compute if no Orin is fitted | Low (ROS 2 node over Ethernet) |
| Go2 EDU + XREAL glasses | Dispatcher or works-crew AR view of jobs and tickets | Medium (separate app, web API) |
| Go2 EDU + Flexiv / Dobot / ROKAE arm | Fixed loading / unloading station for parcels | Medium (docking + pick-and-place) |
| Go2 EDU + Galbot G1 / Galaxea R1 | Indoor mobile manipulation feeding an outdoor legged courier | High (two stacks, one dispatcher) |
| Go2 EDU + Binabik AI or Genisom SomaMind | Agent layer for task planning on top of the SDK | Unknown — interfaces not public |
| G1 EDU + XR headset (xr_teleoperate) | Remote-operated concierge as a safe fallback | Low–medium (official repo) |

## Questions to ask the Unitree Robotics engineers on site

1. Which exact variants are available to teams — **Go2 EDU, X, Pro or Air** — and is the Orin module fitted?
2. How many batteries and chargers per robot, and what is the real swap / recharge time?
3. Is there a built-in mapping and navigation service on this firmware that we can call from the SDK, or must we bring our own SLAM?
4. Is a Go2-W, As2 or As2-W available, and is the **side-follow** function controllable through the SDK?
5. What is the safe continuous payload and the approved mounting points / power output for a cargo box?
6. May we run outdoors on wet or snowy ground, and what is the ingress protection of the units you brought?
7. Is a G1-D on site, and does its base expose a navigation API?
8. What is the recommended network setup for several robots on one LAN (IP ranges, DDS domain IDs), and is a wireless e-stop provided?

## Decision rule

- **Pick Unitree Robotics for T01 if** your idea depends on getting over stairs, slopes or rough ground, you have confirmed EDU-level SDK access, and at least one teammate can stand up ROS 2 navigation on day 1.
- **Avoid if** the core of your idea is manipulation (shelves, doors, cleaning with tools) or a turnkey indoor delivery flow on flat floors — a wheeled mobile manipulator from another vendor gets you there faster.

## Sources

- [Unitree Go2-W](https://www.unitree.com/go2-w)
- [Unitree As2-W](https://www.unitree.com/As2-W)
- [Unitree G1-D](https://www.unitree.com/G1-D)
- [Unitree GitHub organisation — repositories](https://github.com/orgs/unitreerobotics/repositories?type=all&sort=stargazers)
- [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
- [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python)
- [go2_ros2_sdk (community)](https://github.com/abizovnuralem/go2_ros2_sdk)
- [Unitree Go2](https://www.unitree.com/go2) (via the company profile, not re-fetched)
