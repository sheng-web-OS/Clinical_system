"""EVLOOP-S02: offline, fail-closed event/run evidence consistency checker.

Inputs are untrusted JSON. No field, even a matching "platform_event_binding",
can authenticate platform provenance. Never return PASS/VERIFIED.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SHA = re.compile(r"^[a-fA-F0-9]{40}$")
ACTION = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
HEX32 = re.compile(r"^[0-9a-fA-F]{32}$")
STATUSES = {"in_progress", "completed", "failed", "no_update"}


@dataclass(frozen=True)
class Assessment:
    verdict: str
    findings: tuple[str, ...]
    next_gate: str

    def as_dict(self):
        return asdict(self)


def present(value):
    return value is not None and value != "" and value != "NOT_EXPOSED"


def provider_id(value):
    return isinstance(value, str) and bool(UUID.fullmatch(value) or HEX32.fullmatch(value))


def validate_github(g):
    if not isinstance(g, dict):
        return "GITHUB_RECORD_NOT_OBJECT"
    if any(not present(g.get(k)) for k in ("repository", "pr_number", "head_sha", "event_action")):
        return "MISSING_GITHUB_EVENT_FIELDS"
    if not isinstance(g["repository"], str) or not REPO.fullmatch(g["repository"]):
        return "INVALID_GITHUB_REPOSITORY"
    if type(g["pr_number"]) is not int or g["pr_number"] <= 0:
        return "INVALID_GITHUB_PR_NUMBER"
    if not isinstance(g["head_sha"], str) or not SHA.fullmatch(g["head_sha"]):
        return "INVALID_GITHUB_HEAD_SHA"
    if not isinstance(g["event_action"], str) or not ACTION.fullmatch(g["event_action"]):
        return "INVALID_GITHUB_EVENT_ACTION"
    if present(g.get("event_id")) and (not isinstance(g["event_id"], str) or not UUID.fullmatch(g["event_id"])):
        return "INVALID_GITHUB_DELIVERY_ID"
    return None


def validate_run(r):
    if not isinstance(r, dict):
        return "PLATFORM_RUN_NOT_OBJECT"
    if not r or not present(r.get("id")) or not present(r.get("task_id")):
        return None
    if not provider_id(r["id"]) or not provider_id(r["task_id"]):
        return "INVALID_PLATFORM_ID"
    if "recorded_status" in r and (not isinstance(r["recorded_status"], str) or r["recorded_status"] not in STATUSES):
        return "INVALID_PLATFORM_RUN_STATUS"
    chat = r.get("chat_ref")
    if chat is not None and (not isinstance(chat, dict)
                             or chat.get("type") not in ("chatgpt", "codex")
                             or not isinstance(chat.get("id"), str) or not chat["id"]):
        return "INVALID_CHAT_REF"
    result = r.get("latest_result")
    if result is not None and (not isinstance(result, dict)
                               or not provider_id(result.get("run_id"))):
        return "INVALID_PLATFORM_RESULT"
    return None


def validate_claim(name, c):
    if not isinstance(c, dict):
        return name + "_NOT_OBJECT"
    specs = {
        "pr_number": lambda v: type(v) is int and v > 0,
        "head_sha": lambda v: isinstance(v, str) and bool(SHA.fullmatch(v)),
        "repository": lambda v: isinstance(v, str) and bool(REPO.fullmatch(v)),
        "event_action": lambda v: isinstance(v, str) and bool(ACTION.fullmatch(v)),
        "run_id": provider_id,
        "task_id": provider_id,
        "event_id": provider_id,
    }
    for key, valid in specs.items():
        if key in c and present(c[key]) and not valid(c[key]):
            return name + "_INVALID_" + key.upper()
    return None


def assess(e):
    if not isinstance(e, dict):
        return Assessment("INVALID_EVIDENCE", ("ROOT_NOT_OBJECT",), "Reject input")
    g, r = e.get("github", {}), e.get("platform_run", {})
    receipt = e.get("processing_receipt", {})
    binding = e.get("platform_event_binding", {})
    err = validate_github(g)
    if err:
        verdict = "INSUFFICIENT_GITHUB_EVIDENCE" if err == "MISSING_GITHUB_EVENT_FIELDS" else "INVALID_EVIDENCE"
        return Assessment(verdict, (err,), "Read authenticated GitHub event/ref")
    err = validate_run(r)
    if err:
        return Assessment("INVALID_EVIDENCE", (err,), "Reject malformed platform run")
    for name, data in (("PROCESSING_RECEIPT", receipt), ("PLATFORM_EVENT_BINDING", binding)):
        err = validate_claim(name, data)
        if err:
            return Assessment("INVALID_EVIDENCE", (err,), "Reject malformed claim")
    findings = []
    if not present(g.get("event_id")):
        findings.append("GITHUB_DELIVERY_ID_NOT_EXPOSED")
    if not present(r.get("id")) or not present(r.get("task_id")):
        return Assessment("GITHUB_EVENT_ONLY", tuple(findings + ["PLATFORM_RUN_NOT_OBSERVED"]),
                          "Read authenticated platform run")

    for name, data in (("PROCESSING_RECEIPT", receipt), ("PLATFORM_EVENT_BINDING", binding)):
        for field in ("repository", "pr_number", "head_sha", "event_action"):
            if present(data.get(field)) and data[field] != g[field]:
                return Assessment("CONFLICT", (name + "_" + field.upper() + "_MISMATCH",),
                                  "Stop: conflicting repository/PR/ref evidence")
        for field, ref in (("run_id", "id"), ("task_id", "task_id")):
            if present(data.get(field)) and data[field] != r[ref]:
                return Assessment("CONFLICT", (name + "_" + field.upper() + "_MISMATCH",),
                                  "Stop: wrong task/run")
        if present(data.get("event_id")) and present(g.get("event_id")) and data["event_id"] != g["event_id"]:
            return Assessment("CONFLICT", (name + "_DELIVERY_ID_MISMATCH",), "Stop: delivery mismatch")

    result = r.get("latest_result")
    if result is not None and result["run_id"] != r["id"]:
        return Assessment("CONFLICT", ("PLATFORM_LATEST_RESULT_RUN_MISMATCH",),
                          "Discard stale prior-run result")
    if not binding:
        findings.append("NO_PLATFORM_EVENT_TO_RUN_BINDING")
    else:
        required = ("event_id", "run_id", "task_id", "repository", "pr_number", "head_sha", "event_action")
        for field in required:
            if not present(binding.get(field)):
                findings.append("BINDING_" + field.upper() + "_MISSING")
        if not any(x.startswith("BINDING_") for x in findings):
            findings.append("STRUCTURAL_BINDING_MATCH_NOT_PROVIDER_AUTHENTICATED")
    if r.get("recorded_status") == "no_update" and result is None:
        findings.append("NO_UPDATE_NO_OUTPUT")
    if r.get("chat_ref") is None:
        findings.append("NO_CHAT_REFERENCE")
    if receipt:
        if receipt.get("provenance") != "platform_result":
            findings.append("SELF_REPORTED_RECEIPT_NOT_ATTESTATION")
        elif result is None:
            findings.append("CLAIMED_PLATFORM_RESULT_WITHOUT_OBSERVED_RESULT")
        elif not isinstance(receipt.get("nonce"), str) or not receipt["nonce"]:
            findings.append("NO_PROCESSING_NONCE")
        else:
            findings.append("APPLICATION_PROCESSING_CLAIM_ONLY")

    return Assessment("INCONCLUSIVE", tuple(findings),
                      "Require authenticated platform-native event/run binding")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python provenance_probe.py evidence.json")
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(assess(payload).as_dict(), ensure_ascii=False, indent=2))
