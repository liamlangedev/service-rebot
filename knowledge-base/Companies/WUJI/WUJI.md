---
type: company
company: "WUJI"
slug: WUJI
hq: "Shenzhen, China"
founded: 2019
website: https://www.wuji.tech
categories: [dexterous-hand, data, components]
on_site_guess: "Wuji Hand / Wuji Hand 2 (20-DoF direct-drive hands) on a demo stand or partner arm, plus Wuji Glove for teleoperation"
fit_t01: 2
fit_t02: 3
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# WUJI

> **One-liner:** Wuji Technology (舞肌科技, Shenzhen) builds 20-DoF fully direct-drive dexterous robot hands and a tactile data glove, with an unusually open SDK / sim / RL / VLA software stack.
> **Why it matters at Leukerbad:** It is the only pure dexterous-hand vendor on site: an end effector you bolt onto someone else's arm or humanoid, and a glove that gives you teleoperation and demonstration data in hours. It is not a complete robot, so every WUJI project is a multi-vendor project (or a glove-only sensing project).

## Snapshot

| Item | Detail |
|---|---|
| HQ | Shenzhen, Guangdong, China (COFCO Chuangxin R&D Center, Bao'an District); second office in Haidian, Beijing |
| Legal name | 深圳舞肌科技有限公司 (Shenzhen Wuji Technology Co., Ltd.) |
| Founded | **2019** (company statement: started with high-torque-density motors, then hands and data-capture devices) |
| Founders / CEO | not public on the official site. One third-party page says the company grew out of motor maker Pan Motor — ⚠️ unverified |
| Size and funding | not public (no funding round found in this research) |
| Core business | Dexterous hands (Wuji Hand, Wuji Hand 2), data glove (Wuji Glove), SDK / CLI, open-source sim, RL and VLA tooling |
| Website | https://www.wuji.tech (wuji.tech) · sales@wuji.tech · support@wuji.tech |
| Docs / developer portal | https://docs.wuji.tech (English + Chinese, about 167 English pages, has `llms.txt`) |
| GitHub | https://github.com/wuji-technology (24 public repos, mostly MIT / Apache-2.0, pushed as recently as 2026-11-10) |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified from official docs) | Price | Img key |
|---|---|---|---|---|---|
| **Wuji Hand** (gen 1) | 5-finger dexterous hand | ✅ shipping | **20 active DoF** (4 per finger), serial direct-drive joints, self-locking · **580 ± 10 g** · 201 × 75 × 50 mm · fingertip force **15 N** · whole-hand static grasp load **10 kg** · open/close ≈ 0.3 s · **1000 Hz × 20 axes**, position control · **USB 2.0** · 12–20 V DC · IP40 · idle grip life ≥ 300,000 cycles | Official price not public. Reseller listing "from US$5,500" — ⚠️ unverified | wuji-hand |
| **Wuji Hand 2** (2.1 / 2.2 Beta) | 5-finger dexterous hand, 2nd gen | 🧪 beta hardware in the field (docs call 2.2 a "non-tactile prototype", specs not final) | **20 active DoF**, **back-drivable** direct-drive joints, thumb opposition · **650 g** bare (800 g with pads and cables) · 180 × 80 × 40 mm · **MIT force-position hybrid control** (default) + position mode (Beta) · **1000 Hz × 20 axes** · **RJ45 Ethernet 100BASE-TX** + XT30 power · 11–13 V DC, 12 V 20 A adapter · on-board IMU stream · firmware v2.5.1 | Official price not public. Third-party listings US$14,600–19,500 — ⚠️ unverified | wuji-hand-2 |
| **Wuji Glove** | Tactile + pose data glove | ✅ shipping | **526 tactile points** (24 × 31 matrix, full palmar side) at **120 FPS**, 0–20 N, 0.1 N resolution, 4 mm pitch · **5 EMF 6-DoF fingertip trackers** at 120 Hz, ≤ 2 mm RMS, ≤ 10 ms latency · 6-axis IMU at 800 Hz · glove **67.5 g** · USB-C power, RJ45 data via adapter · −5 to 40 °C | not public | wuji-glove |
| **Wuji SDK + Wuji CLI** | Software (Python / C SDK, command-line tool) | ✅ available, free | One SDK for Hand, Hand 2 and Glove · `pip install wuji-sdk` (CPython 3.8–3.14) · Linux x86_64 / arm64, macOS Apple silicon, Windows · MCAP recording · built-in retargeting · C packages incl. Android aarch64 | free (MIT repo) | wuji-sdk |

Not found: any WUJI arm, wrist or humanoid product. Hand 2 tactile version is implied by the "non-tactile prototype" wording but no date is published (🔭).

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organisers or WUJI):**

