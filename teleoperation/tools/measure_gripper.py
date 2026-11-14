#!/usr/bin/env python3
"""Measure the gripper's physical open/closed positions by hand (torque OFF).

  python tools/measure_gripper.py --port /dev/tty.usbmodem00000000050C1

Only the gripper motor is touched and it is disabled, so you can move the
fingers by hand. Open it fully (just until it stops, do not force), press Enter,
close it fully, press Enter. The result goes to config/gripper_limits.json.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import math

from motorbridge import Controller

from teleop import gripper_limits

p = argparse.ArgumentParser()
p.add_argument("--port", required=True)
args = p.parse_args()

bus = Controller.from_dm_serial(serial_port=args.port, baud=921600)
motor = bus.add_damiao_motor(7, 7 + 0x10, "4310")
motor.disable()


def read_deg() -> float | None:
    """Latest gripper position, or None if the motor did not answer."""
    for attempt in range(5):
        motor.request_feedback()
        bus.poll_feedback_once()
        st = motor.get_state()
        if st is not None:
            return math.degrees(st.pos)
        if attempt == 2:
            motor.disable()  # a disable command is answered with a state frame
        time.sleep(0.02)
    return None


def fmt(v) -> str:
    return "no feedback" if v is None else f"{v:8.1f} deg"


def capture(label: str) -> float:
    print(f"\nMove the gripper to FULLY {label} by hand (gently, to the stop), then press Enter.")
    import select
    while True:
        print(f"\r  position: {fmt(read_deg()):>16}", end="", flush=True)
        if select.select([sys.stdin], [], [], 0.1)[0]:
            sys.stdin.readline()
            break
    val = read_deg()
    if val is None:
        raise SystemExit("\nNo feedback from the gripper motor (id 7). Check power and the USB cable.")
    print(f"\n  {label}: {val:.1f} deg")
    return val

try:
    open_deg = capture("OPEN")
    closed_deg = capture("CLOSED")
finally:
    motor.close()
    bus.close()

print(f"\nrange = {abs(open_deg - closed_deg):.1f} deg  (open {open_deg:.1f}, closed {closed_deg:.1f})")
if abs(open_deg - closed_deg) < 20:
    raise SystemExit("range too small, not saving; repeat the measurement")
gripper_limits.save(open_deg, closed_deg)
print(f"saved to {gripper_limits.LIMITS_FILE}")
