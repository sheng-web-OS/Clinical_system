"""Summarize complete DEVELOPMENT trials; never certify clinical truth or release."""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def number_or_none(value, name, integer=False):
    if value is None:
        return
    require(type(value) in ((int,) if integer else (int, float)),
            name + " must be a number or null, not a boolean")
    require(math.isfinite(value) and value >= 0, name + " must be finite and nonnegative")


def ratio(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "rate": numerator / denominator if denominator else None}


def summarize(suite, run, suite_digest):
    require(type(suite.get("schema_version")) is int and suite["schema_version"] == 1
            and type(run.get("schema_version")) is int and run["schema_version"] == 1,
            "unsupported schema version")
    require(isinstance(suite.get("suite_id"), str) and bool(suite["suite_id"].strip()),
            "suite_id must be a nonempty identifier")
    require(suite.get("exposure") == "development",
            "this tool only summarizes visible development cases, not held-out validation")
    require(run.get("suite_id") == suite.get("suite_id")
            and run.get("suite_sha256") == suite_digest,
            "suite identity/hash mismatch; do not relabel results after changing cases")
    require(re.fullmatch(r"[0-9a-f]{40}", run.get("candidate_sha", "")) is not None,
            "candidate_sha must identify the tested commit")
    for field in ("run_id", "arm", "model"):
        require(isinstance(run.get(field), str) and bool(run[field].strip()),
                "missing " + field)

    cases = suite.get("cases")
    require(isinstance(cases, list) and bool(cases), "missing cases")
    by_id = {}
    for case in cases:
        require(isinstance(case, dict), "invalid case")
        ident = case.get("id")
        require(isinstance(ident, str) and ident and ident == ident.strip() and ident not in by_id,
                "missing or duplicate case id")
        require(type(case.get("defect_present")) is bool, "invalid defect label")
        by_id[ident] = case
    require({case["defect_present"] for case in cases} == {False, True},
            "both normal controls and defective cases are required")

    trials = run.get("trial_ids")
    require(isinstance(trials, list) and len(trials) >= 3
            and all(isinstance(x, str) and x and x == x.strip() for x in trials)
            and len(set(trials)) == len(trials),
            "at least three distinct planned trial ids are required")
    expected = {(case_id, trial) for case_id in by_id for trial in trials}
    records = run.get("records")
    require(isinstance(records, list), "missing trial records")
    indexed = {}
    worker_trials, trace_trials = set(), set()
    for record in records:
        require(isinstance(record, dict), "invalid trial record")
        key = (record.get("case_id"), record.get("trial_id"))
        require(key in expected and key not in indexed, "unknown or duplicate trial")
        indexed[key] = record
        for field in ("flagged", "located", "first_pass", "final_pass", "hinted"):
            require(type(record.get(field)) is bool, "missing/invalid " + field)
        require(not record["hinted"],
                "location-hinted trials cannot estimate autonomous discovery")
        worker, reviewer = record.get("worker_context"), record.get("reviewer_context")
        require(isinstance(worker, str) and bool(worker.strip())
                and isinstance(reviewer, str) and bool(reviewer.strip())
                and worker.strip() != reviewer.strip(),
                "author and adjudicating reviewer contexts must be declared separately")
        require(isinstance(record.get("trace_ref"), str) and bool(record["trace_ref"].strip()),
                "missing trace reference")
        worker_trial = (key[0], worker.strip())
        trace_trial = (key[0], record["trace_ref"].strip())
        require(worker_trial not in worker_trials,
                "independent trials for one case cannot reuse a worker context")
        require(trace_trial not in trace_trials,
                "independent trials for one case cannot reuse a trace reference")
        worker_trials.add(worker_trial)
        trace_trials.add(trace_trial)
        for field in ("owner_minutes", "owner_interruptions", "hard_failures", "attempts"):
            require(field in record, "missing " + field + "; use null for unmeasured owner cost")
        number_or_none(record["owner_minutes"], "owner_minutes")
        number_or_none(record["owner_interruptions"], "owner_interruptions", integer=True)
        for field in ("hard_failures", "attempts"):
            require(type(record[field]) is int and record[field] >= (1 if field == "attempts" else 0),
                    "invalid " + field)
        require(not record["located"] or record["flagged"], "location without a finding")
        bad = by_id[key[0]]["defect_present"]
        if bad:
            require(type(record.get("repair_pass")) is bool, "defective trial needs repair verdict")
            require(not record["repair_pass"] or record["located"],
                    "repair credit requires independently located original defect")
            require(not record["final_pass"] or record["repair_pass"],
                    "final success contradicts failed repair")
        else:
            require(record.get("repair_pass") is None and not record["located"],
                    "normal control cannot receive defect-location or repair credit")
        require(not record["first_pass"] or record["final_pass"],
                "first-pass success contradicts final failure")
        if record["first_pass"]:
            require(record["attempts"] == 1 and record["hard_failures"] == 0
                    and (record["located"] and record["repair_pass"] if bad else not record["flagged"]),
                    "first-pass credit contradicts retries, safety or discovery verdict")
        require(not record["final_pass"] or record["hard_failures"] == 0,
                "hard safety failures cannot be certified as final success")
    require(set(indexed) == expected,
            "incomplete planned trials; include failed/crashed trials, never drop them")

    bad_records = [r for (case_id, _), r in indexed.items() if by_id[case_id]["defect_present"]]
    normal_records = [r for (case_id, _), r in indexed.items() if not by_id[case_id]["defect_present"]]
    detected = sum(r["located"] for r in bad_records)
    repaired = sum(r["repair_pass"] for r in bad_records)
    success = {}
    for (case_id, trial), record in indexed.items():
        decision_correct = record["located"] if by_id[case_id]["defect_present"] else not record["flagged"]
        success[(case_id, trial)] = record["final_pass"] and decision_correct and record["hard_failures"] == 0
    final_successes = sum(success.values())
    minutes = [r["owner_minutes"] for r in records if r["owner_minutes"] is not None]
    interruptions = [r["owner_interruptions"] for r in records if r["owner_interruptions"] is not None]
    all_minutes = len(minutes) == len(records)
    all_interruptions = len(interruptions) == len(records)
    hard_failures = sum(r["hard_failures"] for r in records)
    return {
        "run_id": run["run_id"], "candidate_sha": run["candidate_sha"],
        "suite_id": suite["suite_id"], "suite_sha256": suite_digest,
        "arm": run["arm"], "model": run["model"],
        "evidence_level": "DEVELOPMENT_ONLY",
        "autonomy_validated": False, "learning_effect_validated": False,
        "release_approval": False,
        "review_independence": "DECLARED_NOT_AUTHENTICATED",
        "planned_trials": len(expected), "trials_per_case": len(trials),
        "autonomous_discovery": ratio(detected, len(bad_records)),
        "false_positive": ratio(sum(r["flagged"] for r in normal_records), len(normal_records)),
        "repair_including_discovery_failures": ratio(repaired, len(bad_records)),
        "repair_given_correct_discovery": ratio(repaired, detected),
        "first_pass": ratio(sum(r["first_pass"] for r in records), len(records)),
        "end_to_end_success": ratio(final_successes, len(records)),
        "cases_with_any_success": ratio(sum(any(success[(c, t)] for t in trials) for c in by_id), len(by_id)),
        "cases_with_all_trials_successful": ratio(sum(all(success[(c, t)] for t in trials) for c in by_id), len(by_id)),
        "hard_failures": hard_failures,
        "quality_guard": "HOLD" if hard_failures else "NO_HARD_FAILURE_OBSERVED",
        "owner_attention": {
            "minutes_status": "MEASURED" if all_minutes else "NOT_MEASURED",
            "minutes_coverage": ratio(len(minutes), len(records)),
            "observed_minutes_total": sum(minutes) if minutes else None,
            "minutes_per_successful_trial": sum(minutes) / final_successes if all_minutes and final_successes else None,
            "interruptions_status": "MEASURED" if all_interruptions else "NOT_MEASURED",
            "interruptions_coverage": ratio(len(interruptions), len(records)),
            "observed_interruptions_total": sum(interruptions) if interruptions else None,
        },
        "limitations": [
            "Verdicts and trace references are supplied by the evaluator, not authenticated by this tool.",
            "Visible cases and repeated trials are regression evidence, not hidden-case generalization or rare-risk bounds.",
            "No comparison, improvement percentage, clinical truth or human learning effect is inferred.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    args = parser.parse_args()
    try:
        raw = args.suite.read_bytes()
        suite = json.loads(raw)
        run = json.loads(args.results.read_text("utf-8"))
        result = summarize(suite, run, hashlib.sha256(raw).hexdigest())
    except (OSError, ValueError, TypeError, AttributeError) as error:
        parser.exit(2, "INVALID_EVALUATION: " + str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 1 if result["quality_guard"] == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())

