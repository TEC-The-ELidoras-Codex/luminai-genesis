#!/usr/bin/env bash
set -euo pipefail

# Minimal, robust demo script for MVP endpoints; uses jq when available for pretty JSON.
HOST="http://localhost:3000"
CLIENT_ID="demo-client-1"

jq_or_cat() { if command -v jq >/dev/null 2>&1; then jq .; else cat; fi }

echo "1) Sending chat message"
payload=$(printf '{"client_id":"%s","message":"%s"}' "$CLIENT_ID" "I had a craving and feel anxious")
curl -s -X POST "$HOST/api/chat" -H 'Content-Type: application/json' -d "$payload" | jq_or_cat || true

echo
echo "2) Logging a craving"
payload=$(printf '{"client_id":"%s","severity":%d,"note":"%s"}' "$CLIENT_ID" 3 "triggered by stress")
curl -s -X POST "$HOST/api/craving" -H 'Content-Type: application/json' -d "$payload" | jq_or_cat || true

echo
echo "3) Login and fetch a report (auth-protected)"
auth_payload=$(printf '{"username":"%s"}' "therapist1")
TOKEN_JSON=$(curl -s -X POST "$HOST/api/login" -H 'Content-Type: application/json' -d "$auth_payload" || true)
TOKEN=$(printf "%s" "$TOKEN_JSON" | sed -n 's/.*"token":\s*"\([^"]*\)".*/\1/p')
echo "Using token: ${TOKEN:0:16}..."
curl -s -H "Authorization: Bearer $TOKEN" "$HOST/api/report/$CLIENT_ID" | jq_or_cat || true

echo
echo "Done."
