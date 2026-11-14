---
type: roadmap
company: "Unitree Robotics"
slug: Unitree
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# Unitree Robotics — Roadmap and Strategy

⬆ [Unitree Robotics profile](Unitree.md) · [Product portfolio](Unitree-Products.md) · [Developer guide](Unitree-Developer-Guide.md)

> Research note: web search was unavailable in this run. New facts here come from pages fetched directly (GitHub, Hugging Face, PR Newswire, eWeek, Notebookcheck, Wikipedia); IPO and product-launch items marked "(profile)" are carried over from the company profile and were not re-fetched. Nothing newer than what these pages show (e.g. Oct–Nov 2026 press) could be checked.

## Company trajectory

| Date | Milestone |
|---|---|
| 2013–2016 | Wang Xingxing builds the XDog quadruped as a master's project at Shanghai University |
| 26 Aug 2016 | Hangzhou Unitree Technology registered in Hangzhou (Binjiang) |
| 2021 | **Go1** consumer quadruped |
| 2023 | **Go2**, **B2** and the first humanoid **H1** |
| Aug 2024 | **G1** compact humanoid enters mass production (launch price about USD 16K) |
| Jan 2025 | CES showing: Go2, Go2-W, B2-W, H1, G1 |
| Jul 2025 | IPO tutoring starts (CITIC Securities); WIPO Global Award (ICT, SME category) |
| 2025 | **R1**, **A2**, **H2** added; **UnifoLM-WMA-0** world model open-sourced (Sept); about **5,500 humanoids shipped**; revenue about **RMB 1.7 bn**, net income about RMB 288M |
| Feb 2026 | G1 kung-fu routine at the Spring Festival Gala; **As2 / As2-W** unveiled (24 Feb); 2026 target of **10,000–20,000 humanoids** stated |
| Mar 2026 | STAR Market IPO filing; UnifoLM-VLA weights on Hugging Face |
| May 2026 | **GD01** pilotable mecha unveiled (profile) |
| 1 Jun 2026 | **H2 Plus** announced as NVIDIA Isaac GR00T reference humanoid |
| Jun 2026 | US Department of Defense adds Unitree to its list of Chinese military-linked companies |
| 19 Aug 2026 | STAR Market listing, about **RMB 6.1 bn** raised (profile) |
| Aug 2026 | "Superman" humanoid demonstrated (reported 12.66 m/s run, 2 m standing jump — ⚠️ unverified performance claims) |
| 11–28 Sep 2026 | **UnifoLM-WLA-1.0** (6B-parameter humanoid foundation model) and UnifoLM-ER models released under Apache-2.0 |
| Oct–Nov 2026 | `unitree_robotskills` (LLM-agent skills for G1-D / R1-D), **D2** arm and **R1-7a** arm SDK repos published |

## Current focus projects

| Focus | Evidence | Why it matters to you |
|---|---|---|
| **Humanoid volume** | 5,500 units in 2025 → 10–20K target for 2026; R1 from USD 4,900 | Cheap humanoids are the growth story; the company wants proof they are useful, not only acrobatic |
| **"Brain" layer (UnifoLM)** | WMA-0 (2025) → VLA (early 2026) → **WLA-1.0** (Sept 2026: 6B parameters, ~2,500 h real-robot data, 64 tasks); 246 open datasets on Hugging Face | Wang Xingxing names operation outside controlled environments as the main open problem |
| **Data-collection products** | G1-D and R1-D wheeled dual-arm "application plans"; `xr_teleoperate`, `teleimager`, `unitree_lerobot`, Isaac Lab sim with G1-D / R1-D | Unitree is building the pipeline teleop → dataset → policy → deploy and wants people to use it |
| **LLM-agent control** | `unitree_robotskills` (Oct 2026): camera → reasoning → bounded motion tools; drawing, Gomoku, chess, navigation skills; MCP | Signals interest in agentic task execution on top of the SDK |
| **NVIDIA alignment** | H2 Plus GR00T reference robot (Jetson AGX Thor, Sharpa Wave hands); G1 reference workflow promised | Isaac Sim / Lab, GR00T and Jetson are the favoured toolchain |
| **Industrial quadrupeds** | As2 (Feb 2026), A2, B2, wheel-legged "-W" variants, B2-Ex; inspection and fire-rescue solution lines | The revenue base outside research: inspection, emergency response |
| **Arms and hands in-house** | D2 7-DoF arm, R1-7a arm, Dex1-1 / Dex3-1 / Dex5-1 / Dex5-S hands | Moving from "legs only" to complete mobile manipulators |

