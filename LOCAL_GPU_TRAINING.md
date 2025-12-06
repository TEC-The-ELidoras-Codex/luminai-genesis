# Local GPU Training Setup: AMD RX 580 Edition

**Your Hardware**: AMD Ryzen 5 3600 (12 threads) + RX 580 (8GB VRAM) + 32GB RAM  
**Goal**: 100% local, FREE fine-tuning pipeline - NO CLOUD REQUIRED  
**Timeline**: 2-3 hours setup, then own the pipeline forever

---

## Why This Matters

You have a **BEAST** of a machine. RX 580 with 32GB system RAM is MORE than capable of:

- Fine-tuning 7B-8B models locally
- Running inference at 20-40 tokens/sec
- Training on 49-500 examples without breaking a sweat

Cloud providers charge $0.50-$2/hour for inferior GPUs. Your setup is **FREE after initial setup**.

---

## Phase 1: Install ROCm (AMD's CUDA)

ROCm enables PyTorch to use your RX 580 for acceleration.

### Prerequisites Check

```bash
# Verify you have RX 580
lspci | grep -i amd | grep -i vga
# Should show: "Ellesmere [Radeon RX 470/480/570/570X/580/580X/590]"

# Check kernel version (need 5.15+)
uname -r
# You have: 6.17.0-7-generic ✅

# Check free disk space (need 10GB+)
df -h /
# You have: plenty ✅
```

### Install ROCm

```bash
cd ~/luminai-genesis
./scripts/install_rocm_rx580.sh
```

This script will:

1. Add ROCm 6.3 repository
2. Install AMDGPU kernel driver
3. Install ROCm runtime (HIP, device libs)
4. Add you to `video` and `render` groups
5. Set environment variables for RX 580 (gfx803)

**REBOOT REQUIRED** after installation.

### Verify ROCm Installation

```bash
# After reboot, check GPU is detected
rocm-smi

# Should show:
# ========================= ROCm System Management Interface =========================
# GPU  Temp   AvgPwr  SCLK    MCLK     Fan     Perf  PwrCap  VRAM%  GPU%
# 0    XX°C   XXW     XXXMhz  XXXXMhz  XX.X%   auto  XXXW    0%     0%

# Check architecture
rocminfo | grep 'Name:.*gfx'
# Should show: gfx803 (RX 580's architecture)
```

---

## Phase 2: Install PyTorch with ROCm

Remove CUDA PyTorch, install ROCm version.

```bash
# Activate your environment
cd ~/luminai-genesis
source unsloth-venv/bin/activate

# Remove CUDA PyTorch
pip uninstall torch torchvision torchaudio -y

# Install PyTorch with ROCm 6.2 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2

# Verify GPU is detected
python -c "import torch; print(f'ROCm available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Should output:
# ROCm available: True
# GPU: AMD Radeon RX 580 Series
```

---

## Phase 3: Install Unsloth (ROCm-compatible)

Unsloth works with ROCm, but needs special flags.

```bash
# Still in unsloth-venv
pip install "unsloth[rocm] @ git+https://github.com/unslothai/unsloth.git"

# Verify Unsloth can see GPU
python -c "from unsloth import FastLanguageModel; print('Unsloth ready!')"
```

**Note**: If Unsloth fails with ROCm, we'll use standard HuggingFace Transformers (still fast with your 32GB RAM).

---

## Phase 4: Fine-Tune Locally

Your 49-example dataset is ready. Now train.

### Option A: Unsloth (if ROCm install succeeded)

```bash
cd ~/luminai-genesis
source unsloth-venv/bin/activate

# Train with GPU acceleration
python scripts/unsloth_train.py \
  --data_path data/training/persona_sft_dataset_complete.jsonl \
  --output_dir models/luminai-lora \
  --num_epochs 3 \
  --batch_size 2 \
  --max_seq_length 1024

# Expected time: 20-40 minutes with RX 580
```

### Option B: Standard Transformers (if Unsloth has issues)

```bash
# Create fallback training script (uses HuggingFace directly)
python scripts/train_hf_fallback.py \
  --data_path data/training/persona_sft_dataset_complete.jsonl \
  --output_dir models/luminai-lora \
  --num_epochs 3

# Expected time: 40-90 minutes with RX 580
```

---

## Phase 5: Convert to GGUF for Ollama

After training, convert to Ollama-compatible format.

