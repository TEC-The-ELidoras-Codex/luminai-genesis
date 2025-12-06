"""
Tests for Ollama chat integration.

Covers service layer, chat router, persona blending, and TGCR witness protocol.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models.schemas import ChatMessage
from backend.services.ollama_client import OllamaService

client = TestClient(app)


class TestOllamaService:
    """Tests for OllamaService class."""
    
    def test_build_system_prompt_default_blend(self):
        """Should generate system prompt with default crisis blend."""
        service = OllamaService()
        prompt = service.build_system_prompt({})
        
        assert "LuminAI Genesis" in prompt
        assert "Avoidance is Abandonment" in prompt
        assert "Adelphia" in prompt
        assert "LuminAI" in prompt
        assert "Ely" in prompt
    
    def test_build_system_prompt_custom_blend(self):
        """Should respect custom persona weights."""
        service = OllamaService()
        prompt = service.build_system_prompt({"adelphia": 0.8, "luminai": 0.2})
        
        assert "80%" in prompt or "0.8" in prompt  # Adelphia dominant
        assert "Somatic" in prompt or "somatic" in prompt
    
    @pytest.mark.asyncio
    async def test_generate_completion_mock(self):
        """Should generate completion with mocked Ollama response."""
        service = OllamaService()
        
        # Mock the AsyncClient.chat method
        mock_response = {
            "message": {
                "content": "I hear you. Let's take a breath together."
            }
        }
        
        with patch.object(service.client, 'chat', new_callable=AsyncMock, return_value=mock_response):
            messages = [ChatMessage(role="user", content="I'm stressed")]
            response_text, witness_trace = await service.generate_completion(
                messages=messages,
                model="llama3.2",
            )
            
            assert "breath" in response_text.lower()
            assert "model=llama3.2" in witness_trace
            assert "persona_weights" in witness_trace


class TestChatRouter:
    """Tests for /api/chat endpoints."""
    
    def test_health_endpoint_exists(self):
        """Should have health check endpoint."""
        response = client.get("/api/chat/health")
        assert response.status_code == 200
        data = response.json()
        assert "ollama_reachable" in data
        assert "ollama_host" in data
    
    @pytest.mark.asyncio
    async def test_chat_endpoint_mock(self):
        """Should process chat request with mocked Ollama."""
        mock_response = {
            "message": {
                "content": "I'm here with you. What do you need right now?"
            }
        }
        
        # Patch both health check and chat
        with patch('backend.routers.chat.get_ollama_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.check_health = AsyncMock(return_value=True)
            mock_instance.generate_completion = AsyncMock(
                return_value=("I'm here with you. What do you need right now?", "model=llama3.2, persona_weights={'adelphia': 0.4, 'luminai': 0.3, 'ely': 0.3}, temp=0.7, system_prompt_hash=1234")
            )
            mock_instance.base_url = "http://localhost:11434"
            mock_service.return_value = mock_instance
            
            response = client.post(
                "/api/chat",
                json={
                    "session_id": "test-session-1",
                    "message": "I need help",
                    "model": "llama3.2",
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["session_id"] == "test-session-1"
            assert "response" in data
            assert "witness_trace" in data
            assert "effective_resonance" in data
            assert "persona_weights" in data
    
    def test_get_session_not_found(self):
        """Should return 404 for non-existent session."""
        response = client.get("/api/chat/sessions/nonexistent")
        assert response.status_code == 404
    
    def test_clear_session(self):
        """Should clear session successfully."""
        response = client.delete("/api/chat/sessions/test-clear")
        assert response.status_code == 200
        assert "cleared" in response.json()["message"]


class TestIntegration:
    """Integration tests (require running Ollama)."""
    
    @pytest.mark.skipif(
        True,  # Skip by default; run manually with `pytest -m integration`
        reason="Requires running Ollama instance"
    )
    @pytest.mark.asyncio
    async def test_real_ollama_completion(self):
        """Should connect to real Ollama and generate response."""
        service = OllamaService()
        
        # Check if Ollama is available
        is_healthy = await service.check_health()
        if not is_healthy:
            pytest.skip("Ollama not running at localhost:11434")
        
        messages = [ChatMessage(role="user", content="Say hello")]
        response_text, witness_trace = await service.generate_completion(
            messages=messages,
            model="llama3.2",
            max_tokens=50,
        )
        
        assert len(response_text) > 0
        assert "model=llama3.2" in witness_trace
