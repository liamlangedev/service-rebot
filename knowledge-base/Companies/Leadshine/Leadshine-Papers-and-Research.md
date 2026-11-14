---
type: papers
company: "Leadshine Technology Co., Ltd."
slug: Leadshine
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Leadshine Technology Co., Ltd. — Papers and Research

⬆ [Leadshine Technology Co., Ltd. profile](Leadshine.md) · [Solutions and projects](Leadshine-Solutions-and-Projects.md) · [Developer guide](Leadshine-Developer-Guide.md)

> **Bottom line for a hackathon team:** Leadshine (雷赛智能, Shenzhen Stock Exchange 002979) is an engineering and manufacturing company, not a research lab. There is **no 2022–2026 paper, dataset, model or benchmark from the company**, and **no paper was found that uses its DH116 / DH116S / DH2116 hands or PJ3 / HJ2 joint modules**. What exists: the founder's classic robot-control papers (1987–1991), an SDK / ROS 2 / URDF package for the hands, and many third-party lab papers that use Leadshine **stepper motors, drives and motion cards** as building blocks.

## Research footprint

- **Founder is a control theorist.** Li Weiping (李卫平, "Dr. Warren Li" on the English site) holds an MIT PhD in robotics and automation (1990) and co-wrote the textbook *Applied Nonlinear Control* with Jean-Jacques Slotine; he later taught at a US state university ("WSU") and at HKUST before founding Leadshine in 1997. This is the company's only visible academic lineage ("innovation gene originated from MIT" in its own words).
- **No current publication activity found.** No company-authored arXiv / ICRA / IROS / RSS / CoRL paper, no research or technology blog with papers, no citation blocks. The English blog holds product-selection explainers only (stepper vs. servo, integrated vs. separate drives).
- **R&D is in-house and product-driven.** The site states about **10% of revenue** goes to R&D each year and that most R&D engineers hold a master's degree or PhD (page is dated; headcount there "more than 100" — the group has **1,580 employees** per current listing data). A Shenzhen-government-approved engineering laboratory for motion control (2015) and a "Postdoctoral Innovation Practice Base" plaque are listed, without published output. Board-level academic tie: independent director Wang Hong is a professor at Harbin Institute of Technology (Shenzhen).
- **Hands come from a subsidiary.** The Chinese product page names 深圳市灵巧驱控技术有限公司 (Shenzhen Lingqiao Drive-Control Technology, a group company in which Li Weiping is manager and director) as developer of the DH116. No papers under that name were found either.
- **Open-source posture: weak.** No official GitHub organisation. Hand SDK, ROS 2 example and URDF / MJCF are called "open-source" on the product page but ship as download archives (Feishu wiki links in the manuals) with **no licence text found**.
- **How this doc was researched:** web search **was available** (2 extended searches, both used; neither returned a Leadshine-specific paper). Discovery then relied on direct fetches: arXiv listing search for "Leadshine" (0 hits — arXiv searches titles and abstracts only), GitHub repository listing, and Europe PMC open-access full-text search (37 hits for 2021–2026, the track-relevant ones opened and read). Chinese-language journals (CNKI) and IEEE Xplore full text were **not** searched, so Chinese-only papers by staff may exist.

## Company-authored and company-affiliated papers