- **Wuji Hand 2 (2.2 Beta) and/or Wuji Hand gen 1**, left and right, on a desk stand or with wrist flange adapters. Reasoning: these are the only two hardware hand lines; the docs, firmware and ROS 2 packages were all updated in Oct–Nov 2026, so Hand 2 is the product they want developers on.
- **Wuji Glove pairs** for live teleoperation. Reasoning: the official "cross-product teleoperation" quick start is glove to hand, and it is the fastest demo to get working.
- **No arm of their own.** Expect to mount the hand on another vendor's arm or humanoid (Flexiv, ROKAE, Dobot, Unitree, AGIBOT and others on site). Ask WUJI staff on day 1 which flange adapters they brought; the Hand 2 docs include wrist flange drawings.
- Quantity is unknown; hands are costly and fragile (IP40), so plan for **shared or supervised access**.

## Developer platform (summary)

- **Wuji SDK** (unified, Python + C): auto-discovery on the local network, multi-device connect, callback and async subscriptions, device parameters. Docs: https://docs.wuji.tech · repo: https://github.com/wuji-technology/wuji-sdk
- **Control level:** joint-level only. Hand 2 = MIT mode (position, velocity, feed-forward effort, kp / kd per joint) or position mode (Beta); Hand gen 1 = position control. **No built-in grasp planner or high-level skills** — you write those.
- **Platforms:** Linux x86_64 / arm64, macOS (Apple silicon), Windows 10 / 11; Docker deployment guide; Hand 2 and Glove connect over Ethernet (RJ45), Hand gen 1 over USB.
- **ROS 2:** `wuji-ros2` (drivers for Hand 2 and Glove, messages, bringup; distributed via the ROS build farm). Official install targets **Ubuntu 26.04 + ROS 2 Lyrical** — check your laptop / use Docker. Older `wujihandros2` (Hand gen 1, 1000 Hz joint states, RViz) is archived but usable; repo lists Humble and Kilted.
- **Simulation assets:** `wuji-description` with **URDF, MJCF, MJX and USD** for both hand generations; load in MuJoCo and Isaac Sim without hardware. Rigid-body only (no soft-pad deformation).
- **Teleoperation and retargeting:** retargeting is built into the SDK (21 MediaPipe-format keypoints in, 20 joint angles out) — so a webcam + MediaPipe, Vision Pro, VR headset or the Wuji Glove can all drive the hand. `wuji-hand-teleop` adds ROS 2 hand + arm teleop (HTC Vive Tracker and PICO 4 paths; not actively maintained).
- **Data collection:** SDK records multi-channel streams to **MCAP** with episode switching and quality monitoring; glove gives tactile + pose + IMU.
- **Learning stacks (open source):** `wuji-mjlab` (PPO in-hand cube reorientation with sim-to-real bridge, ONNX export), `wuji-isaaclab` (same task for Hand 2), `toporetarget` (human hand-object motion to Wuji Hand, arXiv 2606.16272), `wuji-openpi` (fork of Physical Intelligence openpi for fine-tuning and ROS 2 deployment of **pi0 / pi0.5** on dual-arm + Wuji Hand setups).
- **Pretrained models / on-board compute:** no WUJI foundation model or published checkpoints found (not public). No on-board application compute; the hand is driven from your PC or a Jetson-class host (WUJI benchmarks glove calibration on Jetson AGX Orin).
- **Practical limits:** hand is **IP40** (indoor, dry, no dust); glove EMF tracking degrades near metal (keep at least 3 cm clearance); Hand 2 is beta hardware with non-final parameters.

## Current projects, deployments and customers

Public information on customers and field deployments is **thin**; nothing found for Europe or Switzerland.

