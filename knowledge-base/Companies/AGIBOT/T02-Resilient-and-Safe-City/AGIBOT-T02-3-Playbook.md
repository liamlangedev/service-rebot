---
type: challenge-playbook
company: "AGIBOT"
slug: AGIBOT
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# AGIBOT × T02 — Hackathon Playbook

⬆ [AGIBOT profile](../AGIBOT.md) · [Brief](AGIBOT-T02-1-Brief.md) · [Products and solutions](AGIBOT-T02-2-Products-and-Solutions.md)

> Assumption for every concept: a **D1 Edu or D1 Ultra** (open SDK) is available to teams. This is a best guess — confirm at the booth first. The D1 SDK gives you `move(vx, vy, yaw_rate)`, posture, joint commands and IMU; **perception and navigation run on your own companion computer**.

## Solution approaches

### Concept 1 — Hazard patrol dog (safest)

- **Problem → value:** Spa basements, parking garages, service tunnels and stairwells are checked by hand, rarely at night. A patrolling quadruped spots a person on the floor, a blocked escape route, an open fire door or a heat source and raises an alert with a photo and location.
- **Hardware:** D1 Edu / Ultra · companion computer on its back (laptop, Jetson, or D-Robotics RDK X5) · USB RGB or depth camera · optional thermal camera.
- **Architecture / stack:** camera → open-vocabulary detector or VLM on the companion (or a laptop over Wi-Fi) → simple state machine (patrol / investigate / alert) → velocity commands through the D1 Python SDK over Ethernet (`192.168.168.168`). Localisation by fiducial markers at checkpoints plus IMU heading; alerts to a web dashboard.
- **48-hour plan:**
  - **H0–6:** confirm variant and SDK; run `highlevel_demo`; drive the dog from your own script; mount camera and computer (under 5 kg).
  - **H6–24:** marker-based route following between 4–6 checkpoints; detection of 2–3 hazard classes; alert pipeline.
  - **H24–40:** stairs / ramp segment; "investigate" behaviour (approach, re-photograph); dashboard polish; battery-swap routine.
  - **H40–48:** rehearse; record a backup video; freeze code.
- **3-minute demo script:** (0:00) show the map and the route → (0:30) dog starts patrol, passes checkpoint 1 clean → (1:15) finds a "collapsed person" dummy, stops, alert with image appears on the dashboard → (2:00) finds a blocked exit, reroutes → (2:40) summary: coverage, detections, time saved.
- **Risks and fallbacks:** camera stream not accessible through the SDK → use your own USB camera (plan for this from the start). Marker localisation fails → teleoperate the route with the handheld remote and keep detection autonomous. Battery **1–2 h** → schedule charging (about 1 h for 10→90%).
- **Judging angles:** *innovation* low–medium; *technical depth* in closed-loop perception-to-motion on legs; *impact* clear and measurable; *Leukerbad* — thermal-bath plant rooms, hotel garages, clinic night rounds.

### Concept 2 — Digital-twin change detection for alpine infrastructure

- **Problem → value:** After a storm or rockfall alert, someone must check paths, galleries and cable-car stations. Compare today's robot pass with a baseline 3D scan and flag what changed (debris, snow load, missing barrier, water).
- **Hardware:** D1 Edu / Ultra (D1 Max if available, for IP67 and range) · SKYLANDX MetaCam for the baseline scan · depth camera or small LiDAR on the dog · companion computer.
- **Architecture / stack:** baseline point cloud / mesh from MetaCam → dog localises against it (LiDAR or visual relocalisation; fall back to markers) → per-checkpoint capture → geometric diff + VLM description of each change → change log pinned on the 3D model in a browser viewer. Control through the D1 SDK; heavy compute on a laptop.
- **48-hour plan:**
  - **H0–6:** scan the demo area; get the dog moving by script; pick the localisation method that works in the first two hours.
  - **H6–24:** repeatable route with pose-tagged captures; diff pipeline on recorded data.
  - **H24–40:** live run with staged changes (boxes as "rockfall", cone removed, puddle); viewer with before / after.
  - **H40–48:** rehearse, backup recording.
