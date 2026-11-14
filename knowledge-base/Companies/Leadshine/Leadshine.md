---
type: company
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
hq: "Shenzhen, China"
founded: 1997
website: https://www.leadshine.com
categories: [components, dexterous-hand]
on_site_guess: "DH116 / DH116S / DH2116 dexterous hands plus PJ3 / HJ2 joint modules as demo and loan parts; no complete robot"
fit_t01: 3
fit_t02: 2
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Leadshine Technology Co., Ltd.

> **One-liner:** Shenzhen-listed motion-control maker (steppers, servos, PLCs) that since 2025 also sells humanoid-robot building blocks: frameless motors, integrated joint actuators and five-finger dexterous hands.
> **Why it matters at Leukerbad:** Leadshine does not bring a robot — it brings the **parts you bolt onto someone else's robot**. The dexterous hands (ROS 2 + C++/Python SDK, URDF/MJCF) are the only items a team can realistically program within 48 hours; the joint modules matter only if you build custom mechanics.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Shenzhen, Guangdong, China |
| Founded | 1997 (company states "over 27 years" of experience) |
| Founders / CEO | Founder and chairman Li Weiping ("Dr. Li" in the CES 2026 release) ⚠️ unverified full name/title in this research pass |
| Size and funding | Public: Shenzhen Stock Exchange **002979**. H1 2026 revenue **CNY 1.247 bn (+39.9% YoY)**, net profit **CNY 194 m (+62.8%)**. Site states ~1,500 employees, 500 patents, 10,000 clients (figure may be dated) |
| Core business | Stepper / closed-loop stepper / servo drives and motors, integrated motors, motion-control PLCs, remote I/O, HMIs; robot components (frameless motors, joint actuators, dexterous hands, wheel modules) |
| Website | [leadshine.com](https://www.leadshine.com) · robot components: [leadshine.com/robot](https://www.leadshine.com/robot/index.html) · web store: [store.leadshine.com](https://store.leadshine.com/collections/all) |
| Docs / developer portal | No dedicated developer portal. [Downloads](https://www.leadshine.com/downloads.html) (manuals, datasheets, 3D models, [software](https://www.leadshine.com/download/Software.html)); hand manuals and ROS 2 notes are PDFs on the store |
| GitHub | No official GitHub org found. SDK ("LHandProLib"), ROS 2 package and URDF/MJCF are distributed as download archives linked from the user manuals |

## Portfolio at a glance

Robot-component lines first (most relevant here), then the industrial automation lines.

| Product | Type | Status | Key specs | Price (if public) | Img key |
|---|---|---|---|---|---|
| DH116 series (incl. DH116EC EtherCAT, -M tactile variants; DH116P enhanced variant shown at CES 2026) | Five-finger dexterous hand | ✅ | **11 DoF**, 6 actively driven; **545 g** (±10 g); whole-hand load up to **30 kg**, single finger **5 kg**; lateral grip > 50 N; brushless coreless servo + worm gear; EtherCAT / CAN FD / RS485; rated 1 million grasp cycles; optional tactile sensors (6 standard on -M) | Store: **USD 2,199** (no sensors), **USD 2,799** (tactile -M) sale prices | leadshine-dh116 |
| DH116S series | Compact "ultra-thin" five-finger hand | ✅ (launched WAIC, Jul 2026) | **11 DoF**, **6 active**; 147.54 × 73.53 × 26.35 mm; **< 380 g** (store figure); light-load handling 10 kg; EtherCAT / CAN FD / RS485; sized for 1.1–1.4 m robots; optional tactile on fingers and palm | not public (store lists it; price not captured) | leadshine-dh116s |
| DH2116 series | High-DoF dexterous hand (flagship) | ✅ | **21 DoF: 16 active + 5 passive**; brushless coreless motors + precision screw drive; max whole-hand grip **94 N**; CAN 1 Mbps, CAN FD 1/5 Mbps, RS485 5 Mbps; SDK for Windows / Linux / ROS 2, C++ and Python | not public (store lists it; price not captured) | leadshine-dh2116 |
| PJ3 series | Planetary integrated joint actuator (motor + gearbox + encoder + drive) | ✅ | Models by outer diameter: **PJ3-60** (9.5 N·m rated), **PJ3-75** (14 N·m rated), **PJ3-97** (44 N·m rated); CAN FD or EtherCAT versions; monitoring port (e.g. temperature); targets robot dogs, small/mid humanoids, exoskeletons | Store sale prices: **USD 329** (60 CAN), **USD 399** (75 CAN), **USD 429** (75 EtherCAT), **USD 479** (97 CAN) | leadshine-pj3 |
| HJ2 series | Harmonic integrated joint actuator | ✅ | Sizes **52 / 70 / 80 / 90 / 110 mm**; built-in **24-bit** encoder; EtherCAT and CAN FD; uses FM2 frameless motor; torque values not on product page | not public | leadshine-hj2 |
| FM2 series (FM family) | Frameless torque motor | ✅ | Five standard sizes **43 / 50 / 60 / 70 / 85 mm** on the product page (Automate 2026 release says six sizes, 50–127 mm — sources disagree); 10% higher torque density and 20% lower loss vs previous generation (vendor claim); one FM model cited at 7 N·m peak / 326 g | not public | leadshine-fm2 |
| iW series | Wheel module / low-voltage integrated wheel drive for AGV/AMR | 🧪 shown at WAIC and Automate 2026; no product page found | not public | not public | leadshine-iw |
| Coreless motors + micro servo drives, hollow encoders | Hand / small-joint actuation components | ✅ (per investor disclosures; no English product page) | not public | not public | leadshine-coreless |
| EL7 / EL8 / EL8S AC servo drives + ELM motors | High-voltage AC servo systems | ✅ | EtherCAT (CoE, CiA 402), Modbus RTU / RS485, pulse and analog variants; STO on EL8-EC and UL-listed models; e.g. EL7-EC 750 W–2 kW models | via distributors | leadshine-el8 |
| ELD3 / ELD3 MINI / 2ELD2 low-voltage servo drives | DC servo drives (single and dual axis) | ✅ | Low-voltage, compact; 2ELD2 dual-axis with STO; fieldbus variants (EtherCAT, CANopen, Modbus RTU exist across the low-voltage range) | via distributors | leadshine-eld3 |
| DM5 / EM3E / CS3E / 2CS3EIP / 2EM3EIP stepper and closed-loop stepper drives | Stepper drives | ✅ | Pulse/direction plus EtherCAT (EM3E, CS3E) and EtherNet/IP (dual-axis 2CS3EIP, 2EM3EIP) | via distributors | leadshine-stepper-drives |
| Integrated motors (ISS1 and integrated servo / closed-loop stepper) | Motor + drive + encoder in one unit | ✅ | Standard mounting dimensions; fieldbus options | via distributors | leadshine-integrated-motors |
| SCnU / Sn / MC / LC motion-control PLCs, remote I/O, HMIs | Controllers | ✅ | SCnU: up to 12 pulse axes + 32 EtherCAT axes; MC: up to 64 bus axes; LC: up to 256 synchronized axes | via distributors | leadshine-plc |

## What they will most likely bring to the hackathon

**Best guess — not confirmed by Leadshine or the organizers.**

- **Most likely: dexterous hands** (DH116, DH116S, DH2116). These are what Leadshine demonstrated live at CES, FAIR plus, WAIC and Automate in 2026, they are sold as single units in the web store, and they are the only Leadshine products with a ready SDK, ROS 2 package and URDF.
- **Likely as display or loan parts: PJ3 planetary and HJ2 harmonic joint modules and FM2 frameless motors.** Useful only to teams building their own mechanism (gripper, pan-tilt, small arm, exoskeleton joint).
- **Unlikely: industrial servo / stepper / PLC kits.** They need mains wiring, tuning software and a fieldbus master — poor fit for a 48-hour event.
- **No complete robot.** Leadshine does not make humanoids, arms or quadrupeds. Expect its hands to be mounted on another vendor's arm or humanoid (Leadshine reports AGIBOT as a customer — AGIBOT gave it a supplier award).
- Practical check on arrival: which hand variant (CAN FD / RS485 / EtherCAT), left or right, with or without tactile sensors, and what mechanical flange and power supply come with it.

## Developer platform (summary)

- **Hands — SDK:** "LHandProLib" SDK with demos, described by Leadshine as open-source; **C++ and Python**; Windows and Linux; x86 and ARM.
- **Hands — ROS 2:** official example project for DH116S ("LHandPro") with packages for a state publisher, interfaces, a service node and C++ / Python sequence demos; RViz2 mirrors the physical hand. Third-party reseller docs state ROS 2 Humble on Ubuntu 22.04 ⚠️ unverified against the official PDF.
- **Simulation assets:** **URDF and MJCF** files for the hands are linked from the user manuals. No Isaac / Gazebo scenes found.
- **Low-level buses:** hands speak CAN FD, RS485 and (DH116EC, DH116S) EtherCAT; the CAN FD protocol document is hosted on Feishu, linked from the manual. Control is FOC current loop with hybrid force-position control inside the hand.
- **GUI tool:** a visual "upper-computer" debugging tool (Windows) for jogging fingers and checking sensors — fastest way to verify hardware before coding.
- **Version trap:** the DH116 manual marks downloads dated before **2026-02-10** as "old version"; make sure SDK, firmware and URDF come from the same generation.
- **Joint modules (PJ3 / HJ2):** CAN FD or EtherCAT. No public SDK, ROS 2 driver or protocol document was found in this pass — plan on needing Leadshine staff on site for the protocol.
- **Industrial drives:** EtherCAT drives follow **CiA 402 over CoE**, so any generic EtherCAT master (for example IgH or SOEM-based ROS 2 stacks) can in principle drive them; Modbus RTU and CANopen variants exist. Tuning is done with Leadshine's Windows software from the [download centre](https://www.leadshine.com/download/Software.html).
- **Not offered:** no foundation model, no datasets, no teleoperation / data-collection stack, no on-board compute, no official GitHub org.

## Current projects, deployments and customers

- **2026-01 (CES, Las Vegas, 6–9 Jan):** showed coreless and frameless motors, joint modules and DH116 / DH116P hands; reported booth visits from Tesla Optimus, Boston Dynamics, Amazon and Neura executives and first-day hand pre-orders from North America, Europe and Asia. Visits are not supply contracts. ([PR Newswire Asia](https://en.prnasia.com/releases/global/leadshine-achieves-great-success-at-ces-2026-entering-us-and-european-robotics-supply-chain-518892.shtml))
- **2026-04/05 (FAIR plus, Shenzhen):** claims its components are in the supply chains of **80% of China's leading humanoid makers**; **> 120,000 frameless motors** delivered in 2025; AGIBOT named it an outstanding supplier partner. All company claims. ([Leadshine store blog](https://store.leadshine.com/blogs/news/leadshine-dexterous-hands-and-joint-modules-shine-at-the-shenzhen-fair-plus-2026))
- **2026-06 (Automate, Chicago, 22–25 Jun):** full industrial range plus DH116 / DH2116, HJ2 / PJ3 and FM2; low-voltage integrated wheel solution for AGV/AMR. ([Leadshine news](https://www.leadshine.com/newsEvent/details/automate-2026-concludes-successfully-%7C-leadshine-drives-global-industrial-automation-and-humanoid-robotics-innovation-with-core-motion-control-technologies.html))
- **2026-07 (WAIC, Shanghai, 17–20 Jul):** launched **DH116S**; showed iW wheel modules; cites a supplier award from AGIBOT, a partner award from "Xinghai Tu" (Galaxea), and collaboration with Fourier and Tiangong. ([Leadshine news](https://en.leadshine.com/newsEvent/details/leadshine-successfully-concludes-waic-2026,-showcasing-next-generation-robotics-solutions.html))
- **2026-08 (H1 report, via Chinese financial press):** joint modules and high-DoF hands in volume supply with orders from **nearly 100 robot customers**; frameless-motor orders in hand **> 1 million units**. ([Sina Finance](https://cj.sina.com.cn/articles/view/2311077472/89c03e6002002ndni))
- **Track-relevant deployments:** none found. Leadshine is a component supplier; no public elderly-care, rescue, municipal or sustainability deployments under its own name. CES 2026 talks with exoskeleton, e-bike and medical-equipment prospects were reported but no deals named.
- **Europe / Switzerland:** no specific office, distributor or project announcement found beyond CE / RoHS / REACH compliance and European pre-orders claimed at CES.

## Roadmap and future direction

- **Strategy (2026):** move from motion-control supplier to "platform" supplier of robot core components, focused on two categories — joint modules and dexterous hands; planetary modules prioritised for volume. ([10jqka investor note, 2026-07](https://stock.10jqka.com.cn/20260723/c678395454.shtml))
- **Capacity:** frameless-motor design capacity to reach the million-unit level in 2026; automated capacity under construction quoted as 2 million units/year (May 2026) and **3 million units/year** (H1 2026 report).
- **Hand line-up evolution:** DH series launched March 2025 (11 DoF, trial sales from Q2 2025) → DH2116 21-DoF flagship → DH116S compact hand (July 2026). No next model publicly announced.
- **Overseas:** stated intent to deepen localisation in North America (Automate 2026); "entering US and European robotics supply chain" is a headline claim without named contracts.
- **Finance:** H1 2026 revenue +39.9% YoY; brokerage forecast (not company guidance) of about CNY 2.8 bn revenue for 2026. No external funding round — listed company.
- **Not public:** dated product roadmap, prices for HJ2 / FM2, any software or AI-model plans.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | A dexterous hand upgrades another vendor's arm or mobile manipulator for handling doors, parcels, tools; Leadshine supplies no mobility or autonomy | DH116 / DH116S, DH2116, iW wheel module (if on site) | [T01 brief](T01-Autonomous-Urban-Services/Leadshine-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | Supporting role: robust high-load hand (30 kg whole-hand) for valve / switch / debris manipulation on a host robot | DH116, PJ3 | [T02 brief](T02-Resilient-and-Safe-City/Leadshine-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Supporting role: grasping for waste sorting or efficient actuation in a custom mechanism; no domain product | DH116, PJ3, FM2 | [T03 brief](T03-Sustainable-City/Leadshine-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | Human-like hand with tactile option suits assistive fetch / hand-over and hand-rehab mirroring demos; PJ3 is marketed for exoskeletons but has no public SDK | DH2116, DH116S, DH116-M (tactile), PJ3 | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Leadshine-T04-1-Brief.md) |

**Decision hint:** choose Leadshine as an *add-on*, not as your platform. Pair a hand with an arm or humanoid from another vendor (and, for T04, with EMG capture or AR teleoperation from other vendors on site). Budget half a day for mechanical mounting, power and bus bring-up.

## Related docs
- [Product portfolio](Leadshine-Products.md) · [Developer guide](Leadshine-Developer-Guide.md) · [Roadmap and strategy](Leadshine-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Sources
- [Leadshine official site (home, product categories, company figures)](https://www.leadshine.com)
- [Leadshine robot components overview](https://www.leadshine.com/robot/index.html)
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html)
- [DH116S series product page](https://en.leadshine.com/robots/dextrous-hands/dh116s-series.html)
- [DH2116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [PJ3 series product page](https://www.leadshine.com/robots/integrated-actuators/PJ3-Series.html)
- [HJ2 series product page](https://www.leadshine.com/robots/integrated-actuators/hj2-series.html)
- [FM2 series product page](https://www.leadshine.com/robots/frameless-motors/fm2-series.html)
- [Leadshine web store — all products](https://store.leadshine.com/collections/all)
- [Store: DH116-R1 dexterous hand (price)](https://store.leadshine.com/products/dh116-r1-dexterous-hand)
- [Store: PJ3 planetary integrated actuators (prices)](https://store.leadshine.com/collections/pj3-planetary-integrated-actuators)
- [DH116 / DH116P user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116_DH116P_Series_Dexterous_User_Manual.pdf)
- [DH116S LHandPro ROS2 example project description (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [DH116S user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf)
- [DH2116 user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH2116_Series_Dexterous_Hand_User_Manual.pdf)
- [Leadshine at CES 2026 — supply-chain release (PR Newswire Asia)](https://en.prnasia.com/releases/global/leadshine-achieves-great-success-at-ces-2026-entering-us-and-european-robotics-supply-chain-518892.shtml)
- [Leadshine dexterous hands and frameless motors at CES 2026 (PR Newswire Asia)](https://en.prnasia.com/releases/global/leadshine-s-dexterous-hands-and-frameless-motors-shine-at-ces-2026-519017.shtml)
- [FAIR plus 2026 recap (Leadshine store blog)](https://store.leadshine.com/blogs/news/leadshine-dexterous-hands-and-joint-modules-shine-at-the-shenzhen-fair-plus-2026)
- [Automate 2026 recap (Leadshine news)](https://www.leadshine.com/newsEvent/details/automate-2026-concludes-successfully-%7C-leadshine-drives-global-industrial-automation-and-humanoid-robotics-innovation-with-core-motion-control-technologies.html)
- [WAIC 2026 recap (Leadshine news)](https://en.leadshine.com/newsEvent/details/leadshine-successfully-concludes-waic-2026,-showcasing-next-generation-robotics-solutions.html)
- [H1 2026 results coverage (Sina Finance)](https://cj.sina.com.cn/articles/view/2311077472/89c03e6002002ndni)
- [Investor research note, July 2026 (10jqka)](https://stock.10jqka.com.cn/20260723/c678395454.shtml)
- [DH series launch, March 2025 (Futu news)](https://news.futunn.com/en/post/54351384/china-leadshine-technology-002979-released-the-dh-series-dexterous-hand)
- [EL7-EC2000Z product page (EtherCAT servo drive)](https://www.leadshine.com/product-detail/EL7-EC2000Z.html)
