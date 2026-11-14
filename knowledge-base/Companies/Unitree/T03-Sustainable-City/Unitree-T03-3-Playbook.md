---
type: challenge-playbook
company: "Unitree Robotics"
slug: Unitree
challenge: T03
updated: 2026-11-14
tags: [leukerbad-hackathon, t03, playbook]
---
# Unitree Robotics × T03 — Hackathon Playbook

⬆ [Unitree Robotics profile](../Unitree.md) · [Brief](Unitree-T03-1-Brief.md) · [Products and solutions](Unitree-T03-2-Products-and-Solutions.md)

**Before choosing a concept (15 minutes at the booth):** which robots and variants are available (EDU or not), is an Orin / development PC fitted, how many batteries, is there an arm with a mount, and may the robot go outdoors. Everything below assumes **Go2 EDU** and / or **G1 EDU + Dex3-1**; on-site inventory is not confirmed.

## Solution approaches

### Concept 1 — Heat-Loss Hound: energy and water leak patrol (safest)

- **Problem → value:** heating and hot-water losses (open windows, uninsulated pipes, steam and thermal-water leaks, lights left on) go unnoticed between manual rounds. A robot patrol turns them into a ranked, geo-located fix list. Mirrors what Unitree's commercial inspection line does on B2 / A2, scaled down to a building.
- **Hardware:** Go2 EDU (or Go2-W / As2 if offered) + your own USB thermal camera + optional CO₂ / temperature / humidity sensor on a small board. Optional: D-Robotics RDK X5 as low-power perception box; SKYLANDX MetaCam for a one-off 3D site scan.
- **Architecture / stack:** thermal + RGB frames → hot / cold spot segmentation by threshold against ambient, VLM or small detector labels the object (window, pipe, radiator) → waypoint patrol (teach-and-repeat with odometry, or Nav2 over unitree_ros2 with LiDAR) → unitree_sdk2_python sport client for velocity commands, obstacle avoidance on → findings stored with pose → web dashboard with map pins and estimated loss. Compute: laptop or Orin on the robot; dashboard on the laptop.
- **48-hour plan:**
  - **H0–6:** confirm EDU + SDK connection; drive from Python; get thermal camera streaming; pick a route (corridor + plant room + stairs).
  - **H6–24:** waypoint patrol working end to end; anomaly detection on thermal frames; log findings with pose.
  - **H24–40:** dashboard, loss estimate (clearly labelled as a rough estimate), repeat-run comparison ("fixed since last patrol"); stage 3 reliable anomalies (kettle, open window, warm pipe).
  - **H40–48:** rehearse, record a backup video, trim the pitch.
- **3-minute demo script:** 0:00 problem and Leukerbad hook → 0:30 robot starts patrol, climbs a step → 1:15 stops at a staged hot pipe and an open window, pins appear live → 2:15 report: ranked list, estimated energy wasted, second run shows one item cleared → 2:45 scale-up to As2 / A2 outdoors.
- **Risks and fallbacks:** navigation drift → shorten the route, use visual markers at waypoints; no thermal camera available → RGB-only checks (open windows, lights on, dripping taps) with a VLM; only non-EDU dog → drive by remote and run perception only.
- **Judging angles:** *innovation* medium (known pattern, new setting) · *technical depth* medium · *real-world impact* high and measurable · *Leukerbad relevance* high (thermal-water and heating infrastructure, spa buildings, hotels).

### Concept 2 — Litter and bin scout: collect only where needed