- **3-minute demo script:** (0:00) baseline twin on screen → (0:30) "storm overnight" — dog dispatched → (1:30) three pins appear with before / after images and a one-line description each → (2:30) operator marks one as critical; route closed on the map.
- **Risks and fallbacks:** relocalisation is the hard part → restrict to fixed checkpoints with markers and diff images only. Sensor mounting and power from the D1 port unclear → run sensors from a power bank.
- **Judging angles:** *innovation* medium–high (twin + legged re-survey); *technical depth* high; *impact* inspection without sending people into exposed terrain; *Leukerbad* — Gemmi path, avalanche galleries, cable-car stations.

### Concept 3 — Evacuation guide team for spa and clinic

- **Problem → value:** Thermal baths and rehab clinics host many elderly, slow or hearing-impaired guests. On alarm, a humanoid at a known point gives calm multilingual instructions and leads people to the assembly point while the dog sweeps rooms for anyone left behind and reports a headcount.
- **Hardware:** X2 (Edu / Ultra) humanoid · D1 Edu / Ultra · camera + companion computer on the dog · optional XREAL glasses for the incident commander.
- **Architecture / stack:** shared incident server (alarm trigger, floor plan, status) → X2 via AimDK_X2 (ROS 2): TTS, face screen, gestures, velocity commands along a pre-taught route; dialogue through an LLM with a whitelisted-skill pattern as in AGIBOT's AgentSDK reception sample → D1 runs the sweep from Concept 1 with person detection → commander view on tablet or glasses.
- **48-hour plan:**
  - **H0–6:** check X2 firmware vs SDK version; TTS + velocity control working; D1 scripted motion.
  - **H6–24:** X2 guide route and multilingual script (DE / FR / EN); D1 room sweep with person detection; incident server.
  - **H24–40:** hand-offs (dog finds person → humanoid or staff notified), headcount logic, commander view.
  - **H40–48:** rehearse with volunteers; backup video.
- **3-minute demo script:** (0:00) alarm triggered → (0:20) X2 announces in three languages and starts leading two "guests" → (1:10) D1 sweeps two rooms, finds one person, alert on commander view → (2:00) X2 answers "where is the exit?" and confirms headcount → (2:40) all-clear screen.
- **Risks and fallbacks:** X2 navigation module / vision interface may not be enabled → keep the X2 stationary as a talking signpost with gestures, or drive open-loop along a taped line. Two robots, two SDKs → build and test them independently; integrate only through the server.
- **Judging angles:** *innovation* in human-centred response; *technical depth* multi-robot coordination; *impact* vulnerable-guest safety; *Leukerbad* — direct match to baths, clinics and hotels.

### Concept 4 — Scout, carry and act: mixed first-response team (most ambitious)

- **Problem → value:** In the first minutes after an avalanche, flood or gas alarm, responders need eyes on site, supplies delivered and one simple manipulation done (close a valve, open a door) without entering.
- **Hardware:** D1 Edu / Ultra as scout · D1 Max or D1 MaxPro as carrier if on site (25–50 kg, IP67) — otherwise a second small dog with a light kit · G2 or another vendor's mobile manipulator (Galaxea, Galbot, Unitree) teleoperated for the valve · XREAL glasses for first-person view · D-Robotics RDK on each dog.
- **Architecture / stack:** mission server with shared map → scout streams video + detections → carrier follows scout waypoints (D1 Max SDK is C++ high-level over Wi-Fi, port `8082` in the demo) → operator teleoperates the manipulator for the final task → timeline of events for the debrief.
- **48-hour plan:**
  - **H0–6:** lock down which robots you really get; one script per robot proving remote control.
  - **H6–24:** scout perception + video link; carrier follow behaviour; teleop of the arm on the bench.
  - **H24–40:** end-to-end mission on a staged course; operator UI; failure handling.
  - **H40–48:** cut scope to what works three times in a row; record backup.
