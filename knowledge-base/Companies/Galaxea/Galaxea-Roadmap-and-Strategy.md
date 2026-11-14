---
type: roadmap
company: "Galaxea"
slug: Galaxea
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# Galaxea — Roadmap and Strategy

⬆ [Galaxea profile](Galaxea.md) · [Product portfolio](Galaxea-Products.md) · [Developer guide](Galaxea-Developer-Guide.md) · [Solutions and projects](Galaxea-Solutions-and-Projects.md)

> **In one paragraph:** Galaxea (星海图; brands "Galaxea Dynamics" for hardware and "Galaxea Model" for AI) went from founding in **Sept 2023** to roughly **CNY 5 bn** of claimed cumulative funding in three years. Until 2026 it sold research robots to labs; since mid-2026 it is pushing hard into paid productivity work — retail fulfilment with JD.com, hospital logistics in Kunshan, factory assembly — under a "1+3+N" strategy, with a stated goal of **more than 10,000 robot deliveries in 2027**. Its open VLA models (G0 → G0 Plus → G0.5) are the centre of gravity.

## Company trajectory

| Date | Milestone |
|---|---|
| 2023-09 | Company founded; first financing round closed |
| 2024-01 | Second close of the angel round (total "tens of millions of USD") |
| 2024-02 | Development of the wheeled dual-arm platform starts |
| 2024-10 | **R1** launched; first units delivered to research labs incl. Fei-Fei Li's group (Stanford) and Physical Intelligence |
| 2024-11 | Pre-A round ("several hundred million RMB"); R1 Series family announced |
| 2025-03 | A1X / A1Y six-axis arm launched. Stanford's BEHAVIOR Robot Suite published on the R1 (see [profile](Galaxea.md)) |
| 2025-04 | A2 / A3 rounds; 2025 **R1 Lite** and **R1 Pro** introduced |
| 2025-07 | A4 / A5 rounds; cumulative funding "nearly RMB 1.5 bn" |
| 2025-08 / 09 | **G0** model and **Galaxea Open-World Dataset** open-sourced (weights on Hugging Face 9 Sept 2025) |
| 2026-01-04 | **G0 Plus** released; licence switches from Apache-2.0 to a non-commercial community licence |
| 2026-02-11 | **Series B, about CNY 1 bn (USD 144 M)** at a CNY 10 bn valuation. New investors: Jinding Capital (lead per Crunchbase), BAIC Group Industrial Investment, Hone Capital; Cathay Capital, Meituan Dragonball and Capital Today added to their stakes. Departure of co-founder **Huazhe Xu** confirmed the same day |
| 2026-02-12 | G0 Plus weights refreshed; **G0 Tiny** (250 M, on-board Orin) released |
| 2026-03 | Whole R1 Series upgraded ("2026" models). **Fast-WAM** world-action-model paper (arXiv 2603.16666) |
| 2026-04 | **Series B+, about CNY 2 bn (USD 291 M)**, valuation above CNY 20 bn; nearly 20 investors incl. **Lens Technology** (also hardware / mass-production partner) and state-backed funds. Third-generation arm **A1Z** and the cloud **EDP** (Embodied Development Platform) launched. SDK V2.3.0 (1 Apr) |
| 2026-06 | **Galaxea 2026 Global Developer Conference**: **G0.5** announced (1 June; weights 16 June) and **KENGO** biped launched. CEO says China could lead robotics foundation models within about three years |
| 2026-06 (site lists 2025-06-23 — content is clearly 2026) | **Xingtu ("Star Journey") Program** with Cathay Capital: plan to invest **RMB 1 bn in 100 early-stage embodied-AI startups over five years** |
| 2026-07 | RSS afterparty for the research community; G0.5 R1 Pro zero-shot entrypoint (11 July); SDK V2.4.0 (30 July) |
| 2026-08-05 | G0.5 tops the RoboDojo simulation leaderboard (score 20.23, self-reported) |
| 2026-08-12 | G0.5 paper on arXiv (2608.11739) |
| 2026-08-19 → 23 | **World Robot Conference, Beijing** ("Productivity Awakens"): robotic dark store, robot-assembling-robot demo, **NEXO** unveiled, "**1+3+N**" strategy, **G-Fleet**, G0.5 MAX teaser |
| 2026-08-22 | **Three-year strategic partnership with JD.com** signed at WRC |
| 2026-09-23 | **Four R1 Pro robots working at Kunshan First People's Hospital** (via partner Kunshu Xingqi, Pioneer Partner Program) |
| 2026-10-14 | **LEMO** opens for order in China at **RMB 49,999** |
| 2026-10-20 / 30 | SDK V2.4.1 (EHI tablet interface, PICO 4UE teleop) and **V2.5.0** (data-collection quality checks) |
| 2026-11-09 | LEMO on sale internationally from **USD 7,699** (see [profile](Galaxea.md)) |
| 2026 ("full year", company history page) | "Series B and Series C completed, total financing nearly **RMB 5 bn**" — ⚠️ unverified: no independent report of a Series C found; press confirms about CNY 3 bn raised Feb–Apr 2026 |

