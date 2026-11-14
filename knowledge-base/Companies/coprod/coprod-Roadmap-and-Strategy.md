---
type: roadmap
company: "coprod Inc."
slug: coprod
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# coprod Inc. — Roadmap and Strategy

⬆ [coprod Inc. profile](coprod.md) · [Product portfolio](coprod-Products.md) · [Developer guide](coprod-Developer-Guide.md)

> **In one line:** a three-founder Swiss start-up, about two years old, with **CHF 40k–50k of public non-dilutive funding**, one in-house biped as proof, hardware in pre-order and a wide-open hiring page. Its roadmap is a list of intentions without dates. For a hackathon team the opportunity is access to the founders, not a mature platform.
>
> Research note: built from direct reads of coprod's site, GitHub organisation, Venture Kick, Venturelab and startup.ch. General web search was not available for this pass; press coverage beyond these sources was not checked.

## Company trajectory

| Date | Milestone | Source |
|---|---|---|
| ~2020–2024 | Founders spend 4+ years building robots (rovers, arms, dogs) and get frustrated with component integration | startup.ch |
| **Jul 2024** | Company founded, Prilly (Lausanne area) | startup.ch |
| Aug–Sep 2025 | Earliest activity still visible in the GitHub organisation (profile repo, fork of the `rsl_rl` reinforcement-learning library — last-updated dates) | GitHub |
| 2025 (exact date not public) | Enters Venture Kick; at entry the biped was not yet operational and boards were early PCB prototypes that could not yet communicate reliably | Venture Kick |
| ~Sep–Dec 2025 | co:dodo biped built in a garage in about three months of evenings and weekends | Venture Kick |
| **Dec 2025** | First co:system modules integrated into co:dodo; first "signs of life" just before Christmas | Venture Kick |
| By Apr 2026 | Partnership with an unnamed "global component supplier"; experienced advisors brought in | Venture Kick |
| **2 Apr 2026** | **CHF 40,000** Venture Kick Stage 2. startup.ch lists Venture Kick support of CHF 50,000 for 2026 (most likely Stage 1 + Stage 2 combined — inference) | Venture Kick, startup.ch |
| **May 2026** | Among the 20 start-ups pitching at the Startup Champions Seed Night (15th edition) at EPFL (article dated 8 May 2026) | Venturelab |
| Spring 2026 | Plans to leave the garage for a proper workspace (stated use of funds; completion ⚠️ unverified) | Venture Kick |
| **Sep 2026** | Website rebuilt (sitemap dates 1–10 Sep 2026): five products with pre-order links, co:found programme, community programmes, simulator, nine job openings, empty blog | coprod.co |
| Oct–Nov 2026 | Ongoing firmware-related commits (EtherCAT slave stack and embedded HAL forks pushed 9–11 Nov 2026); KiCad plugin v1.1.0 released | GitHub |
| **14–16 Nov 2026** | On site at the Leukerbad Robotics Hackathon | event context |

## Current focus projects

| Focus | What is happening now | Evidence |
|---|---|---|
| **Getting co:system to shippable** | co:motion, co:power, co:sense, co:battery are 🧪 pre-order; the online shop is still password-protected. Firmware dependencies are being pushed this month | Products page, shop, GitHub |
| **co:act actuator** | First integrated quasi-direct-drive actuator (10 Nm / 25 Nm peak, 60 mm, 420 g) listed 🧪 "coming soon" | Products page |
| **co:dodo as proof of stack** | 6-DoF point-foot biped, 1 kHz whole-body control over EtherCAT; public browser simulator running the walking policy | Systems page, simulator |
| **Developer software** | Hiring a "High-Level Software Engineer" for the co:system API, tooling, logging and simulation — the SDK is still being built out | Jobs page |
| **Community seeding** | Discord community opening with a first cohort; ambassador programme "cohort 01 is forming"; co:campus for clubs and Formula Student teams | Community page |
| **Founder pipeline (co:found)** | 75% off the first CHF 25,000 and 33% off up to CHF 100,000 for robotics start-ups, no equity | co:found page |
| **Market outreach** | Venture Kick money earmarked for travel, trade fairs and marketing; a "Forward Deployed Engineer" role explicitly covers events and hackathons | Venture Kick, jobs page |
| **Team build-out** | **9 open roles**, all Switzerland-based: electronics / PCB, mechanical, high-level software, low-level firmware, full-stack robotics, forward deployed, growth, founder's associate, sales | Jobs page |

## Announced and upcoming products

No item below has a public date or price.

