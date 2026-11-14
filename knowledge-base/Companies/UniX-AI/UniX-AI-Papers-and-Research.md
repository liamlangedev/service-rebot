---
type: papers
company: "UniX AI"
slug: UniX-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# UniX AI — Papers and Research

⬆ [UniX AI profile](UniX-AI.md) · [Solutions and projects](UniX-AI-Solutions-and-Projects.md) · [Developer guide](UniX-AI-Developer-Guide.md)

> **In one line:** UniX AI (优理奇, Suzhou) publishes almost nothing under its own name. Its research footprint is the **visuo-tactile work of its founder Fengyu (Fred) Yang** from his University of Michigan / Yale years, plus **one 2026 paper that carries a UniX AI affiliation (UniTac, ECCV 2026)**. **No paper, dataset or model about the Wanda / Panther / Martian robots exists in public**, and no third-party paper using UniX hardware was found.

## Research footprint

- **Founder-driven, tactile-centred.** Founder and CEO Fengyu Yang (杨丰瑜) built his academic record on vision-based touch sensing: Touch and Go (NeurIPS 2022), Generating Visual Scenes from Touch (ICCV 2023), UniTouch and TaRF (both CVPR 2024). The product model "UniTouch" carries the same name as the CVPR paper (whether the on-robot model is the same network is ⚠️ unverified). Advisors on those papers: Andrew Owens (University of Michigan) and Alex Wong (Yale).
- **Only one paper with a company affiliation was found:** UniTac (arXiv June 2026, accepted at ECCV 2026) lists Fengyu Yang as "Yale University / UNIX AI" and Zhi Tao as "UNIX AI". Its robot experiment runs on an **AgileX Tracer / Cobot Magic dual-arm platform with a GelSight Mini — not on a UniX robot**.
- **The product stack is unpublished.** UniFlex (key-point imitation learning), UniCortex (long-horizon planner) and the on-robot UniTouch have **no paper, code, weights or benchmark**. The only technical description of UniFlex is a press interview (see the last section). The founder said in Sep 2025 that the robots carried **no tactile sensors yet** — so the tactile papers are background, not something you can run on a Wanda or Panther out of the box.
- **Academic link to SJTU:** Prof. Hesheng Wang (Shanghai Jiao Tong University) is named on the company timeline (IROS 2025) and described by Baidu Baike as Chief Scientist since July 2024 (⚠️ unverified — single non-official source). No paper from his lab with a UniX AI affiliation was found (see method note below).
- **Open-source posture: none at company level.** No official GitHub organisation, Hugging Face account or dataset. All usable artifacts are academic releases hosted by the founder or his co-authors. **Beware a name collision:** the GitHub organisation `UniX-AI-Lab` (StreamOPD, WorldReasonBench) is an independent, Tsinghua-led research collective for video models and is **not** the robot company.
- **How this doc was researched:** web search was available but rationed (2 searches, both used; neither surfaced a UniX-hardware paper). Everything else comes from direct fetches of arXiv abstract and full-text pages, project pages, GitHub repositories, the company site (English and Chinese) and its sitemap on 2026-11-14. Every paper below was opened on arXiv; titles, authors and dates are taken from there.

## Company-authored and company-affiliated papers

Affiliation key: **[UniX]** = UniX AI appears in the author affiliations · **[Founder]** = founder's academic work before or beside the company, no UniX AI affiliation on the paper.

