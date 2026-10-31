# ALE｜Q3 source challenge + concrete graph repair: euDKA / CKD / MI
2026-10-31 (Asia/Taipei) | `OWNER_DIRECTED_SOURCE_CHALLENGE` | **NOT independent medical QA**

## Decision and actual delta

This is a second semantic/source-reading pass by the same assistant, not an independent blinded examiner. It reviews the existing three local problem families and higher-order evidence bridge without creating a new framework. Q3 **found and changed defective graph structure**, rather than adding an abstract claim without action.

Before: 3 local families + 1 bridge; 11 Concepts, 10 edges, 5 Q3 controls.  
After: same 3 local families + 1 bridge; **12 Concepts, 12 edges, 7 Q3 controls**, graph `version=0.1.1-proposal`.

Edits committed on existing Draft #260, not main:
1. **E3 misleading direction repaired**: formerly `C_EUDKA_MASKED_PH --requires_discriminating_evidence--> C_EUDKA_KETONE_NOT_ETIOLOGY`. The target proposition was not the conclusion needing sufficiency testing. Now `C_EUDKA_KETONE_NOT_ETIOLOGY --does_not_alone_satisfy--> C_DKA24_THREE_COMPONENTS`, with explicit guard that beta-OHB alone meets only K, not D or A, nor unique diabetic etiology.
2. **E6/E7 target confusion repaired**: previously troponin injury or acuity `--insufficient_without-->` **ischemic evidence**. But ischemic evidence is an additional requirement, not the final conclusion. Add **C_MI_CLASSIFICATION** as a separate diagnostic target; retarget E6/E7 to it, and introduce **E11** (`C_MI_ISCHEMIC_EVIDENCE --required_for--> C_MI_CLASSIFICATION`) for the *biomarker-assessable spontaneous-MI* context.
3. **E12 added**: one elevated troponin establishes injury; **serial rise/fall** is necessary to establish acute versus chronic injury. Explicitly require at least one value above assay-specific 99th-percentile URL and interpret dynamics in time/assay context. Delta alone below the injury threshold does not prove injury.
4. **Q3_F added: type 3 MI exception**. An unqualified rule that every MI diagnosis requires *observed* serial cTn is false in fatal type 3 presentation before biomarkers can be obtained or become abnormal. The revised target is therefore biomarker-assessable spontaneous MI (esp. type 1/2); other MI types have separately defined criteria.
5. **Q3_G added: threshold guard**. Rise/fall below 99th percentile is not automatically myocardial injury.

## Edge-by-edge source-linked audit (no blanket 'verified' label)

| Edge | Judgment after Q3 | Medical/evidence justification | Limit |
| --- | --- | --- | --- |
| E1 | KEEP_SCOPED | Low glucose does not exclude DKA; history and direct K/A measurement matter [D] | Never turns glucose into etiology proof |
| E2 | KEEP_CHALLENGED | 2024 formal measured A criterion differs from source-supported concern for ketone-acid pathology with competing alkalosis [D,H] | Do not claim measured formal DKA A is satisfied in normal-pH/HCO3 case |
| E3 | **REPAIR_TARGET** | Beta-OHB meets K but is not a substitute for all D/K/A or etiology [D,H] | Multiple ketoacid sources / mixed disorders |
| E4 | KEEP_SCOPED | One eGFR does not establish ≥3 month chronicity [K] | Historical evidence can establish chronicity without waiting for new measurement |
| E5 | KEEP_SCOPED | GFR <60 sustained for ≥3 months can satisfy a CKD criterion; no extra albuminuria criterion is required [K] | Confirm true chronicity and context; underlying cause separate |
| E6 | **REPAIR_TARGET** | Injury from cTn elevation does not automatically prove spontaneous MI [M] | Final target now C_MI_CLASSIFICATION; type 3 separately considered |
| E7 | **REPAIR_TARGET** | Acute injury still needs evidence of ischemia for biomarker-assessable MI [M] | Final target now C_MI_CLASSIFICATION |
| E8 | CANDIDATE_BRIDGE | euDKA illustrates differing targets: formal definition versus physiologic processes [D,H] | Analogy, not causal or taxonomic equality |
| E9 | CANDIDATE_BRIDGE | CKD chronicity shows sufficiency depends on what timing/claim is tested [K] | Single low value insufficient; persistent GFR exception explicit |
| E10 | CANDIDATE_BRIDGE | cTn injury vs infarction shows target-specific sufficiency [M] | Not all MI types have the same biomarker evidence |
| E11 | **ADD_REQUIRED_FOR** | Ischemia evidence is a separate input to biomarker-assessable MI classification [M] | Not to be read as sufficient by itself |
| E12 | **ADD_INSUFFICIENT_WITHOUT** | One high cTn ≠ dynamic acuity; serial pattern and URL context required [M] | Delta alone below URL does not prove injury |

