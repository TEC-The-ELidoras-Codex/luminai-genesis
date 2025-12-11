const express = require("express");
const router = express.Router();

module.exports = (db) => {
  // weekly summary endpoint - naive summary (last 7 days messages + cravings)
  router.get("/report/:clientId", (req, res) => {
    const clientId = req.params.clientId;
    const oneWeekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const response = {
      client_id: clientId,
      messages: [],
      cravings: [],
      themes: [],
    };
    // Only include messages where private=0 in general; therapist role middleware
    // ensures the caller is a therapist for this route in demo.
    db.all(
      "SELECT message, type, private, created_at FROM messages WHERE client_id = ? AND created_at >= ? ORDER BY created_at ASC",
      [clientId, oneWeekAgo],
      (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        // rows may include 'private' column; since route is protected to therapist,
        // include all messages (in a real implementation we'd further check consent).
        response.messages = (rows || []).map((r) => ({
          message: r.message,
          type: r.type,
          created_at: r.created_at,
          private: r.private,
        }));
        db.all(
          "SELECT severity, note, created_at FROM cravings WHERE client_id = ? AND created_at >= ? ORDER BY created_at ASC",
          [clientId, oneWeekAgo],
          (err2, cravings) => {
            if (err2) return res.status(500).json({ error: err2.message });
            response.cravings = cravings || [];
            // Naive theme extraction: count keywords
            const text = response.messages
              .map((m) => m.message)
              .join(" ")
              .toLowerCase();
            const themeCounts = {};
            const keywords = [
              "craving",
              "overdose",
              "relapse",
              "panic",
              "trigger",
              "suicide",
              "depressed",
              "anx",
            ];
            for (const kw of keywords) {
              const re = new RegExp(kw, "g");
              const match = text.match(re);
              if (match && match.length) themeCounts[kw] = match.length;
            }
            response.themes = Object.entries(themeCounts).map(([k, v]) => ({
              keyword: k,
              count: v,
            }));
            response.suggested_focus = [];
            if (response.themes.some((t) => t.keyword === "craving"))
              response.suggested_focus.push(
                "Harm reduction + relapse prevention"
              );
            if (
              response.themes.some(
                (t) => t.keyword === "panic" || t.keyword === "anx"
              )
            )
              response.suggested_focus.push(
                "Somatic grounding and anxiety coping"
              );
            if (response.themes.some((t) => t.keyword === "suicide"))
              response.suggested_focus.push(
                'Safety planning and crisis clarification (ask: "What do you mean?")'
              );
            res.json(response);
          }
        );
      }
    );
  });

  return router;
};
