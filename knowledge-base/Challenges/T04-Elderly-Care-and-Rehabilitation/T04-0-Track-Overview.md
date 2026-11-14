---
type: track-overview
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, track]
---
# T04 Elderly Care & Rehabilitation — Track Overview

> **Official tagline:** Assistive robotics for independence, recovery and care.

[Start here](../../00-START-HERE.md) · [Solution patterns](T04-1-Solution-Patterns.md) · [Hardware shortlist](T04-2-Hardware-Shortlist.md) · [Cross-vendor solutions](T04-3-Cross-Vendor-Solutions.md)

**Status of this page:** the official detailed statement had not been published when this was written (the Luma listing gives only the four track names and no rules or criteria). Everything below the checklist is preparation material. Interpretation and inference are labelled; "⚠️ unverified" marks anything that could not be confirmed.

## Official directions for this track

> **Official tagline (carnival website):** "Let robots help people live healthier, more independent and dignified lives."

The organizers publish seven example directions per track. Tracks are **open**: the team defines its own problem, platform and approach inside the theme. Verified on the official site on 2026-11-14.

| # | Official direction |
|---|---|
| T04.1 | Daily living assistance for seniors |
| T04.2 | Smart care robots |
| T04.3 | Rehabilitation training robots |
| T04.4 | Mobility assistance & support |
| T04.5 | Human-robot interaction & companionship |
| T04.6 | Automation in care scenarios |
| T04.7 | Smart health monitoring & assistance |

