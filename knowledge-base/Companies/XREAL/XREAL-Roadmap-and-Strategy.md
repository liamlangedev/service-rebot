---
type: roadmap
company: "XREAL"
slug: XREAL
updated: 2026-11-14
tags: [leukerbad-hackathon, roadmap]
---
# XREAL — Roadmap and Strategy

⬆ [XREAL profile](XREAL.md) · [Product portfolio](XREAL-Products.md) · [Developer guide](XREAL-Developer-Guide.md)

> Research note: live web search was unavailable for this file. It is built from direct reads of the sources listed at the end (trade press, official docs, GitHub) plus the profile. **Nothing after the 28 Oct 2026 AURA launch has been checked** — in particular the Hong Kong listing outcome and AURA's European date.

## Company trajectory

Rows marked † are background knowledge, not re-checked against a source today.

| Date | Milestone |
|---|---|
| 2017 | Founded as **Nreal** in Beijing by Dr. Chi Xu (Xu Chi) |
| 2019–2022 † | Nreal Light (first consumer AR glasses with cameras), then the Air line of lightweight display glasses |
| 2023 † | Renamed **XREAL**; Air 2 / Air 2 Pro |
| Mar 2024 | **Air 2 Ultra** ships — 6DoF developer-oriented glasses (USD 699) |
| 2024 † | **Beam Pro** Android host; first **One series** glasses with the in-house **X1** spatial chip (late 2024) |
| May 2025 | **USD 28.6M** round led by Pudong Venture Capital |
| May 2025 † | **Project Aura** with Google (Android XR) first announced |
| 25 Nov 2025 | **XREAL SDK 3.1.0** — 6DoF on One series via the XREAL Eye camera |
| Jan 2026 (CES) | **XREAL 1S** (USD 449), **Neo** power / video hub, **ROG XREAL R1** with ASUS (240 Hz); multi-year extension of the Google partnership — XREAL named **lead hardware partner for Android XR** on optical see-through devices |
| Jan 2026 | **USD 100M** round at a reported **USD 1B** valuation (supply-chain partners among investors); about **USD 433M** raised in total |
| 1 Apr 2026 | **Hong Kong main-board IPO application** (sponsors CICC, Citi). 2025 revenue about **RMB 516M** (+30.8% YoY), gross margin up from under 20% to **above 35%** (2023→2025), **>70% of revenue overseas** |
| 19 May 2026 | Google I/O: Android XR developer early-access programme for Aura hardware |
| 16 Jun 2026 | Unity 6.5 adds AURA support (first XR glasses supported by Unity on Android XR) |
| 15 Oct 2026 | **XREAL 1 Pro+** on sale (USD 599) |
| 28 Oct 2026 | **XREAL AURA** launches (from USD 1,279; promo USD 1,099); first batch ships **mid-Nov 2026** in US, Canada, Japan, South Korea |

## Current focus projects

| Focus | What is happening now | Evidence |
|---|---|---|
| **AURA rollout** | First shipments this month; 150+ made-for-XR apps; Best Buy + own US shop; accessories (GameSir controller, keyboard) | Road to VR, 28 Oct 2026 |
| **Android XR ecosystem** | Lead hardware partner; developer programme with Google; Unity support live | GamesBeat, Unity blog |
| **One-series refresh** | 1S (entry), 1 Pro+ (flagship, 1,200 nits), R1 (gaming with ASUS) — all on the in-house X1 chip | Profile sources |
| **In-house silicon** | X1 on glasses; **X1S** co-processor inside the AURA puck next to Snapdragon Reality Elite | Road to VR |
| **Capital markets** | HKEX listing targeted **by end of 2026** (CEO statement, Jun 2026). Outcome ⚠️ unverified | Caixin, UC Today |
| **Budget sub-brand (XBX)** | Listed in site navigation; details ⚠️ unverified | Profile |
| **Developer SDK for One series** | SDK 3.1.0 is a year old; docs do not yet cover 1 Pro+ or AURA; Android 16 incompatibility still flagged | docs.xreal.com |

Not a focus (no public evidence): robotics, teleoperation, healthcare, industrial or public-sector deployments.

## Announced and upcoming products

| Item | Status | Timing |
|---|---|---|
| AURA — first-wave deliveries (US, CA, JP, KR) | ✅ / shipping starts | mid-Nov 2026 |
| AURA — **Europe** | 🧪 announced as a later wave | "soon after" the first wave per the profile's sources; no date. Expect few or no retail units in Switzerland today |
| AURA — wider retail incl. select **Google Store** locations (US, Japan) | 🧪 | 2027 |
| Hong Kong listing | 🧪 filed 1 Apr 2026 | target end-2026; ⚠️ unverified whether completed |
| ROG XREAL R1 | ✅ pre-orders opened; announced to ship H1 2026 | actual ship date ⚠️ unverified |
| Subscription / AI-assistant revenue | 🔭 concept mentioned by the CEO | no date |
| Next One-series generation, next X-chip | not public | — |
| SDK update covering 1 Pro+ / Android 16 | not public | — |
| Robotics or teleoperation SDK | not public (nothing announced) | — |

## Strategic direction and markets

