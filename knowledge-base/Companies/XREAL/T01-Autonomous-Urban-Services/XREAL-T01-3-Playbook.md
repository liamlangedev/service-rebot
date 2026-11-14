---
type: challenge-playbook
company: "XREAL"
slug: XREAL
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# XREAL × T01 — Hackathon Playbook

⬆ [XREAL profile](../XREAL.md) · [Brief](XREAL-T01-1-Brief.md) · [Products and solutions](XREAL-T01-2-Products-and-Solutions.md)

**Read first:** XREAL is an add-on. Every concept below needs a robot from another vendor; the glasses provide the human-in-the-loop layer. Statements about other vendors' robots are indicative — check their own profiles. Confirm at the XREAL booth which glasses and hosts are actually available before choosing a concept.

## Solution approaches

### Concept 1 — Walk-along supervisor HUD (no SDK)
- **Problem → value:** A delivery / luggage robot in a pedestrian village still needs a human minder. Today that person stares at a tablet. A HUD keeps eyes on the street and hands free → one minder can safely escort or supervise.
- **Hardware:** One Pro or 1 Pro+ (outdoor: 1 Pro+) as USB-C display on a laptop in a backpack or a DP-capable phone. Robot: e.g. Unitree Go2 / B2 or a wheeled service robot (Galaxea, Galbot, UniX AI).
- **Architecture / stack:** Robot runs its own navigation (vendor stack / ROS 2 Nav2) → publishes camera, pose, battery, mission state → a web dashboard (or Foxglove / RViz layout) on the host → mirrored into the glasses. Input by gamepad or phone. All compute on robot + host; glasses are a monitor.
- **48-hour plan:**
  - H0–6: get glasses showing a laptop screen; get robot video + pose onto the network.
  - H6–24: build one high-contrast dashboard (video, mini-map, next waypoint, E-stop state); robot runs a fixed A → B delivery route.
  - H24–40: add takeover: gamepad teleop when the robot reports "blocked"; alert banner in HUD.
  - H40–48: rehearse route, record backup video.
- **3-minute demo script:** (1) Robot starts hotel → clinic delivery autonomously; operator walks beside it wearing glasses. (2) An obstacle blocks the path; HUD flashes "blocked", operator takes over by gamepad without looking down. (3) Robot resumes autonomy and hands over the parcel; show the HUD view on the projector.
- **Risks and fallbacks:** Host port lacks DP Alt Mode → use a phone / laptop that has it or an HDMI adapter ⚠️ check. Glare outdoors → demo indoors or in shade. Fallback: same dashboard on a tablet.
- **Judging angles:** Innovation low–medium · technical depth sits in the robot · impact: realistic operations model (supervised autonomy) · Leukerbad: car-light village, luggage and spa-supply runs between hotels and clinics.

### Concept 2 — Head-steered remote takeover
- **Problem → value:** When an autonomous robot gets stuck, a remote operator needs fast situational awareness. Turning the head to look around is quicker than joystick camera control → shorter recovery time per incident.
- **Hardware:** One series + XREAL Eye + Beam Pro (6DoF), or plain One series (3DoF head rotation is enough). Robot with a pan-tilt camera, a 360° camera, or a quadruped whose body yaw / pitch can follow the head.
- **Architecture / stack:** Unity app (XREAL SDK 3.1.0) on Beam Pro reads head pose → sends yaw / pitch at 30–60 Hz over UDP / WebSocket (or ROS-TCP-Connector) → robot-side node maps it to the camera gimbal or body orientation → low-latency video (WebRTC / MJPEG) back to a quad in the Unity scene. Driving via phone-as-controller or gamepad. Autonomy stays on the robot.
- **48-hour plan:**
  - H0–6: build and deploy the SDK `HelloMR` sample; print head pose; confirm host + glasses combo.
  - H6–24: pose stream to a robot-side script; video stream into Unity; measure glass-to-glass latency.
  - H24–40: integrate with the robot's "need help" state; add reticle, latency and battery indicators.
  - H40–48: tune smoothing / dead-zones; rehearse.