```bash
# Install llama.cpp tools
pip install llama-cpp-python

# Convert merged weights to GGUF
cd models/luminai-lora_merged
python -m llama_cpp.server \
  --model pytorch_model.bin \
  --n_gpu_layers 35 \
  --host 0.0.0.0 \
  --port 8080

# Or use llama.cpp directly for GGUF conversion
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make
./convert.py ~/luminai-genesis/models/luminai-lora_merged
./quantize ~/luminai-genesis/models/luminai-lora_merged/ggml-model-f16.gguf \
           ~/luminai-genesis/models/luminai-lora_merged/luminai-q4_k_m.gguf q4_k_m
```

---

## Phase 6: Deploy to Ollama

```bash
# Copy GGUF to models directory
cp models/luminai-lora_merged/luminai-q4_k_m.gguf models/

# Create Ollama model
ollama create luminai-rx580 -f models/Modelfile

# Test
ollama run luminai-rx580 "I'm experiencing panic. Help me ground."
```

---

## Timeline Expectations

| Phase                  | Duration       | Can Skip?               |
| ---------------------- | -------------- | ----------------------- |
| ROCm install           | 30-60 min      | ❌ Required             |
| Reboot + verify        | 5 min          | ❌ Required             |
| PyTorch ROCm           | 10-15 min      | ❌ Required             |
| Unsloth install        | 5-10 min       | ✅ Can use Transformers |
| Training (49 examples) | 20-40 min      | ❌ Core task            |
| GGUF conversion        | 5-10 min       | ❌ Required             |
| Ollama deployment      | 2 min          | ❌ Required             |
| **TOTAL**              | **~2-3 hours** | **Then FREE forever**   |

---

## Performance Expectations

### With RX 580 + ROCm

- **Training**: 20-40 min for 3 epochs (49 examples)
- **Inference**: 25-35 tokens/sec (llama-7b, q4_k_m quantization)
- **VRAM usage**: 6-7GB (RX 580 has 8GB - perfect fit)
- **System RAM**: 10-15GB during training (you have 32GB - plenty of headroom)

### Scaling to 200 examples

- **Training time**: 60-120 min (still FREE)
- **Model quality**: Significantly better persona alignment
- **Cost**: $0 (vs $5-10 on cloud)

---

## Troubleshooting

### "rocm-smi not found after install"

```bash
export PATH=$PATH:/opt/rocm/bin
rocm-smi
```

### "torch.cuda.is_available() returns False"

```bash
# Check environment variable for RX 580
export HSA_OVERRIDE_GFX_VERSION=8.0.3
python -c "import torch; print(torch.cuda.is_available())"
```

### "Unsloth fails to load with ROCm"

Use standard Transformers:

```bash
pip install transformers accelerate peft bitsandbytes datasets trl
# Use scripts/train_hf_fallback.py instead
```

### "Out of memory during training"

Reduce batch size:

```bash
python scripts/unsloth_train.py --batch_size 1 --gradient_accumulation_steps 4
```

---

## Why This Beats Cloud

| Aspect            | Your RX 580 Setup       | Cloud GPU (e.g., Colab Pro) |
| ----------------- | ----------------------- | --------------------------- |
| **Setup cost**    | $0                      | $10/month                   |
| **Training cost** | $0 (electricity ~$0.20) | $2-5 per run                |
| **Runs/month**    | Unlimited               | ~10-15 (before quota)       |
| **Privacy**       | 100% local              | Uploaded to cloud           |
| **Speed**         | 25-35 tok/sec           | 40-60 tok/sec (better GPU)  |
| **Learning**      | Full control, debugging | Black box                   |
| **Ownership**     | Forever                 | Subscription                |

**After 3 fine-tune runs, you've paid for the RX 580 vs cloud costs.**

---

## Next Steps

1. **Run ROCm install**: `./scripts/install_rocm_rx580.sh`
2. **Reboot**: `sudo reboot`
3. **Verify GPU**: `rocm-smi`
4. **Install PyTorch**: See Phase 2
5. **Fine-tune**: `python scripts/unsloth_train.py`
6. **Deploy to Ollama**: `ollama create luminai-rx580`
7. **Test in Web UI**: http://localhost:8080

---

**Your machine is a BEAST. Let's make it work for you, not rent someone else's.**

Ready to install ROCm? Run:

```bash
./scripts/install_rocm_rx580.sh
```

Then we'll train your 49-example dataset and deploy to Ollama. 100% local, 100% FREE.
