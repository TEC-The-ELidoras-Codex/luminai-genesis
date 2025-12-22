#!/usr/bin/env bash
set -euo pipefail
echo "Setting up SQLite database for LuminAI MVP..."
DB_DIR="$(dirname "$0")/../database"
mkdir -p "$DB_DIR"
DB_FILE="$DB_DIR/luminai.db"
if [ -f "$DB_FILE" ]; then
  echo "Db already exists: $DB_FILE"
  exit 0
fi

# Try node first (preferred for parity with JS code). If node is not available,
# fallback to a small Python script using the stdlib sqlite3 module.
if command -v node >/dev/null 2>&1; then
  echo "Using node to create DB schema..."
  # Use node to execute an inline script, passing DB file as the first argument
  node - "$DB_FILE" <<'NODE'
const sqlite3 = require('sqlite3').verbose();
const path = process.argv[1];
if (!path) {
  console.error('DB path argument missing');
  process.exit(2);
}
const db = new sqlite3.Database(path);
db.serialize(() => {
  db.run('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, message TEXT, type TEXT, private INTEGER DEFAULT 0, created_at INTEGER)');
  db.run('CREATE TABLE IF NOT EXISTS cravings (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, severity INTEGER, note TEXT, created_at INTEGER)');
  db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, created_at INTEGER)');
});
db.close((err) => {
  if (err) {
    console.error('Failed to close DB', err);
    process.exit(1);
  }
  console.log('DB created');
});
NODE
  true
elif command -v python3 >/dev/null 2>&1; then
  echo "Node not found; using python3 to create DB schema..."
  python3 - <<'PY'
import sqlite3, sys
db = sqlite3.connect(sys.argv[1])
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, message TEXT, type TEXT, private INTEGER DEFAULT 0, created_at INTEGER)')
cur.execute('CREATE TABLE cravings (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, severity INTEGER, note TEXT, created_at INTEGER)')
db.commit()
db.close()
print('DB created')
PY
else
  echo "Error: neither 'node' nor 'python3' was found on PATH; cannot create DB schema." >&2
  exit 1
fi

echo "Done."
