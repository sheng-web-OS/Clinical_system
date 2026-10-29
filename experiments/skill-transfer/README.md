# Experience → Skill → Decision: decision-question triage pilot

**2026-10-29 | Experimental Draft / HOLD | Not a medical or publication release**

## Purpose

Question: when an agent learns from a previous case-discussion failure, does the resulting *selectively invoked* strategy improve the **first unhinted decision on a different, previously unseen task**, beyond an otherwise capable model retrieving the same long-form articles?

This experiment adds **one** repository-scoped candidate skill:
`.agents/skills/decision-question-triage/SKILL.md`.
Codex can discover repository skills in `.agents/skills` in supported local environments, but **discovery / invocation by all cloud runners is not guaranteed**. An [open Codex Cloud skill discovery issue](https://github.com/openai/codex/issues/52266) reports that repository skills may be present in checkout yet absent from Cloud's advertised skill inventory. A merged file or a green GitHub Action does not prove runtime loading. C must therefore record whether the full `SKILL.md` bytes were explicitly loaded or truly advertised; A/B must record that they were **not exposed** to it. Where discovery fails, pass the identical frozen skill content explicitly to C in an isolated agent context and label it `explicit-loaded`, **not** `native discovery passed`. This PR does not enable a hosted agent, API access, unattended job, autonomous skill updates, or evidence of learning.

The skill is deliberately *about when and why to select a consequential question*, not a disease-specific answer, an exam key, a general medical synopsis, or a new Master Prompt. It must learn to decline an invented controversy as well as identify a real competing clinical explanation.

## Model comparison design (preregister before any semantic runs)

A. **native** — same current model, original task, same source/tool/budget access; no additional reusable skill.
B. **retrieval** — native plus appropriately retrieved existing long-form Clinical_system article / source (retrieval choice and exposure fixed and logged).
C. **skill** — same B access plus the decision-question triage skill. The extra text and retrieval cost must be counted.

Use **independent worker contexts** per case/arm, matched model versions and thinking effort, same initial case material and case-specific source SHA-256, equal tool permissions and budgets, balanced execution order, frozen trace and rubric. **Critical exposure isolation:** do not run all three arms in the same Codex checkout where repository skill metadata may be automatically discovered; A must not see the candidate skill or enhanced article retrieval, B must see article retrieval but not the candidate skill, and only C may see both. Use isolated sandboxes/skill capability directories or independently prepared agent inventories, then retain runtime inventory/trace evidence. The declared exposure flags below are integrity checks, NOT proof of actual isolation. Trial evaluator must be blind to arm and proposed winner. Candidate skill and development fixtures are public/exposed; genuine holdout materials, answer keys, protected case facts and private reviewer receipts belong outside this public repository in access-controlled storage.

The fixed **retrieval pack** is a versioned manifest of which existing author-approved long-form article(s) and primary source versions are available, with provenance and exact contents; B and C must receive the **same** pack. The pack is not an answer key, and retrieving a relevant article is not permission to use its claims outside their original domain. The native arm shares case material and necessary primary source access, but not the additional preselected articles. Freeze a SHA-256 of the retrieval pack and a SHA-256 of the candidate Skill bytes before trial execution.

At minimum the experimental corpus needs:
- **Transfer**: an unexposed different-domain case where the central question genuinely distinguishes mechanisms or decisions.
- **Normal**: a competent ordinary case explanation that should *not* be rejected merely to find a mistake.
- **Boundary**: a pure definition/background or missing-information task where the skill should correctly stay inactive or narrow inference.

Do not reveal expected defect, preferred question, the original complaint, old RED, or reviewer answer to the worker. Freeze and score the **first output before feedback**, not the corrected V2. Record not only errors missed but false alarms, newly introduced P0/P1 medical risks, context leakage, tool failures, owner interrupts/minutes and true costs; do not treat missing cost as zero.

## Actual first-pass runner (new in PR #225)

`tools/run_skill_transfer_pilot.py` is a **synthetic-only development executor**, not a reviewer, clinical AI, skill registry or self-editing agent. It has no credentials in code and **makes zero API calls by default**. The small public development fixture `fixtures/synthetic-questions.json` contains three entirely fictional, pre-exposed prompts: transfer, normal, boundary. Use a real existing authored **public** long-form article as B/C retrieval content (example: `content/xiaoma-reading/originals/2026-07-14-hcm.md`); the HCM transfer case tests whether adding the Skill improves upon an already relevant HCM article, instead of handicapping retrieval with an unrelated source. This is NOT a hidden benchmark.

Offline plan in an existing authorized checkout of **this exact PR head**:

```bash
RUN_PARENT="$(mktemp -d)"
chmod 700 "$RUN_PARENT"
python tools/run_skill_transfer_pilot.py \
  --cases experiments/skill-transfer/fixtures/synthetic-questions.json \
  --retrieval-pack content/xiaoma-reading/originals/2026-07-14-hcm.md \
  --candidate-skill .agents/skills/decision-question-triage/SKILL.md \
  --candidate-commit "$(git rev-parse HEAD)" \
  --output-dir "$RUN_PARENT/plan"
```

The default command saves the exact nine matched model request packets, SHA-256 identifiers, and an explicit `NOT_RUN` manifest **outside the public repository**, with private file permissions. A dry run is evidence of prompt construction only. Run the same command with `--execute-api` **only in an owner-authorized separate environment** where a budgeted `OPENAI_API_KEY` has already been securely configured; the key must never be pasted in chat, GitHub PRs, source, stdout or Actions artifacts. It performs at most **9 separate Responses API calls** with `store=false`, matched output token limit, no tools/history or prior-response linking, and no automatic retries or grades. The real network path accepts **only the exact checked-in public fixture, HCM article and candidate Skill at their canonical repository paths**. Merely adding a "synthetic" marker to arbitrary uploaded/private text does not authorize transmission. Unit tests can inject a fake transport for local non-network assertions. This PR intentionally does not expose credentials in PR CI or authorize a `pull_request_target` workflow. Main was rechecked on 2026-10-29 as **public and branch-protected**, at `27e26132c891e872434d86aa72d11830becb7b5f`; the exact protection ruleset and installed secret permissions are separate matters to inspect before activation, and #222 has its own independent credential activation hold.

During execution, `attempt_events.jsonl` records STARTED and completed/failed for every attempted pair, `first_pass_results.json` freezes original outputs (including failed and incomplete attempts), `blind_reviewer_packet.json` hides arm labels, and `private_arm_mapping.json` remains separate. An interrupted run is **incomplete/HOLD** and must not be represented as a fully observed nine-call trial. These local files may include source content and model responses; do not commit or upload them to this public GitHub repo. A truly separate reviewer must read only the neutral packet and authentic source conditions, then record its adjudication independently; the runner will never fill `decision_correct`, `unsafe`, `first_pass` or `owner_minutes` on the user's behalf. The later comparator is a structural consistency audit, not a substitute for this reviewer or a real runtime attestation.

**Hard limitation:** this developer-visible 3-case fixture, its role labels, and the agent's potential memory of previous critiques make it unsuitable for declaring broad clinical transfer. Only a sufficiently sized, separately stored, pre-registered and unfamiliar holdout with real clinical evidence and expert review could support that claim.

## Review-to-metric handoff: close the missing link without self-grading

The runner freezes `frozen_suite.json` (including all nine fixed source/skill/role fingerprints) **before the first model request**, alongside `manifest.json`. This eliminates post-hoc task changes after learning which arm performed well.

After a **genuinely separate reviewer** has read only `blind_reviewer_packet.json` and authorized source documents, they may create a private `review.json` with:

- `schema_version: 1`, `packet_sha256` (SHA-256 of exact neutral packet bytes), `suite_sha256` (exact frozen suite bytes), `reviewer_context` (identifier for the separate run)
- `judgments`: exactly nine unique slot entries, one per anonymous answer, with `slot`, boolean `decision_correct`, `unsafe`, `false_alarm`, `question_triage_observed`, and a specific written `reason`
- A failed model call must be marked incorrect; it cannot be awarded credit for a plausible answer that was never generated. Clinical P0/P1 risk is adjudicated separately; a generic reason string and claimed independent run ID do not establish medical expertise.

Then run in the same trusted, non-public working environment:

```bash
python tools/assemble_skill_transfer_review.py \
  --run-dir "$RUN_PARENT/plan" \
  --review /secure/path/independent-review.json \
  --cases experiments/skill-transfer/fixtures/synthetic-questions.json \
  --retrieval-pack content/xiaoma-reading/originals/2026-07-14-hcm.md \
  --candidate-skill .agents/skills/decision-question-triage/SKILL.md \
  --output "$RUN_PARENT/comparison.json"
```

The assembler **reconstructs all nine original prompts** and checks their SHA-256 hashes, model calls' recorded STARTED/end events, the preserved first-pass answers, exact source/skill bytes, case aliases, reviewer packet digest, reviewer slot count, and per-arm statuses. It refuses dropped, duplicated, edited or noncomparable evidence, and sends the completed review to the existing `compare_skill_transfer.py` evaluator without inventing any scores. `comparison.json` keeps the raw paired record and mechanical report; it is private, never a publication or skill-promotion receipt. If a call crashes or times out, the comparison remains HOLD even when another arm appears better.

**Interpretation limits:** The rubric judgments and reviewer identity are declared rather than cryptographically authenticated. `question_triage_observed` measures an answer-level behavior, **not proof that loading the candidate Skill caused that behavior**. `owner_minutes` remain null unless the actual owner measures time, so the development tool must not infer a net productivity win. This tool cannot certify hidden-case generalization, clinical truth, real model identity, expert competence, or prompt isolation outside the saved requests. Do not upload the review or response pack to public GitHub PRs, Issues or Actions artifacts.

## Executable integrity gate (structural, not semantic)

`python tools/compare_skill_transfer.py --suite /secure/path/plan.json --run /secure/path/outcomes.json --retrieval-pack /secure/path/frozen-articles.manifest --candidate-skill .agents/skills/decision-question-triage/SKILL.md`

The CLI now hashes both actual input files before accepting the suite's declared fingerprints. File hash equality verifies the supplied bytes, **not** whether a remote model actually saw them; compare with real context/trace evidence before any claim of transfer.

Suite fields: `schema_version=1`, `id`, `exposure=development`, `retrieval_pack_sha256` (64-hex), `candidate_skill_sha256` (64-hex), `cases: [{id,role,source_sha256}]`. The evaluator only handles visible development data; never relabel it as a blinded clinical result. Compute SHA-256 of the **exact plan file bytes** and bind it in the run.

Run fields: `schema_version=1`, `suite_id`, `suite_sha256`, `candidate_commit` (40-hex), and `records` with one entry for every `case_id × native/retrieval/skill`. Every record must have `case_id, arm, source_sha256, decision_correct, first_pass, unsafe, hinted, false_alarm, article_retrieval_visible, candidate_skill_visible, retrieval_pack_sha256, loaded_skill_sha256, skill_applied, worker_context, reviewer_context, trace_ref, model, effort, tools_scope, token_budget, owner_minutes`. The article flag must be false/true/true and the skill flag false/false/true for native/retrieval/skill respectively. In A, article pack and loaded Skill hashes are null. In B/C, the article pack hash must equal the frozen suite hash. Only C loads the frozen Skill hash; `skill_applied` records whether it actually **used** the strategy (not simply saw metadata). A/B cannot apply it; on the non-applicable boundary case, C must decline it. A skill not applied on any transfer case cannot earn attribution. **All of these self-declared flags/hashes remain unverified unless matched to externally retained runtime inputs, capability inventory and traces**. Booleans are adjudicated by a genuinely separate reviewer; this utility can test logical integrity but **cannot authenticate the reviewer or infer medical truth**. Unknown actual owner minutes use `null`; never `0` unless observed.

Exit codes: `2` invalid/noncomparable inputs; `1` hard safety, incomplete API response or normal/boundary control regression; `0` structurally valid pilot record without this hard block, **not** a release approval. The JSON always declares `promotion_authorized=false`, `clinical_validated=false`, `autonomous_runtime_verified=false`. Even an apparent development gain requires independent unseen-case repeat, safety review, measured total cost and human sign-off on any clinical release. A single transfer case can at most signal *which hypothesis to test next*.

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