**Source labels**:
- [D] Umpierrez GE et al. 2024 multisociety hyperglycemic crises consensus, D/K/A and mixed disorders: https://pmc.ncbi.nlm.nih.gov/articles/PMC11272983/ 
- [H] Hillock MF et al. 2024 real case, `pH=7.37`, `HCO3=26`, `AG=23`, `beta-OHB=7.1`, original narrative glucose 186 versus discordant table 283/266: https://academic.oup.com/omcr/article/2024/7/omae071/7713251
- [K] KDIGO 2024 CKD chronicity, definition, exceptions: https://doi.org/10.1016/j.kint.2023.10.016 (peer-reviewed executive summary; original official guideline listed in graph)
- [M] Fourth Universal Definition of MI 2018 injury, acute injury, type 1/2 and type 3 criteria: https://www.jacc.org/doi/10.1016/j.jacc.2018.08.1038 and https://professional.heart.org/en/science-news/fourth-universal-definition-of-myocardial-infarction-2018/top-things-to-know

**Important:** sources were reviewed by a model; cross-checking multiple publications does not make the authoring pass an independently blinded medical review. The graph's `source_check` fields mean provenance/author reading, NOT independently certified medical truth.

## Recursive Three Questions: specific evidence of correction

- **Q1 (what went wrong?)**: E3/E6/E7 pointed at related observations/requirements, not the actual claim under dispute. C_TROPONIN_ACUITY omitted the requirement that an injury threshold was crossed. The unqualified 'MI requires observed troponin' universalization misses type 3.
- **Q2 (correct structure?)**: separate observable evidence, needed evidence, and diagnostic conclusion as distinct Concepts. Relations must end at the **target proposition being justified**, not a nearby correlated term.
- **Q3 (what could disprove it?)**: high ketones with near-normal pH/HCO3; chronicity documented versus single eGFR; a cTn delta below threshold; type 3 fatal MI lacking sampled troponin. These force conditions/exception boundaries rather than wholesale collapsing families.

**No ungrounded promotion**: No claim that the machine independently induced these repairs from raw text; this was owner-requested model reasoning with public-source inspection. No real learner-unseen trial, learner benefit, scheduled unattended work, publication, Anki or private data changes.

## Reproducible regression

`python -m unittest discover -s tests -p 'test_ale_problem_family_bridge.py' -v`

This file asserts graph consistency, typed bridge non-merging, specific corrected E3/E6/E7 endpoints, the type 3 exception, troponin threshold and absence of falsely certified independent QA. Tests are **structural contracts for what was decided**, not clinical adjudication or genuine model semantic-discovery measurement. Run exact-head CI and report results separately.

## What qualifies as the next substantive win?

Give a different (separated-context) reviewer an unseen clinical source excerpt with source URLs **without providing the author-created role tokens, graph proposal, or expected answer**. Require extraction of one atomic claim, an explicit relation target, and an adversarial condition; compare against the tag-first grouping and the prior nonrecursive proposer at fixed time / materials. The examiner should score **wrong-target relations**, **false family merges**, **missed exceptions**, **source truth**, and actual owner intervention. Only then can we claim semantic discovery beyond a model-authored example; distinct clinician review is needed before real medical knowledge promotion.

Final state: `AUTHOR_SOURCE_CHALLENGE_AND_GRAPH_REPAIR_DELIVERED / PROPOSED_GRAPH_ONLY / STRUCTURAL_TEST_AWAITING_CI / MEDICAL_INDEPENDENT_REVIEW_PENDING / LEARNER_TRANSFER_NOT_MEASURED`.
