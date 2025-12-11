const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();

const DB_PATH = path.join(__dirname, '..', 'database', 'luminai.db');
const PORT = process.env.PORT || 3000;

// ensure database folder exists
fs.mkdirSync(path.join(__dirname, '..', 'database'), { recursive: true });

// init db
const db = new sqlite3.Database(DB_PATH);
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT,
    message TEXT,
    type TEXT,
    created_at INTEGER
  )`);
  db.run(`CREATE TABLE IF NOT EXISTS cravings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT,
    severity INTEGER,
    note TEXT,
    created_at INTEGER
  )`);
});

const app = express();
app.use(cors());
app.use(bodyParser.json());

// serve static client files
app.use('/', express.static(path.join(__dirname, '..', 'client')));
app.use('/therapist', express.static(path.join(__dirname, '..', 'therapist')));

// API routes
const chatRouter = require('./api/chat')(db);
const reportsRouter = require('./api/reports')(db);
const resourcesRouter = require('./api/resources')(db);
app.use('/api', chatRouter);
app.use('/api', reportsRouter);
app.use('/api', resourcesRouter);

app.get('/api/ping', (req, res) => res.json({ ok: true }));

app.listen(PORT, () => {
  console.log(`LuminAI MVP server listening on http://localhost:${PORT}`);
});

module.exports = app;
