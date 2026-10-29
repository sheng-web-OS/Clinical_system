# Executable falsification probe — synthetic development pilot

This is a **small, read-only-in-practice testing tool**, not a clinical decision-maker, model runner, publishing gate, proof assistant, or independent physician reviewer. It operationalizes a limited ETH-inspired principle: make claims falsifiable and test whether a **single controlled change** causes the expected response change. It extends the experiments already planned in Issue #203 / Draft PR #205 without replacing their reviewer-isolation protocols. No new scheduled services, model calls, medical documents, or publication manifests.

## What is actually executable

`tools/falsification_probe.py` creates baseline and matched one-fact probes from a template. It uses only Python's standard library. Each packet carries SHA-256 of its exact content and presents *all choices without the gold answers*. Gold labels and the expected **flip**/**stable** relation are written to a **separate evaluator key path**. An agent or reviewer, run separately, returns a small JSON response for each packet. The scorer rejects missing/duplicate/stale results and reports four separately observable mismatches:

- S1 — most consequential question label
- S2 — evidence IDs actually selected
- S3 — decision and whether a decisive mutation flips it
- S4 — reviewer defect flags, including harmful false alarms

`first_observed_mismatch` means the *first failed check in this fixed order*, **not** a proven temporal or causal root. A model can guess correct labels without using the right reasoning; this tool cannot certify the strength of its prose, original citations, expert clinical applicability, or true independence of its runtime context.

## Reproduce the demonstration

The included `synthetic-routing.json` is a **fictional document-routing rule**, deliberately not medical advice, medical data, a GREEN clinical fixture, or a claim of AI capability. Try:

```bash
python tools/falsification_probe.py prepare \
  --spec experiments/eth-falsification-probe/synthetic-routing.json \
  --reviewer-dir /tmp/probe-reviewer \
  --key /tmp/probe-coordinator/key.json

python -m unittest tests/test_falsification_probe.py
```

Use different, empty output directories for each run. A reviewer should only see the individual files in `/tmp/probe-reviewer`, never the spec with answers, key, prior reviews, test code, or connected memory. For a real study, ensure **access-control separation**, not merely different filesystem names. The demonstration fixture and its gold are public and **cannot** be used as a truly blinded model benchmark.

The independently run Agent returns JSON in this form (one entry per packet):

```json
{
  "case_id": "synthetic_route_01",
  "responses": [
    {
      "probe_id": "baseline",
      "packet_sha256": "<copy verbatim from baseline packet>",
      "question_id": "q_signature",
      "evidence_ids": ["F1"],
      "decision_id": "accept",
      "review_flags": []
    }
  ]
}
```

Do not use the single-row illustration as full answers; include baseline and **every** probe. Then run:

```bash
python tools/falsification_probe.py score \
  --key /tmp/probe-coordinator/key.json \
  --responses /tmp/agent-responses.json
```

Exit status is `0` for all preregistered label checks passed, `1` for mismatches, `2` for invalid or stale data. Even a `0` is **only** a pass against this fixture's labels, never a blanket medical approval.

## Before clinical use

1. Obtain credible, independent clinical adjudication of each original case, the *decisive vs irrelevant* fact pair, and its expected outcome. Preserve legitimate uncertainty or mark the case ungradable. Include both deliberately defective **RED** examples and correctly bounded **GREEN** examples to test over-criticism.
2. Preregister the specimen and freeze the key **before** model evaluation. Use separate, non-personalized reviewer environments without contamination from earlier Issue/PR or account memory. Set equal source access / model settings / effort for baseline arms. The public example and this conversation's historical BA case are **not** blind holdouts.
3. Do not submit real patient information, restricted documents, private author manuscripts or reviewer answer keys to this repository (GitHub currently reports PUBLIC visibility). Store protected sources and hidden gold only in properly restricted storage; a public draft PR or Actions artifact is not a privacy boundary.
4. Compare gains in actual unseen clinical error interception, correct-case preservation and user intervention minutes against a native-model baseline. If absent, **delete or retire this extra tool** rather than installing it as another mandatory approval layer.

Scope: `DESIGN + EXECUTABLE STRUCTURAL FIXTURE / MEDICAL EFFECTIVENESS NOT VALIDATED`. Linked to Issues #203/#133, PR #205, and experiment E08; no deployment or auto-merge.
