---
type: challenge-products
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, products]
---
# Omnicor AI × T04 — Products and Solutions

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T04-1-Brief.md) · [Playbook](Omnicor-AI-T04-3-Playbook.md)

**Read this first:** OmniCor AI publishes a single one-page website with headings only. There are **no specs, no docs, no SDK, no prices and no care-sector references**. Every product row below is "ask on site". The role in T04 is a supporting one: make language, vision and robot-policy models run **on the device**, so patient audio and video never leave the room.

## Relevant products (ranked for this track)

### OC Agent

**Role in T04:** the tool (or tool-assisted service) that fits a model to a target board. In care this means: get a local LLM, a speech model or a robot VLA running on the robot's own computer instead of in the cloud.

| Track-relevant item | Value |
|---|---|
| What it is | "Agentic deployment environment" (site wording, no further detail) |
| Input you provide | Trained model + target hardware (per the site's contact form) |
| Supported model families (site list) | Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek, OpenVLA, pi0.5 (LeRobot), "and more" |
| Target silicon (ecosystem logos) | Qualcomm, NVIDIA, AMD |
| Porting time per model | Not public |
| Speech (ASR / TTS) or pose models supported | Not public |
| ROS 2 / API surface | Not public |

- **Status / price / availability:** ⚠️ unverified — listed on the site, no release state, no price, no download.
- **Developer interface:** not public. Expect to work **through the OmniCor engineers**, not through a self-serve SDK.

### OC Node

**Role in T04:** a possible plug-in compute box beside or on a care robot, a bedside device or a therapy station.

| Track-relevant item | Value |
|---|---|
| What it is | "Compute platform designed in-house" (site wording) |
| Chip, memory, performance | Not public |
| Power draw, battery operation | Not public |
| Interfaces (USB, Ethernet, CAN, camera, audio) | Not public |
| Noise / fan (matters in a patient room) | Not public |
| Medical or safety certification | None stated |

- **Status / price / availability:** ⚠️ unverified — whether units are on site is unknown.
- **Developer interface:** not public. Ask whether it runs standard Linux with SSH and containers.

### Model optimisation

**Role in T04:** shrink or speed up a model until it meets a latency target on small hardware — e.g. a spoken reply fast enough for a hard-of-hearing guest not to give up, or a VLA fast enough for smooth arm motion.

| Track-relevant item | Value |
|---|---|
| Optimisation targets named on site | Power, speed, memory limits |
| Methods (quantisation, distillation, compilation) | Not public |
| Published benchmarks | None |

- **Status / price / availability:** ⚠️ unverified — a service, terms not public.
- **Developer interface:** none public.

### European delivery

**Role in T04:** not a build tool. It is a **pitch argument**: a European supply chain and European open models (Apertus, Mistral, OpenEuroLLM) support a data-sovereignty story for Swiss clinics. Details (where, who manufactures) are not public. ⚠️ unverified.

## What Omnicor AI already does in this domain

**Nothing public.** No deployment, pilot, demo, partner or statement in elderly care, rehabilitation, healthcare or assistive robotics was found (checked 2026-11-14).

Adjacent, general evidence only:

| Date | Fact | Relevance to T04 |
|---|---|---|
| 2026 (website, undated) | AgiBot, Galbot and "sudo" shown as teams shipping with OmniCor AI; scope not public | Both robot makers are on site — plausible joint build for assistive manipulation. [Source](https://www.omnicorai.io/) |
| 2026 (website, undated) | First listed domain is embodied-AI robots: perception and control on-board within a mobile power budget | Matches care robots that must work without a network. [Source](https://www.omnicorai.io/) |
| 2026 (website, undated) | Model list includes multilingual LLMs and two robot VLAs | Building blocks for a voice-driven assistive robot. [Source](https://www.omnicorai.io/) |

## What they are building next in this domain

- **Announced:** nothing. No roadmap, no healthcare plans.
- **Inference (not a company statement):** the mix of European open LLMs, robot VLAs and a Europe-built compute node suggests a sovereignty-minded edge offer. Care and clinics would be a natural buyer for that, but OmniCor has not said so.

## Software, models and data that help for this track

OmniCor publishes no code. The shortcuts are the **third-party open models it says it deploys**, plus standard on-device tools. None of the "other tools" rows are confirmed as OmniCor-supported.

| Building block | Use in T04 | Facts that matter for 48 h | Status |
|---|---|---|---|
| **Apertus** (Swiss AI Initiative) — on OmniCor's list | Local multilingual dialogue, reminders, summarising a care log | **8B and 70B** sizes, **Apache-2.0**, model card states **1,811** natively supported languages (summary line: over 1,000); quantised community builds usable with llama.cpp / Ollama. Swiss German quality ⚠️ unverified | ✅ |
| **Mistral / Qwen / DeepSeek** — on OmniCor's list | Alternative local LLMs if Apertus is too slow or weak on a task | Exact variants OmniCor supports not public | ✅ (models) |
| **pi0.5 in LeRobot** — on OmniCor's list | Language-conditioned fetch / tidy / hand-over on an arm | Apache-2.0 per LeRobot docs (`lerobot/pi05_base` weights card tagged `gemma`); `pip install 'lerobot[pi]'`; base checkpoint `lerobot/pi05_base`; reference fine-tune is sized for **one 80 GB GPU** — too heavy to retrain casually in 48 h | ✅ |
| **OpenVLA** — on OmniCor's list | Same role, older VLA (`openvla-7b`, about 7.5B parameters) | Code MIT (weights inherit Llama-2 terms); trained on **970K** Open X-Embodiment trajectories; LoRA fine-tune needs roughly **27 GB+** GPU memory | ✅ |
| whisper.cpp (other tool) | Offline speech-to-text for voice commands | MIT, runs on CPU, CUDA, ARM; fully offline | ✅ |
| Piper (other tool) | Offline text-to-speech | GPL-3.0, local; check the voice list for German / French voices ⚠️ unverified | ✅ |
| MediaPipe Pose Landmarker (other tool) | Rehab exercise tracking, posture and fall cues | **33 3D landmarks** per person, world coordinates in metres, built for on-device real-time use | ✅ |

**Datasets:** none from OmniCor. For manipulation you will record your own demonstrations on the robot you borrow.

## Gaps and limits for this track

- **No body.** No robot, arm, gripper, sensors or force control. Every physical capability comes from another vendor.
- **No care evidence.** No clinical pilot, no safety or medical-device certification, no accessibility work.
- **No self-serve path.** No docs, SDK, GitHub or examples to prepare with; progress depends on the engineers' time, which every team will compete for.
- **Unknown performance.** No latency, tokens-per-second or control-rate figures for any model on any board.
- **Unknown hardware on site.** OC Node may not be here at all.
- **Privacy claim is yours to prove.** "On-device" is implied by the site, not stated as a data-handling guarantee. Demonstrate it (network unplugged) rather than cite it.
- **Research limit:** web search quota ran out during this track-specific pass; findings rest on the official site and the company profile. A care reference published elsewhere could have been missed — ask the team.

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [Omnicor AI company profile (this repo)](../Omnicor-AI.md)
- [Apertus-8B-Instruct-2509 model card (Hugging Face)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [LeRobot docs — pi0.5 policy](https://huggingface.co/docs/lerobot/pi05)
- [pi0.5 base model card in LeRobot (Hugging Face)](https://huggingface.co/lerobot/pi05_base)
- [OpenVLA GitHub repository](https://github.com/openvla/openvla)
- [whisper.cpp GitHub repository](https://github.com/ggml-org/whisper.cpp)
- [Piper TTS GitHub repository](https://github.com/OHF-Voice/piper1-gpl)
- [MediaPipe Pose Landmarker guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)