- **2026-11-10** — Docs release: SDK and CLI on Windows and Apple silicon, Hand 2 position mode (Beta), glove calibration solver 15× faster. [Release notes](https://docs.wuji.tech/docs/en/release-notes.md)
- **2026-10** — `wuji-ros2` and `wuji-description` released through the ROS build farm; `wuji-isaaclab` and `wuji-mjlab` updated. [GitHub org](https://github.com/wuji-technology)
- **2026-06** — TopoRetarget paper and code (retargeting human hand-object motion to the Wuji Hand, used for pen-spin RL). [Repo](https://github.com/wuji-technology/toporetarget)
- **2026-06** — `wuji-openpi`: pi0 / pi0.5 fine-tuning and deployment on dual-arm + Wuji Hand rigs (teleop repo references Tianji arms). [Repo](https://github.com/wuji-technology/wuji-openpi)
- **2026-06-05** — Trade press reports WUJI teasing Wuji Hand 2 with a claimed 20% transmission-efficiency gain; no price or ship date disclosed at the time. [RuntimeWire](https://runtimewire.com/article/wuji-tech-hand-2-robotic-hand-teaser)
- Named customers, shipment volumes and commercial deployments in any of the four tracks: **not public**. Positioning in the docs is research, robot integration and human-machine interaction.

## Roadmap and future direction

- 🧪 **Wuji Hand 2 to final product:** docs label 2.2 as a non-tactile beta prototype, which implies a tactile / final version later; no date or spec published (🔭).
- ✅ **Software consolidation (2026):** one Wuji SDK + CLI replaces the older per-product tools (wujihandpy, Wuji Studio, HMI, Upgrader are archived); Hand gen 1 is now also supported by the unified SDK.
- ✅ **Data-loop strategy:** glove → retargeting → hand → MCAP recording → RL / VLA fine-tuning. The company's stated mission is human-level dexterous manipulation for humanoids.
- Funding, valuation, production volumes, overseas offices: **not public**.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 2 | End effector only: adds fine manipulation (buttons, handles, parcels) to another vendor's mobile robot; indoor IP40 limits street use | Wuji Hand 2, Wuji Hand | [T01 brief](T01-Autonomous-Urban-Services/WUJI-T01-1-Brief.md) |
| T02 Resilient & Safe City | 3 | Glove-driven teleoperated dexterous handling (valves, switches, tools) keeps the human out of the hazard; needs a partner arm | Wuji Glove + Wuji Hand 2 | [T02 brief](T02-Resilient-and-Safe-City/WUJI-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Possible sorting / disassembly manipulation, but a 20-DoF hand is overkill versus a gripper for most waste tasks | Wuji Hand, Wuji Glove | [T03 brief](T03-Sustainable-City/WUJI-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | Glove alone measures grip pressure (526 points) and finger pose for hand-rehab assessment; hand + arm enables assistive fetch / feeding demos. Not a medical device | Wuji Glove, Wuji Hand 2 | [T04 brief](T04-Elderly-Care-and-Rehabilitation/WUJI-T04-1-Brief.md) |

## Related docs
- [Product portfolio](WUJI-Products.md) · [Developer guide](WUJI-Developer-Guide.md) · [Roadmap and strategy](WUJI-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources

- [Wuji Technology official site](https://www.wuji.tech) (company description, addresses, product pages [Hand](https://www.wuji.tech/en/hand), [Hand 2](https://www.wuji.tech/en/hand2), [Glove](https://www.wuji.tech/en/glove))
- [Wuji Docs — English index](https://docs.wuji.tech/_llms/en.txt)
- [Wuji Hand 2 (2.2 Beta) product introduction](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md)
- [Wuji Hand 2 version identification and compatibility](https://docs.wuji.tech/docs/en/wuji-hand/latest/version-compatibility.md)
- [Wuji Hand 2 ROS 2 integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/ros2-integration.md)
- [Wuji Hand (gen 1) product introduction](https://docs.wuji.tech/docs/en/wuji-hand/v1/overview.md)
- [Wuji Glove product introduction](https://docs.wuji.tech/docs/en/wuji-glove/latest/introduction.md)
- [Wuji SDK overview](https://docs.wuji.tech/docs/en/wuji-sdk/latest/introduction.md) · [installation](https://docs.wuji.tech/docs/en/wuji-sdk/latest/quick-start.md) · [hand retargeting](https://docs.wuji.tech/docs/en/wuji-sdk/latest/retargeting.md)
- [Wuji Docs release notes](https://docs.wuji.tech/docs/en/release-notes.md)
- [GitHub: wuji-technology](https://github.com/wuji-technology) ([wuji-sdk](https://github.com/wuji-technology/wuji-sdk), [wuji-ros2](https://github.com/wuji-technology/wuji-ros2), [wuji-description](https://github.com/wuji-technology/wuji-description), [wuji-mjlab](https://github.com/wuji-technology/wuji-mjlab), [wuji-openpi](https://github.com/wuji-technology/wuji-openpi), [toporetarget](https://github.com/wuji-technology/toporetarget), [wuji-hand-teleop](https://github.com/wuji-technology/wuji-hand-teleop))
- [RuntimeWire: Wuji Tech teases Wuji Hand 2 (2026-06-05)](https://runtimewire.com/article/wuji-tech-hand-2-robotic-hand-teaser)
- Third-party price listings (unverified, not official): [roboticscenter.ai Wuji Hand](https://www.roboticscenter.ai/store/product/wuji-hand) · [humanoid.guide Wuji Hand 2](https://humanoid.guide/welcome-wuji-hand-2/)
- [LinkedIn: Wuji Tech](https://www.linkedin.com/company/wuji-tech/) (identity reference given in the task; not fetched)
