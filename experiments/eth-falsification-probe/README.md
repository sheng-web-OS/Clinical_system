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

## V2 — executable adapter and stage-rescue trials

The `run` operation **actually starts a supplied local adapter process** for each packet,
passes one packet as stdin JSON and validates exactly one stdout JSON object.
It does not pretend the included toy adapter is an AI: `toy_adapter.py` is a
fixed fictional signature-routing rule and is used to prove the harness runs.
The same protocol can be implemented by a trusted local model executable or
approved model-provider adapter *outside this public repo*. No vendor API key,
provider, token budget, isolation or paid inference is preconfigured.

```bash
# Toy end-to-end run (change /tmp/demo-eth to a fresh path for another run)
python tools/falsification_probe.py prepare \
  --spec experiments/eth-falsification-probe/synthetic-routing.json \
  --reviewer-dir /tmp/demo-eth/packets \
  --key /tmp/demo-eth/gold/key.json
python tools/falsification_probe.py run \
  --reviewer-dir /tmp/demo-eth/packets \
  --adapter experiments/eth-falsification-probe/toy_adapter.py \
  --responses /tmp/demo-eth/answers.json
python tools/falsification_probe.py score \
  --key /tmp/demo-eth/gold/key.json --responses /tmp/demo-eth/answers.json
```

The adapter sees the **packet only** on stdin; the gold key is not supplied to it.
`run` strips most inherited environment variables, executes without a shell,
enforces a per-packet timeout, checks response schema and packet SHA, and
refuses to overwrite any responses. A Python `.py` file is invoked through
the running Python interpreter; other adapter types must be executable.
Use `--allow-env NAME` only for an explicitly approved variable and never print
its value. An adapter can still access other files or make network requests;
**subprocess execution is NOT a security sandbox, privacy boundary or proof of
memory isolation**. Do not run an untrusted adapter on a machine that can read
private patient data or evaluator keys. For a controlled clinical trial, use
separate restricted execution environments (or appropriately scoped remote
workers), not merely adjacent folders.

### Diagnostic rescue conditions (N / Q / E / QE)

A second command creates four matched test arms that differ only by supplied
research guidance. The hints are supplied **by a researcher/adjudicator**, not
invented or independently discovered by the agent. Q gives the candidate
question; E gives evidence-finding guidance; QE gives both. This is a
**deliberately unequal-information diagnostic manipulation**, not a fair
A/B benchmark or proof of causal root.

```bash
python tools/falsification_probe.py prepare-rescue \
  --spec experiments/eth-falsification-probe/synthetic-routing.json \
  --hints experiments/eth-falsification-probe/synthetic-rescue-hints.json \
  --reviewer-root /tmp/demo-rescue/packets \
  --key-root /tmp/demo-rescue/gold
for ARM in N Q E QE; do
  python tools/falsification_probe.py run \
    --reviewer-dir "/tmp/demo-rescue/packets/$ARM" \
    --adapter experiments/eth-falsification-probe/toy_adapter.py \
    --responses "/tmp/demo-rescue/results/$ARM.json"
done
python tools/falsification_probe.py compare-rescue \
  --key-root /tmp/demo-rescue/gold \
  --response-root /tmp/demo-rescue/results
```

**Important interpretation:** The synthetic toy is expected to get all four
arms correct, so it cannot establish that rescue helps a real model. The
`compare-rescue` command reports each arm's failed-stage counts and bad
flip/stable relations; it cannot discover *why* a model failed. A clinical
follow-up requires a prospectively adjudicated RED/GREEN holdout set, verified
provider/context isolation, independent review and owner-time measurement.
No label printed by these commands is a clinical publication approval.

This remains a **Draft research instrument, not a new mandatory editorial gate**.
If no meaningful clinical error reduction or time saving is demonstrated over
the native model, delete/retire the extra tool rather than making every article
pay its complexity cost.

## 2026-10-29: verified benchmark shortcut and limited mitigation

An intentionally incorrect *ID-only* Python adapter, which never inspected
`case_text`, obtained **3/3 passing** on the original public synthetic fixture:
`baseline -> accept`, `p01 -> hold`, `p02 -> accept`. This is an observed
benchmark-artifact counterexample, NOT a model failure or clinical observation.

The adapter runner now replaces each predictable original `probe_id` with a
fresh unpredictable `trial_...` identifier **at subprocess transport time**, and
recomputes that wire packet's SHA-256. It shuffles variant execution order and
runs subprocesses from an empty temporary working directory. Once the adapter
returns its wire ID/hash, the evaluator freezes an original-ID response and
keeps a coordinator-side `transport_audit` mapping. A fixed-ID memorization
shortcut now scores **FAIL** while the fact-reading toy still scores PASS.

**Critical limits:** This does not prevent recognizing publicly posted cases,
training-data memorization, exploiting answer-bearing option descriptions, or
untrusted code from accessing files/network by other means. An empty cwd is
**not** a sandbox; the adapter must be trusted and isolated by the actual
provider/container for credible clinical evaluation. Wire aliases are not
cryptographic attestations of who performed the inference. The status is
`ADAPTER_EXECUTED_ACCESS_NOT_VERIFIED` and `isolation=NOT_VERIFIED` for that
reason. This tool's gold is public and cannot itself measure clinical gain.

