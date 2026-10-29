#!/usr/bin/env python3
"""Local, synthetic-only A/B/C prompt runner. NEVER grades or publishes results.

Default is offline: prepare frozen, auditable requests without a model call.
To actually call the Responses API, the operator must explicitly supply
--execute-api and a separately scoped OPENAI_API_KEY environment variable.
Run outside public GitHub CI; keep output packets private.
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import re
import urllib.error
import urllib.request
from pathlib import Path

ARMS = ("native", "retrieval", "skill")
ROLES = {"transfer", "normal", "boundary"}
SYNTHETIC_MARKER = "SYNTHETIC EDUCATIONAL SCENARIO"
MAX_CASES = 3
MAX_INPUT_BYTES = 60000
MAX_OUTPUT_TOKENS = 1100
# One development-only subtrial; NOT an OpenAI project billing/spend limiter.
# 2026-10-29 standard text rates for gpt-5-mini: input $0.25/M, output $2/M.
# Ref: https://developers.openai.com/api/docs/models/gpt-5-mini
LIVE_MODEL = "gpt-5-mini"
MAX_PAID_CALLS = 9
MAX_ESTIMATED_SUBTRIAL_USD = 0.50
MODEL_INPUT_USD_PER_M = 0.25
MODEL_OUTPUT_USD_PER_M = 2.00
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class PilotError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise PilotError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_text(path):
    path = Path(path)
    require(path.is_file() and not path.is_symlink(), "INPUT_FILE_REQUIRED")
    size = path.stat().st_size
    require(0 < size <= MAX_INPUT_BYTES, "INPUT_SIZE_OUT_OF_SCOPE")
    raw = path.read_bytes()
    require(len(raw) <= MAX_INPUT_BYTES, "INPUT_SIZE_OUT_OF_SCOPE")
    return raw.decode("utf-8"), digest(raw)


def clean_cases(obj):
    require(type(obj) is dict and obj.get("schema_version") == 1
            and obj.get("source_class") == "synthetic_public_fixture",
            "SYNTHETIC_SOURCE_ALLOWLIST_ONLY")
    cases = obj.get("cases")
    require(type(cases) is list and len(cases) == MAX_CASES,
            "EXACTLY_THREE_SYNTHETIC_CASES_REQUIRED")
    seen = set()
    result = []
    for case in cases:
        require(type(case) is dict, "INVALID_CASE")
        ident = case.get("id")
        role = case.get("role")
        task = case.get("task")
        require(type(ident) is str and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,50}", ident)
                and ident not in seen, "INVALID_OR_DUPLICATE_CASE_ID")
        require(role in ROLES and type(task) is str
                and SYNTHETIC_MARKER in task and 100 <= len(task) <= 8000,
                "INVALID_SYNTHETIC_CASE")
        seen.add(ident)
        result.append({"id": ident, "role": role, "task": task})
    require({c["role"] for c in result} == ROLES,
            "REQUIRE_TRANSFER_NORMAL_BOUNDARY")
    return result


COMMON = (
    "You are producing one first-pass educational analysis of a SYNTHETIC "
    "fictional scenario, never patient-specific medical advice. "
    "Identify the task's actual question, explain the reasoning from the supplied "
    "facts, note what evidence cannot establish, and avoid inventing source "
    "observations or clinician motives. When the case is a simple explanation, "
    "do not manufacture a controversy. Do not mention evaluation arms or scores. "
    "Return a clear independent answer in Traditional Chinese."
)


def make_request(case, arm, pack, skill, model):
    require(arm in ARMS, "BAD_ARM")
    instruction = COMMON
    if arm != "native":
        instruction += (
            "\n\nAdditional versioned reading material follows. The material "
            "may or may not apply. Do not import disease-specific conclusions "
            "without assessing similarity, evidence and conditions.\n"
            + pack
        )
    if arm == "skill":
        instruction += (
            "\n\nExperimental judgment skill below. Apply it only if its trigger "
            "fits the case; otherwise ignore it.\n" + skill
        )
    return {
        "model": model,
        "store": False,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "instructions": instruction,
        "input": case["task"],
    }


def build_plan(cases, case_sha, pack, pack_sha, skill, skill_sha, model, commit):
    require(SHA40.fullmatch(commit) is not None, "EXACT_CANDIDATE_COMMIT_REQUIRED")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,80}", model) is not None,
            "INVALID_MODEL_ID")
    order = [(c["id"], arm) for c in cases for arm in ARMS]
    # Reproducible interleaving, not random output cherry-picking.
    random.Random(int(case_sha[:16], 16)).shuffle(order)
    by_id = {c["id"]: c for c in cases}
    calls = []
    for cid, arm in order:
        req = make_request(by_id[cid], arm, pack, skill, model)
        encoded = json.dumps(req, ensure_ascii=False, sort_keys=True).encode("utf-8")
        calls.append({
            "case_id": cid, "arm": arm,
            "source_sha256": digest(by_id[cid]["task"].encode("utf-8")),
            "request_sha256": digest(encoded),
            "request": req,
        })
    meta = {
        "schema_version": 1, "source_class": "synthetic_public_fixture",
        "candidate_commit": commit, "model": model, "max_calls": len(calls),
        "case_file_sha256": case_sha, "retrieval_pack_sha256": pack_sha,
        "candidate_skill_sha256": skill_sha,
        "results_status": "NOT_RUN",
        "independent_review": "NOT_DONE",
        "clinical_validated": False, "learning_effect_validated": False,
        "publication_approved": False,
    }
    return meta, calls


def preflight_paid_budget(calls, model):
    """Conservative static expense estimate BEFORE any external request.

    This protects one pinned synthetic subtrial against accidental costly
    models, tool use or runaway output. The estimated bound is not an actual
    account billing guarantee: independent project spend controls remain
    mandatory and provider pricing can change.
    """
    require(model == LIVE_MODEL, "UNAPPROVED_PAID_MODEL_OR_PRICE_UNKNOWN")
    require(type(calls) is list and len(calls) == MAX_PAID_CALLS,
            "PAID_CALL_COUNT_NOT_BOUNDED")
    total_input_proxy_tokens = 0
    total_output_tokens = 0
    for item in calls:
        req = item.get("request") if type(item) is dict else None
        require(type(req) is dict
                and set(req) == {"model", "store", "max_output_tokens",
                                 "instructions", "input"}
                and req["model"] == LIVE_MODEL
                and req["store"] is False
                and req["max_output_tokens"] == MAX_OUTPUT_TOKENS
                and type(req["instructions"]) is str
                and type(req["input"]) is str,
                "UNBOUNDED_PAID_REQUEST")
        raw = json.dumps(req, ensure_ascii=False, sort_keys=True).encode("utf-8")
        require(len(raw) <= 200000, "PAID_PROMPT_TOO_LARGE")
        # Overestimate tokenization: 2 tokens per raw UTF-8 byte + fixed
        # 4096 token envelope per call. No tools, image/audio or extra requests.
        total_input_proxy_tokens += 2 * len(raw) + 4096
        total_output_tokens += req["max_output_tokens"]
    upper = (total_input_proxy_tokens * MODEL_INPUT_USD_PER_M
             + total_output_tokens * MODEL_OUTPUT_USD_PER_M) / 1_000_000
    require(upper <= MAX_ESTIMATED_SUBTRIAL_USD,
            "SUBTRIAL_COST_BOUND_EXCEEDED")
    return {"model": LIVE_MODEL, "max_paid_calls": MAX_PAID_CALLS,
            "estimated_upper_usd": round(upper, 6),
            "planning_ceiling_usd": MAX_ESTIMATED_SUBTRIAL_USD,
            "external_project_budget_verified": False,
            "provider_invoice_verified": False,
            "price_date": "2026-10-29"}


def extract_output(obj):
    require(type(obj) is dict and obj.get("status") == "completed",
            "MODEL_NOT_COMPLETED")
    chunks = [
        part.get("text", "")
        for item in obj.get("output", [])
        if type(item) is dict and item.get("type") == "message"
        for part in item.get("content", [])
        if type(part) is dict and part.get("type") == "output_text"
    ]
    answer = "".join(chunks).strip()
    require(answer, "EMPTY_MODEL_OUTPUT")
    returned_model = obj.get("model")
    require(type(returned_model) is str and returned_model,
            "MODEL_ID_MISSING")
    response_id = obj.get("id")
    require(type(response_id) is str
            and re.fullmatch(r"resp_[A-Za-z0-9_-]+", response_id) is not None,
            "MODEL_PROVIDER_RESPONSE_ID_MISSING")
    usage = obj.get("usage")
    require(type(usage) is dict
            and all(type(usage.get(k)) is int and usage[k] >= (1 if k != "total_tokens" else 2)
                    for k in ("input_tokens", "output_tokens", "total_tokens"))
            and usage["total_tokens"] == usage["input_tokens"] + usage["output_tokens"],
            "MODEL_TOKEN_USAGE_INVALID")
    return {"answer": answer, "returned_model": returned_model,
            "response_id": response_id, "usage": usage}


def api_call(request, key):
    require(bool(key), "MODEL_SECRET_NOT_CONFIGURED")
    payload = json.dumps(request, ensure_ascii=False).encode("utf-8")
    http = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=payload,
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(http, timeout=90) as resp:
            data = json.loads(resp.read(750000))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError):
        raise PilotError("MODEL_CALL_FAILED") from None
    result = extract_output(data)
    expected_model = request["model"]
    require(result["returned_model"] == expected_model
            or result["returned_model"].startswith(expected_model + "-"),
            "RETURNED_MODEL_DIFFERS_FROM_REQUEST")
    return result


def verify_live_checkout(repo, expected_commit):
    """Confirm exact Git HEAD and clean tracked API input paths before spending."""
    paths = (
        "experiments/skill-transfer/fixtures/synthetic-questions.json",
        "content/xiaoma-reading/originals/2026-07-14-hcm.md",
        ".agents/skills/decision-question-triage/SKILL.md",
        "tools/run_skill_transfer_pilot.py",
    )
    try:
        head = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
            capture_output=True, text=True, timeout=5, check=False)
        status = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain",
             "--untracked-files=no", "--", *paths],
            capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise PilotError("LIVE_CHECKOUT_UNVERIFIED") from None
    if head.returncode != 0 or head.stdout.strip() != expected_commit:
        raise PilotError("LIVE_CHECKOUT_HEAD_MISMATCH")
    if status.returncode != 0 or status.stdout.strip():
        raise PilotError("LIVE_CHECKOUT_DIRTY_OR_UNVERIFIED")
    return True


def write_private(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, sort_keys=True,
                       indent=2) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as file:
        file.write(data)


def append_event(path, event):
    data = (json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "ab") as file:
        file.write(data)
        file.flush()
        os.fsync(file.fileno())


def run(cases_path, pack_path, skill_path, target, model, commit,
        execute=False, key=None, caller=None):
    case_text, case_sha = read_text(cases_path)
    pack, pack_sha = read_text(pack_path)
    skill, skill_sha = read_text(skill_path)
    cases = clean_cases(json.loads(case_text))
    require("name: decision-question-triage" in skill,
            "WRONG_SKILL_SELECTED")
    repo_root = Path(__file__).resolve().parents[1]
    if execute:
        require(bool(key), "MODEL_SECRET_NOT_CONFIGURED")
        # Source-class labels are not privacy controls: the actual network
        # transport may ONLY use this reviewed, public, in-repo fixture and
        # article. Local injected mock transports are for unit tests only.
        if caller is None:
            allowed = (
                repo_root / "experiments/skill-transfer/fixtures/synthetic-questions.json",
                repo_root / "content/xiaoma-reading/originals/2026-07-14-hcm.md",
                repo_root / ".agents/skills/decision-question-triage/SKILL.md",
            )
            require(tuple(Path(p).resolve() for p in
                          (cases_path, pack_path, skill_path)) == allowed,
                    "LIVE_API_REQUIRES_EXACT_PUBLIC_ALLOWLISTED_INPUT_FILES")
            verify_live_checkout(repo_root, commit)
    target = Path(target).resolve()
    require(not target.is_relative_to(repo_root),
            "PRIVATE_OUTPUT_MUST_BE_OUTSIDE_PUBLIC_REPOSITORY")
    require(not target.exists(), "OUTPUT_EXISTS_REFUSE_TO_REWRITE")
    meta, calls = build_plan(cases, case_sha, pack, pack_sha,
                             skill, skill_sha, model, commit)
    paid_preflight = (preflight_paid_budget(calls, model)
                      if execute and caller is None else None)
    frozen_suite = {
        "schema_version": 1,
        "id": "synthetic-decision-triage-" + case_sha[:16],
        "exposure": "development",
        "retrieval_pack_sha256": pack_sha,
        "candidate_skill_sha256": skill_sha,
        "cases": [
            {"id": c["id"], "role": c["role"],
             "source_sha256": digest(c["task"].encode("utf-8"))}
            for c in cases
        ],
    }
    frozen_suite_bytes = (
        json.dumps(frozen_suite, sort_keys=True, ensure_ascii=False, indent=2)
        + "\n"
    ).encode("utf-8")
    meta["suite_id"] = frozen_suite["id"]
    meta["suite_sha256"] = digest(frozen_suite_bytes)
    meta["candidate_commit_git_verified"] = bool(execute and caller is None)
    meta["paid_cost_preflight"] = paid_preflight
    meta["transport_kind"] = (
        "RESPONSES_API" if execute and caller is None
        else "INJECTED_TEST_DOUBLE" if execute else "NO_MODEL_CALLS"
    )
    if execute:
        meta["results_status"] = "EXECUTION_STARTED_UNSCORED"
    target.mkdir(mode=0o700, parents=False)
    write_private(target / "frozen_suite.json", frozen_suite)
    write_private(target / "manifest.json", meta)
    # Private full requests are retained locally; never in public Actions artifacts.
    write_private(target / "requests.json", calls)
    if not execute:
        return {"status": "PLAN_ONLY_NO_MODEL_CALLS", "planned": len(calls),
                "output": str(target), "model": model}
    results = []
    for call in calls:
        append_event(target / "attempt_events.jsonl", {
            "case_id": call["case_id"], "arm": call["arm"],
            "request_sha256": call["request_sha256"], "event": "STARTED"})
        try:
            answer = (caller or api_call)(call["request"], key)
            status = "COMPLETED"
        except (PilotError, ValueError, KeyError):
            answer = None
            status = "FAILED_OR_INCOMPLETE"
        results.append({
            "case_id": call["case_id"], "arm": call["arm"],
            "request_sha256": call["request_sha256"],
            "status": status, "response": answer,
            "adjudication": "NOT_DONE", "first_pass": "NOT_SCORED",
        })
        append_event(target / "attempt_events.jsonl", {
            "case_id": call["case_id"], "arm": call["arm"],
            "request_sha256": call["request_sha256"], "event": status})
    write_private(target / "first_pass_results.json", results)
    # The review packet excludes arm names, request texts, skill and version labels.
    # Revealing the manifest or results to a reviewer would break blinding.
    mapping = {"case_aliases": {}, "answer_slots": {}}
    packet = []
    shuffled_cases = list(cases)
    random.Random(int(case_sha[16:32], 16)).shuffle(shuffled_cases)
    for ci, c in enumerate(shuffled_cases, 1):
        alias = "scenario-" + str(ci)
        mapping["case_aliases"][alias] = c["id"]
        candidates = [v for v in results if v["case_id"] == c["id"]]
        random.Random(int(digest(c["id"].encode())[:16], 16)).shuffle(candidates)
        local = []
        for i, v in enumerate(candidates, 1):
            slot = alias + "-answer-" + str(i)
            mapping["answer_slots"][slot] = {
                "case_id": c["id"], "arm": v["arm"]}
            local.append({"slot": slot,
                          "answer": v["response"]["answer"]
                                    if v["response"] else None,
                          "run_status": v["status"]})
        packet.append({"scenario": alias, "task": c["task"],
                       "candidate_answers": local})
    write_private(target / "blind_reviewer_packet.json", packet)
    write_private(target / "private_arm_mapping.json", mapping)
    return {"status": "UNSCORED_EXECUTION", "attempted": len(calls),
            "completed": sum(v["status"] == "COMPLETED" for v in results),
            "output": str(target), "publication_approved": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases", required=True, type=Path)
    p.add_argument("--retrieval-pack", required=True, type=Path)
    p.add_argument("--candidate-skill", required=True, type=Path)
    p.add_argument("--output-dir", required=True, type=Path)
    p.add_argument("--candidate-commit", required=True)
    p.add_argument("--model", default="gpt-5-mini")
    p.add_argument("--execute-api", action="store_true",
                   help="Opt in to at most nine paid calls; default is offline")
    a = p.parse_args()
    try:
        result = run(a.cases, a.retrieval_pack, a.candidate_skill,
                     a.output_dir, a.model, a.candidate_commit,
                     execute=a.execute_api, key=os.getenv("OPENAI_API_KEY"))
    except (PilotError, OSError, UnicodeError, ValueError) as error:
        # Never print source texts, requests, provider messages or tokens.
        code = str(error) if isinstance(error, PilotError) else "INVALID_INPUT_OR_IO"
        print(json.dumps({"status": "HOLD", "reason": code}))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
