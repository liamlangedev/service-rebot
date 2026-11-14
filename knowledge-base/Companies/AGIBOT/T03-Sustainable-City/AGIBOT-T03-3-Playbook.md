---
type: challenge-playbook
company: "AGIBOT"
slug: AGIBOT
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# AGIBOT × T03 — Hackathon Playbook

⬆ [AGIBOT profile](../AGIBOT.md) · [Brief](AGIBOT-T03-1-Brief.md) · [Products and solutions](AGIBOT-T03-2-Products-and-Solutions.md)

> AGIBOT is a **2/5** fit for T03: no sustainability product or reference code. The concepts below use its robots as a general-purpose body. **First action at H0: confirm which units are on site and what SDK access you get.**

## Solution approaches

### Concept 1 — Heat-loss and waste patrol dog (safest)
- **Problem → value:** Alpine hotels and spa buildings lose heat through open windows, uninsulated pipes and idle equipment. A walking audit finds losses without installing fixed sensors → a ranked fix list for the building manager.
- **Hardware:** D1 Ultra / Edu + your own sensor pod (thermal camera, CO₂ / temperature / humidity) on the back. Optional: D-Robotics RDK X5 as on-robot compute; SKYLANDX MetaCam for the 3D base map.
- **Architecture / stack:** sensor pod → edge board (detection of hot / cold anomalies, timestamps, pose) → laptop dashboard. Locomotion through the D1 SDK high-level commands; teleoperate or follow waypoints. Localisation from an add-on LiDAR or simply odometry plus fiducial markers. All compute off the robot's own controller.
- **48-hour plan:**
  - **H0–6:** get the D1 walking via SDK; mount and power the pod (check the power port rating); log one sensor stream.
  - **H6–24:** anomaly detection on thermal frames; pose tagging; walk one real corridor or façade.
  - **H24–40:** map overlay, ranking by estimated loss, repeat run to show before / after (close a window, re-scan).
  - **H40–48:** rehearse, record backup video, freeze code.
- **3-minute demo script:** (0:00) problem in one sentence → (0:30) D1 walks a short route with stairs → (1:30) live dashboard marks two anomalies → (2:15) fix one, re-scan, marker clears → (2:40) cost and scaling slide.
- **Risks and fallbacks:** D1 not on site → same pod on any quadruped (Unitree Go2, Genisom, Magiclab). Autonomy too slow → joystick-driven route with automatic logging. Savings figures → present as estimates, never as measured.
- **Judging angles:** innovation medium · technical depth medium (sensor fusion, mapping) · impact high and concrete · Leukerbad relevance high (heating demand, thermal-water infrastructure, steep site).

### Concept 2 — Recycling coach at the collection point
- **Problem → value:** Visitors unfamiliar with Swiss separation rules mis-sort waste. A friendly robot identifies the item held up and directs it to the right bin, in the guest's language → less contamination, countable data per fraction.
- **Hardware:** X2 (Ultra or Edu) + external webcam and laptop. Optional: XREAL glasses as a staff view of statistics.
- **Architecture / stack:** webcam → vision-language model on laptop (item class + fraction) → AimDK_X2 calls: TTS, screen emoji / video, preset motion or upper-body pointing gesture. Use the external camera because the on-board vision interface is marked "to be enabled". Log every decision to a simple counter dashboard.
- **48-hour plan:**
  - **H0–6:** match SDK to firmware; run the TTS, emoji and preset-motion examples.
  - **H6–24:** classifier for about 6 fractions; map each to speech + gesture; multilingual prompts.
  - **H24–40:** uncertainty handling ("show me the label"), statistics screen, test with strangers.
  - **H40–48:** polish timing, backup video.
- **3-minute demo script:** (0:00) show a mixed bag → (0:20) volunteer holds up three items; robot answers and points → (1:40) a tricky item triggers a clarifying question → (2:10) dashboard: items sorted, contamination avoided → (2:40) rollout idea for hotels and lift stations.
- **Risks and fallbacks:** judged as "kiosk with legs" → add measured accuracy and the data loop. X2 not available → A2 Ultra (limited SDK) or any speaking robot. Noisy hall → push-to-talk or screen-only flow.
- **Judging angles:** innovation low–medium · technical depth low–medium · impact medium (behaviour change, hard to quantify) · Leukerbad relevance high (international guests).

### Concept 3 — Recyclables sorting cell with a learned policy
- **Problem → value:** Small municipalities cannot afford sorting plants; mixed PET, cans and cartons get burned. A mobile manipulator that sorts at the collection point raises recovery without new infrastructure.
- **Hardware:** G2 or G2 Air (only with AGIBOT staff support). Fallback body: Flexiv / ROKAE / Dobot arm with **OmniPicker 3** (140 N, 110 mm stroke, tactile). Optional: Galaxea or Galbot mobile manipulators as alternative platforms.
- **Architecture / stack:** RGB-D → open-vocabulary detector → grasp pose → arm motion; or teleop demonstrations → fine-tune GO-1 (action-expert only, about 24 GB GPU) → inference on a workstation (about 7 GB GPU). Prototype the task in Genie Sim (G2 maintained) while waiting for robot time.
- **48-hour plan:**
  - **H0–6:** secure robot slot and Genie Studio / teleop access; set up three bins and ten objects; decide classical vs learned.
  - **H6–24:** classical pipeline end to end on 3 classes; in parallel collect 50–100 teleop episodes.
  - **H24–40:** fine-tune and compare learned vs classical; add tactile check for crushed vs full containers.
  - **H40–48:** fix the best-performing path, measure success rate over 20 picks, record video.
