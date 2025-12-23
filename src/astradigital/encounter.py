"""Astradigital Encounter System — Governance-aware battle orchestration.

This module implements the encounter loop for philosophy-driven combat,
managing party/enemy initialization, turn order, and defeat conditions.
Encounters serve as tactical scenarios for testing integrity-based governance:
entities must navigate resource constraints and philosophy checks under stress.

The encounter system acts as a risk-scoring framework: initiative determines
temporal agency, ability costs enforce resource discipline, and integrity
thresholds trigger narrative consequences (twists, defeats).
"""

import json
import logging
from pathlib import Path
from typing import Any

from .kernel import AstradigitalEntity, initiative_order, load_codex, take_turn

logger = logging.getLogger(__name__)


def load_encounter(path: str) -> dict[str, Any]:
    """Load encounter definition JSON (party, enemies, max_rounds)."""

    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def build_party(
    enc: dict[str, Any],
    codex: dict[str, Any],
    ability_db: dict[str, Any],
) -> dict[str, AstradigitalEntity]:
    """Construct party entities from encounter spec and codex.

    Party members are initialized with class-defined stats, resources, and
    abilities (loaded up to current level). This ensures data-driven consistency
    and audit-readiness: all party behavior originates from the codex schema.

    Args:
        enc: Encounter JSON with 'party' list (name, class).
        codex: Class definitions from classes.json.
        ability_db: Ability definitions from abilities.json.

    Returns:
        Dict mapping party member names to AstradigitalEntity instances.
    """
    party: dict[str, AstradigitalEntity] = {}
    for char in enc.get("party", []):
        entity = AstradigitalEntity.from_codex(
            char["name"],
            char["class"],
            codex,
            ability_db,
        )
        party[entity.name] = entity
    return party


def build_enemies(
    enc: dict[str, Any],
    codex: dict[str, Any],
    ability_db: dict[str, Any],
) -> dict[str, AstradigitalEntity]:
    """Construct enemy entities from encounter spec and codex.

    Enemies follow the same initialization as party members, ensuring symmetric
    governance: they are subject to resource costs, ability limits, and integrity
    thresholds. This creates tactical depth and narrative fairness.

    Args:
        enc: Encounter JSON with 'enemies' list (name, class).
        codex: Class definitions from classes.json.
        ability_db: Ability definitions from abilities.json.

    Returns:
        Dict mapping enemy names to AstradigitalEntity instances.
    """
    enemies: dict[str, AstradigitalEntity] = {}
    for char in enc.get("enemies", []):
        entity = AstradigitalEntity.from_codex(
            char["name"],
            char["class"],
            codex,
            ability_db,
        )
        enemies[entity.name] = entity
    return enemies


def run_battle(encounter_path: Path, codex_path: Path) -> None:
    """Execute a full encounter loop with initiative, turns, and defeat conditions.

    This function orchestrates the battle simulation:
    - Loads encounter spec (party, enemies, max_rounds) and codex/abilities
    - Initializes entities with data-driven stats and abilities
    - Runs rounds with initiative-ordered turns until victory, defeat, or timeout
    - Applies defeat conditions: hp <= 0 or integrity <= 1

    The battle loop serves as a governance stress-test: entities must manage
    resources, navigate philosophy checks, and coordinate tactics under constraint.

    Args:
        encounter_path: Path to encounter JSON file.
        codex_path: Path to classes.json.
    """
    enc = load_encounter(str(encounter_path))
    codex = load_codex(str(codex_path))
    # Load abilities db
    ability_path = encounter_path.parent.parent / "codex" / "abilities.json"
    with ability_path.open(encoding="utf-8") as f:
        ability_db = json.load(f)

    party = build_party(enc, codex, ability_db)
    enemies = build_enemies(enc, codex, ability_db)

    logger.info("Encounter: %s", enc.get("name", "Unknown"))
    round_num = 1

    while party and enemies and round_num <= enc.get("max_rounds", 5):
        logger.info("%s", f"\n=== Round {round_num} ===")
        order = initiative_order({**party, **enemies})
        for name, _init in sorted(order.items(), key=lambda kv: kv[1], reverse=True):
            actor = party.get(name) or enemies.get(name)
            side = "party" if name in party else "enemies"
            outcome = take_turn(actor, enemies, party)
            logger.info("[%s (%s)] -> %s", name, side, outcome)
            # simple end condition: mark enemies with integrity 1 or hp 0 as defeated
            if side == "enemies" and (actor.hp <= 0 or actor.integrity <= 1):
                enemies.pop(name, None)
            if side == "party" and (actor.hp <= 0 or actor.integrity <= 1):
                party.pop(name, None)
        round_num += 1

    logger.info("\nBattle ends.")
