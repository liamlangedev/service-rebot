---
type: challenge-brief
company: "Galaxea"
slug: Galaxea
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# Galaxea × T02 Resilient & Safe City — Brief

**Fit: 2/5** — Supporting role only: Galaxea gives you capable indoor "remote hands" (dual-arm, teleoperable, learnable), but no rough-terrain mobility and no safety or emergency track record.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **R1 Pro** (wheeled dual-arm, **5 kg per arm**, ground to **2 m** reach, **7 h** — reseller figures ⚠️ unverified) as an indoor intervention robot; **LEMO + A1Z-T** as a low-latency (**under 50 ms**) teleop bench |
| Strongest proof point | None in this domain. Closest: WRC Beijing, **23–24 Aug 2026** — long-running closed-loop fulfilment and assembly demos (self-reported), showing manipulation reliability, not hazard response |
| Fastest credible 48-hour demo | Operator outside a mock "hazard room" teleoperates an R1 to close a valve, flip a breaker and retrieve an object, with live camera feed and an incident log |
| Biggest risk | Flat indoor floors only; IP rating, slope and threshold limits **not public**; navigation API access unconfirmed |
| Pairs well with | Quadruped scout (Unitree, Genisom, AGIBOT D1, Magiclab) · SKYLANDX MetaCam (3D map) · XREAL (operator view) · D-Robotics RDK (edge detection) |

## Why
- T02 needs robots that reach the problem. Galaxea's shipping robots are wheeled and indoor; they only cover the **last metre: manipulation** once something else has found the fault.
- Teleoperation is a real strength: leader arms, VR, and community whole-body teleop stacks for R1 / R1 Pro already exist.
- **ROS 2 Humble** interfaces expose arms, grippers, torso, chassis and cameras, so a "robot as remote operator" demo is integration work, not research.
- G0.5 and small diffusion policies can turn about 50 teleop demos into one autonomous skill (for example "close this valve") — a credible stretch goal.
- No public Galaxea deployment, pilot or roadmap item in inspection, security, rescue or outdoor work.

## Not a fit for
- Anything outdoors in Leukerbad in November: snow, stairs, slopes, avalanche or rockfall scenarios.
- Wide-area patrol, mapping or search — use a quadruped, drone or handheld scanner.
- Wet, dusty or hot environments (no published ingress protection).

## Sources
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics)
- [RBTX reseller listing — R1 Pro](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof)
- [GitHub — OpenGalaxea/EFMNode](https://github.com/OpenGalaxea/EFMNode)
- [GitHub — awesome-galaxea-developers](https://github.com/OpenGalaxea/awesome-galaxea-developers)
- [Galaxea company profile (this repo)](../Galaxea.md)

⬆ [Galaxea profile](../Galaxea.md) · [Products and solutions](Galaxea-T02-2-Products-and-Solutions.md) · [Playbook](Galaxea-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
