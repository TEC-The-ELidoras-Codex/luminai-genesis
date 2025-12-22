from fastapi import APIRouter, HTTPException

from backend.models.schemas import IngestRequest, Persona, Session

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

# In-memory registry for example purposes only.
SESSIONS: dict[str, Session] = {}


@router.post("", response_model=Session)
def ingest(payload: IngestRequest) -> Session:
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Content must not be empty")

    persona = payload.persona or Persona.arcadia
    session = Session(session_id=payload.session_id, persona=persona)
    SESSIONS[payload.session_id] = session
    return session


@router.get("/{session_id}", response_model=Session)
def get_session(session_id: str) -> Session:
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