**2022–2026: none found.** The only verifiable company-affiliated academic work is the founder's pre-company research at MIT. It is control theory, useful as background on adaptive / force control of manipulators, not as a build recipe.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [Applied Nonlinear Control](https://openlibrary.org/works/OL4465059W) (textbook) | J.-J. E. Slotine, Weiping Li (MIT) | Prentice Hall, 1991 | Standard graduate text on Lyapunov methods, sliding-mode and adaptive control, with robot-manipulator examples; co-authorship is stated in Li's official executive résumé | — | — |
| [Composite adaptive control of robot manipulators](https://doi.org/10.1016/0005-1098%2889%2990094-0) | J.-J. E. Slotine, Weiping Li (MIT) | Automatica 25(4), 1989 | Adaptive controller that uses both tracking error and prediction error to speed up parameter convergence | — | — |
| [Adaptive manipulator control: A case study](https://doi.org/10.1109/9.14411) | J.-J. E. Slotine, Weiping Li (MIT) | IEEE Transactions on Automatic Control 33(11), 1988 | Experimental validation of the adaptive controller on a real manipulator | — | — |
| [On the Adaptive Control of Robot Manipulators](https://doi.org/10.1177/027836498700600303) | J.-J. E. Slotine, Weiping Li (MIT) | International Journal of Robotics Research 6(3), 1987 | The "Slotine–Li" adaptive controller: globally convergent tracking without joint-acceleration measurement | — | — |

Notes
- Attribution of the three journal papers to Leadshine's founder is an inference from name, institution and period (MIT PhD completed 1990); the textbook co-authorship is explicit in his résumé. ⚠️ unverified by a source that names the papers directly.
- The same résumé lists a Chinese monograph, 《运动控制系统原理与应用》 (roughly "Principles and Applications of Motion Control Systems"), and "several academic papers". ⚠️ unverified — publisher, year and co-authors not confirmed.

## Datasets, models and benchmarks released

**No dataset, AI model, foundation model or benchmark has been released by Leadshine.** The only public developer artifacts are hardware-support software for the dexterous hands:

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| LHandProLib SDK + demos (DH116 / DH116S / DH2116) | C++ / Python SDK; Windows and Linux; x86 and ARM | Called "open-source" by Leadshine; no licence text found ⚠️ unverified | Download links inside the user manuals: [DH116S manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf), [DH2116 manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH2116_Series_Dexterous_Hand_User_Manual.pdf) | Position / force commands and sensor read-out from your own code |
| LHandPro ROS 2 example project (DH116S) | ROS 2 packages (state publisher, interfaces, service node, C++ / Python sequence demos, RViz2 mirror) | not stated | [ROS 2 example description (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf) | Fastest route to drive the hand from a ROS 2 stack |
| Hand URDF and MJCF models | Robot description files for RViz / MuJoCo | not stated | Linked from the user manuals above (Feishu wiki; links could not be opened from here) | Simulation, retargeting, motion planning before hardware access |
| CAN FD protocol document | Protocol specification | not stated | Linked from the user manuals (Feishu wiki) | Writing a driver for an MCU or a non-ROS controller |

Community software for Leadshine industrial drives (not from Leadshine, no papers attached):

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| openvmp/stepper_driver_em2rs | ROS 2 (Humble tag) ros2_control driver for EM2RS-series Modbus RTU stepper drives; author reports testing only on a compatible third-party drive | Apache-2.0 | [GitHub](https://github.com/openvmp/stepper_driver_em2rs) | Driving a Leadshine RS485 stepper drive from ROS 2 |
| marcoreps/linuxcnc_leadshine_EL8 | LinuxCNC + EtherCAT configuration for EL8 servo drives | not stated | [GitHub](https://github.com/marcoreps/linuxcnc_leadshine_EL8) | Worked example of EL8 EtherCAT set-up on Linux |

## Third-party papers using their hardware or software

None of these uses the dexterous hands or joint modules. They show the typical academic use of Leadshine: **low-cost stepper motors, stepper drives and PC motion cards inside custom rigs and robots**. All were opened in open-access full text and the Leadshine part quoted from the methods section.

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [A Spatiotemporally Coupled Carbon Flux Monitoring System for Salt Marsh Wetlands Based on Integrated Land–Air Collaborative Intelligence](https://doi.org/10.3390/s26102966) | Zha, Wang, Shi — Nanjing Normal University | Sensors, 2026 | Leadshine 42-frame stepper motor (with a third-party TB6600 driver, STM32 MCU) in an auto-lifting sensor mast, 0–1.5 m | Field system for long-term, low-intervention carbon-flux monitoring with cloud storage, multi-algorithm sensor fusion and a land–air architecture | T03 (T03.2, T03.7) |
| [Influence of acupuncture twisting parameters on analgesic effects mediated by mast cells in AA rat models](https://doi.org/10.1016/j.bj.2025.100876) | Yu, Wang, Qiao, Li, Liu, Huang, Yao — Shanghai Univ. of Medicine & Health Sciences / Fudan | Biomedical Journal, 2026 (DOI year 2025) | Leadshine 42CM08 stepper (0.8 N·m holding torque) as needle-twisting actuator | Robot-controlled twisting angle and frequency change the analgesic effect in an animal model; companion to the system paper below | T04 (T04.6) |
| [A robot arm-assisted acupuncture system with motion and force monitoring: establishment and validation](https://doi.org/10.3389/fbioe.2025.1563263) | Li, Yu, Qiao, Ren, Xu, Wang, Gu, Yao — Fudan University et al. | Frontiers in Bioengineering and Biotechnology, 2025 | Leadshine 35CM015 stepper mounted on the flange of a RealMan RM65 arm as a rotary end-effector, plus force monitoring | Arm + small rotary tool reproduces a therapist's needle manipulations; mean absolute motion error below 0.2 mm; similarity to manual technique quantified | T04 (T04.2, T04.6) |
| [FGA-Corn: an integrated system for precision pesticide application in center leaf areas using deep learning vision](https://doi.org/10.3389/fpls.2025.1571228) | Song, Li, Song, Li — Weifang University / Henan Agricultural University | Frontiers in Plant Science, 2025 | Leadshine HBS57 closed-loop stepper driver (STM32 relay layer) turning a dosing funnel | YOLOv8-based detection triggers targeted dosing instead of blanket spraying — a camera → decision → stepper actuation pipeline | T03 (T03.6) |
| [A radiation therapy platform to enable upright cone beam computed tomography and future upright treatment on existing photon therapy machines](https://doi.org/10.1002/mp.17523) | Korte et al. — Peter MacCallum Cancer Centre / University of Melbourne | Medical Physics, 2025 | Leadshine EM556S stepper driver (800 microsteps/rev) on a slewing drive rotating a patient chair, 0.006° per step | A stepper + slew drive safely rotates a seated patient with high angular accuracy; design process with clinicians and patients | T04 (T04.4) |
| [Soft multifunctional bistable fabric mechanism for electronics-free autonomous robots](https://doi.org/10.1126/sciadv.ads8734) | Yang, Feng, Sun, Wei, Zou, Zhu, Gu — Shanghai Jiao Tong University | Science Advances, 2025 | Leadshine HS2257 stepper in the torque–angle characterisation rig (test equipment only) | Fabric bistable actuator-valves for soft grippers and crawlers running on one constant-pressure air supply | — |
| [A Robotic Solution for Precision Smoothing and Roughening of Precast Concrete Surfaces: Design and Experimental Validation](https://doi.org/10.3390/s24113336) | Gang, Duan, Wang, Nan, Song — Xi'an University of Architecture and Technology | Sensors, 2024 | All five joints on Leadshine steppers: 86CM85-BZ (X, Y), 86CM45-BZ brake motor (Z) with M860D driver, geared 86 / 57 steppers (R1, R2) | Gantry robot with coverage path planning (B-splines, bio-inspired neural network, A* escape from dead zones) around embedded obstacles | T03 (T03.4), T01 (T01.2, T01.6) |
| [Development and Validation of a Novel In Vitro Joint Testing System for Reproduction of In Vivo Dynamic Muscle Force](https://doi.org/10.3390/bioengineering10091006) | Yang, Wang, Zheng, Cheng, Zou, Zhao, Tsai — Shanghai Jiao Tong University | Bioengineering, 2023 | Complete Leadshine chain: DMC3C00 PC motion-control card, ACC-XC00 connection board, DMA882S drive, 86CM120 stepper | Cable-loading rig reproduces time-varying knee-muscle forces (error −6.2% to +1.81%) for implant testing and rehabilitation guidance | T04 (T04.3) |
| [Fully 3D printed flexible, conformal and multi-directional tactile sensor with integrated biomimetic and auxetic structure](https://doi.org/10.1038/s44172-023-00131-x) | Wei, Li, Domingos, Qian, Zhu, Yan, Ren, Wei — University of Manchester / Oxford / Jilin University | Communications Engineering, 2023 | Leadshine 6-axis motion controller running G-code in the custom multi-material 3D printer (fabrication tool) | Normal + shear + temperature tactile sensor printed directly onto the fingertip of an anthropomorphic hand | T04 (T04.5) |

## Reading list by track

### T01 Autonomous Urban Services
No directly relevant paper found for Leadshine's hands or joint modules. Closest material:
- [Precast-concrete surface robot (Sensors 2024)](https://doi.org/10.3390/s24113336) — coverage path planning around obstacles with A* dead-zone escape; the planner idea transfers to cleaning / maintenance coverage (T01.2, T01.6).
- General background, not Leadshine-specific and does not mention Leadshine: [Dexterous Robotic Hands in the Foundation-Model Era: A Full-Stack Survey (arXiv 2611.06724, Ji Pei, Nov 2026)](https://arxiv.org/abs/2611.06724) — orientation on data collection, retargeting and evaluation if you put a DH-series hand on a service robot.

### T02 Resilient & Safe City
No directly relevant paper found.

### T03 Sustainable City
- [Salt-marsh carbon-flux monitoring system (Sensors 2026)](https://doi.org/10.3390/s26102966) — full stack for unattended environmental sensing: sensor node, stepper-driven mast, cloud dashboard, data-fusion; a template for T03.2 / T03.7.
- [FGA-Corn precision application (Front. Plant Sci. 2025)](https://doi.org/10.3389/fpls.2025.1571228) — small detector → decision rule → stepper actuation; the same pattern fits sorting or targeted dosing demos (T03.1, T03.6).
- [Precast-concrete surface robot (Sensors 2024)](https://doi.org/10.3390/s24113336) — stepper-only 5-axis machine with brake motors for power-off safety; reference for a custom mechanism in construction / infrastructure (T03.4).

### T04 Elderly Care & Rehabilitation
- [Robot arm-assisted acupuncture system (Front. Bioeng. Biotechnol. 2025)](https://doi.org/10.3389/fbioe.2025.1563263) — how to bolt a small actuator to an arm flange and validate motion and force against a human therapist; method transfers to any care-procedure demo (T04.2, T04.6).
- [In vitro joint testing system (Bioengineering 2023)](https://doi.org/10.3390/bioengineering10091006) — force-profile tracking with a Leadshine motion card + stepper; useful for rehab-training force targets (T04.3).
- [Upright radiotherapy platform (Medical Physics 2025)](https://doi.org/10.1002/mp.17523) — patient-carrying rotation stage; safety margins, load assumptions and accuracy tests for moving a seated person (T04.4).
- [3D-printed multi-directional tactile sensor (Commun. Eng. 2023)](https://doi.org/10.1038/s44172-023-00131-x) — what normal / shear fingertip sensing enables on an anthropomorphic hand; context for the tactile DH116-M and DH2116 (T04.5).
- [Dexterous-hand survey (arXiv 2611.06724)](https://arxiv.org/abs/2611.06724) — general background for hand-over and assistive manipulation; does not mention Leadshine.

## White papers, patents and technical reports

- **White papers / technical reports:** none found. The English blog has four selection guides (closed-loop stepper series, integrated vs. separate servo, servo sizing, stepper vs. servo for packaging) — practical, not research.
- **Patents:** company statements only. The English technology page (dated) lists 24 invention patents, 45 utility-model patents, 89 design patents and 116 software copyrights; elsewhere the site cites about 500 patents. No individual dexterous-hand or joint-module patent was opened and verified in this pass. ⚠️ unverified at patent level.
- **Standards / certifications:** ISO 9001 (since 2004), CE and TÜV on selected products; no evidence found of Leadshine authoring public technical standards.

## Sources

- [Leadshine corporate overview (founder biography, history, engineering laboratory)](https://www.leadshine.com/abouts/about_corporate_overview.html)
- [Leadshine technology and quality page (R&D share, patent counts, MIT origin)](https://www.leadshine.com/abouts/about_technology_quality.html)
- [Leadshine English blog list](https://www.leadshine.com/newsEvents/Blog.html)
- [Leadshine store news list](https://store.leadshine.com/blogs/news)
- [Leadshine Chinese site (DH116 developer entity)](https://www.leisai.com/)
- [DH2116 series product page (SDK, OS and language support)](https://www.leadshine.com/robots/dextrous-hands/dh2116-series.html)
- [DH116 series product page](https://www.leadshine.com/robots/dextrous-hands/dh116-series.html)
- [DH116S user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_Series_Dexterous_User_Manual.pdf)
- [DH2116 user manual (PDF)](https://store.leadshine.com/cdn/shop/files/DH2116_Series_Dexterous_Hand_User_Manual.pdf)
- [DH116S LHandPro ROS 2 example project description (PDF)](https://store.leadshine.com/cdn/shop/files/DH116S_LHandPro_ROS2_Example_Project_Description.pdf)
- [Eastmoney F10 management data for 002979 (Li Weiping résumé, board)](https://emweb.securities.eastmoney.com/PC_HSF10/CompanyManagement/PageAjax?code=SZ002979)
- [Eastmoney F10 company survey for 002979 (legal name, employees)](https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/PageAjax?code=SZ002979)
- [Crossref record: On the Adaptive Control of Robot Manipulators](https://api.crossref.org/works/10.1177/027836498700600303)
- [Crossref record: Adaptive manipulator control: A case study](https://api.crossref.org/works/10.1109/9.14411)
- [Crossref record: Composite adaptive control of robot manipulators](https://api.crossref.org/works/10.1016/0005-1098%2889%2990094-0)
- [Open Library: Applied nonlinear control](https://openlibrary.org/works/OL4465059W)
- [arXiv listing search for "Leadshine" (no results)](https://arxiv.org/search/?query=Leadshine&searchtype=all)
- [arXiv 2611.06724 — dexterous-hand survey](https://arxiv.org/abs/2611.06724)
- [GitHub repository listing for "leadshine"](https://github.com/search?q=leadshine&type=repositories)
- [GitHub: openvmp/stepper_driver_em2rs](https://github.com/openvmp/stepper_driver_em2rs)
- [GitHub: marcoreps/linuxcnc_leadshine_EL8](https://github.com/marcoreps/linuxcnc_leadshine_EL8)
- [Europe PMC full text: PMC13211138 (salt-marsh carbon flux, Sensors 2026)](https://europepmc.org/article/PMC/PMC13211138)
- [Europe PMC full text: PMC12860710 (acupuncture twisting parameters, Biomed J)](https://europepmc.org/article/PMC/PMC12860710)
- [Europe PMC full text: PMC12364822 (robot arm-assisted acupuncture)](https://europepmc.org/article/PMC/PMC12364822)
- [Europe PMC full text: PMC12279808 (FGA-Corn)](https://europepmc.org/article/PMC/PMC12279808)
- [Europe PMC full text: PMC11788243 (upright radiotherapy platform)](https://europepmc.org/article/PMC/PMC11788243)
- [Europe PMC full text: PMC11784860 (bistable fabric mechanism)](https://europepmc.org/article/PMC/PMC11784860)
- [Europe PMC full text: PMC11174809 (precast-concrete robot)](https://europepmc.org/article/PMC/PMC11174809)
- [Europe PMC full text: PMC10525521 (in vitro joint testing system)](https://europepmc.org/article/PMC/PMC10525521)
- [Europe PMC full text: PMC10956052 (3D-printed tactile sensor)](https://europepmc.org/article/PMC/PMC10956052)
