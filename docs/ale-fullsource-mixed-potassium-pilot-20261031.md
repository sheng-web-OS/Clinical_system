# ALE Full-source Q0 Pilot｜Coexisting true + pseudo-hyperkalemia
**2026-10-31 owner-directed | Draft #260 / Issue #258 | public-source research, no new personal learner record, no medical publication.**

## Direct source evidence actually read

**New complete research source**: Turner AG, Vardesh DL. *Hyperkalemia in Clinical Practice, an Important Reminder of Testing Modality*. *Clinical Case Reports*. 2025;13(10):e71242. DOI [10.1002/ccr3.71242](https://doi.org/10.1002/ccr3.71242); [PMCID PMC12513848](https://pmc.ncbi.nlm.nih.gov/articles/PMC12513848/), PMID 41079794. Complete OA full-text document accessed in this interactive research turn via Europe PMC `PMC12513848/fullTextXML` (21,678 characters extracted as full-text text); the newly committed **Python full-text program itself was NOT yet live-run against the endpoint** during this turn. This distinction matters.

The authors report genuine hyperkalemia related to AKI, including early ECG changes, **and** an in-vitro serum potassium artefact in the setting of thrombocytosis. When the AKI improved, mild apparent hyperkalemia persisted on routine serum testing. Comparing testing modalities supported the pseudohyperkalemic component. Thus **a real potassium disorder and a spurious potassium component may coexist**; being able to identify one artefact does not prove the entire original disorder was false. This is a published patient case, not a simulated prescription and not causal population evidence.

**Existing source actually inspected**: `content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md` and `content/xiaoma-internal-medicine/lab-morning-sheet-sources.md`. They ALREADY thoroughly teach pseudohyperkalemia in AML, thrombocytosis-related clotting artefact, the lack of typical ECG changes failing to rule out dangerous genuine hyperkalemia, and the confounding of re-testing after treatment. A gap-finder must **not** create a new `pseudohyperkalemia` Concept or repeat all those facts. What is at most a **specific candidate relation extension** is explicit *non-mutual-exclusivity*: in-vivo elevation and ex-vivo elevation may contribute concurrently to an observed report; different collection specimens can distinguish components in context without concluding all abnormal results were spurious.

Additional independent published counterexample: [Pseudonormokalemia, PMCID PMC11177651](https://pmc.ncbi.nlm.nih.gov/articles/PMC11177651/) (2024) describes a normal serum potassium result in thrombocytosis hiding hypokalemic plasma potassium. This supports a **direction-of-bias** Q3 challenge, not a universal adjustment formula or diagnostic mandate.

## Topic spine and three-question differential

**Q0 / encountered inconsistency:** Serum potassium remains high, but the clinical context, ECG and alternate specimen can tell a different story; why is the conclusion `either genuine or spurious` too restrictive?

**Q1 / separation of observed evidence:** Genuine AKI-related potassium retention, stage of recovery, actual blood potassium, cell breakage or clotting during specimen processing, specimen type, timing of treatment and recheck, and ECG/clinical state are different variables. None alone explains the other in this published patient. A normal ECG cannot exclude true hyperkalemia, and a discordant serum/plasma pair is an observation requiring specimen/timing analysis.

**Q2 / candidate Concept graph:**

```
published clinical source 2025
       ↓ supports contextual comparison, not population rule
[physiological potassium state] ──→ [true in-vivo potassium]
             |                                    |
             |                                    ▼
             |                           [reported analyte]
             |                                    ▲
[specimen / clotting / cell release] ──→ [ex-vivo artefact]
     │
     └── context-dependent: plasma vs serum, platelet/WBC state,
         hemolysis, transport, timing and method
```

Proposed relation `CAN_COEXIST(in_vivo_abnormality, ex_vivo_measurement_artefact)`; **NOT `is_a`**, **NOT `all serum potassium is artefactual`**, **NOT a deterministic arithmetic subtraction or therapeutic algorithm**. Cross-link the existing `lab-result-does-it-reflect-patient` topic rather than duplicate its original Concepts.

**Q3 / counterexamples:**
- A case may start with a real disorder but later show residual assay-dependent elevation → rejects binary `true XOR pseudo`.
- Normal ECG in severe hyperkalemia is possible → cannot use ECG alone as a truth validator.
- With marked thrombocytosis, a normal serum potassium may *conceal* lower plasma potassium → rejects assuming an artefact always points in the high direction relative to clinical decision threshold.
- ECG changes and serum/plasma discordance in one patient do not establish precise proportions of true vs pseudo elevation, or that a fixed treatment protocol is safe for everyone.
- The earlier Clinical OS AML case has post-treatment confounding; any cross-case integration must preserve **different patient identities and temporal sequences**.

**Revised Q0:** When measurements conflict, which competing parts arise from the patient, and which from collection/processing, and what *context-valid independent observation* differentiates them without prematurely asserting a single mechanism?

## What the new executable full-text tool actually does

- `tools/ale_fullsource_q0.py` can fetch the **entire OA JATS article** by exact PMCID via allowlisted Europe PMC origin, rejecting missing explicit CC license metadata, entity declarations, oversized or nonmatching sources; it can also consume trusted offline fixture XML.
- Parses up to 350 body paragraphs (not references); scans all paragraphs in bounded chunks with existing `ale_raw_q0_probe.extract`; adds a domain-agnostic `COEXISTENCE_HYPOTHESIS` cue, which specifically tests whether apparently exclusive explanations may be joint contributors. It scores an initial *one Q0* for subsequent Q2/Q3, and prints citation/section/paragraph/sha256 plus **at most 12 words** of source preview, not an entire copyrighted document.
- Existing public article is an **optional comparison input**; overlapping English terms merely produce `existing_context_may_cover_topic` warnings. This does **not** prove semantic identity, nor does lack of overlap prove novelty. In particular Chinese vs English coverage prevents trustworthy autonomous novelty classification based on strings.
- No preset topic-specific keywords, Concept ID, typed graph labels or impact scores are inputs. No Anki IDs, owner-private learning records, medical promotion, publication or website change; no paid API or new scheduler.
- `tests/test_ale_fullsource_q0.py` are offline negative-control JATS samples, including mixture case, source ID/rights, malicious XML, dedupe, avoiding reference list and no promotion. **A green CI only verifies engineering paths, NOT successful live Europe PMC retrieval or model-level semantic inference**.

Command (opt-in from branch checkout; source is public CC-license gated):

```bash
python tools/ale_fullsource_q0.py --pmcid PMC12513848 --live-oa --context-file content/xiaoma-internal-medicine/lessons/2026-10-28-lab-morning-sheet.md
python -m unittest discover -s tests -p 'test_ale_fullsource_q0.py' -v
```

## Decision and measurement

Provisional *human-readable* outcome of **this interactive source review**, not automatic clinical semantic output:
`LINK_EXISTING_CONCEPT_FAMILY + PROPOSE_NON_EXCLUSIVE_RELATION_CANDIDATE`. Do **not** make a duplicate pseudo-hyperkalemia family. `NO_CARD`, since no owner's actual unseen answer/reading reasoning evidence was observed. Exposing the case as a learner assessment without first reviewing answer leakage would undermine a future blind test.

**Acceptance remaining:** confirm real program live OA retrieval and total-paragraph selection; have an independent examiner read the prior full Lab lesson and new case in randomized order and adjudicate whether this is a genuine missing relation (not already explained), use a distinct new OA article as hidden test, compare selection quality vs tag routing, and only then consider private ALE learning benefit. If the automatic top Q0 is a generic metadata contrast, count that as **failure** and repair the ranking rather than claiming autonomous discovery.

**Attribution:** new owner-directed work after original early-terminated #137, not evidence for the frozen historical cohort. Delivery-first #254 remains priority; #260 stays Draft.
