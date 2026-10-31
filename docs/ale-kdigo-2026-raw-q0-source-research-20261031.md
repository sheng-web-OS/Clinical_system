# ALE Research Pilot 04｜Unlabelled KDIGO 2026 source → one Q0 → source-checked concept boundary

**2026-10-31, Asia/Taipei | research artifact only | no public site edit, Anki write or clinical decision rule | existing Draft PR #260 and Issue #258**

## Executive result

Without any user-provided Concept ID, ontology role label, importance score or topic-specific keyword, a **bounded deterministic raw-sentence preflight** can find an unlabelled source contrast from the KDIGO 2026 CKD anemia guideline: iron can be retained in stores yet remain unavailable to erythropoiesis. This is a plausible source-linked **missing distinction** relative to the current Clinical OS teaching atlas, not a new biological discovery. An interactive model separately interpreted its meaning using original KDIGO Fig. 3/4 and accompanying text.

**Best candidate action:** propose `iron-storage-vs-erythropoietic-availability` as a new *topic-specific* Concept Family **CANDIDATE**, keep the clinical source and boundaries attached, and do **not** treat every low TSAT or elevated ferritin as either a proven systemic depletion or a proven hepcidin-mediated mechanism. Preserve old labels as synonyms with provenance rather than asserting equivalence across every clinical context.

## 1. Baseline inventory (actual read/search)

- Existing single published atlas: `content/clinical-os/index.md` includes renal perfusion/AKI and oxygen carrying; it does not currently provide a CKD anemia/ferritin/TSAT iron-state reasoning branch in the sections inspected.
- Public repository indexed search for `iron-restricted erythropoiesis`, `TSAT`, `hepcidin` had no content hits; `ferritin` was present in another true severe-anemia case as a lab detail. This is a **search-limited coverage observation**, not proof that no private, draft or unseen source already covers the topic.
- Previous ALE parents `measurement-to-inference-validity` (SpO₂/HbA1c) remain PROPOSAL ONLY. Shared words like hemoglobin and iron do not establish a shared medical mechanism.

## 2. Original external guideline and what was actually checked

2026 KDIGO guideline: `https://kdigo.org/wp-content/uploads/2026/04/KDIGO-2026-Anemia-in-CKD-Guideline.pdf`; PMID **41485812**, *Kidney International* 2026 109 Suppl 1S. Public PDF **visually inspected on source pages S32 and S33** (zero-indexed PDF pages 31 and 32); separately indexed text and recommendations cross-checked against `https://www.sciencedirect.com/science/article/pii/S0085253825004958`.

- **S32, Figure 3 and adjacent definition text**: the guideline differentiates *systemic iron deficiency* (low ferritin, low TSAT) from *iron-restricted erythropoiesis* (higher ferritin, low TSAT). Older names *absolute* and *functional* iron deficiency are explicitly revised to better describe the physiology.
- **S33, Figure 4 and caption**: the latter pattern illustrates inflammation-associated hepcidin increase, reduced ferroportin-mediated macrophage iron release, and relative deprivation of marrow erythroblasts **despite retained iron stores**. In systemic depletion, iron supply and circulating availability are lower, with a different compensatory hepcidin pattern. These schematic states are not guaranteed to be mutually exclusive phenotypes in an individual patient.
- **S32/S33 footnotes and text**: conventional ferritin and TSAT thresholds correlate imperfectly with bone marrow iron and response to iron; ferritin is an acute phase reactant, while TSAT is also not a sufficient standalone treatment rule. Wording such as “stored iron adequate” describes a representative mechanism, not a definitive measurement of a given patient's marrow iron.
- **Treatment is a separate question:** 2026 recommendations 2.1/2.3 propose different initiation thresholds for G5 hemodialysis versus non-hemodialysis/peritoneal dialysis. Eligibility criteria from intervention evidence are **not the same as classifying underlying iron-deficiency states**. Recommendation 2.1 and 2.3 are conditional (2D); active infection and clinical circumstances matter.

No treatment, dosing, clinical case simulation or guideline-derived threshold is proposed by this experimental ALE probe.

## 3. Raw, unlabelled Q0 extraction: actual runnable change

- `tools/ale_raw_q0_probe.py` takes only `source_classification`, `source_ref` and `excerpt`. The user/model cannot supply pre-ranked impact, Concept IDs, family labels or edge roles.
- `experiments/ale-kdigo-2026-raw-excerpt-20261031.json` contains two short **unlabelled verbatim fragments** drawn from the same guideline paragraph (combined <25 original-source words). They identify an apparent contrast and a source-bound caveat without copying the guideline's full text.
- A compact generic lexical cue detector proposes at most one **top Q0** and up to eight anchored source sentences; it always records literal evidence spans and the source PMID. If no suitable cue exists, **ABSTAIN**. It never infers real medical semantics or writes an ontology. With the pilot sentence its intended Q0 is: *What unspoken premise makes both apparently conflicting states possible?*
- `tests/test_ale_raw_q0_probe.py`: **11 negative/positive tests** for legitimate contrast, no-cue abstention, existing inference-limits, terminology change, metadata false positives, order/determinism, exact anchored spans, private-like content and no promotion.

