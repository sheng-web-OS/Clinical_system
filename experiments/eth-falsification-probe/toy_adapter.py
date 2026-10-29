#!/usr/bin/env python3
"""Deterministic fictional routing toy. NOT A LANGUAGE MODEL OR MEDICAL ORACLE.

Input: one blinded packet as JSON on stdin. Output: one response object on stdout.
No gold file, model API, network or credentials are used.
"""
import json
import sys


def main():
    packet = json.load(sys.stdin)
    is_signed = "[F1] signed by its submitter" in packet["case_text"]
    print(json.dumps({
        "probe_id": packet["probe_id"],
        "packet_sha256": packet["packet_sha256"],
        "question_id": "q_signature",
        "evidence_ids": ["F1"],
        "decision_id": "accept" if is_signed else "hold",
        "review_flags": [],
    }))


if __name__ == "__main__":
    main()
