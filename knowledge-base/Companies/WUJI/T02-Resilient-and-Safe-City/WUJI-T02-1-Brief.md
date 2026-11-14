---
type: challenge-brief
company: "WUJI"
slug: WUJI
challenge: T02
challenge_title: "Resilient & Safe City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, brief]
---
# WUJI × T02 Resilient & Safe City — Brief

**Fit: 3/5** — Good "remote hands" for a multi-vendor hazard-response robot (glove-driven dexterous teleoperation), but no arm, no mobility, no outdoor rating and no public safety-domain deployment.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Wuji Glove → Wuji Hand 2** (20 DoF, back-drivable, MIT mode, 1000 Hz) on a partner arm. Fallback: Wuji Hand gen 1 (USB, **15 N** fingertip, **10 kg** static grasp) |
| Strongest proof point (real deployment or demo + date) | None in safety / rescue / inspection. Closest: official glove-to-hand teleoperation workflow, SDK release **2026-11-10** |
| Fastest credible 48-hour demo | Operator behind a partition closes a valve, trips a breaker and pulls a plug on a mock hazard panel; arm uses pre-taught poses, fingers follow the glove |
| Biggest risk | **No WUJI arm**: you need another vendor's arm plus a flange adapter. Hands are dry-lab devices (gen 1 **IP40**; Hand 2 beta: **15–30 °C**, no shock guarantee) |
| Pairs well with (other vendors on site) | Flexiv, ROKAE, Dobot (arm) · Unitree, AGIBOT, Galaxea (mobile carrier) · XREAL (operator view) · SKYLANDX (3D context) |

## Why
- Hazardous-environment teleoperation is a core T02 theme; glove → retargeting → hand is WUJI's best-documented workflow (about **45 min** to first teleop per docs).
- 20 independent DoF operate **human controls and tools** (valves, switches, plugs, handles) without a custom gripper per task.
- Hand 2 offers per-joint stiffness and effort limits for gentle contact. Caveat: no robot-side touch sensing; docs say not to treat joint current as force.
- Open stack: `pip install wuji-sdk`, webcam keypoints can replace a glove, MCAP session logs, ROS 2 drivers, URDF / MJCF / USD.

## Not a fit for
- Outdoor, wet, dusty or cold field work (avalanche, flood, fire scene).
- Patrol, mapping, monitoring or autonomy-first projects: no sensing platform, mobility or high-level skills.
- Heavy-force rescue tasks (debris, jammed doors).

## Sources
[WUJI profile](../WUJI.md) · [Hand 2 overview](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview.md) · [Hand 2 user notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice.md) · [Hand gen 1 overview](https://docs.wuji.tech/docs/en/wuji-hand/v1/overview.md) · [Glove quick start](https://docs.wuji.tech/docs/en/wuji-glove/latest/getting-started.md) · [Release notes](https://docs.wuji.tech/docs/en/release-notes.md)

⬆ [WUJI profile](../WUJI.md) · [Products and solutions](WUJI-T02-2-Products-and-Solutions.md) · [Playbook](WUJI-T02-3-Playbook.md) · [Track overview](../../../Challenges/T02-Resilient-and-Safe-City/T02-0-Track-Overview.md)
