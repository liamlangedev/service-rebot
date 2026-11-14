---
type: products
company: "Omnicor AI"
slug: Omnicor-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, products]
---
# Omnicor AI — Product Portfolio

⬆ [Omnicor AI profile](Omnicor-AI.md) · [Developer guide](Omnicor-AI-Developer-Guide.md) · [Roadmap and strategy](Omnicor-AI-Roadmap-and-Strategy.md)

> **Read this first (30 seconds).** OmniCor AI is **not a robot vendor**. It is an edge-AI deployment company: you bring a trained model and a target hardware platform, they make the model run on-device. Its entire public catalogue is **four headings on a one-page website** — two named products (OC Agent, OC Node) and two service lines. **No specs, no prices, no datasheets, no docs, no product photos are public.** Everything marked "not public" below is a question to ask at their table, not something you can plan against.
>
> **Decision rule:** pick OmniCor as a **supporting layer** (on-board / offline inference) on top of another vendor's robot — never as your only platform. Confirm in the first hour what hardware and access they actually have on site.

## Lineup map

Track relevance: ● strong · ◐ partial · ○ none. Status is ⚠️ unverified for every row: the site lists the item but does not say whether it is shipping, in pilot, or planned.

| Product | Category | Status | Launched | Price (if public) | Positioning (one line) | T01 | T02 | T03 | T04 |
|---|---|---|---|---|---|---|---|---|---|
| **OC Agent** | Software — agentic deployment environment | ⚠️ unverified (listed on site) | not public | not public | Tooling that automates fitting a model to a given edge hardware target | ◐ | ◐ | ◐ | ◐ |
| **OC Node** | Hardware — in-house compute platform | ⚠️ unverified (listed on site) | not public | not public | OmniCor's own compute box / board for running models at the edge | ◐ | ● | ◐ | ◐ |
| **Model optimisation** | Service | ⚠️ unverified (listed on site) | not public | not public | Getting a model inside a power, speed and memory budget | ◐ | ◐ | ◐ | ◐ |
| **European delivery** | Service — design and manufacturing in Europe | ⚠️ unverified (listed on site) | not public | not public | "Designed and built in Europe" supply and delivery | ○ | ○ | ○ | ○ |

Why no ● except OC Node / T02: OmniCor contributes inference, not sensing or actuation, so it can only ever be part of a solution. The one place where it could be the core argument is T02, where "keeps working when the network is down" is the whole point.

## Products

### OC Agent

**What it is:** the site describes it in three words — an "agentic deployment environment". Read together with the rest of the page, it is the software workflow OmniCor uses to take a trained model and produce a deployment for a specific hardware target. Whether it is an internal tool, a hosted service or something you can install is **not public**.

