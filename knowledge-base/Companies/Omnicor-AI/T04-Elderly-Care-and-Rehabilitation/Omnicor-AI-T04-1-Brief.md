---
type: challenge-brief
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Omnicor AI × T04 Elderly Care & Rehabilitation — Brief

**Fit: 3/5** — Not a care robot and no care track record, but a credible **privacy layer**: language and vision models running on the device, so no patient audio or video leaves the room. Needs another vendor's robot.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **OC Agent** (agentic deployment environment) plus **OC Node** (in-house compute box) — both ⚠️ unverified: no specs, SDK or availability are public. Use them under a robot from another vendor. |
| Strongest proof point (real deployment or demo + date) | **None in care or rehab.** Only general evidence: website (2026, undated) names AgiBot and Galbot as teams shipping with OmniCor AI and lists Apertus, Mistral, Qwen, OpenVLA and pi0.5 as models it deploys. |
| Fastest credible 48-hour demo | Offline, multilingual (DE / FR / EN) voice companion and reminder assistant running a local LLM on an edge box next to a robot — network cable unplugged on stage. |
| Biggest risk | Nothing is self-serve. If the team brings no OC Node or cannot port a model within hours, you are left with a generic open-source edge stack and no OmniCor differentiator. |
| Pairs well with (other vendors on site) | **AgiBot**, **Galbot** (listed customers) · UniX AI / Galaxea / Spirit AI (wheeled dual-arm) · D-Robotics (RDK boards) · XREAL (AR therapy) · OriginFlow (EMG) |

## Why
- **Privacy is a real selling point in care.** Health data is sensitive; "all inference stays on the device" is easy for judges and clinics to understand.
- **Offline matters in Leukerbad.** Alpine valley, thick clinic walls, guest Wi-Fi: an assistant that works with no cloud is locally relevant.
- **Multilingual local models.** The site lists Apertus (Swiss open LLM), Mistral and OpenEuroLLM — a fit for German / French / Italian speaking guests ⚠️ on-device speed unverified.
- **Robot VLAs on the list.** OpenVLA and pi0.5 (LeRobot) point at on-board manipulation policies for fetch-and-carry tasks.
- **Customer overlap on site.** AgiBot and Galbot are both here, so a joint build is plausible.

## Not a fit for
- Teams that need a ready-made robot, force-controlled contact (massage, physio) or certified medical hardware — OmniCor supplies none of it.
- Teams that want documented APIs to code against tonight — no docs, GitHub or SDK are public.
- Projects where cloud inference is acceptable — then the OmniCor layer adds little.

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Products and solutions](Omnicor-AI-T04-2-Products-and-Solutions.md) · [Playbook](Omnicor-AI-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [Omnicor AI company profile (this repo)](../Omnicor-AI.md)
