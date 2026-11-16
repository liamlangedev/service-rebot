"""Flag suspicious episodes in local LeRobot v3 datasets from their joint data alone (no video).

python tools/check_dataset.py rebot_sort_bottle rebot_sort_towel_clean ...   # names under RoboCrafty/

Per episode: length, idle head/tail seconds, fraction of idle frames, largest per-frame joint step, gripper
open/close transitions, mean |action - state|, NaNs, timestamp gaps. Episodes are flagged when they are outliers
within their own dataset (robust z-score > 3) or break a hard rule.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.home() / ".cache/huggingface/lerobot/RoboCrafty"
FPS = 30
IDLE = 0.05  # summed |delta action| of the arm joints per frame (deg) below this counts as not moving


def load(name):
    r = ROOT / name
    data = pd.concat(pd.read_parquet(f) for f in sorted((r / "data").glob("*/*.parquet")))
    return data


def episode_stats(g):
    a, s = np.stack(g["action"]), np.stack(g["observation.state"])
    d = np.abs(np.diff(a[:, :6], axis=0)).sum(1)
    moving = np.where(d > IDLE)[0]
    head = moving[0] / FPS if len(moving) else len(g) / FPS
    tail = (len(d) - 1 - moving[-1]) / FPS if len(moving) else 0.0
    grip = a[:, 6]
    mid = (grip.min() + grip.max()) / 2
    closed = grip < mid
    return dict(
        sec=len(g) / FPS, head=head, tail=tail, idle=(d <= IDLE).mean(),
        maxstep=np.abs(np.diff(a[:, :6], axis=0)).max(),
        grip_tr=int((closed[1:] != closed[:-1]).sum()), grip_span=grip.max() - grip.min(),
        lag=np.abs(a[:, :6] - s[:, :6]).mean(),
        nan=int(np.isnan(a).sum() + np.isnan(s).sum()),
        ts_gap=float(np.abs(np.diff(g["timestamp"]) - 1 / FPS).max()),
    )


def robust_z(x):
    med = np.median(x)
    mad = np.median(np.abs(x - med)) * 1.4826 or 1e-9
    return (x - med) / mad


def main():
    pd.set_option("display.width", 200)
    for name in sys.argv[1:]:
        df = load(name)
        rows = {ep: episode_stats(g) for ep, g in df.groupby("episode_index")}
        t = pd.DataFrame(rows).T
        flags = {ep: [] for ep in t.index}
        for col in ("sec", "idle", "maxstep", "lag", "grip_tr", "head", "tail"):
            z = robust_z(t[col].to_numpy(float))
            for ep, v in zip(t.index, z):
                if abs(v) > 3 and (col != "sec" or True):
                    flags[ep].append(f"{col} {'high' if v > 0 else 'low'}")
        for ep, r in t.iterrows():
            if r.nan:
                flags[ep].append("NaN")
            if r.ts_gap > 0.01:
                flags[ep].append("timestamp gap")
            if r.grip_span < 0.5 * np.median(t.grip_span):
                flags[ep].append("gripper barely moves")
            if r.sec < 5:
                flags[ep].append("very short")
        print(f"\n=== {name}: {len(t)} episodes, {t.sec.sum() / 60:.1f} min, median {t.sec.median():.0f}s ===")
        print(t.describe().loc[["min", "50%", "max"]].round(2).to_string())
        bad = {ep: f for ep, f in flags.items() if f}
        print("flagged:" if bad else "no flagged episodes")
        for ep, f in bad.items():
            print(f"  ep {ep}: {', '.join(f)}  ({t.loc[ep, 'sec']:.0f}s)")


if __name__ == "__main__":
    main()