| Item | Value |
|---|---|
| Type | Software (deployment tooling) |
| Inputs (from site's contact prompt) | Your model + your target hardware |
| Model families the site says OmniCor deploys | LLMs: Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek · Robot VLAs: OpenVLA, pi0.5 (LeRobot) · "and others" |
| Silicon ecosystems shown on site | Qualcomm, NVIDIA, AMD (logos only; supported chips / SDK versions not public) |
| Interface (CLI, GUI, API) | not public |
| Supported model formats / runtimes | not public |
| ROS 2 integration | not public ⚠️ unverified |
| Licence / access model | not public |
| Docs, SDK, GitHub | none found |

- **Variants / editions:** none published (no EDU or developer edition is mentioned).
- **Typical applications (per site's deployment domains):** on-board perception and control for embodied-AI robots; multi-sensor inference on L4 autonomous logistics vehicles; rack-side inference on enterprise AI servers.
- **Hackathon use, if available on site:** port a VLA (OpenVLA, pi0.5) or a local LLM (Apertus, Mistral, Qwen) onto the compute of the robot you chose, so the demo runs without cloud.
- **Ask before committing:** Can a participant use it directly, or do OmniCor engineers run it for you? How long does one port take — hours or days?
- **Official page:** [omnicorai.io — What we build](https://www.omnicorai.io/#tech)

### OC Node

**What it is:** a "compute platform designed in-house" — OmniCor's own edge compute hardware. That single phrase is the full public description. Form factor (module, board, box, rack unit) is **not public**.

| Item | Value |
|---|---|
| Type | Hardware (compute platform) |
| Processor / accelerator | not public |
| AI performance (TOPS, tokens/s, Hz for VLAs) | not public |
| Memory / storage | not public |
| Power draw / supply voltage | not public |
| Interfaces (Ethernet, USB, CAN, camera inputs) | not public |
| Size / weight / mounting | not public |
| Operating temperature / IP rating | not public |
| OS / software stack | not public |
| Price / availability | not public |

- **Variants:** none published.
- **Do not assume** it is based on Qualcomm, NVIDIA or AMD silicon: those appear on the site as ecosystem logos for the company, not as the OC Node bill of materials. The site also shows HUIXI as "our partner" (probably the Chinese automotive-chip company — ⚠️ unverified); any link to OC Node is speculation.
- **Typical applications (per site):** the same three domains — robots under a mobile power budget, automotive-grade logistics vehicles, throughput-per-watt servers.
- **Hackathon use, if units are on site:** a plug-in offline "brain" beside a quadruped, humanoid or arm from another vendor — useful where alpine connectivity is weak (T02) or where patient data must stay in the room (T04).
- **Ask before committing:** How many units are here? Chip, power input, and which ports? Is there a ready image with a model server (HTTP / gRPC / ROS 2 topic) so you can call it from your robot code within an hour?
- **Official page:** [omnicorai.io — What we build](https://www.omnicorai.io/#tech)

### Model optimisation

**What it is:** a service line, listed as a heading with no description. From the site's framing, it means making a given model meet the constraints of the target device: mobile power budget on robots, thermal and reliability limits on vehicles, throughput per watt on servers.

| Item | Value |
|---|---|
| Type | Service |
| Techniques used (quantisation, pruning, distillation, compilation) | not public |
| Published benchmarks (speed-up, accuracy loss, watts) | none |
| Turnaround time | not public |
| Price | not public |

- **Typical applications:** shrinking / accelerating an LLM or VLA so it runs on the compute already inside a robot.
- **Hackathon relevance:** most valuable for T03 arguments (less energy per inference) and for any on-robot VLA demo — but only if it can be done inside 48 h. Ask for a concrete before/after number on a model you care about.
- **Official page:** [omnicorai.io — What we build](https://www.omnicorai.io/#tech)

### European delivery

**What it is:** the site's fourth item — "Designed and built in Europe". A sourcing and delivery statement, not something you can build on during the event.

| Item | Value |
|---|---|
| Type | Service / supply-chain positioning |
| Manufacturing location, partners, certifications | not public |
| HQ / legal entity | not public |

- **Hackathon relevance:** none for the build. Useful only as a pitch line (European data-sovereignty and supply-chain angle, alongside European open models such as Apertus, Mistral and OpenEuroLLM).
- **Official page:** [omnicorai.io — What we build](https://www.omnicorai.io/#tech)

## Accessories and ecosystem

OmniCor publishes no accessories. What surrounds the products, as shown on its site:

| Layer | What the site shows | What it does NOT tell you |
|---|---|---|
| Models deployed | Apertus, Mistral AI, OpenEuroLLM, Qwen, DeepSeek, OpenVLA, pi0.5 (LeRobot), "and others" | Model sizes, versions, achieved speed on any hardware |
| Silicon ecosystem | Qualcomm, NVIDIA, AMD | Specific chips or boards supported |
| Partner | HUIXI | Nature of the partnership ⚠️ unverified |
| Customers ("teams shipping with OmniCor AI") | AgiBot, Galbot, "sudo" | Which robots, which models, what volume; identity of "sudo" ⚠️ unverified |
| Deployment domains | Embodied-AI robots · L4 autonomous logistics vehicles · enterprise AI servers | Any named deployment or case study |

**Cross-vendor pairings to explore on site (ideas, not confirmed integrations):**

| Pair with | Why it is plausible | Check first |
|---|---|---|
| **AGIBOT** (G1 / G2, A2, X2) | Listed as an OmniCor customer | Is an OmniCor deployment already running on the units here? |
| **Galbot** (G1) | Listed as an OmniCor customer | Same question; which model? |
| **Unitree** quadrupeds / humanoids with NVIDIA Jetson-class compute | NVIDIA is in OmniCor's ecosystem list | Whether OmniCor has ever targeted that exact board |
| **D-Robotics** RDK boards | Alternative edge compute if no OC Node is available | Not in OmniCor's ecosystem list — likely unsupported ⚠️ unverified |

## Legacy and discontinued

None known. The company has no public product history (website copyright 2026; no earlier announcements found).

## Image credits

**No pictures saved (0 of 4).** The official site contains no product imagery at all: no og:image / twitter:image, and no picture of OC Agent, OC Node or either service. The only images on the site are three small generic illustrations of the deployment domains (robot, logistics vehicle, server), the company logo, and third-party logos. Using any of those as a "product picture" would misrepresent what the products look like, so none was stored under a product key. No press kit or Wikimedia Commons media was found.

| file | shows | source URL |
|---|---|---|
| — (none) | No official image exists for OC Agent, OC Node, Model optimisation or European delivery | [omnicorai.io](https://www.omnicorai.io/) checked 2026-11-14 |

## Sources

- [OmniCor AI official website](https://www.omnicorai.io/) — the only primary source; one-page site (HTML and its English text strings) read on 2026-11-14
- [OmniCor AI — "What we build" section](https://www.omnicorai.io/#tech)
- [Omnicor AI profile in this pack](Omnicor-AI.md) — earlier research (LinkedIn listing, name disambiguation)

Research note: the web-search quota for this run was exhausted before any third-party search on OC Agent / OC Node could be made, so this document rests on the official site alone. No independent coverage is cited because none was checked in this pass.
