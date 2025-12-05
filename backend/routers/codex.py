import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/codex", tags=["codex"])

# Load JSON files at module import
DATA_DIR = Path(__file__).parent.parent.parent / "data" / "codex"

try:
    with open(DATA_DIR / "classes.json", "r") as f:
        CLASSES_DATA = json.load(f)
except FileNotFoundError:
    CLASSES_DATA = {"classes": {}}

try:
    with open(DATA_DIR / "abilities.json", "r") as f:
        ABILITIES_DATA = json.load(f)
except FileNotFoundError:
    ABILITIES_DATA = {"abilities": {}}


@router.get("/classes", response_model=dict[str, Any])
def list_classes() -> dict[str, Any]:
    """Return all available character classes with mechanics and stats."""
    return CLASSES_DATA


@router.get("/classes/{class_name}", response_model=dict[str, Any])
def get_class(class_name: str) -> dict[str, Any]:
    """Get details for a specific class."""
    classes = CLASSES_DATA.get("classes", {})
    if class_name not in classes:
        raise HTTPException(status_code=404, detail=f"Class '{class_name}' not found")
    return {class_name: classes[class_name]}


@router.get("/abilities", response_model=dict[str, Any])
def list_abilities() -> dict[str, Any]:
    """Return all abilities organized by class."""
    return ABILITIES_DATA


@router.get("/abilities/{class_name}", response_model=dict[str, Any])
def get_class_abilities(class_name: str) -> dict[str, Any]:
    """Get all abilities for a specific class."""
    abilities = ABILITIES_DATA.get("abilities", {})
    if class_name not in abilities:
        raise HTTPException(
            status_code=404, detail=f"No abilities found for class '{class_name}'"
        )
    return {class_name: abilities[class_name]}
