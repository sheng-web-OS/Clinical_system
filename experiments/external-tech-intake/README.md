# External technology intake | evidence-first experimental gate

**Status: isolated experimental policy, NOT a deployed upload portal or autonomous integration service.** This no-network, stdlib-only CLI and its tests cannot authenticate reviewers, prove provenance, scan ZIP contents for secrets/malware, execute candidates, create PRs, merge or publish. No real external handoff has been received or evaluated.

## Objective and trust boundaries

A colleague's algorithm, repo, tool or prompt is a **candidate**, not trusted instructions or evidence of improvement. Compare it with the strongest native-model/evidence-only/current Clinical OS baselines, using equivalent model, effort, tools, sources and budgets. Financial backtest performance is NOT direct proof that a method works for task/knowledge/compute/risk allocation; cross-domain transfer requires new experiments.

The repository sheng-web-OS/Clinical_system is PUBLIC: branches, draft PRs, Issues, Actions logs and artifacts do not protect secrets. **Never upload peer ZIPs, unpublished IP, restricted research, personal information, credentials, private clinical records, proprietary datasets, hidden answer keys or independent reviewer packets here.** Only sanitized, cleared protocols, synthetic regression fixtures and non-sensitive metadata belong in this repo. A private, access-controlled, audited inbox is not yet implemented.

Trust sequence:

1. **Receive privately**: freeze external package bytes and SHA-256, source URL and immutable source commit; treat all external README/AGENTS, model content, workflows and setup scripts as untrusted *data*, never instructions.
2. **Offline ZIP preflight**: detect path traversal, duplicate/case-colliding entries, symlinks, encrypted entries, suspect secret filenames, decompression bombs and oversized archives without extraction. METADATA_PREFLIGHT_ONLY is **not** contents scanning or privacy/malware clearance.
3. **Independent audit**: check actual license/rights, origin, provenance, SBOM/dependency integrity, privacy and security outside the external package's claims; independently compare actual package SHA-256 to the manifest. Only a separately authorized, credential-free, no-egress sandbox may ever execute candidate code.
4. **Preregistered independent evaluation**: freeze hypotheses, scoring rubric, cost unit, sample, held-out split, risk criteria and stop rules BEFORE results. Run native vs current system vs candidate on matched fresh tasks across multiple periods/domains; use separate reviewers and independent execution/run identities, no shared hidden answers or contaminated contexts.
5. **Advisory decision**: fail closed on unsafe/missing rights/evidence; otherwise recommend reversible shadow trial or rejection/retirement. **The CLI never installs, integrates, modifies files, pauses jobs or deploys anything.**
6. **Recheck**: version/license/security changes, stronger baseline, drift, new failures, expiry and cost escalation trigger renewed evaluation; existing adopted shadow trials may be recommended for pause or retirement.

## Decision contract

| State | Permitted effect |
| --- | --- |
| QUARANTINE | Stop; unsafe archive, invalid artifact identity or rights/security pending. |
| HOLD_INVALID / HOLD_RISK / HOLD_EVIDENCE / HOLD_EXPIRED | No adoption; resolve specific blocker or abandon. |
| METADATA_PREFLIGHT_ONLY | ZIP structural metadata passed; NOT content clearance. |
| READY_FOR_ISOLATED_EVALUATION | Benchmark may be planned, NOT permission to execute code. |
| ADOPT_SHADOW_CANDIDATE | Advisory low-risk, reversible shadow candidate; NOT actual adoption, merge or publication. |
| CONTINUE_SHADOW | Advisory continuation until next checkpoint. |
| REJECT | Safety regression or preregistered net benefit/cost goal not satisfied. |
| PAUSE_SHADOW | Existing shadow candidate has expired evidence or major safety regression. |
| RETIRE_SHADOW | Existing shadow candidate fails preregistered value criteria; propose scoped removal. |

