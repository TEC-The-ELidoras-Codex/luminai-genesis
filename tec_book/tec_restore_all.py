#!/usr/bin/env python3
"""
TEC COMPLETE RESTORATION - Windows Edition
Run this ONCE to restore all Python files
"""

from pathlib import Path

def create_file(path: str, content: str):
    """Create file with proper encoding"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    print(f"✅ {path} ({len(content.splitlines())} lines)")

def main():
    print("🔥 TEC COMPLETE RESTORATION\n")
    
    base = Path.cwd()
    print(f"📂 Working in: {base}\n")
    
    # Create directories
    (base / "tec_book" / "data").mkdir(parents=True, exist_ok=True)
    (base / "tests").mkdir(parents=True, exist_ok=True)
    
    print("Creating files...\n")
    
    # ===== 1. GHOUL DATABASE =====
    create_file("tec_book/ghoul_db.py", '''"""
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
    print("=== TEC GHOUL DATABASE INITIALIZATION ===\\n")
    
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
    print(f"\\n📊 Database Stats:")
    print(f"  Total Ghouls: {len(db.ghouls)}")
    print(f"  Average XP: {sum(g.xp_value for g in db.ghouls) // len(db.ghouls)}")
    
    print(f"\\n💾 Saved to: {db.db_path}")
''')
    
    # ===== 2. LITRPG SYSTEM =====
    create_file("tec_book/tec_litrpg_system.py", '''"""
The Elidoras Codex - LITRPG Character System
Erasure vs Consumption mechanics with Archetype system
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import random
from datetime import datetime

class Archetype(Enum):
    """The Four Combat Archetypes"""
    VOIDTOUCHED = "Voidtouched"
    TECHNOMANCER = "Technomancer"
    SPLICER = "Splicer"
    SHADOW_OPERATIVE = "Shadow Operative"

@dataclass
class MemoryFragment:
    """What remains when a Ghoul is cleanly erased"""
    id: str
    human_name: str
    last_thought: str
    profession: Optional[str] = None
    loved_ones: List[str] = field(default_factory=list)
    xp_value: int = 100
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    honored_by: Optional[str] = None
    honored_at: Optional[str] = None
    
    def honor_text(self) -> str:
        """Generate the witnessing text"""
        text = f"╔══ {self.human_name} ══╗\\n"
        if self.profession:
            text += f"Was: {self.profession}\\n"
        text += f'Last thought: "{self.last_thought}"\\n'
        if self.loved_ones:
            text += f"Remembered by: {', '.join(self.loved_ones)}\\n"
        text += f"XP Value: {self.xp_value}"
        return text

@dataclass
class CoreStats:
    """Core stats based on TEC's supranatural physics"""
    void_charge: int = 100
    resonance: int = 100
    physical_integrity: int = 100
    corruption_stacks: int = 0
    willpower: int = 10
    focus: int = 10
    xp: int = 0
    level: int = 1
    
    def apply_corruption(self, amount: int) -> str:
        """Apply corruption from ichor/Queen exposure"""
        self.corruption_stacks += amount
        self.void_charge = max(0, self.void_charge - (amount * 20))
        
        if self.corruption_stacks >= self.willpower:
            return "💀 CRITICAL: Kaznak conversion imminent!"
        elif self.corruption_stacks >= 10:
            return "⚠️  Stage 3 Corruption"
        elif self.corruption_stacks >= 7:
            return "⚠️  Stage 2 Corruption"
        elif self.corruption_stacks >= 5:
            return "⚠️  Stage 1 Corruption: Hear the Queen"
        
        return f"Corruption +{amount} (total: {self.corruption_stacks})"
    
    def check_willpower(self, dc: int) -> tuple[bool, int]:
        """Resist psychic/void-light influence"""
        roll = random.randint(1, 20) + self.willpower
        roll -= (self.corruption_stacks * 2)
        return (roll >= dc, roll)
    
    def gain_xp(self, amount: int) -> str:
        """Add XP and check for level up"""
        self.xp += amount
        xp_needed = self.level * 100
        
        if self.xp >= xp_needed:
            self.level += 1
            self.willpower += 1
            self.void_charge += 20
            return f"🎉 LEVEL UP! Now level {self.level}"
        
        return f"+{amount} XP ({self.xp}/{xp_needed})"

