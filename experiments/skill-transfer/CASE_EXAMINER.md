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
