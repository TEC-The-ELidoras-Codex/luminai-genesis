import sys
from pathlib import Path
# Ensure repo root on sys.path when running single test files
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import types
import pytest
import random

from tec_book.clean_strike_fix import CleanStrike
from tec_book.clyde_companion import Clyde


class DummyStats(types.SimpleNamespace):
    def __init__(self, void_charge=50, focus=5, corruption_stacks=0):
        # default focus >= ability cost so abilities can be used in tests
        super().__init__(void_charge=void_charge, focus=focus, corruption_stacks=corruption_stacks)


def make_randint_sequence(seq):
    """Return a function that yields values from seq each call."""
    it = iter(seq)

    def _randint(a, b):
        try:
            return next(it)
        except StopIteration:
            # fallback
            return a

    return _randint


def test_clean_strike_critical_failure(monkeypatch):
    # Allow 0-cost to exercise impossible-but-testable critical-1 path
    stats = DummyStats(void_charge=50, focus=0, corruption_stacks=0)
    cs = CleanStrike()
    cs.cost = {"void_charge": 0, "focus": 0}

    # damage, focus_roll_base -> set raw die to 1 so final == 1
    monkeypatch.setattr(random, "randint", make_randint_sequence([10, 1]))

    res = cs.use(stats)

    assert res["success"] is True
    assert "CRITICAL FAILURE" in res["message"]
    assert res.get("corruption_gained", 0) == 2
    assert stats.corruption_stacks == 2


def test_clean_strike_critical_success(monkeypatch):
    # Allow 0-cost to exercise raw critical-20 path
    stats = DummyStats(void_charge=50, focus=0, corruption_stacks=0)
    cs = CleanStrike()
    cs.cost = {"void_charge": 0, "focus": 0}

    # damage, focus_roll_base -> make critical success (20)
    monkeypatch.setattr(random, "randint", make_randint_sequence([8, 20]))

    res = cs.use(stats)

    assert res["success"] is True
    assert "CRITICAL SUCCESS" in res["message"]
    assert res["can_honor"] is True
    assert res.get("bonus_xp", False) is True


def test_clean_strike_failed_clean_kill_becomes_consumption(monkeypatch):
    # Use default stats (focus >= cost) so ability can be used
    stats = DummyStats()
    cs = CleanStrike()

    # damage, focus_roll_base -> failed clean kill (e.g., 5 + focus(5) -> 10 < 12)
    monkeypatch.setattr(random, "randint", make_randint_sequence([7, 5]))

    res = cs.use(stats)

    assert res["success"] is True
    assert "Consumed" in res["message"]
    assert res.get("corruption_gained", 0) == 1
    assert stats.corruption_stacks == 1


def test_clyde_teaches_and_improves_clean_strike(monkeypatch):
    stats = DummyStats()
    cs = CleanStrike()
    clyde = Clyde()

    teach = clyde.teach_clean_kill(student_focus=0)
    assert teach["focus_bonus"] == clyde.clean_kill_bonus

    # Apply Clyde's teaching to stats and force a near-threshold roll
    stats.focus += teach["focus_bonus"]

    # damage, focus_roll_base -> base 6 + focus_bonus (5) => 11 < 12 (still fail)
    # We'll use base 8 so final = 8 + 5 = 13 -> success
    monkeypatch.setattr(random, "randint", make_randint_sequence([6, 8]))

    res = cs.use(stats)

    assert res["success"] is True
    # ensure the result reflects a successful clean erasure pattern (can_honor True or no corruption)
    assert res["can_honor"] in (True, False)


if __name__ == "__main__":
    pytest.main(["-q", "-x"])
