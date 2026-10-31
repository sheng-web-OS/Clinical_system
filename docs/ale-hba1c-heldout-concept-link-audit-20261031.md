# ALE held-out cross-domain test 03 — HbA1c validity vs optical SpO₂ validity

**Date:** 2026-10-31, Asia/Taipei. **Owner-directed interactive model analysis**, out of early-terminated #137 cohort. **Not medical publication / independently reviewed physiology / autonomous unattended task completion.**

## What was held out

The previous source-first research pilot was about optical SpO₂ reliability. This round independently selected HbA1c from a *different* biomedical measurement and clinical decision domain. The owner supplied **no HbA1c topic, concept IDs, research priority labels, or correct disposition** for this round. However, the model itself chose the topic, extracted relevant scientific relations, assigned graph node types and selected evidence; the test is *not a blinded independent examiner or model-free semantic discovery*.

Relevant current source: `content/xiaoma-internal-medicine/lessons/2026-10-29-eudka-real-case.md` mentions an HbA1c of approximately 12.9% as a detail of the real case. GitHub indexed search of current `Clinical_system` did not find a dedicated *HbA1c validity→diabetes diagnosis* reasoning lesson; **absence in search is not proof that the subject has never been taught**. Earlier `content/clinical-os/index.md` is organized by patient question, but does not establish a canonical, accepted higher-order optical + glycated hemoglobin measurement-validity family. The prior #260 SpO₂ higher-order abstraction is still a *proposal only*.

## Actual external evidence (source-linked model reading, not independent medical review)

1. **2026 ADA Standards of Care, Diagnosis and Classification**: https://pmc.ncbi.nlm.nih.gov/articles/PMC12690183/ and https://doi.org/10.2337/dc26-s002. Recommendations 2.3–2.4 state that marked consistent discordance between A1c and glucose requires evaluation of interference; when A1c–glycemia relationship is altered (e.g. hemoglobin variants, altered RBC turnover), use **plasma-glucose-based criteria** for diagnosing diabetes. In absence of unequivocal hyperglycemia, confirmation of a diabetes diagnosis is required (usually two abnormal results).
2. **NGSP, Factors that interfere with HbA1c test results, updated 2026-10-23:** https://ngsp.org/factors.asp. *Analytical interference* is variant/assay-method-specific; *shortened RBC survival or decreased mean age* produces a falsely lower A1c **regardless of assay method**. Iron deficiency is associated with elevated A1c, so not every hematologic condition shifts it in the same direction.
3. **NGSP HbA1c method interference table, updated 2026-10:** https://ngsp.org/interf.asp. Documented variant-dependent differences between commercial methods. An NGSP-certified method does not immunize against altered RBC life span.
4. **NIDDK patient/clinician guide:** https://www.niddk.nih.gov/health-information/diagnostic-tests/a1c-test/ distinguishes chronic exposure signal from recent blood glucose, warns about recent blood loss, transfusion, hemolysis, kidney/liver disease and some hemoglobin variants.

## Candidate Concept Map

Source-backed premises, scoped to adult diagnosis outside special situations:

```
          source/NGSP-assay-specific-Hb-variant-interference
                                    │
                                    ▼ [CAN_DISTORT_ANALYTICAL_MEASUREMENT]
  measurement/hba1c-result ──────────────────────────> interpretation/glycemic-exposure
                                    ▲
                                    │ [VALIDITY_PREREQUISITE]
                          biology/RBC-survival-and-turnover
                                    │
                                    ▼
           decision/diabetes-diagnostic-criteria + confirmation
```

**Typed relation meaning:** An Hb variant may cause **method-dependent analytical interference**; independent biological variation in RBC age can change the relationship between an analytically valid A1c value and glycemia. A1c diagnostic cutoffs plus necessary confirmation and exception handling are additional decision-level requirements. `is_a` or `same_tag` links are insufficient. `RBC_turnover` is not an HbA1c analyzer's calibration parameter.

**Proposed higher-order candidate:** `measurement-to-inference-validity` *can* encompass both SpO₂ and HbA1c as a **reasoning-role abstraction** (`VALIDITY_PREREQUISITE`), but the child mechanisms are not medically interchangeable. No canonical parent promotion or new clinical diagnosis rule is authorized.

## Recursive Q0–Q3

