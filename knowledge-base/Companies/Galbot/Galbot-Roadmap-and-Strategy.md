---
type: roadmap
company: "Galbot"
slug: Galbot
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# Galbot — Roadmap and Strategy

⬆ [Galbot profile](Galbot.md) · [Product portfolio](Galbot-Products.md) · [Developer guide](Galbot-Developer-Guide.md)

**Read this in 20 seconds:** Galbot is a well-funded (about **US$1.15B** raised, valuation above **RMB 22B**) Beijing company whose money comes from robots doing real shifts in retail, pharmacy and factories. Its bet is "synthetic data + one brain, many bodies". It has **no announced European or Swiss operation**; the visible route abroad is industrial, through Bosch. Research note: web search was unavailable while writing this file, so it rests on the official site, GitHub, the developer portal, TechNode, Sacra, The Robot Report and the company profile; items not re-checked are marked.

## Company trajectory

| Date | Milestone |
|---|---|
| 2023-05 | Company founded in Beijing |
| 2023–2024 | Angel funding of about RMB 700M; strategic round of about RMB 500M in 2024 (Sacra) |
| 2025-05 | GraspVLA paper published (arXiv 2505.03233): grasping model pretrained only on synthetic data |
| 2025-06 | **RMB 1.1B** round led by CATL; valuation passes US$1B |
| 2025-07-25 | GraspVLA weights, simulation playground and real-robot controller open-sourced |
| 2025-09 | OpenTrack humanoid motion-tracking codebase released |
| 2025-12 | Round of **more than US$300M at about US$3B valuation**; total raised about US$800M; investors from China, Singapore and the Middle East. Autonomous "Galbot Store" retail in 30+ Chinese cities |
| 2026-01 | S1 heavy-duty industrial robot launched (reported) ⚠️ unverified date; CES 2026 presence |
| 2026-03 | **RMB 2.5B** round (state AI / industry funds, Sinopec, CITIC-affiliated and others). S1 reported accepted at CATL's Ningde base ⚠️ unverified |
| 2026 (spring) | Hannover Messe 2026 presence |
| 2026-06 | SDK 1.9.0 / 1.9.1: richer navigation APIs, S1 perception, more dexterous hands |
| 2026-08 | ET1 small biped unveiled at WRC Beijing (first legged product); SynGrasp-1B dataset released (08-19); "AstraTennis" autonomous humanoid tennis (08-23); three golds at a humanoid robot sports event (08-26); valuation reported above RMB 22B |
| 2026-09-03 | ET1 pre-orders open, marketed as the first "agent-native" robot |
| 2026-09-22 | SDK 1.10.0: software e-stop, new planning APIs, **"G3" model**, **Jetson AGX Thor** support |
| 2026-09-28 | G1 enters regular operation at a Laobaixing Pharmacy store in Shanghai |
| 2026-10-01 | Joint research wins a best-paper award at IROS 2026 |

Source note on the March 2026 round: TechNode names the National Artificial Intelligence Industry Investment Fund; Sacra names the China Integrated Circuit Industry Investment Fund. The fund identity is therefore ⚠️ unverified; amount and date agree.

## Current focus projects

- **Retail and pharmacy at scale.** G1 runs robot-operated kiosks ("Space Capsule", 170+ locations in 40+ cities per the official site) and 24/7 picking in instant-retail warehouses and pharmacies. The September 2026 Shanghai pharmacy launch shows the model is now human-robot collaboration inside ordinary stores, not only sealed kiosks.
- **Factory work with S1 and G1.** Handling, palletising and machine loading for CATL and automotive customers (Bosch, Toyota, BAIC, SAIC named in press; Hyundai named by The Robot Report as explored). Company claims orders for "thousands of units" ⚠️ unverified.
- **Developer ecosystem as a product.** Since 2026 Galbot sells access in three layers: L1 tools (SDK, docs, sim assets), L2 scenario kits (welcome / guide live; material sorting "coming soon"; site inspection "planned"), L3 turnkey solutions (retail capsule, industrial handling, **education packages for universities**).
- **One brain across bodies.** AstraBrain is presented as a stack: WAM (general world-action model), WBC (whole-body "cerebellum", open as Humanoid-GPT), Dex (dexterous-hand world model), with a 3B–13B "cerebrum" at 5–10 Hz and an 80–300M "cerebellum" at 100–250 Hz (company figures).
- **Legged humanoids as showcase.** Tennis, sports-event wins and ET1 are built on whole-body tracking research (OpenTrack, LATENT, Humanoid-GPT), mostly demonstrated on third-party humanoids until ET1.

