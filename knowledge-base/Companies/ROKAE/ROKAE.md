---
type: company
company: "ROKAE Robotics"
slug: ROKAE
hq: "Beijing, China (listed entity registered in Shandong Province)"
founded: 2014
website: https://www.rokae.com/en/
categories: [arm, mobile-manipulator, humanoid, components, software]
on_site_guess: "xMate force-controlled cobot arms (SR / CR class) with xCore SDK; possibly an AR 7-DoF humanoid arm or a Helios wheeled dual-arm robot"
fit_t01: 3
fit_t02: 2
fit_t03: 3
fit_t04: 4
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# ROKAE Robotics

> **One-liner:** Chinese robot maker (HKEX: 3752) selling industrial arms, force-controlled "flexible" collaborative arms and, since 2025–26, embodied-AI hardware: 7-DoF humanoid arms, force-controlled joints, a wheeled dual-arm robot and a bipedal humanoid.
> **Why it matters at Leukerbad:** ROKAE's core skill is joint-torque force control — the capability you need for anything that touches a person or an unknown surface (massage, physiotherapy, guided ultrasound, compliant handling). It is the most natural arm vendor for a contact-rich T04 build, and a solid manipulation component for T01/T03.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Beijing, China (press datelines, "ROKAE (Beijing) Robotics Co., LTD" on the website). Listed entity: **Rokae (Shandong) Robotics Group Inc.**; manufacturing base in Shandong Province |
| Founded | **2014** per the company's Oct 2026 press release (2015 appears in some older third-party profiles) |
| Founders / CEO | **Tuo Hua**, Founder and CEO |
| Size and funding | Listed on the Hong Kong Main Board on **9 Jul 2026** (code **3752**), raising about **HKD 875M** at HKD 38/share. **1,000+ enterprise customers**, **40+ countries/regions**. Headcount: not public in the sources used. Company guided to a net loss for 2026 (investor commentary) |
| Core business | Industrial robots (NB / XB), flexible collaborative robots (xMate CR / SR / ZR), embodied intelligent robots (AR arms, HSA joints, Helios, Human.X, CMR mobile manipulators, welding robots) |
| Website | https://www.rokae.com/en/ |
| Docs / developer portal | https://docs.rokae.com/en/ (xCore manual, SDK, ROS 2 package manual, plugin development, downloads) |
| GitHub | No official org confirmed in this research. SDK and ROS 2 packages are distributed via the docs portal downloads. ⚠️ unverified: a `RokaeRobot` GitHub account hosting xCoreSDK repos |

