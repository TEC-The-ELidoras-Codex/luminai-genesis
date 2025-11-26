#!/usr/bin/env bash

if [ -d "venv" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
    echo "[Genesis] Virtual environment activated."
else
    echo "[Genesis] No venv found. Run: python3 -m venv venv"
fi
