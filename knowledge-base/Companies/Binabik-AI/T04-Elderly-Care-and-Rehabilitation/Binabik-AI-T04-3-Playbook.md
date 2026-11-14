---
type: challenge-playbook
company: "Binabik AI"
slug: Binabik-AI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Binabik AI × T04 — Hackathon Playbook

⬆ [Binabik AI profile](../Binabik-AI.md) · [Brief](Binabik-AI-T04-1-Brief.md) · [Products and solutions](Binabik-AI-T04-2-Products-and-Solutions.md)

**Before anything else (first 30 minutes):** every concept below needs two yeses. (1) A Binabik engineer agrees to set your team up with Studio / BDK. (2) AGIBOT or Galaxea gives you time on a **G2** or **R1 Pro** and accepts Binabik's software on it. If either answer is no, switch vendor; Binabik has nothing self-serve. All interface details below are assumptions to confirm on site, because Binabik publishes no API documentation.

## Solution approaches

Ordered from safest to most ambitious. None involves physical contact with a person.

### Concept 1 — Therapy-station tending

- **Problem → value:** in a rehab clinic, therapists lose minutes between sessions putting back weights, bands, balls and towels and laying out the next patient's set. A robot that resets and prepares stations gives that time back to patients. This is machine tending with therapy equipment, which is exactly what Binabik's stack is built for.
- **Hardware:** Binabik Studio (Teach, Skill Engine, BDK) on a **Galaxea R1 Pro** or **AgiBot G2**. Two tables as "stations", a shelf, 4–6 rigid objects (dumbbells, therapy balls, rolled towels in a tray).
- **Architecture / stack:** perception = host robot cameras as used by Binabik's skills (details not public) → planning = Skill Engine segments the therapist's demonstration into pick / carry / place steps, plan shown for approval → control = BDK skill calls to the host robot; base navigation between stations by whichever layer Binabik uses on that robot. Compute: on the robot or a laptop on the local network, as Binabik advises. A small web page or tablet lists "Station A: shoulder set / knee set" and triggers the matching taught routine.
- **48-hour plan:**
  - **H0–6:** secure access and robot; pick objects the gripper can hold reliably; record the first demonstration of one station reset.
  - **H6–24:** get one full reset running end to end; teach a second routine ("prepare knee set"); add the selection page.
  - **H24–40:** vary object positions, test 20 runs, log success rate and cycle time; add the plan-approval step to the demo flow.
  - **H40–48:** freeze; rehearse; record a backup video.
- **3-minute demo script:** (0:00) the problem in one sentence with a clinic photo. (0:20) therapist demonstrates a new layout once, live or on video. (1:00) plan appears on screen, therapist approves. (1:15) robot resets station A and prepares station B while the presenter shows measured success rate and time per reset. (2:30) "next step: any routine a therapist can show."
- **Risks and fallbacks:** teaching takes longer than promised → keep one routine only and show variation in object positions. Navigation unreliable → put both stations within arm and torso reach, no driving. No Binabik access → same demo with the host vendor's own teleoperation and replay tools (weaker story, still a demo).
- **Judging angles:** innovation: moderate (re-use of industrial tending). Technical depth: real teach-to-execution pipeline with measured reliability. Impact: therapist time, no patient-safety exposure. **Leukerbad:** rehab clinics and thermal-spa therapy rooms are the town's core business.

### Concept 2 — Carer-taught bedside fetch

- **Problem → value:** residents with limited mobility ask staff for small things all day (water, glasses, remote, pill box). A carer teaches each fetch once; the robot then delivers on request and the carer only approves.
- **Hardware:** as Concept 1, plus a bedside table, a shelf, a call button or tablet for the "resident". Optional: **D-Robotics RDK** board as the request front end (button, simple voice keyword).
- **Architecture / stack:** request (tablet, button or keyword on the edge board) → lookup of the taught routine → Skill Engine plan → **carer approves on a phone or tablet** → BDK executes pick, carry, place on the bedside table (never hand-to-hand) → confirmation message. Speech and request handling are your own code; Binabik does not publish a dialogue module.
- **48-hour plan:**
  - **H0–6:** access, robot, room mock-up; decide 3 objects; first demonstration.
  - **H6–24:** one object end to end; build the request and approval screens.
  - **H24–40:** second and third object; keep-out zone around the bed; repeat tests with moved objects.
  - **H40–48:** rehearse with a volunteer in the "bed"; backup video.
- **3-minute demo script:** (0:00) the problem: small fetch requests fill a carer's shift (quote a number only if you can source it). (0:20) resident taps "water". (0:30) carer's phone shows the plan, taps approve. (0:45) robot fetches the bottle and places it on the bedside table, stops at the marked line. (1:45) carer teaches a new item in one take (shortened). (2:30) privacy point: camera data stays in the building.
- **Risks and fallbacks:** small or shiny objects fail to grasp → put items in handled baskets or trays. Person too close → fixed stop line and a human safety operator with the stop control. Voice unreliable in a noisy hall → button only.
- **Judging angles:** innovation: the carer as the programmer. Technical depth: request → plan → approval → execution loop. Impact: caregiver relief, independence for the resident. **Leukerbad:** many elderly spa guests and clinic patients in a small town with a limited care workforce (our framing; check local figures before quoting).

### Concept 3 — Personal routine library with AR approval

