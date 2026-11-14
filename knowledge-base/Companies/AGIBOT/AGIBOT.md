---
type: company
company: "AGIBOT"
slug: AGIBOT
hq: "Shanghai, China"
founded: 2023
website: https://www.agibot.com
categories: [humanoid, quadruped, mobile-manipulator, dexterous-hand, software, data]
on_site_guess: "X2 (Edu/Ultra) compact humanoids and D1 Edu/Ultra quadrupeds with open SDKs; possibly a G-series wheeled dual-arm robot with Genie Studio and OmniHand end-effectors"
fit_t01: 4
fit_t02: 3
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# AGIBOT

> **One-liner:** Shanghai embodied-AI company (Zhiyuan Robotics) that builds humanoids, wheeled dual-arm manipulators, quadrupeds, cleaning robots and dexterous hands, plus its own foundation models (GO series), simulator (Genie Sim) and data platform (Genie Studio) — the largest humanoid shipper by volume in H1 2026 per IDC and Counterpoint.
> **Why it matters at Leukerbad:** Widest single-vendor hardware range on site (legs, wheels, four legs, hands) with a documented ROS 2 SDK for the X2 and open simulation assets, so a team can prototype in sim and deploy on a real robot within 48 hours. Weak spot: no proven elderly-care or alpine/outdoor deployments.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Shanghai, China (legal entity: AGIBOT Innovation (Shanghai) Technology Co., Ltd.; Chinese brand: Zhiyuan / 智元) |
| Founded | **February 2023** |
| Founders / CEO | Co-founded by Peng Zhihui ("Zhihui Jun", President and CTO) and Deng Taihua (Chairman and CEO); Jiang Qingsong listed as co-founder / COO in a 2026 profile ⚠️ unverified |
| Size and funding | Headcount not public (third-party estimates vary widely). Backers reported: HongShan, Hillhouse, BYD and others. Hong Kong IPO process started **July 2026**; an October 2026 round at a reported **RMB 50 bn** valuation is said to push or suspend the listing (sources differ). Revenue 2025 reported above **RMB 1.05 bn** ⚠️ unverified |
| Scale | **20,000th** robot off the line (company headline, autumn 2026); 15,000th in June 2026; 10,000th in March 2026. H1 2026 humanoid shipments: **8,600+** (IDC) or about **9,700** (Counterpoint) — both rank it no. 1 |
| Core business | General-purpose embodied robots sold as hardware and, increasingly, as outcome-based solutions (industrial handling, logistics sorting, retail, guiding, security inspection, cleaning) |
| Website | https://www.agibot.com (store: https://store.agibot.com) |
| Docs / developer portal | X2 SDK docs: https://x2-aimdk.agibot.com · product manuals and open source: https://www.agibot.com/DOCS/OS · Genie Studio: https://genie.agibot.com/en/geniestudio |
| GitHub | https://github.com/AgibotTech (hands and grippers also at https://www.agilink-ai.com) |

## Portfolio at a glance

