# MedEinst clinical counterfactual to Clinical_system transfer pilot

**2026-10-29 | Draft / HOLD | Artifact + local mechanical Pilot.**
This is an additive adapter, NOT a second evaluator, autonomous agent or medical publishing workflow.

## Why this work exists

Existing Clinical_system has:
- [PR #224](https://github.com/sheng-web-OS/Clinical_system/pull/224): synthetic counterfactual packets, separate evaluator key and staged error accounting.
- [PR #225](https://github.com/sheng-web-OS/Clinical_system/pull/225): A=native / B=articles / C=articles+candidate Skill first-pass experiment, review/attempt integrity.
- [PR #235](https://github.com/sheng-web-OS/Clinical_system/pull/235): synthetic lexical source-gap detection.
- [Issue #133](https://github.com/sheng-web-OS/Clinical_system/issues/133) and [Issue #137](https://github.com/sheng-web-OS/Clinical_system/issues/137): existing failure and growth ledgers.

Missing: a small adapter from the [MedEinst dataset](https://github.com/zhui711/MedEinst) to **separate case packets and facilitator-only labels** without importing a medical agent framework. This patch fills only that gap; it does not duplicate either existing scorer or model transport.

## Research provenance and limitations

MedEinst (arXiv:2601.06636) offers control/trap pairs, with JSONL schema documented in [dataset_interface.md](https://github.com/zhui711/MedEinst/blob/main/docs/dataset_interface.md). The released ECR-Agent includes causal reasoning and memory modules. The dataset uses simulated cases derived from DDXPlus; review upstream provenance and rights before redistribution. **Verified upstream dataset card:** [zhui711/MedEinst](https://huggingface.co/datasets/zhui711/MedEinst/tree/main) lists CC BY 4.0, but this does not supersede upstream DDXPlus terms. The [published `test.jsonl` file](https://huggingface.co/datasets/zhui711/MedEinst/blob/main/test.jsonl), approximately 11.7 MB, advertises SHA-256 `b6b688fa41f788c17cdbf5076b5215782c9eb00efec1a3d3384c002836550a57` (verified 2026-10-29). Source blob identity is pinned; actual clinical contents were not downloaded or reviewed in this PR.

[MedR-Bench](https://github.com/MAGIC-AI4Med/MedRBench) evaluates reasoning quality, while [SDBench](https://github.com/microsoft/sdbench) evaluates sequential information acquisition. [FUTURE-AI](https://www.bmj.com/content/388/bmj-2024-081554.long) motivates provenance, robustness and oversight.

Published benchmark diagnoses are **not** independent medical adjudications; public cases may contaminate model pretraining. Differing control/trap labels do not prove a one-fact causal change or clinical realism. This dataset is a development instrument, NOT final unseen clinical validation.

## Implemented (offline, no API)

The new tool, tools/prepare_medeinst_holdout.py:

1. **Official mode (default):** requires the published `test.jsonl` SHA-256 above as well as the actual input bytes' matching digest; arbitrary self-hashed JSONL cannot masquerade as MedEinst. Synthetic development tests must explicitly pass `--source-mode synthetic-fixture`, and their output is labeled non-MedEinst. Requires 1–12 explicitly preselected pair IDs.
2. Validates bounded JSONL size, unique complete control/trap pairs, differing published labels, distinct narratives, and string IDs before writing. These are mechanical validity gates, not expert causal review.
3. Creates each narrative in its **own anonymous worker directory**, excluding IDs, variant type and label fields. Cases are randomly permuted.
4. Saves a separate **facilitator-only** key with pair identity, labels and exact packet SHA. Both output roots must be new, disjoint and outside the public repository, with private creation permissions.
5. Sets NOT_RUN, model_calls=0, medical_validated=false and skill_transfer_validated=false. There are no external calls, model judgments or publications.

**Privacy rule:** Only supply one worker packet directory to each isolated worker. Do not mount the entire worker parent or the facilitator directory. Keep raw datasets, answers, reviewer notes and model outputs out of this public repository and public Actions.

### Example in an authorized private environment

~~~sh
sha256sum /secure/datasets/medeinst/test.jsonl
python tools/prepare_medeinst_holdout.py \
  --dataset /secure/datasets/medeinst/test.jsonl \
  --expected-sha256 <frozen-64-hex> \
  --case-ids <pre-registered-id-1>,<pre-registered-id-2> \
  --worker-root /secure/new-workers-only \
  --facilitator-root /secure/new-facilitator-only
~~~

This command uses default `--source-mode official-medeinst`; the pinned SHA must match exactly. `--source-mode synthetic-fixture` is ONLY for fictional local testing and cannot certify the benchmark. This command is illustrative, not an executed clinical benchmark. Both output roots must be new under existing trusted directories. Do not process clinical or identifiable data through public Actions.

### Mechanical tests

~~~sh
python -m unittest discover -s tests -p 'test_prepare_medeinst_holdout.py' -v
~~~

2026-10-29 V1 local result: **12/12 PASS**; source-identity hardening V2 local result: **17/17 PASS**, adding official-blob pinning, identical-narrative rejection, malformed ID rejection, and synthetic-mode labeling. Tests use fictional Diagnosis X/Y/P/Q placeholders; no MedEinst clinical vignette was downloaded or evaluated. Exact-head CI on the updated commit and independent review remain separately required.

## All-pairs research quality audit (development only)

Before interpreting MedEinst as a counterfactual reasoning test, run the standalone
`tools/audit_medeinst_pairs.py` over the **entire pinned official test.jsonl**. The PR workflow downloads the actual upstream file, verifies the SHA-256 and runs the audit before creating its four ephemeral anonymous smoke-test packets.

The audit reports only aggregated quantities: number of complete control/trap pairs, same-label pairs, identical-narrative pairs and quartile-like lexical similarity quantiles (p10/median/p90, plus below 0.50 and below 0.80). It never emits clinical narratives, IDs, diagnoses or per-pair information. Unit tests use only synthetic examples and reject malformed input, missing/duplicate variants, duplicate labels, identical narratives, and wrong source digests.

**Observed full-source boundary (2026-10-29):** The initial audit failed on `INVALID_AUDIT_RECORD` ([Actions #40839929371](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40839929371)). An aggregate-only diagnostic over the actual pinned official file measured 10,766 rows and exactly **one narrative longer than 12,000 characters**. The worker packet adapter intentionally refuses narratives above 12,000; the *whole-dataset auditor* now checks such rows structurally but records `pairs_above_worker_limit` and `narratives_above_worker_limit` as explicit exclusions from model execution. This does not waive the per-worker bound, imply that the oversized case is clinically invalid, or allow post-hoc outcome-driven selection. The revised exact-head workflow must pass independently before treating the fix as verified.

**Interpretation is strictly descriptive.** Text overlap is not a measure of true medical similarity or whether one critical clinical variable changed; a valid pivot can be a one-word difference with high lexical overlap, and long similar boilerplate can hide multiple altered clinical facts. Therefore:

- This audit may detect structural dataset defects and flag the size of the remaining clinical content-review task.
- It **cannot certify** intervention isolation, pathophysiologic plausibility, or guideline-relevant decision pivots.
- The full official dataset is public. Even a successful external-model score cannot establish contamination-free unseen transfer.
- A genuine medical blind trial must involve separately protected, expert-validated counterfactual and stable pairs, with frozen A/B/C exposures and blinded reviewers. Use existing #225/#224 rather than adding a second experimental runtime.
- Printed aggregate statistics and CI logs are engineering/research observations, **not model quality or clinical safety scores**.
- The audit is a read-only process (no model calls) and can be retired if it does not inform sampling/clinical reviewer priorities.

To run the aggregate audit in a trusted environment:

~~~sh
python tools/audit_medeinst_pairs.py \
  --dataset /secure/datasets/medeinst/test.jsonl \
  --expected-sha256 b6b688fa41f788c17cdbf5076b5215782c9eb00efec1a3d3384c002836550a57
~~~

## Actual clinical experiment — NOT RUN

1. Freeze dataset SHA and chosen IDs before outcomes; review case validity, contamination and data rights. For actual transfer, create separately protected *expert-reviewed unseen cases*.
2. Reuse the **A/B/C first-pass framework in PR #225**, fixed same model, matched source/budgets and isolated contexts; do not bypass its synthetic-only live-model allowlist. Any real MedEinst input requires a separately reviewed access-controlled runner.
3. Give each worker only ONE narrative and NEVER its control/trap sister in the same context. Keep arm identities hidden from a genuinely separate assessor.
4. Independent clinical adjudication must evaluate diagnosis, competing mechanisms, missingness, decision pivot, false retrievals, evidence source quality and P0/P1. Record first-pass, owner minutes, calls, tokens and real billing. Compare both flip sensitivity and stable-case specificity.
5. Retain existing A/B/C baseline and the simpler system unless Skill C safely improves B. No Skill promotion, scheduled run, auto merge, main merge or medical publication is authorized by this adapter.

**Stop:** If packet segregation adds no value beyond PR #224/#225 or independent judgment is unavailable, retire this code. Structural passing tests are never evidence of autonomous learning.
