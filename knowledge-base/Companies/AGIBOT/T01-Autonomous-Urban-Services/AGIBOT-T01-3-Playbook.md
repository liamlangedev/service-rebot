---
type: challenge-playbook
company: "AGIBOT"
slug: AGIBOT
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# AGIBOT × T01 — Hackathon Playbook

⬆ [AGIBOT profile](../AGIBOT.md) · [Brief](AGIBOT-T01-1-Brief.md) · [Products and solutions](AGIBOT-T01-2-Products-and-Solutions.md)

**Before choosing a concept (first 30 minutes):** ask the AGIBOT booth which units are available to teams, which X2 variant (Ultra or Edu), the firmware / SDK version, and whether the X2 navigation module is enabled. The concepts below are ordered from safest to most ambitious and state which answer each one depends on.

| Concept | Robot | Depends on | Risk |
|---|---|---|---|
| 1 Resort concierge | X2 (any variant) | SDK access, Wi-Fi | Low |
| 2 Stair-and-slope courier | D1 Ultra / Edu | D1 unit + your own sensor | Medium |
| 3 Guide-and-escort | X2 Ultra | navigation module enabled | Medium–high |
| 4 Micro-store relay | G2 + D1 + X2 | AGIBOT staff + Genie Studio | High |

## Solution approaches

### Concept 1 — Resort concierge (X2)
- **Problem → value:** Leukerbad's guests are multilingual and often elderly; information desks close early. A small humanoid at a hotel lobby, bath entrance or bus terminal answers "where / when / how" questions, points the way and hands the guest a route on their phone.
- **Hardware:** X2 Ultra or X2 Edu. Optional: **XREAL** glasses showing the route to the guest; **D-Robotics** RDK X5 as a side computer for speech and vision if the laptop is busy.
- **Architecture / stack:**
  - Perception: SDK microphone stream → speech-to-text (cloud or local Whisper-class model on a laptop); optional person detection from your own camera (the X2 vision interface is marked "to be enabled").
  - Planning: LLM with function calling over a small Leukerbad knowledge base (baths, clinics, bus and cable-car times, avalanche / weather notice). Template: AGIBOT's public AgentSDK hospital-triage sample (intent routing, knowledge base, whitelisted gestures, English locale) — needs AGIBOT platform credentials; otherwise re-implement the same pattern with plain AimDK calls.
  - Control: AimDK_X2 ROS 2 services — TTS, preset motions (wave, point), screen / emoji, short velocity-command moves. Disable the built-in interaction system to use your own voice stack.
  - Compute: laptop on the robot's network (external-PC mode); on-board container on Ultra if allowed.
- **48-hour plan:**
  - H0–6: confirm SDK / firmware match, run the TTS, microphone and preset-motion examples; draft the knowledge base (German, French, English).
  - H6–24: voice loop end to end; function calls for gestures and "turn toward destination"; QR code on the face screen or phone hand-off.
  - H24–40: noise robustness (push-to-talk or head-touch trigger), language switching, timeouts, a "call a human" escalation.
  - H40–48: freeze features, rehearse, record a backup video.
- **3-minute demo script:** guest touches the robot's head → asks in German where the nearest thermal bath is and whether it is step-free → robot answers, points, shows a QR route → second guest asks in English about the last bus to Leuk → robot answers and flags an out-of-scope medical question to staff.
- **Risks and fallbacks:** noisy hall → push-to-talk and a directional USB microphone; no AgentSDK credentials → own LLM + AimDK TTS; Wi-Fi drops → local speech model and cached answers.
- **Judging angles:** impact and Leukerbad relevance are strong (tourism, accessibility, multilingual); technical depth is moderate — add grounding in live timetable / weather data to raise it.

### Concept 2 — Stair-and-slope courier (D1 Ultra)
- **Problem → value:** short deliveries between pharmacy, clinic, hotel and bath involve stairs, ramps and wet or snowy ground where wheeled delivery robots fail. A **5 kg**-payload quadruped (IP54, **40°** slopes, **16 cm** stairs) carries medicine, towels or a meal the last few hundred metres.
- **Hardware:** D1 Ultra or D1 Edu with a lightweight cargo box. Add-on brain: **D-Robotics** RDK X5 + depth camera (or a laptop-class board) on the Ethernet / USB port. Optional: **SKYLANDX** MetaCam to pre-scan the route.
- **Architecture / stack:**
  - Perception: your own sensor — AprilTag / fiducial waypoints plus depth-based obstacle stop; or person-following from the depth camera. The D1 SDK itself provides only IMU and joint states.
  - Planning: waypoint state machine (pickup → route → drop-off → return); simple order app or chat interface.
  - Control: D1 SDK `move(vx, vy, yaw_rate)` from Python / C++; the built-in RL gait handles terrain.
  - Compute: edge board on the robot's back; operator tablet for orders and e-stop.
