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
    return {"schema": "ale-recursive-discovery-v0",
            "origin": "STRUCTURED_PUBLIC_EVIDENCE_PROPOSAL",
            "proposal_count": len(proposals),
            "candidate_preflight": preflight,
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