- **Problem → value:** fixed collection rounds waste fuel and labour; litter on paths and around bins after tourist peaks is found late. A patrol robot maps litter hot spots and bin fill levels so crews are sent only where needed.
- **Hardware:** Go2 EDU or Go2-W (wheels save energy on paved paths). Optional arm only if the booth has one mounted (D1-T on Go2; D2 on As2 / A2). Optional: XREAL glasses to show crews the pins; SKYLANDX for the base map.
- **Architecture / stack:** front camera → litter / bin detector (pretrained open detector, fine-tuned on ~200 own photos) → LiDAR depth for position and bin-opening fill estimate → pose-tagged observations → route optimiser for the collection crew (simple travelling-salesman heuristic) → dashboard. Control through SDK2 high-level moves; compute on Orin or laptop.
- **48-hour plan:**
  - **H0–6:** SDK check; collect images of staged litter and bins; choose the detector.
  - **H6–24:** detector running on live frames; patrol loop; map with pins.
  - **H24–40:** fill-level estimate, route optimiser, "kilometres saved versus fixed round" calculation; optional pick with arm if hardware exists.
  - **H40–48:** rehearsal, backup video.
- **3-minute demo script:** robot walks a staged path → detects three items and one overfull bin → dashboard builds an optimised pick-up route and shows avoided distance → optional: arm picks one bottle.
- **Risks and fallbacks:** detector misses in mixed lighting → restrict to 3–4 classes and controlled background; no arm → present as scout plus human crew (honest, still useful); outdoor use on Go2 is weather-dependent → demo indoors or under cover.
- **Judging angles:** *innovation* medium · *technical depth* medium · *impact* medium-high if you quantify avoided trips · *Leukerbad relevance* high (tourist paths, seasonal peaks, steep streets).

### Concept 3 — Learned sorting station: G1 sorts recyclables from demonstrations

- **Problem → value:** small sites (hotels, clinics, events) cannot justify an industrial sorting line; mixed waste lowers recycling rates. A general-purpose robot taught by demonstration sorts a few item classes into the right bins.
- **Hardware:** G1 EDU + Dex3-1 (or G1-D if on site — safer, wheeled, wrist cameras). XR headset supported by xr_teleoperate (Apple Vision Pro, PICO 4 Ultra Enterprise, Meta Quest 3; XREAL support not confirmed). GPU laptop or workstation for training.
- **Architecture / stack:** teleoperate with xr_teleoperate (`--record`) → convert episodes with unitree_lerobot → train ACT (fastest to converge) → deploy on robot; an RGB classifier chooses which bin and conditions or selects the policy. Compute: training off-board on GPU, inference on PC2 / laptop.
- **48-hour plan:**
  - **H0–6:** teleoperation working; fix the scene (table height, 3 bins, 3 item types: PET bottle, can, paper cup); record first 10 episodes.
  - **H6–24:** record **50–100 episodes per item type**; start training early and iterate overnight.
  - **H24–40:** on-robot evaluation, add recovery demos for failures, add the classifier and a counter ("items diverted").
  - **H40–48:** freeze the best checkpoint; rehearse with fixed item positions.
- **3-minute demo script:** show 20 s of teleoperated teaching → robot sorts three items autonomously → counter and contamination estimate update → explain how a new item class is added in an afternoon.
- **Risks and fallbacks:** policy unreliable → run teleoperated with "shared autonomy" framing and show training curves; G1 balance near a table → sit or support the robot, or use G1-D; no GPU → reduce to one item class or script the motion with fixed poses.
- **Judging angles:** *innovation* medium-high · *technical depth* high · *impact* modest today (throughput is low — say so) · *Leukerbad relevance* medium (hotels, clinics, events).

### Concept 4 — Scout-to-sorter loop with an agent in charge (most ambitious)

- **Problem → value:** closes the loop from finding waste to recycling it, as a small multi-robot service a municipality could run off-peak.
- **Hardware:** Go2 EDU scout with a carry basket + a fixed sorting cell: G1-D / G1 EDU, or a cross-vendor arm (Dobot CR / Flexiv Rizon / ROKAE xMate). Optional D-Robotics board as the low-power coordinator.
- **Architecture / stack:** Concept 2 perception on the dog → human or arm loads the basket → dog delivers to the cell → Concept 3 policy or scripted pick-and-place sorts → an LLM agent schedules tasks through tool calls, following the unitree_robotskills pattern (bounded tools over SDK2, observe → reason → act → verify). Shared state over ROS 2 or a simple message bus.
- **48-hour plan:**
  - **H0–6:** split the team in two (scout / cell); agree the hand-over point and the message format.
  - **H6–24:** each half works stand-alone.
  - **H24–40:** integrate hand-over and the agent; cut scope hard if integration is not done by H36.
  - **H40–48:** rehearse the single golden path only.
