---
type: challenge-playbook
company: "AGIBOT"
slug: AGIBOT
challenge: T04
updated: 2026-11-14
tags: [leukerbad-hackathon, t04, playbook]
---
# AGIBOT × T04 — Hackathon Playbook

⬆ [AGIBOT profile](../AGIBOT.md) · [Brief](AGIBOT-T04-1-Brief.md) · [Products and solutions](AGIBOT-T04-2-Products-and-Solutions.md)

**Ground rules for every concept**

- First 30 minutes: confirm **which variant** is on site (X2 Ultra vs X2 EDU), its firmware, and the matching AimDK version. Voice / screen and end-effector interfaces are documented for Ultra only.
- Put perception and the LLM **off-board** (laptop, or a D-Robotics RDK). The X2 vision interface is not enabled in the SDK.
- Keep the humanoid at least an arm's length plus a step from any seated "patient"; a spotter holds the emergency stop. Never pitch physical support.
- Start ROS nodes slowly (about 2 per second) while the robot is standing — the docs warn that DDS flooding can make it fall.

## Solution approaches

### Concept 1 — "Kurbad Coach": seated rehab-exercise coach (safest)

- **Problem → value:** Rehab guests get a few supervised sessions and are then left to repeat exercises alone; adherence drops. A robot that demonstrates, counts and encourages extends the therapist's reach without touching the patient.
- **Hardware:** X2 Ultra · laptop with webcam (or D-Robotics RDK X5 + camera) · optional OriginFlow EMG band for muscle-effort feedback · optional XREAL glasses showing the target pose.
- **Architecture / stack:**
  - Perception: off-board camera → open-source human-pose estimation → joint angles → repetition counter and range-of-motion score.
  - Planning: small state machine (greet → demonstrate → count → correct → summarise); LLM only for phrasing and small talk.
  - Control: AimDK_X2 over ROS 2 — preset motions or upper-body control for the demonstration, TTS service for speech, emoji service for the face. Robot stays in stable standing; no walking needed.
  - Compute: laptop on the robot's network; nothing on board.
- **48-hour plan:**
  - H0–6: network + SDK version check; trigger TTS, one emoji, one preset motion from the laptop. Pose estimation running on the webcam.
  - H6–24: three exercises (arm raise, shoulder abduction, seated knee extension shown by arm gesture + speech); rep counter; upper-body trajectories rehearsed in the X2 MuJoCo sim first.
  - H24–40: feedback rules ("higher", "slower"), session summary for the therapist (simple web page), German / English speech; add EMG or AR only if the core loop is solid.
  - H40–48: freeze, rehearse the demo ten times, record a backup video.
- **3-minute demo script:** 0:00 problem in one sentence (Leukerbad clinics, home exercise drop-off) → 0:30 volunteer sits, robot greets and demonstrates → 1:00 volunteer does five reps, robot counts aloud and corrects one deliberately shallow rep → 2:00 therapist dashboard shows range of motion and adherence → 2:30 what a clinic pilot would look like.
- **Risks and fallbacks:** only EDU on site → play audio from a laptop speaker and keep the robot for gestures. Upper-body control too fiddly → use preset motions only. Wi-Fi congestion → wired Ethernet to the robot.
- **Judging angles:** *Innovation* — moderate (embodied coach, not a screen). *Technical depth* — closed loop from pose to feedback; EMG fusion lifts it. *Impact* — adherence is a known rehab problem; no contact means a short path to a real pilot. *Leukerbad* — direct fit with the thermal-spa rehab clinics.

### Concept 2 — Clinic concierge and therapy-room escort

- **Problem → value:** Elderly guests get lost between reception, pool and therapy rooms and miss appointments; staff time goes into wayfinding and reminders.
- **Hardware:** X2 Ultra (or A2 Ultra if AGIBOT staff configure LinkSoul for you) · optional SKYLANDX MetaCam to scan the venue once for a map.
- **Architecture / stack:**
  - Start from `agibot_agentsdk_sample_code` (hospital guide): replace the knowledge base with clinic schedule, room list and spa rules; keep the intent routing and the skill whitelist.
  - Speech: the sample handles Simplified Chinese and English. For German / French, run your own ASR and TTS on a laptop using the raw microphone stream topic and audio playback.
  - Escort: locomotion commands at **≤ 0.5 m/s**; route as scripted waypoints (the SLAM / navigation module is optional and may not be installed).
  - Compute: LLM via an OpenAI-compatible endpoint; LinkSoul gateway needs AGIBOT credentials.
