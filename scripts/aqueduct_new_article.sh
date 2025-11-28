#!/usr/bin/env bash
# LuminAI Genesis — Aqueduct: create a new article memo (multi-channel)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INBOX_DIR="$ROOT_DIR/docs/streams/articles/inbox"

mkdir -p "$INBOX_DIR"

TITLE="${1:-Untitled article}"
SLUG="$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')"
DATE="$(date +%Y-%m-%d)"
TS="$(date +%Y%m%d-%H%M%S)"

FILE="$INBOX_DIR/${DATE}-${SLUG:-article}-${TS}.md"

cat > "$FILE" <<EOF
---
title: "$TITLE"
slug: "$SLUG"
date_created: $DATE
date_updated: $DATE
status: inbox
channels:
  - substack
persona: LuminAI 🧠
tags: []
sources: []
related_docs: []
publish_log: []
---

# $TITLE

<!-- Drop your notes or paste research here. -->
EOF

echo "📥 Created: $FILE"
