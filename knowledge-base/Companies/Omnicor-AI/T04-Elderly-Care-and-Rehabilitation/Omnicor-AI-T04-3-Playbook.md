---
type: challenge-playbook
company: "Omnicor AI"
slug: Omnicor-AI
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# Omnicor AI × T04 — Hackathon Playbook

⬆ [Omnicor AI profile](../Omnicor-AI.md) · [Brief](Omnicor-AI-T04-1-Brief.md) · [Products and solutions](Omnicor-AI-T04-2-Products-and-Solutions.md)

**Ground rules for building with OmniCor AI**
- It is the **inference layer**, not the robot. Every concept needs hardware from another vendor (or at least a laptop / edge board).
- Nothing about OC Agent or OC Node is documented. **Build every concept so it also runs on a plain open-source edge stack** (llama.cpp / Ollama, whisper.cpp, MediaPipe); treat OmniCor as the accelerator and the on-robot port, not as a dependency.
- Hour 0 task for all concepts: ask the OmniCor engineers what is physically here and how fast they can port a model (questions below).

## Solution approaches

### Concept 1 — "Unplugged" care companion (safest)

- **Problem → value:** Elderly guests and rehab patients need reminders (medication, therapy slots, drinking), orientation and conversation in their own language. Cloud voice assistants send audio off-site. A fully local assistant keeps health talk private and works with no network.
- **Hardware:** OC Node if available, otherwise a Jetson-class board or D-Robotics RDK, plus microphone and speaker. Optional body: any robot with a head or screen (UniX AI Wanda, AGIBOT X2, Unitree G1) for presence only.
- **Architecture / stack:** microphone → offline speech-to-text (whisper.cpp) → local LLM (Apertus 8B or a smaller Mistral / Qwen variant, quantised; port and tuning via OC Agent ⚠️ unverified) with a small tool set (schedule lookup, reminder, "call nurse" event) → offline text-to-speech (Piper). All compute on the edge box. Care schedule in a local JSON / SQLite file.
- **48-hour plan:**
  - H0–6: confirm hardware with OmniCor; get speech-in → LLM → speech-out running on a laptop in German, French and English.
  - H6–24: move to the edge box; OmniCor optimises the LLM; add reminders and escalation tool calls; measure reply latency.
  - H24–40: test with noisy audio and slow speech; large-text screen; optional robot body gestures.
  - H40–48: latency numbers on a slide, rehearse, record backup video.
- **3-minute demo script:** (1) Pull the network cable on stage. (2) A "guest" asks in German when physiotherapy is; assistant answers. (3) Switch to French: medication reminder fires, guest confirms. (4) Guest says they feel dizzy → local alert event to a "nurse" tablet over LAN. (5) Show latency before and after optimisation.
- **Risks and fallbacks:** LLM too slow on the board → smaller model or shorter answers; Swiss German dialect fails → ask for Standard German and say so; OmniCor has no time → run the stock quantised model, keep the privacy story.
- **Judging angles:** innovation low-to-medium; technical depth from measured on-device latency; impact from privacy and language coverage; Leukerbad relevance high (multilingual spa and clinic guests, Swiss open model).

### Concept 2 — Private rehab exercise coach

- **Problem → value:** Patients do prescribed exercises alone and incorrectly; therapists cannot watch everyone. A camera-based coach counts repetitions and corrects form — but video of patients must not leave the room.
- **Hardware:** edge box (OC Node or equivalent) + RGB camera + screen. Optional: XREAL glasses for an AR overlay; a humanoid (Unitree G1, AGIBOT X2, Magiclab MagicBot) to demonstrate the movement.
- **Architecture / stack:** camera → MediaPipe Pose Landmarker (33 3D landmarks) → joint-angle and repetition logic (plain Python, rule-based per exercise) → local LLM turns numbers into short spoken coaching and a session summary for the therapist → TTS. Only the text summary is stored; frames are discarded.
- **48-hour plan:**
  - H0–6: pick 3 exercises (e.g. sit-to-stand, shoulder raise, knee extension); pose tracking and angle maths on a laptop.
  - H6–24: repetition counter, range-of-motion thresholds, spoken feedback; port LLM to the edge box with OmniCor.
  - H24–40: therapist summary view; optional AR overlay or robot demonstrator; test with different body sizes, seated users, loose clothing.
  - H40–48: polish, backup video.
