---
type: challenge-brief
company: "XREAL"
slug: XREAL
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# XREAL × T03 Sustainable City — Brief

**Fit: 2/5** — Supporting role only: XREAL is the human-interface layer (HUD, egocentric camera, in-situ data overlay) for someone else's robot; it has no sustainability product, deployment or robot of its own.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **One-series glasses (One Pro / 1 Pro+) + XREAL Eye + Beam Pro** — 6DoF, spatial anchors and app access to the Eye RGB camera via XREAL SDK 3.1.0 (Unity). Zero-code option: any model as a USB-C display |
| Strongest proof point (real deployment or demo + date) | **None in this domain.** Closest: academic "ActiveGlasses" (Apr 2026) used Air 2 Ultra head pose to collect egocentric manipulation demos for a robot arm |
| Fastest credible 48-hour demo | Human-in-the-loop **sorting-cell HUD**: a robot arm sorts waste, low-confidence items pop up in the glasses, the operator confirms or corrects hands-free, corrections become training labels |
| Biggest risk | Unity + Android-host toolchain eats the first day; hardware on site is a guess; hand tracking on One + Eye ⚠️ unverified |
| Pairs well with (other vendors on site) | Dobot / Flexiv / ROKAE (sorting arm) · Galaxea / Galbot (mobile manipulator) · D-Robotics (edge inference) · SKYLANDX (3D scan for energy overlays) · Unitree Go2 (sensor patrol) |

## Why
- **Adds the human to an automation loop** — exception handling, teaching and verification are where sorting / repair robots fail; glasses keep the operator's hands free.
- **Eye RGB frames are readable by apps** (YUV textures in SDK 3.1.0) plus first-person streaming samples — enough for "look at item → classifier → overlay" pipelines.
- **Spatial anchors + plane / mesh detection** let you pin robot-collected data (temperature, CO2, fill levels) onto real rooms and bins.
- **Light and cheap:** 82–95 g glasses, USD 99 camera add-on; no-code display path works in minutes.

## Not a fit for
- Teams wanting one vendor for the whole build — XREAL has no actuators, no ROS 2 package, no autonomy stack.
- Outdoor snow / wet work — no IP rating published; tethered to a host.
- Fully autonomous concepts where a human operator adds nothing to the story.

## Sources
- [XREAL company profile (this repo)](../XREAL.md)
- [XREAL SDK 3.1.0 release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.1.0)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XREAL docs — Sample Code](https://docs.xreal.com/Sample%20Code)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/pdf/2604.08534) (via profile)

⬆ [XREAL profile](../XREAL.md) · [Products and solutions](XREAL-T03-2-Products-and-Solutions.md) · [Playbook](XREAL-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
