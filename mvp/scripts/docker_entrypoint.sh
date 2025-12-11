#!/usr/bin/env bash
set -euo pipefail

echo "Running DB setup (if needed)..."
./scripts/setup_db.sh

echo "Starting Node server..."
exec node server/app.js
