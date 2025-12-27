# The Elidoras Codex - Python Game System

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
