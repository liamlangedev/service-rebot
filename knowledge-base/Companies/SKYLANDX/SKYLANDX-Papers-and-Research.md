---
type: papers
company: "SKYLANDX"
slug: SKYLANDX
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# SKYLANDX — Papers and Research

⬆ [SKYLANDX profile](SKYLANDX.md) · [Solutions and projects](SKYLANDX-Solutions-and-Projects.md) · [Developer guide](SKYLANDX-Developer-Guide.md)

> **Read this in 20 seconds:** SKYLANDX publishes **no papers, datasets, models or code under its own name**. Its research footprint is (a) the pre-company HKUST Aerial Robotics Group papers of its staff (VINS-Fusion, GVINS, A-LOAM, fast-flight planning) and (b) **two third-party papers that used MetaCam scanners** — one of which (Wanderland, CVPR 2026) ships an open scan → 3DGS → Isaac Sim pipeline you can reuse this weekend.

## Research footprint

- **Research-rooted, not research-publishing.** The official about page says the core team comes from the HKUST–DJI Joint Innovation Lab and "led" VINS-Mono, VINS-Fusion and A-LOAM, and shows a "top-tier publications & awards" counter — but lists no paper. No paper with a SKYLANDX / Skyland Innovation affiliation was found.
- **Key people (new vs. the profile):** the HKSTP company directory names **Pan Jie (CEO)** — HKUST master's, DJI–HKUST lab, "three top-tier journal papers and five top-tier conference papers" — **Situ Manhao (CTO)**, **Dr Gao Shichao (VP)** and **Cai Guang (engineer)**. A 2024 third-party paper thanks "Manhao Situ, Zhichao Feng, Peng Wu, **Jie Pan** and **Shaozu Cao** from Skyland Innovation" for developing the MetaCam Air.
- **How the staff-paper link was made (inference, stated openly):** Jie Pan and Shaozu Cao are co-authors of the VINS-Fusion papers; Shaozu Cao is first author of GVINS and co-modifier of A-LOAM. The HKUST Aerial Robotics Group publication list shows "J. Pan" on exactly **3 IEEE T-RO papers** plus conference papers, matching the HKSTP description. No single page states "the SKYLANDX CEO is the VINS-Fusion co-author", so treat the identity as **triangulated, not officially stated**.
- **Open-source posture: closed.** No official GitHub organisation, SDK, dataset or model. The production engine (MetaCam Studio "LIV SLAM") is described by a third-party paper as a **proprietary** LiDAR–inertial–visual–GNSS fusion pipeline building on ideas from VINS-Mono, GVINS and FAST-LIVO2. The staff's earlier HKUST code is open (mostly GPL-3.0) but is not maintained by SKYLANDX.
- **Search status for this doc:** web search **was available but rationed** — 2 extended searches were run (the first found the two third-party papers and the HKSTP listing; the second found nothing new). Everything else was verified by opening known pages (arXiv, HKUST lab publication list, GitHub, Hugging Face, official site). More third-party MetaCam papers probably exist; only the two below could be confirmed.

## Company-authored and company-affiliated papers

