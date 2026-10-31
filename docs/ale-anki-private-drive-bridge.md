# ALE-01: owner-local OAuth sync from Anki Desktop to private Google Sheet

**Status:** new code plus synthetic tests only. Real Mac Anki, iPhone, OAuth consent and Google readback are NOT yet validated. This is an opt-in extension of the strictly read-only Anki probe in the same PR: **Anki remains read-only; only the explicitly configured owner-private Google Sheet receives appended rows.** Do not run in public GitHub Actions, Codex Cloud or another public runner.

## Troubleshooting: unexpected Xcode / Rust download on Mac

If the terminal mentions `cryptography-50.x.tar.gz`, `maturin`, `rustc`, `xcode-select: No developer tools were found`, or requests a large Apple Command Line Tools install, **cancel the developer-tool installation**. The older Mac Python can be x86_64 (including Rosetta on Apple Silicon); `cryptography` 49+ no longer ships macOS Intel wheels, so unrestricted pip tries to build from source. This does NOT mean Google Sheets or Anki needs Xcode.

Fix delivered in this PR: `tools/requirements-ale.txt` constrains `cryptography>=48.0.1,<49` (48.0.1 provides macOS universal2 wheel usable on CPython 3.9 x86_64) and `tools/ale_anki_drive_setup.sh` uses `pip --only-binary=:all:` so it cannot silently compile Rust/native dependencies.

With an existing checkout on the Mac, do **not** clone over it or delete it. From its root:

    git status --short
    git pull --ff-only
    bash tools/ale_anki_drive_setup.sh

If `git pull --ff-only` fails due to modified files or branch mismatch, stop and report the **redacted** message rather than using `git reset --hard`. The private OAuth JSON and local state live outside Git and must never be committed. The failed dependency installation is safe to re-run with updated requirements; it did not establish Google OAuth.

PyPI source: https://pypi.org/project/cryptography/48.0.1/ and upstream release note: https://cryptography.io/en/49.0.0/changelog/ .

## First-run setup

1. Confirm Mac Anki Desktop is open, AnkiConnect installed and bound to 127.0.0.1:8765. Sync iPhone AnkiMobile **first**, then sync Mac Anki.
2. At https://console.cloud.google.com/ create/select a Google Cloud project you control. Enable the Google Sheets API.
3. Configure Google Auth Platform / OAuth consent screen. Add your Google account as a test user if the OAuth app is in Testing.
4. Create an OAuth client ID of application type **Desktop app**, download its JSON to the Mac only. Never upload the OAuth JSON to GitHub, ChatGPT or Drive.
5. The existing owner-only spreadsheet must contain an **Error_Events** tab with its current 14 columns. The script refuses to create a replacement or silently change headers.
6. From repository root of the PR branch, in Mac Terminal run:

    bash tools/ale_anki_drive_setup.sh

   This installs minimal dependencies into an owner-private Python environment, then asks for the existing private Google Sheet URL and the LOCAL path to the Desktop OAuth JSON. It opens Google's own browser consent flow. You approve the requested scope yourself. **The assistant cannot do this sign-in for you.**

7. After synchronizing iPhone to AnkiWeb and then Mac Anki, from repository root run:

    bash tools/ale_anki_drive_run.sh

   Expected generic status lines:

    OWNER_PRIVATE_SYNC_OK | new_review_events=N
    DUPLICATE_SAFE | already_recorded=M

   N>0 confirms events were appended and readback verified in the owner-only Sheet. N=0 can be normal if no new review occurred. To confirm iPhone provenance, perform the controlled one-card review workflow from docs/ale-anki-readonly-quickstart.md; revlog itself does not prove which device originated an arbitrary event.

## Privacy/authorization

