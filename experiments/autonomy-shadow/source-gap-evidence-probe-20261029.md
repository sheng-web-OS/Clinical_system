# Evidence gap probe — lexical synthetic experiment (2026-10-29)

**State:** Draft / HOLD, public synthetic material only. Do not connect to the production agent, merge, publish medical content, or activate a schedule based on this experiment.

## Question

Can a program decide whether a local source is *actually absent* by reading the article and its existing repo evidence, instead of accepting a caller-provided \`source_state=missing\`? This is the smallest precursor to proactive retrieval. It does NOT establish autonomous medical question selection or learning.

## Minimal executable probe

\`tools/synthetic_evidence_gap_probe.py\` reads one synthetic Markdown lesson and local caption directory from a bounded repo root, extracts at most one referenced \`Figure F#\`, and returns JSON containing \`decision\`, a fixed diagnostic \`reason\`, \`model_calls:0\`, \`external_reads:0\`, and \`autonomy_certified:false\`.

- \`READ\`: the cited synthetic figure has neither local caption nor hash anchor. This is only a candidate retrieval need, not permission to access restricted sources.
- \`SKIP\`: no figure is referenced, or a matching local caption exists with an integrity-checking SHA-256 anchor. The hash demonstrates local integrity, **not primary-source provenance, clinical truth or authorship rights**.
- \`HOLD\`: missing/inconsistent hash, conflicting candidate, unsupported multiple figures, malformed text, path traversal/symlink, unsafe or oversized file. No network or model calls occur.

Test fixtures are built in a temporary directory; no patient history, real copyrighted figure, source ID, API Key or private evaluation is stored. \`python -m unittest discover -s tests -p 'test_synthetic_evidence_gap_probe.py'\` runs the fail-closed controls.

## Gates before further engineering

1. Run exact-head PR CI and inspect all failing fixtures. Leave as Draft/HOLD.
2. Measure three independent questions separately: can the agent spot a real decision-relevant missing source, does retrieving it actually improve a *first-pass* judgment, and does this generalize to a new case with less owner attention? This trivial regex probe proves none of these.
3. Avoid duplicate production edits: #234 already changes the \`tools/drive_source_agent.py\` metadata preflight; #232 already writes a synthetic connector Draft; #225 holds skill transfer tests and #159 holds unattended evaluation. This PR changes no files they own.
4. For future model-assisted triage, compare deterministic no-model preflight vs model decision at matched source access and record real calls and owner minutes. Do not promote a Skill if Native+retrieval is already as good.
5. The only acceptable expansion is an independently reviewed *public/rights-cleared* evidence gap with explicit proof of correct READ/SKIP/HOLD and an audit trail. Human clinical/source/release approvals remain separate gates.

**Stop rule:** if this lexical path cannot identify decision-relevant gaps beyond the existing #234 check with acceptable false-read and false-skip rates, retire rather than institutionalize another framework.
