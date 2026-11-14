---
type: challenge-playbook
company: "Binabik AI"
slug: Binabik-AI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Binabik AI × T03 — Hackathon Playbook

⬆ [Binabik AI profile](../Binabik-AI.md) · [Brief](Binabik-AI-T03-1-Brief.md) · [Products and solutions](Binabik-AI-T03-2-Products-and-Solutions.md)

> **Before anything else (first 30 minutes):** find the Binabik engineers and confirm (a) you get Studio / BDK access, (b) which robot on site it drives today, (c) how long one demonstration takes to become a running skill. All concepts below assume three yes answers. Binabik's API, languages and compute needs are **not public**, so the stack descriptions name its modules, not its calls. Every concept has a fallback that works without Binabik.

## Solution approaches

### Concept 1 — Reuse-loop tender (safest)

- **Problem → value:** hotels, spas and clinics in Leukerbad run on single-use cups, trays and packaging. Reusable systems fail on handling labour. A robot that unloads returned items, feeds a washer or collection point and stacks clean crates is machine tending under another name, which is the one thing Binabik's stack is shown doing.
- **Hardware:** Binabik Studio (Teach, Skill Engine, BDK) on a **Galaxea R1 Pro** or **AgiBot G2**. Props: return tray, a box standing in for the washer, stackable crates.
- **Architecture / stack:** robot cameras → Binabik Teach records one demonstration → Skill Engine segments it into take, transport, load, unload, stack → BDK skills execute on the robot. Compute location: not public, ask (assume Binabik laptop plus robot onboard computer). Your own code: a counter and impact dashboard.
- **48-hour plan:**
  - **H0–6:** secure access and robot slot; fix one item type and one crate; record the first demonstration.
  - **H6–24:** get the full loop running once; add a second item position; start logging cycle time and success rate.
  - **H24–40:** robustness runs (target 10 consecutive cycles); build the dashboard (items reused, single-use items avoided: your own assumptions, stated openly).
  - **H40–48:** freeze; record a backup video; rehearse.
- **3-minute demo script:** 0:00 problem with one number from a local venue (ask, do not invent) → 0:30 show the single demonstration clip → 1:00 live loop: take returned cups, load, unload, stack → 2:15 dashboard and measured cycle time → 2:40 deployment path: one shared robot tending several machines as a subscription.
- **Risks and fallbacks:** no access or skill not robust → teleoperate the same loop or script it with the robot vendor's SDK, and present Binabik's teach-once layer as the scaling path. Transparent or wet cups fail to grasp → switch to opaque crates and trays.
- **Judging angles:** *Innovation* low to medium · *Technical depth* medium (real loop on a real robot) · *Impact* clear if you bring a real local number · *Leukerbad* strong (spa and hotel reuse).

### Concept 2 — Teach-once recyclables sorter

- **Problem → value:** small sites (a clinic ward, a hotel kitchen, a mountain hut) cannot justify a sorting line. A robot that is shown a new waste fraction once and then sorts it lowers contamination of PET, aluminium and glass streams without a custom dataset.
- **Hardware:** same Binabik stack and host robot as Concept 1. Optional: **D-Robotics RDK** board with a camera for material classification. Three bins.
- **Architecture / stack:** camera → your classifier (material class) on the RDK or a laptop → class selects which taught place-skill to run → Binabik Skill Engine plan → BDK pick and place. Binabik does not describe material classification, so treat perception of *what* the item is as your job and *how to move it* as theirs.
- **48-hour plan:**
  - **H0–6:** access check; choose 3 rigid item types (PET bottle, can, small box); teach one pick-and-drop.
  - **H6–24:** teach the other two; train or adapt a small classifier on photos of your own items; wire class → skill.
  - **H24–40:** mixed-tray runs; measure sort accuracy and items per minute; teach a **fourth** item live to test the "new fraction in minutes" claim.
  - **H40–48:** freeze; backup video; rehearse the live-teach moment.
- **3-minute demo script:** 0:00 contamination problem → 0:30 mixed tray, robot sorts three types → 1:30 judge hands over an unseen item type; you demonstrate once; robot sorts it → 2:30 measured accuracy and time-to-teach → 2:50 where this goes.
- **Risks and fallbacks:** live teaching too slow for the stage → show it as a timed recording and sort only pre-taught items live. Crushed or deformable items fail → restrict to rigid items and say so. No Binabik access → classifier plus vendor-SDK pick and place; lose the teach-once claim.
- **Judging angles:** *Innovation* medium (teach a new fraction on stage) · *Technical depth* medium to high · *Impact* medium · *Leukerbad* medium (decentralised sorting for small alpine sites).

### Concept 3 — One shared robot for several small recycling machines

- **Problem → value:** a village has machines that each sit idle most of the day (bottle return, can crusher, compactor). Instead of fixed automation per machine, one mobile robot serves them in turn. This is Binabik's "one robot, many machines" pitch applied to municipal resource use. The resource-efficiency argument is **our inference**, not a Binabik claim.
- **Hardware:** Binabik stack on a **Galaxea R1 Pro** or **AgiBot G2**; two or three mock stations a few metres apart; optional **SKYLANDX MetaCam** scan of the area for a map and a visual.
- **Architecture / stack:** station status (buttons or a simple script standing in for machine states) → your scheduler decides which station needs service → robot's own navigation to the station → Binabik skill for that station (load, unload, stack). Whether BDK covers navigation between stations is not public; assume the vendor's navigation.
- **48-hour plan:**
  - **H0–6:** access check; confirm base navigation on the chosen robot; build two stations.
  - **H6–24:** teach one skill per station; get station-to-station driving working separately.
  - **H24–40:** integrate scheduler, driving and skills; add the third station only if two are solid.
  - **H40–48:** freeze; record a full run; prepare the utilisation comparison (one robot vs. one fixed cell per machine, assumptions stated).
