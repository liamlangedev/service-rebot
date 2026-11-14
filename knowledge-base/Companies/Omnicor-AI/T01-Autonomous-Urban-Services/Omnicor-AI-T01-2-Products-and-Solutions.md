---
type: challenge-products
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, products]
---
# Omnicor AI × T01 — Products and Solutions

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T01-1-Brief.md) · [Playbook](Omnicor-AI-T01-3-Playbook.md)

**Read this first:** Omnicor AI (written "OmniCor AI" on its site) publishes a single one-page website with headings only. There are **no specs, prices, docs, SDK, GitHub or case studies**. Every "not public" below is literal. The company sells the inference layer (getting a model to run on a given chip within power, speed and memory limits); it does not make robots, sensors or a navigation stack. Research note: only the official site and model pages could be checked in this pass; no press coverage was found by the profile research either.

## Relevant products (ranked for this track)

### OC Agent

**Role in T01:** the tool (or workflow) that fits a model to the compute already inside a delivery or service robot, so task understanding, dialogue or a manipulation policy runs on-board and keeps working when the network drops.

| Track-relevant item | Value |
|---|---|
| What it is (site wording) | "Agentic deployment environment" |
| Input it needs | Your trained model plus your target hardware (site contact prompt) |
| Supported target silicon | Not public. Ecosystem logos shown: Qualcomm, NVIDIA, AMD |
| Model types it claims to deploy | LLMs (Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek) and robot VLAs (OpenVLA, pi0.5 via LeRobot) |
| Porting time per model | Not public |
| Latency / throughput gains | Not public |
| ROS 2 integration | Not public ⚠️ unverified |

- **Status / price / availability:** ⚠️ unverified (listed on site; no release, licence or pricing information). Hackathon access: ask on site.
- **Developer interface:** not public. Assume it is operated by or with Omnicor engineers, not self-serve. It controls *how a model runs* (runtime, precision, memory footprint), not the robot.

### OC Node

**Role in T01:** a possible drop-in compute box to mount on a robot or cart that lacks enough on-board compute, or a local "town edge server" that several robots call over the venue LAN instead of the internet.

| Track-relevant item | Value |
|---|---|
| What it is (site wording) | "Compute platform designed in-house" |
| Chip / accelerator | Not public |
| Compute (TOPS / GPU memory) | Not public |
| Power draw, supply voltage | Not public |
| Size, weight, mounting | Not public |
| I/O (Ethernet, USB, CAN, camera inputs) | Not public |
| Ingress / temperature rating | Not public |

- **Status / price / availability:** ⚠️ unverified. Whether any unit is at Leukerbad is unknown.
- **Developer interface:** not public. Before planning around it, confirm OS, how you log in, and how a model is called (ROS 2 topic, HTTP, gRPC).

### Model optimisation

**Role in T01:** shrinking a model so a small robot can afford it: faster responses for a concierge robot, longer battery life on a delivery round, a VLA that reaches a usable control rate on embedded compute.

| Track-relevant item | Value |
|---|---|
| Stated optimisation targets | Power, speed and memory limits of the target device (site framing) |
| Methods (quantisation, distillation, compilation) | Not public |
| Published benchmarks | None |

- **Status / price / availability:** ⚠️ unverified; reads as a service. Price not public.
- **Developer interface:** none public. You hand over a model and constraints.

### European delivery

**Role in T01:** not usable in a 48-hour build. Relevant only for the pitch: a municipality or hotel buying service robots may prefer compute that is "designed and built in Europe" (site wording) and data that stays on the device.

- **Status / price / availability:** ⚠️ unverified. No factory, location or partner named.

## What Omnicor AI already does in this domain

Short answer: **nothing verifiable**. No dated deployment, pilot, demo or customer story in urban services, delivery or logistics is public.

