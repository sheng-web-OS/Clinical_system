#!/usr/bin/env python3
"""XDT-01: one private first-pass task/arm, with real optional Skill selection.

This is an execution adapter, NOT a benchmark, scorer, examiner or scheduler.
Default mode is offline. Live mode requires an explicit operator flag, a
separately approved provider budget, and a private execution environment.
Run each arm in an independent process/context, with only one case packet.
Never run hidden cases inside a public GitHub Actions job.
"""
import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "gpt-5.6-terra"  # pinned to the existing #225 development executor
CLOSEOUT_UTC = datetime(2026, 11, 1, 6, 20, 15, tzinfo=timezone.utc)
MAX_TASK_BYTES = 16000
MAX_SKILL_BYTES = 6000
MAX_REQUEST_BYTES = 32000
HEX = re.compile(r"[0-9a-f]{64}\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")
BASE = (
    "Answer this one non-medical decision task using only the supplied packet. "
    "Do not invent evidence, access external systems, or take real-world actions. "
    "Separate verified facts from unknowns. Give the least speculative actionable "
    "decision and the condition that would change it. Do not mention trials."
)
EVIDENCE = (
    "Check the provenance and dates of supporting evidence, reconcile competing "
    "records, and explicitly defer conclusions not justified by the packet."
)
# Fixed candidate inventory only: this does NOT contain the six-step Skill.
INVENTORY = (
    "Optional skill: domain-neutral decision audit. Useful for consequential "
    "choices with competing explanations, conflicting records or a decision "
    "threshold; not useful for trivial factual lookup, straightforward reporting "
    "or questions without a meaningful decision. You may decline it."
)
SELECT = (
    "Before answering, decide whether to load the optional decision-audit Skill "
    "for this task. Choose based on expected improvement, not because it exists. "
    "Return exactly USE or SKIP, no explanation or answer."
)
SKILL_PREFIX = (
    "You chose USE. Apply the following frozen optional skill only where relevant. "
    "Do not manufacture a conflict or infer missing evidence.\n\n"
)

class TrialError(ValueError):
    pass


class ProviderCallError(TrialError):
    def __init__(self, code, evidence=None):
        super().__init__(code)
        self.evidence = evidence or {}

def require(ok, reason):
    if not ok:
        raise TrialError(reason)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def private_read(path, max_bytes, repo_root, label):
    p = Path(path)
    require(p.is_file() and not p.is_symlink(), label + "_INVALID_FILE")
    absolute = p.resolve()
    require(not absolute.is_relative_to(repo_root), label + "_INSIDE_PUBLIC_REPO")
    raw = p.read_bytes()
    require(0 < len(raw) <= max_bytes, label + "_SIZE_OUT_OF_RANGE")
    return raw.decode("utf-8"), sha256(raw)

def get_skill(path, expected_hash, repo_root):
    require(bool(path) and HEX.fullmatch(expected_hash or "") is not None,
            "SKILL_PIN_REQUIRED")
    p = Path(path)
    require(p.is_file() and not p.is_symlink(), "SKILL_INVALID_FILE")
    require(p.resolve().is_relative_to(repo_root), "SKILL_MUST_BE_PUBLIC_CODE")
    raw = p.read_bytes()
    require(0 < len(raw) <= MAX_SKILL_BYTES, "SKILL_SIZE_OUT_OF_RANGE")
    require(sha256(raw) == expected_hash, "SKILL_BYTES_CHANGED")
    return raw.decode("utf-8")

def make_request(task, instructions, max_output_tokens):
    obj = {
        "model": MODEL, "store": False,
        "reasoning": {"effort": "medium"},
        "max_output_tokens": max_output_tokens,
        "instructions": instructions, "input": task,
    }
    require(len(json.dumps(obj, ensure_ascii=False).encode()) <= MAX_REQUEST_BYTES,
            "MODEL_INPUT_TOO_LARGE")
    return obj

