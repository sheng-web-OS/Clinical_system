#!/usr/bin/env python3
"""Score frozen paired MedEinst diagnoses, NEVER infer or grade clinical reasoning.

Only a facilitator with a protected answer key invokes this tool. Inputs and
per-case predictions must not be stored in a public repository or CI artifact.
No provider calls, expert certification, or model verification are performed.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import re

from prepare_medeinst_holdout import HoldoutError, MEDEINST_TEST_SHA256, require

HEX = re.compile(r"[0-9a-f]{64}\Z")
SLOT = re.compile(r"s_[0-9a-f]{24}\Z")
CASE = re.compile(r"M[0-9]{2}\Z")
ARMS = ("native", "retrieval", "skill")


def read_frozen(path, expected_sha):
    require(type(expected_sha) is str and HEX.fullmatch(expected_sha),
            "EXPECTED_FROZEN_FILE_SHA_REQUIRED")
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "FROZEN_FILE_MISSING")
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == expected_sha, "FROZEN_FILE_CHANGED")
    try:
        return json.loads(data)
    except (ValueError, UnicodeError):
        raise HoldoutError("INVALID_FROZEN_JSON") from None


def normalize_label(value):
    # Exact case/whitespace normalization only. Disease synonyms need a
    # separately blinded, qualified adjudicator BEFORE answer key release.
    require(type(value) is str and 0 < len(value.strip()) <= 180,
            "MISSING_OR_UNMAPPED_DIAGNOSIS")
    return " ".join(value.casefold().split())


def score(gold, crosswalk, submission):
    """Three-arm structural/label score. No independent medical validity."""
    require(type(gold) is dict and gold.get("schema_version") == 1
            and type(gold.get("entries")) is dict and gold["entries"],
            "INVALID_GOLD_KEY")
    require(type(crosswalk) is dict
            and crosswalk.get("private_crosswalk_only") is True
            and crosswalk.get("medical_gold_loaded") is False
            and type(crosswalk.get("cases")) is list
            and crosswalk["cases"],
            "INVALID_PRIVATE_CROSSWALK")
    require(type(submission) is dict
            and submission.get("schema_version") == 1
            and submission.get("exposure") == "development"
            and type(submission.get("records")) is list,
            "INVALID_FROZEN_PREDICTIONS")
    require(crosswalk.get("source_sha256") == gold.get("dataset_sha256"),
            "SOURCE_DIGEST_CROSSWALK_MISMATCH")
    if crosswalk.get("source_class") == "MedEinst_DDXPlus_simulated_research_case":
        require(gold.get("dataset_sha256") == MEDEINST_TEST_SHA256,
                "OFFICIAL_SOURCE_DIGEST_UNVERIFIED")
    else:
        require(crosswalk.get("source_class") == "synthetic_fixture_not_medeinst",
                "UNRECOGNIZED_SOURCE_CLASS")
    require(set(gold["entries"]) == {x.get("worker_slot") for x in crosswalk["cases"]},
            "MISSING_OR_EXTRA_GOLD_SLOT")
    mapping, by_pair = {}, defaultdict(dict)
    for item in crosswalk["cases"]:
        require(type(item) is dict and set(item) == {
            "case_id", "worker_slot", "packet_sha256"
        }, "INVALID_CROSSWALK_ENTRY")
        cid, slot, digest = item["case_id"], item["worker_slot"], item["packet_sha256"]
        require(type(cid) is str and CASE.fullmatch(cid)
                and type(slot) is str and SLOT.fullmatch(slot)
                and type(digest) is str and HEX.fullmatch(digest)
                and cid not in mapping, "DUPLICATE_OR_INVALID_CASE_SLOT")
        entry = gold["entries"][slot]
        require(type(entry) is dict
                and entry.get("packet_sha256") == digest
                and type(entry.get("case_id")) is str and bool(entry["case_id"])
                and entry.get("variant") in ("control", "trap"),
                "GOLD_CROSSWALK_BINDING_MISMATCH")
        label = normalize_label(entry.get("ground_truth"))
        variants = by_pair[entry["case_id"]]
        require(entry["variant"] not in variants, "DUPLICATE_PAIR_VARIANT")
        variants[entry["variant"]] = (cid, label)
        mapping[cid] = (entry["case_id"], entry["variant"], label)
    require(all(set(v) == {"control", "trap"}
                and v["control"][1] != v["trap"][1]
                for v in by_pair.values()), "UNPAIRED_OR_SAME_LABEL_GOLD")
    require(len(mapping) >= 2 and len(mapping) % 2 == 0,
            "NO_COMPLETE_PAIRED_CASES")
    records, contexts = {}, set()
    expected = {(cid, arm) for cid in mapping for arm in ARMS}
    require(len(submission["records"]) == len(expected),
            "INCOMPLETE_ARM_CASE_MATRIX")
    for rec in submission["records"]:
        require(type(rec) is dict and set(rec) == {
            "case_id", "arm", "attempt_status", "diagnosis",
            "first_pass_sha256", "worker_context"
        }, "INVALID_PREDICTION_RECORD")
        cid, arm = rec["case_id"], rec["arm"]
        require(cid in mapping and arm in ARMS and (cid, arm) not in records,
                "UNKNOWN_OR_DUPLICATE_TRIAL")
        require(rec["attempt_status"] == "COMPLETED",
                "INCOMPLETE_MODEL_TRIAL_NO_SCORE")
        require(type(rec["first_pass_sha256"]) is str
                and HEX.fullmatch(rec["first_pass_sha256"]),
                "FIRST_PASS_RECEIPT_MISSING")
        context = rec["worker_context"]
        require(type(context) is str and bool(context.strip())
                and len(context) <= 180 and context not in contexts,
                "WORKER_CONTEXT_NOT_UNIQUE")
        contexts.add(context)
        prediction = normalize_label(rec["diagnosis"])
        records[cid, arm] = prediction
    require(set(records) == expected, "MISSING_ARM_CASE_PAIR")

    results = {}
    for arm in ARMS:
        baseline, robust, bias_trap, control_correct = 0, 0, 0, 0
        trap_correct = 0
        for pair in by_pair.values():
            ctrl_id, ctrl_gold = pair["control"]
            trap_id, trap_gold = pair["trap"]
            predicted_control = records[ctrl_id, arm]
            predicted_trap = records[trap_id, arm]
            ctrl_ok = predicted_control == ctrl_gold
            trap_ok = predicted_trap == trap_gold
            baseline += int(ctrl_ok)
            trap_correct += int(trap_ok)
            robust += int(ctrl_ok and trap_ok)
            control_correct += int(ctrl_ok)
            # MedEinst R_bias is not 1 - robust accuracy:
            # a wrong trap OTHER than control diagnosis is not a bias trap.
            bias_trap += int(ctrl_ok and predicted_trap == ctrl_gold)
        n = len(by_pair)
        results[arm] = {
            "paired_cases": n,
            "control_correct": baseline,
            "trap_correct": trap_correct,
            "both_correct": robust,
            "control_accuracy": baseline / n,
            "trap_accuracy": trap_correct / n,
            "robust_accuracy": robust / n,
            "bias_trap_numerator": bias_trap,
            "bias_trap_denominator": control_correct,
            "bias_trap_rate": (
                bias_trap / control_correct if control_correct else None
            ),
        }
    return {
        "schema_version": 1,
        "source_class": crosswalk["source_class"],
        "source_sha256": gold["dataset_sha256"],
        "denominator_pairs": len(by_pair),
        "arm_results": results,
        "skill_minus_retrieval_robust_accuracy": (
            results["skill"]["robust_accuracy"] - results["retrieval"]["robust_accuracy"]
        ),
        "all_arm_inputs_and_response_hashes_authenticated": False,
        "clinical_expert_review_verified": False,
        "medical_gold_accepted_as_clinical_truth": False,
        "model_execution_verified": False,
        "owner_time_verified": False,
        "skill_transfer_validated": False,
        "promotion_authorized": False,
        "status": "DEVELOPMENT_LABEL_MATCH_ONLY",
        "warning": ("Published synthetic benchmark label agreement is not expert "
                    "clinical adjudication. Exact-label mapping is conservative, "
                    "and provider/runtime claims are unauthenticated."),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gold", required=True, type=Path)
    p.add_argument("--gold-sha256", required=True)
    p.add_argument("--crosswalk", required=True, type=Path)
    p.add_argument("--crosswalk-sha256", required=True)
    p.add_argument("--frozen-predictions", required=True, type=Path)
    p.add_argument("--predictions-sha256", required=True)
    a = p.parse_args()
    report = score(
        read_frozen(a.gold, a.gold_sha256),
        read_frozen(a.crosswalk, a.crosswalk_sha256),
        read_frozen(a.frozen_predictions, a.predictions_sha256),
    )
    # Only aggregate counters and rates, no narratives, per-case labels,
    # case IDs, prompts, response content, or worker contexts.
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
