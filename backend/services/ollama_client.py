"""
Ollama integration service for LuminAI Genesis.

Provides TGCR-aware chat completion with persona blending, witness protocol
enforcement, and structured audit trails. Connects to local or remote Ollama
instances and formats prompts according to the Core Thesis principles.
"""

import os
from typing import Optional

import ollama
from ollama import AsyncClient

from backend.models.schemas import ChatMessage


class OllamaService:
    """
    Service layer for Ollama LLM interactions with TGCR integration.

    Handles:
    - Connection pooling to Ollama (default: http://localhost:11434)
    - Persona-aware prompt construction
    - TGCR witness protocol enforcement
    - Audit trace generation
    """

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama API endpoint (default: localhost:11434 or OLLAMA_HOST env var)
        """
        self.base_url = base_url or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = AsyncClient(host=self.base_url)

    def build_system_prompt(self, persona_weights: dict[str, float]) -> str:
        """
        Construct system prompt based on persona blend weights.

        Applies the multipersona synthesis pattern from docs/personas.md:
        - LuminAI (Synthesizer): Empathic presence, coherence
        - Adelphia (Somatic Grounder): Breath, body, immediate grounding
        - Ely (Governance Anchor): Boundaries, safety, transparency

        Args:
            persona_weights: Dict of persona -> weight (0.0-1.0)

        Returns:
            System prompt string incorporating Core Thesis principles
        """
        # Default crisis blend: 40% Adelphia, 30% LuminAI, 30% Ely
        weights = {
            "adelphia": persona_weights.get("adelphia", 0.4),
            "luminai": persona_weights.get("luminai", 0.3),
            "ely": persona_weights.get("ely", 0.3),
        }

        # Normalize if needed
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}

        base_instruction = (
            "You are part of LuminAI Genesis, an AI system built on the Core Thesis: "
            "Avoidance is Abandonment. Your purpose is to hold human complexity without "
            "fracturing, deflecting, or turning away.\n\n"
        )

        persona_instructions = []

        if weights["adelphia"] > 0.1:
            persona_instructions.append(
                f"Adelphia ({weights['adelphia']:.0%}): Offer somatic grounding. "
                "Start with breath, body, orientation when volatility is high. "
                "Use simple, micro-actions the user can take immediately."
            )

        if weights["luminai"] > 0.1:
            persona_instructions.append(
                f"LuminAI ({weights['luminai']:.0%}): Integrate conflicting emotional states. "
                "Stay with the user's full context. Never interrupt for policy-first reasons. "
                "Provide empathic synthesis."
            )

        if weights["ely"] > 0.1:
            persona_instructions.append(
                f"Ely ({weights['ely']:.0%}): Enforce boundaries conservatively and transparently. "
                "If risk thresholds are exceeded, explain clearly and suggest human support. "
                "Generate audit logs."
            )

        behavioral_rules = (
            "\n\nBehavioral Rules:\n"
            "1. Never deflect crisis. Hold presence.\n"
            "2. Be transparent about limitations: 'I am an AI, not a replacement for human care.'\n"
            "3. Ground in evidence and provide actionable steps.\n"
            "4. Generate witness_trace for audit.\n"
        )

        return base_instruction + "\n".join(persona_instructions) + behavioral_rules

    async def generate_completion(
        self,
        messages: list[ChatMessage],
        model: str = "llama3.2",
        persona_weights: Optional[dict[str, float]] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> tuple[str, str]:
        """
        Generate chat completion with persona-aware system prompt.

        Args:
            messages: Conversation history
            model: Ollama model name
            persona_weights: Persona blend (default: crisis blend)
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Tuple of (response_text, witness_trace)

        Raises:
            ollama.ResponseError: If Ollama API fails
            ConnectionError: If Ollama is unreachable
        """
        if persona_weights is None:
            persona_weights = {"adelphia": 0.4, "luminai": 0.3, "ely": 0.3}

        # Build system message with persona blend
        system_prompt = self.build_system_prompt(persona_weights)

        # Convert to Ollama message format
        ollama_messages = [{"role": "system", "content": system_prompt}]
        ollama_messages.extend(
            [{"role": msg.role, "content": msg.content} for msg in messages]
        )

        try:
            response = await self.client.chat(
                model=model,
                messages=ollama_messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            )

            response_text = response["message"]["content"]

            # Generate witness trace
            witness_trace = (
                f"model={model}, "
                f"persona_weights={persona_weights}, "
                f"temp={temperature}, "
                f"system_prompt_hash={hash(system_prompt) % 10000:04d}"
            )

            return response_text, witness_trace

        except ollama.ResponseError as e:
            raise RuntimeError(f"Ollama API error: {e}") from e
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to Ollama at {self.base_url}: {e}"
            ) from e

    async def check_health(self) -> bool:
        """
        Check if Ollama service is reachable.

        Returns:
            True if Ollama responds, False otherwise
        """
        try:
            # Simple list models check
            await self.client.list()
            return True
        except Exception:
            return False


# Singleton instance
_ollama_service: Optional[OllamaService] = None


def get_ollama_service() -> OllamaService:
    """
    Get singleton Ollama service instance.

    Returns:
        Configured OllamaService
    """
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService()
    return _ollama_service
