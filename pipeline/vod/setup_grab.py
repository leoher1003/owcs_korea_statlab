"""Grab the top-centre banner region around likely setup phases (map / round / half starts).

    python pipeline/vod/setup_grab.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx tmp/vod/setup/banner.npz \
        261002=URL_FILE 261003=URL_FILE 261004=URL_FILE

Candidates: the start of every map window and every return of the HUD after a gap > GAP_S.
For each, frames from START_PAD s before to SPAN s after are read at 1 fps straight from the
stream (ffmpeg seek; nothing is saved but the crop) and cropped to the banner area, where the
game shows "PREPARE TO ATTACK" / "... UNLOCKS IN" / "ROUND STARTS IN" countdowns during setup.
Saved: t (absolute seconds in the VOD), day, match_id, crop (N x H x W x 3, BGR).
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

import validate_vs_teamfight as v

GAP_S = 4
START_PAD = 5
SPAN = 85
X, Y, W, H = 440, 40, 400, 70
WORKERS = 4


def candidates(maps, day):
    z = np.load(f"tmp/vod/{day}_heroes.npz")
    on = z["hero"][:, 0] != list(z["names"]).index("NO_HUD")
    ids = [m["MATCH_ID"] for m in maps if str(m["MATCH_ID"]).startswith(day)]
    out = []
    for (a, b), mid in zip(v.segments(on), ids):
        idx = np.flatnonzero(on[a:b + 1]) + a
        starts = [idx[0]] + [idx[i + 1] for i in np.flatnonzero(np.diff(idx) > GAP_S * 2)]
        out += [(mid, s / 2) for s in starts]
    return out


def grab(job):
    url, day, mid, t0 = job
    start = max(0.0, t0 - START_PAD)
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", f"{start:.1f}", "-t", str(START_PAD + SPAN), "-i", url,
           "-an", "-vf", f"fps=1,crop={W}:{H}:{X}:{Y}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    crops = np.frombuffer(raw[:n * W * H * 3], np.uint8).reshape(n, H, W, 3)
    return day, mid, start + np.arange(n, dtype=np.float32), crops


def main(xlsx, out, *day_urls):
    maps, _ = v.read_master(xlsx)
    jobs = []
    for du in day_urls:
        day, url_file = du.split("=")
        url = Path(url_file).read_text().strip()
        jobs += [(url, day, mid, t) for mid, t in candidates(maps, day)]
    print(f"{len(jobs)} windows", flush=True)
    res = []
    with ThreadPoolExecutor(WORKERS) as ex:
        for k, r in enumerate(ex.map(grab, jobs), 1):
            res.append(r)
            if k % 10 == 0:
                print(f"{k}/{len(jobs)}", flush=True)
    short = [(d, m) for d, m, t, c in res if len(t) < SPAN // 2]
    if short:
        print("windows with too few frames (stream problem?):", short)
    np.savez_compressed(out,
                        t=np.concatenate([r[2] for r in res]),
                        day=np.concatenate([[r[0]] * len(r[2]) for r in res]),
                        match_id=np.concatenate([[r[1]] * len(r[2]) for r in res]),
                        crop=np.concatenate([r[3] for r in res]))
    print(f"{out}: {sum(len(r[2]) for r in res)} frames")


if __name__ == "__main__":
    main(*sys.argv[1:])
