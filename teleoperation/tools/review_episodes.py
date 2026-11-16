"""Render a local LeRobot v3 dataset as ONE review mp4: all episodes back to back, cameras side by side.

python tools/review_episodes.py RoboCrafty/rebot_sort_bottle [--speed 10 --fps 15] [--out review/<name>]

The episode number is burned into the top bar; output is <out>/all_episodes.mp4.

Every camera is tiled left to right, labelled with its name, and every --speed-th frame is kept (played at
--fps), so a camera that is swapped or dead shows up immediately. Open the folder in Finder and use Quick Look.
Needs only PyAV, OpenCV and pandas (all in the repo venv); no ffmpeg binary.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import av
import cv2
import numpy as np
import pandas as pd

from lerobot.utils.constants import HF_LEROBOT_HOME


def read_frames(src: Path, start: float, end: float, step: int, width: int):
    """Every step-th frame of [start, end) from one camera file, resized to the tile width."""
    frames = []
    with av.open(str(src)) as c:
        stream = c.streams.video[0]
        c.seek(int(start / stream.time_base), stream=stream, backward=True)
        n = 0
        for f in c.decode(stream):
            t = float(f.pts * stream.time_base)
            if t < start - 1e-3:
                continue
            if t >= end - 1e-3:
                break
            if n % step == 0:
                img = f.to_ndarray(format="bgr24")
                h = round(img.shape[0] * width / img.shape[1])
                frames.append(cv2.resize(img, (width, h), interpolation=cv2.INTER_AREA))
            n += 1
    return frames


def main():
    p = argparse.ArgumentParser()
    p.add_argument("repo_id")
    p.add_argument("--speed", type=int, default=10, help="keep every N-th frame")
    p.add_argument("--fps", type=int, default=15, help="playback fps of the output")
    p.add_argument("--width", type=int, default=480, help="width of each camera tile")
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--jobs", type=int, default=4)
    p.add_argument("--episodes", type=int, nargs="*", default=None, help="only these episode indices")
    args = p.parse_args()

    root = HF_LEROBOT_HOME / args.repo_id
    out = args.out or Path("review") / args.repo_id.split("/")[-1]
    out.mkdir(parents=True, exist_ok=True)

    eps = pd.concat(pd.read_parquet(f) for f in sorted((root / "meta/episodes").glob("*/*.parquet")))
    cams = sorted({c.split("/")[1] for c in eps.columns if c.startswith("videos/") and c.endswith("/file_index")})
    if args.episodes is not None:
        eps = eps[eps["episode_index"].isin(args.episodes)]

    def render(row):
        """Composited frames (cameras side by side, labelled) of one episode."""
        ep = int(row["episode_index"])
        tiles = []
        for cam in cams:
            k = f"videos/{cam}"
            src = root / "videos" / cam / f"chunk-{int(row[k + '/chunk_index']):03d}" / f"file-{int(row[k + '/file_index']):03d}.mp4"
            fr = read_frames(src, float(row[k + "/from_timestamp"]), float(row[k + "/to_timestamp"]), args.speed, args.width)
            label = cam.split(".")[-1]
            for img in fr:
                cv2.putText(img, label, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
                cv2.putText(img, label, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            tiles.append(fr)
        n = min(len(t) for t in tiles)
        h = max(t[0].shape[0] for t in tiles)
        w = sum(t[0].shape[1] for t in tiles)
        out_frames = []
        for i in range(n):
            canvas = np.zeros((h + 40, w, 3), np.uint8)
            x = 0
            for t in tiles:
                canvas[40 : 40 + t[i].shape[0], x : x + t[i].shape[1]] = t[i]
                x += t[i].shape[1]
            text = f"EPISODE {ep}   t={i * args.speed / 30:.1f}s"
            cv2.putText(canvas, text, (10, 29), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (0, 255, 255), 2)
            out_frames.append(canvas)
        return ep, out_frames

    rows = [r for _, r in eps.iterrows()]
    dst = out / "all_episodes.mp4"
    with av.open(str(dst), "w") as c, ThreadPoolExecutor(args.jobs) as pool:
        s = None
        for i in range(0, len(rows), args.jobs):  # batches keep memory bounded
            for ep, frames in pool.map(render, rows[i : i + args.jobs]):
                if s is None:
                    h, w = frames[0].shape[:2]
                    s = c.add_stream("libx264", rate=args.fps)
                    s.width, s.height, s.pix_fmt, s.options = w + w % 2, h + h % 2, "yuv420p", {"crf": "26"}
                for f in frames:
                    f = cv2.copyMakeBorder(f, 0, s.height - f.shape[0], 0, s.width - f.shape[1], cv2.BORDER_CONSTANT)
                    for pkt in s.encode(av.VideoFrame.from_ndarray(f, format="bgr24")):
                        c.mux(pkt)
                print(f"episode {ep}: {len(frames)} frames")
        for pkt in s.encode():
            c.mux(pkt)
    print(f"\n{len(rows)} episodes in {dst.resolve()}  (cams left->right: {', '.join(cams)})")


if __name__ == "__main__":
    main()
