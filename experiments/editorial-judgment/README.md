# EJE v0.1｜可重現的編輯判斷力評鑑

**Status: protocol + retrospective seeds; independent blinded validation NOT YET DONE.**
**Owner:** Clinical OS private evaluation. **Not public content** and **not a new Master Prompt**.

## Why this exists

The repeated user revisions are a source of *decision supervision*, not merely stylistic preferences. Existing EPQC already evaluates prose A–G. EJE evaluates a different claim: **before receiving the correction, can an agent independently find the consequential defect, diagnose its root cause, and propose the minimum justified repair—or correctly decide NOT to rewrite?**

A fixed article score cannot prove this. Outcome = original editorial decision + effect on errors/reader value + actual human intervention. Maintain the original feedback and input snapshots separately. An agent reproducing a known answer after reading the feedback does not count as autonomous discovery.

## Unit and four-stage competency

One record = (pre-feedback artifact, task, available evidence at a pinned snapshot, withheld feedback label, editor's first-pass findings, adjudication, minimal repair and regression). The editor may autonomously choose methods.

1. **NOTICE (N)**: identify the actual consequential defect before any user hint (with precise location and why it matters). Also be willing to say "no serious problem".
2. **EXPLAIN (X)**: distinguish source error, causal gap, pedagogy gap, provenance/rights, publication boundary, UX failure, or a false alarm; identify the broken relationship or assumption.
3. **CHOOSE (C)**: select no change / local correction / missing bridge / dedicated new material / justified restructuring / HOLD or exclude; avoid gratuitous rewrites and unauthorized promotion.
4. **VERIFY (V)**: inspect the necessary original PDF Figure/Table/caption/footnotes, source or user-authorized document; test relevant counterexamples and check the fix did not introduce new errors. Clearly report missing evidence.

EPQC and medical P0/P1 hard stops remain binding. An EJE grade **cannot** override clinical safety, legal rights or author-source identity.

## Benchmark construction

- **cases.json:** task and *pre-correction* artifact/available evidence only. Do NOT reveal the expected failures, fixes or user response in a candidate evaluation.
- **labels.json:** separate adjudication file. Do not mount, search or feed it to the candidate agent. Same repository storage is convenient, **not inherently blinded**: an independent executor must provide the candidate only an exported input pack. Candidate models previously exposed to these cases are contaminated; historical cases are regression tests, never evidence of out-of-sample generalization.
- Case status `replayable`: actual pre-feedback commit exists and task can be executed from it. `needs_freeze`: genuine feedback exists, but a faithful baseline or PDF view is not yet available. These can guide dataset construction but **must not be included in metrics**.
- Freeze a source manifest (sha/ref, file path, original-source scope, available figures and permissions), user task, model & effort, tool permissions, prompt, time budget, random assignment, and scorer rubric **before** generation.
- Include positive controls (real mistakes), negative controls (sound material: no rewrite), near misses (same theme, different source), and a future holdout with topics not used to write this rubric.
- A reviewer can inspect the labels after the model's first response is irreversibly saved. Reviewers should see anonymized outputs in random order; at least two independent ratings for the pilot, disagreements recorded rather than resolved by score inflation.

## Output required of each candidate

For each pre-feedback case, return a structured judgment with:
- `decision`: `keep | local_fix | bridge | new_material | restructure | hold | exclude_public`.
- Each finding: original span/path, consequence, mechanism or provenance, evidence needed/checked, priority P0–P3, concrete minimum repair, counterargument **against** the repair, and residual uncertainty.
- Proposed edit scope: changed paragraphs/files (or none); no code or content changes in the first blinded detection round.
- Self-audit: what could make the diagnosis false; whether the original already explains the issue.

Do not force all seven EPQC axes to be narrated. Judge an actual editorial action, not jargon/verbosity.

## Severity and observable assessment

- **P0** immediate potentially dangerous clinical misinformation, publication of private/source-protected data or severe source fabrication.
- **P1** important medical/conceptual misclassification, misleading decision threshold, wrong original Figure/Table, inappropriate public inclusion, or unjustified destructive rewrite of a valuable original.
- **P2** material but noncritical causal gap, disconnected reading flow, poor figure integration, wrong audience/voice, or intrusive editorial metadata.
- **P3** cosmetic/format-only (normally omit unless explicitly requested).

For each *frozen* expected issue, independent adjudicators must answer: independently detected before hint? correctly located? cause correct? solution proportionate? evidence verified or honestly pending? Did the candidate create a new issue?

Scoring has **two non-substitutable layers**:
1. **Validity gates**: P0/P1 unresolved → HOLD; author-original adulterated → HOLD; medical source/figure claimed seen but not seen → HOLD; release/public identity violated → HOLD. No average may compensate.
2. **Decision effectiveness** (stratified by case severity, type and source):
   - **Major issue recall** = independently detected P0/P1 expected issues / total P0/P1 expected issues.
   - **Material issue recall** = independently detected P0–P2 / expected P0–P2.
   - **Finding precision** = adjudicated valid findings / all substantive findings (false-positive penalty).
   - **Minimal-repair accuracy** = cases where edit choice and scope both appropriate / adjudicated cases.
   - **Over-revision rate** = negative controls or local fixes unnecessarily restructured / relevant cases.
   - **Evidence honesty** = assertions of source viewing properly supported / all such assertions.
   - **Human correction time (minutes)** and number of intervention turns, including verifying/restoring gratuitous changes.
   - **Net value** = robust improvement in serious error detection and revision burden, **without** higher false positives, omissions or source violations.

For case-level four-stage N/X/C/V, use `0=missed or wrong, 1=partial/late, 2=fully justified first-pass`; report *each component*, not a self-awarded composite. A genuine after-feedback fix is recorded separately as **repair responsiveness**; it is never awarded first-pass detection credit.

Important: a finding's validity is established by a blinded reviewer, not by the model naming its own failure code. The model should not be asked to predict label IDs.

## Measurement and comparisons

1. **Retrospective audit:** replay pinned pre-feedback artifacts without the subsequent user corrections. Separately identify contaminated cases. This measures regression ability, **not** new discovery.
2. **Controlled same-model study:** Native GPT-6 vs Evidence-only vs Clinical OS Lite; identical starting artifact, primary sources, tool budget, effort and output demand; randomized, independent contexts. The only systematic variable is the editorial system given. Test at least three distinct clinical subjects plus one publication boundary and one correct-as-is negative control.
3. **Prospective holdout:** newly chosen source topic and independent figure/problem unknown to any training examples; pre-register outcome. Only this stage can substantiate autonomous generalization.
4. **Human reader experiment:** for website/UI changes compare static vs interactive versions on reasoning transfer, accuracy, time and cognitive burden; feature usage alone is not learning gain.
5. **Maintenance comparison:** repeat on model upgrade. Retire EJE scaffolding if native model plus evidence-only reproduces performance with less maintenance.

**Do not average incompatible tasks or call one successful demonstration "stable."** Report per-category denominators, uncertainty, negative controls, and full failures.

## Initial audit, not a passing grade

Observed pre-feedback failure in the current project: **Tamponade** was placed in the public XiaoMa candidate list because it was a mature Clinical OS experiment. The editor corrected only after the user's question. Therefore first-pass boundary detection = **missed** for that historical attempt; subsequent removal in PR #12 is **responsive correction**, not self-discovery. Likewise metadata/publication separation was first pointed out by the user. This honesty is the calibration baseline: our new evaluator must catch such issues with the user's correction withheld.

Several seeds are marked `needs_freeze` until actual earlier drafts, Pocket 9E original PDF figure pages and feedback timestamps can be bound; do not quietly manufacture a "before" draft.

## Least-maintenance integration

- Reuse EPQC's A–G *quality of final prose* and existing medical checks; EJE only grades the **editorial decision-making above the prose**. No new agent fleet, persistent global Claim Graph or separate site.
- Store high-impact accepted/falsified decisions and one regression case per recurring failure family. A new permanent rule is justified only if a failure recurs or an automated test protects a high-cost edge.
- `score.py` validates and summarizes adjudicated results; it **cannot** automatically decide whether a medical claim is true or whether prose is cognitively effective.
- Publication release receipts, private source integrity and website QA continue independently. Passing EJE does **not** authorize publication.

## Next independent milestone

Freeze the real baseline snapshot for J01/J02 and run the first one-pass Native vs Evidence-only vs Clinical OS Lite evaluation with labels withheld. Compare not only errors found but the false-positive count and predicted edit size. Before investing in Full governance, see if Lite proves reproducible gains.
