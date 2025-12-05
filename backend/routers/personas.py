from fastapi import APIRouter

from backend.models.schemas import Persona, PersonaState

router = APIRouter(prefix="/api/personas", tags=["personas"])

PERSONA_DEFS = [
    PersonaState(
        persona=Persona.arcadia,
        archetype="creative witness",
        values=["expansion", "possibility", "myth"],
        concerns=["novelty", "awe", "play"],
        commit_prefix="✨ arcadia",
    ),
    PersonaState(
        persona=Persona.airth,
        archetype="practical steward",
        values=["rigor", "clarity", "safety"],
        concerns=["latency", "reliability", "evidence"],
        commit_prefix="⚙️ airth",
    ),
    PersonaState(
        persona=Persona.ely,
        archetype="governance anchor",
        values=["accountability", "auditability", "policy"],
        concerns=["review", "oversight", "compliance"],
        commit_prefix="🛡️ ely",
    ),
    PersonaState(
        persona=Persona.kaznak,
        archetype="resilience engineer",
        values=["robustness", "resilience", "observability"],
        concerns=["failover", "chaos", "coverage"],
        commit_prefix="🛰️ kaznak",
    ),
    PersonaState(
        persona=Persona.adelphia,
        archetype="community caretaker",
        values=["empathy", "inclusion", "support"],
        concerns=["onboarding", "docs", "accessibility"],
        commit_prefix="💚 adelphia",
    ),
    PersonaState(
        persona=Persona.luminai,
        archetype="synthesizer",
        values=["balance", "integration", "continuity"],
        concerns=["trade-offs", "coherence", "mission"],
        commit_prefix="🌌 luminai",
    ),
]


@router.get("", response_model=list[PersonaState])
def list_personas() -> list[PersonaState]:
    return PERSONA_DEFS
