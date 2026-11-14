---
type: challenge-playbook
company: "Magiclab Robotics"
slug: Magiclab
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Magiclab Robotics × T04 — Hackathon Playbook

⬆ [Magiclab Robotics profile](../Magiclab.md) · [Brief](Magiclab-T04-1-Brief.md) · [Products and solutions](Magiclab-T04-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- Magiclab has no care product: you build the care logic; the robot is the body. Which units are on site is **not confirmed** — verify **EDU / Development Version** before committing.
- **No physical contact with people.** Keep at least 1 m between a walking robot and any "patient" actor; humanoid on a gantry or with a spotter.
- Run perception, speech and LLM on **your laptop**, wired to the robot (Ubuntu 22.04+, 192.168.54.x subnet, multicast enabled).

## Solution approaches

### Concept 1 — "Pill Runner": medication and item delivery with spoken reminders (safest)
- **Problem → value:** Care staff lose time on small errands and reminder rounds. A quadruped delivers pill boxes, water or towels to rooms on schedule, announces itself, confirms pick-up and logs it for the caregiver.
- **Hardware:** MagicDog EDU with a basket or tray on its back (payload about 5 kg). Optional: D-Robotics RDK board as on-board camera node; MagicDog-W as a substitute body.
- **Architecture / stack:**
  - Perception: built-in SLAM and localisation via `magicdog_sdk` (`slam_example.py`, `navigation_example.py`); laptop camera pipeline for "item removed" detection (simple before / after image difference or a weight switch in the tray).
  - Planning: schedule table (who, what, when, which room) → navigation targets; LLM only for phrasing reminders.
  - Control: high-level navigation targets and gait from the SDK; SDK audio example for speech output; small web dashboard for the caregiver.
  - Compute: laptop over Ethernet / Wi-Fi.
- **48-hour plan:**
  - H0–6: confirm EDU unit, run SDK quick start, drive by velocity command, play audio.
  - H6–24: map the demo corridor, save three "room" poses, loop navigate → speak → wait.
  - H24–40: pick-up confirmation, missed-dose escalation to dashboard, basket mount, multilingual phrases.
  - H40–48: rehearse 10 full runs, record backup video, tune speeds down.
- **3-minute demo script:** (1) Caregiver enters "Room 2, 10:00, blood-pressure tablet" on the dashboard. (2) Dog walks from the "station" to Room 2, stops at distance, announces the reminder. (3) Actor takes the box; dashboard turns green. (4) Second run: nobody responds → dog repeats, then alerts the caregiver. (5) Dog returns to the dock.
- **Risks and fallbacks:** navigation drift in a crowded hall → shorten the route and use taped waypoints with velocity commands; audio too quiet → Bluetooth speaker in the basket; SDK navigation not working with current firmware → teleoperate the route and keep the autonomy claim to the reminder logic.
- **Judging angles:** Innovation — modest. Technical depth — full autonomy loop with confirmation and escalation. Impact — direct caregiver time saving. Leukerbad — rehab clinics and spa hotels with many elderly guests and long corridors.

### Concept 2 — "Walk Buddy": walking-escort companion with fall watch
- **Problem → value:** Rehab patients are told to walk daily but are afraid to go alone; staff cannot escort everyone. A dog-sized robot walks along, carries a bottle and phone, sets the pace, encourages, and calls for help if the person stops abnormally or falls.
- **Hardware:** MagicDog EDU. Optional: XREAL glasses for a remote therapist view; OriginFlow EMG band on the patient's leg for effort / fatigue signal.
- **Architecture / stack:**
  - Perception: robot camera stream (SDK sensor example) → pose estimation on the laptop → distance to person, gait cadence, "person on the ground" classifier.
  - Planning: state machine — lead / follow / wait / alert; distance and time goals from a therapist-set plan.
  - Control: velocity commands to hold a set distance. If the built-in **Smart Following** can be triggered from the SDK (⚠️ unverified), use it and only add the monitoring layer.
  - Compute: laptop carried by a team member, or a small on-board computer in the basket.
- **48-hour plan:**
  - H0–6: SDK up; test built-in follow mode from the app; decide built-in versus own follower.
  - H6–24: person tracking and distance keeping at slow walking pace; spoken encouragement.
  - H24–40: fall / long-stop detection, alert with camera snapshot to caregiver phone, session summary (distance, pauses).
  - H40–48: rehearse on the real demo floor; test with different clothing and lighting.
- **3-minute demo script:** (1) Therapist sets "200 m, slow". (2) Actor with a walking stick starts; dog walks beside, announces progress. (3) Actor pauses — dog waits and asks if all is well. (4) Actor sits down on the floor — dog stops, asks, gets no answer, sends alert with photo. (5) Show the session report.
- **Risks and fallbacks:** tracking loses the person among spectators → coloured vest marker; false fall alarms → require voice check before alerting; tripping hazard from the dog itself → fixed lateral offset, low speed, state this limit openly.
- **Judging angles:** Innovation — combines escort, coaching and safety net. Technical depth — real-time human tracking plus behaviour logic. Impact — more unsupervised walking in rehab. Leukerbad — promenade and clinic walks; slopes up to 40° are within the dog's stated ability, but snow and ice are untested.

### Concept 3 — "Coach Z": humanoid rehab-exercise coach with rep counting
- **Problem → value:** Home and clinic exercise programmes fail on motivation and correct execution. A small humanoid demonstrates each exercise, watches the patient, counts repetitions, corrects form by voice and reports adherence to the physiotherapist.
- **Hardware:** MagicBot Z1 **Development Version**. Optional: OriginFlow EMG (muscle activation as a second feedback channel); XREAL glasses (therapist sees live joint angles); D-Robotics board for on-board pose estimation.
- **Architecture / stack:**
  - Perception: Z1 head RGB-D stream (SDK sensor example) → pose estimation on laptop → joint angles, rep counter, range-of-motion score.
  - Planning: exercise script (sets, reps, target angles) → dialogue manager; LLM turns scores into short spoken feedback.
  - Control: Z1 demonstrates upper-body movements. Route A: preset "trick" actions and head movement from the high-level controller. Route B: arm joint trajectories through the low-level / hybrid control example while the robot stands (feasibility of arms-only control during balance ⚠️ unverified — ask). TTS through the SDK audio controller.
  - Compute: laptop; robot stationary on a gantry or with spotter.
- **48-hour plan:**
  - H0–6: confirm Development Version, SDK quick start, TTS, camera stream; ask engineers how to command arms while standing.
  - H6–24: pose pipeline with rep counting for three seated exercises (shoulder raise, elbow flexion, arm circle); record three arm trajectories in simulation (URDF / MuJoCo) and replay slowly on the robot.
  - H24–40: feedback rules, session report, optional EMG overlay.
  - H40–48: rehearse; fallback video; battery plan (about 2 h per pack).
- **3-minute demo script:** (1) Z1 greets the seated actor and demonstrates a shoulder raise. (2) Actor does five reps; Z1 counts aloud. (3) Actor does a half-range rep — Z1 notices and asks for a higher lift. (4) Therapist tablet shows range-of-motion trend. (5) Z1 closes the session and schedules the next.
- **Risks and fallbacks:** arm control not accessible in time → Z1 talks and gestures with preset actions while a screen avatar shows the exercise; balance issues → keep it standing still, never walking near the patient; base (non-programmable) Z1 on site → move the concept to a MagicDog EDU as the "coach" with screen, or switch vendor.
- **Judging angles:** Innovation — embodied coach plus objective measurement. Technical depth — perception, motion generation and dialogue in one loop. Impact — adherence is the main failure point of rehab. Leukerbad — fits the village's rehabilitation clinics directly.

### Concept 4 — "Care Avatar": tele-operated humanoid helper with learned hand-over (most ambitious)
- **Problem → value:** One remote nurse or family member could help several people with small physical tasks (hand over a cup, pick up a dropped object) through a robot body, with frequent tasks automated over time.
- **Hardware:** MagicBot Gen1 with MagicHand S01 (only if a hackable unit is on site), or Z1 Development Version with optional dexterous hands. XR headset for the operator — Magiclab's open teleoperation repo targets the **PICO 4 Ultra with body trackers**, which is not an on-site vendor; XREAL would need its own bridge. Optional: WUJI Hand, Binabik AI agent OS.
- **Architecture / stack:**
  - Perception: operator's head and wrist poses; robot RGB-D for the operator view and for object detection.
  - Planning: teleoperation first (`pico_teleoperate` on Gen1); then record demonstrations and fine-tune a policy with the `magicbot-gen1_pi0_demo` pipeline for one task.
  - Control: Gen1 SDK posture mode for teleoperation; learned policy as a switchable skill.
  - Compute: GPU workstation or cloud for training; laptop for inference.
- **48-hour plan:**
  - H0–6: confirm hardware and XR device; get teleoperation running end to end — if this fails by H6, drop to Concept 3.
  - H6–24: reliable tele-operated pick-and-hand-over at a table; start collecting demonstrations.
  - H24–40: fine-tune one skill, or script it with object detection if training lags.
  - H40–48: rehearse with a seated actor behind a table (the table is the safety barrier).
- **3-minute demo script:** (1) Actor asks for the water bottle. (2) Remote operator puts on the headset; the robot mirrors the arms, picks up the bottle, places it within reach on the table. (3) Operator presses "auto": the robot repeats a learned pick-and-place. (4) Explain the supervision model — one nurse, many rooms.
- **Risks and fallbacks:** needs hardware that may not be here (Gen1, PICO) → verify before starting; training does not converge in time → present teleoperation only; latency over venue Wi-Fi → wired link; heavy robot near people → table barrier, no direct hand-to-hand transfer.
- **Judging angles:** Innovation — high. Technical depth — high (teleoperation plus imitation learning). Impact — plausible staffing model, but far from deployable. Leukerbad — remote valleys with scarce care staff make tele-care a credible story.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| MagicBot Z1 dev + **OriginFlow** EMG | Rehab coach that measures muscle activation, not just joint angles | Medium — EMG stream to laptop; no robot-side change |
| MagicDog EDU + **XREAL** glasses | Caregiver or remote therapist sees robot camera, alerts and patient stats hands-free | Low–medium — standalone app fed by your laptop |
| MagicDog EDU or Z1 + **D-Robotics RDK** | On-board pose estimation / fall detection without a tethered laptop | Medium — mounting, power and network on the robot |
| MagicDog EDU (mobile) + **Flexiv Rizon** or **ROKAE xMate** (fixed) | Dog fetches and brings items; force-controlled arm does the contact task (hand-over, guided exercise) | Medium — two independent systems linked by a task manager |
| MagicDog EDU + **SKYLANDX MetaCam** | Fast 3D scan of the clinic for route planning and a digital-twin view | High for navigation use (map formats ⚠️ unverified); low if used only for visualisation |
| Z1 dev / Gen1 + **WUJI Hand** | Finer grasping than the stock hand | High — mechanical and electrical adaptation; not a 48-hour job unless adapters exist |
| Any Magiclab robot + **Binabik AI** | Agent layer for task orchestration and dialogue | Unknown — ask Binabik whether a Magiclab adapter exists |

Naming trap when talking across booths: MagicBot **Z1** is not the Unitree Z1 arm; MagicBot **D1** is not the AGIBOT D1 quadruped; MagicBot **Gen1** is not a Unitree / AGIBOT / Galbot G1.

## Questions to ask the Magiclab Robotics engineers on site

1. Which exact units are here — **MagicDog EDU or PRO, Z1 Development Version or base**? Is low-level control unlocked on them?
2. Can the MagicDog's built-in **Smart Following and human recognition** be started, stopped and read out through the SDK, or only through the app?
3. On the Z1, how do we command **arm joints while the built-in controller keeps balance** — is that what the hybrid motion example does? Are there ready-made arm gestures we can reuse?
4. Does the SDK navigation work on the firmware installed today, and how do we save and reload a map?
5. Which **languages** do TTS and the dialog system support (German, French, English)? Does dialog need internet or a subscription?
6. Is a **MagicArm R1** on site, and is there an SDK we can get today? What are its collision-detection and force-limit settings?
7. What are the recommended **safety limits near people**: maximum speed, stand-off distance, emergency stop, and behaviour on low battery or lost connection?
8. How many batteries and chargers are available per robot, and can we mount a tray or small computer on the MagicDog (power output, mounting points)?

## Decision rule

- **Pick Magiclab Robotics for T04 if** your idea is contact-free — delivery, reminders, escorting, monitoring or exercise coaching — and a programmable MagicDog EDU or Z1 Development Version is confirmed on site.
- **Avoid if** your idea needs physical support or therapeutic contact with a person, precise or heavy manipulation, or a vendor with care-domain references; look at the force-controlled arm and wheeled dual-arm vendors instead.

## Sources

- [Magiclab Robotics company profile](../Magiclab.md)
- [MagicBot Z1 product page](https://www.magiclab.top/en/z1)
- [MagicDog product page](https://www.magiclab.top/en/dog)
- [MagicArm R1 product page](https://www.magiclab.top/en/magicarm-r1)
- [GitHub — MagiclabRobotics organisation](https://github.com/MagiclabRobotics)
- [GitHub — magicbot-z1_sdk](https://github.com/MagiclabRobotics/magicbot-z1_sdk)
- [GitHub — magicdog_sdk](https://github.com/MagiclabRobotics/magicdog_sdk)
- [GitHub — pico_teleoperate](https://github.com/MagiclabRobotics/pico_teleoperate)
- [GitHub — magicbot-gen1_pi0_demo](https://github.com/MagiclabRobotics/magicbot-gen1_pi0_demo)
- [GitHub — Magiclab_GMR](https://github.com/MagiclabRobotics/Magiclab_GMR)
- [EqualOcean — MagicLab targets European logistics, Slovenia postal partnership](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)
