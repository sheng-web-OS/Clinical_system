# ALE: public source sentence → purpose-relation hypothesis → Q3 edge review

**Date** 2026-10-31 Asia/Taipei. **Status** `OWNER_DIRECTED_LEXICAL_EDGE_REVIEW_CANDIDATE`. This is an incremental executable extension of existing Draft #260, not a new ontology, live semantic discovery agent, medical publication, or owner-private learning assessment.

## Problem demonstrated by a real published source

Official 2025 Endocrine Society Primary Aldosteronism (PA) guideline, Adler GK et al., PMID 40658480, DOI https://doi.org/10.1210/clinem/dgaf284, Recommendation 3:
- serum/plasma aldosterone and renin/ARR are the direct screening analytes;
- potassium assessed alongside them is used to **help interpret** aldosterone, not itself the PA screen;
- hypokalemia can suppress measured aldosterone; a negative screen under hypokalemia may require correction and repetition, conditional on the rest of the source guidance.
- Check official 2025 erratum DOI https://doi.org/10.1210/clinem/dgaf472 (renin unit correction) before copying any numerical figure thresholds.

The **same mention of potassium** spans at least screening selection, measurement validity, and conditional retesting. Mere keyword grouping would be a medically poor graph. Source wording about *purpose* is NOT blanket evidence that potassium has no relationship to screening or is never measured before screening.

## Executable chain (bounded and transparent)

```
source: public PMID + exact <=3000-character excerpt, NO semantic labels
  → existing ale_raw_q0_probe.extract (Q0 attention)
  → ale_source_edge_challenge.review
    → find syntactic "not for X but to/for Y"
    → attribute it ONLY to local grammatical subject ("Potassium")
    → preserve exact source-offset spans for negated and affirmed purposes
    → compare against supplied PUBLIC_SYNTHETIC_ONLY edge hypotheses
       (1) DIRECT_SCREENING_TEST at negated target → CHALLENGE_DIRECT_SCREENING_ROLE
       (2) AIDS_INTERPRETATION at affirmed target → TEXT_SUPPORTS_INTERPRETATION_ROLE_CANDIDATE
       (3) stronger or unrelated role → ABSTAIN_SCOPE_NOT_ESTABLISHED
       (4) wrong grammatical subject → ABSTAIN_NO_EXACT_LOCAL_ROLE_MATCH
    → if a positive purpose is missing from comparison hypotheses,
       emit SOURCE_PHRASE_RELATION_REVIEW_NEEDED (not a canonical missing edge)
    → Q3: Does "not a direct screening input" entail "irrelevant to interpretation"?
```

Inputs/paths:
- `experiments/ale-pa-2025-raw-role-contrast-20261031.json` is a short real source snippet + PMID (no tags, roles, impact, Concept ID).
- `experiments/ale-pa-2025-source-edge-comparison-20261031.json` intentionally contains **synthetic wrong and correct edge hypotheses** for falsification: one conflicts with the explicit source-purpose negation; one is consistent with the affirmed purpose; some claim more than source warrants; one attributes potassium's role to nearby-mentioned renin.
- `tools/ale_source_edge_challenge.py` contains the pure source-anchored challenger, CLI and privacy/length gates.
- `tests/test_ale_source_edge_challenge.py` contains 19 controls, including actual source fixture, exact offsets, wrong target, stronger claim, wrong-subject false merge, missing positive role, abstention, private input rejection and repeatability.

Command (repo checkout of this PR branch):
```bash
python tools/ale_source_edge_challenge.py \
  --source experiments/ale-pa-2025-raw-role-contrast-20261031.json \
  --comparison experiments/ale-pa-2025-source-edge-comparison-20261031.json
python -m unittest discover -s tests -p 'test_ale_source_edge_challenge.py' -v
```

### What is new versus prior Q0

The previous `ale_raw_q0_probe.py` could only ask **which question should be pursued**. This extension **outputs two explicitly quoted, local syntactic *purpose* relation hypotheses**, checks relation **target** and **subject attribution** in candidate edges, rejects stronger scope and produces a Q3 counterexample prompt. Crucially, the program **does not infer typed medical causal mechanisms**, determine whether real canonical Concept IDs match, verify guideline applicability or promote an edge. The proposed comparison graph is an experimental fixture; the phrase `SOURCE_PHRASE_RELATION_REVIEW_NEEDED` means *absent from supplied hypotheses*, not *missing in Clinical_system's entire ontology*.

This is a narrowly real text-to-relation improvement in one explicit grammatical form. It does **not** solve arbitrary prose semantics, implicit negation, non-English scientific text, multiple subjects, cross-sentence anaphora, full document QA, role-identity across families or relevance to the learner. Those must remain ABSTAIN or trigger proper semantic source review, not grow a fragile regex taxonomy.

## Next falsifiable stage

Give a different reviewer truly unseen source paragraphs **without** this fixture, expected patterns or pre-annotated roles. Evaluate extraction precision, missed roles, false attribution (especially "measured alongside"), spurious stronger inferences and whether an independently verified correction would change one actual Concept Family decision. Compare equal-budget Q0-only, tag-first and this source-local challenger; if false positives dominate, narrow/remove the rule.

**Acceptance status** `PUBLIC_SOURCE_Q0_TO_LOCAL_EDGE_HYPOTHESIS`, not `LIVE_AUTONOMOUS_SEMANTIC_ONTOLOGY`. No actual Anki/FSRS changes, no private learner state, no publication/merge, no extra task or API cost. Source/QA safety boundaries from #258 remain intact. This improvement belongs to owner-directed post-termination work; do not rewrite #137 72h experimental outcome.