- **3-minute demo script:** (1) "Therapist" selects a programme. (2) "Patient" does sit-to-stand; system counts and says "lean forward a little more". (3) Deliberately poor repetition → correction. (4) Show the therapist summary: reps, range of motion, no video stored. (5) Unplug the network to prove it is local.
- **Risks and fallbacks:** pose jitter with occlusion → restrict to frontal view and 3 exercises; LLM adds little → template sentences, LLM only for the summary; no robot demonstrator → on-screen avatar.
- **Judging angles:** strong real-world impact (Leukerbad rehab clinics); technical depth moderate; innovation is the privacy-by-design framing. Be explicit that it is **not a medical device** and gives no clinical assessment.

### Concept 3 — Night-round guardian with on-robot fall detection

- **Problem → value:** Night staff are scarce; falls at night are found late. A robot patrols corridors or checks rooms on request and raises an alert — without streaming video of sleeping residents anywhere.
- **Hardware:** a mobile base from another vendor (quadruped: Unitree Go2, AGIBOT D1, Genisom, Magiclab MagicDog; or a wheeled humanoid) + its camera + OC Node or the robot's own computer running the OmniCor-optimised models.
- **Architecture / stack:** robot camera → on-board person detection and pose (lying on floor, no movement for N seconds) → local LLM / VLM composes a text alert ("person on floor, corridor 2, responsive: unknown") → LAN message to a nurse tablet; robot asks "are you okay?" via local speech stack and reports the answer. Navigation uses the robot vendor's own stack or waypoint teleoperation — do not write a navigation stack in 48 h.
- **48-hour plan:**
  - H0–6: secure a robot; confirm camera access and where extra compute can be mounted and powered.
  - H6–24: fall heuristic on laptop with recorded clips; port to on-board compute with OmniCor; alert channel.
  - H24–40: integrate with patrol route; voice check-in; false-alarm tests (sitting, kneeling, bending).
  - H40–48: rehearse on the demo floor, backup video.