- **Positioning:** consumer "wearable display" maker for entertainment, gaming and productivity — explicitly **not** enterprise headsets. Lightweight glasses tethered to phones, PCs, consoles.
- **Two product lines:** (1) affordable display glasses with own chips (One series, XBX); (2) premium spatial computing on **Android XR + Gemini** (AURA).
- **AI thesis (CEO, Jun 2026):** glasses are the natural always-on carrier for AI because they see what the user sees; he forecasts **20% penetration by 2030** from under 1% today. Revenue is hardware-only now.
- **Platform dependence by design:** the CEO's view is that only Google and Apple can build a global device ecosystem — XREAL rides Google's.
- **Markets:** sales in about **40 countries and regions**; North America (US largest), Europe and parts of Asia named as key markets. Claims **No. 1 in AR-glasses revenue since 2022** and No. 2 in the wider smart-glasses market in 2025 (company-cited).
- **Europe / Switzerland:** Europe is a sales market (online store and retail). **Swiss office, Swiss partners or Swiss pilots: none found / not public.** AURA is not yet sold in Europe.
- **Partners:** Google (Android XR, Gemini), Qualcomm (Snapdragon Reality Elite), ASUS ROG (R1), Bose (audio), Unity (engine support), GameSir (controller), Sony (micro-OLED panels).
- **Funding:** about **USD 433M** total; Jan 2026 round USD 100M at USD 1B; investors include unnamed supply-chain partners; earlier backer Pudong Venture Capital.
- **Risks the company itself names:** US export controls, tariffs and trade policy; it says it is diversifying supply chain and channels.

## Research and open-source activity

| Area | Finding |
|---|---|
| GitHub ([nreal-ai](https://github.com/nreal-ai)) | **7 public repos**, mostly legacy: NRSDK-MRTK-Samples (58 stars, 2023), MRTK and WebXR forks. Only recent activity: `uvc_android` ("uvc test with puck", Jun 2026). The SDK is a closed tarball download |
| SDK cadence | 3.0.0 → **3.1.0 (25 Nov 2025)**; no newer release visible in the docs as of today |
| In-house R&D | Spatial co-processors **X1 / X1S**, optics (prism-style see-through, 70° FOV on AURA), SLAM / 6DoF tracking |
| Academic output by XREAL | None found for robotics or embodied AI |
| Third-party research using XREAL | "ActiveGlasses" (arXiv 2604.08534, Apr 2026) — egocentric demonstration capture with smart glasses for manipulation learning; academic, not an XREAL project |
| Open standards | AURA sits on OpenXR via Android XR; XREAL SDK plugs into Unity AR Foundation / XR Hands rather than exposing OpenXR directly |
| Models / datasets | None released |

Takeaway: XREAL is a hardware and silicon company with a thin open-source footprint. Anything robotics-related you build is new ground for them.

## What would impress this company at the hackathon

**Inference — not stated by XREAL.** Based on its strategy (AI on glasses, Android XR ecosystem growth, consumer comfort, looking for use cases beyond video and gaming).

What likely lands well in general:

- A demo where the glasses are **worn for the whole task**, hands free — showing why light see-through glasses beat a VR headset or a tablet.
- Use of what is **new**: Eye-based 6DoF + RGB camera on One series, or hands / Gemini on AURA.
- A **non-entertainment use case** with a clear user — XREAL has none in public today.
- Clean engineering on their stack that they could show to other developers (small open-source bridge, e.g. "XREAL head pose → ROS 2").

| Track | Idea that fits XREAL's direction | Pairs with |
|---|---|---|
| **T01 Autonomous Urban Services** | One supervisor wearing glasses oversees several delivery / maintenance robots: world-fixed status cards, glance-to-select, takeover view from the robot camera | Quadrupeds or wheeled mobile manipulators (Unitree, AGIBOT, Galaxea) |
| **T02 Resilient & Safe City** | Hands-free incident HUD for a mountain-rescue or infrastructure operator: quadruped camera feed + map in the glasses, **head pose steers the robot camera**, first-person view streamed to a remote expert | Go2 / B2-class quadruped; SKYLANDX scans as the map layer |
| **T03 Sustainable City** | See-through guidance for sorting or inspection: robot-detected item classes or sensor readings shown in the worker's view; glasses RGB frames feed the classifier | Cobot arm vendors (Dobot, ROKAE, Flexiv) |
| **T04 Elderly Care & Rehabilitation** | Therapist glasses showing live joint angles / force from a rehab robot while keeping eye contact with the patient; or a caregiver "see what I see" assist using Eye first-person streaming — strong Leukerbad clinic relevance | Force-controlled arms (Flexiv, ROKAE), OriginFlow EMG as an input signal |

Bonus points (inference): an **egocentric data-collection rig** (glasses RGB + 6DoF head pose, logged for robot learning) — it connects XREAL to the embodied-AI data trend that the other vendors on site care about.

## Sources

- [GamesBeat — XREAL raises USD 100M (15 Jan 2026)](https://gamesbeat.com/xreal-raises-100m-to-accelerate-ar-glasses-rollout/)
- [UC Today — XREAL files for Hong Kong IPO (10 Apr 2026)](https://www.uctoday.com/devices-workspace-tech/xreal-files-for-hong-kong-ipo-as-smart-glasses-race-intensifies/)
- [Caixin Global — XREAL founder interview (3 Jun 2026)](https://www.caixinglobal.com/2026-06-03/xreal-founder-bets-ai-will-push-smart-glasses-beyond-hype-102450675.html)
- [Road to VR — XREAL AURA launch and pricing (28 Oct 2026)](https://www.roadtovr.com/google-ar-glasses-xreal-aura-release-date-price/)
- [Unity blog — Unity support for XREAL AURA (16 Jun 2026)](https://unity.com/blog/unity-android-xr-wired-glasses-support)
- [XREAL docs — SDK 3.1.0 release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.1.0)
- [XREAL docs — Compatibility](https://docs.xreal.com/XREALDevices/Compatibility)
- [GitHub — nreal-ai organisation](https://github.com/nreal-ai)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/abs/2604.08534)
- [XREAL profile in this vault (further sources listed there)](XREAL.md)