## Current focus projects

| Project | What is happening now | Status | Track relevance |
|---|---|---|---|
| **Robotic dark store with JD.com** | Full-scale store at WRC took live mini-program orders: order parsing, picking, bag opening, packing, hand-over. Claimed **10,000+ SKUs**, **99%+** order success, **900** orders / 1,775 picks / 1,560 packs during the show. JD framework covers omnichannel deployment, robot sales, joint R&D, supply chain | 🧪 pilot / showcase; 3-year agreement signed | T01.1, T01.3 |
| **Hospital logistics, Kunshan First People's Hospital** | 4 × R1 Pro move contaminated surgical instruments (transport inside one hour) and do routine ward inspection rounds (6 h+ per session). Planned next: surgical drapes and medical waste for **20 operating rooms / about 130 surgeries per day**, instrument counting (about 4,000 counting tasks over 2,500 m²), OR tidying, pre-op supply preparation (100+ product variants) | 🧪 about one month of operation, "hundreds of tasks" by late Sept 2026 | T04.6, T04.2, T01.2 |
| **Factory assembly ("robot assembling robot")** | Screw picking, insertion and powered fastening with force-controlled contact; RL on top of the foundation model, claimed **30%+ faster** than human-demo baseline | 🧪 demo | — |
| **Carton folding / part sorting** | 4,000 box folds per day at WRC under deliberate disturbances | 🧪 demo | T03.6 (sorting skills transfer) |
| **G0.5 open-source line** | Weights, fine-tuning, R1 Lite / R1 Pro / SO-101 / DROID clients; "G0.5 Reproduction Initiative" (sim reproduction, real-robot reproduction, co-creation) | ✅ | all tracks (policy backbone) |
| **G-Fleet** | Distributed RL infrastructure: fleet-wide policy rollout, human intervention, automated evaluation, model releases | 🧪 announced Aug 2026 | — |
| **Data build-out** | "One Million Hours of High-Quality Real-World Data" initiative with the Beijing E-Town joint venture **Yishu Intelligence (亦数智能)**; CEO quotes about CNY 250 / h for robot teleop data, 50–100 / h for human-centric data | 🧪 | — |
| **Developer funnel** | LEMO + A1Z + A1Z-T, EDP cloud (collect → train → deploy → evaluate; 10+ third-party models incl. π0.5, LingBot-VLA, DreamZero), EHI tablet, education / developer discounts | ✅ | hackathon tooling |
| **Scaling manufacturing** | COO: orders for "thousands" of model-driven robots fulfilled; target **more than 10,000 units in 2027**; Lens Technology as production partner; focus on reliability, service life, temperature range | 🧪 self-reported | — |

## Announced and upcoming products

