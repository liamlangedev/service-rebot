---
type: dev-guide
company: "XREAL"
slug: XREAL
updated: 2026-11-14
tags: [leukerbad-hackathon, dev-guide]
---
# XREAL — Developer Guide (hackathon edition)

⬆ [XREAL profile](XREAL.md) · [Product portfolio](XREAL-Products.md) · [Roadmap and strategy](XREAL-Roadmap-and-Strategy.md)

> XREAL is an XR vendor, not a robot vendor. The robot-centric headings of the template are adapted: "control levels" becomes "integration levels", and so on. Research note: live web search was unavailable for this guide; everything below comes from direct reads of the official docs, the official GitHub org, Android / Unity pages and the sources already used in the profile.

## TL;DR — how you program it

- **Three stacks, do not mix them up:** (1) no code — glasses are a **USB-C DisplayPort monitor**; (2) **XREAL SDK 3.1.0** — a **Unity (C#)** package for One series / Air 2 Ultra, app runs on an **Android host** (Beam Pro or Samsung S24 / S25); (3) **Android XR** (Unity 6.5 + OpenXR) — **AURA only**.
- **Check the glasses model before you plan features.** Per the official compatibility table: **One series + XREAL Eye = 6DoF head pose + RGB camera, but no hand tracking, planes, image tracking, depth mesh or anchors.** Those need **Air 2 Ultra** (XREAL SDK) or **AURA** (Android XR).
- **Fastest 48-hour route:** render your operator UI (RViz, web dashboard, camera feed) on a laptop or robot computer and show it in the glasses. Zero SDK work, works in 5 minutes.
- **No official ROS 2 package, no Python / C++ / Unreal SDK, no simulation assets, no robot models.** Robot integration = your Unity app talks to ROS 2 over a bridge (ROS-TCP-Connector, rosbridge WebSocket or plain UDP).
- **Hard gotchas:** do **not** update the host to **Android 16**; turn off **Samsung DeX**; 6DoF on One + Eye needs the **latest glasses firmware**; the host's USB-C port is occupied by the glasses, so debug over **wireless ADB**.

## SDKs and interfaces

| SDK / repo | Language | What it controls | Link | Notes |
|---|---|---|---|---|
| **USB-C DP Alt Mode** (no SDK) | none | Glasses as a 1080p / 1200p external display; on X1 glasses (One, One Pro, 1 Pro+, 1S, R1) the screen can be anchored in 3DoF by the glasses themselves | — | ✅ Works with any DP-Alt-Mode host. Check your laptop / SBC port first |
| **XREAL SDK 3.1.0 for Unity** (`com.xreal.xr.tar.gz`) | C# (Unity 2021.3 / 2022.3 / 6000.0 LTS) | Head tracking (0 / 3 / 6DoF), hand tracking, planes, image tracking, depth mesh, spatial anchors, RGB camera, recording, phone-as-controller — **feature set depends on glasses model** (table below) | [docs](https://docs.xreal.com/) · [download](https://developer.xreal.com/download) | ✅ Released 25 Nov 2025. Built on Unity XR Plug-in framework, AR Foundation, XR Interaction Toolkit, XR Hands. Replaces NRSDK 2.x |
| **ControlGlasses 3.1.0** (APK) | — | Companion app on Samsung phones: switches glasses to 3D mode and launches SDK apps | [release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.1.0) | ✅ Required on phones. On Beam Pro the equivalent is **MyGlasses 1.11.0** |
| **First Person View + StreamingReceiver V1.2.0** | Unity prefab + Windows exe | Record or stream the wearer's view to a **Windows PC** on the same LAN | [docs](https://docs.xreal.com/Tools/First%20Person%20View) | ✅ Real-world video only with One series + Eye; other glasses stream virtual content only |
| **Simulator (Unity Editor)** | C# | Test scenes in the Editor without glasses (uses Unity's XR Device Simulator) | [docs](https://docs.xreal.com/Tools/Emulator) | ✅ |
| **CloudXR client** | — | Stream **SteamVR** content from a Windows PC with NVIDIA GPU to the glasses over Wi-Fi | [docs](https://docs.xreal.com/Tools/XR%20Streaming) | ✅ For One series use CloudXR server **3.2** (4.0.1 crashes, will not be fixed) |
| **MRTK3 integration** | C# | Microsoft MRTK3 UI / interaction on top of XREAL SDK | [docs](https://docs.xreal.com/MRTK3_Integration) | ✅ Documented; the GitHub fork was last updated Sep 2024 |
| **Android XR — Unity** (Unity OpenXR: Android XR + Android XR Extensions for Unity) | C# (Unity 6.5) | **AURA only:** hand tracking, planes, anchors (persistent / shareable), marker tracking, occlusion, dimming control, puck trackpad input | [Android docs](https://developer.android.com/develop/xr/unity) · [Unity blog](https://unity.com/blog/unity-android-xr-wired-glasses-support) · [extensions repo](https://github.com/android/android-xr-unity-package) | ✅ OpenXR + **Vulkan** + URP recommended. **No eye tracking on AURA**. One APK can target Galaxy XR and AURA |
| **Android XR — other paths** (Jetpack XR SDK, native OpenXR, WebXR) | Kotlin / C++ / JS | AURA only | [Android XR](https://developer.android.com/develop/xr) | Listed by Google for Android XR in general; per-feature support on AURA ⚠️ unverified |
| `nreal-ai` GitHub org | mixed | 7 public repos, mostly legacy NRSDK samples and WebXR forks; newest is `uvc_android` ("uvc test with puck", C++, Jun 2026) | [GitHub](https://github.com/nreal-ai) | The SDK itself is **not** on GitHub — download the tarball |
| Community Linux drivers (unofficial) | Rust / C | Read head IMU over USB on Linux without Android | [XRLinuxDriver](https://github.com/wheaney/XRLinuxDriver) · [ar-drivers-rs](https://github.com/badicsalex/ar-drivers-rs) | ⚠️ unverified for current One-series / 1 Pro+ firmware; not checked today; no XREAL support |

**Feature matrix — XREAL SDK 3.1.0 (official compatibility page):**

| Feature | One series + XREAL Eye | Air / Air 2 / Air 2 Pro | Air 2 Ultra |
|---|---|---|---|
| Head tracking | **6DoF** (3DoF without Eye) | 3DoF | **6DoF** |
| Hand tracking | No | No | **Yes** |
| Plane detection | No | No | **Yes** |
| Image tracking | No | No | **Yes** |
| Depth mesh | No | No | **Yes** |
| Spatial anchors | No | No | **Yes** |
| RGB camera frames | **Yes** (YUV_420_888) | No camera | No (dual grayscale SLAM cameras, not exposed as RGB) |
| First-person view | App + real world | App only | App only |
| Phone as 3DoF controller | Yes | Yes | Yes |
| Editor simulator | Yes | Yes | Yes |

1 Pro+ is not yet listed in the SDK docs (they stop at One / One Pro / 1S) — SDK behaviour on 1 Pro+ ⚠️ unverified; ask at the booth.

## Control levels

There is no robot to control; think of four **integration levels**, from cheapest to deepest.

| Level | What you get | Effort | Hardware needed |
|---|---|---|---|
| **L0 — Monitor** | Private big screen for any UI. Refresh up to **120 Hz** (R1: 240 Hz) | 5 min | Any glasses + DP-Alt-Mode host |
| **L1 — On-glasses 3DoF (X1 chip)** | Screen stays fixed in space while the head turns; about **3 ms** motion-to-photon. No app code, but also **no pose output to your software** | 5 min | One / One Pro / 1 Pro+ / 1S / R1 |
| **L2 — XREAL SDK app (Unity)** | Head pose (3 / 6DoF) in your code, world-anchored 3D content, phone controller, RGB frames (One + Eye), hands / planes / anchors (Air 2 Ultra only) | 0.5–1 day | Glasses + Beam Pro or Samsung S24 / S25 |
| **L3 — Android XR app** | Full spatial app: 6DoF, hands, planes, anchors, markers, Gemini, Play Store | 0.5–1 day (if you know Unity 6 / OpenXR) | AURA + its puck |

- **Rates:** pose and hand-tracking update rates are **not public** in the docs. Design for display rate (60–120 Hz) and measure on device.
- **Developer / EDU editions:** none. There is no paid licence tier; the SDK download is free. On Beam Pro you must enable **developer mode** (tap the glasses icon in MyGlasses 10 times with no glasses connected) to pick your own MR app.
- **"Low-level" access:** no official raw-IMU or raw-SLAM-camera API. Lowest official level is Unity `XRInputSubsystem` head pose, XR Hands joints and YUV camera textures.

## ROS 2 and middleware

- **Official ROS 2 support: none.** No package, no message definitions, no URDF.
- Working patterns for a hackathon:

| Pattern | How | When to use |
|---|---|---|
| **Display only** | Run RViz2 / Foxglove / a web UI on the robot PC or laptop, plug the glasses in | Operator HUD, fleet dashboard — default choice |
| **Unity ↔ ROS 2 bridge** | Unity [ROS-TCP-Connector](https://github.com/Unity-Technologies/ROS-TCP-Connector) in the app + ROS-TCP-Endpoint node on the robot PC | Publish head pose (`geometry_msgs/PoseStamped`) and hand joints; subscribe to images / status |
| **rosbridge WebSocket** | `rosbridge_server` on the robot, JSON from a small C# WebSocket client | Low-rate status, commands, no custom message generation |
| **Plain UDP pose stream** | Send head pose (7 floats) at display rate to a tiny Python node that republishes | Lowest latency head-tracked camera gimbal / teleop |
| **Video to the glasses** | WebRTC or MJPEG in a Unity texture, or just a browser window at L0 | Robot camera first-person view |

- The bridge repos above are Unity-maintained, not XREAL-specific; they were not re-checked today. Android host and robot must be on the same network — bring your own router or hotspot.
- Community XR-teleop stacks (OpenTeleVision-style, Quest / Vision Pro based) do **not** support XREAL out of the box.

## Simulation and digital twins

- **Robot simulation assets (URDF / MJCF / USD, Isaac Lab, MuJoCo, Gazebo): none** — not applicable.
- **App-side simulation:** Unity Editor **Simulator** (XR Device Simulator prefab) for XREAL SDK scenes; for AURA, Android Studio's Android XR emulator exists for Android XR in general — AURA-specific profile ⚠️ unverified.
- **Digital-twin idea that works:** import the partner robot's URDF into Unity (Unity URDF Importer), drive it from `/joint_states` over the bridge, and overlay it — world-anchored on Air 2 Ultra / AURA, head-locked or 6DoF-fixed on One + Eye.

## AI stack

| Item | Status |
|---|---|
| Pretrained robot policies / VLA / foundation models | **None** from XREAL |
| Datasets | **None** published |
| On-device assistant | **Gemini** built into AURA (Android XR). One series has no on-board AI compute |
| Teleoperation product | **None** official |
| LeRobot support | **None** official |
| Research precedent | "ActiveGlasses" (arXiv 2604.08534): smart glasses + stereo camera to record egocentric bare-hand demos, then the camera rides a 6-DoF perception arm. Per the profile, the paper used an Air 2 Ultra for head pose and added its own stereo camera. No code or dataset link on the arXiv page |

DIY data-collection pipeline that is realistic in 48 h:

1. One series + **XREAL Eye**: log **RGB frames (YUV_420_888)** + **6DoF head pose** from Unity, timestamped.
2. Stream or save (`Application.persistentDataPath`), convert offline to your dataset format (e.g. LeRobot format — your own converter).
3. Hands are **not** tracked on One + Eye: run an off-board hand-pose model on the RGB stream, or use Air 2 Ultra / AURA for native hand joints (26 joints per the profile's read of the hand-tracking docs).

## Compute, sensors and connectivity

| Device | Compute | Sensors exposed to developers | Connection |
|---|---|---|---|
| One / One Pro / 1S (and 1 Pro+ ⚠️) | X1 co-processor only (display + 3DoF). **No app compute** | IMU-based 3DoF pose; with **Eye**: RGB camera + 6DoF | USB-C to host |
| XREAL Eye | — | RGB camera (resolution / fps not stated in docs) | Clips into One-series glasses |
| Air 2 Ultra | None on glasses | Dual grayscale SLAM cameras (used internally), IMU; **no RGB** | USB-C to host |
| Beam Pro | Android handheld; official SDK host | Dual cameras for spatial capture | USB-C to glasses, Wi-Fi |
| Samsung Galaxy S24 (Android 14) / S25 (Android 15) | Official SDK hosts (only Samsung flagships tested) | — | USB-C to glasses, Wi-Fi |
| AURA puck | Snapdragon Reality Elite (up to 48 TOPS) + X1S; 4,455 mAh | 6DoF cameras, AI camera, 4 mics; hand tracking | Tethered to glasses; dual USB-C; wired PC mirroring |

- **Laptop → glasses (L0):** one USB-C cable, laptop port must support DisplayPort Alt Mode. Glasses draw power from the host. XREAL Neo (10,000 mAh hub with DP pass-through) helps with battery-limited hosts.
- **Laptop → host for development:** `adb tcpip 5555` then `adb connect <host-ip>` (wireless ADB), because the host's USB-C port goes to the glasses.
- **Network defaults:** none (no fixed IPs or ports like a robot). First-person streaming auto-discovers the Windows receiver on the LAN.
- **Firmware:** update via MyGlasses 1.11.0 (Beam Pro) or the web OTA tool at https://www.xreal.com/ota/ from a PC.

## First 60 minutes checklist

**Path A — display HUD (any glasses, 10 minutes)**

1. Plug glasses into the laptop or robot PC USB-C port; confirm an external display appears.
2. On X1 glasses, use the on-glasses menu to anchor the screen in space; set brightness / dimming for the room.
3. Put your UI full-screen: RViz2, Foxglove, a web dashboard or the robot camera feed. Use large fonts and high contrast (optical see-through washes out dark colours — black is transparent).
4. Walk the demo path once with the cable to check comfort and snag points. Done.

**Path B — XREAL SDK HelloMR + pose to ROS 2 (One + Eye or Air 2 Ultra)**

1. Ask the booth: which glasses, which host, firmware current, Android version (must be **below 16**), is a sample project provided.
2. Install Unity **2022.3 LTS or 6000.0 LTS** with Android Build Support; Android SDK **API 31+**.
3. New 3D project → switch platform to Android → install **XR Interaction Toolkit** (2.5.x or 3.0.x) + Starter Assets; AR Foundation and XR Hands only if you use Air 2 Ultra features.
4. Package Manager → *Add package from tarball* → `com.xreal.xr.tar.gz`. Enable **XREAL** under XR Plug-in Management (Android tab) → Project Validation → **Fix All** (OpenGL ES3, IL2CPP, ARM64, min API Android 10).
5. XREAL settings: Initial Tracking Type = **6DoF** (or 3DoF), Input Source = Controller (Hands only on Air 2 Ultra), Support Devices = REALITY (6DoF glasses) and / or VISION (3DoF glasses).
6. Open the **HelloMR** scene (Interaction Basics sample) → Build → `adb install` → unplug from PC → plug glasses into host → launch from **ControlGlasses** (phone) or **MyGlasses** (Beam Pro) → grant "display over other apps".
7. Verify: content stays fixed when you turn (3DoF) and when you step sideways (6DoF). Recenter via `XREALUtility.GetInputSubsystem()?.TryRecenter()`.
8. Read sensors: log the main camera transform each frame (head pose). On One + Eye open the **RGBCameraAndCapture** sample to see camera frames.
9. Add a UDP or ROS-TCP sender for the head pose; echo it on the robot PC (`ros2 topic echo`). That is your hello-world integration.

**Path C — AURA (Android XR)**

1. Unity **6.5** → Android XR Build Profile → packages: OpenXR Plugin 1.15+, Unity OpenXR: Android XR, XR Interaction Toolkit 3.5, XR Hands 1.6+, AR Foundation 6.2+.
2. Start from a Unity XR / Mixed Reality template; graphics API **Vulkan**, URP.
3. Request `android.permission.HAND_TRACKING` for XR Hands; design for hands + puck trackpad, no eye tracking.
4. Build and deploy to the puck over ADB; verify hand joints and a plane, then add your network bridge as in Path B.

## Known gotchas and safety

| Gotcha | What to do |
|---|---|
| **Android 16 breaks the XREAL SDK** (official warning, still on every docs page) | Do not accept OS updates on dev phones during the event |
| One + Eye has **6DoF only** — no hands, planes, anchors, image tracking | Use phone controller or head-gaze for input; use markers on the robot side instead |
| Air 2 Ultra has **no RGB camera** access | Mount a separate camera if you need egocentric video |
| 6DoF on One + Eye requires latest firmware + SDK 3.1.0 + matching ControlGlasses / MyGlasses | Update before you start coding |
| Only **Beam Pro and Samsung S24 / S25-class** hosts are supported | Do not plan on your own Pixel / Xiaomi |
| Samsung **DeX** hijacks the display | Disable DeX on the phone |
| XREAL SDK wants **OpenGL ES3**; Android XR wants **Vulkan** | One Unity project per stack; do not try to share a build |
| Overlay content or URP without single-pass | Disable Multithreaded Rendering (per docs) |
| "Not supported on this device" in MyGlasses | Add the `com.nreal.supportDevices` meta-data to `AndroidManifest.xml` (see FAQ) |
| First-person streaming | Windows receiver only; same LAN; **receiver firewall off**; fails on crowded Wi-Fi → use a hotspot |
| Camera / UVC permission on newer Android | Request CAMERA at runtime **before** USB permission |
| Glasses power comes from the host | Bring a power bank or Neo; plan charging between demo runs |
| Docs lag hardware (1 Pro+, AURA not in docs.xreal.com) | Confirm with XREAL staff on site |

Safety (XREAL has no e-stop, modes or torque limits — the risks are human-factors):

- **Never make the glasses the only safety channel.** Teleoperating another vendor's robot through a Wi-Fi pose stream needs a second person holding the robot's own e-stop, plus a dead-man switch and a pose-timeout (stop if no packet for about 200 ms).
- Electrochromic dimming and bright virtual screens **reduce situational awareness** — keep lenses clear when walking near robots; operators should stand or sit still.
- The tether is a **trip and snag hazard**, especially for elderly users (T04). Route the cable behind the ear and down the back; keep sessions short and seated.
- Camera recording of patients or bystanders (Eye, AURA) needs consent — relevant for clinic scenarios in Leukerbad.

## Community resources

- Official docs: https://docs.xreal.com/ (SDK 3.1.0; switch to 2.4.1 for legacy NRSDK)
- Downloads and API reference: https://developer.xreal.com/download · https://developer.xreal.com/reference/nrsdk/overview
- Sample list (HelloMR, PlaneDetection, Anchors, RGBCameraAndCapture, FirstPersonViewStreamingCast, MarkerTracking): https://docs.xreal.com/Sample%20Code
- GitHub (legacy samples): https://github.com/nreal-ai
- AURA: Android XR docs https://developer.android.com/develop/xr and the Unity Discussions thread "XREAL AURA support now available in Unity 6.5" (Android XR tag)
- Official developer forum / Discord: exists per XREAL's site, exact current URL not verified today — ask the booth
- Best resource this weekend: the XREAL staff on site

## Sources

- [XREAL SDK docs — overview (3.1.0)](https://docs.xreal.com/)
- [XREAL docs — Getting Started with XREAL SDK](https://docs.xreal.com/Getting%20Started%20with%20XREAL%20SDK)
- [XREAL docs — SDK 3.1.0 release note](https://docs.xreal.com/Release%20Note/XREAL%20SDK%203.1.0)
- [XREAL docs — Compatibility](https://docs.xreal.com/XREALDevices/Compatibility)
- [XREAL docs — XREAL Glasses](https://docs.xreal.com/XREALDevices/XREAL%20Glasses)
- [XREAL docs — Access RGB Camera](https://docs.xreal.com/Camera/Access%20RGB%20Camera)
- [XREAL docs — Camera](https://docs.xreal.com/Camera/Camera)
- [XREAL docs — First Person View](https://docs.xreal.com/Tools/First%20Person%20View)
- [XREAL docs — Tools](https://docs.xreal.com/category/tools)
- [XREAL docs — CloudXR / XR Streaming](https://docs.xreal.com/Tools/XR%20Streaming)
- [XREAL docs — Sample Code](https://docs.xreal.com/Sample%20Code)
- [XREAL docs — Hand Tracking](https://docs.xreal.com/Input%20and%20Interactions/Hand%20Tracking)
- [XREAL docs — Frequently Asked Questions](https://docs.xreal.com/Frequently%20Asked%20Questions)
- [GitHub — nreal-ai organisation](https://github.com/nreal-ai)
- [Android Developers — Develop with Unity for Android XR](https://developer.android.com/develop/xr/unity)
- [Unity blog — Unity support for XREAL AURA (16 Jun 2026)](https://unity.com/blog/unity-android-xr-wired-glasses-support)
- [Road to VR — XREAL AURA launch and specs (28 Oct 2026)](https://www.roadtovr.com/google-ar-glasses-xreal-aura-release-date-price/)
- [arXiv 2604.08534 — ActiveGlasses](https://arxiv.org/abs/2604.08534)
- [XREAL profile in this vault](XREAL.md)
