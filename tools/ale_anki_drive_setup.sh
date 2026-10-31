#!/bin/bash
# Local Mac setup only; never executes in GitHub Actions.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HOME/Library/Application Support/ClinicalOS-ALE"
mkdir -p "$VAULT"
chmod 700 "$VAULT"
python3 -m venv "$VAULT/venv"
"$VAULT/venv/bin/python3" -m pip install --disable-pip-version-check -r "$HERE/requirements-ale.txt"
"$VAULT/venv/bin/python3" "$HERE/ale_anki_drive_sync.py" configure
"$VAULT/venv/bin/python3" "$HERE/ale_anki_drive_sync.py" authorize
echo "SETUP_COMPLETE | To upload after iPhone + Mac sync, run:"
echo "bash tools/ale_anki_drive_run.sh"
