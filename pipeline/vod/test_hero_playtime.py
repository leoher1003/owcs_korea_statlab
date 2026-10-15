"""Unit tests for the playtime timeline rules (run: python -m pytest pipeline/vod)."""
import numpy as np

from hero_playtime import FPS, GAP_FILL_S, SWAP_HOLD_S, slot_timeline

A, B, X = 1, 2, -1


def seq(*parts):
    return np.concatenate([np.full(n, val) for val, n in parts]).astype(np.int32)


def test_short_run_is_a_misread_and_is_filled():
    lab = seq((A, 20), (B, SWAP_HOLD_S * FPS - 1), (A, 20))
    out, unc = slot_timeline(lab)
    assert (out == A).all() and unc == []


def test_swap_at_hold_threshold_is_kept():
    lab = seq((A, 20), (B, SWAP_HOLD_S * FPS), (A, 20))
    out, _ = slot_timeline(lab)
    assert (out == B).sum() == SWAP_HOLD_S * FPS


def test_gap_within_limit_same_hero_is_filled():
    lab = seq((A, 10), (X, GAP_FILL_S * FPS), (A, 10))
    out, unc = slot_timeline(lab)
    assert (out == A).all() and unc == []


def test_gap_between_different_heroes_takes_previous_hero():
    lab = seq((A, 10), (X, 10), (B, 10))
    out, _ = slot_timeline(lab)
    assert (out == A).sum() == 20 and (out == B).sum() == 10


def test_gap_over_limit_is_not_counted():
    n = GAP_FILL_S * FPS + 1
    lab = seq((A, 10), (X, n), (A, 10))
    out, unc = slot_timeline(lab)
    assert (out == X).sum() == n and unc == [n / FPS]


def test_all_missing_slot_counts_nothing():
    out, unc = slot_timeline(seq((X, 40)))
    assert (out == X).all() and unc == [20.0]


def test_leading_gap_without_previous_hero_is_not_counted():
    out, unc = slot_timeline(seq((X, 8), (A, 10)))
    assert (out == X).sum() == 8 and unc == [4.0]


def test_trailing_gap_takes_previous_hero():
    out, _ = slot_timeline(seq((A, 10), (X, 8)))
    assert (out == A).all()
