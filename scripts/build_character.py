#!/usr/bin/env python3
import logging
import sys
from pathlib import Path

# Ensure local package can be imported when running scripts from repository
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

MIN_ARGS = 3  # Minimum number of arguments required


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)

    if len(sys.argv) < MIN_ARGS:
        logger.error("Usage: build_character.py <Name> <Class>")
        sys.exit(1)
    name = sys.argv[1]
    cls = sys.argv[2]

    # Import project-local modules after ensuring `src` is on sys.path
    from astradigital.kernel import AstradigitalEntity, load_codex  # type: ignore

    root = Path(__file__).resolve().parents[1]
    codex_path = root / "data" / "codex" / "classes.json"
    codex = load_codex(str(codex_path))

    entity = AstradigitalEntity.from_codex(name, cls, codex)
    logger.info(
        {
            "name": entity.name,
            "class": entity.philosophy_class,
            "role": entity.role,
            "integrity": entity.integrity,
            "golf_rule": entity.is_golf_rule,
            "resources": entity.resources,
        },
    )


if __name__ == "__main__":
    main()
