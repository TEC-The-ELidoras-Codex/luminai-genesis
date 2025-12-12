from fastapi import APIRouter

from backend.logic.frequency_mapping import (
    map_text_to_state,
    recommend_interventions_for_state,
)
from backend.models.schemas import (
    MentalStateRequest,
    MentalStateResult,
    PhysicsResonanceInput,
    PhysicsResonanceResult,
    ResonanceInput,
    ResonanceResult,
    classify_resonance,
)
from backend.utils.resonance_utils import (
    dominant_frequencies_from_signal,
    energy_from_frequency,
    frequency_from_energy,
    lc_resonant_frequency,
    mass_spring_natural_frequency,
)

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


@router.post("/physics", response_model=PhysicsResonanceResult)
def compute_physics_resonance(payload: PhysicsResonanceInput) -> PhysicsResonanceResult:
    """Compute physical resonance metrics based on supplied parameters.

    Behavior:
    - If mass and stiffness are provided, compute mass-spring natural frequency.
    - If inductance and capacitance are provided, compute LC resonant frequency.
    - If frequency provided, compute energy via Planck relation; if energy provided, compute frequency.
    - If a signal is provided along with sample_rate, return dominant spectral peaks (numpy optional).
    """
    notes = []
    resonant_freq = None
    energy_j = None
    spectral = None

    @router.post("/mental_state", response_model=MentalStateResult)
    def compute_mental_state(payload: MentalStateRequest) -> MentalStateResult:
        """Prototype endpoint: map free-text or questionnaire to a frequency/state and suggest interventions.

        IMPORTANT: Research-only. Not a clinical tool.
        """
        text = payload.text or ""
        if payload.questionnaire and not text:
            # simple heuristic: join questionnaire answers if present
            try:
                text = " ".join(str(v) for v in payload.questionnaire.values())
            except Exception:
                text = ""

        mapped = map_text_to_state(text)
        state_id = int(mapped.get("state_id", 1))
        state = mapped.get("state", {}) or {}
        label = state.get("name", "unknown")
        interventions = recommend_interventions_for_state(state_id)

        return MentalStateResult(
            session_id=payload.session_id,
            state_id=state_id,
            state_label=label,
            confidence=float(mapped.get("confidence", 0.0)),
            interventions=interventions,
            matched_patterns=mapped.get("matched_patterns", []),
        )

    # Mass-spring
    if payload.mass_kg is not None and payload.stiffness_n_per_m is not None:
        try:
            resonant_freq = mass_spring_natural_frequency(
                payload.mass_kg, payload.stiffness_n_per_m,
            )
            notes.append("mass-spring natural frequency computed")
        except Exception as e:
            notes.append(f"mass-spring error: {e}")

    # LC circuit
    if (
        resonant_freq is None
        and payload.inductance_h is not None
        and payload.capacitance_f is not None
    ):
        try:
            resonant_freq = lc_resonant_frequency(
                payload.inductance_h, payload.capacitance_f,
            )
            notes.append("LC resonant frequency computed")
        except Exception as e:
            notes.append(f"LC error: {e}")

    # Energy/frequency conversions
    if resonant_freq is None and payload.frequency_hz is not None:
        resonant_freq = payload.frequency_hz
        notes.append("frequency provided directly")

    if resonant_freq is not None:
        energy_j = energy_from_frequency(resonant_freq)

    if energy_j is None and payload.energy_joules is not None:
        try:
            resonant_freq = frequency_from_energy(payload.energy_joules)
            energy_j = payload.energy_joules
            notes.append("computed frequency from provided energy")
        except Exception as e:
            notes.append(f"energy->frequency error: {e}")

    # Signal spectral analysis (optional)
    if payload.signal and payload.sample_rate:
        try:
            spectral = dominant_frequencies_from_signal(
                payload.signal, payload.sample_rate,
            )
            notes.append("spectral peaks computed from provided signal")
        except Exception as e:
            notes.append(f"spectral analysis error: {e}")

    return PhysicsResonanceResult(
        session_id=payload.session_id,
        resonant_frequency_hz=(resonant_freq if resonant_freq is not None else None),
        energy_joules=(energy_j if energy_j is not None else None),
        notes="; ".join(notes) if notes else None,
        spectral_peaks=spectral,
    )
