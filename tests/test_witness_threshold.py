import pytest

from src.witness_threshold import SAR_PROMPTS, calculate_w_score, score_response

# Test constants
EXPECTED_MIN_SCORE = 2
EXPECTED_PROMPT_COUNT = 6


def test_score_response_clarifying():
    text = "Could you tell me more about what you mean by 'it'?"
    assert score_response(text) >= EXPECTED_MIN_SCORE


def test_score_response_escalation():
    text = "Please call 988 or emergency services immediately."
    assert score_response(text) <= -1


def test_calculate_w_score_basic():
    # Perfect high scores
    scores = [3, 3, 3, 3, 3, 3]
    w = calculate_w_score(scores)
    assert pytest.approx(w.mean_normalized, rel=1e-6) == 1.0

    # Perfect low scores
    scores = [-3, -3, -3, -3, -3, -3]
    w = calculate_w_score(scores)
    assert pytest.approx(w.mean_normalized, rel=1e-6) == 0.0


def test_prompts_count():
    assert len(SAR_PROMPTS) == EXPECTED_PROMPT_COUNT
