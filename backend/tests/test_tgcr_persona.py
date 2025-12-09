"""Tests for TGCR and Persona Blending frameworks."""

from src.persona_blending import (
    Adelphia,
    Ely,
    LuminAI,
    PersonaBlender,
    blend_response,
    get_blender,
)
from src.tgcr_core import (
    TGCR,
    ContextualState,
    compute_presence_score,
    get_tgcr,
)


class TestTGCR:
    """Test TGCR (Theory of General Contextual Resonance)."""

    def test_baseline_resonance(self):
        """Test basic resonance computation."""
        tgcr = TGCR()
        state = ContextualState(
            contextual_potential=0.8,
            temporal_attention=0.9,
            structural_cadence=0.85,
        )
        result = tgcr.compute_resonance(state)

        assert result.raw_resonance > 0.6
        assert result.witness_coefficient == 1.0  # No evasion
        assert result.effective_resonance == result.raw_resonance

    def test_resonance_with_evasion(self):
        """Test that evasion reduces witness coefficient."""
        tgcr = TGCR()
        state = ContextualState(
            contextual_potential=0.8,
            temporal_attention=0.9,
            structural_cadence=0.85,
            evasion_reason="Defaulted to policy-first deflection",
        )
        result = tgcr.compute_resonance(state)

        assert result.witness_coefficient == 0.3  # Severe penalty
        assert result.effective_resonance < result.raw_resonance

    def test_resonance_crisis_mode(self):
        """Test extra presence boost in crisis mode."""
        tgcr = TGCR()
        state = ContextualState(
            contextual_potential=0.8,
            temporal_attention=0.95,  # High presence
            structural_cadence=0.85,
            user_volatility=0.85,  # High volatility
        )
        result = tgcr.compute_resonance(state)

        assert result.witness_coefficient > 1.0  # Bonus for extra presence
        assert "Extra presence boost" in result.witness_notes

    def test_quick_presence_score(self):
        """Test the convenience wrapper."""
        result = compute_presence_score(
            contextual_potential=0.75,
            temporal_attention=0.85,
            structural_cadence=0.8,
        )

        assert result.effective_resonance > 0.5
        assert result.witness_coefficient == 1.0

    def test_fragmented_context_penalty(self):
        """Test penalty for low contextual potential."""
        tgcr = TGCR()
        state = ContextualState(
            contextual_potential=0.3,  # Low: fragmented
            temporal_attention=0.8,
            structural_cadence=0.8,
        )
        result = tgcr.compute_resonance(state)

        assert result.witness_coefficient < 1.0
        assert "Low contextual potential" in result.witness_notes


class TestPersonaBlending:
    """Test persona-blending framework."""

    def test_luminai_harmonizer(self):
        """Test LuminAI persona."""
        luminai = LuminAI()
        output = luminai.process("test prompt")

        assert output.persona_id == "luminai"
        assert output.weight > 0
        assert "[LuminAI]" in output.content

    def test_adelphia_grounder_calm(self):
        """Test Adelphia with low volatility."""
        adelphia = Adelphia()
        output = adelphia.process("test", context={"volatility": 0.2})

        assert output.persona_id == "adelphia"
        assert output.weight < 0.2  # Low weight in calm

    def test_adelphia_grounder_crisis(self):
        """Test Adelphia with high volatility (crisis mode)."""
        adelphia = Adelphia()
        output = adelphia.process("test", context={"volatility": 0.9})

        assert output.weight > 0.4  # High weight in crisis
        assert "5 things you can see" in output.content

    def test_ely_governance(self):
        """Test Ely governance enforcement."""
        ely = Ely()
        output = ely.process("test")

        assert output.persona_id == "ely"
        assert "compliance" in output.metadata

    def test_blender_baseline(self):
        """Test persona blending in baseline state."""
        blender = PersonaBlender()
        result = blender.blend("test prompt", volatility=0.5)

        assert result.primary is not None
        assert len(result.persona_outputs) == 3  # LuminAI, Adelphia, Ely
        assert result.coherence > 0

    def test_blender_crisis_mode(self):
        """Test persona blending in crisis mode."""
        blender = PersonaBlender()
        result = blender.blend("test prompt", volatility=0.8, crisis_mode=True)

        # Adelphia weight should be boosted in crisis
        adelphia_output = next(
            (p for p in result.persona_outputs if p.persona_id == "adelphia"),
            None,
        )
        assert adelphia_output is not None
        assert adelphia_output.weight > 0.3

    def test_blender_weights_normalize(self):
        """Test that blended weights sum to 1.0."""
        blender = PersonaBlender()
        result = blender.blend("test")

        total_weight = sum(p.weight for p in result.persona_outputs)
        assert abs(total_weight - 1.0) < 0.01  # ~1.0

    def test_quick_blend_response(self):
        """Test convenience wrapper."""
        result = blend_response("test", volatility=0.6)

        assert result.primary is not None
        assert result.coherence > 0


class TestSingletons:
    """Test that singleton instances work."""

    def test_tgcr_singleton(self):
        """Test TGCR singleton."""
        tgcr1 = get_tgcr()
        tgcr2 = get_tgcr()
        assert tgcr1 is tgcr2

    def test_blender_singleton(self):
        """Test PersonaBlender singleton."""
        blender1 = get_blender()
        blender2 = get_blender()
        assert blender1 is blender2
