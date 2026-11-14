---
type: challenge-brief
company: "Galaxea"
slug: Galaxea
challenge: T01
challenge_title: "Autonomous Urban Services"
fit: 4
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, brief]
---
# Galaxea × T01 Autonomous Urban Services — Brief

**Fit: 4/5** — Strong for *indoor* service work (pick, pack, carry, hand over, tidy) in hotels, shops and clinics; no role on streets, snow or stairs.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **R1 Pro** or **R1 Lite** (wheeled dual-arm, omni base, LiDAR + cameras) with the open **G0.5** VLA; **LEMO** desktop dual-arm kit for a fixed pick-and-pack station |
| Strongest proof point | **WRC Beijing, 23–24 Aug 2026**: closed-loop dark-store fulfilment taking live visitor orders — **900 orders, 1,775 picks, 1,560 packing cycles** (self-reported) |
| Fastest credible 48-hour demo | "Order-to-bag" service point: guest orders on a phone, robot picks the items, bags them and hands over or drives them to a pick-up spot |
| Biggest risk | Navigation stack is **not publicly documented** (⚠️ unverified what ships on the robot); G0.5 fine-tuning needs **more than 70 GB VRAM**; which robots are on site is unconfirmed |
| Pairs well with | Unitree / Genisom / Magiclab quadruped (outdoor last leg), SKYLANDX MetaCam (building map), XREAL glasses (staff interface), D-Robotics RDK (edge perception) |

## Why
- The only public Galaxea deployment-style demo is exactly a T01 use case: order picking and packing for retail, live, at volume.
- The **Open-World Dataset** (500+ h, R1 Lite) covers retail, office, kitchen and residential scenes and includes chassis and torso actions — the right prior for service tasks.
- Teleop → dataset → policy loop is the company's core workflow (leader arms, VR, LeRobot conversion, G0.5 fine-tune or small diffusion policy).
- Omni chassis up to **1.5 m/s**, about **7 h** runtime, **5 kg per arm**, reach from floor to about 2 m (reseller / legacy figures, ⚠️ unverified for current units).
- "Commercial services" and "e-commerce / retail" are named target sectors in the Aug 2026 strategy.

## Not a fit for
- Outdoor last-mile, snow, slopes, kerbs or stairs — wheeled indoor base, no IP rating published.
- Street cleaning, waste-bin logistics or anything needing more than about 10 kg payload.
- Teams without access to a GPU (at least 8 GB VRAM for G0.5 inference).

## Sources
- [Galaxea blog — WRC 2026](https://galaxea-dynamics.com/blogs/robotics-insights-news/wrc-2026-embodied-ai-robotics) · [PR Newswire — WRC 2026](https://en.prnasia.com/story/545003-0.shtml) · [GalaxeaVLA](https://github.com/OpenGalaxea/GalaxeaVLA) · [Open-World Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) · [RBTX — R1 Pro listing](https://rbtx.de/en-GB/components/humanoid/galaxea-r1-pro-humanoid-robot-26-dof) · [Legacy R1 software guide](https://userguide-galaxea.github.io/Product_User_Guide/Guide/R1/Software_Guide/)

⬆ [Galaxea profile](../Galaxea.md) · [Products and solutions](Galaxea-T01-2-Products-and-Solutions.md) · [Playbook](Galaxea-T01-3-Playbook.md) · [Track overview](../../../Challenges/T01-Autonomous-Urban-Services/T01-0-Track-Overview.md)
