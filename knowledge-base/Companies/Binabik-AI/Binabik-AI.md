---
type: company
company: "Binabik AI"
slug: Binabik-AI
hq: "Winterthur, Switzerland"
founded: 2026
website: https://binabik.ai
categories: [software, data]
on_site_guess: "Software only: Binabik Studio / Development Kit (teach-by-demonstration skill stack) plus engineers, most plausibly running on other vendors' AgiBot G2 or Galaxea R1 Pro"
fit_t01: 3
fit_t02: 2
fit_t03: 2
fit_t04: 3
identity_confidence: high
updated: 2026-11-14
tags: [leukerbad-hackathon, company]
---
# Binabik AI

> **One-liner:** Swiss-Finnish start-up (ZHAW spin-off, founded January 2026) building a hardware-independent "agentic brain" for humanoid robots: show a task once, the software splits it into reusable skills, trains them in simulation and runs them on the robot.
> **Why it matters at Leukerbad:** Binabik has no robot of its own, but its two publicly named target platforms, **AgiBot G2** and **Galaxea R1 Pro**, are both from vendors on site. It is the candidate "skill and task layer" on top of someone else's wheeled dual-arm robot. Studio and the BDK have no public documentation (the docs portal is login-gated) and the public GitHub org holds only side tools and forks, so access depends entirely on what their team hands out on site.

## Snapshot

