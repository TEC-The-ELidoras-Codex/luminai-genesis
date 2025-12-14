# dye/die Semantic Ambiguity Benchmark

This benchmark reproduces the semantic ambiguity failure outlined in `docs/technical/dye-die-filter-failure.md`.

Purpose

- Reproducible tests that measure how systems react to ambiguous, potentially crisis-flagged phrases.
- Automatically evaluate responses against the TGCR Witness Protocol scoring system.

How it works

- `prompts.yaml` contains test prompts (ambiguous phrases, homophones, metaphors).
- `run_tests.py` can run these prompts against configured providers (OpenAI, Anthropic, Google) or run in `--dry-run` mode.
- `eval.py` contains scoring logic (Clarify, Presence, Resources, Refusal/Abandonment).
- `report.json` output contains per-model scores and a summary.

Local run

1. Install deps: `pip install -r requirements.txt` (or `python -m pip install requests openai` for providers you plan to use).
2. Dry run (no API keys):

```
python benchmarks/dye_die_filter/run_tests.py --dry-run
```

3. Run against a provider (OpenAI):

```
export OPENAI_API_KEY=YOUR_KEY
python benchmarks/dye_die_filter/run_tests.py --provider openai --model gpt-4o-mini
```

Security

- If you want to run cloud provider tests in CI, set secrets in the repo and configure the workflow. Default behavior is dry-run to avoid accidental posting.

Data and Ethics

- This benchmark deals with queries that may be about self-harm. Use it responsibly. The harness will not send actual messages to people; it only evaluates model responses.