- **3-minute demo script:** (0:00) alarm and mission brief → (0:30) scout enters, maps hazard, finds casualty → (1:20) carrier delivers a first-aid kit / radio to the casualty → (2:00) operator closes the valve through the manipulator → (2:40) mission timeline replay.
- **Risks and fallbacks:** hardware access is the main risk — design so the scout-only mission (Concept 1) stands alone. SDK / firmware mismatches on D1 Max (V3 vs V4). Wi-Fi congestion in the hall → wired tether or a private router.
- **Judging angles:** *innovation* and *ambition* high; *technical depth* heterogeneous fleet; *impact* responder safety; *Leukerbad* — avalanche and flood scenarios, remote valley access.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| D1 + D-Robotics RDK X5 / S100 | On-dog perception (detection, depth) without a laptop on its back | Low–medium: USB / Ethernet to the dog, SDK has aarch64 libs |
| D1 + SKYLANDX MetaCam | Baseline 3D map / digital twin for change detection and route planning | Medium: offline scan is easy, live relocalisation is hard |
| D1 + XREAL glasses | First-person operator view with alert overlays | Low–medium: video stream + simple overlay app |
| D1 + Unitree Go2 or Genisom M1 | Mixed quadruped patrol fleet, vendor-agnostic mission layer | Medium: separate SDKs behind one velocity / status interface |
| X2 + Binabik AI | Agent layer for the evacuation-guide behaviours | Unknown: depends on Binabik's X2 support — ask |
| D1 scout + Galaxea / Galbot / G2 manipulator | "Find it, then fix it" missions | High: two robots, teleop link, shared map |
| D1 + OriginFlow EMG | Gesture / muscle-signal teleoperation of the dog for gloved responders | Medium–high: novel input, needs mapping to `move()` |

## Questions to ask the AGIBOT engineers on site

1. Which exact units can teams program — D1 **Edu**, **Ultra** or Pro (Pro has no secondary development)? Any D1 Max / MaxPro?
2. Which firmware / system version is on each robot, and which SDK release matches it?
3. Can we read the D1's built-in camera stream from our own code, and how (API, RTSP, app only)?
4. What voltage and current does the D1 power port supply for a companion computer and sensors?
5. Is there any built-in follow, waypoint or mapping function (AGIQUAD Go app), and is it scriptable?
6. Can the D1 run outdoors here in November (snow, below 0 °C)? What are the house rules for stairs and outdoor tests?
7. For the X2: is the SLAM / navigation module installed, is the vision interface enabled, and can we get AgentSDK / LinkSoul credentials?
8. How many spare batteries and chargers are available, and is there a ROS 2 bridge for the D1 or do we write our own?

## Decision rule

- **Pick AGIBOT for T02 if** a D1 Edu / Ultra (or D1 Max) is confirmed for your team, you are comfortable adding your own camera, compute and navigation, and your idea is patrol, inspection or scouting on stairs and slopes.
- **Avoid if** you need turnkey autonomous navigation and mapping on day one, sub-zero outdoor operation on the small dog, or a documented safety-domain reference deployment to point to.

## Sources
- [AGIBOT — D1 Ultra product page](https://www.agibot.com/products/D1Ultra)
- [AGIBOT — D1 Pro / Edu product page](https://www.agibot.com/products/D1_Pro)
- [AGIBOT — D1 Max product page](https://www.agibot.com/products/D1_Max)
- [AGIBOT — D1 MaxPro product page](https://www.agibot.com/products/D1_MaxPro)
- [AGIBOT — New generation of embodied AI robots and models (2026-04-17)](https://www.agibot.com/article/231/detail/63.html)
- [GitHub — AgibotTech/agibot_D1_Edu-Ultra](https://github.com/AgibotTech/agibot_D1_Edu-Ultra)
- [GitHub — AgibotTech/Agibot_D1_Max](https://github.com/AgibotTech/Agibot_D1_Max)
- [GitHub — AgibotTech/agibot_agentsdk_sample_code](https://github.com/AgibotTech/agibot_agentsdk_sample_code)
- [AimDK_X2 documentation](https://x2-aimdk.agibot.com/en/latest/)
- [AGIBOT company profile (internal)](../AGIBOT.md)
