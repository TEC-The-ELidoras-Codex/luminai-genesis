Copilot instructions — LuminAI Genesis

Purpose
-------
Short, actionable guidance for AI coding agents to be productive in this repo.

Quick start (dev workflow)
--------------------------
- Open the repository root workspace (`luminai-genesis.code-workspace`) so VS Code shows the whole project.
- Create and activate a WSL venv at the repo root:

```bash
cd ~/luminai-genesis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Run the backend dev server (from repo root):

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Big picture (what to know)
-------------------------
- Monorepo layout: `backend/` (FastAPI), `ui/` (Next.js), `cli/` (Typer), `resonance/` (core TGCR engine), `docs/` and `.github/` for governance.
- Backend convention: add small routers under `backend/app/api/*.py` and wire them through `backend/app/api/__init__.py` (see `status.py` & `__init__.py`).
- Models live under `backend/app/models.py` (Pydantic) and should include TGCR metadata where relevant.
- Root `requirements.txt` delegates to `backend/requirements.txt` so `pip install -r requirements.txt` works from repo root.

Project-specific rules and patterns
----------------------------------
- Persona routing: follow the personas in `.github/COPILOT.md` (Airth, Arcadia, Ely, LuminAI, Kaznak). Select persona and document it in commit bodies.
- MEMO frontmatter: any new public doc must include the TEC MEMO frontmatter block (title, dates, status, approvers, owner_checklist, tags, related_docs).
- TGCR artifacts: any code or schema that touches agents, memory, or inference must include TGCR docstring metadata: the TGCR equation, Witness Protocol reference, 16 Frequencies checks, conscience hooks, and metadata fields (timestamps, persona, resonance_score, lineage). See `backend/app/models.py` for an example using `schema_extra`.
- File creation pattern: prefer adding new modules under `backend/app/` and small focused routers; do not edit global config files unless instructed. Never overwrite user configs without explicit consent.

Integration & external dependencies
----------------------------------
- Key Python deps: `fastapi`, `uvicorn`, `pydantic`, `typer`. See `backend/requirements.txt`.
- Cross-component calls: the resonance core will be imported by backend services; keep public interfaces small and well-typed (Pydantic models).

Testing & CI
-----------
- Tests live under `backend/tests/` or top-level `tests/` depending on scope. Use pytest. CI will run CodeQL and Dependabot policies defined in `.github/workflows/`.
- When adding behavior that affects resonance calculations, include unit tests that assert metadata fields (timestamps/persona/resonance_score) and a simple property test for numerical stability.

Commit & PR conventions (enforced)
---------------------------------
- Commit header: `type: short description` (e.g. `feat: Add TGCR engine scaffolding`).
- Commit body MUST include: persona responsible, files touched, reason, resonance impact (↑/↓/neutral).

Quick examples (concrete references)
----------------------------------
- Add a router: create `backend/app/api/foo.py` -> register in `backend/app/api/__init__.py` -> import & include `api_router` in `backend/app/main.py`.
- Health check: `backend/app/api/status.py` exposes `/api/healthz`.
- Model metadata example: `backend/app/models.py` uses `schema_extra` to hold `tgcr` fields.

Do / Don't (short)
------------------
- Do: add MEMO frontmatter to docs, include TGCR metadata in agent code, write focused routers and small Pydantic models.
- Don't: overwrite user workspace or global config files, commit secrets, add heavy dependencies without justification.

If anything above is unclear or you want more examples (router template, test template, or a commit message generator), say which part and I will expand and iterate.
