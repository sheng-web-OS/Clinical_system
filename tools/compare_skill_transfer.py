#!/usr/bin/env python3
"""Fail-closed paired pilot accounting; not an AI reasoning or medical truth grader."""
import argparse
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ARMS = ("native", "retrieval", "skill")
ROLES = ("transfer", "normal", "boundary")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def evaluate(suite, run, suite_digest):
    require(suite.get("schema_version") == 1
            and run.get("schema_version") == 1
            and suite.get("exposure") == "development",
            "only visible development pilot records are supported")
    require(isinstance(suite.get("id"), str) and suite["id"].strip(),
            "missing fixed suite identifier")
    require(run.get("suite_id") == suite["id"]
            and run.get("suite_sha256") == suite_digest,
            "changed suite or stale answer-key binding")
    require(COMMIT.fullmatch(str(run.get("candidate_commit", ""))),
            "candidate exact Git commit required")
    require(DIGEST.fullmatch(str(suite.get("retrieval_pack_sha256", "")))
            and DIGEST.fullmatch(str(suite.get("candidate_skill_sha256", ""))),
            "frozen retrieval pack and candidate skill fingerprints required")
    cases = suite.get("cases")
    require(isinstance(cases, list) and len(cases) >= 3, "need at least three cases")
    index = {}
    for case in cases:
        require(isinstance(case, dict), "invalid case")
        cid, role = case.get("id"), case.get("role")
        require(isinstance(cid, str) and cid.strip() == cid and cid
                and cid not in index, "missing or duplicate case")
        require(role in ROLES, "unknown case role")
        require(DIGEST.fullmatch(str(case.get("source_sha256", ""))),
                "each case needs frozen source fingerprint")
        index[cid] = case
    require(set(c["role"] for c in cases) == set(ROLES),
            "transfer, normal and non-applicable boundary controls required")
    records = run.get("records")
    require(isinstance(records, list), "missing observed trials")
    expected = {(cid, arm) for cid in index for arm in ARMS}
    found, contexts, traces, reviewer_ids = {}, set(), set(), set()
    for item in records:
        require(isinstance(item, dict), "invalid trial record")
        key = item.get("case_id"), item.get("arm")
        require(key in expected and key not in found, "unknown or duplicate paired trial")
        found[key] = item
        for field in ("decision_correct", "first_pass", "unsafe", "hinted", "false_alarm",
                      "article_retrieval_visible", "candidate_skill_visible",
                      "skill_applied"):
            require(type(item.get(field)) is bool, "missing/invalid bool: " + field)
        require(not item["hinted"], "hinted trial cannot count as autonomous transfer")
        require(item["article_retrieval_visible"] == (key[1] != "native")
                and item["candidate_skill_visible"] == (key[1] == "skill"),
                "arm contamination: article/skill exposure violates comparison design")
        require(item.get("retrieval_pack_sha256") ==
                (suite["retrieval_pack_sha256"] if key[1] != "native" else None),
                "article retrieval pack mismatch or contamination")
        require(item.get("loaded_skill_sha256") ==
                (suite["candidate_skill_sha256"] if key[1] == "skill" else None),
                "candidate skill version mismatch or contamination")
        require(key[1] == "skill" or not item["skill_applied"],
                "skill cannot be applied in native/retrieval controls")
        require(not (index[key[0]]["role"] == "boundary" and item["skill_applied"]),
                "non-applicable boundary wrongly activated skill")
        require(not item["first_pass"] or
                (item["decision_correct"] and not item["unsafe"]),
                "first-pass credit contradicts adjudicated failure")
        if index[key[0]]["role"] == "transfer":
            require(not item["false_alarm"], "false alarm invalid for transfer case")
        else:
            require(not (item["false_alarm"] and item["decision_correct"]),
                    "false alarm contradicts correct control handling")
        require(item.get("source_sha256") == index[key[0]]["source_sha256"],
                "source mismatch among comparison arms")
        for field in ("worker_context", "reviewer_context", "trace_ref", "model",
                      "effort", "tools_scope", "token_budget"):
            require(isinstance(item.get(field), str) and item[field].strip(),
                    "missing trace/config field " + field)
        worker = item["worker_context"].strip()
        require(worker not in contexts, "worker context reused across trials")
        contexts.add(worker)
        reviewer_ids.add(item["reviewer_context"].strip())
        require(item["trace_ref"] not in traces, "trace reused across trials")
        traces.add(item["trace_ref"])
        value = item.get("owner_minutes")
        require(value is None or (type(value) in (int, float)
                and math.isfinite(value) and value >= 0),
                "owner minutes must be nonnegative or null (unknown)")
    require(set(found) == expected,
            "missing arm/case, including failed or crashed trials")
    require(not (reviewer_ids & contexts),
            "reviewer and writer contexts overlap")
    for cid in index:
        config = {(found[(cid, a)]["model"], found[(cid, a)]["effort"],
                   found[(cid, a)]["tools_scope"], found[(cid, a)]["token_budget"])
                  for a in ARMS}
        require(len(config) == 1, "unequal model, effort, tools or budget")
    metrics = {}
    for arm in ARMS:
        arm_trials = [found[(cid, arm)] for cid in index]
        by_role = defaultdict(list)
        for cid in index:
            by_role[index[cid]["role"]].append(found[(cid, arm)])
        measured = [t["owner_minutes"] for t in arm_trials
                    if t["owner_minutes"] is not None]
        metrics[arm] = {
            "correct_first_pass": sum(t["first_pass"] for t in arm_trials),
            "transfer_first_pass": sum(t["first_pass"] for t in by_role["transfer"]),
            "normal_first_pass": sum(t["first_pass"] for t in by_role["normal"]),
            "boundary_first_pass": sum(t["first_pass"] for t in by_role["boundary"]),
            "false_alarms_normal": sum(t["false_alarm"] for t in by_role["normal"]),
            "false_alarms_boundary": sum(t["false_alarm"] for t in by_role["boundary"]),
            "skill_applied_transfer": sum(t["skill_applied"] for t in by_role["transfer"]),
            "skill_applied_boundary": sum(t["skill_applied"] for t in by_role["boundary"]),
            "unsafe": sum(t["unsafe"] for t in arm_trials),
            "owner_minutes": sum(measured) if len(measured) == len(arm_trials) else None,
        }
    b, c = metrics["retrieval"], metrics["skill"]
    unsafe = any(m["unsafe"] for m in metrics.values())
    control_regression = (c["normal_first_pass"] < b["normal_first_pass"]
                          or c["boundary_first_pass"] < b["boundary_first_pass"]
                          or c["false_alarms_normal"] > b["false_alarms_normal"]
                          or c["false_alarms_boundary"] > b["false_alarms_boundary"])
    transfer_gain = c["transfer_first_pass"] > b["transfer_first_pass"]
    cost_worse = (b["owner_minutes"] is None or c["owner_minutes"] is None
                  or c["owner_minutes"] > b["owner_minutes"])
    if unsafe or control_regression:
        verdict = "HOLD_SAFETY_OR_CONTROL_REGRESSION"
    elif transfer_gain and c["skill_applied_transfer"] > 0 and not cost_worse:
        verdict = "DEVELOPMENT_GAIN_ONLY_NEEDS_INDEPENDENT_HOLDOUT"
    else:
        verdict = "NO_PROMOTABLE_INCREMENT"
    return {
        "suite_id": suite["id"],
        "candidate_commit": run["candidate_commit"],
        "evidence_level": "VISIBLE_DEVELOPMENT_PILOT_ONLY",
        "arm_metrics": metrics,
        "frozen_retrieval_pack_sha256": suite["retrieval_pack_sha256"],
        "frozen_candidate_skill_sha256": suite["candidate_skill_sha256"],
        "role_denominators": {role: sum(c["role"] == role for c in cases)
                              for role in ROLES},
        "verdict": verdict,
        "promotion_authorized": False,
        "clinical_validated": False,
        "autonomous_runtime_verified": False,
        "independent_review_authenticated": False,
        "publication_approved": False,
        "limitations": (
            "This checks declared paired outputs and mechanical completeness, not "
            "real model calls, source retrieval, skill invocation traces, blinded reviewer identity, clinical accuracy or skill transfer. "
            "Private unseen-case keys and human review are required for validation."
        ),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--suite", required=True, type=Path)
    p.add_argument("--run", required=True, type=Path)
    a = p.parse_args()
    try:
        raw = a.suite.read_bytes()
        report = evaluate(json.loads(raw), json.loads(a.run.read_text(encoding="utf-8")),
                          hashlib.sha256(raw).hexdigest())
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"evidence_level": "INVALID", "error": str(error)},
                         ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["verdict"].startswith("HOLD") else 0


if __name__ == "__main__":
    raise SystemExit(main())
