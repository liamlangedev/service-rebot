---
type: challenge-playbook
company: "Galbot"
slug: Galbot
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Galbot × T04 — Hackathon Playbook

⬆ [Galbot profile](../Galbot.md) · [Brief](Galbot-T04-1-Brief.md) · [Products and solutions](Galbot-T04-2-Products-and-Solutions.md)

**Assumptions:** a Galbot G1 with two-finger grippers and GalbotSDK is on site (best guess, not confirmed). All concepts are indoor, flat-floor, and keep the robot out of body contact: objects are handed over, people are never pushed, lifted or steadied. Always cap base speed and keep one team member on the emergency stop.

## Solution approaches

### Concept 1 — Medication round aide (safest)

- **Problem → value:** night and weekend staff in clinics and care homes spend time on fetching and distributing medication; mix-ups are a safety issue. The robot picks the correct box, delivers it to the correct person and logs it. A nurse or pharmacist still prepares and approves the plan.
- **Hardware:** Galbot G1 (gripper or suction cup). Optional: D-Robotics RDK X5 as a bedside "station" for identity check (QR wristband) and confirmation button.
- **Architecture / stack:**
  - Perception: wrist / head cameras → barcode or label OCR to confirm the box; QR or face match for the resident.
  - Planning: simple task state machine (order → shelf slot → pick → verify → drive → hand over → log). Shelf slots taught as fixed poses.
  - Control: GalbotSDK `navigate_to_goal`, collision-aware motion planning, gripper commands; **force-sensor reading** to release only when the person pulls.
  - Compute: state machine and vision on a laptop over LAN or on the G1's Orin; no large model required.
- **48-hour plan:**
  - H0–6: confirm SDK access, run the pick-and-place and navigation tutorials, map the demo area, build a 2-shelf mock pharmacy.
  - H6–24: taught-pose picking of 4-6 boxes, barcode verification, navigation between shelf and two "rooms".
  - H24–40: force-triggered hand-over, identity check, wrong-box rejection, event log + caregiver dashboard.
  - H40–48: speed limits, failure recovery, rehearsal, backup video.
