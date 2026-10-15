"""Find setup phases (doors closed) in the banner crops and list their frames for hero_playtime.py --exclude.

    python pipeline/vod/setup_phases.py tmp/vod/setup/banner.npz pipeline/vod/setup_templates.npz \
        tmp/vod/setup/exclude_frames.npz

banner.npz comes from setup_grab.py (top-centre banner crops at 1 fps around map / round starts).
Each crop is matched (normalised cross-correlation, grayscale) against the banner-text templates
cropped by hand from the broadcast: WAITING, ASSEMBLE, PREPARE_ATTACK, CP_UNLOCKS, FP_UNLOCKS,
GET_READY, PREPARE_DEF, DEFEND_OBJ (ESCORT is in the file but not used: it also shows in play).
A crop whose best score is >= MATCH_MIN takes that template's label. Labels in SETUP mark setup
time; each such 1 fps sample excludes the 2 fps scan frames within ±0.5 s of it.

The phase set was chosen on 2026-10-14 by fitting VOD-minus-official playtime per map: excluding
these phases (not CP_UNLOCKS / FP_UNLOCKS / DEFEND_OBJ) gave the smallest error.
Output: npz {day: sorted 2 fps frame indices}.
"""
import sys

import cv2
import numpy as np

MATCH_MIN = 0.75
UNUSED = {"ESCORT"}
SETUP = {"WAITING", "ASSEMBLE", "PREPARE_ATTACK", "GET_READY", "PREPARE_DEF"}


def match_phases(crops, templates):
    """Return (best score, best template index) for every BGR crop."""
    names = list(templates)
    best = np.zeros(len(crops))
    lab = np.full(len(crops), -1)
    for i, c in enumerate(crops):
        g = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
        sc = [cv2.minMaxLoc(cv2.matchTemplate(g, templates[k], cv2.TM_CCOEFF_NORMED))[1] for k in names]
        j = int(np.argmax(sc))
        best[i], lab[i] = sc[j], j
    return best, lab


def exclude_frames(t, day, best, lab, names):
    """{day: sorted 2 fps frame indices} for the samples matched to a setup phase."""
    out = {}
    for k in np.flatnonzero(best >= MATCH_MIN):
        if names[lab[k]] in SETUP:
            s = int(round(t[k]))
            out.setdefault(str(day[k]), set()).update({2 * s - 1, 2 * s, 2 * s + 1})
    return {d: np.array(sorted(v)) for d, v in out.items()}


def main(banner, templates, out):
    z = np.load(banner)
    tpl = {k: v for k, v in np.load(templates).items() if k not in UNUSED}
    best, lab = match_phases(z["crop"], tpl)
    ex = exclude_frames(z["t"], z["day"], best, lab, list(tpl))
    np.savez(out, **ex)
    print(f"{out}: " + ", ".join(f"{d} {len(v) / 2:.0f} s" for d, v in sorted(ex.items())) + " (incl. overlap)")


if __name__ == "__main__":
    main(*sys.argv[1:])