## Announced and upcoming products

| Item | Status | Date / detail |
|---|---|---|
| Galbot ET1 deliveries | 🧪 pre-order since 2026-09-03 | Delivery schedule not public |
| "G3" robot model | 🧪 appears in SDK 1.10.0 (2026-09-22) | No product page, no specs ⚠️ unverified what it is |
| Jetson AGX Thor compute option (128 GB) | 🧪 supported in SDK 1.10.0 | Which robots ship with it: not public |
| Material-sorting kit (G1, S1) | 🧪 "coming soon" on developer portal | No date |
| Site-inspection kit (G1, S1) | 🔭 "planned" on developer portal | No date |
| More SDK business modules (beyond SPS sorting and bin handling) | 🔭 "under continuous development" | No date |
| Humanoid-GPT training code and data | 🔭 listed as TODO in the repo | No date |
| GroceryVLA / TrackVLA / NavFoM public release | 🔭 not announced | Used in products and papers only |
| IPO | 🔭 press speculation | No filing confirmed ⚠️ unverified |

## Strategic direction and markets

| Theme | What the evidence says |
|---|---|
| Core thesis | Pretrain on huge synthetic datasets, fine-tune on a small amount of real data, ship full-stack (data, model, hardware in-house) |
| Revenue logic | Sell robots plus recurring fees: vertical solutions, and developer subscriptions at ¥50,000 (Pro) or ¥200,000 (Enterprise) per robot per year |
| Priority verticals | Retail and pharmacy (most mature), manufacturing and logistics (growing fastest), then healthcare, services and education |
| Healthcare | Research cooperation with Xuanwu Hospital (wards, pharmacy, guidance). **No elderly-care or rehabilitation product announced** |
| Funding | About **US$1.15B** lifetime (Sacra); backers include CATL (also a customer), Chinese state-linked industry funds, Sinopec, CITIC, SAIC's finance arm, Bank of China, and Singapore / Middle East investors |
| Partnerships | CATL (investor + factory customer); Bowintec joint venture with a Bosch-linked investment platform, aimed at factory tasks including outside China; pharmacy chains (Laobaixing; Neptunus reported ⚠️ unverified) |
| International | Stated use of the Dec 2025 round includes "expanding global reach", without named markets. Trade-show presence at CES and Hannover Messe 2026. Hong Kong retail stores reported ⚠️ unverified. Enterprise support tier explicitly offers on-site engineers in China **and abroad** |
| **Europe / Switzerland** | **No office, distributor, deployment or programme found.** The plausible entry is following industrial customers (Bosch) into European plants. Presence at Leukerbad is itself a signal that Galbot is scouting European developers and research partners (inference) |
| Competitive position (inference) | Among wheeled dual-arm vendors on site (Galaxea, AGIBOT G-series, Spirit AI, UniX AI), Galbot has the strongest record of unattended 24/7 commercial operation; weaker on open community and Western developer mindshare |

## Research and open-source activity

- **Founder-led academic pipeline:** CEO Wang He holds a Peking University post; many releases are joint with PKU, Tsinghua and other Chinese universities.
- **GitHub org `GalaxyGeneralRobotics`:** about 18 public repositories, most Apache-2.0.

| Release | Venue / date | What it is | Open? |
|---|---|---|---|
| GraspVLA + SynGrasp-1B | arXiv 2025-05; model 2025-07; dataset 2026-08 | Synthetic-data grasping VLA; billion-frame dataset | ✅ code, weights, data |
| OpenWBT | 2025 | Whole-body humanoid teleoperation | ✅ |
| OpenTrack (Any2Track) | 2025-09, updates to 2026-05 | Humanoid motion tracking, MuJoCo-JAX; real-world deployment code | ✅ |
| LATENT | repo 2026-04 | Athletic humanoid tennis skills from imperfect human motion data | ✅ |
| Humanoid-GPT (AstraBrain-WBC 0.5) | CVPR 2026 | GPT-style motion transformer pretrained on 2B frames | ✅ inference + checkpoints; training code pending |
| Click-and-Traverse | repo updated 2026-07 | Research code (topic not checked here ⚠️ unverified) | ✅ |
| UrbanVLA | ICRA 2026 | VLA for urban micromobility navigation | ✅ |
| HumanTracker | ECCV 2026 | Human-aligned motion-tracking benchmark + dataset | ✅ |
| RoboGesture | ECCV 2026 | Real-time co-speech gesture generation for humanoid interaction | ✅ |
| GalbotSDK, description packages, mcap2lerobot | 2026 | Product developer tooling | ✅ |