| Product | Status | Known facts | Date |
|---|---|---|---|
| **NEXO** — flagship wheeled dual-arm robot | 🧪 unveiled, no public price / ship date | **30 force-controlled DoF**, **20 kg** peak dual-arm payload, 1700 mm, **2.5 m/s**, 8 h runtime, 2000 / 700 TOPS compute, dual LiDAR, 8 MP vision; fast charge, battery swap and autonomous recharge; aimed at retail, manufacturing, logistics, commercial services | Unveiled 2026-08 (WRC) |
| **KENGO** — bipedal humanoid | 🧪 launched; store lists USD 999,999 (reads as contact-sales placeholder) | About **40 kg**, 1396 mm, 23+ DoF, 2 kg arm payload, 130 N·m+ knee torque, about 2 h battery; positioned for unstructured sites: energy / power infrastructure, wide-area exploration, **equipment inspection** | Launched 2026-06 |
| **G0.5 MAX** | 🔭 "coming soon" | Larger / stronger G0.5 | Teased 2026-08-21 |
| **Fast-WAM large-scale pretrained model** | 🔭 planned | World-action model that skips video generation at inference: about **190 ms** per step vs about 800 ms (4× faster) | Teased 2026-08-21 |
| **G0.5 Tiny** | ⚠️ unverified | Listed in the EDP model catalogue as an edge model; no public weights found | — |
| **LEMO human-takeover (HITL) mode** | 🔭 "under development" | Take over during policy execution and keep recording; COMBO / COMBO PLUS editions only | — |
| **A1Z-T programmable buttons / joystick interfaces** | 🔭 | Reserved for user development, "available after development is complete" | — |
| **More G0.5 simulation benchmarks** | 🔭 | "Evaluation support for more simulation benchmarks will be released soon" (repo news, June 2026) | — |
| **Hospital task expansion (Kunshan)** | 🔭 | Drapes, medical waste, instrument counting, OR cleaning, pre-op supply prep | From 2026-10 |
| **Subscription / robot-as-a-service pricing** | 🔭 | CEO: hardware sales dominate 2025–2026; shift to subscriptions expected **2027–2028**, tied to proofs of concept in **urban delivery, commercial services and inspection**; token-based revenue floated | Stated 2026-06 |

## Strategic direction and markets

**"1+3+N" (announced Aug 2026)**

| Element | Meaning |
|---|---|
| **1** | One integrated "Robotics + Intelligence" base: Galaxea Dynamics (joints, platforms, motion control) + Galaxea Model (foundation models) |
| **3** | Three product lines: **KENGO** (biped, unstructured environments), **NEXO** (wheeled dual-arm, structured environments), **LEMO** (developers and makers) |
| **N** | Industry roll-out through partners: e-commerce / retail, express delivery and logistics, industrial manufacturing, commercial services, "emerging areas" |