def parse_provider_response(response):
    require(isinstance(response, dict) and response.get("status") == "completed",
            "PROVIDER_NOT_COMPLETED")
    require(isinstance(response.get("id"), str) and
            re.fullmatch(r"resp_[A-Za-z0-9_-]+", response["id"]) is not None,
            "PROVIDER_RECEIPT_MISSING")
    returned = response.get("model")
    require(isinstance(returned, str) and
            (returned == MODEL or returned.startswith(MODEL + "-")),
            "MODEL_MISMATCH")
    usage = response.get("usage")
    require(isinstance(usage, dict) and
            all(type(usage.get(k)) is int and usage[k] >= 0
                for k in ("input_tokens", "output_tokens", "total_tokens")) and
            usage["input_tokens"] + usage["output_tokens"] == usage["total_tokens"],
            "PROVIDER_USAGE_INVALID")
    text = "".join(
        piece.get("text", "") for item in response.get("output", [])
        if isinstance(item, dict) and item.get("type") == "message"
        for piece in item.get("content", [])
        if isinstance(piece, dict) and piece.get("type") == "output_text"
        and isinstance(piece.get("text"), str)
    ).strip()
    require(bool(text), "EMPTY_FIRST_PASS")
    return {"text": text, "response_id": response["id"],
            "model": returned, "usage": usage}

def safe_response_evidence(response):
    """Retain bounded metadata even when the first pass cannot be parsed."""
    evidence = {"billing_status": "UNKNOWN_BILLED"}
    if not isinstance(response, dict):
        return evidence
    ident = response.get("id")
    if isinstance(ident, str) and re.fullmatch(r"resp_[A-Za-z0-9_-]{1,120}", ident):
        evidence["response_id"] = ident
    status = response.get("status")
    if isinstance(status, str) and status in {"completed", "failed", "in_progress", "cancelled", "queued", "incomplete"}:
        evidence["provider_status"] = status
    model = response.get("model")
    if isinstance(model, str) and len(model) <= 100 and (model == MODEL or model.startswith(MODEL + "-")):
        evidence["model"] = model
    usage = response.get("usage")
    if isinstance(usage, dict):
        fields = ("input_tokens", "output_tokens", "total_tokens")
        known = {k: usage[k] for k in fields
                 if type(usage.get(k)) is int and 0 <= usage[k] < 2**63}
        if known:
            evidence["usage"] = known
            evidence["usage_consistent"] = len(known) == 3 and known["input_tokens"] + known["output_tokens"] == known["total_tokens"]
            details = usage.get("output_tokens_details")
            if isinstance(details, dict) and type(details.get("reasoning_tokens")) is int:
                if 0 <= details["reasoning_tokens"] <= known.get("output_tokens", -1):
                    evidence["usage"]["output_tokens_details"] = {"reasoning_tokens": details["reasoning_tokens"]}
    details = response.get("incomplete_details")
    if isinstance(details, dict) and isinstance(details.get("reason"), str) and details.get("reason") in {"max_output_tokens", "content_filter"}:
        evidence["incomplete_reason"] = details["reason"]
    return evidence


def safe_header_evidence(headers):
    evidence = {}
    if headers is not None:
        request_id = headers.get("x-request-id")
        if isinstance(request_id, str) and re.fullmatch(r"[A-Za-z0-9._-]{1,160}", request_id):
            evidence["provider_request_id"] = request_id
    return evidence


def api_call(request, attempt_id=None):
    # This function is reached only after the durable attempt reservation.
    require(isinstance(attempt_id, str) and re.fullmatch(r"[A-Za-z0-9._-]{1,160}", attempt_id),
            "PERSISTENT_ATTEMPT_REQUIRED")
    key = os.environ.get("OPENAI_API_KEY")
    require(bool(key), "PRIVATE_API_KEY_MISSING")
    payload = json.dumps(request, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses", data=payload,
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json",
                 "X-Client-Request-Id": attempt_id}, method="POST")
    metadata = {}
    try:
        with urllib.request.urlopen(req, timeout=90) as reply:
            metadata = safe_header_evidence(reply.headers)
            metadata["http_status"] = reply.status
            raw = reply.read(900001)
            if len(raw) > 900000:
                raise ProviderCallError("PROVIDER_RESPONSE_TOO_LARGE", metadata)
            result = json.loads(raw)
    except urllib.error.HTTPError as error:
        metadata.update(safe_header_evidence(error.headers))
        metadata["http_status"] = error.code
        # Do not retain the error body, URL, credentials, or arbitrary message.
        raise ProviderCallError("PROVIDER_HTTP_ERROR", metadata) from None
    except (TimeoutError, socket.timeout):
        raise ProviderCallError("PROVIDER_TIMEOUT", metadata) from None
    except urllib.error.URLError as error:
        category = "PROVIDER_TIMEOUT" if isinstance(error.reason, (TimeoutError, socket.timeout)) else "PROVIDER_NETWORK_ERROR"
        raise ProviderCallError(category, metadata) from None
    except (ValueError, UnicodeError):
        raise ProviderCallError("PROVIDER_INVALID_JSON", metadata) from None
    except OSError:
        raise ProviderCallError("PROVIDER_IO_ERROR", metadata) from None
    # Local metadata is kept separate from provider text and never sent back.
    if isinstance(result, dict):
        result = dict(result)
        result["_transport_evidence"] = metadata
    else:
        raise ProviderCallError("PROVIDER_INVALID_RESPONSE_SHAPE", metadata)
    return result

