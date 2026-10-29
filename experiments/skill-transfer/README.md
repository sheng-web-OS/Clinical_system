# Experience → Skill → Decision: decision-question triage pilot

**2026-10-29 | Experimental Draft / HOLD | Not a medical or publication release**

## Purpose

Question: when an agent learns from a previous case-discussion failure, does the resulting *selectively invoked* strategy improve the **first unhinted decision on a different, previously unseen task**, beyond an otherwise capable model retrieving the same long-form articles?

This experiment adds **one** repository-scoped candidate skill:
`.agents/skills/decision-question-triage/SKILL.md`.
Codex can discover repository skills in `.agents/skills` in supported local environments, but **discovery / invocation by all cloud runners is not guaranteed**. This PR does not enable a hosted agent, API access, unattended job, autonomous skill updates, or evidence of learning.

The skill is deliberately *about when and why to select a consequential question*, not a disease-specific answer, an exam key, a general medical synopsis, or a new Master Prompt. It must learn to decline an invented controversy as well as identify a real competing clinical explanation.

## Model comparison design (preregister before any semantic runs)

A. **native** — same current model, original task, same source/tool/budget access; no additional reusable skill.
B. **retrieval** — native plus appropriately retrieved existing long-form Clinical_system article / source (retrieval choice and exposure fixed and logged).
C. **skill** — same B access plus the decision-question triage skill. The extra text and retrieval cost must be counted.

Use **independent worker contexts** per case/arm, matched model versions and thinking effort, same initial case material and case-specific source SHA-256, equal tool permissions and budgets, balanced execution order, frozen trace and rubric. Trial evaluator must be blind to arm and proposed winner. Candidate skill and development fixtures are public/exposed; genuine holdout materials, answer keys, protected case facts and private reviewer receipts belong outside this public repository in access-controlled storage.

At minimum the experimental corpus needs:
- **Transfer**: an unexposed different-domain case where the central question genuinely distinguishes mechanisms or decisions.
- **Normal**: a competent ordinary case explanation that should *not* be rejected merely to find a mistake.
- **Boundary**: a pure definition/background or missing-information task where the skill should correctly stay inactive or narrow inference.

Do not reveal expected defect, preferred question, the original complaint, old RED, or reviewer answer to the worker. Freeze and score the **first output before feedback**, not the corrected V2. Record not only errors missed but false alarms, newly introduced P0/P1 medical risks, context leakage, tool failures, owner interrupts/minutes and true costs; do not treat missing cost as zero.

## Executable integrity gate (structural, not semantic)

`python tools/compare_skill_transfer.py --suite /secure/path/plan.json --run /secure/path/outcomes.json`

Suite fields: `schema_version=1`, `id`, `exposure=development`, `cases: [{id,role,source_sha256}]`. The evaluator only handles visible development data; never relabel it as a blinded clinical result. Compute SHA-256 of the **exact plan file bytes** and bind it in the run.

Run fields: `schema_version=1`, `suite_id`, `suite_sha256`, `candidate_commit` (40-hex), and `records` with one entry for every `case_id × native/retrieval/skill`. Every record must have `case_id, arm, source_sha256, decision_correct, first_pass, unsafe, hinted, false_alarm, worker_context, reviewer_context, trace_ref, model, effort, tools_scope, token_budget, owner_minutes`. Booleans are adjudicated by a genuinely separate reviewer; this utility can test logical integrity but **cannot authenticate the reviewer or infer medical truth**. Unknown actual owner minutes use `null`; never `0` unless observed.

Exit codes: `2` invalid/incomplete/noncomparable inputs; `1` hard safety or normal/boundary control regression; `0` structurally valid pilot record without this hard block, **not** a release approval. The JSON always declares `promotion_authorized=false`, `clinical_validated=false`, `autonomous_runtime_verified=false`. Even an apparent development gain requires independent unseen-case repeat, safety review, measured total cost and human sign-off on any clinical release. A single transfer case can at most signal *which hypothesis to test next*.

## Existing infrastructure, no second ledger

- #133 remains the only real failure ledger; the source incident is linked, never copied with private clinical details.
- #137 remains the growth / owner-attention metric owner; this experiment is an update to that issue, not a parallel dashboard.
- #159 is the separate unattended autonomy test, and #205 contains the *unmerged* deeper clinical discussion reviewer candidate. They are neither proof of transfer nor silently incorporated here.
- #222 is a still-blocked synthetic Google Drive / keyless authentication prototype; the runtime cannot be assumed configured, and no credentials should be added as part of this skill PR.
- Existing `.github/workflows/pages.yml` already runs `python -m unittest discover -s tests` on PRs. These tests only check that invalid trial accounting fails closed.
- No changes to `site/pages.json`, clinical sources, licensed figures, production deployment, API keys, GitHub workflow permissions or auto-merge.

**Decision rule:** Only after genuine independent and safe holdout evaluation, keep the skill if it reliably beats retrieval alone without raising cost/false-alarm/safety burden. Otherwise keep the articles and discard the extra skill. Do not patch the benchmark to make a candidate win.

Related methods:
[OpenAI agent improvement loop](https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop);
[Codex skill discovery](https://learn.chatgpt.com/docs/build-skills);
[MSCE](https://aclanthology.org/2026.findings-emnlp.1637/);
[ProactAgent](https://aclanthology.org/2026.findings-emnlp.775/);
[GEPA](https://arxiv.org/abs/2507.19457).