- OAuth scope: https://www.googleapis.com/auth/spreadsheets. This grants **Sheets read/write** access at the OAuth account level; Google does not make this scope sheet-specific. The application restricts its network calls to the single locally configured spreadsheet and the Error_Events tab. If account-wide Sheets authorization is unacceptable, STOP; a Picker-enabled drive.file design would require a different verified flow.
- OAuth tokens, client JSON, sheet ID and sync cursor are stored outside the repo at ~/Library/Application Support/ClinicalOS-ALE/ with private directory/file permissions. This is an owner Mac directory, not a GitHub or cloud runner folder.
- The script uploads only event identity, review timestamps, native Anki card/note IDs, raw answer button numbers, and explicit UNKNOWN/NOT_DIAGNOSED labels to the owner-private spreadsheet. It does not upload Front/Back, user answers, deck names, model guesses or credentials.
- AnkiConnect remains strictly read-only (version, deckNames, cardReviews, cardsInfo). No edit, delete, FSRS override, AnkiWeb sync trigger, remote tunnel or port exposure.
- Mac need not always be online; the sync must run after normal device synchronization.
- An external OAuth app kept in Google's Testing state usually gets a **7-day-expiring refresh token** for this scope. Verify the account's OAuth publication/renewal status before claiming unattended durability; consent is initially required and may later need renewal.

## Sync semantics

- Incremental revlog events are joined by stable review timestamp plus Anki card ID. The bridge validates the 14-column header, compares event keys in the private sheet, appends only unseen events, reads keys back, and only then advances a private local cursor.
- If Google accepts an append but the response is lost, rerun: the bridge checks remote keys first to avoid double append. Existing duplicate event keys are a blocking error. Local lock prevents concurrent copies of the same uploader on the Mac.
- First run looks back 7 days by default, with CLI --lookback-days adjustable 1–90. It is not full historical ingestion.
- Missing current note (for example previously deleted card) is recorded as blank, not guessed. Concept family mapping is deliberately blank until an explicit mapping is separately proven.
- No automatic Anki card changes or private sheet deletions occur. No model prediction is inferred from a review-button result.

## Offline testing

    cd tools
    python3 -m unittest -v test_ale_anki_readonly.py test_ale_anki_drive_sync.py

Five original probe tests plus ten new synthetic bridge tests are supplied. A local synthetic pass is not a Mac live pass. GitHub website CI passing is not equivalent to testing OAuth or AnkiConnect.

## Later gates

1. Actual owner Mac OAuth consent and private Sheet sync with N>0 and safe retry N=0.
2. Verify existing scheduled ChatGPT execution can access newly synced owner-only rows; interactive connector access alone is insufficient.
3. Map actual Anki note/card to a stable concept family without publishing learner records to GitHub.
4. Create and readback a justified private decision; only later test safe card writes in an isolated gated PR.

Keep all #137 frozen 72h experiment runs and all five ChatGPT automations unchanged. No inference about scheduled autonomy success from these offline tests.

References:
- https://github.com/ankicommunity/anki-desktop-addon-connect
- https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append
- https://googleapis.dev/python/google-auth-oauthlib/latest/reference/google_auth_oauthlib.flow.html
- https://developers.google.com/identity/protocols/oauth2


## Read-only private integrity audit (2026-10-31)

After any normal iPhone → AnkiWeb → Mac → owner-private Sheets sync, update your existing Mac checkout without deleting local OAuth:

    cd "$HOME/ClinicalOS-ALE-bridge"
    git status --short
    git pull --ff-only origin experiment/ale01-anki-mobile-readonly-probe-20261031

If git reports local modifications or branch mismatch, stop (do not hard reset); private local tokens are outside this checkout.

Run the new **Google-Sheets-only audit** (Anki need not be open):

    "$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_anki_drive_sync.py audit

Expected on a single real unmapped review:

    OWNER_PRIVATE_AUDIT_PASS | events=1 | duplicates=0 | missing_family_links=1

The audit independently checks source-event/card identity consistency, uniqueness, review button validity, note ID shape, valid timestamp ordering, and read-only sync status. It prints only aggregate counts, never private event/card/note IDs or card text. An integrity PASS **does not** establish Concept Family mastery, explain a wrong answer, prove iPhone provenance on its own, or verify that a ChatGPT **scheduled** run can read the Sheet. The current user's ChatGPT interactive private-record read/write already produced a **proposal-only, zero-card-mutation** decision; scheduled unattended access is a separate pending gate.

