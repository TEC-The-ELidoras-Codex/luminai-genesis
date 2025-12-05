from fastapi import APIRouter

from backend.models.schemas import ResonanceInput, ResonanceResult, classify_resonance

router = APIRouter(prefix="/api/resonance", tags=["resonance"])


@router.post("", response_model=ResonanceResult)
def compute_resonance(payload: ResonanceInput) -> ResonanceResult:
    score = payload.structural_resonance * payload.witness
    return ResonanceResult(
        effective_resonance=score,
        structural_resonance=payload.structural_resonance,
        witness=payload.witness,
        session_id=payload.session_id,
        classification=classify_resonance(score),
    )
