---
type: dev-guide
company: "Omnicor AI"
slug: Omnicor-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Omnicor AI — Developer Guide (hackathon edition)

⬆ [Omnicor AI profile](Omnicor-AI.md) · [Product portfolio](Omnicor-AI-Products.md) · [Roadmap and strategy](Omnicor-AI-Roadmap-and-Strategy.md)

> **Read this first.** OmniCor AI publishes **no SDK, no docs, no repos, no specs**. There is nothing to install before you talk to them. This guide therefore covers (a) what is publicly known, (b) what to ask at their table, and (c) a vendor-neutral fallback so your team is not blocked if their tooling is not self-serve. Anything about OC Agent / OC Node internals is **not public**.

## TL;DR — how you program it

- **You do not program OmniCor directly (as far as is public).** The stated workflow is: you bring a **trained model + a target hardware platform**, they deliver a deployment that fits your **power, speed and memory** limits.
- **It sits at the inference layer**, not the robot-control layer: below your policy / agent code, above the chip. Robot motion still goes through the robot vendor's SDK (AgiBot, Galbot, Unitree, ...).
- **Two named building blocks:** **OC Agent** (agentic deployment environment, software) and **OC Node** (in-house compute platform, hardware). Interfaces, APIs and specs for both: **not public**.
- **Models they say they deploy:** Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek (LLMs) and **OpenVLA, pi0.5** (robot VLAs). All are third-party open models you can already run yourself.
- **Hackathon play:** prototype with the open model on a laptop GPU first, then ask OmniCor to move it **on-board / offline**. Decide in the first hour whether their path fits in 48 h; if not, keep your laptop as the inference server.

## SDKs and interfaces

