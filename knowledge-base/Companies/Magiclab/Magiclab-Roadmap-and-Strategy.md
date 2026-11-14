---
type: roadmap
company: "Magiclab Robotics"
slug: Magiclab
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# Magiclab Robotics — Roadmap and Strategy

⬆ [Magiclab Robotics profile](Magiclab.md) · [Product portfolio](Magiclab-Products.md) · [Developer guide](Magiclab-Developer-Guide.md)

> Read this to judge **what MagicLab cares about** and therefore what a team building on its robots should show. Web search was unavailable in this run: items marked "profile" were not re-fetched and rest on the sources listed in the [company profile](Magiclab.md); everything else was read today on the official site, docs or GitHub.

## Company trajectory

| Date | Milestone | Basis |
|---|---|---|
| 2024-01 | Company founded (Chinese name 魔法原子) | profile (official About page) |
| 2025-02-19 | In-house dexterous hand **MagicHand S01** released | official news |
| 2025-04 | Canton Fair export push; Red Dot Award 2025 | official news |
| 2025-05 | Commercial sales start | profile |
| 2025-07 | **MagicBot Z1** launched; small humanoid and wheel-legged quadruped shown at WAIC 2025 | official news |
| 2025-08 | WRC 2025 full-family showing; Z1 prototype wins bronze in standing high jump at the first World Humanoid Robot Games | official news |
| 2025-09 | First public SDK releases on GitHub (MagicDog v0.0.3 on 17 Sep, Z1 v1.0.0 on 18 Sep) | SDK changelogs |
| 2025-11 | SLAM and navigation interfaces added to both SDKs (v1.2.0) | SDK changelogs |
| 2026-01 | CES debut (Las Vegas) | official news, profile |
| 2026-01-23 | Global Partner Conference in Suzhou; "**1+2+N**" strategy presented; joint modules up to **525 N·m** peak torque stated | official news |
| 2026-02-16 | CCTV Spring Festival Gala as robot strategic partner: **6 Z1 + 2 Gen1** on the main stage, **100+ MagicDog** in panda costume in a swarm show; Gen1 and Z1 shown doing cooking and food-delivery tasks | official news |
| 2026-02 (late) | Co-founder and president Wu Changzheng reported to have left | profile (Chinese press) ⚠️ unverified |
| 2026-03 | MWC Barcelona; **RMB 500M+** round and planned RMB 10B industry fund announced 9 Mar | profile |
| 2026-04-21 | **RMB 150M** order in home smart-health / companion care announced — company calls it the largest single order in China's "big health" sector | official news |
| 2026-04-29 | Silicon Valley summit: Magic-Mix world model, H01 hand, MagicBot X1 | profile |
| 2026-06-10 | Z1 SDK v1.2.5 adds hybrid motion control | SDK changelog |
| 2026-07-17 | WAIC 2026: X1, D1 (wheeled) and MagicDog T1 launched | profile |
| 2026-08-12 | Z1 SDK v1.2.6 adds hand tactile / force data | SDK changelog |
| 2026-09 | IFA Berlin; parcel-sorting partnership with Pošta Slovenije announced | profile |
| 2026-09-22 | "In-Context Visual Guidance with Magic-Brain" technical article | official news |
| 2026-09-30 | `Inference` real-time VLA runtime open-sourced; Magic-W0 project page published | GitHub |
| 2026-10-30 | **Magic-W0** pre-trained and fine-tuned checkpoints plus training code released | GitHub |
| 2026-11-14 | Leukerbad Robotics Hackathon — first Swiss activity found | this event |

## Current focus projects

- **From stage shows to "robots that work".** The company's own gala write-up stresses service tasks (noodle cooking with a dexterous hand, last-metre food delivery by Z1, two robot types cooperating) over choreography, and frames the next phase as engineering maturity and task execution.
- **Factory and logistics pilots.** D1 material handling at a Dreame factory (company-sourced) and a parcel-sorting system with Pošta Slovenije (value and go-live not public) — profile.
- **Home health and companion care.** The April 2026 order covers home health management and smart companionship: customised hardware, a home health solution and showroom experiences, aimed at **10,000 high-net-worth households**. Customer name: not public in the article. Products involved: not specified.
- **Own model stack.** Magic-W0 (open), Magic-VLA K02 and Magic-Mix (closed), and the Magic-Brain agent framework. The September 2026 article reports grasp success rising from **70% to 94.4%** on MolmoSpaces-Bench by adding a VLM-drawn mask in front of the policy (company-reported).
- **Developer platform upkeep.** Z1 SDK is the active line (three releases Jun–Aug 2026). The MagicDog ROS 2 SDK is frozen; C++ / Python SDKs are the supported path.
- **Nine stated application scenarios** (April 2026): flexible industrial production, inspection and security, smart guiding, public safety, smart logistics, events and entertainment, research and education, home life, and health.

