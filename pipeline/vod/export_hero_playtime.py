"""Export VOD per-hero playtime for the site's Hero Playtime page (separate from the scoreboard data).

    python pipeline/vod/export_hero_playtime.py OWCS_STAT_LAB_26_KR_STAGE3.xlsx \
        tmp/vod/s3w1_player_hero_playtime_nosetup.csv data/stage3/vod_hero_playtime.csv site/data/hero_playtime_s3.js

Input: player_playtime.py output (per map, slot, hero; setup excluded). Each row gets the map-level
Position from MATCH_W* (a player can change role between maps), the hero's role (heroes_2026_10.json,
Sombra = DPS before the 2026-10-06 rework) and is aggregated to player x position x hero over the
covered maps. Seconds are VOD estimates, never mixed with official scoreboard playtime.
Writes the CSV (utf-8-sig, like the other public CSVs) and a JS file defining
window.OWCS_HERO_PLAYTIME_S3 = {meta, rows}.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl
import pandas as pd

PATCH_2026_10 = "261006"  # matches from this date on use the post-rework roles (Sombra = Support)


def role_of(hero, match_id, roles):
    if hero == "Sombra" and match_id[:6] < PATCH_2026_10:
        return "D"
    return roles[hero]


def main(xlsx, player_csv, out_csv, out_js):
    roles = json.loads((Path(__file__).parent / "heroes_2026_10.json").read_text())["roles"]
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    position = {}
    for sh in [s for s in wb.sheetnames if s.startswith("MATCH_W")]:
        rows = list(wb[sh].iter_rows(values_only=True))
        if not rows:
            continue
        head = rows[0]
        for r in rows[1:]:
            if r[head.index("MATCH_ID")]:
                position[(r[head.index("MATCH_ID")], r[head.index("Player")])] = r[head.index("Position")]

    d = pd.read_csv(player_csv, encoding="utf-8-sig")
    missing = sorted({(m, p) for m, p in zip(d.match_id, d.player) if (m, p) not in position})
    if missing:
        sys.exit(f"No MATCH_W Position for: {missing[:5]}")
    d["position"] = [position[(m, p)] for m, p in zip(d.match_id, d.player)]
    d["role"] = [role_of(h, m, roles) for h, m in zip(d.hero, d.match_id)]

    agg = defaultdict(lambda: {"seconds": 0.0, "maps": set()})
    for r in d.itertuples():
        a = agg[(r.team, r.player, r.position, r.hero, r.role)]
        a["seconds"] += r.seconds
        a["maps"].add(r.match_id)
    pmaps = d.groupby(["player", "position"]).match_id.nunique().to_dict()  # maps per player x position
    out = [{"team": t, "player": p, "position": pos, "hero": h, "role": ro,
            "seconds": round(a["seconds"], 1), "maps": len(a["maps"]), "player_maps": int(pmaps[(p, pos)])}
           for (t, p, pos, h, ro), a in sorted(agg.items())]

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    per = d.groupby(["match_id", "player"]).agg(vod=("seconds", "sum"), off=("official_seconds", "first"))
    ratio = per.vod / per.off
    maps = sorted(d.match_id.unique())
    meta = {
        "weeks": sorted({int(r[0]) for r in wb["MATCH INFO"].iter_rows(min_row=2, values_only=True)
                         if r[16] in maps}),
        "maps": len(maps),
        "playerMaps": int(len(per)),
        "within5": round(float((abs(ratio - 1) <= 0.05).mean()) * 100, 1),
        "within10": round(float((abs(ratio - 1) <= 0.10).mean()) * 100, 1),
        "medianAbsErrorSec": round(float((per.vod - per.off).abs().median()), 1),
    }
    # per-map rows for the player breakdown on the site (same seconds, not aggregated)
    mi = {r[16]: r for r in wb["MATCH INFO"].iter_rows(min_row=2, values_only=True) if r[16]}
    map_rows = [{"match_id": r.match_id, "date": str(mi[r.match_id][4])[:10], "map": mi[r.match_id][8],
                 "opponent": mi[r.match_id][7] if mi[r.match_id][6] == r.team else mi[r.match_id][6],
                 "player": r.player, "position": r.position, "hero": r.hero, "seconds": round(r.seconds, 1)}
                for r in d.sort_values(["match_id", "player", "seconds"], ascending=[True, True, False]).itertuples()]
    Path(out_js).write_text("window.OWCS_HERO_PLAYTIME_S3 = "
                            + json.dumps({"meta": meta, "rows": out, "mapRows": map_rows}, ensure_ascii=False)
                            + ";\n", encoding="utf-8")
    print(f"{out_csv}: {len(out)} rows; {out_js}; meta {meta}")


if __name__ == "__main__":
    main(*sys.argv[1:])
