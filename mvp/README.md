LuminAI Continuity Partner - MVP
=================================

This folder contains an MVP scaffold for the LuminAI Continuity Partner:

- Node.js + Express backend (simple endpoints)
- SQLite database for initial storage
- Client chat UI (simple HTML/JS)
- Therapist report UI (simple HTML/JS)

This is an early prototype for testing the approach; it is not production-ready or HIPAA-compliant.

Run (local dev):

1. cd mvp
2. npm install
3. npm start

Visit: http://localhost:3000

Key endpoints:
- POST /api/chat -> log a message / get placeholder response
- POST /api/craving -> log craving/relapse event
- GET /api/report/:clientId -> get a weekly summary

--
Files created to accelerate a pilot:
- server/app.js
- server/api/chat.js
- server/api/reports.js
- client/chat/index.html
- therapist/reports/index.html

To do: refine models, add authentication, add privacy controls & encryption.

