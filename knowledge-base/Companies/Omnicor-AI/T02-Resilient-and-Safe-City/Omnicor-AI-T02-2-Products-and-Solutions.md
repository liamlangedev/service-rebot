---
type: challenge-products
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, products]
---
# Omnicor AI × T02 — Products and Solutions

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T02-1-Brief.md) · [Playbook](Omnicor-AI-T02-3-Playbook.md)

> **Read this first.** OmniCor AI publishes a one-page website with headings only. There are **no specs, prices, docs, SDK or case studies** for any product, and nothing specific to safety, inspection or emergency response. Every table below therefore says "not public" where a number would normally be. Treat this page as a list of what to verify at the booth, not as a datasheet.
> Research note: the track-specific web search could not be run (search budget exhausted); findings rest on the official site, re-read on 2026-11-14, plus the company profile.

**Role in T02 in one line:** the on-device inference layer — it makes a detection model, a local LLM or a VLA run on the robot or sensor itself, so the system keeps working when the network does not.

## Relevant products (ranked for this track)

### OC Node

- **Role in T02:** the compute box that rides on a patrol robot or sits at a sensor mast and runs perception + language models with no backhaul. This is the most demo-able Omnicor item for a "resilient" story.
- **What the site says:** a compute platform designed in-house. Nothing more.

| Track-relevant spec | Value |
|---|---|
| Chip / accelerator | Not public (ecosystem logos on site: Qualcomm, NVIDIA, AMD — which one is inside OC Node is not stated) |
| Compute (TOPS / memory) | Not public |
| Power draw / supply voltage | Not public — decisive for battery-powered patrol robots |
| Operating temperature, IP rating, shock / vibration | Not public — decisive for outdoor alpine use in November |
| Interfaces (Ethernet, USB, CAN, camera inputs) | Not public |
| Weight / mounting | Not public |

- **Status / price / availability:** ⚠️ unverified (listed on the site; whether it ships, and whether units are in Leukerbad, is not confirmed). Price not public.
- **Developer interface:** not public. Assume nothing: ask whether you get a shell (Linux?), containers, a ROS 2 node, or only a model endpoint.

### OC Agent

- **Role in T02:** the tooling that fits your model to a target device. In a 48-hour build its value is speed: getting a detector, VLM or local LLM running on the robot's own computer (or an OC Node) without you hand-tuning quantisation and runtimes.
- **What the site says:** an agentic deployment environment. The contact form asks for "your model and your target hardware", which reads as a service-led workflow rather than a self-serve download.

| Track-relevant spec | Value |
|---|---|
| Supported target hardware | Not public (Qualcomm, NVIDIA, AMD shown as ecosystem) |
| Supported model types | Site lists LLMs (Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek) and VLAs (OpenVLA, pi0.5 via LeRobot), "and more". Classic vision detectors are not mentioned ⚠️ unverified |
| Time to port a model | Not public — the key question for a hackathon |
| Output (runtime, API, container) | Not public |

- **Status / price / availability:** ⚠️ unverified. Price not public. No public sign-up, docs or repository found.
- **Developer interface:** not public. Likely operated by, or together with, the Omnicor engineers on site (inference).

### Model optimisation

- **Role in T02:** shrinking a model to fit a power, latency and memory budget. For safety systems this buys longer battery patrols and faster reaction (detect → alert) on small hardware.
- **Specs:** no method, benchmark or speed-up figure is published.
- **Status / price / availability:** ⚠️ unverified service; price not public.
- **Developer interface:** you hand over a model; what comes back (format, accuracy report) is not public. Ask for before / after numbers you can show to judges.

### European delivery

- **Role in T02:** not a build component. It is a pitch argument: public-safety and critical-infrastructure buyers care about where hardware is designed and built, and the site states design and manufacturing in Europe.
- **Specs / status / price:** not public; ⚠️ unverified (no facility, location or certification named).

## What Omnicor AI already does in this domain

**Nothing found that is specific to T02.** No emergency-response, inspection, security-patrol, hazard-monitoring or digital-twin deployment, pilot, demo or partner has been published.

Adjacent facts from the official site (2026, undated):

