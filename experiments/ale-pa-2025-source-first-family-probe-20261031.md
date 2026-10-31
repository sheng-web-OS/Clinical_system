# ALE｜New clinical problem Family from raw source: Primary Aldosteronism (PA)

**2026-10-31 / source-first, owner-directed research candidate / no medical publication or promotion.** This source was selected by the model during the present owner-directed "continue" workflow; the owner supplied NO PA topic, tagging, prior Concept ID, edge type, or expected answer. However the authoring model is still responsible for choosing, interpreting and labelling the source. Therefore this is **not blinded independent semantic discovery**.

## Goal and entry conditions

Use the existing #260 raw-text Q0 module, not a new taxonomy or agent pipeline. Input one attributable, short public guideline sentence rather than author-supplied ontology roles. Test whether it can *notice* a decision-role contrast, then let the model propose **noncanonical** family structure using actual source context and Q3. At this stage the deterministic code has zero ability to infer medical relation types or verify true novelty.

- Clinical guideline: Adler GK et al., *Primary Aldosteronism: An Endocrine Society Clinical Practice Guideline*, *JCEM* 2025;110:2453–2495, PMID **40658480**, DOI https://doi.org/10.1210/clinem/dgaf284, [Endocrine Society official recommendations](https://www.endocrine.org/clinical-practice-guidelines/primary-aldosteronism-2). Explicitly distinguish Recommendation 1 (screen individuals with hypertension) from Recommendation 3 (measure plasma aldosterone / renin; potassium aids accurate interpretation).
- **Important formal correction:** https://doi.org/10.1210/clinem/dgaf472 (published online 2025-08-29, print issue November 2025): in Figure 1 the direct renin concentration unit was corrected **from mU/mL to mU/L** and the PRA unit typography corrected. This candidate does NOT copy potentially erroneous original figure thresholds or dosage, and does not claim this correction changed the role-of-potassium statements.
- Secondary corroboration, not a substitute for the primary guideline: AHA/ACC 2025 hypertension guideline notes that spontaneous hypokalemia occurs only in a fraction of PA patients and is not a valid prerequisite to consider screening: https://doi.org/10.1161/CIR.0000000000001356

## Q0 before semantic interpretation

The machine-readable entry is [a single source-linked short (20-word) exact excerpt](./ale-pa-2025-raw-role-contrast-20261031.json), `source_ref=pmid_40658480`, **without** any family ID, severity rank or relation labels. It explicitly contrasts why potassium is measured alongside renin/aldosterone with what potassium is **not** itself used for. Do not supply a full copyrighted guideline page as input.

**RED baseline:** `tools/ale_raw_q0_probe.py` previously keyed mostly on `despite / cannot / unless`, missing `not for ... but to ...` in the guideline sentence. The 8 newly introduced regression tests exposed this false negative; GitHub Actions commit `ba7a034` failed as expected (additional existing bad unittest method signature was also exposed).

**Repair:** add generic `MEASUREMENT_ROLE_SPLIT` and `MEASUREMENT_VALIDITY_RISK` text cues, suppress editorial `not for publication` lookalikes, retain exact spans, source type and non-private constraints. Also repair existing `test_no_label_or_private_data(self)` signature. **No medical edge is inferred** by the lexical rule. Evidence quality, mechanistic direction and classification still require a separate semantic pass and independent clinical review.

## Candidate problem-centered Family (authoring-model interpretation, NOT code-discovered)

**Clinical Q:** In a person with hypertension, what does potassium contribute to (A) selection for PA screening, (B) interpretation of aldosterone/renin results, and (C) deciding to repeat testing?

| Concept candidate | Small testable proposition | Distinguishing role | Primary source |
| --- | --- | --- | --- |
| `PA-01` | Absence of spontaneous hypokalemia does **not** rule out PA or block screening consideration in hypertension. | Clinical phenotype vs screening eligibility | Guideline Rec 1 and Rec 3 |
| `PA-02` | PA screening rests on aldosterone + renin interpreted jointly (including ARR), not low potassium as a stand-alone screening test. | Measurement target vs supporting context | Guideline Rec 3 |
| `PA-03` | Hypokalemia can suppress observed aldosterone, potentially contributing to a falsely negative PA screen. | Biological measurement validity modifier | Guideline Rec 3 technical remarks |
| `PA-04` | When screening is negative in the presence of hypokalemia, the guideline recommends correcting potassium and repeating the screening test. | Conditional re-test decision | Guideline Rec 3 technical remarks |
| `PA-05` | Medication effects, local assay methods, and pretest probability also matter when interpreting aldosterone/renin testing. | Competing modifiers and scope | Guideline Rec 3 technical remarks |

