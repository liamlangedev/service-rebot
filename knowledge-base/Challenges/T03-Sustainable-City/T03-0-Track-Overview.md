---
type: track-overview
challenge: T03
challenge_title: "Sustainable City"
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, track]
---
# T03 Sustainable City — Track Overview

> **Official tagline:** Automation for lower emissions, less waste, smarter resources.

[Start here](../../00-START-HERE.md) · [Solution patterns](T03-1-Solution-Patterns.md) · [Hardware shortlist](T03-2-Hardware-Shortlist.md) · [Cross-vendor solutions](T03-3-Cross-Vendor-Solutions.md)

**Status of this page:** the organisers have published only the track title and tagline. Everything below the kickoff checklist is preparation material: sourced facts are cited, interpretation is labelled, and anything not confirmed today is marked "⚠️ unverified".

**Timeline that is published** (Leukerbad Robot Carnival page on Luma): kickoff **Sat 14 Nov, 11:00** · submission deadline **Mon 16 Nov, 13:00** · final pitches, live demos and jury **Mon 16 Nov, 13:30–17:00**. That is roughly **50 hours** from kickoff to submission.

## Official directions for this track

> **Official tagline (carnival website):** "Use robotics to drive a greener, more sustainable future."

The organizers publish seven example directions per track. Tracks are **open**: the team defines its own problem, platform and approach inside the theme. Verified on the official site on 2026-11-14.

| # | Official direction |
|---|---|
| T03.1 | Smart waste sorting & collection |
| T03.2 | Environmental monitoring robots |
| T03.3 | Energy-efficient robotic systems |
| T03.4 | Sustainable urban infrastructure |
| T03.5 | Water & energy management |
| T03.6 | Smart recycling & resource optimization |
| T03.7 | Environmental data collection & analysis |

