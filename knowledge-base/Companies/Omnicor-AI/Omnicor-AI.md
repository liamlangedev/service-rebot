---
type: company
company: "Omnicor AI"
slug: Omnicor-AI
hq: "not public (Europe; site says designed and built in Europe)"
founded: unknown
website: "https://www.omnicorai.io/"
categories: [software, compute]
on_site_guess: "Engineers plus an edge-deployment service/toolchain (OC Agent) and possibly an OC Node compute box, to get VLA / LLM models running on-board other vendors' robots"
fit_t01: 3
fit_t02: 3
fit_t03: 2
fit_t04: 3
identity_confidence: medium
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Omnicor AI

> **One-liner:** OmniCor AI is a very small European edge-AI deployment company: it takes a trained model (LLM, VLA) plus a target hardware platform and makes the model run on-device within power, speed and memory limits, using an agentic deployment environment (OC Agent) and an in-house compute platform (OC Node).
> **Why it matters at Leukerbad:** It is not a robot vendor but an enabler: if your idea needs a VLA or a language model running **on the robot** (no cloud, weak alpine connectivity, patient privacy), this is the team to ask. Its site lists **AgiBot** and **Galbot** — both on site — as teams shipping with it.

**Public information is very thin.** Everything below comes from a single one-page official website (no product pages, no specs, no docs, no prices) plus the LinkedIn company listing. Treat all capability detail as "ask on site".

## Snapshot

