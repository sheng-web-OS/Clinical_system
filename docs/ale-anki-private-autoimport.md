# ALE Anki Auto-import | private queue -> Mac -> Anki (opt-in)

**Scope:** This is an owner-private, **add-only** import consumer stacked on existing ALE-01 read-only Mac/Google Sheets bridge (integration PR #269). It is not deployed on the owner's Mac; it does not add a cloud schedule, public service, paid API, AnkiWeb remote API, or public personal-learning records. Existing owner skips are never reset. Auto-import is **disabled by default**.

## End-to-end flow

1. Authorized Clinical OS author/reviewer proposes a card in the existing owner-private Google Sheet, not GitHub.
2. Independently reviewed medical/source QA passes and a separate release decision marks the immutable payload ready. A string flag + URL alone is **attestation, not cryptographic proof of reviewer independence**. The importer does not judge medical truth.
3. At existing Mac 30-minute LaunchAgent wake (only while awake), read-only review upload/classification runs before the optional importer.
4. If locally opted in, importer preflights up to 10 released cards from up to 300 private rows, checks stable Anki IDs and compatibility with previously manually imported ALE26 pilot cards, adds only missing Basic notes into ClinicalOS::ALE decks, reads back actual Anki content, writes private Sheet receipt.
5. If cloud receipt fails after local add, next invocation detects and reconciles existing note without duplicating. Conflicts, changed payloads, unsafe HTML, missing QA, owner skip, wrong source and multiple matches fail closed. No existing notes are overwritten/deleted/suspended; FSRS is never changed.

**AnkiMobile:** A local Mac import is not an AnkiWeb or iPhone sync. Normal Anki Desktop <-> AnkiWeb sync and AnkiMobile sync are still necessary. This does not wake sleeping Mac, remotely connect to localhost, force sync or change FSRS.

## Existing owner-private spreadsheet schema

One-time owner-Mac enable creates the Card_Import_Queue tab **only in the Sheet already configured by the local OAuth bridge** if absent; it verifies A:L headers. Conflicting headers cause refusal. No card contents or private identifiers are placed in GitHub.

A:L column order:
A card_key (stable unique key such as ALE26-M08-01)
B front_html (Basic Front)
C back_html (Basic Back, evidence and Q3)
D tags (Anki space-separated)
E deck (ClinicalOS::ALE or child deck only)
F source_ref (original medical source URL)
G independent_review_ref (specific public GitHub review receipt URL; no private learner data)
H qa_status (INDEPENDENT_MEDICAL_QA_PASS)
I release_status (READY_TO_IMPORT or HOLD)
J import_status (PENDING / SKIPPED / HOLD / IMPORTED)
K anki_note_id (empty before import)
L content_sha256 (SHA256 of compact JSON [front_html, back_html], UTF-8, ensure_ascii=False)

Call the package helper q.digest(front, back) to construct the digest inside an authorized **private** authoring workflow. The existing signed-in ChatGPT connector may propose cards in the sheet if permitted; it cannot directly call the owner's local AnkiConnect. An author-model self-check comment must not count as independent medical QA.

The six previously delivered pilot cards are **not automatically queued**: their independent medical QA and prior Anki imports have not been verified. If already manually imported with ALE::pilot tag, exact Front/Back matching and ALE26 HTML marker can reconcile rather than duplicate; content disagreement halts.

## One-time owner-Mac setup

Only on the checkout including the ALE integration and this reviewed feature, after existing local OAuth and AnkiConnect setup:

    "$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_anki_import_queue.py status
    "$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_anki_import_queue.py enable
    "$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_anki_import_queue.py run
    "$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_anki_launchd.py status

If the LaunchAgent is absent, validate the existing read-only sync and use existing ale_anki_launchd.py install. Code committed to GitHub never installs it on the Mac. Enable is a **one-time opt-in for future QA-released cards**. Disable at any time via ale_anki_import_queue.py disable; this stops future adds but does not delete already imported notes.

## Acceptance (not yet claimed)

1. Exact code SHA, synthetic test suite and full CI.
2. Real owner-Mac opt-in and private Sheet schema; existing review uploader unaffected.
3. Exactly one QA-approved card enters owner-private queue; Mac wake imports exactly one local Basic note, tags/fields read back exactly, private receipt matches ID/hash; rerun makes no duplicates.
4. Lost receipt after Anki add -> reconciliation without second add.
5. Previous ALE26 pilot note matches or goes HOLD on conflict, never silently duplicates or overwrites.
6. Separately verify desktop -> AnkiWeb -> AnkiMobile sync.
7. Observe actual recall/unseen/delayed transfer; counts of added cards are not learning gains.

Non-goals: automatic rewrite of existing cards based only on Anki Again; unsupervised medical promotion; public personalized deck; claiming successful import on owner Mac before runtime acceptance.
