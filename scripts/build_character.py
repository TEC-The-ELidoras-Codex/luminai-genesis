#!/usr/bin/env python3
import sys
from pathlib import Path

# Script argument constants for readability and linting
MIN_ARGS = 3

# Ensure local package can be imported when running scripts from repository
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

# Delay importing local modules until after sys.path modification


def main():
    if len(sys.argv) < MIN_ARGS:
        print("Usage: build_character.py <Name> <Class>")
        sys.exit(1)
    name = sys.argv[1]
    cls = sys.argv[2]

    # Import project-local modules after ensuring `src` is on sys.path
    from astradigital.kernel import (AstradigitalEntity,  # type: ignore
                                     load_codex)

    root = Path(__file__).resolve().parents[1]
    codex_path = root / "data" / "codex" / "classes.json"
    codex = load_codex(str(codex_path))

    entity = AstradigitalEntity.from_codex(name, cls, codex)
    print(
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
