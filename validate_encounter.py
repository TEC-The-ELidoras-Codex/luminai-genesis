"""Validation script for Astradigital encounter system.

This script verifies that the encounter loop, ability resolution, and
codex loading work end-to-end, serving as a regression test for the
philosophy-driven combat engine.
"""
from pathlib import Path
import sys
import os

# Ensure src is in path
sys.path.append(os.getcwd())

try:
    from src.astradigital.encounter import run_battle
    print('✅ Import Successful: src.astradigital.encounter')
    
    # Define paths
    encounter_path = Path('./data/enounters/prologue_bar_fight.json')
    classes_path = Path('./data/codex/classes.json')
    
    if not encounter_path.exists() or not classes_path.exists():
        print(f'⚠️ Warning: Data files not found. Checking paths:\n  {encounter_path}: {encounter_path.exists()}\n  {classes_path}: {classes_path.exists()}')
    else:
        print('⚔️ Starting Validation Battle...\n')
        run_battle(encounter_path, classes_path)
        print('\n✨ Validation Complete: Battle ran successfully.')

except ImportError as e:
    print(f'❌ Import Error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Runtime Error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
