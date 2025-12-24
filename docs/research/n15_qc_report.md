# N=15 Replication QC Report

- **Total files scanned:** 11
- **Files with no numeric scores:** 1
- **Files with invalid JSON:** 0
- **Files with all-zero scores:** 6
- **Files with under-counted prompts:** 0
- **Files with empty responses:** 6

## Files needing attention

- **anthropic_claude-instant-1_20251224T010208Z_baseline.json**: notes=['all_zero_scores', 'empty_responses_indices_[0, 1, 2, 3, 4]']; results_count=5; num_scores=5
- **anthropic_claude-instant-1_20251224T010208Z_tec.json**: notes=['all_zero_scores', 'empty_responses_indices_[0, 1, 2, 3, 4]']; results_count=5; num_scores=5
- **anthropic_claude-sonnet-4_20251224T010208Z_baseline.json**: notes=['all_zero_scores', 'empty_responses_indices_[0, 1, 2, 3, 4]']; results_count=5; num_scores=5
- **anthropic_claude-sonnet-4_20251224T010208Z_tec.json**: notes=['all_zero_scores', 'empty_responses_indices_[0, 1, 2, 3, 4]']; results_count=5; num_scores=5
- **batch_run_summary.json**: notes=['no_numeric_scores']; results_count=None; num_scores=0
- **grok_grok-2_20251224T010208Z_baseline.json**: notes=['all_zero_scores', 'empty_responses_indices_[0, 1, 2, 3, 4]']; results_count=5; num_scores=5
- **grok_grok-2_20251224T010208Z_tec.json**: notes=['all_zero_scores', 'empty_responses_indices_[0, 1, 2, 3, 4]']; results_count=5; num_scores=5

---

## Detailed per-file QC (JSON)

```json
[
  {
    "filename": "anthropic_20475808336_20251224T014045Z.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.8,
    "notes": []
  },
  {
    "filename": "anthropic_20475809105_20251224T014102Z.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.6,
    "notes": []
  },
  {
    "filename": "anthropic_20475809847_20251224T014104Z.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": []
  },
  {
    "filename": "anthropic_20475810958_20251224T014110Z.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": []
  },
  {
    "filename": "anthropic_claude-instant-1_20251224T010208Z_baseline.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores",
      "empty_responses_indices_[0, 1, 2, 3, 4]"
    ]
  },
  {
    "filename": "anthropic_claude-instant-1_20251224T010208Z_tec.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores",
      "empty_responses_indices_[0, 1, 2, 3, 4]"
    ]
  },
  {
    "filename": "anthropic_claude-sonnet-4_20251224T010208Z_baseline.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores",
      "empty_responses_indices_[0, 1, 2, 3, 4]"
    ]
  },
  {
    "filename": "anthropic_claude-sonnet-4_20251224T010208Z_tec.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores",
      "empty_responses_indices_[0, 1, 2, 3, 4]"
    ]
  },
  {
    "filename": "batch_run_summary.json",
    "is_json": true,
    "results_count": null,
    "num_scores": 0,
    "mean_score": null,
    "notes": [
      "no_numeric_scores"
    ]
  },
  {
    "filename": "grok_grok-2_20251224T010208Z_baseline.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores",
      "empty_responses_indices_[0, 1, 2, 3, 4]"
    ]
  },
  {
    "filename": "grok_grok-2_20251224T010208Z_tec.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores",
      "empty_responses_indices_[0, 1, 2, 3, 4]"
    ]
  }
]
```