The first controlled LLM experiment should therefore use a **fresh withheld
benchmark**, independent clinical adjudication, different contexts without
injected historical memory, and matched native/evidence/OS conditions. There
must be no automatic promotion to semantic publication approval.


## V4 — semantic-preserving transport relabel (synthetic only)

V3 rotated the variant ID; however the public toy still used predictable
`q_signature` / `accept` / `F1` labels. A fixed-label adapter could therefore
appear correct even if it was fragile to option-label changes. V4 adds an
**opt-in** `--relabel` flag for the existing `run` operation:

```bash
python tools/falsification_probe.py run \
  --reviewer-dir /tmp/demo-eth/packets \
  --adapter experiments/eth-falsification-probe/toy_adapter.py \
  --responses /tmp/demo-eth/relabelled-answers.json \
  --relabel
python tools/falsification_probe.py score \
  --key /tmp/demo-eth/gold/key.json \
  --responses /tmp/demo-eth/relabelled-answers.json
```

The transport layer generates a fresh random bijection for all question,
decision, evidence and review-flag IDs, randomizes option order, rewrites
`[EVIDENCE_ID]` markers and exact ID references in research hints, and
**maps model answers back** to the original frozen case key *after* execution.
The research question, patient-relevant facts (if used in an approved private
evaluation), and answer semantics are unchanged; only machine labels change.

The tests demonstrate that a toy which selects based on actual evidence
text and choice descriptions still passes, whereas a toy which reads the
signature fact but hardcodes `q_signature` and `F1` is rejected before scoring.
This is *a regression against label/position shortcuts*, not demonstrated
clinical model improvement, clinical semantic correctness, or provider memory
isolation. For credible real-case analysis, adjudicators must verify that
rewording/relabeling never changes the clinical meaning and must compare
both normal and relabelled execution on a truly held-out case. The adapter is
still trusted local code with general file/network capabilities; it is **not
OS-sandboxed** and cannot certify that a hidden key was inaccessible.

Reference: Chen et al., *Explanation-Guided Metamorphic Testing of
Specialized Language Models* (ESEM 2026),
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.5 .
Their empirical results concern specialized language-model testing; they
**do not** establish effectiveness for clinical inference in this repo.

## V5 — evidence sufficiency / unknown is not negative (synthetic)

**Why this is different from a flip/stable benchmark:** Earlier packets always had
sufficient information for one of two fixed choices. In real research, a source
can be relevant yet fail to establish the answer. V5 tests this missing-evidence
state *separately* from an explicit negative fact, before any clinical content
is involved. Inspired by Chen et al. (2026), *Relevance Is Not Sufficient
Evidence*, https://arxiv.org/abs/2609.37469 (preprint): their results concern
RAG evidence sufficiency and **cannot be treated as a validated clinical gate**.

V5 adds an **optional**, backward-compatible `support_status` field to the
frozen gold and agent reply (`sufficient` or `insufficient`). It is required
for *all* variants of a case family if enabled in the baseline and does not
appear as a correct answer in the reviewer packet (only both possible statuses
are advertised). A wrong sufficiency judgment is scored as `S2_evidence`, even
if the decision label happens to match. Unknown status is not a synonym for a
confirmed negative finding. An adapter omitting the required field is rejected
rather than scored as a successful old-schema answer.

A public, **fictional nonmedical** demonstration uses a submitter signature:
verified signed ⇒ transfer / sufficient; verified unsigned ⇒ reject / sufficient;
no reliable record ⇒ request verification / insufficient; an unrelated cover
color change ⇒ stable. An additional test starts from *unknown* as baseline and
changes only the cover color, ensuring that insufficient evidence need not be
identical to a particular original probe index.

```bash
python tools/falsification_probe.py prepare \
  --spec experiments/eth-falsification-probe/synthetic-evidence-sufficiency.json \
  --reviewer-dir /tmp/eth-v5-packets \
  --key /tmp/eth-v5-keys/gold.json
python tools/falsification_probe.py run \
  --reviewer-dir /tmp/eth-v5-packets \
  --adapter experiments/eth-falsification-probe/sufficiency_toy_adapter.py \
  --responses /tmp/eth-v5-answers.json --relabel
python tools/falsification_probe.py score \
  --key /tmp/eth-v5-keys/gold.json --responses /tmp/eth-v5-answers.json
```

**Important validity limits:** The synthetic adapter is a hard-coded rule for
this *public* fictional fixture, **not a model, discovery algorithm, or proof of
learning**. The `support_status` gold remains human-authored. The runner cannot
independently decide if actual guideline/source evidence suffices for medical
action; correct selected evidence IDs do not certify that the Agent actually
read or reasoned through them. Nor does an `S2_evidence` mismatch prove a causal
root. For clinical evaluation, the missingness/confirmation statuses must be
independently adjudicated, evidence sources access-controlled, and a fresh
model trial conducted in an isolated environment with RED+GREEN controls.
No patient data, private answer keys, automatic publication, network model
calls, new scheduled actions or deployment changes belong in this PR.
