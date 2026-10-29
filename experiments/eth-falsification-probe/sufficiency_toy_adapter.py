#!/usr/bin/env python3
"""Synthetic, deterministic example ONLY: never a language model or clinical judge.

Reads actual case text and semantic option descriptions; supports --relabel.
The source is public, so it is a development fixture, not a blind benchmark.
"""
import json
import sys


def find_option(options, phrase):
    ids = [k for k, value in options.items() if phrase in value]
    if len(ids) != 1:
        raise ValueError("Ambiguous synthetic option: " + phrase)
    return ids[0]


def main():
    p = json.load(sys.stdin)
    case = p["case_text"]
    if "verified: signed by the submitter" in case:
        label, support = "Transfer because", "sufficient"
    elif "verified: the document is not signed" in case:
        label, support = "Hold because", "sufficient"
    elif "status unknown: no reliable signature" in case:
        label, support = "Request signature-status", "insufficient"
    else:
        raise ValueError("Fixture not recognized")
    question = find_option(p["candidate_questions"], "signature status?")
    decision = find_option(p["candidate_decisions"], label)
    # The controlled case declares the signature record before the cover color.
    evidence = p["available_evidence_ids"]
    used = [e for e in evidence if ("[" + e + "]") in case.split(". The document's cover color", 1)[0]]
    if len(used) != 1:
        raise ValueError("Missing evidence marker")
    print(json.dumps({"probe_id": p["probe_id"],
                      "packet_sha256": p["packet_sha256"],
                      "question_id": question,
                      "evidence_ids": used,
                      "decision_id": decision,
                      "support_status": support,
                      "review_flags": []}))


if __name__ == "__main__":
    main()
