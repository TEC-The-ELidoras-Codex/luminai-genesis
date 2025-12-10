#!/bin/bash
# Install ROCm for AMD RX 580 (Polaris/GCN 4.0) on Ubuntu 25.10
# This script sets up AMD GPU acceleration for PyTorch training
# Your hardware: 32GB RAM, Ryzen 5 3600, RX 580 - PERFECT for local ML

set -e

echo "=========================================="
echo "ROCm Installation for AMD RX 580"
echo "=========================================="
echo "Hardware: AMD Radeon RX 580 (Polaris)"
echo "RAM: 32GB (excellent for ML)"
echo "CPU: Ryzen 5 3600 (12 threads)"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
   echo "❌ Don't run as root. Run as regular user with sudo."
   exit 1
fi

# Step 1: Add ROCm repository (modern method for Ubuntu 22.04+)
echo "[1/6] Adding ROCm 6.3 repository..."
sudo mkdir -p /etc/apt/keyrings
wget -qO - https://repo.radeon.com/rocm/rocm.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/rocm.gpg
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.3/ ubuntu main" | sudo tee /etc/apt/sources.list.d/rocm.list

# Step 2: Update package list
echo "[2/6] Updating package list..."
sudo apt update

# Step 3: Install ROCm kernel driver
echo "[3/6] Installing ROCm kernel driver (amdgpu-dkms)..."
sudo apt install -y amdgpu-dkms

# Step 4: Install ROCm runtime
echo "[4/6] Installing ROCm runtime..."
sudo apt install -y rocm-hip-runtime rocm-device-libs

# Step 5: Add user to video and render groups
echo "[5/6] Adding $USER to video and render groups..."
sudo usermod -a -G video "$USER"
sudo usermod -a -G render "$USER"

# Step 6: Set environment variables
echo "[6/6] Setting ROCm environment variables..."
cat >> ~/.bashrc << 'EOF'

# ROCm environment for AMD RX 580
export ROCM_PATH=/opt/rocm
export HIP_VISIBLE_DEVICES=0
export HSA_OVERRIDE_GFX_VERSION=8.0.3  # RX 580 is gfx803
export PATH=$PATH:/opt/rocm/bin
EOF

source ~/.bashrc

echo ""
echo "=========================================="
echo "✅ ROCm installation complete!"
echo "=========================================="
echo ""
echo "⚠️  IMPORTANT: You must REBOOT for changes to take effect."
echo ""
echo "After reboot, verify installation:"
echo "  rocm-smi"
echo "  rocminfo | grep 'Name:.*gfx'"
echo ""
echo "Then install PyTorch with ROCm:"
echo "  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.2"
echo ""
read -p "Reboot now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo reboot
fi
