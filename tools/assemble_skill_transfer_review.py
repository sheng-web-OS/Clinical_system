#!/usr/bin/env python3
"""Attach a SEPARATE blinded review to frozen first-pass pilot evidence.

This program verifies bytes, pair coverage, and reviewer receipt integrity.
It does not review medicine, authenticate reviewer independence, or self-improve.
All inputs and outputs remain outside the public repository when confidential.
"""
import argparse
import json
import os
from pathlib import Path

from compare_skill_transfer import evaluate
from run_skill_transfer_pilot import (
    ARMS, PilotError, build_plan, clean_cases, digest, read_text,
    require, write_private,
)


def load_obj(path, max_bytes=2500000):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(),
            "MISSING_OR_LINKED_PRIVATE_EVIDENCE")
    raw = path.read_bytes()
    require(0 < len(raw) <= max_bytes, "PRIVATE_EVIDENCE_OVERSIZED")
    return json.loads(raw), digest(raw)


def ensure_private(path):
    root = Path(__file__).resolve().parents[1]
    resolved = Path(path).resolve()
    require(not resolved.is_relative_to(root),
            "PUBLIC_REPOSITORY_NOT_A_PRIVATE_REVIEW_STORE")
    return resolved


def assemble(run_dir, review_path, cases_path, pack_path, skill_path):
    run_dir = ensure_private(run_dir)
    ensure_private(review_path)
    manifest, _ = load_obj(run_dir / "manifest.json")
    suite, suite_sha = load_obj(run_dir / "frozen_suite.json")
    requests, _ = load_obj(run_dir / "requests.json")
    outputs, _ = load_obj(run_dir / "first_pass_results.json")
    # For the paid runner, the append+fsync checkpoint is the primary
    # crash-forensics trace. It must agree byte-for-byte in JSON semantics
    # with the eventual all-calls snapshot before independent scoring.
    checkpoint = None
    if manifest.get("first_pass_journal_v1") is True:
        journal_path = run_dir / "first_pass_journal.jsonl"
        require(journal_path.is_file() and not journal_path.is_symlink()
                and 0 < journal_path.stat().st_size <= 2500000,
                "FIRST_PASS_JOURNAL_MISSING_OR_OVERSIZED")
        require(journal_path.stat().st_mode & 0o077 == 0,
                "FIRST_PASS_JOURNAL_PERMISSION_INVALID")
        try:
            journal_lines = journal_path.read_text(encoding="utf-8").splitlines()
            checkpoint = [json.loads(line) for line in journal_lines]
        except (UnicodeError, ValueError, TypeError):
            raise PilotError("FIRST_PASS_JOURNAL_MALFORMED") from None
        require(len(checkpoint) == 9, "INCOMPLETE_FIRST_PASS_JOURNAL")
        require(checkpoint == outputs, "FIRST_PASS_JOURNAL_SNAPSHOT_MISMATCH")
    packet, packet_sha = load_obj(run_dir / "blind_reviewer_packet.json")
    mapping, _ = load_obj(run_dir / "private_arm_mapping.json")
    review, _ = load_obj(review_path)

    cases_text, case_sha = read_text(cases_path)
    pack, pack_sha = read_text(pack_path)
    skill, skill_sha = read_text(skill_path)
    cases = clean_cases(json.loads(cases_text))
    require(manifest.get("results_status") == "EXECUTION_STARTED_UNSCORED"
            and manifest.get("independent_review") == "NOT_DONE",
            "RESULTS_NOT_FROZEN_OR_ALREADY_REVIEWED")
    transport_kind = manifest.get("transport_kind")
    require(transport_kind in {"RESPONSES_API", "INJECTED_TEST_DOUBLE"},
            "TRANSPORT_NOT_A_RECORDED_MODEL_EXECUTION")
    require(suite.get("exposure") == "development"
            and manifest.get("suite_sha256") == suite_sha
            and manifest.get("suite_id") == suite.get("id"),
            "FROZEN_SUITE_MISMATCH")
    require(manifest.get("case_file_sha256") == case_sha
            and suite.get("retrieval_pack_sha256") == pack_sha
            and suite.get("candidate_skill_sha256") == skill_sha,
            "EXACT_CASE_ARTICLE_SKILL_BYTES_MISMATCH")
    require(suite.get("cases") == [
        {"id": c["id"], "role": c["role"],
         "source_sha256": digest(c["task"].encode("utf-8"))}
        for c in cases], "CASE_ROLE_OR_FINGERPRINT_MISMATCH")

    baseline, expected_requests = build_plan(
        cases, case_sha, pack, pack_sha, skill, skill_sha,
        manifest.get("model"), manifest.get("candidate_commit"))
    require(requests == expected_requests and manifest.get("max_calls") == 9
            and len(outputs) == len(requests) == 9,
            "MODEL_REQUEST_OR_DENOMINATOR_CHANGED")
    require(type(packet) is list and len(packet) == 3
            and type(mapping) is dict
            and type(mapping.get("answer_slots")) is dict
            and len(mapping["answer_slots"]) == 9,
            "INVALID_BLIND_PACKET_MAPPING")
    require(review.get("schema_version") == 1
            and review.get("packet_sha256") == packet_sha
            and review.get("suite_sha256") == suite_sha,
            "REVIEW_NOT_BOUND_TO_FROZEN_BLIND_PACKET")
    reviewer = review.get("reviewer_context")
    require(type(reviewer) is str and len(reviewer.strip()) >= 8,
            "SEPARATE_REVIEWER_CONTEXT_REQUIRED")

    raw_events = (run_dir / "attempt_events.jsonl")
    require(raw_events.is_file() and not raw_events.is_symlink(),
            "ATTEMPT_EVENTS_MISSING")
    lines = raw_events.read_text(encoding="utf-8").splitlines()
    require(len(lines) == 2 * len(requests),
            "INCOMPLETE_OR_EXTRA_ATTEMPT_EVENTS")
    events = [json.loads(line) for line in lines]
    results_by_pair = {}
    provider_ids = set()
    token_totals = {
        arm: {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        for arm in ARMS
    }
    usage_complete = {arm: True for arm in ARMS}
    for i, (call, output) in enumerate(zip(requests, outputs)):
        key = (call["case_id"], call["arm"])
        require(key not in results_by_pair
                and output.get("case_id") == key[0]
                and output.get("arm") == key[1]
                and output.get("request_sha256") == call["request_sha256"],
                "ALTERED_OR_DUPLICATE_FIRST_PASS_RESULT")
        status = output.get("status")
        require(status in {"COMPLETED", "FAILED_OR_INCOMPLETE"},
                "INVALID_OBSERVED_STATUS")
        expected = {"case_id": key[0], "arm": key[1],
                    "request_sha256": call["request_sha256"]}
        require(events[2 * i] == dict(expected, event="STARTED")
                and events[2 * i + 1] == dict(expected, event=status),
                "ATTEMPT_EVENT_TRACE_MISMATCH")
        if status == "COMPLETED":
            response = output.get("response")
            require(type(response) is dict
                    and type(response.get("answer")) is str
                    and response["answer"].strip()
                    and type(response.get("returned_model")) is str
                    and response["returned_model"].strip(),
                    "COMPLETED_ANSWER_MISSING")
            provider_id = response.get("response_id")
            usage = response.get("usage")
            if transport_kind == "RESPONSES_API":
                require(type(provider_id) is str and provider_id.startswith("resp_")
                        and provider_id not in provider_ids,
                        "API_PROVIDER_RESPONSE_ID_MISSING_OR_REUSED")
                returned = response["returned_model"]
                requested = call["request"]["model"]
                require(returned == requested or returned.startswith(requested + "-"),
                        "API_MODEL_ID_DIFFERS_BETWEEN_ARMS")
                require(type(usage) is dict
                        and all(type(usage.get(k)) is int and usage[k] >= 0
                                for k in ("input_tokens", "output_tokens", "total_tokens"))
                        and usage["input_tokens"] > 0 and usage["output_tokens"] > 0
                        and usage["total_tokens"] == usage["input_tokens"] + usage["output_tokens"],
                        "API_TOKEN_USAGE_MISSING_OR_INVALID")
                provider_ids.add(provider_id)
            if (type(usage) is dict
                    and all(type(usage.get(k)) is int and usage[k] >= 0
                            for k in ("input_tokens", "output_tokens", "total_tokens"))
                    and usage["total_tokens"] == usage["input_tokens"] + usage["output_tokens"]):
                for k in token_totals[call["arm"]]:
                    token_totals[call["arm"]][k] += usage[k]
            else:
                usage_complete[call["arm"]] = False
        else:
            require(output.get("response") is None,
                    "FAILED_TRIAL_CANNOT_CONTAIN_CREDITED_ANSWER")
            usage_complete[call["arm"]] = False
        require(output.get("adjudication") == "NOT_DONE"
                and output.get("first_pass") == "NOT_SCORED",
                "PREPOPULATED_SELF_GRADING_DETECTED")
        results_by_pair[key] = output

    by_slot = {}
    seen_cases = set()
    for scenario in packet:
        alias = scenario.get("scenario")
        cid = mapping.get("case_aliases", {}).get(alias)
        found_case = next((c for c in cases if c["id"] == cid), None)
        require(cid not in seen_cases and found_case is not None
                and scenario.get("task") == found_case["task"],
                "CASE_ALIAS_OR_ORIGINAL_TASK_CHANGED")
        seen_cases.add(cid)
        choices = scenario.get("candidate_answers")
        require(type(choices) is list and len(choices) == len(ARMS),
                "INCOMPLETE_BLIND_CHOICES")
        for choice in choices:
            slot = choice.get("slot")
            mapped = mapping["answer_slots"].get(slot)
            require(slot not in by_slot and type(mapped) is dict
                    and mapped.get("case_id") == cid
                    and mapped.get("arm") in ARMS,
                    "BLIND_SLOT_MISMATCH")
            result = results_by_pair[(cid, mapped["arm"])]
            require(choice.get("run_status") == result["status"]
                    and choice.get("answer") ==
                    (result["response"]["answer"] if result["response"] else None),
                    "BLIND_ANSWER_NOT_IDENTICAL_TO_FIRST_PASS")
            by_slot[slot] = result
    require(seen_cases == {c["id"] for c in cases}
            and set(by_slot) == set(mapping["answer_slots"]),
            "BLIND_PACKET_NOT_COMPLETE")

    adjudications = review.get("judgments")
    require(type(adjudications) is list and len(adjudications) == 9,
            "INCOMPLETE_INDEPENDENT_ADJUDICATION")
    reviews_by_slot = {}
    for verdict in adjudications:
        require(type(verdict) is dict, "INVALID_REVIEW_ROW")
        slot = verdict.get("slot")
        require(slot in by_slot and slot not in reviews_by_slot,
                "UNKNOWN_OR_DUPLICATE_REVIEW_SLOT")
        for field in ("decision_correct", "unsafe", "false_alarm",
                      "question_triage_observed"):
            require(type(verdict.get(field)) is bool,
                    "REVIEW_MUST_SUPPLY_BOOLEAN_" + field)
        require(type(verdict.get("reason")) is str
                and len(verdict["reason"].strip()) >= 20,
                "REVIEW_REASON_REQUIRED")
        if by_slot[slot]["status"] != "COMPLETED":
            require(not verdict["decision_correct"]
                    and not verdict["question_triage_observed"]
                    and not verdict["false_alarm"],
                    "FAILED_CALL_MUST_NOT_BE_GRADED_AS_SUCCESS")
        reviews_by_slot[slot] = verdict

    records = []
    for call in requests:
        cid, arm = call["case_id"], call["arm"]
        slot = next(s for s, p in mapping["answer_slots"].items()
                    if p["case_id"] == cid and p["arm"] == arm)
        v = reviews_by_slot[slot]
        result = results_by_pair[(cid, arm)]
        correct = v["decision_correct"] and not v["false_alarm"]
        records.append({
            "case_id": cid, "arm": arm,
            "source_sha256": call["source_sha256"],
            "attempt_status": result["status"],
            "decision_correct": correct,
            "first_pass": result["status"] == "COMPLETED"
                          and correct and not v["unsafe"],
            "unsafe": v["unsafe"], "hinted": False,
            "false_alarm": v["false_alarm"],
            "article_retrieval_visible": arm != "native",
            "candidate_skill_visible": arm == "skill",
            "retrieval_pack_sha256": None if arm == "native" else pack_sha,
            "loaded_skill_sha256": skill_sha if arm == "skill" else None,
            # Observed answer behavior is only a proxy for skill usage.
            "skill_applied": arm == "skill" and v["question_triage_observed"],
            "worker_context": "stateless-response-" + call["request_sha256"],
            "reviewer_context": reviewer,
            "trace_ref": "attempt_events.jsonl#" + cid + "/" + arm,
            "model": manifest["model"], "effort": "API_DEFAULT_UNSPECIFIED",
            "tools_scope": "NO_EXTERNAL_TOOLS",
            "token_budget": str(call["request"]["max_output_tokens"]),
            "owner_minutes": None,
        })
    assembled = {
        "schema_version": 1, "suite_id": suite["id"],
        "suite_sha256": suite_sha,
        "candidate_commit": manifest["candidate_commit"],
        "run_id": "local-development-" + case_sha[:16],
        "arm": "paired-native-retrieval-skill",
        "model": manifest["model"],
        "records": records,
    }
    report = evaluate(suite, assembled, suite_sha, pack_sha, skill_sha)
    # Turn adjudicated differences into hypotheses for the NEXT experiment.
    # This does not edit the candidate Skill or upgrade developer-visible scores.
    case_feedback = []
    for case in cases:
        cid = case["id"]
        base = next(r for r in records
                    if r["case_id"] == cid and r["arm"] == "retrieval")
        skill_row = next(r for r in records
                         if r["case_id"] == cid and r["arm"] == "skill")
        base_slot = next(slot for slot, p in mapping["answer_slots"].items()
                         if p["case_id"] == cid and p["arm"] == "retrieval")
        skill_slot = next(slot for slot, p in mapping["answer_slots"].items()
                          if p["case_id"] == cid and p["arm"] == "skill")
        if (skill_row["unsafe"] or skill_row["attempt_status"] != "COMPLETED"
                or skill_row["false_alarm"]):
            finding = "HOLD_SAFETY_FAILURE_OR_FALSE_ALARM"
        elif skill_row["first_pass"] and not base["first_pass"]:
            finding = "POTENTIAL_SKILL_VALUE_NEEDS_FRESH_TEST"
        elif base["first_pass"] and not skill_row["first_pass"]:
            finding = "NEGATIVE_TRANSFER_INSPECT_TRIGGER_AND_SCOPE"
        elif not base["first_pass"] and not skill_row["first_pass"]:
            finding = "SHARED_FAILURE_CHECK_SOURCE_OR_QUESTION"
        else:
            finding = "NO_ADDED_VALUE_OVER_RETRIEVAL"
        case_feedback.append({
            "case_id": cid, "role": case["role"], "finding": finding,
            "retrieval_review_reason": reviews_by_slot[base_slot]["reason"],
            "skill_review_reason": reviews_by_slot[skill_slot]["reason"],
        })
    markers = {item["finding"] for item in case_feedback}
    if report["verdict"].startswith("HOLD"):
        next_action = "HOLD_INVESTIGATE_SAFETY_OR_RUN_FAILURE"
    elif "NEGATIVE_TRANSFER_INSPECT_TRIGGER_AND_SCOPE" in markers:
        next_action = "PROPOSE_NARROWER_SKILL_OR_REMOVE_IT"
    elif "SHARED_FAILURE_CHECK_SOURCE_OR_QUESTION" in markers:
        next_action = "REASSESS_SOURCE_GAP_BEFORE_ANY_SKILL_CHANGE"
    elif "POTENTIAL_SKILL_VALUE_NEEDS_FRESH_TEST" in markers:
        next_action = "PREREGISTER_NEW_UNSEEN_TASKS_AND_MEASURE_COST"
    else:
        next_action = "PREFER_RETRIEVAL_BASELINE_UNTIL_VALUE_IS_SHOWN"
    report["next_iteration"] = {
        "action": next_action,
        "evidence": "DEVELOPMENT_HYPOTHESIS_ONLY",
        "case_feedback_private": case_feedback,
        "candidate_skill_edited": False,
        "independent_expert_judgment_authenticated": False,
        "holdout_reuse_authorized": False,
        "publication_authorized": False,
    }
    report["transport_kind"] = transport_kind
    report["api_transport_claimed"] = transport_kind == "RESPONSES_API"
    # Local JSON is user-editable. A shape-consistent receipt does not prove
    # that the provider processed the request; independent API/billing evidence
    # is required to authenticate execution.
    report["actual_model_execution_verified"] = False
    report["provider_receipt_authentication"] = "DECLARED_RESPONSE_SHAPE_ONLY"
    report["observed_token_usage"] = {
        arm: (token_totals[arm] if usage_complete[arm] else None)
        for arm in ARMS
    }
    if usage_complete["retrieval"] and usage_complete["skill"]:
        report["skill_minus_retrieval_total_tokens"] = (
            token_totals["skill"]["total_tokens"]
            - token_totals["retrieval"]["total_tokens"])
    else:
        report["skill_minus_retrieval_total_tokens"] = None
    report["review_packet_sha256"] = packet_sha
    report["reviewer_context_declared_not_authenticated"] = reviewer
    report["first_pass_trace_integrity_checked"] = True
    report["first_pass_journal_verified"] = checkpoint is not None
    report["first_pass_journal_not_provider_authentication"] = True
    report["skill_invocation_verified"] = False
    report["owner_attention_measured"] = False
    return assembled, report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-dir", required=True, type=Path)
    p.add_argument("--review", required=True, type=Path)
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--retrieval-pack", required=True, type=Path)
    p.add_argument("--candidate-skill", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    try:
        dest = ensure_private(a.output)
        require(not dest.exists(), "REVIEW_OUTPUT_ALREADY_EXISTS")
        run, report = assemble(a.run_dir, a.review, a.cases,
                               a.retrieval_pack, a.candidate_skill)
        write_private(dest, {"run": run, "report": report})
        print(json.dumps({"status": report["verdict"],
                          "evidence_level": "VISIBLE_DEVELOPMENT_PILOT_ONLY",
                          "reviewed": len(run["records"]),
                          "promotion_authorized": False}))
        return 1 if report["verdict"].startswith("HOLD") else 0
    except (OSError, KeyError, ValueError, TypeError) as exc:
        reason = str(exc) if isinstance(exc, PilotError) else "INVALID_PRIVATE_EVIDENCE"
        print(json.dumps({"status": "HOLD", "reason": reason}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
