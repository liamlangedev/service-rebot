---
type: company
company: "Spirit AI"
slug: Spirit-AI
hq: "Hangzhou, China"
founded: 2024
website: https://www.spirit-ai.com
categories: [humanoid, mobile-manipulator, software, data]
on_site_guess: "Moz1 wheeled force-controlled humanoid with Quest VR teleop kit and MozRobot SDK; open-source Spirit v1.5 VLA as the model story"
fit_t01: 3
fit_t02: 2
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Spirit AI

> **One-liner:** Chinese embodied-AI company (Chinese name 千寻智能 / Qianxun Intelligence) that builds the Moz wheeled, fully force-controlled humanoids and the Spirit family of vision-language-action (VLA) foundation models.
> **Why it matters at Leukerbad:** Moz1 is a documented dual-arm mobile manipulator (Python SDK, ROS 2 Humble, VR teleop, URDF) and Spirit v1.5 is an open-source VLA (MIT) — a realistic base for an indoor "tidy / fetch / sort" demo. The catch: the VLA needs data-centre GPUs to fine-tune, so in 48 hours plan on teleop + scripted SDK skills or a pre-trained checkpoint, not training from scratch.

**Identity caveat:** this is the robotics company (LinkedIn slug `spiritai-robotics`, domain `spirit-ai.com`). It is **not** the UK game-AI firm also called Spirit AI.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Hangzhou (Yuhang District), China; further offices in Beijing (Haidian) and Shenzhen (Nanshan). The website's ICP filing entity is Beijing-registered, so "HQ" is ⚠️ unverified between Hangzhou and Beijing; press and Hangzhou government sources call it a Hangzhou start-up |
| Founded | 2024 (⚠️ exact date unverified; the company's own June 2025 news calls it a "one-year-old unicorn") |
| Founders / CEO | Han Fengtao (founder, CEO); Gao Yang (co-founder, chief scientist) ⚠️ roles not stated on the official site, taken from press |
| Size and funding | Headcount not public. 2025: **RMB 528M** Pre-A, **RMB 600M** Pre-A+ (JD.com lead). 2026: **~RMB 2B** over two rounds (Feb/Mar), **RMB 1B** more (7 Apr), **RMB 1.5B** A+ (3 Jun, per Chinese press). Valuation reported above RMB 10B / ~USD 1.4–1.5B ⚠️ unverified |
| Core business | Embodied foundation models (Spirit VLA) + in-house force-controlled wheeled humanoids (Moz series) + data-collection hardware (uDAS); deployments in industry first, commercial services next, home last |
| Website | https://www.spirit-ai.com (English: https://www.spirit-ai.com/en) |
| Docs / developer portal | https://docs.spirit-ai.com (Chinese at /zh; versions v2.6 and v2.7) |
| GitHub | https://github.com/Spirit-AI-Team (public repo: `spirit-v1.5`) |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified unless marked) | Price | Img key |
|---|---|---|---|---|---|
| **Moz1** | Wheeled dual-arm humanoid, whole-body force control (industrial / research) | ✅ shipping (deployed at CATL, JD) | **26 DoF** · **7-DoF** arms with force/position hybrid control · omnidirectional wheeled base · whole-body STO safety + collision detection · 3 RealSense cameras used by SDK · control loop up to **120 Hz** · separate industrial PC + inference host. Height, weight, payload, battery: not on the official pages I could read | not public | spirit-ai-moz1 |
| **Moz2** | Commercial service robot (retail, hospitality, office buildings) | 🧪 public debut WAIC, July 2026; early validation | **32 DoF** · omnidirectional steering-wheel chassis · foldable leg structure · 7-DoF arms · **4-DoF three-finger** hands · LiDAR + vision + ultrasonic · magnetic mounting points for accessories (delivery rack, inspection module) | not public | spirit-ai-moz2 |
| **Spirit v1.5** | Open-source VLA foundation model | ✅ available (weights + inference code Jan 2026, fine-tuning code Apr 2026) | MIT licence (GitHub) · topped RoboChallenge Table30 as of 11 Jan 2026 (score **66.09**, success **50.33 %**, per Xinhua) · tested on NVIDIA A100 80 GB · fine-tune recommended on **8× A100** · Python 3.10+ · ~4B-class VLM backbone ⚠️ unverified | free | spirit-ai-spirit-v1-5 |
| **Spirit v1.6** | VLA + world-model foundation model (closed) | 🧪 demoed on Moz1 at WAIC and WRC 2026; not released | Long-horizon tasks from one instruction, dynamic replanning, millimetre-level pill sorting. A claimed #1 RoboArena ranking (Jun 2026) was reported as later delisted — treat as disputed ⚠️ unverified | not public | spirit-ai-spirit-v1-6 |
| **uDAS** | Data-collection device used with the robot and model stack | 🧪 named in WAIC 2026 coverage; no public spec | not public | not public | spirit-ai-udas |
| **MozRobot SDK** | Python SDK for Moz1 | ✅ available to customers (v0.1.0, 2025-09-25; a v0.1.2 package is referenced) | Python ≥ 3.10 · Ubuntu 22.04 · ROS 2 Humble · x86_64 and aarch64 wheels · dual-arm and whole-body configs, with or without base | bundled | spirit-ai-mozrobot-sdk |

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organisers):**

