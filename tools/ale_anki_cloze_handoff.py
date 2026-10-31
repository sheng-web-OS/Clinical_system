#!/usr/bin/env python3
"""Pure, private-runtime handoff: graph-reviewed Cloze PREVIEW -> HOLD queue row.

Consumes the JSON-shaped output of the separate graph-first preview (PR #260).
No Google Drive/Anki writes, no automatic clinical clearance, and no private data
in GitHub. The authoring model is not its own independent medical reviewer.
"""
import html

import ale_anki_import_queue as q


def masked_fronts(text, groups):
    """Deterministic basic (unnested) masked-front previews for comparison only."""
    result = {}
    for group in groups:
        def replace(match):
            answer, *hint = match.group(2).split("::")
            return "[" + (hint[0] or "...") + "]" if int(match.group(1)) == group else answer
        result[str(group)] = q.CLOZE_RE.sub(replace, text)
    return result


def candidate_hold_row(proposal, *, card_key, deck, tags, source_url):
    """Create a 12-column private Sheet row that CANNOT be auto-imported.

    For subsequent release a genuinely separate source/medical reviewer must
    inspect all masked siblings, validate claims against the original source,
    and set review receipt + QA + release only via authorized private workflow.
    This function deliberately offers no approve/release operation.
    """
    if not isinstance(proposal, dict) or proposal.get("note_type") != "Cloze":
        raise ValueError("Graph-first Cloze preview required")
    if (proposal.get("semantic_acceptance") != "PENDING_INDEPENDENT_REVIEW" or
            proposal.get("ready_to_import") is not False or
            proposal.get("source_verified") is not False or
            proposal.get("semantic_quality_verified") is not False):
        raise ValueError("Expected unapproved graph-first Cloze preview")
    for name in ("concept_family_id", "edge_id", "scope_boundary_for_reviewer"):
        if not isinstance(proposal.get(name), str) or not proposal[name].strip():
            raise ValueError("Missing family/edge/Q3 boundary: " + name)
    text = proposal.get("text")
    if not isinstance(text, str):
        raise ValueError("Preview text missing")
    groups = sorted({int(m.group(1)) for m in q.CLOZE_RE.finditer(text)})
    if not groups or proposal.get("card_groups") != groups or proposal.get("card_count") != len(groups):
        raise ValueError("Preview sibling groups differ from Cloze text")
    q.note_payload(text, "Q3 boundary and source review pending")
    if proposal.get("masked_fronts_for_review") != masked_fronts(text, groups):
        raise ValueError("Preview masked fronts missing or mismatched")
    if not q.KEY_RE.fullmatch(card_key) or not q.SAFE_DECK.fullmatch(deck):
        raise ValueError("Unsafe local card identity or deck")
    if not q.SOURCE.fullmatch(source_url):
        raise ValueError("Qualified source URL required")
    if not isinstance(tags, (list, tuple)) or not tags or len(tags) > 20:
        raise ValueError("Tags must be a bounded nonempty list")
    if any(not isinstance(tag, str) or not q.SAFE_TAG.fullmatch(tag) for tag in tags):
        raise ValueError("Malformed tag")
    # Text and Q3 are author proposals, not affirmed facts. Escape everything
    # interpolated into HTML; all private learner context stays in private Sheet.
    extra = "Q3 boundary (pending review): " + html.escape(
        proposal["scope_boundary_for_reviewer"]) + "\nSource (pending review): " + html.escape(source_url)
    if len(text) > q.MAX_HTML or len(extra) > q.MAX_HTML or q.BAD_HTML.search(text):
        raise ValueError("Unsafe/overlong private proposal")
    return dict(
        card_key=card_key,
        front_html=text,
        back_html=extra,
        tags=" ".join(dict.fromkeys(tags)),
        deck=deck,
        source_ref=source_url,
        independent_review_ref="",
        qa_status="PENDING_INDEPENDENT_MEDICAL_QA",
        release_status="HOLD",
        import_status="HOLD",
        anki_note_id="",
        content_sha256=q.digest(text, extra),
    )
