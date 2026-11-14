---
type: challenge-playbook
company: "XREAL"
slug: XREAL
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# XREAL × T02 — Hackathon Playbook

⬆ [XREAL profile](../XREAL.md) · [Brief](XREAL-T02-1-Brief.md) · [Products and solutions](XREAL-T02-2-Products-and-Solutions.md)

**Ground rule:** the robot does the T02 work (scout, inspect, patrol); XREAL makes the human in the loop faster and hands-free. Build the robot pipeline first, add the glasses second. Robot-side details below are generic — check the other vendor's profile for its real SDK.

| Concept | XREAL device needed | XREAL code needed | Risk |
|---|---|---|---|
| 1 Head-up scout console | Any glasses | None | Low |
| 2 Look-to-steer camera | One + Eye or Air 2 Ultra + Android host | Small Unity app | Medium |
| 3 Two-way responder link | One + Eye + Beam Pro | Unity app from samples | Medium |
| 4 Anchored hazard twin | Air 2 Ultra or AURA | Unity app + frame alignment | High |

## Solution approaches

### Concept 1 — Head-up scout console

- **Problem → value:** an operator sending a quadruped into a tunnel, avalanche-debris edge or flooded plant room must watch video, map and alerts while driving. A tablet takes eyes and one hand away. Glasses keep **eyes up and both hands on the controller**.
- **Hardware:** One Pro / 1 Pro+ / 1S plugged into the operator laptop (USB-C DisplayPort — confirm the port supports DP Alt Mode). Robot: Unitree Go2 / B2, AGIBOT D1, Magiclab MagicDog or Genisom M1 / L1. Optional: D-Robotics RDK on the robot for on-board detection.
- **Architecture / stack:**
  - Perception: robot camera (+ thermal / gas sensor if you have one) → detector on robot or laptop (person, smoke, fallen object).
  - Planning: waypoint patrol or manual drive; alerts raised by the detector.
  - Control: gamepad through the robot vendor's SDK.
  - UI: one full-screen web page or RViz layout — video centre, mini-map and alert list at the edges, large fonts. The glasses are just the second monitor. Compute: laptop + robot.
- **48-hour plan:**
  - H0–6: get robot video on the laptop; confirm glasses work as an external display; sketch the HUD layout.
  - H6–24: detector + alert logic; HUD page with video, map, alert feed.
  - H24–40: tune the layout for see-through optics (dark background, high contrast, nothing important in the corners); run the full scenario repeatedly.
  - H40–48: rehearse; record a backup video; mirror the glasses view to a projector for judges.
- **3-minute demo script:** (0:00) the scenario — "rockfall has closed the access tunnel". (0:30) operator puts on glasses, picks up the gamepad, robot enters the mock tunnel. (1:30) robot finds a "casualty" dummy / heat source; alert pops in the HUD; judges see the mirrored view. (2:30) operator marks the location and hands over to the rescue team.
- **Risks and fallbacks:** laptop port lacks DP Alt Mode → use a different laptop or an HDMI-to-USB-C adapter (ask XREAL staff). Glare → 1 Pro+ or clip-on shade. If the glasses fail entirely, the same UI runs on the laptop screen.
- **Judging angles:** innovation low; technical depth sits in the robot / perception side; impact is honest and practical; Leukerbad relevance: tunnel, rockfall and avalanche scouting where a responder must stay mobile.

### Concept 2 — Look-to-steer camera

- **Problem → value:** inspecting a structure (cable-car pylon, bridge underside, pipe gallery) by joystick-panning a camera is slow. Let the inspector **look around naturally**: head pose drives the robot's camera or head, video returns to the glasses.
- **Hardware:** One Pro + XREAL Eye (6DoF) or Air 2 Ultra, on Beam Pro / Samsung S24–S25. Robot with a steerable view: a humanoid head (Unitree G1 / H1, AGIBOT), a quadruped whose body pitch / yaw you command, or a camera on a small arm (Unitree Z1, Dobot, Flexiv Rizon — the configuration the ActiveGlasses paper used).
- **Architecture / stack:**
  - Input: Unity app (XREAL SDK 3.1.0) reads the head pose from the XR Origin camera every frame → UDP / WebSocket (or ROS-TCP-Connector) → ROS 2 node on the robot computer.
  - Planning: map head yaw / pitch to joint or body targets; rate-limit and clamp; dead-man switch on the phone controller.
  - Control: robot vendor SDK executes targets.
  - Feedback: robot camera → low-latency stream (MJPEG or WebRTC) → textured quad in the Unity scene, head-locked. Compute: robot + Android host; no cloud.