- **3-minute demo script:** nurse approves a plan on a tablet → G1 picks box A, shows the barcode check on screen → drives to resident 1, asks for wristband, hands over when pulled → second run with a deliberately misplaced box: robot detects the mismatch and refuses → dashboard shows the audit trail.
- **Risks and fallbacks:** grasp failures on small boxes → use suction cup or larger pill organisers; navigation drift → short route with relocalisation point; no SDK low-level access → the concept needs only high-level calls.
- **Judging angles:** *impact* (medication errors, staff time), *technical depth* (closed-loop verification, force hand-over), *Leukerbad relevance* (rehab clinics, small night teams), *credibility* (mirrors Galbot's real pharmacy deployments). Innovation is moderate.

### Concept 2 — "Bring me…" fetch and floor pick-up helper

- **Problem → value:** bending down and reaching high are hard and risky for people with limited mobility. A voice request gets a drink, glasses, remote or a dropped item delivered to the hand.
- **Hardware:** Galbot G1. Optional: XREAL glasses for a caregiver or the user to point at an object; WUJI hand only if the Galbot team confirms a mount (unlikely in 48 h).
- **Architecture / stack:**
  - Perception: speech-to-text (your own, e.g. local Whisper) → LLM parses the request → open-vocabulary detector on head camera locates the object.
  - Planning: grasp by **GraspVLA** (language-conditioned, ~9 GB GPU, ~200 ms per step, on a workstation GPU) or, as baseline, detector + depth grasp pose + SDK motion planning.
  - Control: SDK navigation and arm execution; SDK "execute VLA" tutorial as the template for sending model actions; force-triggered release.
  - Compute: models on a GPU laptop / workstation on the LAN; robot runs SDK calls.
- **48-hour plan:**
  - H0–6: SDK bring-up; decide grasp path (ask Galbot which grasp model is preloaded); camera streams to the laptop.
  - H6–24: baseline detector + depth grasp for 5 household objects on a table; voice request parsing.
  - H24–40: floor pick-up (wrist reach goes down to floor level), search across two locations, hand-over, spoken confirmations; try GraspVLA for unseen objects.
  - H40–48: reliability pass on the 3 best objects, rehearsal, backup video.
- **3-minute demo script:** seated user says "bring me my glasses" → G1 finds them on a side table, hands them over → user drops a TV remote, says "I dropped it" → G1 picks it from the floor → judge names an unseen object from a tray to show generalisation.
- **Risks and fallbacks:** GraspVLA was trained on Franka-format data, transfer to G1 is not documented → keep the classical grasp baseline as primary; speech in a noisy hall → push-to-talk microphone or tablet buttons; cluttered floor → fixed drop zone.
- **Judging angles:** *innovation* (open-vocabulary assistance), *technical depth* (VLA + classical fallback), *impact* (independence, fewer risky bends), *Leukerbad relevance* (hotel and clinic rooms for elderly spa guests).

### Concept 3 — Night-round companion with fall alert and tele-care

- **Problem → value:** one night nurse cannot watch every corridor. The robot patrols, spots a person on the floor or out of bed, alerts staff, opens a video link and brings a first-response item (water, blanket, phone).
- **Hardware:** Galbot G1 as patrol + delivery robot. Optional: D-Robotics RDK X5 for edge pose / fall detection; XREAL glasses as the nurse's remote view and overlay; SKYLANDX MetaCam to pre-map the ward quickly.
- **Architecture / stack:**
  - Perception: head / torso cameras → person detection + pose estimation (lying vs standing, time on floor). Run on the Orin or an RDK board. LiDAR for navigation only.
  - Planning: waypoint patrol; on alert → approach to a safe distance (do not touch), speak, wait for response, escalate.
  - Control: SDK `navigation_through_waypoints`, audio output, arm hand-over routine reused from Concept 1.
  - Compute: detection at the edge; alert service + web dashboard on a laptop; video stream to the nurse device.
- **48-hour plan:**
  - H0–6: SDK bring-up, map a corridor and two rooms, camera stream out.
  - H6–24: patrol loop, pose-based fall detection tuned on team members, alert + video link.
  - H24–40: spoken check-in dialogue, escalation logic, fetch-and-bring item, nurse view (tablet or XREAL).
  - H40–48: false-alarm tests (sitting, kneeling), privacy mode (on-device processing, no recording by default), rehearsal.
- **3-minute demo script:** lights dimmed; G1 patrols → actor lies on the floor → robot stops 1.5 m away, asks "are you all right?" → no answer → nurse device rings with live view → nurse speaks through the robot and sends it for a blanket → incident report appears.
- **Risks and fallbacks:** false positives → require pose + duration + no verbal response; low-light camera quality → keep a night light, state the limit honestly; privacy objections → pose skeletons only, show the design; robot cannot help a person up → say so, it is an alerting and fetching aide.
- **Judging angles:** *impact* (response time after falls, staff relief), *technical depth* (multi-sensor, edge AI, tele-operation link), *innovation* (patrol + manipulation in one robot), *Leukerbad relevance* (clinics and hotels with elderly guests, thin night staffing in a mountain village).

### Concept 4 — Object-based reach-and-grasp rehab coach (most ambitious)

- **Problem → value:** upper-limb rehabilitation needs many repetitions of reaching and grasping, with a therapist for only part of the day. The robot presents objects at graded heights and distances, counts repetitions, and records range of motion and pull force, so a therapist can supervise several patients and see progress data.
- **Hardware:** Galbot G1 (presents and receives objects; wrist F/T measures the patient's pull or push on the object). Optional: OriginFlow EMG capture for muscle-activation feedback; XREAL glasses for AR targets; D-Robotics board for pose estimation.
- **Architecture / stack:**
  - Perception: camera-based upper-body pose estimation → shoulder / elbow angles and reach distance; F/T at hand-over → grip-pull force curve; optional EMG stream.
  - Planning: exercise script with adaptive difficulty (target height, distance, object weight up to a few hundred grams); stop on pain word, fatigue or compensation posture.
  - Control: SDK IK + straight-line moves to pre-validated target poses inside a fixed safe volume; slow speeds; the robot holds still while the patient moves.
  - Compute: pose and analytics on a laptop; therapist dashboard in a browser.
- **48-hour plan:**
  - H0–6: SDK bring-up; define the safe workspace and speed caps; validate 9 target poses (3 heights x 3 distances) in simulation with the URDF / MJCF.
  - H6–24: present-and-take loop with force-triggered release; pose estimation and repetition counting.
  - H24–40: adaptive difficulty, session report (range of motion, force, repetitions), optional EMG or AR layer.
  - H40–48: safety review, therapist-view polish, rehearsal with a seated "patient".
- **3-minute demo script:** therapist picks a "shoulder flexion, level 2" session → G1 offers a ring at chest height, patient takes it, places it back higher → live angles and force on screen → patient compensates by leaning; system flags it and lowers the target → session report with a progress chart.
- **Risks and fallbacks:** clinical validity cannot be shown in 48 h → present it as a measurement and repetition tool under therapist control, not a therapy device; robot arm moving near a seated person → robot moves only when the patient's hands are outside the volume; compliant control may not be available → rely on stillness during contact and force thresholds; EMG / AR integration slips → drop them, the core loop stands alone.
- **Judging angles:** *innovation* (general-purpose manipulator as a therapy partner with quantitative feedback), *technical depth* (pose + force + adaptive loop), *impact* (therapist time, objective progress data), *Leukerbad relevance* (rehabilitation is a core local activity). Weakest on proof: Galbot has no rehab track record.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| G1 + D-Robotics RDK X5 | Edge fall / pose detection or bedside ID station feeding the robot's task queue | Low: separate device, talks over network |
| G1 + XREAL glasses | Nurse sees robot camera and alerts hands-free; AR targets for rehab exercises | Medium: video stream + simple overlay app |
| G1 + OriginFlow (EMG) | Muscle-activation feedback in the rehab coach; EMG gesture as a "bring it" trigger for users who cannot speak | Medium: depends on their data API, ask early |
| G1 + Flexiv Rizon | G1 fetches and delivers; the force-controlled arm does the contact task (e.g. guided limb exercise or massage demo) | Medium-high: two stacks, shared task state only |
| G1 + Unitree Go2 / other quadruped | Quadruped covers outdoor or stair legs (e.g. bringing medication between buildings), G1 does indoor hand-over | Medium: hand-off point and shared order queue |
| G1 + SKYLANDX MetaCam | Fast 3D scan of the mock ward for planning and a digital-twin visual | Low-medium: map import into G1 navigation not confirmed ⚠️ unverified |
| G1 + WUJI Hand | Finer manipulation (blister packs, bottle caps) | High: mount, wiring and SDK support unknown |
| ET1 (if on site) + G1 | ET1 as companion / exercise demonstrator, G1 as the hands | High: ET1 developer access not confirmed ⚠️ unverified |

## Questions to ask the Galbot engineers on site

1. Which robot(s) and end effectors are here, and which SDK / robot environment version is installed (V1.10.0 expects V1.18)?
2. Is low-level control unlocked, or only the high-level navigation and planning APIs?
3. Is a grasp model (GraspVLA or the pharmacy picking stack) preloaded and callable, or must we bring our own grasping?
4. Can we use the wrist F/T sensors for compliant or force-limited motion, or only read the values?
5. What speed limits, safety zones and e-stop options can we set for operation next to a seated person?
6. Does the robot have built-in speech recognition / TTS, and in which languages? Can we route our own audio?
7. How do we build and save a map of our demo area, and how long does it take?
8. Are teleoperation and MCAP data recording available here, so we can collect demonstrations and convert them with `galbot-mcap2lerobot`?

## Decision rule

- **Pick Galbot for T04 if** your idea is fetch, verify, deliver and hand over (medication, drinks, dropped objects, therapy objects) indoors, and you want a robot with a real pharmacy track record and a ready Python SDK.
- **Avoid if** your idea needs body contact or physical support (lifting, walking aid, massage, exoskeleton), outdoor or stair mobility, or a clinically proven care product.

## Sources
- [Galbot company profile (this repo)](../Galbot.md)
- [Galbot G1 product page](http://www.galbot.com/g1/)
- [Galbot ET1 product page](http://www.galbot.com/et1/)
- [Galbot developer portal](https://developer.galbot.com/?lang=en)
- [GalbotSDK (GitHub, README and G1 example tree)](https://github.com/GalaxyGeneralRobotics/GalbotSDK)
- [GitHub org GalaxyGeneralRobotics (repo list)](https://github.com/GalaxyGeneralRobotics)
- [GraspVLA code (PKU-EPIC)](https://github.com/PKU-EPIC/GraspVLA)
- [CGTN, 2026-03-13: China's first pharmacy robot goes into service in Beijing](https://news.cgtn.com/news/2026-03-13/China-s-first-pharmacy-robot-goes-into-service-in-Beijing-1LtZ7juLcZ2/p.html)
- [The Paper, 2026-09-30: G1 at Laobaixing Pharmacy, Shanghai](https://m.thepaper.cn/newsDetail_forward_34179567)
