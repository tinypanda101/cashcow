#!/usr/bin/env bash
# Gets a fresh clone ready to run. Safe to run more than once.
# Run from Bash:  bash bin/setup.sh

set -euo pipefail
 
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
 
if python3 --version > /dev/null 2>&1; then
    PYTHON=python3
elif python --version > /dev/null 2>&1; then
    PYTHON=python
else
    echo "ERROR: Python not found. Install Python 3.10+ and re-run." >&2
    exit 1
fi
 
if ! command -v npm > /dev/null; then
    echo "ERROR: npm not found. Install Node.js and re-run." >&2
    exit 1
fi
 
cd "$ROOT/backend"
 
if [ -d ".venv" ]; then
    echo "backend/.venv already exists"
else
    echo "Creating backend/.venv"
    "$PYTHON" -m venv .venv
fi
 
if [ -f ".venv/Scripts/python.exe" ]; then
    VENV_PYTHON=".venv/Scripts/python.exe"
else
    VENV_PYTHON=".venv/bin/python"
fi
 
"$VENV_PYTHON" -m pip install --quiet -r requirements.txt
 
if [ -f ".env" ]; then
    echo "backend/.env already exists, not changing it"
else
    cp .env.example .env
    echo "Created backend/.env from .env.example. Fill in your values."
fi
 
cd "$ROOT/frontend"
npm install
 
echo "Setup complete"