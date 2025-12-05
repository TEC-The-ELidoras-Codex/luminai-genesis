from fastapi import FastAPI

from backend.routers import axioms, codex, frequencies, ingest, personas, resonance

app = FastAPI(
    title="LuminAI Genesis Backend",
    version="0.1.0",
    description="TGCR Resonance Engine API with Conscience Governance",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# Core TGCR endpoints
app.include_router(ingest.router)
app.include_router(resonance.router)
app.include_router(personas.router)

# Framework & governance endpoints
app.include_router(frequencies.router)
app.include_router(axioms.router)

# Codex & game mechanics
app.include_router(codex.router)