- **Q0 / observation:** Why may a clinically unexpected HbA1c conflict with directly measured plasma glucose despite a technically functioning standardized assay?
- **Q1 / alternatives:** At least two different failure types must remain live: Hb variant/assay-method interference and shortened or otherwise altered erythrocyte lifespan. Blood glucose specimen issues or interval change in glycemia can also contribute; do not assume the lab A1c is wrong.
- **Q2 / necessary premise:** Before using HbA1c as evidence for glycemia and diagnosis, establish that the analytical method and the patient's biological glycation/turnover context make the A1c–glycemia relationship appropriate. Then apply the current ADA diagnostic criteria and confirmatory rules.
- **Q3 / adversarial counterexamples:** (a) A better hemoglobin-variant-resistant assay does not solve shortened RBC survival; (b) iron deficiency can shift A1c upward, contradicting “all anemia produces falsely low A1c”; (c) discordant A1c and glucose are not proof of analytical error; (d) a single asymptomatic elevated A1c is not always sufficient to diagnose diabetes without confirmation. Each modifies a different edge.
- **Recursive new Q0:** Which process failed — instrument-level estimation, biological proxy validity, specimen preanalytics or diagnosis confirmation — and what *independent discriminating evidence* is available? Do **not** collapse all into “A1c unreliable” or produce a universal correction factor.

## Actual executable increment

New files on existing #260 branch:
- `tools/ale_unranked_graph_probe.py`: read-only, **no supplied importance/rank labels**, receives a bounded public-source-linked structured graph with node kinds/statuses, existing edges and source-annotated proposed edges. It selects candidate `VALIDITY_PREREQUISITE` **before** `DIAGNOSTIC_CONFIRMATION` for this *hypothesis-testing policy*; other mechanisms are queued and disconnected branches may be left unknown. Returns an explicit status and `clinical_truth_verified=false`; no automatic medical content mutation.
- `tests/test_ale_unranked_graph_probe.py`: **13** structural tests, including out-of-scope branches, source format/privacy, previous relation, valid-vs-associative edges, deterministic ranking and a held-out cross-domain SpO₂ case. The comparison tests a shared *role*, explicitly **not** semantic identity or medical truth.
- `experiments/ale-hba1c-unranked-graph-20261031.json`: minimal role-token fixture. No rank/impact values or learner responses/Anki IDs.

Run on a checkout containing this branch:
```bash
python tools/ale_unranked_graph_probe.py --input experiments/ale-hba1c-unranked-graph-20261031.json
python -m unittest discover -s tests -p 'test_ale_unranked_graph_probe.py' -v
```

**Important limitation:** The program does **NOT** read ADA/NGSP or natural-language textbook sentences and invent correct semantic node labels. An interactive GPT reasoning step authored those concepts/roles, based on the cited public sources. Removing prior `impact` annotations is genuine but only a **partial** increase in autonomous selection. Its ordering rule is unvalidated and may be wrong for other clinical settings; independent clinician + unseen domain tests are necessary.

## Concept action decision

**Current disposition: `LINK_EXISTING_ABSTRACTION_CANDIDATE` + `PROPOSE_TWO_SEPARATE_MECHANISMS` rather than `PROMOTE_NEW_PARENT`.** At the research level, the existing prior measurement-validity candidate already describes the relevant epistemic bridge; HbA1c adds separate analytical and biological failure processes. Since the parent itself is not accepted, these are *reversible relations/hypotheses*, not a canonical ontology migration.

**Card decision = `NO_CARD / LEARNER_GAP_NOT_OBSERVED`.** No owner-private answer or reading-recall was accessed. It would be improper to generate a card only because this report exists.

## Meaningful acceptance remaining

1. An independent source reviewer checks the ADA recommendation version, NGSP technical semantics, and whether the concepts are actually absent from the existing context.
2. A genuinely blind new subject/source packet tests whether the agent *generates the nodes and relations without model-assigned mechanism labels*, and rejects misleading same-keyword merges.
3. Compare to the static tag-based concept selection and breadth-first topic completion at a matched research budget; score semantic false-merge/split, change in practical next learning decision, and (only with consent, privately) learner-unseen/delayed reasoning.
4. If false positives dominate or graph ranking produces unnecessary research, **revert or abandon** the policy instead of accumulating reports and synthetic tests.

Existing #254 remains delivery priority. No merge, automatic publication, owner-private Anki/Drive access, schedule increase, or model spend authorized. Historical #137 verdict remains EARLY_TERMINATED / FULL_WINDOW_NOT_EVALUABLE.
