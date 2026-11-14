---
type: roadmap
company: "Binabik AI"
slug: Binabik-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# Binabik AI — Roadmap and Strategy

⬆ [Binabik AI profile](Binabik-AI.md) · [Product portfolio](Binabik-AI-Products.md) · [Developer guide](Binabik-AI-Developer-Guide.md)

> **In one line:** a ten-month-old Swiss-Finnish spin-off that narrowed from "a brain for any robot" to **humanoid machine tending sold as a service**, funded so far only by Venture Kick grants, with no published product roadmap. Public information is thin; this page is short on purpose.
>
> Research limit: web search was unavailable for this page; it relies on direct reads of the company site, its GitHub and Hugging Face orgs, and three third-party articles. Trade-press news after April 2026 may be missing.

## Company trajectory

| Date | Milestone |
|---|---|
| Aug–Sep 2025 | GitHub org `binabik-ai` goes live; first open-source releases `mcp-lab` and `mcp-rosbags` (LLM agents querying robot logs via MCP) |
| 2025 | Pre-incorporation prototype: software on a quadruped that patrols an area and looks for changes |
| Late 2025 (approx.) | Venture Kick Stage I, **CHF 10,000**; during its three months, a proof of concept with an unnamed industrial partner, shown to that company's leadership |
| Dec 2025 – Jan 2026 | Fork of NVIDIA Isaac GR00T N1.6 with added fine-tuning scripts |
| Jan 2026 | Binabik GmbH founded as a spin-off of the ZHAW Centre for Artificial Intelligence |
| 13 Feb 2026 | Venture Kick Stage II, **CHF 40,000**; focus now on humanoids, one industrial vertical |
| By 2 Mar 2026 | Best start-up pitch at the Humanoid Forum, Biel/Bienne (per the [profile](Binabik-AI.md)) |
| 2026 | Listed in European Robotics Forum 2026 matchmaking as "The Agentic Operating System for Physical AI" |
| 14 Apr 2026 | Move into Technopark Winterthur announced; **5** people, plan for **15** within 12 months |
| May–Jul 2026 | Public work on Unitree G1 imitation learning in Isaac Lab (forks of `unitree_lerobot`, `unitree_sim_isaaclab`); first Hugging Face checkpoint on 2 Jul 2026 |
| Nov 2026 | Site sells Binabik Solutions (machine tending as a service) and Binabik Studio (request access); **8** people on the about page; 8 open roles plus open applications |
| 14–16 Nov 2026 | On site at the Leukerbad Robotics Hackathon |

## Current focus projects

- **Machine tending with humanoids, as a service.** One robot serves several machines (lathe, press, conveyor, pallet). Shown on **Galaxea R1 Pro**; **AgiBot G2** also named. Customer engagement runs workshop (1 day) → proof of concept → prototype in production → scaling.
- **Turning the internal toolchain into a product.** Studio bundles Teach, Skill Engine, Sim and the Development Kit; still request-access with no public docs. A docs portal exists behind a login.
- **Hiring toward 15 people.** Open roles: robotics, software and infrastructure, perception, two research internships (robot learning; robotics software and evaluation), Head of Go-to-Market, two business internships. All in Winterthur; open applications also for Espoo.
- **Proof points still missing in public:** no named customer, the Solutions demo video is "coming soon", the blog is empty.

## Announced and upcoming products

Binabik publishes **no dated roadmap**. Everything below is stated intent or visible work in progress.

| Item | Status | Date | Evidence |
|---|---|---|---|
| Binabik Studio general availability | 🧪 request access | not public | Studio page |
| Development Kit support for more robots beyond G2 and R1 Pro | 🔭 | not public | Home page: more platforms "as the market moves"; none named |
| Solutions demo video | 🧪 | "coming soon" | Solutions page |
| Machine-builder partner programme (machine sold with its robot operator) | 🧪 offered, no partner named | not public | Home and Solutions pages |
| Additional verticals beyond the first industrial one | 🔭 | not public | Venture Kick interview, Feb 2026 |
| "Insights & Research" publication stream | 🔭 section exists, no posts | not public | Blog page |
| Public developer documentation | 🔭 portal exists, gated | not public | docs.binabik.ai returns a login |

## Strategic direction and markets

| Theme | Detail |
|---|---|
| Positioning | Hardware-independent software and skills on top of third-party humanoids; "agentic" task layer rather than a foundation model |
| Narrowing | Any robot body (2025) → humanoids (Stage I) → one vertical, machine tending in production and logistics (2026) |
| Business model | Robot as a service: hardware, software, updates and support in one subscription; price not public |
| Channels | Direct to manufacturers; joint offers with machine builders; system integrators using the Development Kit; Academy training |
| Selling points | No robotics team needed at the customer; teach once; data stays in the factory; plans reviewable before execution |
| Hardware partners | Uses AgiBot G2 and Galaxea R1 Pro. No formal partnership announcement found (⚠️ unverified) |
| Technology suppliers | NVIDIA ecosystem visible: SimReady assets, Isaac Lab and GR00T forks. No NVIDIA partnership announced |
| Switzerland | HQ Technopark Winterthur; origin ZHAW; supported by Greater Zurich Area and House of Winterthur; Venture Kick grantee |
| Finland / Europe | Second office in Finland (Espoo per contact and careers pages, Turku per ERF listing); present at ERF 2026 matchmaking; site in English and German |
| Funding | **CHF 50,000** in Venture Kick grants (10k + 40k). No equity round public. A 15-person plan implies fundraising, but nothing is announced (inference) |
| Stated wider interests | ERF listing names healthcare, smart cities and infrastructure inspection, logistics, energy, agri-tech, construction, security among areas of activity. These are 🔭 interests, not products |

