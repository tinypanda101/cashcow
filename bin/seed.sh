#!/usr/bin/env bash
# Seeds the database. Safe to run more than once.
# Run from Git Bash:  bash bin/seed.sh [--reset] [--yes]
 
set -euo pipefail
 
BACKEND="$(cd "$(dirname "${BASH_SOURCE[0]}")/../backend" && pwd)"
 
if [ -f "$BACKEND/.venv/Scripts/python.exe" ]; then
    PYTHON="$BACKEND/.venv/Scripts/python.exe"
else
    PYTHON="$BACKEND/.venv/bin/python"
fi
 
if [ ! -f "$PYTHON" ]; then
    echo "ERROR: backend/.venv not found. Run: bash bin/setup.sh" >&2
    exit 1
fi
 
cd "$BACKEND"
"$PYTHON" -m scripts.seed_data "$@"
 