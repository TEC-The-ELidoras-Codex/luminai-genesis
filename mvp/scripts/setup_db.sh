#!/usr/bin/env bash
set -e
echo "Setting up SQLite database for LuminAI MVP..."
DB_DIR="$(dirname "$0")/../database"
mkdir -p "$DB_DIR"
DB_FILE="$DB_DIR/luminai.db"
if [ -f "$DB_FILE" ]; then
  echo "Db already exists: $DB_FILE"
else
  node -e "const sqlite3=require('sqlite3').verbose(); const db=new sqlite3.Database('$DB_FILE'); db.serialize(()=>{db.run('CREATE TABLE messages (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, message TEXT, type TEXT, created_at INTEGER)'); db.run('CREATE TABLE cravings (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, severity INTEGER, note TEXT, created_at INTEGER)');}); db.close(); console.log('DB created');"
fi
echo "Done."
