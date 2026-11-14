---
type: track-overview
challenge: T01
challenge_title: "Autonomous Urban Services"
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, track]
---
# T01 Autonomous Urban Services — Track Overview

> **Official tagline:** Robots that move, deliver and maintain the city.

[Start here](../../00-START-HERE.md) · [Solution patterns](T01-1-Solution-Patterns.md) · [Hardware shortlist](T01-2-Hardware-Shortlist.md) · [Cross-vendor solutions](T01-3-Cross-Vendor-Solutions.md)

**Status of this page:** the public event pages (BuilderBase, Luma) give only the track title and tagline. Everything below the kickoff checklist is **preparation and interpretation**, not the official brief. Legend: ● easy / good fit · ◐ stretch / partial fit · ○ unrealistic / poor fit · ⚠️ unverified.

## Official directions for this track

> **Official tagline (carnival website):** "Let robots become intelligent service partners of the future city."

The organizers publish seven example directions per track. Tracks are **open**: the team defines its own problem, platform and approach inside the theme. Verified on the official site on 2026-11-14.

| # | Official direction |
|---|---|
| T01.1 | Autonomous delivery & urban logistics |
| T01.2 | Smart cleaning & facility maintenance |
| T01.3 | Public-space service robots |
| T01.4 | Autonomous urban inspection |
| T01.5 | Smart guidance & information services |
| T01.6 | Autonomous navigation & path planning |
| T01.7 | Human-robot interaction in complex cities |

