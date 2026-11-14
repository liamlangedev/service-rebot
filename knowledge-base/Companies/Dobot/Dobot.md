---
type: company
company: "Dobot Robotics"
slug: Dobot
hq: "Shenzhen, China"
founded: 2015
website: https://www.dobot-robots.com
categories: [arm, humanoid, quadruped, software, data]
on_site_guess: "Desktop and light cobot arms (Magician E6, Nova 2/5, CR3A/CR5A), possibly an X-Trainer dual-arm teleop rig or an Atom humanoid"
fit_t01: 3
fit_t02: 2
fit_t03: 3
fit_t04: 4
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Dobot Robotics

> **One-liner:** Shenzhen-based, Hong Kong-listed cobot maker (100,000+ robots shipped) that is expanding from 6-axis collaborative arms into humanoids, consumer legged robots and its own embodied foundation model.
> **Why it matters at Leukerbad:** The most "just works" arm option on site: one TCP/IP API with actively maintained Python and ROS 2 repos across desktop arms and cobots, and a cobot (Nova 5) that Dobot itself positions for physiotherapy — a direct hook into T04.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Shenzhen, Guangdong, China |
| Founded | **2015** |
| Founders / CEO | Liu Peichao (founder, chairman) ⚠️ unverified in this research pass |
| Legal entity / listing | Shenzhen Dobot Corp Ltd (formerly Shenzhen Yuejiang Technology), **HKEX: 2432** |
| Size and funding | Public company. FY2025 revenue **RMB 492M** (+31.7%), net loss RMB 84M. H1 2026 revenue **RMB 316.3M** (+106.6%); embodied-AI robots **RMB 45.2M** (14.3% of revenue). **100,000+** robots shipped cumulatively (company figure). Headcount: not public in sources used |
| Core business | Collaborative arms (3–30 kg), desktop / education arms, humanoid (Atom), teleop data rigs (X-Trainer), consumer robots under the INFFNI sub-brand |
| Website | https://www.dobot-robots.com |
| Docs / developer portal | Download center: https://www.dobot-robots.com/service/download-center (manuals, TCP/IP interface guides, Atom SDK guide) |
| GitHub | https://github.com/Dobot-Arm (44 public repos, several pushed in Nov 2026) |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified on official pages unless marked) | Price | Img key |
|---|---|---|---|---|---|
| CRA series (CR3A, CR5A, CR7A, CR6AL, CR10A, CR12A, CR16A, CR16AL, CR20A, CR30A) | 6-axis cobot | ✅ | Payload **3–30 kg**; reach **620–1,800 mm**; repeatability ±0.02 to ±0.05 mm; CR3A 16.5 kg, CR5A 25 kg; PLd Cat.3 safety controller, 20+ safety functions; Modbus TCP/RTU, EtherNet/IP, PROFINET; optional SafeSkin pre-collision sensing. Variants: **CRAF** (torque sensor), **CRA-IP68** | not public | dobot-cra |
| CR 30H | Heavy-payload cobot | ✅ | **30 kg** payload; 300°/s joint speed | not public | dobot-cr30h |
| CRH series | High-performance cobot | 🧪 (unveiled Oct 2026) | **7 kg / 12 kg** payload; torque sensors on **all joints**; J6 450°/s; TCP up to 7 m/s; TÜV-certified, 30+ safety functions; aimed at welding, spraying, inspection | not public | dobot-crh |
| CRS series (CR3AS, CR5AS, CR10AS) | 6-axis cobot | ✅ | Listed on site; specs not checked ⚠️ unverified | not public | dobot-crs |
| PULSA (PULSA 7, PULSA 12) | High-speed industrial / collaborative arm | 🧪 (unveiled Oct 2026) | **7 kg / 12 kg** payload; repeatability ±0.02 / ±0.03 mm; J6 up to 790°/s; PLd Cat.3; switchable high-speed and collaborative modes | not public | dobot-pulsa |
| Nova series (Nova 2, Nova 5) | Compact commercial cobot | ✅ | Nova 2: **2 kg**, 625 mm, **11 kg**. Nova 5: **5 kg**, 850 mm, **14 kg**. ±0.05 mm; IP54; palm-size controller (1.3 kg) on **30–60 V DC**; collision stop in 0.01 s; positioned for retail (Nova 2) and **physiotherapy** (Nova 5) | not public | dobot-nova |
| MG400 | 4-axis desktop arm | ✅ | Desktop industrial arm; detailed specs not checked ⚠️ unverified | not public | dobot-mg400 |
| M1 Pro | 4-axis SCARA-type arm | ✅ | Listed on site; specs not checked ⚠️ unverified | not public | dobot-m1-pro |
| Magician E6 | 6-axis desktop education / research arm | ✅ | **750 g** payload; **450 mm** reach; ±0.1 mm; **≤7.2 kg**; 2 Ethernet ports (TCP/IP, Modbus TCP); 16 DI / 16 DO at base; same V4 API as CRA | not public | dobot-magician-e6 |
| Magician / Magician Lite / Magician Go | 4-axis education arms and kits | ✅ | Classroom arms with vision, sensor, AI and rail kits; specs not checked ⚠️ unverified | not public | dobot-magician |
| E6 ROS Mobile Platform | Mobile base + Magician E6 (education) | ✅ | Listed on site; specs not checked ⚠️ unverified | not public | dobot-e6-ros-platform |
| X-Trainer | Dual-arm teleoperation / data-collection rig | ✅ | 2 x Nova 2 followers; **2 kg** per arm (3 kg dual); 625 mm reach per arm; **25 Hz** end-to-end interface; leader handles under 400 g; SDK covers collect, train, infer | not public | dobot-x-trainer |
| Atom (Atom, Atom Max, Atom D / Trainer) | Full-size humanoid | ✅ (mass production since Jun 2025) | Atom: **28 upper-body DoF**, binocular RGB, straight-knee gait. Atom Max: **41 DoF**, 6-DoF hands, RealSense D455, **1500 TOPS** AI module, VR/MR teleop. Atom D: dual 7-DoF arms + 2-DoF head for data collection. Height / weight not on official page (resellers: 1.53 m, 62 kg ⚠️ unverified) | CNY **199,000** (about US$27,500) at 2025 launch; reseller prices much higher | dobot-atom |
| LUMO | Compact embodied-AI robot (companion, research, commercial) | 🧪 (shown IFA Sep 2026, launched Oct 2026) | Runs DobotWAM; voice + vision emotion / intent recognition; local long-term memory. Dobot calls it both "all-terrain robot" and "compact humanoid"; no spec sheet public | about US$12,000 on a third-party listing ⚠️ unverified | dobot-lumo |
| Rover X1 (INFFNI sub-brand; Flex variant) | Wheel-legged consumer quadruped | ✅ | Hybrid wheel-leg mobility, carries small loads, follow / patrol; SDK reported by resellers ⚠️ unverified; no official spec page found | CNY **7,499** (about US$1,030) at China launch; about EUR 2,600+ at EU resellers | dobot-rover-x1 |
| Kongyi DobotWAM | Embodied foundation model (world action model) | 🧪 (announced Jun 2026, closed weights per secondary sources) | Company-reported **99.25%** on LIBERO suites ⚠️ unverified independently | not public | dobot-wam |
| DobotStudio Pro / DobotStudio Sim / DobotLab | Programming, simulation and education software | ✅ | Blockly + Lua scripting; drag-to-teach; mobile app for Nova | not public | dobot-studio |

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organisers or Dobot):**

