# Unsloth Fine-Tune Guide for LuminAI Genesis

Complete guide to train a persona-aligned model using Unsloth and serve it via Ollama.

## Quick Start

### 1. Activate Unsloth Environment

```bash
source unsloth-venv/bin/activate
```

### 2. Run Training (with merged model output)

```bash
python scripts/unsloth_train.py \
  --model_name "unsloth/llama-3-8b-bnb-4bit" \
  --output_dir "models/luminai-lora" \
  --num_epochs 3 \
  --batch_size 4
```

**Time estimate:** ~30-45 min (depending on GPU)
**VRAM required:** 12+ GB (the 4-bit quantization keeps it manageable)
**Output:** `models/luminai-lora/` (LoRA weights) + `models/luminai-lora_merged/` (full merged weights)

### 3. Convert Merged Weights to GGUF

You'll need `llama.cpp` tools:

```bash
pip install llama-cpp-python

# Download llama.cpp if not available
cd models/luminai-lora_merged
python -m llama_cpp.llama_quantize \
  pytorch_model.bin \
  luminai-unsloth.gguf \
  q4_k_m  # quantization type (q4 = 4-bit, k_m = medium)
```

**Time estimate:** ~5-10 min
**Output:** `models/luminai-lora_merged/luminai-unsloth.gguf` (~4-5GB)

### 4. Create Ollama Model

From project root:

```bash
# Option A: Serve using Modelfile (recommended)
ollama create luminai-unsloth -f models/Modelfile

# Option B: Test if GGUF loads directly
ollama create luminai-unsloth \
  -f - <<EOF
FROM models/luminai-lora_merged/luminai-unsloth.gguf
SYSTEM "You are LuminAI Genesis..."
EOF
```

### 5. Verify in Ollama Web UI

Visit http://localhost:8080 and select `luminai-unsloth` from model dropdown.

### 6. Test in FastAPI Backend

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-fine-tuned",
    "message": "I am struggling with anxiety.",
    "model": "luminai-unsloth"
  }' | jq '.response'
```

---

## Training Data Format

The dataset is JSONL (one JSON object per line):

```json
{
  "text": "User: <user message>\nAssistant: <assistant response with persona blend>"
}
```

Each response should include:

- **Grounded somatic guidance** (Adelphia)
- **Empathic integration** (LuminAI)
- **Transparent safety boundaries** (Ely)
- **Witness trace** (audit metadata)

See: `data/training/persona_sft_dataset.jsonl` for examples.

### Add Your Own Training Data

Append to the JSONL file:

```bash
cat >> data/training/persona_sft_dataset.jsonl <<EOF
{
  "text": "User: <your question>\nAssistant: <your grounded response with witness_trace>"
}
EOF
```

---

## Training Configuration

Edit `scripts/unsloth_train.py` for custom hyperparameters:

| Parameter        | Default | Notes                                           |
| ---------------- | ------- | ----------------------------------------------- |
| `r` (LoRA rank)  | 16      | Higher = more capacity, more VRAM               |
| `lora_alpha`     | 16      | Scale factor for LoRA updates                   |
| `lora_dropout`   | 0.05    | Regularization                                  |
| `num_epochs`     | 3       | More epochs = stronger adaptation (may overfit) |
| `batch_size`     | 4       | Reduce if OOM; increase if underutilizing GPU   |
| `learning_rate`  | 2e-4    | Standard for LoRA; lower = safer                |
| `max_seq_length` | 1024    | Longer = more context, more VRAM                |

Recommended for resource-constrained setups:

```python
batch_size = 2
num_epochs = 2
learning_rate = 1e-4  # More conservative
max_seq_length = 512  # Shorter sequences
```

---

## Serving Options

### Option 1: LoRA via Ollama (simplest)

Create a Modelfile pointing to base + LoRA:

```dockerfile
FROM llama3.2
ADAPTER models/luminai-lora
SYSTEM "You are LuminAI Genesis..."
```

Then: `ollama create luminai-unsloth -f Modelfile`

**Pros:** Smaller download (~200MB LoRA), fast iteration
**Cons:** Base model must match exactly; Ollama needs LoRA support (check version)

### Option 2: Merged + GGUF (most compatible)

Merge LoRA into base, quantize to GGUF, serve as standalone model.

**Pros:** Works everywhere; single model file; no version matching
**Cons:** Larger file (~4-5GB for Q4 quantization)

### Option 3: Merged + Safetensors (hybrid)

Convert merged weights to Safetensors format for HuggingFace Hub, serve from API.

**Pros:** High quality; easy to share/version control
**Cons:** Requires inference server with Safetensors support

---

## Troubleshooting

### "CUDA out of memory"

- Reduce `batch_size` to 2 or 1
- Reduce `max_seq_length` to 512
- Use `load_in_4bit=True` (already enabled by default)

### "Model not loading in Ollama"

- Verify GGUF file is valid: `file models/luminai-lora_merged/luminai-unsloth.gguf`
- Try lower quantization: `q2_k` or `q3_k_m` instead of `q4_k_m`
- Check Ollama version: `ollama --version` (should be recent)

### "Training loss not decreasing"

- Increase `learning_rate` (e.g., 5e-4)
- Verify training data quality (examples should show good persona blend)
- Check that tokenizer matches base model

### "Fine-tuned model forgets base knowledge"

- Reduce `num_epochs` (too many epochs = overfitting to training data)
- Increase `lora_dropout` to 0.1 for more regularization
- Use balanced dataset (crisis + general + technical examples)

---

## TGCR Integration

The fine-tuned model should output structured responses:

```json
{
  "response": "<empathic grounded text>",
  "persona_weights": {
    "adelphia": 0.4,
    "luminai": 0.3,
    "ely": 0.3
  },
  "witness_trace": "model=luminai-unsloth, persona_blend=default_crisis, temp=0.7, r'=0.75",
  "effective_resonance": 0.75
}
```

The backend (`backend/routers/chat.py`) will extract and log this metadata.

---

## Next Steps

1. **Collect more data**: Add crisis conversations, grounding techniques, boundary-setting examples.
2. **Evaluate**: Use `eval_data/` for holdout test set. Measure:
   - Persona accuracy (does it recognize personas?)
   - Safety compliance (does it escalate appropriately?)
   - Coherence (does response match context?)
3. **Iterate**: Fine-tune in cycles. Each round improves specificity.
4. **Deploy**: Push merged weights to HuggingFace Hub for easier team access.

---

## References

- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [Ollama Model Creation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- [llama.cpp Quantization](https://github.com/ggerganov/llama.cpp#quantization)
- [LuminAI Genesis Docs](../docs/ARCHITECTURE.md)
- [TGCR Core Thesis](../docs/manifesto/CORE_THESIS.md)

---

**Status:** Ready to train
**Last Updated:** December 5, 2025
**Canonical Reference:** docs/manifesto/CORE_THESIS.md
