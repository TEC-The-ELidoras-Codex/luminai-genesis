#!/usr/bin/env bash
set -euo pipefail

# Fetch secrets from Bitwarden and write to .env.local (overwrites existing values for mapped keys)
# Requirements: bw (Bitwarden CLI), jq
# Usage: ./scripts/fetch-secrets-from-bw.sh

SECRETS_MAP="secrets/secret-map.json"
OUT_FILE=".env.local"

if [ ! -f "$SECRETS_MAP" ]; then
  echo "Secrets map $SECRETS_MAP not found. Create and map your Bitwarden items there." >&2
  exit 1
fi

if ! command -v bw >/dev/null 2>&1; then
  echo "Error: bw (Bitwarden CLI) not found. Install from https://bitwarden.com/help/cli/" >&2
  exit 1
fi

# Ensure jq
if ! command -v jq >/dev/null 2>&1; then
  echo "Error: jq not found. Please install jq." >&2
  exit 1
fi

# Login using client credentials if BW_SESSION is not set
if [ -z "${BW_SESSION:-}" ]; then
  if [ -n "${BW_CLIENTID:-}" ] && [ -n "${BW_CLIENTSECRET:-}" ]; then
    echo "Logging into Bitwarden using client credentials..."
    BW_SESSION=$(bw login --client "$BW_CLIENTID" --secret "$BW_CLIENTSECRET" --raw)
    export BW_SESSION
  else
    echo "BW_SESSION not set and BW_CLIENTID/BW_CLIENTSECRET not provided. Please login interactively: bw login or export BW_SESSION." >&2
    exit 1
  fi
fi

tmpfile="${OUT_FILE}.tmp"
touch "$tmpfile"

# Preserve existing non-mapped variables from current .env.local if present
if [ -f "$OUT_FILE" ]; then
  # copy existing lines that don't match mapped env names
  jq -r '.mappings[].env' "$SECRETS_MAP" | while read -r mapped; do
    # build a grep -v pattern
    patterns+=("^${mapped}=")
  done
  if [ ${#patterns[@]} -gt 0 ]; then
    # invert match of mapped keys
    grep -Ev "${patterns[*]}" "$OUT_FILE" >> "$tmpfile" || true
  else
    cat "$OUT_FILE" >> "$tmpfile"
  fi
fi

echo "# Generated .env.local (from Bitwarden)" > "$tmpfile"

jq -c '.mappings[]' "$SECRETS_MAP" | while read -r mapping; do
  envname=$(echo "$mapping" | jq -r '.env')
  item=$(echo "$mapping" | jq -r '.bw_item')
  field=$(echo "$mapping" | jq -r '.field')

  echo "Fetching $envname from Bitwarden item '$item' field '$field'..."
  item_json=$(bw get item "$item" --session "$BW_SESSION" 2>/dev/null || true)
  if [ -z "$item_json" ]; then
    echo "Warning: item $item not found or not accessible. Skipping $envname." >&2
    continue
  fi
  # try fields[] name match
  value=$(echo "$item_json" | jq -r --arg fld "$field" '.fields[]? | select(.name==$fld) | .value' | head -n1)
  if [ -z "$value" ] || [ "$value" = "null" ]; then
    # try login.password
    value=$(echo "$item_json" | jq -r '.login.password // empty')
  fi
  if [ -z "$value" ]; then
    echo "Warning: no value found for $envname in item $item. Skipping." >&2
    continue
  fi
  # Escape any newline characters
  safe_value=$(printf '%s' "$value" | sed ':a;N;$!ba;s/\n/\n/g')
  echo "${envname}=${safe_value}" >> "$tmpfile"
done

mv "$tmpfile" "$OUT_FILE"
chmod 600 "$OUT_FILE"
echo "Written $OUT_FILE with fetched secrets (safely)."
