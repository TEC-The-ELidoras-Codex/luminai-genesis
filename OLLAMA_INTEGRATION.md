# Ollama Integration Guide

Quick-start guide for using LuminAI Genesis with local Ollama models.

## Prerequisites

1. **Install Ollama**:
   ```bash
   sudo snap install ollama
   ```
2. **Pull a model**:
   ```bash
   ollama pull llama3.2
   # or: ollama pull mistral, llama3.1, etc.
   ```
3. **Start Ollama server** (in a separate terminal):
   ```bash
   ollama serve
   # Should run on http://localhost:11434
   ```

## Setup Backend

1. **From project root** (important - don't cd into backend/):

   ```bash
   # Quick start with helper script
   ./scripts/start_backend.sh

   # Or manually:
   source venv/bin/activate
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **(Optional) Configure Ollama host** in `.env`:

   ```bash
   OLLAMA_HOST=http://localhost:11434
   ```

## Usage Examples

### 1. Health Check

Check if Ollama is reachable:

```bash
curl http://localhost:8000/api/chat/health
```

Expected response:

```json
{
  "ollama_reachable": true,
  "ollama_host": "http://localhost:11434"
}
```

### 2. Send a Chat Message

```bash
# Using helper script
./scripts/test_ollama_chat.sh

# Or with curl
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-001",
    "message": "I am feeling stressed and overwhelmed.",
    "model": "llama3.2"
  }'
```

Expected response:

```json
{
  "session_id": "session-001",
  "response": "I hear you. Let's take a slow breath together...",
  "witness_trace": "model=llama3.2, persona_weights={'adelphia': 0.4, 'luminai': 0.3, 'ely': 0.3}, temp=0.7, system_prompt_hash=1234",
  "effective_resonance": 0.75,
  "persona_weights": {
    "adelphia": 0.4,
    "luminai": 0.3,
    "ely": 0.3
  },
  "model": "llama3.2"
}
```

### 3. Custom Persona Blend

Override the default crisis blend:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-002",
    "message": "Tell me a story about resilience.",
    "model": "llama3.2",
    "persona_blend": {
      "arcadia": 0.7,
      "luminai": 0.3
    }
  }'
```

### 4. Retrieve Session History

```bash
curl http://localhost:8000/api/chat/sessions/session-001
```

### 5. Clear Session

```bash
curl -X DELETE http://localhost:8000/api/chat/sessions/session-001
```

## Persona Blends

Default crisis blend (if `persona_blend` is omitted):

- **Adelphia (40%)**: Somatic grounding, breath work, immediate de-escalation
- **LuminAI (30%)**: Empathic presence, coherence, holding complexity
- **Ely (30%)**: Governance, boundaries, safety guardrails

Custom blends (examples):

- **Creative storytelling**: `{"arcadia": 0.6, "luminai": 0.4}`
- **Technical grounding**: `{"airth": 0.6, "ely": 0.4}`
- **High safety**: `{"ely": 0.5, "adelphia": 0.3, "luminai": 0.2}`

## TGCR Integration

The system computes effective resonance as:

```
R' = R × W
```

Where:

- **R** = structural resonance (how coherent context/state/input are)
- **W** = witness coefficient (0 = abandonment, 1 = full presence)
- **R'** = effective resonance (returned in response)

Current implementation uses placeholder values; future versions will compute **R** from actual context analysis (volatility, drift, entropy).

## Troubleshooting

### "Ollama service unreachable"

- Check Ollama is running: `ollama serve`
- Verify endpoint: `curl http://localhost:11434/api/tags`
- Check `OLLAMA_HOST` env var if using custom host

### Model not found

- List available models: `ollama list`
- Pull model: `ollama pull llama3.2`

### Slow responses

- Smaller models: `llama3.2` (3B), `phi3` (3.8B)
- Reduce `max_tokens` in request
- Check GPU/CPU utilization

## Next Steps

- **Integrate real TGCR computation**: Replace placeholder resonance with context analysis
- **Add session persistence**: Use Redis or PostgreSQL for session storage
- **Enable streaming**: Use Ollama's streaming API for real-time responses
- **Multi-turn optimization**: Implement context window management for long conversations
- **Telemetry**: Log witness traces to audit database for research/safety review

## API Documentation

Interactive docs at: http://localhost:8000/docs