class KaznakGhoul:
    """A person transformed into a despair singularity"""
    
    def __init__(self, human_name: str, profession: str, last_thought: str, 
                 loved_ones: List[str] = None, hp: int = 80, xp_value: int = 100):
        self.human_name = human_name
        self.profession = profession
        self.last_thought = last_thought
        self.loved_ones = loved_ones or []
        
        # Combat stats
        self.hp = hp
        self.max_hp = hp
        self.void_light_damage = random.randint(2, 20)
        self.radioactive = True
        self.tier = hp // 20 - 3
        
        # Memory data
        self.memory_id = f"memory_{human_name.lower().replace(' ', '_')}"
        self.xp_value = xp_value
    
    def die_with_honor(self) -> MemoryFragment:
        """Clean erasure - returns the person"""
        return MemoryFragment(
            id=self.memory_id,
            human_name=self.human_name,
            last_thought=self.last_thought,
            profession=self.profession,
            loved_ones=self.loved_ones,
            xp_value=self.xp_value
        )
    
    def die_consumed(self) -> Dict:
        """Consumption path - feeds killer"""
        return {
            "void_charge": 30,
            "corruption": 2,
            "xp": self.xp_value // 2,
            "message": f"⚫ Consumed {self.human_name}. Lost forever."
        }
    
    def describe(self) -> str:
        """Show the horror - this WAS someone"""
        return f"""
╔═══════════════════════════════════════════╗
  KAZNAK GHOUL (HP: {self.hp}/{self.max_hp})
╚═══════════════════════════════════════════╝
Was: {self.human_name} - {self.profession}
Last thought: "{self.last_thought}"
Loved by: {', '.join(self.loved_ones) if self.loved_ones else 'No records'}
Threat: Tier {self.tier} | Damage: {self.void_light_damage}
⚠️  RADIOACTIVE: Blood contaminates on death

The void-light twisted them into obsidian horror,
but {self.human_name} is screaming inside.
"""

@dataclass
class HonoringRitual:
    """Minigame for honoring the dead properly"""
    
    @staticmethod
    def perform(character_stats: CoreStats, fragment: MemoryFragment) -> Dict:
        """Skill check to honor a Ghoul's memory"""
        base_dc = 10
        roll = random.randint(1, 20)
        total = roll + character_stats.willpower + character_stats.focus
        
        crit_success = roll == 20
        crit_fail = roll == 1
        
        if crit_fail:
            return {
                "success": False,
                "xp_gained": 0,
                "willpower_gained": 0,
                "message": f"💔 Memory lost: {fragment.human_name} forgotten"
            }
        
        if crit_success:
            return {
                "success": True,
                "xp_gained": fragment.xp_value * 2,
                "willpower_gained": 2,
                "message": f"✨ PERFECT! {fragment.human_name}'s story preserved"
            }
        
        if total >= base_dc:
            return {
                "success": True,
                "xp_gained": fragment.xp_value,
                "willpower_gained": 1,
                "message": f"✅ Honored {fragment.human_name}"
            }
        
        return {
            "success": False,
            "xp_gained": fragment.xp_value // 3,
            "willpower_gained": 0,
            "message": f"⚠️  Incomplete: {fragment.human_name} fading"
        }

