---
type: challenge-brief
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Omnicor AI × T02 Resilient & Safe City — Brief

**Fit: 3/5** — Not a robot and no public safety track record, but "the model keeps running on the robot when the network is gone" is exactly the resilience argument; usable only as the on-device inference layer of a multi-vendor build.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **OC Node** (in-house compute platform) + **OC Agent** (agentic deployment environment) + model optimisation service. All specs **not public**; availability on site ⚠️ unverified |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** Only a website claim (2026, undated) that AgiBot, Galbot and "sudo" ship with OmniCor AI, and that it targets embodied-AI robots, L4 logistics vehicles and AI servers |
| Fastest credible 48-hour demo | "Cut the cable" patrol: a quadruped or sensor mast runs hazard detection + a local LLM incident report fully on-board; unplug Wi-Fi live and show it still works |
| Biggest risk | Nothing to prepare against: no SDK, docs, GitHub or specs. If the team brings no hardware or a port takes days, you have no Omnicor component left |
| Pairs well with (other vendors on site) | Unitree Go2 / B2 or AGIBOT D1 (patrol body) · SKYLANDX MetaCam (3D map) · D-Robotics RDK (fallback edge board) · AGIBOT / Galbot (listed as Omnicor customers) · XREAL (responder display) |

## Why
- **Offline is the T02 story.** Avalanche, storm or tunnel = no cloud. Inference on the device is the only inference left.
- **Model list fits.** The site names open LLMs (Apertus, Mistral, Qwen, DeepSeek) and robot VLAs (OpenVLA, pi0.5) it deploys — enough for local reasoning and reporting in German / French.
- **Customer overlap on site.** AgiBot and Galbot appear on the Omnicor site; a working deployment may already be in the hall (ask).
- **Measurable judging angle:** latency, watts, "works with the router off".

## Not a fit for
- Teams needing a robot, sensors, mapping or navigation from one vendor — Omnicor supplies none.
- Teams wanting a documented, self-serve SDK tonight — none is public.
- Projects where a cloud API is acceptable.

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Products and solutions](Omnicor-AI-T02-2-Products-and-Solutions.md) · [Playbook](Omnicor-AI-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [Omnicor AI on LinkedIn](https://www.linkedin.com/company/omnicor-ai/) (via profile research; not readable without login)
