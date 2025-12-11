const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const sqlite3 = require("sqlite3").verbose();

const DB_PATH = path.join(__dirname, "..", "database", "luminai.db");
const PORT = process.env.PORT || 3000;

// ensure database folder exists
fs.mkdirSync(path.join(__dirname, "..", "database"), { recursive: true });

// init db
const db = new sqlite3.Database(DB_PATH);
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT,
    message TEXT,
    type TEXT,
    private INTEGER DEFAULT 0,
    created_at INTEGER
  )`);
  db.run(`CREATE TABLE IF NOT EXISTS cravings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT,
    severity INTEGER,
    note TEXT,
    created_at INTEGER
  )`);
  // Ensure migrations: add 'private' column to messages when missing
  db.all("PRAGMA table_info(messages)", (err, cols) => {
    if (err) return;
    const hasPrivate = (cols || []).some((c) => c.name === "private");
    if (!hasPrivate) {
      db.run("ALTER TABLE messages ADD COLUMN private INTEGER DEFAULT 0");
    }
  });
  // Ensure users table exists and has expected columns
  db.all("PRAGMA table_info(users)", (err2, ucols) => {
    if (err2) return;
    if (!ucols || ucols.length === 0) {
      db.run(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, role TEXT, created_at INTEGER)"
      );
    }
  });
});

const app = express();
app.use(cors());
app.use(bodyParser.json());

// serve static client files
app.use("/", express.static(path.join(__dirname, "..", "client")));
app.use("/therapist", express.static(path.join(__dirname, "..", "therapist")));

// API routes
const chatRouter = require("./api/chat")(db);
const reportsRouter = require("./api/reports")(db);
const resourcesRouter = require("./api/resources")(db);
const authRouter = require("./api/auth")(db);
const { requireAuth, requireRole } = require("./middleware/auth");
app.use("/api", chatRouter);
app.use("/api", authRouter);
// protect /report endpoints (therapist role in demo) using requireAuth
// Reports are therapist-facing; require role: 'therapist'
app.use("/api/report", requireAuth);
app.use("/api/report", requireRole("therapist"));
app.use("/api", reportsRouter);
app.use("/api", resourcesRouter);

app.get("/api/ping", (req, res) => res.json({ ok: true }));

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`LuminAI MVP server listening on http://localhost:${PORT}`);
  });
}

module.exports = app;
