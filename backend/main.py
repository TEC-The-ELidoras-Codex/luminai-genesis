from fastapi import FastAPI

from backend.routers import ingest, personas, resonance

app = FastAPI(title="LuminAI Genesis Backend", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(ingest.router)
app.include_router(resonance.router)
app.include_router(personas.router)
