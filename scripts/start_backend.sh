#!/bin/bash
# Start LuminAI Genesis backend with Ollama integration
#
# Run from project root: ./scripts/start_backend.sh

set -e

cd "$(dirname "$0")/.."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r backend/requirements.txt

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo ""
    echo "WARNING: Ollama not detected at localhost:11434"
    echo "Start it in another terminal: ollama serve"
    echo ""
fi

# Start backend from project root (fixes import paths)
echo "Starting backend on http://localhost:8000..."
echo "Docs at: http://localhost:8000/docs"
echo ""

cd "$(dirname "$0")/.."
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
