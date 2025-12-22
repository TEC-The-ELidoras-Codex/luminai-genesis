#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Installing npm dependencies (if missing)..."
npm install

echo "Initializing database (if missing)..."
./scripts/setup_db.sh

echo "Starting server (foreground)..."
npm start

"""Note: Ctrl-C to stop the server. To run in dev mode with auto-reload use: npm run dev"""
