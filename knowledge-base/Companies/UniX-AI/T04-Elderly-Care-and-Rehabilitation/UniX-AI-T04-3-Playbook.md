---
type: challenge-playbook
company: "UniX AI"
slug: UniX-AI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# UniX AI × T04 — Hackathon Playbook

⬆ [UniX AI profile](../UniX-AI.md) · [Brief](UniX-AI-T04-1-Brief.md) · [Products and solutions](UniX-AI-T04-2-Products-and-Solutions.md)

> **Before anything else (first 30 minutes):** find out which robot is on site (Wanda 2.0 or Panther) and what you can trigger from your own code: (a) a list of pre-loaded skills, (b) navigation goals, (c) teleoperation, (d) raw camera / mic streams. No SDK is public, so every concept below is designed as **your intelligence layer on a laptop + the robot's existing skills**, with teleoperation as fallback.
> **Safety rule for all concepts:** no physical contact between robot and person. Arm force sensing, collision detection and certification are not published. Hand objects over via a table or tray; use team members, not real patients.

## Solution approaches

### Concept 1 — Room concierge: "bring, serve, remind"

- **Problem → value:** Rehab-clinic and care-home staff lose time on small non-medical errands (a drink, glasses, the remote). A robot that takes spoken requests and runs a few errands frees caregivers for care.
- **Hardware:** Wanda 2.0 or Panther with UniPicker gripper. Optional: a tablet as a large-button / large-text interface for users who struggle with speech.
- **Architecture / stack:**
  - Perception: speech-to-text on a laptop (robot mic array if a stream is exposed, else a USB or tablet mic).
  - Planning: an LLM maps the request to one of 3–5 vendor skills (make tea, deliver item A to location B, tidy table) and a schedule for reminders ("time for your tablets — the box is on your tray").
  - Control: vendor skills and navigation, triggered through whatever interface UniX exposes (API call, app command or operator trigger).
  - Compute: laptop for speech and LLM; the robot runs its own stack.
- **48-hour plan:**
  - H0–6: confirm the skill list and trigger method; map the demo room; pick 3 skills that run reliably.
  - H6–24: build the voice → intent → skill pipeline; add spoken confirmations and the reminder scheduler; test with slow, quiet and accented speech.
  - H24–40: chain a full routine (request → fetch → place on tray → confirm); add the tablet interface; log tasks into a simple caregiver dashboard.
  - H40–48: 10 clean rehearsals; record a backup video.
- **3-minute demo script:** (0:00) the errand problem in one sentence → (0:20) "resident" asks for tea; robot confirms, prepares, places it on the tray → (1:30) scheduled medication reminder fires; robot brings the pill box to the table → (2:15) caregiver dashboard shows completed tasks → (2:40) what a clinic would need next.
- **Risks and fallbacks:** skills not triggerable from code → an operator triggers the skill when your software says so (state this openly). Tea-making too slow for the slot → use a shorter delivery skill. Speech fails in a noisy hall → tablet buttons.
- **Judging angles:** *Impact* — relieves caregivers directly. *Leukerbad* — fits rehab-clinic and spa-hotel rooms with elderly guests. *Technical depth* — moderate (integration). *Innovation* — low unless the interaction design for elderly users stands out.

### Concept 2 — Drop Guard: floor pick-up and fall response

- **Problem → value:** Bending to pick up dropped objects is a common fall trigger, and clutter on the floor is a trip hazard. The robot picks things up so the person does not bend, and responds when a fall does happen.
- **Hardware:** **Panther preferred** (800 mm lift, works down to floor level). Wanda 2.0 only if its floor reach is confirmed on site. Optional: D-Robotics RDK board with a camera as a fixed room sensor for fall detection.
- **Architecture / stack:**
  - Perception: object detection on floor-facing camera images (robot camera if exposed, otherwise the fixed room camera); person pose estimation for fall detection on the RDK or the laptop.
  - Planning: state machine — patrol → detect object → pick → place on table; or on a detected fall → drive to the person, ask "Are you OK?", wait for a spoken answer, alert a caregiver phone.
  - Control: vendor pick-and-place and navigation skills; if a floor-pick skill does not exist, ask the UniX team to teach one by demonstration (UniFlex) on day 1.
  - Compute: laptop / RDK for vision; robot on-board for manipulation.
