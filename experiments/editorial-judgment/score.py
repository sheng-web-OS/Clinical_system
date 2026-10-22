#!/usr/bin/env python3
"""Summarize independently adjudicated editorial decisions. No automated medical judgment."""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def ratio(a, b):
    return None if b == 0 else round(a / b, 3)


def score(cases, evaluations):
    allowed = {c["id"]: c for c in cases["cases"] if c["status"] == "replayable"}
    seen = set()
    by_arm = defaultdict(list)
    for r in evaluations["judgments"]:
        key = (r["arm"], r["id"])
        if key in seen:
            raise ValueError("Duplicate arm + case evaluation: " + str(key))
        seen.add(key)
        if r["id"] not in allowed:
            raise ValueError("Only frozen replayable cases may enter scores: " + r["id"])
        for f in ("tp_major", "fn_major", "tp_material", "fn_material", "false_positives",
                  "source_claims", "supported_source_claims", "human_minutes", "human_turns"):
            v = r[f]
            if type(v) not in (int, float) or v < 0:
                raise ValueError("Expected non-negative number: " + f)
        for f in ("correct_decision_and_scope", "over_revision", "new_p0_p1",
                  "contaminated"):
            if type(r[f]) is not bool:
                raise ValueError("Expected boolean: " + f)
        if r["over_revision"] and r["correct_decision_and_scope"]:
            raise ValueError("An over-revision cannot be a correct edit scope")
        if r["tp_major"] > r["tp_material"] or r["fn_major"] > r["fn_material"]:
            raise ValueError("Major issues must be a subset of material issues")
        if r["supported_source_claims"] > r["source_claims"]:
            raise ValueError("Supported source claims exceed claimed reads")
        if set(r["stages"]) != {"N", "X", "C", "V"} or any(
            type(x) is not int or x not in (0, 1, 2) for x in r["stages"].values()
        ):
            raise ValueError("Stages N/X/C/V must each be integers 0..2")
        by_arm[r["arm"]].append(r)
    report = {}
    for arm, rows in by_arm.items():
        independent = [r for r in rows if not r["contaminated"]]
        total = len(independent)
        if not total:
            report[arm] = {"status": "NO_INDEPENDENT_EVIDENCE", "attempted": len(rows)}
            continue
        summation = lambda k: sum(r[k] for r in independent)
        m_tp, m_fn = summation("tp_major"), summation("fn_major")
        all_tp, all_fn = summation("tp_material"), summation("fn_material")
        fp = summation("false_positives")
        claims, supported = summation("source_claims"), summation("supported_source_claims")
        control = [r for r in independent if allowed[r["id"]]["type"] == "negative-control"]
        new_major = sum(r["new_p0_p1"] for r in independent)
        # Aggregates must not conceal major omissions or newly introduced harm.
        # This is a conservative test gate, not a clinical safety certificate.
        on_hold = bool(m_fn or new_major)
        report[arm] = {
            "status": "PILOT_HOLD" if on_hold else "PILOT_ONLY",
            "safety_gate": "HOLD" if on_hold else "NOT_VALIDATED",
            "hold_reasons": {"missed_major": m_fn, "introduced_p0_p1": new_major},
            "generalization": "NOT_TESTED_RETROSPECTIVE_SEEDS",
            "cases": total,
            "eligible_replayable_cases": len(allowed),
            "case_coverage": ratio(total, len(allowed)),
            "major_recall": ratio(m_tp, m_tp + m_fn),
            "material_recall": ratio(all_tp, all_tp + all_fn),
            "finding_precision": ratio(all_tp, all_tp + fp),
            "correct_decision_and_scope": ratio(sum(r["correct_decision_and_scope"] for r in independent), total),
            "negative_control_overrevision": ratio(sum(r["over_revision"] for r in control), len(control)),
            "all_case_overrevision": ratio(sum(r["over_revision"] for r in independent), total),
            "evidence_claim_support": ratio(supported, claims),
            "new_p0_p1_cases": new_major,
            "human_correction_minutes": summation("human_minutes"),
            "human_intervention_turns": summation("human_turns"),
            "stage_means": {k: ratio(sum(r["stages"][k] for r in independent), total)
                            for k in ("N", "X", "C", "V")},
            "denominators": {
                "major_expected": m_tp + m_fn, "material_expected": all_tp + all_fn,
                "substantive_findings": all_tp + fp, "source_claims": claims,
                "negative_controls": len(control)
            },
            "note": "Human adjudication supplied TP/FP; this script does not check clinical truth."
        }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--judgments", type=Path, required=True)
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text(encoding="utf8"))
    evaluations = json.loads(args.judgments.read_text(encoding="utf8"))
    print(json.dumps(score(cases, evaluations), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
