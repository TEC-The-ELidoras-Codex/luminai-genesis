#!/usr/bin/env bash
set -euo pipefail

APP_ID=2186310
PRIV_KEY="${HOME}/luminai-key.pem"
REPO_OWNER="Elidorascodex"
REPO="luminai-genesis"
HEAD="feat/ultimate-checklist"
BASE="main"
BODY_FILE="pr_body.json"

# Prechecks
if [[ ! -f "$PRIV_KEY" ]]; then
  echo "ERROR: Private key not found at $PRIV_KEY" >&2
  exit 1
fi
if [[ ! -f "$BODY_FILE" ]]; then
  echo "ERROR: PR body file not found: $BODY_FILE" >&2
  exit 1
fi
command -v jq >/dev/null || { echo "ERROR: jq missing; sudo apt update && sudo apt install -y jq" >&2; exit 1; }
command -v openssl >/dev/null || { echo "ERROR: openssl missing" >&2; exit 1; }

# Build JWT
now=$(date +%s)
iat=$((now - 60))
exp=$((now + 600))
header_b64=$(printf '%s' '{"alg":"RS256","typ":"JWT"}' | openssl base64 -A | tr '+/' '-_' | tr -d '=')
payload_b64=$(printf '%s' "{\"iat\":$iat,\"exp\":$exp,\"iss\":$APP_ID}" | openssl base64 -A | tr '+/' '-_' | tr -d '=')
unsigned="${header_b64}.${payload_b64}"
sig=$(printf '%s' "$unsigned" | openssl dgst -sha256 -sign "$PRIV_KEY" | openssl base64 -A | tr '+/' '-_' | tr -d '=')
JWT="${unsigned}.${sig}"
echo "JWT created (len ${#JWT})"

# Get installation id for repo
INSTALL_INFO=$(curl -s -H "Authorization: Bearer $JWT" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO_OWNER/$REPO/installation")
if echo "$INSTALL_INFO" | jq -e '.id' >/dev/null 2>&1; then
  INSTALL_ID=$(echo "$INSTALL_INFO" | jq -r '.id')
  echo "Found installation id: $INSTALL_ID"
else
  echo "ERROR: Could not find installation id for repo. Response:"
  echo "$INSTALL_INFO" | jq
  exit 1
fi

# Create installation token
TOKEN_JSON=$(curl -s -X POST -H "Authorization: Bearer $JWT" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/app/installations/$INSTALL_ID/access_tokens")
INSTALL_TOKEN=$(echo "$TOKEN_JSON" | jq -r '.token // empty')
if [[ -z "$INSTALL_TOKEN" ]]; then
  echo "ERROR: Could not create installation token. Response:"
  echo "$TOKEN_JSON" | jq
  exit 1
fi
echo "Got installation token (len ${#INSTALL_TOKEN})"

# Check existing PR
existing=$(curl -s -H "Authorization: token $INSTALL_TOKEN" \
  "https://api.github.com/repos/$REPO_OWNER/$REPO/pulls?head=$REPO_OWNER:$HEAD&base=$BASE")
if [[ "$(echo "$existing" | jq 'length')" != "0" ]]; then
  echo "PR already exists: $(echo "$existing" | jq -r '.[0].html_url')"
  exit 0
fi

# Create PR
PR_JSON=$(curl -s -X POST -H "Authorization: token $INSTALL_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$REPO_OWNER/$REPO/pulls" -d @"$BODY_FILE")
echo "PR creation response:"
echo "$PR_JSON" | jq -r '.html_url, .number, .message'