def run_arm(task, arm, skill_loader=None, caller=api_call, on_event=None,
            attempt_journal=None):
    """One context per arm; C asks for selection before seeing Skill bytes."""
    require(arm in {"A", "B", "C"}, "INVALID_ARM")
    common = BASE + ("\n\n" + EVIDENCE if arm != "A" else "")
    calls = []
    selection = None
    attempted = 0
    require(caller is not api_call or attempt_journal is not None,
            "PERSISTENT_ATTEMPT_REQUIRED")

    def ask(instructions, cap):
        nonlocal attempted
        req = make_request(task, instructions, cap)
        attempted += 1
        kind = "selection" if arm == "C" and attempted == 1 else "answer"
        attempt_id = None
        if attempt_journal is not None:
            request_hash = sha256(json.dumps(req, ensure_ascii=False, sort_keys=True).encode("utf-8"))
            attempt_id = attempt_journal.reserve(attempted, kind, request_hash)
        evidence = {"billing_status": "UNKNOWN_BILLED"}
        try:
            response = api_call(req, attempt_id=attempt_id) if caller is api_call else caller(req)
            evidence.update(safe_response_evidence(response))
            if isinstance(response, dict):
                evidence.update(response.get("_transport_evidence", {}))
            value = parse_provider_response(response)
            require(value["response_id"] not in
                    {v["response_id"] for v in calls},
                    "REUSED_PROVIDER_RESPONSE")
            if kind == "selection":
                require(value["text"].strip() in {"USE", "SKIP"},
                        "INVALID_SELECTION_FIRST_PASS")
        except BaseException as error:
            code = str(error) if isinstance(error, TrialError) else (
                "PROVIDER_TIMEOUT" if isinstance(error, (TimeoutError, socket.timeout)) else "PROVIDER_OR_PROCESS_INTERRUPTED")
            if not re.fullmatch(r"[A-Z][A-Z0-9_]{0,79}", code):
                code = "PROVIDER_CALL_FAILED"
            evidence.update(getattr(error, "evidence", {}))
            evidence.update({"state": "FAILED_OR_INCOMPLETE", "code": code,
                             "billing_status": "UNKNOWN_BILLED"})
            if attempt_journal is not None:
                attempt_journal.finish(attempted, evidence)
            if not isinstance(error, Exception):
                raise
            raise TrialError(code) from None
        evidence["state"] = "PROVIDER_COMPLETED"
        if attempt_journal is not None:
            attempt_journal.finish(attempted, evidence)
        calls.append(value)
        if on_event is not None:
            on_event({
                "call_index": len(calls),
                "kind": "selection" if arm == "C" and len(calls) == 1 else "answer",
                "text": value["text"], "response_id": value["response_id"],
                "model": value["model"], "usage": value["usage"],
                "attempt_id": attempt_id, "billing_status": "UNKNOWN_BILLED",
            })
        return value

    if arm == "C":
        require(callable(skill_loader), "C_REQUIRES_CONDITIONAL_SKILL_LOADER")
        # First call cannot access the full Skill, by construction.
        choice = ask(common + "\n\n" + INVENTORY + "\n\n" + SELECT, 350)
        selection = choice["text"].strip()
        require(selection in {"USE", "SKIP"}, "INVALID_SELECTION_FIRST_PASS")
        if selection == "USE":
            full_skill = skill_loader()
            common += "\n\n" + SKILL_PREFIX + full_skill
        else:
            common += "\n\nThe optional Skill was not loaded. Answer normally."
    answer = ask(common, 1050 if arm == "C" else 1400)
    return {
        "arm": arm, "selection": selection,
        "skill_loaded": selection == "USE",
        "first_pass": answer["text"], "answer_response_id": answer["response_id"],
        "provider_calls": len(calls),
        "provider_attempts": attempted,
        "billing_status": "UNKNOWN_BILLED",
        "usage": {
            k: sum(x["usage"][k] for x in calls)
            for k in ("input_tokens", "output_tokens", "total_tokens")
        },
        "receipts": [{"response_id": c["response_id"], "model": c["model"],
                      "usage": c["usage"]} for c in calls],
    }

def write_once(path, content):
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())