**Typed, *not-yet-approved* edges**:
- `PA-01 --disproves_prerequisite--> [hypokalemia_required_for_screening]` (explicitly reject this invented rule)
- `PA-03 --can_bias--> [measured_aldosterone]` (conditional, no universal correction factor)
- `PA-03 --qualifies_interpretation_of--> [PA-02]` (disease-screen interpretation versus phenotype)
- `PA-03 --conditional_retest_trigger--> [PA-04]` only when screen is negative and relevant confounding is present.
- `PA-05 --competes_with_and_modifies--> [PA-02]` (clinical context, not an assertion that all drugs have identical direction).

## New higher-order relation (DO NOT merge families)

Candidate cross-family **`one-observation-multiple-decision-roles`**: one observable quantity may have different roles as a screening eligibility feature, assay/biological interpretation modifier, or intervention safety variable. PA's potassium is **not medically identical** to potassium in DKA. PA relates potassium to aldosterone diagnostic interpretation; DKA relates extracellular potassium to insulin-treatment safety and total-body potassium depletion. It is a **typed reasoning analogy**, not `is_a`, `causes`, or an automatic merge. Nor is this the same as the previously proposed `evidence-sufficiency-is-target-relative` bridge: it concerns **variable role across distinct decision stages**.

## Recursive Three Questions + Q3 negative controls

- **Q1 observed paradox:** Potassium is measured with ARR, yet is not itself the screening criterion. Absent hypokalemia does not exclude PA.
- **Q2 structure:** Separate *who to screen* from *what laboratory evidence screens* and *conditions that undermine interpretation*. Low K may lower aldosterone and lead to misleading negative interpretation.
- **Q3-A:** A hypertensive patient with normal potassium still meets the population described in conditional Recommendation 1. Reject `normal potassium → no screen`.
- **Q3-B:** With an initially negative screen and hypokalemia, the direction is to correct and reassess rather than conclude `PA excluded`; this is not a blanket command to retest every negative result.
- **Q3-C:** A positive ARR does not, by itself, establish unilateral adrenal disease or direct surgical candidacy. Distinguish disease screening from lateralization.
- **Q3-D:** Correction of an *unrelated lab unit* in the guideline is a document-version issue; it must not be silently treated as changing all clinical decision semantics. Check figure errata before copying thresholds.

**No-card is the current action**: the owner's personal learning gap has not been observed on this subject. No Anki tags, private answers, inferred mastery or card proposals are written to public GitHub.

## Technical falsification and honest milestones

- `tests/test_ale_raw_q0_pa_role_split.py`: 8 new cases assert finding the evidence phrase with zero supplied clinical label, generic false-signal cues, provenance spans, negative/metadata controls and no forced concept creation.
- `experiments/ale-pa-2025-raw-role-contrast-20261031.json`: tiny attributable source excerpt. 
- `tools/ale_raw_q0_probe.py`: improved Q0 *attention* only. Formal semantic induction, accepted ontology edge, independent clinician QA, cross-run memory and unseen learner benefit remain **NOT_MEASURED / NOT_IMPLEMENTED**.
- Comparison outcome needed: hold the same source and time budget; compare *tag-first*, original Q0, revised Q0 plus independent Q2/Q3 analysis. Measure exact-span recall, useful questions per source, false triggers, wrong edge targets, overlooked applicability exceptions and owner prompts. **Do not inflate a hand-written 8-test regression to scientific generalization.**

**Stop conditions:** If generic Q0 generates many false triggers, revert the new cue; if Q2/Q3 cannot distinguish screening eligibility from test validity or the authoring-model semantic error rate is not improved on truly unseen material, stop promotion and investigate before expanding. No additional scheduler, private database, site release, canonical Concept Family promotion, paid API or #137 numerator changes.
