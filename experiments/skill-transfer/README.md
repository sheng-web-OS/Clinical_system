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

The assembler **reconstructs all nine original prompts** and checks their SHA-256 hashes, model calls' recorded STARTED/end events, the preserved first-pass answers, exact source/skill bytes, case aliases, reviewer packet digest, reviewer slot count, and per-arm statuses. It also produces a private `next_iteration` decision: a safety/tool failure triggers HOLD, C worse than retrieval suggests narrowing/removing a Skill, both arms failing suggests revisiting evidence, C apparently better suggests a genuinely new unseen test, and equivalent results favor the simpler retrieval baseline. This is an **experimental hypothesis**, not an automatic rewrite, score-certified learning, or permission to reuse exposed cases as holdout. It refuses dropped, duplicated, edited or noncomparable evidence, and sends the completed review to the existing `compare_skill_transfer.py` evaluator without inventing any scores. `comparison.json` keeps the raw paired record and mechanical report; it is private, never a publication or skill-promotion receipt. If a call crashes or times out, the comparison remains HOLD even when another arm appears better.

**Provider provenance and actual costs:** Mock/injected test runs are explicitly stamped `INJECTED_TEST_DOUBLE`; only the real Responses API path may be labelled `RESPONSES_API`. A completed API response must carry a unique `resp_...` response ID, an equivalent returned model identifier, and mathematically consistent `input_tokens`, `output_tokens` and `total_tokens`; missing/duplicated/mismatched receipts fail closed. The private evaluation now reports per-arm token totals and the observed C-minus-B token difference when all calls finish. It separates `api_transport_claimed` from `actual_model_execution_verified=false`: locally editable, format-correct provider IDs are NOT authenticated proof of a real call. This is not a monetary invoice: token prices, cache conditions, provider account, and human attention are separate, and locally forged ID strings cannot authenticate a provider. Before claiming a genuine run, match metadata with trusted platform usage/billing evidence, not a string in a self-reported JSON file.

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


## 2026-10-29: conditional source-access probe (new, still Draft/HOLD)

**Why separate from the original A/B/C pilot:** `run_skill_transfer_pilot.py` preloads the long-form article into B/C. That tests assisted reading, **not** the agent's ability to determine if, when and what to retrieve. The new `tools/selective_retrieval_probe.py` is a small supplementary development fixture within this same PR, not a new autonomy registry or a replacement of the existing comparator.

**Important scope distinction:** the new probe conditionally exposes an already loaded, synthetic *local reference text* to the model. It does **not** authenticate a live Drive/tool retrieval, assess provider source discovery, or prove source availability checks. Actual external-read decisions must later be validated with an independently attested tool trace and a genuinely missing/present source condition. The successful OIDC synthetic Drive test is separate infrastructure evidence and must not be counted as this probe's model-selection outcome.

**Two-phase intervention:**
1. Freeze and record an initial `RETRIEVE|SKIP|HOLD` choice, gap type, specific source ID, evidence question, prospective decision pivot, provisional answer and confidence (0–100). The model sees the task and, in B/C only, identical candidate source **titles/IDs**. It never sees document bodies before this decision. C additionally sees the frozen candidate Skill. There is no gold answer or expected label in the model prompt.
2. After the first decision, a deterministic gate blocks retrieval for `missing_patient_fact` and `none` gap types, unallowlisted source IDs, SKIP/HOLD and the native arm (no extra corpus). Only an eligible B/C request receives its one approved public synthetic source body. Final first-pass explanation follows; no retries, hints, source substitution or automatic grading.

**Interpretation:** Native A has no additional retrieval corpus, B and C have identical candidate catalog and source access; the controlled estimate of the *candidate Skill's marginal effect* is C versus B. A is a no-extra-corpus contextual baseline, **not** an equal-tool-access causal comparison of retrieval choice. Candidate source titles may prime the worker; count false-positive reads and no-retrieval controls. A separate future experiment would be needed to isolate tool-discovery friction. A pre-retrieval provisional answer is not an equivalent-length clinical Discussion; independent raters must assess whether post-retrieval reasoning changed **appropriately** and distinguish additional explanation from better decisions.

**Visible development fixtures:** `fixtures/selective-retrieval-synthetic.json` contains three completely fictional, already exposed teaching scenarios and two fictional references. They include a potentially helpful laboratory method source, a missing individual-record case that articles cannot repair, and a self-contained physiology explanation. These are mechanical and model-development controls, **never blinded/unseen clinical transfer cases**. Fail-closed unit tests assert no source-body leakage to the first decision, conditional read, inappropriate retrieval denial, white-listed source identity, stage audit, no clinical-validity certification, and rejection of non-public payload substitution. Separate actual calls or human judgments are not implied by CI.

