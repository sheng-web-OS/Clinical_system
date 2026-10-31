#!/usr/bin/env python3
"""Bounded ALE Q0 discovery from unlabelled, public-source text fragments.

This is a lexical hypothesis generator, not a medical semantic parser,
source verifier, taxonomy creator, or user/Anki reader. It receives NO concept
IDs, edge types or prioritization labels. All candidates require real Q2/Q3
semantic review; never promote knowledge based on a cue or word overlap.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

EXPECTED = {"source_classification", "source_ref", "excerpt"}
PUBLIC_SOURCE = re.compile(r"pmid_[1-9][0-9]{6,8}\Z")
# Any supplied classification is an input assertion, NOT authorization
# to send private material to a public GitHub Action.
SENTENCES = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")
CUES = (
    # Clinical role contrast can omit ordinary 'cannot/despite' wording.
    # This is a QUESTION CUE only; no causal relation or diagnostic rule is inferred.
    ("MEASUREMENT_ROLE_SPLIT", re.compile(
        r"\bnot\s+(?:primarily\s+)?for\b.{0,110}?\bbut\s+(?:to|for)\b",
        re.IGNORECASE), 5),
    # A measurement can be biased even when it is not a screening criterion.
    ("MEASUREMENT_VALIDITY_RISK", re.compile(
        r"\b(?:may|can|could)\s+(?:lead\s+to|cause|yield|produce|result\s+in)"
        r"\s+(?:(?:an?|the)\s+)?(?:falsely\s+(?:low|high)|"
        r"false[- ](?:positive|negative))\b", re.IGNORECASE), 4),
    ("APPARENT_CONTRAST", re.compile(
        r"\b(?:despite|although|even though|whereas|nevertheless|however)\b",
        re.IGNORECASE), 4),
    ("INFERENCE_BOUNDARY", re.compile(
        r"\b(?:cannot|does not|do not|not necessarily|insufficient|not alone|"
        r"not always|doesn't|cannot be inferred)\b", re.IGNORECASE), 3),
    ("CONDITION_DEPENDENCE", re.compile(
        r"\b(?:depends on|may vary|differs? depending|only when|"
        r"only if|unless|in contrast)\b", re.IGNORECASE), 2),
    ("RECLASSIFICATION_SIGNAL", re.compile(
        r"\b(?:previously termed|historically labeled|historically termed|"
        r"renamed|new nomenclature|instead of)\b", re.IGNORECASE), 3),
)
EDITORIAL_ONLY = re.compile(
    r"\b(?:copyright|downloaded|page count|author list|"
    r"website layout|publication date|published online|"
    r"not for publication|editorial approval)\b", re.IGNORECASE
)
PRIVATE_HINT = re.compile(
    r"\b(?:anki|card[_ -]?id|note[_ -]?id|patient[_ -]?id|"
    r"medical[_ -]?record[_ -]?number|oauth|password|private[_ -]?sheet)\b",
    re.IGNORECASE
)
URL_OR_EMAIL = re.compile(r"https?://|www\.|\S+@\S+", re.IGNORECASE)
QUESTIONS = {
    "MEASUREMENT_ROLE_SPLIT":
        "Which decision is this observation NOT intended to make, and which separate interpretation does it support?",
    "MEASUREMENT_VALIDITY_RISK":
        "What threatens measurement validity, and which condition might require a repeat or alternative measurement?",
    "APPARENT_CONTRAST":
        "What unspoken premise makes both apparently conflicting states possible?",
    "INFERENCE_BOUNDARY":
        "Which missing premise prevents the claimed inference from following?",
    "CONDITION_DEPENDENCE":
        "Under which specific condition would the inference change?",
    "RECLASSIFICATION_SIGNAL":
        "What distinction in mechanism or scope motivated the revised terminology?",
}

def extract(packet: dict) -> dict:
    if type(packet) is not dict or set(packet) != EXPECTED:
        raise ValueError("invalid source packet: raw public excerpt and citation only")
    if packet["source_classification"] != "PUBLIC_SOURCE_EXCERPT":
        raise ValueError("owner-private or unclassified material forbidden")
    source = packet["source_ref"]
    body = packet["excerpt"]
    if type(source) is not str or PUBLIC_SOURCE.fullmatch(source) is None:
        raise ValueError("source must be a public PMID identifier")
    if (type(body) is not str or not 24 <= len(body) <= 3000
            or URL_OR_EMAIL.search(body) or PRIVATE_HINT.search(body)
            or any(ord(ch) < 32 and ch not in "\n\t" for ch in body)):
        raise ValueError("invalid or potentially private source excerpt")
    candidates = []
    for match in SENTENCES.finditer(body):
        raw = match.group()
        sentence = raw.strip()
        if not sentence or len(sentence.split()) < 7 or EDITORIAL_ONLY.search(sentence):
            continue
        hits = [(name, value) for name, pattern, value in CUES
                if pattern.search(sentence)]
        if not hits:
            continue
        kind, weight = sorted(hits, key=lambda x:(-x[1], x[0]))[0]
        # The gap is QUESTION-LEVEL only; no ontology node is declared.
        candidates.append({
            "source_ref": source, "start_char": match.start() + len(raw)-len(raw.lstrip()),
            "end_char": match.end() - (len(raw)-len(raw.rstrip())),
            "exact_evidence": sentence,
            "cue": kind, "cue_count": len(hits),
            "lexical_attention": weight + min(2, len(hits)-1),
            "proposed_q0": QUESTIONS[kind],
            "needs_semantic_source_review": True,
            "concept_novelty_verified": False,
            "concept_relation_inferred": False,
        })
    candidates.sort(key=lambda c:(-c["lexical_attention"],c["start_char"]))
    return {
        "schema":"ale-raw-q0-probe-v0",
        "source_classification":"PUBLIC_SOURCE_EXCERPT",
        "source_ref":source,
        "source_provenance_checked_by_program":False,
        "concept_ids_received":False,
        "relation_roles_received":False,
        "priority_labels_received":False,
        "top_candidate":candidates[0] if candidates else None,
        "candidates":candidates[:8],
        "decision":"ASK_ONE_Q0_PENDING_Q2_Q3" if candidates else "ABSTAIN_NO_BOUNDARY_CUE",
        "medical_semantics_verified":False,
        "concept_promotions":0,
        "source_fetch_performed":False,
        "owner_private_data_accessed":False,
    }

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",type=Path,required=True)
    args=ap.parse_args()
    print(json.dumps(extract(json.loads(args.input.read_text(encoding="utf-8"))),
                     ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