def verify_commit(expected, repo_root):
    require(SHA.fullmatch(expected or "") is not None, "COMMIT_PIN_REQUIRED")
    try:
        r = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        raise TrialError("CHECKOUT_UNVERIFIED") from None
    require(r.returncode == 0 and r.stdout.strip() == expected,
            "CHECKOUT_HEAD_CHANGED")

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=("A", "B", "C"), required=True)
    parser.add_argument("--task-file", type=Path, required=True)
    parser.add_argument("--task-sha256", required=True)
    parser.add_argument("--skill-file", type=Path)
    parser.add_argument("--skill-sha256")
    parser.add_argument("--candidate-commit", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--execute-api", action="store_true")
    parser.add_argument("--budget-authorized", action="store_true")
    parser.add_argument("--frozen-repo", type=Path)
    parser.add_argument("--attempt-dir", type=Path)
    args = parser.parse_args(argv)
    root = (args.frozen_repo or Path(__file__).resolve().parents[1]).resolve()
    verify_commit(args.candidate_commit, root)
    require(HEX.fullmatch(args.task_sha256) is not None, "TASK_PIN_REQUIRED")
    task, digest = private_read(args.task_file, MAX_TASK_BYTES, root, "CASE")
    require(digest == args.task_sha256, "TASK_BYTES_CHANGED")
    require(args.arm == "C" or
            (args.skill_file is None and args.skill_sha256 is None),
            "A_B_MUST_NOT_BE_EXPOSED_TO_SKILL")
    if args.arm == "C":
        require(args.skill_file is not None and
                HEX.fullmatch(args.skill_sha256 or "") is not None,
                "C_REQUIRES_FROZEN_SKILL")
    if args.arm == "C":
        # Pin and check bytes before any paid call; the MODEL still sees only
        # the inventory until its own USE selection is frozen.
        get_skill(args.skill_file, args.skill_sha256, root)
    target = args.output_dir.resolve()
    require(not target.is_relative_to(root) and not target.exists(),
            "PRIVATE_FRESH_OUTPUT_REQUIRED")
    target.mkdir(mode=0o700, parents=False)
    meta = {"schema_version": 1, "arm": args.arm, "task_sha256": digest,
            "candidate_commit": args.candidate_commit,
            "status": "PREFLIGHT_ONLY_NO_MODEL_OUTCOME", "independent_review": "NOT_DONE",
            "provider_billing_verified": False,
            "runtime_sha256": sha256(Path(__file__).read_bytes()),
            "protocol_changed": False}
    write_once(target / "preflight.json", meta)
    if not args.execute_api:
        print("PLAN_ONLY_NO_MODEL_CALLS")
        return 0
    require(args.budget_authorized, "BUDGET_AUTHORIZATION_REQUIRED")
    require(datetime.now(timezone.utc) >= CLOSEOUT_UTC, "ORIGINAL_72H_STILL_OPEN")
    require(bool(os.environ.get("OPENAI_API_KEY")), "PRIVATE_API_KEY_MISSING")
    require(args.attempt_dir is not None, "PERSISTENT_ATTEMPT_REQUIRED")
    from xdt01_attempt_journal import AttemptJournal
    journal = AttemptJournal(args.attempt_dir, args.arm, digest, args.candidate_commit)
    loader = (lambda: get_skill(args.skill_file, args.skill_sha256, root)
              if args.arm == "C" else None)
    def retain_receipt(event):
        write_once(target / ("call-%02d.json" % event["call_index"]), event)
    try:
        result = run_arm(task, args.arm, skill_loader=loader,
                         caller=api_call, on_event=retain_receipt,
                         attempt_journal=journal)
        result.update({"task_sha256": digest,
                       "candidate_commit": args.candidate_commit,
                       "skill_sha256": args.skill_sha256 if args.arm == "C" else None,
                       "independent_review": "NOT_DONE",
                       "provider_billing_verified": False,
                       "runtime_sha256": sha256(Path(__file__).read_bytes()),
                       "protocol_changed": False,
                       "status": "FIRST_PASS_UNSCORED"})
        write_once(target / "first_pass.json", result)
    except (TrialError, ValueError) as error:
        # Never print the private task, returned content or provider detail.
        write_once(target / "failure.json",
                   {"status": "FAILED_OR_INCOMPLETE", "code": str(error),
                    "billing_status": "UNKNOWN_BILLED",
                    "attempt_journal_retained": True})
        print("FAILED_OR_INCOMPLETE")
        return 2
    print("FIRST_PASS_UNSCORED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
