"""Label every HUD portrait in full scans with a hero, using the human-named clusters as references.

    python pipeline/vod/classify_heroes.py tmp/vod/clusters,tmp/vod/clusters_unknown tmp/vod/261002_scan.npz ...

References: every crop in each folder's members.npz whose cluster (or split sub-cluster) has a
hero in that folder's labels.csv / split_labels.csv (comma-separate several naming rounds). Classification is k-nearest-neighbour on cluster_portraits.features
(cosine distance), majority vote of K neighbours.
    - A crop farther than the reference set's own 99th-percentile neighbour distance -> UNKNOWN
      (new look or new hero; flagged, never forced to the closest hero).
    - Frames without the in-game HUD -> NO_HUD.
Label hygiene: hero names must be in heroes_2026_10.json or NONE (case-insensitive match on
exact spelling only); state is lower-cased. Any other name stops the run with the offending rows.

Also reports leave-one-day-out agreement with the cluster labels (consistency check only: those
labels are cluster-level, so this is not ground-truth accuracy).

Writes <scan>_heroes.npz next to each scan: hero[frame, slot] (index into names), dist, names.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import torch

from cluster_portraits import features, hud_present

K = 5
BATCH = 1024  # queries per distance block: 1024 x n_ref floats (~250 MB at 62k refs)
HERE = Path(__file__).parent
CANON = {h.upper(): h for h in json.loads((HERE / "heroes_2026_10.json").read_text())["roles"]}
CANON["NONE"] = "NONE"
DEV = "mps" if torch.backends.mps.is_available() else "cpu"


def read_labels(folder):
    """cluster (or (cluster, sub)) -> hero; raises on names outside the hero list."""
    labels, bad = {}, []
    for name, key in (("labels.csv", lambda r: int(r["cluster"])),
                      ("split_labels.csv", lambda r: (int(r["cluster"]), int(r["sub"])))):
        path = folder / name
        if not path.exists():
            continue
        for r in csv.DictReader(open(path, encoding="utf-8-sig")):
            h = r["hero"].strip()
            if not h:
                continue
            if h.upper() not in CANON:
                bad.append(f"{name} cluster {r['cluster']}{'.' + r['sub'] if 'sub' in r else ''}: {h!r}")
                continue
            labels[key(r)] = CANON[h.upper()]
    if bad:
        sys.exit("Unknown hero names (fix the csv; no fuzzy matching):\n  " + "\n  ".join(bad))
    return labels


def references(folder, labels):
    mem = np.load(folder / "members.npz")
    src, lab, scans = mem["src"], mem["cluster"], [str(s) for s in mem["scans"]]
    hero = np.array([labels.get(int(c), "") for c in lab], dtype=object)
    split = folder / "split_members.npz"
    if split.exists():
        for i, sub in np.load(split)["members"]:
            hero[i] = labels.get((int(lab[i]), int(sub)), "")  # split result replaces the parent label
    keep = np.nonzero(hero != "")[0]
    # one scan in memory at a time: each hud array is ~1 GB and holding all of them thrashes swap
    crops = np.empty((len(keep), 32, 32, 3), np.uint8)  # scan_vod.py crop size
    for si, s in enumerate(scans):
        rows = np.nonzero(src[keep, 0] == si)[0]
        if len(rows):
            hud = np.load(s)["hud"]
            crops[rows] = hud[src[keep][rows, 1], src[keep][rows, 2]]
            del hud
    day = np.array([Path(scans[s]).name[:6] for s in src[keep, 0]])  # yymmdd: same day across partial/full scans
    key = np.array([f"{d}:{f}:{sl}" for d, (_, f, sl) in zip(day, src[keep])])  # same crop in any scan of that day
    return features(crops), hero[keep], day, key


def knn(ref, ref_y, q, names):
    """Return (label index, mean cosine distance of the K neighbours) for each query row."""
    r = torch.tensor(ref, device=DEV)
    y = torch.tensor([names.index(h) for h in ref_y], device=DEV)
    out_l, out_d = [], []
    for b in range(0, len(q), BATCH):
        qb = torch.tensor(q[b:b + BATCH], device=DEV)
        d, i = torch.topk(1 - qb @ r.T, K, largest=False)
        votes = torch.nn.functional.one_hot(y[i], len(names)).sum(1)
        out_l.append(votes.argmax(1).cpu())
        out_d.append(d.mean(1).cpu())
        del qb, d, i, votes
    if DEV == "mps":
        torch.mps.empty_cache()
    return torch.cat(out_l).numpy(), torch.cat(out_d).numpy()


def main(folders, *scans):
    parts = [references(Path(f), read_labels(Path(f))) for f in folders.split(",")]
    ref, ref_y, day, key = (np.concatenate(x) for x in zip(*parts))
    # A crop labelled in several rounds is kept once (Leo, 2026-10-14, rule "b"): a hero name beats
    # NONE whichever round gave it; between two hero names the latest (most targeted) round wins.
    # Labels are per cluster row, so a frame can inherit its row's majority label; disagreements
    # are reported, never merged silently.
    chosen = {}
    for i, k in enumerate(key):
        j = chosen.get(k)
        if j is None or ref_y[i] != "NONE" or ref_y[j] == "NONE":
            chosen[k] = i
    conflicts = Counter()
    for i, k in enumerate(key):
        if ref_y[i] != ref_y[chosen[k]]:
            conflicts[(ref_y[i], ref_y[chosen[k]])] += 1
    keep = np.array(sorted(chosen.values()))
    if conflicts:
        print(f"{sum(conflicts.values())} conflicting references resolved (hero > NONE, else latest):",
              ", ".join(f"{a}->{b} {c}" for (a, b), c in conflicts.most_common()))
    ref, ref_y, day = ref[keep], ref_y[keep], day[keep]
    names = sorted(set(ref_y)) + ["UNKNOWN", "NO_HUD"]
    print(f"{len(ref)} reference crops, {len(names) - 2} classes (incl. NONE)")

    for d in np.unique(day):  # leave-one-day-out consistency with the cluster labels
        tr, te = day != d, day == d
        pred, _ = knn(ref[tr], ref_y[tr], ref[te], names)
        print(f"  held-out day {d}: {np.mean(np.array(names)[pred] == ref_y[te]):.1%} agree ({te.sum()} crops)")

    self_l, self_d = knn(ref, ref_y, ref, names)
    # distance to K neighbours includes the crop itself; use the 99th percentile as the novelty cut
    cut = float(np.percentile(self_d, 99))
    print(f"UNKNOWN cut (cosine distance): {cut:.3f}")

    for s in scans:
        z = np.load(s)
        on = hud_present(z["thumb"])
        hud = z["hud"]
        hero = np.full(hud.shape[:2], names.index("NO_HUD"), np.int16)
        dist = np.full(hud.shape[:2], np.nan, np.float32)
        fi = np.nonzero(on)[0]
        q = features(hud[fi].reshape(-1, *hud.shape[2:]))
        lab, dd = knn(ref, ref_y, q, names)
        lab[dd > cut] = names.index("UNKNOWN")
        hero[fi] = lab.reshape(len(fi), -1)
        dist[fi] = dd.reshape(len(fi), -1)
        out = Path(s).with_name(Path(s).name.replace("_scan.npz", "_heroes.npz"))
        np.savez_compressed(out, hero=hero, dist=dist, names=np.array(names), t=z["t"])
        h = hero[fi].ravel()
        share = {n: np.mean(h == i) for i, n in enumerate(names) if n in ("NONE", "UNKNOWN")}
        print(f"{out}: {len(fi)} HUD frames, NONE {share.get('NONE', 0):.1%}, UNKNOWN {share.get('UNKNOWN', 0):.1%}")


if __name__ == "__main__":
    main(*sys.argv[1:])
