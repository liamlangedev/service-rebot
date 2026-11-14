---
type: challenge-brief
company: "Unitree Robotics"
slug: Unitree
challenge: T03
challenge_title: "Sustainable City"
fit: 3
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, brief]
---
# Unitree Robotics × T03 Sustainable City — Brief

**Fit: 3/5** — A very good *mobile sensing platform* for energy, water and litter monitoring on stairs, slopes and snow, but nothing purpose-built for waste, recycling or resource management.

| Question | Answer |
|---|---|
| Best hardware / platform for this track | **Go2 EDU** (15 kg, 4D LiDAR L2, full SDK, optional Orin) as sensor carrier; **G1 EDU + Dex3-1** only if you want a sorting / manipulation demo |
| Strongest proof point | Official quadruped inspection solution (B2 / A2 / As2) lists cases at a **smart water plant, a hydropower station and a renewable-energy 110 kV substation**, with thermal, acoustic and gas payloads. Customers and dates: not public |
| Fastest credible 48-hour demo | Go2 EDU + USB thermal camera patrols a building or spa plant room, flags heat and water leaks on a map, outputs a "wasted energy" report |
| Biggest risk | Variant trap: **Go2 Air / Pro have no SDK**. No arm on the small dogs by default, so "pick up litter" needs extra hardware. You bring the sustainability sensors yourself |
| Pairs well with | SKYLANDX (3D map of the site) · D-Robotics (low-power edge AI) · Dobot / Flexiv / ROKAE (fixed sorting arm) · XREAL (operator overlay) |

## Why
- **Mobility is the asset:** legs handle stairs, plant rooms, snow and steep paths where wheeled monitoring robots stop. As2 (IP54), A2 (IP56) and B2 (IP67) are weather-rated; Go2 is not.
- **Inspection stack is real:** autonomous patrol, meter reading, thermal anomaly and leak detection, auto-recharge and reports exist as a product — on the industrial dogs, not as an open hackathon kit.
- **Fastest developer path on site:** unitree_sdk2 (C++ / Python), unitree_ros2, MuJoCo sim, large community codebase.
- **Manipulation route exists:** G1 EDU teleoperation → imitation learning (xr_teleoperate + unitree_lerobot, ACT / Pi0 / GR00T) for a small sorting task.
- **Leukerbad angle:** thermal-water and heating infrastructure, spa buildings and snowy paths are a natural patrol target.

## Not a fit for
- Throughput waste sorting, recycling lines or disassembly — use a fixed arm vendor.
- EV-charging automation or precise force-controlled work.
- Teams that want a ready sustainability application rather than a robot to build on.

## Sources
- [Unitree — Advanced quadruped inspection solution](https://www.unitree.com/mobile/industry/electricity)
- [Unitree GitHub organisation](https://github.com/unitreerobotics) · [xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate) · [unitree_lerobot](https://github.com/unitreerobotics/unitree_lerobot)
- [Unitree Robotics company profile (internal; product specs)](../Unitree.md)

⬆ [Unitree Robotics profile](../Unitree.md) · [Products and solutions](Unitree-T03-2-Products-and-Solutions.md) · [Playbook](Unitree-T03-3-Playbook.md) · [Track overview](../../../Challenges/T03-Sustainable-City/T03-0-Track-Overview.md)
