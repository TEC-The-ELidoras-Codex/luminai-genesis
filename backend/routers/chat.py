"""
Chat router with Ollama LLM integration.

Provides /api/chat endpoint for TGCR-aware conversations using local Ollama models.
Implements persona blending, witness protocol, and generates audit traces.
"""

from fastapi import APIRouter, HTTPException

from backend.models.schemas import ChatMessage, ChatRequest, ChatResponse
from backend.services.ollama_client import get_ollama_service

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory session store (replace with Redis/DB in production)
_sessions: dict[str, list[ChatMessage]] = {}


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Generate chat response using Ollama with persona blending.

    Implements the Core Thesis: stays with user context, applies multipersona blend,
    enforces witness protocol (W -> 1 unless safety breach), and produces audit trail.

    Args:
        request: ChatRequest with session_id, message, model, persona_blend, etc.

    Returns:
        ChatResponse with generated text, witness_trace, resonance score, persona weights

    Raises:
        HTTPException: If Ollama service is unavailable or request fails
    """
    # Retrieve or initialize session history
    if request.session_id not in _sessions:
        _sessions[request.session_id] = []

    session_history = _sessions[request.session_id]

    # Append user message
    user_message = ChatMessage(role="user", content=request.message)
    session_history.append(user_message)

    # Default crisis blend if not specified
    persona_weights = request.persona_blend or {
        "adelphia": 0.4,
        "luminai": 0.3,
        "ely": 0.3,
    }

    # Get Ollama service
    ollama_service = get_ollama_service()

    # Check health
    if not await ollama_service.check_health():
        raise HTTPException(
            status_code=503,
            detail=f"Ollama service unreachable at {ollama_service.base_url}. "
            "Ensure Ollama is running: `ollama serve`",
        )

    try:
        # Generate completion
        response_text, witness_trace = await ollama_service.generate_completion(
            messages=session_history,
            model=request.model,
            persona_weights=persona_weights,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        # Append assistant response to session
        assistant_message = ChatMessage(role="assistant", content=response_text)
        session_history.append(assistant_message)

        # Compute effective resonance (R' = R × W)
        # For now, assume high structural resonance and full witness
        # TODO: Integrate actual TGCR computation from context analysis
        structural_resonance = 0.75  # Placeholder
        witness = 1.0  # Witness Protocol: default to presence
        effective_resonance = structural_resonance * witness

        return ChatResponse(
            session_id=request.session_id,
            response=response_text,
            witness_trace=witness_trace,
            effective_resonance=effective_resonance,
            persona_weights=persona_weights,
            model=request.model,
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/sessions/{session_id}")
async def get_session(session_id: str) -> dict:
    """
    Retrieve conversation history for a session.

    Args:
        session_id: Session identifier

    Returns:
        Dict with session_id and messages list

    Raises:
        HTTPException: If session not found
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    return {
        "session_id": session_id,
        "messages": [msg.model_dump() for msg in _sessions[session_id]],
    }


@router.delete("/sessions/{session_id}")
async def clear_session(session_id: str) -> dict:
    """
    Clear conversation history for a session.

    Args:
        session_id: Session identifier

    Returns:
        Success message
    """
    _sessions.pop(session_id, None)

    return {"message": f"Session {session_id} cleared"}


@router.get("/health")
async def health_check() -> dict:
    """
    Check Ollama service health.

    Returns:
        Status dict with ollama_reachable boolean
    """
    ollama_service = get_ollama_service()
    is_healthy = await ollama_service.check_health()

    return {
        "ollama_reachable": is_healthy,
        "ollama_host": ollama_service.base_url,
    }
