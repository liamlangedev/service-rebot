---
type: roadmap
company: "D-Robotics"
slug: D-Robotics
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# D-Robotics — Roadmap and Strategy

⬆ [D-Robotics profile](D-Robotics.md) · [Product portfolio](D-Robotics-Products.md) · [Developer guide](D-Robotics-Developer-Guide.md)

> **In one line:** a well-funded (about **USD 770M** disclosed since 2025) chip-and-platform supplier that wants to be the default "brain" under other companies' robots, from vacuums to humanoids. It wins when developers and start-ups ship products on its boards.

## Company trajectory

| Date | Milestone |
|---|---|
| May 2024 | Spun off from Horizon Robotics as an independent robotics compute company |
| 2024 (H2) | RDK X5 (10 TOPS) launched; RDK Ultra (96 TOPS) teased. Exact launch date ⚠️ unverified |
| 2025 | Series A, **USD 100M** |
| Mid-2025 | RDK S100 (80 TOPS, CPU + BPU + MCU on one SoC) launched at RMB 2,799. Exact date ⚠️ unverified |
| 21 Nov 2025 | DDC 2025 developer conference, Shenzhen: Sunrise **S600** (560 TOPS) previewed, one-stop cloud development platform announced. Company-reported: shipments **+180%** YoY, customers +200%, **100,000+** developers, 500+ universities, 60+ ecosystem partners |
| Mar 2026 | embedded world (Nuremberg): RDK S100 + LeRobot demo. Series B1 **USD 120M** (reported 16 Mar) |
| Apr 2026 | Series B2 **USD 150M** (Series B total USD 270M) |
| Summer 2026 | RDK Challenge 2026 Summer: 45 days, 11 community projects |
| Aug 2026 | "X-Lens" open-sourced (per official blog title; details ⚠️ unverified). RDK S100P reviewed by trade press |
| Sep 2026 | IFA Berlin showcase of consumer robots on Sunrise chips. **Series C USD 400M** (17 Sep). ROSCon Global, Toronto (22–24 Sep): demos with AgileX Piper arm and LooperRobotics cameras, lightning talk on "AI-native + ROS" |
| 30 Sep – 15 Dec 2026 | Robotics Dream Keeper Challenge 2026 Winter on RDK X5 (judging 16–31 Dec, awards 7 Jan 2027). Stage 2 "Build" (11–26 Nov) runs during this hackathon |
| Nov 2026 | RDK S600 manual (v5.1.1) and TROS support for S600 live on the developer portal; docs repos updated daily |

## Current focus projects

- **Scaling the S600 into embodied-AI customers.** Company-reported: **20+** embodied-AI customers within six months of launch, most in mass production. Named: TARS, **Spirit AI** (also on site at Leukerbad), X Square Robot, UBTECH, PaXini, Astribot, Fourier, Booster Robotics.
- **Volume consumer robotics.** **8M+** Sunrise chips shipped cumulatively (H1 2026); robot vacuums, mowers, companion robots, drones, a rideable outdoor wagon (Kago).
- **Developer funnel.** RDK X5 as the cheap entry board, RDK Classroom course, RDK Studio with the Moss AI assistant, seasonal online challenges, university programmes.
- **Model zoo refresh.** One unified `main` branch now targets X5, S100, S100P and S600; recent additions include YOLO26, Gemma4-E2B, MiniCPM5-2B, Pi0 and ACT submodules, HIMLoco for Unitree Go2.
- **Gravity Program (DGP).** Start-up support from product definition to supply chain, go-to-market and fundraising; **500+** teams across 10 categories.
- **Partner demos at ROS events.** Arms (AgileX Piper), spatial cameras with embedded X5 modules (LooperRobotics), community robots.

## Announced and upcoming products

| Item | Status | Timing | Notes |
|---|---|---|---|
| RDK S600 developer platform | 🧪 | Previewed Nov 2025, release slated Q1 2026; English manual live Nov 2026 | Availability outside China reported as limited (see profile). 560 TOPS is a vendor figure with a sparsity footnote |
| One-stop cloud development platform | 🧪 | Announced 21 Nov 2025 | Three services: data closed loop, embodied training field (parallel sim training), agent development service. No public self-serve access found |
| "Sunrise chips at every compute tier" | 🔭 | Stated use of Series C proceeds (Sep 2026) | No specific new chip named publicly |
| Full-chain robot software platform | 🔭 | Stated use of Series C proceeds | Builds on RDK OS, TROS, RDK Studio, cloud platform |
| S600-based robot controllers by ODM partners | 🔭 | Announced Nov 2025 | Partners named in trade press include Huaqin and Luxshare; product dates not public |
| DDC 2026 conference | ⚠️ unverified | DDC 2025 was on 21 Nov; no 2026 date confirmed | If it follows last year's rhythm, new announcements could land within weeks of this hackathon (inference) |
| RDK Ultra | ⚠️ unverified | — | Still referenced in the S-series manual's family list, absent from the 2026 product navigation |

