"""
Fixed CleanStrike ability that matches demo expectations
"""

import random
from dataclasses import dataclass


@dataclass
class CleanStrike:
    """VoidMancer Erasure ability - Clyde's signature technique"""

    name: str = "Clean Strike"
    cost: dict = None
    description: str = "Erase target without blood or fallout"

    def __post_init__(self):
        if self.cost is None:
            self.cost = {"void_charge": 10, "focus": 5}

    def can_use(self, stats) -> bool:
        """Check if character has resources"""
        return (
            stats.void_charge >= self.cost["void_charge"]
            and stats.focus >= self.cost["focus"]
        )

    def use(self, stats, target=None):
        """Execute ability and apply costs"""
        if not self.can_use(stats):
            return {
                "success": False,
                "message": "Insufficient resources!",
                "damage": 0,
                "can_honor": False,
            }

        # Apply costs
        stats.void_charge -= self.cost["void_charge"]

        return self._effect(stats, target)

    def _effect(self, stats, target=None):
        """Core mechanic: Clean kill check"""
        # Roll for damage
        damage = random.randint(1, 20) + (stats.void_charge // 10)

        # Focus check for clean kill (DC 12)
        focus_roll = random.randint(1, 20) + stats.focus

        # Critical failure (1) - contaminated kill
        if focus_roll == 1:
            stats.corruption_stacks += 2
            return {
                "success": True,
                "message": "CRITICAL FAILURE! Messy kill. Ichor everywhere.",
                "damage": damage // 2,  # Reduced damage
                "can_honor": False,
                "corruption_gained": 2,
            }

        # Critical success (20) - perfect erasure
        if focus_roll == 20:
            return {
                "success": True,
                "message": "CRITICAL SUCCESS! Perfect molecular dissolution.",
                "damage": damage * 2,  # Bonus damage
                "can_honor": True,
                "bonus_xp": True,  # Flag for honoring ritual
            }

        # Failed clean kill - consumption instead
        if focus_roll < 12:
            stats.corruption_stacks += 1
            return {
                "success": True,
                "message": "Consumed instead of erased! The hunger took over.",
                "damage": damage,
                "can_honor": False,
                "corruption_gained": 1,
            }

        # Successful clean kill
        return {
            "success": True,
            "message": "Clean erasure. No blood. No contamination.",
            "damage": damage,
            "can_honor": True,
        }


# Example usage
if __name__ == "__main__":
    from types import SimpleNamespace

    # Mock stats
    stats = SimpleNamespace(void_charge=50, focus=10, corruption_stacks=0)

    ability = CleanStrike()

    # Test 5 strikes
    print("=== TESTING CLEAN STRIKE ===\n")
    for i in range(5):
        result = ability.use(stats, target=None)
        print(f"Strike {i+1}:")
        print(f"  Message: {result['message']}")
        print(f"  Damage: {result['damage']}")
        print(f"  Can Honor: {result['can_honor']}")
        print(f"  Corruption: {stats.corruption_stacks}")
        print()
