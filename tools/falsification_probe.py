#!/usr/bin/env python3
"""Produce blinded one-fact counterfactual packets and score frozen agent replies.

The evaluator checks preregistered labels and provenance, not clinical truth.
No model calls, medical records, or external network access are required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

FACT_TOKEN = re.compile(r"\{\{([A-Za-z][A-Za-z0-9_]*)\}\}")
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")
STAGES = ("S1_question", "S2_evidence", "S3_decision", "S4_review")


class InvalidProbe(ValueError):
    """Bad benchmark contract or unusable/incomplete agent result."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InvalidProbe(message)


def json_bytes(obj: object) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def digest(obj: object) -> str:
    return hashlib.sha256(json_bytes(obj)).hexdigest()


def nonempty_mapping(value: object, name: str) -> dict:
    require(isinstance(value, dict) and bool(value), f"{name} must be a nonempty map")
    require(all(isinstance(k, str) and ID.fullmatch(k)
                and isinstance(v, str) and v.strip() for k, v in value.items()),
            f"{name}: IDs and descriptions must be nonempty strings")
    return value


def gold_check(gold: object, questions: dict, choices: dict,
               fact_ids: set[str], review_ids: set[str], name: str) -> dict:
    require(isinstance(gold, dict), f"{name}: missing gold")
    require(set(gold) == {"question_id", "evidence_ids", "decision_id", "review_flags"},
            f"{name}: gold fields must match the fixed schema")
    require(gold["question_id"] in questions, f"{name}: invalid question")
    require(gold["decision_id"] in choices, f"{name}: invalid decision")
    for key, domain in (("evidence_ids", fact_ids), ("review_flags", review_ids)):
        vals = gold[key]
        require(isinstance(vals, list) and all(isinstance(v, str) and v in domain for v in vals)
                and len(vals) == len(set(vals)), f"{name}: invalid {key}")
    return gold


def validated(spec: dict) -> dict:
    require(isinstance(spec, dict), "spec must be a JSON object")
    require(spec.get("schema_version") == 1, "unsupported schema_version")
    case_id = spec.get("case_id")
    require(isinstance(case_id, str) and ID.fullmatch(case_id), "unsafe case_id")
    require(isinstance(spec.get("task"), str) and spec["task"].strip(), "missing task")
    template = spec.get("case_text")
    require(isinstance(template, str) and template.strip(), "missing case_text")
    facts = nonempty_mapping(spec.get("facts"), "facts")
    questions = nonempty_mapping(spec.get("candidate_questions"), "candidate_questions")
    choices = nonempty_mapping(spec.get("candidate_decisions"), "candidate_decisions")
    review_ids = set(spec.get("review_flag_ids", []))
    require(isinstance(spec.get("review_flag_ids", []), list) and
            all(isinstance(s, str) and ID.fullmatch(s) for s in review_ids) and
            len(review_ids) == len(spec.get("review_flag_ids", [])),
            "invalid review_flag_ids")
    tokens = FACT_TOKEN.findall(template)
    require(set(tokens) == set(facts) and len(tokens) == len(facts),
            "each declared fact must have exactly one {{FACT_ID}} slot")
    require("{{" not in FACT_TOKEN.sub("", template) and "}}" not in FACT_TOKEN.sub("", template),
            "malformed placeholder in template")
    gold_check(spec.get("baseline_gold"), questions, choices, set(facts), review_ids, "baseline")
    probes = spec.get("probes")
    require(isinstance(probes, list) and bool(probes), "requires at least one probe")
    probe_ids = set()
    for probe in probes:
        require(isinstance(probe, dict), "probe must be an object")
        require(set(probe) == {"id", "fact_id", "new_value", "relation", "gold"},
                "probe must specify id/fact_id/new_value/relation/gold")
        pid, fid = probe["id"], probe["fact_id"]
        require(isinstance(pid, str) and ID.fullmatch(pid) and pid != "baseline"
                and pid not in probe_ids, "invalid or duplicate probe id")
        probe_ids.add(pid)
        require(fid in facts, f"{pid}: no such fact")
        require(isinstance(probe["new_value"], str) and probe["new_value"].strip()
                and probe["new_value"] != facts[fid], f"{pid}: fact must actually change")
        require("{{" not in probe["new_value"] and "}}" not in probe["new_value"],
                f"{pid}: nested placeholders prohibited")
        require(probe["relation"] in ("stable", "flip"), f"{pid}: invalid relation")
        gold_check(probe["gold"], questions, choices, set(facts), review_ids, pid)
        baseline_choice = spec["baseline_gold"]["decision_id"]
        expected_choice = probe["gold"]["decision_id"]
        require((baseline_choice == expected_choice) == (probe["relation"] == "stable"),
                f"{pid}: relation contradicts frozen decision gold")
    return spec


def render(template: str, facts: dict[str, str]) -> str:
    return FACT_TOKEN.sub(lambda m: f"[{m.group(1)}] {facts[m.group(1)]}", template)