## Portfolio at a glance

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| xMate SR series (SR3, SR5) | Compact 6-axis force-controlled cobot | ✅ | **3 / 5 kg** payload · **705 / 919 mm** reach · ~13.8 / 16.5 kg · ±0.03 mm · 48 VDC · IP54 · Cartesian stiffness adjustable 0–3000 N/m · 1.2 kg MSC controller | not public | rokae-xmate-sr |
| xMate CR series (CR5, CR7, CR12, CR18, CR20, CR35) | 6-axis (some 5-axis) cobot | ✅ | **5–45 kg** payload · **988–2246 mm** reach · joint torque sensing for collision detection · IP67 (site-wide claim) · cabinet-less option | not public | rokae-xmate-cr |
| xMate ZR series (ZR6) | 6-axis cobot | ✅ | **6 kg** · **980 mm** · other specs not checked | not public | rokae-xmate-zr |
| xMate ER Pro (ER3 Pro / ER7 Pro) | 7-DoF cobot with joint torque sensors | ⚠️ unverified status (legacy line; not on the current English cobot page, still in Japanese case studies) | ER7 Pro: **7 kg** · **850 mm** · **7 DoF** | not public | rokae-xmate-er-pro |
| AR series (AR3, AR5, AR10) | 7-DoF humanoid force-controlled arm | ✅ (10,000th unit delivered, Sep–Oct 2026) | **3 / 5 / 10 kg** payload · **650 / 683 / 815 mm** reach · **8 / 10 / 19.5 kg** arm weight · joint torque sensors standard · force resolution ≤0.05 N · EtherCAT 1 ms cycle · 48 VDC · IP54 | not public | rokae-ar |
| HSA series (HSA-11 … HSA-32) | Integrated force-controlled joint module | ✅ | Peak torque **11–459 Nm** · weight **0.45–6.0 kg** · torque sensor resolution ≤0.05 Nm · 1 kHz force loop · EtherCAT · 48 V | not public | rokae-hsa |
| Helios (Helios II) | Wheeled dual-arm humanoid | ✅ (deployed at Schaeffler) | **23 DoF** in spec table (intro text says 42) · **5 kg per arm** · omni chassis **1.5 m/s** · height 1493–2000 mm · **160 kg** · ~4 h runtime · 2× 3D LiDAR + head stereo camera · Orin NX / AGX Orin / Thor options · ROS 2 + Python SDK | not public | rokae-helios |
| Human.X | Full-size bipedal humanoid | 🧪 (launched mid-2026; availability not stated) | **1.7 m** · ~**75 kg** · 7-DoF arms, **3 kg per arm** · walking ≥0.5 m/s · 6-DoF hands (12 joints, 540 g) | not public | rokae-human-x |
| CMR series (CMR-S, CMR-L, CMR-CR) | Mobile manipulator (AMR + cobot) | ✅ | Arm payload **7–45 kg** by model · max **1.3–1.5 m/s** · laser SLAM, 2 LiDARs · docking ±5 to ±10 mm · 7–12 h operation · chassis 150–1500 kg | not public | rokae-cmr |
| Intelligent Welding Robot series | Cobot welding package | ✅ | Specs not checked | not public | rokae-welding |
| NB / XB series (NB4, XB7, NB12, NB12h, NB25, NB25h, NB80, NB220) | 6-axis industrial robots | ✅ | **4–220 kg** payload · **475–3201 mm** reach | not public | rokae-nb-xb |
| xCore / iNex | Control system (xCore) and embodied-AI control system (iNex) | ✅ xCore · 🧪 iNex (named in press release, no public technical detail found) | xCore manual V3.2; compact MAC controller (213 × 145.5 × 45 mm) drives 7, 14 or 20+ joints | bundled | rokae-xcore |

## What they will most likely bring to the hackathon

**Best guess, not confirmed — check the vendor table on site.**

- **Most likely: xMate SR3 / SR5 or a small CR (CR7 / CR12).** These are the 48 V, light, cabinet-light cobots ROKAE shows at trade fairs and uses for commercial demos (massage, coffee, picking). They ship by air easily and work with the public SDK.
- **Plausible: AR-series 7-DoF arm(s), single or dual.** This is ROKAE's 2026 headline product (10,000 delivered) and it has its own SDK branch (0.7.x-AR). A dual-AR bench rig would fit an "embodied AI" hackathon.
- **Possible but heavier logistics: Helios wheeled dual-arm robot** (160 kg). If one is on site it is the only ROKAE platform that covers mobility plus manipulation out of the box.
- **Unlikely:** Human.X biped (new, availability unclear), NB/XB industrial arms, large CMR units (500–1500 kg chassis).
- **Bring-your-own parts to plan for:** gripper or tool, camera, and a Linux PC for the SDK — none of these are confirmed as supplied.

## Developer platform (summary)