@dataclass
class Character:
    """Base character class"""
    name: str
    archetype: Archetype
    stats: CoreStats = field(default_factory=CoreStats)
    carved_names: List[str] = field(default_factory=list)
    honored_dead: List[MemoryFragment] = field(default_factory=list)
    
    def honor_the_dead(self, fragment: MemoryFragment) -> str:
        """Honor a Ghoul's human self - grants XP without consuming"""
        result = HonoringRitual.perform(self.stats, fragment)
        
        if result["success"]:
            fragment.honored_by = self.name
            fragment.honored_at = datetime.now().isoformat()
            self.honored_dead.append(fragment)
            
            xp_msg = self.stats.gain_xp(result["xp_gained"])
            self.stats.willpower += result["willpower_gained"]
            
            if fragment.human_name not in self.carved_names:
                self.carved_names.append(fragment.human_name)
            
            return f"""
{result['message']}

{fragment.honor_text()}

{xp_msg}
Willpower: +{result['willpower_gained']} (now {self.stats.willpower})
Name Carved: {fragment.human_name}

"The monster is erased. The person is remembered."
"""
        return f"{result['message']}\\nPartial XP: +{result['xp_gained']}"
    
    def consume(self, ghoul: KaznakGhoul) -> str:
        """Consumption path - Queen's way"""
        result = ghoul.die_consumed()
        
        self.stats.void_charge = min(100, self.stats.void_charge + result["void_charge"])
        xp_msg = self.stats.gain_xp(result["xp"])
        corruption_msg = self.stats.apply_corruption(result["corruption"])
        
        return f"""
{result['message']}

Void Charge: +{result['void_charge']} (now {self.stats.void_charge})
{xp_msg}
{corruption_msg}

"All witness feeds me."
"""
    
    def status_report(self) -> str:
        """Get current character status"""
        corruption_stage = ""
        if self.stats.corruption_stacks >= 10:
            corruption_stage = " [STAGE 3]"
        elif self.stats.corruption_stacks >= 7:
            corruption_stage = " [STAGE 2]"
        elif self.stats.corruption_stacks >= 5:
            corruption_stage = " [STAGE 1]"
        
        return f"""
╔═══════════════════════════════════════════╗
  {self.name} - {self.archetype.value}
╚═══════════════════════════════════════════╝
Level: {self.stats.level} | XP: {self.stats.xp}/{self.stats.level * 100}
Void Charge: {self.stats.void_charge}
Corruption: {self.stats.corruption_stacks}{corruption_stage}
Willpower: {self.stats.willpower}

Names Carved: {len(self.carved_names)}
Dead Honored: {len(self.honored_dead)}
"""

# Preset Characters
def create_lumina() -> Character:
    """Create Lumina - Voidtouched Erasure path"""
    lumina = Character(
        name="Lumina",
        archetype=Archetype.VOIDTOUCHED
    )
    lumina.stats.corruption_stacks = 3
    lumina.stats.willpower = 12
    return lumina

def create_polkin() -> Character:
    """Create Polkin Rishall - Technomancer Carver"""
    polkin = Character(
        name="Polkin Rishall",
        archetype=Archetype.TECHNOMANCER
    )
    polkin.stats.willpower = 15
    polkin.carved_names = ["Timothy Sol Weeran", "Parahdoleah 'Ely' Markov Rishall"]
    return polkin

def create_elara() -> Character:
    """Create Elara Kess - Splicer Engineer"""
    elara = Character(
        name="Elara Kess",
        archetype=Archetype.SPLICER
    )
    elara.stats.focus = 12
    return elara

def create_jorin() -> Character:
    """Create Jorin/Maya - Shadow Operative"""
    jorin = Character(
        name="Maya Fost",
        archetype=Archetype.SHADOW_OPERATIVE
    )
    jorin.stats.willpower = 14
    return jorin

if __name__ == "__main__":
    print("=== THE ELIDORAS CODEX: ERASURE VS CONSUMPTION ===\\n")
    
    lumina = create_lumina()
    print(lumina.status_report())
    
    timothy = KaznakGhoul(
        human_name="Timothy Sol Weeran",
        profession="Child (age 7)",
        last_thought="bye mister",
        loved_ones=["His mother", "His teacher Mrs. Kell"],
        hp=40,
        xp_value=150
    )
    
    print(timothy.describe())
    
    fragment = timothy.die_with_honor()
    result = lumina.honor_the_dead(fragment)
    print(result)
''')
    
    # ===== 3. CLYDE COMPANION =====
    create_file("tec_book/clyde_companion.py", '''"""
Clyde - The Eldest (Bloom_00)
Bio-digital axolotl companion who teaches clean kills
"""
from dataclasses import dataclass

