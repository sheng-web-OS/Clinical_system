# ALE-01｜Bounded Recursive Three-Question Concept Family Prototype

**Status: code artifact and public-safe synthetic regression only. Not a measured learning gain, independent medical review, autonomous semantic discovery, or authorization to edit Anki / published materials.**

## Practical problem

When an agent observes reasoning defects in more than one existing concept family, it should be allowed to propose a **new higher-order Concept Family**, not merely correct individual cards. It must also falsify overbroad abstractions and trace which dependent claims may need rechecking. Recursive three-question reasoning inspires the workflow:

- Q0/Q1: isolate an observed contradiction; distinguish observed error from hypothetical cause.
- Q2: articulate an explicit shared inference pattern and necessary conditions.
- Q3: seek counterexamples and a boundary; recurse only into a premise that may change the parent judgment; propagate revision upward as a **request to recheck**, not automatic invalidation.

## Runnable artifact

`tools/ale_recursive_family.py` accepts a public-safe JSON file with `observations`, `proposals` and optional `dependencies`. An observation has `id`, `family_id`, `pattern`, `role` (support/counterexample), `source_ref`, `source_check`. A proposal has `id`, `label`, `pattern`, `boundary`, `support_ids` and `acknowledged_counterexample_ids`. Dependencies contain `id` and `depends_on`.

Example (invented data, no patient or learner history):

```json
{
  "observations": [
    {"id":"example-a","family_id":"family-a","pattern":"signal_not_mechanism","role":"support","source_ref":"fixture/a","source_check":"checked"},
    {"id":"example-b","family_id":"family-b","pattern":"signal_not_mechanism","role":"support","source_ref":"fixture/b","source_check":"checked"}
  ],
  "proposals": [
    {"id":"meta-signal","label":"A measurement is not the mechanism","pattern":"signal_not_mechanism","boundary":"Other evidence may establish the mechanism","support_ids":["example-a","example-b"],"acknowledged_counterexample_ids":[]}
  ],
  "dependencies": [{"id":"conclusion-c","depends_on":["example-a"]}]
}
```

Run: `python tools/ale_recursive_family.py --input /path/to/public-fixture.json`

Test: `python -m unittest discover -s tests -p 'test_ale_recursive_family.py' -v`

## What this actually does

- Requiring >=2 **distinct** families prevents repeated examples of one family from masquerading as cross-family generalization.
- Explicit pattern identity (not word similarity) and source-check metadata gate proposals.
- A counterexample of that pattern must be acknowledged. An acknowledged exception changes state to `CHALLENGED_PENDING_INDEPENDENT_QA`, never automatic promotion.
- Bounded (3-hop default) dependency traversal identifies downstream claims to **recheck**, not automatically mark false.
- Output is a reversible link proposal, no graph mutation. Input `source_check=checked` is a claim by the packet author; it does NOT prove external source validity.

## Next genuine capability increment

Give a ChatGPT reasoning run a bounded, non-private set of verified concept statements; have it **generate novel pattern keys, candidate abstract rules and scope conditions**, plus independently sourced adversarial examples. Run this gate, then send qualified proposals to a distinct reviewer/known-unseen task before any promotion. Compare to non-recursive three-question and generic evidence-only baselines on false family merges, source fidelity, downstream missed rechecks and cost. The current deterministic gate is **not** autonomous semantic discovery.

Do not copy private Drive learner state, Anki review identifiers, credentials, hidden question material or medical/patient records into public GitHub or Actions. No public-site changes, no Anki/FSRS modifications, no new schedule, no #137 cohort changes. Integration belongs to #258; prioritization stays with #254. This owner-directed code contribution is outside the frozen 72h measurement.


## Stage 2 — generate parent candidates from cross-family reasoning signatures (2026-10-31)

New program: tools/ale_candidate_discovery.py. It creates candidate parent IDs, proposed links and explicit adversarial holds from **source-linked, structured reasoning roles**, instead of requiring an author-supplied pattern name. It is deterministic and does not read raw medical prose to infer semantic truth.

Run: python tools/ale_candidate_discovery.py --input experiments/ale-recursive-concept-probe-20261031.json

The first ChatGPT-authored public-source probe identifies a possible cross-domain distinction: measured signals are not automatically equivalent to every disease classification. Three independent family examples: cardiac troponin / MI, eGFR / CKD chronicity, and ALT or HBV DNA / fibrosis stage. Source references, for later separate review:

- ESC 2023 ACS guideline: https://academic.oup.com/ehjacc/article/13/1/55/7280662
- National Kidney Foundation CKD criteria: https://www.kidney.org/what-criteria-ckd
- AASLD/IDSA chronic HBV guidance: https://doi.org/10.1097/hep.0000000000001549

A deliberately hostile scope case asks whether persistent low GFR itself satisfies a CKD criterion. This **challenges an overbroad claim**, not necessarily the properly scoped epistemic principle. Expected output: one proposed new parent spanning three families, explicit unresolved counterexample, HOLD_REVISION_REQUIRED, downstream-only recheck suggestions, zero automatic promotions.

Caution: the example was formulated by ChatGPT from public source material. Input source_check=checked is not an independent medical truth attestation. Stage 2 **clusters model-annotated causal roles**, not independent text-to-semantic role discovery. Do not claim autonomous discovery of genuinely new causal knowledge, independent QA, or improved learning transfer. Do not publish the candidate as a medical rule without external verification.

Validation: python -m unittest discover -s tests -p 'test_ale_candidate_discovery.py' -v

Privacy, autonomy and publication: no owner-private answer events, no Anki writes, no new paid model API, no new schedule, no public-site changes and no changes to the frozen #137 trial.
