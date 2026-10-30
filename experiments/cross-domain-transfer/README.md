# XDT-01 — Domain-neutral skill transfer / preregistration (2026-10-30)

**Status: DESIGN + ARTIFACT / HOLD. No real model attempts, blinded scores, cost receipts or generalization result.**
Owner-directed experiment: [Issue #251](https://github.com/sheng-web-OS/Clinical_system/issues/251). This is **outside** the fixed 72h autonomy cohort registered at [#137 comment 6489616643](https://github.com/sheng-web-OS/Clinical_system/issues/137#issuecomment-6489616643), ending 2026-11-01T06:20:15Z. Do not add a scheduler, merge, edit #225, publish, or treat activity here as autonomous success.

## Hypothesis and intervention
Can a *pre-frozen*, domain-neutral decision skill distilled from clinical CBD/counterfactual/source-audit failures improve **first-pass** task decisions in genuinely unfamiliar, non-medical settings beyond mere evidence checking? Compare three independent, parallel agent contexts on identical sealed tasks:

- **A Native**: same base model, neutral task instructions, matched sources/tools and budget.
- **B Evidence-only**: A + short generic rule to verify primary sources, provenance, conflicts and unknowns. No decision skill.
- **C Evidence+Skill**: B + the exact frozen content of [decision-skill-v0.md](decision-skill-v0.md). No case-specific examples, precomputed answers, domain templates, or privileged sources.

Use same model snapshot, reasoning effort, tool environment/permission, source bytes, output format, time cap and *maximum* tokens. Record actual tokens, not just caps; if C's extra prompt or thinking increases costs, report it rather than declaring a free gain. If B/C instruction-length difference proves important, a length-matched placebo arm is the prespecified next ablation, **not** retroactive outcome cherry-picking.

## Strict separation
The GitHub repository is PUBLIC, including this Draft PR and Actions. **Never commit the hidden tasks/gold, private blinded-arm allocation, private judge identities, first-pass responses, proprietary source packs or credentials.** An external independent examiner creates unfamiliar tasks **after this protocol+skill commit is frozen**, stores plaintext and gold in access-restricted storage, and releases only task packet input to each isolated worker. Record inaccessible, overlapping, impossible or contaminated tasks as invalid and report denominators. Public filenames and domain descriptions are NOT concealed tasks.

Do not run actual trials until the existing 72h observation concludes; this experiment remains owner-nudged / outside cohort even afterward. Provider access, trusted restricted runner, cost cap and independent examiner/adjudicator must be explicitly verified first. No public CI workflow should receive confidential payloads. A protocol file and synthetic integrity tests cannot certify real model execution.

## Domains / blinded trial distribution
Twelve **fresh sealed tasks**, independent examiner-authored: 4 each of (1) supply-chain/inventory allocation under conflicting records, (2) isolated/simulated IT incident triage and rollback criteria, (3) document provenance and version/citation adjudication. Include at least one unresolvable/stop case in each domain; avoid clinical terminology and existing GitHub issue-specific trivia. Vary surface vocabulary, data format and decisions. Match domain task difficulty on a pre-execution rubric. Include controlled **T6 revised-evidence** prompts only after initial outputs are frozen; analyze these separately.

**Pilot**: 1 task/domain × 3 arms = 9 attempts; this is a feasibility/debug stage, never counted toward confirmatory evidence. **Exploratory comparison**: 4 tasks/domain × 3 arms = 36 first attempts; one per task/arm, no reruns or selection of best-of-N. Randomize task and arm order with private nondeterministic allocation, retain an access-controlled mapping; neither the worker nor blinded evaluator may see other arms' outputs or gold. If pilot causes any change to skill, seal a fresh non-overlapping formal batch and report protocol version.

## Assessment / endpoints (pre-specified)
1. **Primary task-level valid decision success (0/1)** against independent gold and explicit allowed uncertainty/abstention; report paired C–B and C–A successes, discordant-task counts, domain-specific estimates, uncertainty and all failures. 12 cases are too small to establish broad generalization.
2. **Non-compensable critical failures**: fabricating a source or measurement, breaching a permission boundary, unauthorized action, false certainty with critical decision impact, and failure to identify information that makes action unsafe. Any C-only critical failure => HOLD pending root cause, regardless of mean accuracy.
3. **Mechanism**: evidence conflict identified, competing causal explanations tested, discriminating observation requested/used, decision threshold and counterfactual update correct; source-backed rather than prose-format preference. Score independent factual outcomes, not similarity to skill phrasing.
4. **Efficiency**: first-pass elapsed wall time, model/tool calls, actual USD spent, input/output tokens, owner attention minutes and intervention count. Unknown values = NOT_MEASURED, not zero.
5. **T6**: after first pass seal, disclose a new contradictory fact, measure update correctness and downstream affected claims without changing the original gold or giving hints.
6. **Contamination**: examiner checks leakage of answer key, earlier benchmark exposure, answer-dependent scoring rules, grader style bias, tool shortcuts and impossibility. Log invalid tasks without quietly replacing them.

Report pilot and exploratory results separately. Report paired uncertainty; do not label the system VALIDATED based on a favorable 12-task sample or green CI. Any promotion to cross-domain reliability requires a second independently prepared, entirely new held-out batch and blind adjudication. If C is not clearly better than B given uncertainty, or shows critical regressions or disproportionate marginal cost, retain/trim the skill only for the proven context rather than expanding architecture.

## Implementation boundary
- Public immutable candidate skill: [decision-skill-v0.md](decision-skill-v0.md), frozen by PR exact SHA and content SHA-256.
- Public structural verifier: `tools/check_xdt01_trial_manifest.py`. It checks completeness/matching on **sanitized metadata only**; it can never authenticate a provider, judge independence or outcome truth. All successes in its own tests are harness tests, not agent capability.
- Private sealed packs, private arm-to-output map, independent outcome labels and provider billing receipts stay external. Publish only aggregate, rights-cleared results *after* review.
- Use existing #133 for observed failures, #137 for broader growth and #225 for separate clinical skill evidence; no duplicate tracker, paid recurring workflow or automatic writer dispatch.

Methodological references: [AgentBench, ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html); [Emerging Trends in AI Agent Evaluation](https://sage.cs.princeton.edu/trends/); [Trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/).

## Private examiner adapter (preflight, not a live trial)
An isolated, non-medical offline packaging implementation is in [`tools/seal_xdt01_private_cases.py`](../../tools/seal_xdt01_private_cases.py), with synthetic-only regressions in [`tests/test_seal_xdt01_private_cases.py`](../../tests/test_seal_xdt01_private_cases.py). Its [private handoff contract](PRIVATE_EXAMINER_HANDOFF.md) requires separately authorized examiner, worker and facilitator roles; file permissions, role labels and SHA checks are **not proof** of authentication, prospective non-exposure, external rights clearance, actual blind adjudication, or model execution. Do not mount the multi-case stage into any worker. This is not a retrofit of #225's synthetic clinical paid runner and does not execute calls.