## Strategic direction and markets

- **Positioning:** infrastructure supplier, not a robot maker. Stated ambition (DDC 2025): the "mother ecosystem" of the robot era. Analogy most observers use: an NVIDIA Jetson alternative with lower price points and integrated real-time MCU cores.
- **Two-speed market:** high-volume consumer robots today (cash and chip volume) and embodied AI / humanoids next (S100 / S600).
- **"Brain + cerebellum" on one chip:** AI cores and real-time R52+ cores together, to replace the separate motion-control board in humanoids and quadrupeds.
- **Funding:**

| Round | Amount | Date | Investors (as reported) |
|---|---|---|---|
| Series A | USD 100M | 2025 | see profile |
| Series B1 | USD 120M | Mar 2026 | see profile |
| Series B2 | USD 150M | Apr 2026 | see profile |
| Series C | USD 400M | 17 Sep 2026 | strategic investment from an unnamed "leading global internet company", institutional investors, existing shareholders |

- **Business momentum (company-reported, H1 2026):** revenue up several-fold YoY; embodied-AI business in mass production. Absolute revenue: not public. IPO plans: not public.
- **Europe:** trade-show presence (embedded world Nuremberg Mar 2026, IFA Berlin Sep 2026) and reseller distribution. No European office or entity confirmed.
- **Switzerland:** no office, customer or partnership found. The Leukerbad hackathon appears to be its first visible Swiss activity (inference).
- **North America:** ROSCon Global 2026 (Toronto) via partner booths; Ultralytics collaboration (YOLO benchmarks and demos).
- **Ecosystem partnerships:** Hugging Face LeRobot (fork and BPU tooling), Ultralytics, AgileX, LooperRobotics, OriginBot education platform; DDC 2025 strategic S600 customers additionally listed Fourier, Booster Robotics, X Square Robot, Robotera, LimX Dynamics, GAC Group and two Chinese humanoid innovation centres (names from a machine-translated article; English mapping partly inferred).
- **Risks to keep in mind:** ecosystem narrower than NVIDIA's; export-control sensitivity (the Series C release footnotes TPP below 4800); S600 availability outside China.

## Research and open-source activity

- **GitHub:** about **269 public repositories**; core perception, kernel, camera and docs repos were updated within the last two days. Most-starred: `rdk_model_zoo` (406), `moss` (144), `hobot_stereonet` (79), `x5-rdk-gen` (71).
- **Open-source building blocks:** TROS nodes (hobot_dnn, hobot_cv, hobot_codec, hobot_mipi_cam), stereo depth and occupancy (`hobot_stereonet`, `dstereo_occnet`), OS build tooling and X5 kernel, LeRobot BPU tools, `openpi_runtime`, agent tooling (`moss`, `rdk-skills`).
- **Algorithms presented at DDC 2025:** stereo depth, stereo occupancy and "Omni-OCC" multi-stereo panoramic occupancy; "VO-DP" vision-only manipulation policy with vendor claims against DP / DP3. Peer-reviewed papers behind these: not checked, ⚠️ unverified.
- **Simulation and learning:** `drobotics_robosim` (Gazebo home-robot testbed, early) and `robot-learning-platform` (MuJoCo / MJX web workbench for MicroDuck + X5, Sim2Real pending real measurements). The cloud training field reportedly supported a CVPR challenge / RoboTwin.
- **Academic programme:** a young-scholars research funding scheme for embodied intelligence was announced at DDC 2025; 500+ universities use the platform (company-reported).
- **No own foundation model or public dataset** found. The strategy is to run other people's models (Pi0, ACT, Qwen-VL, YOLO) efficiently.

## What would impress this company at the hackathon

*Inference from the strategy above, not stated by D-Robotics.* Their pitch is "our board is the brain of your robot", so they will favour projects that prove it on someone else's body, fully on-device, and look like a product.

