"""Merge docs/frequency_mapping.yaml into
data/frequencies/SIXTEEN_FREQUENCIES_MAPPING.json.

Purpose: enrich the canonical JSON with fields from the YAML prototype. Example
fields merged include representative_interventions, behavioral_markers, and
neurochemical_signature. Writes `SIXTEEN_FREQUENCIES_MAPPING.merged.json` as
output and leaves a backup of the original JSON as `.bak`.

This is a one-off utility to be run by the repo maintainer.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
yaml_path = os.path.join(ROOT, "docs", "frequency_mapping.yaml")
json_path = os.path.join(
    ROOT,
    "data",
    "frequencies",
    "SIXTEEN_FREQUENCIES_MAPPING.json",
)
out_path = os.path.join(
    ROOT,
    "data",
    "frequencies",
    "SIXTEEN_FREQUENCIES_MAPPING.merged.json",
)


def load_yaml_simple(path: str) -> list:
    try:
        import yaml
    except ImportError:
        logger = logging.getLogger(__name__)
        logger.error(
            "PyYAML not available; cannot merge YAML. "
            "Install pyyaml or run in an environment with it.",
        )
        sys.exit(2)
    p = Path(path)
    with p.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # YAML shape: list of mappings
    return data


def load_json(path: str) -> dict:
    p = Path(path)
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def main():
    if not os.path.exists(json_path):
        logger = logging.getLogger(__name__)
        logger.error("Canonical JSON not found: %s", json_path)
        sys.exit(1)
    if not os.path.exists(yaml_path):
        logger = logging.getLogger(__name__)
        logger.error("YAML prototype not found (skipping merge): %s", yaml_path)
        sys.exit(1)

    logger = logging.getLogger(__name__)
    logger.info("Loading JSON: %s", json_path)
    j = load_json(json_path)
    freqs = j.get("frequencies") if isinstance(j, dict) else j

    logger.info("Loading YAML: %s", yaml_path)
    y = load_yaml_simple(yaml_path)

    # Build lookup by name (lowercase)
    y_map = {str(item.get("name", "")).strip().lower(): item for item in y}

    merged = []
    for f in freqs:
        name = str(f.get("name", "")).strip()
        key = name.lower()
        extra = y_map.get(key)
        if extra:
            # copy specific fields if present
            if "representative_interventions" in extra:
                f["representative_interventions"] = extra[
                    "representative_interventions"
                ]
            if "behavioral_markers" in extra:
                f["behavioral_markers"] = extra["behavioral_markers"]
            if "neurochemical_signature" in extra:
                f["neurochemical_signature"] = extra["neurochemical_signature"]
        merged.append(f)

    # backup original
    bak = json_path + ".bak"
    if not os.path.exists(bak):
        os.rename(json_path, bak)
        logger.info("Backed up original JSON to %s", bak)
    else:
        logger.info("Backup already exists: %s", bak)

    out = {"frequencies": merged, "metadata": j.get("metadata", {})}
    with Path(out_path).open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    logger.info("Wrote merged mapping to %s", out_path)


if __name__ == "__main__":
    main()
