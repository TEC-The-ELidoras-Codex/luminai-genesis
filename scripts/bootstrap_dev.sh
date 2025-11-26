#!/usr/bin/env bash
set -e

echo "🔧 Bootstrapping LuminAI Genesis development environment..."

# Python virtualenv
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt || true

# Node
echo "📦 Installing Node dependencies..."
if [ -f "ui/package.json" ]; then
  cd ui
  npm install
  cd ..
fi

# Pre-commit hooks
echo "🔐 Installing pre-commit hooks..."
pip install pre-commit
pre-commit install

echo "🧠 Initializing Persona Registry..."
mkdir -p runtime/personas
touch runtime/personas/.keep

echo "✨ Done. Welcome, Steward."
