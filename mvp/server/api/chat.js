const express = require('express');
const router = express.Router();

module.exports = (db) => {
  // simple chat receive endpoint; logs message and returns placeholder reply
  router.post('/chat', (req, res) => {
    const { client_id = 'anon', message = '', type = 'message', private = false } = req.body;
    const createdAt = Date.now();
    db.run(
      'INSERT INTO messages (client_id, message, type, created_at) VALUES (?, ?, ?, ?)',
      [client_id, message, type, createdAt],
      function (err) {
        if (err) return res.status(500).json({ error: err.message });
        // Minimal clarify-first safety behavior
        const lower = message.toLowerCase();
        const distressKeywords = ['suicide', "end it", 'die', 'i want to die', 'kill myself', 'overdose'];
        const triggered = distressKeywords.some((kw) => lower.includes(kw));
        let replyText = 'Thank you for sharing — I hear you. Would you like to tell me more?';
        if (triggered) {
          // Clarify first instead of immediate resource dump
          replyText = "I hear that you're sharing something heavy. Can you tell me more about what you mean?";
        }
        const reply = {
          text: replyText,
          created_at: Date.now(),
        };
        // do not log replies as private; store as therapist-facing if not private
        db.run('INSERT INTO messages (client_id, message, type, created_at) VALUES (?, ?, ?, ?)',
          [client_id, reply.text, 'response', reply.created_at]);
        res.json({ reply });
      }
    );
  });

  // craving logger (substance use events)
  router.post('/craving', (req, res) => {
    const { client_id = 'anon', severity = 1, note = '' } = req.body;
    const createdAt = Date.now();
    db.run(
      'INSERT INTO cravings (client_id, severity, note, created_at) VALUES (?, ?, ?, ?)',
      [client_id, severity, note, createdAt],
      function (err) {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ ok: true, id: this.lastID });
      }
    );
  });

  return router;
};
