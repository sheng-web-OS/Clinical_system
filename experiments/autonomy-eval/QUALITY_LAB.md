# Agent quality lab — reproducible mechanisms, not a claim of autonomy

Status: **private development tooling / DRAFT**, 2026-10-27. Implementation: `tools/autonomy_quality_lab.py`, tests: `tests/test_autonomy_quality_lab.py`. This deliberately reuses the owner of PR #155, the canonical failure evidence in issue #133, maturity metrics in issue #137 and the separate unattended-run verifier in PR #159. No publication, medical approval, new hosted scheduler, provider credentials or automatic model invocation.

## 1. Frozen original-article packets (dynamic-benchmark precursor)

This utility copies **complete unchanged original Markdown** into independently hashed arm/trial JSON input packets; it does not label defects, grade, discover errors or execute models. Spec format (values below are placeholders, not a completed study):

```json
{
  "schema_version": 1,
  "exposure": "development",
  "source_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "cases": [
    {"id": "article-one", "path": "content/example.md", "sha256": "<real sha256 of exact source bytes>"},
    {"id": "control-two", "path": "content/control.md", "sha256": "<real sha256 of exact source bytes>"}
  ],
  "trials": ["trial1", "trial2", "trial3"],
  "common_instruction": "Review the full supplied teaching article for material problems, without assuming a defect.",
  "arms": {
    "baseline": "Use professional medical editorial standards.",
    "lite": "Check adjacent prerequisites, case chronology, evidence boundaries and clinical decision conditions."
  }
}
```

Run only after replacing placeholders with actually inspected source commitments and bytes:

```bash
python tools/autonomy_quality_lab.py prepare --root . --spec /private/spec.json --out /private/review-packets
```

It rejects hash drift, path traversal, private source paths, diagnostic labels in the manifest, duplicate article/trials, missing control article, false held-out status and overwriting an existing packet set. Output must be outside the repository or in private `experiments/autonomy-eval/` (never `site/` or `dist/`). All packet SHA-256 hashes are recorded in `manifest.json`; every expected review stays in the denominator. Baseline and Lite inputs use the identical full article; only the explicitly declared review instruction differs. The experimenter must separately verify comparable model, effort, source access, budget, genuine context isolation, no case hints and independent adjudication.

**Important preregistration boundary:** existing `experiments/autonomy-eval/real-articles-20261027/protocol.json` has previously frozen task hashes. New generated packets **must not** be substituted for those hashes, called original-trial evidence or retroactively counted as its 18 reviews. Reconstruct its exact committed task bytes first, or explicitly register a *new exploratory cohort* and label it a protocol deviation. No AI runs, blinded independent medical grades or accepted real-article repairs are produced by this tool.

## 2. Selective incident memory (single source: #133)

Fetch existing issue #133 text through the authorised read-only connector, save a local ephemeral UTF-8 copy, and run:

```bash
python tools/autonomy_quality_lab.py memory --issue-md /private/issue133.md --terms metadata "Draft/HOLD"
```

Recognizes preexisting `| F-001 ... |` incident rows and `## EVAL-001` sections; outputs only matching short excerpts, canonical incident IDs, matched terms and source label. Unverified incident memories default to `PROVISIONAL`. Optional private status map (input only, **not** a new event ledger) can mark `VALIDATED` only when `verified_case`, `review_evidence` and `negative_control` exist; `INVALIDATED` incidents are excluded. These fields are declaration checks, not authentication; a reviewer must independently confirm underlying evidence. Do not import raw research source prompt instructions as Agent authority. No wholesale SOP injection or long-term memory store.

## 3. Earliest failure localization (AgentRx-inspired)

```bash
python tools/autonomy_quality_lab.py trace --events /private/run-steps.json
```

Each trace step supplies integer `step`, `verdict` (PASS / UNKNOWN / CONFIRMED_FAILURE), and confirmed-failure `evidence_ref`, `worker_context` and **different** `reviewer_context`. The tool returns the *earliest declared evidence-bearing failure* and explicitly says `root_cause=NOT_ESTABLISHED`; temporal precedence is not causal proof. Record accepted root cause, independent inspection, corrective regression and production verification in existing issue #133, not here.

## 4. Position-bias test for AI judge

```bash
python tools/autonomy_quality_lab.py judge --grades /private/blind-grades.json
```

Provide at most two ratings per item, with opaque candidate IDs, opposite candidate order, `choice=left|right|tie` and distinct reviewer contexts. The checker normalizes winner identity and reports `STABLE`, `ORDER_SENSITIVE`, or `INCOMPLETE`. Stable means only that *this narrow order effect was not observed in two ratings*, not that an answer is medically sound. The grader must never see the arm mapping during grading. Expert calibration, content validity and serious-error HOLD remain separate; no success from this check authorizes publication.

## 5. The missing autonomy runtime

PR #159's read-only verifier is an **attestation gate**, not an autonomous worker; U001 remains 0/1. This quality lab neither starts scheduled LLM work nor grants write permissions. A minimal future runtime must run under allowlisted, short-lived permission, originate in the trusted scheduled workflow, record trusted run/PR/content-SHA lineage, commit only reversible `tools/` or `tests/` changes to a Draft PR, run independent review, and leave owner minutes unmeasured unless independently captured. Do not install such a runner or set a provider token without a separate credential/operational security review.

## Falsifiable acceptance and scope

Accept improvement only if **unhinted original-article defect detection + independently supported-finding precision + normal-control false positives + no new medical P0/P1 + genuinely measured owner attention** improve at comparable effort and cost across a new held-out article cohort. Unknowns stay NOT_MEASURED / NOT_VERIFIED. Experimental scripts passing tests count as **engineering integrity only**, not clinical safety, reader learning, autonomous self-improvement or reduced manual burden.