| Date | Item | Relevance to T01 | Source |
|---|---|---|---|
| 2026 (site, undated) | "L4 Autonomous Logistics Vehicles" listed as a deployment domain, described as continuous multi-sensor inference under automotive thermal and reliability constraints | Closest claim to autonomous delivery. No vehicle maker, city, fleet size or date given | [Official site](https://www.omnicorai.io/) |
| 2026 (site, undated) | "Embodied AI Robotics" listed as a domain: perception and control on-board within a moving platform's power budget | Applies to service and delivery robots generally | [Official site](https://www.omnicorai.io/) |
| 2026 (site, undated) | Customer logos: AgiBot, Galbot, "sudo" | Both robot makers are on site; scope of the work is not public; "sudo" not identified ⚠️ unverified | [Official site](https://www.omnicorai.io/) |
| 2026 (site, undated) | Partner logo HUIXI; ecosystem logos Qualcomm, NVIDIA, AMD | HUIXI is probably the Chinese automotive-chip firm, which would fit the L4 vehicle claim ⚠️ unverified | [Official site](https://www.omnicorai.io/) |

## What they are building next in this domain

- **Announced:** nothing. No roadmap, release dates, events or funding news found.
- **Inference (not a statement by the company):** the pairing of an automotive-chip partner logo with the L4 logistics domain suggests work on vehicle-grade inference for delivery vehicles; the AgiBot and Galbot logos plus OpenVLA / pi0.5 suggest on-board VLA deployment for mobile manipulators. Either would be relevant to T01, neither is confirmed.

## Software, models and data that help for this track

Omnicor publishes no code, models or datasets. The shortcuts are the third-party open models its site says it deploys; you can start on these immediately on a laptop GPU and ask Omnicor to move them on-device.

| Asset | What it gives a T01 build | Facts checked | Status |
|---|---|---|---|
| Apertus 8B Instruct (Swiss AI Initiative) | Local multilingual dialogue and task parsing for concierge, wayfinding, order taking | **8B** and 70B sizes · Apache-2.0 · 1,811 supported languages stated · served via Transformers, vLLM (OpenAI-compatible API), SGLang, MLX; community quantised builds exist for llama.cpp / Ollama | ✅ |
| OpenVLA | Manipulation policy for pick-up and hand-over steps (image + instruction in, 7-DoF action out) | `openvla-7b` checkpoint, about **7.5B** parameters · code MIT, weights inherit Llama-2 community licence terms · LoRA fine-tuning script provided (about 27 GB GPU memory minimum stated for LoRA) · inference rate on embedded hardware not stated | ✅ |
| pi0.5 in LeRobot (`lerobot/pi05_base`) | Alternative VLA with multi-camera input, loadable through LeRobot | About **4B** parameters · weights card tagged `gemma` licence (LeRobot docs state Apache 2.0 for the implementation) · LeRobot port has the flow-matching action head only · fine-tune with `lerobot-train` | ✅ |
| Mistral, Qwen, DeepSeek, OpenEuroLLM | Other LLM options the site lists | Not checked in this pass | ⚠️ unverified which variants Omnicor supports |

Practical notes:
- **VLAs do not navigate.** OpenVLA and pi0.5 are arm-manipulation policies. Street and corridor navigation must come from the robot vendor's own stack or a standard ROS 2 navigation setup.
- **Fine-tuning a VLA needs data and a large GPU**; plan on pretrained behaviour or a very narrow task within 48 hours.
- No Omnicor datasets, simulation assets or sample apps exist publicly.

## Gaps and limits for this track

- **No robot, no sensors, no navigation, no payload.** A T01 project needs a body from another vendor; Omnicor is at most one layer in it.
- **Zero public technical detail.** No latency, power or memory numbers, so you cannot size a design before talking to the team.
- **No self-serve path.** No SDK, docs or repo: progress depends on engineer availability during the event.
- **Porting risk.** Whether a model can be optimised for a specific robot's computer within 48 hours is unknown.
- **Value is easy to miss in a demo.** "It runs locally" is invisible unless you stage it (unplug the network, show power or latency on screen).
- **Proof points are logos only.** Do not cite AgiBot, Galbot or L4 logistics work in a pitch as demonstrated deployments.

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/) (domains, "what we build" list, model, customer and ecosystem logos)
- [OpenVLA repository](https://github.com/openvla/openvla)
- [pi0.5 base model in LeRobot (Hugging Face)](https://huggingface.co/lerobot/pi05_base)
- [Apertus 8B Instruct model card (Hugging Face)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [Omnicor AI company profile (internal)](../Omnicor-AI.md)