- **48-hour plan:**
  - H0–6: build and deploy the SDK sample to the host; log head pose over Wi-Fi to a laptop. In parallel, command the robot's view from a script.
  - H6–24: close the loop (pose → robot); get video into the Unity quad; measure end-to-end latency.
  - H24–40: smoothing, limits, recentre gesture; add an "inspection snapshot" button that saves frame + pose; optional defect detector overlay.
  - H40–48: rehearse; prepare fallback.
- **3-minute demo script:** (0:00) show the joystick way on video — slow. (0:30) inspector puts on glasses; robot camera mirrors their head live. (1:30) inspector finds a planted "crack" marker on a mock pylon, taps to capture; report line appears. (2:30) show latency number and the safety clamp.
- **Risks and fallbacks:** video latency causes discomfort → keep the video in a fixed window rather than full-view, and move the camera slowly. No Eye / Air 2 Ultra available → use 3DoF rotation only (enough for pan-tilt). Unity build trouble → fall back to Concept 1 and steer with the gamepad.
- **Judging angles:** innovation medium; technical depth good (closed loop, latency budget, safety limits); impact — faster remote inspection without rope access; Leukerbad relevance: cable cars, avalanche barriers, thermal-water infrastructure on steep ground.

### Concept 3 — Two-way responder link

- **Problem → value:** in an incident, the person on the ground and the command post see different things. Give the responder a **robot scout's findings in their view**, and give command the **responder's first-person video** — hands-free on both ends.
- **Hardware:** One Pro + XREAL Eye + Beam Pro on the responder; Windows laptop as command post; a scout robot (quadruped) searching ahead. Optional: SKYLANDX MetaCam scan of the venue as the shared map.
- **Architecture / stack:**
  - Uplink: the SDK's First Person View streaming sample sends the responder's view (real-world video + overlays) to the StreamingReceiver app on the command laptop over a dedicated Wi-Fi network.
  - Scout: robot runs detection (person, heat, obstacle) and publishes findings with map coordinates.
  - Downlink: small relay server (WebSocket) pushes findings, a 2D mini-map and command-post text / arrows to the Unity app; shown as head-locked HUD cards (One + Eye has no spatial anchors — keep overlays screen-space, with a compass-style bearing arrow from the 6DoF pose).
  - Optional AI: run a detector on Eye RGB frames (read as YUV textures, forwarded to the laptop) to flag hazards in the responder's own view.
- **48-hour plan:**
  - H0–6: run the FirstPersonViewStreamingCast sample end-to-end on a hotspot; robot team gets detections + positions.
  - H6–24: relay server; HUD cards and mini-map in Unity; command-post page with POV video + map + "send instruction" box.
  - H24–40: bearing arrow from head pose; scenario script; network hardening (own router, fixed IPs).
  - H40–48: rehearse with a split-screen view for judges.
- **3-minute demo script:** (0:00) split screen: command post left, responder POV right. (0:30) robot scout enters "smoke-filled corridor", reports a casualty at a map position. (1:15) card + bearing arrow appear in the responder's glasses; responder walks, hands free carrying kit. (2:00) command sees the POV, sends "valve on your left — close it"; responder complies. (2:40) recap.
- **Risks and fallbacks:** streaming is LAN-only and sensitive to busy Wi-Fi (docs say so) → bring your own router / hotspot. Protocol is undocumented, so re-using the stream in your own pipeline may not work → show the receiver window side by side instead. If Eye is unavailable → drop the uplink; keep the downlink HUD.
- **Judging angles:** innovation medium (human–robot–command triangle); technical depth moderate; impact strong and easy to grasp; Leukerbad relevance: volunteer mountain rescue and clinic evacuation, where few responders cover a lot of ground.

### Concept 4 — Anchored hazard twin

- **Problem → value:** a map on a screen forces responders to translate "3 m behind that wall". Show robot-detected hazards and the robot's live position as **world-locked markers in the real scene** — an "X-ray" of what the scout found.
- **Hardware:** Air 2 Ultra (anchors, image tracking, hand tracking) on Beam Pro, or AURA if on site. Scout robot with localisation (quadruped with LiDAR). SKYLANDX MetaCam for a venue point cloud. Printed fiducial markers.
- **Architecture / stack:**
  - Mapping: MetaCam scan or the robot's SLAM map defines the world frame.
  - Alignment: fix a printed image marker at a surveyed pose in that map; the glasses detect it (image tracking) → compute map-to-glasses transform → create a spatial anchor so alignment survives when the marker leaves view.
  - Perception / planning: robot patrols, detects hazards, publishes poses in the map frame.
  - Display: Unity app subscribes (ROS-TCP-Connector / WebSocket) and renders hazard pins, robot ghost and safe-route line in place. Hand pinch or phone controller to acknowledge a hazard or send the robot to a point.
