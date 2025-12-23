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
import logging
import torch

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

logger.info("%s", "="*50)
logger.info("PyTorch ROCm Test Results")
logger.info("%s", "="*50)

# Check if CUDA (ROCm) is available
cuda_available = torch.cuda.is_available()
logger.info("GPU Available: %s", cuda_available)

if cuda_available:
    logger.info("GPU Count: %s", torch.cuda.device_count())
    logger.info("GPU Name: %s", torch.cuda.get_device_name(0))
    logger.info("GPU Memory: %.1f GB", (torch.cuda.get_device_properties(0).total_memory / 1024**3))
    logger.info("%s", "\n✅ SUCCESS! Your RX 580 is ready for training!")
    logger.info("\nNext: Run fine-tuning with:")
    logger.info("  python scripts/unsloth_train.py \\")
    logger.info("    --data_path data/training/persona_sft_dataset_complete.jsonl \\")
    logger.info("    --num_epochs 3 --batch_size 2")
else:
    logger.warning("%s", "\n⚠️  GPU not detected by PyTorch")
    logger.info("Possible fixes:")
    logger.info("1. Reboot if you haven't already")
    logger.info("2. Check: rocminfo | grep gfx")
    logger.info("3. Set: export HSA_OVERRIDE_GFX_VERSION=8.0.3")
    logger.info("\nFalling back to CPU training (slower but works)")

logger.info("%s", "="*50 + "\n")
EOF

echo ""
echo "Installation complete!"
