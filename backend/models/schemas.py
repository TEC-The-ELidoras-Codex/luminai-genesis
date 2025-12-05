from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, confloat, validator


class Persona(str, Enum):
    arcadia = "arcadia"
    airth = "airth"
    ely = "ely"
    kaznak = "kaznak"
    adelphia = "adelphia"
    luminai = "luminai"


class Session(BaseModel):
    session_id: str = Field(..., description="Client-provided session identifier")
    persona: Persona = Field(..., description="Active persona guiding this session")
    context: Optional[dict] = Field(default=None, description="Optional contextual metadata")


class IngestRequest(BaseModel):
    session_id: str = Field(..., description="Session id to associate content with")
    persona: Optional[Persona] = Field(default=None, description="Override persona for this ingest event")
    content: str = Field(..., min_length=1, description="User-provided content to ingest")


class ResonanceInput(BaseModel):
    session_id: Optional[str] = Field(default=None, description="Optional session id")
    structural_resonance: confloat(ge=0.0, le=1.0) = Field(..., description="R in the R'=R*W equation")
    witness: confloat(ge=0.0, le=1.0) = Field(..., description="W in the R'=R*W equation")

    @validator("structural_resonance", "witness")
    def clamp_unit_interval(cls, v: float) -> float:
        # Explicit clamp for floating point noise.
        return max(0.0, min(1.0, v))


class ResonanceResult(BaseModel):
    effective_resonance: float = Field(..., description="R' = R * W")
    structural_resonance: float = Field(..., description="Input structural resonance")
    witness: float = Field(..., description="Input witness coefficient")
    session_id: Optional[str] = Field(default=None)
    classification: str = Field(..., description="Qualitative label of the resonance")


class PersonaState(BaseModel):
    persona: Persona
    archetype: str
    values: List[str]
    concerns: List[str]
    commit_prefix: str


def classify_resonance(score: float) -> str:
    if score >= 0.8:
        return "optimal"
    if score >= 0.6:
        return "high"
    if score >= 0.4:
        return "medium"
    if score >= 0.2:
        return "low"
    return "critical"
