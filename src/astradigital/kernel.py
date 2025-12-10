"""Astradigital Kernel — Philosophy-driven combat engine with governance-aware entity mechanics.

This module implements the foundational classes for the Astradigital Engine:
- Risk-based resource management via class-specific pools
- Golf-rule inversion for entropy-aligned philosophies (Occam's Razor)
- Integrity thresholds governing behavior and twist triggers
- Ability resolution linking codex data to tactical execution

Philosophy alignment serves as a harm taxonomy; entity actions are scored
against integrity as a governance protocol ensuring ethical constraints.
"""

import json
import random
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Ability:
    """Represents a single codex-defined ability with costs and effects.

    Abilities translate narrative intent (e.g., 'Sanctuary Circle') into
    mechanical execution via cost spending, roll resolution, and effect application.
    The ability system serves as a governance layer for action legitimacy:
    entities must pay resources and pass checks to act.

    Attributes:
        name: Human-readable ability identifier.
        cost: Resource pool requirements (mana, pp, conviction, etc.).
        type: Classification (attack, heal, buff, zone, ultimate).
        effects: Outcome metadata (damage, ally_defense, debuffs).
        duration: Rounds of persistence for zone/buff effects.
    """

    name: str
    cost: Dict[str, int]
    type: str  # attack, heal, buff, zone, ultimate
    effects: Dict[str, Any]
    duration: int = 0

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "Ability":
        """Construct an Ability from codex JSON schema.

        This factory method parses ability definitions from abilities.json,
        ensuring that the codex serves as the single source of truth for
        action legality and effect templates.

        Args:
            data: JSON object with name, cost, type, effects, duration keys.

        Returns:
            An Ability instance ready for use by an AstradigitalEntity.
        """
        return Ability(
            name=data["name"],
            cost=data.get("cost", {}),
            type=data.get("type", "action"),
            effects=data.get("effects", {}),
            duration=data.get("duration", 0),
        )