- **48-hour plan:**
  - H0–6: get App ID / Key / Secret and Agent Code from AGIBOT staff; run the sample unchanged.
  - H6–24: clinic knowledge base; appointment reminder flow; German speech path.
  - H24–40: short escort along a fixed corridor; "follow me, I will walk slowly" behaviour with pauses; hand-off message to staff.
  - H40–48: rehearse; fallback video.
- **3-minute demo script:** guest asks in German where the hydrotherapy is → robot answers, shows the time on its face screen, offers to walk there → walks 5 m slowly, checks back verbally → reminds about the next appointment and medication time.
- **Risks and fallbacks:** no credentials or no cloud access → bypass LinkSoul, keep your own speech + LLM loop. Navigation unavailable → stationary concierge plus a short teleoperated walk, declared as such. Noisy hall → push-to-talk or a lapel microphone.
- **Judging angles:** *Innovation* — low to moderate. *Technical depth* — moderate (agent routing, multilingual speech). *Impact* — closest to what AGIBOT already deploys (guiding), so credible. *Leukerbad* — multilingual tourist and clinic setting.

### Concept 3 — Night-round and fetch companion on four legs

- **Problem → value:** Night staff are thin; falls are found late. A quiet quadruped does corridor rounds, spots a person on the floor, alerts the carer and brings a call button, water or a blanket (up to 5 kg).
- **Hardware:** D1 Ultra (IP54, 5 kg payload) with a basket · depth camera + small computer on its back (D-Robotics RDK X5 fits the role) · optional X2 Ultra as the "voice" at the bedside.
- **Architecture / stack:**
  - Perception: on-back camera → person detection + pose → "lying on floor for more than N seconds" rule.
  - Planning: patrol waypoints; on detection, stop at a distance, speak through a speaker ("Are you all right?"), send an alert with a snapshot to a phone.
  - Control: D1 open SDK (velocity commands) from the back-mounted computer over Ethernet. Follow-me and navigation are **not** built in — script them.
  - Compute: fully on the dog; phone alert over Wi-Fi.
- **48-hour plan:**
  - H0–6: mount camera and computer, power from the dog's port, drive the dog from code.
  - H6–24: fall detector on recorded clips; patrol loop along a marked corridor.
  - H24–40: alert pipeline; fetch run with basket; voice check-in; test on a ramp and a stair outside.
  - H40–48: rehearse with a volunteer on a mat; backup video.
- **3-minute demo script:** dog patrols → volunteer lies down on a mat → dog stops, asks, no reply → carer phone buzzes with image and location → dog returns with the basket (blanket, call button).
- **Risks and fallbacks:** payload power or mounting problems → carry a battery pack. Unreliable patrol → teleoperate the walk, keep detection autonomous. Privacy objection → process on-device, send a skeleton image instead of video.
- **Judging angles:** *Innovation* — moderate. *Technical depth* — moderate, self-integrated autonomy. *Impact* — fall response time is a clear metric. *Leukerbad* — works on slopes, snow slush and chalet stairs where wheeled robots fail.

### Concept 4 — Tele-care hands: remote fetch and handover (most ambitious)

- **Problem → value:** A relative or carer far down the valley helps with small physical tasks (pass the glasses, open the pill box, bring the cup) through a robot, with learned autonomy taking over repeated tasks.
- **Hardware:** G2 or G1 with OmniPicker / OmniHand (requires AGIBOT staff and Genie Studio) · XREAL glasses for the operator's view · optional OriginFlow EMG for grip-intent input. Low-budget variant: X2 Ultra with OmniPicker for objects under 1 kg.
- **Architecture / stack:**
  - Stage A: teleoperation (Genie Studio rig or OmniGlove) with a video feed to the operator.
  - Stage B: collect 50–100 demonstrations of one handover task; fine-tune a GO model in Genie Studio, or GO-1 from the open weights if a GPU is available.
  - Safety: use the gripper "stalled" / "object dropped" states and low speed for release-on-pull handover.
- **48-hour plan:**
  - H0–6: confirm a G-series robot and teleoperation are actually available; if not, drop to the X2 variant or switch concept.
  - H6–24: reliable teleoperated fetch of three objects; start recording demonstrations.
  - H24–40: fine-tune and evaluate one autonomous task; keep teleoperation as the default path.
  - H40–48: rehearse both modes; backup video.