**Critical limitation:** The detector works on narrowly supplied, genuinely public short source fragments. It does **not** autonomously obtain full guidelines, identify a genuine novel concept, or validate source truth. The source excerpt was chosen during this ChatGPT interaction. This is an **incremental demonstrable raw-input Q0 substrate**, not autonomous multi-source clinical research. Public-source classification is a caller claim.

Command on the existing #260 branch:

```bash
python tools/ale_raw_q0_probe.py --input experiments/ale-kdigo-2026-raw-excerpt-20261031.json
python -m unittest discover -s tests -p 'test_ale_raw_q0_probe.py' -v
```

## 4. Separate human-readable semantic Q0–Q3 pass

**Q0 / contradiction:** How can a CKD patient appear to have iron stores, yet erythropoiesis remain iron-restricted? This question is caused by a *true source-described physiological contrast*, not by overlapping tag strings.

**Q1 / what is observed:** Ferritin is often used as a storage indicator but may also rise in inflammation; circulating transferrin iron availability is represented approximately by TSAT. Neither alone directly measures the complete functional iron supply to marrow; anemia can additionally reflect reduced erythropoietin or blood loss.

**Q2 / explanatory bridge:** In one pathway there is insufficient systemic iron stock; in another, iron is retained within macrophage/storage pools, with inflammation/hepcidin/ferroportin dynamics reducing transport to circulating transferrin and marrow. The distinction is **stock vs distribution/availability vs marrow utilisation**. A recommendation to start iron is yet another decision layer conditioned by CKD modality and evidence, not simply an `is_a` or synonym relationship.

**Q3 / falsification controls:**
1. `high ferritin ⇒ adequate usable iron ⇒ no iron deficiency effect on erythropoiesis` fails in the iron-restricted model.
2. `low TSAT ⇒ total body iron stores depleted` fails as a universal rule. It can represent different mechanisms.
3. `normal/high ferritin with low TSAT ⇒ proven hepcidin excess` is **not justified** from these indices alone; variation, inflammation, alternative causes and population effects require independent evidence.
4. `systemic deficiency` and `iron-restricted erythropoiesis` **must not be simplified to exhaustive, mutually exclusive diagnoses** based solely on a lab cutoff.
5. `KDIGO iron-start threshold ⇒ universal definition of iron-deficient physiology` fails; guideline recommendation populations are different and benefit/harm assumptions apply.
6. Missing source-figure details (hepcidin / ferroportin arrows, marrow) would make simple tag grouping deceptively plausible; therefore source figures mattered in this source review.

**Recursive new Q0:** Which next observation would discriminate *iron stores are depleted* from *iron is present but not being made available to erythropoiesis*, while accounting for CKD modality and inflammation? The program cannot choose that observation based on raw text alone; this remains a model/source review question, not a patient order.

## 5. Candidate Concept Family and typed edges (NOT promoted)

```
family/ckd-anemia
    ├── mechanism/reduced-epo-supply              [SEPARATE_CONTRIBUTOR]
    └── family/iron-storage-vs-marrow-availability [NEW_CANDIDATE]
            ├── concept/systemic-iron-deficiency  [LOWER_STORES_AND_AVAILABILITY]
            ├── concept/iron-restricted-erythropoiesis
            │       [STORED_IRON_NOT_EQUIVALENT_TO_AVAILABLE_IRON]
            ├── process/hepcidin-ferroportin      [MECHANISTIC_MEDIATOR_CANDIDATE]
            └── measurement/ferritin-and-tsat     [INDIRECT_EVIDENCE_WITH_LIMITS]

decision/start-iron-according-to-ckd-modality [CONTEXT_DEPENDENT_RECOMMENDATION]
  ≠ family/physiological-definition-of-iron-state
```

Concept family and relation identifiers above are **proposed by the separate ChatGPT research pass, not produced by the lexical program**; they are not automatically added to private `Concepts`, `Card_Concept_Map`, `Error_Events`, the canonical public atlas or any published article. The previous measurement-validity meta-family is a possible **shared epistemic analogy only**, not a claim that the mechanisms are equivalent.

**Card action:** `NO_CARD / LEARNER_GAP_NOT_OBSERVED`; no evidence from the user's answers establishes a memory or reasoning deficit.

## 6. Baselines, observations, and acceptance

**Topic-tag-only baseline (hypothesized failure):** group the new claims under `CKD/anemia/iron deficiency`, omitting the store/availability/erythropoiesis distinction. This comparison is an argument, NOT an executed equal-budget baseline.

**Actual result:** source pages visually inspected; candidate previously absent from currently indexed atlas; distinction and false-conclusion checks documented; unlabelled source-fragment preflight plus 11 generic regression tests committed. No source redistribution, clinical patient details, or private learning state.

**Still unproved:** end-to-end automatic topic selection, raw full-text → correct Concept graph, novel semantic inference, independent clinician acceptance, real learner unseen or delayed improvement, independent no-nudge cross-wake autonomy. Source full text and diagrams are not copied to GitHub.

**Next genuine acceptance step:** give a separate reviewer the KDIGO Figures 3–4 and a second unrelated source where superficial wording overlaps but mechanisms differ, without the above candidate map; compare:
- no-graph tag routing,
- lexical Q0 cues plus one structured semantic pass,
- source-aware Q0→Q3 candidate revision.

Score genuinely new missing-bridge detection, false merges, unsupported clinical implications and research minutes. Only promote after independent clinical/source review. Keep existing #254 delivery priority, and historical #137 cohort untouched.
