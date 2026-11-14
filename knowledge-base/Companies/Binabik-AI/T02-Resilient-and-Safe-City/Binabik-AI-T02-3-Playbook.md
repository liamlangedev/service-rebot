---
type: challenge-playbook
company: "Binabik AI"
slug: Binabik-AI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Binabik AI × T02 — Hackathon Playbook

⬆ [Binabik AI profile](../Binabik-AI.md) · [Brief](Binabik-AI-T02-1-Brief.md) · [Products and solutions](Binabik-AI-T02-2-Products-and-Solutions.md)

**Fit 2/5.** Binabik is a supporting layer here, not a platform. Every concept below needs two things confirmed in the first hour: (a) Studio / BDK access from the Binabik team, (b) a free **AgiBot G2** or **Galaxea R1 Pro**. Binabik's APIs are not public, so the stack descriptions name layers, not function calls. Each concept has a fallback that survives without Binabik.

## Solution approaches

### Concept 1 — Teach-once plant-room responder (safest)

- **Problem → value:** when the access road is closed by snow or avalanche risk, a technician may not reach a pump room or electrical cabinet. A robot already on site performs the first intervention (close a valve, flip a breaker, press a reset) after being shown the procedure once.
- **Hardware:** Galaxea R1 Pro or AgiBot G2 with Binabik Studio (Teach + Skill Engine) and BDK. A mock panel: ball valve, breaker switch, push button, status lamp.
- **Architecture / stack:**
  - Perception: robot cameras as recorded by Binabik Teach; locating the panel is handled by the taught skill (generalisation over positions is a company claim).
  - Planning: Skill Engine segments the demonstration into skills and sequences them.
  - Control: BDK skill execution on the robot; low-level control stays with the vendor SDK.
  - Trigger: a simple team-built alarm (button, MQTT message or script) that starts the task. Whether Studio accepts an external trigger is not public; worst case an operator starts it by hand.
  - Compute: wherever Binabik's team runs Studio (not public).
- **48-hour plan:**
  - H0–6: confirm access and robot; build the mock panel; agree the exact three-step procedure with Binabik engineers.
  - H6–24: record demonstrations; get the first autonomous replay; measure success rate on 10 runs.
  - H24–40: move the panel, change lighting, repeat; add the alarm trigger and a status dashboard.
  - H40–48: rehearse; record a backup video; freeze.
- **3-minute demo script:** 0:00 scenario (road closed, pump alarm) → 0:30 show the 60-second recording of the single demonstration → 1:00 alarm fires, robot drives to panel and executes → 2:15 panel moved 20 cm, robot repeats → 2:45 success numbers and what a real deployment needs.
- **Risks and fallbacks:** no Studio access → script the three motions with the robot vendor's own SDK or teleoperation and present Binabik as the intended teaching layer. Valve torque too high → use a lever valve or switch only.
- **Judging angles:** innovation (teach instead of program); technical depth (repeatability numbers, moved-panel test); impact (first response without a technician); Leukerbad (thermal-bath pump rooms, road closures in winter).

### Concept 2 — One robot, re-tasked for the emergency

- **Problem → value:** small towns cannot afford dedicated emergency robots. Resilience comes from re-tasking an everyday service robot within an hour: today it restocks, during a disruption it packs and hands out emergency kits at a shelter.
- **Hardware:** same robot and Binabik stack as Concept 1. Props: blankets, water bottles, first-aid pouches, crates.
- **Architecture / stack:**
  - Perception and control as in Concept 1.
  - Planning: two taught tasks in the skill library (routine task, emergency kit packing); the point is that the second reuses skills from the first.
  - Team-built: a mode switch and a counter showing kits packed per hour.
- **48-hour plan:**
  - H0–6: confirm access; choose two tasks with overlapping motions (pick, place, carry).
  - H6–24: teach and stabilise the routine task.
  - H24–40: teach the emergency task **on a timer** and log how long re-teaching takes; this number is the result.
  - H40–48: rehearse the live switch; backup video.
- **3-minute demo script:** 0:00 robot does the routine task → 0:30 "landslide alert" → 0:45 show time-lapse of the re-teaching with the measured duration → 1:30 robot packs and hands over a kit → 2:30 skill-reuse diagram and time-to-retask figure.
- **Risks and fallbacks:** re-teaching takes longer than hours → teach both tasks beforehand and report the real time honestly. Soft items (blankets) are hard to grasp → use rigid boxes.
- **Judging angles:** innovation (resilience as re-taskability); technical depth (measured re-teach time, skill reuse); impact (affordable for small municipalities); Leukerbad (a resort town with many guests and few staff during a road closure).

### Concept 3 — Patrol spots it, manipulator fixes it

- **Problem → value:** inspection robots find problems but cannot act; manipulators can act but do not patrol. Link them: a patrolling sensor detects a change, the dual-arm robot performs the taught response.
- **Hardware:** Binabik stack on Galaxea R1 Pro or AgiBot G2 for the response. Detection from another vendor: a quadruped (Unitree Go2, Genisom AI or AGIBOT D1) or a SKYLANDX MetaCam scan. Binabik's own 2025 quadruped patrol prototype is not a product; do not plan on it unless the team offers it.
- **Architecture / stack:**
  - Perception: team-built change detection (before/after scan or image difference) on the patrol side.
  - Planning: a small team-built dispatcher maps "anomaly type at location" to a taught Binabik task.
  - Control: quadruped via its vendor SDK; manipulator via BDK skills.
  - Compute: team laptop for detection and dispatch; Binabik side as their team specifies.
