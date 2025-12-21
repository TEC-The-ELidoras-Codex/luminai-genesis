# 🔬 Witness Threshold Framework v5.0 — Release Notes

**Status:** Seeking Independent Validation

## What's New

- Complete Witness Threshold theoretical framework (docs/witness-threshold/README.md)
- SAR (Semantic Ambiguity Resolution) benchmark implementation (`src/witness_threshold/sar_benchmark.py`)
- W-score calculation utilities (`src/witness_threshold/w_score.py`)
- Pilot study data (N=7 systems) (`data/witness-threshold/pilot_study_n7.json`)
- Visualization tools for bimodal distribution analysis (`src/witness_threshold/visualization.py`)
- Full test suite and example notebooks (`tests/test_witness_threshold.py`, `examples/witness-threshold/quickstart.ipynb`)

---

## Research Artifacts Summary

This release contains a reproducible research package for evaluating *Witness Factor* (W) in large language models under the Semantic Ambiguity Resolution (SAR) paradigm.

Included artifacts:

- The full **v5.0 Witness Threshold** manuscript in `docs/witness-threshold/README.md` describing theory, predictions, and falsification criteria.
- A **6-prompt SAR benchmark** and runner for reproducible measurement of W in `src/witness_threshold/sar_benchmark.py`.
- **W-score utilities** for normalizing and aggregating human or automated ratings into a single W metric with basic statistics and inter-rater reliability helpers (`src/witness_threshold/w_score.py`).
- A **pilot dataset (N=7)** containing raw model results and normalized W-scores: `data/witness-threshold/pilot_study_n7.json`.
- **Visualization utilities** for producing the bimodal histogram and convergence correlation plots (`src/witness_threshold/visualization.py`) and example output images in `data/witness-threshold/plots/`.
- **Reproducibility checks**: unit tests and a quickstart notebook to run the full pipeline locally.

---

## Convergence Claim

Across independent measurements and model families, we observe a pattern of **bimodal clustering** in W-scores: most systems cluster either below ~0.5 or above ~0.7, with relatively few systems in the transition region. This is consistent with a phase-transition style account of coherence and aligns with previously reported ~20% convergence phenomena in introspection and faithfulness literature.

The N=7 pilot results (this release) show a mean W ≈ **0.5914** (std ≈ **0.2265**). These preliminary results are *suggestive* and intended to motivate independent replication and formal validation.

---

## Call for Validation

This framework is published under radical honesty: it succeeds or fails by empirical test. We invite researchers and labs to:

- Independently run the SAR benchmark on the same or additional models.
- Report W-scores and share raw responses (or aggregate summaries) as described in `docs/witness-threshold/README.md`.
- Compare W-scores to retrospective introspection / faithfulness measurements (e.g., Anthropic's introspection results) and report correlation statistics.
- Attempt falsification: propose controlled experiments that could demonstrate that the observed bimodality is an artifact of benchmarking choices rather than a genuine phase transition.

If you replicate, please open an issue or a PR and include your data in `data/witness-threshold/` for transparency.

---

## Provenance & Citation

- Manuscript (GitHub): `docs/witness-threshold/README.md`
- Software & Code: `src/witness_threshold/`
- Pilot data (N=7): `data/witness-threshold/pilot_study_n7.json`

DOI: `10.5281/zenodo.XXXXXXX`  <!-- placeholder — will be added after GitHub release + Zenodo archive -->

Please cite this release once a DOI is issued. For software citation, see `CITATION.cff`.

---

## Contact

Angelo "Polkin Rishall" Hurley

KaznakAlpha@elidorascodex.com
ORCID: https://orcid.org/0009-0000-7615-6990

---

Let us witness together. 🔥