| Item | Relevance to T02 | Source |
|---|---|---|
| Deployment domain "embodied AI robotics": perception and control that must run on-board a moving platform | Same constraint as a patrol or rescue robot without connectivity | [omnicorai.io](https://www.omnicorai.io/) |
| Deployment domain "L4 autonomous logistics vehicles": continuous multi-sensor inference under automotive thermal and reliability limits | Closest hint at ruggedised, always-on operation; no product or customer named | [omnicorai.io](https://www.omnicorai.io/) |
| Customers shown: AgiBot, Galbot, "sudo" | AgiBot and Galbot robots are on site; scope of the work is not public; "sudo" ⚠️ unverified | [omnicorai.io](https://www.omnicorai.io/) |
| Partner logo HUIXI; ecosystem logos Qualcomm, NVIDIA, AMD | Suggests which silicon they can target; HUIXI identity ⚠️ unverified | [omnicorai.io](https://www.omnicorai.io/) |

## What they are building next in this domain

- **Announced:** nothing. No roadmap, launch date or safety-related plan is public.
- **Inference (not a company statement):** the automotive-style wording (thermal and reliability constraints) and the in-house compute node point towards ruggedised edge compute, which would suit outdoor safety robots later. Do not present this as a plan.

## Software, models and data that help for this track

Omnicor publishes **no code, models or datasets** of its own. What shortcuts a 48-hour build are the third-party open models its site says it deploys:

| Asset | Useful for in T02 | Verified facts | Licence |
|---|---|---|---|
| **Apertus** (Swiss AI Initiative) | Local incident reports and voice / text Q&A for responders, offline, multilingual | **8B** and **70B** sizes; **1,811** natively supported languages; context up to **65,536** tokens | Apache-2.0 |
| **OpenVLA** | On-board manipulation policy (e.g. operate a switch or valve) on a mobile manipulator | `openvla-7b` checkpoint, about **7.5 B** parameters; LoRA fine-tuning needs roughly **27 GB+** GPU memory per the repo | Code MIT; weights carry Llama-2 community-licence terms |
| **pi0.5 in LeRobot** | Same role as OpenVLA with a maintained training / rollout toolchain | `pip install 'lerobot[pi]'`, `policy.type=pi05`; base checkpoints `lerobot/pi05_base`, `lerobot/pi05_libero_base`; example fine-tune sized for one **80 GB** GPU | Apache-2.0 per LeRobot docs; `lerobot/pi05_base` weights card tagged `gemma` |
| Mistral AI, Qwen, DeepSeek, OpenEuroLLM | Alternative local LLMs / VLMs | Named on the Omnicor site only; sizes and variants supported by Omnicor not public | Varies by model |

Practical notes:

- **Whether Omnicor has these models ready-to-run on hardware in the hall is ⚠️ unverified** — the site lists them as "models we deploy" without device, speed or accuracy figures.
- VLA fine-tuning needs data and a large GPU; inside 48 hours, treat VLAs as "use a pre-trained or vendor-provided policy" unless the team brings compute.
- For hazard detection (smoke, person down, blocked exit) a small vision model or a compact VLM is the realistic choice; ask whether OC Agent handles such models.

## Gaps and limits for this track

- **No robot, sensor, mapping, navigation or teleoperation product.** You must bring the body and the perception stack from another vendor.
- **No public developer access.** No SDK, API reference, repo, simulator or sample; you cannot prepare before talking to the team.
- **No environmental data** for OC Node (temperature, IP, shock) — an outdoor alpine claim cannot be backed with numbers.
- **No proof points in safety or inspection**, and no named deployments at all beyond three customer logos.
- **Service dependency.** If porting needs Omnicor engineers and they are shared across many teams, your critical path sits in someone else's queue.
- **Very small company (2–10 people per LinkedIn, ⚠️ unverified):** limited on-site support capacity is likely (inference).

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/) (single page; sections "Where our deployments run", "What we build", "Models we deploy", customers, partners)
- [Omnicor AI on LinkedIn](https://www.linkedin.com/company/omnicor-ai/) (company size; via profile research, page not readable without login)
- [OpenVLA GitHub repository](https://github.com/openvla/openvla)
- [Apertus-8B-Instruct-2509 model card (Hugging Face, swiss-ai)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [LeRobot documentation: pi0.5 policy](https://huggingface.co/docs/lerobot/pi05)
- [pi0.5 base model card in LeRobot (Hugging Face)](https://huggingface.co/lerobot/pi05_base)