- **3-minute demo script:** "daughter" in another room sees the scene in AR glasses → guides the robot to bring a pill box → then says "do it again" and the robot repeats the task autonomously → handover releases only when the "patient" pulls.
- **Risks and fallbacks:** no G-series access (likely) → X2 variant with a light object. Fine-tuning fails → show teleoperation plus the data pipeline. Latency → wired link.
- **Judging angles:** *Innovation* — high (shared autonomy for care). *Technical depth* — high (VLA fine-tuning). *Impact* — strong story, long path to deployment. *Leukerbad* — remote valleys and thin care staffing.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| X2 Ultra + D-Robotics RDK X5 | Off-board pose estimation and speech without a laptop | Low — ROS 2 on both sides |
| X2 Ultra + OriginFlow EMG | Coach reacts to real muscle effort, not just pose | Medium — depends on OriginFlow's data API |
| X2 Ultra + XREAL glasses | Patient sees target pose overlay; therapist sees live metrics | Medium |
| X2 Ultra (voice, face) + Flexiv Rizon or ROKAE xMate (force-controlled arm) | Robot explains while a force-controlled arm does guided passive motion or resistance training | High — two stacks, contact-safety design |
| D1 Ultra + SKYLANDX MetaCam | Scan the venue once, patrol against the map | Medium — map format conversion |
| D1 Ultra + X2 Ultra | Dog fetches, humanoid talks | Medium — two SDKs, simple message bus |
| OmniHand 3 + another vendor's arm | Tactile, gentle handover on a stronger arm | Medium — mechanical adapter + SDK |

## Questions to ask the AGIBOT engineers on site

1. Which exact units can teams program — X2 Ultra, X2 Ultra (new version) or X2 EDU? Firmware and matching AimDK version?
2. On X2 EDU, is there any supported way to use TTS, the microphone stream and the face screen?
3. Can teams get LinkSoul / AgentSDK credentials (App ID, Key, Secret, Agent Code) and the offline `linksoul-agentsdk` wheel this weekend? Does it work from a Swiss network?
4. Is the SLAM / navigation module installed, and is any camera stream accessible from the SDK today?
5. Which end-effectors are mounted (OmniPicker, OmniHand)? Is force or effort control available on them?
6. Is a G1 or G2 with a teleoperation rig and Genie Studio access available to hackathon teams, and how long does a fine-tune take on site?
7. What are the rules for operating the humanoid near seated volunteers (stand-off distance, emergency stop, speed cap)?
8. Has AGIBOT run any elderly-care, hospital or rehab pilot we may cite — including the reported family-care partnership?

## Decision rule

- **Pick AGIBOT for T04 if** your idea is interaction-first (coach, companion, concierge, reminders, night rounds) and an X2 Ultra or a D1 is confirmed available with a matching SDK.
- **Avoid if** your idea needs lifting, body contact, force-controlled therapy or certified medical hardware, or if only X2 EDU / showpiece A-series units are on site and no engineer can unlock the interaction stack.

## Sources

- [AGIBOT company profile (this repo)](../AGIBOT.md)
- [AimDK_X2 documentation — overview](https://x2-aimdk.agibot.com/en/latest/)
- [AimDK_X2 — robot specifications](https://x2-aimdk.agibot.com/en/latest/about_agibot_X2/robot_specifications.html)
- [AimDK_X2 — interaction interfaces](https://x2-aimdk.agibot.com/en/latest/Interface/interactor/index.html)
- [AimDK_X2 — LinkSoul cloud interaction](https://x2-aimdk.agibot.com/en/latest/Interface/interactor/linksoul.html)
- [AimDK_X2 — end-effector control](https://x2-aimdk.agibot.com/en/latest/Interface/control_mod/endeffector.html)
- [AGIBOT — D1 Ultra product page](https://www.agibot.com/products/D1Ultra)
- [AGIBOT — A2 Ultra product page](https://www.agibot.com/products/A2_Ultra)
- [AGIBOT — G2 product page](https://www.agibot.com/products/G2)
- [AGILINK — OmniHand 3](https://www.agilink-ai.com/omni-hand3.html)
- [GitHub — AgibotTech repositories](https://github.com/orgs/AgibotTech/repositories)
- [GitHub — agibot_agentsdk_sample_code](https://github.com/AgibotTech/agibot_agentsdk_sample_code)
- [GitHub — AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)