Lineup as listed on agibot.com on 2026-11-14. Specs are official-page or press-release values unless flagged.

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| A3 Ultra | Full-size humanoid (service / commercial) | 🧪 launched July 2026, availability not public | **1.74 m**, **60 kg**, **51 active DoF**, **5 kg per arm**, up to **8 h** combined runtime, NVIDIA Thor, 3D LiDAR + RGB-D + fisheye + stereo, GPS / RTK / UWB, autonomous charging | not public | agibot-a3-ultra |
| A3 | Full-size humanoid (interaction / performance) | ✅ listed (launched April 2026) | **173 cm**, **55 kg**, **10 h** runtime, **10 s** battery swap, UWB cm-level positioning for swarms up to 100 robots, shoulder touch sensing, 360° mic array | not public | agibot-a3 |
| A2 Ultra | Full-size humanoid (reception / guiding) | ✅ shipping | **169 cm**, about **69 kg**, **40 DoF**, arm load about **2 kg**, standing **3 h** / walking **1.5 h+**, hot-swap battery, **1.2 m/s**, Jetson Orin 64 GB + 16-core CPU, 3D LiDAR + RGB-D, face screen, LinkSoul persona / knowledge base | not public | agibot-a2-ultra |
| A2 Lite | Full-size humanoid (lighter A2 variant) | ✅ listed | specs not verified | not public | agibot-a2-lite |
| X2 (Neo / Ultra / Edu) | Compact humanoid (interaction, education, research) | ✅ shipping | about **131 cm**, **35–39 kg**, **25–30 active DoF** by variant (Edu: 29 ⚠️ unverified); Ultra adds LiDAR + RGB-D and Orin NX ⚠️ unverified; AimDK ROS 2 SDK (Python / C++); MuJoCo sim | X2 Neo listed at **USD 25,600** on the official store ⚠️ unverified (search snippet); reseller prices for other variants vary from about USD 30k to 50k | agibot-x2 |
| X1 | Open-source humanoid reference design | ✅ open source (hardware, RL training and inference code on GitHub) | not a commercial deployment product; full design files published | not public (build-it-yourself) | agibot-x1 |
| G2 | Wheeled dual-arm mobile manipulator (industrial + interactive) | ✅ shipping | **IP42**, automotive-grade components, force-controlled arms with sub-millimetre assembly claims, Genie RL for fast task deployment, expressive face and multi-user dialogue; dimensions / payload not on product page | not public | agibot-g2 |
| G2 Max | Heavy-payload industrial task robot (handling, palletizing) | 🧪 launched July 2026 | specs not public | not public | agibot-g2-max |
| G2 Air | Single-arm mobile manipulator | 🧪 launched April 2026 | **7 DoF** arm, **3 kg** payload, **750–800 mm** reach, width under **800 mm**, speed **≥ 1.5 m/s** | not public | agibot-g2-air |
| G1 / G1 Max | Wheeled dual-arm data-collection and manipulation platform (Genie-1) | ✅ shipping | the reference robot for the AgiBot World dataset and GO-1 in Genie Studio; specs not verified in this pass | not public | agibot-g1 |
| D1 Ultra (also D1 Pro / Edu) | Small quadruped | ✅ shipping | **5 kg** payload, **3.7 m/s** max, range **6 ± 1 km**, **IP54**, **40°** slope, **16 cm** stairs, joint peak torque about **48 N·m**; ports: Ethernet, USB, power, SBUS, UART; open SDK, URDF, Isaac Sim + MuJoCo | not public | agibot-d1-ultra |
| D1 Max / D1 MaxPro | Larger quadrupeds (industrial / outdoor) | ✅ listed | specs not verified; GitHub repos exist for both | not public | agibot-d1-max |
| D2 Max | All-terrain quadruped ("Level 3 autonomous") | 🧪 announced April 2026, not yet on product menu | specs not public | not public | agibot-d2-max |
| C5 | Autonomous commercial cleaning robot | ✅ shipping | sweep + scrub + dust-mop, up to **1,980 m²/h**, **550 mm** scrub width, **3 h** scrubbing, **90 L** tank, docking workstation, laser-vision navigation, elevator / access-control linkage | not public | agibot-c5 |
| OmniHand family (Ultra-T, Ultra, standard, Lite) | Dexterous hands (AGILINK brand) | ✅ / 🧪 by model | OmniHand 3 Ultra-T: **22+3 DoF** tendon-driven, **500 g**, 10:1 load-to-weight, full-hand 3D tactile + palm camera; SDK with C++ / Python / ROS 2 API | not public | agibot-omnihand |
| OmniPicker 3 | Adaptive gripper | ✅ listed | **140 N** grip force, **1,000,000**-cycle life, modular tactile sensing | not public | agibot-omnipicker |
| MEgo | Robot-free data-collection kit (gripper + egocentric view + engine) | 🧪 announced April 2026 | specs not public | not public | agibot-mego |
| GO-1 / GO-2 / GO-3 (preview) | Manipulation foundation models (ViLLA / VLA) | GO-1 ✅ open weights · GO-2 ✅ in Genie Studio (April 2026) · GO-3 🧪 preview (Oct 2026) | GO-2: action chain-of-thought, dual-system planner + executor; company-reported **98.5%** LIBERO | not public | agibot-go-model |
| Genie Studio | Data collection, fine-tuning, evaluation and deployment platform | ✅ available | closed-loop pipeline for G-series robots with GO models; commercial, not open source | not public | agibot-genie-studio |
| Genie Sim 3.0 | Open-source simulation platform | ✅ open source | Isaac-based, ROS 2 runtime (MoveIt, ros2_control), open assets, datasets and evaluation code | free | agibot-genie-sim |

