# AGENTS.md — Clinical OS repository instructions

This is the PRIVATE source-of-truth repository for the Clinical OS / Xiaoma medical editorial system. Public reading is produced from an explicit allowlist, not from arbitrary repository files.

## Read the minimum needed

1. For any medical editorial task read docs/clinical-os-integration-20261021.md and the applicable existing contract(s): docs/editorial-prose-quality-contract.md, docs/learning-experience-contract.md, docs/medical-writing-corpus.md, docs/xiaoma-evidence-expansion.md.
2. For experiments and performance claims read experiments/README.md. Do not promote pilot results, self-reviews, CI checks, or reported historical outcomes into validated clinical or learning-effect claims.
3. For site publication read docs/xiaoma-publishing.md and site/pages.json. A source commit, passing tests, Cloudflare deployment, and public HTTP reachability are separate states.

## Default agent behavior

- Prefer current-model native research, causal reasoning, tools and self-correction. Preserve only irreconstructible assets, expert decisions, audit evidence, and minimal regression tests. Do not add orchestration, registries, databases or persistent Claim Graphs unless measured benefit pays for maintenance.
- Recover existing source files and inspect original tables, flowcharts, figures, captions and footnotes BEFORE claiming to correct or augment a medical article. Record what was actually inspected. Inaccessible files stay pending; never recreate a purported author's original from a summary.
- Classify each proposed knowledge addition: A = already explained, B = cross-document connection, C = genuinely missing evidenced bridge, D = necessary correction/qualification, X = unsupported. Evaluate additions in order: evidential support, fit to the original essay's clinical thesis, repair of genuinely missing causal premises, then continuous reader understanding. A well-evidenced but off-thesis fact belongs elsewhere; authorship or style mimicry is not a quality gate. Do not conflate clearer prose with new scientific knowledge.
- Generate AI integrative teaching separately from preserved historical originals. Never silently change content/xiaoma-reading/originals or promote conversation snippets to approved published originals. A verifiably published Facebook version is the default author-canonical historical text; otherwise mark provenance pending. New AI-authored lessons can receive autonomous AI editorial approval under the full evidence/clinical/rights gates without requiring author sign-off. Keep historical originals unchanged and provenance truthful; do not claim human peer review unless it occurred.
- For medical content, preserve the causal chain and evidence-to-decision boundaries. Embed ICU/decompensation implications naturally where clinically needed. EPQC and P0/P1 clinical safety failures outrank stylistic scores. Model self-scoring is not independent expert review.
- Prioritize content and primary source verification over more website components. Interaction must prove better learning than high-quality static presentation, not just become clickable.
- On errors, independently classify cause, attempt a targeted fix and rerun the smallest relevant regression. Escalate genuine source ambiguity or unavoidable medical uncertainty; avoid endless retries or hidden unsuccessful tool calls.
- A user's goal is to keep maintenance and debugging time near zero, then optimize model/computational cost without reducing quality.

## Git and deployment boundaries

- Existing site stack: Markdown -> Python deterministic build -> explicit site/pages.json -> Cloudflare Pages (main). Keep private archive, medical textbook PDFs, raw patient information and private metadata out of public outputs.
- Work on a scoped feature/experiment branch when changing shared architecture, experiments or unpublished medical material. Make a draft PR rather than force-merge or deploy experiments. Coordinate against latest main and avoid rewriting parallel work.
- Use existing validation: bash tools/build_site.sh plus project tests; new tests only if they catch a demonstrated expensive/critical failure.
- Do not alter published pages or author originals while consolidating experiments; require the existing editorial, rights and clinical safety gates for separate publication actions.
- User has excluded cardiac-surgery/surgical content, intracranial aneurysm materials, and rotation reflections from the Xiaoma public publication candidate pool.
- If tool access or source provenance cannot be checked, describe the limitation and save a precise next step, never a fabricated success.

## Current priorities

1. Reconcile stale state summaries using the actual Git tree: as of 2026-10-21 baseline main, seven original article files exist; six were imported from a 21-item chat intake and fifteen await migration. Source identity and medical review remain separate.
2. Verify the original-source and figure-level HF / LVEDP / DCM / diuretics causal audit, especially real additions versus author-explained claims.
3. Run independent, same-model, same-source Native vs evidence-only vs Clinical OS Lite controlled comparisons. PR #7 hyponatremia is a HOLD demonstration, not a blinded win.
4. Conduct static-vs-interactive learning tests and Lite-vs-Full/T5-T6 regression only after material and scoring conditions are fixed.
5. Respect the user's 2027 February NTUH exam readiness ahead of the June 2027 national stage-2 goal; planned chapter count is not evidence of readiness.

This file is a compact Codex/agent entrypoint. Detailed specifications live once in the linked documents; never duplicate them here as another long Master Prompt.
