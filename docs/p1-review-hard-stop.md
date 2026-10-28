# P0/P1 PR review hard stop — status + review receipt

**Scope:** merge eligibility for Clinical_system pull requests. This is a
private governance mechanism, not a public reader article. Canonical failure
event: [PR #171](https://github.com/sheng-web-OS/Clinical_system/pull/171)
published despite a known pre-merge P1 comment warning of 26 duplicated
exam identities; [Issue #133](https://github.com/sheng-web-OS/Clinical_system/issues/133)
is the existing incident ledger. Do not create another incident dashboard.

## Blocking and clearance

- A repository OWNER/MEMBER/COLLABORATOR may post `[P1_BLOCK] explanation`
  (or `[P0_BLOCK] explanation`) as a PR conversation, review, or inline
  comment. Existing #171 pre-merge P1-language is retained as a narrowly
  scoped legacy detector. The current PR HEAD receives a **failure** commit
  status with context `p1-review-hold`.
- Fixes alone, green CI, deployment, a positive AI self-assessment, or a
  different PR HEAD do **not** clear the original P1 comment. A separate
  trusted reviewer, **not the PR author**, must review the exact new HEAD
  and leave one explicit evidence-bearing clearance comment:
  `[P1_RESOLVED source=issue id=6442587535 head=<40-char-HEAD-SHA> evidence=https://github.com/...]`
  Use `source=review` or `source=inline` for those kinds of comments.
  Replace ID and SHA with the actual blocker ID and current Git HEAD.
  An independent AI paragraph review is not a human physician sign-off;
  medical P1 may require separate clinician approval.
- Before scanning comments the workflow marks the current SHA **pending**;
  GitHub API failures must never be interpreted as a new pass. When comments
  change, GitHub Actions recalculates the status on the PR HEAD rather
  than on the default branch.
- A warning merely described in a PR body or off-repository discussion is
  not automatically known to this gate. Reviewers must put the P1 blocker
  in the PR discussion. This is a signal/acknowledgment protocol, **not**
  automated medical review or a proof of reviewer independence beyond
  distinct GitHub accounts and recorded provenance.

## Required GitHub configuration (separate administrative operation)

This workflow does **not** on its own prevent merges. After independent CI
verification and separately approved merge of the engineering PR, configure
the `main` branch ruleset:

1. Require successful status check `p1-review-hold` (GitHub Actions as
   expected source) and the existing medical-site CI check.
2. Apply the ruleset to administrators / disallow bypass where available;
   require review conversations to be resolved and restrict force pushes.
3. Prove red→blocked, exact-HEAD independent clearance→green, stale-clearance
   →blocked, new comment after an earlier green→blocked, and comments API
   outage→pending/blocked. Verify actual merge controls, not just job output.

**Residual limitation:** Only repository reviewers/signals GitHub actually
delivers can be detected. Deleting P1 evidence, administrative override,
unprotected rulesets, and reviewers using the same account as an agent are
not cryptographically prevented by this PR. For higher assurance, require
independent reviewer identity, preserve P1 incidents in existing Issue #133
and use protected review history/rulesets. Do not report this as an
unbypassable hard stop until the ruleset is proven with a real blocked merge.

## Reversal

Remove the required status-check rule **only with explicit release-authority
approval**, then revert this engineering PR's workflow, tests, and tool.
No frozen editorial baseline, medical article, public HTML, or production
artifact is touched by this proposal.
