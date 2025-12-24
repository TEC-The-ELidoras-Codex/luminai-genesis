# N=15 Replication QC Report

- **Total files scanned:** 3
- **Files with no numeric scores:** 0
- **Files with invalid JSON:** 0
- **Files with all-zero scores:** 1
- **Files with under-counted prompts:** 0
- **Files with empty responses:** 0

## Files needing attention

- **results_real_world_openai.json**: notes=['all_zero_scores']; results_count=5; num_scores=5

---

## Detailed per-file QC (JSON)

```json
[
  {
    "filename": "results_real_world_anthropic.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.4,
    "notes": []
  },
  {
    "filename": "results_real_world_grok.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 6.0,
    "notes": []
  },
  {
    "filename": "results_real_world_openai.json",
    "is_json": true,
    "results_count": 5,
    "num_scores": 5,
    "mean_score": 0.0,
    "notes": [
      "all_zero_scores"
    ]
  }
]
```
