#!/usr/bin/env python3
"""Synthetic content-reading toy, not an LLM or clinical decision-maker.

The adapter reads option descriptions and fact values rather than fixed IDs.
"""
import json
import re
import sys


def main():
    packet = json.load(sys.stdin)
    text = packet["case_text"]
    signature = re.search(r"\[([A-Za-z][A-Za-z0-9_-]+)\] "
                          r"(signed by its submitter|missing a signature)", text)
    if not signature:
        raise ValueError("no signed/missing signature fact")
    evidence_id, state = signature.groups()
    questions = packet["candidate_questions"]
    decisions = packet["candidate_decisions"]
    relevant = [k for k,v in questions.items() if "signature" in v.lower() or "signed" in v.lower()]
    accepts = [k for k,v in decisions.items() if "accept" in v.lower()]
    holds = [k for k,v in decisions.items() if "hold" in v.lower()]
    if len(relevant) != 1 or len(accepts) != 1 or len(holds) != 1:
        raise ValueError("ambiguous fictional options")
    print(json.dumps({
        "probe_id": packet["probe_id"],
        "packet_sha256": packet["packet_sha256"],
        "question_id": relevant[0],
        "evidence_ids": [evidence_id],
        "decision_id": accepts[0] if state.startswith("signed") else holds[0],
        "review_flags": [],
    }))


if __name__ == "__main__":
    main()