- **3-minute demo script:** (1) Operator sits out of sight of the robot. (2) Robot on a service route stops at an ambiguous obstacle and calls for help. (3) Operator looks left / right — robot camera follows — picks a gap, drives through, releases control.
- **Risks and fallbacks:** Latency over venue Wi-Fi → bring your own router, lower resolution. Unity ↔ ROS friction → plain JSON over WebSocket. No Eye available → 3DoF rotation only (fine for this concept).
- **Judging angles:** Innovation medium · technical depth: real-time loop, latency budget · impact: remote-ops cost per robot · Leukerbad: one operator at the tourist office covering robots across steep, snowy lanes.

### Concept 3 — "Look and dispatch" for municipal maintenance
- **Problem → value:** Faults in public space (overflowing bin, ice patch, blocked path, spill in a spa corridor) are noticed by staff on foot but reported late. Worker looks at the issue, says / clicks "report" → a robot is dispatched to handle or cordon it.
- **Hardware:** One series + **XREAL Eye** + Beam Pro (RGB frames are confirmed accessible on this combo). Robot: quadruped or wheeled manipulator for the response. Optional: D-Robotics RDK board for on-robot perception; SKYLANDX scan as the shared site map.
- **Architecture / stack:** Unity app grabs Eye frame (YUV → JPEG) + 6DoF pose on trigger → HTTP to a laptop service → VLM / detector classifies the issue and writes a task (type, photo, location) → task queue → robot navigates to the location and performs a simple action (stand guard with warning light, photograph, pick up item). Location: nearest named waypoint chosen by the worker in the HUD list, or a fiducial at the site — do **not** rely on glasses pose for town-scale coordinates. Result and robot ETA shown back in the HUD.
- **48-hour plan:**
  - H0–6: run `RGBCameraAndCapture` sample; save one frame; choose 3 issue types and 4 waypoints.
  - H6–24: frame upload + VLM classification; task queue; robot goes to named waypoints.
  - H24–40: HUD feedback (task accepted, ETA, done photo); one robot response behaviour per issue type.
  - H40–48: end-to-end runs, failure handling, backup video.
- **3-minute demo script:** (1) Worker walks past a tipped bin, looks at it, taps the phone controller. (2) Screen shows classification "waste overflow, waypoint 3"; robot leaves its dock. (3) Robot arrives, performs the response; HUD shows "resolved" with the robot's photo.
- **Risks and fallbacks:** Camera access or resolution weaker than expected → use the Beam Pro's own camera for the photo. VLM latency → small fixed-class detector. Robot navigation unreliable → shorten the route, pre-map.
- **Judging angles:** Innovation medium–high (human perception + robot action) · technical depth: full perception → task → navigation loop · impact: faster municipal response with existing staff · Leukerbad: ice and snow hazards on walkways used by elderly spa guests.

### Concept 4 — Shared-space AR: see the robot's intent (most ambitious)
- **Problem → value:** People distrust service robots in crowded pedestrian areas because they cannot tell where the robot will go. Staff with glasses see the robot's planned path, drop-off point and stop zone drawn in the real corridor → smoother shared use of space and faster handovers.
- **Hardware:** **Air 2 Ultra** (image tracking + anchors) or **AURA** (Android XR) — One + Eye cannot do this. Robot with a known planner output (Nav2 path). Printed image marker on the robot or at its dock.
- **Architecture / stack:** Glasses detect the marker (SDK `BasicImageTracking` / experimental `MarkerTracking`) → compute the transform glasses-frame ↔ robot map frame → subscribe to path and goal topics → render path ribbon and goal disc in Unity. Re-localise each time the marker is seen; keep overlays within a few metres of the marker (docs advise ≤3 m from an anchor).
- **48-hour plan:**
  - H0–6: confirm device availability; run image-tracking sample; static cube locked to marker.
  - H6–24: frame alignment maths; stream the robot path; draw it.
  - H24–40: goal editing by gaze + phone controller (or hand pinch on Air 2 Ultra); send new goal to the robot.
  - H40–48: stabilise drift, rehearse in the exact demo spot and lighting.