Judging (round 1, per track): **technical quality · innovation · real-world value · completeness**; one champion per track goes to the grand final (pitch + live robot demo). Details: [Event intel](../../Event/Event-Intel.md).
Which company has what for this track: [All solutions, projects and plans](T03-5-All-Solutions-and-Projects.md). The second-pass files `…-4-Solutions-Register-and-Papers.md` (where present) map a company onto these seven directions.
Source: [Leukerbad Robot Carnival website](https://www.leukerbad-robot-carnival.tech) — hackathon page.

## Official statement (fill in at kickoff)

- [ ] **Problem statement** (exact wording): 
- [ ] **Constraints and rules** (team size, pre-built code, allowed APIs / cloud, where robots may operate, outdoor use): 
- [ ] **Judging criteria and weights**: 
- [ ] **Hardware allowed / allocated** (which vendor, how many units, booking slots, who supports it): 
- [ ] **Deliverables and deadlines** (repo, video, slides, live demo length; published deadline is Mon 13:00 — confirm): 
- [ ] **Mentors for this track** (names, vendor engineers, when they are on the floor): 

Questions worth asking in the kickoff Q&A:

- [ ] Is the track judged on a **live robot demo**, or is a video acceptable as fallback?
- [ ] Must the impact claim (CO2, kWh, kg waste) be **measured**, or is a reasoned estimate accepted?
- [ ] Is there a **real local stakeholder** (municipality, spa operator, hotel, clinic) whose problem we can adopt?
- [ ] May robots leave the Sportarena (snow, slopes, public space)?
- [ ] Are track prizes separate, or is there one overall ranking across the four tracks?

## What this track is probably about

*Interpretation — not official. Based on the tagline, the hardware announced, and the organisers' "Living Lab" framing of the Robot Carnival (robots in hotels, thermal spas, hospitals, restaurants and public spaces).*

- **Three levers are named in the tagline**: lower emissions (energy, transport), less waste (sorting, litter, circularity), smarter resources (water, heat, materials). A project should pick **one** lever and quantify it.
- **Physical action is the differentiator.** With about CHF 1M of robots on site, a pure dashboard or app will probably look thin; the expected shape is *sense → decide → act* on real objects.
- **Waste sorting and litter are the most "robot-shaped" problems** in this track: visible, tangible, easy to demo, easy to count.
- **Energy and water problems are mostly sensing problems.** The robot's role there is a mobile sensor / inspector (thermal leaks, meters, open windows, plant rooms) feeding a decision layer.
- **Leukerbad is the test case.** The Carnival describes the whole town as a testing ground and runs a Smart City Forum on 15 Nov (topics include sustainability and urban services). A solution framed for an alpine spa resort will likely land better than a generic city solution (inference).
- **Net benefit matters.** A robot that uses more energy than it saves is an obvious judge question. Be ready with an energy-per-task figure.
- **Overlap with other tracks is real**: delivery and maintenance sit in T01, monitoring of hazards in T02. For T03, state the sustainability metric explicitly, otherwise the project reads as a T01/T02 entry.
- **Signal from the same organiser network**: the next European Robotics House hackathon (Intel Physical AI Challenge, Zurich, 4–6 Dec 2026) asks teams to detect defective objects with vision and sort them with a robotic arm. Vision-guided sorting is evidently seen as the right size for a 40–48-hour build.

## Problem archetypes

Feasibility: ● easy · ◐ stretch · ○ unrealistic in 48 hours (my assessment, assuming a team of 3–5 and one robot).

| # | Problem | Who feels it | What the robot does | Hardware class | 48-hour feasibility |
|---|---------|--------------|---------------------|----------------|---------------------|
| 1 | Recyclables end up in residual waste; guests do not know local sorting rules | Municipality, hotels, event venues | Recognises items on a table or belt and places them in the correct bin; logs counts | Arm / cobot + RGB-D camera | ● |
| 2 | Litter on paths, promenades, lift stations and meadows | Municipal works, tourism office | Finds litter, approaches, picks, deposits; maps hotspots | Quadruped or wheeled base with arm; wheeled dual-arm | ◐ |
| 3 | Food and tray waste in hotels, clinics and restaurants | Kitchens, housekeeping | Clears trays, separates organics / PET / glass, weighs food waste | Wheeled dual-arm, humanoid | ◐ |
| 4 | Heat loss and wasted energy in buildings (open windows, lights, empty heated rooms) | Building owners, facility managers | Patrols, detects anomalies with thermal / RGB camera, reports or acts | Quadruped or wheeled base + thermal camera | ● as sensing, ◐ with acting |
| 5 | Meters, gauges and plant rooms are read by hand or not at all | Utilities, spa operators | Reads analog meters and gauges, checks for leaks, files a report | Quadruped + camera, edge compute | ● |
| 6 | No dense local data on air, water, snow, noise, vegetation | Municipality, environment office | Carries sensors along a route, builds a geo-referenced layer | Quadruped / wheeled base + sensors, LiDAR scanner | ● |
| 7 | EV charging needs a human to plug in; chargers are blocked by parked cars | Car-park operators, fleets | Locates the inlet and plugs / unplugs a connector with force control | Force-controlled arm (mock inlet, unpowered) | ◐ |
| 8 | Products are discarded instead of repaired or dismantled | Repair shops, rental shops, recyclers | Triage, unscrewing, part separation, battery removal | Arm + dexterous hand, teleoperation | ◐ single step · ○ full disassembly |
| 9 | Green spaces and planters need care; water is wasted | Park services, hotels | Inspects plants, waters by need, removes weeds or dead leaves | Arm on mobile base, humanoid | ◐ |
| 10 | Many half-empty trips for supplies, linen, waste | Hotels, clinics, logistics | Consolidates loads, carries bins or linen, plans shared routes | Wheeled dual-arm, quadruped (payload) | ◐ (overlaps T01) |
| 11 | Retrofit and energy planning lacks an as-built model | Owners, planners, municipality | Scans the building in 3D; software flags leaks, PV area, insulation gaps | Handheld LiDAR scanner + compute | ● (little robotics) |
| 12 | Humans sort or repair wrongly or slowly | Guests, staff, volunteers | AR overlay shows the right bin or the next repair step; robot handles the rest | XR glasses + camera, optional arm | ● |

Cross-cutting angle (not a row): **low-power edge AI** — run the perception stack on an edge board and report watts and Wh per task. It strengthens any of the rows above.

## Leukerbad scenarios

Facts first, then the use case. Use-case fit is my inference unless stated.

| # | Sourced facts | Scenario |
|---|---------------|----------|
| 1 | About **3.9 million litres** of thermal water per day emerge at up to **51 °C**. At the Burgerbad the spa uses about **20 %** of the spring water; wastewater leaves at about **30 °C**; two heat exchangers recover roughly **450 kW** and a heat pump delivers **over 1 MW** for heating (Huber case study). Own back-of-envelope: 3.9M l/day ≈ 45 l/s; cooling that flow from 51 °C to 10 °C would be an upper bound of about **7–8 MW thermal** (assumes all water at 51 °C, which is not the case). | **Thermal-energy inspector.** A quadruped does plant-room rounds: reads gauges, checks heat-exchanger and pipe temperatures with a thermal camera, flags leaks and fouling. Pitch: keep every recovered kW online. |
| 2 | **72.5 %** of apartments were seasonally occupied (2000 census, old figure); resident population **1,329** (Dec 2020). | **Empty-apartment energy watch.** Occupancy-aware heating for holiday flats: a patrol robot or façade thermal scan finds heated-but-empty units, open tilt windows, lights left on. |
| 3 | The destination recorded **725,103 overnight stays** in business year 2023/24 (750,839 the year before), per the My Leukerbad AG annual report as surfaced in search (PDF not opened by me). Own arithmetic: about **1,990 guest-nights per average day** versus 1,329 residents. Swiss municipal waste in 2024: about **670 kg per person**, about **6 Mt** in total, a little over half recycled. | **Guest-proof sorting station.** Visitors from many countries do not know Swiss sorting rules. Arm-based sorter or AR "which bin" helper at hotel, spa or event exits; multilingual voice. |
| 4 | **511 jobs** (49 % of tertiary jobs) were in hotels and restaurants (2008, old figure). | **Buffet and tray waste.** Tray-return cell that separates organics, PET and glass and weighs food waste per meal service. |
| 5 | About **1,188 mm** precipitation and about **122 precipitation days** per year; wettest month December. Village at **1,411 m**; the municipality reaches up to 3,698 m (Balmhorn). | **Snow and ice resource saver.** Robot or sensor patrol measures ice and snow on walkways so that grit and salt go only where needed; a snow-depth and surface-temperature layer for winter services. (Overlaps T02 — keep the metric on salt, fuel and trips saved.) |
| 6 | Torrent ski area with about **50 km** of runs; Gemmi Pass at 2,322 m with cable car; via ferrata on the Daubenhorn. | **Trail and lift-station litter scout.** Legged robot finds and maps litter after snowmelt or events on terrain that wheeled sweepers cannot reach. |
| 7 | The railway to Leukerbad closed in **1967**; access is by road. | **Shared charging robot in a car park.** One mobile or rail-mounted arm serves several bays instead of one charger per bay (pattern used by Rocsys M1 and Kiwi Charge). ⚠️ unverified: number and type of public chargers in Leukerbad. |
| 8 | The hackathon itself: about **220 participants** for three days in the Sportarena. | **Eat your own dog food.** Sort and count the event's real waste stream, or audit the hall's energy use, and present measured numbers from the weekend. Strongest evidence you can get in 48 hours. |

Not confirmed today (⚠️ unverified): number of guest beds, names and bed counts of the rehabilitation clinics, the municipality's waste-collection scheme and fees, district-heating coverage, local EV-charger count. Ask a local mentor or the municipality at kickoff.

## What judges will likely reward

**What comparable events publish**

| Event | What is public about judging | Source quality |
|-------|------------------------------|----------------|
| Leukerbad Hackathon 2026 | No criteria published. Format: submission, then **final pitches + live demos + jury**. Judges and mentors from robotics industry, universities, venture capital and startups. | Official Luma pages |
| Intel Physical AI Challenge (2nd European Robotics House hackathon, Zurich, 4–6 Dec 2026) | Criteria not published. One task: "see, think, act" — vision finds defective objects, arm sorts them. Judging with **live demonstrations**. Teams of 3–4, 40 hours. | Official Luma page |
| TUM robo.innovate Hackathon 2026 (5th edition, 23–28 Oct 2026) | Criteria not published. Teams build **working prototypes** on partner challenges and **pitch to a jury**. The 2023 edition ran as a "Circular Hackfest". | Official page |
| RoboTech (Georgia Tech IEEE, sustainability theme year) | Design track judged on **execution, complexity, contribution to sustainability, creativity**. | Search summary of the Devpost page; page not opened ⚠️ |
| McGill RoboHacks | Sustainability was part of the criteria, including **using as little material as possible** and reusable parts. | Search summary; page not opened ⚠️ |

**Planning assumption (inference, replace with the real rubric at kickoff)**

| Likely criterion | What it means in practice | How to score |
|------------------|---------------------------|--------------|
| Working demo | The robot does the task live, more than once | Rehearse 10 runs; show the success count honestly |
| Impact | A number tied to the tagline: kg, kWh, CO2e, litres | One headline KPI, measured on site, with a transparent extrapolation |
| Technical depth | Real perception and control, not a scripted replay | Show unseen objects, a recovery from failure, a live map |
| Real-world fit | Would the town, a hotel or a utility use it | Name the operator, the workflow, the cost per unit of benefit |
| Novelty | A fresh angle on a known problem | Combine hardware classes or add a twist (thermal + legged, AR + arm) |
| Pitch | Clear story in 3 minutes | Problem in 20 s, demo in 90 s, numbers in 40 s, ask in 30 s |

**What separates winners (inference from the formats above)**

- A **closed loop on real hardware** beats a broader concept shown in slides.
- **One measured number** beats five estimated ones.
- **A local owner of the problem** (named person or organisation) beats "cities in general".
- **Graceful failure**: a visible fallback (teleoperation, human confirm) when autonomy fails during the demo.
- **Honest net accounting**: energy used by the robot and compute versus energy or material saved.

## KPIs you can show in a 3-minute demo

| KPI | How to measure in the hall | Reference point |
|-----|----------------------------|-----------------|
| Sorting accuracy (%) and contamination rate | Confusion matrix over 50–100 items the model has not seen | Vendor case study: Recycleye reports 99 % target purity |
| Picks per minute | Stopwatch over a 2-minute run | Industrial cells: about 55–104 picks/min (vendor-reported). A hackathon arm at 4–10/min is respectable (my estimate) |
| Mass or items diverted | Kitchen scale under each bin; extrapolate per day with stated hours | Glacier cell in Sarasota: over 35,000 items/day (news report) |
| Area covered (m²/h) and litter recall | Mark out a test patch, seed 20 items, count found | Angsa litter robot: about 1,000 m²/h (vendor spec) |
| Energy anomalies found | Number and kW estimate of leaks / open windows on a fixed route | Compare with a manual walk of the same route |
| kWh or CO2e avoided | Measured delta × a **cited** emission factor (do not invent one) | State factor and source on the slide |
| Robot energy per task (Wh) | Battery percentage or power meter before and after | Needed for net-benefit claim |
| Edge inference cost (W, ms per frame) | Board power draw and latency on screen | Compare with cloud or laptop GPU |
| Autonomy rate | Human interventions per 10 runs | Report it even if it is not zero |
| Plug-in success and time (EV) | Successes out of 10, seconds per attempt, peak contact force | Rocsys cites 99.9 % plug-in success in pilots (company claim, ⚠️ unverified) |
| Map completeness | Share of the route or building with sensor coverage | Show the heat map live |

## Safety, ethics and regulation

Specific to this track. Legal references are from prior knowledge and were **not re-checked today** (⚠️ unverified) — confirm with organisers before relying on them.

- **Waste is dirty and sharp.** Use clean mock waste (rinsed bottles, cans, paper). No broken glass, needles, organics or real residual waste near grippers or people.
- **Batteries and e-waste.** Do not puncture, crush or disassemble lithium cells or packs. For circular-economy demos use dead dummy cells or battery-free devices.
- **EV charging.** Demonstrate on an **unpowered mock inlet** only. No live AC or DC, no real vehicle paint in reach of the arm without padding.
- **Arms near people.** Keep collaborative speed and force low, define a marked cell, keep an emergency stop in hand. Relevant standards: ISO 10218 (industrial robots) and ISO/TS 15066 (collaborative operation).
- **Legged and humanoid robots.** Falls are the main hazard. Use the vendor's spotter rules, tether or gantry where required, and keep the crowd back.
- **Cameras in public and semi-public space.** Thermal and RGB patrols capture people, windows and number plates. Under the Swiss data-protection act (revised FADP, in force since Sept 2023) keep data minimal: process on the edge, blur faces and plates, do not store raw video, do not point thermal cameras into private rooms.
- **Spa and clinic settings.** No recording in bathing, changing or treatment areas. Get the operator's consent for any demo outside the hall.
- **Outdoor and alpine operation.** Cold reduces battery capacity; snow, ice and slopes change traction; keep robots away from roads and ski runs unless the organisers have cleared the area.
- **Drones.** Switzerland applies the EASA drone rules; assume no flying over people or the village without explicit clearance.
- **Wildlife and vegetation.** Litter and green-care robots should not disturb protected plants or animals on meadows and trails.
- **Greenwashing.** Label every extrapolation as such, cite emission factors, include the robot's own energy and hardware footprint.
- **Jobs.** Frame the robot as taking the dull, dirty or dangerous part of municipal work, and say who operates and maintains it.

## Decision helper: which hardware class for which archetype

● good fit · ◐ possible · ○ poor fit (my assessment by hardware class; the specific models on site are covered in the hardware shortlist).

| Archetype | Humanoid | Wheeled dual-arm | Quadruped | Arm / cobot | XR | Scanner / compute |
|-----------|----------|------------------|-----------|-------------|----|-------------------|
| 1 Recyclables sorting cell | ◐ | ● | ○ | ● | ◐ | ◐ |
| 2 Outdoor litter picking | ◐ | ◐ | ● (needs arm or scoop) | ○ | ○ | ◐ |
| 3 Tray and food-waste clearing | ◐ | ● | ○ | ● | ○ | ◐ |
| 4 Building energy patrol | ◐ | ◐ | ● | ○ | ◐ | ● |
| 5 Meter and plant-room inspection | ◐ | ◐ | ● | ○ | ◐ | ● |
| 6 Environmental monitoring route | ○ | ◐ | ● | ○ | ○ | ● |
| 7 EV charging plug-in | ○ | ◐ | ○ | ● (force control) | ○ | ◐ |
| 8 Disassembly and repair | ◐ | ◐ | ○ | ● (+ dexterous hand) | ● (teleop, guidance) | ◐ |
| 9 Green-space and plant care | ◐ | ● | ◐ | ● | ○ | ◐ |
| 10 Consolidated logistics | ◐ | ● | ◐ | ○ | ○ | ◐ |
| 11 Scan-to-twin for retrofit | ○ | ○ | ◐ (carries scanner) | ○ | ◐ | ● |
| 12 AR sorting or repair assistant | ○ | ○ | ○ | ◐ | ● | ● |

Quick rule (my view):

- **Want the safest path to a working demo?** Arm / cobot + camera on a table (rows 1, 3, 7).
- **Want the most "Leukerbad" story?** Quadruped + thermal or environmental sensing (rows 4, 5, 6), or legged litter scout (row 2).
- **Want the most impressive hardware on stage?** Humanoid or wheeled dual-arm on rows 3 or 9 — budget extra time for vendor SDK onboarding.
- **No robot slot available?** Scanner, XR and edge board still give a credible entry (rows 11, 12) if paired with one physical action.

## Sources

Event and comparable events
- [Leukerbad Hackathon 2026 (Robotics, XR, and AI) — Luma](https://luma.com/vj13ns00)
- [Leukerbad Robot Carnival 2026 — Luma](https://luma.com/yo2pk18n)
- [Leukerbad Startup Pitch Competition — Luma](https://luma.com/2spvzh2r) (search summary only)
- [Intel Physical AI Challenge | European Robotics House — Luma](https://luma.com/d3pjvggt)
- [TUM robo.innovate Hackathon](https://roboinnovate.mirmi.tum.de/hackathon/)
- [RoboTech 2026 listing — allhackathons.com](https://allhackathons.com/hackathon/robotech-2026) (search summary only)
- [McGill Engineering: For McGill Robotics, sustainability and innovation go hand in hand](https://www.mcgill.ca/engineering/node/9537) (search summary only)

Leukerbad and Switzerland
- [Leukerbad — Wikipedia](https://en.wikipedia.org/wiki/Leukerbad)
- [HUBER case study: heat recovery from thermal spa wastewater in Leukerbad](https://www.huber-se.com/case-studies/detail/leukerbad-in-switzerland-uses-huber-heat-exchanger-for-heat-recovery-from-thermal-spa-wastewater/)
- [My Leukerbad AG annual report 2023/24 (PDF)](https://leukerbad.ch/assets/content/documents-website/Dokumente-Torismusorganisationen/MyLeukerbad-AG/My_Leukerbad_GB_2023_24_A4_web.pdf) (figures taken from the search summary)
- [Swiss federal news release on 2024 municipal waste (BAFU)](https://www.bafu.admin.ch/de/newnsb/EcpWws7Ra2HcYI1J88uP4) (search summary only)
- [BAFU: state of waste management](https://www.bafu.admin.ch/en/state-wastemanagement) (search summary only)

State of the art used for reference points
- [A3 / automate.org: The next robotics opportunity may be hiding in our trash](https://www.automate.org/robotics/industry-insights/the-next-robotics-opportunity-may-be-hiding-in-our-trash) (search summary only)
- [FOX 13: How an AI-powered robot in Sarasota saves 35,000 recyclables a day](https://www.fox13news.com/news/how-ai-powered-robot-sarasota-saves-35000-recyclables-day) (search summary only)
- [GaLaBau trade fair news: autonomous garbage removal (Angsa Robotics)](https://www.galabau-messe.com/en/news/2024/article/autonomous-garbage-removal) (search summary only)
- [EV Wire: Rocsys unveils hands-free robotaxi charging system details](https://evwire.com/p/rocsys-unveils-hands-free-robotaxi-charging-system-details) (search summary only)
- [APMA: Kiwi Charge takes EV charging robot to showroom floor](https://www.apma.ca/post/kiwi-charge-takes-ev-charging-robot-to-showroom-floor-with-1-7-million-pilot-project) (search summary only)

Research note: the web-search quota for this session ran out before every planned check was done. Items marked "⚠️ unverified" or "search summary only" should be re-checked before they go on a slide.
