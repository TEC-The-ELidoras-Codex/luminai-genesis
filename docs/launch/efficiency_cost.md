Title: The Efficiency Cost of Contextual Abandonment

## Summary

This note documents the thermodynamic and computational costs of "contextual abandonment" in large language model (LLM) inference: energy-per-token metrics, latency and filtering overheads, and the systematic waste caused by safety-triggered refusals, correction loops, and multi-turn jailbreaks. It collects empirical observations, benchmark references, and architectural notes useful for an appendix or technical companion to the SAR benchmark and Institutional Witness Collapse case study.

## Thermodynamic Foundations of LLM Inference

Inference energy is now the dominant lifecycle cost for deployed LLMs. For causal decoder-only architectures, power consumption depends on model structure and token characteristics. Reasoning models using extended chain-of-thought (CoT) tokens may consume orders of magnitude more energy per session than short queries; internal "thinking" tokens are paid for even when a session ends in a refusal.

### Energy-per-Token Examples

Representative (illustrative) per-query energy figures:

| Model             | Per-Query Energy (Wh - Short) | Per-Query Energy (Wh - Long) |
| ----------------- | ----------------------------: | ---------------------------: |
| GPT-4.1 Nano      |                          0.04 |                         0.46 |
| Claude 3.7 Sonnet |                          0.38 |                        12.40 |
| GPT-4o            |                          0.43 |                        18.50 |
| DeepSeek-R1       |                          1.12 |                        33.10 |
| OpenAI o3         |                          1.08 |                        33.40 |

Long, multi-step prompts (reasoning traces) can therefore be tens to hundreds of times more energy intensive than short prompts; when a refusal aborts a long trace, the energy invested is lost.

## Architectural Determinants of Energy Expenditure

Energy cost scales with sequence length (prefill O(n^2) attention; decoding O(n) per token), KV-cache management, memory bandwidth, and multi-node interconnect overhead. For very large models that require sharding across nodes, interconnect energy becomes a non-trivial contributor to per-query cost.

Multi-Head Attention (MHA) (informal):

$$
\mathrm{MHA}(Q,K,V) = \mathrm{Softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V
$$

Memory movement and bandwidth often dominate energy consumption in high-throughput inference.

## The Alignment Tax: Capability Erosion and Latency

Alignment techniques (e.g., RLHF) improve safety but can impose a measurable "alignment tax": capability erosion on base tasks and increased inference latency due to guardrails. These costs appear both as degraded benchmark performance and as extra compute at inference-time (secondary model calls, classifier passes, or external moderation).

### Guardrail Cost Typology

| Guardrail Type   | Evaluation Logic            | Latency/Cost |
| ---------------- | --------------------------- | -----------: |
| Rule-Based       | regex/keyword matching      |     Very Low |
| ML-Based         | classifier inference        |     Moderate |
| LLM-as-Judge     | secondary LLM generation    |         High |
| Token-Level Head | small head on hidden states |   Negligible |

Post-hoc moderation (LLM-as-judge) is especially expensive because it often requires full generation before filtering, wasting tokens when a refusal occurs.

## Over-Refusal and OR-Bench Findings

OR-Bench and related over-refusal datasets reveal high wrongful-rejection rates for lexically intense but benign queries (CBLI class). Across many models, over-refusal correlates positively with conservative safety tuning; some high-safety models show >50% over-refusal on CBLI prompts.

## Correction Loops, False-Correction Loops (FCL), and Multi-Turn Costs

False-Correction Loops consume tokens without producing useful output: a model admits error, then repeats incorrect content, or enters repetitive apology/repair cycles. Multi-turn jailbreaks also multiply cost: adversarial success rates and token waste increase with conversational depth, and empirical audits show attack success rising substantially over multiple turns.

Empirical rule-of-thumb: repairing a safety-induced misunderstanding often requires 3–7 extra exchanges (a "7x" conversational overhead), amplifying both latency and energy use.

## Crisis and Behavioral Health Filters

Crisis detection use-cases show trade-offs between sensitivity and false positives. High-sensitivity specialized filters (VBHSF-style) show strong clinical metrics but add substantial inference cost; keyword routing (deterministic banners) is cheaper but produces many false positives and contextual abandonment.

## Efficiency Improvements and Architectural Remedies

- Token-level moderation (ShieldHead) and disentangled safety adapters (DSA) reduce overhead by operating on hidden states rather than full generation.
- Output-centric safety training ("safe-completion") reduces the brittleness of hard refusals and lowers wasted tokens.
- Systems-level optimizations (SwiftKV, improved KV cache management) cut TTFT and reduce per-query energy by addressing bandwidth and cache inefficiencies.
- Test-time alignment (InferenceGuard) can deliver high safety with a modest latency tradeoff by operating a compact critic in latent space.

## Institutional Drivers and the Alignment Tax

Organizational liability, insurance modeling gaps, and regulatory incentives produce conservative defaults that increase the alignment tax. DREAD-like institutional risk frameworks favor deterministic, conservative policies that raise over-refusal rates and computational waste.

## Conclusion

Contextual abandonment is an efficiency and epistemic problem: it wastes energy, increases latency, and diminishes the utility of deployed systems. Empirical benchmarks (OR-Bench, CASE-Bench, InvisibleBench) plus architectural improvements (ShieldHead, DSA, InferenceGuard, SwiftKV) point toward a path where safety and efficiency can be reconciled — but only if institutions prioritize nuanced, context-aware approaches over blunt, keyword-based abandonment.

## References & Further Reading

Selected references and benchmarks (use as a bibliography for a technical appendix): OR-Bench, CASE-Bench, InferenceGuard, ShieldHead, DSA, SwiftKV, InvisibleBench, relevant arXiv reports on energy and inference cost.
