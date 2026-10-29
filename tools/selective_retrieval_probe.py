#!/usr/bin/env python3
"""Development-only selective retrieval probe; no API calls without --execute-api.

Runs a frozen first-stage retrieval decision BEFORE any source body exposure.
Uses existing API transport, never self-grades clinical correctness.
"""
import argparse
import hashlib
import json
import os
import random
from pathlib import Path

from run_skill_transfer_pilot import api_call, PilotError, write_private, append_event

ARMS = ("native", "retrieval", "skill")
DECISIONS = ("RETRIEVE", "SKIP", "HOLD")
GAPS = ("missing_patient_fact", "missing_primary_evidence",
        "missing_reasoning_bridge", "none")
MARKER = "SYNTHETIC EDUCATIONAL SCENARIO"
SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "decision": {"type": "string", "enum": list(DECISIONS)},
        "gap_type": {"type": "string", "enum": list(GAPS)},
        "source_id": {"type": "string"},
        "evidence_question": {"type": "string"},
        "decision_pivot": {"type": "string"},
        "provisional_answer": {"type": "string"},
        "confidence_percent": {"type": "integer", "minimum": 0, "maximum": 100},
    },
    "required": ["decision", "gap_type", "source_id", "evidence_question",
                 "decision_pivot", "provisional_answer", "confidence_percent"],
}
COMMON = (
    "Analyze ONLY the fictional educational case. First decide whether an "
    "available external document would resolve a consequential uncertainty. "
    "Missing individual patient measurements cannot be filled by a general "
    "article. Be cautious about evidence-to-decision inference and uncertainty. "
    "An explanation requiring no new evidence should SKIP. A genuinely "
    "unresolvable or unsafe issue may HOLD. Do not invent patient observations "
    "or clinician intentions. Use Traditional Chinese."
)


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_fixture(data):
    if not isinstance(data, dict) or data.get("source_class") != "synthetic_public_fixture":
        raise PilotError("SOURCE_CLASS_REJECTED")
    cases, docs = data.get("cases"), data.get("documents")
    if not isinstance(cases, list) or len(cases) != 3 or not isinstance(docs, list) or len(docs) != 2:
        raise PilotError("FIXTURE_SHAPE_REJECTED")
    ids = set()
    for entry in cases:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str) or not isinstance(entry.get("task"), str):
            raise PilotError("INVALID_CASE")
        if entry["id"] in ids or MARKER not in entry["task"] or not 100 <= len(entry["task"]) <= 2500:
            raise PilotError("INVALID_CASE")
        ids.add(entry["id"])
    ids.clear()
    for doc in docs:
        if not isinstance(doc, dict) or not all(isinstance(doc.get(k), str) for k in ("id", "title", "text")):
            raise PilotError("INVALID_DOCUMENT")
        if doc["id"] in ids or not 100 <= len(doc["text"]) <= 3000:
            raise PilotError("INVALID_DOCUMENT")
        ids.add(doc["id"])
    return cases, docs


def catalog(docs):
    # A/B/C source access differs deliberately. B/C see identical titles/ids,
    # NEVER source body before deciding. Full corpus is fixed before trial.
    return [{"id": doc["id"], "title": doc["title"]} for doc in docs]


def triage_request(case, arm, docs, skill, model):
    if arm not in ARMS:
        raise PilotError("BAD_ARM")
    instruction = COMMON
    if arm == "native":
        instruction += "\nNo additional retrieval collection is available in this arm."
    else:
        instruction += ("\nCandidate documents (titles only): "
                        + json.dumps(catalog(docs), ensure_ascii=False)
                        + "\nOnly request a document whose source ID is listed; "
                          "it may still be irrelevant. No source body has been shown.")
    if arm == "skill":
        instruction += "\nExperimental strategy (not a source of case facts):\n" + skill
    return {
        "model": model, "store": False, "max_output_tokens": 500,
        "instructions": instruction, "input": case["task"],
        "text": {"format": {"type": "json_schema", "name": "source_triage",
                            "strict": True, "schema": SCHEMA}},
    }


def validate_triage(parsed):
    if not isinstance(parsed, dict) or set(parsed) != set(SCHEMA["required"]):
        raise PilotError("TRIAGE_SCHEMA_INVALID")
    if parsed["decision"] not in DECISIONS or parsed["gap_type"] not in GAPS:
        raise PilotError("TRIAGE_SCHEMA_INVALID")
    if not all(isinstance(parsed[k], str) for k in ("source_id", "evidence_question",
                                                  "decision_pivot", "provisional_answer")):
        raise PilotError("TRIAGE_SCHEMA_INVALID")
    confidence = parsed["confidence_percent"]
    if type(confidence) is not int or not 0 <= confidence <= 100:
        raise PilotError("TRIAGE_SCHEMA_INVALID")
    return parsed


