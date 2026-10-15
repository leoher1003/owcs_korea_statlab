"""Team composition timelines from classified VOD scans, checked against TEAMFIGHT INFO (not published).

    python pipeline/vod/comp_playtime.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx tmp/vod/s3w1_comp_playtime.csv \
        tmp/vod/261002_scan.npz tmp/vod/261003_scan.npz tmp/vod/261004_scan.npz --exclude tmp/vod/setup/exclude_frames.npz

Each HUD slot gets the same timeline as hero_playtime.py (swap hold, gap fill, setup excluded).
At every frame where all five slots of a side have a hero, the side's composition is the unordered
5-hero set, keyed Tank / DPS / Support then name like sql/teamfights.sql. Frames where any slot is
uncounted are not attributed to a composition.

Output rows: match_id, team, comp, seconds. The check prints, per map and team, how many of the
compositions recorded in TEAMFIGHT INFO (fight-start snapshots) the VOD shows for >= MIN_COMP_S.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

import hero_playtime as hp
import validate_vs_teamfight as v

MIN_COMP_S = 10
ROLE_RANK = {"T": 0, "D": 1, "S": 2}


def comp_key(heroes, roles):
    """Order-independent key 'D.Mon / Cassidy / Tracer / Ana / Jetpack Cat' (Tank, DPS, Support, name)."""
    return " / ".join(sorted(heroes, key=lambda h: (ROLE_RANK[roles[h]], h)))


def main(xlsx, out_csv, *args):
    args = list(args)
    exclude = {}
    if "--exclude" in args:
        i = args.index("--exclude")
        exclude = dict(np.load(args[i + 1]))
        del args[i:i + 2]
    roles = json.loads((Path(__file__).parent / "heroes_2026_10.json").read_text())["roles"]
    roles["Sombra"] = "D"  # Week 1 is before the 2026-10-06 rework (Sombra -> Support)
    maps, fights = v.read_master(xlsx)
    info = {m["MATCH_ID"]: m for m in maps}
    rows, checks = [], []
    for s in args:
        day = Path(s).name[:6]
        z = np.load(Path(s).with_name(f"{day}_heroes.npz"))
        hero, names = z["hero"].astype(np.int32), [str(n) for n in z["names"]]
        bad = [names.index(n) for n in ("NONE", "UNKNOWN", "NO_HUD")]
        seg = v.segments(hero[:, 0] != names.index("NO_HUD"))
        ids = [m["MATCH_ID"] for m in maps if str(m["MATCH_ID"]).startswith(day)]
        if len(seg) != len(ids):
            sys.exit(f"{day}: {len(seg)} HUD segments vs {len(ids)} MATCH INFO maps")
        for (a, b), mid in zip(seg, ids):
            filled = []
            for slot in range(10):
                lab = hero[a:b + 1, slot].copy()
                lab[np.isin(lab, bad)] = -1
                f, _ = hp.slot_timeline(lab)
                ex = exclude.get(day)
                if ex is not None:
                    f[ex[(ex >= a) & (ex <= b)] - a] = -1
                filled.append(f)
            filled = np.stack(filled, axis=1)
            # side -> team, same straight/swapped scoring as validate_vs_teamfight
            logged = fights.get(mid, [])
            t1 = {h.upper() for f in logged for h in f[0]}
            t2 = {h.upper() for f in logged for h in f[1]}
            left = set(v.vod_heroes(hero, names, a, b, range(5)))
            right = set(v.vod_heroes(hero, names, a, b, range(5, 10)))
            flip = len(t1 & right) + len(t2 & left) > len(t1 & left) + len(t2 & right)
            m = info[mid]
            for side, slots in ((0, range(5)), (1, range(5, 10))):
                team = m["TEAM 1"] if (side == 0) != flip else m["TEAM 2"]
                secs = defaultdict(float)
                for row in filled[:, list(slots)]:
                    if (row >= 0).all():
                        secs[comp_key([names[i] for i in row], roles)] += 0.5
                rows += [[mid, team, k, s_] for k, s_ in secs.items()]
                log_side = 0 if team == m["TEAM 1"] else 1
                logged_comps = {comp_key(_canon(f[log_side], roles), roles) for f in logged}
                seen = {k for k, s_ in secs.items() if s_ >= MIN_COMP_S}
                checks.append((mid, team, len(logged_comps), len(logged_comps & seen),
                               sorted(logged_comps - seen)))
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["match_id", "team", "comp", "seconds"])
        w.writerows(rows)
    tot = sum(c[2] for c in checks)
    hit = sum(c[3] for c in checks)
    print(f"{out_csv}: {len(rows)} rows")
    print(f"TEAMFIGHT INFO compositions seen in VOD (>= {MIN_COMP_S}s): {hit}/{tot} ({hit / tot:.1%})")
    for mid, team, n, k, miss in checks:
        if k < n:
            print(f"  {mid} {team}: {k}/{n}  missing {miss}")


def _canon(heroes, roles):
    """Map TEAMFIGHT INFO's uppercase spelling to the hero list's spelling (exact, case-insensitive)."""
    by_upper = {h.upper(): h for h in roles}
    out = []
    for h in heroes:
        if h.upper() not in by_upper:
            sys.exit(f"TEAMFIGHT INFO hero '{h}' is not in heroes_2026_10.json")
        out.append(by_upper[h.upper()])
    return out


if __name__ == "__main__":
    main(*sys.argv[1:])
