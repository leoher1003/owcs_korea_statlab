"""Re-cluster mixed clusters from cluster_portraits.py into smaller sub-clusters for naming.

    python pipeline/vod/split_clusters.py tmp/vod/clusters 79 76 95 35

Writes into the same folder:
    split_sheet.png   one row per sub-cluster (row label = cluster.sub, size)
    split_labels.csv  cluster,sub,n,hero,state  -> fill like labels.csv
    split_members.npz per member of the split clusters: index into members.npz, sub id
Sub-cluster count per cluster is chosen as max(2, min(SUB_K, n // 40)).
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np
from sklearn.cluster import KMeans

from cluster_portraits import CELL, PER_ROW, features

SUB_K = 8


def main(folder, *clusters):
    out = Path(folder)
    mem = np.load(out / "members.npz")
    src, lab, scans = mem["src"], mem["cluster"], [str(s) for s in mem["scans"]]
    huds = [np.load(s)["hud"] for s in scans]
    rng = np.random.default_rng(0)
    rows, table, members = [], [], []
    for c in map(int, clusters):
        idx = np.nonzero(lab == c)[0]
        crops = np.stack([huds[s][f, slot] for s, f, slot in src[idx]])
        k = max(2, min(SUB_K, len(idx) // 40))
        sub = KMeans(n_clusters=k, random_state=0, n_init=5).fit_predict(features(crops))
        for s in np.argsort(-np.bincount(sub, minlength=k)):
            m = np.nonzero(sub == s)[0]
            pick = rng.choice(m, size=min(len(m), PER_ROW), replace=False)
            cells = [cv2.resize(crops[i], (CELL, CELL), interpolation=cv2.INTER_NEAREST) for i in pick]
            cells += [np.zeros((CELL, CELL, 3), np.uint8)] * (PER_ROW - len(cells))
            head = np.zeros((CELL, 110, 3), np.uint8)
            cv2.putText(head, f"#{c}.{s}", (4, 22), 0, 0.6, (0, 255, 255), 2)
            cv2.putText(head, f"n={len(m)}", (4, 42), 0, 0.45, (255, 255, 255), 1)
            rows.append(np.hstack([head, *cells]))
            table.append([c, s, len(m), "", ""])
        members += [(i, s) for i, s in zip(idx, sub)]
    cv2.imwrite(str(out / "split_sheet.png"), np.vstack(rows))
    with open(out / "split_labels.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["cluster", "sub", "n", "hero", "state"])
        w.writerows(table)
    np.savez_compressed(out / "split_members.npz", members=np.array(members))
    print(f"{len(rows)} sub-clusters from clusters {clusters}")


if __name__ == "__main__":
    main(*sys.argv[1:])