- **48-hour plan:**
  - H0–6: SDK connected, velocity commands from your board, cargo box mounted, e-stop procedure agreed with staff.
  - H6–24: tag-to-tag navigation on flat floor; obstacle stop; order app.
  - H24–40: stairs and a ramp segment; delivery confirmation (QR or PIN on phone); payload tests up to 5 kg.
  - H40–48: reliability runs, battery plan, backup video outdoors.
- **3-minute demo script:** "pharmacy" operator loads a medicine bag and taps the destination → dog walks the route including a stair flight → stops for a person crossing → recipient confirms with a QR code → dog returns.
- **Risks and fallbacks:** autonomous stairs unreliable → follow-me mode behind a staff member (the robot still does the carrying); localization drift → denser tags; unit unavailable → same stack on a **Unitree** Go2 or **Genisom** quadruped.
- **Judging angles:** highest Leukerbad relevance of the four (steep terrain, elderly guests, clinics); technical depth comes from the perception and navigation you add; be honest that winter operation is untested.

### Concept 3 — Guide-and-escort (X2 Ultra with navigation)
- **Problem → value:** in a large bath or clinic complex guests get lost. The robot does not only explain the way — it walks the guest there, at their pace, then returns to its post. Mirrors AGIBOT's real guiding deployments (Guangzhou Metro, Chimelong, WAIC 2026).
- **Hardware:** X2 Ultra with the perception module enabled (not available on X2 Edu). Optional: **SKYLANDX** MetaCam scan as a reference floor plan; **XREAL** glasses for a staff supervisor view.
- **Architecture / stack:**
  - Perception: on-board LiDAR + RGB-D through AimDK; SLAM interface for map building, map retrieval and relocalization.
  - Planning: Concept 1's dialogue layer resolves a spoken destination to a map coordinate and publishes a navigation task; pace control by checking that the guest is still behind (rear camera or a simple distance check).
  - Control: AimDK navigation task topic; TTS announcements at turns; fallback to velocity commands.
  - Compute: on-board container (Ultra) plus laptop for the LLM.
- **48-hour plan:**
  - H0–6: get the navigation module unlocked; build one map; send one goal from the Python example.
  - H6–24: named places table; voice → goal; return-to-post; relocalization routine.
  - H24–40: guest-pace logic, blocked-path handling, multi-stop tours.
  - H40–48: tune on the demo floor, rehearse, backup video.
- **3-minute demo script:** guest asks for "physiotherapy room 2" → robot confirms, says "follow me", walks the route, pauses when the guest stops, announces arrival → navigates back alone.
- **Risks and fallbacks:** module not enabled or map unstable → drop to Concept 1 plus a scripted waypoint walk; crowds at the venue → short fenced route; humanoid walking speed and battery life are unverified, so keep the route under about 30 m.
- **Judging angles:** technical depth (speech-to-navigation on a biped) and a clear link to proven deployments; innovation comes from the pace-adaptive escort for elderly guests.

### Concept 4 — Micro-store relay (G2 + D1 + X2)
- **Problem → value:** a village shop or hotel kiosk that keeps serving off-hours. A guest orders by voice or phone; a wheeled dual-arm robot picks the item; a quadruped carries it to the room or chalet door. A small-scale version of AGIBOT's six-robot convenience-store trial (1,730 tasks in 24 h, November 2026).
- **Hardware:** G2 (picker), D1 Ultra (courier), X2 (front desk, optional). Optional: **WUJI** hand or OmniPicker for grasping; **Flexiv** or **ROKAE** arm as a substitute picker if no G2 is available to teams.
- **Architecture / stack:**
  - Perception: G2 head / wrist cameras for item recognition on a small shelf (3–5 items).
  - Planning: your own lightweight orchestrator (order queue, task states, retries) — an imitation of AGIBOT's non-public Genie Master idea.
  - Control: G2 pick-and-place via Genie Studio (teleoperation demos → GO-model fine-tune) or, if that is too slow, scripted grasps taught by AGIBOT staff; hand-over into the D1 cargo box; D1 runs Concept 2's stack.
  - Compute: Genie Studio / AGIBOT workstation for the G2; edge board on the D1; laptop for orchestration.
