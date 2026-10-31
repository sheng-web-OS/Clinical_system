# ALE | Incremental knowledge-gap research triage (public-safe, read-only)

Owner decision 2026-10-31: incomplete topic maps are normal. The autonomous agent should select the highest-value knowledge gap to investigate, queue the rest, and deliberately leave low-impact unknowns unresolved. This is a bounded **policy baseline**, not independent semantic understanding.

## Existing lineage

Extension of #258, stacked within the existing #260 Concept Family Draft experiment (also related to #263/#268). Input Concepts and any clinical reasoning roles must come from verified external source work or an explicitly marked unverified hypothesis; **tags are retrieval hints, not canonical concept identities**. Reuse `content/clinical-os/index.md` knowledge-context backbone and its clinical question → physiology → discriminating evidence structure. No second ontology, backlog service, automation or database.

## Contract

`tools/ale_gap_triage.py` accepts **only PUBLIC_SYNTHETIC_ONLY bounded role-token fixtures** and implements a deterministic choice per gap:
- `RESEARCH_NOW`: critical or currently blocking uncertainty with available capacity, pending a genuine source check.
- `QUEUE_RESEARCH`: meaningful but non-immediate, or transfer leverage across at least two distinct Concept Families.
- `PRESERVE_UNKNOWN`: no present decision impact or justified transfer value; reopen when material evidence changes.
- `DIAGNOSTIC_FIRST`: tag-only, passive-reading, or Anki-review-rating-only evidence, which cannot prove a concept error or clinical truth.
- `CRITICAL_UNRESOLVED_HOLD`: critical gap exceeds research capacity, **not safe to silently downgrade**.
- `SCOPE_CONFLICT_HOLD`: critical risk declared outside the task scope; must reconcile assumptions.

The ordering is **qualitative, unvalidated, explainable**, not a numeric causal utility formula: critical → blocking → cross-family transfer → low, with current scope, family reach, effort and stable ID for ties. Limited `max_active_research` counts concurrent research selection, not automatic research execution. All outputs say source independently verified = false and concept promotion authorized = false.

### Synthetic example

Save the following in a temporary local JSON file (NOT an actual user or medical case):

```json
{
  "source_classification":"PUBLIC_SYNTHETIC_ONLY",
  "max_active_research":1,
  "gaps":[
    {"id":"inference_conflict","origin":"SOURCE_CONTRADICTION","impact":"CRITICAL","scope":"CURRENT","source_state":"PENDING","linked_family_count":1,"research_effort":"SMALL"},
    {"id":"shared_bridge","origin":"COVERAGE_GAP","impact":"TRANSFER","scope":"NEARBY","source_state":"SOURCE_ATTESTED","linked_family_count":3,"research_effort":"LARGE"},
    {"id":"passive_click","origin":"PASSIVE_READING","impact":"BLOCKING","scope":"CURRENT","source_state":"ABSENT","linked_family_count":0,"research_effort":"UNKNOWN"}
  ]
}
```

Run:
```bash
python tools/ale_gap_triage.py --input /path/to/synthetic-packet.json
python -m unittest discover -s tests -p 'test_ale_gap_triage.py' -v
```

Expected: `inference_conflict → RESEARCH_NOW` requiring independent source verification; `shared_bridge → QUEUE_RESEARCH`; `passive_click → DIAGNOSTIC_FIRST`. No clinical conclusion, website publishing, Anki / FSRS mutation, credentials, user study record or actual external research occurs.

## Why this is only stage 0

The program accepts **caller-declared** impact, scope, family reach, and source annotations. Its rules do not infer which gaps exist, whether an IBCC / guideline branch really matters, or whether a source statement is true. A validated next stage should create a public-safe topic reasoning spine from real consulted references; a separate reviewer should challenge missing mechanisms, applicability, and counterexamples (recursive Q0–Q3), then prospectively compare the top-1 research choice against static breadth-first completion under equal time.

### First meaningful acceptance

On one already published topic, an authorized reasoning pass identifies 3–5 genuine source-linked gaps, a different review checks their importance and context, and the decision-maker selects exactly one question to resolve. Preserve original uncertainty. Assess **changed concept quality and learner-unseen reasoning**, false merges, research minutes and owner intervention count. If the priority choice is not useful or the source cannot be verified, revise or abandon the policy; do not expand synthetic tests as a substitute.

Public GitHub/CI must never process actual private Anki, learning events, reading records, card identities, private Sheets URLs or medical patient data. Original #137 experiment remains closed and historically unchanged. No new cloud scheduler, paid API, merge or deployment.