Judging (round 1, per track): **technical quality · innovation · real-world value · completeness**; one champion per track goes to the grand final (pitch + live robot demo). Details: [Event intel](../../Event/Event-Intel.md).
Which company has what for this track: [All solutions, projects and plans](T01-5-All-Solutions-and-Projects.md). The second-pass files `…-4-Solutions-Register-and-Papers.md` (where present) map a company onto these seven directions.
Source: [Leukerbad Robot Carnival website](https://www.leukerbad-robot-carnival.tech) — hackathon page.

## Official statement (fill in at kickoff)

- [ ] **Problem statement** (exact wording): 
- [ ] **Constraints and rules** (team size, indoor / outdoor, pre-built code, allowed cloud APIs): 
- [ ] **Judging criteria and weights**: 
- [ ] **Hardware allowed / allocated** (which robot, how many hours, shared or dedicated, SDK access level): 
- [ ] **Deliverables and deadlines** (demo slot, video, repo, pitch length, submission platform): 
- [ ] **Mentors for this track** (name, company, where to find them): 

Questions worth asking at kickoff if not answered:

- [ ] Is the demo judged **live on the robot**, by video, or both? Is a fallback video accepted?
- [ ] May robots leave the Sportarena (corridors, forecourt, street)? Who signs off on safety?
- [ ] Is teleoperation allowed in the final demo, and must it be disclosed?
- [ ] Is venue Wi-Fi good enough for cloud LLM / VLM calls, or should inference be local?
- [ ] Is there one overall ranking or a prize per track?

## What this track is probably about

*Interpretation — based on the tagline's three verbs (move, deliver, maintain), the announced hardware classes and how comparable events were framed.*

- **Move** = autonomous navigation in spaces shared with people: corridors, lobbies, forecourts, slopes and stairs. Expect emphasis on robustness around humans rather than on speed.
- **Deliver** = getting an item from A to B *and into someone's hands*: indoor delivery in hotels, clinics and venues, the "last 100 metres" from a vehicle or bus stop to a door, porter and luggage service.
- **Maintain** = upkeep of public space and facilities: cleaning, tidying, litter and bin monitoring, inspection rounds, reporting defects to a works crew.
- **Service interaction** is the fourth, implied theme: guide, wayfinding and concierge robots for a resort town whose guests greatly outnumber residents.
- **"City" will mean "Leukerbad-sized"**: the organisers stress "real robots meet real-world challenges" in "a small town in the Swiss Alps". Solutions that fit a 1,300-resident alpine spa village are likely to land better than generic megacity concepts.
- **Full system, not a model benchmark**: with humanoids, quadrupeds, arms and XR on site, judges will probably expect an end-to-end loop (perceive, decide, act, report) on real hardware.
- **Overlap to manage**: clinic logistics borders on T04 (elderly care); bin and energy optimisation borders on T03; hazard patrol borders on T02. Pitch the *service operations* angle to stay clearly in T01.
- **Out of scope in practice**: road-legal autonomous vehicles. Nobody builds a street-driving delivery van in 48 hours, and public-road operation is regulated (see Safety section).

## Problem archetypes

| # | Problem | Who feels it | What the robot does | Hardware class | 48 h |
|---|---|---|---|---|---|
| 1 | Indoor point-to-point delivery (linen, meals, parcels, therapy aids) | Hotel, spa and clinic staff | Takes an order, drives a mapped route, announces arrival, confirms handover | Wheeled dual-arm or any mobile base | ● |
| 2 | Last 100 metres outdoors (slopes, kerbs, stairs) | Couriers, hotels, guests with luggage | Carries a load from vehicle or bus stop to the door over rough ground | Quadruped | ◐ |
| 3 | Fetch and hand over (pick an item, bring it, give it) | Reception, bar, ward staff | Finds the named object, grasps it, navigates, hands it over safely | Wheeled dual-arm, humanoid | ◐ |
| 4 | Tidying and surface cleaning (tables, litter, lost items) | Venue and municipal cleaners | Detects items, picks them, sorts into bins; wipes a defined surface | Mobile manipulator, arm on a cart | ◐ |
| 5 | Facility inspection rounds (lights, leaks, doors, blocked exits, full bins) | Facility managers, works department | Patrols waypoints, takes images, a VLM flags anomalies, files a ticket | Quadruped, any mobile base | ● |
| 6 | Waste-collection logistics | Municipal works, hotels | Estimates bin fill level, plans collection order, optionally hauls a bin or bag | Camera plus compute; quadruped or mobile base | ● (sensing) / ◐ (hauling) |
| 7 | Guide, wayfinding and concierge | Tourists, older guests, event visitors | Answers questions in several languages, walks the person to the destination | Humanoid, quadruped, wheeled dual-arm | ● |
| 8 | Winter pavement and access patrol (ice, snow, obstacles) | Works crew, pedestrians with reduced mobility | Walks a route, detects and geo-tags hazards, reports priorities | Quadruped | ◐ |
| 9 | Operating building infrastructure (lift buttons, doors, switches) | Any robot that must cross floors | Locates a button or handle and actuates it with force control | Force-controlled arm, dexterous hand | ◐ |
| 10 | Remote-operated service ("remote hands") | Small towns with staff shortages | An operator in XR does the hard part; autonomy does transit and simple skills | XR glasses plus humanoid or dual-arm | ● |
| 11 | Digital twin for robot operations | Municipality, facility owner | Scans a site in 3D, produces a navigable map with slopes, stairs, no-go zones | Handheld LiDAR scanner plus compute | ● |
| 12 | Multi-robot dispatch across vendors | Operator of a mixed fleet | One task broker assigns jobs to different robots and tracks status | Compute plus two or more robots | ◐ |
| 13 | Street-driving autonomous delivery vehicle | Logistics firms | Drives on public roads without a driver | Not on site | ○ |
| 14 | Mechanical snow clearing or street sweeping | Works department | Clears or sweeps large areas | Not on site (needs purpose-built machine) | ○ |

## Leukerbad scenarios

Facts first (sourced), then the scenario (interpretation).

| Fact | Value | Source |
|---|---|---|
| Residents | **1,329** (Dec 2020) | Wikipedia |
| Overnight stays | **725,103** in FY 2023/24; record **777,663** in 2021/22 | My Leukerbad AG annual reports |
| Guests vs residents | about **2,000 overnight guests on an average night**, i.e. roughly 1.5 guests per resident (own calculation: 725,103 / 365) | derived |
| Thermal water | **3.9 million litres per day**, up to **51 °C**, 65 springs (8 most productive in use), 22–30 pools depending on source | Valais Tourism, Leukerbad brochure, Wikipedia |
| Jobs | about **49 %** in hotels and restaurants, about **18 %** in health care (2008) | Wikipedia |
| Access | road only, from the south via Leuk; the electric railway closed in **1967** | Wikipedia |
| Terrain and climate | village at **1,411 m**; 67.2 km² of which about 74 % unproductive land; **1,188 mm** precipitation per year, December wettest; historic avalanche damage | Wikipedia |
| Rehabilitation | Leukerbad Clinic: musculoskeletal, internal-medicine and oncological rehabilitation (bed count ⚠️ unverified) | Krebsliga flyer, MySwitzerland |
| Municipal finances | first Swiss municipality to go bankrupt (**CHF 346 M** debt by 1998; under cantonal administration 1998–2004) | Wikipedia |
| Languages | German first language for about 83 % of residents; about 40 % foreign nationals (2008) | Wikipedia |

1. **Bath and hotel linen runs.** Several thermal-bath complexes and many hotels move towels, bathrobes and laundry all day, and hospitality is the largest employer. A mobile robot shuttles linen between laundry, reception and pool entrance on request. Demo: order by voice or QR, autonomous run, handover confirmation. Watch out: wet floors and steam near pools.
2. **Clinic and hotel internal logistics.** Rehabilitation clinics and hotels need many small transports (therapy aids, meals, parcels). A wheeled dual-arm robot does fetch-and-deliver between two rooms and hands the item over. Keep the pitch on logistics so it stays in T01, not T04.
3. **Arrival porter for the last 100 metres.** Guests arrive by road only and then face steep lanes and steps with luggage. A quadruped carries a bag or parcel from the drop-off point to a door while following or leading the guest. Payload and stairs are the honest limits to show.
4. **Winter pavement patrol.** High precipitation, a December peak and an older guest population (inference from the spa and rehabilitation profile) make icy paths a daily service issue. A quadruped walks a fixed loop at dawn, geo-tags ice, snow ridges and blocked ramps, and sends a prioritised list to the works crew.
5. **Multilingual concierge and guide.** Residents are mainly German-speaking while guests are international. A robot at the Sportarena or a bath lobby answers "where is…", "when does … open" in German, French and English and walks the guest there. Ground answers in a small local knowledge file to avoid hallucinated opening hours.
6. **Peak-season litter and bin logistics.** Municipal services are sized for about 1,300 residents but must serve a guest population that is larger than the resident one, with a constrained budget history. A robot (or just cameras on a robot doing other rounds) estimates bin fill and litter hotspots; a dashboard proposes the collection route.
7. **Venue upkeep at the Sportarena.** The hackathon venue itself is the most demo-able "facility": a night inspection round that checks doors, lights, spills and blocked exits, then files tickets with photos.
8. **3D twin of the village core.** A handheld LiDAR scan of the venue forecourt and adjacent lanes becomes a slope-and-stairs-aware map that tells each robot class where it may go. Useful as the shared base layer for any of the scenarios above.

## What judges will likely reward

**No official criteria are published yet.** The event page says prizes go to "the most creative, ambitious and technically outstanding teams" and that judges come from industry, universities, venture capital and startups. A separate Leukerbad startup pitch competition is listed for 15 Nov (per its Luma listing: 1st place CHF 5,000, community prize CHF 1,000), which signals a commercial lens on the weekend.

What comparable events used:

| Event | Framing | Published criteria / what won |
|---|---|---|
| Intel Physical AI Challenge, European Robotics House (Zurich, 4–6 Dec 2026; residency co-created by EuroTech Federation, ESRA and EIII) | One task: "a robot that sees, thinks, and acts" — vision-based defect sorting with an SO-101 arm, 40 h, teams of 3–4, prizes EUR 5,000 / 3,000 / 2,000 | Live demonstrations before judging; weights not published |
| Europe Embodied 2026, TUM International (48 h, 108 selected from 350+ applicants) | Three partner tracks: industrial arms with VLMs, autonomous quadruped inspection, drone racing | 1st: a system letting a VLM-driven robot use physical properties such as weight; 2nd: a drone clearing the gate course in **8 s**, 3 s ahead of the runner-up; 3rd: an agentic inspection system |
| NVIDIA robotics hackathon (2026, USD 5,000 top prize) | Open robotics / physical-AI builds | Technical implementation, design, potential impact, quality of the idea |
| AMD AI DevMaster, Physical AI track (2026) | ROS developers, local inference | 100-point scale; functional completeness, practical / application value and innovation carry **60–80 points** depending on the version |
| Embodied AI Hackathon 2025 (NVIDIA, Hugging Face, Seeed; 100+ participants, 15+ teams) | Home and cooking tasks with VLA models on edge compute | Working real-robot VLA demos |

Likely rubric for T01 (inference; replace with the real one at kickoff):

| Probable criterion | What it means here | How to score on it |
|---|---|---|
| Technical execution | Does it work live, on the real robot, more than once? | Show 3 consecutive runs; show one recovery from a failure |
| Real-world impact | Is it a real problem for a real operator? | Name the operator (bath, hotel, clinic, works crew) and the minutes or francs saved |
| Innovation / ambition | Is there one thing others did not do? | One crisp new capability, not five half-working ones |
| Use of provided hardware | Did you use what the sponsors brought? | Use a robot's distinctive strength (legs on stairs, force control on buttons, XR for teleop) |
| Presentation and viability | Can a VC or a municipality see the next step? | One slide: user, cost per task, deployment path, regulation |

What distinguished winners elsewhere (inference from the results above): a **narrow, measurable claim** ("8 seconds", "uses weight as an input") demonstrated end to end, rather than a broad vision with a partial demo.

## KPIs you can show in a 3-minute demo

| KPI | How to measure in the venue | Target worth quoting |
|---|---|---|
| Task success rate | n successful out of N attempts, logged over the weekend | State N honestly (e.g. 8 of 10) |
| Autonomy share | Runs or metres without human intervention; interventions per run | Zero interventions in the live run |
| Time per task | Order placed to handover confirmed, versus a human doing the same walk | Within 2–3x human time is credible |
| Navigation robustness | Reaches goal with a person stepping into the path; replans without stopping the demo | Shown live once |
| Handover or grasp success | Successful grasps or handovers out of attempts | State both numbers |
| Interaction latency | Speech in to speech out, in seconds | Under about 2 s feels natural (rule of thumb) |
| Detection quality | Hazards, bins or litter items found versus planted | Plant 5, find 5; show one false positive honestly |
| Coverage | Area or waypoints patrolled per battery charge or per hour | Extrapolate to a named Leukerbad route |
| Cost per task | Robot time and amortisation versus staff minutes (state assumptions) | One line, clearly labelled estimate |
| Setup time for a new site | Minutes to map a new room and run the first mission | Strong differentiator for small towns |

## Safety, ethics and regulation

- **Public roads:** Switzerland's Ordinance on Automated Driving has been in force since **1 March 2025**. It covers motorway pilots, driverless vehicles on **canton-approved routes** supervised from a control centre, and automated parking. The sources found do not address pavement delivery robots, so assume any outdoor operation on public ground needs explicit permission (⚠️ unverified — ask the organisers before leaving the venue).
- **People nearby:** a humanoid, quadruped or arm in a crowd of about 220 participants is the main real risk. Keep a person on the emergency stop, cap speed, mark a demo zone, never hand over sharp or hot items, and treat children and older visitors as untrained bystanders.
- **Standards to name in the pitch** (from background knowledge, not re-checked today ⚠️ unverified): ISO 13482 for personal-care and service robots; ISO 10218 with the collaborative-operation guidance of ISO/TS 15066 for arms working near people; the EU Machinery Regulation 2023/1230 for products placed on the EU market from 2027.
- **Cameras and microphones in public space:** patrol and concierge robots record people. Process on the robot where possible, blur faces, store no audio, and show a visible notice. Swiss data-protection law (revised FADP) applies to any real deployment (⚠️ unverified detail — not checked today).
- **Honest autonomy:** disclose teleoperation and scripted steps. Swiss Post frames its robot test as assistance, stating that people remain indispensable for parcel delivery; a "robot supports the crew" story is both more accurate and more acceptable locally than a "robot replaces staff" story.
- **Jobs and acceptance:** in the Sion SmartShuttle trial (Valais), people who had ridden the shuttles were clearly more positive about them, and a 2016 collision with a van tailgate took both vehicles out of service for two weeks. Lesson: let judges and bystanders interact with the robot, and show how it fails safely.
- **Wet, cold and steep:** pool decks, snow and slopes are outside the rated envelope of most research platforms. Check the ingress-protection rating and slope limits of the specific robot before promising a bath or winter scenario.

## Decision helper: which hardware class for which archetype

| Archetype | Humanoid | Wheeled dual-arm | Quadruped | Arm / cobot | XR | Scanner / compute |
|---|---|---|---|---|---|---|
| 1 Indoor delivery | ◐ | ● | ◐ | ○ | ○ | ◐ |
| 2 Last 100 m outdoors | ◐ | ○ | ● | ○ | ○ | ◐ |
| 3 Fetch and hand over | ◐ | ● | ○ | ◐ | ◐ | ◐ |
| 4 Tidying and cleaning | ◐ | ● | ○ | ● | ◐ | ◐ |
| 5 Inspection rounds | ◐ | ◐ | ● | ○ | ◐ | ● |
| 6 Waste logistics | ○ | ◐ | ◐ | ◐ | ○ | ● |
| 7 Guide and concierge | ● | ● | ◐ | ○ | ◐ | ◐ |
| 8 Winter pavement patrol | ○ | ○ | ● | ○ | ○ | ● |
| 9 Lift buttons and doors | ◐ | ● | ○ | ● | ○ | ○ |
| 10 Remote hands (teleop) | ● | ● | ◐ | ◐ | ● | ○ |
| 11 Digital twin | ○ | ○ | ◐ | ○ | ◐ | ● |
| 12 Multi-robot dispatch | ◐ | ● | ● | ◐ | ◐ | ● |

How to read it (inference, to be checked against the actual robots on the bench):

- **Wheeled dual-arm mobile manipulators** are the safest all-round choice for T01: stable base, standard navigation stack, two arms for handover.
- **Quadrupeds** win wherever the story involves slopes, stairs, snow or long patrols; they are weak at manipulation unless an arm is mounted.
- **Humanoids** win on presence and human-like interaction; whole-body autonomy is the hardest thing to make reliable in 48 hours, so pair them with teleoperation or keep them stationary.
- **Arms and cobots** fit a fixed "service station" (sorting, button pressing, parcel locker) and are the most reliable to demo.
- **XR glasses, LiDAR scanners and edge compute** are multipliers, rarely a project on their own: use them for operator interfaces, maps and on-robot inference.

## Sources

- [Leukerbad Hackathon 2026 (Robotics, XR, and AI) — Luma](https://luma.com/vj13ns00)
- [Leukerbad Robotics Hackathon — BuilderBase event page](https://builderbase.com/event/leukerbad-robotics-hackathon)
- [Leukerbad Startup Pitch Competition — Luma](https://luma.com/2spvzh2r)
- [Intel Physical AI Challenge | European Robotics House — Luma](https://luma.com/d3pjvggt)
- [Europe Embodied 2026: 48-Hour Hackathon — TUM International](https://tum-international.com/europe-embodied-2026-48-hour-hackathon/)
- [NVIDIA launches robotics hackathon with $5,000 top prize — Robotics and Automation News](https://roboticsandautomationnews.com/2026/02/08/nvidia-launches-robotics-hackathon-with-5000-top-prize-to-spur-physical-ai-development/98768)
- [AMD AI DevMaster Hackathon, Physical AI track — Open Robotics Discourse](https://discourse.openrobotics.org/t/opportunity-for-ros-developers-amd-ai-devmaster-hackathon-physical-ai-track/56629)
- [2025 Embodied AI Hackathon recap — Seeed](https://seeed.cc/post/2025-embodied-ai-hackathon-recap)
- [Leukerbad — Wikipedia](https://en.wikipedia.org/wiki/Leukerbad)
- [Leukerbad — Valais Tourism](https://www.valais.ch/de/orte/leukerbad-region/leukerbad)
- [Thermal water brochure — Leukerbad](https://leukerbad.ch/assets/content/images/general/Thermalwasser/Brosch%C3%BCre-Thermalwasser-Leukerbad_EN.pdf)
- [My Leukerbad AG annual report 2023/24](https://leukerbad.ch/assets/content/documents-website/Dokumente-Torismusorganisationen/MyLeukerbad-AG/My_Leukerbad_GB_2023_24_A4_web.pdf)
- [My Leukerbad AG annual report 2022/23](https://leukerbad.ch/assets/content/documents-website/Dokumente-Torismusorganisationen/MyLeukerbad-AG/My_Leukerbad_GB_2022_23_A4_web.pdf)
- [Leukerbad Clinic, oncological rehabilitation flyer — Krebsliga](https://www.krebsliga.ch/fileadmin/downloads/onkoreha/stationaer/flyer-leukerbad-clinic-onkologische-rehabilitation.pdf)
- [Rheumatology and rehabilitation centre Leukerbad — MySwitzerland](https://www.myswitzerland.com/en/experiences/rheumatology-and-rehabilitation-centre/)
- [Swiss Post tests the use of auxiliary robots for parcel delivery — SWI swissinfo.ch](https://www.swissinfo.ch/eng/research-frontiers/swiss-post-tests-the-use-of-auxiliary-robots-for-parcel-delivery/89940924)
- [Automated driving — Federal Roads Office ASTRA](https://www.astra.admin.ch/astra/en/home/topics/intelligent-mobility/automated-driving.html)
- [Swiss Federal Council greenlights automated driving ordinance — SAAM](https://www.saam.swiss/swiss-federal-council-greenlights-automated-driving-ordinance/)
- [Initial study indicates public acceptance for self-driving buses — PostAuto](https://www.postauto.ch/en/about-us-and-news/media/press-releases/2017/initial-study-indicates-public-acceptance-for-self-driving-buses)
- [Swiss driverless buses a hit despite accident — Le News](https://lenews.ch/2017/06/30/swiss-driverless-buses-a-hit-despite-accident/)