| Paper | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [Dexterous Tactile World Model (DTWM)](https://arxiv.org/abs/2609.34286) **[Founder]** ⚠️ author identity inferred from name, Yale affiliation and co-author overlap | Ziyao Zeng, Xiatao Sun, Hao Wang, Yueyang Pan, Zhengxiang Yu, Fengyu Yang, Tianyu Liu, Zhiwen Fan, Daniel Rakita · Yale, Texas A&M, UCLA, U Washington | arXiv preprint, Sep 2026 | Video world model that predicts future egocentric manipulation frames from video **plus whole-hand tactile-glove signals**; touch cuts the under-estimation of hand motion from **23% to 9%** versus a vision-only twin | [Project page](https://adonis-galaxy.github.io/dtwm-project-page/) · [code](https://github.com/Adonis-galaxy/Dexterous-Tactile-World-Model) (Apache-2.0) | — |
| [UniTac: A Unified Multimodal Model for Cross-Sensor Tactile Understanding and Generation](https://arxiv.org/abs/2606.31451) **[UniX]** | Jiahang Tu*, Fengyu Yang*, Chenyang Ma, Xihang Yu, Ziyao Zeng, Shaokai Wu, Hanbin Zhao, Zhi Tao, Chao Zhang, Hui Qian, Alex Wong · Zhejiang U, Yale, **UniX AI**, Oxford, MIT, SJTU | ECCV 2026 (arXiv Jun 2026) | One model that both **describes touch in language** (hardness, roughness, comparisons, sensor ID) and **generates tactile images** across sensors; trained on about **400K clips / 1.6M frames** merged from five public datasets; real-robot test: pick the softer of two look-alike towels, and deformation-aware cup grasping with a π0.5-based policy with real or predicted touch | No code or weights link on the arXiv page (checked 2026-11-14) | T04 T01 |
| [TextToucher: Fine-Grained Text-to-Touch Generation](https://arxiv.org/abs/2409.05427) **[Founder]** | Jiahang Tu, Hao Fu, Fengyu Yang, Hanbin Zhao, Chao Zhang, Hui Qian · Zhejiang U group (affiliations not shown on arXiv HTML) | AAAI 2025 (arXiv Sep 2024) | Generates tactile images from text that describes both the object (texture, shape) and the sensor gel state; adds a text-touch contrastive metric (CTTP) | [Code](https://github.com/TtuHamg/TextToucher) (Apache-2.0) | — |
| [Tactile-Augmented Radiance Fields (TaRF)](https://arxiv.org/abs/2405.04534) **[Founder]** | Yiming Dou, Fengyu Yang, Yi Liu, Antonio Loquercio, Andrew Owens · U Michigan, Yale, UC Berkeley | CVPR 2024 | Registers sparse touch probes into a NeRF scene and trains a diffusion model that **predicts what any visible point would feel like**; ships a 13-scene visuo-tactile dataset | [Project page](https://dou-yiming.github.io/TaRF) · [code, data, checkpoints](https://github.com/Dou-Yiming/TaRF) | T02 (weak) |
| [Binding Touch to Everything: Learning Unified Multimodal Tactile Representations (UniTouch)](https://arxiv.org/abs/2401.18084) **[Founder]** | Fengyu Yang*, Chao Feng*, Ziyang Chen*, Hyoungseob Park, Daniel Wang, Yiming Dou, Ziyao Zeng, Xien Chen, Rit Gangopadhyay, Andrew Owens, Alex Wong · Yale, U Michigan | CVPR 2024 | Aligns touch embeddings from several vision-based tactile sensors with a pretrained image embedding space, giving **zero-shot material classification, grasp-stability prediction, cross-modal retrieval and touch question answering (Touch-LLM)** | [Project page](https://cfeng16.github.io/UniTouch/) · [code](https://github.com/cfeng16/UniTouch) · [weights](https://huggingface.co/chfeng/Touch-LLM) (MIT tag) | T03 T04 |
| [Generating Visual Scenes from Touch](https://arxiv.org/abs/2309.15117) **[Founder]** | Fengyu Yang, Jiacheng Zhang, Andrew Owens · U Michigan | ICCV 2023 | Latent-diffusion model for touch-to-image and image-to-touch synthesis; first to generate a scene image from touch alone | [Project page](https://fredfyyang.github.io/vision-from-touch/) · [code repo](https://github.com/fredfyyang/vision-from-touch) | — |
| [Touch and Go: Learning from Human-Collected Vision and Touch](https://arxiv.org/abs/2211.12498) **[Founder]** | Fengyu Yang, Chenyang Ma, Jiacheng Zhang, Jing Zhu, Wenzhen Yuan, Andrew Owens · U Michigan, CMU | NeurIPS 2022 (Datasets and Benchmarks) | In-the-wild dataset of paired egocentric video and GelSight touch collected by people probing real objects; baselines for visuo-tactile self-supervision, tactile-driven image stylisation and future-touch prediction | [Project page and dataset](https://touch-and-go.github.io/) (CC BY 4.0) · [code](https://github.com/fredfyyang/Touch-and-Go) | T02 T03 |

Notes on scope and identity:

- "Fengyu Yang" is a common name. arXiv lists other people with it (speech synthesis at Xiaomi, optimisation at UNC, a Meituan team member). Only the tactile / Michigan / Yale line above is attributed to the UniX founder; Baidu Baike independently names Touch and Go, the ICCV touch-vision diffusion paper, UniTouch and TaRF as his.
- The founder also co-authored non-robotics vision papers with the same Yale and Zhejiang groups (language-guided monocular depth, neural-signal binding, super-resolution). They are left out as irrelevant to the hackathon.
- Baidu Baike credits him with **15 papers** in total (⚠️ unverified count).
- **Method note (affiliation scan):** 165 arXiv papers submitted since June 2024 by Hesheng Wang and by the UniTac co-author group were pulled from the arXiv listing and their full text checked for a UniX AI affiliation or product name. SCAN_RESULT_PLACEHOLDER

## Datasets, models and benchmarks released

**Company releases: none.** Everything below is an academic release by the founder or his co-authors. None of it controls a UniX robot.

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| **Touch and Go** | Dataset: paired egocentric RGB video + GelSight tactile video, material labels on touch-onset frames | CC BY 4.0 (per project page) | [Project page with download](https://touch-and-go.github.io/) | Training or testing a material classifier from touch or from vision; widely reused as a tactile pre-training corpus |
| Touch and Go code | PyTorch code: visuo-tactile contrastive learning, tactile-driven image stylisation | No licence file found | [fredfyyang/Touch-and-Go](https://github.com/fredfyyang/Touch-and-Go) | Reference baselines only |
| **UniTouch** code | Touch encoder loading, touch QA, touch-to-image scripts (built on ImageBind and LLaMA-Adapter) | No licence file found in the repo ⚠️ | [cfeng16/UniTouch](https://github.com/cfeng16/UniTouch) | Zero-shot material / property recognition from GelSight-type images; touch embeddings (1024-d) for retrieval |
| **Touch-LLM / UniTouch weights** | Pretrained touch encoder checkpoint + LLaMA-Adapter 7B weights | MIT (Hugging Face tag) | [chfeng/Touch-LLM](https://huggingface.co/chfeng/Touch-LLM) | Running UniTouch without training |
| **TaRF** dataset + code + checkpoints | 13 captured scenes (images, camera poses, touch), Nerfstudio plugin, image-to-touch diffusion model | No licence file found ⚠️ | [Dou-Yiming/TaRF](https://github.com/Dou-Yiming/TaRF) | Estimating touch from an RGB-D view; research only |
| Generating Visual Scenes from Touch code | Code repository linked from the project page (contents not inspected) | not stated | [fredfyyang/vision-from-touch](https://github.com/fredfyyang/vision-from-touch) | Touch-image synthesis research |
| TextToucher code | PyTorch implementation of text-to-touch generation | Apache-2.0 | [TtuHamg/TextToucher](https://github.com/TtuHamg/TextToucher) | Synthetic tactile data generation |
| DTWM code | Implementation of the tactile-conditioned video world model | Apache-2.0 | [Adonis-galaxy/Dexterous-Tactile-World-Model](https://github.com/Adonis-galaxy/Dexterous-Tactile-World-Model) | World-model research; needs large GPU budget, not a 48-hour tool |
| UniTac model | — | — | not released (no link on arXiv as of 2026-11-14) | — |
| UniFlex / UniCortex / product UniTouch | — | — | **not public** | — |
| Robot datasets, URDF / MJCF, benchmarks from UniX deployments | — | — | **not public** | — |

## Third-party papers using their hardware or software

**Hardware: no third-party paper using a Wanda, Panther, Martian or UniPicker was found** (two web searches, an arXiv catalogue query for the company and product names, and the affiliation scan above). This matches the closed developer posture described in the [developer guide](UniX-AI-Developer-Guide.md).

The table therefore lists independent work that builds on the **founder's open academic datasets and models** — the only UniX-related assets outsiders can actually use.

| Paper | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| [Where to Generate Touch: Do Image Latents Preserve Material Recognition?](https://arxiv.org/abs/2611.15834) | Wanghao Ye, Aarosh Das, Sihan Chen and 26 co-authors, last author Ang Li | arXiv preprint, Nov 2026 | **Touch and Go** dataset (with ObjectFolder Real, YCB-Slide) | Material classifiers trained on real GelSight presses survive Stable-Diffusion-VAE reconstruction almost unchanged but lose accuracy with 16x discrete tokenizers — guidance for choosing a latent space for generated touch | T03 |
| [The Potential of Haptic Foundation Models](https://arxiv.org/abs/2608.28664) | Jianquan Wang, Haiwei Dong, Abdulmotaleb El Saddik | IEEE Consumer Electronics Magazine (accepted), 2026 | **UniTouch** model, benchmarked with AnyTouch, T3 and Sparsh on TacBench | Side-by-side comparison of tactile foundation models on force estimation, slip detection and relative pose; useful overview of where UniTouch stands | T04 |
| [Towards Generalization of Tactile Image Generation: Reference-Free Evaluation in a Leakage-Free Setting](https://arxiv.org/abs/2503.06860) | Cagri Gungor, Derek Eppinger, Adriana Kovashka | arXiv preprint, Mar 2025 | **Touch and Go** dataset (with HCT) | Shows train/test overlap inflates reported tactile-generation scores on common datasets; proposes a leakage-free split and reference-free metrics | — |
| [AnyTouch: Learning Unified Static-Dynamic Representation across Multiple Visuo-tactile Sensors](https://arxiv.org/abs/2502.12191) | Ruoxuan Feng, Jiangyu Hu, Wenke Xia, Tianci Gao, Ao Shen, Yuhao Sun, Bin Fang, Di Hu | ICLR 2025 | **Touch and Go** as one of its training datasets; **UniTouch** as a compared baseline | A newer multi-sensor tactile encoder; UniTac (above) uses the AnyTouch encoder and data organisation, so the lineage runs Touch and Go → UniTouch → AnyTouch → UniTac | T03 T04 |

## Reading list by track

**Read this caveat first:** every paper here assumes a **vision-based tactile sensor** (GelSight, DIGIT or similar). UniX robots are not documented as carrying one. These papers help only if (a) a team mounts its own tactile sensor on a gripper, or (b) you use the ideas for vision-only material / property reasoning. For actually commanding a UniX robot, the papers do not help — the booth engineers do.

### T01 Autonomous Urban Services

- [UniTac](https://arxiv.org/abs/2606.31451) — the only paper with a UniX AI affiliation; its towel-selection and cup-grasp experiments are the closest published thing to the housekeeping and tea-service skills the company demos (T01.2, T01.3). Read sections 4.5 and appendix B.1 for the task definitions and success criteria.
- No directly relevant paper found for navigation, guidance, delivery or public-space interaction (T01.1, T01.4–T01.7). UniX's key-point imitation learning (UniFlex), which is what powers its hotel skills, is unpublished.

### T02 Resilient & Safe City

- No directly relevant paper found.
- Closest, as background only: [Touch and Go](https://arxiv.org/abs/2211.12498) (surface-material recognition from touch could support T02.3 infrastructure checks) and [TaRF](https://arxiv.org/abs/2405.04534) (predicting surface feel across a scanned scene). Neither is practical in 48 hours.

### T03 Sustainable City

- [Binding Touch to Everything (UniTouch)](https://arxiv.org/abs/2401.18084) — zero-shot material classification with released weights; the fastest route to a "sort by material, not by looks" demo for T03.1 / T03.6 **if you have a GelSight-type sensor**.
- [Touch and Go](https://arxiv.org/abs/2211.12498) — CC BY 4.0 data with material labels; usable to train or sanity-check a small material classifier (also vision-only, from the paired RGB frames).
- [AnyTouch](https://arxiv.org/abs/2502.12191) — third-party successor encoder that covers more sensors; check it before committing to UniTouch.
- [Where to Generate Touch](https://arxiv.org/abs/2611.15834) — only if you plan to augment scarce tactile data synthetically.

### T04 Elderly Care & Rehabilitation

- [UniTac](https://arxiv.org/abs/2606.31451) — tactile reasoning for **skin-safe material choice** (softer towel) and **force-aware grasping of deformable cups**: direct inspiration for gentle handling in T04.1 / T04.2 / T04.6. Shows that even touch *predicted from RGB* improves a π0.5-style policy.
- [Binding Touch to Everything (UniTouch)](https://arxiv.org/abs/2401.18084) — grasp-stability prediction and touch question answering; a ready-made "is this grip secure?" check before handing an object to a person.
- [The Potential of Haptic Foundation Models](https://arxiv.org/abs/2608.28664) — short survey with a benchmark on force, slip and pose; good for picking a tactile model for safe physical assistance.
- [Dexterous Tactile World Model](https://arxiv.org/abs/2609.34286) — background on why force history predicts what a hand does next (relevant to T04.3 rehab-glove ideas); too heavy to train during the event.

## White papers, patents and technical reports

- **White papers / technical reports: none published** by UniX AI (company site and sitemap checked: product, application, recruitment and news-photo pages only; no research or technology section).
- **Patents: not checked** — no patent database was queried for this document. ⚠️ unverified
- **Closest thing to a technical description of the product stack** is the founder's interview with 36Kr (English version on KrASIA, 15 Sep 2025). Claims from that interview (company statements, not peer-reviewed):

| Component | What the founder says |
|---|---|
| **UniFlex** | Perception and manipulation are decoupled; actions are broken into **key points + motion trajectories** and learned by imitation; related in spirit to movement primitives (DMP / VMP); a new task from **5–10 demonstrations**; demonstrations captured with **VR teleoperation** (a door-closing skill was re-recorded and retrained overnight at the World Humanoid Robot Games) |
| **Why not VLA** | End-to-end vision-language-action models judged impractical for now because robot data is scarce; long-term he expects VLA to win |
| **UniTouch (product)** | Vision-tactile fusion fed into the key-point framework rather than a single latent vector; lets the robot estimate how an object should feel from vision alone |
| **Tactile hardware** | **Not fitted on the robots as of Sep 2025** — cost (about RMB 6,000–8,000 per finger sensor), durability and bulk cited |
| **Data strategy** | Deploy robots in hotels first, collect naturally distributed data from real work, improve models through a data flywheel |

- Practical takeaway for teams: if the booth allows skill teaching, the published claim to test is "5–10 VR demonstrations per new skill" — ask for exactly that workflow.

## Sources

- [arXiv 2606.31451 — UniTac (abstract)](https://arxiv.org/abs/2606.31451) · [full text with affiliations](https://arxiv.org/html/2606.31451)
- [arXiv 2609.34286 — Dexterous Tactile World Model](https://arxiv.org/abs/2609.34286) · [project page](https://adonis-galaxy.github.io/dtwm-project-page/) · [code](https://github.com/Adonis-galaxy/Dexterous-Tactile-World-Model)
- [arXiv 2409.05427 — TextToucher](https://arxiv.org/abs/2409.05427) · [code](https://github.com/TtuHamg/TextToucher)
- [arXiv 2405.04534 — Tactile-Augmented Radiance Fields](https://arxiv.org/abs/2405.04534) · [code](https://github.com/Dou-Yiming/TaRF)
- [arXiv 2401.18084 — Binding Touch to Everything (UniTouch)](https://arxiv.org/abs/2401.18084) · [project page](https://cfeng16.github.io/UniTouch/) · [code](https://github.com/cfeng16/UniTouch) · [weights on Hugging Face](https://huggingface.co/chfeng/Touch-LLM)
- [arXiv 2309.15117 — Generating Visual Scenes from Touch](https://arxiv.org/abs/2309.15117) · [project page](https://fredfyyang.github.io/vision-from-touch/)
- [arXiv 2211.12498 — Touch and Go](https://arxiv.org/abs/2211.12498) · [project page and dataset](https://touch-and-go.github.io/) · [code](https://github.com/fredfyyang/Touch-and-Go)
- [arXiv 2502.12191 — AnyTouch](https://arxiv.org/abs/2502.12191)
- [arXiv 2503.06860 — Towards Generalization of Tactile Image Generation](https://arxiv.org/abs/2503.06860)
- [arXiv 2608.28664 — The Potential of Haptic Foundation Models](https://arxiv.org/abs/2608.28664)
- [arXiv 2611.15834 — Where to Generate Touch](https://arxiv.org/abs/2611.15834)
- [KrASIA / 36Kr interview with Yang Fengyu, 15 Sep 2025](https://kr-asia.com/hotels-may-be-the-first-stop-for-humanoid-robots-says-unix-ai-founder)
- [Baidu Baike (English): Yang Fengyu](https://baike.baidu.com/en/item/Yang%20Fengyu/3313801)
- [About UniX AI (company timeline, algorithm stack names)](https://www.unix-group.ai/About-Unix-AI)
- [UniX AI sitemap](https://www.unix-group.ai/sitemap.xml)
- [GitHub organisation UniX-AI-Lab (unrelated name-alike, checked to rule it out)](https://github.com/UniX-AI-Lab) · [arXiv 2605.10434 — WorldReasonBench](https://arxiv.org/abs/2605.10434) · [arXiv 2608.16320 — StreamOPD](https://arxiv.org/abs/2608.16320)
- [UniX AI profile (this repository)](UniX-AI.md) · [Developer guide (this repository)](UniX-AI-Developer-Guide.md)
