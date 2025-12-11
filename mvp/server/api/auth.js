const express = require("express");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const router = express.Router();

// NOTE: This is a demo-only auth route. In a real deployment, use a proper
// user store, password hashing and secure key management.
const JWT_SECRET = process.env.JWT_SECRET || "dev-secret-key";

module.exports = (db) => {
  // Register endpoint (creates new user with username + password + role)
  router.post("/register", async (req, res) => {
    const { username, password, role = "client" } = req.body || {};
    if (!username || !password)
      return res.status(400).json({ error: "username and password required" });
    const created_at = Date.now();
    const hashed = bcrypt.hashSync(password, 8);
    db.run(
      "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)",
      [username, hashed, role, created_at],
      function (err) {
        if (err) {
          // Unique username constraint: return 409 for conflict
          if (
            (err.message && err.message.includes("UNIQUE")) ||
            err.code === "SQLITE_CONSTRAINT"
          ) {
            return res.status(409).json({ error: "username already exists" });
          }
          return res.status(500).json({ error: err.message });
        }
        res.json({ ok: true, id: this.lastID });
      }
    );
  });

  // Login endpoint verifies username/password and returns token
  router.post("/login", (req, res) => {
    const { username, password, role: roleClaim } = req.body || {};
    if (!username) return res.status(400).json({ error: "username required" });
    // lookup user
    db.get(
      "SELECT id, username, password, role FROM users WHERE username = ?",
      [username],
      (err, row) => {
        if (err) return res.status(500).json({ error: err.message });
        if (!row) {
          // Backward demo behavior: if no registered user, allow token with provided role (demo-only)
          const payload = { username, role: roleClaim || "client" };
          const token = jwt.sign(payload, JWT_SECRET, { expiresIn: "7d" });
          return res.json({ ok: true, token, role: payload.role });
        }
        // verify password
        if (!password)
          return res.status(400).json({ error: "password required" });
        const isValid = bcrypt.compareSync(password, row.password);
        if (!isValid)
          return res.status(401).json({ error: "invalid credentials" });
        const payload = { username: row.username, role: row.role };
        const token = jwt.sign(payload, JWT_SECRET, { expiresIn: "7d" });
        res.json({ ok: true, token, role: row.role });
      }
    );
  });

  return router;
};
