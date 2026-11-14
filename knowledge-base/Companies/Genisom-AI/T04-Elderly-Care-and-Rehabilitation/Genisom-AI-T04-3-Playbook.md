---
type: challenge-playbook
company: "Genisom AI"
slug: Genisom-AI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Genisom AI × T04 — Hackathon Playbook

⬆ [Genisom AI profile](../Genisom-AI.md) · [Brief](Genisom-AI-T04-1-Brief.md) · [Products and solutions](Genisom-AI-T04-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- The robot never touches or supports the person. Keep at least 1 m distance, walking speed or slower, one teammate on the stop control.
- On-site models are not confirmed. Each concept names a preferred robot and a fallback that works on an **L1 EDU** (the most likely unit).
- SDKs are **C++ only**. Fastest pattern: a small C++ bridge that takes velocity commands over a local socket, with perception and logic in Python on a laptop or the Orin NX.
- Whether built-in following and voice can be triggered from the SDK is ⚠️ unverified. Ask first (see questions below); otherwise write your own.

## Solution approaches

### Concept 1 — Night-round fall sentinel
- **Problem → value:** Night staff in clinics and care homes cannot watch every corridor. A robot walks the round, finds a person on the floor or out of bed, and alerts a caregiver with a photo and location. Fewer long lies after falls.
- **Hardware:** L1 EDU (indoor) or L2. Optional: D-Robotics RDK X5 as a second vision computer; XREAL glasses for the caregiver's alert view; SKYLANDX MetaCam to scan the corridor map quickly.
- **Architecture / stack:** Camera + LiDAR → open pose-estimation model (lying-posture and no-motion rule) on Orin NX or laptop → patrol waypoints via RoamerX Lite (ROS 2 Humble / Nav2) or a simple scripted route with SDK velocity commands → alert service (web dashboard or phone message) with snapshot and map position → two-way audio through a USB speaker-microphone.
- **48-hour plan:**
  - H0–6: confirm robot, connect SDK, stand and walk; get the camera stream onto the laptop.
  - H6–24: pose model + "person on floor" rule; scripted or Nav2 corridor route; alert dashboard.
  - H24–40: integrate, approach-and-stop behaviour at a safe distance, voice check-in ("Are you OK?"), false-alarm tests (person sitting, bending, lying on a sofa).
  - H40–48: rehearse, record a backup video, polish the dashboard.
- **3-minute demo script:** Robot starts its round → teammate lies on the floor → robot stops 1.5 m away, asks if help is needed → no answer → caregiver's phone or glasses show photo, room label and live video → caregiver speaks through the robot → robot resumes its round.
- **Risks and fallbacks:** Navigation not ready → teleoperate the route, keep detection autonomous. Camera stream not accessible → mount a USB camera on the open USB port. False positives → require 5 s without motion.
- **Judging angles:** Impact — clear and measurable (time to detection). Technical depth — perception + navigation + alert loop. Leukerbad — rehab clinics and hotels with elderly guests. Innovation — moderate; privacy-friendly variant (pose skeleton only, no stored video) lifts it.

### Concept 2 — Follow-and-carry walking companion
- **Problem → value:** Guests with a walker or crutches cannot carry a bag, towel or oxygen bottle between clinic, hotel and thermal bath. The robot follows hands-free and carries up to **16 kg** (L2) or **8 kg** (L1).
- **Hardware:** L2 (GLUE UWB + vision following) or M1 Pro (voice + following). Fallback: L1 EDU with your own follower. Optional: OriginFlow EMG band for a "stop / come" gesture; a simple basket on the payload rails.
- **Architecture / stack:** Built-in following if the booth can enable it; otherwise depth camera or LiDAR → person tracker → distance-keeping controller → SDK velocity commands. Add rules: stop when the person stops, wait at stairs, speak a warning when the gap grows. Voice commands via a laptop speech model and USB speaker-microphone.
- **48-hour plan:**
  - H0–6: test built-in following; if unavailable, start own tracker.
  - H6–24: stable following at slow walking pace; stop / wait / come commands; basket mount.
  - H24–40: trials with a walker on a ramp and a few stairs; lost-person recovery (robot stops and calls out).
  - H40–48: rehearse route, backup video.
- **3-minute demo script:** Teammate with a walker puts a bag in the basket → says "follow me" → walks through a doorway and up a ramp, robot keeps 1.5 m behind → person stops to rest, robot sits or stands by → "go back to reception" sends it home (teleoperated if navigation is not ready).
- **Risks and fallbacks:** Robot loses the person in a crowd → UWB tag or a coloured vest. Trip hazard → robot follows behind and to the side, never in front. Outdoor cold → L1 is rated 0–40 °C; stay indoors with it.
- **Judging angles:** Leukerbad relevance — very high (steep paths, snow, bath visits). Impact — independence for mobility-impaired guests. Technical depth — moderate if the built-in feature is used; say so honestly.

### Concept 3 — Rehab walk pacer and logger
- **Problem → value:** Walking tests and gait training in rehabilitation need a therapist to pace, time and measure. A robot that walks ahead or beside at a prescribed speed, adapts when the patient falls behind, and logs distance, speed and rest stops frees therapist time and gives objective progress data.
- **Hardware:** M1 or L2 outdoors; L1 EDU in a corridor. Optional: XREAL glasses showing pace and distance to the patient; OriginFlow EMG for muscle-activity data alongside the walk log.
- **Architecture / stack:** Odometry (SDK) for distance and speed → LiDAR or depth camera measures the gap to the patient → pace controller (target speed, slow down if gap grows, stop if patient stops) → session log and therapist dashboard with speed curve, rests and total distance → spoken encouragement at set intervals.
- **48-hour plan:**
  - H0–6: read odometry, validate distance against a measured 20 m course.
  - H6–24: gap measurement and adaptive pace controller; session logger.
  - H24–40: timed-walk protocol (for example a six-minute walk on a marked course), dashboard, voice prompts.
  - H40–48: accuracy numbers for the pitch, rehearsal.
- **3-minute demo script:** Therapist sets "0.8 m/s for 2 minutes" on a tablet → robot paces a patient along a corridor → patient slows, robot slows and says so → at the end the dashboard shows distance, average speed and a comparison with the last session.
- **Risks and fallbacks:** Odometry drift on legs → correct with LiDAR or floor markers; report measured error. Patient tracking unreliable → fixed pace mode plus a manual lap button.
- **Judging angles:** Proof point — the M1 already paced a half marathon by following. Impact — measurable outcome data for clinics. Innovation — robot as an objective rehab instrument, not a gadget. Not a medical device; present it as a research prototype.

### Concept 4 — Voice-directed guide dog for low-vision seniors
- **Problem → value:** Older guests with poor eyesight struggle with unfamiliar hotel and clinic layouts. The robot takes a spoken destination ("take me to the pool entrance"), leads the way, and announces doors, stairs and obstacles. Matches Genisom's own "Smart Guide Dog" application cases.
- **Hardware:** L2 or L1 EDU. Optional: a light tether or soft handle with a slack sensor (no rigid load on the person); SKYLANDX MetaCam for the building map; D-Robotics board for obstacle classification.
- **Architecture / stack:** Speech → LLM maps the request to a named place on the map → RoamerX Lite goal → robot speed tied to the user's pace (tether slack or rear distance) → vision model announces hazards. Stretch: `genisom_vln` for open-vocabulary goals such as "find a free chair" (documented for the MATRiX simulator; real-robot use not documented, needs a strong GPU or a cloud model).
- **48-hour plan:**
  - H0–6: map one floor, confirm goal navigation works on the real robot.
  - H6–24: speech-to-destination, pace matching, hazard announcements.
  - H24–40: blindfolded-teammate trials with a sighted spotter; stairs handled by stopping and announcing, not climbing with the user.
  - H40–48: rehearsal, backup video, safety narrative.
- **3-minute demo script:** Blindfolded teammate says the destination → robot confirms and leads → pauses at a door and announces it → detours around a chair → stops at stairs and offers the lift route → arrives and says so.
- **Risks and fallbacks:** Highest technical and safety risk. Navigation fails → pre-recorded route with live hazard announcements. Tether tangles → use distance-based pacing only. Always a spotter beside the user.
- **Judging angles:** Innovation and impact — high. Technical depth — full speech + navigation + perception loop. Leukerbad — tourists in unfamiliar buildings. Be explicit that this is a concept demo, far from a certified mobility aid.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Genisom quadruped + D-Robotics RDK X5 | Extra on-robot vision (pose, fall, obstacle classes) on the open USB / Ethernet ports | Low |
| Genisom quadruped + XREAL glasses | Caregiver or therapist sees alerts, live video or pace data hands-free | Low to medium |
| Genisom quadruped + OriginFlow EMG | Gesture or muscle-signal commands ("stop", "come"); muscle data alongside walk logs | Medium |
| Genisom quadruped + SKYLANDX MetaCam | Fast 3D scan of the venue to seed the navigation map | Medium (map format conversion ⚠️ unverified) |
| Genisom quadruped + Galaxea / Galbot / UniX AI mobile manipulator | Arm robot picks and loads items; dog carries them over stairs and outdoors | High (two stacks, hand-over station) |
| Genisom quadruped + Flexiv or ROKAE arm (fixed rehab station) | Arm does force-controlled therapy; dog handles escort and logistics | High; two separate demos unless tightly scripted |

## Questions to ask the Genisom AI engineers on site
1. Which models are here, how many, and is the EDU sensor kit (Orin NX, LiDAR, depth camera) fitted?
2. Can person-following (GLUE on L2, UWB on M1 Pro) be started, stopped and monitored from the SDK, or only from the app?
3. Is there a speaker and microphone on the unit, and an API for voice output? If not, which USB port can power an audio device?
4. How do we get the camera and LiDAR streams — SDK call, ROS 2 topic or RTSP — and at what rate?
5. Is the full RoamerX installed, and can we send "go to pose" goals and get arrival feedback?
6. Is there Python or ROS 2 access on the current firmware, or is the C++ UDP SDK the only route?
7. What are the minimum stable walking speed and the quietest gait, and can speed and acceleration limits be capped?
8. What safety stops exist (remote e-stop, obstacle stop distance), and what do you require when people stand close to the robot?

## Decision rule
- **Pick Genisom AI for T04 if** your idea is a mobile companion that follows, carries, patrols, paces or guides — especially across stairs, slopes or outdoors — and you have a C++-capable teammate.
- **Avoid if** your idea needs an arm, physical contact with the patient, force control, or a quiet wheeled indoor platform; choose a mobile manipulator or a force-controlled arm vendor instead.

## Sources
- [Genisom AI — Emerging Applications (Accessibility & Public Services, Smart Guide Dog cases)](https://www.genisomai.com/en/industry/emerging-applications)
- [Genisom L2 product page](https://www.genisomai.com/en/product-robot/L2)
- [Genisom M1 product page](https://www.genisomai.com/en/product-robot/M1)
- [Genisom L1 product page](https://www.genisomai.com/en/product-robot/L1)
- [genisom_L1_sdk (GitHub)](https://github.com/zsibot/genisom_L1_sdk)
- [genisom_robot_sdk (GitHub)](https://github.com/zsibot/genisom_robot_sdk)
- [genisom_vln (GitHub)](https://github.com/zsibot/genisom_vln)
- [genisom_roamerx_open (GitHub; facts taken from the company profile)](https://github.com/zsibot/genisom_roamerx_open)
- [Genisom AI company profile (general research)](../Genisom-AI.md)
