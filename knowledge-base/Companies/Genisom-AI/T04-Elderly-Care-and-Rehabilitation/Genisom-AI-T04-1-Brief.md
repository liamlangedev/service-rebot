---
type: challenge-brief
company: "Genisom AI"
slug: Genisom-AI
challenge: T04
challenge_title: "Elderly Care & Rehabilitation"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, brief]
---
# Genisom AI × T04 Elderly Care & Rehabilitation — Brief

**Fit: 2/5** — A rugged robot dog that can follow, carry, patrol and guide, but has no arm, no force-safe contact and no care product; a supporting or "mobile companion" role only.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Genisom L2** (GLUE UWB + vision person-following, **16 kg** payload, RoamerX multi-floor navigation) or **M1 Pro** (voice dialogue + following). **L1 EDU** if that is what is on site (Orin NX, LiDAR, depth camera). On-site models are not confirmed. |
| Strongest proof point | Official "Accessibility & Public Services" application area with two **Smart Guide Dog** cases (Mianyang, HIT Suzhou) — titles only, no dates or details public. Plus M1 paced a **21 km** half marathon by autonomous following (2026). |
| Fastest credible 48-hour demo | Night-round robot: patrols a corridor, spots a person on the floor with a pose model, calls the caregiver with photo and location. |
| Biggest risk | Safety and acceptance: a legged robot close to frail people, with no certified safe-contact behaviour. SDK is **C++ only** and it is unclear whether following and voice are callable from it. |
| Pairs well with | D-Robotics (extra edge vision), XREAL (caregiver view), OriginFlow (EMG / gesture commands), SKYLANDX (fast 3D map of the clinic), Galaxea / Galbot (arm loads, dog carries) |

## Why
- Follow-and-carry is a product feature (L2 GLUE, M1 Pro UWB + laser-vision), so "walk with me and carry my things" is realistic.
- Handles stairs, slopes and wet or snowy paths (L2 IP66, M1 IP67, both −20 to 55 °C) — relevant between Leukerbad clinics, hotels and thermal baths.
- Open stack shortens the build: C++ SDKs, RoamerX (ROS 2 Nav2), MATRiX simulator, vision-language navigation baseline.
- The company itself names guidance and accessible mobility as an application area, but calls it exploratory.

## Not a fit for
- Anything that touches the patient: feeding, dressing, transfer, massage, physiotherapy with force control.
- Fetch-and-place tasks (TA01 arm has no public specs or product page).
- Teams wanting Python-first or a manipulation foundation model.

## Sources
[Emerging Applications page](https://www.genisomai.com/en/industry/emerging-applications) · [L2 page](https://www.genisomai.com/en/product-robot/L2) · [M1 page](https://www.genisomai.com/en/product-robot/M1) · [L1 page](https://www.genisomai.com/en/product-robot/L1) · [GEN2 SDK](https://github.com/zsibot/genisom_robot_sdk) · [L1 SDK](https://github.com/zsibot/genisom_L1_sdk)

⬆ [Genisom AI profile](../Genisom-AI.md) · [Products and solutions](Genisom-AI-T04-2-Products-and-Solutions.md) · [Playbook](Genisom-AI-T04-3-Playbook.md) · [Track overview](../../../Challenges/T04-Elderly-Care-and-Rehabilitation/T04-0-Track-Overview.md)
