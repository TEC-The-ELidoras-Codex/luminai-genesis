# LuminAI Continuity Partner - MVP Architecture

This file provides a short overview of the MVP architecture so collaborators can quickly get oriented and contribute.

## Overview

- Backend: Node.js + Express hosting a tiny REST API. It serves static HTML client pages and a few simple API endpoints used for the demo.
- Storage: SQLite database stored at `./database/luminai.db` — tables `messages` and `cravings`.
- Client: Static HTML + JS served from `/client` and a therapist UI from `/therapist`.

## Endpoints

- POST `/api/chat` — accepts JSON payload {client_id, message, private?}. Stores incoming messages, returns short clarify-first reply. Reply also stored as a `response` type message for therapist access.
- POST `/api/craving` — accepts JSON payload {client_id, severity, note}. Logs a craving event.
- GET `/api/report/:clientId` — returns a naive weekly summary of messages & cravings and simple theme extraction based on keyword matches.
- GET `/api/resources` — returns static curated harm reduction resources (prototype).
- POST `/api/login` — returns a demo JWT token (username only) for protected endpoints such as `/api/report`.

## DB schema

- messages: id, client_id, message, type, created_at
- cravings: id, client_id, severity, note, created_at

## Key behaviors

- Clarify-first safety behavior: If a message contains terms that hint at imminent self-harm (keywords defined in `server/api/chat.js`), the server replies asking for clarification before offering specific crisis resources — this reduces false positives and follows the planned witness-first approach.
- Naive theme extraction in the `/report` endpoint is for demo use only.

## Auth & demo flows

- A minimal JWT-based login endpoint is included for demo use only. The `/api/report` endpoint requires a valid JWT. This is a lightweight demonstration of an auth/protected flow and should be replaced or extended with a proper user store and auth provider in production.

## How to run locally

1. Install dependencies: `npm install`
2. Create DB: `./scripts/setup_db.sh` (it uses Node or Python3 as a fallback)
3. Start the server: `npm start`
4. Visit `http://localhost:3000` to try the client, `http://localhost:3000/therapist/reports/index.html` for therapist prototype.

## Next suggested steps for contributors

1. Add authentication and data access controls using JWT + roles (client/therapist/admin).
2. Replace SQLite with a secure backend or add encryption-at-rest + field-level encryption for PHI.
3. Implement audit logging for access to client records.
4. Convert resources endpoint to dynamic, moderated dataset with localization features.
5. Build automated unit/integration tests and CI steps for the server.

## Acknowledgement

This scaffold was implemented as a solo prototype to accelerate pilot planning — feedback and collaboration are welcome! The goal is to be functional enough to get human collaborators and therapists to iterate and make it production-ready.
