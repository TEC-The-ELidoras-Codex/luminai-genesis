import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/axioms", tags=["axioms"])

# Load Conscience Axioms at module import
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "axioms"

try:
    with open(DATA_DIR / "LUMINAI_CONSCIENCE_AXIOMS.json") as f:
        AXIOMS_DATA = json.load(f)
except FileNotFoundError:
    AXIOMS_DATA = {"axioms": [], "metadata": {}}


@router.get("", response_model=dict[str, Any])
def list_axioms() -> dict[str, Any]:
    """
    Return all LuminAI Conscience Axioms.

    These foundational principles govern conscience-aware AI behavior,
    including Witness Protocol bindings and governance constraints.
    """
    return AXIOMS_DATA


@router.get("/{axiom_id}", response_model=dict[str, Any])
def get_axiom(axiom_id: int) -> dict[str, Any]:
    """Get details for a specific axiom by ID."""
    axioms = AXIOMS_DATA.get("axioms", [])
    for axiom in axioms:
        if axiom.get("id") == axiom_id:
            return axiom

    return {"error": f"Axiom {axiom_id} not found", "available_axioms": len(axioms)}


@router.get("/category/{category}", response_model=dict[str, Any])
def get_axioms_by_category(category: str) -> dict[str, Any]:
    """
    Get all axioms in a specific category.

    Categories: foundational, operational, epistemic, governance, trajectory
    """
    axioms = AXIOMS_DATA.get("axioms", [])
    filtered = [a for a in axioms if a.get("category") == category]

    return {"category": category, "count": len(filtered), "axioms": filtered}


@router.get("/witness-protocol/bindings", response_model=dict[str, Any])
def get_witness_protocol_axioms() -> dict[str, Any]:
    """
    Get all axioms with witness_protocol_binding=true.

    These are non-negotiable principles enforced by the W multiplier.
    """
    axioms = AXIOMS_DATA.get("axioms", [])
    bound = [a for a in axioms if a.get("witness_protocol_binding") is True]

    return {
        "binding_count": len(bound),
        "axioms": bound,
        "enforcement": "W multiplier in R' = R × W equation",
    }