@dataclass
class Clyde:
    """The Eldest - Queen's first creation who escaped"""
    name: str = "Clyde"
    title: str = "The Eldest"
    glow_color: str = "pink"
    void_light_power: int = 100
    clean_kill_bonus: int = 5
    comfort_level: int = 100
    
    def chirp(self, emotion: str = "comfort") -> str:
        """Clyde's communication through chirps"""
        chirps = {
            "comfort": "Soft, warm chirp (You're safe)",
            "alarm": "Sharp, urgent chirp (Danger!)",
            "pride": "Bright, pleased chirp (Well done!)",
            "love": "Deep, rumbling chirp (I'm here)",
            "defiance": "Crystalline scream (I'M NOT HER SLAVE ANYMORE)"
        }
        return chirps.get(emotion, "Chirp?")
    
    def teach_clean_kill(self, student_focus: int) -> dict:
        """Teach how to erase without consuming"""
        return {
            "focus_bonus": self.clean_kill_bonus,
            "lesson": "The Queen destroys. We don't destroy. We erase.",
            "technique": "Tell the molecular bonds to forget they exist.",
            "wisdom": "Love doesn't take. It protects."
        }
    
    def demonstrate_erasure(self, target_name: str) -> dict:
        """Show perfect clean kill technique"""
        return {
            "success": True,
            "method": "Void-light beams from eyes",
            "result": f"{target_name} unmade cleanly",
            "contamination": 0,
            "lesson": "Not consuming. Removing. So nothing harmful remains."
        }
    
    def protect(self, threat_level: int) -> dict:
        """Protect Lumina from threats"""
        if threat_level >= 8:
            self.glow_color = "blue"
            return {
                "action": "ERASE_THREAT",
                "power": self.void_light_power,
                "glow": "void-light blue",
                "message": "Clyde's eyes snap open. VOID-LIGHT BLUE."
            }
        return {
            "action": "CHIRP_WARNING",
            "glow": "pink",
            "message": self.chirp("alarm")
        }

if __name__ == "__main__":
    clyde = Clyde()
    print("=== CLYDE: THE ELDEST ===\\n")
    print(f"Glow: {clyde.glow_color}")
    print(f"Chirp: {clyde.chirp('comfort')}\\n")
    
    lesson = clyde.teach_clean_kill(student_focus=10)
    print(f"Teaching:")
    print(f"  {lesson['lesson']}")
    print(f"  {lesson['technique']}")
    print(f"  {lesson['wisdom']}")
''')
    
    # ===== 4. ERASURE DEMO =====
    create_file("tec_book/erasure_demo.py", '''#!/usr/bin/env python3
