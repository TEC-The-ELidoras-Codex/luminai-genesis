const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const sqlite3 = require("sqlite3").verbose();

// In tests, use an in-memory sqlite database to keep runs hermetic and avoid
// file-system race conditions that can surface as stream errors.
const DB_PATH =
  process.env.NODE_ENV === "test"
    ? ":memory:"
    : path.join(__dirname, "..", "database", "luminai.db");
const PORT = process.env.PORT || 3000;

// ensure database folder exists
fs.mkdirSync(path.join(__dirname, "..", "database"), { recursive: true });

// init db
// eslint-disable-next-line no-console
console.log("Using sqlite database at:", DB_PATH);
const db = new sqlite3.Database(DB_PATH);
// initialize DB schema with a single exec to ensure tables exist before handling
// requests. We also expose app.locals.dbReady as a promise that resolves after
// the SQL exec completes so tests can await it.
const initSql = `
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id TEXT,
  message TEXT,
  type TEXT,
  private INTEGER DEFAULT 0,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS cravings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id TEXT,
  severity INTEGER,
  note TEXT,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password TEXT,
  role TEXT,
  created_at INTEGER
);
`;

let resolveDbReady;
const dbReady = new Promise((resolve, reject) => {
  resolveDbReady = resolve;
});

db.exec(initSql, (err) => {
  if (err) {
    // eslint-disable-next-line no-console
    console.error("DB initialization error:", err);
  }
  resolveDbReady();
});

const app = express();
// expose db and readiness promise through app.locals for test harnesses or external tooling to close
app.locals.db = db;
app.locals.dbReady = dbReady;
app.use(cors());
app.use(bodyParser.json());

// Attach a generic response error handler for all requests so we can log
// and surface any streaming errors that might happen while piping files
// or other readable streams to the response.
app.use((req, res, next) => {
  req.on("error", (err) => {
    // eslint-disable-next-line no-console
    console.error("Request stream error:", err);
  });
  res.on("error", (err) => {
    // eslint-disable-next-line no-console
    console.error("Response stream error:", err);
  });
  next();
});

// Global error handling for unexpected errors and promise rejections to help
// CI debugging and avoid silent process crashes from readable stream errors.
process.on("unhandledRejection", (reason, promise) => {
  // eslint-disable-next-line no-console
  console.error("Unhandled Rejection at:", promise, "reason:", reason);
});
process.on("uncaughtException", (err) => {
  // eslint-disable-next-line no-console
  console.error("Uncaught Exception:", err);
  // rethrow to allow CI or supervisors to pick up a crash; useful for tests
  // so failures are visible instead of silent stream errors.
  throw err;
});

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

// Global express error handler (captures synchronous and async errors)
app.use((err, req, res, next) => {
  // eslint-disable-next-line no-console
  console.error("Express error:", err && err.stack ? err.stack : err);
  if (res.headersSent) return next(err);
  res.status(500).json({ error: "Internal server error" });
});

app.get("/api/ping", (req, res) => res.json({ ok: true }));

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`LuminAI MVP server listening on http://localhost:${PORT}`);
  });
}

module.exports = app;