- **3-minute demo script:** (1) Concierge wearing glasses sees a glowing path from the robot to room door B. (2) Guest changes the request; concierge drags the goal disc to a new spot; robot replans and the path updates live. (3) Robot arrives exactly on the disc.
- **Risks and fallbacks:** Hardware not on site → drop to Concept 2. Drift / misalignment → marker on the robot, short distances, indoor only. Fallback: show the same path on a top-down map in the HUD (Concept 1).
- **Judging angles:** Innovation high · technical depth: co-localisation, bidirectional control · impact: human–robot trust in public space · Leukerbad: hotel and clinic corridors with slow-moving guests.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| XREAL One series + Unitree Go2 / B2 | Supervised delivery on steep or snowy paths with HUD and head-steered camera | Medium — video + pose stream, vendor SDK details per Unitree profile |
| XREAL + Galaxea / Galbot / UniX AI wheeled manipulators | Hotel / clinic concierge robot with staff HUD for handover and takeover | Medium — depends on the robot's exposed topics |
| XREAL Eye + D-Robotics RDK | Glasses frames or robot frames processed at the edge instead of a laptop | Medium — network + model deployment |
| XREAL + SKYLANDX MetaCam | Pre-scanned 3D map of the venue as the mini-map / shared waypoint frame | Low–medium — export map, render top-down |
| XREAL (Air 2 Ultra / AURA) + any Nav2 robot | Path and goal overlays in the real space (Concept 4) | High — co-localisation and device availability |
| XREAL + Binabik AI / Genisom agent stacks | Natural-language tasking of the robot with HUD confirmation | Unknown — APIs not verified |

## Questions to ask the XREAL engineers on site
1. Which glasses, how many XREAL Eye modules and which hosts (Beam Pro, Samsung S24 / S25) can teams borrow — and are any Air 2 Ultra or AURA units here?
2. Does 1 Pro+ work with XREAL Eye and SDK 3.1.0 for 6DoF, or only One / One Pro / 1S?
3. What resolution and frame rate do Eye RGB frames reach inside a Unity app, and can they be streamed while 6DoF tracking runs?
4. Is there a ready sample for sending head pose over the network (UDP / WebSocket / ROS)? Any internal ROS 2 bridge?
5. How does 6DoF tracking behave outdoors — snow, low texture, bright light, walking 50+ m?
6. Can the glasses run from a Linux laptop or a robot dev board as a plain display (DP Alt Mode / HDMI adapter), and is head pose readable on Linux without the Android SDK?
7. Is `FirstPersonViewStreamingCast` usable for low-latency remote viewing, and over which protocol?
8. Is a newer SDK than 3.1.0 or an on-site build available, and which Android versions must be avoided?

## Decision rule
- **Pick XREAL for T01 if** you already have a robot team-mate / vendor for mobility and autonomy and want a credible supervised-autonomy or remote-takeover story with a wearable HUD — starting with the display-only path and adding head pose or Eye camera only if time allows.
- **Avoid if** you expected a robot platform, need world-anchored AR but only One-series glasses are on site, or nobody on the team can build a Unity Android app and you want more than a screen.

## Sources
- [XREAL developer docs — overview (SDK 3.1.0)](https://docs.xreal.com/)
- [XREAL docs — Compatibility (feature matrix, supported phones)](https://docs.xreal.com/XREALDevices/Compatibility)
- [XREAL docs — XREAL Glasses (device table)](https://docs.xreal.com/XREALDevices/XREAL%20Glasses)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XREAL docs — Sample Code](https://docs.xreal.com/Sample%20Code)
- [XREAL docs — Spatial Anchor intro](https://docs.xreal.com/Spatial%20Anchor/intro)
- [Android Developers — Develop with Unity for Android XR](https://developer.android.com/develop/xr/unity)
- [Unity-Technologies / ROS-TCP-Connector (GitHub)](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [XREAL company profile (internal)](../XREAL.md)