- **Problem → value:** every resident has different routines (which cup, which shelf, which order). Build a per-person skill library that carers extend during normal work and review hands-free.
- **Hardware:** Concept 2 setup plus **XREAL** glasses for the carer.
- **Architecture / stack:** Teach captures each new routine → Skill Engine stores it under a resident profile (your own small database) → before execution, the plan steps are shown as a checklist in the carer's glasses → approve by gesture or phone → BDK executes. The glasses app talks to your own service, not to Binabik directly; whether plans can be exported from Studio as text is a question for the team.
- **48-hour plan:**
  - **H0–6:** confirm with Binabik that plan steps can be read out programmatically; if not, drop to Concept 2.
  - **H6–24:** two residents × two routines taught; profile store; plan export.
  - **H24–40:** glasses checklist and approval; test switching between profiles.
  - **H40–48:** rehearse; backup video.
- **3-minute demo script:** (0:00) two "residents", two different morning set-ups. (0:30) carer in glasses sees the plan for resident 1, approves, robot lays out the items. (1:30) switch to resident 2, different result from the same skills. (2:15) carer adds a new routine in one demonstration.
- **Risks and fallbacks:** plan export not possible → show the plan on Studio's own screen. Glasses integration slips → tablet. Too many routines → two is enough to make the point.
- **Judging angles:** innovation: personalised care routines without programming. Technical depth: two vendors, profile logic, human-in-the-loop approval. Impact: person-centred care. **Leukerbad:** short-stay rehab guests change weekly, so fast re-teaching matters.

### Concept 4 — Night-round assistant

- **Problem → value:** night staff are few. A robot does rounds, notices that something changed (object on the floor, door open, person on the floor), alerts the carer and can fetch an item on approval.
- **Hardware:** G2 or R1 Pro with Binabik stack; **D-Robotics RDK** board with a camera for person-on-floor detection using an open-source pose model; optional **SKYLANDX** scan as the reference map of the ward.
- **Architecture / stack:** round = taught or scripted waypoint tour → perception = your own change / fall detector on the edge board (Binabik's 2025 quadruped prototype did patrol and change detection, but that function is not in the current product; ask whether any of it survives) → event → alert to carer's phone with snapshot → carer picks a taught response routine ("bring blanket", "clear object") → Skill Engine plan → approve → execute.
- **48-hour plan:**
  - **H0–6:** confirm navigation tour is possible through Binabik's layer or the host robot's own; get the detector running on recorded video.
  - **H6–24:** tour of 3 waypoints; alert pipeline; one response routine taught.
  - **H24–40:** integrate detector with the tour; false-alarm tests; second routine.
  - **H40–48:** rehearse in dimmed light; backup video.
- **3-minute demo script:** (0:00) one night nurse, many rooms. (0:20) robot tours; a volunteer lies on a mat. (0:50) alert with photo on the carer's phone. (1:10) carer approves "bring blanket and stay"; robot fetches and places the blanket beside the person, keeps distance. (2:20) second event: object on the floor, robot removes it.
- **Risks and fallbacks:** three subsystems in 48 hours is a lot → cut to detection + alert + one fetch. Navigation not exposed → robot stationary at a corridor post. Detection weak → simulate the trigger with a button and say so openly.
- **Judging angles:** innovation: highest of the four. Technical depth: multi-vendor perception, navigation and manipulation. Impact: fall response time, night staffing. **Leukerbad:** clinics and hotels with elderly guests; snow and ice make falls a familiar local concern.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Binabik + **AGIBOT G2** | Named supported robot. Per AGIBOT's profile the G2 has force-controlled arms, a face display and dialogue features, which help the human-facing side | Low to medium, if both teams cooperate |
| Binabik + **Galaxea R1 Pro** | Named supported robot and the one in Binabik's own imagery, so probably their best-tested platform (inference) | Low to medium |
| Binabik + **D-Robotics RDK** | Edge box for request button, keyword, person or fall detection that triggers a taught routine | Medium; your own glue code |
| Binabik + **XREAL** | Hands-free plan checklist and approval for the carer | Medium to high; depends on reading plans out of Studio |
| Binabik + **SKYLANDX** | 3D scan of the room as a reference map or simulation backdrop | High; scene import into Binabik Sim not public |
| Binabik + **OriginFlow** | EMG capture of a therapist's hand motion as an alternative demonstration input | High; no public interface on Binabik's side, speculative |
| Binabik + other robots (Unitree, Galbot, Spirit AI, UniX AI, Dobot, Flexiv) | Would widen hardware choice | Unknown; support not public ⚠️ unverified. Ask before planning |

## Questions to ask the Binabik AI engineers on site

1. Which robots at this event can your stack drive **today**, and will you run it for a hackathon team?
2. What do we get: a Studio seat, a Python API, or an engineer operating it for us?
3. How long from one demonstration to a skill that works with objects moved 10–20 cm? How many demonstrations in practice?
4. Does the Skill Engine handle base navigation between rooms, or only manipulation at a station?
5. Can we read the plan steps out (text / JSON) to show them on our own approval screen?
6. What happens when a person walks into the workspace mid-task? Is there any speed or distance limit we can set?
7. Does it need internet, and where does camera data go during the hackathon?
8. Which grippers and object types work reliably? Cups, bottles, soft items?

## Decision rule

- **Pick Binabik AI for T04 if** a Binabik engineer commits to your team in the first hour, you have a G2 or R1 Pro slot, and your idea is "non-experts teach a robot care logistics" with no physical contact.
- **Avoid if** you need documented self-serve tools, physical assistance (lifting, massage, gait support), or a voice / companionship / monitoring product; go directly to a hardware vendor with an open SDK instead.

## Sources
- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Solutions](https://binabik.ai/solutions)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [Venture Kick — Binabik AI receives CHF 40,000 (13 Feb 2026)](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- [Switzerland Global Enterprise — Binabik establishes presence in Winterthur (14 Apr 2026)](https://www.s-ge.com/invest/en/articles/news/ai-robotics-start-binabik-establishes-presence-winterthur)
- [ERF Matchmaking 2026 — Binabik profile](https://www.b2match.com/e/erf2026/participations/705635)