| Item | Status | What is stated |
|---|---|---|
| **co:act** (60 mm, 420 g) | 🧪 coming soon | Quasi-direct drive, 16:1, hollow shaft, dual encoder, controller built in |
| More co:act sizes | 🔭 | "Multiple sizes coming soon" |
| **Safe Torque Off module** for co:motion | 🔭 | "Coming" — today only controlled braking |
| **EtherCAT Junction** | 🔭 planned | Passive and active junctions for star / branch wiring |
| **IO Board** | 🔭 planned | Digital / analog IO, fast-sampled, time-stamped on the bus |
| **Tactile Sensor** | 🔭 planned | High-bandwidth tactile array for contact-rich manipulation |
| More co:sense modalities | 🔭 | "More sensor modalities on the way" |
| **Dual-arm teleop platform** | 🔭 planned system | Tactile sensing on the end effectors |
| **Humanoid robot** | 🔭 planned system | Full-body control, human-like locomotion |
| Online shop | 🧪 | Pre-order buttons point to a store that was password-locked on 2026-11-14 |
| Public SDK / docs / examples | 🔭 implied | GitHub profile promises documentation, examples and pre-built systems; none public yet |
| Engineering blog | 🔭 | Page exists, first write-up "on the bench" |

**Read-across:** tactile sensor → dual-arm teleop platform → humanoid is a coherent path from "actuation parts" toward "manipulation and data-collection hardware". The stated rule is that they build what their own robots need.

## Strategic direction and markets

**Positioning**

- "The Legos of robotics": standardise the layer between sensors, drives, power and the developer's function call — **one bus (EtherCAT), one clock, one API**.
- Sell to **builders of robots**, not to end users: start-ups, research labs, university clubs, hobbyists. Headline promise: **time to first step under 6 months** for a new robot.
- Components are meant to work both as a complete kit and as drop-in parts for an existing robot.

**Europe and Switzerland**

- Fully Swiss: HQ in Prilly (Vaud); every open job is in Switzerland; funding and visibility come through the Swiss start-up pipeline (Venture Kick, Venturelab Seed Night at EPFL).
- Explicit **European-sovereignty narrative**: the co:found text says coprod wants young European robot companies to be able to compete with technology from China and overseas, and to protect local jobs with task-specific robots.
- Any direct EPFL affiliation is ⚠️ unverified (location and event venue only).

**Go-to-market**

- Bottom-up community: Discord, campus ambassadors, club sponsorship, founder discounts. This is the developer-tool playbook applied to hardware.
- co:found is a land-grab for the next cohort of European robotics start-ups: steep discounts early, so that the start-up's robot is designed around co:system.
- Sales role requires prior robotics-industry experience → B2B selling to companies is intended, not only hobbyists.

**Funding and partnerships**

| Item | Detail |
|---|---|
| Public funding | Venture Kick: **CHF 40,000** (Stage 2, Apr 2026); CHF 50,000 total listed on startup.ch |
| Equity round | not public |
| Partners | One unnamed global component supplier (Apr 2026). No other partner named |
| Customers | none named |
| Hackathon co-vendors | No announced partnership with any other vendor on site |

**Risks to keep in mind (inference)**

- Nine open roles against roughly CHF 50k of known funding means a financing round is needed or under way; roadmap timing depends on it.
- Competes with established modular-actuator and EtherCAT-drive suppliers and with low-cost integrated actuators from Asia; coprod's differentiator is the unified software and timing layer, which is exactly the part not yet public.
- Everything on the roadmap is undated. Do not plan a post-hackathon project around a specific delivery.

## Research and open-source activity