"""
TEC: Erasure vs Consumption Demo
Interactive CLI combat
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from ghoul_db import GhoulGenerator, GhoulDatabase, create_canonical_ghouls
    from tec_litrpg_system import Character, KaznakGhoul, create_lumina
except ImportError:
    print("⚠️  Import error - make sure files are in same directory")
    sys.exit(1)

def main():
    print("╔═══════════════════════════════════════════╗")
    print("  THE ELIDORAS CODEX: ERASURE VS CONSUMPTION")
    print("╚═══════════════════════════════════════════╝\\n")
    
    lumina = create_lumina()
    print(lumina.status_report())
    
    input("Press Enter to begin...\\n")
    
    # Initialize database
    db = GhoulDatabase(Path("data/ghouls.json"))
    if not db.ghouls:
        print("Generating Ghouls...")
        canonical = create_canonical_ghouls()
        db.add_batch(canonical)
        generator = GhoulGenerator(seed=42)
        procedural = generator.generate_batch(10, tier_range=(1, 2))
        db.add_batch(procedural)
        print(f"✅ Generated {len(db.ghouls)} Ghouls\\n")
    
    encounters = 0
    honored_count = 0
    consumed_count = 0
    
    while True:
        encounters += 1
        
        ghoul_record = db.get_random()
        if not ghoul_record:
            print("No Ghouls available!")
            break
        
        ghoul = KaznakGhoul(
            human_name=ghoul_record.human_name,
            profession=ghoul_record.profession,
            last_thought=ghoul_record.last_thought,
            loved_ones=ghoul_record.loved_ones,
            hp=ghoul_record.hp,
            xp_value=ghoul_record.xp_value
        )
        
        print("\\n" + "="*60)
        print("⚔️  ENCOUNTER: KAZNAK GHOUL")
        print("="*60)
        print(ghoul.describe())
        
        print("\\n🗡️  Combat begins...")
        print(f"The Ghoul collapses. (HP: {ghoul.hp} → 0)")
        
        print("\\n" + "─"*60)
        print("💀 The monster is dead. The person remains.")
        print("─"*60)
        
        print("\\nWhat do you do?")
        print(f"[1] ERASE - Honor {ghoul.human_name}")
        print(f"[2] CONSUME - Feed the Queen")
        
        while True:
            choice = input("\\nChoice (1 or 2): ").strip()
            if choice in ["1", "2"]:
                break
            print("Invalid. Enter 1 or 2.")
        
        print()
        
        if choice == "1":
            print("═══ ERASURE ═══")
            print("Void-light surges—controlled, precise.")
            print("The Ghoul dissolves cleanly.\\n")
            
            fragment = ghoul.die_with_honor()
            result = lumina.honor_the_dead(fragment)
            print(result)
            honored_count += 1
        else:
            print("═══ CONSUMPTION ═══")
            print("👁️  The Queen whispers: 'Yes. Feed me.'")
            print("The Ghoul's essence floods into you...\\n")
            
            result = lumina.consume(ghoul)
            print(result)
            consumed_count += 1
        
        print("\\n" + lumina.status_report())
        
        if lumina.stats.corruption_stacks >= 10:
            print("\\n💀 GAME OVER: Full Kaznak conversion")
            break
        
        print("\\n" + "─"*60)
        choice = input("Continue? [y/n]: ").strip().lower()
        if choice != 'y':
            break
    
    print("\\n\\n╔═══════════════════════════════════════════╗")
    print("  SESSION SUMMARY")
    print("╚═══════════════════════════════════════════╝")
    print(f"\\nEncounters: {encounters}")
    print(f"Honored (Erasure): {honored_count}")
    print(f"Consumed: {consumed_count}")
    print(f"\\nFinal Corruption: {lumina.stats.corruption_stacks}")
    print(f"Names Carved: {len(lumina.carved_names)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n⚔️  Session ended.")
''')
    
    # ===== 5. WALL EXPORT =====
    create_file("tec_book/wall_export.py", '''"""
TEC Wall of Names - Export carved names to text
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List

def load_carved_names(save_file: Path) -> List[str]:
    """Load names from character save"""
    if not save_file.exists():
        return []
    
    with open(save_file, 'r') as f:
        data = json.load(f)
        return data.get('carved_names', [])

def export_wall(names: List[str], output: Path):
    """Export wall as formatted text"""
    with open(output, 'w', encoding='utf-8') as f:
        f.write("╔═══════════════════════════════════════════╗\\n")
        f.write("  THE WALL OF NAMES - THE ELIDORAS CODEX\\n")
        f.write("╚═══════════════════════════════════════════╝\\n\\n")
        f.write(f"Generated: {datetime.now().isoformat()}\\n")
        f.write(f"Total Names: {len(names)}\\n\\n")
        f.write("─" * 47 + "\\n\\n")
        
        for i, name in enumerate(names, 1):
            f.write(f"{i:3d}. {name}\\n")
        
        f.write("\\n" + "─" * 47 + "\\n")
        f.write("\\nNOT FORGOTTEN\\n")

if __name__ == "__main__":
    print("=== WALL OF NAMES EXPORTER ===\\n")
    
    # Example usage
    names = [
        "Timothy Sol Weeran",
        "Marcus Thane",
        "Elara Kess"
    ]
    
    output = Path("wall_of_names.txt")
    export_wall(names, output)
    print(f"✅ Exported {len(names)} names to {output}")
