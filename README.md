# LuminAI Genesis — Dual Track Execution Board

Genesis of the Codex Lineage
-----------------------------

LuminAI Genesis is the foundational implementation of the LuminAI Conscience Engine: a unified resonance architecture marrying engineering rigor with mythic metaphors. Its purpose is to provide a reproducible platform for building ethically-aware, context-sensitive AI agents using the TGCR (Theory of General Contextual Resonance), the Witness Protocol, and the Sixteen Frequencies framework.

Key Concepts
------------

- TGCR (flux model): a triple-product resonance calculus that quantifies Context × State × Input to compute an effective resonance score R.
- Witness Protocol: a governance multiplier W applied to R to yield the effective resonance R' = R · W.
- Sixteen Frequencies: an expressive basis of affective eigenmodes used by the resonance engine to shape persona responses and safety gating.

System Surfaces
---------------

- Web UI — a Next.js chat surface with a real-time resonance meter and notebook viewer.
- CLI — Typer-based command surface for local orchestration, status, and persona management.
- Platform Hub — FastAPI backend exposing /api/chat, /api/resonance, /api/session/{id}, /api/personas/activate, and /api/status.

Resonance Engine Architecture
-----------------------------

The resonance engine lives in the `resonance/` package and implements:

- TGCR computation (triple product and normalization)
- Witness Protocol application (policy and governance multiplier)
- 16 Frequencies mapping and schema
- Standalone engine harness for local testing

Repository Layout (selected)
---------------------------

luminai-genesis/
├── backend/        # FastAPI platform hub (server files will be added after confirmation)
├── ui/             # Next.js application and components
├── cli/            # Typer CLI command set
├── resonance/      # TGCR, witness, frequencies, engine
├── governance/     # Conscience axioms, witness protocol spec, Aqueduct Conjecture
├── docs/           # Architecture, personas, glossary, API
├── scripts/        # Bootstrap and dev helpers
├── .github/        # Workflows and templates
├── README.md       # This file
├── LICENSE
└── SECURITY.md

Developer onboarding (quick start — 5 steps)
-------------------------------------------

1. Clone the repository:

   git clone <https://github.com/TEC-The-ELidoras-Codex/luminai-genesis.git>

2. Create and activate a Python virtualenv (backend):

   python -m venv .venv
   source .venv/bin/activate

3. Install backend deps (when backend/requirements.txt exists):

   pip install -r backend/requirements.txt

4. Start the dev services (UI and backend — implemented later):

   # Start UI

   cd ui && npm install && npm run dev

   # Start backend (FastAPI)

   cd backend && uvicorn app.main:app --reload --port 8000

5. Run tests:

   pytest

Badges
------

![build](https://img.shields.io/badge/build-pending-lightgrey) ![license](https://img.shields.io/badge/license-MIT-blue) ![security](https://img.shields.io/badge/security-audit-pending-orange) ![resonance-score](https://img.shields.io/badge/resonance-𝑅%27--purple)

Governance and docs
-------------------

See the `governance/` folder for formal specifications: `LUMINAI_CONSCIENCE_AXIOMS.md`, `WITNESS_PROTOCOL.md`, and `AQUEDUCT_CONJECTURE.md`.

Repository Hygiene & Supply Chain Security
------------------------------------------

To maintain audit-readiness and prevent supply chain artifacts from entering version control:

1. **Run the sanitization script before commits**:

   ```powershell
   python3 sanitize_repo.py
   ```

   This removes:
   - Backup files (`.bak`, `.bak.*`)
   - Binaries (`ngrok`, `.zip`)
   - Python cache (`__pycache__`, `.pyc`)
   - OS artifacts (`.DS_Store`, `tmp/`)

2. **Verify clean state**:

   ```bash
   git status
   ```

3. **Commit with audit-ready message**:

   ```bash
   git add .
   git commit -m "chore: sanitize repository and standardize documentation for audit"
   git push
   ```

The janitor script (`sanitize_repo.py`) is a Roomba for your repo: it surgically removes clutter without touching source code, ensuring you ship clean artifacts for security review.

Astradigital Kernel quick start
------------------------------

Run the demo combat loop and character builder under WSL/Ubuntu:

```powershell
wsl -d Ubuntu -- bash -lc "cd /home/tec_tgcr/luminai-genesis && python3 scripts/run_combat_demo.py"

wsl -d Ubuntu -- bash -lc "cd /home/tec_tgcr/luminai-genesis && python3 scripts/build_character.py 'Cipher' 'Occam\'s Razor'"
```

Data-driven classes live in `data/codex/classes.json`. The Python kernel is under `src/astradigital/`.