- **SDK ("xCore SDK"):** documented for **C++, Python and C#** on docs.rokae.com; versions listed are **0.7.x, 0.7.x-AR (humanoid arm) and 0.8.x**. Includes quick start, error codes, FAQ and a table mapping SDK calls to pendant (HMI) functions.
- **Real-time mode:** the C++ docs contain real-time-mode troubleshooting, i.e. a low-level streaming interface exists for C++. Exact rate and available modes (joint position / Cartesian impedance / torque) were not confirmed here — ⚠️ unverified: 1 kHz real-time control with impedance and direct torque modes. Hardware side: AR joints run a 1 ms EtherCAT cycle and HSA joints quote a 1 kHz force loop.
- **High-level control:** non-real-time motion commands via SDK; pendant with drag teaching and graphical flow programming; **RokaeStudio** offline programming.
- **ROS 2:** an official "Rokae xMate ROS 2 User Manual" and package exist on the docs portal. Supported distros, MoveIt and ros2_control details not confirmed. Helios lists **ROS 2 + Python SDK** for secondary development.
- **Plugins:** a plugin-development section exists for extending the controller/HMI.
- **Simulation assets:** URDFs are expected with the ROS 2 package; official MuJoCo / Isaac assets — not public / not found.
- **Teleoperation / data collection:** a remote-ultrasound case uses ER7 Pro under teleoperation; Helios lists only gamepad control. No public data-collection toolkit or dataset found.
- **Pretrained models:** none public. Human.X marketing mentions a VLA "intelligent core" and the press release names the iNex embodied-AI control system, without downloadable models. Plan to bring your own policy (for example LeRobot / OpenVLA-style) or pair with another vendor's VLA.
- **On-board compute:** cobots use the xCore controller (no GPU) — add an external PC. Helios offers Jetson Orin NX 8 GB, AGX Orin 64 GB or Thor T5000.
- **Links:** [docs hub](https://docs.rokae.com/en/) · [SDK docs](https://docs.rokae.com/en/docs/SDK) · [ROS 2 manual](https://docs.rokae.com/en/docs/ROS2) · [download center](https://www.rokae.com/en/service/190/Download-Center.html). Some spec sheets require a MyROKAE login.

## Current projects, deployments and customers

- **Oct 2026** — 10,000th AR humanoid force-controlled arm delivered; **80+ industrial partners** have integrated the arms; **1,000+ enterprise customers** overall ([TechNode Global / PR Newswire](https://technode.global/?p=996114)).
- **Oct 2026** — **Schaeffler** Taicang lighthouse factory runs **five Helios** wheeled humanoids with AR arms for parts handling, assembly and inspection on a humanoid-component line ([same release](https://technode.global/?p=996114)).
- **Jul 2026** — Hong Kong IPO; prospectus cites customers in **40+ countries and regions**, top-six position among Chinese cobot providers and top-five in embodied robotic arms (CIC data quoted by [Deloitte China](https://www.deloitte.com/cn/en/about/press-room/deloitte-china-assists-listing-of-rokae-robotics-on-sehk.html)).
- **Q1 2026** — 5,100+ robots shipped in the quarter and confirmed orders of RMB 577.3M at 31 Mar 2026, per secondary IPO analysis (⚠️ unverified against the prospectus).
- **Healthcare / wellness (undated case studies on rokae.com):** AI massage robot on SR arms; [moxibustion therapy robot](https://www.rokae.com/jp/case/show/1196/%E3%81%8A%E7%81%B8%E6%B2%BB%E7%99%82%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88.html) (xMate + vision); [teleoperated ultrasound diagnosis](https://www.rokae.com/jp/case/show/1189/%E9%81%A0%E9%9A%94%E6%93%8D%E4%BD%9C%E5%9E%8B%E8%B6%85%E9%9F%B3%E6%B3%A2%E8%A8%BA%E6%96%AD%E3%83%BB%E6%B2%BB%E7%99%82%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88.html) with xMate ER7 Pro. These are integrator applications, not certified ROKAE medical devices.
- **Commercial services (SR product page):** robotic coffee and ice cream, fruit picking, chemical catalyst preparation.
- **Europe:** sold through distributors (for example ZTEC in Denmark lists xMate cobots). No Swiss deployment or subsidiary found — not public.

## Roadmap and future direction

- **Jul 2026** — IPO proceeds (~HKD 875M) raised; detailed use of proceeds not confirmed in the sources used.
- **Mid-2026** — "Embodied Intelligent Robot" line established as a third business pillar: AR arms, HSA joints, Helios, Human.X, CMR, welding. Human.X bipedal humanoid reported launched around **Jul 2026** (single secondary source plus official product page) 🧪.
- **Oct–Nov 2026** — Messaging centres on being a force-control component and arm supplier to other humanoid makers (10,000 arms, 80+ partners) rather than only a full-robot brand.
- **Nov 2026** — Company news mentions a "Northeast Intelligent Manufacturing Alliance" launch (headline only; details not checked).
- **iNex embodied-AI control system** 🧪 and VLA-based "intelligent core" 🔭 — named, no public developer access found.
- Profitability: net loss expected for 2026 per investor commentary — treat long-term support promises accordingly.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | Good manipulation half of a service robot (kiosk, handover, maintenance tasks); mobility only if Helios or CMR is on site, otherwise pair with another vendor's base | xMate SR / CR, Helios, CMR-S | [T01 brief](T01-Autonomous-Urban-Services/ROKAE-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | Arms are indoor, fixed-base tools; useful for remote manipulation or inspection contact tasks, not for terrain or hazard response | xMate CR (IP67 claim), AR arm on another vendor's mobile base | [T02 brief](T02-Resilient-and-Safe-City/ROKAE-T02-1-Brief.md) |
| T03 Sustainable City | 3 | Standard cobot path to waste sorting, disassembly, picking or lab automation with a camera; nothing sustainability-specific from ROKAE | xMate SR5 / CR7 / CR12, CMR | [T03 brief](T03-Sustainable-City/ROKAE-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 4 | Force control with adjustable stiffness and existing massage, moxibustion and tele-ultrasound applications give a clear 48-hour path to a safe contact demo | xMate SR3 / SR5, AR5, ER7 Pro (if available) | [T04 brief](T04-Elderly-Care-and-Rehabilitation/ROKAE-T04-1-Brief.md) |

## Related docs
- [Product portfolio](ROKAE-Products.md) · [Developer guide](ROKAE-Developer-Guide.md) · [Roadmap and strategy](ROKAE-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [ROKAE official site (EN) — lineup, navigation, news](https://www.rokae.com/en/)
- [ROKAE — Collaborative Robots overview](https://www.rokae.com/en/product/182/Collaborative-Robots.html)
- [ROKAE — SR cobots](https://www.rokae.com/en/product/show/349/SR-Cobots.html)
- [ROKAE — Humanoid Force-Controlled Arm AR](https://www.rokae.com/en/product/show/595/Humanoid-Force-Controlled-Arm-AR.html)
- [ROKAE — Wheeled Dual-Arm Robot Helios](https://www.rokae.com/en/product/show/596/Wheeled-Dual-Arm-Robot-Helios.html)
- [ROKAE — Humanoid Robot Human.X](https://www.rokae.com/en/product/show/597/Humanoid-Robot-Human.X.html)
- [ROKAE — Integrated Force-Controlled Joint HSA](https://www.rokae.com/en/product/show/598/Integrated-Force-Controlled-Joint-HSA.html)
- [ROKAE — Mobile Manipulator CMR](https://www.rokae.com/en/product/show/599/Mobile-Manipulator-CMR.html)
- [ROKAE documentation hub](https://docs.rokae.com/en/)
- [ROKAE SDK documentation](https://docs.rokae.com/en/docs/SDK)
- [ROKAE ROS 2 package manual](https://docs.rokae.com/en/docs/ROS2)
- [TechNode Global (PR Newswire) — ROKAE delivers its 10,000th humanoid force-controlled arm, 27 Oct 2026](https://technode.global/?p=996114)
- [Deloitte China — listing of Rokae Robotics on SEHK, Jul 2026](https://www.deloitte.com/cn/en/about/press-room/deloitte-china-assists-listing-of-rokae-robotics-on-sehk.html)
- [Origin of Bots — ROKAE launches Human.X](https://www.originofbots.com/news/rokae-launches-humanx-bipedal-humanoid-robot-for-industrial-applications)
- [Minichart — Rokae IPO analysis (orders, Q1 2026 shipments)](https://www.minichart.com.sg/2026/07/05/rokae-shandong-robotics-group-inc-ipo-analysis-financial-outlook-broker-coverage-and-listing-prospects/)
- [iTiger / Deep News — key investor concerns for Rokae IPO](https://www.itiger.com/news/1197773788)
- [ROKAE Japan — moxibustion therapy robot case](https://www.rokae.com/jp/case/show/1196/%E3%81%8A%E7%81%B8%E6%B2%BB%E7%99%82%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88.html)
- [ROKAE Japan — teleoperated ultrasound robot case (ER7 Pro)](https://www.rokae.com/jp/case/show/1189/%E9%81%A0%E9%9A%94%E6%93%8D%E4%BD%9C%E5%9E%8B%E8%B6%85%E9%9F%B3%E6%B3%A2%E8%A8%BA%E6%96%AD%E3%83%BB%E6%B2%BB%E7%99%82%E3%83%AD%E3%83%9C%E3%83%83%E3%83%88.html)
- [ZTEC (Denmark) — ROKAE cobot reseller listing](https://www.ztec.dk/en/cobots)
