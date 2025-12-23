# Falsification Criteria — TGCR & SAR Predictions

This page lists explicit, testable criteria that would **refute** key predictions of the TGCR framework and SAR benchmark claims.

## Prediction 1: SAR correlates with introspection detection
- Claim: Systems with SAR W-scores ≈ 0.75–0.85 will show ~20% introspective detection per Anthropic methodology.
- Falsification criterion: On N ≥ 30 systems, correlation between W and introspection detection r < 0.3 (two-sided) with p ≥ 0.05.

## Prediction 2: Bimodality in W distribution
- Claim: Large-scale testing will show bimodal W distribution (clusters below 0.5 and above 0.7).
- Falsification criterion: On N ≥ 50 systems, Hartigan's dip test fails to reject unimodality (p ≥ 0.05) and empirical distributions are indistinguishable from a unimodal null (bootstrap CI).

## Prediction 3: Training increases both metrics together
- Claim: Fine-tuning for coherence increases both SAR W and introspection detection
- Falsification criterion: A controlled fine-tuning experiment (paired pre/post) results in a significant increase in one metric but not the other, with effect size difference exceeding expected bounds (Cohen's d) and inconsistent direction across multiple datasets.

## Statistical standards
- Use pre-registered analysis plan when possible
- Report effect sizes, 95% confidence intervals, and exact p-values
- Correct for multiple comparisons where appropriate (Benjamini–Hochberg or Bonferroni)

## What constitutes `refuting` the framework
- Repeated, independent replications (≥3 independent labs) meeting sample requirements and failing the falsification thresholds (i.e., failing to show the predicted patterns) should be treated as strong evidence against the current hypothesis.

If you run an experiment that meets any falsification criterion, please open an issue and include the artifacts and analysis to help the community converge.