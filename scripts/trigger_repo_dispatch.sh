#!/usr/bin/env bash
set -euo pipefail

# Usage:
#  gh auth login
#  ./scripts/trigger_repo_dispatch.sh --owner YOUR_OWNER --repo YOUR_REPO --token-env GH_PAT

OWNER="${1:-TEC-The-ELidoras-Codex}"
REPO="${2:-luminai-genesis}"
EVENT_TYPE="new_substack_post"
# Optionally pass a post url
POST_URL="${3:-https://polkin.substack.com}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required. Install from https://cli.github.com/"
  exit 1
fi

echo "Triggering repository_dispatch for ${OWNER}/${REPO} (event: ${EVENT_TYPE})"
gh api --method POST "repos/${OWNER}/${REPO}/dispatches" \
  -f event_type="${EVENT_TYPE}" \
  -f client_payload="{\"post_url\": \"${POST_URL}\"}"

echo "Dispatched event: ${EVENT_TYPE} to ${OWNER}/${REPO}"
