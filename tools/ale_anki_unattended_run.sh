#!/bin/bash
# Owner-local read-only capture, then optional opt-in add-only Anki import.
set -euo pipefail
umask 077
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
VAULT="$HOME/Library/Application Support/ClinicalOS-ALE"
PY="$VAULT/venv/bin/python3"
if [[ ! -x "$PY" ]]; then
  echo "ALE_SETUP_MISSING"
  exit 0
fi
# Anki Desktop/AnkiConnect may not be running: skip without cloud access.
PROBE=$(/usr/bin/curl --silent --show-error --fail --max-time 3 \
  --header 'Content-Type: application/json' \
  --data '{"action":"version","version":6}' \
  'http://127.0.0.1:8765' 2>/dev/null) || {
  echo "ALE_LOCAL_ANKI_NOT_READY"
  exit 0
}
if ! printf '%s' "$PROBE" | "$PY" -c 'import json,sys; x=json.load(sys.stdin); sys.exit(0 if isinstance(x.get("result"),int) and x.get("error") is None else 1)'; then
  echo "ALE_ANKICONNECT_PROBE_FAILED"
  exit 0
fi
# Review capture is always first; failed synchronization stops classification.
# Each script uses the existing owner-private OAuth and the uploader lock.
"$PY" "$HERE/ale_anki_drive_sync.py" sync
# Tag-driven proposals are unconfirmed; prior owner skips remain excluded.
# No question text, credential, private card ID or concept ID enters public logs.
"$PY" "$HERE/ale_anki_auto_classify.py"
# Importer is disabled by default. Only owner-private QA-released queue rows
# can trigger an add-only Anki write; no old note or FSRS modification.
"$PY" "$HERE/ale_anki_import_queue.py" run