**Safe offline plan**, in a checkout of the exact PR head:

```bash
RUN_PARENT="$(mktemp -d)"
chmod 700 "$RUN_PARENT"
python tools/selective_retrieval_probe.py \
  --fixture experiments/skill-transfer/fixtures/selective-retrieval-synthetic.json \
  --skill .agents/skills/decision-question-triage/SKILL.md \
  --candidate-commit "$(git rev-parse HEAD)" \
  --output-dir "$RUN_PARENT/plan"
```

This produces `manifest.json` with `model_calls_made=0` and `NOT_RUN`, outside the public Git checkout. **A separately authorized real development execution**, if the dedicated budgeted `OPENAI_API_KEY` is already configured in a trusted local/isolated environment, uses the same allowlisted command with `--execute-api` and a *different fresh* output directory. Only `gpt-5-mini`, precisely these checked-in public fixture bytes and the candidate Skill bytes, and at most 18 sequential Responses calls are accepted. A request event log is written under a private directory; calls are not made by PR CI, no retries or background schedule are activated, and the code never handles patient materials. Interrupted/incomplete requests remain incomplete, not silently successful.

**Required audit before any result claim:** trust-but-verify actual provider billing receipts rather than treating local response IDs as authenticated; preserve first-stage choices, real source exposures, case-arm answer records, attempt failures, first-pass errors, raw token use and owner time. Independently blinded expert review, with held-out source conditions external to public GitHub, must score decision-relevant gap selection, retrieval precision/recall and false reads, source-grounded reasoning improvement, unjustified confidence, normal/boundary regressions, clinical P0/P1, and second-case transfer without reminders. Do not import the synthetic candidate labels as an answer key. Prefer no extra Skill if C does not beat B safely and consistently. No merge, production deploy, recurrence or self-certification authorized.


### Selective probe first-pass evidence packet (2026-10-29 follow-up)

A real or simulated `--execute-api` execution must preserve two different times: the *pre-run* `manifest.json` is intentionally immutable and stays `NOT_RUN`, while the *post-run* `run_receipt.json` records attempts, failed case-arm pairs, status, stage-level token totals when genuine Responses usage is present, and `owner_minutes=null` / `cost_usd=null` until independently measured. It must not rewrite the prior plan to conceal failures.

`attempt_events.jsonl` retains STARTED/COMPLETED/FAILED for each first-stage and conditional second-stage request. `first_pass_unscored.json` preserves the raw decision and initial-versus-final educational answer. `blind_reviewer_packet.json` contains anonymized case slots and answers, while `private_arm_mapping.json` is stored separately with restricted local permissions and **must never be sent to a reviewer**. This is blinding support, not verification that the reviewer remained blinded; receipt/response IDs are format-checked but do not authenticate the underlying provider or independent adjudicator. A failed call yields `HOLD_INCOMPLETE`, never a free success or retry.

The three case arms use a frozen balanced order (each arm begins one case) to reduce chronological-order artifacts; B and C still receive the same source catalog, but only C receives the Skill. Compare C versus B, not an unqualified A versus C headline. Strict limit: this public synthetic development pack cannot be an unseen benchmark. Exact provider billing usage, a protected clinical holdout and an independently blind first-pass review remain separate acceptance gates.

### 2026-10-29 OpenSkill-inspired minimal source policy (experimental)