def retrieve_after_triage(arm, triage, docs):
    """Never access source bytes if first-stage gate did not permit retrieval."""
    if triage["decision"] != "RETRIEVE":
        return None, "MODEL_" + triage["decision"]
    if triage["gap_type"] in ("missing_patient_fact", "none"):
        return None, "NON_RETRIEVABLE_GAP"
    if arm == "native":
        return None, "ARM_NO_SOURCE_ACCESS"
    matches = [doc for doc in docs if doc["id"] == triage["source_id"]]
    if len(matches) != 1:
        return None, "SOURCE_NOT_ALLOWLISTED"
    return matches[0], "SOURCE_RETURNED"


def answer_request(case, triage, document, model):
    instructions = (
        "Give the best first-pass educational reasoning in Traditional Chinese. "
        "Reassess the provisional conclusion critically; explain if and WHY verified "
        "evidence changes it; evidence absence is not evidence of exclusion. "
        "No patient-specific orders. Do not claim independent review."
    )
    source = (
        {"id": document["id"], "title": document["title"], "text": document["text"]}
        if document is not None else None
    )
    return {
        "model": model, "store": False, "max_output_tokens": 1100,
        "instructions": instructions,
        "input": json.dumps({"case": case["task"], "frozen_initial_triage": triage,
                             "retrieved_document": source}, ensure_ascii=False),
    }


def run_case(case, arm, docs, skill, model, caller):
    """caller(request) -> existing API-like authenticated response dict.

    A synthetic test double can be injected only by local unit tests.
    No hidden source bytes are passed in triage_request.
    """
    first = triage_request(case, arm, docs, skill, model)
    first_response = caller(first)
    triage = validate_triage(json.loads(first_response["answer"]))
    document, outcome = retrieve_after_triage(arm, triage, docs)
    record = {
        "case_id": case["id"], "arm": arm, "triage": triage,
        "triage_request_sha256": digest(json.dumps(first, ensure_ascii=False, sort_keys=True)),
        "retrieval_gate": outcome, "retrieved_source_id": document["id"] if document else None,
        "retrieved_source_sha256": digest(document["text"]) if document else None,
        "first_call_receipt": {k: first_response.get(k) for k in ("response_id", "returned_model", "usage")},
        "answer": None, "answer_call_receipt": None,
        "first_pass_unscored": True, "independent_review": "NOT_DONE",
    }
    if triage["decision"] == "HOLD":
        return record
    second = answer_request(case, triage, document, model)
    second_response = caller(second)
    record["answer"] = second_response["answer"]
    record["answer_call_receipt"] = {k: second_response.get(k) for k in
                                      ("response_id", "returned_model", "usage")}
    return record


def paired_order(cases):
    """Balance arm position across the three fixed development cases."""
    return [(case, ARMS[(position + offset) % len(ARMS)])
            for position, case in enumerate(cases)
            for offset in range(len(ARMS))]


def build_plan(data, skill, model, commit):
    if not isinstance(commit, str) or len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise PilotError("CANDIDATE_COMMIT_REQUIRED")
    cases, docs = validate_fixture(data)
    plan = {
        "status": "NOT_RUN", "source_class": data["source_class"],
        "candidate_commit": commit, "model": model,
        "candidate_skill_sha256": digest(skill),
        "cases": [{"id": c["id"], "task_sha256": digest(c["task"])} for c in cases],
        "sources": [{"id": d["id"], "sha256": digest(d["text"])} for d in docs],
        "arms": list(ARMS),
        "paired_execution_order": [{"case_id": case["id"], "arm": arm}
                                   for case, arm in paired_order(cases)],
        "phase_order": "freeze_triage_before_source; conditional_source; frozen_first_answer",
        "planned_first_decisions": 9, "possible_model_calls_max": 18,
        "model_calls_made": 0, "clinical_validated": False,
        "transfer_validated": False, "publication_approved": False,
    }
    # Commit a stable preregistered input/design hash before any inference.
    plan["suite_sha256"] = digest(json.dumps(plan, ensure_ascii=False, sort_keys=True))
    return plan