| Item | Detail |
|---|---|
| HQ | Not public. Site states "designed and built in Europe"; site is offered in Chinese, English, French, German, Spanish, Italian |
| Founded | Unknown (website copyright 2026) |
| Founders / CEO | Not public. People associated on LinkedIn per search snippets: Margueritta Chen, Philippe Chen (names and roles ⚠️ unverified; LinkedIn page not readable without login) |
| Size and funding | 2–10 employees (LinkedIn listing, ⚠️ unverified: page not readable without login). Funding: not public. A search snippet attributed a EUR 3.5M pre-seed to a related LinkedIn profile — ⚠️ unverified, no primary source found, do not rely on it |
| Core business | Deploying and optimising AI models on heterogeneous edge hardware: embodied-AI robots, L4 autonomous logistics vehicles, enterprise AI servers |
| Website | https://www.omnicorai.io/ (contact: contact@omnicorai.com) |
| Docs / developer portal | Not public (none found) |
| GitHub | No public code. A GitHub account [`OmnicorAI`](https://github.com/OmnicorAI) exists with **0 public repositories**; not linked from the official site, ownership ⚠️ unverified |

Name caveats: written "OmniCor AI" on its own site. Not ABB's OmniCore controller, not "OmniCore AI" (several unrelated firms), not Omnicor (South African assessment company), not omnicor.tech (unrelated "launching soon" placeholder).

## Portfolio at a glance

The website lists four "what we build" items, with headings only — no specs published.

| Product | Type | Status | Key specs | Price | Img key |
|---|---|---|---|---|---|
| OC Agent | Software — agentic deployment environment (automates fitting a model to target hardware) | ⚠️ unverified (listed on site, availability not stated) | Not public | Not public | omnicor-ai-oc-agent |
| OC Node | Hardware — compute platform designed in-house | ⚠️ unverified (listed on site, availability not stated) | Not public (chip, TOPS, power, I/O all unstated) | Not public | omnicor-ai-oc-node |
| Model optimisation | Service — optimising models for power / latency / memory budgets | ⚠️ unverified | Not public | Not public | omnicor-ai-model-optimization |
| European delivery | Service — design and manufacturing in Europe | ⚠️ unverified | Not public | Not public | omnicor-ai-europe-delivery |

**Models the site says it deploys:** Apertus (Swiss open LLM), Mistral AI, OpenEuroLLM, Qwen, DeepSeek, OpenVLA, pi0.5 (LeRobot), "and more".
**Silicon ecosystem logos:** Qualcomm, NVIDIA, AMD. **Partner logo:** HUIXI (most likely the Chinese automotive-chip company — ⚠️ unverified).

## What they will most likely bring to the hackathon

**Best guess, not confirmed:**

- **People, not robots.** A 2–10 person deployment company most plausibly brings engineers who help teams run models on-board hardware from other vendors.
- **Possibly OC Node units** as a plug-in compute box, and **OC Agent** access as the workflow for porting a model. Neither is confirmed; no public spec or SDK exists to prepare against.
- **Most natural pairing:** AgiBot and Galbot robots (both shown as customers on the OmniCor site), and NVIDIA / Qualcomm / AMD-based compute, e.g. Jetson-class boards.
- **Reasoning:** the site's first use case is embodied-AI robots where perception and control must run on-board within a mobile power budget, and the deployed-model list includes two robot VLAs (OpenVLA, pi0.5).

## Developer platform (summary)

- **SDK / languages:** not public. No docs portal, no GitHub org, no package names found.
- **Engagement model (from site):** you provide the trained model and the target hardware; they build the deployment to fit power, speed and memory limits. This reads as a service plus tooling, not a self-serve SDK.
- **Control level:** not a robot-control stack. It sits at the inference layer (model runtime / optimisation), under your policy and above the chip.
- **ROS 2:** not stated ⚠️ unverified.
- **Simulation assets, teleoperation, datasets:** none public.
- **Pretrained models:** no models of its own are published; it deploys third-party open models (Apertus, Mistral, OpenEuroLLM, Qwen, DeepSeek, OpenVLA, pi0.5).
- **On-board compute:** OC Node (in-house); also targets Qualcomm, NVIDIA and AMD platforms per the ecosystem logos.
- **Questions to ask on site:**
  1. What is physically here — OC Node units? How many, what chip, power draw, interfaces (USB / Ethernet / CAN)?
  2. Which robots on site already have a working OmniCor deployment (AgiBot? Galbot?) and which models?
  3. Inference rate and latency for OpenVLA / pi0.5 on your hardware?
  4. How long to port a new or fine-tuned model — hours or days? Can it be done inside 48 h?
  5. Is there a ROS 2 node or simple HTTP / gRPC API to call the model?
  6. Can a local LLM (Apertus, Mistral, Qwen) run fully offline with speech in German / French?

## Current projects, deployments and customers

- 2026 (website, undated): **AgiBot, Galbot and "sudo"** shown as teams shipping with OmniCor AI. Scope, products and volumes not public; identity of "sudo" ⚠️ unverified. [Source](https://www.omnicorai.io/)
- 2026 (website, undated): three stated deployment domains — embodied-AI robots, L4 autonomous logistics vehicles, enterprise (rack-side) AI servers. No named deployments or case studies. [Source](https://www.omnicorai.io/)
- 2026-11: the public Leukerbad Hackathon event page lists **"Omnicor AI"** among its hardware / development-platform providers (linked to the LinkedIn company page). What it brings is not stated. [Source](https://luma.com/vj13ns00)
- No press coverage or press releases found as of 2026-11-14.

## Roadmap and future direction

- Nothing announced publicly: no roadmap, launch dates, funding announcement or expansion plans found.
- Readable direction from the site (inference, not statement): a Europe-based delivery arm for edge AI that bridges Chinese robot makers and open models (including European ones such as Apertus, Mistral, OpenEuroLLM) with Qualcomm / NVIDIA / AMD silicon and its own compute node.

## Challenge fit

Scores reflect a supporting, multi-vendor role and the lack of public tooling; raise them by one if the team confirms hardware and a fast porting path on site.

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | On-board VLA / perception for delivery or service robots where mountain connectivity is patchy; needs another vendor's robot | OC Agent, OC Node | [T01 brief](T01-Autonomous-Urban-Services/Omnicor-AI-T01-1-Brief.md) |
| T02 Resilient & Safe City | 3 | Offline inference is the point when networks fail (avalanche, storm, tunnel); local detection on quadrupeds or sensors | OC Node, model optimisation | [T02 brief](T02-Resilient-and-Safe-City/Omnicor-AI-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Lower inference power per task is a real but indirect contribution; hard to demo as the core of a project | Model optimisation | [T03 brief](T03-Sustainable-City/Omnicor-AI-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | Private, on-device language and vision models (no patient data leaving the clinic), multilingual local LLMs incl. Swiss Apertus | OC Agent, OC Node | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Omnicor-AI-T04-1-Brief.md) |

## Related docs
- [Product portfolio](Omnicor-AI-Products.md) · [Developer guide](Omnicor-AI-Developer-Guide.md) · [Roadmap and strategy](Omnicor-AI-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Verification log (2026-11-14)

Fact-check pass over all 16 docs in this folder. General web search was unavailable in this pass (budget exhausted), so every check is a direct read of an official page. 20 claims checked: 12 confirmed, 5 corrected, 3 unverified.

- ✔ confirmed — Site lists exactly four offerings (OC Agent, OC Node, model optimisation, European delivery) with no specs, prices or docs. [omnicorai.io](https://www.omnicorai.io/)
- ✔ confirmed — "Models we deploy" logos: Apertus, Mistral AI, Open Euro LLM, Qwen, DeepSeek, OpenVLA, PI 0.5 (by LeRobot). [omnicorai.io](https://www.omnicorai.io/)
- ✔ confirmed — Customer logos AgiBot, Galbot and "sudo" are on the site. This is OmniCor's own claim only; nothing from AgiBot or Galbot confirms it. [omnicorai.io](https://www.omnicorai.io/#customers)
- ✔ confirmed — Partner logo HUIXI; ecosystem logos Qualcomm, NVIDIA, AMD (logos only, no chips named). [omnicorai.io](https://www.omnicorai.io/#partners)
- ⚠ unverified — Which company "HUIXI" is (logo has no link or description). [omnicorai.io](https://www.omnicorai.io/#partners)
- ✔ confirmed — Three deployment domains: embodied-AI robots, L4 autonomous logistics vehicles, enterprise AI servers. [omnicorai.io](https://www.omnicorai.io/)
- ✔ confirmed — Six site languages, page markup defaults to Chinese with location-based language pick, copyright 2026, contact@omnicorai.com. [omnicorai.io](https://www.omnicorai.io/)
- ✎ corrected — Profile said GitHub "none found"; a GitHub account `OmnicorAI` exists with 0 public repositories (ownership unverified), as the developer guide already stated. [github.com/OmnicorAI](https://github.com/OmnicorAI)
- ✎ corrected — Profile and roadmap said the public event page does not name Omnicor; it does list "Omnicor AI" among hardware / development-platform providers, linked to its LinkedIn page. [Luma event page](https://luma.com/vj13ns00)
- ⚠ unverified — LinkedIn details (2–10 employees, associated people). Page returns an error without login. [LinkedIn](https://www.linkedin.com/company/omnicor-ai/)
- ⚠ unverified — EUR 3.5M pre-seed figure: no primary source; do not use. [omnicorai.io](https://www.omnicorai.io/) (no funding information on the site)
- ✎ corrected — OpenVLA size was "7B" in the developer guide and "7.5B" elsewhere; harmonised to "`openvla-7b` checkpoint, about 7.5B parameters". Confirmed unchanged: 970K trajectories, DINOv2 + SigLIP + Llama-2, `vla-scripts/deploy.py` REST server, LoRA about 27 GB minimum (about 72 GB at batch 16), code MIT. [OpenVLA repo](https://github.com/openvla/openvla)
- ✔ confirmed — pi0.5 in LeRobot: `pip install 'lerobot[pi]'`, `policy.type=pi05`, checkpoints `lerobot/pi05_base` and `lerobot/pi05_libero_base`, gated PaliGemma tokenizer, reference fine-tune sized for one 80 GB GPU, default chunk size 50, `train_expert_only`, quantile stats (`q01` / `q99`). [LeRobot pi0.5 docs](https://huggingface.co/docs/lerobot/pi05)
- ✎ corrected — pi0.5 licence was "Apache 2.0" in some docs and "gemma" in another. Both sources exist: LeRobot docs state Apache 2.0, the `lerobot/pi05_base` weights card is tagged `gemma`. All docs now say both. [pi05_base model card](https://huggingface.co/lerobot/pi05_base)
- ✔ confirmed — `lerobot/pi05_base`: about 4B parameters, flow-matching action head only. [pi05_base model card](https://huggingface.co/lerobot/pi05_base)
- ✎ corrected — Apertus language count was "1,811" in two docs and "over 1,000" in a third; the model card gives both (1,811 natively supported). Harmonised. Confirmed unchanged: 8B and 70B sizes, Apache-2.0, context up to 65,536 tokens, Transformers / vLLM / SGLang / MLX. [Apertus-8B-Instruct-2509 card](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- ✔ confirmed — Small Apertus v1.1 variants (0.5B / 1.5B / 4B, with Instruct versions) and multimodal Apertus v1.5 (8B, 70B) exist on the Hub. [swiss-ai on Hugging Face](https://huggingface.co/swiss-ai)
- ✔ confirmed — Smallest YOLO26 detector about 2.4M parameters; AGPL-3.0; ONNX / TensorRT export. [Ultralytics repo](https://github.com/ultralytics/ultralytics)
- ✔ confirmed — MediaPipe Pose Landmarker: 33 landmarks, world coordinates in metres, built for on-device real-time use. [MediaPipe guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)
- ✔ confirmed — LeRobot is Apache-2.0 and ships ACT, SmolVLA and pi0.5 with `lerobot-record` / `lerobot-train`; Piper TTS is GPL-3.0 and local. [LeRobot repo](https://github.com/huggingface/lerobot) · [Piper repo](https://github.com/OHF-Voice/piper1-gpl)

Structural fixes in the same pass: 16 image lines removed from the four track "Products and Solutions" docs (the assets folder is empty; the site has no product imagery); a Sources section added to the T01 brief; briefs now end with Sources. Not re-checked: licences of whisper.cpp, CodeCarbon, TACO and TrashNet.

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [Omnicor AI on LinkedIn](https://www.linkedin.com/company/omnicor-ai/) (company listing; page not readable without login, details from starting notes and search snippets)
- [Leukerbad Hackathon 2026 event page (Luma)](https://luma.com/vj13ns00) (lists "Omnicor AI" among hardware / development-platform providers; no detail on what it brings)
- [OmnicorAI account on GitHub](https://github.com/OmnicorAI) (no public repositories; ownership unverified)
- [OpenVLA repository](https://github.com/openvla/openvla), [LeRobot pi0.5 docs](https://huggingface.co/docs/lerobot/pi05), [pi05_base model card](https://huggingface.co/lerobot/pi05_base), [Apertus-8B-Instruct-2509 model card](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509), [swiss-ai on Hugging Face](https://huggingface.co/swiss-ai), [Ultralytics repository](https://github.com/ultralytics/ultralytics), [MediaPipe Pose Landmarker guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker), [LeRobot repository](https://github.com/huggingface/lerobot), [Piper TTS repository](https://github.com/OHF-Voice/piper1-gpl) (third-party facts checked in the verification log)