| Area | Status |
|---|---|
| Papers / preprints | none found |
| Patents | not public |
| Benchmarks or published test data | none; the blog promises "numbers with units" but has no posts |
| Open-source SDK | ❌ not released |
| GitHub organisation | [coprod-Inc](https://github.com/coprod-Inc), 9 public repos. Mostly forks of dependencies: `SOES` (EtherCAT slave stack), `modm` (embedded C++ HAL), `FreeRTOS-Cpp`, `tinycrypt`, `rsl_rl` (legged-robot RL), `lerobot` (Hugging Face robot learning) |
| Original open-source work | `kicad_project_manager` — MIT-licensed KiCad 9 / 10 plugin, v1.1.0; `robolitude` — placeholder repo labelled "Social Robotics" (MIT, no content described) |
| Open hardware | Site mentions "open-source integration examples" for the battery latch; not yet found in the public org ⚠️ unverified |
| Simulation | Public browser simulator (MuJoCo WASM + ONNX); model and training code not released |
| Stated attitude | "Built in the open" is the declared intent; so far the public output is tooling and forks, not the core stack |

**Signals worth noting (inference):** the `rsl_rl` and `lerobot` forks show the team works with mainstream learning tools — a locomotion-RL pipeline today, imitation-learning / teleop interest for the planned dual-arm platform. Website footer still links to an old GitHub name (`coprod-llc`, 404), consistent with a recent rename to "coprod Inc.".

## What would impress this company at the hackathon

**All of this section is inference** from coprod's stated values (results, fail fast, urgency), its hiring page and its roadmap. Nothing here is a stated judging criterion.

General principles:

- **Something physically moving on co:system within hours.** Their core claim is build speed; a team that reaches "first motion" on day 1 is live evidence for their pitch.
- **Drop-in use on another vendor's robot.** "Or to drop into yours" is on the product page; a clean cross-vendor integration proves interoperability better than a standalone rig.
- **Use the bus, not just the motor.** Synchronised IMU + motion + power telemetry on one clock is their differentiator — show a plot that needs it.
- **Honest, specific feedback.** A written list of API gaps, wiring pain and missing examples is valuable to a company still building its SDK; post a build log in their Discord.
- **A ROS 2 or LeRobot bridge** left behind as reusable code would fill a visible gap.
- **Start-up intent.** co:found exists to recruit founders; the jobs page recruits engineers. A credible "we would keep building this" matters to them.

Per track:

| Track | Idea that plays to coprod's strengths | Why it would land |
|---|---|---|
| **T01 Autonomous Urban Services** | A custom **add-on mechanism** for another vendor's mobile robot — parcel hatch, lift, dispenser or a small 4-wheel velocity-controlled base — driven by co:motion with co:power / co:battery | Mirrors the home-page API sample (wheel velocities + camera motor); shows "module that composes" |
| **T02 Resilient & Safe City** | An actuated **sensor mast or tool** for alpine hazards (snow, steep terrain): co:sense dual-redundant IMU for tilt and vibration, e-stop and power supervision via co:power, logged fault handling | Redundancy, deterministic timing and safe stopping are their engineering identity |
| **T03 Sustainable City** | An **energy-aware actuator**: sorting flap or valve whose motion profile is optimised using live power telemetry, with regenerative braking measured through the brake-chopper path | Uses a feature most vendors do not expose (power on the same clock as motion); modest but demonstrable |
| **T04 Elderly Care & Rehabilitation** | A **single-joint torque-controlled rehab or assist prototype** (for example elbow or knee exerciser on a dummy limb) with backdrivable assistance, range limits and IMU-based motion tracking — relevant to Leukerbad's rehab clinics | Quasi-direct-drive torque control is the right primitive; aligns with their move toward contact-rich, tactile systems. Must be shown with conservative safety limits, since there is no STO or certification |

Stretch ideas aligned with their roadmap: a minimal **teleoperation demo** (leader joint → follower joint with force feedback) anticipating the planned dual-arm teleop platform; or a **sim-to-real story** around co:dodo if the team shares the model.

## Sources

- [coprod — home page](https://coprod.co/)
- [coprod — products and module roadmap](https://coprod.co/products.html)
- [coprod — systems (co:dodo, planned systems)](https://coprod.co/systems.html)
- [coprod — co:found founder programme](https://coprod.co/cofound.html)
- [coprod — community (Discord, ambassador, co:campus)](https://coprod.co/community.html)
- [coprod — jobs](https://coprod.co/jobs.html)
- [coprod — values](https://coprod.co/values.html)
- [coprod — blog (empty)](https://coprod.co/blog/)
- [coprod — co:dodo simulator](https://coprod.co/simulator/)
- [Venture Kick — coprod receives CHF 40,000 (2 Apr 2026)](https://www.venturekick.ch/coprod-receives-CHF-40000-from-Venture-Kick-to-build-scalable-interoperable-robotics-ecosystem)
- [Venturelab — Startup Champions Seed Night celebrates 15th edition at EPFL (8 May 2026)](https://www.venturelab.swiss/Startup-Champions-Seed-Night-celebrates-15th-edition-at-EPFL)
- [startup.ch — coprod listing](https://www.startup.ch/coprod)
- [GitHub — coprod-Inc organisation](https://github.com/coprod-Inc)
- [GitHub — coprod-Inc/kicad_project_manager](https://github.com/coprod-Inc/kicad_project_manager)
