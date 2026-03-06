#!/usr/bin/env bash
set -Eeuo pipefail

# --- config ---
PY_SCRIPT="main.py"
# --------------

# Activate the virtual environment
VENV_PATH=".venv"
if [ -d "$VENV_PATH" ]; then
  source "$VENV_PATH/bin/activate"
else
  echo "ERROR: Virtual environment not found at $VENV_PATH" >&2
  exit 1
fi

# Optional diagnostics (comment out once happy)
echo "[debug] Activated venv: $VENV_PATH"
echo "[debug] python:  $(command -v python)"

# Run the app
exec python "$PY_SCRIPT"
