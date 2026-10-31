# ALE-01 | opt-in Mac background capture (not cloud Agent proof)

This narrow addition only schedules the **existing** Mac AnkiConnect read-only uploader.
It uses macOS user LaunchAgent and the already-authorized local Google OAuth
credentials. It neither installs another ChatGPT automation nor changes Anki
cards, FSRS, AnkiWeb, Clinical OS site, GitHub Actions, or public repositories.

**Limit:** launchd runs only while the user's Mac session is active/awake. It
cannot wake a sleeping Mac, force AnkiMobile to sync, or invoke Anki Desktop's
own AnkiWeb sync. The original consent/scope and refresh-token expiration
conditions still apply. New mobile reviews are not visible until the user
normally syncs iPhone to AnkiWeb and Mac Anki receives those records.

## Local opt-in (Mac only)

**Critical prerequisite:** this branch was originally stacked on #259 while #261
holds the full immutable event-content validation. The installer intentionally
refuses to start unless its checked-out uploader includes #261's remote
record-content reconciliation. Do **not** bypass this gate or edit it away.
The feature is a Draft until the branches are integrated safely and the
owner-Mac tests pass.

First run the existing `bash tools/ale_anki_drive_setup.sh`, complete the
OAuth and Anki checks, and verify a manual
`bash tools/ale_anki_drive_run.sh` succeeds against the **owner-private**
Google Sheet. Do not paste credentials, IDs or card content into GitHub.

From the checkout containing this stacked branch:

```bash
"$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" \
  tools/ale_anki_launchd.py install
"$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" \
  tools/ale_anki_launchd.py status
```

If installed, LaunchAgent checks every 30 minutes (plus on load); it skips
when Anki Desktop/AnkiConnect is unavailable. It performs no manual AnkiWeb
sync. The underlying uploader retains lock, remote content reconciliation,
duplicate detection, and fail-closed cursor. Logs remain **Mac-private** at
`~/Library/Application Support/ClinicalOS-ALE/logs/`, not in CI or Git.

To remove the scheduled runner without deleting any OAuth token or review
record:

```bash
"$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" \
  tools/ale_anki_launchd.py uninstall
```

To re-install after moving this checkout, uninstall then install with the
new absolute checkout path. Do not copy the user-specific generated plist
into public GitHub.

## Acceptance: three separate gates

1. **Offline engineering:** Python plist tests succeed, shell syntax valid.
2. **Owner-Mac:** install/status succeeds; two runs following a real normal
   Anki sync give one new event then zero duplicates; Anki is not modified.
3. **Cloud learning loop:** a real pre-existing ChatGPT scheduled Writer run
   reads the owner-only Sheet, compares evidence and actually updates
   `Next_Actions` or append-only proposal `Card_Decisions` with a reversible,
   measured decision. This third gate is **NOT proven by a local success**.

Only test with real review evidence in owner-private Google Drive. Never
upload personal review logs or OAuth JSON to a public PR/Action. No relation
to the frozen #137 72-hour trial cohort.
