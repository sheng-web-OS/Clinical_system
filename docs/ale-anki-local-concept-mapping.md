# ALE-01 local concept mapping pilot

Status: implementation committed; owner Mac live mapping not yet verified.

After iPhone and Mac Anki synchronization, keep Anki Desktop open.

From a checkout of this Draft PR branch:

    cd "$HOME/ClinicalOS-ALE-bridge"
    git pull --ff-only origin experiment/ale01-anki-mobile-readonly-probe-20261031
    "$HOME/Library/Application Support/ClinicalOS-ALE/venv/bin/python3" tools/ale_anki_concept_map.py

The command previews the latest reviewed question locally, lists existing concept IDs,
and accepts a single selection. Choose 0 when no concept matches.
Type YES only if that card direction really tests the selected concept.

Successful owner-private readback: OWNER_PRIVATE_CONCEPT_LINK_OK
Skipping: OWNER_SKIPPED. Existing exact link: ALREADY_LINKED.

No Anki card or FSRS changes. Do not infer cognitive cause or general mastery.
Only the specific card direction receives a proposed owner-confirmed concept link.
Other cards from the same note are not automatically linked.
Scheduled private-Drive access requires a separate real-world check after #137 closeout.

Synthetic unit checks:

    cd tools
    python3 -m unittest -v test_ale_anki_concept_map.py

## Unmatched cards: owner-local skip

For a review card that tests none of the existing Concepts, type `0`. No cloud mapping is written and Anki remains unchanged. The updated Mac script stores the skipped card ID **only** under `~/Library/Application Support/ClinicalOS-ALE/concept_map_skips.json` (private file mode 0600), associated with a fingerprint of the current owner-private concept catalog. Re-running on the same catalog advances past that card instead of repeatedly showing it; after the private Concepts catalog changes, an explicitly skipped card remains skipped; catalog updates never silently undo an owner skip. No skips or identifiers are recorded on public GitHub. Do not select an overly broad concept to force coverage.

Older versions of this tool had no persistent skip; first `git pull --ff-only` then choose `0` to activate local skip persistence. An already-running pre-update process safely skips without recording the new skip state.
