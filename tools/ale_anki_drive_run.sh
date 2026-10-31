#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VAULT="$HOME/Library/Application Support/ClinicalOS-ALE"
if [ ! -x "$VAULT/venv/bin/python3" ]; then
  echo "LOCAL_SETUP_MISSING | Run: bash tools/ale_anki_drive_setup.sh"
  exit 1
fi
echo "Ensure iPhone AnkiMobile synced to AnkiWeb, then Mac Anki Desktop synced and is open."
exec "$VAULT/venv/bin/python3" "$HERE/ale_anki_drive_sync.py" sync
