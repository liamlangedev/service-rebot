---
type: challenge-brief
company: "XREAL"
slug: XREAL
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# XREAL × T02 Resilient & Safe City — Brief

**Fit: 3/5** — A good hands-free operator interface (HUD, head-pose input, first-person video link) for someone else's robot; XREAL has no robot, no rugged device and no public safety deployments.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **One-series glasses (One Pro / 1 Pro+ / 1S) + XREAL Eye + Beam Pro**: plug-in HUD on any USB-C DisplayPort host; with the SDK, 6DoF head pose + RGB frames + first-person streaming. **Air 2 Ultra** or **AURA** if you need anchors / hand tracking |
| Strongest proof point (real deployment or demo + date) | No XREAL safety / rescue / inspection deployment found. Closest: **ActiveGlasses** (arXiv, Apr 2026) — researchers used Air 2 Ultra 6DoF head pose to drive a camera-carrying robot arm (with a Flexiv Rizon4) |
| Fastest credible 48-hour demo | Patrol quadruped streams camera + alerts to a laptop; operator sees it in the glasses as a **head-up console**, hands free for the gamepad. No XREAL SDK code |
| Biggest risk | SDK path = Unity + Android host (Beam Pro / Samsung S24–S25, **not Android 16**). One + Eye gives **6DoF only** — no hand tracking, planes, anchors. Consumer hardware, cable-tethered, no IP rating found |
| Pairs well with (other vendors on site) | Unitree Go2 / B2, AGIBOT D1, Magiclab MagicDog, Genisom M1 / L1 (scout robots) · SKYLANDX MetaCam (3D map) · D-Robotics RDK (edge video) · Flexiv (head-driven camera arm) |

## Why
- **Hands-free situational awareness** is a real responder need: watch the robot's feed without looking down at a tablet.
- **Lowest integration cost on site**: every model is a USB-C external display — your existing web / RViz UI just appears in the glasses.
- **Head pose as input**: 6DoF via Eye or Air 2 Ultra — look around to steer a robot's camera.
- **Documented first-person streaming** (One + Eye → Windows receiver on the same LAN) gives a command-post "see what I see" link.
- **1 Pro+ at 1,200 nits** is the most usable model on snow / outdoors; glasses weigh **82–95 g**.

## Not a fit for
- Teams wanting XREAL as the **core platform** — it cannot sense hazards, move or act.
- Claims about **rugged, gloved, wet or sub-zero** field use — nothing public supports them.
- Teams with **no Unity / Android skills** who still want 6DoF or anchors in 48 hours.

⬆ [XREAL profile](../XREAL.md) · [Products and solutions](XREAL-T02-2-Products-and-Solutions.md) · [Playbook](XREAL-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