Upstream reference: [OpenSkill `targeted_dr.py`](https://github.com/OpenLAIR/OpenSkill/blob/main/libs/openskill/targeted_dr.py), Apache-2.0. **Design adapted, no upstream source copied or new provider dependency installed.** The implementation stays inside the existing `selective_retrieval_probe.py`: only `missing_primary_evidence` can trigger a read, and only when the first-stage request identifies a concrete evidence question, a possible decision pivot and an allowlisted source. `missing_reasoning_bridge`, `missing_patient_fact` and `none` cannot become literature reads. Exact already-provided source bytes and previously retrieved source hashes are rejected. Each case still permits **at most one** synthetic source; the optional per-task retrieved-hash ledger prepares a future multi-hop caller without enabling any external search loop.

A denied `RETRIEVE` is retained as the model's **observed wrong triage**, not silently converted to a successful SKIP; reviewers must score false-read attempts and decision accuracy separately. The exact-substring source-presence safeguard is intentionally conservative: it does **not** infer medical equivalence from shared terminology, and neither hashes nor textual matches establish clinical source fidelity. Tests use mocks only, no paid API or hidden patient data.

### 2026-10-29 EVAL-003 cost-missingness correction

The prior review assembler sets `owner_minutes=null` when no validated owner-time receipt exists. The comparator formerly folded that unknown into a negative cost signal, making a positive development gain verdict impossible even if reviewer scores favored C over B. The revised report exposes `semantic_comparison` and `owner_cost_comparison` separately: **uncosted observed development gain**, **measured cost regression**, **measured non-worse gain**, and **no observed gain** are distinguishable. Safety, control and incomplete-run HOLDs retain priority. No output promotes a skill, authenticates reviewers or proves clinical autonomy. Absent owner time is still unknown, **not zero**; prospective independent owner-time measurement remains required.

### 2026-10-29: archived Stage1 B/C package generator (no inference)

`tools/prepare_staged_bc_packets.py` prepares only **worker input ZIP files** from an externally stored, pre-frozen, version-2 staging manifest and Stage1 ZIP. It verifies the SHA-256 of the complete private facilitator manifest, every Stage1 file (byte count and digest), and exact `.agents/skills/decision-question-triage/SKILL.md` bytes. It never reads Stage2, reviewer-only, or original case outcomes. For each selected case it creates a B ZIP containing `task.md` and `instructions.txt`, and an otherwise identical C ZIP that additionally contains `candidate_skill.md`; a separate facilitator-only manifest records hashes and **NOT_RUN**. Default small pilot selection is H01 and S01. Outputs must be outside this public repository, directories and ZIPs use restrictive permissions, existing outputs cannot be overwritten, and malformed/tampered archives fail closed.

Example in a **trusted local environment**, using copies of the previously frozen *private* material (not checked into GitHub):

```sh
python tools/prepare_staged_bc_packets.py \
  --stage1-zip /private/worker_stage1_only.zip \
  --manifest /private/facilitator/manifest.json \
  --skill .agents/skills/decision-question-triage/SKILL.md \
  --manifest-sha256 <approved-64-character-hex-manifest-digest> \
  --skill-sha256 <actual-64-character-hex-skill-digest> \
  --candidate-commit "$(git rev-parse HEAD)" \
  --output-dir /private/new-staged-bc-packets --cases H01 S01
```

**Critical boundaries:** preparing separate ZIPs does **not** establish separate model worker contexts; the entire shared output directory must never be mounted to either worker. Each ZIP must be supplied **individually** to a separately instantiated worker with equal model/version/effort/tool limits. B must have no access to C's Skill or reviewer material. This generator performs no API calls, enforces no OpenAI billing cap, never authenticates the claimed Git SHA, and cannot certify that workers read the provided source or skill. Subsequent Stage2 release still requires the existing private `stage_gate.py` to freeze an actual independent V1 decision, and blinded medical review remains mandatory. No public case text, reviewer rubric, or raw model output is committed with this code.

## 2026-10-29 first real-model pilot budget preflight (PENDING execution)

The original runner `tools/run_skill_transfer_pilot.py` has a genuine Responses API execution path, but **this public Draft PR's CI does not receive an API key and has not completed a paid medical or synthetic reasoning trial**. To respect the owner's US$10 overall research budget, the **synthetic 3-case / 3-arm subtrial** now preflights a conservative **US$0.50 maximum planning envelope** before any paid request is made.

The paid code path is fail-closed to **gpt-5-mini only**, the same nine distinct case×arm calls, `max_output_tokens=1100` per call, no retrieval tools, no conversation carryover and no implicit retry. Each request has a 200 KB serialized bound. A conservative input-token proxy of *two tokens per raw UTF-8 byte plus 4096 envelope tokens* per request, together with the full allowable output tokens, is priced at the officially published 2026-10-29 gpt-5-mini standard text rates, US$0.25/M input and US$2.00/M output. The total *estimated* ceiling must be at most US$0.50; model overrides, tool exposure, inflated max output, extra calls or excessive prompts cause an immediate HOLD. This intentionally overestimates expected cost and ignores prompt-cache discounts, not the reverse.

**This is not a guaranteed account hard spending cap.** Actual API billing can differ if provider fees or pricing change, and model IDs/usage receipts are not authenticated simply by local string matching. Before any real experiment, a separate dedicated OpenAI Project with owner-enforced spending controls must be confirmed; no public PR event may receive the key. The script's live-call allowlist remains exactly the fixed checked-in public synthetic fixture, authored HCM reading and Skill bytes, with an exact clean Git checkout requirement. Nothing in this cost gate authorizes sending official MedEinst narratives, patient cases, protected gold or licensed full texts to the model. It neither changes experimental outcomes nor constitutes a clinical claim.

**Execution remains BLOCKED in this chat environment:** no `OPENAI_API_KEY` exists here; the connected GitHub tool does not expose `workflow_dispatch`, and this branch is still Draft/HOLD. Do not insert credentials into chat or PR, merge merely to launch, enable schedule/automated approval, or claim calls were executed. The next real observation is one authorized, trusted, isolated pilot with a provider-authenticated run receipt and blinded independent first-pass review. If no safe private runtime is available, stop at the verified preflight rather than claiming learning.


## 2026-10-29 crash-safe first-pass trace (no provider calls in CI)

The candidate `run_skill_transfer_pilot.py` now **appends and fsyncs each completed or failed first-pass response** to `first_pass_journal.jsonl` before attempting another model request. This private, permission-restricted journal is retained even when the process terminates before all nine cases finish. The original `attempt_events.jsonl` still records STARTED and COMPLETED/FAILED per request. Neither journal nor review pack may be uploaded to public GitHub Actions artifacts or committed. Provider IDs and actual output text may be sensitive even for a simulated public case.

The exact nine-response `first_pass_results.json` and arm-blind `blind_reviewer_packet.json` are produced only after all attempts have returned to the orchestrator; the journal is **not** automatically resumed, retried, backfilled, published or promoted. A crash on call N can leave a paid, externally executed attempt with STARTED but no COMPLETED receipt. That case must be marked **unknown/missing**, and the suite must remain HOLD; rerunning the entire suite on the same saved output directory is prohibited. Human/agent reviewers can inspect the journal and separately reconstruct what happened, but may not claim unobserved responses existed.

For a genuine non-mock API run, the manifest sets `first_pass_journal_v1=true`. Before any review score, `assemble_skill_transfer_review.py` requires an intact permission-restricted journal with exactly nine rows and exact JSON-record identity to the frozen results. Missing, truncated, malformed, or post-hoc edited first-pass records fail closed. The unit tests deliberately simulate an abrupt third-call exception and subsequent tampering; these tests **never** spend API credits or verify independent clinical reasoning.

This protects recoverability and *local internal consistency*, **not provenance against a party able to edit the manifest and all local files**. A self-declared `resp_*` ID, locally saved journal, or string `RESPONSES_API` is not an independent provider attestation. For an actual claim of model ability, additionally require provider-verified API billing/traces, deliberately different worker contexts with checked model settings, a blind outside reviewer and a protected unfamiliar case pool. No auto-merge, schedule or medical publication is authorized by a green CI status.

## 2026-10-29 blinded-review allocation correction (public-seed leak)

The experimental runner originally shuffled cases using a deterministic digest of its **public** case-file bytes and shuffled the A/B/C candidate answers using a digest of the **public** case ID. A reviewer with the public repository and code could reconstruct the arm-to-answer positions from the allegedly blinded packet without seeing `private_arm_mapping.json`. That is unacceptable for an independent A/B/C experiment, regardless of whether test fixtures and review JSON are mechanically valid.

The new `blind_reviewer_packet.json` creation uses the operating system's cryptographic RNG for **two independent case/answer shuffles**, assigns each answer an opaque 128-bit random token, and keeps the only authoritative token→case/arm crosswalk in `private_arm_mapping.json` with restricted local file permissions. The original model-call scheduling remains deterministically frozen for reproducibility; the *reviewer assignment* alone is unpredictable. The same request suite now produces different reviewer slot tokens, independently checked by unit tests without model cost.

**Boundary of the claim:** Randomized arm labels do **not** prove a reviewer was independent or unaware of study design. A response can reveal which Skill instructions were received through its language, and a reviewer could have read confidential results or mapping elsewhere. Use an independently separated reviewer context, transfer only the reviewer packet, ask the reviewer to disclose attempted arm guesses before unblinding, and keep `independent_review_authenticated=false` until identity/process evidence exists. The experimental result cannot claim clinical Skill transfer merely because this privacy leak is repaired. Public GitHub and PR Actions must not receive complete reviewer packets, private mappings, API credentials or patient notes.
