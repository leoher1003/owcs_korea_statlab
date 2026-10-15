"""Cluster the portraits classify_heroes.py marked UNKNOWN, for another naming round.

    python pipeline/vod/unknown_sheet.py tmp/vod/clusters_unknown tmp/vod/261002_scan.npz ...
    python pipeline/vod/unknown_sheet.py tmp/vod/clusters_unknown2 --icons tmp/vod/hero_icons tmp/vod/2610*_scan.npz

Reads <scan>_heroes.npz next to each scan, samples UNKNOWN crops every STEP frames, and writes
the same sheets / labels.csv / members.npz as cluster_portraits.py into the output folder.
Pass that folder to classify_heroes.py together with the earlier ones to use the new labels.

--icons DIR: official 2D hero icons (<hero-key>.png, RGBA). Each cluster centre is compared with
every icon and the closest one is written to labels.csv as `suggest` (with its similarity) and
drawn at the end of the sheet row. The hero column stays empty: a suggestion is only a hint,
because broadcast portraits (semi-transparent tile, team tint, 32x32) differ from the icon art.
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np

from cluster_portraits import CELL, cluster_and_write, features

STEP = 2
K = 48


def icon_features(folder):
    """Icons composited on mid-grey, resized like a HUD crop, then the usual features."""
    names, crops = [], []
    for p in sorted(Path(folder).glob("*.png")):
        im = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
        rgb, a = im[..., :3].astype(np.float32), im[..., 3:4].astype(np.float32) / 255
        flat = (rgb * a + 128 * (1 - a)).astype(np.uint8)
        names.append(p.stem)
        crops.append(cv2.resize(flat, (32, 32), interpolation=cv2.INTER_AREA))
    return names, np.stack(crops), features(np.stack(crops))


def add_suggestions(out, icons_dir):
    names, icon_imgs, icon_f = icon_features(icons_dir)
    cent = np.load(out / "centroids.npy")
    cent /= np.linalg.norm(cent, axis=1, keepdims=True) + 1e-6
    sim = cent @ icon_f.T
    rows = list(csv.reader(open(out / "labels.csv", encoding="utf-8-sig")))
    head, body = rows[0], rows[1:]
    sheets = sorted(out.glob("sheet_*.png"))
    imgs = [cv2.imread(str(s)) for s in sheets]
    pad = []
    for r in body:
        c = int(r[0])
        j = int(np.argmax(sim[c]))
        r.append(f"{names[j]} ({sim[c, j]:.2f})")
        cell = cv2.resize(icon_imgs[j], (CELL, CELL), interpolation=cv2.INTER_NEAREST)
        tag = np.zeros((CELL, 120, 3), np.uint8)
        cv2.putText(tag, names[j][:12], (4, 20), 0, 0.45, (0, 200, 255), 1)
        cv2.putText(tag, f"sim {sim[c, j]:.2f}", (4, 40), 0, 0.4, (200, 200, 200), 1)
        pad.append(np.hstack([np.full((CELL, 8, 3), 255, np.uint8), cell, tag]))
    for si, img in enumerate(imgs):
        part = pad[si * 24:(si + 1) * 24]
        cv2.imwrite(str(sheets[si]), np.hstack([img, np.vstack(part)]))
    with open(out / "labels.csv", "w", newline="", encoding="utf-8-sig") as fh:
        csv.writer(fh).writerows([head + ["suggest"]] + body)


def main(out_dir, *args):
    args = list(args)
    icons = None
    if "--icons" in args:
        i = args.index("--icons")
        icons = args[i + 1]
        del args[i:i + 2]
    crops, src = [], []
    for si, s in enumerate(args):
        h = np.load(Path(s).with_name(Path(s).name.replace("_scan.npz", "_heroes.npz")))
        unk = h["hero"] == list(h["names"]).index("UNKNOWN")
        unk[np.arange(len(unk)) % STEP != 0] = False
        hud = np.load(s)["hud"]
        for f, slot in zip(*np.nonzero(unk)):
            crops.append(hud[f, slot])
            src.append((si, f, slot))
        del hud
        print(f"{s}: {np.count_nonzero(unk)} UNKNOWN crops sampled", flush=True)
    k = min(K, max(2, len(crops) // 50))
    cluster_and_write(Path(out_dir), np.stack(crops), np.array(src), args, k)
    if icons:
        add_suggestions(Path(out_dir), icons)


if __name__ == "__main__":
    main(*sys.argv[1:])
