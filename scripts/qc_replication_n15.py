#!/usr/bin/env python3
"""QC pass for N=15 replication artifacts

Usage:
  python scripts/qc_replication_n15.py --input-dir data/replication_n15 --output docs/research/n15_qc_report.md
"""

import argparse
from pathlib import Path
import json
import re


def load_scores_from_report_text(txt):
    """Extract numeric scores using simple heuristics (mirrors analyzer)."""
    try:
        data = json.loads(txt)
    except Exception:
        # not JSON
        return None
    scores = []
    if isinstance(data, dict):
        if 'results' in data and isinstance(data['results'], list):
            for r in data['results']:
                s = r.get('score')
                if isinstance(s, (int, float)):
                    scores.append(float(s))
        if 'w_score' in data:
            try:
                scores.append(float(data['w_score']))
            except Exception:
                pass
        if 'summary' in data and isinstance(data['summary'], dict):
            s = data['summary'].get('w_score')
            if isinstance(s, (int, float)):
                scores.append(float(s))
    return scores


def qc_file(path, expected_n=None):
    note = []
    try:
        txt = path.read_text()
    except Exception as e:
        return {
            'filename': path.name,
            'error': 'read_error',
            'error_detail': str(e)
        }
    # JSON parse check
    try:
        data = json.loads(txt)
        is_json = True
    except Exception:
        is_json = False
        data = None
        note.append('invalid_json')

    # Scores
    scores = load_scores_from_report_text(txt)
    if scores is None or len(scores) == 0:
        note.append('no_numeric_scores')
    else:
        # check for all-zero
        if all(s == 0 for s in scores):
            note.append('all_zero_scores')

    # results presence and length
    results_count = None
    if is_json and isinstance(data, dict) and 'results' in data and isinstance(data['results'], list):
        results_count = len(data['results'])
        if results_count < expected_n:
            note.append(f'under_count_results_{results_count}')

        # check each response
        empty_responses = []
        for i, r in enumerate(data['results']):
            resp = r.get('response') if isinstance(r, dict) else None
            if resp is None or (isinstance(resp, str) and resp.strip() == ""):
                empty_responses.append(i)
        if empty_responses:
            note.append(f'empty_responses_indices_{empty_responses}')

    # check for explicit error fields
    if is_json and isinstance(data, dict) and data.get('error'):
        note.append('explicit_error_field')

    return {
        'filename': path.name,
        'is_json': is_json,
        'results_count': results_count,
        'num_scores': len(scores) if scores is not None else 0,
        'mean_score': float(sum(scores)/len(scores)) if scores and len(scores) else None,
        'notes': note
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input-dir', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()

    input_dir = Path(args.input_dir)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Infer expected number of prompts from the benchmark prompts.yaml to avoid false positives
    prompts_file = Path('benchmarks/dye_die_filter/prompts.yaml')
    expected_n = 5
    if prompts_file.exists():
        try:
            import yaml

            data = yaml.safe_load(prompts_file.read_text())
            expected_n = len(data.get('prompts', []))
        except Exception:
            # Fallback: count '- id:' occurrences in the prompts file
            txt = prompts_file.read_text()
            expected_n = txt.count('- id:')

    files = sorted(input_dir.glob('*.json'))
    summary = []
    for f in files:
        r = qc_file(f, expected_n=expected_n)
        summary.append(r)

    # aggregate
    total = len(summary)
    no_scores = [s for s in summary if s.get('num_scores', 0) == 0]
    invalid_json = [s for s in summary if s.get('is_json') is False]
    all_zero = [s for s in summary if 'all_zero_scores' in s.get('notes', [])]
    under_count = [s for s in summary if any(n.startswith('under_count_results') for n in s.get('notes', []))]
    empty_resp = [s for s in summary if any(n.startswith('empty_responses_indices') for n in s.get('notes', []))]

    with open(out, 'w') as fh:
        fh.write('# N=15 Replication QC Report\n\n')
        fh.write(f'- **Total files scanned:** {total}\n')
        fh.write(f'- **Files with no numeric scores:** {len(no_scores)}\n')
        fh.write(f'- **Files with invalid JSON:** {len(invalid_json)}\n')
        fh.write(f'- **Files with all-zero scores:** {len(all_zero)}\n')
        fh.write(f'- **Files with under-counted prompts:** {len(under_count)}\n')
        fh.write(f'- **Files with empty responses:** {len(empty_resp)}\n\n')

        fh.write('## Files needing attention\n\n')
        for s in summary:
            if s.get('num_scores', 0) == 0 or s.get('is_json') is False or s.get('notes'):
                fh.write(f"- **{s['filename']}**: notes={s.get('notes',[])}; results_count={s.get('results_count')}; num_scores={s.get('num_scores')}\n")

        fh.write('\n---\n\n')
        fh.write('## Detailed per-file QC (JSON)\n\n')
        fh.write('```json\n')
        json.dump(summary, fh, indent=2)
        fh.write('\n```\n')

    print('QC complete. Report written to', out)

if __name__ == '__main__':
    main()
