# Intake #66–#69 → single release gate (2026-10-27, HOLD)

**Decision:** Do not release, merge as publication, add `site/pages.json` entries, or deploy any of the four articles on the basis of this audit. Preserve the source / audit history and discontinue development on superseded intake branches. This file is an **engineering and source-reconciliation record**, not an independent physician sign-off or publication approval.

## 0. Evidence hierarchy and authoritative surfaces

- **Source preservation**: `archive/xiaoma-reading/intake/*-user-supplied.md` contains conversation-supplied historical manuscript snapshots; it must not be silently revised or promoted to Facebook-canonical author originals.
- **Existing review**: individual Figure/medical audits linked below were incorporated into current `main`; their medical assertions are provisional until independently reviewed.
- **Publication registry**: `site/pages.json` is the public allowlist. It contains no registration under cholestasis, infiltrative pattern, chronic diarrhea or cirrhosis for these candidates at this audit; no deployed status is inferred.
- **Single existing intake inventory**: `archive/xiaoma-reading/intake/2026-10-21-chat-manuscripts.md`; current `main` records the 21 historical manuscripts as 6 imported, 11 private source snapshots, 4 conversation-only. Do not create a second intake list.
- **Site build**: main's later `audit/intake-reading-publication-20261026.md` records the `source_snapshot_archived` parser fix and passing 68 unit tests, inventory and local build. These tests apply to the tested main state, **not** to uncreated public manuscripts in these four topics.
- **Rights boundary**: the Pocket Medicine screenshots were privately reviewed; neither permission to mirror the textbook figures publicly nor right to reproduce layouts at scale is established. Prefer precise textbook citation + independently authored causal/decision figures; obtaining rights or a documented applicable exception is required for any original-pixel public reproduction.

## 1. Redundancy verified: old PR content already present on main

The original and audit blobs from four PR head commits were compared to current `main` and matched exactly (Git blob SHAs, not just file names). All four PRs are still open/draft at the time of reconciliation and have three files each (original, audit, shared ledger). Their edits to the ledger reflect older branch-local counts and **must not overwrite main's newer 6/11/4 inventory**.

