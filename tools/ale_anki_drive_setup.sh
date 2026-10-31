#!/bin/bash
# Mac-local installation only; never run in GitHub Actions.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HOME/Library/Application Support/ClinicalOS-ALE"
mkdir -p "$VAULT"
chmod 700 "$VAULT"
python3 -m venv "$VAULT/venv"
# Explicitly refuse source compilation. macOS Intel/Rosetta Python otherwise
# triggers multi-GB Apple Command Line Tools / Rust for cryptography >=49.
if ! "$VAULT/venv/bin/python3" -m pip install --disable-pip-version-check --only-binary=:all: -r "$HERE/requirements-ale.txt"; then
  echo >&2 "ALE_DEPENDENCY_SETUP_FAILED | No compatible prebuilt wheels. Do not install Xcode/Rust solely for this bridge."
  echo >&2 "Check your Python version/architecture, then request a compatible wheel-based fix."
  exit 1
fi
"$VAULT/venv/bin/python3" "$HERE/ale_anki_drive_sync.py" configure
"$VAULT/venv/bin/python3" "$HERE/ale_anki_drive_sync.py" authorize
echo "SETUP_COMPLETE | To upload after iPhone + Mac sync, run:"
echo "bash tools/ale_anki_drive_run.sh"
