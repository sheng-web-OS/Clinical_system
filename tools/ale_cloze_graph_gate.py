#!/usr/bin/env python3
"""ALE graph-first Cloze candidate gate (public-safe, no Anki/FSRS writes).

The deterministic portion anchors an author-written Cloze note to an actual
typed, sourced, problem-centered Concept Family edge. It does not prove a
medical statement, invent a question from literature, or adjudicate if all
hidden terms are pedagogically appropriate. A distinct semantic/medical review
and owner-private pilot remain necessary.
"""
from __future__ import annotations

import re
from tools.ale_cloze_preview import render_cloze_proposal

# This is only a narrow negative control for known bad exam-meta wording,
# never a substitute for natural-language semantic review.
META_FRAMING = re.compile(r"國考|考題|解題|題目中|考試中|在題目裡|test question|exam question", re.I)
RETRIEVAL_ROLES = {
    "insufficient_without": "missing_condition_or_evidence",
    "satisfies_criterion": "sufficient_narrow_criterion",
    "required_for": "required_evidence_to_target",
    "does_not_alone_satisfy": "partial_criterion_not_total",
    "does_not_exclude": "negative_result_does_not_exclude",
    "challenges_equivalence": "observation_vs_disease_process",
}


def list_graph_targets(graph: dict) -> list[dict]:
    """Provide concept-linked targets, NOT fabricated flashcards."""
    families = {f["id"]: f for f in graph["families"] if f["kind"] == "problem_centered"}
    nodes = {n["id"]: n for n in graph["concepts"]}
    results = []
    for edge in graph["typed_edges"]:
        if edge["type"] not in RETRIEVAL_ROLES:
            continue
        a, b = nodes.get(edge["from"]), nodes.get(edge["to"])
        if not a or not b:
            continue
        membership = set(a["family_ids"]) & set(b["family_ids"]) & set(families)
        if len(membership) != 1:
            continue   # never invent a cross-family causal identity
        source_ids = set(edge["source_ids"]) & set(a["source_ids"]) & set(b["source_ids"])
        if not source_ids:
            continue
        results.append({
            "edge_id": edge["id"],
            "concept_family_id": next(iter(membership)),
            "concept_node_id": edge["to"],
            "tested_relation": edge["type"],
            "retrieval_role": RETRIEVAL_ROLES[edge["type"]],
            "from_concept_id": edge["from"],
            "to_concept_id": edge["to"],
            "boundary": edge["condition"],
            "source_refs": sorted(source_ids),
            "suggested_format": "Cloze",
            "candidate_only": True,
            "has_generated_card": False,
        })
    return results


def check_graph_anchored_cloze(graph: dict, proposal: dict) -> dict:
    """Fail before rendering if graph target, constraints or context is missing.

    Checks schema/lineage and a few known anti-patterns. It deliberately leaves
    independent semantic fitness and medical source truth unverified.
    """
    if not isinstance(proposal, dict):
        raise ValueError("proposal must be an object")
    targets = {item["edge_id"]: item for item in list_graph_targets(graph)}
    edge_id = proposal.get("edge_id")
    target = targets.get(edge_id)
    if target is None:
        raise ValueError("MISSING_OR_UNSUPPORTED_TYPED_EDGE")
    for key in ("concept_family_id", "concept_node_id", "tested_relation"):
        if proposal.get(key) != target[key]:
            raise ValueError("WRONG_CONCEPT_TARGET_OR_EDGE_ROLE: " + key)
    if not isinstance(proposal.get("source_refs"), list) or not proposal["source_refs"]:
        raise ValueError("SOURCE_PROVENANCE_MISSING")
    if not set(proposal["source_refs"]) <= set(target["source_refs"]):
        raise ValueError("SOURCE_MISMATCH_WITH_TYPED_EDGE")
    if not isinstance(proposal.get("retrieval_role"), str) or proposal["retrieval_role"] != target["retrieval_role"]:
        raise ValueError("RETRIEVAL_ROLE_NOT_DERIVED_FROM_GRAPH")
    if not isinstance(proposal.get("scope_boundary"), str) or len(proposal["scope_boundary"].strip()) < 12:
        raise ValueError("NO_EXPLICIT_SCOPE_OR_COUNTEREXAMPLE")
    if not isinstance(proposal.get("reason_this_tests_edge"), str) or len(proposal["reason_this_tests_edge"].strip()) < 12:
        raise ValueError("NO_REASONED_EDGE_TO_RETRIEVAL_MAPPING")
    for key in ("context", "template", "learning_goal"):
        if META_FRAMING.search(str(proposal.get(key, ""))):
            raise ValueError("EXAM_META_NOT_A_CLINICAL_RETRIEVAL_TARGET")
    rendered = render_cloze_proposal(proposal)
    rendered.update({
        "edge_id": edge_id,
        "concept_family_id": target["concept_family_id"],
        "concept_node_id": target["concept_node_id"],
        "from_concept_id": target["from_concept_id"],
        "retrieval_role": target["retrieval_role"],
        "source_references_asserted_not_independently_verified": list(proposal["source_refs"]),
        "graph_condition_for_reviewer": target["boundary"],
        "scope_boundary_for_reviewer": proposal["scope_boundary"],
        "semantic_acceptance": "PENDING_INDEPENDENT_REVIEW",
        "owner_acceptance": "NOT_OBSERVED",
        "ready_to_import": False,
    })
    return rendered