- **48-hour plan:**
  - H0–6: confirm G2 and Genie Studio access; decide pick method; start Concept 2 in parallel.
  - H6–24: one reliable pick of one item into the box; D1 tag route working.
  - H24–40: three items, order app, hand-over alignment (dog parks at a fixed tag), retries.
  - H40–48: end-to-end runs, measure success rate, backup video.
- **3-minute demo script:** guest orders "sunscreen and a water bottle" → G2 picks both and places them in the dog's box → dog walks to the "room door" and waits for QR confirmation → dashboard shows tasks completed and autonomous minutes (a nod to AGIBOT's "Worken" metric).
- **Risks and fallbacks:** policy training does not converge → teleoperated pick with autonomous delivery, stated openly; no G2 for teams → cobot arm from another vendor; hand-over misalignment → funnel-shaped box.
- **Judging angles:** strongest on innovation and technical depth (multi-robot, manipulation + locomotion); real-world impact is credible given the Shanghai trial; highest execution risk.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| X2 + D-Robotics RDK X5 | Own camera / speech pipeline when the X2 vision interface is unavailable | Low — ROS 2 on both sides |
| D1 Ultra + D-Robotics RDK X5 + depth camera | Tag or person-following navigation on a velocity-only quadruped | Medium — mounting, power, calibration |
| X2 Ultra or D1 + SKYLANDX MetaCam | Fast 3D scan of the venue as a reference map or digital twin | Medium — map format conversion is not guaranteed |
| X2 + XREAL glasses | AR route for the guest or a supervisor view of robot state | Low–medium — Android app talking to your ROS bridge |
| D1 Ultra + Unitree Go2 / B2 | Mixed courier fleet behind one dispatcher; heavier loads on the B2 | Medium — two SDKs, one waypoint layer |
| G2 or other arm + WUJI Hand / OmniPicker | More reliable grasping of small retail items | Medium–high — end-effector mounting and drivers |
| Any AGIBOT robot + Binabik AI agent OS | Higher-level task orchestration across robots | Unknown — depends on Binabik's adapters |

## Questions to ask the AGIBOT engineers on site
1. Which robots can teams actually program this weekend, and how many units of each?
2. Is the X2 here an Ultra, Ultra (new version) or Edu, and which firmware / AimDK version is installed?
3. Can you enable the X2 SLAM / navigation module for us, and does it work on this venue's floor and crowd level?
4. Is the X2 camera stream accessible now, given the vision interface is marked "to be enabled"?
5. Can we get AgentSDK / LinkSoul credentials (App ID, key, agent code) and the `linksoul-agentsdk` package for the weekend? Which languages does the built-in speech stack support?
6. For the D1: what is the real battery runtime with a 5 kg load, may we walk it outdoors in the cold and wet, and is there any follow or navigation add-on?
7. Is a G2 with Genie Studio available, and how long does a typical pick task take from teleop data to a deployed policy?
8. What are the safety rules: e-stop, tethering, maximum speed, who must be present when the robot moves?

## Decision rule
- **Pick AGIBOT for T01 if** your idea is an indoor guide, concierge or greeter (X2), or a small courier that must handle stairs and slopes (D1) — and the booth confirms the unit, firmware and, for escorting, the navigation module.
- **Avoid if** you need turnkey autonomous outdoor navigation, payloads above 5 kg, a programmable cleaning robot, or cannot get staff support for the G-series.

## Sources
- [AGIBOT — Six G2 robots complete 1,730 tasks in 24-hour convenience-store trial (2026-11-06)](https://www.agibot.com/article/231/detail/134.html)
- [AGIBOT — Worken introduced at AGIBOT Innovation Day 2026 (2026-10-28)](https://www.agibot.com/article/231/detail/131.html)
- [PR Newswire via AAP — Four new products at WAIC 2026 (2026-07-20)](https://www.aap.com.au/aapreleases/cision20260719ae07639/)
- [AimDK_X2 documentation](https://x2-aimdk.agibot.com/en/latest/)
- [AimDK_X2 — Perception module (optional)](https://x2-aimdk.agibot.com/en/latest/Interface/perception/index.html)
- [AGIBOT — D1 Ultra product page](https://www.agibot.com/products/D1Ultra)
- [GitHub — AgibotTech/agibot_D1_Edu-Ultra](https://github.com/AgibotTech/agibot_D1_Edu-Ultra)
- [GitHub — AgibotTech/agibot_agentsdk_sample_code](https://github.com/AgibotTech/agibot_agentsdk_sample_code)
- [GitHub — AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)
- [AGIBOT — G2 product page](https://www.agibot.com/products/G2)
- [AGIBOT company profile (this repo)](../AGIBOT.md)
