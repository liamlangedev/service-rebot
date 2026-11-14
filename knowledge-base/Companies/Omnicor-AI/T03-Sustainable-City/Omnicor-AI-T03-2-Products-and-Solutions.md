---
type: challenge-products
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, products]
---
# Omnicor AI × T03 — Products and Solutions

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T03-1-Brief.md) · [Playbook](Omnicor-AI-T03-3-Playbook.md)

**Read this first:** Omnicor AI (written "OmniCor AI" on its site) publishes a single one-page website with headings only. There are **no specs, prices, docs, SDK or case studies**. Every capability below is "ask on site". Nothing on the site addresses sustainability, waste, energy management or environmental monitoring directly; the T03 link is **lower energy per inference** and **cloud-free operation**.

Research note: general web search was unavailable for this pass; findings rest on the official site (re-read 2026-11-14) and the official pages of the open-source projects listed under Sources.

## Relevant products (ranked for this track)

### Model optimisation

- **Role in T03:** the only item that maps onto a sustainability metric. Shrinking or accelerating a model so it fits a power, latency and memory budget means fewer joules per decision, smaller batteries or longer runtime per charge.
- **Status:** ⚠️ unverified (listed on site, no description) · **Price:** not public · **Availability:** by contact ("tell us about your model and your target hardware").

| Track-relevant spec | Value |
|---|---|
| Techniques used (quantisation, pruning, distillation, compilation) | Not public |
| Energy or speed gain achieved | Not public |
| Models named on site | Apertus, Mistral AI, Open Euro LLM, Qwen, DeepSeek, OpenVLA, pi0.5 (LeRobot), "and others" |
| Target silicon (ecosystem logos) | Qualcomm, NVIDIA, AMD |
| Turnaround for a new model | Not public |

- **Developer interface:** none published. Service-style engagement: you hand over a trained model and a target device; they return a deployment. What you can tune yourself is unknown.

### OC Node

- **Role in T03:** a compute box to bolt onto a robot or sorting station so inference runs locally at low power instead of on a GPU workstation or in the cloud.
- **Status:** ⚠️ unverified (site says "compute platform designed in-house"; no photo, no datasheet) · **Price:** not public · **Availability:** not public; on-site presence unconfirmed.

| Track-relevant spec | Value |
|---|---|
| Chip / accelerator | Not public |
| Power draw (idle / load) | Not public |
| Memory, I/O (USB, Ethernet, CAN), supply voltage | Not public |
| Weight, size, IP rating, operating temperature | Not public |

- **Developer interface:** not public. Ask whether it runs standard Linux with ROS 2 and whether you get shell access.

### OC Agent

- **Role in T03:** described only as an "agentic deployment environment". Plausible reading (inference): an automated workflow that fits a model to a target chip. For T03 it matters only as the thing that makes porting fast enough for 48 hours.
- **Status:** ⚠️ unverified · **Price:** not public · **Availability:** not public; no sign-up, CLI or package found.

| Track-relevant spec | Value |
|---|---|
| Inputs / outputs, supported runtimes | Not public |
| Self-serve or operated by Omnicor staff | Not public |
| Reports energy or latency per model variant | Not public |

- **Developer interface:** not public.

### European delivery

- **Role in T03:** marginal. "Designed and built in Europe" could support a short-supply-chain or data-sovereignty argument in a pitch, but there is nothing to build with. No location, factory or volume is public. Status ⚠️ unverified.

## What Omnicor AI already does in this domain

**Nothing specific to sustainable-city applications is public.** No deployment, pilot, demo, partnership or application page for waste, recycling, energy, EV charging, environmental monitoring or urban farming was found.

Closest adjacent statements, all from the official site (2026, undated, no detail):

