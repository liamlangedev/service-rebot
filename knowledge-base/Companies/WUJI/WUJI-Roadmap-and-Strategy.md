---
type: roadmap
company: "WUJI"
slug: WUJI
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# WUJI — Roadmap and Strategy

⬆ [WUJI profile](WUJI.md) · [Product portfolio](WUJI-Products.md) · [Developer guide](WUJI-Developer-Guide.md) · [Solutions and projects](WUJI-Solutions-and-Projects.md)

> **Read this first:** WUJI (舞肌科技, Wuji Tech) publishes **no dated product roadmap**. What follows is assembled from its release notes, docs warnings, GitHub READMEs and its own videos, plus Chinese trade press for funding. Funding data comes from third-party databases and press, **not** from a WUJI announcement, and the sources label the rounds differently — treat round names as ⚠️ unverified and investor names as reported.
> **One-line strategy:** be the open, research-grade **dexterous hand + human-data** supplier for embodied-AI model builders — sell the hand, the glove and a free software stack, and let partner models (Dyna-2, RynnBrain, Natura-1, GENE-26.5, pi0.5) prove the hardware.

## Company trajectory

| Date | Milestone | Source type |
|---|---|---|
| 2018 | Founder **Pan Yunzhe (潘韫哲)** graduates from UIUC (computer science and chemistry), per IT Juzi | trade press |
| 2019-03 | Company founded; starts with **high-torque-density micro motors**. Press and databases name the founding entity 上海舞肌科技有限公司 (Shanghai); the current site lists Shenzhen and Beijing offices and carries a Shanghai ICP filing | official (year) + press (month, entity) |
| 2019 – about 2022 | "F-series" motor developed over roughly three years; press quotes **8 N·m peak torque at 200 g** | trade press ⚠️ unverified |
| 2023-08 | Angel round (IT Juzi) | trade press ⚠️ unverified |
| 2023-11-24 | Pre-A round — ZhenFund (真格基金), Sequoia China Seed Fund (TheRoboRadar) | database |
| late 2023 | Full pivot from motors to dexterous hands (Chinese press summary; article itself could not be opened) | ⚠️ unverified |
| 2025-09-17 | **Wuji Hand (gen 1) released**: 20 DoF, direct drive, USB | official video |
| 2025-11-07 to 12-05 | Gen-1 firmware reaches full closed-loop control, then v1.0.0 with 1 kHz real-time control | official changelog |
| 2025-11-13 | Round reported as "Pre-A+" (TheRoboRadar) or "A" (IT Juzi) — 5Y Capital (五源资本), Huafang, ZhenFund, Sequoia China | database / press |
| 2026-02-06 | Round reported as "A" (TheRoboRadar) or "A+" (IT Juzi) — Alphaist Partners, 中移和创, Huafang Capital, 碧鸿投资 | database / press |
| 2026-02-09 / 02-14 | Wuji Studio + Python SDK, then **Wuji Glove 1.0** | official |
| 2026-03 to 2026-07 | "Several A+ rounds in quick succession" (IT Juzi); listed round on **2026-07-15**: Monolith, 尚势资本, Meituan Longzhu (美团龙珠), **Ant Group**, 德石投资 | database / press |
| 2026-04 to 2026-05 | Partner model demos on Wuji Hand: LiberAI breakfast preparation, Genesis AI GENE-26.5 | official videos |
| 2026-06-01 / 06-05 | **Wuji Hand 2** release film, then global debut at **ICRA 2026** (Vienna) | official videos |
| 2026-06-10 / 06-15 | `wuji-openpi` released; TopoRetarget paper (CoRL 2026) | GitHub / arXiv |
| 2026-07 | Software generation change: unified resource-style SDK, Hand 2 in the C SDK, retargeting moved into the SDK, firmware v2.0.0 for Hand 2.2 | release notes |
| 2026-08 | Dyna-2 (Dyna Robotics) and RynnBrain 1.1 (Alibaba DAMO) real-robot work on Wuji hands | official videos + partner pages |
| 2026-08-26 | Beijing News reports valuation "risen to **RMB 5 billion**" after several rounds in the year | single press source ⚠️ unverified |
| 2026-09 | VLA post-training paper and report (20 / 20 on five skills); MINT open-sourced; X Square Robot's WALL-B reported as adapted to the Wuji Hand (database news item ⚠️ unverified) | arXiv / official / database |
| 2026-10 | Natura-1 (Nature Will, ROKAE AR5 arms + Wuji hands); EgoExplorer dataset uses Wuji Glove; **IROS 2026** booth and salon (Pittsburgh); ROS 2 drivers, macOS SDK, RL checkpoint bundle | official |
| 2026-11-10 | Hand 2 firmware **v3.0.0** with position mode (Beta); SDK and CLI on Windows; glove calibration solver 15× faster | release notes |
| 2026-11-14 to 11-16 | On site at the Leukerbad Robotics Hackathon | event context |