**OmniCor's own interfaces**

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| OC Agent | not public | Automates fitting a model to a target device (per site: "agentic deployment environment") | [site](https://www.omnicorai.io/#tech) | No download, CLI, API or docs published. Access model (hosted / on-prem / operated by their engineers) not public |
| OC Node | not public | Compute box that runs the deployed model | [site](https://www.omnicorai.io/#tech) | Chip, memory, power, I/O, OS: not public |
| GitHub account `OmnicorAI` | — | — | [github.com/OmnicorAI](https://github.com/OmnicorAI) | Account exists, **0 public repositories**; not linked from the official site, ownership ⚠️ unverified |
| Docs portal / Hugging Face org / PyPI package | — | — | — | None found (docs subdomain does not resolve; no HF org under obvious names) |

**What you will actually code against (third-party, verified)**

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| LeRobot (`lerobot[pi]`) | Python | pi0.5 policy: fine-tune, eval, rollout on a robot | [docs](https://huggingface.co/docs/lerobot/pi05) | `policy.type=pi05`; checkpoints `lerobot/pi05_base`, `lerobot/pi05_libero_base`; LeRobot docs state Apache 2.0, but the `lerobot/pi05_base` weights card is tagged `gemma` licence — check before reuse |
| openpi | Python | Physical Intelligence reference implementation of pi0 / pi0.5 | [repo](https://github.com/Physical-Intelligence/openpi) | LeRobot's pi0.5 is adapted from it |
| OpenVLA | Python (PyTorch, HF Transformers) | 7-DoF end-effector actions from one image + instruction | [repo](https://github.com/openvla/openvla) | `openvla-7b` checkpoint, about **7.5B** params per the repo; `vla-scripts/deploy.py` exposes a REST server; code MIT, weights inherit Llama-2 licence terms |
| Apertus (swiss-ai) | any HF-compatible runtime | Swiss open LLM, multilingual | [HF org](https://huggingface.co/swiss-ai) | Sizes on the Hub include `Apertus-v1.1-0.5B / 1.5B / 4B(-Instruct)`, `Apertus-8B-Instruct-2509`, 70B, and multimodal `Apertus-v1.5-8B` |

## Control levels

Not a robot-control product, so "high-level vs joint-level" does not apply. Think of it as three layers:

| Layer | Who owns it | What you do |
|---|---|---|
| Task / agent logic (what to do, when) | **You** | Your Python / ROS 2 code |
| Model inference (VLA action chunks, LLM tokens, perception) | **OmniCor's layer** | Hand over model + hardware; get back a runtime that meets latency / power / memory targets |
| Robot actuation (joint, torque, base, gripper) | **Robot vendor SDK** | Use that vendor's dev guide; OmniCor does not replace it |

- **Rates:** nothing published. As a rule of thumb, a VLA runs at a few Hz to tens of Hz and outputs **action chunks**; the robot's own controller interpolates at its native rate. OmniCor has not published any Hz / latency figure for any model or chip.
- **EDU / developer editions:** none exist publicly. No licence tiers known.

## ROS 2 and middleware

- **ROS 2 support: not stated** ⚠️ unverified. No ROS 2 package, message definitions or bridge are published.
- **Practical pattern (works regardless of what they give you):** wrap the model behind a small local service and keep ROS 2 on the robot side.
  - Robot side: vendor ROS 2 driver / SDK publishes camera + joint state, accepts action targets.
  - Inference side: one process that takes `image(s) + state + instruction` and returns an action chunk (HTTP, gRPC or ZeroMQ on the LAN). OpenVLA's `deploy.py` already follows this shape.
- **Ask on site:** "Do you hand us a ROS 2 node, a REST / gRPC endpoint, or a library we link against?"

## Simulation and digital twins

- **None from OmniCor.** No URDF / MJCF / USD assets, no Isaac Lab / MuJoCo / Gazebo repos.
- Use the **robot vendor's** simulation assets, and LeRobot's simulation benchmarks (e.g. LIBERO, which the pi0.5 docs use for the reference fine-tune) to sanity-check a policy before touching hardware.
- **Why it still matters here:** an optimised (quantised / compiled) model can behave differently from the original. Re-run the same eval episodes before and after optimisation and compare success rate, not just speed.

## AI stack

| Item | Status | What is known |
|---|---|---|
| Own pretrained policies / foundation model | none public | OmniCor deploys other people's models |
| LLMs listed on site | ✅ third-party, open | Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek, "and others" |
| VLAs listed on site | ✅ third-party, open | OpenVLA, pi0.5 (site logo is labelled pi0.5; LeRobot ships it as `pi05`) |
| Optimisation methods (quantisation, compilation, distillation, runtime) | not public | Site says only "model optimisation" for power / speed / memory |
| Datasets | none public | — |
| Teleoperation / data collection | none | Use the robot vendor's teleop + LeRobot recording |
| LeRobot support | indirect | pi0.5 is a LeRobot policy; whether OC Agent ingests a LeRobot checkpoint directly is ⚠️ unverified |

**Facts worth knowing before you hand a model over**

- **pi0.5 (LeRobot):** install `pip install 'lerobot[pi]'`; needs the **gated** `google/paligemma-3b-pt-224` tokenizer (accept licence on the Hub, `hf auth login`). Default action **chunk size 50**. The reference full fine-tune is sized for a **single 80 GB GPU**; `train_expert_only=true` freezes the VLM and cuts memory. Supports Real-Time Chunking for latency-tolerant rollout.
- **OpenVLA:** fused DINOv2 + SigLIP vision, Llama-2 language backbone, trained on **970K** Open X-Embodiment trajectories. Output is a single 7-DoF action un-normalised per dataset key (`unnorm_key`), so it needs fine-tuning for a new robot. LoRA fine-tune needs roughly **27 GB VRAM minimum** (about 72 GB at batch 16). OpenVLA-OFT is the faster, multi-image, bimanual-capable fine-tuning recipe.
- **Apertus:** small variants (0.5B / 1.5B / 4B) are the realistic candidates for a fully offline on-robot assistant; check each model card for licence and language coverage.

## Compute, sensors and connectivity

| Topic | What is known |
|---|---|
| OC Node hardware | Exists per site ("compute platform designed in-house"). Chip, RAM, power draw, ports, OS, price: **not public** |
| Silicon ecosystem | Site shows **Qualcomm, NVIDIA, AMD** logos; partner logo **HUIXI** (⚠️ unverified which company) |
| Sensors | None. Cameras / LiDAR come from the robot or other vendors |
| Connecting a laptop | Not documented. Expect Ethernet / Wi-Fi to whatever box runs the model; confirm on site |
| Network defaults (IP, ports, credentials) | Not public |
| Cloud dependency | Their pitch is on-device inference; whether OC Agent itself needs internet during the porting step is ⚠️ unverified — **ask**, venue connectivity may be limited |

**Fallback compute if no OC Node is available:** your team's laptop GPU on the robot's LAN, the robot's own on-board computer, or another vendor's edge board on site (e.g. D-Robotics RDK, per the event vendor list).

## First 60 minutes checklist

1. **Find the OmniCor table (5 min).** Ask what is physically here: OC Node units (how many, which chip), OC Agent access, and which robots on site already run an OmniCor deployment.
2. **Ask the go / no-go question (5 min):** "If we give you a fine-tuned pi0.5 / OpenVLA checkpoint or a small LLM tonight, when do we get it running on-board, and what do we call — ROS 2 node, HTTP, library?" If the answer is longer than about half a day, plan to keep inference on a laptop.
3. **Pick the model and robot now (10 min).** VLA manipulation (pi0.5 / OpenVLA on a dual-arm or arm platform) or offline language / vision assistant (Apertus / Qwen / Mistral small variant). Write down your budget: target Hz or tokens/s, max latency, power source.
4. **Stand up the unoptimised baseline in parallel (20 min).** On a laptop GPU: `pip install 'lerobot[pi]'`, accept the PaliGemma licence, load `lerobot/pi05_base`; or load a small Apertus / Qwen instruct model with your usual runtime. This is your fallback and your "before" measurement.
5. **Define the I/O contract (5 min).** Inputs (camera keys, resolution, state vector, instruction string), outputs (action dimension, chunk length, units), transport. Share it with OmniCor and with whoever writes the robot-side code.
6. **Hello-world inference (10 min).** Feed one recorded frame + instruction, print the action / reply and the **wall-clock latency**. Do not send actions to a real robot yet.
7. **Verify on hardware (5 min).** Once a deployed version exists: same input, compare output against the baseline and log latency, memory and (if they can show it) power. Only then close the loop on the robot at low speed with the vendor's e-stop in hand.

## Known gotchas and safety

- **Service, not self-serve (most likely).** With a 2–10 person company (LinkedIn figure, ⚠️ unverified) and no public tooling, your throughput depends on their engineers' time. Get in the queue early.
- **No published numbers.** Any Hz, watt or memory claim you hear on site is unverifiable in advance; measure it yourself before you put it in your pitch.
- **Optimisation changes behaviour.** Quantised / compiled VLAs can lose precision on fine manipulation. Re-test success rate after optimisation.
- **A zero-shot VLA will not work on a new robot.** OpenVLA and pi0.5 both need embodiment-specific fine-tuning data; budget teleop + training time (cloud or on-site GPU), which is outside OmniCor's stated scope.
- **Licences and gating.** PaliGemma tokenizer (pi0.5) is gated and the `lerobot/pi05_base` weights card carries a `gemma` licence tag; OpenVLA weights inherit Llama-2 community licence terms. Download everything **before** you lose connectivity.
- **pi0.5 dataset stats.** It normalises with quantiles; older LeRobot datasets without `q01` / `q99` fail on the first batch — recompute stats or switch to mean/std normalisation.
- **E-stop and modes are the robot vendor's.** OmniCor's layer has no safety function. A learned policy must always run behind the robot's own limits, speed caps and emergency stop; keep people (especially for T04 care scenarios) out of reach during first closed-loop runs.
- **Name confusion.** Not ABB OmniCore (robot controller). Searching "omnicore" returns the wrong documentation.

## Community resources

- **OmniCor:** no forum, Discord, GitHub issues or docs. Only channel: the team on site and `contact@omnicorai.com`.
- **LeRobot:** [docs](https://huggingface.co/docs/lerobot/index) and [repo](https://github.com/huggingface/lerobot) (issues, Discord linked from the repo).
- **OpenVLA:** [repo](https://github.com/openvla/openvla) issues.
- **openpi:** [repo](https://github.com/Physical-Intelligence/openpi) issues.
- **Apertus:** model cards under [swiss-ai on Hugging Face](https://huggingface.co/swiss-ai).

Research note: general web search was unavailable when this guide was written; findings rest on the official site (page and script bundle), direct checks of likely developer URLs, and the profile's earlier research.

## Sources

- [OmniCor AI official website](https://www.omnicorai.io/) (page text, meta description and site script bundle; only public primary source)
- [OmnicorAI account on GitHub](https://github.com/OmnicorAI) (no public repositories; ownership unverified)
- [LeRobot documentation — pi0.5 policy](https://huggingface.co/docs/lerobot/pi05)
- [LeRobot documentation index](https://huggingface.co/docs/lerobot/index)
- [LeRobot repository](https://github.com/huggingface/lerobot)
- [OpenVLA repository README](https://github.com/openvla/openvla)
- [pi0.5 base model card in LeRobot (Hugging Face)](https://huggingface.co/lerobot/pi05_base)
- [openpi repository (Physical Intelligence)](https://github.com/Physical-Intelligence/openpi)
- [swiss-ai organisation on Hugging Face (Apertus models)](https://huggingface.co/swiss-ai)
- [Omnicor AI profile in this vault](Omnicor-AI.md) (company size, people and customer-logo details)
