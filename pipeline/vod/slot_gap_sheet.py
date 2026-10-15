"""Naming sheet from the unlabelled frames (NONE / UNKNOWN) of specific player-map slots.

    python pipeline/vod/slot_gap_sheet.py tmp/vod/clusters_slots OWCS_STAT_LAB_26_KR_STAGE3.xlsx \
        tmp/vod/s3w1_player_hero_playtime_nosetup.csv 261002_CB_PF_S1:SORI ... -- tmp/vod/2610*_scan.npz

For slots whose VOD playtime falls short of the official MATCH_W1 playtime: take that slot's
frames inside the map window that are classified NONE or UNKNOWN (sampled every STEP frames)
and cluster them for naming, like the other rounds.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from cluster_portraits import cluster_and_write
import validate_vs_teamfight as v

STEP = 2


def main(out_dir, xlsx, player_csv, *rest):
    i = rest.index("--")
    targets, scans = [t.split(":") for t in rest[:i]], list(rest[i + 1:])
    maps, _ = v.read_master(xlsx)
    slots = pd.read_csv(player_csv, encoding="utf-8-sig").drop_duplicates(["match_id", "player"])
    slot_of = {(m, p): s for m, p, s in zip(slots.match_id, slots.player, slots.slot)}
    crops, src = [], []
    for si, s in enumerate(scans):
        day = Path(s).name[:6]
        mine = [(m, p) for m, p in targets if m.startswith(day)]
        if not mine:
            continue
        z = np.load(Path(s).with_name(f"{day}_heroes.npz"))
        hero, names = z["hero"], [str(n) for n in z["names"]]
        seg = v.segments(hero[:, 0] != names.index("NO_HUD"))
        ids = [m["MATCH_ID"] for m in maps if str(m["MATCH_ID"]).startswith(day)]
        hud = np.load(s)["hud"]
        gap = [names.index("NONE"), names.index("UNKNOWN")]
        for mid, player in mine:
            a, b = seg[ids.index(mid)]
            slot = slot_of[(mid, player)]
            fr = np.arange(a, b + 1, STEP)
            fr = fr[np.isin(hero[fr, slot], gap)]
            crops += [hud[f, slot] for f in fr]
            src += [(si, f, slot) for f in fr]
            print(f"{mid} {player} slot {slot}: {len(fr)} NONE/UNKNOWN crops", flush=True)
        del hud
    cluster_and_write(Path(out_dir), np.stack(crops), np.array(src), scans, min(30, max(2, len(crops) // 40)))


if __name__ == "__main__":
    main(*sys.argv[1:])
