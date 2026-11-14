---
type: dev-guide
company: "Binabik AI"
slug: Binabik-AI
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# Binabik AI — Developer Guide (hackathon edition)

⬆ [Binabik AI profile](Binabik-AI.md) · [Product portfolio](Binabik-AI-Products.md) · [Roadmap and strategy](Binabik-AI-Roadmap-and-Strategy.md)

> **Read this first.** Binabik is a software vendor with no robot of its own. Its commercial stack (Studio, BDK) is **request-access only** and has **no public documentation**. What is public and usable today is a small GitHub org (two original MCP tools, three forks) and one Hugging Face checkpoint. Everything about the Studio / BDK API below is taken from marketing pages, so treat it as a list of things to confirm with the Binabik team on site.
>
> Research limit: web search was unavailable for this guide; findings come from direct reads of official pages, the GitHub org and Hugging Face.

## TL;DR — how you program it

- **Workflow, not joint commands:** demonstrate a task once (by hand or teleoperation) → Skill Engine splits it into steps and maps each to a library skill → Binabik Sim varies parts, positions and lighting → the same program runs on the robot. Company claim: "first demonstration to a running robot in **days**", so a 48-hour build only works with skills that already exist in their library.
- **Access is gated:** Studio is "Request access" via the contact form; `docs.binabik.ai` exists but sits behind a login wall. **The on-site engineers are your SDK.**
- **Robots:** publicly named targets are **AgiBot G2** and **Galaxea R1 Pro** (both vendors are on site). Public repos also show work on **Unitree G1** in Isaac Lab simulation (forks, not a product statement).
- **Self-serve today:** `mcp-rosbags` (LLM-queryable ROS 1 / ROS 2 bag analysis, Apache-2.0) and `mcp-lab` (test bench for MCP servers). Both are Python and run on a laptop in minutes, on any vendor's robot data.
- **Decision rule:** build on Binabik only if, within the first 30 minutes, they confirm (a) a robot you can book, (b) Studio / BDK access for your team, (c) the skills you need already exist. Otherwise use the robot vendor's own SDK and keep `mcp-rosbags` as a debugging and demo aid.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| Binabik Development Kit (BDK) | not public | Skill library + hardware abstraction; one skill set across robots | [binabik.ai/studio](https://binabik.ai/studio) | 🧪 request access. Site says engineers get "the same API we use". No public reference, package name or version |
| Binabik Studio (Teach, Skill Engine, Sim, code editor) | not public | Demonstration capture, plan generation, simulation, on-robot testing in one workspace | [binabik.ai/studio](https://binabik.ai/studio) | 🧪 request access. Includes code generation; start from a working program or write new ones |
| Docs portal | — | — | [docs.binabik.ai](https://docs.binabik.ai) | Resolves, but redirects to a login. Ask the team for credentials |
| `mcp-rosbags` | Python | Nothing on the robot; an MCP server that lets an LLM query recorded bags (`.bag`, `.db3`, `.mcap`): trajectories, LaserScan, images, TF, logs, plots | [github.com/binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags) | ✅ Apache-2.0, **29** stars, offline analysis only. Contact in README: dev@binabik.ai |
| `mcp-lab` | Python (FastAPI) | Local web UI to test MCP servers against Groq / OpenAI / Anthropic models; logs tokens, latency, tool calls to SQLite | [github.com/binabik-ai/mcp-lab](https://github.com/binabik-ai/mcp-lab) | ✅ Apache-2.0, 5 stars, last commits Sept 2025 |
| `unitree_lerobot` (fork) | Python | LeRobot training / evaluation for Unitree G1 with dexterous hands | [github.com/binabik-ai/unitree_lerobot](https://github.com/binabik-ai/unitree_lerobot) | Fork of Unitree's repo; default branch `binabik/main`; mid-2026 commits bump the LeRobot version and add a G1 config |
| `unitree_sim_isaaclab` (fork) | Python | Unitree simulation environments on Isaac Lab | [github.com/binabik-ai/unitree_sim_isaaclab](https://github.com/binabik-ai/unitree_sim_isaaclab) | Fork; June 2026 commits fix the Dockerfile |
| `Isaac-GR00T` (fork) | Python / notebooks | NVIDIA GR00T N1.6 foundation model | [github.com/binabik-ai/Isaac-GR00T](https://github.com/binabik-ai/Isaac-GR00T) | Fork; Jan 2026 commits add a SLURM fine-tuning script and a distributed-training fix |

No AgiBot G2 or Galaxea R1 Pro code is public in the org.

## Control levels

| Level | What Binabik exposes | Status |
|---|---|---|
| Task / skill (high level) | Demonstrate → segment → map to skills → review plan → execute. Skills named on the site: load and unload machines, carry parts, palletize, pick and place | 🧪 this is the product |
| Program / code | Code editor in Studio; generated programs can be edited; same interface for sim and real robot | 🧪 language not public |
| Motion primitives, joint, torque | Not described anywhere public | Assume it stays in the robot vendor's SDK (AgiBot, Galaxea) |
| Control rates | not public | — |

- No EDU or developer edition is published. There is one gate: request access.
- The only public hint at policy-level control is the Hugging Face checkpoint (see AI stack): a **16-dimensional** state and action vector with **50-step** action chunks, trained for a Unitree G1 simulation task. That describes one experiment, not the BDK interface.

## ROS 2 and middleware

- **Product stack:** ROS 2 is not mentioned on any product page (⚠️ unverified either way). Ask.
- **Indirect evidence:** Binabik's own `mcp-rosbags` reads ROS 1 and ROS 2 bags and standard messages (`nav_msgs/Odometry`, `sensor_msgs/LaserScan`, `sensor_msgs/Image`, `sensor_msgs/PointCloud2`, `tf2_msgs/TFMessage`, `rcl_interfaces/Log`). The team clearly works with ROS data, which makes a ROS 2 bridge plausible (inference).
- **Agent middleware:** both original repos use the **Model Context Protocol (MCP)**. If you build an LLM agent layer, MCP tools are the integration style this team already uses.
- **Hackathon use regardless of Binabik access:** record a bag on any ROS 2 robot on site, point `mcp-rosbags` at it and ask an LLM "what happened at t = …", "plot the path", "find error logs".

## Simulation and digital twins

| Item | What is known |
|---|---|
| Binabik Sim | Process simulator: machines, fixtures, cycle times; thousands of variations of parts, positions, lighting. The site states it is **not** a reinforcement-learning sandbox |
| Engine | Not named. Factory assets are credited to **NVIDIA SimReady** (CC BY 4.0), and the public forks use **Isaac Lab**, so an Isaac Sim / Omniverse base is likely (inference, ⚠️ unverified) |
| Robot assets (URDF / MJCF / USD) | None published by Binabik. Use the robot vendor's assets |
| Sim-to-real | Claimed single interface for sim and robot, so a validated program runs unchanged |
| Public sim repo | `unitree_sim_isaaclab` fork (Unitree G1 tasks). Needs an NVIDIA GPU workstation; not a laptop job |

Hackathon reality: you will not rebuild a cell in Binabik Sim in 48 hours unless their engineers do it with you. Plan for real-robot demonstration plus a short sim clip at most.

## AI stack

| Topic | Status |
|---|---|
| Approach | "Small data": zero-shot / few-shot, show the task once, generalise over part variants, positions and tolerances without retraining from scratch (company claim) |
| Pretrained policies | One public checkpoint: [`binabik-ai/act_PickPlaceRedBlock`](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock) (2 Jul 2026). ACT-style policy, **~51.6M** parameters, ResNet-18 backbone, 3 cameras at 640×480 (head + two wrists), 16-D state and action, chunk size 50. Trained on Unitree's `G1_Dex1_PickPlaceRedBlock_Dataset_Sim` |
| Caveats on that checkpoint | No model card, no licence, policy type is `binabik_act`, which is not a stock LeRobot policy name; where the matching class lives is not public (⚠️ unverified). Treat it as a research artefact, not a deliverable |
| VLA / foundation models | No Binabik model released. They forked NVIDIA **GR00T N1.6** and added fine-tuning scripts (Jan 2026); careers and about pages list VLA models and reinforcement learning as interests |
| Datasets | None published (Hugging Face org: 0 datasets) |
| Teleoperation / data collection | Binabik Teach records all movements and camera frames of one demonstration, by hand guiding or remote control. Teleop hardware not named |
| LeRobot | Used internally (fork of `unitree_lerobot`, LeRobot-format training config). No official LeRobot integration for G2 or R1 Pro is published by Binabik |
| LLM agents | MCP-based tooling with Groq, OpenAI and Anthropic backends in `mcp-lab`. Which LLM runs inside the Skill Engine is not public |

## Compute, sensors and connectivity

| Item | Detail |
|---|---|
| On-board compute | Whatever the host robot has (AgiBot G2 or Galaxea R1 Pro). Binabik requirements not public |
| Extra compute | Not public. Fine-tuning forks target GPU clusters (SLURM); expect a GPU laptop or workstation for anything learning-based |
| Sensors | Robot cameras plus task-specific additions; Solutions page mentions a parallel gripper with a fingertip camera, a centric gripper and a vacuum gripper |
| Data location | Site states processes and camera data stay in the customer's factory. Whether Studio needs internet during the event: **ask** (venue Wi-Fi at 1,400 m is a risk) |
| Laptop connection, network defaults | not public. Follow the robot vendor's guide for the G2 or R1 Pro, then whatever Binabik's engineers add |
| `mcp-lab` | Runs locally on `http://localhost:8000`; needs at least one LLM API key (Groq, OpenAI or Anthropic) |

## First 60 minutes checklist

Steps 1–5 depend on Binabik staff; steps 6–8 work with no access at all.

1. **Minute 0–5: go to the Binabik table.** Ask: Which robots here can you drive today? Is there a Python API? Can we get Studio and `docs.binabik.ai` logins now? Does it need internet? Which skills exist out of the box? Can a team add its own skill in two days?
2. **Minute 5–10: book hardware.** Binabik brings no robot. Reserve a slot on an AgiBot G2 or Galaxea R1 Pro with that vendor and confirm Binabik's stack is installed on that specific unit.
3. **Minute 10–20: verify.** Log in to Studio, open an existing program, run it in simulation. If login or sim fails here, switch to the fallback (step 6) and do not wait.
4. **Minute 20–35: hello-world motion.** Run one library skill on the real robot (pick and place of a single object). Review the plan on screen before the robot moves; keep the vendor's e-stop in hand.
5. **Minute 35–50: teach once.** Record one demonstration with Teach, inspect how the Skill Engine segmented it, and note which steps mapped to existing skills and which are "missing". Missing skills are your schedule risk.
6. **Fallback, in parallel from minute 10:** one teammate brings up the robot vendor's own SDK (see the AgiBot or Galaxea developer guide) so the project survives without Binabik.
7. **Read sensors:** record a short ROS 2 bag on the robot (camera, odometry, TF). Then:
   ```bash
   git clone https://github.com/binabik-ai/mcp-rosbags.git
   cd mcp-rosbags && python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
   Register `src/server.py` as an MCP server (set `MCP_ROSBAG_DIR` to your bag folder) and ask an LLM client to list bags and plot the odometry path.
8. **Minute 50–60: decide.** Go with Binabik if steps 3–5 worked; otherwise keep them as advisers and build on the vendor SDK.

## Known gotchas and safety

- **No self-serve path.** No public docs, no downloadable SDK, no forum. If the team is busy with other groups, you are blocked.
- **E-stop and modes belong to the robot vendor.** Binabik describes "supervised operation: every plan can be checked before the robot moves", which is a software review step, not a safety function. Learn the G2 / R1 Pro e-stop before running any generated plan.
- **Timescales are industrial.** Their own numbers: first application in **months**, follow-ups in **days**. A 48-hour demo must reuse existing skills.
- **Sim is process-oriented.** Do not plan an RL training loop in Binabik Sim.
- **Robot coverage is narrow.** Only G2 and R1 Pro are named. Unitree G1 appears in public forks (simulation) but is not a stated supported platform. Do not assume Flexiv, Dobot, ROKAE or quadrupeds work.
- **Public checkpoint is not plug-and-play:** custom policy type, no licence, simulation-only training data.
- **Licences:** `mcp-rosbags` and `mcp-lab` are Apache-2.0. The forks keep upstream licences (check each before reuse). Studio / BDK terms for hackathon code and IP are not public; ask before you build something you want to keep.
- **`mcp-rosbags` is offline only:** it analyses recorded bags, it does not subscribe to live topics or command the robot.
- **Company claim "up to 85%" greater learning efficiency** (ERF 2026 listing only) is unverified; do not quote it in a pitch as fact.

## Community resources

| Resource | Link | Note |
|---|---|---|
| GitHub org | [github.com/binabik-ai](https://github.com/binabik-ai) | 5 code repos; issues open on `mcp-rosbags` |
| Hugging Face org | [huggingface.co/binabik-ai](https://huggingface.co/binabik-ai) | 1 model, 0 datasets |
| Developer contact | dev@binabik.ai | From the `mcp-rosbags` README |
| Studio access request | [binabik.ai/contact](https://binabik.ai/contact) | Topic "Studio access" |
| Training | Binabik Academy, on site or in Winterthur | On request |
| Forum / Discord / Slack | none found | — |
| Blog | [binabik.ai/blog](https://binabik.ai/blog) | "Insights & Research" section, currently empty |

Related: [Binabik AI profile](Binabik-AI.md) for company background and track fit.

## Sources

- [Binabik AI — home](https://binabik.ai)
- [Binabik AI — Studio](https://binabik.ai/studio)
- [Binabik AI — Solutions](https://binabik.ai/solutions)
- [Binabik AI — About](https://binabik.ai/about)
- [Binabik AI — Open positions](https://binabik.ai/open-positions)
- [Binabik AI — Blog](https://binabik.ai/blog)
- [Binabik AI — Contact](https://binabik.ai/contact)
- [Binabik AI — docs portal (login required)](https://docs.binabik.ai)
- [GitHub — binabik-ai organisation](https://github.com/binabik-ai)
- [GitHub — binabik-ai/mcp-rosbags](https://github.com/binabik-ai/mcp-rosbags)
- [GitHub — binabik-ai/mcp-lab](https://github.com/binabik-ai/mcp-lab)
- [GitHub — binabik-ai/unitree_lerobot](https://github.com/binabik-ai/unitree_lerobot)
- [GitHub — binabik-ai/unitree_sim_isaaclab](https://github.com/binabik-ai/unitree_sim_isaaclab)
- [GitHub — binabik-ai/Isaac-GR00T](https://github.com/binabik-ai/Isaac-GR00T)
- [Hugging Face — binabik-ai](https://huggingface.co/binabik-ai)
- [Hugging Face — binabik-ai/act_PickPlaceRedBlock](https://huggingface.co/binabik-ai/act_PickPlaceRedBlock)
