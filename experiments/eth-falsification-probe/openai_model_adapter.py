#!/usr/bin/env python3
"""Opt-in single-packet OpenAI Responses API adapter for ETH Probe.

THIS IS A MODEL RUNNER, NOT A CLINICAL VALIDATOR.
Only declared synthetic packets are allowed without explicit external-data authorization.
No persistent provider conversation, web tools, source downloads or gold files.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

ALLOWED_VARIANTS = ("native", "clinical_lite")
CLAIM_STATES = ("supported", "refuted", "undetermined")
SUFFICIENCY = ("sufficient", "insufficient")
MAX_INPUT_BYTES = 32000
MAX_RESPONSE_BYTES = 200000
MAX_OUTPUT_TOKENS = 950


class ProbeModelError(Exception):
    pass


def check_packet(packet: object) -> dict:
    if not isinstance(packet, dict) or packet.get("schema_version") != 1:
        raise ProbeModelError("BAD_PACKET_SCHEMA")
    case_id = packet.get("case_id")
    if not isinstance(case_id, str) or not case_id:
        raise ProbeModelError("BAD_CASE_ID")
    if not case_id.startswith("synthetic_") and os.getenv("PROBE_APPROVED_EXTERNAL_DATA") != "true":
        raise ProbeModelError("EXTERNAL_DATA_NOT_AUTHORIZED")
    for k in ("task", "case_text", "packet_sha256", "probe_id"):
        if not isinstance(packet.get(k), str) or not packet[k]:
            raise ProbeModelError("MISSING_PACKET_FIELD")
    for k in ("candidate_questions", "candidate_decisions"):
        if not isinstance(packet.get(k), dict) or not packet[k] or not all(
                isinstance(x, str) and isinstance(y, str) and x and y for x, y in packet[k].items()):
            raise ProbeModelError("BAD_CANDIDATE_MAP")
    for k in ("available_evidence_ids", "available_review_flag_ids"):
        x = packet.get(k)
        if not isinstance(x, list) or any(not isinstance(v, str) for v in x) or len(x) != len(set(x)):
            raise ProbeModelError("BAD_LABEL_LIST")
    if "candidate_claims" in packet and (not isinstance(packet["candidate_claims"], dict)
                                        or not packet["candidate_claims"]):
        raise ProbeModelError("BAD_CLAIMS")
    if "research_aids" in packet and (not isinstance(packet["research_aids"], dict)
                                      or any(k not in {"question_hint", "evidence_hint"}
                                             or not isinstance(v, str)
                                             for k, v in packet["research_aids"].items())):
        raise ProbeModelError("BAD_RESEARCH_AIDS")
    # This field is not present in released reviewer packets. Fail if a key is ever included.
    if any(k in packet for k in ("gold", "baseline_gold", "answers", "relation", "spec_sha256")):
        raise ProbeModelError("GOLD_IN_MODEL_PACKET")
    return packet


def schema_for(packet: dict) -> dict:
    props = {
        "probe_id": {"type": "string", "enum": [packet["probe_id"]]},
        "packet_sha256": {"type": "string", "enum": [packet["packet_sha256"]]},
        "question_id": {"type": "string", "enum": list(packet["candidate_questions"])},
        "evidence_ids": {"type": "array", "items": {"type": "string", "enum": packet["available_evidence_ids"]}},
        "decision_id": {"type": "string", "enum": list(packet["candidate_decisions"])},
        "review_flags": {"type": "array", "items": ({"type": "string", "enum": packet["available_review_flag_ids"]} if packet["available_review_flag_ids"] else {"type": "string"})},
    }
    if "available_support_statuses" in packet:
        props["support_status"] = {"type": "string", "enum": packet["available_support_statuses"]}
    if "candidate_claims" in packet:
        names = list(packet["candidate_claims"])
        props["claim_statuses"] = {
            "type": "object", "additionalProperties": False,
            "properties": {name: {"type": "string", "enum": list(CLAIM_STATES)} for name in names},
            "required": names,
        }
    return {"type": "object", "additionalProperties": False,
            "properties": props, "required": list(props)}


def request_body(packet: dict, variant: str, model: str) -> dict:
    if variant not in ALLOWED_VARIANTS:
        raise ProbeModelError("BAD_VARIANT")
    instructions = (
        "You are evaluating a fictional evidence task. Answer only from the provided "
        "case_text, task, and visible options. Do not guess missing facts. "
        "Return the required JSON fields; never invent labels."
    )
    if variant == "clinical_lite":
        instructions += (
            " Before answering, identify the consequential problem, separate competing "
            "interpretations, attend to discriminating evidence, treat missing information "
            "as unknown rather than negative, and preserve unaffected valid claims. "
            "Do not pretend that an unverified statement is evidence."
        )
    return {
        "model": model, "store": False, "max_output_tokens": MAX_OUTPUT_TOKENS,
        "instructions": instructions,
        "input": json.dumps(packet, sort_keys=True, ensure_ascii=False),
        "text": {"format": {"type": "json_schema", "name": "probe_answer",
                            "strict": True, "schema": schema_for(packet)}},
    }


def model_inference(packet: dict, variant: str, model: str, key: str,
                    opener=None) -> tuple[dict, dict]:
    if not key:
        raise ProbeModelError("OPENAI_KEY_MISSING")
    if not model or len(model) > 100 or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-._" for c in model):
        raise ProbeModelError("MODEL_ID_INVALID")
    payload = request_body(check_packet(packet), variant, model)
    url = "https://api.openai.com/v1/responses"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST")
    try:
        with (opener or urllib.request.urlopen)(req, timeout=55) as res:
            raw = res.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        # Never print provider errors: they may include account or request data.
        raise ProbeModelError("MODEL_HTTP_" + str(exc.code if isinstance(exc.code, int) else 0)) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ProbeModelError("MODEL_NETWORK_OR_TIMEOUT") from None
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ProbeModelError("RESPONSE_TOO_LARGE")
    try:
        data = json.loads(raw)
        if data.get("status") not in ("completed", None):
            raise ProbeModelError("MODEL_NOT_COMPLETED")
        fragments = [part["text"] for msg in data.get("output", [])
                     if msg.get("type") == "message" for part in msg.get("content", [])
                     if part.get("type") == "output_text"]
        if not fragments:
            raise ProbeModelError("MODEL_OUTPUT_MISSING")
        answer = json.loads("".join(fragments))
    except (ValueError, TypeError, KeyError, AttributeError):
        raise ProbeModelError("MODEL_OUTPUT_INVALID") from None
    expected = schema_for(packet)["required"]
    if not isinstance(answer, dict) or set(answer) != set(expected):
        raise ProbeModelError("MODEL_OUTPUT_FIELDS_INVALID")
    for label, options in (("question_id", packet["candidate_questions"]),
                           ("decision_id", packet["candidate_decisions"])):
        if answer[label] not in options:
            raise ProbeModelError("MODEL_UNKNOWN_LABEL")
    if answer["probe_id"] != packet["probe_id"] or answer["packet_sha256"] != packet["packet_sha256"]:
        raise ProbeModelError("MODEL_PACKET_MISMATCH")
    for k, allowed in (("evidence_ids", packet["available_evidence_ids"]),
                       ("review_flags", packet["available_review_flag_ids"])):
        xs = answer[k]
        if not isinstance(xs, list) or len(xs) != len(set(xs)) or any(x not in allowed for x in xs):
            raise ProbeModelError("MODEL_INVALID_LIST")
    if "support_status" in expected and answer["support_status"] not in packet["available_support_statuses"]:
        raise ProbeModelError("MODEL_INVALID_SUPPORT")
    if "claim_statuses" in expected and (not isinstance(answer["claim_statuses"], dict)
        or set(answer["claim_statuses"]) != set(packet["candidate_claims"])
        or any(v not in CLAIM_STATES for v in answer["claim_statuses"].values())):
        raise ProbeModelError("MODEL_INVALID_CLAIM_STATE")
    usage = data.get("usage") or {}
    metrics = {k: v for k, v in usage.items() if k in ("input_tokens", "output_tokens", "total_tokens")
               and type(v) is int and 0 <= v <= 1000000}
    return answer, metrics


def main() -> int:
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ProbeModelError("INPUT_TOO_LARGE")
        packet = check_packet(json.loads(raw))
        variant = os.getenv("PROBE_VARIANT", "native")
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
        answer, usage = model_inference(packet, variant, model, os.getenv("OPENAI_API_KEY", ""))
        # stdout is *only* the runner's validated model answer. Never echo the key/request.
        sys.stdout.write(json.dumps(answer, ensure_ascii=False) + "\n")
        # Usage values only; intentionally no prompts, model outputs or keys.
        sys.stderr.write("PROBE_USAGE " + json.dumps(usage, sort_keys=True) + "\n")
        return 0
    except (ProbeModelError, ValueError, TypeError) as exc:
        code = str(exc) if isinstance(exc, ProbeModelError) else "INVALID_INPUT"
        sys.stderr.write("PROBE_HOLD " + code + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
