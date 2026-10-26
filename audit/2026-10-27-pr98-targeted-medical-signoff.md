# PR #98 — P0/P1 targeted medical and semantic sign-off packet

Date: 2026-10-27 · Scope: four newly authored AI-integrated liver/GI chapters · **UNSIGNED / publication HOLD**.

This is a minimal reviewer interface, **not another intake ledger**. Author snapshots, Pocket 9E viewer figure locations, original-image rights strategy, the seven original preflight figure contracts (now **eight**, with a real-case ALP counterexample), and routine code/layout testing are delegated to Agent and existing CI. The reviewer should make **four per-article judgments**, not redo source transcription or a full audit report.

## Policy agreed for the Clinical_system release cycle

- **Agent owns**: independent research and drafting; fact/claim extraction; direct citation verification; prevention of copying publisher pixels; corrections to original figures; source link validation; layout at 360/390/1280px; site and exam regressions; same-commit build; preparing a deploy-ready PR and checking actual deployment afterward. A CI pass is an **engineering result, not a medical result**.
- **Independent medically competent reviewer owns**: whether any P0 clinical instruction is unsafe, whether any P1 diagnostic/test inference is misleading, and whether the article's decisive figure could lead a clinical reader to an unsafe shortcut. Reviewer must actually read the relevant text and graphic; Agent's own interpretation is not an independent review.
- **Release owner owns**: article-specific ACCEPT or HOLD. A reviewer ACCEPT is evidence for a decision but not authorization for unrelated pages. No default whole-PR merge of four chapters merely because one passes.
- **Author provenance**: Facebook canonical verification is not a gate for a new explicitly AI-integrated article; never label historical originals canonical without evidence. Pocket textbook **viewer PDF** page labels are allowed when explicitly labelled; do not invent printed page identifiers.
- **Rights**: the new decision figures and explicitly cited numerical case reconstruction contain no reproduced Pocket Medicine pixels; a subsequent addition of a third-party original image reopens rights review **for that image only**. Do not make general image clearance a perpetual blocker for pages using independent diagrams.
- **Change invalidation**: medical sign-off applies to the exact content SHA/PR revision. Changes to a signed clinical claim or its decisive figure require targeted re-review; unrelated CSS or source formatting that passes regression checks should not invalidate every medical signature.
- **Sequential publication**: after targeted medical + figure sign-off and same-commit successful CI, select only approved article(s) and shared source page for release, confirm merged main, deploy and URL/visual verification. Unapproved articles remain Draft/HOLD in the working branch. Avoid additional parallel release infrastructure.

## Focused independent judgments (the reviewer should not re-check unrelated text)

| Article | P0: must not teach unsafe clinical action | P1: inference / numerical boundary | Key figure | Reviewer verdict |
|---|---|---|---|---|
| Cholestasis #66 | Suspected cholangitis with sepsis/organ dysfunction triggers timely antibiotics, resuscitation and source-control evaluation; 48h is **not** permission for an unstable patient to wait. | Nondilated ducts on RUQ US do **not** absolutely exclude early/occult obstruction; stable nondilated cases instead need directed PBC/PSC/DILI workup. ERCP is not routine first-line diagnostic test in a stable low-risk case. | 2×2 **US dilation × clinical urgency**; urgent bottom-right branch must clearly override ultrasound result. | **PENDING** |
| Infiltrative ALP #67 | Negative SPEP alone must **not** rule out AL amyloidosis. SIFE, UIFE and sFLC are combined where clinical suspicion exists, and screening is not pathologic typing. | Real 2020 example: 95% of **biopsy specimen**, not whole liver, involved; ALP **85 IU/L**. A single case cannot estimate sensitivity or stage disease. | Claim boundary matrix plus biopsy-versus-serum real-case evidence; no apparent direct linear relationship. | **PENDING** |
| Chronic diarrhea #68 | Normal visual colonoscopy and/or negative calprotectin must not automatically exclude microscopic colitis: biopsies are needed when indicated. Alarm features must not wait for an osmotic-gap workflow. | 290−2(Na+K) gives the **estimate**, not a directly measured stool osmolality. Synthetic case gaps 10, 60, 130 mOsm/kg; thresholds and 50–100/125 gray zone are contextual, not diagnostic disease labels. | Priority-of-evidence matrix and quantitative worked example; no claim that stool gap has routine universal clinical utility. | **PENDING** |
| Cirrhosis #69 | Baveno VIII first decompensation: portal-hypertension-related clinically evident ascites/hydrothorax, variceal bleeding and/or overt HE (West Haven ≥II), **not uncomplicated varices**. | CSPH LSM/platelet rule-out and LSM ≥25 rule-in apply to defined populations and limitations. Recompensation requires controlled etiology, ascites absent off ascites diuretics, no HE off directed drugs, no recurrent variceal bleeding (NSBB continuation permitted), >6 months and Child–Pugh A5/A6; a falling score alone is insufficient. | Five-axis causal distinction + compensated-vs-bleeding clinical event counterfactual; no conflation with biopsy fibrosis stage. | **PENDING** |

## Evidence to inspect (read rather than re-transcribe)

- [ASGE 2021 cholangitis guideline](https://www.asge.org/home/resources/publications/guidelines/asge-guideline-on-the-management-of-cholangitis) and [ACG 2017 abnormal liver chemistries](https://gi.org/guideline/evaluation-of-abnormal-liver-chemistries/).
- [ASH 2026 AL amyloidosis diagnosis guideline](https://pmc.ncbi.nlm.nih.gov/articles/PMC13425172/) and [Doe-Williams et al. 2020 AL liver counterexample](https://pmc.ncbi.nlm.nih.gov/articles/PMC7265701/) (ALP 85 IU/L, 95% sampled biopsy).
- [BSG 2018 chronic diarrhoea guideline](https://pmc.ncbi.nlm.nih.gov/articles/PMC6204957/) and [RCPA faecal osmolar gap](https://www.rcpa.edu.au/Manuals/RCPA-Manual/Pathology-Tests/F/Faecal-osmolar-gap).
- [Baveno VIII 2026](https://www.journal-of-hepatology.eu/article/S0168-8278%2826%2902778-9/fulltext), especially 3.3–3.4 and 7.1–7.4, and [MELD 3.0 original model](https://pmc.ncbi.nlm.nih.gov/articles/PMC8608337/).
- [Public-facing source map](../content/xiaoma-reading/liver-gi-source-review-20261027.md) and existing figure gate JSON on this **same revision**. Original snapshots and previous clinical audits remain privately archived; they need not be duplicated in this packet.

## Exact review / release record

For each article, a medically competent independent reviewer records **ACCEPT** or **REQUEST CHANGES**, the PR head SHA, and any P0/P1 error by quoting the affected sentence/figure identifier. Incomplete or missing review = HOLD. The Agent may address corrections and re-request **only the changed question**. A reviewer acceptance alone does not imply the live site changed.

Engineering checklist prior to release: source/figure gate PASS for candidate, 360/390/1280px rendered HTML and figure checks PASS, full GitHub Actions commit PASS, image rights declaration, deployment confirmation, live URL and mobile visual check. Currently these are **preflight checks**, not authority to deploy.

**Present state:** all four reviewer verdicts PENDING. This packet does not certify medical correctness; no article is automatically approved by creating it.