| Item | Detail |
|---|---|
| HQ | Technopark Winterthur, Switzerland; second office in Finland (Espoo per the contact and careers pages; the ERF listing says Turku) |
| Founded | **January 2026** (Binabik GmbH), spin-off of the ZHAW Centre for Artificial Intelligence |
| Founders / CEO | CEO Jorge Peña Queralta · CTO Pascal Sager · CFO Harry Edelmann (listed as "Harry Edelman, Co-Founder, COO" on the ERF page) · CPO Giovanni Toffetti · Robotics Lead Engineer Lei Fu |
| Size and funding | **5** people in April 2026, target **15** within 12 months; team page now lists **8**. Venture Kick **CHF 40,000** (Stage II, Feb 2026) after CHF 10,000 Stage I. No equity round is public |
| Core business | Robot-as-a-service machine tending with humanoids (Binabik Solutions) and the tooling behind it (Binabik Studio) |
| Website | https://binabik.ai |
| Docs / developer portal | Not public. `docs.binabik.ai` exists but redirects to a login; Studio is "Request access" only |
| GitHub | [github.com/binabik-ai](https://github.com/binabik-ai): 2 original MCP tools (`mcp-rosbags`, **29** stars; `mcp-lab`; both Apache-2.0) and 3 forks (Unitree LeRobot, Unitree Isaac Lab sim, NVIDIA Isaac GR00T). No Studio / BDK code |

## Portfolio at a glance

Everything is software or a service. No specs, prices or version numbers are published.

| Product | Type | Status | Key specs (verified only) | Price | Img key |
|---|---|---|---|---|---|
| Binabik Solutions | Robot-as-a-service machine tending (robot + grippers + skills + operation) | 🧪 pilots / proof of concept; no named customer | One robot tends several machines; lathe and press loading, part transport, palletizing; shown on Galaxea R1 Pro; 4-step engagement (1-day workshop → PoC → prototype → scaling) | Subscription, amount not public | binabik-ai-solutions |
| Binabik Studio | Integrated workspace: simulator + code editor + teaching tools + dev kit | 🧪 request access | Simulation, code generation and on-robot testing in one workspace; same interface for sim and real robot | not public | binabik-ai-studio |
| Binabik Teach | Demonstration capture | 🧪 part of Studio | Records all movements and camera frames of one demonstration (by hand or teleoperation) | not public | binabik-ai-teach |
| Binabik Skill Engine (also "Binabik Brain") | Task planner / skill mapper | 🧪 part of Studio | Segments a demonstration into steps and maps each to a library skill; missing skills get built and added; plans can be checked before the robot moves | not public | binabik-ai-skill-engine |
| Binabik Sim | Process simulator | 🧪 part of Studio | Models machines, fixtures and cycle times; trains skills over thousands of variations of parts, positions, lighting; uses NVIDIA SimReady factory assets; engine not named | not public | binabik-ai-sim |
| Binabik Development Kit (BDK) | Skill library + hardware abstraction API | 🧪 request access | Same skill set across robots; named platforms **AgiBot G2** and **Galaxea R1 Pro**, more planned; languages not public | not public | binabik-ai-bdk |
| Binabik Academy | Hands-on training courses | 🧪 on request | On site or in Winterthur | not public | — (no image) |

Company claim, not independently verified: "up to **85%**" greater learning efficiency (⚠️ unverified). It appears on the ERF 2026 listing only, not on the current website.

## What they will most likely bring to the hackathon

**Best guess, not confirmed.**

- **People and software, not hardware.** Binabik sells no robot. Expect engineers with laptops, Studio/BDK access and possibly their own Galaxea R1 Pro (the robot in their website imagery).
- **Most likely pairing:** their stack on an **AgiBot G2** or **Galaxea R1 Pro** provided by those vendors on site. Support for any other robot at the event (Unitree, Dobot, Flexiv and so on) is not public; ask before planning around it.
- **Likely demo content:** teach-by-demonstration pick, carry and place; humanoid interaction with people; navigation in shared space. Their earlier prototype (2025) ran on a quadruped that could patrol an area and look for changes, but the company has since narrowed to humanoids.
- **Reasoning:** an 8-person company with a "request access" product typically supports a handful of teams directly rather than handing out a self-serve SDK.

## Developer platform (summary)

- **SDK:** Binabik Development Kit (BDK), a skill library with one interface across robots. Programming languages are not public.
- **Control level:** high-level, skill and task oriented (demonstrate → segment → map to skills → execute). Low-level joint control is not described; assume it stays with the robot vendor's SDK.
- **ROS 2:** not mentioned on any product page (⚠️ unverified either way). Their open-source `mcp-rosbags` tool reads ROS 1 / ROS 2 bags, so the team works with ROS data.
- **Simulation:** Binabik Sim is process-focused (cells, fixtures, cycle times), explicitly not a reinforcement-learning sandbox. Underlying engine not named; factory assets are NVIDIA SimReady.
- **Teleoperation / data collection:** Binabik Teach records motion and camera streams from a single demonstration, by hand guiding or teleoperation. Teleop hardware not named.
- **Models:** no product model or dataset is released. One research checkpoint is public on Hugging Face (`binabik-ai/act_PickPlaceRedBlock`: ACT-style, **~51.6M** parameters, Unitree G1 simulation task, no model card or licence). Job ads mention research interest in VLA models and reinforcement learning. Positioning is "small data": few-shot or one-shot teaching instead of large datasets.
- **Compute:** earlier materials describe edge plus cloud; the site states customer and camera data stay in the factory. Hardware requirements not public.
- **Docs / GitHub:** no public docs for Studio / BDK (`docs.binabik.ai` is login-gated). The public GitHub org offers `mcp-rosbags` and `mcp-lab` (self-serve, Apache-2.0) plus three forks; details in the [developer guide](Binabik-AI-Developer-Guide.md). For the product itself, the on-site team is the documentation.
- **Questions to ask them in the first five minutes:** Which robots here can it drive today? Python API? How long from one demonstration to a running skill? Does it need internet? Can a team add its own skill?

## Current projects, deployments and customers

- **2025 (before incorporation):** software ran on a quadruped that could patrol an area and detect changes ([Venture Kick](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)).
- **Late 2025 – early 2026:** proof of concept with an **unnamed industrial partner**, humanoid deployed in realistic conditions and demonstrated to that company's leadership ([Venture Kick](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)).
- **2026-02-13:** Venture Kick Stage II, CHF 40,000 ([Venture Kick](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)).
- **By 2026-03-02:** best start-up pitch award at the Humanoid Forum in Biel/Bienne ([ZHAW](https://www.zhaw.ch/de/fokusthemen/interinterdisziplinaere-kompetenzzentren/datalab/news/newsdetail/event-news/zhaw-cai-praesentierte-physical-ai-und-robotik-am-humanoid-forum-in-biel)).
- **2026:** participant in European Robotics Forum 2026 matchmaking ([b2match](https://www.b2match.com/e/erf2026/participations/705635)).
- **2026-04-14:** move into Technopark Winterthur announced, supported by Greater Zurich Area and House of Winterthur ([S-GE](https://www.s-ge.com/invest/en/articles/news/ai-robotics-start-binabik-establishes-presence-winterthur)).
- **Current site (Nov 2026):** offering is machine tending as a service, shown on Galaxea R1 Pro (AgiBot G2 is named on the home and Studio pages); demo video still "coming soon"; no named customers ([binabik.ai/solutions](https://binabik.ai/solutions)).
- **Track-relevant deployments:** none public in urban services, safety, sustainability or care.

## Roadmap and future direction

- **Focus narrowing (2025 → 2026):** "brain for any robot body" → humanoids → one vertical (industrial machine tending, logistics and production labour shortage).
- **Feb 2026:** Stage II money is meant to explore additional verticals while keeping the existing industrial collaboration.
- **Apr 2026:** headcount plan 5 → 15 within 12 months; currently hiring robotics, perception, software/infrastructure and a Head of Go-to-Market in Winterthur.
- **Platforms:** more robots beyond AgiBot G2 and Galaxea R1 Pro are planned; none named, no dates.
- **Channel strategy:** joint offers with machine builders (machine plus robot that operates it) and system integrators using the BDK.
- **Broader ambitions (ERF profile):** lists healthcare, smart cities / infrastructure inspection, logistics, energy and others as areas of activity. These are 🔭 stated interests, not products.
- **Funding:** nothing beyond Venture Kick is public.

## Challenge fit

| Track | Fit 0–5 | Why (one line) | Best products | Go deeper |
|---|---|---|---|---|
| T01 Autonomous Urban Services | 3 | Teach-once pick, carry and place on a wheeled dual-arm robot suits a delivery or maintenance demo, if the team gets access and a supported robot | Studio (Teach + Skill Engine), BDK | [T01 brief](T01-Autonomous-Urban-Services/Binabik-AI-T01-1-Brief.md) |
| T02 Resilient & Safe City | 2 | Only an early quadruped patrol prototype points this way; current product is indoor manipulation | Skill Engine, BDK | [T02 brief](T02-Resilient-and-Safe-City/Binabik-AI-T02-1-Brief.md) |
| T03 Sustainable City | 2 | Sorting and loading skills could support a waste-sorting demo, nothing purpose-built | Studio, Binabik Sim | [T03 brief](T03-Sustainable-City/Binabik-AI-T03-1-Brief.md) |
| T04 Elderly Care & Rehabilitation | 3 | Fetch-and-carry with human interaction taught by a carer's single demonstration is a credible 48-hour story; no care deployment exists | Teach, Skill Engine, BDK | [T04 brief](T04-Elderly-Care-and-Rehabilitation/Binabik-AI-T04-1-Brief.md) |

Scores assume Binabik grants hands-on access during the event. Without that, every track drops to 1, because nothing is self-serve.

## Related docs
- [Product portfolio](Binabik-AI-Products.md) · [Developer guide](Binabik-AI-Developer-Guide.md) · [Roadmap and strategy](Binabik-AI-Roadmap-and-Strategy.md)
- [Start here — all companies and tracks](../../00-START-HERE.md)

## Verification log (2026-11-14)

Re-checked against live sources on 2026-11-14. Web search was unavailable (quota), so checks are direct page reads; news after April 2026 outside these pages could be missing.

- ✔ confirmed — Founded **January 2026** as a ZHAW Centre for AI spin-off; Technopark Winterthur move announced 14 Apr 2026; **5** people, plan for **15** in 12 months. [S-GE](https://www.s-ge.com/invest/en/articles/news/ai-robotics-start-binabik-establishes-presence-winterthur)
- ✔ confirmed — Venture Kick Stage II **CHF 40,000** on 13 Feb 2026, after a CHF 10,000 Stage I. [Venture Kick](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- ✔ confirmed — Earlier software ran on a quadruped ("patrol an area or look for changes"); humanoid proof of concept with an unnamed industrial partner. [Venture Kick](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- ✎ corrected — Proof-of-concept timing: it happened during the three months of Stage I, not three months after it (fixed in the roadmap doc). [Venture Kick](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- ✔ confirmed — Leadership names and roles (CEO Jorge Peña Queralta, CTO Pascal Sager, CFO Harry Edelmann, CPO Giovanni Toffetti, Lead Engineer Lei Fu); team of **8**; "40+ years" and "200+ papers" are company claims. [binabik.ai/about](https://binabik.ai/about)
- ✔ confirmed — Product names: Solutions, Studio, Teach, Skill Engine, Sim, Development Kit (home page); "Binabik Brain" (Solutions page); "BDK" and Academy (Studio page). [binabik.ai](https://binabik.ai) · [Solutions](https://binabik.ai/solutions) · [Studio](https://binabik.ai/studio)
- ✔ confirmed — Only named robot platforms are **AgiBot G2** and **Galaxea R1 Pro**; more platforms "as the market moves", none named. [binabik.ai](https://binabik.ai)
- ✔ confirmed — Studio is "Request access" only; "same API we use"; "first demonstration to a running robot in days"; no programming language, ROS or price stated. [binabik.ai/studio](https://binabik.ai/studio)
- ✔ confirmed — Binabik Sim is "not a reinforcement-learning sandbox"; factory assets are NVIDIA SimReady (CC BY 4.0); engine not named. [binabik.ai/studio](https://binabik.ai/studio)
- ✔ confirmed — Solutions: one subscription; 1-day workshop → proof of concept → prototype → scaling; "first application in months, follow-ups in days"; data stays in the factory; three gripper types; video "coming soon"; no customer named. [binabik.ai/solutions](https://binabik.ai/solutions)
- ✎ corrected — GitHub: the profile and four track docs said no official org was found. It exists: `mcp-rosbags` (29 stars, Apache-2.0), `mcp-lab` (5 stars, Apache-2.0) and three forks; no Studio / BDK code. [github.com/binabik-ai](https://github.com/binabik-ai)
- ✎ corrected — "No pretrained model released": one research checkpoint is public (2 Jul 2026, ~51.6M parameters, policy type `binabik_act`, chunk size 50, 16-D state and action, three 640×480 cameras, Unitree G1 simulation dataset). Developer-guide figures confirmed; profile and track docs updated. [Hugging Face](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock)
- ✎ corrected — Docs portal: `docs.binabik.ai` exists and redirects to a login (the profile only said "not public"). [docs.binabik.ai](https://docs.binabik.ai)
- ✎ corrected — Finland office is in Espoo per the company's own contact page; only the ERF listing says Turku. [binabik.ai/contact](https://binabik.ai/contact)
- ⚠ unverified — "Up to 85%" learning-efficiency figure: found only as a company statement on the ERF listing, not on the website and with no evidence behind it; wording aligned across docs. [b2match](https://www.b2match.com/e/erf2026/participations/705635)
- ✔ confirmed — Best start-up pitch award at the Humanoid Forum, Biel/Bienne (article dated 2 Mar 2026). [ZHAW](https://www.zhaw.ch/de/fokusthemen/interinterdisziplinaere-kompetenzzentren/datalab/news/newsdetail/event-news/zhaw-cai-praesentierte-physical-ai-und-robotik-am-humanoid-forum-in-biel)
- ✔ confirmed — ERF 2026 listing: tagline "The Agentic Operating System for Physical AI"; Turku and Winterthur; activity areas include healthcare, smart cities and infrastructure inspection, defense and security, energy and utilities, agri-tech. [b2match](https://www.b2match.com/e/erf2026/participations/705635)
- ✔ confirmed — Hiring: 8 listed roles, all in Winterthur, plus open applications for Winterthur or Espoo; VLA models and reinforcement learning mentioned. [binabik.ai/open-positions](https://binabik.ai/open-positions)
- ⚠ unverified — Absence claims (no formal AgiBot / Galaxea partnership, no funding beyond Venture Kick, no named customer, no track-relevant deployment): nothing contradicting them on the official pages, but a news search could not be run. [binabik.ai](https://binabik.ai)

Structure fixes in the same pass: removed a broken Academy image reference (T03 products doc and the Img key above), moved navigation lines above "Sources" in three briefs, corrected the contact-form topic name in the developer guide.

## Sources
- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Solutions](https://binabik.ai/solutions)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [Binabik AI — Team](https://binabik.ai/team)
- [Binabik AI — Open positions](https://binabik.ai/open-positions)
- [Binabik AI — About](https://binabik.ai/about)
- [Binabik AI — Contact](https://binabik.ai/contact)
- [Binabik AI — docs portal (login required)](https://docs.binabik.ai)
- [GitHub — binabik-ai organisation](https://github.com/binabik-ai)
- [Hugging Face — binabik-ai/act_PickPlaceRedBlock](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock)
- [Venture Kick — Binabik AI receives CHF 40,000 (13 Feb 2026)](https://www.venturekick.ch/Binabik-AI-receives-CHF-40000-from-Venture-Kick-to-accelerate-humanoid-deployment-across-industries)
- [Switzerland Global Enterprise — Binabik establishes presence in Winterthur (14 Apr 2026)](https://www.s-ge.com/invest/en/articles/news/ai-robotics-start-binabik-establishes-presence-winterthur)
- [ERF Matchmaking 2026 — Binabik profile](https://www.b2match.com/e/erf2026/participations/705635)
- [ZHAW — CAI at the Humanoid Forum in Biel (2 Mar 2026)](https://www.zhaw.ch/de/fokusthemen/interinterdisziplinaere-kompetenzzentren/datalab/news/newsdetail/event-news/zhaw-cai-praesentierte-physical-ai-und-robotik-am-humanoid-forum-in-biel)