Cadence worth noting: **26 dated software releases between 2026-02-09 and 2026-11-10** — roughly one every two weeks.

## Current focus projects

| Focus | What is happening now | Evidence |
|---|---|---|
| **Wuji Hand 2 from prototype to product** | Two beta revisions in the field (2.1 frozen, 2.2 active). Docs list what is still open: thermal design, durability, joint zero accuracy, back-drive consistency, soft-pad hardness, skin design, load curves | [Hand 2 user notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md) |
| **Control maturity** | MIT mode default; whole-hand position mode added as Beta; feed-forward compensation from October 2026 units; thermal derating and current-sensing fault tolerance added in firmware | [release notes](https://docs.wuji.tech/docs/en/release-notes.md) |
| **One software stack** | Unified SDK + CLI replaces Studio, HMI, Upgrader, `wujihandpy`; now on Linux, macOS (Apple silicon), Windows, Android (C); ROS 2 Lyrical drivers; Docker recipe; AI-agent skills for the CLI | [SDK overview](https://docs.wuji.tech/docs/en/wuji-sdk/latest/introduction.md) |
| **Human-data loop** | Glove → retargeting → hand → MCAP → RL / VLA. Recent work is on data quality: EMF confidence warnings, IMU timestamp stability, guided tactile calibration, offline re-solving | [glove docs](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md) |
| **Dexterous learning showcases** | Pen spinning under disturbance (RL), VLA post-training on dual Tianji arms + dual Wuji hands, TopoRetarget, MINT | [papers](WUJI-Papers-and-Research.md) |
| **Model-company partnerships** | Hands supplied to or used by Dyna Robotics, Alibaba DAMO, Nature Will, Genesis AI, LiberAI, Gento; open call for teams to co-develop real-world dexterous applications | [solutions register](WUJI-Solutions-and-Projects.md) |
| **Gen-1 hand in maintenance** | Docs mark gen 1 as "kept for existing devices"; still supported by the unified SDK | [docs home](https://docs.wuji.tech/docs/en/index.md) |

## Announced and upcoming products

No item below has a published date. "Official" = WUJI wrote it; "inferred" = follows from WUJI's wording.

| Status | Item | When | Basis |
|---|---|---|---|
| 🧪 | **Wuji Hand 2.2 Beta** — current hardware, firmware v3.0.0 (2026-11-10) | shipping as beta now | official |
| 🧪 | **Position control mode** for Hand 2 leaving Beta | no date | inferred from the "(Beta)" label |
| 🔭 | **Wuji Hand 2 final / production version** — both revisions are called prototypes whose parameters "don't represent the final product" | no date | inferred |
| 🔭 | **Tactile sensing on Hand 2** — 2.2 is described as a "non-tactile prototype" | no date | inferred |
| 🔭 | **New external interface and supply-voltage range** for Hand 2 (no longer XT30 + RJ45 as two separate cables) | "later versions" | official (docs warning) |
| 🔭 | **Product version of the hand + arm teleoperation stack**, replacing the unmaintained `wuji-hand-teleop` | "coming soon" | official (README) |
| 🔭 | **VLA post-training code** (hand-action codec, DAgger takeover, residual RL) | "when it is released" | official (report) |
| 🔭 | Deformable soft-pad simulation; SDK-label-to-model-actuator axis mapping; IMU-to-hand frame definition; wrist load, bending and screw specifications; electrical pin-out and power figures | "will be added later" | official (docs notes) |
| 🔭 | Hand 2 unboxing and setup video | "in production" | official (videos page) |
| 🔭 | More device types — the SDK is described as covering gloves, hands "and more" / "other peripherals" | no date | inferred |
| — | Arm, wrist, humanoid, wireless glove, own foundation model | nothing announced | — |

Prices are not published by WUJI. Third-party figures: gen-1 list price **¥39,800** (TheRoboRadar), reseller "from US$5,500" and Hand 2 listings of US$14,600–19,500 — all ⚠️ unverified.

## Strategic direction and markets

**Positioning**

- Stated mission: give robots human-level dexterous manipulation and speed up general physical intelligence.
- Technical bet: **fully direct-drive, 20 independent joints**, built on in-house motors, instead of tendon or linkage hands. Chinese press places WUJI among the mid-stream whole-hand makers (with Linkerbot and Sharpa) and as a representative of the direct-drive / quasi-direct-drive route; one outlet files it under core drive components because of the motor origin.
- Hand 2's headline change is **back-drivability and compliance** ("yield over strength"). Press also quotes an industry practitioner saying gen 1 had heat and return-rate problems that gen 2 improved (temperatures under 50 °C) — third-party claim ⚠️ unverified.
- Business model: hardware sales on inquiry (sales@wuji.tech) plus a free, permissively licensed software stack. No subscription, no vertical solutions, no certified products.

**Customers and partners (all research / demo use, none a field deployment)**

| Type | Names |
|---|---|
| Embodied-AI model companies | Dyna Robotics (USA), Genesis AI, LiberAI, Nature Will, X Square Robot (⚠️ unverified), Gento |
| Corporate / institutional labs | Alibaba DAMO Academy (RynnBrain 1.1), Shanghai AI Laboratory (EgoExplorer) |
| Universities (co-authors) | IIIS Tsinghua, ShanghaiTech, HKU, Zhejiang University |
| Arm pairings seen in public work | Tianji 7-DoF (WUJI's own reference), ROKAE AR5 (Nature Will), YAM 6-DoF (Dyna) |
| Distribution | Direct from Shenzhen / Beijing; US reseller Robotics Center linked from the site footer |

**Funding**

| Reported date | Round label (source A / source B) | Reported investors | Amount |
|---|---|---|---|
| 2023-08 | Angel (IT Juzi only) | not named | undisclosed |
| 2023-11-24 | Pre-A | ZhenFund, Sequoia China Seed Fund | undisclosed |
| 2025-11-13 | Pre-A+ / A | 5Y Capital, Huafang, ZhenFund, Sequoia China | undisclosed |
| 2026-02-06 | A / A+ | Alphaist Partners, 中移和创, Huafang Capital, 碧鸿投资 | undisclosed |
| 2026-07-15 (and others Mar–Jul) | A+ | Monolith, 尚势资本, Meituan Longzhu, Ant Group, 德石投资 | undisclosed |

- Valuation: "risen to RMB 5 billion" in one Beijing News article (2026-08-26). No second source found.
- Context: Chinese press describes a 2026 funding surge across the dexterous-hand sector, with WUJI named among companies closing several rounds in the first seven months.
- No amounts, revenue, headcount or shipment figures are public. An industry list (Aibang, 2026-07-31) includes WUJI among 29 hand suppliers without a volume.

**Europe and Switzerland**

- **No European office, subsidiary or distributor found.** Offices listed: Shenzhen (Bao'an) and Beijing (Haidian).
- European touchpoints on record: Hand 2's public debut at **ICRA 2026 in Vienna** (June 2026) and this hackathon in Leukerbad (November 2026). The official X handle is `@wuji_global`, and the GitHub profile advertises international hiring.
- Docs, SDK and site are fully bilingual (English / Chinese); the US is the only market with a named reseller.
- No CE, medical or safety certification is mentioned for any product — relevant for any European pilot.

## Research and open-source activity

| Area | Output | Status |
|---|---|---|
| Papers | TopoRetarget (CoRL 2026, arXiv 2606.16272) with IIIS Tsinghua; VLA post-training (arXiv 2609.19666) with ShanghaiTech; MINT (arXiv 2609.04958) with ShanghaiTech, Tsinghua, HKU, Zhejiang | ✅ published |
| Third-party research on WUJI hardware | EgoExplorer dataset (glove), Dyna-2, RynnBrain 1.1, Natura-1, GENE-26.5 | ✅ public |
| Core tooling (MIT) | `wuji-sdk`, `wuji-cli`, `wuji-ros2`, `wuji-description`, `toporetarget`, `wuji-hand-teleop` | ✅ active except teleop (unmaintained) |
| Learning stacks (Apache-2.0) | `wuji-mjlab` (with checkpoints, 40 pen-spin clips, jig CAD), `wuji-isaaclab`, `wuji-openpi` | ✅ active |
| Data / models released | RL checkpoints; pen-spin capture bundle; MINT weights and annotations for 560,649 episodes / 1,021 h of egocentric video | ✅ |
| Not released | WUJI VLA or foundation-model weights, teleoperation demonstration datasets, post-training code | 🔭 / not public |
| Community | Docs with `llms.txt` and agent skills, open lecture notes on rigid-body mechanics, "Wuji's Talk" podcast / salon series, IROS 2026 salon | ✅ |

Pattern: WUJI opens the full path from **human motion to robot hand** (capture, retarget, simulate, train, deploy) and keeps the hardware and firmware closed. About 24 public repos; details and author lists are in [papers and research](WUJI-Papers-and-Research.md).

## What would impress this company at the hackathon

**Inference, not a WUJI statement.** Derived from where WUJI spends its engineering time and what its partner videos show.

General signals:

- **Use the 20 DoF.** A task a parallel gripper could do will not stand out. Pinch, in-hand adjustment, tool use, lids, zips, cutlery, switches do.
- **Use compliance on Hand 2.** Tune kp / kd per finger and show safe, yielding contact — the feature gen 2 was built around.
- **Close the data loop.** Glove teleop → MCAP recording → a learned or replayed skill is exactly WUJI's published pipeline; even a small imitation result from on-site demonstrations fits their story.
- **Integrate with another vendor's arm cleanly.** WUJI has no arm; a reusable mount + TF + driver bridge for an arm at the venue (ROKAE, Flexiv, Dobot, Unitree, AGIBOT and others) is directly useful to them. ROKAE + Wuji already has a public precedent (Natura-1).
- **Give feedback on the beta.** Documented bugs, a ROS 2 Humble / Jazzy bridge, a LeRobot adapter, or the missing SDK-to-model axis mapping would be contributions they can ship.
- **Stay inside the limits.** Indoor, dry, supervised; no medical or safety claims.

| Track | Idea that plays to WUJI's strengths | Why it fits |
|---|---|---|
| **T01 Autonomous Urban Services** (T01.3, T01.5, T01.7) | Mobile manipulator with a Wuji Hand 2 that operates human interfaces: lift buttons, door handles, card readers, handing over small items | Shows fingers doing what grippers cannot; mirrors partner demos (meal delivery, tidying) |
| **T02 Resilient & Safe City** (T02.2, T02.7) | Glove-driven dexterous teleoperation of valves, breakers, connectors and tools from a safe distance, with recorded sessions that later seed autonomy | WUJI's own IROS booth demo was hands-on teleoperation; strongest natural fit |
| **T03 Sustainable City** (T03.1, T03.6) | Fine disassembly or sorting step that needs dexterity (unscrewing caps, separating mixed-material items, pulling batteries), taught by demonstration | Weakest fit — only convincing if the task truly needs fingers |
| **T04 Elderly Care & Rehabilitation** (T04.1, T04.3, T04.7) | Glove-only hand-function assessment (grip-pressure map, finger range, contact events over time), or a compliant assistive hand that opens containers and holds a cup or spoon | Uses the 526-point tactile glove without any robot, or Hand 2's back-drivability near people |

## Sources

- [Wuji Technology official site](https://www.wuji.tech/en) · [Purchase and Partnership](https://www.wuji.tech/en/cooperation) · [Careers (office addresses)](https://www.wuji.tech/en/careers) · [VLA post-training report](https://www.wuji.tech/blog/post-training-0)
- [Wuji Docs release notes](https://docs.wuji.tech/docs/en/release-notes.md) · [docs index](https://docs.wuji.tech/_llms/en.txt) · [docs home](https://docs.wuji.tech/docs/en/index.md) · [videos page](https://docs.wuji.tech/docs/en/videos.md)
- [Wuji Hand 2 user notice (capability boundaries)](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md) · [electrical and network integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/electrical-network-integration.md) · [control guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/control-guide.md) · [Hand 2 overview](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md)
- [Wuji SDK overview](https://docs.wuji.tech/docs/en/wuji-sdk/latest/introduction.md) · [Wuji Glove introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md)
- GitHub: [wuji-technology](https://github.com/wuji-technology) · [wuji-sdk](https://github.com/wuji-technology/wuji-sdk) · [wuji-ros2](https://github.com/wuji-technology/wuji-ros2) · [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop) · [wuji-openpi](https://github.com/wuji-technology/wuji-openpi) · [wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab)
- [YouTube channel @WUJI_TECH](https://www.youtube.com/@WUJI_TECH/videos) (release, ICRA, IROS and partner videos; individual links in the [solutions register](WUJI-Solutions-and-Projects.md))
- arXiv: [2606.16272 TopoRetarget](https://arxiv.org/abs/2606.16272) · [2609.19666 VLA post-training](https://arxiv.org/abs/2609.19666) · [2609.04958 MINT](https://arxiv.org/abs/2609.04958) · [2610.18872 EgoExplorer](https://arxiv.org/abs/2610.18872)
- Funding and company background (third party): [TheRoboRadar — WUJI TECH company profile](https://theroboradar.com/companies/wuji-tech) · [IT Juzi via Sina Tech — 2026 dexterous-hand funding review (2026-08-12)](https://finance.sina.com.cn/tech/roll/2026-08-13/doc-inimzytm3603256.shtml) · [Beijing News — dexterous-hand funding feature (2026-08-26)](https://m.bjnews.com.cn/detail/1787753981129466.html) · [GGII via Tencent News — funding in the first seven months of 2026 (2026-08-05)](https://news.qq.com/rain/a/20260805A0ERC600)
- Industry context (third party): [Dingjiao One via Sina Finance — "no standard hand yet" (2026-08-11)](https://finance.sina.com.cn/roll/2026-08-11/doc-inimwyqv4421934.shtml) · [same article on Huxiu](https://m.huxiu.com/article/4882124.html) · [Aibang Robotics — 29 dexterous-hand suppliers (2026-07-31)](https://www.aibangbots.com/a/11893)
- Not opened (HTTP 403), cited only as the origin of the "late-2023 pivot" claim: [Zhihu — Ant Group and Meituan invest in Wuji Tech](https://zhuanlan.zhihu.com/p/2062483738613883285)
- In this pack: [WUJI profile](WUJI.md) · [solutions and projects](WUJI-Solutions-and-Projects.md) · [papers and research](WUJI-Papers-and-Research.md) (partner projects, dates of videos and unverified third-party prices are carried over from their sources)
