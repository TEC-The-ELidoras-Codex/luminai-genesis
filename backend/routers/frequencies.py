import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/frequencies", tags=["frequencies"])

# Load Sixteen Frequencies mapping at module import
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "frequencies"

# Prefer the merged mapping if available, fall back to the canonical JSON.
FREQUENCIES_DATA = {"frequencies": [], "metadata": {}}
for candidate in (
    DATA_DIR / "SIXTEEN_FREQUENCIES_MAPPING.merged.json",
    DATA_DIR / "SIXTEEN_FREQUENCIES_MAPPING.json",
):
    if candidate.exists():
        try:
            with open(candidate, "r") as f:
                FREQUENCIES_DATA = json.load(f)
        except Exception:
            FREQUENCIES_DATA = {"frequencies": [], "metadata": {}}
        break


@router.get("", response_model=dict[str, Any])
def list_frequencies() -> dict[str, Any]:
    """
    Return all sixteen affective frequency eigenmodes.

    Each frequency maps neurochemical axes to emotional archetypes,
    forming the basis for resonance computation and persona responses.
    """
    return FREQUENCIES_DATA


@router.get("/{frequency_id}", response_model=dict[str, Any])
def get_frequency(frequency_id: int) -> dict[str, Any]:
    """Get details for a specific frequency by ID (1-16)."""
    frequencies = FREQUENCIES_DATA.get("frequencies", [])
    for freq in frequencies:
        if freq.get("id") == frequency_id:
            return freq

    return {"error": f"Frequency {frequency_id} not found", "valid_range": "1-16"}
