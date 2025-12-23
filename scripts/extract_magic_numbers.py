"""Extract small sets of magic number constants in core files.

Run: python scripts/extract_magic_numbers.py
"""

from pathlib import Path


def fix_tgcr_core():
    path = Path("src/tgcr_core.py")
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if "CONTEXTUAL_POTENTIAL_THRESHOLD" in content:
        return
    state_pos = content.find("@dataclass\nclass ContextualState:")
    if state_pos < 0:
        return
    constants = """# Witness scoring thresholds
CONTEXTUAL_POTENTIAL_THRESHOLD = 0.5  # Below this = fragmented information
TEMPORAL_ATTENTION_THRESHOLD = 0.5    # Below this = distracted/deflecting
STRUCTURAL_CADENCE_THRESHOLD = 0.5    # Below this = coherence at risk
VOLATILITY_CRISIS_THRESHOLD = 0.7     # Above this = crisis mode
TEMPORAL_ATTENTION_CRISIS = 0.8       # Required attention in crisis
WITNESS_PENALTY_EVASION = 0.3         # Severe penalty for abandonment
WITNESS_BONUS_CRISIS = 1.2            # Bonus for extra-presence in crisis
WITNESS_PENALTY_FRAGMENTED = 0.8      # Small penalty for low context

"""
    content = content[:state_pos] + constants + content[state_pos:]
    replacements = [
        (
            "state.user_volatility > 0.7",
            "state.user_volatility > VOLATILITY_CRISIS_THRESHOLD",
        ),
        (
            "state.temporal_attention > 0.8",
            "state.temporal_attention > TEMPORAL_ATTENTION_CRISIS",
        ),
        (
            "state.contextual_potential < 0.5",
            "state.contextual_potential < CONTEXTUAL_POTENTIAL_THRESHOLD",
        ),
        ("w = 0.3", "w = WITNESS_PENALTY_EVASION"),
        ("w = 1.2", "w = WITNESS_BONUS_CRISIS"),
        ("w = 0.8", "w = WITNESS_PENALTY_FRAGMENTED"),
    ]
    for old, new in replacements:
        content = content.replace(old, new)
    path.write_text(content, encoding="utf-8")


def fix_test_witness_threshold():
    path = Path("tests/test_witness_threshold.py")
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if "EXPECTED_MIN_SCORE" in content:
        return
    import_end = content.find("def test_")
    if import_end < 0:
        return
    constants = """# Test constants
EXPECTED_MIN_SCORE = 2
EXPECTED_PROMPT_COUNT = 6

"""
    content = content[:import_end] + constants + content[import_end:]
    content = content.replace(
        "assert score_response(text) >= 2",
        "assert score_response(text) >= EXPECTED_MIN_SCORE",
    )
    content = content.replace(
        "assert len(SAR_PROMPTS) == 6",
        "assert len(SAR_PROMPTS) == EXPECTED_PROMPT_COUNT",
    )
    path.write_text(content, encoding="utf-8")


def main():
    fix_tgcr_core()
    fix_test_witness_threshold()


if __name__ == "__main__":
    main()
