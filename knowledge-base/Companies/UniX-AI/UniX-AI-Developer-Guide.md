---
type: dev-guide
company: "UniX AI"
slug: UniX-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# UniX AI — Developer Guide (hackathon edition)

⬆ [UniX AI profile](UniX-AI.md) · [Product portfolio](UniX-AI-Products.md) · [Roadmap and strategy](UniX-AI-Roadmap-and-Strategy.md)

> **Read this first:** UniX AI publishes **no SDK, no docs portal, no GitHub code, no ROS 2 packages and no simulation assets**. Everything below separates what is confirmed on official pages from what you must ask the on-site engineers. Do not commit to a UniX-based build until you have seen the interface with your own eyes.

## TL;DR — how you program it

- **No self-serve route exists publicly.** No SDK download, API reference, URDF or forum. Your interface is whatever the UniX booth team hands you on day 1.
- **Most realistic mode: skill composition.** Wanda 2.0 and Panther ship with pre-loaded "L4-level" applications (tea service, tidying, wiping, guiding, restocking, waste sorting were all demoed publicly). Plan to **trigger existing skills + navigation goals from your own laptop** and add your own perception / LLM / UI layer on top.
- **Second mode: teach a skill by demonstration.** The UniFlex stack is an imitation-learning framework (semantic keypoints + trajectory imitation). Whether hackathon teams get the teaching / teleoperation tool is **not public — ask**.
- **Only Martian (biped) officially promises APIs**: "high-/low-level API interfaces" for secondary development, CAN FD bus, OTA. Languages, rates and docs are not public, and Martian is the least likely robot to be on site.
- **Decision rule:** if within the first hour the booth cannot show you (a) a way to send a command from your laptop and (b) a way to read at least one sensor or robot state, treat UniX as a **demo actor in a multi-vendor system**, not as your development platform.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| Official SDK (Wanda 2.0 / Panther) | not public | not public | none | Product pages state no API, SDK or secondary-development interface. ⚠️ Existence of a partner / internal SDK is unverified |
| Martian development API | not public | High-level and low-level interfaces (per product page) | [Martian page](https://www.unix-group.ai/Martian) | Only a one-line claim; no docs, no download. Bus: CAN FD |
| UniPicker Pro gripper protocol | not public | Hybrid force / velocity / position control | [UniPicker page](https://www.unix-group.ai/UniPicker) | Communication interface, voltage and flange are not published |
| Official GitHub org | — | — | none found | `github.com/UniX-AI` and `github.com/unix-group-ai` do not exist; an account named "UnixAI" exists but is empty and shows no link to the company |
| Docs portal | — | — | none found | No docs sub-domain resolves; website has product pages only |
| UniTouch (academic code, CVPR 2024) | Python | Nothing on the robot — a research model for vision-based tactile sensors | [cfeng16/UniTouch](https://github.com/cfeng16/UniTouch) | First author Fengyu Yang is the UniX founder. ⚠️ Whether the product "UniTouch" model equals this code is unverified. Check the repo licence before use |

## Control levels

| Level | Wanda 2.0 | Panther | Martian |
|---|---|---|---|
| Pre-loaded applications / skills | ✅ stated ("preloaded L4-level applications") | ✅ stated | not stated |
| Task-level API (call a skill, send a nav goal) | not public — **ask** | not public — **ask** | "high-level API" claimed |
| Joint position / velocity streaming | not public | not public | "low-level API" claimed |
| Torque / current control | not public | not public | not public (150 N·m peak joint torque listed, control mode not) |
| Control rates | not public | not public | not public |
| EDU / developer edition | none announced; "Research & Education" is listed only as an application category | same | none announced |

Practical reading: assume **task-level only** for the wheeled robots unless told otherwise. Do not plan a project that needs torque control or custom whole-body controllers.

## ROS 2 and middleware

- **ROS 2 support: not public.** No packages, message definitions or bridge are published.
- **Internal bus:** CAN FD is stated for Martian only. For Wanda / Panther the bus is not published.
- **If the booth exposes ROS 2** (⚠️ unverified possibility): ask for the distro, DDS vendor, domain ID and a topic list before writing code; record a short bag of sensors and state first so the whole team can develop offline.
- **If it does not:** wrap whatever exists (HTTP, gRPC, a tablet app, a vendor script) in one thin adapter process on your laptop and keep the rest of your stack vendor-neutral.

## Simulation and digital twins

- **URDF / MJCF / USD: not public.** No Isaac Lab, MuJoCo or Gazebo assets were found.
- Do not spend hackathon hours building a model from the spec sheet. Kinematic facts you can rely on for reach planning only:

| Robot | Arm | Reach | Dual-arm payload | Torso lift | Base |
|---|---|---|---|---|---|
| Wanda 2.0 | 8 DoF ("4+1+3" shoulder-elbow-wrist) | **982 mm** | **12 kg** (6 kg single arm) | 280 mm | differential drive, **1.5 m/s**, min. passage 75 cm |
| Panther | 8 DoF | **982 mm** | **12 kg** | **800 mm**, reaches floor level | 4WS + 4WD, **2 m/s**, min. passage 65 cm |

- Fallback: test your perception and task logic on recorded camera data or with a stand-in arm, then integrate on the real robot in booked slots.

## AI stack

| Component | What it is (company description) | Public artefacts |
|---|---|---|
| **UniFlex** | Imitation-learning framework for cross-scenario task generalisation | none |
| **UniTouch** | Vision-tactile multimodal model for precise manipulation | No product weights. Related academic paper + code exist (see table above) |
| **UniCortex** | Long-sequence task planner for multi-step chores | none |
| Datasets | Company says real-world data comes from robots working in hospitality and service sites | none released |
| Teleoperation / data collection | Implied by the imitation-learning approach | tooling not public |
| LeRobot / open VLA support | — | none found |

What this means for you:

- You cannot fine-tune or swap their models. Bring **your own high-level brain** (LLM / VLM planner, speech, person or object detection) and let the robot's built-in skills do the manipulation.
- If demonstration teaching is offered, budget for it honestly: ask how many demos a new skill needs and how long training takes **before** designing around a custom skill.
- Running the academic UniTouch code is a research exercise, not a path to controlling the robot; it also needs a vision-based tactile sensor, and no tactile hardware is listed on the Wanda / Panther spec pages.

## Compute, sensors and connectivity

| Item | Wanda 2.0 | Panther | Martian |
|---|---|---|---|
| On-board compute | up to **275 TOPS** | optional up to **2070 TOPS** | "40T" platform, **32 GB RAM** |
| Chip / OS | not public | not public | not public |
| Head | RGB + RGBD cameras, 2-DoF head (yaw ±90°, pitch ±30°) | dual RGB; RGBD optional | depth camera + 2 RGB |
| Navigation sensors | 360° LiDAR, ultrasonic, base RGBD | front and rear 360° LiDAR; top 3D LiDAR optional | IMU |
| Audio | 6-mic circular array | 6-mic array + dual speakers | not stated |
| Battery | **8–16 h** | **4–8 h**, 48 V platform | 48 V / 9 Ah |
| Wi-Fi / Ethernet / ports / default IPs | not public | not public | not public |

- **How to connect a laptop: not documented.** Ask the booth for the supported path (robot hotspot, shared router or wired port) and whether you may put your own process on the on-board computer. Assume **no** until told yes.
- Safe default architecture: your laptop (or an edge board such as a D-Robotics RDK) on the same network runs perception and planning and talks to one robot-side endpoint.
- Raw sensor access (camera streams, LiDAR scans, mic audio) is **not guaranteed**. If it is refused, mount your own camera or use an external sensor (for example a SKYLANDX scan for the map, XREAL glasses for the operator view).

## First 60 minutes checklist

1. **Ask which robots and how many** are available to teams (Wanda 2.0? Panther?) and how slots are booked.
2. **Ask the interface question verbatim:** "From my laptop, how do I (a) start a pre-loaded skill, (b) send a navigation goal, (c) read robot state and camera images?" Write down protocol, language, IP and port.
3. **Get the skill list**: every pre-loaded skill, its parameters (object, location) and its known failure cases.
4. **Safety briefing**: where is the e-stop, who holds it, what modes exist (manual / autonomous / teaching), and what speed limits apply indoors with people around.
5. **Connect**: join the robot network as instructed and confirm you can reach the robot endpoint from your laptop.
6. **Verify state**: read one value live (battery level, base pose or joint state) and print it.
7. **Hello-world motion**: with a vendor engineer at the e-stop, trigger the smallest safe action — head nod, gripper open/close or a 0.5 m base move in a cleared area.
8. **Read a sensor**: grab one head-camera frame (or a LiDAR scan) and save it to disk. If not possible, decide now which external sensor you will use instead.
9. **Mapping**: ask whether the venue is already mapped and how to add named waypoints (reception, table, bed, bin).
10. **Chain two steps**: navigate to a waypoint, then run one skill. Time it and note the success rate over 3 tries.
11. **Teaching**: ask whether you may record demonstrations for a new skill, how many are needed and the turnaround time.
12. **Go / no-go at minute 60**: steps 5–8 done → build on UniX. Otherwise → use the robot as a scripted actor triggered by the vendor team and put your engineering into the surrounding system.

## Known gotchas and safety

- **No public safety documentation.** E-stop location, collision detection and force limits are not described on any product page. Get the briefing before powering anything.
- **These are heavy, fast machines near people**: up to 2 m/s base speed and 12 kg dual-arm payload. Keep spectators out of arm reach (about 1 m around the torso) during tests.
- **Indoor flat floors only.** Wheeled bases with 65–75 cm minimum passage; nothing published about slopes, thresholds, wet floors or snow. Do not take them outside in Leukerbad in November.
- **Closed stack**: one third-party database describes the software as closed-source (⚠️ single source). Expect no access to planners, models or firmware; OTA and firmware changes are vendor-only.
- **Skills are scene-dependent.** Demoed tasks (tea-making, bed-making, waste sorting) were shown in prepared setups; lighting, object type and table height may matter. Re-test in your own demo corner early.
- **Battery asymmetry**: Panther lists 4–8 h versus 8–16 h for Wanda 2.0. Charging method and time are not public — ask before an overnight run.
- **Spec inconsistencies to keep in mind**: founding year (2024 on the company site, 2023 in one press article); Panther dated Sep 2025 on the company timeline but launched by press release in Apr 2026.
- **Research limits of this guide**: built from the official product pages, press releases and direct checks for GitHub / docs hosts on 2026-11-14. Web search was unavailable for this pass, so developer-forum chatter and Chinese-language developer material could not be checked.

## Community resources

| Resource | Status |
|---|---|
| Developer forum / Discord / WeChat developer group | none found |
| Official docs or tutorials | none found |
| Company channels | [LinkedIn](https://www.linkedin.com/company/unix-ai/), plus X, YouTube and Facebook linked from the website (demo videos only) |
| Contact | global@unix-group.ai · business@unix-group.ai |
| Best resource this weekend | the UniX engineers at the booth — treat them as your documentation |
| Related open research | [UniTouch paper](https://arxiv.org/abs/2401.18084) and [code](https://github.com/cfeng16/UniTouch) |

## Sources

- [UniX AI profile (this repository)](UniX-AI.md)
- [Wanda 2.0 product page](https://www.unix-group.ai/Wanda)
- [Panther product page](https://www.unix-group.ai/Panther)
- [Martian product page](https://www.unix-group.ai/Martian)
- [UniPicker Pro product page](https://www.unix-group.ai/UniPicker)
- [About UniX AI](https://www.unix-group.ai/About-Unix-AI)
- [Press release, 2 Jan 2026: Wanda 2.0 at CES 2026 (via Webull / PR Newswire)](https://www.webull.com/news/14134140025406464)
- [Press release, 8 Apr 2026: Panther launch (via TechNode Global / PR Newswire Asia)](https://technode.global/prnasia/unix-ai-introduces-panther-the-worlds-first-service-humanoid-robot-to-enter-real-household-deployment-powered-by-its-differentiated-wheeled-dual-arm-architecture/)
- [arXiv 2401.18084: Binding Touch to Everything (UniTouch)](https://arxiv.org/abs/2401.18084)
- [GitHub: cfeng16/UniTouch (CVPR 2024 code)](https://github.com/cfeng16/UniTouch)
- [Humanoid.press database entry for Wanda 2.0 (closed-source note, cited via the profile)](https://humanoid.press/database/humanoid-press-database-wanda-2-0/)
