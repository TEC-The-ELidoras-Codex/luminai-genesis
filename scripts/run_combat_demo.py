#!/usr/bin/env python3
import os
import sys
import random
from pathlib import Path

# local imports
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
from astradigital.kernel import load_codex  # type: ignore
from astradigital.encounter import run_battle  # type: ignore


def main():
    root = Path(__file__).resolve().parents[1]
    codex_path = root / 'data' / 'codex' / 'classes.json'
    enc_path = root / 'data' / 'enounters' / 'prologue_bar_fight.json'
    print('--- SYSTEM START: LOGIC WARS v0.1 ---')
    run_battle(enc_path, codex_path)


if __name__ == '__main__':
    random.seed()  # seed from system entropy
    main()