- **Moz1** is the only Spirit AI robot with public manuals, an SDK, teleop tooling and a URDF, and it is the unit the company ships to customers and labs. If a physical robot is on site, it is almost certainly Moz1 — probably one unit, given the size and value of the machine.
- A **Quest VR teleoperation kit** normally ships with Moz1 (the docs describe headset + two controllers + cable), so teleop and data collection should be possible on day 1.
- **Moz2** is still in early commercial validation (first shown July 2026); bringing it to a Swiss developer event is unlikely.
- **Spirit v1.5** is the model developers can actually touch (open weights). v1.6 is closed; expect it only as a company-run demo, if at all.
- No Europe or Switzerland activity was found in public sources; expect a small travelling team and Chinese-first documentation.

## Developer platform (summary)

- **SDK:** MozRobot SDK, **Python only** (≥ 3.10), delivered as a wheel plus `requirements.txt`; Ubuntu 22.04 recommended; x86_64 and aarch64.
- **ROS 2:** ROS 2 **Humble**, `ROS_DOMAIN_ID=33`. Host connects by Ethernet on the `172.16.0.x` subnet (robot at `172.16.0.20`).
- **Control level:** dual-arm or whole-body configurations (with / without base), control loop up to **120 Hz**, optional soft-real-time setup. Teleop offers relative and Cartesian modes. Low-level torque API: not documented publicly.
- **Perception:** native RealSense multi-camera support (reference setup uses **3** cameras over USB 3.0).
- **Teleoperation and data collection:** Quest VR headset; the collection app has a mutually exclusive inference mode for running a deployed policy. Dataset paths suggest LeRobot-style data ⚠️ unverified format.
- **Pretrained models:** Spirit v1.5 (GitHub + Hugging Face, base checkpoint and one fine-tuned RoboChallenge checkpoint). The docs also give a **Pi0.5 / openpi adaptation** for Moz1 (`pi05_moz` config, policy server + robot client, Docker compose); the adapted source and sample dataset are distributed via after-sales support, not a public repo.
- **Simulation:** Moz1 URDF download (26 DoF) on the docs site; MuJoCo page (convert with `urdf2mjcf`) and an NVIDIA Isaac page. No ready-made MJCF / USD confirmed.
- **Navigation:** a SLAM navigation section exists in the docs (contents not reviewed).
- **Compute:** on-robot industrial PC plus an inference host (specs not public). Spirit v1.5 has been ported to D-Robotics' **Sunrise S600** (560 TOPS) — integration done, on-robot testing announced as next step (May 2026).
- **Operator tools:** Windows HMI (MovaXHelper) and a tablet app (SpiritAI MovaX) over the robot's Wi-Fi hotspot; three emergency stops (base, back, wireless handheld).
- **Links:** [docs](https://docs.spirit-ai.com/zh) · [SDK quick start](https://docs.spirit-ai.com/zh/sdk/get-started.html) · [teleop](https://docs.spirit-ai.com/zh/teleop/get-started.html) · [GitHub](https://github.com/Spirit-AI-Team/spirit-v1.5)

**48-hour reality check:** fine-tuning Spirit v1.5 is specified for 8× A100 80 GB. Without cloud GPUs and pre-collected data, build on teleop, SDK-scripted skills and an off-the-shelf perception model, and use the VLA only if Spirit AI staff provide a working checkpoint.

## Current projects, deployments and customers

- **2025 (Sept, inferred from site):** Moz1 launched as a fully force-controlled humanoid — [Spirit AI news](https://www.spirit-ai.com/en/news/13).
- **2025-12:** Company reports large-scale deployment of its robots on a **CATL** battery production line — [Spirit AI news](https://www.spirit-ai.com/en/news/23). Press later reported "tens" of Moz1 units across CATL and JD.com lines ⚠️ unverified count.
- **2026-01:** Spirit v1.5 tops RoboChallenge Table30 and is open-sourced — [Spirit AI news](https://www.spirit-ai.com/en/news/25), [Xinhua via ehangzhou.gov.cn](https://www.ehangzhou.gov.cn/2026-01/14/c_296331.htm).
- **2026-03-19:** Strategic agreement with **JD.com**; Moz robots connected to JD MALL retail scenarios (for example coffee making), per Chinese press — [NBD](https://www.nbd.com.cn/articles/2026-06-03/4416899.html) ⚠️ unverified detail.
- **2026-05-07:** Partnership with **Bosch China** — data loop in Bosch factories and logistics centres in China, Bosch sensors and actuators, benchmarking Spirit v1.5 on industrial tasks — [Spirit AI news](https://www.spirit-ai.com/en/news/29).
- **2026-05-20:** Partnership with **D-Robotics** (also on site at Leukerbad) — Spirit v1.5 running end-to-end on Sunrise S600 — [Spirit AI news](https://www.spirit-ai.com/en/news/45).
- **2026 (date not shown):** Strategic partnership with **Schaeffler** — [Spirit AI news](https://www.spirit-ai.com/en/news/46).
- **2026-07 (WAIC, Shanghai):** Moz1 + Spirit v1.6 demo: "tidy up the living room" from one instruction (cans, dishwasher loading, waste paper), dynamic replanning, pill sorting; Moz2 debut — [Spirit AI news](https://www.spirit-ai.com/en/news/48).
- **Track relevance:** all confirmed deployments are industrial (battery manufacturing) and retail. No elderly-care, rehabilitation, emergency-response or outdoor deployment found.

## Roadmap and future direction

- **Stated sequence:** "Industry first, commercial services next, home last" (WAIC 2026).
- **Moz2** 🧪: commercial service robot targeting retail shelf stocking, hotel delivery, building inspection and exhibition guidance; will progressively inherit Moz1 capabilities. No ship date or price.
- **Models:** v1.5 open (Jan 2026) → v1.6 closed, VLA + world model (mid-2026). Successor names: not public.
- **Data:** press reports **200,000+ hours** of interaction data and a target of **1M hours** by end of 2026, with a data team growing towards 1,000 people ⚠️ unverified (press, not official pages read).
- **Timing view:** founder Han Fengtao is quoted describing 2026 as a model-performance year, with large-scale deployment expected from H2 2027 to 2028 ⚠️ unverified (Chinese press).
- **Funding:** roughly **RMB 4.5–5B** raised in H1 2026 across three announcements (see Snapshot); investors include Yunfeng Capital, Shunwei Capital, HongShan, JD.com, Prosperity7, TCL Venture Capital.
- **Edge compute:** S600 port with D-Robotics points to on-board VLA inference without a GPU workstation 🔭.
- **Europe / Switzerland:** no announced plans found. Bosch and Schaeffler ties are with the groups' China operations.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | Indoor wheeled manipulator suited to fetch, deliver, restock and tidy in hotels, shops and lobbies; no outdoor, stairs or snow capability | Moz1 (Moz2 if present), Spirit v1.5 | [T01 brief](T01-Autonomous-Urban-Services/Spirit-AI-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | Could do indoor inspection or valve / switch manipulation, but flat-floor wheeled base and no hazard-rated hardware | Moz1 | [T02 brief](T02-Resilient-and-Safe-City/Spirit-AI-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Dual-arm sorting (waste, recyclables, dishwasher loading) is demonstrable; no sustainability-specific product or deployment | Moz1, Spirit v1.5 | [T03 brief](T03-Sustainable-City/Spirit-AI-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | Force-controlled, collision-detecting arms plus shown pill sorting and room tidying map to assisted-living chores; home use is last on the company's roadmap and there is no care deployment or medical certification | Moz1, Spirit v1.5 / v1.6 demos | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Spirit-AI-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Spirit-AI-Products.md) · [Developer guide](Spirit-AI-Developer-Guide.md) · [Roadmap and strategy](Spirit-AI-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Spirit AI official site (home)](https://www.spirit-ai.com)
- [Spirit AI — product page (EN)](https://www.spirit-ai.com/en/product)
- [Spirit AI — about (EN)](https://www.spirit-ai.com/en/about)
- [Spirit AI — news index (EN)](https://www.spirit-ai.com/en/news)
- [Spirit AI news: WAIC 2026, Moz2 debut](https://www.spirit-ai.com/en/news/48)
- [Spirit AI news: D-Robotics partnership, Spirit v1.5 on Sunrise S600](https://www.spirit-ai.com/en/news/45)
- [Spirit AI news: Bosch partnership](https://www.spirit-ai.com/en/news/29)
- [Spirit AI news: nearly RMB 2B funding](https://www.spirit-ai.com/en/news/27)
- [Spirit AI news: Moz1 launch](https://www.spirit-ai.com/en/news/13)
- [Spirit AI docs portal (ZH)](https://docs.spirit-ai.com/zh)
- [Docs: Moz1 quick start](https://docs.spirit-ai.com/zh/moz1/get-started.html)
- [Docs: Moz1 product introduction](https://docs.spirit-ai.com/zh/moz1/product-intro.html)
- [Docs: MozRobot SDK quick start](https://docs.spirit-ai.com/zh/sdk/get-started.html)
- [Docs: teleoperation quick start](https://docs.spirit-ai.com/zh/teleop/get-started.html)
- [Docs: MuJoCo simulation](https://docs.spirit-ai.com/zh/simulation/mujoco.html)
- [Docs: Pi0.5 adaptation](https://docs.spirit-ai.com/zh/open-resources/pi.html)
- [GitHub: Spirit-AI-Team/spirit-v1.5](https://github.com/Spirit-AI-Team/spirit-v1.5)
- [Xinhua via ehangzhou.gov.cn: Chinese AI startup tops embodied intelligence benchmark (2026-01-14)](https://www.ehangzhou.gov.cn/2026-01/14/c_296331.htm)
- [Gasgoo: Spirit AI secures nearly 2 billion yuan](https://autonews.gasgoo.com/articles/icv/2026146686038994944)
- [Gasgoo: Spirit AI secures another 1 billion yuan](https://autonews.gasgoo.com/articles/icv/seeds-spirit-ai-secures-another-1-billion-yuan-funding-2041520154024787969)
- [NBD: funding round, 2026-04-07](https://www.nbd.com.cn/articles/2026-04-07/4328144.html)
- [NBD: A+ round and Spirit v1.6, 2026-06-03](https://www.nbd.com.cn/articles/2026-06-03/4416899.html)
- [Huxiu: Spirit AI feature (targets, RoboArena dispute)](https://www.huxiu.com/article/4872028.html)