**None of these carries a SKYLANDX affiliation.** All are HKUST Aerial Robotics Group papers (Prof. Shaojie Shen's lab) written before or outside the company, co-authored by people later credited as Skyland Innovation staff. Newest first by publication date.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [A General Optimization-based Framework for Global Pose Estimation with Multiple Sensors](https://arxiv.org/abs/1901.03642) (VINS-Fusion, global part) | Tong Qin, **Shaozu Cao**, **Jie Pan**, Shaojie Shen — HKUST | arXiv 2019; journal version IET Cyber-Systems and Robotics 7(1), 2025 ([DOI](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/csy2.70023), per lab list) | Pose-graph fusion of any local odometry (VO / VIO) with global sensors (GPS, magnetometer, barometer) → locally accurate, globally drift-free pose | [VINS-Fusion code](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) (GPL-3.0) | T01 T02 |
| [GVINS: Tightly Coupled GNSS-Visual-Inertial Fusion for Smooth and Consistent State Estimation](https://arxiv.org/abs/2103.07899) | **Shaozu Cao**, Xiuyuan Lu, Shaojie Shen — HKUST | IEEE T-RO 38(4), 2022 (arXiv 2021) | Tightly couples raw GNSS (pseudorange, Doppler) with camera + IMU; survives indoor ↔ outdoor transitions and gains from even one satellite | [GVINS code](https://github.com/HKUST-Aerial-Robotics/GVINS) (GPL-3.0) · [GVINS-Dataset](https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset) | T01 T02 |
| [RAPTOR: Robust and Perception-aware Trajectory Replanning for Quadrotor Fast Flight](https://arxiv.org/abs/2007.03465) | Boyu Zhou, **Jie Pan**, Fei Gao, Shaojie Shen — HKUST | IEEE T-RO 37(6), 2021 (arXiv 2020) | Fast replanning in unknown clutter that accounts for what the sensor can and cannot see (perception-aware, risk-aware) | [Fast-Planner code](https://github.com/HKUST-Aerial-Robotics/Fast-Planner) | T02 |
| [Real-time temporal and rotational calibration of heterogeneous sensors using motion correlation analysis](https://ieeexplore.ieee.org/document/9271875) ¹ | K. Qiu, T. Qin, **J. Pan** ², S. Liu, S. Shen — HKUST | IEEE T-RO 37(2), 2021 | Online time-offset and rotation calibration between different sensor types from their motion — the kind of problem multi-sensor scanners must solve | None found | T01 T02 |
| [Teach-Repeat-Replan: A Complete and Robust System for Aggressive Flight in Complex Environments](https://arxiv.org/abs/1907.00520) | Fei Gao, Luqi Wang, Boyu Zhou, Xin Zhou, **Jie Pan**, Shaojie Shen — HKUST (journal author list per lab list; the arXiv preprint lists Luxin Han in place of Xin Zhou) | IEEE T-RO 36(5), 2020 (arXiv 2019) | Turns a rough human-piloted "teach" path into a smooth, safe, feasible trajectory and replans locally around new obstacles; framed for inspection, transport, search-and-rescue | [Teach-Repeat-Replan code](https://github.com/HKUST-Aerial-Robotics/Teach-Repeat-Replan) (GPL-3.0) | T01 T02 |
| [Robust Real-time UAV Replanning Using Guided Gradient-based Optimization and Topological Paths](https://arxiv.org/abs/1912.12644) | Boyu Zhou, Fei Gao, **Jie Pan**, Shaojie Shen — HKUST | ICRA 2020 | Avoids local minima in gradient-based replanning by exploring several topologically distinct paths in parallel | [Fast-Planner code](https://github.com/HKUST-Aerial-Robotics/Fast-Planner) | T02 |
| [A General Optimization-based Framework for Local Odometry Estimation with Multiple Sensors](https://arxiv.org/abs/1901.03638) (VINS-Fusion, local part) | Tong Qin, **Jie Pan**, **Shaozu Cao**, Shaojie Shen — HKUST | arXiv technical report, 2019 | One factor-graph odometry framework for stereo, mono + IMU and stereo + IMU sensor suites | [VINS-Fusion code](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) (GPL-3.0) | T01 T02 |
| [Real-time dense stereo embedded in a UAV for road inspection](https://ieeexplore.ieee.org/document/9025600) ¹ | R. Fan, J. Jiao, **J. Pan** ², H. Huang, S. Shen, M. Liu — HKUST | UAVision workshop at CVPR 2019 | Embedded real-time dense stereo on a drone to reconstruct road surfaces for damage inspection | None found | T02 T03 |
| [Optimal time allocation for quadrotor trajectory generation](https://ieeexplore.ieee.org/document/8593579) ¹ | F. Gao, W. Wu, **J. Pan** ², B. Zhou, S. Shen — HKUST | IROS 2018 | Computes the time profile along a planned path so the trajectory is as fast as limits allow | None found | — |
| [ACT: an autonomous drone cinematography system for action scenes](https://ieeexplore.ieee.org/document/8460703) ¹ | C. Huang, F. Gao, **J. Pan** ², Z. Yang, W. Qiu, P. Chen, X. Yang, S. Shen, K. Cheng — HKUST | ICRA 2018 | Drone that tracks and films a moving human subject autonomously | None found | — |
| [VINS-Mono: A Robust and Versatile Monocular Visual-Inertial State Estimator](https://arxiv.org/abs/1708.03852) | Tong Qin, Peiliang Li, Shaojie Shen — HKUST. **Claimed lineage only:** the about page credits the core team with VINS-Mono, but none of the three authors could be confirmed as SKYLANDX staff ⚠️ unverified | IEEE T-RO, 2018 (arXiv 2017) | The reference monocular camera + IMU estimator: robust initialisation, tightly coupled optimisation, loop closure, relocalisation | [VINS-Mono code](https://github.com/HKUST-Aerial-Robotics/VINS-Mono) (GPL-3.0) | T01 T02 |

¹ Title, authors and venue taken from the HKUST Aerial Robotics Group publication list, which links to the IEEE Xplore page shown; the IEEE page itself was not opened.
² Listed only as "J. Pan" on the lab list — full name not confirmed for this entry ⚠️ unverified.

**Bold** = named as Skyland Innovation staff in the LiVisSfM acknowledgements (Jie Pan, Shaozu Cao) and, for Pan Jie, as CEO in the HKSTP directory. No papers could be attributed to Situ Manhao, Gao Shichao, Cai Guang, Zhichao Feng or Peng Wu.

## Datasets, models and benchmarks released

**Released by SKYLANDX itself: nothing** (no dataset, model, benchmark or code; "Get Sample Data" is a request form). The table lists what is usable instead — clearly separated by who released it.

| Name | Type | Released by | Licence | Link | Useful for |
|---|---|---|---|---|---|
| Wanderland dataset | **Dataset captured with a MetaCam Air**: fisheye + undistorted images, dense point clouds, 3DGS models, COLMAP poses, Isaac Sim USDZ scenes, navigation episodes. Paper: **530 scenes, 420k+ frames, 100+ h, 3.8M+ m²** (New York City, Jersey City). Public release today: **335 scenes** | NYU AI4CE lab (third party) | Apache-2.0 | [Hugging Face](https://huggingface.co/datasets/ai4ce/wanderland) | Shows exactly what MetaCam data looks like after processing; ready-made urban scenes for navigation tests |
| wanderland | Code: download tools, 3D-reconstruction benchmark, **3DGS training on MetaCam-derived data** (gsplat), PLY → USDZ export notes, navigation episode generation | NYU AI4CE lab (third party) | Apache-2.0 | [GitHub](https://github.com/ai4ce/wanderland) | Template for "scan → 3DGS → simulator" with your own MetaCam scan |
| wanderland-lab | Benchmark / simulator: closed-loop navigation evaluation and residual RL fine-tuning on **Isaac Sim 5.1 / IsaacLab 2.3**; CityWalker as reference policy; needs an NVIDIA GPU (≥ 24 GB VRAM recommended) | NYU AI4CE lab (third party) | Apache-2.0 | [GitHub](https://github.com/ai4ce/wanderland-lab) | Plug in a navigation policy, get success rate / SPL back |
| VINS-Fusion | Code (ROS 1): multi-sensor visual-inertial odometry + GPS fusion example | HKUST Aerial Robotics (staff lineage) | GPL-3.0 | [GitHub](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) | Camera + IMU localization back end |
| VINS-Mono | Code (ROS 1): monocular visual-inertial SLAM | HKUST Aerial Robotics (claimed lineage) | GPL-3.0 | [GitHub](https://github.com/HKUST-Aerial-Robotics/VINS-Mono) | Background; lightweight VIO |
| A-LOAM | Code (ROS 1): clean re-implementation of LOAM LiDAR odometry; modifiers Tong Qin and **Shaozu Cao**; no paper of its own | HKUST Aerial Robotics (staff lineage) | BSD-style (see repository LICENSE) | [GitHub](https://github.com/HKUST-Aerial-Robotics/A-LOAM) | Simple LiDAR odometry to learn from. Note: LiVisSfM reports classic LOAM could not read the MetaCam Air data format |
| GVINS | Code (ROS 1): GNSS-visual-inertial estimator | HKUST Aerial Robotics (staff lineage) | GPL-3.0 | [GitHub](https://github.com/HKUST-Aerial-Robotics/GVINS) | Indoor ↔ outdoor localization |
| GVINS-Dataset | Dataset: synchronized visual, inertial and raw GNSS measurements | HKUST Aerial Robotics (staff lineage) | Not checked | [GitHub](https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset) | Testing GNSS fusion without hardware |
| Fast-Planner | Code (ROS 1): quadrotor planner; linked from the RAPTOR and ICRA 2020 replanning papers | HKUST Aerial Robotics (staff lineage) | Not checked | [GitHub](https://github.com/HKUST-Aerial-Robotics/Fast-Planner) | Drone replanning in clutter |
| Teach-Repeat-Replan | Code (ROS 1): full teach-and-repeat quadrotor system | HKUST Aerial Robotics (staff lineage) | GPL-3.0 | [GitHub](https://github.com/HKUST-Aerial-Robotics/Teach-Repeat-Replan) | Teach-and-repeat pattern for inspection routes |

**GPL-3.0 warning:** fine for a hackathon demo; check before building a commercial product on it. The lineage repositories target ROS 1 (Kinetic / Melodic per the VINS-Fusion and A-LOAM READMEs) — porting to ROS 2 is your work.

## Third-party papers using their hardware or software

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [Wanderland: Geometrically Grounded Simulation for Open-World Embodied AI](https://arxiv.org/abs/2511.20620) · [project page](https://ai4ce.github.io/wanderland/) | Xinhao Liu, Jiaqi Li, Youming Deng, Ruxin Chen, Yingjia Zhang, Yifei Ma, Li Guo, Yiming Li, Jing Zhang, Chen Feng — New York University, Cornell University | **CVPR 2026 (Highlight)**; arXiv Nov 2025 | **SkylandX MetaCam Air** (described as Livox Mid-360 LiDAR with IMU + two synchronized 4K fisheye cameras > 180° + RTK-GNSS antenna) and **MetaCam Studio** "LIV SLAM" for metric colorized point clouds and camera poses. Authors thank SkylandX for technical support | A real-to-sim pipeline: handheld multi-sensor capture → metric reconstruction → 3DGS → Isaac Sim scenes. Finds that image-only reconstruction scales poorly and that **geometry quality drives both view-synthesis and navigation-benchmark reliability**. Benchmarks point-goal, image-goal and vision-language navigation, 3D reconstruction and novel-view synthesis | T01 T02 |
| [LiVisSfM: Accurate and Robust Structure-from-Motion with LiDAR and Visual Cues](https://arxiv.org/abs/2410.22213) | Hanqing Jiang, Liyang Zhou, Zhuang Zhang, Yihao Yu (SenseTime Research), Guofeng Zhang (State Key Lab of CAD&CG, Zhejiang University) | arXiv preprint, Oct 2024 (no venue listed) | **MetaCam-Air** handheld scanner "produced by Skyland Innovation"; four self-captured scenes (outdoor office, tearoom, corridor, campus building with clock tower) plus KITTI | An IMU-free LiDAR + visual SfM with joint bundle adjustment and loop closure that reports better poses and dense reconstruction than LIO / LIVO baselines on MetaCam data. No code; data on request only | T02 T03 |

Only these two could be opened and confirmed. Both use the **first-generation MetaCam Air**; no paper using MetaCam Air 2, Pro, Lite or the C01 LiDAR was found.

## Reading list by track

### T01 Autonomous Urban Services
- **Wanderland (CVPR 2026)** — the closest thing to a recipe for T01.6 / T01.1: scan a street or corridor with a MetaCam, build a 3DGS + USDZ scene, and evaluate a navigation policy in closed loop before touching a robot. Code and data are Apache-2.0.
- **wanderland-lab README** — read this rather than the paper if you only have an hour: installation, the `Policy` interface, KPIs.
- **VINS-Fusion, global pose paper** — how to fuse a local odometry source with GNSS in a pose graph; useful when a delivery robot crosses between sky-view and covered areas.
- **GVINS (T-RO 2022)** — indoor ↔ outdoor transitions with intermittent GNSS; relevant to a village route that passes through arcades or buildings.
- **Teach-Repeat-Replan (T-RO 2020)** — the "teach a route once, repeat it safely" pattern maps directly onto a scan-once, relocalize-later delivery demo.

### T02 Resilient & Safe City
- **GVINS (T-RO 2022)** — robust state estimation when satellites drop out; the published background to the "GPS-denied" claim.
- **Teach-Repeat-Replan (T-RO 2020)** — explicitly motivated by infrastructure inspection and search-and-rescue; shows global map + local replanning around unmapped obstacles.
- **RAPTOR (T-RO 2021)** — perception-aware replanning for fast flight in unknown clutter (T02.6); a reference for what "safe at speed with limited sensing" requires.
- **LiVisSfM (arXiv 2024)** — evidence of the reconstruction accuracy reachable from MetaCam data; relevant if your demo is scan-to-scan change detection (T02.3).
- **Real-time dense stereo embedded in a UAV for road inspection (UAVision 2019)** — a compact example of robot-carried surface-damage inspection (T02.3).
- **Wanderland (CVPR 2026)** — its indoor–outdoor capture protocol and geometry-quality findings apply to digital twins for emergency planning.

### T03 Sustainable City
- No paper on waste, recycling, water or energy was found. Closest transferable work:
- **LiVisSfM (arXiv 2024)** — accurate dense reconstruction of buildings from MetaCam data, the starting point for retrofit or volume measurements (T03.4).
- **Real-time dense stereo embedded in a UAV for road inspection (UAVision 2019)** — infrastructure condition monitoring that extends asset life (T03.4).
- **Wanderland dataset** — a worked example of large-scale environmental 3D data collection and release (T03.7), not an environmental-monitoring study.

### T04 Elderly Care & Rehabilitation
- **No directly relevant paper found.**
- Transferable only: the **Wanderland** pipeline (scan → 3DGS → USDZ → Isaac Sim) can be pointed at a care room or apartment to give another team's assistive robot a simulation scene. The paper's scenes are urban, not care settings.

## White papers, patents and technical reports

- **No white paper, technical report or patent could be verified.** Patent databases were not searched (search budget).
- Official technical material is limited to product brochures (specification tables for MetaCam Air 2, MetaCam Pro, C01 LiDAR — linked from the [developer guide](SKYLANDX-Developer-Guide.md)) and one blog post, [What makes a SLAM scanner](https://skylandx.com/blog/slam-scanner-algorithm/) (2026-09-20), which cites no papers.
- The about page's "top-tier publications & awards" counter is not backed by a public list.

## Sources

- [SKYLANDX — About (team background, VINS-Mono / VINS-Fusion / A-LOAM claim)](https://skylandx.com/about/)
- [SKYLANDX — Blog index](https://skylandx.com/blog/) · [Blog: What makes a SLAM scanner](https://skylandx.com/blog/slam-scanner-algorithm/)
- [SKYLANDX — Case studies: Robotics](https://skylandx.com/case-studies-robotics/)
- [SKYLANDX — MetaCam Air (first generation)](https://skylandx.com/metacam-air/)
- [SKYLANDX — sitemap](https://skylandx.com/sitemap.xml)
- [HKSTP company directory — Skyland Innovation Company Limited (leadership names, publication counts)](https://www.hkstp.org/directory/electronics/skyland-innovation-company-limited)
- [HKUST Aerial Robotics Group — publication list](https://uav.hkust.edu.hk/publications/)
- [arXiv 2511.20620 — Wanderland](https://arxiv.org/abs/2511.20620) · [HTML full text](https://arxiv.org/html/2511.20620v2) · [project page](https://ai4ce.github.io/wanderland/)
- [GitHub — ai4ce/wanderland](https://github.com/ai4ce/wanderland) · [ai4ce/wanderland-lab](https://github.com/ai4ce/wanderland-lab) · [Hugging Face — ai4ce/wanderland dataset](https://huggingface.co/datasets/ai4ce/wanderland)
- [arXiv 2410.22213 — LiVisSfM](https://arxiv.org/abs/2410.22213) · [HTML full text](https://arxiv.org/html/2410.22213v1)
- [arXiv 1901.03642 — VINS-Fusion global pose estimation](https://arxiv.org/abs/1901.03642)
- [arXiv 1901.03638 — VINS-Fusion local odometry estimation](https://arxiv.org/abs/1901.03638)
- [arXiv 2103.07899 — GVINS](https://arxiv.org/abs/2103.07899)
- [arXiv 2007.03465 — RAPTOR](https://arxiv.org/abs/2007.03465)
- [arXiv 1907.00520 — Teach-Repeat-Replan](https://arxiv.org/abs/1907.00520)
- [arXiv 1912.12644 — Robust real-time UAV replanning](https://arxiv.org/abs/1912.12644)
- [arXiv 1708.03852 — VINS-Mono](https://arxiv.org/abs/1708.03852)
- [GitHub — HKUST-Aerial-Robotics/VINS-Fusion](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) · [VINS-Mono](https://github.com/HKUST-Aerial-Robotics/VINS-Mono) · [A-LOAM](https://github.com/HKUST-Aerial-Robotics/A-LOAM) · [GVINS](https://github.com/HKUST-Aerial-Robotics/GVINS) · [GVINS-Dataset](https://github.com/HKUST-Aerial-Robotics/GVINS-Dataset) · [Fast-Planner](https://github.com/HKUST-Aerial-Robotics/Fast-Planner) · [Teach-Repeat-Replan](https://github.com/HKUST-Aerial-Robotics/Teach-Repeat-Replan)
