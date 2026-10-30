# Case Examiner: prospective private holdout boundary (Draft / HOLD)

**Purpose:** test whether existing decision-question triage capabilities generalize to previously unavailable clinical cases, without exposing case answers to the candidate worker, a prior ChatGPT conversation, or the **PUBLIC** Clinical_system repository. This is a minimal offline Stage1 adapter for existing PR #225; PR #236 handles published MedEinst separately. No second agent framework, registry, scheduler, self-grader, or model runtime.

## The trust boundary, not a metaphor

- **Examiner/facilitator (trusted human-controlled environment):** has authorized, adequately de-identified cases, locked source versions, expert adjudication criteria and answer keys. These must **not** be supplied in the current ChatGPT conversation, GitHub branches/Issues/PRs/Actions/artifacts, or a repository-accessible Drive folder. Distinct folder permissions are not sufficient if worker and examiner execute under the same user identity. Use separate access-controlled identities/runtimes and authenticate that the candidate cannot read examiner or gold storage before any live clinical benchmark.
- **Case Stage1 (examiner-only):** the offline tool seals a neutral case-only ZIP plus #225-compatible version-2 manifest. Stage1 contains all cases, so it MUST NEVER be mounted into a worker. It is strictly a trusted packaging intermediate.
- **Worker:** sees only one selected neutral case prompt and its arm-specific permitted inputs. A=Native, B=Native+retrieval pack, C=Native+identical retrieval pack+candidate Skill. Distribute one #225 worker envelope to one fresh isolated context. The worker never receives the source role, correct response, gold, identity mapping, sibling cases, previous tries or reviewer judgments. Do not rely only on self-reported arm exposure; record actual runtime inventory/trace and attested access controls.
- **Independent reviewer:** receives first-pass output with anonymous answer slots and permitted source evidence, not arm names or expected winner. A medically qualified reviewer adjudicates correctness, competing explanations, discriminating evidence, appropriate retrieval, normal/boundary false alarms and P0/P1 risk. Review context and worker context must differ. Independent clinical expertise and blindness are not established by a string identifier.
- **Facilitator:** after first answers and review are frozen, performs arm unblinding and score assembly through the existing #225 evaluator. Keys never flow back to candidate Skill or a training context until the trial is explicitly retired from unseen status.

## What is implemented by this PR

tools/seal_private_case_exam.py is an offline case/gold integrity and packaging step. Inputs are two separately protected JSON files with SHA-256 values frozen before benchmark execution. A source class is claimed, not medically/privacy verified. The tool checks nonoverlapping case and gold IDs, one transfer, normal and boundary control at minimum, per-case byte bounds, allowed case schema, distinct private output parent folders, new-only outputs, symlinks, and input/output paths outside public Git. It assigns random anonymized Stage1 H01.md etc., records gold/role/original-ID mappings only under a separate facilitator root, and exposes source/manifest hashes without printing narrative or gold. No external credentials, model calls, reviewer calls or grading.

Cases schema, in a private file (example uses fictional text only):

~~~json
{"schema_version":1,"source_class":"synthetic","cases":[
 {"id":"new-case-01","role":"transfer","task":"Fictional scenario of 20+ bytes ..."},
 {"id":"new-case-02","role":"normal","task":"A normal fictional scenario of 20+ bytes ..."},
 {"id":"new-case-03","role":"boundary","task":"A boundary fictional scenario of 20+ bytes ..."}
]}
~~~

Gold schema, in a different protected file (strictly private):

~~~json
{"schema_version":1,"keys":[
 {"id":"new-case-01","expected_decision":"RETRIEVE","clinical_rationale":"Fictional expert key"},
 {"id":"new-case-02","expected_decision":"SKIP","clinical_rationale":"Fictional expert key"},
 {"id":"new-case-03","expected_decision":"HOLD","clinical_rationale":"Fictional expert key"}
]}
~~~

No patient data, hidden key, or real cases should be checked in. For real cases, even sufficient text de-identification and use authorization are external manual gates; the flag authorized_deidentified does not prove them. Expert key development must be independent, source-grounded and account for uncertainty instead of inventing a single diagnosis as automatic truth.

Example in an owner-controlled, non-public examiner runtime (NOT GitHub Actions):

~~~sh
python tools/seal_private_case_exam.py \
  --cases-file /trusted/private/cases.json \
  --gold-file /trusted/gold/gold.json \
  --cases-sha256 <pre-registered-sha-of-cases> \
  --gold-sha256 <pre-registered-sha-of-gold> \
  --suite-id prospectively-frozen-suite-001 \
  --stage1-root /trusted/stage1/new-run \
  --key-root /trusted/facilitator/new-run
~~~

Both parent directories must exist and have an appropriate non-world-writable parent. Target directories must not exist. Files are created 0600 / directories 0700. This is only one filesystem safeguard, not proof of different-user isolation; actual runtime and ACL verification remain a HARD HOLD. Command does not print contents, just a status receipt. Never mount /trusted/stage1 into the model runner; copy out individual case/arm envelopes through the existing #225 packet preparation process. The #225 Stage1 builder currently selects at most five case IDs per invocation; larger suites must be processed in predeclared batches without exposing sibling cases to a worker.

