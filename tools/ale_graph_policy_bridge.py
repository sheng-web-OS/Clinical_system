#!/usr/bin/env python3
"""Read-only public-safe fixture for graph-aware ALE intervention proposals.

Pure adapter only: no Anki/Drive access, semantic NLP, source verification,
learner profiling, mastery claims, or writes. Real private event processing
must remain exclusively in authorized private execution contexts.
"""
from __future__ import annotations

import re

ID = re.compile(r"[a-z][a-z0-9_-]{1,63}\Z")
KINDS = {"ENTITY", "INFERENCE"}
STATUS = {"SOURCE_REVIEWED", "CANDIDATE"}
RELATIONS = {"REQUIRES", "RELATED", "TESTS"}
BASIS = {"COLD_REASONED_ANSWER", "DELAYED_REASONED_RECALL",
         "READING_RECALL", "REVIEW_BUTTON_ONLY", "TAG_ONLY"}
FINDINGS = {"INCORRECT_REASONING", "RETRIEVAL_FAILURE", "REASONED_PASS",
            "TRANSFER_PASS", "UNOBSERVED"}


def _token(value):
    return type(value) is str and ID.fullmatch(value) is not None


def propose(graph: dict, observation: dict) -> dict:
    """Offer one reversible next action using caller-supplied public-safe roles.

    The policy illustrates compatibility with a typed Concept Family;
    every source/learning-status assertion is unverified at this boundary.
    """
    if type(graph) is not dict or set(graph) != {"classification", "version", "nodes", "edges"}:
        raise ValueError("invalid graph contract")
    if graph["classification"] != "PUBLIC_SYNTHETIC_ONLY":
        raise ValueError("private or non-fixture graph rejected")
    if type(graph["version"]) is not int or graph["version"] < 1:
        raise ValueError("invalid graph version")
    if type(graph["nodes"]) is not list or len(graph["nodes"]) > 24:
        raise ValueError("invalid node collection")
    if type(graph["edges"]) is not list or len(graph["edges"]) > 64:
        raise ValueError("invalid edge collection")
    nodes = {}
    for n in graph["nodes"]:
        if type(n) is not dict or set(n) != {"id", "kind", "status"}:
            raise ValueError("unexpected node fields")
        if not _token(n["id"]) or n["id"] in nodes or n["kind"] not in KINDS or n["status"] not in STATUS:
            raise ValueError("invalid or duplicate node")
        nodes[n["id"]] = n
    for e in graph["edges"]:
        if type(e) is not dict or set(e) != {"from", "to", "relation", "status"}:
            raise ValueError("unexpected edge fields")
        if e["from"] not in nodes or e["to"] not in nodes or e["relation"] not in RELATIONS or e["status"] not in STATUS:
            raise ValueError("invalid edge")
    if type(observation) is not dict or set(observation) != {
            "classification", "target_id", "graph_version", "basis", "finding"}:
        raise ValueError("invalid learning observation contract")
    if observation["classification"] != "PUBLIC_SYNTHETIC_ONLY":
        raise ValueError("private or non-fixture observation rejected")
    if not _token(observation["target_id"]) or observation["basis"] not in BASIS or observation["finding"] not in FINDINGS:
        raise ValueError("invalid observation role")
    if type(observation["graph_version"]) is not int or observation["graph_version"] < 1:
        raise ValueError("invalid observation graph version")

    target = observation["target_id"]
    action, selected, reason = "ABSTAIN", None, "No reliable inference from available evidence"
    if target not in nodes:
        action, reason = "UNMAPPED_DIAGNOSTIC_FIRST", "No known stable concept identity; never fabricate one from a tag"
    elif observation["graph_version"] != graph["version"]:
        action, reason = "RECHECK_VERSIONED_MAPPING", "Concept graph version changed; preserve old learning evidence"
    elif nodes[target]["status"] != "SOURCE_REVIEWED":
        action, reason = "VERIFY_CONCEPT_SOURCE", "Candidate concept is not eligible for a source-backed learning assertion"
    elif observation["basis"] in {"TAG_ONLY", "REVIEW_BUTTON_ONLY"}:
        action, reason = "DIAGNOSTIC_FIRST", "Tags and review ratings do not establish the learner's reasoning"
    elif observation["finding"] == "INCORRECT_REASONING":
        prerequisites = sorted({e["to"] for e in graph["edges"]
                               if e["from"] == target and e["relation"] == "REQUIRES"
                               and e["status"] == "SOURCE_REVIEWED" and nodes[e["to"]]["status"] == "SOURCE_REVIEWED"})
        if prerequisites:
            action, selected = "REPAIR_PREREQUISITE_CANDIDATE", prerequisites[0]
            reason = "A source-reviewed prerequisite relation provides a candidate intervention; diagnostic confirmation remains necessary"
        else:
            action, reason = "DIAGNOSTIC_FIRST", "Reasoning failure observed, but no supported prerequisite is available"
    elif observation["finding"] == "RETRIEVAL_FAILURE":
        action, selected = "CARD_CANDIDATE", target
        reason = "An observed retrieval failure may justify a small card, subject to worthiness and workload checks"
    elif observation["finding"] == "TRANSFER_PASS":
        action, reason = "NO_CARD", "Observed transfer supports withholding an unnecessary new card; delayed retention still unknown"
    elif observation["finding"] == "REASONED_PASS":
        action, reason = "UNSEEN_TRANSFER_TEST", "Reasoned correctness alone does not establish transfer"
    return {
        "schema": "ale-graph-policy-bridge-v0", "graph_version": graph["version"],
        "target_id": target, "action": action, "selected_concept_id": selected,
        "reason": reason, "basis": observation["basis"],
        "policy_status": "DETERMINISTIC_UNVALIDATED_SHADOW",
        "caller_evidence_independently_verified": False,
        "learner_gain": "NOT_MEASURED", "graph_mutations": 0,
        "anki_mutations": 0, "private_data_processed": False,
    }
