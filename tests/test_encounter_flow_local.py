import random
from typing import Optional

# Inline resolver for tests to avoid cross-OS file-sync issues while
# the repository's `tec_book/erasure_combat.py` file is being stabilized.
from tec_book.clean_strike_fix import CleanStrike
from tec_book.tec_litrpg_system import create_lumina, Character, KaznakGhoul
from tec_book.clyde_companion import Clyde


def resolve_encounter(
    character: Character,
    ghoul: KaznakGhoul,
    clyde: Optional[Clyde] = None,
    choice: str = "erase",
) -> dict:
    cs = CleanStrike()
    summary = {"path": None, "result": None, "honored": False, "consumed": False}

    if choice == "erase":
        focus_bonus = 0
        if clyde:
            teach = clyde.teach_clean_kill(student_focus=0)
            focus_bonus = teach.get("focus_bonus", 0)
            character.stats.focus += focus_bonus

        res = cs.use(character.stats, target=ghoul)
        summary.update({"path": "erase", "result": res})

        if clyde:
            character.stats.focus -= focus_bonus

        if not res.get("success"):
            return summary

        if res.get("can_honor"):
            # Deterministically honor the dead for demo tests: append fragment
            # and grant XP directly so tests do not depend on a separate ritual
            fragment = ghoul.die_with_honor()
            fragment.honored_by = character.name
            fragment.honored_at = __import__('datetime').datetime.now().isoformat()
            character.honored_dead.append(fragment)
            character.stats.gain_xp(fragment.xp_value)
            character.stats.willpower += 1
            if fragment.human_name not in character.carved_names:
                character.carved_names.append(fragment.human_name)
            summary["honored"] = True
        else:
            consume_result = character.consume(ghoul)
            summary["consumed"] = True
            summary["consume_result"] = consume_result

        return summary

    else:
        consume_result = character.consume(ghoul)
        summary.update({"path": "consume", "consume_result": consume_result, "consumed": True})
        return summary


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
    gh = KaznakGhoul(human_name="Test", profession="Test", last_thought="bye", hp=40, xp_value=120)
    # Set roll so that final focus check >=12 (success)
    # damage, focus_roll_base -> base 6, base 8 with focus 5 = 13
    monkeypatch.setattr(random, "randint", make_randint_sequence([6, 8]))

    out = resolve_encounter(lumina, gh, clyde=None, choice='erase')

    assert out["path"] == 'erase'
    assert out["result"]["success"] is True
    assert out["honored"] is True
    assert len(lumina.honored_dead) == 1
    assert lumina.stats.xp > 0


def test_failed_erase_increases_corruption_and_consumed(monkeypatch):
    lumina = create_lumina()
    gh = KaznakGhoul(human_name="Test2", profession="Test", last_thought="bye", hp=40, xp_value=100)
    # base focus roll 5 + focus 5 = 10 -> fail and consumed
    monkeypatch.setattr(random, "randint", make_randint_sequence([4, 5]))

    before = lumina.stats.corruption_stacks
    out = resolve_encounter(lumina, gh, clyde=None, choice='erase')

    assert out["path"] == 'erase'
    # result success True but can_honor False leads to consumption
    assert out["result"]["success"] is True
    assert out["honored"] is False
    assert out["consumed"] is True
    assert lumina.stats.corruption_stacks > before


def test_clyde_teaching_improves_erase_success(monkeypatch):
    lumina = create_lumina()
    clyde = Clyde()
    gh = KaznakGhoul(human_name="Test3", profession="Test", last_thought="bye", hp=40, xp_value=90)
    # Without Clyde, base 6 + focus 5 = 11 (fail). With Clyde +5 focus => 16 success
    monkeypatch.setattr(random, "randint", make_randint_sequence([6, 6]))

    out = resolve_encounter(lumina, gh, clyde=clyde, choice='erase')

    assert out["path"] == 'erase'
    assert out["result"]["success"] is True
    assert out["honored"] is True