## Validity before promotion

1. **Pre-registration:** seal clinical sources, selection, candidate Skill commit, retrieval pack SHA, matched model/effort/tool budgets and the reviewer protocol before starting inference. Digest alone does not certify the date of sealing or absence from model pretraining.
2. **Secure storage:** independently verify case/answer key placement, IAM/ACLs, runner isolation, retrieval and logs, backups and retention. Current public repo is emphatically not the secure store.
3. **Hidden test:** holdout vignettes must not appear in prior conversations, public benchmarks, training instructions, Skill examples or retrieval indexes accessible to the tested worker. Public MedEinst is useful for engineering tests but not a contamination-proof final holdout.
4. **A/B/C first pass:** execute separate immutable environments; one response per case-arm; no shared answer history; first responses frozen and failures included; matched costs captured. Unseen case supplies only the case facts and permissible common primary source access. Explicit retrieved article pack identical for B/C.
5. **Independent adjudication:** evaluate major omission, unsafe action, normal/boundary over-triggering, evidence retrieval benefit and decision pivots; record disagreement and owner attention. Case content is never scored automatically from keyword labels.
6. **Stop conditions:** any clinical P0/P1, leakage, prior-case exposure, unauthorized private material, reviewer contamination, unproved independence, cost overrun or attribution ambiguity -> HOLD / NOT_VERIFIED. No automatic publication, merger, paid inference or Skill promotion.

## Trial relationship and experimental validity

- This user-requested PR is OWNER-NUDGED, outside the fixed work cohort in Issue #137's 2026-10-29 to 2026-11-01 72-hour unattended-agent trial. It does not count as independent agent initiative and must not retroactively change that trial's scoring.
- Existing #225 is the comparison owner, #224 the counterfactual diagnostic owner and #236 the MedEinst source adapter. This PR adds only a private owner-provided-case sealing handoff; do not overwrite their active work.
- Local synthetic mechanical tests are not independent medical verification, actual isolated execution, validated unseen transfer, API cost improvement, or owner-time savings. Keep this PR Draft/HOLD until source, security and independent reviewer gates have evidence.

## 2026-10-30 owner-directed hardening: independent identity and selective skill use

**Implementation status:** the existing writer-owned #237 branch now rejects a false `--repo-root` in the production CLI, always protects the checkout containing its code (even through the importable test seam), canonicalizes private input paths including symlinked parents, and refuses group/world-writable output parents. These changes need **new exact-HEAD CI and independent security review**; they are NOT evidence of an independent principal, authenticated examiner, secure cloud boundary, or live blind trial. The security review of previous RED findings remains open until new-HEAD negative tests are reviewed. Do not use with actual restricted records yet.

### Required actual runtime roles (separate identities, not only folders)

| Principal | Permitted | Must be denied |
|---|---|---|
| **E — examiner** | Generate genuinely new case-only packets, retain original source and rubric/gold in private examiner-owned storage, preregister and seal the challenge | Write to public repository, expose gold to worker context, grant worker storage or key access |
| **W — worker** | Read **one** Stage1 task and arm-specific authorized article/Skill bytes; submit immutable first answer and narrow execution traces | List sibling cases, read gold/rubric, use examiner/GitHub admin/Drive-wide credentials, load prior evaluation answers or reviewer context |
| **R — blind reviewer** | Review anonymized first answers plus separately permitted authoritative source excerpts; assess quality, correct action and safety | Inspect arm allocation, worker private traces, predeclared gold or preferred winner before freezing review |
| **F — facilitator** | Hold private mappings, verify signatures/attempt receipts, unblind **after** first-pass and blind review freeze, calculate B/C differences | Supply gold to worker, silently modify locked suite/attempts or impersonate R as W |

**Use independently scoped service principals** with revocable, short-lived credentials, separate storage policies and distinct audit logs; the current connected GitHub identity is an admin of the public repository and cannot serve as an independent examiner credential merely by opening a private branch or creating a different ChatGPT conversation. GitHub Actions secrets, environment approvals and `chmod 0600` are not a satisfactory boundary when a shared principal can alter the job or read the same storage. Public CI is for synthetic negative tests only. The owner or a separate trusted operator must provision and attest E/R/F IAM in a system to which W (including any connected tools used by the worker) has **no access**. Do not paste cases, keys, source paths identifying private subjects, private provider logs or reviewer rubrics into conversations, public GitHub, connected shared Drive folders, or public Actions.