| Intake PR | Author snapshot (unchanged on main) | Figure / medical review (unchanged on main) | Status |
|---|---|---|---|
| [#66](https://github.com/sheng-web-OS/Clinical_system/pull/66) Cholestasis | `archive/xiaoma-reading/intake/2026-07-19-cholestasis-primary-secondary-user-supplied.md` — `b7a650d643bde09efb9a802f3793f9221c5f23cd` | `audit/cholestasis-20260719-pocket9e-figure3-3.md` — `5e0046077252da386f239d06139085f3234ce889` | source archived; public HOLD |
| [#67](https://github.com/sheng-web-OS/Clinical_system/pull/67) Infiltrative ALP | `archive/xiaoma-reading/intake/2026-07-19-infiltrative-pattern-user-supplied.md` — `30cf09dc32c1ddbc435ac3dede76098efacb6ac1` | `archive/xiaoma-reading/intake/2026-07-19-infiltrative-pattern-review.md` — `513bb5cde537d87f5ce5fc02297a67c26e080bb1` | source archived; public HOLD |
| [#68](https://github.com/sheng-web-OS/Clinical_system/pull/68) Chronic diarrhea | `archive/xiaoma-reading/intake/2026-07-21-chronic-diarrhea-user-supplied.md` — `d9c321974d2655de734660094857050afa4cfa01` | `audit/chronic-diarrhea-2026-10-26-source-and-clinical-review.md` — `0c2ab812a49ff95bf64fb8a6461d996cb8b6e6fd` | source archived; public HOLD |
| [#69](https://github.com/sheng-web-OS/Clinical_system/pull/69) Cirrhosis | `archive/xiaoma-reading/intake/2026-07-23-cirrhosis-user-supplied.md` — `1cb6370912ca7a6ce91530d58a90f7a0f5b7b1fc` | `archive/xiaoma-reading/intake/2026-07-23-cirrhosis-figure-review.md` — `0f56bfae509b86944ac71a5547ece31f7048e724` | source archived; public HOLD |

**Do not redo:** raw manuscript intake, snapshot transcription, already cited initial guideline reviews, or the earlier CI-inventory mismatch fix. Avoid re-merging the stale shared ledger.

## 2. New source-page recovery (2026-10-27, partial → materially advanced)

A Library-held item titled *Pocket Medicine: The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition* (file display title: `內科_Pocket Medicine The Massachusetts General Hospital Handbook of Internal Medicine, 9th Edition_625A_Flatten(1).pdf`) was **directly read and page images inspected**. The readable Library copy reports **463 PDF pages**. This copy has **not** been byte-hash matched with the earlier repository audit's cited **464-page / SHA256 ad283f7db19b6575775341972360a5ca1e5b40f51383ce02d9c11c8d21a0b3c5** source: raw-byte materialization failed. Therefore, do **not** assume they are identical editions/files or promote all source-fingerprint gates to PASS. Printed textbook page labels and errata remain to be independently established.

PDF page indices below are **1-based viewer pages in this Library copy**, NOT confirmed printed textbook page labels:

| Topic | PDF pages physically examined | Figure / textual evidence recovered | Status |
|---|---|---|---|
| Chronic diarrhea #68 | **124–126** | Chronic diarrhea starts p.124; p.125 lists functional, malabsorption/maldigestion, inflammatory and introduces **Figure 3-2**; **Figure 3-2 decision-flow image is on p.126**. Main branch of figure: fecal fat or inflammatory markers first; stool osmotic gap only after that; book's visual threshold is **<100 vs ≥100** (book algorithm, not exclusive current clinical rule). | Visual layout and proximal text verified in Library copy; print page/cross-version fingerprint pending |
| Cholestasis #66 | **137–139** | Laboratory definitions / liver origin of ALP p.137; injury and differential context p.138; **Figure 3-3** image on **p.139**, showing RUQ ultrasound duct dilation branch and nondilated biliary epithelial / intrahepatic hypotheses. | Visual layout verified; print page/cross-version fingerprint pending |
| Infiltrative ALP #67 | **137–139** | Pattern table / ALP sources p.137; **Figure 3-4** on **p.139**, with malignancy, granulomas, abscesses, medications/amyloid, investigations and an explicitly limited `SPEP to r/o amyloid` line. | Visual layout verified; print page/cross-version fingerprint pending |
| Cirrhosis #69 | **145–147** | `CIRRHOSIS` heading starts p.145; **definition, etiologies, exam, labs and workup on p.146**; Child–Pugh/MELD prognostic context extends onto **p.147**. The cross-referenced **Child–Pugh Appendix scoring table has not been located/visually checked**. | Chapter body verified; Appendix and print page pending |

**Important editorial correction:** `Figure 3-2` is located visually on **PDF page 126**, although the figure title appears near the bottom of page 125. Do not fabricate a one-page location from the title alone.

No original textbook figure pixels are committed or cleared for public site display by this audit.

## 3. Unified release gate — evidence, agent capability, external dependency

| Gate | #66 | #67 | #68 | #69 | Responsibility / next action |
|---|---|---|---|---|---|
| S0 immutable conversation snapshot | PASS | PASS | PASS | PASS | **No further work.** Blob SHAs identical on main. |
| S1 historical Facebook canonical identity | HOLD | HOLD | HOLD | HOLD | Agent can seek public permalink and compare exact text; if unavailable, author must attest or label as conversation snapshot. Exact-title public-web search yielded no reliable matching canonical link; this does not prove a post does not exist. |
| S2 Pocket 9E page/figure context | PARTIAL+ | PARTIAL+ | PARTIAL+ | PARTIAL+ | Agent already located and inspected pages above. Remaining: confirm print labels, original file hash/version, figure footnotes and Cirrhosis appendix; do not restage the entire book. |
| S3 original figure legal reuse | HOLD | HOLD | HOLD | HOLD | Agent can design own figures linked to causal decision breakpoints; for public original textbook pixels, explicit rights determination is needed. |
| M0 evidence-based integrated manuscript | HOLD | HOLD | HOLD | HOLD | Agent drafts separately from immutable original; existing A/B/C/D medical audits are inputs, not finished integrated chapters. |
| M1 safety / independent medical sign-off | HOLD | HOLD | HOLD | HOLD | Agent checks P0/P1 claims, clinical counterexamples, evidence levels; independent competent medical judgment/sign-off remains separate. |
| V0 figure semantics + small-screen usability | HOLD | HOLD | HOLD | HOLD | Agent must make actual evidence/decision diagrams (not decorative text cards); validate figures at 360/390 px; medical interpretation reviewed separately. |
| E0 regression tests and build for public candidate | NOT APPLICABLE YET | NOT APPLICABLE YET | NOT APPLICABLE YET | NOT APPLICABLE YET | Main already fixed historic schema error; run fresh validation only on the eventual integrated content commit. |
| E1 allowlist + deploy + reachable URL | HOLD | HOLD | HOLD | HOLD | No allowlist edits / merge / deploy without complete sign-offs. |

## 4. Article-specific acceptance tests (cannot be shared as one medical approval)

- **#66 — Cholestasis**: Can the reader explain why ALP-predominant pattern ≠ etiology, confirm hepatobiliary ALP source, why *no ultrasound duct dilation* does not rule out obstruction, and when cholangitis/organ dysfunction changes triage to urgent clinical intervention? Separate diagnostic MRCP/EUS from therapeutic ERCP; don't equate cholestasis with proven hepatocyte dysfunction.
- **#67 — Infiltrative ALP**: Can the reader distinguish measured ALP phenotype from hypothesized tissue infiltration, with competing etiologies (PBC, PSC, DILI, systemic diseases)? Is `SPEP to r/o amyloid` explicitly constrained (SPEP alone insufficient for AL evaluation)? Imaging-negative ≠ microscopic infiltration ruled in or out; ALP magnitude ≠ infiltrated tissue volume.
- **#68 — Chronic diarrhea**: Does the diagram express **prioritization of signals**, not obligatory linear natural history? Contextualize the original `<100/≥100` gap threshold against recognized clinical grey zones, fasting clues and sample artifacts; explain that normal calprotectin or normal gross colonoscopy cannot rule out microscopic colitis when clinically indicated; avoid categorization = diagnosis.
- **#69 — Cirrhosis**: Do histologic structure, cACLD/NIT risk, CSPH, first decompensation, liver function, and prognosis remain distinct concepts? Verify applicability limits of Baveno VIII cutoffs. Child–Pugh retains prognostic use and MELD 3.0 is not just bilirubin/INR/creatinine. Varices alone ≠ decompensation; score improvement ≠ recompensation. Appendix source gate remains open.

## 5. Lowest-maintenance work order

1. **Record closure of redundant intake PRs** (as superseded/unmerged) without losing their author source history; consolidate new actions here, **not** by re-merging a stale manifest.
2. **Finish remaining original-source evidence** using located page ranges and resolve 463-versus-464-page / hash question; locate Cirrhosis scoring Appendix; cross-check page labels and caption/footnotes.
3. **Canonical check once per author text**, not separate source-import jobs. Explicitly label a snapshot when canonical cannot be verified; do not block unrelated *draft research* on that label.
4. **Agent: #66 → #67 as a two-piece liver-chemistry causal chain**; #69 is an independent structure/portal-pressure/compensation axis, not a later stage of cholestasis; #68 independent diarrhea phenotyping. Preserve original author manuscripts untouched.
5. **Build only decision-relevant illustrations**, prove figure-specific information added, test visually on desktop and mobile, and audit citations / current guidelines and real-case sourcing.
6. **Independent medical review** and rights/author-version disposition **per article**. If any unresolved P0/P1 safety concern, no release.
7. **Only after sign-off** run same-commit publication tests, update `site/pages.json`, obtain explicit release decision and separately verify Cloudflare deploy + HTTPS.

## 6. Historic CI evidence (not four distinct medical defects)

PRs #66–#69 previously passed 66 unit tests each, then failed `Evidence-gated site build` due to the old intake inventory parser rejecting `source_snapshot_archived` (workflow IDs **40350093014, 40350637580, 40350348762, 40350464031**). Main's later engineering audit and `tools/check_corpus_inventory.py` document repair. Old failed run histories remain accurate historical outcomes; neither retrying those stale heads nor claiming retrospective green statuses is needed. The gate for future public manuscripts is a **new commit's actual CI + medical review**, not this legacy error.

**Publication verdict as of this record: #66 HOLD / #67 HOLD / #68 HOLD / #69 HOLD.** No independent human medical sign-off, canonical Facebook verification, image-reuse clearance or newly authored site pages for these four is established.
