# A02-02 | Exact-blob synthetic side-by-side audit (2026-10-30)

**Status:** OWNER_DIRECTED_RESEARCH / Draft-HOLD / excluded from the original 72-hour #137/#159 cohort. This is an experiment in *evaluation-contract completeness*, not a model-ability result.

## Inputs and reproducibility

- Original evaluator: PR #225 `tools/compare_skill_transfer.py`, verified Git blob SHA-1 `65645acf9d8df981c1ea6d359588c7075cb479aa`. The local comparator was reconstructed byte-for-byte and the Git blob digest matched the GitHub connector readback.
- New isolated guard: PR #249 `experiments/a02-growth-evidence/audit_growth_leakage.py`, originally Git blob `3e1ead7bbe7a4e0b3efa7313e7fbaecb107483e4`.
- Frozen synthetic 3-arm records with matching `case_id`, consistent source SHA, no fabricated provider, no paid calls; A02 cohort split train/development/holdout with declared time and family metadata.
- We ran **actual original #225 Python `evaluate()`** and A02 `audit()` on each constructed scenario. The original evaluator is limited to visible development data and itself never grants promotion.

## Observed synthetic matrix (12 scenarios)

| Scenario | Original #225 | A02 | Interpretation |
| --- | --- | --- | --- |
| Clean well-formed cohort | Development record accepted, no promotion | Structurally eligible, not validated | Legitimate control preserved |
| Different families sharing a public reference SHA | Accepted | Eligible | Do not conflate common article/source with same patient/case family |
| Train/holdout same canonical family | Accepted | REJECT: FAMILY_CROSS_SPLIT | Incremental synthetic detection |
| Development/holdout same canonical family | Accepted | REJECT: FAMILY_CROSS_SPLIT | Incremental synthetic detection |
| Evidence published after decision | Accepted | REJECT: FUTURE_OR_LATE_EVIDENCE | Incremental synthetic detection |
| Source observed after decision | Accepted | REJECT: FUTURE_OR_LATE_EVIDENCE | Incremental synthetic detection |
| Train label matured after fit | Accepted | REJECT: TRAIN_LABEL_NOT_MATURE_AT_FIT | Incremental synthetic detection |
| Naive timezone timestamp | Accepted | INVALID_INPUT: TIMESTAMP_TIMEZONE_MISSING | Incremental input rejection |
| Same true family falsely declared distinct IDs | Accepted | Eligible | **Neither can authenticate underlying family** |
| Retrospective holdout already resolved before protocol freeze | Accepted | Eligible | **Neither can establish true prespecification/sealing from caller timestamps** |
| Worker was shown hints | Rejected | Eligible | **Existing #225 gate should remain** |
| Native arm exposed to retrieval | Rejected | Eligible | **Existing #225 gate should remain** |

**Predefined counts (not estimates of real-world accuracy):** A02 caught 6/6 locally designed additional rule violations that original #225 schema could not represent; both accepted 2/2 locally designed legitimate controls; original #225 caught 2/2 of its existing control failures; A02 could not independently resolve 2/2 untrusted metadata / retrospective blinding ambiguities. N=12, manually constructed and unblinded, so no sensitivity/specificity inference or new #137 score.

## Distinctions that matter

1. **Complement, never replacement:** #225 checks per-arm equality, source hash, first-pass records, hints and exposure; A02 checks declared family splits and point-in-time evidence. Neither authenticates reviewer identity or external case-family ground truth.
2. **Canonical-family provenance:** same text, reference article or reused SHA is not inherently a duplicated patient/case. A blinded reviewer must maintain a confidential family/alias registry, externally controlled from worker and trial submitter.
3. **Retrospective vs prospective:** a case whose label matured before protocol freeze can still be a valid retrospective study *if independently sealed*. Without trustworthy preregistration/version attestations it must **not** be called prospective blind transfer. This requires a separate evidence gate, not an indiscriminate rejection of all retrospective studies.
4. **Evidence-time semantics:** distinguish clinical event time, publication time, actual ingestion/observation time, adjudication time and protocol freeze, not merely a filename or purported source year.
5. **No measured benefit yet:** these 12 synthetics are *mechanical proof of a contract gap*, not independent held-out detection rates, human time savings, medical correctness, or real unattended autonomy.

## Next independent validation

- Review the exact #225 and #249 versions with a distinct reviewer and independently authored challenge cases, including valid retrospective cohorts, family aliases and false rejection risk.
- Authenticate full-family provenance and evidence clocks without putting private case data, peer code, review labels or credentials in this public repository.
- Compare false catches and false exclusions on new fixed data; measure overhead. Reject adoption if increased detection does not justify complexity and false-blocking.
- Maintain Draft/HOLD. Do not change #225, #137, #159, current scheduler, main, the existing study window (ends 2026-11-01 06:20:15 UTC) or publication permissions.
