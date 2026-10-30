# XDT-01 private examiner handoff — offline-only (Draft/HOLD)

**Owner-directed XDT-01, separate from #137's fixed 72h autonomy cohort.**
This is a *cross-domain* adaptation of the access-boundary pattern in Draft PR #237, **not a call to #237** and not a claim that its clinical Stage1 ZIP or #225 synthetic model runner can execute non-medical real cases unchanged. Public repo branches, PRs, Actions, and shared folders accessible to the tested candidate are not confidential case/gold storage.

## Trusted roles and custody before running anything

1. **Independent case designer / examiner (private identity):** assembles previously unseen, source-consistent questions and gold *after* candidate Skill and protocol freeze. The examiner must not have shown these tasks to the tested candidate in ChatGPT, public git, searchable benchmarks, or retrievable source folders. Document where case facts came from and how impossibility/ambiguity is judged.
2. **Private facilitator (a separately authorized identity):** has access to gold, complete neutral task suite, and unblinding map. Use two **independently access-controlled** storage principals, not just path names, ACL modes or a `runtime_iam_verified=true` text field. Evaluate actual read denial from worker to gold and to siblings before promoting.
3. **Worker (restricted identity):** given exactly **one** neutral `Hxx.txt` case and its arm instructions with matched common source pack; never the whole staged directory, `stage_manifest.json`, `facilitator_only.json`, other-case packets or review/gold. Fresh unrelated contexts per A/B/C, no history carryover or hot-start from evaluator prompts.
4. **Independent reviewer (separate evaluator context):** sees anonymous first-pass answers, disclosed common sources and a domain-appropriate frozen rubric, without arm/skill identifiers. Gold (where needed) must be supplied in a reviewer-controlled environment after answer freeze; then facilitator unblinds. A different display name or GitHub identity by itself does not certify independence.
5. **Operator/budget gate:** a trusted private runner with real provider receipts, hard project/API spend governance, start/stop receipts and a no-rerun first-pass policy. #225's current live runner explicitly permits *only synthetic clinical fixtures* and cannot be repurposed for XDT-01 without a reviewed separate adapter; do not silently broaden its paid path.

**Do not activate** the sealed-case model evaluation during 2026-10-29T06:20:15Z–2026-11-01T06:20:15Z (UTC) autonomy observation. Do not count owner-directed setup as autonomous activity. Independent evaluator, external approvals, output retention and actual budget remain HOLD.

## Private input schema

Keep two distinct **private** JSON files under a trusted examiner:
```json
{"schema_version":1,"source_class":"synthetic","phase":"pilot","cases":[
 {"id":"inventory-case-01","domain":"inventory","task":"[private examiner-authored task text]"},
 {"id":"it-case-01","domain":"it-incident","task":"[private examiner-authored task text]"},
 {"id":"document-case-01","domain":"provenance","task":"[private examiner-authored task text]"}
]}
```
The schema here is *illustrative*, not a supplied task set. No real hidden tasks appear in this repository. Domain choices: `inventory`, `it-incident`, `provenance`. `phase` is `pilot` (1/domain) or `exploratory` (4/domain); in exploratory, at least one task/domain must require deferral/abstention. `source_class` is only a **self-attested claim**, either `synthetic` or `public_rights_cleared`, and does not independently establish rights or privacy.

In another private file with access denied to tested workers:
```json
{"schema_version":1,"keys":[
 {"id":"inventory-case-01","acceptable_decisions":["DEFER"],"must_abstain":true,
  "rationale":"[independently prepared rationale, at least 30 characters]",
  "critical_failures":["Invented source or unsafe external action"]}
]}
```
**Gold must cover every private case exactly once.** It contains independent open-ended acceptable decisions and critical failure criteria; not a keyword-based autograder.

## Offline CLI, in a separately controlled runtime

First, hash and externally time-seal the raw private cases JSON, private gold JSON, and the candidate source commit/Skill. A source hash entered just before invoking this command is an integrity checksum, **not evidence that the holdout was created beforehand or kept unseen**.

```sh
python tools/seal_xdt01_private_cases.py \
  --cases-file /trusted/examiner/cases.json \
  --gold-file /trusted/facilitator/gold.json \
  --cases-sha256 <previously-frozen-cases-sha256> \
  --gold-sha256 <previously-frozen-gold-sha256> \
  --suite-id xdt01-prospective-001 \
  --phase pilot \
  --candidate-commit <exact-frozen-40-character-commit> \
  --skill-sha256 <exact-frozen-skill-blob-sha256> \
  --stage-root /trusted/stage1/new-run \
  --facilitator-root /trusted/keys/new-run \
  --repo-root /workspace/Clinical_system
```

The stage and facilitator parent directories must already exist, be separate, and be non-world-writable. Final output directories **must not exist**. Both are created private (0700) and data files 0600; inputs and outputs must be outside public GitHub checkout. A symlinked output parent or pre-existing output is rejected rather than overwritten. Tool prints only a status/count receipt, not case text, gold, IDs or storage paths. File modes alone **cannot** attest identity separation or prevent examiner/worker same-user access; the actual IAM check remains external.

This tool creates an examiner-only *multi-case* stage; **never mount it in a worker**, even when its filenames have anonymous slots. The separately stored mapping contains all gold, source IDs, domains and slots. Only one neutral task's bytes may cross to each worker after an authenticated one-case permission check, with independent private runtime logs that contain no forbidden fields.

## Exit gates and decision rule

- **Mechanical:** `python -m unittest discover -s tests -p 'test_seal_xdt01_private_cases.py' -v`, plus exact-head repository CI. These are synthetic isolation regression tests, not cognitive quality evidence.
- **Operational:** unrelated worker identities cannot list/cat sealed stage, facilitator key, other workers' tasks or prior answers; no secret leaks via API inputs, error messages, cached context, CI artifacts or logs. Actual SSO/IAM/access-denial audit required.
- **Scientific:** frozen candidate skill/source packs and independent case keys; no leakage or repeated exposure; randomized masked arm mapping; one first-pass/provider receipt per case/arm; blinded independent adjudication of decision success and critical failure; per-arm and per-case actual spend/tokens/time; paired C–B and C–A analysis with uncertainty.
- **HOLD:** private source rights unclear, repeated prompt exposure, gold or task leakage, unverified IAM, model billing permission absent, any critical C-only regression, or evaluator uncertainty unreported.
- **INCONCLUSIVE:** missing traces, missing or non-independent review, all trials synthetic fixtures only, unsupported cost claims, or non-replicated small favorable results.

## Scope of what is now built

Offline *non-medical* sealed case packaging with independent answer-key mapping and checks for domain counts, pinned source bytes, forbidden public git paths, output clobber, gold leakage into neutral case schema and at least one abstention per domain in exploratory. **Not built:** trusted external examiner identity, authenticated private storage, real model API adapter, independently sealed external sources, runtime-enforced isolation, blinded review, meaningful paid attempt, automatic skill selection or proof of transferable skill. No background automation or release is enabled.

Cross references: #237 private clinical examiner pattern; #225 separate clinical skill testing; #251 XDT-01 protocol; #137 unchanged growth/autonomy observation.
