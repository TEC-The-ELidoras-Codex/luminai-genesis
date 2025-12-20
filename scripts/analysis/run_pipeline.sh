#!/usr/bin/env bash
set -euo pipefail

# Run the reddit extraction + scoring pipeline.
# Usage:
#   ./scripts/analysis/run_pipeline.sh --url THREAD_URL
#   ./scripts/analysis/run_pipeline.sh --json reddit_thread.json
#   ./scripts/analysis/run_pipeline.sh --test   # run only scoring on the seeded CSV

OUT_CSV="docs/research/witness_data/reddit_megathread_expanded.csv"
SUMMARY="docs/research/witness_data/summary.txt"
SEED_CSV="docs/research/witness_data/reddit_megathread_cases.csv"

function usage() {
  echo "Usage: $0 [--url THREAD_URL | --json FILE | --test] [--out PATH] [--summary PATH]"
  exit 1
}

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found on PATH. Install Python 3 and try again." >&2
  exit 2
fi

if [ "$#" -eq 0 ]; then
  usage
fi

MODE=""
URL=""
JSON=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --url)
      MODE="url"; URL="$2"; shift 2;;
    --json)
      MODE="json"; JSON="$2"; shift 2;;
    --test)
      MODE="test"; shift 1;;
    --out)
      OUT_CSV="$2"; shift 2;;
    --summary)
      SUMMARY="$2"; shift 2;;
    -h|--help)
      usage;;
    *)
      echo "Unknown arg: $1"; usage;;
  esac
done

if [ "$MODE" = "test" ]; then
  echo "Running scoring on existing seed CSV: $SEED_CSV"
  python3 scripts/analysis/compute_witness_scores.py --in "$SEED_CSV" --out "$SUMMARY"
  echo "Summary written to $SUMMARY"
  exit 0
fi

if [ "$MODE" = "url" ]; then
  if [ -z "$URL" ]; then
    echo "--url requires a THREAD_URL"; usage
  fi
  echo "Fetching comments from Pushshift for: $URL"
  python3 scripts/analysis/scrape_reddit_thread.py --url "$URL" --out "$OUT_CSV"
  echo "Extraction complete: $OUT_CSV"
fi

if [ "$MODE" = "json" ]; then
  if [ -z "$JSON" ]; then
    echo "--json requires a path to the exported reddit json file"; usage
  fi
  echo "Loading local JSON: $JSON"
  python3 scripts/analysis/scrape_reddit_thread.py --json "$JSON" --out "$OUT_CSV"
  echo "Extraction complete: $OUT_CSV"
fi

if [ "$MODE" = "url" ] || [ "$MODE" = "json" ]; then
  echo "Scoring extracted CSV -> $SUMMARY"
  python3 scripts/analysis/compute_witness_scores.py --in "$OUT_CSV" --out "$SUMMARY"
  echo "Summary written to $SUMMARY"
fi

echo "Done."