- **Most likely: Magician E6 and/or Nova 2 / Nova 5, plus a small CRA (CR3A / CR5A).** These are light (7–25 kg), run from a wall socket or DC supply, and all speak the same V4 TCP/IP API that Dobot's GitHub actively maintains for "CRA/E6/Nova". Dobot's Frankfurt conference (Oct 2026) had an education forum with TUM and Fraunhofer — and TUM-XR co-organises this event — so the EDU kit is the natural thing to ship.
- **Plausible: X-Trainer.** It is Dobot's standard offering for imitation-learning research and suits a 48-hour "collect demos, train a policy" workflow.
- **Possible: Atom humanoid or Rover X1 / LUMO as showpieces.** Dobot toured these at CES and IFA 2026. Expect limited hands-on access compared with the arms; Atom has a public SDK, ROS 2 package and URDF, LUMO has no public developer material.
- **Unlikely: CR20A / CR 30H / PULSA** (heavy, need rigid mounting and industrial power).

Ask the Dobot booth first: which models, how many, which end-effectors (gripper, suction, camera), and whether controller firmware is V4.

## Developer platform (summary)

- **One protocol for all arms:** TCP/IP remote-control interface (dashboard commands + motion commands + real-time feedback port). V4 covers **CRA, Magician E6 and Nova**; V3 covers older CR / Nova firmware; a separate 4-axis variant covers MG400 / M1 Pro. Check firmware generation before picking a repo.
- **Languages (official demos):** Python (`TCP-IP-Python-V4`, pushed 2026-11-13), C++ (`TCP-IP-CR-CPP-V4`), C#, Java, MATLAB, LabVIEW, Android.
- **ROS 2:** `DOBOT_6Axis_ROS2_V4` (CRA / E6 / Nova, pushed 2026-11-06); ROS 1 via `TCP-IP-ROS-6AXis`. Exact ROS distros, MoveIt and Gazebo coverage: check the repo README ⚠️ unverified here.
- **Control level:** High-level joint / Cartesian moves, I/O, drag-teach and trajectory replay are the well-trodden path. Torque-level control is not a documented general feature; force sensing needs CRAF (torque sensor) or CRH (all-joint torque sensors).
- **No-code path:** DobotStudio Pro (Blockly, Lua), teach-by-demonstration, CRStudio mobile app for Nova — useful for a fast first demo.
- **Simulation:** DobotStudio Sim (vendor simulator); Atom URDF in `dobot_atom_urdf`. Arm URDFs ship inside the ROS packages ⚠️ unverified.
- **Teleoperation / data collection:** `dobot_xtrainer` (teleop + data collection for X-Trainer) and `Embodylink` (data collection, annotation, training management, teleop toolkit). Supported policy types (ACT, diffusion, LeRobot format) are not stated on the official page ⚠️ unverified.
- **Humanoid:** `dobot_atom_sdk`, `dobot_atom_ros2`, plus an official "Atom series SDK application development guide" (v2.1, Aug 2026). Atom Max offers VR/MR teleop (full-body or segmented).
- **Pretrained models:** ROM-1 (100M-parameter operator model on Atom) and Kongyi DobotWAM are proprietary; no public weights found. `voice_txt_command` is a small open demo for voice-to-object-segmentation.
- **Industrial I/O:** Modbus TCP/RTU, EtherNet/IP, PROFINET on CRA; 24 V digital I/O on all controllers; ecosystem grippers and cameras (OnRobot, SCHUNK, Schmalz, SICK, Mech-Mind) via the Dobot+ plugin system.

