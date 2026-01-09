import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import random

from tec_book.clyde_companion import Clyde
from tec_book.erasure_combat import resolve_encounter
from tec_book.tec_litrpg_system import KaznakGhoul, create_lumina


def make_randint_sequence(seq):
    it = iter(seq)

    def _randint(a, b):
        try:
            return next(it)
        except StopIteration:
            return a

    return _randint


def test_erase_honors_and_grants_xp(monkeypatch):
    lumina = create_lumina()
    gh = KaznakGhoul(
        human_name="Test", profession="Test", last_thought="bye", hp=40, xp_value=120,
    )
    # Set roll so that final focus check >=12 (success)
    # damage, focus_roll_base -> base 6, base 8 with focus 5 = 13
    monkeypatch.setattr(random, "randint", make_randint_sequence([6, 8]))

    out = resolve_encounter(lumina, gh, clyde=None, choice="erase")

    assert out["path"] == "erase"
    assert out["result"]["success"] is True
    assert out["honored"] is True
    assert len(lumina.honored_dead) == 1
    assert lumina.stats.xp > 0


def test_failed_erase_increases_corruption_and_consumed(monkeypatch):
    lumina = create_lumina()
    gh = KaznakGhoul(
        human_name="Test2", profession="Test", last_thought="bye", hp=40, xp_value=100,
    )
    # base focus roll 5 + focus 5 = 10 -> fail and consumed
    monkeypatch.setattr(random, "randint", make_randint_sequence([4, 5]))

    before = lumina.stats.corruption_stacks
    out = resolve_encounter(lumina, gh, clyde=None, choice="erase")

    assert out["path"] == "erase"
    # result success True but can_honor False leads to consumption
    assert out["result"]["success"] is True
    assert out["honored"] is False
    assert out["consumed"] is True
    assert lumina.stats.corruption_stacks > before


def test_clyde_teaching_improves_erase_success(monkeypatch):
    lumina = create_lumina()
    clyde = Clyde()
    gh = KaznakGhoul(
        human_name="Test3", profession="Test", last_thought="bye", hp=40, xp_value=90,
    )
    # Without Clyde, base 6 + focus 5 = 11 (fail). With Clyde +5 focus => 16 success
    monkeypatch.setattr(random, "randint", make_randint_sequence([6, 6]))

    out = resolve_encounter(lumina, gh, clyde=clyde, choice="erase")

    assert out["path"] == "erase"
    assert out["result"]["success"] is True
    assert out["honored"] is True