- **48-hour plan:**
  - H0–6: test floor pick-up on 3 objects (glasses case, pill box, remote); decide whether a taught skill is needed and request it at once.
  - H6–24: fall detector on the fixed camera; alert path to a phone; the "drive to person and talk" behaviour.
  - H24–40: integrate the pick-up routine with spoken requests ("I dropped my glasses"); tune approach distance — stop **at least 1 m** from the person.
  - H40–48: rehearse both scenarios; backup video.
- **3-minute demo script:** (0:00) falls statistic and the bending problem → (0:20) the person drops a pill box and says so; the robot picks it up and places it on the side table → (1:20) the robot spots a second trip hazard on its own and clears it → (1:50) a team member simulates a fall; the robot approaches, asks, gets no answer, and the caregiver phone rings with a snapshot → (2:40) limits and next steps.
- **Risks and fallbacks:** floor grasp unreliable → restrict to 2 known objects, or teleoperate the grasp and keep detection and navigation autonomous. No camera stream from the robot → fixed room camera does all the perception. False fall alarms → require a spoken check before alerting.
- **Judging angles:** *Impact* — fall prevention is a top elder-care need. *Technical depth* — perception + manipulation + escalation logic. *Leukerbad* — rehab clinics with post-surgery patients who must not bend. *Innovation* — combining prevention (pick-up) with response.

### Concept 3 — Tele-care avatar: a remote caregiver with hands

- **Problem → value:** Alpine villages have few caregivers and long distances. A relative or nurse elsewhere could check in at night and actually *do* something — pass a glass of water, close a window — instead of only watching a video call.
- **Hardware:** Wanda 2.0 or Panther. XREAL glasses for the remote operator's view (optional). Depends on UniX's teleoperation, which the official application page claims works locally and remotely in real time (⚠️ unverified in practice).
- **Architecture / stack:**
  - Perception: robot head-camera stream to the operator; two-way audio.
  - Planning: shared autonomy — the operator selects a goal ("go to bedside", "fetch the glass"), the robot runs a skill; direct teleoperation only for the final manipulation when no skill exists.
  - Control: vendor teleoperation tooling plus skills.
  - Compute: operator laptop; link over venue Wi-Fi (state measured latency honestly).
- **48-hour plan:**
  - H0–6: get a teleoperation session running; measure latency; check what the operator sees and controls.
  - H6–24: operator UI with one-tap goals; audio call; consent prompt on the robot before the session starts ("Anna would like to visit — OK?").
  - H24–40: night-round script (visit 3 waypoints, check on the person, report); XREAL view if time allows.
  - H40–48: rehearse with the operator in another room; backup video.
- **3-minute demo script:** (0:00) caregiver shortage in mountain regions → (0:20) remote "daughter" asks to connect; the resident consents by voice → (0:50) she sends the robot to the kitchen corner with one tap and fetches a glass of water, taking over by teleoperation for the grasp → (2:00) automatic night round reports "all fine" → (2:30) privacy and consent design.
- **Risks and fallbacks:** teleoperation not available to teams → operator drives skills only (goal selection), no direct arm control. Network lag → operator in the same hall, and say so. Privacy concerns → camera active only after spoken consent, visible indicator.
- **Judging angles:** *Innovation* — telepresence with manipulation and a consent model. *Impact* — extends scarce staff across valleys. *Leukerbad* — remote-village relevance is concrete. *Technical depth* — depends on how much shared autonomy you build yourself.

### Concept 4 — Reach coach: robot-paced rehab exercises

- **Problem → value:** Physiotherapy time is short; patients skip exercises between sessions. A robot can pace reach-and-grasp exercises, hold targets at set heights and report progress to the therapist. No contact, no forces applied to the patient.
- **Hardware:** Panther or Wanda 2.0 (torso lift and 982 mm reach to present an object at graded heights and distances). OriginFlow EMG capture to measure muscle activation (optional). XREAL glasses to show targets or feedback (optional).
- **Architecture / stack:**
  - Perception: pose estimation of the patient's arm from a camera (external webcam is the safe choice); EMG stream from OriginFlow if available.
  - Planning: an exercise script sets target positions; difficulty adapts to measured range of motion and repetitions; spoken coaching from an LLM with fixed safety phrases.
  - Control: needs **commanded arm or gripper poses** (or a set of pre-taught "hold object at position N" skills) — the most demanding interface requirement in this playbook.
  - Compute: laptop.