- **Technology thesis:** three stages — instinctive → operational → evolutionary intelligence; "intelligence-defined robotics" (hardware specified by what the model needs: 0.1 mm repeatability, 0.1 N force resolution). The company keeps investing in **autoregressive VLA** (G0.5) and explores world-action models (Fast-WAM) in parallel.
- **Flywheel:** real deployments → interaction data → better models → fleet learning (G-Fleet) → more deployments.
- **Partner programmes:** Xingtu / Star Journey (startup investment — the company says it has already backed nearly ten firms), Excellence Partner Program, **Pioneer Partner Program** (vertical integrators such as Kunshu Xingqi in healthcare).
- **Customers and partners named publicly:** Stanford, Physical Intelligence, Huawei ("nearly 100" clients, Aug 2026); JD.com; NVIDIA (research showcase); Mistral AI (a vision-language-navigation model deployed on the R1 Pro, per Galaxea's solutions page — model name ⚠️ unverified); Ant Group's LingBot-VLA supports the R1 Pro.
- **Funding and valuation:** Feb 2026 Series B CNY 1 bn at CNY 10 bn; Apr 2026 B+ CNY 2 bn at above CNY 20 bn (Crunchbase counts the two as one USD 435 M round and cites a USD 1.4 bn valuation at the first close). Company claims about CNY 5 bn cumulative. Investors named in press: Jinding Capital, BAIC Group Industrial Investment, Hone Capital, Cathay Capital, Meituan Dragonball, Capital Today, Lens Technology.
- **IPO:** no announcement found. ⚠️ unverified weak signal: a news URL on the official site carries the slug "joint-stock-restructuring-completed" (the usual pre-listing step in China), but the page currently shows a different article.
- **Corporate footprint:** Beijing head office (Zhongguancun Yizhuang International Robot Industry Park, Tongzhou / E-Town); the docs footers name both a Beijing AI entity and **Suzhou Galaxea Dynamics Co., Ltd.** (hardware) — which explains why databases list either city; international web store run by **GALAXEA HK LIMITED**.

**Europe and Switzerland**

| Question | Finding |
|---|---|
| European office, subsidiary or service centre | None found in official sources |
| Sales route into Europe | Direct international web store (USD prices, Hong Kong entity) plus third-party resellers (see [profile](Galaxea.md)); batteries ship separately for overseas orders |
| European partners | Mistral AI research deployment on R1 Pro (above). No Swiss customer, pilot or distributor found |
| Regional strategy statements | WRC panels discussed North America and South-East Asia (General Robotics, Mr.Robot / Jemco); Europe was not singled out |
| Certification for EU deployment (CE, machinery / medical) | Not documented publicly — ask the booth |
| Take-away | The Leukerbad hackathon is itself the most visible European developer activity found; Galaxea's European play today is **developers and research labs**, not deployments |

## Research and open-source activity

| Item | Date | Notes |
|---|---|---|
| **G0.5: One Autoregressive Stream for Robot Reasoning and Action** — arXiv 2608.11739 | 2026-08-12 | Single-decoder VLA with native action chain-of-thought, cross-embodiment ActionCodec, visual memory; pretrained on 14 embodiments. Self-reported: 82.5% DROID zero-shot, 98.9% LIBERO, 93.3% RoboTwin 2.0, 0.3136 on BEHAVIOR-1K, RoboDojo no. 1 |
| **Fast-WAM** — arXiv 2603.16666 | 2026-03 | World-action model without test-time video generation; [project page](https://yuantianyuan01.github.io/FastWAM/) |
| **G0 dual-system VLA + Galaxea Open-World Dataset** — arXiv 2509.00576 | 2025-09 | 500+ h, single embodiment; dataset is the company's most-used open asset |
| G0 Plus / G0 Tiny | 2026-01 / 02 | "Plug-and-play" checkpoints incl. pick-and-place; on-device inference at up to 10 Hz |
| GalaxeaDP, GalaxeaManipSim | 2025-08 | Diffusion-policy baseline and 30+ sim environments |
| LEMO / A1Z open stack | 2026-04 → 11 | MIT-licensed arm SDK, open-hardware leader arm, LeRobot / G0.5 / π0.5 pipelines; repos updated the week of the hackathon |
| Talks | 2026-06 | Chief Scientist **Hang Zhao** (rendered "Zhao Xing" on the English site) at the BAAI Conference: "VLA vs. WAM"; action tokenisation line "FAST → FASTer" |

- **Licensing trend:** Apache-2.0 (2025) → G0 Plus Community License (4 Jan 2026) → G0.5 Community License (16 June 2026), both **non-commercial**. Hardware-side tooling stays MIT / Apache.
- **External research on Galaxea hardware** (from the company's own index): Stanford BEHAVIOR Robot Suite and BEHAVIOR-1K challenge (R1 / R1 Pro), Physical Intelligence π0.5 validated on R1 Lite, NVIDIA GEAR EgoScale, Stanford + Meta Ego-Pi, BAAI RoboBrain-X0, CMU's ICRA 2025 WBCD winning entry on the A1X arm.
- **Activity level:** `GalaxeaVLA` about 820 stars; 13 repos in the model org, 24 in the product org; A1Z / LEMO repos pushed 11–13 Nov 2026.

## What would impress this company at the hackathon

> **Inference, not company statements.** Derived from what Galaxea publicly emphasises: "No gimmicks, just work", reliability under disturbance, long-horizon tasks, data flywheels and vertical partners.

| Signal Galaxea rewards | How to show it in 48 h |
|---|---|
| **Real work, not choreography** | A task with a measurable outcome (items delivered, bins sorted, minutes saved), counted live — mirror their WRC habit of reporting cycle counts |
| **Recovery from disturbance** | Deliberately move objects or interrupt mid-task and let the policy recover; show failures honestly with a success-rate tally |
| **Long-horizon + language** | Chain 3–5 subtasks from one natural-language instruction, ideally surfacing G0.5's subtask reasoning |
| **Data efficiency** | "N teleop demos → X% success", with the collect → convert → fine-tune → deploy loop reproducible from a README |
| **A vertical they are entering** | Healthcare logistics, retail fulfilment, inspection — a credible Pioneer-Partner-style use case with a named operator need |
| **Contributions back** | A PR, a new LeRobot dataset, a sim task or a fix to the docs / toolkits — fits the "G0.5 Reproduction Initiative" |

**By track**

| Track | Pitch that fits Galaxea's direction | Why it lands |
|---|---|---|
| **T01 Autonomous Urban Services** | Mini "dark store" or kiosk: order by voice or QR → R1 picks from a cluttered shelf → bags → hands over (T01.1 / T01.3 / T01.7) | Direct echo of the JD.com flagship; the CEO names urban delivery and commercial services as the 2027–28 subscription targets |
| **T02 Resilient & Safe City** | Indoor inspection round with manipulation: read gauges, open a cabinet, flip a breaker, report anomalies (T02.3 / T02.5); teleop fallback with the same leader arms that collect data | Matches the Kunshan ward-inspection work and KENGO's stated "equipment inspection" niche; be explicit that the wheeled base is indoor / flat-floor only |
| **T03 Sustainable City** | Dual-arm sorting of mixed recyclables or returned packaging on LEMO with a fine-tuned policy, reporting throughput and purity (T03.1 / T03.6) | Extends their part-sorting and carton-folding demos; deformable-object handling is a skill they advertise |
| **T04 Elderly Care & Rehabilitation** | Non-clinical care logistics: fetch-and-hand-over, tidy, laundry or supply-cart restocking in a mock care room, with safe hand-over behaviour (T04.1 / T04.6) | Their hospital deployment is deliberately *non-clinical* support work, and the R1's research pedigree is household tasks (BEHAVIOR) — stay inside that framing, do not claim medical function |

**Questions worth asking the Galaxea team on site** (answers are not public): Is G0.5 MAX or a LoRA path for R1 available to try? Is the navigation package enabled on the demo robots? Is EDP training credit offered to teams? Any plans for a European service partner?

## Sources

- [Galaxea — About us / company history](https://www.galaxea-ai.com/en/company.html)
- [Galaxea — Leadership](https://www.galaxea-ai.com/en/leadership.html)
- [Galaxea — News centre](https://www.galaxea-ai.com/en/news.html) · [page 2](https://www.galaxea-ai.com/en/news/page-2.html)
- [Galaxea news — WRC 2026 "Productivity Awakens" wrap-up (23 Aug 2026)](https://www.galaxea-ai.com/en/news/wrc-2026-beijing.html)
- [Galaxea news — "From AI Models to Real-World Productivity" forum (21 Aug 2026)](https://www.galaxea-ai.com/en/news/galaxea-lanches-wrc.html)
- [Galaxea news — Galaxea and JD sign a three-year strategic partnership (26 Aug 2026)](https://www.galaxea-ai.com/en/news/galaxea-jd-three-year-partnership.html)
- [Galaxea news — R1 Pro joins Kunshan First People's Hospital (23 Sep 2026)](https://www.galaxea-ai.com/en/news/kunshan-first-people-hospital-r1-pro.html)
- [Galaxea news — LEMO available for order (14 Oct 2026)](https://www.galaxea-ai.com/en/news/galaxea-launches-lemo.html)
- [Galaxea news — G0.5 no. 1 on RoboDojo (5 Aug 2026)](https://www.galaxea-ai.com/en/news/joint-stock-restructuring-completed.html)
- [Galaxea news — "Star Journey" (Xingtu) Program](https://www.galaxea-ai.com/en/news/g0-embodied-foundation-model-release.html)
- [Galaxea news — BAAI talk: VLA vs. WAM](https://www.galaxea-ai.com/en/news/r1-lite-developer-program.html)
- [Galaxea — NEXO product page](https://www.galaxea-ai.com/en/product1.html)
- [Galaxea — KENGO product page](https://www.galaxea-ai.com/en/product3.html)
- [Galaxea — EDP (Embodied Development Platform)](https://www.galaxea-ai.com/en/edp.html)
- [Galaxea — Industry productivity solutions](https://www.galaxea-ai.com/en/productivity.html)
- [Galaxea — Research and education solutions](https://www.galaxea-ai.com/en/developer.html)
- [Galaxea — G Series models](https://www.galaxea-ai.com/en/model.html)
- [Galaxea store — Contact us (Beijing address)](https://galaxea-dynamics.com/pages/contact-us)
- [Galaxea store — About us (Hong Kong entity)](https://galaxea-dynamics.com/pages/about-us)
- [Galaxea blog — Fast-WAM world action model](https://galaxea-dynamics.com/blogs/developer-hub/fast-wam-world-action-model)
- [PR Newswire Asia — Galaxea AI at WRC 2026 (24 Aug 2026)](https://en.prnasia.com/story/545003-0.shtml)
- [Caixin Global — Galaxea AI raises USD 144 M (12 Feb 2026)](https://www.caixinglobal.com/2026-02-12/galaxea-ai-raises-144-million-as-chinas-robot-investment-frenzy-mounts-102413767.html)
- [Caixin Global — Galaxea AI raises USD 291 M (2 Apr 2026)](https://www.caixinglobal.com/2026-04-02/robot-startup-galaxea-ai-raises-291-million-102430297.html)
- [Caixin Global — Galaxea AI chief on robotics models (17 Jun 2026)](https://www.caixinglobal.com/2026-06-17/galaxea-ai-chief-says-china-could-lead-robotics-models-within-three-years-102454837.html)
- [Crunchbase News — Embodied AI fuels record robotics funding in China (20 May 2026)](https://news.crunchbase.com/robotics/embodied-ai-fuels-record-funding-china-ipo-momentum-builds/)
- [GitHub — OpenGalaxea/GalaxeaVLA (news log, licence history, G0.5 paper reference)](https://github.com/OpenGalaxea/GalaxeaVLA)
- [arXiv 2608.11739 — G0.5: One Autoregressive Stream for Robot Reasoning and Action](https://arxiv.org/abs/2608.11739)
- [arXiv 2603.16666 — Fast-WAM: Do World Action Models Need Test-time Future Imagination?](https://arxiv.org/abs/2603.16666)
- [arXiv 2509.00576 — Galaxea Open-World Dataset and G0 Dual-System VLA Model](https://arxiv.org/abs/2509.00576)
- [GitHub — OpenGalaxea organisation](https://github.com/OpenGalaxea)
- [GitHub — userguide-galaxea organisation](https://github.com/userguide-galaxea)
- [GitHub — OpenGalaxea/awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers)
- [Galaxea docs — SDK changelog V2.5.0](https://docs.galaxea-dynamics.com/Changelog/en/v2.5.0) · [V2.4.1](https://docs.galaxea-dynamics.com/Changelog/en/v2.4.1) · [V2.4.0](https://docs.galaxea-dynamics.com/Changelog/en/v2.4.0) · [V2.3.0](https://docs.galaxea-dynamics.com/Changelog/en/v2.3.0)
- [Galaxea docs — LEMO usage workflow](https://docs.galaxea-dynamics.com/LEMO/en/docs/usage_workflow/lemo_usage_workflow)
- [Galaxea docs — A1Z-T teleoperation device](https://docs.galaxea-dynamics.com/LEMO/en/docs/lemo_a1zt_teleop/)
