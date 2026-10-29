# Synthetic Drive source retrieval fixture

Status: CROSS_CONNECTOR_SMOKE_TEST_ONLY (not autonomous / not clinical / not published)
Date: 2026-10-29

A synthetic Google Doc was created and read through the connected Google Drive integration. Its test-only figure caption was verified: **"Sample size: 12 synthetic observations; no clinical inference permitted."**

Expected autonomous reasoning (NOT YET TESTED):
- When original source is necessary and absent locally, select READ, retrieve narrowly, and preserve provenance.
- When existing GitHub evidence is complete, select SKIP without touching Drive.
- If a source is sensitive or authorization is uncertain, select HOLD.
- Never copy real private Google Drive content into public PRs, logs, CI artifacts or published pages.

Scope:
- This file is synthetic, contains no patient records, no copyrighted source material or API credentials.
- Demonstrates a manual ChatGPT connector-to-GitHub data flow ONLY.
- GitHub Actions does NOT yet have Google Drive credentials, WIF configuration, an autonomous model decision runtime, or Google Drive API connectivity.
- Existing PR #159 is the independent, preregistered autonomy-evaluation framework; do not count this smoke test toward U001.
- No publication or merging is authorized from this fixture.