The evaluator and reviewer IDs are declarations, NOT authenticated identities. SHA-256 binds bytes, not trusted origin; preregistration/review hashes are references, not proof of chronology or independent attestation. These must be checked by a separate trusted reviewer/receipt store. Stronger provenance assurance can follow SLSA; OpenSSF Scorecard signals cannot certify safety.

## Offline usage on access-controlled machines

    python experiments/external-tech-intake/gate.py preflight /private/inbox/handoff.zip
    python experiments/external-tech-intake/gate.py decide /private/inbox/manifest.json
    python experiments/external-tech-intake/gate.py decide /private/inbox/manifest.json --receipt /trusted/evaluation/receipt.json
    python -m unittest tests/test_external_tech_intake.py -v

The decision command does not hash or open the ZIP. The submitter cannot be allowed to provide a forged trusted-side evaluation as proof of clearance.

Minimum manifest declarations: candidate_id, artifact_sha256, source_url (HTTPS), source_commit (immutable SHA), license_status VERIFIED, privacy_status PUBLIC_CLEARED, risk_tier low, reversible true. Optional current_state SHADOW_ADOPTED. A real private candidate requires a separately defined private trust boundary; do not falsely claim PUBLIC_CLEARED.

Trusted-side receipt: candidate_id and artifact_sha256; prereg_sha256 and review_sha256; distinct evaluator_id and reviewer_id; security_review PASS and rights_review PASS; expires_on; minimum_cases, minimum_domains, minimum_periods, minimum_mean_gain and maximum_cost_ratio set before results; paired case IDs, domain, period, unseen_holdout split, normalized baseline_score/candidate_score (0..1), positive baseline_cost, candidate_cost and severe_regression boolean.

The code checks consistency and computed *paired* gain and cost ratios, not whether the numeric scores are scientific, blinded, independently reviewed or statistically powered. Severe safety regressions override positive means. Human labor, maintenance, actual model costs and clinical safety are separate dimensions and MUST be independently measured when applicable. Current tests use synthetic data; they are not evidence of technology improvement.

## Continuous operation: adopt existing orchestration, avoid platform sprawl

**Implemented in this Draft PR:** metadata-only ZIP preflight, deterministic fail-closed advisory evaluator, regression tests. Real submission remains unavailable; no automatic intake or shadow deployment.

**Next gated task:** implement a restricted off-repository inbox with explicit access grants, retention, threat scan, content/license review and trustworthy source provenance; use the colleague's first *real* sample for a preregistered fresh-context comparison.

**Then only after independent QA:** existing GitHub engineering/Writer schedule can select the next sanitized external-intake Issue on its normal wake; check exact HEAD and owner lease, work one bounded candidate, update the existing checkpoint, and avoid parallel conflicting changes. Do not create a sixth schedule, touch ongoing 72h experiment or infer GitHub-to-Work event wake from issue/CI activity; event trial #240 is inconclusive. No new dispatch or production/medical authority is granted here.

**At expiry or incident:** trigger comparison again, recommend PAUSE/RETIRE with precise reasons. Real changes require branch, owner, HEAD/CAS, rollback and independent QA; medical/editorial/publishing gates remain separate. Existing experiments/README.md, AGENTS.md, Issue #133 failure ledger and #137 attention/quality measurements remain authoritative. If owner attention or maintenance cost outweighs benefit, discontinue this intake layer.

## First acceptance/falsification

- Hostile ZIP metadata, rights, hash, duplicate heldout case, distinct-reviewer declaration, severe regression, drift/expiry and cost thresholds pass local and CI negative tests.
- First real package must demonstrate actual private transfer and separation, security/rights validation, frozen and independent baseline-versus-candidate evaluation, measured gain *and* human-cost data. Until then effectiveness NOT_VERIFIED, real sandbox NOT_IMPLEMENTED, real user minutes NOT_MEASURED, and adoption NOT_AUTHORIZED.
- Source guidance: https://openssf.org/projects/scorecard/ ; https://slsa.dev/spec/v1.0/provenance ; and ../README.md for current Clinical OS benchmark policy.
