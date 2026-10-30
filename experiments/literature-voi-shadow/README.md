# Literature → Code S01: research-value shadow probe

**Status:** DESIGN / ARTIFACT; OWNER_DIRECTED_PARALLEL; Draft/HOLD. This is not an autonomous execution outcome, a new scheduler, or a production GDC. It MUST NOT enter the original #137 72-hour autonomy numerator.

## Precisely scoped question

When an agent already has at least two **eligible** task actions, is an additional literature lookup expected to improve the next decision enough to pay its research cost? The probe compares the utility of choosing now against the *hypothetical* expected utility after obtaining evidence. This is a small, independently authored adaptation of **rational metareasoning / expected value of information**, not a reproduction of any paper's software or a deployed task router.

Primary published conceptual sources:
- Russell & Wefald (1991), *Principles of metareasoning*, Artificial Intelligence 49, 361–395, DOI [10.1016/0004-3702(91)90015-C](https://doi.org/10.1016/0004-3702(91)90015-C).
- Wan et al. (2026), *The Shadow Price of Reasoning: Economic Perspective on Optimal Budget Allocation for LLMs*, ICML / PMLR 306, [published record](https://proceedings.mlr.press/v306/wan26p.html). This motivates resource-bounded selection **but the code does not implement CLEAR**.

## Model correction: upper bound is not realized search value

**Red-team finding (2026-10-30):** First version used `sum_state p(state) max_action utility`, which assumes perfect knowledge after a literature search. That is **EVPI**, an upper bound on what any imperfect research signal can deliver, not the expected net benefit of an ordinary paper search. It could incorrectly recommend a search that yields no actionable information.

Current version uses EVPI **only as a cheap rejection ceiling**. If EVPI <= research cost, output CONTINUE_DIRECT. If EVPI > cost but no `research_signals` model is supplied, output **SHADOW_NEEDS_SIGNAL_MODEL**, never RESEARCH. For a specified *hypothetical* observation distribution `P(signal|state)`, compute EVSI and suggest research only when **EVSI > cost**. A search equally likely to produce the same signal under every state has EVSI=0. All estimates are unvalidated and remain advisory.

The method and the EVPI/EVSI distinction are grounded in Jackson et al. (2021), *A guide to value of information methods for prioritising research in health impact modelling*, Epidemiological Methods, DOI [10.1515/em-2021-0012](https://doi.org/10.1515/em-2021-0012). Clinical examples in that article provide decision theory only; this lab does **not** provide clinical recommendations.

## Implemented artifact

`voi.py` accepts a JSON proposal on stdin and returns **SHADOW_SUGGEST_RESEARCH**, **SHADOW_CONTINUE_DIRECT**, **SHADOW_NEEDS_SIGNAL_MODEL**, or **HOLD**. It has no network/model/GitHub calls and cannot trigger a task or grant authority. Eligibility is an upstream hard gate; a held action can never become eligible because it scores well. Estimated values and probabilities are caller-provided and **NOT calibrated**; they MUST NOT be interpreted as measured work value. The comparison is a mathematical toy until evaluated on independent outcomes.

Simple call:

```bash
printf '%s\n' '{"schema_version":1,"mode":"shadow","research_cost":1,"actions":[{"id":"fix","gate":"eligible"},{"id":"inspect","gate":"eligible"}],"evidence_outcomes":[{"id":"red","probability":0.5,"action_values":{"fix":10,"inspect":0}},{"id":"green","probability":0.5,"action_values":{"fix":0,"inspect":10}}],"research_signals":[{"id":"paper-supports-fix","likelihood_by_state":{"red":0.75,"green":0.25}},{"id":"paper-supports-inspection","likelihood_by_state":{"red":0.25,"green":0.75}}]}' | python experiments/literature-voi-shadow/voi.py
python -m unittest discover -s tests -p test_literature_voi_shadow.py
```

## Preregistered next test (NOT RUN)

Keep existing task/authority baselines and #244 as canonical GDC owner; do not amend #241, #137/#159 or PR #224/#225/#234/#235. On a future independently selected, **nonmedical and nonrelease** task cohort whose as-of inputs are frozen *before* seeing outcomes, compare (A) existing priority-first/no extra research, (B) native GPT-6 with the same information and budget, and (C) the same native model with this **advisory** VOI gate. Blind an independent reviewer to arm, log authorized task completion, wrong task decisions, actual human interventions, elapsed time, tools and actual cost (or NOT_MEASURED); count safety/rights violations as disqualifying. Keep evidence-outcome estimates isolated from holdout results and measure calibration; if uncalibrated, label conclusions INCONCLUSIVE. Report per-task paired effects, not PR count. Stop/retire if C fails to improve verified delivery over B, raises intervention or cost without offsetting gains, or increases unsafe recommendations.

**No observed gain claimed:** deterministic synthetic unit tests verify mathematical/gating mechanics only; consult exact-head CI for test count. No real literature fetch by the agent, no true probabilities, no model head-to-head, no CI result before exact-head check, no independent QA, no user-time savings, no active scheduler.

**Canonical links:** [#244 GDC](https://github.com/sheng-web-OS/Clinical_system/issues/244) and [#245 external intake candidate](https://github.com/sheng-web-OS/Clinical_system/pull/245). No duplication of its package security gate. Shadow-only deployment.

## Next real deliverable (not executed yet)

Use independently selected, non-sensitive historical/public GitHub engineering tasks with evidence available **as of** decision time, and compare how often the native decision changes after useful retrieval. Do not use the 72h protected holdout, any secretly sealed case, or post-outcome data to calibrate the model. Explicitly label probability estimates `UNVERIFIED` until measured from separate cases. Native-only (B) remains a serious competitor; if no measured reduction in user interventions over B, **REJECT** and remove the new rule. No further heuristic modules until this discriminating test is run.
