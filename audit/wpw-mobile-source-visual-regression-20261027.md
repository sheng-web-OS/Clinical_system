# WPW mobile source-figure regression: real-screen evidence (2026-10-27)

## Scope and observed failure

- Source: `content/xiaoma-reading/integrated/2026-10-26-wpw-conduction-mechanism.md`, Figure `wpw-pathway-figure`.
- Inspected GitHub Actions run `40371037191` (previous passing run) screenshot artifacts: desktop `wpw-wpw-pathway-figure-1280.png` and phone `wpw-wpw-pathway-figure-390.png`. [Run and downloadable QA artifacts](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40371037191).
- **Regression that CI incorrectly passed:** phone displayed individual source panels but CSS `aspect-ratio:250 / 305; top:-21.312%` omitted original heading and the bottom source ECG annotations, while part of the neighboring figure column could appear at the right edge. Source itself is a 750×446 three-panel teaching diagram with valuable titles and original annotations.
- Visual judgement: **HOLD**, despite the earlier layout-only CI success. Content was cropped such that viewers could not independently cross-check all source figure labels.

## Second review: a passing screenshot still exposed cut English labels

- Independently inspected [Actions #40372975065](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40372975065), including both the full desktop source and the 390px phone screenshot. The intermediate full-height `250 / 446` crop retained source bullet points but clipped the left/right margins of English headers, e.g. Orthodromic AVRT, while adjacent column fragments were visible. **This is a visual HOLD despite a green CI result.**
- Based on the complete original 750×446 image, retain **only the original anatomy and ECG waveform pixel region** in each phone window: source x = `0..250`, `250..500`, `500..750`; common source y = `75..385`. At this position the heart diagram and ECG wave remain visible, while broken English title fragments and original footnote text do not appear in the crop.
- Preserve actual original source pixel data unchanged and retain a direct full-size original link; separately typeset source-derived PR/delta-wave, P-wave, QRS and reentry caveats as mobile-readable text. The graphic should not be presented as a separate real patient ECG recording.
- CSS now uses `aspect-ratio:250 / 310`, `top:-24.194%`, and accurate one-/two-column horizontal offsets. Browser QA checks the **exact displayed source rectangle**, failing when ROI boundaries shift, rather than incorrectly insisting that all original source text be compressed within a phone crop.
- The crop geometry is a structural regression guard, not proof of semantic accuracy, medical review, source-rights clearance or legibility of every small ECG detail. The new actual Chromium screenshots still require visual examination before publication.

## Remaining gates

- Recheck actual post-change Chromium 360/390/1280px captures and adjacent explanatory text. Earlier passing screenshots belong to the **old version**, not the correction.
- Original third-party reuse/crop rights remain independently unresolved; the medical article and referenced original-image legend are not automatically approved by rendering changes.
- Do not merge/deploy based solely on a green test. Medical source accuracy, medical editorial judgement, visual readability, copyright and website deployment are separate decisions.
