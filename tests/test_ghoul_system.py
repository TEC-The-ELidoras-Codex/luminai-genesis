"""
TEC Unit Tests - Verify core mechanics
"""

import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tec_book"))

from ghoul_db import GhoulGenerator, GhoulDatabase
from tec_litrpg_system import create_lumina, KaznakGhoul

def test_ghoul_generator():
    """Test Ghoul generation"""
    gen = GhoulGenerator(seed=123)
    ghouls = gen.generate_batch(5, tier_range=(1, 2))
    
    assert len(ghouls) == 5
    assert all(g.hp >= 60 for g in ghouls)
    assert all(g.human_name for g in ghouls)
    print("✅ Ghoul generation test passed")

def test_erasure_mechanics():
    """Test honor system"""
    lumina = create_lumina()
    tim = KaznakGhoul(
        human_name="Timothy Sol Weeran",
        profession="Child (age 7)",
        last_thought="bye mister",
        loved_ones=["His mother"],
        hp=40,
        xp_value=150
    )
    
    fragment = tim.die_with_honor()
    prev_will = lumina.stats.willpower
    lumina.honor_the_dead(fragment)
    
    assert fragment.human_name in lumina.carved_names
    assert len(lumina.honored_dead) == 1
    assert lumina.stats.willpower >= prev_will
    print("✅ Erasure mechanics test passed")

def test_consumption_mechanics():
    """Test consumption system"""
    lumina = create_lumina()
    initial_corruption = lumina.stats.corruption_stacks
    
    tim = KaznakGhoul(
        human_name="Test Victim",
        profession="Worker",
        last_thought="...",
        hp=40,
        xp_value=100
    )
    
    lumina.consume(tim)
    
    assert lumina.stats.corruption_stacks > initial_corruption
    assert lumina.stats.void_charge > 0
    print("✅ Consumption mechanics test passed")

if __name__ == "__main__":
    test_ghoul_generator()
    test_erasure_mechanics()
    test_consumption_mechanics()
    print("\n🎉 All tests passed!")
