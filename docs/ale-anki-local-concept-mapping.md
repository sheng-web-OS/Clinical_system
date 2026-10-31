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