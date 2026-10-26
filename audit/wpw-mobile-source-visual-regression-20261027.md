# WPW mobile source-figure regression: real-screen evidence (2026-10-27)

## Scope and observed failure

- Source: `content/xiaoma-reading/integrated/2026-10-26-wpw-conduction-mechanism.md`, Figure `wpw-pathway-figure`.
- Inspected GitHub Actions run `40371037191` (previous passing run) screenshot artifacts: desktop `wpw-wpw-pathway-figure-1280.png` and phone `wpw-wpw-pathway-figure-390.png`. [Run and downloadable QA artifacts](https://github.com/sheng-web-OS/Clinical_system/actions/runs/40371037191).
- **Regression that CI incorrectly passed:** phone displayed individual source panels but CSS `aspect-ratio:250 / 305; top:-21.312%` omitted original heading and the bottom source ECG annotations, while part of the neighboring figure column could appear at the right edge. Source itself is a 750×446 three-panel teaching diagram with valuable titles and original annotations.
- Visual judgement: **HOLD**, despite the earlier layout-only CI success. Content was cropped such that viewers could not independently cross-check all source figure labels.

## Targeted correction and regression

- For each phone panel, use the complete original source-column aspect ratio `250 / 446`, `top:0`, and true thirds `-33.333%` / `-66.667%`. Remove opaque pseudo-element masks; do not redraw the scientific source.
- `tests/test_wpw_source_mobile_qa.py` locks these conditions. `tools/visual_qa_browser.py` now compares displayed source-image and crop-frame heights/vertical origin and reports `source annotation clipped vertically in mobile WPW crop` on mismatch.
- The check guards this *known failure mode*. It cannot itself certify that every original label is visually legible or that CSS percentage translation is scientifically suitable without reviewing the new screenshot.

## Remaining gates

- Recheck actual post-change Chromium 360/390/1280px captures and adjacent explanatory text. Earlier passing screenshots belong to the **old version**, not the correction.
- Original third-party reuse/crop rights remain independently unresolved; the medical article and referenced original-image legend are not automatically approved by rendering changes.
- Do not merge/deploy based solely on a green test. Medical source accuracy, medical editorial judgement, visual readability, copyright and website deployment are separate decisions.
