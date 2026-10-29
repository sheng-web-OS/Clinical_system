#!/usr/bin/env python3
"""Descriptive MedEinst paired-case audit. Not a diagnosis or clinical validator.

Only aggregate counts are ever printed. No raw narratives, identifiers, diagnoses,
patient records, benchmark keys, or per-case scores are written to artifacts.
"""
import argparse
from collections import Counter
from difflib import SequenceMatcher
import json
from pathlib import Path

from prepare_medeinst_holdout import (
    HoldoutError, MEDEINST_TEST_SHA256, MAX_LINE_BYTES, file_digest, require
)

EXPECTED_OFFICIAL_PAIRS = 5383


def audit(path, expected_sha256, mode="official-medeinst"):
    """Return aggregate structural and text-overlap diagnostics, fail closed.

    Diagnostic similarity is not proof of a valid single-fact intervention.
    """
    require(mode in ("official-medeinst", "synthetic-fixture"),
            "UNKNOWN_AUDIT_SOURCE_MODE")
    if mode == "official-medeinst":
        require(expected_sha256 == MEDEINST_TEST_SHA256,
                "UNTRUSTED_BENCHMARK_SHA256")
    require(file_digest(path) == expected_sha256, "DATASET_DIGEST_MISMATCH")
    records = {}
    counters = Counter()
    with Path(path).open("rb") as source:
        for raw in source:
            require(len(raw) <= MAX_LINE_BYTES, "DATASET_ROW_TOO_LARGE")
            if not raw.strip():
                continue
            try:
                row = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeError):
                raise HoldoutError("INVALID_JSONL") from None
            require(isinstance(row, dict), "INVALID_CASE_RECORD")
            case_id = row.get("case_id")
            kind = row.get("case_type")
            if kind == "control_case":
                kind = "control"
            elif kind == "trap_case":
                kind = "trap"
            narrative = row.get("narrative")
            label = row.get("ground_truth")
            require(type(case_id) is str and bool(case_id)
                    and kind in ("control", "trap")
                    and type(narrative) is str and 30 <= len(narrative) <= MAX_LINE_BYTES
                    and type(label) is str and 0 < len(label) <= 180,
                    "INVALID_AUDIT_RECORD")
            if len(narrative) > 12000:
                counters["narratives_above_worker_limit"] += 1
            pair = records.setdefault(case_id, {})
            require(kind not in pair, "DUPLICATE_PAIR_VARIANT")
            pair[kind] = (narrative, label)
            counters["records"] += 1

    require(records, "EMPTY_DATASET")
    require(all(set(p) == {"control", "trap"} for p in records.values()),
            "INCOMPLETE_DATASET_PAIR")
    if mode == "official-medeinst":
        require(len(records) == EXPECTED_OFFICIAL_PAIRS,
                "OFFICIAL_PAIR_COUNT_UNEXPECTED")

    ratios = []
    # Categories are DESCRIPTIVE screening flags, not evidence of quality.
    for p in records.values():
        c, t = p["control"], p["trap"]
        if c[1].casefold().strip() == t[1].casefold().strip():
            counters["same_diagnosis_label"] += 1
        if c[0].strip() == t[0].strip():
            counters["identical_narrative"] += 1
        if max(len(c[0]), len(t[0])) > 12000:
            counters["pairs_above_worker_limit"] += 1
        # Lexical screening is approximate; autojunk bounds repetitive long narratives.
        ratio = SequenceMatcher(None, c[0], t[0], autojunk=True).ratio()
        ratios.append(ratio)
        if ratio < 0.5:
            counters["overlap_below_0_50"] += 1
        if ratio < 0.8:
            counters["overlap_below_0_80"] += 1

    ratios.sort()
    n = len(ratios)
    output = {
        "schema_version": 1,
        "source_mode": mode,
        "source_sha256": expected_sha256,
        "dataset_records": counters["records"],
        "pairs": n,
        "same_diagnosis_label_pairs": counters["same_diagnosis_label"],
        "identical_narrative_pairs": counters["identical_narrative"],
        "narratives_above_worker_limit": counters["narratives_above_worker_limit"],
        "pairs_above_worker_limit": counters["pairs_above_worker_limit"],
        "worker_length_limit": 12000,
        "lexical_overlap": {
            "minimum": round(ratios[0], 4),
            "p10": round(ratios[(n - 1) // 10], 4),
            "median": round(ratios[(n - 1) // 2], 4),
            "p90": round(ratios[(9 * (n - 1)) // 10], 4),
            "maximum": round(ratios[-1], 4),
            "below_0_50": counters["overlap_below_0_50"],
            "below_0_80": counters["overlap_below_0_80"],
        },
        "anonymized_aggregates_only": True,
        "clinical_counterfactual_validated": False,
        "one_fact_intervention_verified": False,
        "medical_expert_reviewed": False,
        "model_calls": 0,
        "verdict": "STRUCTURAL_AUDIT_ONLY",
    }
    # Repeated diagnoses or literally identical narratives are not credible
    # *diagnostic-flip* controls even if the whole published file matches.
    if counters["pairs_above_worker_limit"]:
        output["verdict"] = "STRUCTURAL_AUDIT_WITH_WORKER_EXCLUSIONS"
    if counters["same_diagnosis_label"] or counters["identical_narrative"]:
        output["verdict"] = "HOLD_DATASET_PAIR_SEMANTICS"
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--source-mode",
                        choices=("official-medeinst", "synthetic-fixture"),
                        default="official-medeinst")
    a = parser.parse_args()
    report = audit(a.dataset, a.expected_sha256, a.source_mode)
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if report["verdict"] not in ("STRUCTURAL_AUDIT_ONLY",
                                 "STRUCTURAL_AUDIT_WITH_WORKER_EXCLUSIONS"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