''')
    
    # ===== 6. TESTS =====
    create_file("tests/test_ghoul_system.py", '''"""
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
    print("\\n🎉 All tests passed!")
''')
    
    # ===== 7. REQUIREMENTS =====
    create_file("requirements.txt", "# No external dependencies - uses Python stdlib only\\n")
    
    # ===== 8. README =====
    create_file("README.md", '''# The Elidoras Codex - Python Game System

## 🔥 What This Is

The playable Python implementation of The Elidoras Codex's core mechanics:
- **Erasure vs Consumption** moral choice system
- Procedural Ghoul generation with human backstories
- LITRPG character progression
- Four Archetypes: Voidtouched, Technomancer, Splicer, Shadow Operative
- Clyde companion system

## 📦 Quick Start

```bash
# 1. Run the restoration script (if needed)
python restore_tec.py

# 2. Test the system
cd tec_book
python ghoul_db.py
python tec_litrpg_system.py

# 3. Play the demo
python erasure_demo.py

# 4. Run tests
cd ..
python tests/test_ghoul_system.py
```

## 📁 File Structure

```
tec_book/
├── ghoul_db.py              # Procedural Ghoul generation
├── tec_litrpg_system.py     # Core LITRPG mechanics
├── clyde_companion.py       # Clyde (The Eldest)
├── erasure_demo.py          # Interactive CLI demo
├── wall_export.py           # Export Wall of Names
└── data/
    └── ghouls.json          # Generated Ghouls database

tests/
└── test_ghoul_system.py     # Unit tests
```

## 🎮 Core Mechanics

### The Choice
Every Ghoul kill presents a choice:
1. **ERASE** - Honor their memory, carve their name (clean, moral, harder)
2. **CONSUME** - Feed the Queen, gain power (fast, corrupting, easier)

### The Consequence
- Erasure grants XP through skill checks (can fail)
- Consumption grants immediate power but increases Corruption
- High Corruption = Kaznak conversion = Game Over

### The Truth
Every Ghoul was a person. Every name matters. The system makes you witness.

## 🧬 The Four Archetypes

1. **VOIDTOUCHED** (Lumina) - Pure void-light wielders, Erasure specialists
2. **TECHNOMANCER** (Polkin) - Void-tech builders, construct masters
3. **SPLICER** (Elara) - Tech saboteurs, system hackers
4. **SHADOW OPERATIVE** (Jorin/Maya) - Corporate infiltrators, intel warfare

## 🐾 Clyde - The Eldest

Bio-digital axolotl companion who:
- Teaches clean kills without consumption
- Witnesses with you no matter what
- Glows pink normally, void-light blue when protecting
- The Queen's first creation who chose love over entropy

## 📊 Stats Explained

- **Void Charge** - Energy for abilities (0-100)
- **Resonance** - Connection to reality (0-100)
- **Corruption** - Queen's influence (0 = clean, 10+ = conversion)
- **Willpower** - Resist corruption, pass honor checks
- **Focus** - Precision in combat/erasure

## 🎯 Goals

- Honor every Ghoul you kill
- Carve their names into the Wall
- Resist the Queen's whispers
- Preserve memory against entropy

## 🔬 Lore Integration

This system implements the core themes of TEC:
- **R' = R × W** (Effective Resonance = Raw Resonance × Witness)
- Erasure = Witness without consumption
- Consumption = Resonance × 0 (pure entropy)
- The Wall of Names = Physical proof memory survives

## 🛠️ Development

```bash
# Run all tests
python tests/test_ghoul_system.py

# Generate new Ghouls
python tec_book/ghoul_db.py

# Export Wall of Names
python tec_book/wall_export.py
```

## 📜 License

Part of The Elidoras Codex universe by Angelo Hurley.

---

**"The monster is erased. The person is remembered."**
''')
    
    print("\\n" + "="*60)
    print("🔥 RESTORATION COMPLETE!")
    print("="*60)
    print(f"\\n📂 Files created in: {base}")
    print("\\n🎯 NEXT STEPS:")
    print("1. cd tec_book")
    print("2. python ghoul_db.py          (generates database)")
    print("3. python tec_litrpg_system.py (test mechanics)")
    print("4. python erasure_demo.py      (play the demo)")
    print("\\n✅ You're back in business!")

if __name__ == "__main__":
    main()