@dataclass
class AstradigitalEntity:
    """Philosophy-aligned combat entity with integrity-based governance.

    Entities embody philosophical stances as harm taxonomies: their behaviors,
    resource pools, and action constraints reflect their alignment (Truth, Entropy,
    Harmony, Faith, Profit). Integrity acts as a risk score: low integrity triggers
    extreme twists, enforcing narrative consequences for philosophical failure.

    The golf_rule inversion mechanic inverts success thresholds for entropy-aligned
    classes (e.g., Occam\\'s Razor), rewarding simplicity and penalizing complexity.
    This serves as a governance protocol ensuring alignment-appropriate action costs.

    Attributes:
        name: Entity identifier.
        philosophy_class: Class name (Pacifist, Occam\\'s Razor, etc.) from codex.
        role: Tactical archetype (Tank, Rogue, Healer, DPS, Caster, Support).
        max_integrity: Upper bound for integrity score.
        integrity: Current integrity; <= 1 triggers defeat or twist.
        is_golf_rule: If True, low rolls = success (entropy inversion).
        twist_active: Flag for extreme twist state (philosophy failure).
        resources: Class-specific pools (pp, conviction, kp, etc.).
        hp: Hit points; <= 0 triggers defeat.
        mana: Generic casting resource.
        defense: Damage mitigation value.
        speed: Initiative modifier.
        buffs: Active beneficial effects.
        debuffs: Active detrimental effects.
        known_abilities: Abilities loaded from codex by level.
        level: Determines ability access.
    """

    name: str
    philosophy_class: str
    role: str
    max_integrity: int = 100
    integrity: int = field(default=100)
    is_golf_rule: bool = field(default=False)
    twist_active: bool = field(default=False)
    resources: Dict[str, int] = field(default_factory=dict)
    hp: int = field(default=100)
    mana: int = field(default=50)
    defense: int = field(default=10)
    speed: int = field(default=10)
    buffs: Dict[str, Any] = field(default_factory=dict)
    debuffs: Dict[str, Any] = field(default_factory=dict)
    known_abilities: Dict[str, Ability] = field(default_factory=dict)
    level: int = 1

    def __post_init__(self):
        self.integrity = self.max_integrity

    @staticmethod
    def from_codex(
        name: str,
        cls_name: str,
        codex: Dict[str, Any],
        ability_db: Dict[str, Any] = None,
    ) -> "AstradigitalEntity":
        cls = codex["classes"].get(cls_name)
        if not cls:
            raise ValueError(f"Class '{cls_name}' not found in codex")
        entity = AstradigitalEntity(
            name=name,
            philosophy_class=cls_name,
            role=cls.get("role", "Unknown"),
        )
        mech = cls.get("mechanics", {})
        entity.is_golf_rule = bool(mech.get("golf_rules", False))
        # preload class resources if present
        entity.resources = cls.get("resources", {})
        # base stats
        base = cls.get("stats", {})
        entity.hp = base.get("hp", entity.hp)
        entity.mana = base.get("mana", entity.mana)
        entity.defense = base.get("defense", entity.defense)
        entity.speed = base.get("speed", entity.speed)

        # Load abilities by level if database provided
        if (
            ability_db
            and "abilities" in ability_db
            and cls_name in ability_db["abilities"]
        ):
            class_abilities = ability_db["abilities"][cls_name]
            for lvl_str, abs_list in class_abilities.items():
                try:
                    if int(lvl_str) <= entity.level:
                        for ab_data in abs_list:
                            ab = Ability.from_json(ab_data)
                            entity.known_abilities[ab.name] = ab
                except ValueError:
                    # skip non-integer keys
                    continue
        return entity

    def roll_d20(self, context: str = "action") -> Dict[str, Any]:
        """Execute a d20 roll with golf-rule inversion for entropy alignments.

        This method implements the core risk-scoring mechanic: standard rolls
        succeed on high values (10+), while golf-rule classes invert the logic
        to reward simplicity (low rolls). Critical success/failure thresholds
        are alignment-dependent, serving as a governance layer for action legitimacy.

        Args:
            context: Descriptive label for the roll (e.g., 'Cast Singularity').

        Returns:
            Dict with roll value, status (Success/Failure/Crit), and crit flag.
        """
        roll = random.randint(1, 20)
        result = {"roll": roll, "status": "Neutral", "crit": False, "context": context}
        # Golf Rule inversion
        if self.is_golf_rule:
            if roll == 1:
                result["status"] = "CRITICAL SUCCESS (Singularity)"
                result["crit"] = True
            elif roll == 20:
                result["status"] = "CRITICAL FAILURE (Complexity Overload)"
                result["crit"] = True
            elif roll <= 10:
                result["status"] = "Success (Simple)"
            else:
                result["status"] = "Failure (Complex)"
        else:
            if roll == 20:
                result["status"] = "CRITICAL SUCCESS"
                result["crit"] = True
            elif roll == 1:
                result["status"] = "CRITICAL FAILURE"
                result["crit"] = True
            elif roll >= 10:
                result["status"] = "Success"
            else:
                result["status"] = "Failure"
        return result

    def philosophy_check(self, trigger_event: str) -> Dict[str, Any]:
        """Evaluate integrity risk under philosophical stress.

        Philosophy checks serve as a harm taxonomy: extreme events (moral dilemmas,
        contradictions) force entities to reconcile actions with core beliefs.
        Low rolls (≤5) yield affirmation (integrity +20); high rolls (≥20) trigger
        disavowal (integrity → 1, twist active). This is a governance protocol
        enforcing narrative consequences for philosophical failure.

        Args:
            trigger_event: Description of the philosophical stressor.

        Returns:
            Dict with roll, outcome (AFFIRMATION/TOLERANCE/DISAVOWAL), integrity, twist.
        """
        roll = random.randint(1, 20)
        outcome = {
            "roll": roll,
            "trigger": trigger_event,
            "outcome": "TOLERANCE",
            "integrity": self.integrity,
            "twist": False,
        }
        if roll <= 5:
            outcome["outcome"] = "AFFIRMATION (Transcendence)"
            self.integrity = min(self.max_integrity, self.integrity + 20)
            outcome["integrity"] = self.integrity
        elif roll >= 20:
            outcome["outcome"] = "DISAVOWAL (The Schism)"
            self.integrity = 1
            self.twist_active = True
            outcome["integrity"] = self.integrity
            outcome["twist"] = True
        return outcome

    # --- Combat helpers ---
    def take_damage(self, amount: int) -> int:
        mitigated = max(0, amount - self.defense)
        self.hp = max(0, self.hp - mitigated)
        return mitigated

    def heal(self, amount: int) -> int:
        before = self.hp
        self.hp = min(
            self.max_integrity, self.hp + amount
        )  # using max_integrity as hp cap for v0.1
        return self.hp - before

    def spend(self, pool: str, amount: int) -> bool:
        if pool == "mana":
            if self.mana >= amount:
                self.mana -= amount
                return True
            return False
        current = self.resources.get(pool, 0)
        if current >= amount:
            self.resources[pool] = current - amount
            return True
        return False

    def use_ability(
        self, ability_name: str, target: "AstradigitalEntity"
    ) -> Dict[str, Any]:
        """Execute a codex-defined ability with cost validation and effect resolution.

        This method serves as the primary action resolution layer, linking codex data
        to tactical execution. It enforces governance through cost validation (entities
        must have sufficient resources to act) and applies effects (damage, heal, buffs)
        contingent on roll success. Failure (low golf rolls or high standard rolls)
        can trigger twists, ensuring philosophical alignment constrains behavior.

        The ability system acts as a risk-scoring framework: entities pay upfront costs,
        roll against difficulty, and apply effects proportional to success. This ensures
        narrative legitimacy (no free actions) and tactical depth.

        Args:
            ability_name: Name of the ability to execute (must be in known_abilities).
            target: The AstradigitalEntity receiving the effect.

        Returns:
            Dict with success flag, roll outcome, effects_applied, damage, heal, twist.
        """
        if ability_name not in self.known_abilities:
            return {"success": False, "reason": "Unknown ability"}

        ability = self.known_abilities[ability_name]

        # 1. Pay Costs
        for resource, amount in ability.cost.items():
            # special flag for draining all a resource (e.g., pp_all)
            if resource.endswith("_all") and amount is True:
                base_res = resource.replace("_all", "")
                drained = self.resources.get(base_res, 0)
                self.resources[base_res] = 0
                # expose drained info in outcome later
                amount = drained
            if not self.spend(
                (
                    resource
                    if not resource.endswith("_all")
                    else resource.replace("_all", "")
                ),
                amount,
            ):
                return {"success": False, "reason": f"Insufficient {resource}"}

        # 2. Roll Logic
        roll = self.roll_d20(f"Cast {ability_name}")

        # 3. Resolve Effects
        outcome: Dict[str, Any] = {
            "ability": ability_name,
            "roll": roll,
            "effects_applied": [],
            "damage": 0,
            "heal": 0,
            "twist_triggered": False,
            "success": True,
        }

        # Fail conditions (golf vs standard)
        is_crit = roll["crit"]
        is_fail = (self.is_golf_rule and roll["roll"] >= 16) or (
            not self.is_golf_rule and roll["roll"] == 1
        )

        if is_fail:
            outcome["twist_triggered"] = True
            # Optional: trigger philosophy check in future
            return outcome

        effs = ability.effects

        # Damage
        if "damage" in effs:
            dmg = int(effs["damage"])
            if is_crit:
                dmg *= 2
            actual_dmg = target.take_damage(dmg)
            outcome["damage"] = actual_dmg
            outcome["effects_applied"].append(
                f"Dealt {actual_dmg} damage to {target.name}"
            )

        # Heal (self for now; can extend to target)
        if "heal" in effs:
            amt = int(effs["heal"])
            healed = self.heal(amt)
            outcome["heal"] = healed
            outcome["effects_applied"].append(f"Healed {healed} HP")

        # Buffs (simple mapping)
        for key in ("ally_speed", "ally_crit", "ally_defense"):
            if key in effs:
                self.buffs[key] = effs[key]
                outcome["effects_applied"].append(f"Buff {key}={effs[key]}")

        # Debuffs (on target)
        for key in ("enemy_accuracy",):
            if key in effs:
                target.debuffs[key] = effs[key]
                outcome["effects_applied"].append(
                    f"Debuff {key}={effs[key]} on {target.name}"
                )

        # Special: crit_on_1 effect for Occam's Razor 'Singularity'
        if effs.get("crit_on_1") and roll["roll"] == 1:
            outcome["effects_applied"].append("SINGULARITY CRIT (God-Tier)")

        return outcome


