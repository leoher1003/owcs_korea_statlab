"""Unit tests for canonical map names (run: python -m pytest pipeline/test_names.py)."""
from names import canonical_map


def test_case_and_accent_variants_fold_to_one_name():
    for raw in ["ROUTE 66", "Route 66", "route 66"]:
        assert canonical_map(raw) == "Route 66"
    for raw in ["ESPERANÇA", "Esperança", "Esperanca"]:
        assert canonical_map(raw) == "Esperanca"
    assert canonical_map("NEON JUNCTION") == "Neon Junction"


def test_punctuation_is_ignored():
    assert canonical_map("Watchpoint Gibraltar") == "Watchpoint: Gibraltar"


def test_unknown_or_missing_is_none_not_a_guess():
    assert canonical_map("Anubis") is None
    assert canonical_map(None) is None


def test_player_id_confusables_match_the_canonical_id():
    from names import match_player
    roster = ["A1IEN", "M1NUT2", "CH0R0NG", "JASM1NE", "SP1NT", "SORI"]
    assert match_player("ALIEN", roster) == "A1IEN"
    assert match_player("MINUT2", roster) == "M1NUT2"
    assert match_player("CHORONG", roster) == "CH0R0NG"
    assert match_player("jasmine", roster) == "JASM1NE"
    assert match_player("SP1NT", roster) == "SP1NT"


def test_player_id_without_unique_match_is_none():
    from names import match_player
    assert match_player("SORE", ["SORI"]) is None          # real typo: needs an explicit alias
    assert match_player("AIIEN", ["A1IEN", "ALIEN"]) is None  # ambiguous: never merge two players
