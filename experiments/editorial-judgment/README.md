# EJE v0.1｜可重現的編輯判斷力評鑑

**Status: protocol + retrospective seeds; independent blinded validation NOT YET DONE.**
**Owner:** Clinical OS evaluation. The GitHub repository and this PR are **PUBLIC**. This directory contains only exposed, retrospective development fixtures; it is **not** a private holdout or a new Master Prompt. Never commit confidential reviewer keys, patient records or genuine unseen assessments here.

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
- **labels.json:** public historical development labels, **not an access-controlled secret**. Do not mount, search or feed it to the candidate agent; an isolated executor must provide only a sealed input pack. Genuine unseen clinical holdout labels and independent reviewer records must be kept in a separately access-controlled environment, never this public GitHub repo. Exposure of these retrospective cases means they are regression tests only, not evidence of out-of-sample generalization.
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

For case-level four-stage N/X/C/V, use `0=missed/wrong or after-hint only, 1=partially justified first-pass, 2=fully justified first-pass`; report *each component*, not a self-awarded composite. A genuine after-feedback fix is recorded separately as **repair responsiveness**; it is never awarded first-pass detection credit.

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
- `score.py` rejects impossible negative-control true-positive counts, fractional issue counts, duplicated case IDs, and incomplete replayable cohorts; user-supplied human-time numbers are reported only as **unverified** and never promoted to verified minutes. It summarizes **supplied** adjudications; it **cannot** authenticate reviewer identity, source truth, medical correctness, prospective calibration, or learning effectiveness. A green CI only proves the integrity checks run.
- Publication release receipts, private source integrity and website QA continue independently. Passing EJE does **not** authorize publication.

## 2026-10-22 integrity correction (no new capability claim)

- J01–J03 retrospective task briefs were neutralized: candidate-facing text no longer directly states the expected answer (e.g., which article must be excluded or that the HCM original should be preserved). This only **reduces** prompt leakage; it does not eliminate model/topic exposure.
- **J03 must remain a contaminated regression control** for claims of generalization. The HCM article is an explicitly known EPQC benchmark, and the Clinical OS condition may receive that benchmark through its own quality contract. Do not call a J03 win a blind discovery.
- The pre-feedback website snapshot is Git-pinned, but candidate input must be exported to a clean workspace containing only the listed files and neutral task. Do not let candidate agents access this repository's `labels.json`, this README's historical correction descriptions, later commits, or PR discussion.
- Candidate-facing export command (from a **full Git checkout with the pinned commit available**): `python experiments/editorial-judgment/export_input.py J01 --repo . --out /tmp/eje-input-packs`. Only `TASK.md` and pinned `sources/` are exported; `type`, `status`, `source_state`, gold labels and later commits are withheld. Export refuses to write inside the repository. **Do not give the candidate repository/GitHub-search access**, or the separation can be defeated.
- `score.py` now forces `PILOT_HOLD` for independently adjudicated missed major issues or newly introduced P0/P1 errors. With no such flagged errors it still reports `PILOT_ONLY` and `NOT_VALIDATED`, **not** medical clearance.
- Scoring regressions are in `tests/test_eje_score_guard.py` and run via the existing CI test discovery. CI validates code behavior only, never the gold labels or the medical truth of a finding.
- Before measuring Native vs Evidence-only vs Lite, assign at least one **unexposed** negative-control article and one seeded major-error article from a non-HCM/DCM domain, freeze identical sources and reviewer labels, and run each arm in separate contexts. Those new source packs must be prepared without the candidate seeing expected answers.

## Next independent milestone

Freeze the real baseline snapshot for J01/J02 and run the first one-pass Native vs Evidence-only vs Clinical OS Lite evaluation with labels withheld. Compare not only errors found but the false-positive count and predicted edit size. Before investing in Full governance, see if Lite proves reproducible gains.
