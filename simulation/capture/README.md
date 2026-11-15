# Capture: real cameras + arm → calibrated sim and a splat dataset

Tools for a session on the real setup:

- **Device UI:** which USB camera is which, which port is the arm, and lens calibration.
- **Capture session:** the arm holds poses while all cameras are captured. It compares
  every frame with the sim, calibrates the cameras from a ChArUco board, and pauses for
  your phone video.
- **Splat dataset:** packs the session for Gaussian-splat training on Hugging Face Jobs.

Run everything from `simulation/` with the teleop environment:
`uv run --project ../teleoperation python -m capture.<tool>`. Add `--fake` to any tool to
try it without hardware (simulated arm and cameras).

## Is a checkerboard needed?

No, but it helps a lot. Without it, the camera poses come from hand-picked landmarks
(`tools/calibrate_cameras.py`, about 10–25 px). With a printed **ChArUco** board:

- the lens calibration (focal length + distortion) of every camera, including the
  100° lenses;
- the fixed cameras' poses to a few mm, solved automatically in every session;
- the wrist camera's mount on the gripper (hand-eye), from several arm poses;
- a joint check: if the wrist-camera results disagree between poses, the sim's joint
  zeros or link lengths are off;
- a metric anchor in the phone capture, for aligning the splat to the sim later.

Make it: `python -m rebot_sim.charuco board.pdf`. Print at 100 % ("actual size") on A4,
then check that a square measures 35 mm; if not, put the measured size in
`real_setup.json` → `charuco.square`. Glue it to cardboard so it stays flat.

## 1. Device setup (once per machine, or when cameras change)

```bash
python -m capture.device_ui          # then open http://localhost:8770
```

- Each camera shows a live preview. Cover a lens with your hand to see which preview it
  is, and set its role: `cam_corner` (C920 on the gooseneck), `cam_far` (on the far
  edge), `wrist` (on the gripper).
- Pick the arm's serial port and press **Save**. This writes `capture/devices.json`,
  keyed by stable USB ids, so replugging is fine.
- **Lens calibration** (with the board, per camera, about 1 minute each): press
  *Collect*, then slowly move the board in front of that camera. Tilt it, bring it near
  and far, and cover all corners of the image. Once about 20 views are kept, press
  *Solve*. The result goes to `rebot_sim/calibration/<role>.json`; under 0.5 px rms is
  good.

## 2. Capture session (about 6 minutes)

1. Lay the board flat on the table in front of the robot, edges parallel to the walls,
   caption edge towards the robot. Measure where the pattern's corner nearest the left
   and near walls is, and set `charuco.near_left` (metres from the left wall, from the
   near wall) and `charuco.enabled: true` in `rebot_sim/real_setup.json`. The default
   spot `[0.48, 0.175]` centres it under the wrist camera at the ready pose.
2. Run:
   ```bash
   python -m capture.capture_session --name s1 --write
   ```
   - The arm moves to the ready pose (it asks first) and holds it, with commands
     streamed so the motors stay stiff.
   - It captures every camera at 1920×1080 together with the measured joint angles.
   - **Pause, 3 minutes** (`--pause` changes it; Enter ends it early): take the phone
     video for the splat. The guide is printed on screen: remove the can and cup, lock
     exposure and focus, and do 3 slow loops (high, mid, table level) plus close-ups
     under the gripper and inside the bins. Don't touch the cameras or the board.
   - It captures again to check nothing moved, then visits `pan_left`, `pan_right`,
     `reach` and `roll`, capturing at each.
   - It solves the camera poses from the board and the wrist mount from board + arm
     kinematics, and prints how they compare with the current sim. `--write` puts them
     into `real_setup.json`; the previous file is kept in the session folder.
3. Look at `captures/s1/compare/*.jpg`: real | sim | real with the sim robot's outline.
   If the outline doesn't sit on the real arm in some pose, that joint's mapping or zero
   is off.

Needs the same files as real teleop: `follower.json` (repo root) and
`teleoperation/config/gripper_limits.json`. `--no-arm` captures cameras only.

## 3. Gaussian-splat dataset and training on Hugging Face

```bash
hf auth login                                           # once, token with write access
python -m capture.prepare_splat_dataset s1 --media ~/phone/VID_*.mp4 --repo-id <user>/rebot_scene_s1
```

This copies your phone files into `captures/s1/phone/` and uploads the session as a
private dataset. The dataset includes `hf_jobs/train_splat.sh`. Then it prints the
training command:

```bash
hf jobs run --flavor a10g-large --timeout 3h --secrets HF_TOKEN \
  -e OUTPUT_REPO=<user>/rebot_scene_s1_splat \
  -v hf://datasets/<user>/rebot_scene_s1:/data \
  ghcr.io/nerfstudio-project/nerfstudio:latest bash /data/train_splat.sh
```

The job extracts video frames (`FRAMES` per video, default 200, each the sharpest of
`PICK`=3 neighbours, which drops motion-blurred frames), runs COLMAP, trains nerfstudio `splatfacto`, and
uploads `splat.ply`, `transforms.json` and the COLMAP model to a private model repo.
Follow it with `hf jobs ps` and `hf jobs logs <id>`. Aligning the splat to the sim and
rendering it behind the MuJoCo robot is the next step; the board in the phone frames
gives the scale and position for that.

### Without a capture session: scene or object videos

Plain phone videos work too (`--standalone`). For a video circling **one object on a
table**, give its measured size; it goes into `object.json`:

```bash
python -m capture.prepare_splat_dataset splat_towel --standalone \
  --media real_setup_photos/videos/VID_20261115_154922434.mp4 \
  --object towel --pose lying --length 0.26 --diameter 0.04 \
  --repo-id <user>/rebot_splat_towel        # --pose upright: length is the height
```

Train it with the printed command (add `-e FRAMES=300` for long videos). Then cut the
object out of the table and scale it to metres:

```bash
hf download <user>/rebot_splat_towel_splat --local-dir splats/towel
python tools/crop_object_splat.py splats/towel/splat.ply \
  --object splats/towel/object.json --out splats/towel_object.ply
```

It levels the table, finds the object, and scales the splat so that the object's length
matches `object.json`. The output's origin is on the table under the object, with z up
(x along the length if lying). It also writes `.json` (scale, measured diameter as a
cross-check, transform) and `.png` (top and side views on a 1 cm grid). The phone videos
in `real_setup_photos/videos/` are gitignored; their datasets are on the Hub.
