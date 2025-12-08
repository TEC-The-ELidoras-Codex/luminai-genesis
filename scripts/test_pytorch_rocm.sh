#!/bin/bash
# Test AMD RX 580 with PyTorch ROCm
# Run this AFTER logging out/in or rebooting

echo "=========================================="
echo "Testing AMD RX 580 + PyTorch ROCm"
echo "=========================================="

# Activate environment
cd ~/luminai-genesis
source unsloth-venv/bin/activate

# Remove old CUDA PyTorch
echo "[1/3] Removing CUDA PyTorch..."
pip uninstall -y torch torchvision torchaudio 2>/dev/null || true

# Install PyTorch with ROCm 6.0
echo "[2/3] Installing PyTorch with ROCm 6.0 support..."
echo "This will download ~2GB, may take 5-10 minutes..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0

# Test GPU detection
echo "[3/3] Testing GPU detection..."
python3 << 'EOF'
import torch

print("\n" + "="*50)
print("PyTorch ROCm Test Results")
print("="*50)

# Check if CUDA (ROCm) is available
cuda_available = torch.cuda.is_available()
print(f"GPU Available: {cuda_available}")

if cuda_available:
    print(f"GPU Count: {torch.cuda.device_count()}")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    print("\n✅ SUCCESS! Your RX 580 is ready for training!")
    print("\nNext: Run fine-tuning with:")
    print("  python scripts/unsloth_train.py \\")
    print("    --data_path data/training/persona_sft_dataset_complete.jsonl \\")
    print("    --num_epochs 3 --batch_size 2")
else:
    print("\n⚠️  GPU not detected by PyTorch")
    print("Possible fixes:")
    print("1. Reboot if you haven't already")
    print("2. Check: rocminfo | grep gfx")
    print("3. Set: export HSA_OVERRIDE_GFX_VERSION=8.0.3")
    print("\nFalling back to CPU training (slower but works)")

print("="*50 + "\n")
EOF

echo ""
echo "Installation complete!"
