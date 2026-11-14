#!/usr/bin/env python3
"""Checks that the teleop setup is complete, without a headset or robot.

  uv run tools/check_setup.py

Each check prints OK / WARN / FAIL. Only FAIL blocks the simulator; WARN items
are needed only for a specific mode (headset, recording, real arm).
"""
import importlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

results = []


def check(name, fn, required=True):
    try:
        detail = fn() or ""
        status = "OK"
    except Exception as e:  # report and keep going
        detail = f"{type(e).__name__}: {e}"
        status = "FAIL" if required else "WARN"
    results.append(status)
    print(f"[{status:4}] {name}{' - ' + detail if detail else ''}")


def robot_model():
    from teleop.rebot_model import RebotSim
    sim = RebotSim()
    return f"{sim.model.nu} actuators, cameras: " + ", ".join(
        sim.model.camera(i).name for i in range(sim.model.ncam))


def ik():
    import numpy as np
    from teleop.ik import DiffIK
    from teleop.rebot_model import ARM_JOINTS, HOME_QPOS, TCP_SITE, RebotSim
    sim = RebotSim()
    solver = DiffIK(sim.model, TCP_SITE, ARM_JOINTS, HOME_QPOS)
    pos, rot = solver.fk(HOME_QPOS)
    q = HOME_QPOS.copy()
    for _ in range(300):
        q, err, _ = solver.solve(q, pos + np.array([0.05, 0.1, -0.1]), rot, 0.01)
    if err > 0.005:
        raise RuntimeError(f"IK error {err * 1000:.1f} mm")
    return f"reaches a test target within {err * 1000:.2f} mm"


def headless_demo():
    out = subprocess.run(
        [sys.executable, "-W", "ignore", str(ROOT / "sim_teleop.py"),
         "--input", "demo", "--headless", "--duration", "2"],
        capture_output=True, text=True, timeout=60, cwd=ROOT)
    if out.returncode != 0 or "ENGAGED" not in out.stdout:
        raise RuntimeError((out.stderr or out.stdout).strip().splitlines()[-1])
    return "2 s of scripted teleop ran"


def module(name):
    return lambda: getattr(importlib.import_module(name), "__version__", "") or "importable"


def apk():
    apk = ROOT / "third_party/oculus_reader/oculus_reader/APK/teleop-debug.apk"
    if not apk.exists() or apk.stat().st_size < 1_000_000:
        raise FileNotFoundError("APK missing or Git LFS pointer; run ./scripts/setup_assets.sh")
    return f"{apk.stat().st_size / 1e6:.1f} MB"


def adb():
    path = shutil.which("adb")
    if not path:
        raise FileNotFoundError("adb not found: sudo apt install android-tools-adb")
    out = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=10).stdout
    devices = [line for line in out.splitlines()[1:] if line.strip()]
    return f"{len(devices)} device(s): {'; '.join(devices) or 'none connected'}"


def calibration():
    from teleop.quest_input import calibration_file
    found = [s for s in ("webxr", "oculus") if calibration_file(s).exists()]
    if not found:
        raise FileNotFoundError("not calibrated yet (uses the default guess): "
                                "uv run tools/calibrate_quest_axes.py")
    return "calibrated: " + ", ".join(found)


def follower_calibration():
    path = ROOT.parent / "follower.json"
    if not path.exists():
        raise FileNotFoundError(f"{path} missing")
    return str(path.relative_to(ROOT.parent))


print("== simulator (required) ==")
check("reBot model assets", lambda: str((ROOT / "assets/reBot-DevArm").relative_to(ROOT))
      if (ROOT / "assets/reBot-DevArm").exists()
      else (_ for _ in ()).throw(FileNotFoundError("run ./scripts/setup_assets.sh")))
check("mujoco", module("mujoco"))
check("model builds", robot_model)
check("IK", ik)
check("headless demo run", headless_demo)

print("== Quest input ==")
check("WebXR relay (vr-teleop-kit)", module("vr_teleop_kit.relay.server"), required=False)
check("OculusReader package", module("oculus_reader.reader"), required=False)
check("OculusReader APK", apk, required=False)
check("adb", adb, required=False)
check("Quest axis calibration", calibration, required=False)

print("== recording / real arm (uv sync --extra lerobot) ==")
check("lerobot datasets", module("lerobot.datasets.lerobot_dataset"), required=False)
check("lerobot reBot driver (motorbridge)", module("motorbridge"), required=False)
check("follower.json calibration", follower_calibration, required=False)

n_fail, n_warn = results.count("FAIL"), results.count("WARN")
print(f"\n{len(results) - n_fail - n_warn} OK, {n_warn} WARN, {n_fail} FAIL")
sys.exit(1 if n_fail else 0)
