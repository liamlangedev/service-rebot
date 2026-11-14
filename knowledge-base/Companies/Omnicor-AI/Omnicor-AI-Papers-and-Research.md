---
type: papers
company: "Omnicor AI"
slug: Omnicor-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, papers]
---
# Omnicor AI — Papers and Research

⬆ [Omnicor AI profile](Omnicor-AI.md) · [Solutions and projects](Omnicor-AI-Solutions-and-Projects.md) · [Developer guide](Omnicor-AI-Developer-Guide.md)

> **Bottom line:** OmniCor AI has **no public research output** as of 2026-11-14 — **0 papers, 0 datasets, 0 models, 0 benchmarks, 0 repositories**. The only research worth reading in connection with it is the third-party work behind the open models its website says it deploys (OpenVLA, pi0.5, Apertus, Qwen, DeepSeek, Mistral). Those papers are listed separately below and are clearly **not** OmniCor work.

## Research footprint

- **Not research-driven in public.** The company presents itself as an edge-AI *deployment* business (OC Agent, OC Node, model optimisation). Its one-page website has no research, technology, blog, news or publications section; the site script bundle contains no link to arXiv, GitHub, Hugging Face or any paper.
- **Key people and labs: not public.** No founder, CTO or scientific advisor is named on the site, so no author search was possible. Names seen earlier in LinkedIn search snippets (Margueritta Chen, Philippe Chen) are ⚠️ unverified and were **not** used to attribute any paper. No university lab affiliation is stated anywhere.
- **Open-source posture: none so far.** GitHub account [`OmnicorAI`](https://github.com/OmnicorAI) was created **2026-09-30** and has **0 public repositories** (ownership ⚠️ unverified). No Hugging Face organisation exists under `OmnicorAI`, `omnicor-ai`, `omnicorai`, `OmniCor` or `OmniCorAI` (all return "not found").
- **What it builds on is fully open and well documented.** Every model on its "models we deploy" list has a public paper and public weights, so teams can read and reproduce the baseline without OmniCor.
- **Search status for this doc:** web search **was available** (1 extended query, the full allowance). It returned only the company homepage plus unrelated "OmniCore" namesakes. Additional direct checks: company site and script bundle, GitHub API, Hugging Face, and an arXiv full-text query for "OmniCor" (**0 results**). All papers listed below were opened on arXiv and the metadata taken from there.

## Company-authored and company-affiliated papers

**None found.** No paper, technical report or preprint authored by OmniCor AI, its (unnamed) founders or an affiliated lab could be identified.

| Paper (title as a link) | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts (code / weights / data links) | Tracks |
|---|---|---|---|---|---|
| — none found — | — | — | — | — | — |

What was checked: official site (all six language versions live in one script bundle), GitHub account, Hugging Face org names, arXiv search on the company name, one extended web search. LinkedIn is not readable without login, so staff-level publication lists could not be checked ⚠️ unverified.

## Datasets, models and benchmarks released

**None.** OmniCor AI has not published any dataset, model checkpoint, benchmark, latency table or optimisation toolkit.

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| — none released — | — | — | — | — |

Third-party artifacts you can use instead (the same models the site lists):

| Name | Type | Licence | Link | Useful for |
|---|---|---|---|---|
| OpenVLA (`openvla-7b`) | VLA checkpoint + training code | Code MIT; weights inherit Llama-2 licence terms | [repo](https://github.com/openvla/openvla) | Single-arm manipulation baseline; has a ready REST inference server |
| OpenVLA-OFT | Fine-tuning recipe + checkpoints | See project page | [project page](https://openvla-oft.github.io/) | Faster, chunked, bimanual-capable OpenVLA fine-tunes |
| pi0.5 in LeRobot (`lerobot/pi05_base`) | VLA checkpoint | LeRobot docs: Apache 2.0; weights card tagged `gemma` | [model card](https://huggingface.co/lerobot/pi05_base) · [docs](https://huggingface.co/docs/lerobot/pi05) | Household / mobile-manipulation policies |
| openpi | Reference code for pi0 / pi0.5 | See repo | [repo](https://github.com/Physical-Intelligence/openpi) | Original implementation and checkpoints |
| SmolVLA (in LeRobot) | Small VLA + code + data | Apache 2.0 (LeRobot) | [repo](https://github.com/huggingface/lerobot) | VLA that runs on consumer GPU or CPU |
| Apertus 8B / 70B and small v1.1 variants | Open multilingual LLM | Apache 2.0 | [swiss-ai on Hugging Face](https://huggingface.co/swiss-ai) | Offline assistant in German / French / Italian / Romansh |
| BitVLA | 1-bit VLA code + weights | See repo | [code](https://github.com/ustcwhy/BitVLA) · [weights](https://huggingface.co/lxsy/bitvla-bf16) | Memory-constrained on-robot inference |
| EdgeVLA (EVLA) | Small VLA code + checkpoints | See repo | [code](https://github.com/kscalelabs/evla) | Edge-device VLA inference |

## Third-party papers using their hardware or software

**None found.** No paper mentions OC Agent, OC Node or OmniCor AI as hardware, software or deployment partner. The customer logos on the site (AgiBot, Galbot, "sudo") are OmniCor's own claim; no publication from those companies references it.

| Paper (link) | Authors / organisation | Venue, year | Hardware / software used | What it shows | Tracks |
|---|---|---|---|---|---|
| — none found — | — | — | — | — | — |

For research by the two listed customers that are on site, see [AGIBOT papers and research](../AGIBOT/AGIBOT-Papers-and-Research.md) and the [Galbot profile](../Galbot/Galbot.md).

### Background reading — papers behind the models OmniCor says it deploys (NOT OmniCor work)

All entries verified on arXiv on 2026-11-14. Listed newest first. OmniCor is not an author, sponsor or named user in any of them.

| Paper (link) | Authors / organisation | Venue, year | What it contributes (one line) | Artifacts | Tracks |
|---|---|---|---|---|---|
| [Apertus: Democratizing Open and Compliant LLMs for Global Language Environments](https://arxiv.org/abs/2509.14233) | Project Apertus (A. Hernández-Cano … I. Schlag; 100+ authors; Swiss AI Initiative, EPFL / ETH Zurich / CSCS) | arXiv, 2025 | Fully open LLM at **8B and 70B**, trained on **15T tokens** from **1,800+ languages** (about 40% non-English), compliance-filtered data, anti-memorisation objective | [weights](https://huggingface.co/swiss-ai) | T01 T02 T04 |
| [Real-Time Execution of Action Chunking Flow Policies](https://arxiv.org/abs/2506.07339) | K. Black, M. Y. Galliker, S. Levine (Physical Intelligence) | NeurIPS 2025 | Real-time chunking (RTC): next action chunk is generated while the current one executes; works on any flow / diffusion VLA **without retraining**; robust to inference delay | [project page](https://pi.website/research/real_time_chunking) | T01 T04 |
| [BitVLA: 1-bit Vision-Language-Action Models for Robotics Manipulation](https://arxiv.org/abs/2506.07530) | H. Wang, C. Xiong, R. Wang, X. Chen | arXiv, 2025 | Ternary-weight VLA that matches OpenVLA-OFT while cutting memory **11.0x** and end-to-end latency **4.4x** | [code](https://github.com/ustcwhy/BitVLA) · [weights](https://huggingface.co/lxsy/bitvla-bf16) | T03 |
| [SmolVLA: A Vision-Language-Action Model for Affordable and Efficient Robotics](https://arxiv.org/abs/2506.01844) | M. Shukor, D. Aubakirova, F. Capuano … R. Cadene (Hugging Face) | arXiv, 2025 | Compact VLA trainable on one GPU and deployable on consumer GPU or CPU; asynchronous inference stack; comparable to VLAs **10x larger** | [code](https://github.com/huggingface/lerobot) | T01 T03 T04 |
| [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) | A. Yang … Z. Qiu (Qwen team, Alibaba; 60 authors) | arXiv, 2025 | LLM family from **0.6B to 235B** parameters, thinking / non-thinking modes with a thinking budget, **119 languages**, Apache 2.0 | — | T01 T02 T04 |
| [pi0.5: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | Physical Intelligence (K. Black, N. Brown … U. Zhilinsky) | arXiv, 2025 | Co-training on multi-robot, web and semantic-subtask data; long-horizon tasks such as cleaning a kitchen or bedroom in **previously unseen homes** | [LeRobot weights](https://huggingface.co/lerobot/pi05_base) · [openpi](https://github.com/Physical-Intelligence/openpi) | T01 T04 |
| [Fine-Tuning Vision-Language-Action Models: Optimizing Speed and Success](https://arxiv.org/abs/2502.19645) | M. J. Kim, C. Finn, P. Liang (Stanford) | RSS 2025 | OpenVLA-OFT recipe (parallel decoding, action chunking, continuous actions, L1 loss): LIBERO success **76.5% → 97.1%**, action throughput **26x** | [project page](https://openvla-oft.github.io/) | T01 T04 |
| [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) | DeepSeek-AI (D. Guo … Z. Zhang) | Nature 645, 633–638 (2025) | Reasoning LLM trained with reinforcement learning; basis of the distilled small reasoning models often used on edge devices | — | — |
| [FAST: Efficient Action Tokenization for Vision-Language-Action Models](https://arxiv.org/abs/2501.09747) | K. Pertsch, K. Stachowicz, B. Ichter … S. Levine (Physical Intelligence) | arXiv, 2025 | DCT-based action tokeniser for high-frequency dexterous data; training up to **5x** faster with pi0 | [project page](https://www.pi.website/research/fast) | — |
| [pi0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164) | K. Black, N. Brown, D. Driess … U. Zhilinsky (Physical Intelligence) | RSS 2025 | Flow-matching VLA on a pretrained VLM; predecessor of pi0.5 | [openpi](https://github.com/Physical-Intelligence/openpi) | T01 T04 |
| [TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation](https://arxiv.org/abs/2409.12514) | J. Wen, Y. Zhu, J. Li … J. Tang | arXiv, 2024 | Compact VLA with a diffusion decoder; faster and more data-efficient than OpenVLA, no pre-training stage | [project page](https://tiny-vla.github.io) | T03 |
| [EdgeVLA: Efficient Vision-Language-Action Models](https://arxiv.org/abs/2507.14049) | P. Budzianowski, W. Maa, M. Freed … B. Bolte (K-Scale Labs) | IROS MoMA3 workshop 2024 (arXiv 2025) | Non-autoregressive end-effector prediction (**7x** faster inference) plus a small language model for edge devices | [code](https://github.com/kscalelabs/evla) | T02 T03 |
| [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246) | M. J. Kim, K. Pertsch, S. Karamcheti … C. Finn (Stanford, UC Berkeley, TRI, Google DeepMind and others) | arXiv, 2024 | **7B**-parameter open VLA trained on **970k** real robot demos; LoRA fine-tuning on consumer GPUs; **quantised serving without loss of success rate** | [code](https://github.com/openvla/openvla) · [project page](https://openvla.github.io/) | T01 T04 |
| [Mistral 7B](https://arxiv.org/abs/2310.06825) | A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford and others (Mistral AI) | arXiv, 2023 | The original 7B open LLM from Mistral AI; a common small-model baseline for local inference | — | — |
| [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864) | Open X-Embodiment Collaboration (290+ authors) | arXiv, 2023 | The pooled multi-robot dataset that OpenVLA is trained on | [project page](https://robotics-transformer-x.github.io) | — |

No paper was found for OpenEuroLLM (also on the site's model list) — not listed.

## Reading list by track

OmniCor has no papers of its own, so every item below is third-party background for the kind of work you would bring to its table: **running an open model on-board, offline, inside a power and memory budget**.

### T01 Autonomous Urban Services
- [OpenVLA](https://arxiv.org/abs/2406.09246) — the baseline for language-conditioned pick / place / hand-over; its quantisation result is the evidence that quantised serving can keep success rate (T01.1, T01.3).
- [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) — if OpenVLA is too slow on your robot, this recipe gives 26x throughput with chunked actions (T01.3).
- [Real-time chunking](https://arxiv.org/abs/2506.07339) — how to keep motion smooth when on-board inference is slower than the control loop; no retraining needed (T01.6, T01.7).
- [Apertus](https://arxiv.org/abs/2509.14233) and [Qwen3](https://arxiv.org/abs/2505.09388) — local multilingual LLMs for a guidance / information robot without cloud access (T01.5).
- [SmolVLA](https://arxiv.org/abs/2506.01844) — realistic to fine-tune inside 48 h on one GPU.

### T02 Resilient & Safe City
- **No directly relevant paper found** (nothing from OmniCor; none of the model papers targets rescue, inspection or security).
- Closest useful background for the "works when the network is down" argument (T02.4, T02.7): [EdgeVLA](https://arxiv.org/abs/2507.14049) for fast edge inference, and [Qwen3](https://arxiv.org/abs/2505.09388) (0.6B-class models) or [Apertus](https://arxiv.org/abs/2509.14233) for an offline multilingual operator assistant.

### T03 Sustainable City
- [BitVLA](https://arxiv.org/abs/2506.07530) — hard numbers (11x less memory, 4.4x lower latency) for an energy-efficient-inference pitch (T03.3).
- [SmolVLA](https://arxiv.org/abs/2506.01844) — a VLA that runs on CPU / consumer GPU; a small sorting policy is feasible in a weekend (T03.1, T03.3).
- [EdgeVLA](https://arxiv.org/abs/2507.14049) and [TinyVLA](https://arxiv.org/abs/2409.12514) — design choices that cut compute per action (T03.3).
- No paper on waste, water or environmental monitoring is connected to OmniCor.

### T04 Elderly Care & Rehabilitation
- [pi0.5](https://arxiv.org/abs/2504.16054) — the most relevant: household tasks in homes never seen in training (T04.1, T04.6).
- [Apertus](https://arxiv.org/abs/2509.14233) — open, compliance-oriented Swiss LLM; the argument for a private on-device assistant in local languages where no patient data leaves the room (T04.5, T04.7).
- [Real-time chunking](https://arxiv.org/abs/2506.07339) — smoother motion near people when inference is slow (T04.2).
- [OpenVLA-OFT](https://arxiv.org/abs/2502.19645) — bimanual, high-frequency fine-tuning recipe for assistive manipulation (T04.1).
- [SmolVLA](https://arxiv.org/abs/2506.01844) — lightest path to a working fetch-and-hand-over demo.

## White papers, patents and technical reports

None found. No white paper, benchmark report, datasheet or patent could be attributed to OmniCor AI. A patent search by company name was not possible within this pass ⚠️ unverified.

## Sources

- [OmniCor AI official website](https://www.omnicorai.io/) (page and script bundle; no research section, no outbound research links)
- [OmnicorAI account on GitHub](https://github.com/OmnicorAI) (created 2026-09-30, 0 public repositories; ownership unverified)
- [Omnicor AI on LinkedIn](https://www.linkedin.com/company/omnicor-ai/) (not readable without login; nothing taken from it)
- [arXiv 2509.14233 — Apertus](https://arxiv.org/abs/2509.14233)
- [arXiv 2506.07339 — Real-Time Execution of Action Chunking Flow Policies](https://arxiv.org/abs/2506.07339)
- [arXiv 2506.07530 — BitVLA](https://arxiv.org/abs/2506.07530)
- [arXiv 2506.01844 — SmolVLA](https://arxiv.org/abs/2506.01844)
- [arXiv 2505.09388 — Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)
- [arXiv 2504.16054 — pi0.5](https://arxiv.org/abs/2504.16054)
- [arXiv 2502.19645 — OpenVLA-OFT](https://arxiv.org/abs/2502.19645)
- [arXiv 2501.12948 — DeepSeek-R1](https://arxiv.org/abs/2501.12948)
- [arXiv 2501.09747 — FAST](https://arxiv.org/abs/2501.09747)
- [arXiv 2410.24164 — pi0](https://arxiv.org/abs/2410.24164)
- [arXiv 2409.12514 — TinyVLA](https://arxiv.org/abs/2409.12514)
- [arXiv 2507.14049 — EdgeVLA](https://arxiv.org/abs/2507.14049)
- [arXiv 2406.09246 — OpenVLA](https://arxiv.org/abs/2406.09246)
- [arXiv 2310.06825 — Mistral 7B](https://arxiv.org/abs/2310.06825)
- [arXiv 2310.08864 — Open X-Embodiment](https://arxiv.org/abs/2310.08864)
- [OpenVLA repository](https://github.com/openvla/openvla) · [LeRobot pi0.5 docs](https://huggingface.co/docs/lerobot/pi05) · [pi05_base model card](https://huggingface.co/lerobot/pi05_base) · [swiss-ai on Hugging Face](https://huggingface.co/swiss-ai) (licence and artifact details, as verified in the company profile's verification log)
- [Omnicor AI profile in this vault](Omnicor-AI.md)
