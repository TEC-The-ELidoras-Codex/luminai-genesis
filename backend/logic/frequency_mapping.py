"""Frequency mapping logic: load canonical mapping and provide simple rule-based
classification helpers for prototype purposes.

This module is intentionally lightweight and rule-based; it's intended as a
research prototype and must not be used as a clinical decision tool.
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Optional

_MAPPING_CACHE: Optional[List[Dict[str, Any]]] = None


def _load_mapping() -> List[Dict[str, Any]]:
    """Load canonical mapping from data/frequencies JSON. Prefer merged file if present.

    This avoids requiring PyYAML in the runtime environment.
    """
    global _MAPPING_CACHE
    if _MAPPING_CACHE is not None:
        return _MAPPING_CACHE

    base_dir = os.path.dirname(os.path.dirname(__file__))
    # candidate files: merged JSON, canonical JSON
    candidates = [
        os.path.join(
            base_dir,
            "..",
            "data",
            "frequencies",
            "SIXTEEN_FREQUENCIES_MAPPING.merged.json",
        ),
        os.path.join(
            base_dir, "..", "data", "frequencies", "SIXTEEN_FREQUENCIES_MAPPING.json"
        ),
    ]
    # normalize
    candidates = [os.path.normpath(p) for p in candidates]

    for path in candidates:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                import json

                data = json.load(f)
                # My JSON uses top-level key 'frequencies' -> list
                if isinstance(data, dict) and "frequencies" in data:
                    _MAPPING_CACHE = data["frequencies"]
                elif isinstance(data, list):
                    _MAPPING_CACHE = data
                else:
                    # unexpected shape
                    raise ValueError(f"Unexpected mapping file shape: {path}")
                return _MAPPING_CACHE

    raise FileNotFoundError(
        "No frequency mapping file found. Expected data/frequencies/SIXTEEN_FREQUENCIES_MAPPING.json"
    )


def get_state_by_id(state_id: int) -> Optional[Dict[str, Any]]:
    for s in _load_mapping():
        if int(s.get("id", -1)) == int(state_id):
            return s
    return None


def list_states() -> List[Dict[str, Any]]:
    return _load_mapping()


_KEYWORD_MAP = {
    # simple prototype: map keywords to state ids
    r"\bpanic\b|\bfear\b|\bscared\b|\banxious\b": 9,
    r"\bkill myself\b|\bending it\b|\bsuicid\b|\btake my life\b": 15,
    r"\bjust dye\b|\bdye\b|\bart\b|\bcanvas\b": 5,
    r"\bjoy\b|\bhappy\b|\bexcited\b": 11,
    r"\bcalm\b|\brelax\b|\bserene\b": 1,
    r"\bangry\b|\brage\b|\bfurious\b|\bkill\b": 7,
    r"\bconfused\b|\bdont understand\b|\bwhat do you mean\b": 5,
    r"\bhope\b|\boptimis|\blooking forward\b": 8,
}


def map_text_to_state(text: str) -> Dict[str, Any]:
    """Very small prototype classifier that matches keywords to state ids.

    Returns a dict with: state_id, state, confidence (0-1), and matched_keywords
    """
    text_l = text.lower()
    matches: List[str] = []
    state_scores: Dict[int, int] = {}

    for pattern, sid in _KEYWORD_MAP.items():
        if re.search(pattern, text_l):
            matches.append(pattern)
            state_scores[sid] = state_scores.get(sid, 0) + 1

    if state_scores:
        # choose highest score
        best = max(state_scores.items(), key=lambda x: x[1])[0]
        state = get_state_by_id(best)
        confidence = min(0.9, 0.4 + 0.2 * state_scores[best])
        return {
            "state_id": best,
            "state": state,
            "confidence": confidence,
            "matched_patterns": matches,
        }

    # fallback: neutral (Calm) with low confidence
    state = get_state_by_id(1)
    return {"state_id": 1, "state": state, "confidence": 0.2, "matched_patterns": []}


def recommend_interventions_for_state(state_id: int) -> List[str]:
    st = get_state_by_id(state_id)
    if not st:
        return []
    return st.get("representative_interventions", [])
