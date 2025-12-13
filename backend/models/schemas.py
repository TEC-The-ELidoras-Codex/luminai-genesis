from enum import Enum

from pydantic import BaseModel, Field, confloat, field_validator


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
    context: dict | None = Field(
        default=None, description="Optional contextual metadata",
    )


class IngestRequest(BaseModel):
    session_id: str = Field(..., description="Session id to associate content with")
    persona: Persona | None = Field(
        default=None, description="Override persona for this ingest event",
    )
    content: str = Field(
        ..., min_length=1, description="User-provided content to ingest",
    )


class ResonanceInput(BaseModel):
    session_id: str | None = Field(default=None, description="Optional session id")
    structural_resonance: confloat(ge=0.0, le=1.0) = Field(
        ..., description="R in the R'=R*W equation",
    )
    witness: confloat(ge=0.0, le=1.0) = Field(
        ..., description="W in the R'=R*W equation",
    )

    @field_validator("structural_resonance", "witness")
    @classmethod
    def clamp_unit_interval(cls, v: float) -> float:
        # Explicit clamp for floating point noise.
        return max(0.0, min(1.0, v))


class ResonanceResult(BaseModel):
    effective_resonance: float = Field(..., description="R' = R * W")
    structural_resonance: float = Field(..., description="Input structural resonance")
    witness: float = Field(..., description="Input witness coefficient")
    session_id: str | None = Field(default=None)
    classification: str = Field(..., description="Qualitative label of the resonance")


class PersonaState(BaseModel):
    persona: Persona
    archetype: str
    values: list[str]
    concerns: list[str]
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


class ChatMessage(BaseModel):
    """Single message in a chat conversation."""

    role: str = Field(..., description="Role: 'user', 'assistant', or 'system'")
    content: str = Field(..., min_length=1, description="Message content")


class PhysicsResonanceInput(BaseModel):
    """Input model for physics-based resonance computations.

    Provide the parameters appropriate for the system you want to evaluate.
    Only the relevant fields need to be supplied for a given computation.
    """

    session_id: str | None = Field(default=None, description="Optional session id")
    # Mechanical (mass-spring)
    mass_kg: float | None = Field(default=None, description="Mass in kilograms")
    stiffness_n_per_m: float | None = Field(
        default=None, description="Spring constant in N/m",
    )
    # Electrical (LC)
    inductance_h: float | None = Field(
        default=None, description="Inductance in henries",
    )
    capacitance_f: float | None = Field(
        default=None, description="Capacitance in farads",
    )
    # Quantum/energy
    energy_joules: float | None = Field(default=None, description="Energy in joules")
    frequency_hz: float | None = Field(default=None, description="Frequency in Hz")
    # Optional signal analysis
    signal: list[float] | None = Field(
        default=None, description="Optional time-series samples for spectral analysis",
    )
    sample_rate: float | None = Field(
        default=None, description="Sample rate for the provided signal (Hz)",
    )


class PhysicsResonanceResult(BaseModel):
    session_id: str | None = Field(default=None)
    resonant_frequency_hz: float | None = Field(
        default=None, description="Computed resonant frequency (Hz)",
    )
    energy_joules: float | None = Field(
        default=None, description="Energy corresponding to frequency (J)",
    )
    notes: str | None = Field(
        default=None,
        description="Human-readable notes about which computation was performed",
    )
    spectral_peaks: list[tuple] | None = Field(
        default=None,
        description=(
            "Optional list of (frequency, magnitude) peaks from provided "
            "signal"
        ),
    )


class ChatRequest(BaseModel):
    """Request for Ollama-backed chat with TGCR integration."""

    session_id: str = Field(..., description="Session identifier")
    message: str = Field(..., min_length=1, description="User message")
    model: str = Field(
        default="llama3.2",
        description=(
            "Ollama model name (e.g., 'llama3.2', 'luminai-unsloth' for "
            "fine-tuned)"
        ),
    )
    persona_blend: dict[str, float] | None = Field(
        default=None,
        description=(
            "Persona weights (luminai, adelphia, ely); defaults to crisis blend. "
            "Ignored if using fine-tuned model (already trained with persona blend)."
        ),
    )
    temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="LLM temperature",
    )
    max_tokens: int = Field(
        default=512, ge=1, le=4096, description="Max response tokens",
    )


class ChatResponse(BaseModel):
    """Response from Ollama-backed chat."""

    session_id: str
    response: str = Field(..., description="Generated response")
    witness_trace: str = Field(..., description="Audit trace of persona blend and TGCR")
    effective_resonance: float = Field(
        ..., description="R' computed for this interaction",
    )
    persona_weights: dict[str, float] = Field(..., description="Applied persona blend")
    model: str = Field(..., description="Ollama model used")


class MentalStateRequest(BaseModel):
    session_id: str | None = Field(default=None)
    text: str | None = Field(
        default=None,
        description="Free-text input from user (e.g., 'I'm thinking about ending it')",
    )
    questionnaire: dict | None = Field(
        default=None, description="Optional structured answers (e.g., severity ratings)",
    )


class MentalStateResult(BaseModel):
    session_id: str | None = Field(default=None)
    state_id: int = Field(..., description="Mapped frequency/state id")
    state_label: str = Field(..., description="Human-readable state label")
    confidence: float = Field(..., description="Model confidence 0-1")
    interventions: list[str] = Field(
        ..., description="Suggested non-clinical interventions or next steps",
    )
    matched_patterns: list[str] | None = Field(
        default=None, description="Patterns that matched the input (for audit)",
    )