- **Pattern:** research code is opened generously for *humanoid whole-body control* (mostly on Unitree hardware), while the *commercial manipulation models* running on G1 in shops (GroceryVLA and successors) stay closed.
- **2026 direction of travel:** from grasping → whole-body athletic skills → human interaction (gestures, agent-native ET1).

## What would impress this company at the hackathon

**Inference from the strategy above, not company statements.**

| Signal Galbot cares about | How to show it in 48 h |
|---|---|
| **Unattended reliability** (their brand is 24/7 operation) | Run the same task 20 times in a row and report the success rate and failure causes. A boring, repeatable demo beats a one-off spectacular one |
| **New verticals for the same pick-fetch-hand-over skill** | Reuse the retail / pharmacy pattern in a setting they have not productised |
| **Use of their SDK layers as intended** | Built-in planning + navigation + force/torque wrists, with your own perception or policy plugged in through the documented VLA interface |
| **Material for the unreleased kits** (sorting, inspection) | A working prototype of a sorting or inspection flow is exactly what their L2 roadmap lacks |
| **A European / care use case** | They have none; a credible Swiss scenario gives them a story to take home |

Track-specific angles:

- **T01 Autonomous Urban Services:** an unattended micro-kiosk or hotel / clinic concierge: guest asks by voice, G1 picks the item from a shelf and hands it over. Add restocking detection. Closest to Galbot's core business, so judge on reliability and a twist (multilingual guests, after-hours pharmacy pick-up for a mountain village).
- **T02 Resilient & Safe City:** indoor only. Emergency-supply depot robot that kits and hands out avalanche or first-aid packs on request, or a patrol that checks cabinets, extinguishers and exits (this is the "site inspection" kit they have not shipped). Pair with a quadruped from another vendor for outdoor legs.
- **T03 Sustainable City:** open-vocabulary sorting of returns, deposit bottles or spa-hotel waste streams with a measured purity rate (maps to the "material sorting" kit marked coming soon); shelf-life-aware restocking to cut food waste.
- **T04 Elderly Care & Rehabilitation:** medication and item fetching for a rehab-clinic ward: verify the item (barcode or label read with the wrist camera), deliver to the bedside, hand over gently using the wrist force/torque sensors, log the hand-over. Stay inside the 5 kg-per-arm limit and avoid any physical patient support. This extends their pharmacy stack into care, where they have research ties (Xuanwu Hospital) but no product.

## Sources

- [Galbot official site (news list, AstraBrain section)](https://www.galbot.com)
- [Galbot About page](http://www.galbot.com/about/)
- [Galbot developer platform (product layers, kits, subscription tiers)](https://developer.galbot.com/?lang=en)
- [GitHub org GalaxyGeneralRobotics](https://github.com/GalaxyGeneralRobotics)
- [GalbotSDK CHANGELOG](https://raw.githubusercontent.com/GalaxyGeneralRobotics/GalbotSDK/HEAD/CHANGELOG.md)
- [GraspVLA repository (release dates, SynGrasp-1B)](https://github.com/PKU-EPIC/GraspVLA)
- [GraspVLA paper (arXiv 2505.03233)](https://arxiv.org/abs/2505.03233)
- [Humanoid-GPT repository](https://github.com/GalaxyGeneralRobotics/Humanoid-GPT)
- [OpenTrack repository](https://github.com/GalaxyGeneralRobotics/OpenTrack)
- [HumanTracker repository](https://github.com/GalaxyGeneralRobotics/HumanTracker)
- [TechNode, 2026-08-27: Galbot's industrial AI journey](https://technode.com/2026/08/27/how-far-are-robots-from-actually-working-on-production-lines-galbots-industrial-ai-journey/)
- [The Robot Report, 2025-12-23: Galbot brings in $300M](https://www.therobotreport.com/galbot-brings-in-300m-to-scale-mobile-manipulator-deployments/)
- [Sacra: Galbot company profile](https://sacra.com/c/galbot/)
- [Galbot company profile in this pack](Galbot.md)
