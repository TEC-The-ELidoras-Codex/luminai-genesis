# LuminAI Continuity Partner - MVP

This folder contains an MVP scaffold for the LuminAI Continuity Partner:

- Node.js + Express backend (simple endpoints)
- SQLite database for initial storage
- Client chat UI (simple HTML/JS)
- Therapist report UI (simple HTML/JS)

This is an early prototype for testing the approach; it is not production-ready or HIPAA-compliant.

Quick start (local dev) ✅

Prerequisites:

- Node.js (>=14) or Python3 (for DB setup)
- npm

1. cd mvp
2. npm install
3. ./scripts/setup_db.sh # creates database at ./database/luminai.db
4. npm start

Visit the demo at: http://localhost:3000

Included pages

- Client chat: /index.html (interactive client UI)
- Harm reduction resources: /resources.html
- Therapist portal: /therapist/reports/index.html

Key API endpoints

- POST /api/chat

  - body: { client_id, message, private? }
  - Stores the message and returns a short, clarify-first reply (prototype safety behavior).

- POST /api/craving

  - body: { client_id, severity (1-5), note }
  - Logs a craving/relapse event for the client.

- GET /api/report/:clientId
  - Returns a naive weekly summary of messages/cravings and simple theme extraction.

Example commands (using curl)

1. POST a chat message (client):

```
curl -X POST http://localhost:3000/api/chat \
	-H 'Content-Type: application/json' \
	-d '{"client_id":"client123","message":"I feel anxious and had a craving last night"}'
```

2. POST a craving event:

```
curl -X POST http://localhost:3000/api/craving \
	-H 'Content-Type: application/json' \
	-d '{"client_id":"client123","severity":4,"note":"after seeing a triggering post"}'
```

3. Fetch weekly summary:

```
curl http://localhost:3000/api/report/client123
```

4. POST a private message (client-side):

```
curl -X POST http://localhost:3000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"client_id":"client123","message":"This is private","private":true}'
```

Troubleshooting & notes ⚠️

- If ./scripts/setup_db.sh exits with 'node not found', install Node.js or ensure Python3 is available — the script falls back to Python.
- This MVP is intentionally small and synchronous; it's built to show the approach and to make it easy for a single developer to iterate on quickly.

Files created to accelerate a pilot (snapshot)

- server/app.js
- server/api/chat.js
- server/api/reports.js
- server/api/resources.js
- client/chat/index.html
- client/resources.html
- therapist/reports/index.html

Next steps (for the pilot)

- Add authentication and encrypted storage for PHI before enrolling participants.
- Add integration tests and an automated startup script for staging deployment.
- Expand resource curation and include localization.

Quick demo

The README contains example `curl` commands above that exercise the key endpoints (`/api/chat`, `/api/craving`, `/api/report`). Use those example commands to test the server quickly. The `npm` scripts `setup-db` and `demo` are available for convenience; run `npm run setup-db` to create the DB, and use the curl examples to exercise the API.

Author & status

- Built solo as a prototype scaffold to accelerate pilot planning — enough to show the idea and iterate with human partners.
- Not production-ready: please treat this as a research/dev prototype and do not collect PHI without proper safeguards.

If you'd like, I can add a one-command script to run the whole demo (install, db init, start) and a tiny Dockerfile for staging.

Auth (demo-only)

This MVP includes a minimal JWT login endpoint for demonstration purposes. POST a username to `/api/login` to receive a token, then set `Authorization: Bearer <token>` for protected routes (the `/api/report` route is protected).

Example:

Register a user (demo):

```
curl -X POST http://localhost:3000/api/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"therapist1","password":"secret","role":"therapist"}'
```

Login with username/password to receive a token:

```
curl -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' -d '{"username":"therapist1","password":"secret"}'
curl -X POST http://localhost:3000/api/login -H 'Content-Type: application/json' -d '{"username":"therapist1","role":"therapist"}'
```

Then use the token to fetch a report:

```
curl -H "Authorization: Bearer <token>" http://localhost:3000/api/report/client123
```

Docker & staging

Build and run with Docker (optional):

```
cd mvp
docker build -t luminai-mvp .
docker run -p 3000:3000 -v $(pwd)/database:/app/database -e JWT_SECRET=dev-secret-key luminai-mvp
```

Or use docker-compose:

```
cd mvp
docker-compose up --build
```

Running tests

Install dev dependencies and run tests:

```
cd mvp
npm install
npm test
```