- **3-minute demo script:** 0:00 idle-machine problem → 0:30 station A calls, robot drives and unloads → 1:20 station B calls, robot loads → 2:10 change the "order mix" live and show the robot re-tasked → 2:40 utilisation slide.
- **Risks and fallbacks:** navigation plus manipulation is two integrations in 48 hours → place stations within arm reach of one parking spot and drop driving. Skills do not transfer between stations → one skill, two stations.
- **Judging angles:** *Innovation* medium · *Technical depth* high if navigation and skills both run · *Impact* medium to high with honest numbers · *Leukerbad* medium (small municipality, shared assets).

### Concept 4 — Show-once disassembly for repair and reuse (most ambitious)

- **Problem → value:** repair and reuse fail because disassembly is manual and every product differs. Capture a technician's single demonstration and replay it for a simple, repeatable step (open a housing, pull a battery pack, separate two parts).
- **Hardware:** Binabik stack on **Galaxea R1 Pro** or **AgiBot G2**; one easy mock product with large latches or magnets. Optional: **OriginFlow** EMG capture or **XREAL** glasses on the technician for the demonstration story (whether either feeds Binabik Teach is not public).
- **Architecture / stack:** technician demonstrates (teleoperation or hand guiding) → Binabik Teach → Skill Engine segmentation into grasp, hold, pull, place → dual-arm execution. Contact-rich steps are beyond what Binabik shows publicly; expect to simplify the product until it works.
- **48-hour plan:**
  - **H0–6:** access check; ask Binabik directly whether two-arm, contact-rich steps are realistic; build the mock product.
  - **H6–24:** one step only (for example lift the lid); decide at H24 whether to continue or fall back to Concept 2.
  - **H24–40:** add the second step; sort the separated parts into reuse and recycle bins.
  - **H40–48:** freeze; backup video.
- **3-minute demo script:** 0:00 repair gap → 0:30 technician's demonstration clip → 1:10 robot repeats the step on a second unit → 2:10 parts go to reuse and recycle bins → 2:40 what a repair café or municipal depot would need next.
- **Risks and fallbacks:** highest technical risk of the four; a 20-person team's roadmap item, not a weekend job. Fallback at **H24**: switch to Concept 2 with the parts you already have.
- **Judging angles:** *Innovation* high · *Technical depth* high · *Impact* high in principle, weak evidence in 48 hours · *Leukerbad* low to medium.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Binabik + **Galaxea R1 Pro** | The pairing shown on Binabik's own site; most likely to work on day one | Low, if Binabik confirms the R1 Pro on site is supported |
| Binabik + **AgiBot G2** | Second named platform | Low to medium; confirm on site |
| + **D-Robotics RDK** | Material classifier at the edge, feeding the class to the skill selection | Medium: your own model and a simple message to your control script |
| + **SKYLANDX MetaCam** | 3D scan of the work area for mapping or as a visual for the pitch | Low as a visual; high if it must feed Binabik Sim (import path not public) |
| + **XREAL** glasses | Operator view of plan and counters; demonstration story | Medium; no known link to Binabik |
| + **OriginFlow** EMG capture | Alternative demonstration capture for Concept 4 | High; no known link to Binabik Teach |
| + any other robot (Unitree, Dobot, Flexiv, ROKAE …) | Only if Binabik says the BDK drives it | Unknown: support is not public, assume no |

## Questions to ask the Binabik AI engineers on site

1. Which robots at this event can the BDK drive **today**, and do you bring your own R1 Pro?
2. What do we program in (language, API style), and is there a ROS 2 bridge?
3. How long from one recorded demonstration to a skill running on the robot, and how many demonstrations do you really use?
4. Can a team add its own skill or edit the plan the Skill Engine produces, or only replay yours?
5. Can we feed in an external signal (our classifier's output, a station status) to choose which skill runs?
6. Does it need internet or your cloud, and what compute do we need on our side?
7. What breaks it: transparent, wet, crushed or deformable items? Dual-arm contact tasks?
8. How many teams can you support this weekend, and can you lend a Sim scene or is Sim out of scope for 48 hours?

## Decision rule

- **Pick Binabik AI for T03 if** your idea is indoor pick, carry, load and stack on a Galaxea R1 Pro or AgiBot G2, the Binabik team commits to working with you in the first hours, and "taught once, no dataset" is the core of your pitch.
- **Avoid if** you need monitoring, energy, outdoor or building automation, want a self-serve SDK or open code, or cannot get a confirmed access and robot slot by H2.

## Sources
- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Solutions](https://binabik.ai/solutions)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [ERF Matchmaking 2026 — Binabik profile](https://www.b2match.com/e/erf2026/participations/705635)
- [Venture Kick — Binabik AI receives CHF 40,000 (13 Feb 2026)](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries) (re-verified 2026-11-14)
- [Binabik AI company profile (this repo)](../Binabik-AI.md)