## Announced and upcoming products

| Item | Status | Date / timing | Notes |
|---|---|---|---|
| H2 Plus (H2 + Sharpa Wave 22-DoF hands + Jetson AGX Thor T5000, 75 DoF total) | 🧪 | Announced 1 Jun 2026; availability "late 2026" — shipping status not confirmed | Reference humanoid for NVIDIA Isaac GR00T |
| GR00T reference workflow for G1 | 🧪 | "Soon" as of Jun 2026; release not confirmed in this run | To be published on GitHub / Hugging Face |
| "Superman" humanoid | 🧪 prototype | Demonstrated Aug 2026 | No product name, price or date public |
| R1-D, H2-A / H2-D application plans | ✅ / 🧪 listed on the official site | 2026 | R1-D already has an Isaac Lab model and agent skills; prices not public |
| UniPlatform / UniStore / UniUni | 🧪 | Linked from the official site | Model, data and app platforms; contents not checked |
| General-purpose humanoid embodied foundation model (scene, instruction, action, task generalisation; cloud training + edge inference + real-world data loop) | 🔭 | By about **2030** (IPO filing, as reported) | Paired with a cheaper general-purpose home humanoid, sales targeted within about three years of the filing |
| Household, elder-care and daily-living humanoids | 🔭 | "As technology matures"; ~2030 horizon | Directly relevant to track T04 |
| GD01 mecha | 🧪 / ✅ | May 2026 (profile) | Showpiece; not hackathon-relevant |

## Strategic direction and markets

- **Price leadership:** undercut everyone (Go2 from USD 1,600, R1 from USD 4,900, G1 USD 13.5K) by building motors, reducers, LiDAR, hands and controllers in-house.
- **Customer mix:** about **73.6%** of humanoid revenue in the first three quarters of 2025 came from research and education, **9.0%** from industrial use (company exchange responses, via Wikipedia). The developer community is the core market — hackathons are its home turf.
- **Move up the stack:** from hardware vendor to hardware + open models + data + app store, to keep developers on Unitree robots as VLA models commoditise.
- **Funding:** listed on the Shanghai STAR Market since 19 Aug 2026, about RMB 6.1 bn raised (profile). Pre-IPO backers include HongShan, Matrix Partners, Shunwei Capital and affiliates of Tencent, Alibaba, Ant Group and Meituan; shareholders also include state-linked funds.
- **Partnerships:** NVIDIA (GR00T, Jetson Thor), Sharpa (hands on H2 Plus); third-party hands from Inspire and BrainCo are supported in the teleop stack; Pi and GR00T models supported in the training fork.
- **Scale:** about 500 employees in 2025 (Wikipedia) — small for its output; expect lean on-site support.
- **Geopolitical and trust headwinds:** US DoD "Chinese military company" listing (Jun 2026), a US House committee request for investigation (2025), and published security findings (2025: remote-access vulnerability, Bluetooth exploit, undisclosed telemetry on G1). European public-sector, healthcare and critical-infrastructure buyers will ask about data handling — a real factor for T02 and T04 pitches.
- **Europe / Switzerland:** no Unitree subsidiary, office or Swiss deployment was found in the sources read; sales in Europe run through distributors / resellers (names ⚠️ unverified, not checked in this run). International consumer sales of R1 via AliExpress were reported in Apr 2026 (profile). Ask the on-site team who handles Swiss sales and service.

## Research and open-source activity

| Area | Output | Status |
|---|---|---|
| SDK and middleware | `unitree_sdk2` (1.4k stars), `unitree_sdk2_python`, `unitree_ros2`, `unitree_ros` — all updated in the second half of 2026 | ✅ actively maintained |
| RL locomotion | `unitree_rl_gym` (3.7k stars, legacy), `unitree_rl_lab` (Isaac Lab), `unitree_rl_mjlab` (mjlab; Go2, A2, As2, G1, R1, H1-2, H2) | ✅ |
| Simulation | `unitree_mujoco`, `unitree_sim_isaaclab` (Isaac Sim 6.2 / Isaac Lab 3.0, updated Nov 2026) | ✅ |
| Teleoperation and data | `xr_teleoperate` (1.7k stars), `teleimager`, `unitree_lerobot` | ✅ |
| Foundation models | `unifolm-world-model-action` (1.2k stars), `unifolm-vla`, `unifolm-wla` (Apache-2.0); 8 models on Hugging Face | ✅ open weights |
| Datasets | 246 Hugging Face datasets, mostly G1 table-top (Dex1 / Dex3 / BrainCo) and whole-body teleop sets; new sets were being uploaded during this research | ✅ |
| Agents | `unitree_robotskills` (Apache-2.0) | ✅ new |
| Hardware openness | `Qmini` open-source small biped; LiDAR SDKs and Point-LIO port | ✅ |
| Academic papers | `Publications` repo not updated since 2023; Unitree's research impact comes mainly through third-party labs using its robots | — |