- **48-hour plan:**
  - H0–6: confirm device availability; run Spatial Anchor and Image Tracking samples; robot team gets a map and pose stream.
  - H6–24: marker-based alignment; show a robot "ghost" that matches the real robot in line of sight (this is the acceptance test).
  - H24–40: hazard pins, occluded-robot view, point-to-send command; drift re-alignment on marker re-sighting.
  - H40–48: rehearse; record a through-the-lens capture (Air 2 Ultra records virtual content only — film a composite or mirror the app view).
- **3-minute demo script:** (0:00) responder at the door of an "unsafe building". (0:30) looks at the marker; the scene aligns. (1:00) robot disappears behind a partition — its ghost stays visible. (1:45) robot flags a "gas leak"; a pin appears through the wall; responder pinches to dispatch the robot to a second room. (2:30) show the same pins in the 3D twin on the command screen.
- **Risks and fallbacks:** alignment drift or poor tracking in low-texture / dim spaces → more markers, small demo area. Air 2 Ultra or AURA not on site → concept is not feasible on One + Eye; drop to Concept 3. AURA needs a separate Android XR project (Unity 6) — do not switch stacks mid-hackathon.
- **Judging angles:** innovation high; technical depth high (multi-frame registration, shared spatial state); impact credible for search and inspection; Leukerbad relevance: locating people or leaks inside buildings and galleries after an avalanche or rockfall.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| XREAL (display only) + any quadruped (Unitree, AGIBOT D1, Magiclab, Genisom) | Hands-free scout console (Concept 1) | **Low** — external monitor |
| XREAL One + Eye + humanoid head or arm-mounted camera (Unitree, Dobot, Flexiv) | Head-driven remote inspection (Concept 2) | **Medium** — Unity app + pose bridge + video return |
| XREAL One + Eye + quadruped + Windows command laptop | Responder ↔ command ↔ robot link (Concept 3) | **Medium** — SDK sample + relay server |
| XREAL Air 2 Ultra / AURA + SKYLANDX MetaCam + quadruped | World-anchored hazard twin (Concept 4) | **High** — frame alignment across three systems |
| XREAL + D-Robotics RDK | On-robot detection and video encoding feeding the HUD | **Low–Medium** — standard edge-AI pipeline |
| XREAL + OriginFlow (EMG) | Hands-busy command input (muscle gesture) alongside the HUD | **High** — two novel input stacks; ⚠️ check OriginFlow's real-time API |
| XREAL + XR-teleop of a mobile manipulator (Galaxea, Galbot, AGIBOT G1) | Remote valve / switch operation in a hazard zone | **High** — community XR-teleop stacks target Quest / Pico, not XREAL |

## Questions to ask the XREAL engineers on site

1. Which glasses, how many XREAL Eye modules, and which host devices (Beam Pro / Samsung) can a team borrow — and for how long?
2. Are Air 2 Ultra or AURA units here? If AURA: is app camera access enabled, and is there a ready Unity 6 project?
3. Does 1 Pro+ work with XREAL Eye and SDK 3.1.0 for 6DoF, or only One / One Pro / 1S?
4. Eye RGB frames: what resolution, frame rate and latency do apps get, and can we get camera intrinsics?
5. Can a laptop (Windows / Linux / macOS) read head pose from the glasses over USB, or is pose only available inside the Android SDK?
6. What protocol does First Person View streaming use — can we receive it in our own app (e.g. OpenCV / GStreamer) instead of StreamingReceiver.exe?
7. Is the XREAL Marker / image-tracking sample usable on One + Eye, or strictly Air 2 Ultra?
8. Any ruggedness data — operating temperature, moisture, use with a helmet — and a recommended way to power glasses + host for a multi-hour field session?

## Decision rule

- **Pick XREAL for T02 if** your team already has (or is building) a working robot pipeline on another vendor's platform and wants a hands-free operator or responder interface — and you can either live with display-only use or have one person fluent in Unity + Android.
- **Avoid if** you need XREAL to be the system that senses or acts, you need rugged field hardware claims, or your concept depends on anchors / hand tracking and only One-series glasses are available.

## Sources

- [XREAL company profile (this repo)](../XREAL.md)
- [XREAL docs — SDK overview (3.1.0)](https://docs.xreal.com/)
- [XREAL docs — Compatibility](https://docs.xreal.com/XREALDevices/Compatibility)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XREAL docs — First Person View](https://docs.xreal.com/Tools/First%20Person%20View)
- [XREAL docs — Sample Code](https://docs.xreal.com/Sample%20Code)
- [Android Developers — Develop with Unity for Android XR](https://developer.android.com/develop/xr/unity)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/abs/2604.08534)