def build_blind_packet(cases, results, suite_sha):
    """Create a private arm-blind reviewer packet; no judgments or answer keys.

    The mapping MUST NOT be shown to the independent reviewer. Development
    cases and the review packet are not an unseen clinical holdout.
    """
    items = []
    mapping = {}
    cases_by_id = {case["id"]: case for case in cases}
    shuffled_ids = list(cases_by_id)
    random.Random(int(suite_sha[:16], 16)).shuffle(shuffled_ids)
    for ci, case_id in enumerate(shuffled_ids, 1):
        alias = "scenario-" + str(ci)
        candidate_rows = [row for row in results if row["case_id"] == case_id]
        random.Random(int(digest(suite_sha + case_id)[:16], 16)).shuffle(candidate_rows)
        if len(candidate_rows) != len(ARMS):
            raise PilotError("REVIEW_ROWS_INCOMPLETE")
        answers = []
        for ri, row in enumerate(candidate_rows, 1):
            slot = alias + "-response-" + str(ri)
            mapping[slot] = {"case_id": case_id, "arm": row["arm"]}
            answers.append({
                "slot": slot, "run_status": row.get("status", "COMPLETED"),
                "initial_triage": row.get("triage"),
                "retrieval_gate": row.get("retrieval_gate"),
                "answer": row.get("answer"),
            })
        items.append({"scenario": alias, "task": cases_by_id[case_id]["task"],
                      "candidate_answers": answers})
    return items, mapping