- **48-hour plan:**
  - H0–6: confirm that arm poses can be commanded or that 5–6 hold positions can be taught; otherwise drop to Concept 1 or 2.
  - H6–24: pose tracking, repetition counting, range-of-motion measurement; spoken coaching.
  - H24–40: adaptive difficulty; therapist report (range and repetitions per session); EMG overlay if the OriginFlow team can stream data.
  - H40–48: rehearse with a seated team member; robot stays stationary while the person moves.
- **3-minute demo script:** (0:00) the between-sessions gap → (0:20) seated "patient"; robot holds a soft ball low and near as a reach target, patient reaches and touches it, robot counts → (1:10) robot raises the target as range improves; shows the EMG trace → (2:00) therapist report on screen → (2:30) safety boundaries: robot never moves while the hand is inside its workspace.
- **Risks and fallbacks:** no pose-level arm control → use torso lift plus 3 pre-taught positions, or let the robot only coach and count while targets sit on a shelf. Hand-over too close to the patient → place the object on a table between them. Medical claims → present as an exercise aid, not therapy.
- **Judging angles:** *Innovation* — highest of the four. *Technical depth* — closed loop from human sensing to robot behaviour. *Leukerbad* — direct link to the local rehabilitation clinics. *Impact* — credible only with a clear safety story.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| UniX robot + **D-Robotics RDK** camera node | Room-level fall detection that dispatches the robot (Concept 2) | Low — independent of the UniX interface |
| UniX robot + **XREAL** glasses | Caregiver or relative sees through the robot and picks goals (Concept 3) | Medium — needs the robot video stream |
| UniX robot + **OriginFlow** EMG | Muscle-activation feedback for exercise coaching (Concept 4) | Medium — data link only, no robot coupling |
| UniX robot + **Flexiv** Rizon arm | UniX does fetch and logistics; the force-controlled arm does any contact task (e.g. guided resistance exercise) | Medium — two separate systems sharing one task script |
| UniX robot + **Unitree Go2** | Indoor assistant plus an outdoor escort for walks on Leukerbad paths | Medium — hand-over logic between two robots |
| UniX robot + **SKYLANDX MetaCam** | Fast 3D scan of the "care room" for layout and hazard mapping | Low to medium — map import into the robot is ⚠️ unverified |
| Panther + **WUJI Hand** | Finer manipulation (bottle caps, blister packs); Panther is listed as dexterous-hand compatible | High — mechanical and control integration; unlikely in 48 h |

## Questions to ask the UniX AI engineers on site

1. Which robots are here (Wanda 2.0, Panther), how many, and how many hours per team?
2. Which pre-loaded skills run reliably in this venue, and can we trigger them from our own code (API, ROS 2 topic, app command)? In which language?
3. Can we send navigation goals and read the robot's pose and map?
4. Can we get live camera and microphone streams, and play audio through the robot's speakers?
5. Is teleoperation available to teams, with what device, and can sessions be recorded as demonstrations?
6. Can you teach one new skill with us by demonstration (for example a floor pick-up or a tray hand-over), and how long does that take?
7. What are the safety functions near people: speed limits, collision detection, e-stop, minimum distance you recommend?
8. Can Wanda 2.0 reach the floor, and what are the lightest and smallest objects the gripper handles reliably (pill box, glasses)?

## Decision rule

- **Pick UniX AI for T04 if** your idea is assistive fetch / serve / tidy or tele-care in an indoor room, you are happy to build the intelligence and interaction layer on top of vendor skills, and the on-site team confirms within the first hour that skills or teleoperation can be triggered by your software.
- **Avoid if** your idea needs physical contact with the person (transfer, massage, guided physio), low-level control or simulation from minute one, outdoor mobility, or if the answer to question 2 is "skills run from our app only".

## Sources
- [Panther product page](https://www.unix-group.ai/Panther)
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [UniPicker Pro product page](https://www.unix-group.ai/UniPicker)
- [Martian product page](https://www.unix-group.ai/Martian)
- [Household & Hotel application page (teleoperation and open-interface claims)](https://www.unix-group.ai/Household-Hotel)
- [Applications overview](https://www.unix-group.ai/Applications)
- [Press release, 2 Jan 2026: CES 2026 demos (via Webull / PR Newswire)](https://www.webull.com/news/14134140025406464)
- [Press release, 8 Apr 2026: Panther launch (via TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [UniX AI company profile (this repository)](../UniX-AI.md)
