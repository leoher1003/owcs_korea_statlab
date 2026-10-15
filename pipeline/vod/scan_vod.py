"""Pass 1 over a broadcast VOD: decode at 2 fps (1280x720) and keep only small per-frame features.

    python3 pipeline/vod/scan_vod.py tmp/vod/261002.mp4 tmp/vod/261002_scan.npz
    python3 pipeline/vod/scan_vod.py "$(yt-dlp -g -f 'bv*[height<=480]' URL)" tmp/vod/261002_scan.npz   # stream, nothing saved

Saved arrays:
    t        seconds from the start of the VOD
    thumb    80x45 grayscale thumbnail of every frame (result-screen / replay detection)
    hud      10 HUD portrait crops per frame, 32x32 RGB (alive/dead and hero identity)
Portrait boxes come from hud_layout.json (1280x720 coordinates). Nothing here calls a model.
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

W, H, FPS = 1280, 720, 2
LAYOUT = json.loads(Path(__file__).with_name("hud_layout.json").read_text())


def frames(path):
    src = str(path)
    net = ["-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "10"] if src.startswith("http") else []
    cmd = ["ffmpeg", "-loglevel", "error", *net, "-i", src, "-an",
           "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
    size = W * H * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    p.wait()


def main(vod, out):
    boxes = LAYOUT["portraits"]["team1"] + LAYOUT["portraits"]["team2"]
    t, thumbs, huds = [], [], []
    for i, f in enumerate(frames(vod)):
        t.append(i / FPS)
        thumbs.append(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (80, 45), interpolation=cv2.INTER_AREA))
        huds.append([cv2.resize(f[y:y + h, x:x + w], (32, 32), interpolation=cv2.INTER_AREA) for x, y, w, h in boxes])
        if i % 1200 == 0:
            print(f"{i / FPS / 60:.0f} min", flush=True)
    np.savez_compressed(out, t=np.array(t, np.float32), thumb=np.array(thumbs), hud=np.array(huds))
    print(f"{out}: {len(t)} frames")


if __name__ == "__main__":
    main(*sys.argv[1:3])
