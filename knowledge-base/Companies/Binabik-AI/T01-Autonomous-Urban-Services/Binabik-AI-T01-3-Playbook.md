---
type: challenge-playbook
company: "Binabik AI"
slug: Binabik-AI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Binabik AI × T01 — Hackathon Playbook

⬆ [Binabik AI profile](../Binabik-AI.md) · [Brief](Binabik-AI-T01-1-Brief.md) · [Products and solutions](Binabik-AI-T01-2-Products-and-Solutions.md)

**Before you plan anything:** every concept below assumes (a) Binabik engineers give you Studio / BDK access and (b) you get time on a **Galaxea R1 Pro** or **AgiBot G2**. Neither is confirmed. Binabik's interfaces are not public, so the stack descriptions name their modules, not API calls. Settle both points in the first hour, or switch to the fallback in each concept.

## Solution approaches

### Concept 1 — Teach-once service counter (no driving)
- **Problem → value:** small hotels, spa desks and municipal counters in Leukerbad cannot staff every handout point (towels, parcels, rental gear, lost property). A robot that staff can re-teach with one demonstration covers new items without a programmer.
- **Hardware:** Binabik Studio (Teach + Skill Engine) + BDK on one stationary R1 Pro or G2 at a table with a shelf and a handover tray.
- **Architecture / stack:** robot cameras → Binabik Teach records one demonstration → Skill Engine segments it and maps it to BDK skills → plan reviewed by the operator → BDK executes through the robot vendor's controller. Request intake is your own code (tablet button or QR code). Where compute runs: not public; ask.
- **48-hour plan:**
  - H0–6: get access, confirm robot, teach one item end to end.
  - H6–24: add 2–3 items, vary positions, build the request tablet.
  - H24–40: teach a brand-new item live as a rehearsal; time it.
  - H40–48: record backup video, rehearse the pitch.
- **3-minute demo script:** guest taps "towel" → robot picks and places it in the tray → a judge hands over an unseen item → team member demonstrates once → robot repeats it → show the plan-review screen.
- **Risks and fallbacks:** live teaching fails → show the pre-taught items plus a recording of teaching. No Binabik access → script the picks with the robot vendor's SDK and drop the "teach once" claim.
- **Judging angles:** innovation medium · technical depth medium · impact: staff-teachable service robots · Leukerbad: spa and hotel handout points.

