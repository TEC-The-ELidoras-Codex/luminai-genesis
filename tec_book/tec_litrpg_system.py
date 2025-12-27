"""
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
        text = f"╔══ {self.human_name} ══╗\n"
        if self.profession:
            text += f"Was: {self.profession}\n"
        text += f'Last thought: "{self.last_thought}"\n'
        if self.loved_ones:
            text += f"Remembered by: {', '.join(self.loved_ones)}\n"
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
        return f"{result['message']}\nPartial XP: +{result['xp_gained']}"
    
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
    # Use a lower starting focus to match demo/test expectations
    lumina.stats.focus = 5
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
    print("=== THE ELIDORAS CODEX: ERASURE VS CONSUMPTION ===\n")
    
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
