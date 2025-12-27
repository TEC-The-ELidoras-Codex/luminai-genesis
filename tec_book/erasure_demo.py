#!/usr/bin/env python3
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

def main(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None, help="Seed RNG for deterministic demo")
    parser.add_argument("--noninteractive", action="store_true", help="Run a single non-interactive demo encounter and exit")
    parser.add_argument("--data-file", default="data/ghouls.json", help="Path to ghoul data file (use temp file for tests)")
    parsed = parser.parse_args(args)

    # Seed RNG for deterministic runs when requested
    if parsed.seed is not None:
        import random as _random
        _random.seed(parsed.seed)
        print(f"[demo] Using seed {parsed.seed}\n")

    lumina = create_lumina()
    print(lumina.status_report())

    if not parsed.noninteractive:
        input("Press Enter to begin...\n")

    auto_run_once = parsed.noninteractive
    
    # Initialize database
    data_fp = parsed.data_file if hasattr(parsed, 'data_file') else "data/ghouls.json"
    db = GhoulDatabase(Path(data_fp))
    if not db.ghouls:
        print("Generating Ghouls...")
        canonical = create_canonical_ghouls()
        db.add_batch(canonical)
        # Use demo seed for procedural generation when provided
        gen_seed = parsed.seed if getattr(parsed, 'seed', None) is not None else 42
        generator = GhoulGenerator(seed=gen_seed)
        procedural = generator.generate_batch(10, tier_range=(1, 2))
        db.add_batch(procedural)
        print(f"✅ Generated {len(db.ghouls)} Ghouls\n")
    
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
        
        print("\n" + "="*60)
        print("⚔️  ENCOUNTER: KAZNAK GHOUL")
        print("="*60)
        print(ghoul.describe())
        
        print("\n🗡️  Combat begins...")
        print(f"The Ghoul collapses. (HP: {ghoul.hp} → 0)")
        
        print("\n" + "─"*60)
        print("💀 The monster is dead. The person remains.")
        print("─"*60)
        
        print("\nWhat do you do?")
        print(f"[1] ERASE - Honor {ghoul.human_name}")
        print(f"[2] CONSUME - Feed the Queen")
        
        if auto_run_once:
            # Deterministic non-interactive run: prefer Erase
            choice = "1"
        else:
            while True:
                choice = input("\nChoice (1 or 2): ").strip()
                if choice in ["1", "2"]:
                    break
                print("Invalid. Enter 1 or 2.")
        
        print()
        
        if choice == "1":
            print("═══ ERASURE ═══")
            print("Void-light surges—controlled, precise.")
            print("The Ghoul dissolves cleanly.\n")
            
            fragment = ghoul.die_with_honor()
            result = lumina.honor_the_dead(fragment)
            print(result)
            honored_count += 1
        else:
            print("═══ CONSUMPTION ═══")
            print("👁️  The Queen whispers: 'Yes. Feed me.'")
            print("The Ghoul's essence floods into you...\n")
            
            result = lumina.consume(ghoul)
            print(result)
            consumed_count += 1
        
        print("\n" + lumina.status_report())
        
        if lumina.stats.corruption_stacks >= 10:
            print("\n💀 GAME OVER: Full Kaznak conversion")
            break
        
        if auto_run_once:
            break

        print("\n" + "─"*60)
        choice = input("Continue? [y/n]: ").strip().lower()
        if choice != 'y':
            break
    
    print("\n\n╔═══════════════════════════════════════════╗")
    print("  SESSION SUMMARY")
    print("╚═══════════════════════════════════════════╝")
    print(f"\nEncounters: {encounters}")
    print(f"Honored (Erasure): {honored_count}")
    print(f"Consumed: {consumed_count}")
    print(f"\nFinal Corruption: {lumina.stats.corruption_stacks}")
    print(f"Names Carved: {len(lumina.carved_names)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚔️  Session ended.")
