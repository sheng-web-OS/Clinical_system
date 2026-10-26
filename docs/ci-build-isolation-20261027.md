# CI build isolation and publication contract

Status: **Engineering Draft / NOT medical, visual, copyright or publication approval.**

## Purpose

The October 26 failures had two independent sources: an old intake parser rejecting archived source snapshots, and temporary remote ECG delivery failures blocking full static builds of unrelated PRs. The parser has already been fixed in main. PR #89 has already shipped the verified Silverman ECG cache. This proposal makes only one additional, conservative CI optimization.

## Required for every pull request

1. Run the entire unit/regression test suite.
2. Validate the publication manifest, public source links and source Figure/Table gate using tools/validate.py.
3. Validate the live original/snapshot intake ledger using tools/check_corpus_inventory.py.

Only a PR whose *entire* changed path set is inside archive/xiaoma-reading/intake/ may skip a redundant full static-site build and its output artifact. The classifier must read the exact merge-result diff against the triggering PR base SHA, with NUL-delimited filenames. Empty or ambiguous diffs, missing base commits and classification errors MUST fail closed or require full build.

Main pushes and workflow_dispatch always build and verify the entire site. Any change to content/, site/, audit/, tests/, tools/, docs/, GitHub Actions, or an unknown path also requires full build.

## Release boundaries preserved

- Source snapshots are private archival evidence, not author canonical originals and not a publication authorization.
- Public teaching content must still pass the existing source and Figure Gate contracts and a full build.
- No change is made to site/pages.json or Cloudflare deployment configuration.
- ECG source identity, sha256, dimensions and fail-closed checks are never bypassed.
- Unit tests and successful builds do not independently certify image readability, clinical accuracy, source rights or a matching Cloudflare production deployment.
- A Draft/HOLD PR remains Draft/HOLD. This proposal does not approve merging or publishing.

## Acceptance and adversarial checks

- Private-intake-only PR: full tests, source validation and corpus inventory pass; no redundant site build artifact is expected.
- Mixed private/public, Figure Gate, visual QA, workflow or unknown changes: full build and artifact are required.
- Empty and malformed diffs are fail-closed; Unicode paths are parsed without newline splitting.
- Main and manual run: full site build and output validation always required.
- Production deploy SHA, actual HTTPS content, mobile screenshots and medical peer review are separate release evidence.

## Scope decision

Do not introduce a second release manifest, background service, permanent agent, blanket visual approval or any auto-merge action. Wider path-based optimization requires separate evidence and explicit review.
