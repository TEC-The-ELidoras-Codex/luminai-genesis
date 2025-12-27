"""
TEC Ghoul Database - Procedural Generation
Generates story-consistent Kaznak Ghouls with human backstories
"""

import random
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime

# Name pools (Crossroads workers, Eldora refugees)
FIRST_NAMES = [
    "Marcus", "Elara", "Zane", "Lena", "Timothy", "Aria", "Joss", 
    "Maya", "Polkin", "Raj", "Sela", "Thane", "Kess", "Merrick",
    "Sol", "Torres", "Patel", "Fost", "Rishall", "Weeran"
]

LAST_NAMES = [
    "Thane", "Kess", "Merrick", "Torres", "Patel", "Fost", "Sol",
    "Rishall", "Weeran", "Drake", "Chen", "Okafor", "Novak", 
    "Singh", "Martinez", "Kim", "Adeyemi", "Kowalski"
]

# Crossroads professions (reflects undercity labor)
PROFESSIONS = [
    "Maintenance Tech, Sublevel 4",
    "Power Grid Monitor",
    "Circuit Splicer",
    "Child (age 7)",
    "Child (age 9)", 
    "Child (age 12)",
    "Food Service Worker",
    "Data Recovery Specialist",
    "Conduit Repair Crew",
    "Emergency Medical Tech",
    "School Teacher",
    "Shop Owner",
    "Transit Operator",
    "Waste Recycler"
]

# Last thoughts (moments before transformation)
LAST_THOUGHTS = [
    "I was just trying to fix the lights...",
    "My shift ends in an hour...",
    "bye mister",
    "Did I remember to call home?",
    "The power spike wasn't my fault",
    "Please, I have kids waiting",
    "Why is it so cold?",
    "I should have listened",
    "Not now, not like this",
    "The throttle hit too hard",
    "Someone will remember me, right?"
]

# Relationship pools (loved ones left behind)
RELATIONSHIPS = [
    "His daughter Aria",
    "His son Marcus", 
    "Her partner Joss",
    "Her mother Elena",
    "His teacher Mrs. Kell",
    "Their children (2)",
    "The neighborhood kids",
    "His coworkers",
    "Her study group",
    "His brother Zane"
]

@dataclass
class GhoulRecord:
    """Complete record of a person who became a Ghoul"""
    id: str
    human_name: str
    profession: str
    last_thought: str
    loved_ones: List[str]
    hp: int
    void_damage: int
    xp_value: int
    created_at: str
    location: str = "Crossroads, Sublevel Unknown"
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class GhoulGenerator:
    """Generates procedural Ghouls with consistent lore"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        self.generated_count = 0
        
    def generate_one(self, tier: int = 1) -> GhoulRecord:
        """Generate a single Ghoul
        
        Args:
            tier: Difficulty tier (1-5) affects HP/damage/XP
        """
        self.generated_count += 1
        
        # Generate identity
        first = self.rng.choice(FIRST_NAMES)
        last = self.rng.choice(LAST_NAMES)
        human_name = f"{first} {last}"
        
        profession = self.rng.choice(PROFESSIONS)
        last_thought = self.rng.choice(LAST_THOUGHTS)
        
        # Generate loved ones (0-4, weighted toward connections)
        num_loved = self.rng.choices([0, 1, 2, 3, 4], weights=[1, 3, 4, 2, 1])[0]
        loved_ones = self.rng.sample(RELATIONSHIPS, min(num_loved, len(RELATIONSHIPS)))
        
        # Scale stats by tier
        hp = 60 + (tier * 20)
        void_damage = self.rng.randint(2 * tier, 10 * tier)
        
        # XP value: base + bonus for connections
        xp_value = (80 * tier) + (len(loved_ones) * 15)
        
        return GhoulRecord(
            id=f"ghoul_{self.generated_count:04d}",
            human_name=human_name,
            profession=profession,
            last_thought=last_thought,
            loved_ones=loved_ones,
            hp=hp,
            void_damage=void_damage,
            xp_value=xp_value,
            created_at=datetime.now().isoformat(),
            location="Crossroads, Sublevel Unknown"
        )
    
    def generate_batch(self, count: int, tier_range: tuple = (1, 3)) -> List[GhoulRecord]:
        """Generate multiple Ghouls"""
        return [
            self.generate_one(tier=self.rng.randint(*tier_range))
            for _ in range(count)
        ]

class GhoulDatabase:
    """Persistent storage for generated Ghouls"""
    
    def __init__(self, db_path: Path = Path("data/ghouls.json")):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ghouls: List[GhoulRecord] = []
        self.load()
    
    def load(self):
        """Load from JSON"""
        if self.db_path.exists():
            with open(self.db_path, 'r') as f:
                data = json.load(f)
                self.ghouls = [GhoulRecord.from_dict(g) for g in data]
    
    def save(self):
        """Save to JSON"""
        with open(self.db_path, 'w') as f:
            json.dump([g.to_dict() for g in self.ghouls], f, indent=2)
    
    def add_batch(self, ghouls: List[GhoulRecord]):
        """Add multiple Ghouls"""
        self.ghouls.extend(ghouls)
        self.save()
    
    def get_random(self, tier: Optional[int] = None) -> Optional[GhoulRecord]:
        """Get a random Ghoul, optionally filtered by tier"""
        candidates = self.ghouls
        if tier:
            candidates = [g for g in self.ghouls if g.hp // 20 - 3 == tier]
        return random.choice(candidates) if candidates else None

def create_canonical_ghouls() -> List[GhoulRecord]:
    """Generate the named Ghouls from TEC chapters"""
    
    timothy = GhoulRecord(
        id="ghoul_timothy_sol_weeran",
        human_name="Timothy Sol Weeran",
        profession="Child (age 7)",
        last_thought="bye mister",
        loved_ones=["His mother", "His teacher Mrs. Kell"],
        hp=40,
        void_damage=8,
        xp_value=150,
        created_at="2174-03-12T07:13:00",
        location="Crossroads, Junction 4-B"
    )
    
    marcus = GhoulRecord(
        id="ghoul_marcus_thane",
        human_name="Marcus Thane",
        profession="Maintenance Tech, Sublevel 4",
        last_thought="I was just trying to fix the lights...",
        loved_ones=["His daughter Aria", "His partner Joss"],
        hp=80,
        void_damage=15,
        xp_value=130,
        created_at="2174-03-12T06:45:00",
        location="Crossroads, Maintenance Sublevel 4"
    )
    
    return [timothy, marcus]

if __name__ == "__main__":
    print("=== TEC GHOUL DATABASE INITIALIZATION ===\n")
    
    # Initialize database
    db = GhoulDatabase()
    
    # Add canonical ghouls
    canonical = create_canonical_ghouls()
    db.add_batch(canonical)
    print(f"✅ Added {len(canonical)} canonical Ghouls")
    
    # Generate procedural ghouls
    generator = GhoulGenerator(seed=42)
    procedural = generator.generate_batch(count=20, tier_range=(1, 3))
    db.add_batch(procedural)
    print(f"✅ Generated {len(procedural)} procedural Ghouls")
    
    # Display stats
    print(f"\n📊 Database Stats:")
    print(f"  Total Ghouls: {len(db.ghouls)}")
    print(f"  Average XP: {sum(g.xp_value for g in db.ghouls) // len(db.ghouls)}")
    
    print(f"\n💾 Saved to: {db.db_path}")
