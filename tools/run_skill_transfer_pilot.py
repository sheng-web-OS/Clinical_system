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
    return {"answer": answer, "returned_model": returned_model,
            "response_id": obj.get("id"), "usage": obj.get("usage")}


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
    return extract_output(data)


def write_private(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, sort_keys=True,
                       indent=2) + "\n").encode("utf-8")
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as file:
        file.write(data)


def run(cases_path, pack_path, skill_path, target, model, commit,
        execute=False, key=None, caller=None):
    case_text, case_sha = read_text(cases_path)
    pack, pack_sha = read_text(pack_path)
    skill, skill_sha = read_text(skill_path)
    cases = clean_cases(json.loads(case_text))
    require("name: decision-question-triage" in skill,
            "WRONG_SKILL_SELECTED")
    if execute:
        require(bool(key), "MODEL_SECRET_NOT_CONFIGURED")
    target = Path(target)
    require(not target.exists(), "OUTPUT_EXISTS_REFUSE_TO_REWRITE")
    meta, calls = build_plan(cases, case_sha, pack, pack_sha,
                             skill, skill_sha, model, commit)
    target.mkdir(mode=0o700, parents=False)
    write_private(target / "manifest.json", meta)
    # Private full requests are retained locally; never in public Actions artifacts.
    write_private(target / "requests.json", calls)
    if not execute:
        return {"status": "PLAN_ONLY_NO_MODEL_CALLS", "planned": len(calls),
                "output": str(target), "model": model}
    results = []
    for call in calls:
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
    write_private(target / "first_pass_results.json", results)
    # The review packet excludes arm names, request texts, skill and version labels.
    # Revealing the manifest or results to a reviewer would break blinding.
    mapping = {}
    packet = []
    for c in cases:
        candidates = [v for v in results if v["case_id"] == c["id"]]
        random.Random(int(digest(c["id"].encode())[:16], 16)).shuffle(candidates)
        local = []
        for i, v in enumerate(candidates, 1):
            slot = c["id"] + "-answer-" + str(i)
            mapping[slot] = v["arm"]
            local.append({"slot": slot,
                          "answer": v["response"]["answer"]
                                    if v["response"] else None,
                          "run_status": v["status"]})
        packet.append({"case_id": c["id"], "task": c["task"],
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