## Research and open-source activity

| Output | What it shows |
|---|---|
| [`mcp-rosbags`](https://github.com/binabik-ai/mcp-rosbags) (Apache-2.0, **29** stars) | Original work: LLM agents that inspect robot recordings through tools. Fits the "agentic" positioning |
| [`mcp-lab`](https://github.com/binabik-ai/mcp-lab) (Apache-2.0) | Original work: benchmarking tool-calling across LLM providers |
| Forks of `Isaac-GR00T`, `unitree_lerobot`, `unitree_sim_isaaclab` | Hands-on evaluation of VLA fine-tuning and imitation learning in Isaac Lab, on Unitree G1 |
| [`act_PickPlaceRedBlock`](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock) on Hugging Face | One ACT-style checkpoint with a custom policy type, no model card or licence |
| Papers | The team cites **200+** papers and **40+** years of combined experience (company claim). No paper published under the Binabik name was found; the Hugging Face org lists 0 papers |
| Academic base | ZHAW Centre for Artificial Intelligence; research internships and master's theses are advertised |

Reading: the open-source output is tooling and experiments, not the product. The Skill Engine, Sim and Development Kit are closed.

## What would impress this company at the hackathon

**Inference, not company statements.** Based on their positioning (teach once, reusable skills, hardware independence, supervised plans, search for new verticals).

General signals they are likely to value:
- A task **taught from one or two demonstrations** and then shown working on a changed layout or a different object.
- **Skill reuse:** the same small skill set recombined for a second task without new training.
- **The same program on two robots** (for example AgiBot G2 and Galaxea R1 Pro), which is their core claim.
- **Plan preview and human approval** before motion, plus honest failure handling when the robot is unsure.
- A credible **new vertical** with a paying user in mind; Stage II money is explicitly for exploring verticals.

| Track | Idea that maps to their stack | Why it lands |
|---|---|---|
| T01 Autonomous Urban Services | Wheeled dual-arm robot restocks or tends several service points (parcel locker, vending shelf, linen cart) from one demonstration each | "One robot, several machines" moved from the factory to city services |
| T02 Resilient & Safe City | Patrol-and-detect-change routine with an LLM agent that explains anomalies from recorded data using `mcp-rosbags` | Reuses their 2025 quadruped patrol idea and their open-source tooling; weakest fit with today's product |
| T03 Sustainable City | Sort-and-load skill for recyclables or reusable containers, re-taught for a new item in minutes | Sorting and loading are named target tasks; shows fast changeover instead of big datasets |
| T04 Elderly Care & Rehabilitation | A carer demonstrates a fetch-and-hand-over routine once (water, walking aid, towel); the robot shows its plan before acting | Healthcare is a stated interest with no deployment yet; Leukerbad's clinics make the use case concrete |

Practical tip: ask the Binabik engineers which vertical they are exploring next and shape the demo around it; a hackathon result that doubles as their first non-industrial showcase is the strongest pitch.

## Sources

- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Solutions](https://binabik.ai/solutions)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [Binabik AI — About](https://binabik.ai/about)
- [Binabik AI — Open positions](https://binabik.ai/open-positions)
- [Binabik AI — Blog](https://binabik.ai/blog)
- [Binabik AI — Contact](https://binabik.ai/contact)
- [Venture Kick — Binabik AI receives CHF 40,000 (13 Feb 2026)](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- [Switzerland Global Enterprise — Binabik establishes presence in Winterthur (14 Apr 2026)](https://www.s-ge.com/invest/en/articles/news/ai-robotics-start-binabik-establishes-presence-winterthur)
- [ERF Matchmaking 2026 — Binabik profile](https://www.b2match.com/e/erf2026/participations/705635)
- [GitHub — binabik-ai organisation](https://github.com/binabik-ai)
- [GitHub — binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags)
- [GitHub — binabik-ai/mcp-lab](https://github.com/binabik-ai/mcp-lab)
- [GitHub — binabik-ai/Isaac-GR00T](https://github.com/binabik-ai/Isaac-GR00T)
- [GitHub — binabik-ai/unitree_lerobot](https://github.com/binabik-ai/unitree_lerobot)
- [GitHub — binabik-ai/unitree_sim_isaaclab](https://github.com/binabik-ai/unitree_sim_isaaclab)
- [Hugging Face — binabik-ai/act_PickPlaceRedBlock](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock)
