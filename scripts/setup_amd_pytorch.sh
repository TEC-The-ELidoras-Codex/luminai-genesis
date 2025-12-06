#!/bin/bash
# Alternative AMD GPU setup for RX 580 on Ubuntu 25.10
# Uses Mesa/RADV drivers (already installed) + PyTorch ROCm prebuilt binaries

set -e

echo "=========================================="
echo "AMD RX 580 Setup for PyTorch (Ubuntu 25.10)"
echo "=========================================="
echo "Hardware: AMD Radeon RX 580 (Polaris)"
echo "Strategy: Use existing Mesa drivers + PyTorch ROCm binaries"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
   echo "❌ Don't run as root. Run as regular user with sudo."
   exit 1
fi

# Step 1: Install Mesa OpenCL for AMD (ICD loader)
echo "[1/5] Installing Mesa OpenCL runtime..."
sudo apt update
sudo apt install -y mesa-opencl-icd clinfo ocl-icd-libopencl1

# Step 2: Verify OpenCL can see GPU
echo "[2/5] Checking OpenCL device detection..."
clinfo | grep -i "Device Name" || echo "⚠️  OpenCL may not detect GPU (non-critical)"

# Step 3: Install ROCm-compatible libraries from Ubuntu repos
echo "[3/5] Installing AMD compute libraries..."
sudo apt install -y \
    rocm-core \
    rocm-smi \
    hip-runtime-amd \
    rocm-device-libs || echo "⚠️  Some ROCm packages unavailable (will use PyTorch fallback)"

# Step 4: Add user to video and render groups
echo "[4/5] Adding $USER to video and render groups..."
sudo usermod -a -G video "$USER"
sudo usermod -a -G render "$USER"

# Step 5: Set environment variables
echo "[5/5] Setting environment variables..."
cat >> ~/.bashrc << 'EOF'

# AMD RX 580 environment for PyTorch
export HSA_OVERRIDE_GFX_VERSION=8.0.3  # RX 580 = gfx803
export HIP_VISIBLE_DEVICES=0
export PYTORCH_HIP_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:512
EOF

source ~/.bashrc

echo ""
echo "=========================================="
echo "✅ AMD GPU environment configured!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Log out and log back in (or reboot) for group changes"
echo ""
echo "2. Install PyTorch with ROCm support:"
echo "   source ~/luminai-genesis/unsloth-venv/bin/activate"
echo "   pip uninstall torch torchvision torchaudio -y"
echo "   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0"
echo ""
echo "3. Test GPU detection:"
echo "   python -c 'import torch; print(f\"GPU available: {torch.cuda.is_available()}\")'"
echo ""
echo "4. If GPU not detected, we'll use CPU training (slower but works)"
echo ""
echo "=========================================="
echo ""