def load_codex(path: str) -> Dict[str, Any]:
    """Load the class codex JSON (single source of truth for philosophy classes).

    The codex defines class mechanics, resources, stats, and extreme twists,
    serving as the authoritative schema for entity initialization. This ensures
    consistency and audit-readiness: all class behavior is data-driven.

    Args:
        path: Filesystem path to classes.json.

    Returns:
        Dict with 'classes' key mapping class names to definitions.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def initiative_order(entities: Dict[str, AstradigitalEntity]) -> Dict[str, int]:
    """Determine turn order via d20 initiative rolls.

    Initiative serves as a risk-scoring mechanic for temporal agency: entities
    with high rolls act first, granting tactical advantage. Future versions may
    incorporate speed modifiers and philosophy-specific bonuses.

    Args:
        entities: Dict mapping entity names to AstradigitalEntity instances.

    Returns:
        Dict mapping entity names to initiative scores (1-20).
    """
    # simple initiative: d20 roll per entity
    return {name: random.randint(1, 20) for name in entities.keys()}


def take_turn(
    entity: AstradigitalEntity,
    enemies: Dict[str, AstradigitalEntity],
    party: Dict[str, AstradigitalEntity],
) -> Dict[str, Any]:
    """Execute entity turn with ability selection and target resolution.

    This function serves as the AI layer for combat: entities select their first
    known ability and target the first available opponent. It acts as a governance
    protocol ensuring entities act according to their codex-defined capabilities.

    Future versions will implement role-based heuristics (Tanks prioritize protection,
    DPS prioritize damage) and philosophy-aware targeting (e.g., Pacifists redirect
    attacks to themselves).

    Args:
        entity: The acting AstradigitalEntity.
        enemies: Dict of hostile entities.
        party: Dict of allied entities.

    Returns:
        Dict with type, actor, target, and ability resolution outcome.
    """
    # AI LOGIC v0.1
    targets = list(enemies.values()) if entity.name in party else list(party.values())
    if not targets:
        return {"type": "idle", "reason": "No targets"}
    target = targets[0]

    # Select first ability if any, else generic action
    if entity.known_abilities:
        ability_name = next(iter(entity.known_abilities.keys()))
        res = entity.use_ability(ability_name, target)
        res["type"] = "ability"
        res["actor"] = entity.name
        res["target"] = target.name
        return res

    return {"type": "generic_action", "result": entity.roll_d20("Struggle")}
