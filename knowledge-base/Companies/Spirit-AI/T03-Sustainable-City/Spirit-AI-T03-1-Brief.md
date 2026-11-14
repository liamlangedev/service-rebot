---
type: challenge-brief
company: "Spirit AI"
slug: Spirit-AI
challenge: T03
challenge_title: "Sustainable City"
fit: 2
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Spirit AI × T03 Sustainable City — Brief

**Fit: 2/5** — A capable indoor dual-arm sorter (Moz1) with an open VLA, but no sustainability product, deployment or roadmap; credible only as the "hands" of a waste-sorting or reuse demo.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Moz1** ✅ (wheeled dual-arm, force-controlled, **26 DoF**) + MozRobot SDK + Quest VR teleop. On-site presence ⚠️ unverified |
| Strongest proof point | WAIC Shanghai, **July 2026**: Moz1 + Spirit v1.6 tidied a room from one instruction — cans away, dishes into the dishwasher, crumpled paper thrown on the table detected and binned. Industrial: CATL battery-pack line, **>99 %** connector-insertion success (reported Dec 2025) |
| Fastest credible 48-hour demo | Table-top recyclables sorting: RealSense image → off-the-shelf classifier → scripted SDK pick-and-place into PET / aluminium / glass / residual bins, VR teleop as fallback |
| Biggest risk | Access: no confirmed robot on site, Chinese-only docs, API reference and gripper / payload specs not public. Spirit v1.5 fine-tuning wants **8× A100 80 GB** |
| Pairs well with | **D-Robotics** (low-power edge perception; Spirit v1.5 already ported to their Sunrise S600) · **SKYLANDX** (building map for a patrol concept) · **XREAL** (operator / audit overlay) |

## Why
- Sorting and tidying are exactly what the company demos: binning stray paper, loading a dishwasher, pill sorting — all transferable to "sort waste, recover reusables".
- Force / position hybrid arms with collision detection suit mixed, fragile items (glass, cups) next to people.
- **Spirit v1.5** is open (MIT) with a public "move objects into box" checkpoint — the closest ready-made skill to bin sorting.
- Docs describe Quest teleop + data collection + a Pi0.5 / openpi adaptation, so a learned policy is possible if GPUs and staff support exist.
- The D-Robotics port gives a "low-power edge AI" story 🧪 (no latency or wattage figures published).

## Not a fit for
- Anything outdoors: litter picking in snow, vegetation, water or air monitoring, steep terrain — Moz1 is a flat-floor indoor machine with no public IP rating.
- EV charging, energy metering or building-automation products — Spirit AI has none.
- Teams that need a quantified emissions case: a high-value humanoid sorting cans is a capability demo, not an efficiency argument.

⬆ [Spirit AI profile](../Spirit-AI.md) · [Products and solutions](Spirit-AI-T03-2-Products-and-Solutions.md) · [Playbook](Spirit-AI-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
