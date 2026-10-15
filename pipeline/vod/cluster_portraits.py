"""Group HUD portrait crops into look-alike clusters so a person can name each cluster once.

    python pipeline/vod/cluster_portraits.py tmp/vod/clusters tmp/vod/partial/*_scan_partial.npz

Inputs are scan_vod.py outputs. A frame is used only when the in-game HUD bar is on screen
(top band of the thumbnail close to hud_ref.npz), and a crop only when it barely changes from the
same slot 1 s earlier (drops transitions and replays). Remaining crops are sampled every STEP frames, clustered
with MiniBatchKMeans, and written out as:
    sheet_XX.png      contact sheets, one row per cluster (row label = cluster id, size)
    labels.csv        cluster,n,hero,state  -> fill hero (exact list name, or NONE) and state (alive/dead)
    centroids.npy     cluster centers in feature space (for nearest-template classification)
    members.npz       per kept crop: source file index, frame index, slot, cluster
Nothing is labeled automatically; hero names come only from the filled-in labels.csv.
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

STEP = 4            # sample every 4th frame (2 s at 2 fps)
STABLE_LAG = 2      # compare with the crop 2 frames (1 s) earlier
STABLE_MAD = 30.0   # HUD tiles are semi-transparent (median MAD ~15 in-game); this only drops cuts
K = 96
PER_ROW = 14
CELL = 48


REF = np.load(Path(__file__).with_name("hud_ref.npz"))


def hud_present(thumb):
    """True where the thumbnail's top band (y 0-127 at 720p) matches the in-game HUD reference.

    Mean absolute difference over the reference's stable pixels (team-name text excluded). The
    reference, mask and threshold live in hud_ref.npz; see its `source` field for calibration.
    """
    band = thumb[:, 0:8, :].astype(np.float32)
    return np.abs(band - REF["ref"])[:, REF["mask"]].mean(axis=1) < float(REF["threshold"])


def features(crops):
    """16x16 RGB, L2-normalised after mean removal: robust to small brightness shifts."""
    small = np.stack([cv2.resize(c, (16, 16), interpolation=cv2.INTER_AREA) for c in crops]).astype(np.float32)
    f = small.reshape(len(small), -1)
    f -= f.mean(axis=1, keepdims=True)
    f /= np.linalg.norm(f, axis=1, keepdims=True) + 1e-6
    return f


def main(out_dir, *scans):
    out = Path(out_dir)
    crops, src = [], []
    for si, path in enumerate(scans):
        z = np.load(path)
        hud = z["hud"]
        on = hud_present(z["thumb"])
        idx = np.arange(STABLE_LAG, len(hud), STEP)
        idx = idx[on[idx] & on[idx - STABLE_LAG]]
        mad = np.abs(hud[idx].astype(np.int16) - hud[idx - STABLE_LAG].astype(np.int16)).mean(axis=(2, 3, 4))
        for fi, slot in zip(*np.nonzero(mad < STABLE_MAD)):
            crops.append(hud[idx[fi], slot])
            src.append((si, idx[fi], slot))
        print(f"{path}: {len(hud)} frames, {on.mean():.0%} with HUD, kept {np.count_nonzero(mad < STABLE_MAD)} crops",
              flush=True)
    cluster_and_write(out, np.stack(crops), np.array(src), scans, K)


def cluster_and_write(out, crops, src, scans, k):
    """Cluster crops into k groups and write sheets, an empty labels.csv, centroids and members.

    src rows are (scan index, frame, slot) into scans; members.npz keeps them so labelled
    clusters can be traced back to their crops (classify_heroes.py reads it).
    """
    out.mkdir(parents=True, exist_ok=True)
    feats = features(crops)
    km = MiniBatchKMeans(n_clusters=k, random_state=0, batch_size=4096, n_init=3).fit(feats)
    lab = km.labels_
    dist = np.linalg.norm(feats - km.cluster_centers_[lab], axis=1)

    order = np.argsort(-np.bincount(lab, minlength=k))
    rows = []
    rng = np.random.default_rng(0)
    for c in order:
        m = np.nonzero(lab == c)[0]
        # half nearest to the centre, half random: shows both the typical look and the spread
        near = m[np.argsort(dist[m])[:PER_ROW // 2]]
        rand = rng.choice(m, size=min(len(m), PER_ROW - len(near)), replace=False)
        pick = list(near) + list(rand)
        # scan_vod crops are BGR (ffmpeg bgr24), which is what cv2.imwrite expects
        cells = [cv2.resize(crops[i], (CELL, CELL), interpolation=cv2.INTER_NEAREST) for i in pick]
        cells += [np.zeros((CELL, CELL, 3), np.uint8)] * (PER_ROW - len(cells))
        head = np.zeros((CELL, 110, 3), np.uint8)
        cv2.putText(head, f"#{c}", (4, 22), 0, 0.6, (0, 255, 255), 2)
        cv2.putText(head, f"n={len(m)}", (4, 42), 0, 0.45, (255, 255, 255), 1)
        rows.append(np.hstack([head, *cells]))
    for p in range(0, len(rows), 24):
        cv2.imwrite(str(out / f"sheet_{p // 24:02d}.png"), np.vstack(rows[p:p + 24]))

    with open(out / "labels.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["cluster", "n", "hero", "state"])
        for c in order:
            w.writerow([c, int(np.count_nonzero(lab == c)), "", ""])
    np.save(out / "centroids.npy", km.cluster_centers_)
    np.savez_compressed(out / "members.npz", src=src, cluster=lab, scans=np.array(scans))
    print(f"{len(crops)} crops -> {k} clusters, {len(rows)} sheet rows in {out}")


if __name__ == "__main__":
    main(*sys.argv[1:])