Judging (round 1, per track): **technical quality · innovation · real-world value · completeness**; one champion per track goes to the grand final (pitch + live robot demo). Details: [Event intel](../../Event/Event-Intel.md).
Which company has what for this track: [All solutions, projects and plans](T04-5-All-Solutions-and-Projects.md). The second-pass files `…-4-Solutions-Register-and-Papers.md` (where present) map a company onto these seven directions.
Source: [Leukerbad Robot Carnival website](https://www.leukerbad-robot-carnival.tech) — hackathon page.

## Official statement (fill in at kickoff)

- [ ] **Problem statement** (exact wording): 
- [ ] **Constraints and rules** (team size, pre-built code, sim vs real robot, human-contact rules): 
- [ ] **Judging criteria and weights**: 
- [ ] **Hardware allowed / allocated** (which vendor, how many units, booking slots, who supports it): 
- [ ] **Deliverables and deadlines** (demo length, video, repo, slides, submission platform): 
- [ ] **Mentors for this track** (name, organisation, when available): 
- [ ] Are demos with a **real person in contact with the robot** allowed, or dummy only?
- [ ] Is the separate **Startup Pitch Competition (Nov 15)** open to hackathon teams?

## What this track is probably about

*Interpretation, based on the tagline, the event's hardware list and how comparable events frame the theme.*

- **Three verbs in the tagline map to three user groups.** "Independence" = older people at home or in a hotel/apartment; "recovery" = rehab patients (post-surgery, musculoskeletal, neurological); "care" = professional and family caregivers.
- **The scarce resource is caregiver time, not robots.** Swiss forecasts point to a large staffing gap (about **70,000** additional health and support staff needed by 2029, per Obsan as reported by Swissinfo). Projects that return minutes to nurses and therapists are easier to justify than projects that replace human contact.
- **Falls are the single biggest measurable problem.** BFU-based reporting puts Swiss fall deaths at **more than 1,700 per year**, overwhelmingly people aged 65+; hundreds of thousands are injured. Detection, prevention and post-fall response are all demo-friendly.
- **The hardware on site pushes towards physical interaction.** Force-controlled arms, dexterous hands, humanoids, wheeled dual-arm platforms, EMG wearables and AR glasses were announced. Expect the organisers to want robots doing something physical, not a chatbot on a screen.
- **Rehab is the local angle.** Leukerbad is a thermal-spa town with a rehabilitation clinic recognised since 1961; exercise coaching, force-controlled physio and AR-guided therapy fit the place.
- **Human-in-the-loop is acceptable and realistic.** The current state of the art in care humanoids (Waseda AIREC, 1X NEO) is explicitly teleoperation-first or remote-expert-assisted; shared autonomy is not a weakness in this domain.
- **Judges will include investors.** The Luma page names judges from industry, universities, venture capital and the startup ecosystem, so a credible user, buyer and deployment path matter alongside the demo.
- **Likely out of scope for a weekend:** anything load-bearing on a real person (lifting, transfers), anything invasive, and any claim of clinical efficacy.

## Problem archetypes

Feasibility: ● easy / ◐ stretch / ○ unrealistic in about 48 hours with a team of 3–5 and vendor SDK support.

| # | Problem | Who feels it | What the robot does | Hardware class | 48 h |
|---|---|---|---|---|---|
| 1 | **Fetch and carry** (dropped object, water, phone, walking aid) | Person with limited mobility; caregiver interrupted for small errands | Understands a spoken request, finds the object, picks it, hands it over safely | Wheeled dual-arm or humanoid; arm on a table for a reduced version | ◐ (● with teleop fallback) |
| 2 | **Fall detection and response** | Person living alone; night-shift staff | Detects a fall from pose, approaches, asks "are you OK", escalates with location and video snapshot | Quadruped or humanoid with camera; or fixed camera plus edge compute | ● |
| 3 | **Fall-risk prevention** (home hazard audit, gait and balance screening) | Older residents, physiotherapists, landlords of holiday apartments | Scans a room in 3D, flags trip hazards, thresholds, missing rails; or scores a sit-to-stand / walking test | Handheld LiDAR scanner plus compute; camera; AR glasses for overlay | ● |
| 4 | **Rehab exercise coaching** | Patients between therapy sessions; therapists with too many patients | Demonstrates the exercise, counts repetitions, scores range of motion and form, sends a session report | Humanoid (demonstrator) plus camera; or AR glasses; or screen plus camera | ● |
| 5 | **Force-controlled physio or massage** | Therapists (repetitive manual work); patients waiting for slots | Follows a body-surface path with a regulated contact force; stops on excess force or voice command | Force-controlled arm or cobot with force sensing | ◐ (dummy or forearm only) |
| 6 | **Medication and item delivery with reminders** | Patients with complex schedules; nurses doing rounds | Navigates to the room, identifies the person, hands over the right box, confirms intake, logs it | Wheeled platform or quadruped with payload; voice interface | ● |
| 7 | **Caregiver logistics and night rounds** | Nurses and care assistants | Carries linen, meals, samples; patrols corridors at night and reports anomalies (person out of bed, door open) | Quadruped or wheeled mobile base | ● to ◐ |
| 8 | **Companionship and cognitive stimulation** | Lonely or cognitively impaired older people; activity staff | Holds a conversation, runs memory or movement games, remembers the person, reports mood trends | Humanoid or desk robot with LLM voice agent | ● (but weak differentiation) |
| 9 | **Telepresence and tele-care with hands** | Remote therapist, doctor or family member | Lets a remote person see, talk and physically act (pass a glass, point, demonstrate) through the robot | Humanoid or wheeled dual-arm plus XR teleoperation | ◐ |
| 10 | **Intention interfaces (EMG, gaze, head, voice)** | People with weak grip, paralysis or amputation; rehab patients needing biofeedback | Turns muscle signals or head motion into robot arm or hand commands; shows activation as therapy feedback | EMG wearable plus arm or dexterous hand | ◐ |
| 11 | **Assisted eating and drinking** | People with upper-limb impairment; care staff at mealtimes | Picks up a bite or a cup, brings it near the mouth, waits for a ready signal | Arm with camera | ◐ (manikin only) |
| 12 | **Transfers, lifting, dressing, bathing** | Caregivers (back injuries); bed-bound patients | Repositions or lifts a person, puts on a garment | Humanoid or dual-arm with whole-body force control | ○ |

Notes on the ratings (inference):

- Row 12 is where the need is greatest and the research frontier is. The 2027 Physical Robot Caregiving Challenge still treats putting a T-shirt on a seated **manikin in simulation** as a competition-grade problem with a 15-minute time budget per episode.
- Rows 2, 3, 4 and 6 give the best ratio of visible result to engineering risk.
- Row 8 is easy to build and therefore crowded; it only stands out when combined with a physical function (rows 4, 6 or 2).

## Leukerbad scenarios

Sourced facts first, then the scenario (the scenario itself is interpretation).

| # | Local fact | Scenario |
|---|---|---|
| 1 | The Leukerbad Clinic (Rehazentrum Leukerbad) has been recognised by Swiss health authorities **since 1961** and focuses on musculoskeletal rehabilitation, oncology, internal and integrative medicine; a job listing gives about **130 employees**. | **Between-sessions rehab coach:** a humanoid or AR-glasses coach supervises prescribed post-surgery exercises in the patient lounge and sends the therapist a per-patient report (repetitions, range of motion, pain flag). |
| 2 | About **3.9 million litres** of thermal water at up to **51 °C** flow daily from **65 springs**; water-based physiotherapy is what the rehab clinic became known for. | **Dry-side helper for bath therapy:** the robot stays out of the water and handles escort from changing area to pool edge, towel and walking-aid delivery, and a slip watch on wet floors. Robots in the pool are not realistic. |
| 3 | **750,878 overnight stays** in business year 2024/25 against **1,329 residents** (2020). That is roughly **2,050 guests per night on average**, about 1.5 guests per resident (own calculation). In 2000, **72.5%** of apartments were seasonally occupied. | **Fall-safe holiday apartment:** a 10-minute handheld LiDAR scan of a rental flat or hotel room produces a hazard report (rugs, thresholds, bath entry, lighting, missing grab rails). A 2025 BFU survey found only **6%** of older respondents had ever had their home professionally checked. |
| 4 | Village at **1,411 m**; about **1,188 mm** precipitation on about **122 days** a year, December the wettest month. | **Winter walking escort:** a quadruped walks ahead of an older guest from hotel to bath, picks the cleared route, carries a bag, and raises an alarm with position if the person falls. |
| 5 | German-speaking municipality (82.8% German first language in 2000) with **39.5%** foreign nationals (2008) and an international guest mix. Hotels and restaurants made up about half of service-sector jobs (2008). | **Multilingual care concierge:** a voice agent on a mobile robot reminds guests of therapy appointments and medication in their own language and hands over to staff when unsure. |
| 6 | No railway since **1967**; the nearest acute hospitals are down in the Rhône valley (⚠️ unverified: exact distance and travel time). National forecast of about **70,000** additional health staff needed by 2029. | **Night rounds for a small clinic or care home:** one robot patrols corridors, checks that doors are closed and nobody is on the floor, and brings a tele-nurse on screen when something is off. |
| 7 | Rehab stays are time-limited and guests travel home afterwards (⚠️ unverified: typical length of stay in Leukerbad). | **Take-home tele-rehab:** the exercise programme captured with the robot or AR glasses in the clinic continues on the patient's phone at home; the Leukerbad therapist sees adherence on a dashboard. |
| 8 | The destination markets itself on thermal wellness and massage-type treatments (interpretation from tourism material). | **Force-controlled massage station:** a force-controlled arm performs a simple back or forearm routine with a hard force cap; pitched as extra capacity at peak season, not as a therapist replacement. |

## What judges will likely reward

**What is known for this event:** the Luma page says prizes go to teams that are "creative, ambitious, and technically outstanding", and that judges come from the robotics industry, universities, venture capital and the startup ecosystem. No weights or rubric were public at the time of writing.

**Criteria used at comparable events:**

| Event | Published criteria or scoring | What won |
|---|---|---|
| robo.innovate Hackathon 2025 (TUM MIRMI, Munich, 100+ participants, 10 challenges) | Business value, market demand, technical feasibility, scalability, novelty | A field robot plus data platform (champion), a Franka-arm unpacking cell with a robot-as-a-service model ("most scalable"), a custom-gripper container-lashing system ("best problem-solution fit") |
| robo.innovate Hackathon 2026 (5th edition, 23–28 Oct 2026) | Held partly at the MIRMI **Geriatronics** Campus; 2026 criteria and winners not found (⚠️ unverified) | — |
| AI Meets Robotics hackathon (lablab.ai, 2026) | Innovation, technical depth, market potential | Simulation-first projects |
| Hackster Embodied AI Hackathon | Rubric includes **documentation (30 points)**; remaining items not retrieved | — |
| PhyRC 2027 (Cornell EmPRISE and KAIST RIRO), robot-assisted dressing | Milestone points divided by time; averaged over randomised starts; failed runs count as zero | Phase 1 still running (submissions close 15 Dec 2026) |
| LabORA 2026 Assistive Robotics Hackathon (UPC, Barcelona) | Six challenges set by companies and research centres; "specialized jury"; three prizes of €2,000 | Not published on the page read |

**What distinguishes winners (inference from the above):**

1. **A working physical demo on the real robot**, shown live, with a recorded backup video.
2. **A named user and buyer.** "Physiotherapists at a 130-person rehab clinic" beats "the elderly".
3. **A number.** Success rate over N trials, seconds to alert, repetitions counted correctly, peak contact force. PhyRC-style milestone scoring is a good template for self-reporting.
4. **Problem-solution fit over raw complexity.** robo.innovate awards went to systems where robot, perception and a simple business model fit one concrete task.
5. **Visible safety thinking.** In this track a force limit, a stop word and a consent screen are part of the product.
6. **Clear documentation.** A README with architecture diagram and reproduction steps costs an hour and is explicitly scored in some rubrics.

## KPIs you can show in a 3-minute demo

| KPI | How to measure it quickly | Fits archetype |
|---|---|---|
| **Task success rate** (x of N trials) | Run 10 trials before judging, report honestly | 1, 6, 11 |
| **Time to complete** vs a human doing the same errand | Stopwatch, two runs each | 1, 6, 7 |
| **Fall-to-alert latency** (seconds) | Staged falls onto a mat, timestamp event and notification | 2 |
| **False alarms** on non-fall actions (sitting, bending, lying on a sofa) | 20 scripted actions | 2 |
| **Repetition-count accuracy** and **joint-angle error** | Compare with manual count and a goniometer or phone app | 4 |
| **Peak and mean contact force** (N) with the configured limit | Log from the arm's force sensor, plot live | 5 |
| **Autonomy ratio** (% of run without operator input) | Count interventions | 1, 9 |
| **Hazards found per room** vs a manual checklist | One room, two assessors | 3 |
| **Voice round-trip latency** and languages supported | Log speech-end to speech-start | 6, 8 |
| **Caregiver minutes saved per shift** (estimate, show assumptions) | Errands per shift × minutes per errand | 6, 7 |
| **Quick usability score** from 5 strangers at the venue | System Usability Scale, 10 questions | all |

Tip: put one KPI on screen during the demo as a live counter; judges remember what they saw move.

## Safety, ethics and regulation

*Short orientation, not legal advice. The standards and laws below are named from general knowledge and were not re-checked today; confirm the current edition before quoting one (⚠️ unverified versions).*

- **Physical contact.** Default to a manikin, a foam limb or the team's own forearm. No load-bearing on a person, no contact near head or neck, low speed, a hard force cap, a hardware emergency stop within reach, and one person whose only job is the stop button.
- **Relevant standards to name in a pitch.** ISO 13482 (personal care robots), ISO 10218 and ISO/TS 15066 (collaborative robots, contact force and pressure limits), IEC 80601-2-78 (rehabilitation robots).
- **Medical-device boundary.** A robot that claims to treat, diagnose or monitor a condition falls under medical-device rules (EU MDR; in Switzerland the Medical Devices Ordinance, supervised by Swissmedic). Phrase the hackathon project as assistance, coaching or logistics, and say that clinical validation would follow.
- **Do not over-claim efficacy.** Even for established rehab robots the evidence is mixed: reviews report that trials of stationary gait robots have not shown superiority over comparable conventional therapy. Claim more repetitions, better adherence or therapist time saved, which you can measure.
- **Data protection.** Video, pose, voice and health notes of patients are sensitive personal data under the Swiss Federal Act on Data Protection. Process on the edge where possible, store no raw video, show a consent screen, and blur bystanders in recordings made at the venue.
- **Remote operators.** Telepresence and teleoperation put a stranger's eyes in a bedroom. Show when a human is connected (light, sound) and let the user refuse.
- **Dignity and honesty.** Companion robots should not pretend to be human or a relative, especially with people who have dementia. Keep a human escalation path and let the person end the interaction.
- **Evidence on companionship is uneven.** Agency- and vendor-reported results are strong (for example a reported 95% loneliness reduction among ElliQ users), while small independent studies are more cautious. Present it as a complement to human contact.
- **Hygiene and environment.** Wipeable surfaces, no fabric grippers for food tasks, and keep robots away from wet pool areas.

## Decision helper: which hardware class for which archetype

● best fit · ◐ workable · ○ poor fit. "Scanner / compute" covers handheld LiDAR scanners, edge-AI boards, fixed cameras and wearables such as EMG bands. Confirm on site which units are actually bookable.

| Archetype | Humanoid | Wheeled dual-arm | Quadruped | Arm / cobot | XR | Scanner / compute |
|---|---|---|---|---|---|---|
| 1 Fetch and carry | ◐ | ● | ○ | ◐ (tabletop only) | ◐ (teleop) | ◐ |
| 2 Fall detection and response | ◐ | ◐ | ● | ○ | ○ | ● |
| 3 Fall-risk prevention | ○ | ○ | ◐ (carries scanner) | ○ | ● (overlay) | ● |
| 4 Rehab exercise coaching | ● | ◐ | ○ | ○ | ● | ● |
| 5 Force-controlled physio or massage | ○ | ◐ | ○ | ● | ◐ (path preview) | ◐ (body scan) |
| 6 Medication and item delivery | ◐ | ● | ● | ○ | ○ | ◐ |
| 7 Logistics and night rounds | ◐ | ● | ● | ○ | ○ | ◐ |
| 8 Companionship | ● | ◐ | ◐ | ○ | ◐ | ◐ |
| 9 Telepresence with hands | ● | ● | ○ | ◐ | ● | ○ |
| 10 Intention interfaces (EMG) | ◐ | ◐ | ○ | ● (with dexterous hand) | ◐ | ● |
| 11 Assisted eating and drinking | ○ | ◐ | ○ | ● | ○ | ◐ |
| 12 Transfers, dressing, bathing | ◐ | ◐ | ○ | ○ | ○ | ○ |

**Fast rule of thumb (inference):**

- Little robotics experience in the team → archetype 4 or 3 (perception plus interface; the robot is the presenter).
- Strong manipulation or control skills → archetype 5 or 10 on a force-controlled arm.
- Strong navigation skills → archetype 2, 6 or 7 on a quadruped or wheeled base.
- Want a humanoid on stage → archetype 4 (demonstrator) or 9 (teleoperated), not 12.

## Sources

Event
- [Leukerbad Hackathon 2026 (Robotics, XR, and AI) — Luma](https://luma.com/vj13ns00)
- [Leukerbad Startup Pitch Competition — Luma](https://luma.com/2spvzh2r)

Leukerbad and Switzerland
- [Leukerbad — Wikipedia](https://en.wikipedia.org/wiki/Leukerbad)
- [Thermal baths in Valais — valais.ch](https://valais.ch/en/activities/wellness-water/thermal-baths)
- [Leukerbad: mountain sports and thermal springs — BLS](https://bls.ch/en/fahren/autoverlad/freizeit/leukerbad)
- [Leukerbad is living proof the Romans knew how to relax — Swissinfo](https://www.swissinfo.ch/eng/aging-society/leukerbad-is-living-proof-the-romans-knew-how-to-relax/1931622)
- [My Leukerbad AG, Geschäftsbericht 2024/25 (PDF)](https://leukerbad.ch/assets/content/documents-website/Dokumente-Torismusorganisationen/MyLeukerbad-AG/Gesch%C3%A4ftsbericht-MYLAG_2024_25_web.pdf)
- [Leukerbad Clinic company profile — jobup.ch](https://www.jobup.ch/en/enterprises/20196-leukerbad-clinic)
- [Leukerbad Clinic directory entry — search.ch](https://search.ch/tel/leukerbad/willy-spuehlerstrasse-2/leukerbad-clinic.en.html)
- [Musculoskeletal rehabilitation — MySwitzerland](https://www.myswitzerland.com/en/planning/about-switzerland/health/rehabilitation/musculoskeletal-rehabilitation/)
- [Survey: falls among the elderly result in high costs (BFU) — blue News](https://www.bluewin.ch/en/news/survey-falls-among-the-elderly-result-in-high-costs-li.3583495)
- [Fatal household accidents on the rise in Switzerland — Swissinfo](https://www.swissinfo.ch/eng/life-aging/fatal-household-accidents-on-the-rise-in-switzerland/87523642)
- [Need for healthcare staff set to rise steeply, says report (Obsan) — Swissinfo](https://www.swissinfo.ch/eng/politics/need-for-healthcare-staff-set-to-rise-steeply-says-report/46927578)
- [Nursing staff — Swiss Health Observatory (Obsan)](https://obsan.admin.ch/en/health-themes/health-professionals/nursing-staff)

Comparable events
- [robo.innovate Hackathon 2025: Advancing Robotics and AI Solutions — TUM MIRMI](https://www.mirmi.tum.de/en/mirmi/news/article/roboinnovate-hackathon-2025-advancing-robotics-and-ai-solutions)
- [robo.innovate Hackathon 2026 — TUM MIRMI](https://roboinnovate.mirmi.tum.de/robot-hackathon-2026/)
- [PhyRC 2027 Physical Robot Caregiving Challenge — Cornell EmPRISE Lab](https://emprise.cs.cornell.edu/phyrc/challenge-2027/)
- [LabORA 2026 Assistive Robotics Hackathon — UPC Doctoral School](https://doctorat.upc.edu/en/news/labora-2026-assistive-robotics-hackathon)
- [AI Meets Robotics Hackathon summary — lablab.ai](https://lablab.ai/blog/ai-meets-robotics-hackathon-summary)
- [Embodied AI Hackathon rules — Hackster.io](https://www.hackster.io/contests/embodiedAI/rules)

State of the art and evidence
- [Waseda's AIREC pushes humanoid care robots toward teleoperation-first nursing tasks — Origin of Bots](https://www.originofbots.com/news/wasedas-airec-pushes-humanoid-care-robots-toward-teleoperation-first-nursing-tasks)
- [Home robots available in 2026 (1X NEO pricing and remote supervision) — The Gadgeteer](https://the-gadgeteer.com/2026/05/20/home-robots-available-2026/)
- [Seniors are building deep bonds with this AI robot (ElliQ, New York State figure) — Entrepreneur](https://www.entrepreneur.com/business-news/a-new-ai-robot-is-helping-seniors-combat-loneliness/502676)
- [Older adults using Pleo for two weeks: can a social robot really reduce loneliness? — Gerontechnology](https://journal.gerontechnology.org/currentIssueContent.aspx?aid=4909)
- [Electromechanical gait trainers — Stroke Engine](https://strokengine.ca/en/interventions/electromechanical-gait-trainers/)
- [Systematic review on wearable lower-limb exoskeletons — Journal of NeuroEngineering and Rehabilitation](https://jneuroengrehab.biomedcentral.com/track/pdf/10.1186/s12984-021-00815-5)
