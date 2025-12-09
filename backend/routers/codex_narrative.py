"""Codex and narrative asset routers."""

import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/codex", tags=["codex"])

# Load characters data
_characters_cache = None


def _load_characters():
    """Load characters.json from data/codex/."""
    global _characters_cache
    if _characters_cache is not None:
        return _characters_cache

    characters_file = (
        Path(__file__).parent.parent / "data" / "codex" / "characters.json"
    )
    try:
        if characters_file.exists():
            with open(characters_file) as f:
                _characters_cache = json.load(f)
                logger.info(f"Loaded {len(_characters_cache)} characters from codex")
                return _characters_cache
    except Exception as e:
        logger.error(f"Error loading characters: {e}")

    # Fallback: empty dict
    _characters_cache = {}
    return _characters_cache


@router.get("/characters", summary="List playable characters from the Codex")
def get_characters(filter_playable: Optional[bool] = None):
    """Fetch all characters from the LuminAI Genesis Codex.

    Query Parameters:
    - filter_playable (bool, optional): Return only playable characters if True

    Returns:
    - dict: Character list with IDs, names, descriptions, and metadata
    """
    characters = _load_characters()

    if not characters:
        return {"characters": [], "count": 0}

    if filter_playable:
        playable = {k: v for k, v in characters.items() if v.get("playable", False)}
        return {"characters": playable, "count": len(playable)}

    return {"characters": characters, "count": len(characters)}


@router.get("/characters/{character_id}", summary="Get a specific character")
def get_character(character_id: str):
    """Fetch a single character by ID.

    Args:
        character_id: Character ID (e.g. 'elara_kess', 'polkin_rishall')

    Returns:
        Character object with full metadata
    """
    characters = _load_characters()

    if character_id not in characters:
        raise HTTPException(
            status_code=404, detail=f"Character '{character_id}' not found"
        )

    return characters[character_id]


@router.get("/characters/{character_id}/portrait", summary="Get character portrait URL")
def get_character_portrait(character_id: str):
    """Fetch the portrait URL or image data for a character.

    Args:
        character_id: Character ID

    Returns:
        dict with portrait_url, description, and other visual metadata
    """
    characters = _load_characters()

    if character_id not in characters:
        raise HTTPException(
            status_code=404, detail=f"Character '{character_id}' not found"
        )

    char = characters[character_id]
    return {
        "character_id": character_id,
        "name": char.get("name"),
        "portrait_url": char.get("portrait_url"),
        "visual_description": char.get("visual_description"),
        "alignment": char.get("alignment"),
    }


@router.get("/characters/{character_id}/lore", summary="Get character lore")
def get_character_lore(character_id: str):
    """Fetch deep lore for a character (biography, story arcs, etc).

    Args:
        character_id: Character ID

    Returns:
        dict with biography, story arcs, relationships, and notes
    """
    characters = _load_characters()

    if character_id not in characters:
        raise HTTPException(
            status_code=404, detail=f"Character '{character_id}' not found"
        )

    char = characters[character_id]
    return {
        "character_id": character_id,
        "name": char.get("name"),
        "biography": char.get("biography"),
        "story_arcs": char.get("story_arcs", []),
        "relationships": char.get("relationships", {}),
        "notes": char.get("notes"),
    }