- **3-minute demo script:** (0:00) dump mixed items → (0:20) robot sorts five items live → (1:40) show failure recovery (re-grasp) → (2:10) success-rate table and throughput → (2:40) cost per tonne argument.
- **Risks and fallbacks:** no G-series access → arm + OmniPicker cell. Fine-tuning does not converge → ship the classical pipeline and show the learned one in sim. OmniPicker integration on a foreign arm (CAN-FD / RS485, voltage, flange) may eat hours — confirm cabling at H0.
- **Judging angles:** innovation medium · technical depth high · impact high if throughput is honest · Leukerbad relevance medium.

### Concept 4 — Scout and collect: two-robot litter loop (most ambitious)
- **Problem → value:** Litter along paths and around lift stations is found late, especially after snow melt. A quadruped scouts and geo-tags; a manipulator collects and sorts on flat ground → cleaner trails with fewer vehicle trips.
- **Hardware:** D1 Ultra (scout with camera) + G2 Air or another vendor's wheeled manipulator (collector). Optional: D-Robotics board for on-dog detection; SKYLANDX map.
- **Architecture / stack:** D1 camera → litter detector on edge board → tagged positions in a shared map → task queue → manipulator navigates, picks, sorts by class. ROS 2 as the common bus; each robot keeps its vendor controller.
- **48-hour plan:**
  - **H0–6:** two sub-teams; agree on map frame and message format.
  - **H6–24:** scout detection and tagging; collector pick-and-drop at a fixed spot.
  - **H24–40:** connect the queue; one full loop on a 5 × 5 m arena.
  - **H40–48:** reliability runs; cut scope to what works.
- **3-minute demo script:** (0:00) scatter items → (0:20) D1 patrols and tags on a live map → (1:20) collector drives to tag, picks, sorts → (2:20) summary: items found, collected, fraction → (2:40) outlook.
- **Risks and fallbacks:** integration of two stacks is the main risk → demo the halves separately with a shared map. Outdoor run is unrealistic for IP42 manipulators → indoor arena. Any robot missing → human collector guided by the scout map.
- **Judging angles:** innovation high · technical depth high · impact medium · Leukerbad relevance high (trails, tourism).

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| D1 + D-Robotics RDK X5 | On-dog low-power perception; a "watts per inspection" story | Low–medium (USB / Ethernet, own power) |
| D1 + SKYLANDX MetaCam | 3D building or street model to anchor sensor readings | Low (offline scan, then overlay) |
| OmniPicker 3 + Flexiv Rizon / ROKAE xMate / Dobot CR | Force-aware sorting cell without needing a G-series | Medium–high (bus, voltage, flange not documented) |
| X2 + XREAL glasses | Staff-side live sorting statistics | Low |
| G2 / G2 Air + Galaxea or Galbot models | Compare VLA policies on the same sorting task | High |
| GO-1 + OriginFlow or MEgo-style data capture | Faster demonstration collection | High, ⚠️ unverified compatibility |

## Questions to ask the AGIBOT engineers on site

1. Which exact models and variants are here for teams, and how many hours of robot time per team?
2. D1: is the SDK high-level only or joint-level too? What voltage and current does the payload power port supply?
3. D1: operating temperature range and behaviour on snow or wet stone?
4. X2: firmware version and matching AimDK release? Is the vision interface enabled on these units?
5. G2 / G2 Air: can teams get Genie Studio accounts and teleoperation for data collection during the event?
6. Can GO-1 or GO-2 be fine-tuned and deployed on the on-site G-series within 48 hours — and on whose GPUs?
7. OmniPicker 3: supply voltage, flange pattern, and is there a ROS 2 driver to run it on a third-party arm?
8. Has AGIBOT done any waste-sorting, recycling or environmental-inspection pilot that is not public?

## Decision rule

- **Pick AGIBOT for T03 if** a D1 with SDK access is available for a sensor-carrier concept, or AGIBOT staff commit a G-series robot plus Genie Studio support for a sorting demo.
- **Avoid if** you need purpose-built sustainability hardware, outdoor manipulation, or a documented manipulation SDK you can use without vendor help.

## Sources
- [AGIBOT company profile (internal)](../AGIBOT.md)
- [AGIBOT — D1 Ultra product page](https://www.agibot.com/products/D1Ultra)
- [AGIBOT — G2 product page](https://www.agibot.com/products/G2)
- [AGIBOT — C5 product page](https://www.agibot.com/products/C5)
- [AGILINK — OmniPicker 3](https://www.agilink-ai.com/omni-picker3.html)
- [AGIBOT — New generation of embodied AI robots and models (2026-04-17)](https://www.agibot.com/article/231/detail/63.html)
- [AimDK_X2 documentation](https://x2-aimdk.agibot.com/en/latest/)
- [GitHub — AgibotTech/genie_sim](https://github.com/AgibotTech/genie_sim)
- [GitHub — OpenDriveLab/Agibot-World (GO-1, dataset)](https://github.com/OpenDriveLab/Agibot-World)
