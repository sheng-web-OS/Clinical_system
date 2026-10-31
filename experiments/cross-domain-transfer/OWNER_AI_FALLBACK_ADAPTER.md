# XDT-01 OWNER_AI_FALLBACK — rich JSON offline adapter (code only)

**Status: DRAFT / OFFLINE_STAGED_REVIEW_HOLD.** This is an owner-authorized code-only implementation of the internal exploratory fallback described in #256 (parent #251). This branch is intentionally separate from the pinned frozen candidate in Draft #252. **No private questions, answer keys, reviewer notes, API credentials, provider responses or scoring outcomes belong in this PUBLIC repository.**

## What it does

`tools/prepare_xdt01_rich_pilot.py` accepts three separately hash-pinned, already-saved **private** UTF-8 JSON files: `cases.json`, `gold.json`, `scoring.private.json`. It validates case/rubric ID parity and exactly one case per required pilot domain, checks referenced embedded source-text SHA-256, and serializes each task into a single JSON text packet preserving its complete `task`, all `evidence` entries and global `instructions`. This prevents the **missing-evidence** bug if only the input `task` field is passed to the existing worker.

It writes three separately shuffled `Hxx.txt` files into a NEW facilitator-only multi-case stage, plus a private manifest. Rich gold and original per-case scoring remain **unmodified in meaning and separate** under an independently specified private facilitator output root. It rejects existing output directories, public repo inputs/outputs, symlink ancestors, missing source pins, malformed duplicate JSON keys and oversized packets.

It uses existing #252-compatible **field names** for stage/facilitator manifests. It does NOT claim the local, uncommitted Docker launcher or private scorer has passed an integration test against this new adapter. **Never mount the multi-case stage into a worker**: each independent worker sees only one `Hxx.txt`.

## Verify synthetic-only tests

```sh
python3 -m unittest discover -s tests -p test_prepare_xdt01_rich_pilot.py -v
```

In the original code-only development container, 15/15 tests passed. This is **engineering test evidence only**; exact-head GitHub CI status is separate.

## Offline invocation on a privately controlled host

```sh
python3 tools/prepare_xdt01_rich_pilot.py \
  --cases-file /EXAMINER/cases.json \
  --gold-file /EXAMINER/gold.json \
  --scoring-file /EXAMINER/scoring.private.json \
  --cases-sha256 <hash-of-actual-saved-file-bytes> \
  --gold-sha256 <hash-of-actual-saved-file-bytes> \
  --scoring-sha256 <hash-of-actual-saved-file-bytes> \
  --candidate-commit 03f29b980ba326ac0509299b9c94292d6a1a5d5a \
  --skill-sha256 <hash-of-frozen-skill-bytes> \
  --repo-root /READONLY/Clinical_system-sparse \
  --stage-root /PRIVATE/STAGING/new-run \
  --facilitator-root /OTHER-PRIVATE/FACILITATOR/new-run
```

The output is always `OFFLINE_STAGED_REVIEW_HOLD`, and the command has **zero** provider/API calls. It is never sufficient to start the actual model trial. Distinct paths and POSIX modes are NOT proof of independent identities or access denial.

## Mandatory unresolved gates

1. **Provenance:** Candidate case/gold/rubric contents were disclosed in the owner's research conversation. This is **INTERNAL_EXPLORATORY**, not a certified unseen external holdout. Do not upgrade its class by using a fresh output filename.
2. **Primary decision outcome:** Rich candidate rubric supplies 0–100 checklist scoring, but #251 pre-registers a **binary per-task valid decision success** as primary. An examiner must prospectively define the binary necessary conditions, critical-error disqualifiers and `UNADJUDICABLE` handling, then hash/freeze the changed rubric before any first pass. Never pick a post-hoc score cutoff.
3. **Routing observability:** The frozen C selection turn is strictly `USE` or `SKIP`; it does not emit a contemporaneous explanation. Rubric criteria demanding that explanation cannot be blindly assigned full marks. Mark NOT_OBSERVABLE or prospectively revise the rubric, preserving the frozen candidate selector.
4. **Private custody:** Verify local source SHA after actual save, separately controlled backup+restore, independent examiner/facilitator/worker/judge access, actual denial of worker reads to gold and sibling tasks. Same UID/root is NOT isolation. No private cases or gold in public Actions logs/artifacts.
5. **Run authorization:** The original #137 72h interval ends 2026-11-01T06:20:15Z. No paid model call before its verified closeout, and no paid model call merely because these tests pass. Need owner-approved, enforced project spending limit, restricted key, model entitlement and reviewed local overlay. No auto-retries of UNKNOWN_BILLED attempts, no new schedules.
6. **Scientific honesty:** Report `real_first_pass=0/9`, `provider_calls=0/12`, `C_minus_B=NOT_MEASURED` until separately evidenced. Do not pool fallback scores with externally independently judged batches or claim generalization.

## Files

- `tools/prepare_xdt01_rich_pilot.py` — private offline rich case/gold/rubric packaging, no LLM call.
- `tests/test_prepare_xdt01_rich_pilot.py` — 15 synthetic-only unit tests.

No changes to original candidate #252 code, medical publication, site, GitHub workflows, budgets, automations or #137 trial.