## Current projects, deployments and customers

- **2026-10-20** — Robotics Ecosystem Conference in Frankfurt: launched LUMO, PULSA and CRH; 18 live demos; ecosystem partners named: Siemens, SCHUNK, Mech-Mind, SICK, Piab, SEER, OnRobot, Schmalz; German customers Unsinn and Unista presented palletizing and welding deployments ([Dobot news](https://www.dobot-robots.com/insights/news/dobot-unveils-three-new-products-at-its-2026-robotics-ecosystem-conference.html)).
- **2026-09-04 to 09-08** — IFA Berlin: Rover X1, Rover-based character robots and LUMO shown under the INFFNI consumer sub-brand ([Dobot news](https://www.dobot-robots.com/insights/news/dobot-brings-the-future-of-robotics-to-ifa-berlin-2026.html)).
- **2026-08-24** — H1 2026 results: revenue RMB 316.3M (+106.6%), embodied-AI robots RMB 45.2M ([HKEX filing](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0824/2026082400904.pdf), [Gasgoo](https://autonews.gasgoo.com/articles/news/dobot-embodied-intelligence-shipment-value-exceeded-40-million-yuan-in-first-half-2074845611093184513)).
- **2026-07-23** — Partnership with RiACT on easier-to-deploy automation (details not reviewed) ([Dobot news index](https://www.dobot-robots.com/insights/news/dobot-unveils-three-new-products-at-its-2026-robotics-ecosystem-conference.html)).
- **2026-06** — Kongyi DobotWAM embodied model announced ([Gasgoo](https://autonews.gasgoo.com/articles/news/dobot-unveils-dobotwam-embodied-large-model-2061817635740909569)).
- **2026-01-06 to 01-09** — CES 2026: INFFNI debut with Rover X1; Atom demonstrated ([Dobot news](https://www.dobot-robots.com/insights/news/inffni-a-sub-brand-of-dobot-robotics-makes-its-mark-at-ces-2026.html)).
- **2025-06** — Atom entered mass production; first units delivered at a launch event in Nagoya ([Dobot news](https://www.dobot-robots.com/insights/news/dobot-debuted-global-delivery-of-humanoid-robot.html)).
- **Standing claims (company):** deployed in 15 industries and 200+ application scenarios; 100+ Fortune Global 500 customers.
- **Track-relevant deployments:** Dobot positions **Nova 5 for physiotherapy** and Nova 2 for retail / beverage service on its product page. Named clinics, care homes or city-service customers: none found in this pass — treat massage / moxibustion and coffee-kiosk references as integrator applications, not documented Dobot projects ⚠️ unverified.
- **Switzerland:** no Swiss office, distributor or deployment confirmed in this pass.

## Roadmap and future direction

- **Strategy (FY2025 report, Mar 2026):** move from "cobot leader" to a multimodal embodied-AI platform; 2025 described as the first year of mass production and commercialisation of embodied robots.
- **Guidance:** management reportedly targets about **50% revenue growth in 2026**; losses expected to continue because of R&D (R&D was 32.1% of H1 2026 revenue) ([Yicai](https://www.yicaiglobal.com/news/humanoid-robot-sales-surge-but-rd-costs-keep-chinas-dobot-ubtech-loss-making)).
- **Models:** DobotWAM is the stated brain for LUMO and future embodied products; no public release plan for weights 🔭.
- **Hardware pipeline:** CRH and PULSA (Oct 2026) push into force-sensitive and high-speed work; availability dates not public 🧪.
- **Consumer:** INFFNI sub-brand (2026) for home robots; Rover X1 platform extended with character variants.
- **Geography:** H1 2026 materials state accelerated expansion in Europe, Asia-Pacific and the Americas; Germany highlighted as a growth market and chosen for the 2026 ecosystem conference.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | Arms are strong for kiosk / retail / handover cells; mobility needs another vendor's base (or the consumer-grade Rover X1) | Nova 2, CR3A / CR5A, Magician E6, Rover X1 | [T01 brief](T01-Autonomous-Urban-Services/Dobot-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | Fixed-base arms play a supporting role (tool handling, valve / switch manipulation on a partner's mobile base); IP68 CRA exists but is unlikely on site | CRA-IP68, CR5A, Rover X1 | [T02 brief](T02-Resilient-and-Safe-City/Dobot-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Vision-guided sorting / pick-and-place for waste and recycling is a clear 48-hour demo with a desktop arm and camera | Magician E6, MG400, CR5A, X-Trainer | [T03 brief](T03-Sustainable-City/Dobot-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 4 | Nova 5 is marketed for physiotherapy; light, safe, drag-teachable arms suit assisted exercise, feeding or fetch demos; teleop rig enables quick imitation learning | Nova 5, Nova 2, CRAF, X-Trainer, Atom | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Dobot-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Dobot-Products.md) · [Developer guide](Dobot-Developer-Guide.md) · [Roadmap and strategy](Dobot-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Dobot official site (product navigation)](https://www.dobot-robots.com)
- [CRA series](https://www.dobot-robots.com/products/cra-series/dobot-cra-series.html)
- [Nova series](https://www.dobot-robots.com/products/nova-series/dobot-nova-series.html)
- [Magician E6](https://www.dobot-robots.com/products/education/magician-e6.html)
- [Atom humanoid](https://www.dobot-robots.com/products/humanoid-robots/atom.html)
- [X-Trainer](https://www.dobot-robots.com/products/humanoid-robots/x-trainer.html)
- [LUMO overview page](https://www.dobot-robots.com/insights/case-studies/1283.html)
- [Dobot: three new products at the 2026 Robotics Ecosystem Conference](https://www.dobot-robots.com/insights/news/dobot-unveils-three-new-products-at-its-2026-robotics-ecosystem-conference.html)
- [Dobot at IFA Berlin 2026](https://www.dobot-robots.com/insights/news/dobot-brings-the-future-of-robotics-to-ifa-berlin-2026.html)
- [INFFNI at CES 2026](https://www.dobot-robots.com/insights/news/inffni-a-sub-brand-of-dobot-robotics-makes-its-mark-at-ces-2026.html)
- [Dobot: global delivery of Atom](https://www.dobot-robots.com/insights/news/dobot-debuted-global-delivery-of-humanoid-robot.html)
- [Dobot-Arm on GitHub](https://github.com/Dobot-Arm)
- [TCP-IP-Python-V4](https://github.com/Dobot-Arm/TCP-IP-Python-V4)
- [DOBOT_6Axis_ROS2_V4](https://github.com/Dobot-Arm/DOBOT_6Axis_ROS2_V4)
- [Atom SDK application development guide v2.1 (PDF)](https://a.storyblok.com/f/298593/x/ad7c499105/dobot-atom-series-humanoid-robot-sdk-application-development-guide_v2-1_20260826_en.pdf)
- [HKEX interim results announcement, 2026-08-24](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0824/2026082400904.pdf)
- [Gasgoo: embodied-intelligence shipments H1 2026](https://autonews.gasgoo.com/articles/news/dobot-embodied-intelligence-shipment-value-exceeded-40-million-yuan-in-first-half-2074845611093184513)
- [Gasgoo: DobotWAM embodied model](https://autonews.gasgoo.com/articles/news/dobot-unveils-dobotwam-embodied-large-model-2061817635740909569)
- [Yicai Global: R&D costs keep Dobot loss-making](https://www.yicaiglobal.com/news/humanoid-robot-sales-surge-but-rd-costs-keep-chinas-dobot-ubtech-loss-making)
- [SCMP: Dobot's US$27,500 humanoid](https://www.scmp.com/tech/tech-trends/article/3302868/chinese-robotics-firm-shenzhen-dobot-excites-investors-us27500-humanoid)
- [The Robot Report: Dobot enters the humanoid race with Atom](https://www.therobotreport.com/dobot-enters-the-humanoid-robot-race-with-atom/)
- [TechNode: Rover X1 debut](https://technode.com/2025/11/04/dobot-rover-x1-robot-dog-debuts-at-1030-carries-items-and-follows-for-filming/)
- [Gizmochina: Rover X1 launch, specs and price](https://www.gizmochina.com/2025/11/04/dobot-rover-x1-smart-home-robot-dog-launched-specs-price/)
