---
type: challenge-playbook
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T02
updated: 2026-11-14
tags: [leukerbad-hackathon, t02, playbook]
---
# Omnicor AI × T02 — Hackathon Playbook

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T02-1-Brief.md) · [Products and solutions](Omnicor-AI-T02-2-Products-and-Solutions.md)

> **Ground rule for every concept below:** Omnicor AI is the on-device inference layer, never the whole system. Nothing about OC Node or OC Agent is publicly specified, so each concept names a **Plan B compute** (robot's own computer, a laptop, or a D-Robotics RDK board) that keeps the project alive if the Omnicor part is not available. Spend the first hour at their booth before committing.

## Solution approaches

### Concept 1 — "Cut the cable" hazard sentinel (safest)

- **Problem → value:** Fixed cameras at a tunnel portal, cable-car station or avalanche-prone road stop being useful the moment the uplink fails. A sentinel that detects, reasons and alerts locally keeps protecting during the outage.
- **Hardware:** OC Node (if available) + USB / IP camera on a tripod. Plan B compute: laptop or D-Robotics RDK. No robot required.
- **Architecture / stack:** camera → small detector or compact VLM (person down, smoke, blocked exit, debris on road) → rule layer for alarm thresholds → local LLM (Apertus 8B or a Qwen / Mistral variant) turns events into a short incident report in German / French / English → local dashboard + siren / light over GPIO or LAN. All compute on the node; network used only to sync when it returns.
- **48-hour plan:**
  - H0–6: confirm what Omnicor can run tonight; pick 3 hazard classes; get camera → detector running on Plan B.
  - H6–24: port detector + LLM to OC Node with the Omnicor team; build event log and report prompt.
  - H24–40: add store-and-forward sync, measure latency and power, stage the scenes.
  - H40–48: rehearse; record a backup video.
- **3-minute demo script:** (1) show live dashboard; (2) pull the Ethernet cable on stage; (3) a teammate "collapses" or a smoke machine / cardboard "rockfall" enters the scene; (4) alarm fires and a three-language report appears in seconds; (5) plug the cable back, the log syncs; (6) show latency and watts on one slide.
- **Risks and fallbacks:** OC Node absent → run on Plan B and present Omnicor as the path to production. False alarms → restrict to 2 classes with staged scenes.
- **Judging angles:** innovation modest; technical depth = measured offline latency and power; impact = works in outages; Leukerbad = road and gallery closures, cable-car stations, thermal-bath plant rooms.

### Concept 2 — Offline patrol dog for infrastructure rounds

- **Problem → value:** After a storm or avalanche warning, someone must check galleries, plant rooms and paths. A quadruped that inspects and reports without connectivity removes people from the hazard and still works in a tunnel.
- **Hardware:** quadruped from another vendor (Unitree Go2 / B2, AGIBOT D1, Genisom M1 / L1 or Magiclab MagicDog) + OC Node as payload, or Omnicor-optimised models on the robot's own computer. Optional SKYLANDX MetaCam for a prior 3D map.
- **Architecture / stack:** robot's stock locomotion and waypoint navigation (vendor SDK / ROS 2) → on-board camera frames → VLM checklist per waypoint ("is the door closed?", "is there water on the floor?", "read the gauge") → local LLM compiles a round report → stored on the robot, offloaded when back in range. Omnicor layer = making the VLM + LLM fit the robot's power and memory budget.
- **48-hour plan:**
  - H0–6: secure a robot slot; check payload power / mounting for OC Node; teleoperate a route.
  - H6–24: waypoint patrol working; VLM checklist on Plan B compute; start port to OC Node.
  - H24–40: integrate on-board, run with Wi-Fi off, tune prompts on 4–5 inspection points, add anomaly photo log.
  - H40–48: rehearse full round; fallback video.
- **3-minute demo script:** (1) show the robot's router being switched off; (2) dog walks three checkpoints; (3) one has a staged fault (open cabinet, "leak", obstacle); (4) dog returns, report with photos appears on a tablet; (5) one slide: on-board inference time per checkpoint, battery impact.
- **Risks and fallbacks:** payload mounting or power not possible → run models on the robot's built-in computer or a backpack laptop. Navigation unreliable → teleoperate the walk, keep inspection autonomous. VLM too slow → inspect only when stopped.
- **Judging angles:** innovation = fully offline semantic inspection; depth = navigation + on-board VLM; impact = fewer people in hazard zones; Leukerbad = steep, snowy paths, avalanche galleries on the access road, spa technical rooms.

### Concept 3 — Responder copilot: local map + local language model

- **Problem → value:** First responders entering a damaged or smoke-filled building need "what is where" hands-free, and radio / mobile coverage is often the first thing lost. A wearable or carried unit that answers questions from a local 3D scan and live detections needs no network.
- **Hardware:** OC Node as a belt / backpack compute unit + SKYLANDX MetaCam (scan) + XREAL glasses (display). Plan B compute: laptop in a backpack.
- **Architecture / stack:** MetaCam scan → point cloud / floor plan with tagged objects (exits, extinguishers, hazards, detected persons) → structured scene memory → local LLM answers voice / text queries ("nearest exit?", "where was the last person seen?") → overlay or text on XREAL. Speech-to-text and LLM both on-device; multilingual output via Apertus.
- **48-hour plan:**
  - H0–6: scan one corridor + room; export format agreed; LLM answering from a hand-written scene file.
  - H6–24: automatic tagging from detections; query interface; XREAL text view.
  - H24–40: port models to OC Node; latency tuning; offline test walk.
  - H40–48: rehearse, backup video.
- **3-minute demo script:** (1) show the pre-scan; (2) responder with glasses enters, phone in flight mode; (3) asks two questions aloud in German or French; (4) answers and direction appear; (5) a new "casualty" is detected and added to the map; (6) incident summary exported.
- **Risks and fallbacks:** three vendors to integrate → drop XREAL and use a phone / tablet screen. Live map update too hard → static pre-scan plus live detections list. Speech recognition unreliable in noise → push-to-talk or text.
- **Judging angles:** innovation = language interface over a local digital twin; depth = SLAM + LLM grounding on edge compute; impact = responder safety; Leukerbad = hotels, clinics and bath complexes with many elderly guests to evacuate.

### Concept 4 — Comms-loss handover: teleoperated manipulator that finishes the job alone (most ambitious)

- **Problem → value:** Robots in hazardous zones are teleoperated, and the link is the weak point. When it drops mid-task (closing a valve, flipping a breaker, clearing a small obstacle), an on-board policy completes or safely aborts the action instead of freezing.
- **Hardware:** wheeled dual-arm manipulator from an Omnicor-listed customer (AGIBOT G1 / G2 or Galbot G1) + on-board VLA deployed with Omnicor (OpenVLA or pi0.5), on OC Node or the robot's computer.
- **Architecture / stack:** operator teleop over Wi-Fi → link-quality monitor → on loss, switch to on-board VLA with a language goal ("close the red valve") or to a safe-retreat behaviour → on reconnect, hand back with a status report from a local LLM. Use the vendor's own pre-trained model where possible (AGIBOT GO-1, Galbot GraspVLA family) rather than training from scratch.
- **48-hour plan:**
  - H0–6: confirm with Omnicor and the robot vendor that a VLA already runs on-board; if not, **stop and pick Concept 2**.
  - H6–24: teleop baseline for one task; collect demonstrations if fine-tuning is feasible; link monitor.
  - H24–40: autonomous completion of one task on a mock panel; handover logic; safe-abort path.
  - H40–48: rehearse 10 runs, report success rate honestly; backup video.
- **3-minute demo script:** (1) operator starts turning a valve by teleop; (2) teammate kills the Wi-Fi; (3) status light changes, robot finishes the turn or retreats; (4) Wi-Fi back, operator receives a spoken / text summary; (5) show success count from rehearsals.
- **Risks and fallbacks:** no ready on-board VLA → scripted motion primitive as the "autonomous" finisher, VLA shown as roadmap. Fine-tuning compute missing (pi0.5 examples assume a large GPU) → use a vendor pre-trained skill. Safety → low speed, soft mock-up, e-stop in hand.
- **Judging angles:** innovation high (graceful autonomy under comms loss); depth high (teleop + VLA + on-device inference); impact = real hazardous-environment need; Leukerbad = thermal-water plant, tunnels and cable-car machinery where radio coverage is poor.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Omnicor + Unitree Go2 / B2 | Offline patrol and inspection (Concept 2) | Medium — payload power / mounting and model port are the unknowns |
| Omnicor + AGIBOT (D1, G1 / G2, GO-1) | Patrol or manipulation on a robot whose maker is listed as an Omnicor customer | Medium — lower if a deployment already exists (⚠️ unverified) |
| Omnicor + Galbot G1 | On-board VLA manipulation under comms loss (Concept 4) | High — depends on an existing on-board model |
| Omnicor + SKYLANDX MetaCam | Local 3D map as memory for an offline LLM (Concept 3) | Medium — data export format to settle early |
| Omnicor + XREAL | Hands-free responder display of local inference results | Medium — keep to text overlay |
| Omnicor + D-Robotics RDK | Low-cost target board and Plan B compute; "any device" story with two targets | Low to medium — whether OC Agent supports this board is ⚠️ unverified |
| Omnicor + Genisom / Magiclab quadrupeds | Alternative patrol bodies if Unitree slots run out | Medium |
| Omnicor + Binabik AI | Agent OS on top, optimised models underneath | High — two young software stacks, interfaces not public |

## Questions to ask the Omnicor AI engineers on site

1. What did you physically bring: OC Node units (how many?), and what is the chip, memory, power draw and supply voltage?
2. Can OC Node run on a quadruped's battery rail, and is there any temperature / IP rating for outdoor use?
3. Which robots in this hall already run an Omnicor deployment (AgiBot? Galbot?), with which model, at what inference rate?
4. How long does OC Agent need to port a new model — a small detector, a compact VLM, an 8B LLM? Minutes, hours or days?
5. What do we get back: a ROS 2 node, an HTTP / gRPC endpoint, a container, or a binary? Can we log in to the device?
6. Does OC Agent handle classic vision models and speech-to-text, or only LLMs and VLAs?
7. Can Apertus (or Qwen / Mistral) run fully offline on your hardware with usable speed in German and French? Tokens per second?
8. Can you give us before / after numbers (latency, memory, watts, accuracy) that we may show to the judges?

## Decision rule

- **Pick Omnicor AI for T02 if** your core claim is "it still works with no network", you already have a robot or sensor from another vendor, and the Omnicor team confirms in the first hour that your model can run on hardware they have here.
- **Avoid if** you need a complete platform, documented APIs tonight, or your demo does not visibly benefit from on-device inference; choose a robot vendor first and treat Omnicor as optional.

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [Omnicor AI company profile (this repository)](../Omnicor-AI.md)
- [OpenVLA GitHub repository](https://github.com/openvla/openvla)
- [Apertus-8B-Instruct-2509 model card (Hugging Face, swiss-ai)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [LeRobot documentation: pi0.5 policy](https://huggingface.co/docs/lerobot/pi05)
