---
type: company
company: "D-Robotics"
slug: D-Robotics
hq: "Shenzhen, China"
founded: 2024
website: https://en.d-robotics.cc/
categories: [compute, components, software]
on_site_guess: "RDK X5 and RDK S100 / S100P edge-AI developer boards with cameras, running RDK OS + TogetheROS.Bot (ROS 2 Humble)"
fit_t01: 3
fit_t02: 3
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# D-Robotics

> **One-liner:** Horizon Robotics spin-off (Chinese name Digua / "Sweet Potato" Robotics) that sells the on-board brain for robots: Sunrise AI chips, RDK developer boards (5 to 560 TOPS) and a ROS 2 based software stack. It does not build robots itself.
> **Why it matters at Leukerbad:** D-Robotics is the "compute" choice, not a robot. Pick it when your idea needs cheap, low-power on-device vision / AI on a custom or third-party robot (or a fixed smart sensor), and pair it with another vendor's arm, quadruped or mobile base.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Shenzhen, China (⚠️ unverified on an official page; its developer conference DDC 2025 was held in Shenzhen; Series C release is datelined Hong Kong) |
| Founded | Spun off from Horizon Robotics in **May 2024** (site copyright runs from 2023) |
| Founders / CEO | CEO **Wang Cong**; VP developer ecosystem **Hu Chunxu** |
| Size and funding | Headcount not public. Series A **USD 100M** (2025) · Series B1 **USD 120M** (Mar 2026) · Series B2 **USD 150M** (Apr 2026) · Series C **USD 400M** (17 Sep 2026). Investors reported include Hillhouse, Vertex Growth, Linear Capital, Didi, Meituan Longzhu and an unnamed "leading global internet company" |
| Core business | Sunrise robot SoCs (BPU AI accelerator), RDK developer kits, RDK OS / TogetheROS.Bot, cloud development platform. **8M+** Sunrise chips shipped cumulatively (H1 2026) |
| Website | [en.d-robotics.cc](https://en.d-robotics.cc/) (d-robotics.cc redirects here) |
| Docs / developer portal | [developer.d-robotics.cc](https://developer.d-robotics.cc/en) · [doc center](https://developer.d-robotics.cc/rdk_doc_center/en) · [English forum](https://forum-en.d-robotics.cc/) |
| GitHub | [github.com/D-Robotics](https://github.com/D-Robotics) |

## Portfolio at a glance

| Product | Type | Status | Key specs | Price (if public) | Img key |
|---|---|---|---|---|---|
| RDK X3 (and X3 Module) | Entry edge-AI board | ✅ | Sunrise 3 chip · **5 TOPS** BPU · Raspberry Pi 4B-compatible interfaces (Module is CM4-compatible) · Ubuntu 22.04 + ROS 2 Humble | not confirmed | d-robotics-rdk-x3 |
| RDK X5 (and X5 Module) | Mid edge-AI board | ✅ | Sunrise 5 · 8x Cortex-A55 · **10 TOPS** BPU · 32 GFLOPS GPU · **4 or 8 GB** LPDDR4 · Ubuntu 22.04 + ROS 2 Humble | about **USD 100–190** depending on RAM / kit / reseller (DFRobot 8 GB kit USD 190) | d-robotics-rdk-x5 |
| RDK S100 | Embodied-AI kit (CPU + BPU + MCU on one SoC) | ✅ | S100E SoC · 6x Cortex-A78AE · 4x Cortex-R52+ real-time MCU · **80 TOPS** · **12 GB** LPDDR5 | RMB 2,799 at launch (about USD 390); resellers USD 440–630+ | d-robotics-rdk-s100 |
| RDK S100P | Higher-end embodied-AI kit | ✅ (availability outside China limited) | 6x A78AE @ 2.0 GHz · 4x R52+ · **128 TOPS** · **24 GB** LPDDR5 · 64 GB eMMC · 3x 4-lane MIPI CSI (+4 GMSL via add-on) · 2x GbE · 12–20 V, 90 W adapter · 0–45 °C | USD 899 (DFRobot) / USD 999.99 (Waveshare) | d-robotics-rdk-s100p |
| RDK S600 / Sunrise S600 | Flagship embodied-AI compute platform | 🧪 (China only so far) | **560 TOPS** (INT8, vendor figure with sparsity footnote) · 18x A78AE · 6x R52+ MCU · 6 MIPI, 6 USB 3.0, 4 PCIe 3.0 · aimed at on-device VLA / VLM / LLM | not public | d-robotics-rdk-s600 |
| RDK Ultra | Older high-compute board (96 TOPS) | ⚠️ unverified current status (not on the 2026 official product nav) | 96 TOPS (trade press) | not public | d-robotics-rdk-ultra |
| RDK Stereo Camera family + accessories | Sensors / add-ons | ✅ | Stereo camera SDK on GitHub; MIPI cameras, camera and MCU expansion boards | not confirmed | d-robotics-stereo-camera |
| TogetheROS.Bot (TROS) | Robot middleware | ✅ | ROS 2 Foxy / Humble / Jazzy based · BPU-accelerated nodes (hobot_dnn, hobot_codec, hobot_sensor, hobot_cv) · apt install | free, open source | d-robotics-tros |
| RDK Studio | Desktop dev workspace | ✅ | Device manager, flashing, terminals, "Moss" AI assistant, board-side OpenClaw agent · supports X3, X5, S100 / S100P | free | d-robotics-rdk-studio |
| NodeHub + RDK Model Zoo | App / model library | ✅ | **200+** open-source algorithms and demos · model zoo (YOLO family etc.) | free | d-robotics-nodehub |
| One-stop cloud development platform | Cloud toolchain | 🧪 | Data closed loop, embodied training field (sim), agent development service (announced Nov 2025) | not public | d-robotics-cloud-platform |

Note: TOPS figures are vendor numbers and not directly comparable with NVIDIA Jetson ratings.

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organisers):**

- **RDK X5 kits** in quantity: the standard giveaway / workshop board at their developer events (prize draw at embedded world 2026), cheap, well documented in English.
- **RDK S100 (possibly S100P)**: the board they demoed in Europe in March 2026 with Hugging Face LeRobot and ACT policies; the natural pick for an embodied-AI hackathon.
- **Cameras** (MIPI / stereo) and possibly a small reference robot or a LeRobot-style arm demo. ⚠️ unverified.
- **RDK S600: unlikely** (reported as China-only for now).
- No robots of their own. Expect them to act as the compute layer for other teams' hardware and to staff technical support.

## Developer platform (summary)

- **OS:** RDK OS, an Ubuntu 22.04 image (Linux 6.1 on S100P); flashing via RDK Studio or the D-Navigation tool from Windows, Linux or Apple-silicon Mac.
- **Languages:** Python and C/C++; standard ROS 2 packages run unmodified, accelerated nodes come from TogetheROS.Bot (`apt install`).
- **AI toolchain:** OpenExplorer converts ONNX models to the board format with **INT8 quantization** (`.hbm` on S100). Compiled models are board-specific. Custom models need this conversion step, so budget time; pre-converted models from the Model Zoo are the 48-hour shortcut.
- **Pretrained models:** [rdk_model_zoo](https://github.com/D-Robotics/rdk_model_zoo) (YOLO family and more); NodeHub one-command demos (detection, pose, gesture, voice, SLAM-style apps).
- **Robot learning:** forked LeRobot with BPU tooling; **ACT policy on RDK S100** documented on the forum. Pi0 and Qwen2.5-VL optimisation is claimed for the S600 only.
- **Real-time control:** S100 / S100P / S600 include Cortex-R52+ MCU cores for motor loops next to the AI cores (S100P caveat: BMI088 IMU on the MCU expansion board unsupported in some OS versions).
- **Agent tooling:** RDK Studio "Moss" assistant, OpenClaw board-side agent, and an [rdk-skills](https://github.com/D-Robotics/rdk-skills) repo. Not a safety or real-time controller.
- **Simulation:** a `drobotics_robosim` repo exists and a cloud "embodied training field" is announced; maturity ⚠️ unverified.
- **Ecosystem caveat:** narrower than NVIDIA CUDA / TensorRT / Isaac; no CUDA.
- **Links:** [RDK X docs](https://developer.d-robotics.cc/rdk_x_doc/en/RDK) · [RDK S docs](https://developer.d-robotics.cc/rdk_s_doc/en/RDK) · [TROS docs](https://developer.d-robotics.cc/tros_doc/en/tros) · [RDK Studio](https://developer.d-robotics.cc/en/rdkstudio) · [NodeHub](https://developer.d-robotics.cc/en/nodehub)

## Current projects, deployments and customers

- **Sep 2026:** Series C release reports **8M+** Sunrise chips shipped, embodied-AI business in mass production, **100,000+ developers**, **500+ universities**, 20+ countries. ([Kyodo PR Wire](https://kyodonewsprwire.jp/release/202609176168))
- **Sep 2026:** Sunrise S600 adopted by **20+** embodied-AI customers within six months, including Spirit AI, UBTECH, Fourier, Booster Robotics, Astribot, PaXini, TARS and X Square Robot. Spirit AI is also on site at Leukerbad. ([Kyodo PR Wire](https://kyodonewsprwire.jp/release/202609176168))
- **Sep 2026 (IFA Berlin):** consumer robots on Sunrise chips shown: TCL "hey AiMe" companion robot, Vbot SuperDog, xLean TR1 floor-washing robot. ([OpenELAB](https://openelab.io/blogs/learn/d-robotics-ifa-2026-home-robot-ai-chips-rdk))
- **Mar 2026 (embedded world, Nuremberg, booth 3A-426):** RDK S100 + LeRobot demo, Ultralytics YOLO26 demo; Gravity Program start-ups Vbot SuperDog, Aura home companion, BirdieSense golf coach. ([D-Robotics blog](https://en.d-robotics.cc/blog/d-robotics-returns-to-embedded-world-2026-with-the-theme-intelligence-embedded-robotics-reborn))
- **Mar 2026:** Leju Robotics, LimX Dynamics and RealMan Robotics reported as RDK S100 adopters. ([Caixin Global](https://www.caixinglobal.com/2026-03-16/d-robotics-raises-120-million-as-investor-appetite-for-embodied-ai-grows-102423516.html))
- **Nov 2025:** cited chip customers include a robot vacuum maker, Insta360 (drone) and a companion robot dog maker. ([36Kr](https://eu.36kr.com/en/p/3566819733830529))
- Switzerland-specific activity: none found.

## Roadmap and future direction

- **Nov 2025:** Sunrise S600 previewed at DDC 2025 (Shenzhen), official release slated for Q1 2026; 🧪 RDK S600 manual now on the developer portal (updated Nov 2026), availability reported as China-only. ([36Kr](https://eu.36kr.com/en/p/3566819733830529), [RDK S docs](https://developer.d-robotics.cc/rdk_s_doc/en/RDK))
- **Nov 2025:** 🧪 one-stop cloud platform (data closed loop, embodied training field, agent development service). ([36Kr](https://eu.36kr.com/en/p/3566819733830529))
- **2026 funding:** about **USD 670M** raised across B1, B2 and C; stated use is Sunrise chips at every compute tier plus a full-chain robot software platform. ([TechNode](https://technode.com/2026/09/18/d-robotics-raises-400-million-in-series-c-funding/), [Yicai Global](https://www2.yicaiglobal.com/news/chinas-d-robotics-raises-usd150-million-in-new-funding-series-b-total-hits-usd270-million))
- **Strategy:** "infrastructure" supplier from consumer robots (vacuums, mowers, companions) up to humanoids; Gravity Program (DGP) supports **500+** robotics start-ups.
- **Europe:** visible presence at embedded world (Mar 2026) and IFA (Sep 2026); boards sold through resellers (DFRobot, Waveshare, OpenELAB and others). No European office confirmed.
- IPO plans: not public.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | On-board perception / navigation compute for a delivery or cleaning robot built on another vendor's base; proven in consumer cleaning robots | RDK X5, RDK S100 | [T01 brief](T01-Autonomous-Urban-Services/D-Robotics-T01-1-Brief.md) |
| T02 Resilient & Safe City | 3 | Low-power edge vision node (hazard, person, smoke or snow detection) fixed or riding on a quadruped | RDK X5, RDK S100, stereo camera | [T02 brief](T02-Resilient-and-Safe-City/D-Robotics-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Supporting role: cheap vision compute for waste sorting or resource monitoring, needs someone else's actuator | RDK X5, Model Zoo | [T03 brief](T03-Sustainable-City/D-Robotics-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | On-device (privacy-friendly) fall, pose and voice sensing; chips already power companion robots | RDK X5, RDK S100, NodeHub demos | [T04 brief](T04-Elderly-Care-and-Rehabilitation/D-Robotics-T04-1-Brief.md) |

## Related docs
- [Product portfolio](D-Robotics-Products.md) · [Developer guide](D-Robotics-Developer-Guide.md) · [Roadmap and strategy](D-Robotics-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources

- [D-Robotics official site (EN)](https://en.d-robotics.cc/)
- [D-Robotics developer portal](https://developer.d-robotics.cc/en)
- [RDK X series manual](https://developer.d-robotics.cc/rdk_x_doc/en/RDK)
- [RDK S series manual (S100 / S600)](https://developer.d-robotics.cc/rdk_s_doc/en/RDK)
- [Introduction to TogetheROS.Bot](https://developer.d-robotics.cc/tros_doc/en/tros)
- [RDK Studio](https://developer.d-robotics.cc/en/rdkstudio)
- [D-Robotics GitHub org](https://github.com/D-Robotics)
- [D-Robotics blog: embedded world 2026](https://en.d-robotics.cc/blog/d-robotics-returns-to-embedded-world-2026-with-the-theme-intelligence-embedded-robotics-reborn)
- [Forum: LeRobot ACT policy on RDK](https://forum-en.d-robotics.cc/t/lerobot-act-policy-on-rdk/391)
- [Kyodo PR Wire: USD 400M Series C (17 Sep 2026)](https://kyodonewsprwire.jp/release/202609176168)
- [TechNode: Series C](https://technode.com/2026/09/18/d-robotics-raises-400-million-in-series-c-funding/)
- [Yicai Global: Series B2](https://www2.yicaiglobal.com/news/chinas-d-robotics-raises-usd150-million-in-new-funding-series-b-total-hits-usd270-million)
- [Caixin Global: Series B1 (16 Mar 2026)](https://www.caixinglobal.com/2026-03-16/d-robotics-raises-120-million-as-investor-appetite-for-embodied-ai-grows-102423516.html)
- [CNX Software: RDK S100P review (31 Aug 2026)](https://www.cnx-software.com/2026/08/31/d-robotics-rdk-s100p-a-128-tops-alternative-to-nvidia-jetson-orin-nx-16gb-with-cortex-a78ae-r52-cores/)
- [CNX Software: RDK X5](https://www.cnx-software.com/2025/06/30/d-robotics-rdk-x5-development-board-features-sunrise-x5-octa-core-soc-with-10-tops-bpu-for-ros-projects/)
- [Hackster: RDK X5 launch and RDK Ultra tease](https://www.hackster.io/news/d-robotics-launches-the-10-tops-edge-ai-rdk-x5-and-teases-the-96-tops-rdk-ultra-c88714dab9d5)
- [KrASIA: RDK S100 launch](https://kr-asia.com/as-robots-get-smarter-d-robotics-ships-an-soc-kit-to-close-the-loop)
- [36Kr: DDC 2025 and S600](https://eu.36kr.com/en/p/3566819733830529)
- [OpenELAB: D-Robotics at IFA 2026](https://openelab.io/blogs/learn/d-robotics-ifa-2026-home-robot-ai-chips-rdk)
- [OpenELAB: RDK Studio and OpenClaw](https://openelab.io/blogs/learn/d-robotics-rdk-studio-openclaw-robot-development)
- [DFRobot: RDK X5 listing](https://www.dfrobot.com/product-2944.html)