## Announced and upcoming products

| Item | Status | Date | Note |
|---|---|---|---|
| MagicBot X1 / X1 Ultra (full-size humanoid) | 🧪 | unveiled 2026-04-29, shown 2026-07 | Shipping status not confirmed; no SDK repo or docs section found |
| MagicBot D1 (wheeled industrial humanoid) | 🧪 | launched 2026-07-17 | Specs not public; no SDK repo found |
| MagicDog T1 (light-industry quadruped) | 🧪 | launched 2026-07-17 | Numeric specs not public; no SDK repo found |
| H01 dexterous hand | 🧪 | announced 2026-04-29 | Specs not public |
| Magic-Mix world model | 🧪 | announced 2026-04-29 | No code or weights |
| Magic-VLA K02 | 🧪 | 2026-04 (press) | No public weights |
| Magic-Brain agent framework | 🧪 | article 2026-09-22 | No code |
| Magic-W0 world–action model | ✅ open | weights 2026-10-30 | MIT code; relationship to K02 and Magic-Mix is not explained publicly |
| European certification | 🔭 | targeted Q4 2026 | profile; completion not confirmed |
| Cross-border retail via AliExpress Brand+ | 🔭 | announced 2026-09 | profile |
| RMB 10B embodied-AI industry fund | 🔭 | announced 2026-03-09 | "planned" |
| IPO preparation | 🔭 | reported | not confirmed |
| SDK / firmware roadmap | — | — | Not public. No stated plan for ROS 2 on humanoids. |

## Strategic direction and markets

- **"1+2+N"** (January 2026): **one** full-stack, self-developed hardware-plus-software base; **two** core product lines (humanoids and quadrupeds, as the portfolio implies); **N** ecosystem touchpoints growing from modular products. Two stated engines: **commercialisation** and **globalisation**.
- **Full-stack in-house**: joint modules, hands, arm, robots and models all developed internally; joint modules are also sold as components.
- **Leadership named on the official site**: co-founder Gu Shitao (strategy talks) and co-founder / CTO Chen Chunyu. Current CEO: not confirmed.
- **Dreame link**: D1 is reported working in a Dreame factory, and MagicLab's own retargeting code names the Z1 `dreame_z1`. Press widely describes MagicLab as incubated by Dreame; the official site does not state this ⚠️ unverified.
- **Go-to-market**: sales mainly to research institutions and integrators through distributors (profile); the company now talks about scenario solutions rather than bare robots.
- **Funding**: RMB 150M angel round; a round in May 2025; **RMB 500M+** in March 2026 (profile). Long-range company target of USD 14B revenue by 2036 is a company statement, not a forecast.
- **Europe**: three European or global trade shows in 2026 (CES, MWC Barcelona, IFA Berlin); Slovenian postal partnership; claimed inspection work at European energy sites; certification work targeted for Q4 2026; separate global storefront (magiclabglobal.com).
- **Switzerland**: no office, distributor, customer or research partnership found. Treat the hackathon as an early market-entry step (inference).
- **Priority verticals, in apparent order**: logistics and parcel sorting → factory handling → inspection and security → guiding / public service → home health and companionship.

## Research and open-source activity

- **Papers**: five company-authored arXiv preprints in September–October 2026, all on VLA / world-action policies (real-time inference, memory, replanning, Magic-W0). Details and links: [Papers and research](Magiclab-Papers-and-Research.md).
- **Open-sourced in 2026**: Magic-W0 (code + weights), `Inference` runtime, `Magiclab_GMR` (Jun), `magicbot-mimic` (May), Z1 deployment pipeline. Earlier: per-robot SDKs, URDF / MJCF models, pi0 recipe for Gen1, PICO teleoperation.
- **Pattern**: MagicLab ports strong upstream work (BeyondMimic, GMR, openpi) to its robots, and publishes its own work mainly on manipulation policies. Locomotion controllers shipped on the robots stay closed.
- **Not open**: Magic-VLA K02, Magic-Mix, Magic-Brain, datasets, quadruped RL environments.
- **Community size**: 22 public repos with single-digit to low double-digit stars. A good hackathon project built on these repos would be visible to the company.
- **Weights location**: Magic-W0 checkpoints sit under a personal Hugging Face account, not a company organisation.

## What would impress this company at the hackathon

**Inference from the strategy above — not a statement by MagicLab.**