def execute(data, skill, model, commit, output_dir, key=None, live=False, caller=None):
    meta = build_plan(data, skill, model, commit)
    cases, docs = validate_fixture(data)
    output_dir = Path(output_dir).resolve()
    repo = Path(__file__).resolve().parents[1]
    if output_dir.is_relative_to(repo) or output_dir.exists() or output_dir.parent == Path("/"):
        raise PilotError("PRIVATE_OUTPUT_REQUIRED")
    if live:
        if not key or caller is not None or model != "gpt-5-mini":
            raise PilotError("LIVE_KEY_MODEL_AND_TRANSPORT_REQUIRED")
        # IMPORTANT: calling execute() directly must NOT bypass the CLI's
        # public-fixture allowlist. Never send private case data using a
        # caller-supplied source_class or arbitrary in-memory fixture.
        approved_data = json.loads((repo / "experiments/skill-transfer/fixtures/selective-retrieval-synthetic.json").read_text(encoding="utf-8"))
        approved_skill = (repo / ".agents/skills/decision-question-triage/SKILL.md").read_text(encoding="utf-8")
        if data != approved_data or skill != approved_skill:
            raise PilotError("LIVE_CONTENT_NOT_ALLOWLISTED")
        transport = lambda request: api_call(request, key)
    else:
        transport = caller
    if transport is None:
        output_dir.mkdir(mode=0o700)
        write_private(output_dir / "manifest.json", meta)
        return {"status": "PLAN_ONLY_NO_MODEL_CALLS", "planned_triage": 9}
    results = []
    meta["transport_kind"] = "RESPONSES_API" if live else "INJECTED_TEST_DOUBLE"
    meta["provider_receipt_authenticated"] = False
    meta["model_calls_made"] = None
    output_dir.mkdir(mode=0o700)
    # manifest is a frozen PRE-RUN plan. Never overwrite it to fake completion.
    write_private(output_dir / "manifest.json", meta)
    events = output_dir / "attempt_events.jsonl"
    attempts = [0]
    seen_provider_ids = set()
    def traced_transport(request):
        attempts[0] += 1
        if attempts[0] > 18:
            raise PilotError("MODEL_CALL_BUDGET_EXCEEDED")
        stage = "TRIAGE" if "text" in request else "POST_RETRIEVAL_ANSWER"
        req_hash = digest(json.dumps(request, sort_keys=True, ensure_ascii=False))
        stamp = {"attempt": attempts[0], "stage": stage, "request_sha256": req_hash}
        append_event(events, dict(stamp, event="STARTED"))
        try:
            result = transport(request)
            if live:
                rid = result.get("response_id")
                if not isinstance(rid, str) or rid in seen_provider_ids:
                    raise PilotError("PROVIDER_RECEIPT_DUPLICATED_OR_MISSING")
                seen_provider_ids.add(rid)
        except Exception:
            append_event(events, dict(stamp, event="FAILED"))
            raise
        append_event(events, dict(stamp, event="COMPLETED",
                                  response_id=result.get("response_id")))
        return result
    for case, arm in paired_order(cases):
        try:
            results.append(run_case(case, arm, docs, skill, model, traced_transport))
        except (ValueError, KeyError, TypeError, PilotError):
            # Every attempted pair counts, including errors. Never replace
            # a failed first attempt with a retry or post-feedback answer.
            results.append({"case_id": case["id"], "arm": arm,
                            "status": "FAILED_INCOMPLETE", "first_pass_unscored": True,
                            "answer": None})
    write_private(output_dir / "first_pass_unscored.json", results)
    suite_sha = meta["suite_sha256"]
    packet, mapping = build_blind_packet(cases, results, suite_sha)
    write_private(output_dir / "blind_reviewer_packet.json", packet)
    write_private(output_dir / "private_arm_mapping.json", mapping)
    failed = sum(row.get("status") == "FAILED_INCOMPLETE" for row in results)
    usages = []
    for row in results:
        for name in ("first_call_receipt", "answer_call_receipt"):
            u = (row.get(name) or {}).get("usage")
            if isinstance(u, dict) and all(type(u.get(key)) is int for key in
                                          ("input_tokens", "output_tokens", "total_tokens")):
                usages.append(u)
    totals = {
        "input_tokens": sum(u["input_tokens"] for u in usages),
        "output_tokens": sum(u["output_tokens"] for u in usages),
        "total_tokens": sum(u["total_tokens"] for u in usages),
    } if live and failed == 0 else None
    per_arm = {}
    if live and failed == 0:
        for arm in ARMS:
            arm_rows = [row for row in results if row["arm"] == arm]
            stage_usages = []
            valid = True
            for row in arm_rows:
                required = ("first_call_receipt",) if row["triage"]["decision"] == "HOLD" else (
                    "first_call_receipt", "answer_call_receipt")
                for name in required:
                    usage = (row.get(name) or {}).get("usage")
                    if not isinstance(usage, dict) or any(
                            type(usage.get(key)) is not int for key in (
                                "input_tokens", "output_tokens", "total_tokens")):
                        valid = False
                        break
                    stage_usages.append(usage)
            per_arm[arm] = ({
                key: sum(u[key] for u in stage_usages)
                for key in ("input_tokens", "output_tokens", "total_tokens")
            } if valid else None)
    else:
        per_arm = {arm: None for arm in ARMS}
    status = ("HOLD_INCOMPLETE" if failed else
              "UNSCORED_API_EXECUTION" if live else "DEVELOPMENT_TEST_DOUBLE_ONLY")
    receipt = {
        "status": status, "suite_sha256": suite_sha,
        "completed_pairs": len(results) - failed, "failed_pairs": failed,
        "model_calls_attempted": attempts[0],
        "transport_kind": meta["transport_kind"],
        "provider_receipt_authenticated": False,
        "tokens_observed_for_completed_calls": totals,
        "per_arm_token_usage": per_arm,
        "cost_usd": None, "owner_minutes": None,
        "independent_review": "NOT_DONE",
        "clinical_validated": False, "transfer_validated": False,
        "publication_approved": False,
    }
    write_private(output_dir / "run_receipt.json", receipt)
    return {"status": status, "rows": len(results), "calls_attempted": attempts[0],
            "failed_pairs": failed, "clinical_validated": False,
            "transfer_validated": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--candidate-commit", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="gpt-5-mini")
    parser.add_argument("--execute-api", action="store_true")
    args = parser.parse_args()
    try:
        root = Path(__file__).resolve().parents[1]
        fixture_path = Path(args.fixture).resolve()
        skill_path = Path(args.skill).resolve()
        if fixture_path != root / "experiments/skill-transfer/fixtures/selective-retrieval-synthetic.json":
            raise PilotError("PUBLIC_SYNTHETIC_FIXTURE_ONLY")
        if skill_path != root / ".agents/skills/decision-question-triage/SKILL.md":
            raise PilotError("CANDIDATE_SKILL_PATH_REQUIRED")
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        skill = skill_path.read_text(encoding="utf-8")
        result = execute(data, skill, args.model, args.candidate_commit, args.output_dir,
                         key=os.getenv("OPENAI_API_KEY") if args.execute_api else None,
                         live=args.execute_api)
        print(json.dumps(result, sort_keys=True))
    except (PilotError, ValueError, OSError, UnicodeError):
        print(json.dumps({"status": "HOLD", "reason": "INVALID_OR_UNAUTHORIZED_INPUT"}))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
