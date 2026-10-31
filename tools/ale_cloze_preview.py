#!/usr/bin/env python3
"""Render Cloze-first ALE proposals without writing to Anki.

A structural preview, NEVER an automated clinical, semantic or source approval.
Accept owner-private proposals only in an owner-private runtime; don't log them in
public GitHub/CI. Public tests contain only synthetic non-personal material.
"""
from __future__ import annotations

import re
from collections import Counter

SLOT = re.compile(r"\[\[([a-z][a-z0-9_]*)\]\]")
CLINICAL_REVIEW_PENDING = "STRUCTURE_ONLY_PENDING_SEMANTIC_SOURCE_AND_OWNER_REVIEW"


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())



def preview_masked_fronts(rendered: str, groups) -> dict:
    """Expose the actual all-blanks-hidden reading task for each generated card.

    Other cloze groups remain readable as in Anki. This reveals cases where
    two or more simultaneous omissions destroy the causal context. It does NOT
    claim to judge clinical correctness or semantic answerability.
    """
    pattern = re.compile(r"\{\{c([1-9][0-9]*)::([^{}]*?)(?:::([^{}]*?))?\}\}")
    def front(group):
        def replacement(match):
            if int(match.group(1)) == group:
                return "[" + (match.group(3) or "...") + "]"
            return match.group(2)
        return pattern.sub(replacement, rendered)
    return {str(group): front(group) for group in sorted(groups)}

def render_cloze_proposal(p: dict) -> dict:
    """Return one Anki Cloze note preview; same group means same review card.

    Expected fields: concept_family_id, concept_node_id, tested_relation,
    learning_goal, context, template, source_refs, slots. Each slot has
    key, answer, group (positive integer), optional hint, optional needs_hint.
    'context' remains VISIBLE when all clozes in a group are hidden.
    """
    if not isinstance(p, dict):
        raise ValueError("proposal must be a mapping")
    for key in ("concept_family_id", "concept_node_id", "tested_relation",
                "learning_goal", "context", "template"):
        if not _nonempty(p.get(key)):
            raise ValueError("missing concept/goal or visible retrieval context: " + key)
    refs = p.get("source_refs")
    if not isinstance(refs, list) or not refs or not all(_nonempty(r) for r in refs):
        raise ValueError("source references required (not verified by this renderer)")
    slots = p.get("slots")
    if not isinstance(slots, list) or not slots:
        raise ValueError("one or more cloze slots required")
    keys = [s.get("key") for s in slots if isinstance(s, dict)]
    if len(keys) != len(slots) or any(not _nonempty(k) for k in keys) or len(set(keys)) != len(keys):
        raise ValueError("slot keys must be nonempty and unique")
    matches = SLOT.findall(p["template"])
    if Counter(matches) != Counter(keys):
        raise ValueError("each declared slot must occur once in the visible template")
    if "[[" in SLOT.sub("", p["template"]) or "]]" in SLOT.sub("", p["template"]):
        raise ValueError("unrecognized slot syntax")
    seen = {}
    groups = Counter()
    for s in slots:
        group = s.get("group")
        if type(group) is not int or group < 1:
            raise ValueError("cloze group must be a positive integer")
        answer = s.get("answer")
        hint = s.get("hint", "")
        if not _nonempty(answer):
            raise ValueError("empty answer")
        if not isinstance(hint, str) or (s.get("needs_hint", False) and not _nonempty(hint)):
            raise ValueError("required disambiguating hint missing")
        if hint and answer.casefold() in hint.casefold():
            raise ValueError("hint reveals the complete answer")
        if "::" in answer or "::" in hint or "{{" in answer or "}}" in answer:
            raise ValueError("Anki markup collision")
        groups[group] += 1
        replacement = "{{c" + str(group) + "::" + answer
        if hint:
            replacement += "::" + hint
        seen[s["key"]] = replacement + "}}"
    if any(count > 1 for count in groups.values()) and not _nonempty(p.get("why_together")):
        raise ValueError("multi-cloze card needs explicit concept-coherence rationale")
    text = SLOT.sub(lambda m: seen[m.group(1)], p["template"])
    if "{{c" in p["context"] or "[[" in p["context"]:
        raise ValueError("context must stay visible with all groups hidden")
    rendered_text = p["context"].strip() + "\n" + text
    return {
        "note_type": "Cloze",
        "text": rendered_text,
        "card_groups": sorted(groups),
        "masked_fronts_for_review": preview_masked_fronts(rendered_text, groups),
        "card_count": len(groups),
        "cloze_count": len(slots),
        "single_card_multi_cloze": any(n > 1 for n in groups.values()),
        "status": CLINICAL_REVIEW_PENDING,
        "source_verified": False,
        "semantic_quality_verified": False,
        "anki_mutated": False,
    }
