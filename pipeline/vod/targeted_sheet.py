"""Naming sheet aimed at heroes the classifier misses on specific maps.

    python pipeline/vod/targeted_sheet.py tmp/vod/clusters_target OWCS_STAT_LAB_26_KR_STAGE3.xlsx \
        261002_SEJ_T1_S3 261003_CB_ROZE_S3 ... -- tmp/vod/261002_scan.npz tmp/vod/261003_scan.npz ...

For each listed map: find its HUD segment (same pairing as validate_vs_teamfight.py), take the
HUD slots of the side(s) whose TEAMFIGHT INFO compositions contain a hero the VOD never showed,
and keep crops whose current label is NOT one of the heroes recorded for that side on that map
(UNKNOWN, NONE or a hero the log does not have). Those are the likely misreads. They are
clustered and written like the other naming rounds (sheets, labels.csv, members.npz).
Side orientation uses the same straight/swapped scoring as validate_vs_teamfight.py.
"""
import sys
from pathlib import Path

import numpy as np

from cluster_portraits import cluster_and_write
import validate_vs_teamfight as v

STEP = 2
K = 30


def main(out_dir, xlsx, *rest):
    i = rest.index("--")
    targets, scans = rest[:i], list(rest[i + 1:])
    maps, fights = v.read_master(xlsx)
    crops, src = [], []
    for si, s in enumerate(scans):
        day = Path(s).name[:6]
        mine = [t for t in targets if t.startswith(day)]
        if not mine:
            continue
        z = np.load(Path(s).with_name(f"{day}_heroes.npz"))
        hero, names = z["hero"], [str(n).upper() for n in z["names"]]
        seg = v.segments(hero[:, 0] != names.index("NO_HUD"))
        rows = [m["MATCH_ID"] for m in maps if str(m["MATCH_ID"]).startswith(day)]
        if len(seg) != len(rows):
            sys.exit(f"{day}: {len(seg)} segments vs {len(rows)} maps; fix segmentation first")
        hud = np.load(s)["hud"]
        for mid in mine:
            a, b = seg[rows.index(mid)]
            t = [set().union(*[set(h.upper() for h in f[k]) for f in fights[mid]]) for k in (0, 1)]
            left = v.vod_heroes(hero, names, a, b, range(5))
            right = v.vod_heroes(hero, names, a, b, range(5, 10))
            flip = len(t[0] & set(right)) + len(t[1] & set(left)) > len(t[0] & set(left)) + len(t[1] & set(right))
            vod = (right, left) if flip else (left, right)
            for side in (0, 1):
                if not t[side] - set(vod[side]):
                    continue  # nothing missing on this side
                slots = range(5, 10) if (side == 0) == flip else range(0, 5)
                ok = {names.index(h) for h in t[side] if h in names}
                n0 = len(crops)
                for f in range(a, b + 1, STEP):
                    for slot in slots:
                        if hero[f, slot] not in ok and hero[f, slot] != names.index("NO_HUD"):
                            crops.append(hud[f, slot])
                            src.append((si, f, slot))
                print(f"{mid} side {side + 1} ({'right' if slots[0] else 'left'} HUD): missing "
                      f"{sorted(t[side] - set(vod[side]))}, {len(crops) - n0} suspect crops", flush=True)
        del hud
    cluster_and_write(Path(out_dir), np.stack(crops), np.array(src), scans, min(K, max(2, len(crops) // 40)))


if __name__ == "__main__":
    main(*sys.argv[1:])
