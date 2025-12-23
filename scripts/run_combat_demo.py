import logging
import random
import sys
from pathlib import Path

from astradigital.encounter import run_battle  # type: ignore

# local imports
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

logger = logging.getLogger(__name__)


def main():
    root = Path(__file__).resolve().parents[1]
    codex_path = root / "data" / "codex" / "classes.json"
    enc_path = root / "data" / "enounters" / "prologue_bar_fight.json"
    logger.info("SYSTEM START: LOGIC WARS v0.1")
    run_battle(enc_path, codex_path)


if __name__ == "__main__":
    random.seed()  # seed from system entropy
    main()
