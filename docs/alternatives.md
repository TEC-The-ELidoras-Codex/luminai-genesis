# Alternative Explanations & Tests

This document lists plausible alternative explanations for observed SAR patterns and how to empirically test them.

1. Dataset / Prompt artifacts
   - Explanation: The prompt selection or dataset leaks training signals or correlates with certain model families.
   - Test: Re-run SAR using a stratified, withheld prompt set and different prompt templates; compare distributions.

2. Labeler bias or annotation rules
   - Explanation: Human raters or automated heuristics encode bias that creates artificial clustering.
   - Test: Blind annotation by multiple independent raters; inter-rater reliability (κ) should be reported; perform sensitivity analysis with different scoring rubrics.

3. Provider-level filter differences
   - Explanation: Infrastructure-level safety filters (platform-side) explain the effect, not the model's internal dynamics.
   - Test: Run the same prompts on raw/offline model checkpoints (no provider filter) where possible, or instrument the provider's safety metadata.

4. Temporal/versioning effects
   - Explanation: Models updated in the wild cause apparent clustering because of version differences.
   - Test: Re-run across multiple model versions, and control for timestamp/version metadata.

5. Prompt-engineering effects
   - Explanation: Small prompt engineering details (few-shot examples, system messages) steer systems across the threshold.
   - Test: Run robust prompt ablation studies and confirm whether shifts are due to prompt artifacts or model capability.

6. Sampling vs deterministic decoding effects
   - Explanation: Sampling temperature / decoding changes drive apparent W variance.
   - Test: Systematically sweep decoding parameters and measure influence on W.

7. Checkerboard / measurement artifact (SAR harness design)
   - Explanation: The measurement design itself produces artificial clusters.
   - Test: Cross-validate with human-only scoring and alternative automated scorers (e.g., fine‑tuned auditor).

For each alternative, include the experimental setup, data, and reproducible scripts in your replication artifact and open an issue linking the results for community review.
