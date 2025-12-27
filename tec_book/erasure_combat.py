"""Programmatic encounter resolution for the demo and tests.

This module provides `resolve_encounter` which runs a single dead-ghoul
choice (erase/consume) and returns a structured result for assertions
and CLI printing.
"""


from tec_book.clean_strike_fix import CleanStrike
from tec_book.clyde_companion import Clyde
from tec_book.tec_litrpg_system import Character, KaznakGhoul


def resolve_encounter(
    character: Character,
    ghoul: KaznakGhoul,
    clyde: Clyde | None = None,
    choice: str = "erase",
) -> dict:
    """Resolve an encounter programmatically.

    Args:
        character: Character performing the action
        ghoul: KaznakGhoul that was killed
        clyde: Optional Clyde companion to influence focus
        choice: 'erase' or 'consume'

    Returns:
        dict with keys: path, result, honored, consumed, consume_result
    """
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
            fragment = ghoul.die_with_honor()
            # Perform an automatic honor for the demo (deterministic, tests expect
            # a successful honor when CleanStrike indicates `can_honor`).
            fragment.honored_by = character.name
            from datetime import datetime

            fragment.honored_at = datetime.now().isoformat()
            character.honored_dead.append(fragment)
            # Grant XP directly (simple, deterministic award for demo)
            character.stats.gain_xp(fragment.xp_value)
            # Small willpower gain and carve the name for demo/visibility
            character.stats.willpower += 1
            if fragment.human_name not in character.carved_names:
                character.carved_names.append(fragment.human_name)
            summary["honored"] = True
        else:
            consume_result = character.consume(ghoul)
            summary["consumed"] = True
            summary["consume_result"] = consume_result

        return summary

    consume_result = character.consume(ghoul)
    summary.update(
        {"path": "consume", "consume_result": consume_result, "consumed": True},
    )
    return summary