Pattern: Unitree open-sources **tooling, models and data** generously, but keeps the **on-board locomotion controllers and firmware closed** and gates SDK access by edition (EDU).

## What would impress this company at the hackathon

**Inference, not company statements** — based on the stated bottleneck (robots working outside controlled settings), the 2030 household / elder-care goal, and where Unitree invests open-source effort.

| Track | What would likely land well | Why |
|---|---|---|
| T01 Autonomous Urban Services | A Go2 / As2 that completes a **real errand on Leukerbad terrain** — stairs, slope, snow patch, door — with autonomous navigation and a clear hand-over to a person; or a wheel-legged delivery run with energy / time numbers | Shows usefulness beyond demos; exercises LiDAR, obstacle avoidance and the high-level SDK |
| T02 Resilient & Safe City | Quadruped **inspection or search patrol** with anomaly detection (thermal, gas, snow load, blocked path) and a mission report; multi-robot hand-off; operation in cold and wet | Matches Unitree's own inspection and fire-rescue lines; reliability evidence is what industrial buyers lack |
| T03 Sustainable City | Mobile sensing with a measurable outcome: e.g. energy-loss or waste-contamination survey done by a robot instead of fixed sensors, with data quality shown | Unitree has nothing purpose-built here; a credible new vertical is valuable |
| T04 Elderly Care & Rehabilitation | G1 EDU + Dex hands doing **one household / care task end-to-end** learned from a small teleop dataset (fetch and hand over, walking-aid retrieval, rehab-exercise coaching) with explicit safety behaviour around a frail person | Directly on the 2030 roadmap; uses the full teleop → LeRobot → policy pipeline Unitree wants adopted |

Cross-cutting signals that should score with Unitree staff:

- **Uses their open stack end-to-end** (SDK2 + `xr_teleoperate` + `unitree_lerobot` or UnifoLM-WLA) and **contributes back**: a dataset on Hugging Face, a bug fix, a new skill in the `unitree_robotskills` style.
- **Autonomy in an uncontrolled setting** — outdoors, real stairs, real people — rather than a choreographed routine.
- **An LLM agent with bounded, verifiable tools** driving the robot through a multi-step task.
- **Honest robustness numbers** (success rate over N runs, recovery from failure) and a visible safety concept (tether, speed limits, stop behaviour).
- **Pairing with other vendors on site** — e.g. SKYLANDX scans for maps, D-Robotics boards for extra edge compute, XREAL glasses for operator interfaces — shows the platform plays well in an ecosystem.

## Sources

- [Unitree profile in this repo (IPO, launches, shipment figures carried over)](Unitree.md)
- [Wikipedia — Unitree Robotics (history, financials, customer mix, shareholders, security and US listings)](https://en.wikipedia.org/wiki/Unitree_Robotics)
- [PR Newswire — Unitree H2 Plus, NVIDIA Isaac GR00T reference humanoid (1 Jun 2026)](https://tools.prnewswire.com/en-us/live/20823/release/20260601EN72140)
- [eWeek — Unitree aims to ship up to 20,000 humanoids in 2026](https://www.eweek.com/news/unitree-20000-humanoid-robots-2026-china/)
- [Notebookcheck — Unitree plans household and elder-care humanoid by 2030](https://www.notebookcheck.net/Beyond-kung-fu-Unitree-plans-humanoid-robot-for-household-chores-and-elder-care-by-2030.1255707.0.html)
- [Unitree GitHub organisation](https://github.com/unitreerobotics) · [repositories by stars](https://github.com/orgs/unitreerobotics/repositories?type=all&q=&sort=stargazers)
- [unifolm-wla (UnifoLM-WLA-1.0 release notes)](https://github.com/unitreerobotics/unifolm-wla)
- [unitree_robotskills](https://github.com/unitreerobotics/unitree_robotskills)
- [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)
- [unitree_rl_mjlab](https://github.com/unitreerobotics/unitree_rl_mjlab)
- [unitree_lerobot](https://github.com/unitreerobotics/unitree_lerobot)
- [xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate)
- [Unitree on Hugging Face (models and datasets)](https://huggingface.co/unitreerobotics)
- [Unitree official open-source page (application plans, platform links)](https://www.unitree.com/opensource)
