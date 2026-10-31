#!/usr/bin/env python3
"""Generate *candidate* parent Concept Families from cross-family reasoning signatures.

No API, credentials, Anki access or semantic truth assertions. This is a
reproducible proposer over explicit, source-linked reasoning annotations. The
annotations themselves require a separate model/evidence/clinical reviewer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from ale_recursive_family import evaluate

SIGNATURE_FIELDS = ("from_role", "to_role", "missing_bridge_role")


def _nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value.strip()


def _signature(record: dict) -> tuple[str, str, str]:
    sig = record.get("reasoning_signature")
    if not isinstance(sig, dict):
        raise ValueError("reasoning_signature must be an object")
    return tuple(_nonempty(sig.get(key), key) for key in SIGNATURE_FIELDS)


def _key(signature: tuple[str, str, str]) -> str:
    canonical = json.dumps(signature, ensure_ascii=False, separators=(",", ":"))
    return "inference-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]



def _feature_set(record: dict) -> frozenset[str] | None:
    """Return annotated conditions, or None when scope evidence is absent.

    A feature is an author-provided *hypothesis*, not a source-verified fact.
    Restrict names to stable public-safe role tokens to discourage prose/PHI.
    """
    features = record.get("context_features")
    if features is None:
        return None
    if not isinstance(features, list) or len(features) > 16:
        raise ValueError("context_features must be a list of at most 16 tokens")
    import re
    if any(not isinstance(x, str) or
           not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", x) for x in features):
        raise ValueError("context_features must contain only role tokens")
    if len(set(features)) != len(features):
        raise ValueError("duplicate context feature")
    return frozenset(features)


def scoped_refinements(groups: dict, contrary: dict) -> list[dict]:
    """Q3 counterexample -> next Q0: propose a minimal *conditional* repair.

    The refined candidate stays UNVERIFIED, even when a guard separates all
    known examples. A new unseen counterexample sharing the guard is mandatory.
    """
    from itertools import combinations
    revised: list[dict] = []
    for signature, supports in sorted(groups.items()):
        challenges = contrary.get(signature, [])
        # Candidate scope repairs require the same canonical family identity as
        # parent discovery; whitespace cannot manufacture an extra family.
        if len({x["family_id"].strip() for x in supports}) < 2 or not challenges:
            continue
        # Input flags are NOT independent source truth; nevertheless, missing or
        # explicitly unchecked references must not produce a scope proposal.
        if any(not isinstance(x.get("source_ref"), str)
               or not x["source_ref"].strip()
               or x.get("source_check") != "checked"
               for x in supports + challenges):
            continue
        positive = [_feature_set(x) for x in supports]
        negative = [_feature_set(x) for x in challenges]
        if any(x is None for x in positive + negative):
            continue
        shared = sorted(set.intersection(*(set(x) for x in positive)))
        if not shared:
            continue
        guard = None
        # Bounded hitting set: all supports have every guard condition, while
        # every known counterexample is missing at least one guard condition.
        for count in range(1, min(3, len(shared)) + 1):
            options = (part for part in combinations(shared, count)
                       if all(not set(part).issubset(neg) for neg in negative))
            guard = next(options, None)
            if guard is not None:
                break
        if guard is None:
            continue
        original_id = _key(signature)
        revised.append({
            "parent_candidate": original_id,
            "candidate_id": original_id + "-scoped",
            "stage": "Q3_TO_Q0_SCOPE_HYPOTHESIS",
            "required_context_features": list(guard),
            "support_ids": sorted(x["id"] for x in supports),
            "known_excluded_counterexamples": sorted(x["id"] for x in challenges),
            "question_q0": "Does the proposed condition change the original inference?",
            "question_q1": "Is the contradiction genuine or a scope mismatch?",
            "question_q2": "Which primary evidence supports the proposed conditional bridge?",
            "question_q3": "Find an unseen counterexample sharing EVERY proposed condition.",
            "verdict": "SCOPED_CANDIDATE_NEEDS_SEMANTIC_REVIEW",
            "promotion_authorized": False,
            "reason": "Role features are proposer assertions; matching them is not clinical or logical proof."
        })
    return revised


def discover(data: dict) -> dict:
    """Discover cross-family clusters; run skeptical gate, never promote.

    Input uses examples (possible overreaches) and challenges (limiting cases).
    No upstream record specifies a concept pattern or a candidate parent ID.
    """
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    examples = data.get("examples", [])
    challenges = data.get("challenges", [])
    dependencies = data.get("dependencies", [])
    if not all(isinstance(v, list) for v in (examples, challenges, dependencies)):
        raise ValueError("examples, challenges, dependencies must be lists")

    seen_ids: set[str] = set()
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    contrary: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    observations = []
    for kind, records, dest in (("support", examples, groups),
                                ("counterexample", challenges, contrary)):
        for entry in records:
            if not isinstance(entry, dict):
                raise ValueError("observations must be objects")
            eid = _nonempty(entry.get("id"), "id")
            family = _nonempty(entry.get("family_id"), "family_id")
            if eid in seen_ids:
                raise ValueError(f"duplicate observation id: {eid}")
            seen_ids.add(eid)
            signature = _signature(entry)
            dest[signature].append(entry)
            observations.append({"id": eid, "family_id": family,
                                 "pattern": _key(signature), "role": kind,
                                 "source_ref": entry.get("source_ref"),
                                 "source_check": entry.get("source_check")})

    proposals = []
    preflight = []
    for signature, matching in sorted(groups.items()):
        families = sorted({x["family_id"].strip() for x in matching})
        if len(families) < 2:
            continue
        key = _key(signature)
        counter_ids = sorted(e["id"] for e in contrary.get(signature, []))
        # This wording is intentionally generic: domain-specific meaning and
        # clinical correctness are NOT inferred by this deterministic program.
        label = f"{signature[0].replace('_', ' ')} → {signature[1].replace('_', ' ')}"
        boundary = ("Candidate shared inference only; require "
                    f"{signature[2].replace('_', ' ')}. Domain-specific criteria "
                    "and exceptions must be independently reviewed.")
        proposals.append({"id": key, "pattern": key, "label": label,
                          "boundary": boundary,
                          "support_ids": sorted(e["id"] for e in matching),
                          "acknowledged_counterexample_ids": []})
        preflight.append({"id": key, "signature": dict(zip(SIGNATURE_FIELDS, signature)),
                          "families": families,
                          "challenge_status": ("OPEN_COUNTEREXAMPLE" if counter_ids
                                               else "COUNTEREXAMPLE_NOT_OBSERVED"),
                          "challenge_ids": counter_ids,
                          "abstracted_by": "STRUCTURAL_CLUSTER_NOT_SEMANTIC_PROOF"})

    checked = evaluate({"observations": observations, "proposals": proposals,
                        "dependencies": dependencies})
    # No scoped descendant without a proposed parent. Keep the original
    # skeptical parent gate in place; this does not authorize promotion.
    valid_parent_ids = {proposal["id"] for proposal in proposals}
    refinements = [item for item in scoped_refinements(groups, contrary)
                   if item["parent_candidate"] in valid_parent_ids]
    return {"schema": "ale-recursive-discovery-v0",
            "origin": "STRUCTURED_PUBLIC_EVIDENCE_PROPOSAL",
            "proposal_count": len(proposals),
            "candidate_preflight": preflight,
            "recursive_scope_refinements": refinements,
            "gate": checked,
            "next_step": "independent semantic and source verification; resolve adversarial cases",
            "external_model_calls": 0,
            "promotions_performed": 0,
            "personal_state_accessed": False}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    opts = ap.parse_args()
    print(json.dumps(discover(json.loads(opts.input.read_text(encoding="utf-8"))),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
