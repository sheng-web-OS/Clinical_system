# ALE Anki Auto-import | private queue -> Mac -> Anki (opt-in)

**Scope:** This is an owner-private, **add-only** import consumer stacked on existing ALE-01 read-only Mac/Google Sheets bridge (integration PR #269). It is not deployed on the owner's Mac; it does not add a cloud schedule, public service, paid API, AnkiWeb remote API, or public personal-learning records. Existing owner skips are never reset. Auto-import is **disabled by default**.

## End-to-end flow

1. Authorized Clinical OS author/reviewer proposes a card in the existing owner-private Google Sheet, not GitHub.
2. Independently reviewed medical/source QA passes and a separate release decision marks the immutable payload ready. A string flag + URL alone is **attestation, not cryptographic proof of reviewer independence**. The importer does not judge medical truth.
3. At existing Mac 30-minute LaunchAgent wake (only while awake), read-only review upload/classification runs before the optional importer.
4. If locally opted in, importer preflights up to 10 released cards from up to 300 private rows, checks stable Anki IDs and compatibility with previously manually imported ALE26 pilot cards, adds only missing Basic or native Cloze notes into ClinicalOS::ALE decks, reads back actual Anki content, writes private Sheet receipt.
5. If cloud receipt fails after local add, next invocation detects and reconciles existing note without duplicating. Conflicts, changed payloads, unsafe HTML, missing QA, owner skip, wrong source and multiple matches fail closed. No existing notes are overwritten/deleted/suspended; FSRS is never changed.

**AnkiMobile:** A local Mac import is not an AnkiWeb or iPhone sync. Normal Anki Desktop <-> AnkiWeb sync and AnkiMobile sync are still necessary. This does not wake sleeping Mac, remotely connect to localhost, force sync or change FSRS.

## Existing owner-private spreadsheet schema

One-time owner-Mac enable creates the Card_Import_Queue tab **only in the Sheet already configured by the local OAuth bridge** if absent; it verifies A:L headers. Conflicting headers cause refusal. No card contents or private identifiers are placed in GitHub.

A:L column order:
A card_key (stable unique key such as ALE26-M08-01)
B front_html (Basic Front, or native Cloze Text containing {{cN::answer::optional hint}})
C back_html (Basic Back, or Cloze Extra: source-grounded explanation and Q3 boundary)
D tags (Anki space-separated)
E deck (ClinicalOS::ALE or child deck only)
F source_ref (original medical source URL)
G independent_review_ref (specific public GitHub review receipt URL; no private learner data)
H qa_status (INDEPENDENT_MEDICAL_QA_PASS)
I release_status (READY_TO_IMPORT or HOLD)
J import_status (PENDING / SKIPPED / HOLD / IMPORTED)
K anki_note_id (empty before import)
L content_sha256 (SHA256 of compact JSON [front_html, back_html], UTF-8, ensure_ascii=False)

**Cloze-first compatibility (2026-10-31 engineering increment):** The 12-column private Sheet schema and the existing SHA256 digest are unchanged. The Mac importer selects native `Cloze` **only** when column B contains supported `{{c1::answer::hint}}` syntax; B maps to Anki `Text`, C to `Extra`. Repeated `c1` deletions within one note are one card; distinct `c1` and `c2` create sibling cards. Existing rows without deletion markers continue to use `Basic` / `Front` + `Back`. The Mac must have the standard `Cloze` note type; `modelNames` preflight aborts the entire bounded batch before any add if it is absent. After an add or recovered receipt, `notesInfo.cards` must contain exactly one valid sibling ID per distinct c-number; missing/mismatched cards block import confirmation. This still does not validate the actual rendered question CSS or medical answerability.

The importer **rejects**, rather than silently converting into Basic, malformed / unmatched cloze markup, c0 or 0-prefixed groups, empty deletions or hints, exact hint=answer disclosure, deletions without visible prompt context, nested/advanced multi-index syntax, or any cloze token in Extra. This narrow compatibility parser is intentional; it does *not* establish that the prompt is medically or semantically valid, nor does it inspect how the masked front actually renders on an owner's Anki theme. More advanced Anki cloze expressions remain on HOLD pending dedicated implementation/tests. No extra artificial one-blank or one-cloze-group limit is imposed on ordinary syntax.

**Quality gates are distinct:** A model-generated Concept Family preview (PR #260) is an *unreviewed candidate*, never a `READY_TO_IMPORT` card by itself. Import requires authenticated owner-private queue access, source review with an actual independent medical reviewer and separate release decision. The row's QA text/reference are presently only assertions, **not** proof of reviewer independence. An author-model self-review may not release a card. The importer performs deterministic structural and integrity validation, not the source review. First real private trial must demonstrate a useful clinical question with all c1 gaps hidden, appropriate hints, source-backed causal edges, a Q3 boundary/counterexample, and review of each generated sibling front before enabling continuous authoring.

Call the package helper q.digest(front, back) to construct the digest inside an authorized **private** authoring workflow. The existing signed-in ChatGPT connector may propose cards in the sheet if permitted; it cannot directly call the owner's local AnkiConnect. An author-model self-check comment must not count as independent medical QA.

The six previously delivered pilot cards are **not automatically queued**: their independent medical QA and prior Anki imports have not been verified. If already manually imported with ALE::pilot tag, exact Front/Back matching and ALE26 HTML marker can reconcile rather than duplicate; content disagreement halts.

## Graph-first candidate → private HOLD queue (not automatic approval)

PR #271 also supplies `tools/ale_anki_cloze_handoff.py`. Its pure `candidate_hold_row(proposal, card_key=..., deck=..., tags=..., source_url=...)` function consumes the JSON-like, graph-anchored Cloze preview returned by PR #260's `check_graph_anchored_cloze`. It verifies that the source-preview groups and each masked sibling front match the native Cloze text, then prepares the unchanged A:L private queue schema. It **forces** `PENDING_INDEPENDENT_MEDICAL_QA / HOLD / HOLD`, with an empty reviewer receipt, and never contacts Anki or Google. It does not promote a model's approval, fabricate a second reviewer, choose the owner-specific concept, or write a candidate to the private Sheet. The owner-private authoring workflow must handle identity, permissions, deduplication, and actual writing; no public fixture may contain private card text or learning status.

The missing path is **actual second-context medical/source reviewer acceptance and independently authorized private release**. No generative output, synthetic CI PASS, or this HOLD adapter can fill those gates. A future approved writer may append idempotent HOLD rows to the existing private Sheet, then separate QA can release *only* a reviewed, unmodified SHA256 payload. Revisions require returning to HOLD and a new review rather than silently changing a released row. Until the owner Mac is enabled and real source review, queue and Anki readbacks are performed, **zero actual automatic Anki additions are verified**.

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
3. Exactly one independently QA-approved native Cloze note enters owner-private queue; Mac wake creates the exact Text/Extra fields and stable tag, reads back the note ID and payload; repeat wake makes no duplicate. Verify sibling counts and masked fronts on actual Anki separately.
4. Lost receipt after Anki add -> reconciliation without second add.
5. Previous ALE26 pilot note matches or goes HOLD on conflict, never silently duplicates or overwrites.
6. Separately verify desktop -> AnkiWeb -> AnkiMobile sync.
7. Observe actual recall/unseen/delayed transfer; counts of added cards are not learning gains.

Non-goals: automatic rewrite of existing cards based only on Anki Again; unsupervised medical promotion; public personalized deck; claiming successful import on owner Mac before runtime acceptance.
