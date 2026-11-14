---
type: challenge-playbook
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T01
updated: 2026-11-14
tags: [leukerbad-hackathon, t01, playbook]
---
# Omnicor AI × T01 — Hackathon Playbook

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T01-1-Brief.md) · [Products and solutions](Omnicor-AI-T01-2-Products-and-Solutions.md)

**Ground rules for every concept below**
- Omnicor AI supplies the on-device inference layer only. Each concept needs a robot from another vendor, and that vendor's SDK does the moving.
- No Omnicor SDK, spec or doc is public. **Hour 0 task: talk to the Omnicor engineers** (questions below) and learn what OC Agent / OC Node can do here. Until then, develop on a laptop GPU with the same open models so you are never blocked.
- Make the edge value visible: every demo should include an **"unplug the network" moment** and, if possible, a live latency or power readout.

## Solution approaches

### Concept 1 — Offline alpine concierge and guide (safest)

- **Problem → value:** Spa guests and elderly visitors need directions, opening hours and escort between hotel, baths and clinic. A robot that answers in German, French, Italian and English and leads the way, with no cloud dependency and no voice data leaving the device.
- **Hardware:** OC Agent-deployed LLM on the robot's own computer, or an OC Node strapped on (both ⚠️ unverified) · body: Unitree Go2 or a wheeled service humanoid (UniX AI Wanda, Spirit AI Moz1) · microphone and speaker.
- **Architecture / stack:** speech-to-text (local) → local LLM such as Apertus 8B Instruct (Apache-2.0, multilingual) with a small Leukerbad facts file and a tool call `go_to(place)` → the robot vendor's navigation to pre-recorded waypoints → text-to-speech. All inference on-board; no internet.
- **48-hour plan:**
  - H0–6: confirm Omnicor support and target compute; run the LLM on a laptop behind an OpenAI-compatible endpoint; record 4–5 waypoints with the robot vendor's tools.
  - H6–24: wire speech in / out and the `go_to` tool; hand the model to Omnicor for on-device porting in parallel.
  - H24–40: switch inference to the robot / OC Node; tune response latency; add four languages and a "follow me" pace suited to slow walkers.
  - H40–48: rehearse; freeze; record a backup video.
- **3-minute demo script:** (1) Judge asks in French where the thermal bath entrance is. (2) Robot answers and leads to the marked spot. (3) Teammate visibly pulls the Wi-Fi router plug; second judge asks in German; robot still answers and guides. (4) Show the latency / power readout and one slide on privacy.
- **Risks and fallbacks:** port not ready → keep the LLM on a laptop in a backpack or on the local LAN (still offline). Noisy hall → push-to-talk button or typed input. Navigation flaky → short straight route with two waypoints.
- **Judging angles:** innovation moderate · technical depth in on-device multilingual dialogue · impact: tourism and elderly guests · Leukerbad relevance high (multilingual resort, patchy coverage).

### Concept 2 — "Last ten metres" delivery hand-over