| Track | What likely lands well | Why (their signal) | Realistic on their kit |
|---|---|---|---|
| T01 Autonomous Urban Services | A MagicDog that **completes a delivery or guiding loop end to end**: map, navigate, hand over, return | "Smart guiding" and logistics are named scenarios; the gala demo was a last-metre delivery; European push is postal | MagicDog EDU with the SLAM / navigation API and a 5 kg payload |
| T02 Resilient & Safe City | **Patrol with a useful finding**: route patrol, detect an anomaly (blocked exit, person down, ice patch), report with photo and map position | Inspection, security and public safety are three of the nine scenarios; Y1 is positioned for energy-site inspection | MagicDog EDU as stand-in for Y1 / T1; laptop-side perception |
| T03 Sustainable City | A **sorting or resource-monitoring demo** that reuses their logistics story (waste or returnables sorting, mobile sensing of heat loss / air quality) | Flexible sorting is their flagship European project | Weakest fit; sensor-carrier dog is the safe option |
| T04 Elderly Care & Rehabilitation | A **home-health companion**: voice interaction, fetch-and-carry, medication or exercise reminders, escort walking; show it with real older guests in mind | The RMB 150M home-health order shows where the money is going, yet no care product is public — a credible prototype fills a gap | Z1 Development Version (trick actions, 2–3 kg arms) or MagicDog EDU with voice |

Cross-track signals:

- **Finish the task, live, twice.** Their own messaging values reliability and "engineering maturity" over spectacle. A modest loop that works every time beats a fragile stunt.
- **Use their open stack visibly**: Python SDK + navigation API, URDF / MJCF for a digital twin, or the `Inference` server pattern. Mention which repos you used.
- **Two robots cooperating** (dog carries, humanoid hands over) mirrors the gala demo and the "one model stack, several bodies" framing.
- **VLM-in-front-of-policy** design: a VLM agent selects or marks the target, a simple skill executes. That is exactly the architecture they wrote about in September 2026.
- **Local relevance**: thermal-spa and rehabilitation-clinic settings, steep and snowy paths, elderly guests. These map onto guiding, inspection and home health at once.
- **Feed back to the platform**: a clean ROS 2 wrapper for the Python SDK, or documented bugs filed as GitHub issues, is rare and useful to a small developer community.
- **Avoid**: dance-only demos (they have done that on national TV), and anything that needs low-level biped control to work for the first time on stage.

## Sources

Read in this run:

- [MagicLab news — Global Partner Conference 2026 (Chinese)](https://www.magiclab.top/news/57)
- [MagicLab news — CCTV Spring Festival Gala review (Chinese)](https://www.magiclab.top/news/62)
- [MagicLab news — RMB 150M health-sector order (Chinese)](https://www.magiclab.top/news/63)
- [MagicLab news — In-Context Visual Guidance with Magic-Brain](https://www.magiclab.top/en/news/65)
- [MagicLab news index](https://www.magiclab.top/en/news)
- [GitHub — MagiclabRobotics organisation](https://github.com/MagiclabRobotics)
- [GitHub — magicbot-z1_sdk changelog](https://github.com/MagiclabRobotics/magicbot-z1_sdk/blob/main/CHANGELOG.md)
- [GitHub — magicdog_sdk changelog](https://github.com/MagiclabRobotics/magicdog_sdk/blob/main/CHANGELOG.md)
- [GitHub — Magic-W0](https://github.com/MagiclabRobotics/Magic-W0)
- [GitHub — Inference](https://github.com/MagiclabRobotics/Inference)
- [GitHub — Magiclab_GMR](https://github.com/MagiclabRobotics/Magiclab_GMR)
- [Docs — MagicDog ROS2 SDK user guide](https://support.magiclab.top/en/docs/dog/ros2_sdk)

Carried over from the company profile (not re-fetched today):

- [MagicLab — About Us](https://www.magiclab.top/en/about)
- [PR Newswire — MagicLab made its debut at CES](https://tools.prnewswire.com/en-us/live/20813/release/20260107EN58050)
- [PR Newswire — MagicLab at MWC](https://tools.prnewswire.com/en-us/live/20823/release/20260303EN00016)
- [Caixin Global — Chinese robotics startups push into Europe](https://www.caixinglobal.com/2026-03-10/chinese-robotics-startups-push-into-europe-as-industry-seeks-scale-102421334.html)
- [10jqka — RMB 500M round and industry fund (Chinese)](https://news.10jqka.com.cn/20260310/c675178183.shtml)
- [Stockstar — funding and leadership change (Chinese)](https://wap.stockstar.com/detail/IG2026031000009190)
- [AAP / Cision — Silicon Valley summit release, 29 Apr 2026](https://www.aap.com.au/aapreleases/cision20260429ae46475/)
- [Gasgoo — WAIC 2026: MagicLab launches three new robot products](https://autonews.gasgoo.com/articles/news/waic-2026-magiclab-launches-three-new-robot-products-embodied-intelligence-accelerates-entry-into-factories-and-public-scenarios-2079099620004175873)
- [EqualOcean — MagicLab targets European logistics, Slovenia postal partnership](https://equalocean.com/news/2026090822169-magiclab-targets-european-logistics-robotics-showcase-slovenia-postal)