- **3-minute demo script:** (1) Robot walks a short route. (2) Team member lies down; robot stops, asks if they are okay. (3) No answer → alert appears on tablet as text only. (4) Second pass: person kneels to tie a shoe → no alarm. (5) Show that no image left the robot.
- **Risks and fallbacks:** robot access or camera API blocked → fixed camera on a tripod plus the same pipeline; false alarms → require stillness plus failed voice check; compute mounting issues → tethered edge box on LAN.
- **Judging angles:** clear caregiver relief; technical depth in on-board perception under a power budget (OmniCor's stated core case); Leukerbad relevance via clinics and hotels with elderly guests.

### Concept 4 — Voice-commanded fetch-and-hand-over with an on-board VLA (most ambitious)

- **Problem → value:** People with limited mobility need small things fetched (water bottle, glasses, remote). A robot that understands a spoken request and manipulates objects **with all models on-board** is the full assistive-robot story.
- **Hardware:** wheeled dual-arm mobile manipulator from an OmniCor-listed customer — **AGIBOT G1 / G2** or **Galbot G1** — or Galaxea R1, Spirit AI Moz1, UniX AI Wanda. Compute: robot's own computer and/or OC Node.
- **Architecture / stack:** speech → local LLM parses the request into a short task string → VLA policy (pi0.5 via LeRobot, OpenVLA, or the robot vendor's own model such as GO-1, GraspVLA or G0) produces arm actions → vendor low-level controller. OmniCor's job: make the VLA and the LLM share the on-board compute at a usable control rate ⚠️ unverified whether a port already exists for the robot you get.
- **48-hour plan:**
  - H0–6: **go / no-go** — is there a robot already running a VLA through OmniCor? If not, drop to the fallback now.
  - H6–24: one object, one table, one hand-over location; record demonstrations if fine-tuning is feasible (pi0.5 reference fine-tune assumes an 80 GB GPU — check what GPUs exist on site); voice front-end in parallel.
  - H24–40: integrate voice → task → policy; add second object only if the first is reliable; safe hand-over pose, low speed.
  - H40–48: 10 consecutive rehearsals, record the best run.
- **3-minute demo script:** (1) Seated "resident" asks in German for the water bottle. (2) Robot confirms verbally, picks the bottle, brings it to a hand-over tray. (3) Second request in French for glasses. (4) Network unplugged throughout; show on-board resource use.
- **Risks and fallbacks:** fine-tuning not feasible → use the vendor's pretrained grasping model or scripted grasps with the local LLM as planner; control rate too low → run the VLA on a tethered edge box; safety near people → hand over via tray, never directly to a hand, keep an operator on the stop button.
- **Judging angles:** highest innovation and technical depth if it works; highest failure risk. Leukerbad relevance: clinic and hotel rooms, weak in-room connectivity.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| OmniCor AI + AGIBOT (G1 / G2) or Galbot (G1) | On-board VLA fetch-and-carry; both are listed OmniCor customers, so a port may already exist ⚠️ unverified | Medium if a port exists, high otherwise |
| OmniCor AI + D-Robotics RDK | Low-cost bedside companion or coach box; tests OmniCor's "any device" claim on small silicon ⚠️ support unverified | Low to medium |
| OmniCor AI + XREAL | AR-guided therapy with pose and coaching computed locally | Medium (AR app work) |
| OmniCor AI + Unitree Go2 / AGIBOT D1 / Genisom | Night-round patrol with on-robot fall detection | Medium (camera access, mounting, power) |
| OmniCor AI + UniX AI Wanda / Spirit AI Moz1 / Galaxea R1 | Service humanoid with private voice interface | Medium to high (no known prior port) |
| OmniCor AI + Flexiv / ROKAE | Local voice control for a force-controlled physio arm; OmniCor adds only the language layer | Medium; contact safety is the hard part and not OmniCor's |
| OmniCor AI + OriginFlow | EMG intent signals classified on-device for rehab feedback | High (new signal type, no known support) |
| OmniCor AI + Binabik AI / coprod | Swiss software and hardware stack with on-device inference underneath | Unknown — ask both teams |

## Questions to ask the Omnicor AI engineers on site

1. What did you bring: OC Node units (how many, which chip, memory, power, ports), or only software and people?
2. Which robots here already run a model deployed by you — AGIBOT, Galbot? Which model, at what control rate?
3. Which LLM can you run fully offline for a spoken dialogue, and what reply latency and tokens per second should we expect on your hardware?
4. Can you port a model we choose (e.g. Apertus 8B, a pi0.5 fine-tune) within the first 6–12 hours? What do you need from us?
5. How do we call the model: ROS 2 node, HTTP / gRPC endpoint, Python library? Is there any sample code?
6. Do you support speech models (ASR / TTS) and small vision models (pose, detection), or only LLMs and VLAs?
7. Can an LLM and a VLA run at the same time on one OC Node, and what is the power draw on battery?
8. Can you show, technically, that no data leaves the device (no telemetry, no licence call-home)? We want to claim that on stage.

## Decision rule

- **Pick Omnicor AI for T04 if** your idea's core value is privacy or offline operation, you already have a robot or device from another vendor, and the OmniCor engineers confirm in the first hours that they can port your model in time.
- **Avoid if** you need a physical robot, force-controlled contact or documented APIs from this vendor, or if your concept works just as well with cloud inference.

## Sources
- [OmniCor AI official website](https://www.omnicorai.io/)
- [Omnicor AI company profile (this repo)](../Omnicor-AI.md)
- [Apertus-8B-Instruct-2509 model card (Hugging Face)](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509)
- [LeRobot docs — pi0.5 policy](https://huggingface.co/docs/lerobot/pi05)
- [OpenVLA GitHub repository](https://github.com/openvla/openvla)
- [whisper.cpp GitHub repository](https://github.com/ggml-org/whisper.cpp)
- [Piper TTS GitHub repository](https://github.com/OHF-Voice/piper1-gpl)
- [MediaPipe Pose Landmarker guide](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)
