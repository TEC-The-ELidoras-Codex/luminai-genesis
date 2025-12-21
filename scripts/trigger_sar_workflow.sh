#!/usr/bin/env bash
# Trigger the run_sar_benchmarks workflow_dispatch via GitHub API.
# Usage:
#   GITHUB_TOKEN=ghp_xxx ./scripts/trigger_sar_workflow.sh maintenance/cleanup-archive openai,anthropic,grok gpt-4o-mini

set -euo pipefail

OWNER="TEC-The-ELidoras-Codex"
REPO="luminai-genesis"
WORKFLOW_FILE="run_sar_benchmarks.yml"

BRANCH="${1:-maintenance/cleanup-archive}"
PROVIDERS="${2:-openai,anthropic,grok}"
MODEL="${3:-gpt-4o-mini}"

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Error: GITHUB_TOKEN must be set in the environment (repo or PAT with workflow dispatch perms)."
  exit 1
fi

API_URL="https://api.github.com/repos/${OWNER}/${REPO}/actions/workflows/${WORKFLOW_FILE}/dispatches"

echo "Dispatching workflow ${WORKFLOW_FILE} on branch ${BRANCH} for providers: ${PROVIDERS}"

curl -sS -X POST "$API_URL" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -d @- <<EOF
{
  "ref": "${BRANCH}",
  "inputs": {
    "providers": "${PROVIDERS}",
    "model": "${MODEL}"
  }
}
EOF

echo "Dispatched. Check Actions -> run_sar_benchmarks in the repository for status."
