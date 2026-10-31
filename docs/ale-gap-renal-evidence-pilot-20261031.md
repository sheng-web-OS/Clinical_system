# ALE Evidence-Driven Knowledge Gap Pilot｜Renal/Hypernatremia
**2026-10-31｜Public-safe research artifact｜candidate only｜no learner or patient data**

## 0. What was actually inspected

Existing source: [Clinical OS renal overview](../content/clinical-os/index.md), [108-year renal concepts article](../content/xiaoma-internal-medicine/lessons/2026-10-22-exam108-renal-foundations.md). The second document **already** explains KDIGO AKI time windows, why FENa may fail with vomiting/bicarbonaturia, hypernatremia water deficit vs sodium correction, and the 2023 Feigin hypernatremia adult cohort. Thus those explanations **are not missing content**. The selected gap is the *newer conflicting evidence and distinction between observed treatment trajectory and causal prescription*.

External public evidence checked at abstract or freely available full-text level, 2026-10-31:
- [PMID 37768662](https://pubmed.ncbi.nlm.nih.gov/37768662/): Feigin et al. *JAMA Network Open* 2023, adults with Na >=155, N=4,265; faster observed correction (>0.5 mmol/L/h) associated with lower 30-day mortality; retrospective association.
- [PMID 40152929](https://pubmed.ncbi.nlm.nih.gov/40152929/): *Relationship between Rate of Hypernatremia Correction and Outcomes in Hospitalized Patients* (2025), N=37,913 adults with hypernatremia at admission; slower correction associated with **lower in-hospital mortality** (PS-weighted aOR 0.63, 95% CI 0.59–0.67), but more nursing facility/hospice discharges. This points in an opposite direction from the 2023 cohort for the selected mortality association.
- [PMID 39765195](https://pubmed.ncbi.nlm.nih.gov/39765195/): Kitisin et al. *J Crit Care* 2025 meta-analysis of 12 studies; faster correction overall mortality OR 0.68 (95% CI 0.38–1.24), substantial heterogeneity I²=95%; some admission/severe/early subgroups differ. Search through Aug 2024, so not exhaustive for 2025–2026 studies.
- [PMID 41240509](https://pubmed.ncbi.nlm.nih.gov/41240509/): Pattamin/Chuasuwan, *J Crit Care* 2026 Apr, online Nov 2025; MIMIC-IV target-trial emulation of severe hypernatremia in critically ill adults, 1,861 eligible, 430 propensity-matched; faster early correction associated with lower 30-day mortality (adjusted HR 0.49, 95% CI 0.28–0.84). **Target-trial emulation is still observational, not a randomized trial**.
- [PMID 40390726](https://pubmed.ncbi.nlm.nih.gov/40390726/): smaller US 2025 regional retrospective cohort (N=150), no statistically significant 90-day/1-year mortality differences between >8 vs <=8 mmol/L/day groups; inadequate to settle effect.
- [UpToDate topic index](https://www.uptodate.com/contents/treatment-of-hypernatremia-in-adults) updated July 23, 2026; useful as a *coverage outline* only in this review. Restricted sections were **not** read or treated as source evidence.

Related domain gaps, which remain lower priority and need separate full-text/applicability checking:
- [PMID 39698350](https://pubmed.ncbi.nlm.nih.gov/39698350/): 2024 Kidney International Reports, serial UPCR in 329 AKI patients had useful predictive signals despite nonsteady SCr.
- [PMID 42901297](https://pubmed.ncbi.nlm.nih.gov/42901297/): online Oct 20, 2026 AJKD, 100 patients, paired spot ratio vs **24-hour urine excretion** showed substantial imprecision during AKI. **Different estimands/comparators, not evidence that one paper falsifies the other**.
- [PMID 30626576](https://pubmed.ncbi.nlm.nih.gov/30626576/): Palmer/Clegg CJASN 2019 on urine chemistries; urine Na/Cl discordance in alkalosis is already explained in the existing article; only a cross-family linkage opportunity, not a new missing mechanism.
- [PMID 32734201](https://pubmed.ncbi.nlm.nih.gov/32734201/): kinetic GFR nonsteady-state model, a lower-urgency extension; not a reason to imply ordinary steady-state eGFR is valid during rapidly changing SCr.

All `source_state` and `impact` values in the executable fixture are **model-authored, provisional annotations**, not independent truth checks.

## 1. Four gaps (not four claims of missing text)

| Candidate ID | Actual possible gap | Why priority differs | Action expected |
| --- | --- | --- | --- |
| `hypernatremia_causal_rate` | New conflicting 2025/26 rate-mortality associations not integrated into *inference bounds* of the existing 2023-based section | Current actionable risk: converting observational associations into a fixed bedside correction target could be harmful | `RESEARCH_NOW`, but no clinical action/promotion |
| `aki_upcr_target_validity` | Distinguish AKI longitudinal spot-ratio predictiveness from spot-vs-24h agreement, rather than equating study conclusions | A prerequisite before revising existing UPCR caution, second priority | `QUEUE_RESEARCH` (capacity one) |
| `renal_urine_chloride_context` | Relate urinary anion balance to broader measurement-context family | Current renal article already has mechanism; incremental cross-family value only | `QUEUE_RESEARCH` |
| `kinetic_gfr_context` | When kinetic-GFR modeling warrants attention rather than routine nonsteady eGFR | Interesting advanced extension, not current blocking clinical issue | `QUEUE_RESEARCH` |

Run the actual source-indexed role packet:

```bash
python tools/ale_gap_source_case.py --input experiments/ale-gap-renal-source-linked-20261031.json
python -m unittest discover -s tests -p 'test_ale_gap_source_case.py' -v
```

The adapter **does not browse, read papers, or judge their truth**. It only verifies that IDs are public PubMed-format references, rejects arbitrary private text, calls the already existing `ale_gap_triage.py`, and preserves the citation IDs next to each policy decision. The model did the literature interpretation in this research artifact; there is no independent reviewer pass.

## 2. One selected gap actually investigated: rate–outcome causal bridge

**Initial candidate overgeneralization A:** If rapid correction is associated with reduced mortality, intentionally prescribing rapid correction must reduce mortality.

**Q0/Q1: What was actually measured?**
- Observed achieved correction rate is a **post-baseline time-dependent outcome of multiple processes**: prescribed fluid, ongoing fluid losses, kidney function, severity/other treatments, frequency/timing of sodium sampling, and duration of survival. The primary cohorts measure *associations*, not randomized treatment assignment.
- Study populations differ (admission hypernatremia versus admission-or-hospital-acquired, severe threshold versus broader admission hypernatremia, ICU-specific sample), exposure windows differ (early 24-h versus overall), and endpoints differ (30-day versus in-hospital, competing dispositions). These differences matter but are **not themselves proven explanations for the opposite observed directions**.
- In 2025 large multi-center cohort slow rate correlated with lower in-hospital mortality, directly challenging any universal observational rule that faster is associated with better survival. However, hospice/nursing disposition differences prevent a simplistic reverse causal interpretation.
- The 2025 meta-analysis is mixed/heterogeneous, and the 2026 target-trial emulation improves design relative to crude comparisons but remains susceptible to residual bias and assumptions.

**Q2: What Concept structure is actually needed?**

Propose (NOT promote) a higher-order family `candidate/observed-trajectory-vs-causal-intervention`:
- `measurement/serum-sodium-trajectory` --[**DESCRIBES**, not **DETERMINES_CAUSALLY**]→ `outcome/observed-mortality-association`.
- `intervention/prescribed-water-replacement-strategy` --[**AFFECTS_WITH_OTHER_FACTORS**]→ `measurement/serum-sodium-trajectory`.
- `context/time-zero-severity-onset-disposition` --[**MODIFIES_INTERPRETATION_OF**]→ `outcome/observed-mortality-association`.
- `source/design-and-confounding-limits` --[**CONSTRAINS_INFERENCE**]→ `claim/optimal-correction-rate`.

Do not model these as `is_a` links, convert a tag into a causal edge, assume only one cause of rate differences, or infer a numeric ideal correction target. Potential sibling families: measured biomarker trajectory versus disease classification; physiologic response versus diagnosis; treatment intensity versus attained intermediate outcome. **Cross-domain equivalence is a candidate analogy, not verified semantic identity.**

**Q3: Attempt to falsify the overreach**
1. If faster correction *necessarily* implies better survival, how can a much larger admission cohort report the opposite association? → Overgeneralization A **fails** (does not mean slow treatment is proven causally superior).
2. If slower correction is always safer, why does 2023 severe hypernatremia and 2026 TTE show associations favoring faster correction? → Reverse universal rule also **fails**.
3. If the lack of chart-documented cerebral edema establishes safety at all correction rates, what about ascertainment of rare delayed events and noncomparable children/chronicity groups? → Safety universalization **not supported**.
4. Could an apparent subgroup explanation (early vs overall, severe vs any hypernatremia, admission vs hospital acquired) resolve all findings? → **NOT VERIFIED**; retain a research question, not a proven mechanism.

**Recursive new Q0:** For which precisely defined adults, onset/chronicity, initial severity, time zero, dynamic treatment trajectories and outcome measure could a *causally interpretable* estimate of correction strategy be made? Which study assumptions and actual exposure measurements would be required to distinguish efficacy from confounding / survivor bias? **No single numeric treatment recommendation follows from this pilot.**

## 3. What really changed in the topic map

**Before:** `Hypernatremia → traditional slow-correction concern → 2023 observational challenge → cautious bedside adjustment` (existing manuscript already contains this).

**After (candidate projection only):** `Hypernatremia severity/onset → prescribed treatment strategy ≠ achieved correction trajectory → heterogeneous observational rate–mortality evidence → cannot infer one optimal causal rate → continue individualized source-verified clinical assessment`.

This is a *decision-inference repair*, **not** a newly discovered hypernatremia physiology mechanism. It can be incorporated into an updated renal editorial candidate after separate medical/source review. Do not directly alter the published website or established clinical protocols.

**Card decision:** `NO_CARD_YET / DIAGNOSTIC_FIRST`. No actual learner confusion has been observed in this pilot. The correct next learning question would test whether the learner distinguishes observed association, estimand and causal strategy; only an observed deficit plus genuine unseen transfer justifies a future card candidate.

## 4. Contrast and acceptance

- **Static completion baseline:** Expand all four article topic branches or generate cards wherever bibliography changed. This would spend effort on the already-covered urine Na/Cl issue and conflate information coverage with inference quality.
- **Triage candidate:** Investigate the single high-consequence contradictory source cluster, then challenge the parent inference and preserve other questions without treating them as fully answered.
- **Observed now:** A real externally sourced 2025–26 contradictory evidence cluster has been identified, a bounded source-linked *model-authored* concept repair exists, public-safe executable gap triage and negative tests exist.
- **NOT observed:** Independently verified per-paper clinical source appraisal, agent choosing its own initial impact labels from raw medical text, QA accepted semantic promotion, same-budget controlled comparison, owner-private learning outcome or unattended autonomous wakeup.
- **Next proof:** A distinct medical reviewer checks study designs, estimands and Q3 counterexamples; another source/topic is held out. Compare same-time static completion vs Q3-prioritized strategy for semantic errors, time, false merges, learner-unseen transfer and human interventions. Correct sources/medical safety must remain hard gates.

**Integration:** #258 ALE; existing #260 recursive Concept Family Draft; #254 delivery-first controls scheduling. No new automation, premium API, or published knowledge changes. Preserve #137 early-terminated attribution.