- **Problem → value:** Delivery robots usually fail at the final step: taking the item off the shelf and handing it to a person. A mobile manipulator fetches a towel, pharmacy bag or room-service item and hands it over, with the policy running on-board.
- **Hardware:** Galbot G1 or AGIBOT G1 / G2 (both listed as Omnicor customers on its site; scope ⚠️ unverified) or Galaxea R1 · OC Agent / OC Node for the on-board model.
- **Architecture / stack:** camera → object and person detection → the robot vendor's own grasp model (Galbot GraspVLA family, AGIBOT GO-1) or OpenVLA / pi0.5 → vendor arm control; base motion via vendor navigation between two stations; a local LLM parses the order ("bring a towel to seat 3"). Omnicor's job: make the chosen model run on the robot's computer at a usable rate.
- **48-hour plan:**
  - H0–6: ask Omnicor and the robot vendor which model already runs on-board that robot; pick that one, do not start a new port if a working one exists.
  - H6–24: scripted pick from a fixed shelf and hand-over at a fixed station; order parsing on laptop.
  - H24–40: move order parsing on-device; add two or three item types; add safe hand-over (wait for the person's hand, release slowly).
  - H40–48: run 20 trials, report success rate honestly; record backup video.
- **3-minute demo script:** (1) Spoken order. (2) Robot drives to the shelf, picks the item. (3) Drives to the "guest", hands over. (4) Network unplugged, second order succeeds. (5) Slide: success rate and on-board latency.
- **Risks and fallbacks:** VLA unreliable on new objects → restrict to two known items or use the vendor's scripted grasp. No time to fine-tune → pretrained behaviour only. Robot access limited → simulate the base, show the arm only.
- **Judging angles:** technical depth high (on-board VLA) · real-world impact for hotels and clinics · innovation depends on how robust the hand-over looks.

### Concept 3 — Street and facility inspector with offline ticketing

- **Problem → value:** A small municipality cannot patrol every path for ice, litter, overfull bins or blocked walkways. A quadruped does the round, classifies issues on-board and files tickets locally; it syncs when coverage returns.
- **Hardware:** Unitree Go2 / B2 or Genisom M1 / L1 · on-board camera · OC Node or the robot's own computer running a compact vision-language model · optional SKYLANDX MetaCam scan for the map.
- **Architecture / stack:** camera frames → small detector for candidate issues → local vision-language model writes a one-line description and severity → ticket stored with pose from the robot's localisation → simple web dashboard on the LAN. Route following via the vendor SDK.
- **48-hour plan:**
  - H0–6: define four issue classes; collect photos around the venue; confirm which vision-language model Omnicor can put on-device.
  - H6–24: detector plus description pipeline on laptop; dashboard; patrol route.
  - H24–40: on-device port; measure frames per second and battery impact with and without optimisation.
  - H40–48: staged course with planted issues; rehearse.
- **3-minute demo script:** (1) Robot walks a short course with a planted "ice patch" mat, a litter pile and a blocked path. (2) Tickets appear on the dashboard with photo, text, location. (3) Show the same round with the network off, then sync. (4) One number: on-device rate versus the unoptimised baseline.
- **Risks and fallbacks:** vision-language model too slow on-board → detector only, text from templates. Outdoor snow or cold stops the robot → indoor mock street. No optimisation gain to show → present offline operation as the value.
- **Judging angles:** Leukerbad relevance high (winter paths, small works department) · impact clear · technical depth in edge perception · innovation moderate.

### Concept 4 — Town edge brain for a mixed robot fleet (most ambitious)

- **Problem → value:** A resort will own robots from several makers. Instead of each calling a foreign cloud, one local compute node runs the shared language and planning models and dispatches tasks: a quadruped carries, a mobile manipulator loads and hands over.
- **Hardware:** OC Node as the local server (⚠️ unverified; fallback: any GPU machine) · one quadruped (Unitree Go2) · one wheeled dual-arm robot (Galbot G1 or AGIBOT G1) · optional Binabik AI or coprod software layer for cross-robot interfaces · optional XREAL glasses for an operator view.
- **Architecture / stack:** request (voice or app) → local LLM agent on the node decomposes it into robot tasks → per-robot adapters call each vendor SDK → on-robot models handle perception and grasping → status back to a dashboard. Matches Omnicor's "enterprise AI server" plus "embodied robots" domains.
- **48-hour plan:**
  - H0–6: fix one scenario (guest orders an item, manipulator loads it onto the quadruped, quadruped delivers); write the adapter interface; confirm node availability.
  - H6–24: each robot performs its half alone, triggered by a fixed command.
  - H24–40: LLM dispatcher on the node; hand-off between robots; failure handling (retry, ask human).
  - H40–48: reduce scope to what works; rehearse the full chain five times.
- **3-minute demo script:** (1) Spoken request. (2) Dashboard shows the plan split across two robots. (3) Manipulator loads; quadruped delivers. (4) Internet cable pulled, LAN only, second request runs. (5) Closing slide: one local node, many robots, data stays in the valley.
- **Risks and fallbacks:** two vendors' SDKs in 48 h is a lot → drop to one robot plus a simulated second. Robot-to-robot hand-off fails → human places the item, keep the dispatch story. Node not available → laptop server.
- **Judging angles:** innovation and technical depth highest · strong sovereignty and scalability story · execution risk highest.

## Cross-vendor combos worth considering

Effort ratings are estimates; none of these integrations is documented publicly.

| Combo | What it enables | Integration effort |
|---|---|---|
| Omnicor AI + Galbot G1 | On-board grasp / VLA for delivery hand-over; possibly an existing relationship (site logo) | Medium, lower if a deployment already exists ⚠️ unverified |
| Omnicor AI + AGIBOT G1 / G2 / X2 | Same, on wheeled dual-arm or humanoid; GO-1 as the policy | Medium ⚠️ unverified |
| Omnicor AI + Unitree Go2 / B2 | Offline concierge or patrol inspector with a local LLM or vision-language model | Low to medium (compute box plus network link to the robot) |
| Omnicor AI + D-Robotics RDK X5 / S100 | Target board for optimisation: show a model that did not fit now running on a small board | Medium; support for this silicon not confirmed |
| Omnicor AI + Binabik AI | Agentic OS on top, optimised on-device models underneath | Medium to high (two young software stacks) |
| Omnicor AI + SKYLANDX MetaCam | Fast 3D map of the venue for patrol or delivery routes while models run on-board | Low (map is prepared offline) |
| Omnicor AI + XREAL glasses | Operator or supervisor view of tickets and robot status served from the local node | Low to medium |

## Questions to ask the Omnicor AI engineers on site

1. What did you physically bring: OC Node units (how many, which chip, power input, interfaces, mounting) or software and people only?
2. Which robots here already run an Omnicor deployment, and with which models (GO-1, GraspVLA, OpenVLA, pi0.5)?
3. How long does OC Agent need to port a new model to a given robot computer: hours or days? What do you need from us (weights format, sample inputs, accuracy target)?
4. How do we call a deployed model: ROS 2 node, HTTP / gRPC, Python library? Is there a streaming interface for LLM tokens?
5. What control rate do you reach for a VLA on-board, and what response time for an 8B-class LLM such as Apertus?
6. Which local speech-to-text and vision-language models can you deploy alongside the LLM on one device?
7. Can you give us before / after numbers (latency, memory, watts) that we may show in the final pitch?
8. What was the L4 logistics-vehicle work: which sensors and models, and is any of it reusable for a small delivery robot?

## Decision rule

- **Pick Omnicor AI for T01 if** your idea's selling point is a service or delivery robot that keeps working offline (or keeps data private), you already have a robot from another vendor, and the Omnicor team confirms in the first hours that they can put your model on that robot's compute.
- **Avoid if** you need a robot body, navigation or documented APIs from this vendor, if nobody from Omnicor can commit time to your team, or if your demo looks the same with a laptop or cloud model.

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [OpenVLA repository](https://github.com/openvla/openvla)
- [pi0.5 base model in LeRobot (Hugging Face)](https://huggingface.co/lerobot/pi05_base)
- [Apertus 8B Instruct model card (Hugging Face)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [Omnicor AI company profile (internal)](../Omnicor-AI.md)
