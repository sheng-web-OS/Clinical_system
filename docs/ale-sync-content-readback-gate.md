# ALE-01 / #259: immutable review-event readback gate

A **successful append response and key presence are insufficient** to attest review-event integrity. A bad rating or card/note identity in the owner-private Error_Events sheet would corrupt later Concept Family decisions while falsely advancing the local sync cursor.

This narrowly scoped patch reads the complete 14-column persisted event rows and compares immutable fields from a read-only current Anki revlog snapshot **both for already-present keys and immediately after append**. It preserves editable learning-diagnosis fields. For a card that no longer exists, the historical note ID cannot be independently checked; the bridge preserves the stored historical link rather than fabricating one. It never copies owner-private rows to public GitHub logs.

## Verification

The existing `tools/test_ale_anki_drive_sync.py` cases are supplemented by explicit corruption/lost-ack negative controls and made discoverable in the normal repository CI through `tests/test_ale_bridge_content_readback.py`.

Offline commands, from repository root:

```bash
python -m unittest discover -s tests -p test_ale_bridge_content_readback.py -v
(cd tools && python -m unittest -v test_ale_anki_drive_sync.py)
```

Required behavior: new normal append PASS, clean existing-key rerun idempotent PASS, lost-ACK clean retry PASS, altered event rating/note/card/identity HOLD with **no cursor commit**, and modified diagnosis annotations remain intact.

## Owner-local acceptance boundary

The original local OAuth/Anki read-only bridge remains the only authorized real sync interface. Merge or cherry-pick this repair into the owned #259 branch only after its author reviews the exact code/CI evidence. Then run one owner-local non-destructive check, preserving local OAuth tokens and private state; inspect only aggregate audit/readback statuses. This patch does not grant access to Mac or Google credentials, attach to existing automations, change FSRS, or infer concepts or unseen transfer.

This stacked PR targets #259; it is **not** an independent site feature or part of frozen #137's autonomy cohort.
