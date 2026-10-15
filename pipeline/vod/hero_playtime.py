"""Per-hero playtime per map, HUD slot and team from classified VOD scans (not published).

    python pipeline/vod/hero_playtime.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx tmp/vod/s3w1_hero_playtime.csv \
        tmp/vod/261002_scan.npz tmp/vod/261003_scan.npz tmp/vod/261004_scan.npz

Rules (tmp/vod/PLAYTIME_DEFINITION_DRAFT.md, adopted 2026-10-14):
  - Map window = HUD segment paired with MATCH INFO (validate_vs_teamfight.segments / order).
  - A slot's hero run shorter than SWAP_HOLD_S is a misread and becomes a gap.
  - Gaps (no HUD, NONE, UNKNOWN, removed runs) of <= GAP_FILL_S take the hero immediately
    before the gap; a gap with no hero before it (start of the window) is not counted. Longer
    gaps are not counted and are reported. (Leo, 2026-10-14)
  - Time between rounds / halves is excluded: those transitions hide the HUD, so they fall under
    the gap rule; a transition of <= GAP_FILL_S would still be filled (see the gap report).
  - Dead time counts. Frames listed in --exclude (setup phases with the doors closed, detected by
    setup_phases.py) are removed after gap filling and never count.
Team per side: HUD left/right is matched to MATCH INFO team 1/2 with the same straight/swapped
composition scoring as validate_vs_teamfight.py, and the CSV says whether the side was flipped.
Output rows: match_id, map, hud_side, team, flipped, slot, hero, seconds.
"""
import csv
import sys
from pathlib import Path

import numpy as np

import validate_vs_teamfight as v

FPS = 2
SWAP_HOLD_S = 3
GAP_FILL_S = 30


def runs(x):
    """(start, end_exclusive, value) for consecutive equal values."""
    edges = np.flatnonzero(np.diff(x)) + 1
    st = np.r_[0, edges]
    en = np.r_[edges, len(x)]
    return [(int(a), int(b), int(x[a])) for a, b in zip(st, en)]


def slot_timeline(lab):
    """Apply the swap-hold and gap-fill rules to one slot's labels (-1 = no hero).

    Returns (filled labels with -1 where uncounted, list of uncounted gap lengths in seconds).
    """
    lab = lab.copy()
    for a, b, val in runs(lab):
        if val >= 0 and b - a < SWAP_HOLD_S * FPS:
            lab[a:b] = -1
    out = lab.copy()
    rs = runs(lab)
    uncounted = []
    for k, (a, b, val) in enumerate(rs):
        if val >= 0:
            continue
        prev = rs[k - 1][2] if k > 0 else -1
        if (b - a) > GAP_FILL_S * FPS or prev < 0:
            uncounted.append((b - a) / FPS)
            continue
        out[a:b] = prev
    return out, uncounted


def main(xlsx, out_csv, *scans):
    scans = list(scans)
    exclude = {}
    if "--exclude" in scans:  # npz {day: frame indices (2 fps)} that are never playtime, e.g. setup phases
        i = scans.index("--exclude")
        exclude = dict(np.load(scans[i + 1]))
        del scans[i:i + 2]
    maps, fights = v.read_master(xlsx)
    info = {m["MATCH_ID"]: m for m in maps}
    rows, report = [], []
    for s in scans:
        day = Path(s).name[:6]
        z = np.load(Path(s).with_name(f"{day}_heroes.npz"))
        hero, names = z["hero"].astype(np.int32), [str(n) for n in z["names"]]
        bad = [names.index(n) for n in ("NONE", "UNKNOWN", "NO_HUD")]
        seg = v.segments(hero[:, 0] != names.index("NO_HUD"))
        ids = [m["MATCH_ID"] for m in maps if str(m["MATCH_ID"]).startswith(day)]
        if len(seg) != len(ids):
            sys.exit(f"{day}: {len(seg)} HUD segments vs {len(ids)} MATCH INFO maps; not pairing by guess")
        for (a, b), mid in zip(seg, ids):
            m = info[mid]
            flip = False
            if mid in fights:
                t1 = set().union(*[set(h.upper() for h in f[0]) for f in fights[mid]])
                t2 = set().union(*[set(h.upper() for h in f[1]) for f in fights[mid]])
                left = set(v.vod_heroes(hero, names, a, b, range(5)))
                right = set(v.vod_heroes(hero, names, a, b, range(5, 10)))
                flip = len(t1 & right) + len(t2 & left) > len(t1 & left) + len(t2 & right)
            window = (b - a + 1) / FPS
            for slot in range(10):
                lab = hero[a:b + 1, slot].copy()
                lab[np.isin(lab, bad)] = -1
                filled, unc = slot_timeline(lab)
                ex = exclude.get(day)
                if ex is not None:
                    ex = ex[(ex >= a) & (ex <= b)] - a
                    filled[ex] = -1
                side = "left" if slot < 5 else "right"
                team = m["TEAM 1"] if (slot < 5) != flip else m["TEAM 2"]
                ids_, cnt = np.unique(filled[filled >= 0], return_counts=True)
                for i, c in zip(ids_, cnt):
                    rows.append([mid, m["MAP"], side, team, flip, slot, names[i], c / FPS])
                report.append((mid, slot, window, float(np.count_nonzero(filled >= 0)) / FPS, unc))
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["match_id", "map", "hud_side", "team", "flipped", "slot", "hero", "seconds"])
        w.writerows(rows)
    print(f"{out_csv}: {len(rows)} rows")
    # per-map coverage: counted seconds per slot vs map window; uncounted long gaps
    by_map = {}
    for mid, slot, window, counted, unc in report:
        by_map.setdefault(mid, []).append((window, counted, unc))
    for mid, lst in by_map.items():
        window = lst[0][0]
        cov = [c / window for _, c, _ in lst]
        long_gaps = sorted({round(g) for _, _, u in lst for g in u if g > GAP_FILL_S})
        print(f"  {mid:22s} window {window / 60:5.1f} min  slot coverage {min(cov):.0%}-{max(cov):.0%}"
              f"{'  long gaps (s): ' + str(long_gaps) if long_gaps else ''}")


if __name__ == "__main__":
    main(*sys.argv[1:])
