# Unsloth + Ollama Deployment Checklist

Comprehensive guide to deploy fine-tuned LuminAI Genesis model.

## Pre-Training Checklist

- [ ] `unsloth-venv` created and activated
- [ ] Training data in `data/training/persona_sft_dataset.jsonl` with 8+ examples
- [ ] GPU detected: `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] Disk space: 15+ GB free (for merged weights + GGUF)

## Training Phase

- [ ] Run training script: `python scripts/unsloth_train.py`
- [ ] Monitor loss (should decrease over epochs)
- [ ] Training complete: `models/luminai-lora/` and `models/luminai-lora_merged/` exist
- [ ] Merged weights verified: `ls models/luminai-lora_merged/*.safetensors`

## GGUF Conversion

- [ ] Install llama-cpp: `pip install llama-cpp-python`
- [ ] Convert to GGUF: `python -m llama_cpp.llama_quantize ...`
- [ ] GGUF file created: `models/luminai-lora_merged/luminai-unsloth.gguf` (~4GB)
- [ ] File size reasonable (not 0 bytes or >20GB)

## Ollama Integration

- [ ] Ollama running: `ollama serve` in background
- [ ] Modelfile in place: `models/Modelfile`
- [ ] Create Ollama model: `ollama create luminai-unsloth -f models/Modelfile`
- [ ] Model listed: `ollama list | grep luminai-unsloth`
- [ ] Health check passes: `curl -s http://localhost:11434/api/tags | jq .models`

## Backend Integration

- [ ] FastAPI backend running: `./scripts/start_backend.sh`
- [ ] Chat endpoint responds: `curl http://localhost:8000/api/chat/health`
- [ ] Schema updated: `ChatRequest.model` supports "luminai-unsloth"

## End-to-End Testing

- [ ] Test with base model: `{"model": "llama3.2", "message": "Hello"}`
- [ ] Test with fine-tuned: `{"model": "luminai-unsloth", "message": "I'm anxious"}`
- [ ] Response includes `witness_trace`
- [ ] `effective_resonance` computed correctly
- [ ] Session history persists: GET `/api/chat/sessions/{id}`

## Web UI Testing

- [ ] Ollama Web UI running: http://localhost:8080
- [ ] Select `luminai-unsloth` from model dropdown
- [ ] Send test message (should recognize LuminAI persona blend)
- [ ] Response time acceptable (<30s for first token)

## Performance Validation

- [ ] VRAM usage during inference: `nvidia-smi`
- [ ] Throughput: ~20-50 tokens/sec (acceptable for local model)
- [ ] No memory leaks: test repeated /api/chat calls
- [ ] Error handling: test with invalid model name, malformed JSON

## Production Hardening

- [ ] Load test: 5+ concurrent sessions
- [ ] Witness trace logs stored: `logs/witness_traces.jsonl`
- [ ] Error logs reviewed: no CUDA errors, no abandoned requests
- [ ] API documentation updated: http://localhost:8000/docs
- [ ] Commit all changes: `git add . && git commit -m "..."`

## Deployment to Cloud (Optional)

- [ ] Weights pushed to HuggingFace Hub (private or public)
- [ ] Docker image built with Ollama + fine-tuned model
- [ ] Azure Container Registry tag: `luminai-unsloth:latest`
- [ ] Helm chart or ARM template for Kubernetes/Azure

## Rollback Plan

If issues arise:

```bash
# Revert to base model
ollama delete luminai-unsloth
ollama pull llama3.2
# Update API to use "llama3.2"
```

## Success Criteria

✅ **System working when:**

- Fine-tuned model loaded in Ollama
- API responds with persona-aligned outputs
- Witness traces logged correctly
- Web UI functional with new model
- No CUDA errors after 1000 API calls

---

## Command Reference

```bash
# Activate environment
source unsloth-venv/bin/activate

# Train
python scripts/unsloth_train.py --num_epochs 3 --batch_size 4

# Convert to GGUF
cd models/luminai-lora_merged
python -m llama_cpp.llama_quantize pytorch_model.bin luminai-unsloth.gguf q4_k_m

# Create Ollama model
ollama create luminai-unsloth -f models/Modelfile

# Test
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"I need grounding","model":"luminai-unsloth"}'

# Monitor
watch -n 1 nvidia-smi
tail -f logs/witness_traces.jsonl
```

---

**Status:** Ready for deployment
**Last Updated:** December 5, 2025
