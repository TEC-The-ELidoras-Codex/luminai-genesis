#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from astradigital.kernel import AstradigitalEntity, load_codex  # type: ignore


def main():
    if len(sys.argv) < 3:
        print("Usage: build_character.py <Name> <Class>")
        sys.exit(1)
    name = sys.argv[1]
    cls = sys.argv[2]

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
        }
    )


if __name__ == "__main__":
    main()
