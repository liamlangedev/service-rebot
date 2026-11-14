---
type: papers
company: "Spirit AI"
slug: Spirit-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Spirit AI — Papers and Research

⬆ [Spirit AI profile](Spirit-AI.md) · [Solutions and projects](Spirit-AI-Solutions-and-Projects.md) · [Developer guide](Spirit-AI-Developer-Guide.md)

> **Scope note:** this is the robotics company Spirit AI (千寻智能, `spirit-ai.com`), not the UK game-AI firm of the same name.
> **Coverage caveat:** the web-search quota for this pass was exhausted before paper hunting started. Everything below was verified by opening official pages directly (arXiv, GitHub, Hugging Face, the company blog, the chief scientist's publication page). Items that normally need a search to find — third-party papers that use Moz1 or Spirit v1.5, patents, a Spirit v1.6 write-up — could **not** be hunted and are marked as gaps, not as "none exist".

## Research footprint

- **Research-led, but publishes mostly through its chief scientist's university lab.** Spirit AI itself has published **one** technical report (the Spirit-v1.5 blog, Jan 2026). The peer-reviewed output comes from Gao Yang's group at Tsinghua IIIS / Shanghai Qi Zhi Institute, where **"Spirit AI" / "Spirit.AI" appears in the author affiliations of 5 arXiv papers** I opened (OneTwoVLA, Point-VLA, HuMI, Legato, OpenHLM). Two of them also acknowledge a "Spirit AI Innovation Program".
- **Key people seen on papers:** Yang Gao (Tsinghua IIIS; Spirit AI affiliation on arXiv), Junliang Guo and Junyuan Xie (Spirit AI; Junliang Guo is also a listed contact on the `spirit-v1.5` repo), Yufeng Liu, Kaiyu Li, Cheng Ma (Spirit AI on Point-VLA), plus Tsinghua students Yingdong Hu, Fanqi Lin, Ruiqian Nai, Chengbo Yuan, Tong Zhang, Chuan Wen (now SJTU).
- **Research themes that map to the product:** (1) VLA foundation models and data scaling (Data Scaling Laws → Spirit-v1.5 "diverse collection"), (2) VLA usability add-ons on top of π0 / π0.5 (adaptive reasoning, pointing instructions, smooth action chunking), (3) whole-body humanoid manipulation (HuMI, OpenHLM, HuB — all on **Unitree G1**, not Moz), (4) tactile and human-video learning.
- **Open-source posture:** one real public repo (`spirit-v1.5`, **MIT**, **671 stars**, inference + fine-tuning code) and two Hugging Face checkpoints. No dataset has been released; the pre-training corpus is proprietary. No arXiv paper exists for Spirit-v1.5 (the README cites the blog). Spirit v1.6 is closed and I found no technical write-up for it.
- **Not found on any paper I opened:** the Moz1 robot named as the experimental platform. Point-VLA and Legato describe "a dual-arm robot" (7-DoF arms, head + two wrist cameras) and "a full-body humanoid" without naming the model — plausibly Moz1 ⚠️ unverified.

## Company-authored and company-affiliated papers

Legend for the Authors column: **[SA]** = Spirit AI listed in the author affiliations (checked in the arXiv HTML); **[lab]** = Gao Yang's Tsinghua lab, Spirit AI affiliation either absent or not checked. Venues are taken from Gao Yang's publication page.

| Paper | Authors / organisation | Venue, year | What it contributes | Artifacts | Tracks |
|---|---|---|---|---|---|
| [EgoTac: In-the-wild Tactile Prediction from Egocentric Vision](https://arxiv.org/abs/2608.15060) | W. Zhang, C. Yuan, Z. Zhang, Z. Cheng, Y. Gao · **[lab]** | NeurIPS 2026 | Predicts force and contact from egocentric human video; trained on **5.7M** image–tactile pairs | [Project page](https://egotac.github.io/) | T04 |
| [OpenHLM: An Empirical Recipe for Whole-Body Humanoid Loco-Manipulation](https://arxiv.org/abs/2606.22174) | Y. Hu, H. Zhu, B. Zheng, Y. Hu, T. Zhang, Z. Chen, J. Zhao, R. Nai, Y. Gao · Tsinghua IIIS, Shanghai Qi Zhi, **[SA]** | CoRL 2026 | One-variable-at-a-time study of how to build a whole-body humanoid VLA (π0.5 init, joint-space teleop with PICO VR, co-training with cheaper data); Unitree G1; inference on one RTX 5080 | [Project page](https://openhlm-project.github.io/) (code, checkpoints, demo data per the paper) | T01 T02 |
| [FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation](https://arxiv.org/abs/2606.13102) | C. Yuan, Z. Zhang, M. Zhou, W. Chen, … C. Wen, C. Lu, K. Zhang, Y. Gao (17 authors) · Tsinghua, Sharpa, SJTU, UC Berkeley, ETH Zurich and others · **[lab]** (Spirit AI not in affiliations) | CoRL 2026 | Tactile policy pre-trained on **~3,000 h** from **26** sources and **21** tactile sensors; shared token space across sensor types | [Project page](https://ftp1-policy.github.io/) · code / weights 🔭 "to be released" | T04 |
| [Learning Native Continuation for Action Chunking Flow Policies](https://arxiv.org/abs/2602.12978) ("Legato") | Y. Liu, H. Yu, J. Zhao, B. Li, D. Zhang, M. Li, W. Wu, Y. Hu, J. Xie, J. Guo, D. Wang, Y. Gao · SJTU, **[SA]**, Tsinghua, Tongji, USTC | RSS 2026 | Training-time fix that makes consecutive action chunks join smoothly (alternative to inference-time real-time chunking); tested on π0.5, π0, GR00T N1.6; dual-arm robot, single RTX 4090 | [Project page](https://lyfeng001.github.io/Legato/) · no code link found | T01 T03 T04 |
| [HuMI: Humanoid Whole-Body Manipulation from Humanoid-Free Demonstrations](https://arxiv.org/abs/2602.06643) | R. Nai, B. Zheng, J. Zhao, H. Zhu, S. Dai, Z. Chen, Y. Hu, Y. Hu, T. Zhang, C. Wen, Y. Gao · Tsinghua IIIS, Shanghai Qi Zhi, **[SA]**, SJTU | CoRL 2026 | Collect whole-body demos with UMI-style handheld grippers + 5 VIVE trackers (no robot needed), then run a diffusion policy + whole-body controller on Unitree G1 | [Project page](https://humanoid-manipulation-interface.github.io/) | T01 T02 |
| [Spirit-v1.5: Clean Data Is the Enemy of Great Robot Foundation Models](https://www.spirit-ai.com/en/blog/spirit-v1-5) | Spirit AI Team · **[SA]** (company technical blog, no arXiv version) | Spirit AI Blog, Jan 2026 | Argues for open-ended "diverse collection" over scripted demos; reports **+200 %** collection hours per person, **−60 %** researcher attention, **40 %** fewer fine-tune iterations vs clean-data pre-training; **#1 on RoboChallenge Table30** as of 11 Jan 2026 | [Code (MIT)](https://github.com/Spirit-AI-Team/spirit-v1.5) · [base weights](https://huggingface.co/Spirit-AI-robotics/Spirit-v1.5) · [fine-tuned weights](https://huggingface.co/Spirit-AI-robotics/Spirit-v1.5-for-RoboChallenge-move-objects-into-box) | T01 T03 T04 |
| [Point What You Mean: Visually Grounded Instruction Policy](https://arxiv.org/abs/2512.18933) ("Point-VLA") | H. Yu, J. Zhao, Y. Liu, K. Li, C. Ma, D. Zhang, Y. Hu, G. Chen, J. Xie, J. Guo, J. Zhao, Y. Gao · Tongji, SJTU, **[SA]**, Tsinghua | IROS 2026 | Adds a bounding box on the overhead camera image to the text instruction so the policy knows *which* object; **92.5 %** average success vs **32.4 %** for text-only on six pick / place tasks; π0.5 backbone | [Project page](https://yuhang-harry.github.io/Point-VLA/) · no code link found | T01 T03 T04 |
| [MotionTrans: Human VR Data Enable Motion-Level Learning for Robotic Manipulation Policies](https://arxiv.org/abs/2509.17759) | C. Yuan, R. Zhou, M. Liu, Y. Hu, S. Wang, L. Yi, C. Wen, S. Zhang, Y. Gao · **[lab]** | ICRA 2026 | Co-trains on human VR recordings + robot data; motions for **13** tasks transfer from human data, **9** reach non-trivial zero-shot success | [Project page](https://motiontrans.github.io/) (data, code, weights per the abstract) | — (data-collection enabler) |
| [OneTwoVLA: A Unified Vision-Language-Action Model with Adaptive Reasoning](https://arxiv.org/abs/2505.11917) | F. Lin, R. Nai, Y. Hu, J. You, J. Zhao, Y. Gao · Tsinghua, Shanghai Qi Zhi, **[SA]** (Y. Gao) | ICLR 2026 | One model that both acts and reasons, switching to explicit reasoning at key moments of long-horizon tasks; built on π0; Franka + dual ARX arms | [Project page](https://one-two-vla.github.io/) | T01 T04 |
| [HuB: Learning Extreme Humanoid Balance](https://arxiv.org/abs/2505.07294) | T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath, Y. Gao · **[lab]** | CoRL 2025 (oral) | Extreme balance poses on Unitree G1 via motion refinement, balance-aware policy learning and sim-to-real robustness | [Project page](https://hub-robot.github.io) | — |
| [KineDex: Learning Tactile-Informed Visuomotor Policies via Kinesthetic Teaching for Dexterous Manipulation](https://arxiv.org/abs/2505.01974) | D. Zhang, C. Yuan, C. Wen, H. Zhang, J. Zhao, Y. Gao · **[lab]** | CoRL 2025 | Hand-guided demonstration collection for dexterous hands with tactile input and force control; **74.4 %** average success on contact-rich tasks | — | T04 |
| [FP3: A 3D Foundation Policy for Robotic Manipulation](https://arxiv.org/abs/2503.08950) | R. Yang, G. Chen, C. Wen, Y. Gao · **[lab]** | ICRA 2026 (best-paper finalist, robot learning) | Point-cloud diffusion-transformer policy pre-trained on **60k** trajectories; new task from **80** demos with **>90 %** success in unseen scenes | [Project page](https://3d-foundation-policy.github.io) | T01 T03 |
| [Data Scaling Laws in Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2410.18647) | F. Lin, Y. Hu, P. Sheng, C. Wen, J. You, Y. Gao · **[lab]** | ICLR 2025 | Shows that the number of **environments and objects** matters far more than demos per setup — the intellectual root of Spirit-v1.5's data strategy | — (arXiv page lists none) | T01 T03 T04 |
| [CoPa: General Robotic Manipulation through Spatial Constraints of Parts with Foundation Models](https://arxiv.org/abs/2403.08248) | H. Huang, F. Lin, Y. Hu, S. Wang, Y. Gao · **[lab]** | IROS 2024 | Training-free manipulation: a VLM picks the grasp part and spatial constraints, a solver outputs 6-DoF poses | [Project page](https://copa-2024.github.io/) | T01 T02 T03 T04 |
| [General Flow as Foundation Affordance for Scalable Robot Learning](https://arxiv.org/abs/2401.11439) | C. Yuan, C. Wen, T. Zhang, Y. Gao · **[lab]** | CoRL 2024 | Predicts 3D point flow from human RGB-D video; zero-shot human-to-robot transfer, **81 %** success over 18 tasks | [Project page](https://general-flow.github.io) (code, data) | — |
| [Any-point Trajectory Modeling for Policy Learning](https://arxiv.org/abs/2401.00025) | C. Wen, X. Lin, J. So, K. Chen, Q. Dou, Y. Gao, P. Abbeel · **[lab]** + UC Berkeley, CUHK | RSS 2024 | Pre-trains a point-track predictor on action-free video to guide policies with little labelled data | [Project page](https://xingyu-lin.github.io/atm) (code) | — |
| [Look Before You Leap: Unveiling the Power of GPT-4V in Robotic Vision-Language Planning](https://arxiv.org/abs/2311.17842) ("ViLa") | Y. Hu, F. Lin, T. Zhang, L. Yi, Y. Gao · **[lab]** | arXiv preprint, 2023 | Uses a vision-language model directly on camera images to produce multi-step task plans, no separate perception module | — | T01 T02 T03 T04 |

**More from the same lab (listed on the publication page, not individually opened here):** EasyInsert, Prior Reinforce, TimeRewarder, SKIL, "Best of Sim and Real", Spatially-anchored Tactile Awareness, RoboEngine — see [Gao Yang's publication list](https://yang-gao.weebly.com/publications.html).

## Datasets, models and benchmarks released

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| **Spirit-v1.5 (base)** ✅ | VLA checkpoint: Qwen3-VL-4B-Instruct backbone + DiT action head, **~5B params**, F32 safetensors | **apache-2.0** on the Hugging Face card; the GitHub repo is **MIT** (the two differ — check before redistributing) | [Hugging Face](https://huggingface.co/Spirit-AI-robotics/Spirit-v1.5) | Starting point for fine-tuning a manipulation policy; needs an **A100 80 GB**-class GPU to run as tested |
| **Spirit-v1.5 for RoboChallenge "move objects into box"** ✅ | Fine-tuned checkpoint for one Table30 task | not checked ⚠️ unverified | [Hugging Face](https://huggingface.co/Spirit-AI-robotics/Spirit-v1.5-for-RoboChallenge-move-objects-into-box) (link from the GitHub README; card not opened) | Reproducing the benchmark result; reference for what a fine-tuned checkpoint looks like |
| **spirit-v1.5 code** ✅ | Inference code (Jan 2026) + fine-tuning code (Apr 2026); PyTorch FSDP training; fine-tune recommended on **8× A100 80 GB** | MIT | [GitHub](https://github.com/Spirit-AI-Team/spirit-v1.5) | Running / fine-tuning the model; example uses the public `RoboChallenge/task_table30_move_objects_into_box` dataset |
| **Moz1 URDF** ✅ | Robot description (26 DoF) for MuJoCo / Isaac conversion | not stated | [Docs portal](https://docs.spirit-ai.com/zh) | Simulation and motion planning for Moz1 |
| **π0.5 adaptation for Moz1 (`pi05_moz`)** 🧪 | openpi config + policy server / robot client | distributed via after-sales support, not public | [Docs: Pi0.5 adaptation](https://docs.spirit-ai.com/zh/open-resources/pi.html) | Running a π0.5 policy on Moz1 — ask on-site staff for the package |
| **issac_moz1** 🔭 | Isaac simulation repo for Moz1 — **currently empty** | none | [GitHub](https://github.com/Spirit-AI-Team/issac_moz1) | Nothing yet; placeholder |
| Forks: `PI_Official` (openpi), `lerobot`, `ByteCheckpoint` | Upstream forks, no Spirit-specific release confirmed | Apache-2.0 (upstream) | [GitHub org](https://github.com/Spirit-AI-Team) | Signals the stack the company builds on (openpi, LeRobot data format, ByteCheckpoint for large-scale checkpointing) |
| OpenHLM release (lab-affiliated) ✅ | Code, checkpoints and demonstration data for Unitree G1 whole-body VLA (per the paper) | not checked | [Project page](https://openhlm-project.github.io/) | Teams with a Unitree G1 |
| MotionTrans release (lab-affiliated) ✅ | Human VR + robot data, code, weights (per the abstract) | not checked | [Project page](https://motiontrans.github.io/) | Learning from Quest-style human VR recordings |

- **Datasets released by the company:** none found. The Spirit-v1.5 pre-training corpus ("diverse collection") is not public.
- **Benchmarks created by the company:** none. Spirit-v1.5 is evaluated on the third-party **RoboChallenge Table30** (30 table-top tasks on Franka, ARX5, UR5 and ALOHA, per the Spirit blog).

## Third-party papers using their hardware or software

**No third-party paper that uses Moz1, Moz2, the MozRobot SDK or Spirit-v1.5 could be confirmed.** This is a coverage gap, not a finding: the search quota ran out, so no hunt was possible. Moz1 only launched in late 2025 and Spirit-v1.5 was opened in Jan 2026, so the body of external work is likely small in any case.

Closest verified third-party work (it does **not** use Spirit AI hardware — it is the benchmark and the baseline Spirit AI builds on):

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [RoboChallenge: Large-scale Real-robot Evaluation of Embodied Policies](https://arxiv.org/abs/2510.17950) | A. Yakefu, B. Xie, C. Xu, … Z. Yan (37 authors, alphabetical) · RoboChallenge | arXiv, Oct 2025 | Remote real-robot test bed; **Table30** benchmark. Spirit-v1.5 was later submitted to and topped this leaderboard (Jan 2026) | How online real-robot evaluation works and how VLAs compare on 30 table-top tasks | T01 T03 |
| [π0.5: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | Physical Intelligence (K. Black, N. Brown, J. Darpinian, K. Dhabalia and others) | arXiv, Apr 2025 | The model Spirit AI ports to Moz1 (`pi05_moz`) and the backbone of Point-VLA, Legato and OpenHLM | Open-world household manipulation via co-training on heterogeneous data | T01 T04 |

## Reading list by track

### T01 Autonomous Urban Services
- **[Spirit-v1.5 blog](https://www.spirit-ai.com/en/blog/spirit-v1-5)** — what the open model can and cannot do, and how to collect teleop data that transfers (diverse, goal-driven sessions rather than repeated scripts).
- **[Point-VLA](https://arxiv.org/abs/2512.18933)** — "fetch *that* one": box-on-image instructions fix the ambiguity that breaks text-only VLAs in cluttered retail / concierge scenes.
- **[CoPa](https://arxiv.org/abs/2403.08248)** + **[ViLa](https://arxiv.org/abs/2311.17842)** — no training needed: VLM planning plus part-level grasp constraints. The most realistic recipe for a 48-hour build on Moz1's SDK.
- **[OneTwoVLA](https://arxiv.org/abs/2505.11917)** — pattern for long multi-step service tasks: act fast, reason only at decision points.
- **[Data Scaling Laws](https://arxiv.org/abs/2410.18647)** — if you do collect demos, vary environments and objects; do not pile up repeats of one setup.

### T02 Resilient & Safe City
- No directly relevant paper found (nothing on search and rescue, inspection, security or hazardous-environment teleoperation).
- Nearest enablers: **[ViLa](https://arxiv.org/abs/2311.17842)** / **[CoPa](https://arxiv.org/abs/2403.08248)** for zero-shot "open the valve / press the switch" manipulation, and **[HuMI](https://arxiv.org/abs/2602.06643)** / **[OpenHLM](https://arxiv.org/abs/2606.22174)** if a team works with a Unitree G1 humanoid rather than Moz1.

### T03 Sustainable City
- No paper targets waste sorting, energy or environmental monitoring directly.
- **[Point-VLA](https://arxiv.org/abs/2512.18933)** — cluttered picking and slot placement with pointed targets; maps well onto sorting recyclables into bins.
- **[FP3](https://arxiv.org/abs/2503.08950)** — data-efficient pick-and-place from point clouds (80 demos per new task) if a depth camera is available.
- **[Spirit-v1.5 blog](https://www.spirit-ai.com/en/blog/spirit-v1-5)** + **[RoboChallenge](https://arxiv.org/abs/2510.17950)** — the repo ships a public fine-tuning example for the Table30 task "move objects into box", the closest ready-made analogue to bin sorting.
- **[Legato](https://arxiv.org/abs/2602.12978)** — smoother, faster chunked execution when throughput on a sorting line matters.

### T04 Elderly Care & Rehabilitation
- No paper addresses elder care, rehabilitation or medical use directly.
- **[OneTwoVLA](https://arxiv.org/abs/2505.11917)** — reasoning-while-acting for long household chores and for reacting to a person mid-task.
- **[Point-VLA](https://arxiv.org/abs/2512.18933)** — a user (or caregiver on a tablet) points at the object to fetch; low-effort interface for people who cannot give precise verbal descriptions.
- **[KineDex](https://arxiv.org/abs/2505.01974)** and **[FTP-1](https://arxiv.org/abs/2606.13102)** — tactile, force-controlled contact; background reading for any physical-contact task (wiping, pressing, massage-like motions).
- **[EgoTac](https://arxiv.org/abs/2608.15060)** — estimating contact force from egocentric video; useful idea for monitoring how hard a person or robot presses.
- **[CoPa](https://arxiv.org/abs/2403.08248)** — training-free assistive manipulation (open a drawer, pour, hand over) to prototype with.

## White papers, patents and technical reports

- **Spirit-v1.5 technical blog** (Jan 2026) is the company's only technical report; the GitHub README's citation block points to it ("Spirit AI Team, 2026, Spirit AI Blog"). Figures worth a look: [Fig. 2 — diverse vs clean pre-training](https://www.spirit-ai.com/blog/images/blogs/spirit-v1-5/figure2.png), [Fig. 3 — scaling with data volume](https://www.spirit-ai.com/blog/images/blogs/spirit-v1-5/figure3.png), [Fig. 4 — Table30 leaderboard, 11 Jan 2026](https://www.spirit-ai.com/blog/images/blogs/spirit-v1-5/figure4.png).
- **Spirit v1.6** (VLA + world model, mid-2026): no paper, blog post or model card found. Treat capability claims as demo-level until a write-up appears.
- **Patents:** not researched in this pass (search quota exhausted). ⚠️ unverified

## Sources

- [Spirit AI blog — Spirit-v1.5: Clean Data Is the Enemy of Great Robot Foundation Models](https://www.spirit-ai.com/en/blog/spirit-v1-5)
- [GitHub — Spirit-AI-Team/spirit-v1.5 (README, citation block, releases)](https://github.com/Spirit-AI-Team/spirit-v1.5)
- [GitHub — Spirit-AI-Team organisation (repo list)](https://github.com/Spirit-AI-Team)
- [GitHub — Spirit-AI-Team/issac_moz1 (empty)](https://github.com/Spirit-AI-Team/issac_moz1)
- [Hugging Face — Spirit-AI-robotics/Spirit-v1.5 model card](https://huggingface.co/Spirit-AI-robotics/Spirit-v1.5)
- [Gao Yang — publication list (venues)](https://yang-gao.weebly.com/publications.html)
- [arXiv 2608.15060 — EgoTac](https://arxiv.org/abs/2608.15060)
- [arXiv 2606.22174 — OpenHLM](https://arxiv.org/abs/2606.22174)
- [arXiv 2606.13102 — FTP-1](https://arxiv.org/abs/2606.13102)
- [arXiv 2602.12978 — Learning Native Continuation for Action Chunking Flow Policies](https://arxiv.org/abs/2602.12978)
- [arXiv 2602.06643 — HuMI](https://arxiv.org/abs/2602.06643)
- [arXiv 2512.18933 — Point What You Mean](https://arxiv.org/abs/2512.18933)
- [arXiv 2509.17759 — MotionTrans](https://arxiv.org/abs/2509.17759)
- [arXiv 2505.11917 — OneTwoVLA](https://arxiv.org/abs/2505.11917)
- [arXiv 2505.07294 — HuB](https://arxiv.org/abs/2505.07294)
- [arXiv 2505.01974 — KineDex](https://arxiv.org/abs/2505.01974)
- [arXiv 2503.08950 — FP3](https://arxiv.org/abs/2503.08950)
- [arXiv 2410.18647 — Data Scaling Laws in Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2410.18647)
- [arXiv 2403.08248 — CoPa](https://arxiv.org/abs/2403.08248)
- [arXiv 2401.11439 — General Flow](https://arxiv.org/abs/2401.11439)
- [arXiv 2401.00025 — Any-point Trajectory Modeling](https://arxiv.org/abs/2401.00025)
- [arXiv 2311.17842 — Look Before You Leap (ViLa)](https://arxiv.org/abs/2311.17842)
- [arXiv 2510.17950 — RoboChallenge](https://arxiv.org/abs/2510.17950)
- [arXiv 2504.16054 — π0.5](https://arxiv.org/abs/2504.16054)
- [Spirit AI docs portal (URDF, Pi0.5 adaptation; via the company profile)](https://docs.spirit-ai.com/zh)
