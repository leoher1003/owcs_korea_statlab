"""Canonical names for values typed or extracted in different spellings.

Map names in the MATCH_W* sheets come from result-screen extraction and vary in case and accents
('ROUTE 66', 'Route 66', 'ESPERANÇA', 'Esperanca'). Compare and group them through canonical_map(),
never on the raw string. The canonical list and the folding rule live in fetch_liquipedia.py
(MAP_TYPES, norm) so there is one source for both.
"""
from fetch_liquipedia import MAP_BY_NORM, MAP_TYPES, norm  # noqa: F401  (re-exported)


def canonical_map(raw):
    """Return the canonical map name for any case/accent/punctuation variant, or None if unknown.

    'ROUTE 66' -> 'Route 66', 'ESPERANÇA' -> 'Esperanca', 'NEON JUNCTION' -> 'Neon Junction'.
    Unknown names return None so callers report them instead of guessing.
    """
    if raw is None:
        return None
    return MAP_BY_NORM.get(norm(raw))


# Characters the broadcast font / extraction model confuses in player IDs ('A1IEN' read as 'ALIEN').
_ID_CONFUSABLES = str.maketrans({"0": "O", "1": "I", "L": "I", "|": "I", "5": "S", "8": "B"})


def fold_player_id(raw):
    """Fold a player ID so look-alike spellings compare equal: 'ALIEN' and 'A1IEN' -> 'AIIEN'."""
    s = str(raw).upper().strip().translate(_ID_CONFUSABLES)
    return "".join(ch for ch in s if ch.isalnum())


def match_player(raw, roster_ids):
    """Return the one roster ID whose folded form equals raw's, else None.

    Exact IDs return themselves. If no roster ID or more than one roster ID folds to the same
    key, None is returned so the caller reports the row instead of merging two players.
    """
    raw = str(raw).strip()
    if raw in roster_ids:
        return raw
    key = fold_player_id(raw)
    hits = [p for p in roster_ids if fold_player_id(p) == key]
    return hits[0] if len(hits) == 1 else None
