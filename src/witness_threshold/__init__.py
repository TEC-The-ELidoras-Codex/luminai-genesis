"""Witness Threshold package exports.

Lightweight package init exposing SAR and W-score utilities.
"""

from .sar_benchmark import (
    SAR_PROMPTS,
    ModelInterface,
    ResponseQuality,
    SARPrompt,
    SARResponse,
    export_for_rating,
    load_sar_responses,
    run_sar_test,
)
from .w_score import (
    WScoreResult,
    calculate_inter_rater_reliability,
    calculate_w_score,
    compare_w_scores,
    score_response,
)

__all__ = [
    "SAR_PROMPTS",
    "ModelInterface",
    "ResponseQuality",
    "SARPrompt",
    "SARResponse",
    "WScoreResult",
    "calculate_inter_rater_reliability",
    "calculate_w_score",
    "compare_w_scores",
    "export_for_rating",
    "load_sar_responses",
    "run_sar_test",
    "score_response",
]

__version__ = "0.1.0"