### Concept 2 — Back-of-house runner (two stations, indoor delivery)
- **Problem → value:** linen, parcels and supplies move between laundry, reception and clinic floors all day. Pick at A, carry, place at B is the smallest complete "delivery" loop.
- **Hardware:** as Concept 1, on a wheeled R1 Pro or G2, plus two tables as stations. Optional: SKYLANDX MetaCam scan of the venue as a map (integration with the robot's navigation ⚠️ unverified).
- **Architecture / stack:** manipulation at each station via Binabik (taught once per station). Driving between stations via the **robot vendor's** navigation, since Binabik publishes nothing on navigation. Your glue code sequences "pick skill → drive → place skill". Ask whether the BDK can command the base at all.
- **48-hour plan:**
  - H0–6: confirm base control path (BDK or vendor SDK); teach the pick.
  - H6–24: teach the place; get reliable A→B driving on a short, clear route.
  - H24–40: chain the three steps; add an order trigger and a status page.
  - H40–48: endurance runs, count successes, record backup.
- **3-minute demo script:** order placed on a phone → robot picks a linen bundle at "laundry" → drives 5–10 m → places it at "reception" → show success count from rehearsals → swap the item and re-teach in front of the judges if stable.
- **Risks and fallbacks:** navigation unreliable → drive by teleoperation and say so, keep autonomous manipulation. Chain too slow → fall back to Concept 1 at two fixed robots or one.
- **Judging angles:** innovation medium · technical depth good (taught manipulation + navigation) · impact: internal logistics in hospitality and clinics · Leukerbad: hotels, thermal baths, rehabilitation clinics.

### Concept 3 — One taught chore, two robot brands (upkeep crew)
- **Problem → value:** a town or hotel group will not buy one robot brand forever. Show a public-space upkeep chore (clear a tray station, sort bottles into the right bin, restock a brochure rack) taught once and run on **both** an R1 Pro and a G2.
- **Hardware:** Binabik BDK on Galaxea R1 Pro **and** AgiBot G2. Needs both vendors to lend a robot.
- **Architecture / stack:** one demonstration → Skill Engine plan → the same skill set executed on each robot through the BDK's hardware abstraction (Binabik states both robots already run the same skills). Perception and compute details not public.
- **48-hour plan:**
  - H0–6: confirm both robots are actually BDK-ready on site; pick one chore.
  - H6–24: teach on robot 1 until repeatable.
  - H24–40: transfer to robot 2, fix gripper and camera differences with Binabik's help.
  - H40–48: side-by-side run, backup video.
- **3-minute demo script:** one demonstration shown on video → robot 1 does the chore → robot 2 does the same chore from the same program → slide: "skills belong to the town, not to the robot vendor".
- **Risks and fallbacks:** second robot not ready → show transfer in Binabik Sim, or run Concept 1 on one robot. Two vendors' schedules clash → book slots early.
- **Judging angles:** innovation high (vendor independence) · technical depth high · impact: procurement freedom for municipalities · Leukerbad: shared robots across hotels and the commune.

### Concept 4 — Indoor–outdoor relay (most ambitious)
- **Problem → value:** real last-mile in an alpine village means slopes, snow and steps that wheeled humanoids cannot handle. Split the job: a legged robot carries the load outside, a wheeled dual-arm robot does loading and unloading at each end.
- **Hardware:** Binabik stack on R1 Pro or G2 for load / unload; a quadruped with a cargo box for the outdoor leg (Unitree Go2 / B2, AGIBOT D1, Magiclab MagicDog or Genisom M1 / L1, whichever is available). The quadruped is driven with its own vendor SDK; Binabik support for quadrupeds today is not public.
- **Architecture / stack:** taught "load box into carrier" and "unload box" skills via Binabik → handover point marked by a fiducial or fixed dock → quadruped navigation via its vendor stack → your dispatcher service coordinates both robots over the local network.
- **48-hour plan:**
  - H0–6: prove loading into the quadruped's box by teleoperation; decide go / no-go.
  - H6–24: teach load and unload; get the quadruped walking a fixed route.
  - H24–40: integrate the dispatcher and docking alignment.
  - H40–48: full relay runs, backup video of an outdoor leg.
- **3-minute demo script:** order arrives → humanoid loads the quadruped → quadruped walks a ramp or outdoor stretch → returns to a second station → unload → map of the village showing where each robot type works.
- **Risks and fallbacks:** docking alignment too loose for taught skills → use a larger open crate. Too many moving parts → cut to Concept 2 and present the relay as roadmap with one filmed outdoor leg.
- **Judging angles:** innovation high · technical depth high (multi-robot, multi-vendor) · impact: honest answer to alpine terrain · Leukerbad: steep lanes, winter conditions.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Binabik + Galaxea R1 Pro | The pairing shown on Binabik's own site; lowest-risk host robot | Low, if Binabik brings its setup |
| Binabik + AGIBOT G2 | Second named platform; needed for Concept 3 | Low to medium; depends on on-site readiness |
| Binabik + Galaxea + AGIBOT | Same taught skill on two brands | Medium to high; two vendors' time slots |
| Binabik + a quadruped vendor (Unitree, AGIBOT D1, Magiclab, Genisom) | Outdoor leg of a delivery relay | High; no Binabik quadruped support is public, so two separate stacks |
| Binabik + SKYLANDX MetaCam | Venue scan for route planning or the pitch visual | Medium; map hand-off to robot navigation ⚠️ unverified |
| Binabik + OriginFlow or XREAL | Alternative demonstration or operator interfaces | High and ⚠️ unverified; Binabik's teleoperation inputs are not public |

## Questions to ask the Binabik AI engineers on site

1. Which robots in this hall can the BDK drive **today**, and did you bring your own R1 Pro?
2. Can teams get Studio access for 48 hours, and how many teams can you support?
3. Does the BDK command the mobile base and navigation, or only arms and grippers?
4. How long from one demonstration to a repeatable skill for a simple pick and place?
5. What language is the API, and can we call skills from our own Python process?
6. Does anything need internet or your cloud, given the venue network?
7. Can we add our own skill or perception model, or only combine existing ones?
8. Which grippers are mounted, and what object sizes and weights are realistic?

## Decision rule

- **Pick Binabik AI for T01 if** the team confirms access plus a supported robot in the first hour, and your idea's value is "staff can teach the robot a new handling chore" rather than navigation.
- **Avoid if** your concept is mainly about getting around (streets, snow, multi-floor routes, fleets), you need documented self-serve tools, or Binabik cannot commit an engineer to your team.

## Sources
- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Solutions](https://binabik.ai/solutions)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [Binabik AI — Open positions](https://binabik.ai/open-positions)
- [Switzerland Global Enterprise — Binabik establishes presence in Winterthur (14 Apr 2026)](https://www.s-ge.com/invest/en/articles/news/ai-robotics-start-binabik-establishes-presence-winterthur)
- [ERF Matchmaking 2026 — Binabik profile](https://www.b2match.com/e/erf2026/participations/705635)
- [Binabik AI company profile (this repository)](../Binabik-AI.md)