- **48-hour plan:**
  - H0–6: split into two sub-teams; fix the interface (one message: anomaly type + location).
  - H6–24: sub-team A gets patrol and change detection working; sub-team B does Concept 1.
  - H24–40: integrate; run the full chain end to end at least five times.
  - H40–48: rehearse; keep each half demonstrable alone.
- **3-minute demo script:** 0:00 patrol robot walks the route → 0:40 a valve handle has been moved or a leak marker placed; detection flagged on screen → 1:10 dispatcher sends the manipulator → 2:20 patrol confirms the fix → 2:40 architecture slide.
- **Risks and fallbacks:** integration eats the time → show the two halves separately with a manual hand-off. Two vendors' robots in one space → agree floor zones early.
- **Judging angles:** innovation (detect-and-act loop across vendors); technical depth (multi-robot integration); impact (closes the gap between inspection and intervention); Leukerbad (tunnels, cable-car stations and plant rooms that are hard to reach in winter).

### Concept 4 — Expert teaches from a safe distance (most ambitious)

- **Problem → value:** in a hazardous room (gas, heat, unstable structure) the expert should not enter. The expert teleoperates the robot through the task once from outside; the robot then repeats it without a continuous link.
- **Hardware:** Binabik Teach in teleoperation capture mode on a supported robot; XREAL glasses for the operator's remote view (team-built video feed); optional OriginFlow EMG capture as an input device (integration with Binabik not public).
- **Architecture / stack:**
  - Perception: robot cameras streamed to the operator and recorded by Teach.
  - Planning: Skill Engine converts the teleoperated run into a repeatable task.
  - Control: vendor teleoperation for the demonstration, BDK skills for the autonomous repeat.
  - Open point: which teleoperation hardware Binabik Teach supports is not public.
- **48-hour plan:**
  - H0–6: verify with Binabik that teleoperated capture works on the available robot; if not, stop and switch to Concept 1.
  - H6–24: teleoperated demonstration recorded and replayed autonomously once.
  - H24–40: add the remote view in the glasses; cut the video link during the repeat to prove autonomy.
  - H40–48: rehearse; backup video.
- **3-minute demo script:** 0:00 "do not enter" zone → 0:30 operator outside teaches via teleoperation → 1:30 link is unplugged → 1:45 robot repeats alone → 2:40 what this means for hazardous interventions.
- **Risks and fallbacks:** teleop capture unsupported → hand-guided demonstration and reframe as Concept 1. AR feed latency → plain monitor.
- **Judging angles:** innovation (teach remotely, run autonomously); technical depth (teleop-to-skill pipeline); impact (removes people from hazardous rooms); Leukerbad (isolated installations during avalanche or rockfall closures).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Binabik + Galaxea R1 Pro | The robot in Binabik's own site imagery; most likely to work on day 1 | Low, if Binabik supports it on site |
| Binabik + AgiBot G2 | Second publicly named platform; a "same skill, other robot" demonstration if both are available | Low to medium |
| Binabik + Unitree / Genisom AI / AGIBOT D1 quadruped | Patrol and detection feeding a manipulation response (Concept 3) | Medium to high; dispatcher is team-built, quadruped is not driven by Binabik |
| Binabik + SKYLANDX MetaCam | Before/after 3D scan as the change detector or as a room model | Medium; scan comparison is team-built |
| Binabik + XREAL | Remote operator view while teaching or supervising | Medium; video pipeline is team-built |
| Binabik + D-Robotics RDK | Edge box for the team's own detection and alarm logic | Low; independent of Binabik |
| Binabik + any other arm or humanoid (Flexiv, Dobot, ROKAE, Unitree G1 and others) | Unknown; support is not public | Assume high or impossible until Binabik confirms |

## Questions to ask the Binabik AI engineers on site

1. Which robots in this hall can your stack drive **today**, and can we get one for 48 hours?
2. How long, realistically, from one demonstration to a reliable autonomous replay here: hours or days?
3. Can a taught task be started by an external signal (script, MQTT, ROS 2 topic), or only from Studio?
4. What language is the API, and can we write our own skill or only compose existing ones?
5. Does it run without internet, and what compute do you need next to the robot?
6. Does Teach record teleoperated demonstrations on this robot, and with which teleop device?
7. Does anything from the 2025 quadruped patrol / change-detection prototype still exist that we could use?
8. How many teams are you supporting, and will an engineer sit with us during the teaching sessions?

## Decision rule

- **Pick Binabik AI for T02 if** your idea is a manipulation response to an infrastructure fault, the Binabik team commits an engineer and a supported robot (G2 or R1 Pro) to you in the first hour, and your pitch is "teach once, respond autonomously".
- **Avoid if** your idea is outdoor, mobile, mapping or sensing led, if you need documented APIs you can use without help, or if Binabik cannot confirm access before H2. In that case build on a quadruped or scanner vendor directly.

## Sources
- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [Venture Kick — Binabik AI receives CHF 40,000 (13 Feb 2026)](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- [ERF Matchmaking 2026 — Binabik profile](https://www.b2match.com/e/erf2026/participations/705635)
- [Binabik AI company profile (internal)](../Binabik-AI.md)