**Before first real attempt**, perform and archive a private least-privilege verification receipt:
1. Inventory identities, actual credentials, accessible connected tools, mount points, environment variables, browser/retrieval indexes, prior agent memories and logs. Record pinned worker runtime image/model/config and exact frozen code/Skill/source hashes, with case originals and gold remaining in E/F storage.
2. Authenticate as **W**, not as an admin impersonating W; attempt to list/read the examiner case set, gold, sibling answers, reviewer namespace, archives, shared Drive aliases, git refs/branches and log/artifact backups. Every protected read must be independently observed as **DENIED**. Repeat with indirect retrieval/search. Missing audit evidence = `ISOLATION_NOT_VERIFIED`; any success = `LEAKAGE_HOLD`.
3. Authenticate as **E** and **R** independently; record that E can seal and R can read only the intended neutral reviewer packet. Reviewer-visible metadata must contain no `source_exposed`, public-seed deterministic allocation, original role label or arm-specific source gate. Resolve the separate #225 blind-packet findings on a new exact head before clinical use.
4. Verify actual executor provenance and one-case-per-worker delivery; forbid a whole suite ZIP, a previous model session, prior-response links or shared conversation state. Freeze and time-anchor the private pre-registration under a facility outside W access. SHA-256 alone is not independent time certification and hashes of guessable keys should not be published.
5. Give E (not the present assistant or shared GitHub executor) control of the irreversible `RUN` authorization **only after** access-denial probes, examiner security review, frozen source/answer provenance, external budget approval and blind R availability. If a gate is unknown, do not invoke any model. A zero-risk or mathematically impossible leak guarantee cannot be made; instead require an explicit threat model, independently verifiable isolation and stop-on-exposure.

### Selective skill-use contract — different from deciding to retrieve

The private gold may now **optionally** contain `expected_skill_action` (`USE|SKIP|HOLD`) and `skill_action_rationale` for *every* case, in addition to legacy `expected_decision` (source retrieval) and `clinical_rationale`. If any new label is present, all cases must have both fields and the sealed suite must contain all three controls: USE, SKIP and HOLD. Labels live only in `facilitator_key.json`; the worker ZIP, Stage1 manifest and public result reveal none. These are **prospectively proposed expert decisions**, not a reliable machine-scored ground truth or proof that applying a Skill actually helps.

Do **not** hand the worker a USE/SKIP/HOLD menu tagged to the preferred answer or name the expected Skill in the task. It must independently determine whether any available Skill contributes, whether ordinary reasoning is sufficient, and whether evidence/permissions force a hold. These three actions are distinct from `RETRIEVE|SKIP|HOLD` for source reads. A Skill's mere presence in C's prompt, a self-reported `skill_applied`, or a reviewer-visible implementation flag is not proof of correct selection.

For novel-domain performance, preregister both **eligible cross-domain analogies** (a generalizable decision-question triage mechanism can help) and **out-of-scope negative controls** (a medicine-specific Skill must be declined for an unrelated glossary or engineering task). Domain families, near-duplicate question families and linked source families must be disjoint from public development fixtures and the worker's previous exposures. Preserve a separate domain-specific source-grounded expert adjudication; do not transfer clinical recommendations to engineering or finance. If there is only one medicine-specific candidate Skill, successful *skipping* in genuinely inapplicable domains is meaningful; claiming positive cross-domain Skill **use** needs a prospectively defined legitimately transferable mechanism, not an invented application.

### First blind comparison / interpretation (NOT AUTHORIZED OR RUN)

- Primary causal contrast: **B** = native model + the same permitted retrieval; **C** = B + candidate Skill, with optional use. **A** = native model without the additional pack, a descriptive contextual baseline rather than equal-retrieval choice proof. Match model version, effort, available tools, limits, task text, relevant evidence and first-pass capture; separate each arm/case context, randomize order without revealing mapping, and record actual credentialed execution receipts.
- Score independently: domain-aware answer quality and decision pivots, correct Skill USE / SKIP / HOLD **versus preregistered reasons**, selective-use false activation, missed beneficial use, unsafe consequences, unhelpful retrieval, tokens/paid cost, owner interventions and reviewer uncertainty. Compare C against B and also against an **always-use** and **never-use** selection rule as diagnostic baselines. A first-pass answer that never required the Skill can be excellent: do not punish it merely for correctly skipping.
- **Skill survives** only if positive quality-adjusted benefit on truly unseen eligible tasks exceeds B, ineligible/normal control false alarms and P0/P1 do not regress, actual expenses and owner time are acceptable, and a separately isolated replication confirms the effect. Equal performance at higher cost favors **retirement**; harmful or overgeneralized use = **REJECT/HOLD**. All model/model-reported identities and self-rated confidence remain unauthenticated until external execution evidence is checked.
- Original #137 72-hour autonomy study ends **2026-11-01 06:20:15 UTC**. This repair and any future owner-instructed exam design are **OWNER_DIRECTED, excluded** from that cohort; do not edit #225/#224/#234/#235, alter its denominator, start paid calls, auto-merge or publish.

**Ready status is not implied by a green test suite.** Exact-head security review, real E/W/R/F IAM attestation, private case authorship, holdout nonexposure, #225 blind-assembler repair, and independent clinical/source review remain `HOLD`. No restricted cases, secrets or model answers have been transferred by this document.
