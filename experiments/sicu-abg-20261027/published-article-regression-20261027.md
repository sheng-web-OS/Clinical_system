# Published CTICU 01 production regression — 2026-10-27 Asia/Taipei

Scope: existing **published** CABG lactate/ScvO₂ article from merged PR #72, independent of the **unpublished** oxygen-delivery V1/V2 drafts in this PR.

- GitHub `main` observed at `a0c9a18e987aa11f02106508b07485c28570306b`.
- Cloudflare Pages project `sheng-clinical-system`, production deploy at `2026-10-27T00:42:47Z` (08:42:47 Asia/Taipei), commit **a0c9a18e987aa11f02106508b07485c28570306b**, stage **deploy: success**.
- Browser live HTTPS: https://sheng-clinical-system.pages.dev/xiaoma-20261027-cticu-abg-cabg-lactate . Page title loads, article content and in-page source section present.
- Browser read-only visual check (TinyFish run `f08e2e31-0efe-4d8b-9eec-745635f26efb`): **Figure 1** four observation layers HTML div diagram rendered; **Figure 2** CABG lactate/BE/ScvO₂ SVG rendered; captions visible; no horizontal overflow at mobile viewport; in-page provenance anchor `#part-8` opens with references.
- Browser check `a139aa97-dc28-40a8-be63-6bc33a246e12`: title and linked source-page URL detected in DOM, but it did not independently open every external citation.
- **Limitations:** Browser result is automated visual inspection, not a medical or accessibility audit. Individual external links and source page separate HTTPS route were not all individually tested in this run. The published article has previously documented Figure Gate; do not conflate this browser check with independent physician review.
- **Regression outcome:** no new visible layout/figure failure found in the checked production article. Do not modify its publication manifest as part of draft 02.

No user action requested; the second article remains **HOLD**.