## What they will most likely bring to the hackathon

**Best guess — not confirmed by the organisers or AGIBOT.**

| Likelihood | Model | Reasoning |
|---|---|---|
| High | **X2 (Edu / Ultra)** | The only AGIBOT humanoid with a public, documented developer SDK (AimDK_X2); the X2 Edu was launched in July 2026 explicitly for education, competitions and research. Small (about 131 cm), transportable, safe around crowds. |
| High | **D1 Edu / Ultra quadruped** | Cheap, rugged (IP54), open SDK + URDF + sim; the standard "developer dog" for events. Best match for Leukerbad's slopes and stairs. |
| Medium | **G1 or G2 wheeled dual-arm** | The event listing names G1/G2; these are the platforms for GO-model manipulation and Genie Studio teleoperation. Heavier logistics, needs AGIBOT staff support. |
| Medium | **A2 / A2 Ultra** | Named in the event listing; typically used as a reception / guiding showpiece. Public SDK is limited (LinkSoul customisation, dance and swarm tools), so less hackable. |
| Low–medium | **OmniHand / OmniPicker** | Small, open SDK, easy to ship; useful as end-effectors on other vendors' arms. |
| Low | A3 / A3 Ultra, G2 Max, C5 | New, scarce or bulky; more likely shown than handed to teams. |

European logistics run through Minth Group (strategic partner and sales agent in Europe since February 2026), so on-site units and support staff may come via that channel.

## Developer platform (summary)

- **AimDK_X2** — official SDK for the X2 (X2 Ultra, X2 Ultra new version, X2 Edu). Built on **ROS 2**, **Python and C++**. On-board development modes apply to the Ultra variants only. SDK version must match robot firmware — check this first on site. Docs: https://x2-aimdk.agibot.com
- **High-level control:** motion-mode switching, locomotion velocity commands, preset motions, LinkCraft motion playback, TTS / audio / microphone, face screen and LEDs, LinkSoul cloud dialogue.
- **Low-level control:** joint control, upper-body control, end-effector control (grippers and dexterous hands, including a low-level interface); RL policy deployment on the X2 is documented.
- **Sensors exposed (X2):** IMU, LiDAR, RGB-D, front stereo and interaction cameras, rear camera, head touch, GNSS; SLAM / navigation module is optional and the vision interface is marked "to be enabled" in the docs.
- **Simulation:** X2 MuJoCo simulation (local or Docker) and X2 URDF repo; D1 supports Isaac Sim and MuJoCo; A3 / A3 Ultra robot models and USD files are on GitHub; **Genie Sim 3.0** (open source) for manipulation with a native ROS 2 runtime.
- **Quadrupeds:** open SDK and repos for D1 Edu / Ultra, D1 Max and D1 MaxPro on GitHub; expansion via Ethernet, USB, UART, SBUS for LiDAR, depth camera, RTK, 4G.
- **Hands:** `agilink_omnihand_sdk` offers C++ / Python / ROS 2 APIs across the OmniHand range, plus URDF descriptions and a data-collection toolbox.
- **Models and data:** GO-1 weights and fine-tuning code plus the AgiBot World dataset are published via the OpenDriveLab/AgiBot-World repo and Hugging Face; ACoT-VLA (the method behind GO-2) and Genie Envisioner world models are on the AgibotTech org. GO-2 itself is served through Genie Studio; its open-source status is not public.
- **Agents:** an `agibot_agentsdk_sample_code` repo exists (AgentSDK sample code, Oct 2026) — scope not verified.
- **On-board compute:** A2 Ultra — Jetson Orin 64 GB + 16-core CPU; A3 Ultra — NVIDIA Thor; X2 Edu — RK3588 and X2 Ultra — Orin NX (both ⚠️ unverified, third-party datasheets).

## Current projects, deployments and customers

