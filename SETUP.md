# Setup (macOS, Ubuntu/Debian, Fedora, Windows)

Gets a fresh machine to the point where `teleoperation/record_episodes.py` runs. Usage is in
[teleoperation/REAL_ARM.md](teleoperation/REAL_ARM.md).

Tested only on macOS (Apple Silicon, Python 3.12). The Linux and Windows steps follow the vendors' documentation and were
**not tested**; where a package name or URL may have changed, the step says so.

## 0. Windows: native or WSL?

**Use native Windows, not WSL.** The setup needs four things that WSL2 handles badly:
- the Ultraleap tracking service and the Leap USB device (WSL2 needs `usbipd-win` USB passthrough plus a Linux service; fragile)
- the arm's serial port and three USB cameras (same passthrough, and cameras need a custom WSL kernel)
- global key capture (S/G/H, arrow keys, space clutch): pynput in WSL only sees keys inside WSL windows, not your Windows desktop
- the MuJoCo viewer (needs WSLg)

Everything the project needs has a native Windows build: Ultraleap Gemini (official Windows installer), `motorbridge` (a
`win_amd64` wheel exists on PyPI), PyTorch, lerobot, MuJoCo, OpenCV, pynput. Use WSL only if you do not need the Leap or the
real arm, for example to train policies on a Linux GPU; for that, follow the Ubuntu steps inside WSL.

## 1. System packages

**macOS**
```bash
xcode-select --install                   # C compiler for the Leap bindings
brew install uv ffmpeg git
```

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install -y git curl build-essential python3-dev ffmpeg libgl1 libglib2.0-0 libusb-1.0-0 v4l-utils
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Fedora**
```bash
sudo dnf install -y git curl gcc gcc-c++ make python3-devel ffmpeg-free mesa-libGL libusb1 v4l-utils
curl -LsSf https://astral.sh/uv/install.sh | sh
```
(`ffmpeg` on Fedora needs RPM Fusion for the full build; `ffmpeg-free` is enough for most things. PyAV, used by lerobot for
video, ships its own FFmpeg libraries.)

**Windows** (PowerShell, Windows 10/11 64-bit)
```powershell
winget install --id Git.Git -e
winget install --id astral-sh.uv -e
winget install --id Gyan.FFmpeg -e
winget install --id Microsoft.VisualStudio.2022.BuildTools -e   # then add the "Desktop development with C++" workload
```
The C++ build tools are only needed to build the Leap bindings (step 4b). Open a new terminal afterwards so PATH updates.

## 2. Clone and create the environment

