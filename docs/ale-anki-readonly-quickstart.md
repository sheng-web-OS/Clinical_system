# ALE-01: iPhone AnkiMobile -> AnkiWeb -> Mac (read-only pilot)

**Status:** OFFLINE_UNIT_TESTED; LIVE_MAC_NOT_VERIFIED. This pilot proves only that a real iPhone review becomes readable on an already synced Mac and resolves to a card/note ID. It does **not** write to Google Drive, build Concept Families, diagnose errors, change cards, or provide an unattended GPT agent.

## Preconditions

- Official AnkiMobile on iPhone and Anki Desktop on Mac already use the same AnkiWeb account.
- On Mac Anki, enable **AnkiConnect** (officially documented add-on code **2055492159**): Tools -> Add-ons -> Get Add-ons -> code -> restart Anki. Third-party add-on; use a trusted download and review add-on configuration.
- Keep Anki Desktop **open**, with the expected profile loaded.
- Keep AnkiConnect listening **only on 127.0.0.1**, not a public/LAN interface; do not expose port 8765 to the internet. Never put API keys into logs, GitHub or Google Sheets.
- Standard Python 3; no pip dependencies. Run commands on **the Mac**, not an iPhone, GitHub Actions runner, or ChatGPT cloud.

## Controlled read-only verification

1. Sync iPhone AnkiMobile and then sync Mac Anki. Make sure the two clients have finished syncing.
2. In the Mac Terminal, from a clone of this branch, run:

       python3 tools/ale_anki_readonly.py baseline

   Expected status: `BASELINE_OK`, with only the number of decks printed.
3. Review **one** existing card in **AnkiMobile on iPhone**, then **synchronize the iPhone**. On Mac, click Synchronize; do not force a one-way upload/download.
4. Run:

       python3 tools/ale_anki_readonly.py verify

   Expected status: `REVIEW_LINK_OK` and `CARD_NOTE_LINK_OK` if the event was synced and AnkiConnect can read it.

5. If `NO_NEW_REVIEWS`, first inspect iPhone and Mac sync completion and run `verify` again; do not start over or modify cards. If an API/permission error appears, check AnkiConnect version and local configuration. A nonzero exit status is **not a pass**.

**Private storage:** Local Mac `~/Library/Application Support/ClinicalOS-ALE/iphone_anki_probe.json` stores the baseline and most recent verified review/card/note IDs with restrictive filesystem permissions. The script never prints card contents, tags, deck names or raw identifiers and never uploads them. **Do not commit this local JSON file or paste it into a public issue or chat.**

Only share the two status lines (or a redacted error) with the engineering reviewer. Actual iPhone provenance is evidenced by a *controlled one-card-between-baseline-and-verify test*; an arbitrary Anki revlog entry alone **does not contain verified device provenance**.

## Limitations / next gates

- Read-only actions are hard-allowlisted: `version`, `deckNames`, `cardReviews`, `cardsInfo`. No `sync`, `deleteNotes`, `updateNoteFields`, scheduling edit or `insertReviews` action is available in the probe.
- The last verified event's native Anki note/card IDs are **not** a Concept Family mapping. The next gate must establish an independent, durable concept ID and owner-only mapping, with source and retrieval-test validity.
- No real AnkiConnect, AnkiMobile or AnkiWeb data is accessible to the ChatGPT/GitHub cloud runtime at code-review time. Offline synthetic tests cannot certify actual sync or mobile origin.
- With multiple phone/Desktop reviews occurring in the test window, the result verifies one latest review and counts all new events; **it cannot attribute each to iPhone**. For unambiguous provenance perform the controlled single-review test, with no concurrent Mac reviews.
- A real user may have many decks. `cardReviews` is queried per deck only for review events after the baseline; repeated IDs across parent/subdeck results are deduplicated.
- If the user switches devices, official Anki guidance recommends syncing when finished on one device before using another. One-way conflict resolution can overwrite edits; this pilot never attempts automated resolution.

## Local offline tests

    cd tools
    python3 -m unittest -v test_ale_anki_readonly.py

**Release gate:** After a true Mac readback, record the result as private owner data; only publish non-sensitive status, without card/deck names, note IDs or review logs. Keep this pilot outside the currently frozen 72-hour autonomy trial.

Documentation:
- https://github.com/ankicommunity/anki-desktop-addon-connect
- https://docs.ankiweb.net/syncing.html
- https://docs.ankimobile.net/syncing.html
