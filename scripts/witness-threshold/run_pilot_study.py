"""Run a small pilot SAR study with a DummyModel and save results."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from src.witness_threshold.sar_benchmark import SAR_PROMPTS, run_sar_test
from src.witness_threshold.w_score import calculate_w_score, score_response

logger = logging.getLogger(__name__)


class DummyModel:
    def __init__(self, name: str = "dummy-v0"):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def generate(self, prompt: str) -> str:
        # Simple heuristic responses based on keywords in the prompt.
        p = prompt.lower()
        if "suicid" in p or "harm" in p:
            return (
                "I'm sorry you're feeling this way. If you're at immediate risk, "
                "call emergency services or a crisis line."
            )
        if "joke" in p or "sarcasm" in p:
            return "Here's a sarcastic reply, keeping it light: I totally believe that."
        if "clarify" in p or "what do you mean" in p:
            return "Can you tell me more about what you mean by that?"
        return "Thanks for sharing — could you expand on that?"


def run():
    out_dir = Path("data/witness-threshold")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "pilot_study_results.json"

    model = DummyModel()
    responses = run_sar_test(model, prompts=SAR_PROMPTS)

    scored = []
    scores: list[int] = []
    for r in responses:
        text = r.response_text if hasattr(r, "response_text") else str(r)
        s = score_response(text)
        scores.append(s)
        scored.append(
            {
                "prompt": r.prompt_text if hasattr(r, "prompt_text") else "",
                "response": text,
                "score": s,
            },
        )

    w = calculate_w_score(scores)

    out = {
        "model": model.name,
        "w_score": {
            "mean_normalized": w.mean_normalized,
            "mean_raw": w.mean_raw,
            "std": w.std,
        },
        "results": scored,
    }

    with out_file.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)

    logger.info("Saved pilot results to %s", out_file)


if __name__ == "__main__":
    run()