```bash
git clone git@github.com:niru-5/steel_team.git && cd steel_team
git checkout dev/roboCrafy
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```
`lerobot[rebot]` pulls in PyTorch, the Damiao `motorbridge` driver and OpenCV. Check:
```bash
python -c "import lerobot, motorbridge, mujoco, scipy, pynput; print('ok')"
```
**Windows (PowerShell):** `uv venv --python 3.12 .venv`, then `.venv\Scripts\Activate.ps1` (if scripts are blocked:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`), then `uv pip install -r requirements.txt`. Multi-line commands in the
repo docs end lines with a backslash; in PowerShell put the command on one line or end lines with a backtick instead.

If you prefer plain pip, `python -m venv .venv && pip install -r requirements.txt` works the same.

## 3. Robot model and arm access

```bash
cd teleoperation
./scripts/setup_assets.sh          # downloads Seeed's MJCF into assets/ (git-ignored)
```
On Windows run `setup_assets.sh` in **Git Bash** (installed with Git), or run the two `git clone` commands from the script by hand.

Serial port of the arm:
- **Windows:** `COM3` or similar: Device Manager > Ports (COM & LPT). Pass it as `--port COM3`.
- **macOS:** `/dev/tty.usbmodem...` (`ls /dev/tty.usbmodem*`)
- **Linux:** `/dev/ttyACM0`. Add yourself to the serial group, then log out and in:
  `sudo usermod -aG dialout $USER` (Ubuntu/Debian) or `sudo usermod -aG dialout,lock $USER` (Fedora).

## 4. Leap Motion Controller

The Leap needs the Ultraleap tracking service (Gemini) plus the Python bindings built against its SDK.

### 4a. Tracking service
- **macOS:** install the Ultraleap Hand Tracking app from <https://leap.ultraleap.com/downloads/> (Gemini, v5.x).
  It lands in `/Applications/Ultraleap Hand Tracking.app`. Open the Visualizer: your hands should show at about 100+ fps.
- **Ubuntu 20.04/22.04:** Ultraleap publishes an apt repository and the `ultraleap-hand-tracking` package. Follow the Linux
  section on the same download page (the repo URL and key change over time, so copy the current commands from there), then
  `sudo systemctl status leapd` should say active. `ultraleap-hand-tracking-control-panel` is the visualizer.
- **Fedora:** there is no official RPM. Options: run an Ubuntu/Debian container or VM with USB passthrough, or convert the
  `.deb` with `alien` (untested). If you can, use Ubuntu for the machine that runs the Leap.
- **Windows:** install the Ultraleap Gemini (Hand Tracking) installer from the same download page, then check the Visualizer
  shows your hands at about 100+ fps. The SDK lands in `C:\Program Files\Ultraleap\LeapSDK`.
- The original Leap Motion Controller is supported by Gemini. Plug it into a USB port directly, not through a hub.

### 4b. Python bindings
They are not on PyPI. With the venv from step 2 active:
```bash
cd ~/git        # anywhere outside this repo
git clone https://github.com/ultraleap/leapc-python-bindings
cd leapc-python-bindings
uv pip install -r requirements.txt build
python -m build leapc-cffi
uv pip install leapc-cffi/dist/leapc_cffi-0.0.1.tar.gz
uv pip install -e leapc-python-api
```
On Windows (PowerShell) the commands are the same. The build needs the C++ build tools from step 1; Ultraleap ships prebuilt
modules only for old Python versions, so expect to build.

Where the SDK is expected (set `LEAPSDK_INSTALL_LOCATION` if yours is elsewhere):
- macOS: `/Applications/Ultraleap Hand Tracking.app/Contents/LeapSDK`
- Windows: `C:/Program Files/Ultraleap/LeapSDK`
- Linux x64: `/usr/lib/ultraleap-hand-tracking-service`
- Linux ARM: `/opt/ultraleap/LeapSDK`

**Known problem (seen on macOS):** `import leap` fails with `Library not loaded: @rpath/libLeapC.6.dylib`.
Copy the library next to the compiled module:
```bash
cp "/Applications/Ultraleap Hand Tracking.app/Contents/LeapSDK/lib/libLeapC.6.dylib" \
   "$(python -c 'import leapc_cffi,os;print(os.path.dirname(leapc_cffi.__file__))')/"
```
On Windows the equivalent is `LeapC.dll`: copy it from the SDK's `lib\x64` folder next to the `_leapc_cffi*.pyd` file, or add that
folder to `PATH`. On Linux it is `libLeapC.so`: put its directory on `LD_LIBRARY_PATH`, or copy it next to `_leapc_cffi`.
The exact library path inside the SDK may differ by version: use `find` to locate it.

Test (hand over the sensor):
```bash
python -c "import leap; print('leap ok')"
python /path/to/leapc-python-bindings/examples/tracking_event_example.py
```

## 5. Permissions

- **macOS:** System Settings > Privacy & Security: give your terminal **Accessibility** and **Input Monitoring**
  (pynput: space clutch, S/G/H and arrow keys) and **Camera**.
- **Windows:** Settings > Privacy & security > Camera: allow desktop apps. pynput needs no extra permission, but it cannot see
  keys typed into an elevated (administrator) window unless your terminal is elevated too: run both the same way.
- **Linux:** pynput needs an **X11 session** (log in with "Ubuntu on Xorg" or "GNOME on Xorg"); it does not work under Wayland.
  Cameras: add yourself to the `video` group (`sudo usermod -aG video $USER`).

## 6. First-run checklist

Run from `teleoperation/` with the venv active. Details and options are in `REAL_ARM.md`.
```bash
python sim_teleop.py --input leap                           # hand axes in simulation, nothing moves
lerobot-find-cameras opencv                                 # then edit config/cameras.json
python tools/probe_cameras.py                               # modes and fps per camera
python tools/measure_gripper.py --port <PORT>               # gripper range -> config/gripper_limits.json
python go_ready.py --port <PORT>                            # arm to the ready pose
python record_episodes.py --port <PORT> --repo-id <user>/<name> --task "<task>"
hf auth login                                               # once, before push_dataset.py
```
If someone re-calibrated the arm (`lerobot-calibrate`), re-run `measure_gripper.py`.

## 7. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `import leap` fails, `Library not loaded` / `libLeapC` | copy or point to the library, step 4b |
| `ModuleNotFoundError: leapc_cffi._leapc_cffi` | the compiled module was not built; redo `python -m build leapc-cffi` |
| Hands not detected, visualizer empty | tracking service not running, or the sensor is on a hub |
| Space / S / G / H do nothing | missing Accessibility permission (macOS) or Wayland (Linux) |
| `Permission denied: /dev/ttyACM0` | not in the `dialout` group yet (log out and in) |
| Camera `Timed out waiting for frame` | another process holds the camera, or USB bandwidth; use separate ports |
| `ensure_mode failed: register 10 write ack not received` | motor not answering: power-cycle the arm, check the port is free (`lsof <PORT>`) |
| `could not open port COMx` (Windows) | wrong COM number, or another program (e.g. a serial monitor) holds the port |
| Cameras black or slow on Windows | close the Camera app; use separate USB ports; indices change on replug |
| Missing `assets/reBot-DevArm` | run `scripts/setup_assets.sh` |
