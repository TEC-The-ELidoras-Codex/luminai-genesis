from src.astradigital.kernel import Ability, AstradigitalEntity


def make_entity(name: str) -> AstradigitalEntity:
    e = AstradigitalEntity(name=name, philosophy_class="Test", role="Tester")
    e.resources = {}
    e.hp = 100
    e.max_integrity = 100
    return e


def test_use_ability_insufficient_resource():
    a = make_entity("attacker")
    target = make_entity("target")
    ability = Ability(name="Drain", cost={"pp": 5}, type="attack", effects={})
    a.known_abilities[ability.name] = ability

    res = a.use_ability(ability.name, target)
    assert res["success"] is False
    assert "Insufficient" in res["reason"]


def test_use_ability_damage_and_heal_and_crit():
    a = make_entity("attacker")
    target = make_entity("target")
    # give resource so cost passes
    a.resources["pp"] = 10
    ability = Ability(
        name="Smite", cost={"pp": 5}, type="attack", effects={"damage": 5, "heal": 3},
    )
    a.known_abilities[ability.name] = ability

    # deterministic roll: not a fail, non-crit
    a.roll_d20 = lambda context=None: {"roll": 10, "crit": False, "context": context}

    res = a.use_ability(ability.name, target)
    assert res["success"] is True
    assert res["damage"] >= 0
    assert res["heal"] >= 0


def test_use_ability_singularity_crit_on_1():
    a = make_entity("attacker")
    target = make_entity("target")
    a.resources["pp"] = 10
    ability = Ability(
        name="Singularity",
        cost={"pp": 1},
        type="attack",
        effects={"damage": 2, "crit_on_1": True},
    )
    a.known_abilities[ability.name] = ability

    # make roll be 1 and set golf-rule so 1 is a success
    a.is_golf_rule = True
    a.roll_d20 = lambda context=None: {"roll": 1, "crit": False, "context": context}

    res = a.use_ability(ability.name, target)
    assert any("SINGULARITY CRIT" in s for s in res["effects_applied"])
