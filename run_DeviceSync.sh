#!/usr/bin/env bash
set -Eeuo pipefail

# --- config ---
CONDA_HOME="/home/dieter/miniforge3"
ENV_NAMES=("default" "default311")  # list in priority order
APP_DIR="/home/dieter/Dropbox/PythonRepos/DeviceSync"
PY_SCRIPT="main.py"
# --------------

# Initialize conda for non-interactive shells
if [ -f "$CONDA_HOME/etc/profile.d/conda.sh" ]; then
  # shellcheck source=/dev/null
  . "$CONDA_HOME/etc/profile.d/conda.sh"
else
  echo "ERROR: conda.sh not found at $CONDA_HOME/etc/profile.d/conda.sh" >&2
  exit 1
fi

# Try to activate the first available environment
ENV_FOUND=""
for env in "${ENV_NAMES[@]}"; do
  if conda env list | awk '{print $1}' | grep -qx "$env"; then
    conda activate "$env"
    ENV_FOUND="$env"
    break
  fi
done

if [ -z "$ENV_FOUND" ]; then
  echo "ERROR: None of the specified environments found: ${ENV_NAMES[*]}" >&2
  exit 1
fi

# Optional diagnostics (comment out once happy)
echo "[debug] Activated env: $ENV_FOUND"
echo "[debug] python:  $(command -v python)"
echo "[debug] rshell:  $(command -v rshell)"

# Run the app
cd "$APP_DIR"
exec python "$PY_SCRIPT"