- **3-minute demo script:** dog finds an item → carries it to the cell → sorter bins it → dashboard shows the loop and the agent's decisions.
- **Risks and fallbacks:** integration time is the killer → fall back to Concept 2 and Concept 3 shown side by side; two vendors, two SDKs → keep the interface to one message ("item delivered at station").
- **Judging angles:** *innovation* high · *technical depth* high · *impact* medium (story stronger than throughput) · *Leukerbad relevance* medium.

## Cross-vendor combos worth considering

| Combo | What it enables | Integration effort |
|---|---|---|
| Go2 EDU + SKYLANDX MetaCam | Accurate 3D base map of the site; robot findings pinned on it | Low — offline scan, shared coordinate frame by hand |
| Go2 EDU + D-Robotics RDK X5 / S100 | Low-power on-board perception; "low-power edge AI" story | Low–medium — Ethernet + DDS / ROS 2 |
| Go2 scout + Dobot / Flexiv / ROKAE arm cell | Reliable sorting with a fixed arm; dog does logistics | Medium — two SDKs, one hand-over message |
| G1 EDU + WUJI Hand | Finer grasping of mixed waste | High — mechanical and driver integration; not advised in 48 h |
| Go2 EDU + XREAL glasses | Field crew sees leak / litter pins in AR | Medium — separate app, shared map |
| G1 EDU + OriginFlow EMG capture | Alternative demonstration capture for sorting skills | High / unproven ⚠️ unverified |

## Questions to ask the Unitree Robotics engineers on site

1. Which exact variants are here — **Go2 EDU or Air / Pro / X**, G1 EDU or base — and is the Orin / PC2 fitted?
2. Is there an open navigation or mapping API on the Go2 EDU (go-to-pose, saved maps), or do we bring our own SLAM / Nav2?
3. Which DDS topics give LiDAR point clouds and odometry on this firmware, and at what rate?
4. Is any arm available with a mount and power cable (D1-T on Go2, D2 on As2 / A2, Z1), and is its SDK on the laptop image?
5. Are any inspection payloads here (thermal gimbal, gas sensor), and can teams read their data?
6. How do we power a 5 V / 12 V sensor and USB device from the dog — which port, what current limit?
7. For G1: which hands are fitted, which XR headsets are available for xr_teleoperate, and is there a GPU for training?
8. How many batteries and chargers per team, may the robot leave the building, and where is the remote e-stop?

## Decision rule

- **Pick Unitree Robotics for T03 if** your idea is *go there and measure* — energy, water, litter or environmental monitoring across stairs, slopes or snow — and you can bring the sensor and the analytics yourself; or you want to show learned sorting on a humanoid and have a GPU and people to record demonstrations.
- **Avoid if** your idea needs reliable, fast manipulation (sorting throughput, disassembly, EV plug-in), a ready-made sustainability application, or you can only get a non-EDU robot.

## Sources

- [Unitree Robotics company profile (internal)](../Unitree.md)
- [Unitree — Advanced quadruped inspection solution](https://www.unitree.com/mobile/industry/electricity)
- [Unitree Go2-W product page](https://www.unitree.com/go2-w)
- [Unitree D2 product page](https://www.unitree.com/D2)
- [Unitree Z1 product page](https://www.unitree.com/z1)
- [Unitree GitHub organisation](https://github.com/unitreerobotics)
- [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python)
- [xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate)
- [unitree_lerobot](https://github.com/unitreerobotics/unitree_lerobot)
- [unitree_robotskills](https://github.com/unitreerobotics/unitree_robotskills)