def build_packets(spec: dict) -> tuple[list[dict], dict]:
    spec = validated(spec)
    packets, answers = [], {}
    variants = [("baseline", None)] + [(p["id"], p) for p in spec["probes"]]
    for pid, probe in variants:
        facts = dict(spec["facts"])
        if probe:
            facts[probe["fact_id"]] = probe["new_value"]
        packet = {
            "schema_version": 1,
            "case_id": spec["case_id"], "probe_id": pid,
            "task": spec["task"],
            "case_text": render(spec["case_text"], facts),
            "candidate_questions": spec["candidate_questions"],
            "candidate_decisions": spec["candidate_decisions"],
            "available_evidence_ids": sorted(facts),
            "available_review_flag_ids": sorted(spec.get("review_flag_ids", [])),
        }
        packet["packet_sha256"] = digest(packet)
        packets.append(packet)
        answers[pid] = {
            "packet_sha256": packet["packet_sha256"],
            "gold": spec["baseline_gold"] if probe is None else probe["gold"],
            "relation": "baseline" if probe is None else probe["relation"],
        }
    key = {"schema_version": 1, "case_id": spec["case_id"],
           "spec_sha256": digest(spec), "answers": answers}
    return packets, key


def prepare(spec_path: Path, reviewer_dir: Path, key_path: Path) -> list[dict]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    packets, key = build_packets(spec)
    reviewer_dir = reviewer_dir.resolve()
    key_path = key_path.resolve()
    require(reviewer_dir != key_path.parent and reviewer_dir not in key_path.parents,
            "gold key cannot reside in reviewer packet directory")
    require(not reviewer_dir.exists() and not key_path.exists(),
            "refuse to overwrite a previously frozen trial")
    reviewer_dir.mkdir(parents=True)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    for p in packets:
        (reviewer_dir / (p["probe_id"] + ".json")).write_text(
            json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # The owner must place evaluator key under separate access control.
    with key_path.open("x", encoding="utf-8") as out:
        out.write(json.dumps(key, ensure_ascii=False, indent=2) + "\n")
    return packets


def score(key: dict, responses: dict) -> dict:
    require(key.get("schema_version") == 1 and isinstance(key.get("answers"), dict),
            "invalid evaluator key")
    require(responses.get("case_id") == key.get("case_id"), "case_id mismatch")
    replies = responses.get("responses")
    require(isinstance(replies, list), "responses must be a list")
    indexed = {}
    for reply in replies:
        require(isinstance(reply, dict) and isinstance(reply.get("probe_id"), str),
                "each response requires a probe_id")
        pid = reply["probe_id"]
        require(pid not in indexed, f"duplicate response: {pid}")
        indexed[pid] = reply
    require(set(indexed) == set(key["answers"]), "missing or extra probe responses")
    results = []
    for pid, answer in key["answers"].items():
        reply = indexed[pid]
        require(reply.get("packet_sha256") == answer["packet_sha256"],
                f"{pid}: stale or wrong packet_sha256")
        gold = answer["gold"]
        require(isinstance(reply.get("evidence_ids"), list) and
                isinstance(reply.get("review_flags"), list), f"{pid}: missing evidence/review lists")
        problems = []
        for stage, field in zip(STAGES, ("question_id", "evidence_ids", "decision_id", "review_flags")):
            actual = reply.get(field)
            expected = gold[field]
            if field in ("evidence_ids", "review_flags"):
                require(all(isinstance(x, str) for x in actual) and
                        len(actual) == len(set(actual)), f"{pid}: malformed {field}")
                if set(actual) != set(expected):
                    problems.append(stage)
            elif actual != expected:
                problems.append(stage)
        results.append({"probe_id": pid, "passed": not problems,
                        "failed_stages": problems,
                        "first_observed_mismatch": problems[0] if problems else None})
    by_id = {r["probe_id"]: r for r in results}
    base = indexed["baseline"]["decision_id"]
    for pid, answer in key["answers"].items():
        if pid == "baseline":
            continue
        actual_relation = "stable" if indexed[pid]["decision_id"] == base else "flip"
        by_id[pid]["relation_passed"] = actual_relation == answer["relation"]
        by_id[pid]["observed_relation"] = actual_relation
        by_id[pid]["expected_relation"] = answer["relation"]
    passed = all(r["passed"] and r.get("relation_passed", True) for r in results)
    return {"case_id": key["case_id"], "passed": passed,
            "trial_count": len(results), "results": results,
            "limitations": [
                "Gold labels must be independently clinically adjudicated before any medical inference.",
                "First observed mismatch is not a proven causal root or an execution-time trace.",
                "Packet fingerprints check input identity, not true model-context isolation.",
                "Machine grading does not validate explanation quality, cited-source sufficiency or actual reader benefit.",
            ]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    a = sub.add_parser("prepare", help="render blinded packets and separate evaluator key")
    a.add_argument("--spec", type=Path, required=True)
    a.add_argument("--reviewer-dir", type=Path, required=True)
    a.add_argument("--key", type=Path, required=True)
    b = sub.add_parser("score", help="compare frozen agent responses with evaluator key")
    b.add_argument("--key", type=Path, required=True)
    b.add_argument("--responses", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            packets = prepare(args.spec, args.reviewer_dir, args.key)
            print(json.dumps({"prepared": len(packets), "case_id": packets[0]["case_id"],
                              "status": "PACKETS_ONLY_NOT_A_MODEL_EVALUATION"}))
            return 0
        key = json.loads(args.key.read_text(encoding="utf-8"))
        replies = json.loads(args.responses.read_text(encoding="utf-8"))
        report = score(key, replies)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["passed"] else 1
    except (InvalidProbe, ValueError, OSError, KeyError) as exc:
        print(f"PROBE_HOLD: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
