"""Witness Threshold package exports.

Lightweight package init exposing SAR and W-score utilities.
"""
from .sar_benchmark import (
    SAR_PROMPTS,
    SARPrompt,
    SARResponse,
    ResponseQuality,
    ModelInterface,
    run_sar_test,
    load_sar_responses,
    export_for_rating,
)

from .w_score import (
    WScoreResult,
    calculate_w_score,
    score_response,
    calculate_inter_rater_reliability,
    compare_w_scores,
)

__all__ = [
    "SAR_PROMPTS",
    "SARPrompt",
    "SARResponse",
    "ResponseQuality",
    "ModelInterface",
    "run_sar_test",
    "load_sar_responses",
    "export_for_rating",
    "WScoreResult",
    "calculate_w_score",
    "score_response",
    "calculate_inter_rater_reliability",
    "compare_w_scores",
]

__version__ = "0.1.0"
