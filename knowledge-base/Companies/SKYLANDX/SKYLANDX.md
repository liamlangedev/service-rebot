---
type: company
company: "SKYLANDX"
slug: SKYLANDX
hq: "Shenzhen, China"
founded: 2020
website: https://skylandx.com/
categories: [sensors, software, data]
on_site_guess: "MetaCam Air 2 handheld LiDAR + vision scanners with MetaCam Go / Studio / Cloud; possibly a C01 SLAM LiDAR or a robot-mount (MetaCam Hub) kit"
fit_t01: 3
fit_t02: 4
fit_t03: 3
fit_t04: 2
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# SKYLANDX

> **One-liner:** Shenzhen-based reality-capture company (HKUST / DJI SLAM lineage) that makes MetaCam handheld LiDAR + camera + RTK 3D scanners, a small SLAM LiDAR (C01) and the software to turn scans into point clouds, meshes and 3D Gaussian splats — also usable as a perception payload on robots.
> **Why it matters at Leukerbad:** It is not a robot; it is the fastest way to get a **centimetre-level 3D map / digital twin** of a room, clinic corridor, street or slope that every other team's robot can localize in, simulate in or inspect against. Strongest for mapping, inspection and GPS-denied localization (T02), a supporting part elsewhere.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Shenzhen, China (legal entity: Shenzhen Skyland Innovation Technology Co., Ltd.; street address not stated on the site — ⚠️ city inferred from the legal name) |
| Founded | Building its technology "since 2020" (about page); first integrated handheld scanner shipped **2023** |
| Founders / CEO | CEO not public on the pages checked. CTO: Stuart Situ (quoted in Oct 2026 press). Core team from the HKUST–DJI Joint Innovation Lab; team members led VINS-Mono, VINS-Fusion and A-LOAM SLAM research |
| Size and funding | Headcount not public. Funding amounts not public ("top-tier investors"; first team incubated under Prof. Li Zexiang's HKCRC initiative). **5,000+ units shipped**, **1 billion+ m²** captured (company claim, Oct 2026) |
| Core business | Handheld / robot-mounted 3D laser scanners (MetaCam), SLAM LiDAR module (C01), spatial-perception kits for drones and ground robots, capture / processing / cloud software |
| Website | https://skylandx.com/ |
| Docs / developer portal | No public developer portal found. API and ROS details are "contact SKYLANDX" |
| GitHub | No official GitHub org found (not public) |

## Portfolio at a glance

| Product | Type | Status | Key specs (verified unless marked) | Price | Img key |
|---|---|---|---|---|---|
| MetaCam Air 2 | Handheld LiDAR + panoramic vision + RTK scanner; robot-mountable | ✅ | **619 g** handheld · **< 1 cm** relative accuracy · point-cloud thickness < 1 cm · built-in RTK · TimeSync 3.0 microsecond hardware sync · real-time colorized point cloud preview · exports JPG / LAS / RCP / PLY | Not public officially; about USD 5,000 at one reseller ⚠️ unverified | skylandx-metacam-air-2 |
| MetaCam Air 3 | Next-gen handheld survey-grade scanner with in-house LiDAR | 🧪 (unveiled INTERGEO, Oct 2026; availability and configs not announced) | LiDAR FOV **360° × 240°** · 2 × **50 MP** panoramic cameras + 1 × 48 MP forward camera + global-shutter VSLAM camera · RTK (NTRIP or UHF radio) and PPK · removable RTK module · range, weight, accuracy not public | Not public | skylandx-metacam-air-3 |
| MetaCam Lite | Entry-level compact handheld SLAM scanner (interiors) | ✅ (announced with Japan distribution, May 2026) | Dual **48 MP** cameras, 360° panoramas · TimeSync 3.0 · exports LAS / PCD / PLY / RCP / E57 · outputs point cloud, 3DGS, OBJ mesh · weight, range, RTK not stated on product page | Not public | skylandx-metacam-lite |
| MetaCam Pro | Survey-grade scanner; handheld, backpack, vehicle, robot / quadruped, drone | ✅ | **128-channel** LiDAR · up to **5.24 M pts/s** · up to **200 m** range · **1.16 kg** · **5 mm** relative / **3 cm** absolute accuracy · RTK / PPK / GCP · 48 MP main + dual 48 MP panoramic + 1.3 MP VSLAM cameras · open API | Not public | skylandx-metacam-pro |
| C01 LiDAR | Compact 3D SLAM LiDAR module for AMRs, service robots, quadrupeds, humanoids | ✅ | FOV **360° × 65°** (-20° to +45°) · **216,000 pts/s** (dual-line) · range **40 m @ 10 %** / 70 m @ 80 % reflectivity (some resellers list 25 m / 50 m ⚠️ unverified) · 200 Hz 6-axis IMU · UDP output · 12–30 V DC, max 15 W | Not public | skylandx-c01-lidar |
| Spatial Perception Robots / Modular Perception Kit | Ready-to-deploy aerial and ground robots, plug-and-play sensing kits, custom integrations | ✅ (sold via sales; no model names or specs public) | Real-time SLAM + navigation APIs · raw images / LiDAR / IMU / RTK access · GPS-denied operation (tunnels, mines) · platforms: drone, wheeled UGV, quadruped, humanoid | Not public | skylandx-spatial-perception-robots |
| MetaCam Fly | Autonomous-flight drone scanning platform | 🔭 (listed in inquiry form; described as in development, May 2026) | Not public | Not public | skylandx-metacam-fly |
| MetaCam Hub | Accessory to mount a MetaCam on robot platforms | ✅ ⚠️ unverified details | Mechanical / interface specs not public | Not public | skylandx-metacam-hub |
| MetaCam Go | Mobile app (Android, iOS) | ✅ | One-tap scan · live colorized point cloud · coverage check · device status | Not public | skylandx-metacam-go |
| MetaCam Studio | Desktop processing software (PC) | ✅ | Point cloud optimization, editing, measurement · RTK / control-point calibration · alignment and coordinate conversion · native RCP export | Not public | skylandx-metacam-studio |
| Skyland Cloud (also written MetaCam Cloud) | Web cloud platform | ✅ | Cloud processing · **3DGS generation** · browser 3D viewer · sharing and collaborative review | Not public | skylandx-cloud |

## What they will most likely bring to the hackathon

**Best guess (not confirmed by the organizer or the company):**

- **MetaCam Air 2 units** — the volume product, light (619 g), one-button, with a "standard robot interface" and magnetic quick-mount; the natural loaner for teams.
- **MetaCam Go + Studio + Cloud access** — needed to get anything out of the scanner; cloud processing is how 3DGS scenes are produced.
- **Possibly** a MetaCam Air 3 demo unit (unveiled five weeks ago, good showcase), a C01 LiDAR and a MetaCam Hub for mounting on a quadruped or wheeled robot from another vendor.
- **Unlikely as loaners:** MetaCam Pro (survey-grade, costly) and complete "Spatial Perception Robots".
- **Plan on:** SKYLANDX staff pre-scanning venues or helping with processing. Ask them on arrival about API / Rosbridge access — none of it is documented publicly.

## Developer platform (summary)

- **No public SDK, docs portal or GitHub org found.** Treat the API as something you obtain from SKYLANDX staff on site.
- **Open APIs (per official robotics page):** real-time pose, map, structured spatial model, and raw sensor streams (images, LiDAR, IMU, RTK); MetaCam can also output navigation commands. Languages and protocol details not public.
- **ROS:** supported through a **WebSocket interface using the Rosbridge protocol** — streams point clouds, images, IMU and pose without a custom driver. Supported ROS versions and message types: not public ("contact SKYLANDX"). ⚠️ ROS 2 specifically is unverified.
- **C01 LiDAR:** UDP data output, built-in 200 Hz IMU, advertised as plug-and-play with mainstream open-source SLAM algorithms; no official ROS driver found.
- **Control level:** high-level only (localization, mapping, relocalization against an existing map, navigation outputs). It does not control another vendor's robot actuators — you bridge pose / map into that robot's stack.
- **Data export (the practical integration path):** point clouds **PLY, PCD, LAS, E57, RCP**; 3DGS as **PLY**; mesh as **OBJ**; 360° panoramas (JPG).
- **Simulation:** scans are positioned for robot simulation and digital twins (point cloud / mesh / 3DGS). Direct USD or Isaac Sim export is not mentioned — expect to convert OBJ / PLY yourself.
- **Pretrained models / datasets:** none public. "Get Sample Data" request form exists on product pages.
- **On-board compute:** SLAM runs on the device in real time (no prior map needed); heavy colorization and 3DGS run in Studio / Cloud.
- Links: [Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/) · [Spatial perception robots](https://skylandx.com/spatial-intelligence-robots/) · [Software platforms](https://skylandx.com/software-platforms/)

## Current projects, deployments and customers

No named customers are public. What is documented:

- **2026-10** — MetaCam Air 3 unveiled at INTERGEO 2026 (Munich); company states 5,000+ units shipped since 2023 and 1 billion+ m² captured. [3D Mag](https://www.3dmag.com/?p=14376)
- **2026-09** — Listed as a supplier on Unmanned Systems Technology with 3D mapping and navigation solutions for UAVs and autonomous systems. [UST](https://www.unmannedsystemstechnology.com/2026/09/3d-mapping-navigation-solutions-for-uavs-autonomous-systems/)
- **2026-05** — GEOSURF begins distributing SKYLANDX products in Japan (MetaCam Lite introduced; MetaCam Fly described as in development). [GEOSURF news](https://aeo.washinmura.jp/ai/%E3%82%B8%E3%82%AA%E3%82%B5%E3%83%BC%E3%83%95%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE/en/news/2026-05-25-geosurf-begins-domestic-distribution-of)
- **Ongoing (official use cases, no named clients):** GPS-denied tunnel and mine mapping, construction progress vs BIM, indoor safety patrol (cracks, leaks, hazards), bridges / dams / substations, stockpile measurement, forestry and terrain mapping, cultural heritage, 3D data for embodied-AI training. [Robots page](https://skylandx.com/spatial-intelligence-robots/) · [MetaCam Pro](https://skylandx.com/metacam-pro/)
- **Europe / Switzerland:** presence at INTERGEO Munich; no Swiss deployment or distributor found (not public).

## Roadmap and future direction

- **2026-10** — MetaCam Air 3 🧪: first handheld with SKYLANDX's own survey-oriented LiDAR; price, configurations and regional availability "to be announced".
- **2026** — MetaCam Fly 🔭: autonomous-flight drone scanning platform, in development; no date or specs.
- **Direction:** moving from handheld scanners toward in-house LiDAR (C01, Air 3) and "spatial intelligence" for robots — perception kits, navigation APIs, relocalization, 3DGS environments for Physical AI training and simulation.
- **Channel expansion:** distributors (Japan, May 2026) and trade listings (UST, DirectIndustry) in 2026.
- **Funding:** no 2026 round found (not public).

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | Gives delivery / maintenance robots a prior map, relocalization and GPS-denied pose, but needs another vendor's robot to act | MetaCam Air 2, C01 LiDAR, MetaCam Hub | [T01 brief](T01-Autonomous-Urban-Services/SKYLANDX-T01-1-Brief.md) |
| T02 Resilient & Safe City | 4 | Core use cases match: tunnel / slope / infrastructure mapping, crack and hazard patrol, change detection between scans, operation without GNSS | MetaCam Air 2, MetaCam Pro, Skyland Cloud | [T02 brief](T02-Resilient-and-Safe-City/SKYLANDX-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Scan-to-BIM for building retrofits, stockpile / volume measurement, forestry and terrain mapping; analysis layer must be built by the team | MetaCam Air 2, MetaCam Lite, MetaCam Studio | [T03 brief](T03-Sustainable-City/SKYLANDX-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 2 | Supporting role: digital twin of a clinic or apartment for assistive-robot navigation, simulation or fall-hazard audit | MetaCam Lite, MetaCam Air 2, Skyland Cloud | [T04 brief](T04-Elderly-Care-and-Rehabilitation/SKYLANDX-T04-1-Brief.md) |

## Related docs
- [Product portfolio](SKYLANDX-Products.md) · [Developer guide](SKYLANDX-Developer-Guide.md) · [Roadmap and strategy](SKYLANDX-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [SKYLANDX — official site (home)](https://skylandx.com/)
- [SKYLANDX — About](https://skylandx.com/about/)
- [SKYLANDX — MetaCam Air 2](https://skylandx.com/metacam-air-2/)
- [SKYLANDX — MetaCam Lite](https://skylandx.com/metacam-lite/)
- [SKYLANDX — MetaCam Pro](https://skylandx.com/metacam-pro/)
- [SKYLANDX — C01 LiDAR](https://skylandx.com/c01-slam-lidar/)
- [SKYLANDX — Spatial Perception Robots](https://skylandx.com/spatial-intelligence-robots/)
- [SKYLANDX — Robotics & Physical AI](https://skylandx.com/industry/robotics-simulation/)
- [SKYLANDX — Software platforms](https://skylandx.com/software-platforms/)
- [3D Mag — SKYLANDX launches MetaCam Air 3 (2026-10-07)](https://www.3dmag.com/?p=14376)
- [Unmanned Systems Technology — 3D mapping and navigation solutions for UAVs and autonomous systems (2026-09)](https://www.unmannedsystemstechnology.com/2026/09/3d-mapping-navigation-solutions-for-uavs-autonomous-systems/)
- [Unmanned Systems Technology — MetaCam Air 3 announcement (2026-10; search snippet only, page blocked)](https://www.unmannedsystemstechnology.com/2026/10/skylandx-introduces-metacam-air-3-for-survey-grade-reality-capture/)
- [GEOSURF — domestic distribution of SkylandX products (2026-05-25)](https://aeo.washinmura.jp/ai/%E3%82%B8%E3%82%AA%E3%82%B5%E3%83%BC%E3%83%95%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE/en/news/2026-05-25-geosurf-begins-domestic-distribution-of)
- [DirectIndustry — MetaCam Air 2 brochure (export formats; search snippet)](https://pdf.directindustry.com/pdf/skylandx/metacam-air-2-brochure-en/4623723-1148083.html)
- [DirectIndustry — C01 LiDAR brochure (specs; search snippet)](https://pdf.directindustry.com/pdf/skylandx/en-c01-lidar-brochure/4623723-1148080.html)
- [AIFITLAB — MetaCam Air 2 reseller listing (price; search snippet)](https://aifitlab.com/collections/skylandx-lidar/products/skylandx-metacam-air2-lidar-scanner)