| What they likely value | Why |
|---|---|
| **Everything runs on the board, no cloud, no laptop in the loop** | Core selling point versus cloud AI and versus a Jetson |
| **BPU actually used** (zoo model or your own converted model, measured FPS shown) | Demonstrates the toolchain, their main adoption hurdle |
| **Cross-vendor integration:** RDK as brain for a Unitree, AGIBOT, Dobot, Flexiv or Galaxea robot | Mirrors how they sell (S600 inside Spirit AI, Fourier, UBTECH) |
| **Reusable ROS 2 package** with a clean README, publishable to NodeHub | Feeds their developer ecosystem |
| **Product-shaped idea with a cost story** (a CHF 100–200 board instead of a CHF 1,000+ computer) | Gravity Program looks for start-up-ready concepts |
| Use of RDK Studio / Moss or the stereo camera | Their newest tooling and accessories |

Track-specific angles:

| Track | Idea that plays to their strengths |
|---|---|
| T01 Autonomous Urban Services | RDK X5 / S100 as the perception and navigation computer on a quadruped or wheeled base: stereo depth + open-vocabulary detection for snow, steps and pedestrians on steep village streets; coverage-cleaning logic reused from their home-robot stack |
| T02 Resilient & Safe City | Battery-powered edge sentinel: X5 + camera detecting rockfall debris, blocked paths, smoke or a person down, sending only alerts (low bandwidth, privacy-preserving); or the same node riding a quadruped patrol |
| T03 Sustainable City | Low-cost vision sorter: X5 + YOLO classifying waste on a small conveyor, triggering another vendor's arm; emphasise watts per inference and bill of materials |
| T04 Elderly Care & Rehabilitation | On-device fall / pose / gait monitoring and voice interaction for spa and clinic guests with **no video leaving the device**; rehab-exercise counter using pose models; companion-robot behaviours with the small on-board VLM |

Things unlikely to impress: using the board as a plain Linux PC with CPU-only inference, or streaming camera frames to a cloud model.

Research note: live web search was unavailable while preparing this file, so any announcement from the last few weeks (for example a DDC 2026 date or a new chip) may be missing. Ask the D-Robotics team on site.

## Sources

- [Kyodo PR Wire: USD 400M Series C (17 Sep 2026)](https://kyodonewsprwire.jp/release/202609176168)
- [36Kr: DDC 2025 and S600](https://eu.36kr.com/en/p/3566819733830529)
- [D-Robotics blog index](https://en.d-robotics.cc/blog)
- [D-Robotics blog: ROSCon Global 2026](https://en.d-robotics.cc/blog/d-robotics-heads-to-roscon-global-2026)
- [D-Robotics blog: embedded world 2026](https://en.d-robotics.cc/blog/d-robotics-returns-to-embedded-world-2026-with-the-theme-intelligence-embedded-robotics-reborn)
- [Robotics Dream Keeper Challenge 2026 Winter](https://github.com/D-Robotics/Robotics-Dream-Keeper-Challenge-Winter)
- [D-Robotics GitHub organisation (repository list)](https://github.com/orgs/D-Robotics/repositories?type=all&sort=stargazers)
- [rdk_model_zoo README](https://github.com/D-Robotics/rdk_model_zoo)
- [drobotics_robosim](https://github.com/D-Robotics/drobotics_robosim)
- [robot-learning-platform](https://github.com/D-Robotics/robot-learning-platform)
- [RDK S series manual](https://developer.d-robotics.cc/rdk_s_doc/en/RDK)
- [TROS: installation](https://developer.d-robotics.cc/tros_doc/en/quick_start/install_tros)
- [Caixin Global: Series B1 (16 Mar 2026)](https://www.caixinglobal.com/2026-03-16/d-robotics-raises-120-million-as-investor-appetite-for-embodied-ai-grows-102423516.html)
- [Yicai Global: Series B2](https://www2.yicaiglobal.com/news/chinas-d-robotics-raises-usd150-million-in-new-funding-series-b-total-hits-usd270-million)
- [TechNode: Series C](https://technode.com/2026/09/18/d-robotics-raises-400-million-in-series-c-funding/)
- [Hackster: RDK X5 launch and RDK Ultra tease](https://www.hackster.io/news/d-robotics-launches-the-10-tops-edge-ai-rdk-x5-and-teases-the-96-tops-rdk-ultra-c88714dab9d5)
- [KrASIA: RDK S100 launch](https://kr-asia.com/as-robots-get-smarter-d-robotics-ships-an-soc-kit-to-close-the-loop)
- [D-Robotics profile (this folder)](D-Robotics.md)
