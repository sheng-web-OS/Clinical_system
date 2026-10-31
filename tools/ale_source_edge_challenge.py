#!/usr/bin/env python3
"""Source-anchored Q0 -> tentative purpose-edges -> Q3 edge-target review.

Not a clinical semantic parser, general relation extractor, guideline validator,
or canonical graph editor. The lexical rule only parses an explicitly expressed
"not for X but to/for Y" purpose contrast, with attribution to a local
grammatical subject. The provided comparison edges are *hypotheses*, not truth.
All inputs must be bounded and public-safe. Never read private learner state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from ale_raw_q0_probe import extract

EDGE_PACKET_KEYS = {"source_classification", "edges"}
EDGE_KEYS = {"id", "subject_anchor", "target_anchor", "relation"}
RELATIONS = {"DIRECT_SCREENING_TEST", "AIDS_INTERPRETATION",
             "REQUIRED_PRECONDITION", "EXCLUDES_DIAGNOSIS_IF_NORMAL"}
ID = re.compile(r"[a-z][a-z0-9_-]{1,49}\Z")
ANCHOR = re.compile(r"[A-Za-z][A-Za-z0-9 -]{1,79}\Z")
# An explicit contrast with positive and negative complements, not a generic
# exclusion. Allow dashes, variable spacing, and "but to" or "but for".
ROLE = re.compile(
    r"\bnot\s+for\s+(?P<negative>.+?)\s*,?\s*but\s+(?:to|for)\s+"
    r"(?P<positive>.+?)(?:[.!?]|$)", re.IGNORECASE)
# Only a local subject in declarative measurement syntax is attributed.
# Never assign the role to all other biomarkers listed "alongside" it.
SUBJECT = re.compile(
    r"^\s*(?P<subject>(?:the\s+)?[A-Za-z][A-Za-z -]{0,50}?)\s+"
    r"(?:should\s+be\s+measured|is\s+measured|is\s+assessed|"
    r"should\s+be\s+assessed|was\s+measured|is\s+tested)\b",
    re.IGNORECASE)


def _norm(value: str) -> str:
    return " ".join(value.casefold().split())


def _span(sentence: str, phrase: str) -> dict:
    start = sentence.casefold().find(phrase.casefold())
    if start < 0:
        raise ValueError("source phrase not found")
    return {"start": start, "end": start + len(phrase)}


def _safe_edges(packet: dict) -> list[dict]:
    if type(packet) is not dict or set(packet) != EDGE_PACKET_KEYS:
        raise ValueError("invalid comparison packet")
    if packet["source_classification"] != "PUBLIC_SYNTHETIC_ONLY":
        raise ValueError("private or unclassified edge hypotheses forbidden")
    edges = packet["edges"]
    if type(edges) is not list or len(edges) > 12:
        raise ValueError("unbounded comparison edges")
    seen = set()
    for edge in edges:
        if type(edge) is not dict or set(edge) != EDGE_KEYS:
            raise ValueError("invalid edge fields")
        eid, subject, target, role = (
            edge["id"], edge["subject_anchor"], edge["target_anchor"],
            edge["relation"])
        if (type(eid) is not str or not ID.fullmatch(eid) or eid in seen
                or type(subject) is not str or not ANCHOR.fullmatch(subject)
                or type(target) is not str or not ANCHOR.fullmatch(target)
                or role not in RELATIONS):
            raise ValueError("invalid public-safe edge anchors")
        seen.add(eid)
    return edges


def review(source_packet: dict, comparison_packet: dict) -> dict:
    """Use exact source phrase evidence to challenge only scoped purpose roles."""
    edges = _safe_edges(comparison_packet)
    q0 = extract(source_packet)  # strict existing public-only / PII gate
    source_text = source_packet["excerpt"]
    # Absence of a cue is a valid end state, not an invented relation.
    parsed = []
    for candidate in q0["candidates"]:
        if candidate["cue"] != "MEASUREMENT_ROLE_SPLIT":
            continue
        sentence = candidate["exact_evidence"]
        match = ROLE.search(sentence)
        sub = SUBJECT.search(sentence[:match.start()] if match else sentence)
        if not match or not sub:
            continue
        negative = match.group("negative").strip(" ,;—–")
        positive = match.group("positive").strip(" ,;—–")
        subject = sub.group("subject").strip()
        if not (negative and positive):
            continue
        base = candidate["start_char"]
        parsed.append({
            "subject_quote": subject, "negative_purpose_quote": negative,
            "positive_purpose_quote": positive,
            "source_offsets": {
                "subject": {k: v + base for k, v in _span(sentence, subject).items()},
                "negative": {k: v + base for k, v in _span(sentence, negative).items()},
                "positive": {k: v + base for k, v in _span(sentence, positive).items()},
            },
            "source_sentence_sha256": hashlib.sha256(
                sentence.encode("utf-8")).hexdigest(),
            "source_ref": q0["source_ref"],
            "parse_basis": "EXPLICIT_PURPOSE_CONTRAST",
        })
    # An explicit subject from a single source sentence is not an accepted
    # canonical Concept ID, or proof of subject identity across families.
    judgments = []
    for edge in edges:
        outcome, reason, matched = (
            "ABSTAIN_NO_EXACT_LOCAL_ROLE_MATCH",
            "No source-anchored purpose contrast justifies this proposed edge.",
            None)
        for local in parsed:
            if _norm(edge["subject_anchor"]) != _norm(local["subject_quote"]):
                continue
            negative = _norm(local["negative_purpose_quote"])
            positive = _norm(local["positive_purpose_quote"])
            target = _norm(edge["target_anchor"])
            in_negative = target in negative
            in_positive = target in positive
            if edge["relation"] == "DIRECT_SCREENING_TEST" and in_negative:
                outcome = "CHALLENGE_DIRECT_SCREENING_ROLE"
                reason = ("The source explicitly denies this direct purpose; "
                          "it does not deny all clinical utility.")
                matched = "negative"
                break
            if edge["relation"] == "AIDS_INTERPRETATION" and in_positive:
                outcome = "TEXT_SUPPORTS_INTERPRETATION_ROLE_CANDIDATE"
                reason = ("An explicitly stated supporting purpose exists; "
                          "disease mechanism and applicability still need review.")
                matched = "positive"
                break
            if in_negative or in_positive:
                outcome = "ABSTAIN_SCOPE_NOT_ESTABLISHED"
                reason = ("This phrase does not establish the claimed stronger "
                          "necessity, diagnosis-exclusion, or causal inference.")
                matched = "negative" if in_negative else "positive"
                break
        judgments.append({"id": edge["id"], "decision": outcome,
                          "matched_side": matched, "reason": reason,
                          "medical_truth_verified": False,
                          "graph_change_authorized": False})
    has_supported_role = any(
        j["decision"] == "TEXT_SUPPORTS_INTERPRETATION_ROLE_CANDIDATE"
        for j in judgments)
    return {
        "schema": "ale-source-edge-challenge-v0",
        "source_ref": q0["source_ref"],
        "q0_decision": q0["decision"],
        "source_local_role_contrasts": parsed[:4],
        "edge_judgments": judgments,
        "missing_positive_role_review": (
            "SOURCE_PHRASE_RELATION_REVIEW_NEEDED"
            if parsed and not has_supported_role else "NONE_DETECTED"),
        "q3_question": (
            "Does 'not a direct input to this decision' imply 'irrelevant to "
            "interpretation', or are those distinct roles? Test a different "
            "decision stage and check the full original source."
            if parsed else None),
        "original_source_full_context_checked": False,
        "existing_graph_semantics_verified": False,
        "canonical_concept_ids_created": 0,
        "graph_edits": 0,
        "learner_state_read": False,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--comparison", required=True, type=Path)
    args = ap.parse_args()
    print(json.dumps(review(json.loads(args.source.read_text(encoding="utf-8")),
                            json.loads(args.comparison.read_text(encoding="utf-8"))),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
