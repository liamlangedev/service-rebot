"""Find the grasp in each rebot_sort_v1 episode and cut a clip around it.

The gripper channel (index 6, lerobot degrees) is about -365 when open and -5 when closed.
The grasp is the first close that stays closed for `min_closed` frames. Episodes with
more than one close event (regrasps, fumbles) are rejected unless `allow_regrasp`.

Pure numpy/pandas, so it runs on the raw parquet files without decoding any video.
"""

from __future__ import annotations

import glob
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

GRIPPER = 6
CLOSED_ABOVE = -100.0  # gripper action above this (towards -5) counts as closed
MIN_CLOSED = 15        # frames (0.5 s) the close must last


@dataclass
class Grasp:
    episode: int
    length: int
    t_close: int      # first frame of the sustained close command
    n_closes: int     # number of open->closed transitions in the episode
    t_release: int    # first frame after t_close where the command opens again
    n_closes_before: int = 0  # brief closes (fumbles) before the sustained one

    @property
    def clean(self) -> bool:
        return self.n_closes == 1


def load_frames(root: str | Path) -> pd.DataFrame:
    files = sorted(glob.glob(f"{root}/data/*/*.parquet"))
    if not files:
        raise FileNotFoundError(f"no parquet files under {root}/data")
    return pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)


def episode_arrays(df: pd.DataFrame) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    """episode -> (state [T,7], action [T,7]) in lerobot degrees."""
    out = {}
    for ep, g in df.sort_values("index").groupby("episode_index"):
        out[int(ep)] = (np.stack(g["observation.state"].to_numpy()),
                        np.stack(g["action"].to_numpy()))
    return out


def find_grasp(episode: int, action: np.ndarray) -> Grasp | None:
    closed = action[:, GRIPPER] > CLOSED_ABOVE
    t_close = next((t for t in range(len(closed) - MIN_CLOSED)
                    if closed[t:t + MIN_CLOSED].all()), None)
    if t_close is None:
        return None
    rises = np.flatnonzero(np.diff(closed.astype(int)) == 1) + 1
    if closed[0]:
        rises = np.r_[0, rises]
    t_release = next((t for t in range(t_close, len(closed)) if not closed[t]), len(closed))
    return Grasp(episode, len(closed), t_close, len(rises), t_release,
                 n_closes_before=int(np.sum(rises < t_close)))


def clip_windows(g: Grasp, pre_frames: list[int], post_frames: int) -> list[tuple[int, int]]:
    """[start, end) windows ending `post_frames` after the close, one per pre offset.

    Several start offsets per grasp act as handoff-timing augmentation: the policy sees
    the arm handed over at slightly different heights above the object.
    """
    end = min(g.t_close + post_frames, g.t_release, g.length)
    return [(max(g.t_close - pre, 0), end) for pre in pre_frames]