| Statement | T03 relevance | Source |
|---|---|---|
| Robot deployments must run on-board within the moving platform's power budget | Energy-efficient mobile robots | [omnicorai.io](https://www.omnicorai.io/) |
| Enterprise AI servers: throughput per watt drives operating cost | Efficiency of inference infrastructure | [omnicorai.io](https://www.omnicorai.io/) |
| L4 autonomous logistics vehicles: continuous multi-sensor inference under thermal limits | Resource-efficient logistics (indirect) | [omnicorai.io](https://www.omnicorai.io/) |
| Customer logos: AgiBot, Galbot, "sudo" | Possible existing path onto robots that are on site; scope not public | [omnicorai.io](https://www.omnicorai.io/) |

## What they are building next in this domain

- **Announced:** nothing. No roadmap, news or release notes exist publicly.
- **Inference only:** the site's positioning (European and open models, Qualcomm / NVIDIA / AMD silicon, own compute node, built in Europe) points to a sovereign, efficient edge-inference offering. Energy efficiency is a selling point in that pitch, not a product line. Do not expect sustainability-specific tooling.

## Software, models and data that help for this track

Omnicor publishes no code. These third-party open resources are what you would actually build with; the first four are models the Omnicor site names.

| Resource | What it gives you for T03 | Notes |
|---|---|---|
| [OpenVLA](https://github.com/openvla/openvla) | Open vision-language-action policy for pick / sort tasks | 7B-class model; code MIT, weights inherit Llama-2 terms. LoRA fine-tune needs a GPU with at least about **27 GB**; ships a REST server script (`deploy.py`) usable as off-board fallback |
| [LeRobot](https://github.com/huggingface/lerobot) (pi0.5, SmolVLA, ACT) | Record demos, train and run policies with `lerobot-record` / `lerobot-train` | Apache-2.0. ACT or SmolVLA are the realistic choices to train inside 48 h |
| [openpi](https://github.com/Physical-Intelligence/openpi) | Reference code and checkpoints for the pi0 family | Heavier; use only if a checkpoint already fits your robot |
| [Apertus 8B](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509) | Swiss open LLM for an offline, multilingual operator or resident interface | Apache-2.0; quantised community builds exist for local runtimes |
| [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) | Small detectors (smallest YOLO26 model about **2.4M** parameters) with ONNX / TensorRT export | AGPL-3.0; a strong low-power baseline for waste or litter detection |
| [TACO](https://github.com/pedropro/TACO) and [TrashNet](https://github.com/garythung/trashnet) | Open litter and waste-category image datasets | Check licences and class lists before training |
| [CodeCarbon](https://github.com/mlco2/codecarbon) | Estimates energy and CO2 of compute from CPU / GPU / RAM use | MIT. Pair with a wall-plug meter for a number judges trust |

## Gaps and limits for this track

- **No robot, sensor or actuator.** Every T03 build needs another vendor's hardware.
- **No public numbers.** No watts, tokens per second, control rate or energy savings to quote; you must measure on site.
- **No self-serve tooling.** Without Omnicor staff time, there is no Omnicor contribution.
- **Indirect impact.** Inference is usually a small share of a robot's energy use next to motors; an honest pitch must say so or pick a task where compute dominates (static sorting station, always-on monitoring).
- **Unknown on-site kit.** OC Node presence, quantity and supported robots are unconfirmed.
- **Licensing detail.** OpenVLA weights and AGPL detectors carry conditions; fine for a hackathon, relevant afterwards.

## Sources

- [OmniCor AI official website](https://www.omnicorai.io/)
- [OpenVLA (GitHub)](https://github.com/openvla/openvla)
- [LeRobot (GitHub)](https://github.com/huggingface/lerobot)
- [openpi (GitHub)](https://github.com/Physical-Intelligence/openpi)
- [Apertus-8B-Instruct-2509 model card (Hugging Face)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [Ultralytics YOLO (GitHub)](https://github.com/ultralytics/ultralytics)
- [TACO dataset (GitHub)](https://github.com/pedropro/TACO)
- [TrashNet dataset (GitHub)](https://github.com/garythung/trashnet)
- [CodeCarbon (GitHub)](https://github.com/mlco2/codecarbon)