- **2026-11-06** — Six G2 robots completed **1,730 tasks** in a 24-hour convenience-store trial in Shanghai ([agibot.com news](https://www.agibot.com)). Relevant to T01.
- **2026-10-29** — GO-3 Preview announced as topping three embodied-AI benchmarks (company claim; [agibot.com news](https://www.agibot.com)).
- **Autumn 2026** — 20,000th general-purpose embodied robot rolled off the line ([agibot.com](https://www.agibot.com)).
- **2026-09** — Exhibited at IFA 2026 in Berlin; TÜV Rheinland certification for the A-Series reported ([AGIBOT](https://agibot.com/article/231/detail/96.html)).
- **2026-09** — More than 300 robots reported at Chimelong Spaceship Park (Hengqin), and 100 X2 robots for in-store greeting and guidance at a retail chain ⚠️ unverified (search summary only, no primary source read).
- **2026-07-20** — More than **30 robots** ran visitor guidance and information services across WAIC 2026 venues ([press release](https://www.aap.com.au/aapreleases/cision20260719ae07639/)).
- **2026-06** — 15,000th robot produced; a factory livestream of tablet quality inspection concluded ([Yicai Global](https://www2.yicaiglobal.com/news/chinas-agibot-ships-15000th-humanoid-robot-completes-live-tablet-quality-inspection-test)).
- **2026-04-17** — Company states hundreds of robots are deployed per project across industrial handling, logistics sorting, retail, security inspection and commercial operations ([AGIBOT](https://www.agibot.com/article/231/detail/63.html)).
- **Elderly care / rehabilitation:** no public deployment found. Treat any T04 use as a new application, not a proven one.
- **Switzerland:** no public deployment or partner found.

## Roadmap and future direction

- **2026-01-30 / 2026-02-24** — European launch in Milan, then German market entry in Munich with Minth Group as European partner and sales agent; Minth is working on localized European production ([Yicai Global](https://www.yicaiglobal.com/news/global-humanoid-robot-leader-agibot-taps-minth-group-to-drive-european-rollout), [Pudong government](https://english.pudong.gov.cn/2026-02/28/c_1162918.htm)).
- **2026-04-09** — GO-2 foundation model released: action chain-of-thought, integrated with Genie Studio for fleet data collection and online post-training ([The Robot Report](https://www.therobotreport.com/agibot-releases-go-2-foundation-model-embodied-ai/)).
- **2026-04-17** — Partner conference: A3, G2 Air, D2 Max, OmniHand 3 Ultra-T, OmniPicker 3, MEgo, and eight models (BFM, GCFM, AGIBOT WORLD 2026, GO-2, GE-2, Genie Sim 3.0, SOP, WITA Omni). Strategy: "one robotic body, three intelligences" (locomotion, interaction, manipulation) and a shift from selling units to outcome-based solutions; 2026 framed as the first year of real deployment ([AGIBOT](https://www.agibot.com/article/231/detail/63.html)).
- **2026-07-20** — WAIC: A3 Ultra, X2 Edu, G2 Max, OmniHand 3 Ultra-M ([press release](https://www.aap.com.au/aapreleases/cision20260719ae07639/)).
- **2026-07-24** — Hong Kong IPO process begun, reported valuation target HK$40–50 bn ([Gasgoo](https://autonews.gasgoo.com/articles/news/agibot-launches-hong-kong-ipo-process-2082120389458100225)).
- **2026-10-14** — New funding round near an RMB 50 bn valuation; listing likely delayed beyond 2026 ([TechNode](https://technode.com/2026/10/14/robot-maker-agibot-nears-new-funding-round-at-rmb-50-billion-valuation/)).
- **2026-10-29** — GO-3 preview 🧪; general release date not public.
- **UK** — APC2026 partner event held in London to push European commercial deployment ([AGIBOT](https://www.agibot.com/article/231/detail/81.html)).

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | **4** | Real guiding, retail and store-operation deployments plus a commercial cleaning robot; X2 SDK gives a 48-hour path for guide / concierge / delivery demos | X2, G2, A2 Ultra, C5, D1 | [T01 brief](T01-Autonomous-Urban-Services/AGIBOT-T01-1-Brief.md) |
| T02 Resilient & Safe City | **3** | D1 quadruped (IP54, 40° slopes, sensor expansion) suits patrol and inspection; security inspection is a listed solution area but no hazard-response product | D1 Ultra, D1 Max, D2 Max, G2 | [T02 brief](T02-Resilient-and-Safe-City/AGIBOT-T02-1-Brief.md) |
| T03 Sustainable City | **2** | Supporting role: sorting / handling with G-series and GO models, water-efficient cleaning with C5; nothing purpose-built for emissions or waste | G2, G2 Air, C5, OmniPicker | [T03 brief](T03-Sustainable-City/AGIBOT-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | **3** | Friendly compact humanoid with voice, face screen and LinkSoul persona works for companionship, reminders and guided exercise; no proven care deployment and physical-assist payloads are low | X2, A2 Ultra, G2, OmniHand | [T04 brief](T04-Elderly-Care-and-Rehabilitation/AGIBOT-T04-1-Brief.md) |

## Related docs
- [Product portfolio](AGIBOT-Products.md) · [Developer guide](AGIBOT-Developer-Guide.md) · [Roadmap and strategy](AGIBOT-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [AGIBOT official site — product menu, news headlines](https://www.agibot.com)
- [AGIBOT — A2 Ultra product page](https://www.agibot.com/products/A2_Ultra)
- [AGIBOT — G2 product page](https://www.agibot.com/products/G2)
- [AGIBOT — D1 Ultra product page](https://www.agibot.com/products/D1Ultra)
- [AGIBOT — C5 product page](https://www.agibot.com/products/C5)
- [AGIBOT — New generation of embodied AI robots and models (2026-04-17)](https://www.agibot.com/article/231/detail/63.html)
- [AGIBOT — UK APC2026 in London](https://www.agibot.com/article/231/detail/81.html)
- [AGIBOT — IFA 2026](https://agibot.com/article/231/detail/96.html)
- [AGIBOT — No. 1 in H1 2026 shipments (Counterpoint)](https://agibot.com/article/231/detail/89.html)
- [PR Newswire via AAP — Four new products at WAIC 2026 (2026-07-20)](https://www.aap.com.au/aapreleases/cision20260719ae07639/)
- [AimDK_X2 documentation](https://x2-aimdk.agibot.com/en/latest/)
- [GitHub — AgibotTech organisation](https://github.com/AgibotTech)
- [GitHub — AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)
- [GitHub — OpenDriveLab/Agibot-World (GO-1, dataset)](https://github.com/OpenDriveLab/Agibot-World)
- [Genie Studio](https://genie.agibot.com/en/geniestudio)
- [AGIBOT store — X2 Neo](https://store.agibot.com/products/x2)
- [The Robot Report — GO-2 foundation model (2026-04-09)](https://www.therobotreport.com/agibot-releases-go-2-foundation-model-embodied-ai/)
- [AI Business — Agibot expands portfolio with four new products](https://aibusiness.com/robotics/agibot-expands-embodied-ai-portfolio-new-products)
- [Yicai Global — AgiBot taps Minth Group for European rollout](https://www.yicaiglobal.com/news/global-humanoid-robot-leader-agibot-taps-minth-group-to-drive-european-rollout)
- [Pudong government — AgiBot enters German market](https://english.pudong.gov.cn/2026-02/28/c_1162918.htm)
- [Yicai Global — 15,000th humanoid robot](https://www2.yicaiglobal.com/news/chinas-agibot-ships-15000th-humanoid-robot-completes-live-tablet-quality-inspection-test)
- [Gasgoo — IDC: AgiBot leads H1 2026 shipments](https://autonews.gasgoo.com/articles/news/idc-agibot-leads-global-humanoid-robot-shipments-with-over-8600-units-in-h1-2108532019490680833)
- [Gasgoo — AgiBot launches Hong Kong IPO process](https://autonews.gasgoo.com/articles/news/agibot-launches-hong-kong-ipo-process-2082120389458100225)
- [TechNode — New funding round at RMB 50 bn valuation (2026-10-14)](https://technode.com/2026/10/14/robot-maker-agibot-nears-new-funding-round-at-rmb-50-billion-valuation/)
