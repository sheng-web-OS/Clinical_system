#!/usr/bin/env python3
"""Produce blinded one-fact counterfactual packets and score frozen agent replies.

The evaluator checks preregistered labels and provenance, not clinical truth.
No model calls, medical records, or external network access are required.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
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


RESCUE_ARMS = ("N", "Q", "E", "QE")


def prepare_rescue(spec_path: Path, hints_path: Path,
                   reviewer_root: Path, key_root: Path) -> dict:
    """Create four intentionally unequal-information *diagnostic* conditions.

    The Q/E aids are supplied by an adjudicator; they are not discoveries by
    this tool, and comparing arms does not measure autonomous clinical ability.
    """
    spec = validated(json.loads(spec_path.read_text(encoding="utf-8")))
    hints = json.loads(hints_path.read_text(encoding="utf-8"))
    require(isinstance(hints, dict) and set(hints) == {"question_hint", "evidence_hint"},
            "hints must provide question_hint and evidence_hint only")
    require(all(isinstance(x, str) and x.strip() and len(x) <= 3000
                for x in hints.values()), "hints must be 1-3000 nonempty characters")
    packets, common_key = build_packets(spec)
    reviewer_root, key_root = reviewer_root.resolve(), key_root.resolve()
    require(reviewer_root != key_root and
            reviewer_root not in key_root.parents and
            key_root not in reviewer_root.parents,
            "reviewer and key roots must be disjoint")
    require(not reviewer_root.exists() and not key_root.exists(),
            "refuse to overwrite a frozen rescue experiment")
    reviewer_root.mkdir(parents=True)
    key_root.mkdir(parents=True)
    manifest = {"schema_version": 1, "case_id": spec["case_id"],
                "spec_sha256": digest(spec), "arms": {}}
    for arm in RESCUE_ARMS:
        reviewer = reviewer_root / arm
        reviewer.mkdir()
        answers = {}
        for original in packets:
            packet = dict(original)
            packet.pop("packet_sha256")
            aids = {}
            if "Q" in arm:
                aids["question_hint"] = hints["question_hint"]
            if "E" in arm:
                aids["evidence_hint"] = hints["evidence_hint"]
            if aids:
                packet["research_aids"] = aids
            packet["packet_sha256"] = digest(packet)
            (reviewer / (packet["probe_id"] + ".json")).write_text(
                json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            answers[packet["probe_id"]] = {
                "packet_sha256": packet["packet_sha256"],
                "gold": common_key["answers"][packet["probe_id"]]["gold"],
                "relation": common_key["answers"][packet["probe_id"]]["relation"],
            }
        key = {"schema_version": 1, "case_id": spec["case_id"],
               "spec_sha256": digest(spec), "answers": answers}
        (key_root / (arm + ".json")).write_text(
            json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest["arms"][arm] = {"packets": len(packets),
                                 "packet_set_sha256": digest(sorted(a["packet_sha256"] for a in answers.values()))}
    (key_root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def run_adapter(reviewer_dir: Path, responses_path: Path, adapter: Path,
                timeout: int = 30, allowed_env: tuple[str, ...] = ()) -> dict:
    """Execute a provided local executable once per frozen packet, without gold.

    No provider/network safety promise: the adapter itself is trusted software.
    """
    reviewer_dir = reviewer_dir.resolve()
    responses_path = responses_path.resolve()
    adapter = adapter.resolve()
    require(reviewer_dir.is_dir(), "missing reviewer packet directory")
    require(adapter.is_file() and (adapter.suffix == ".py" or os.access(adapter, os.X_OK)),
            "adapter must be a Python script or an executable local file")
    require(1 <= timeout <= 600, "timeout must be between 1 and 600 seconds")
    require(not responses_path.exists(), "refuse to overwrite frozen responses")
    require(responses_path.parent != reviewer_dir and reviewer_dir not in responses_path.parents,
            "response file must be outside reviewer packet directory")
    require(all(re.fullmatch(r"[A-Z_][A-Z0-9_]*", k) for k in allowed_env),
            "invalid allow-env name")
    env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL") if k in os.environ}
    for k in allowed_env:
        require(k in os.environ, f"requested environment variable is absent: {k}")
        env[k] = os.environ[k]
    command = [sys.executable, str(adapter)] if adapter.suffix == ".py" else [str(adapter)]
    files = sorted(reviewer_dir.glob("*.json"))
    require(bool(files), "no reviewer packets")
    seen = set()
    case_id = None
    outputs = []
    for path in files:
        packet = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(packet, dict) and packet.get("schema_version") == 1,
                f"{path.name}: bad packet schema")
        pid = packet.get("probe_id")
        require(isinstance(pid, str) and ID.fullmatch(pid) and pid == path.stem and pid not in seen,
                f"{path.name}: invalid/duplicate probe ID")
        seen.add(pid)
        require(packet.get("packet_sha256") == digest({k: v for k, v in packet.items()
                                                        if k != "packet_sha256"}),
                f"{pid}: altered packet or SHA")
        if case_id is None:
            case_id = packet.get("case_id")
        require(case_id == packet.get("case_id"), "mixed case IDs")
        try:
            finished = subprocess.run(command, input=json.dumps(packet, ensure_ascii=False),
                                      text=True, capture_output=True, timeout=timeout,
                                      env=env, cwd=reviewer_dir, check=False)
        except subprocess.TimeoutExpired:
            raise InvalidProbe(f"{pid}: adapter timeout") from None
        require(finished.returncode == 0, f"{pid}: adapter exited nonzero")
        require(len(finished.stdout) <= 100_000, f"{pid}: adapter stdout too large")
        try:
            reply = json.loads(finished.stdout)
        except (json.JSONDecodeError, TypeError):
            raise InvalidProbe(f"{pid}: adapter did not emit exactly one JSON object") from None
        require(isinstance(reply, dict) and set(reply) == {
            "probe_id", "packet_sha256", "question_id", "evidence_ids",
            "decision_id", "review_flags"}, f"{pid}: unexpected response fields")
        require(reply["probe_id"] == pid and
                reply["packet_sha256"] == packet["packet_sha256"],
                f"{pid}: response does not match packet")
        require(isinstance(reply["question_id"], str) and
                reply["question_id"] in packet["candidate_questions"],
                f"{pid}: invalid question label")
        require(isinstance(reply["decision_id"], str) and
                reply["decision_id"] in packet["candidate_decisions"],
                f"{pid}: invalid decision label")
        for field, available in (("evidence_ids", packet["available_evidence_ids"]),
                                 ("review_flags", packet["available_review_flag_ids"])):
            values = reply[field]
            require(isinstance(values, list) and all(isinstance(v, str) and v in available
                    for v in values) and len(set(values)) == len(values),
                    f"{pid}: invalid {field}")
        outputs.append(reply)
    require("baseline" in seen, "missing baseline packet")
    responses_path.parent.mkdir(parents=True, exist_ok=True)
    # exclusive create; failed runs do not create an incomplete file
    with responses_path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps({"case_id": case_id, "responses": outputs},
                                ensure_ascii=False, indent=2) + "\n")
    return {"case_id": case_id, "executed": len(outputs),
            "status": "ADAPTER_EXECUTED_GOLD_NOT_ACCESSED", "isolation": "NOT_VERIFIED"}


def compare_rescue(key_root: Path, response_root: Path) -> dict:
    """Score four matched rescue conditions; do not infer a causal root."""
    out = {}
    for arm in RESCUE_ARMS:
        key = json.loads((key_root / (arm + ".json")).read_text(encoding="utf-8"))
        responses = json.loads((response_root / (arm + ".json")).read_text(encoding="utf-8"))
        report = score(key, responses)
        out[arm] = {"passed": report["passed"],
                    "failed_stage_counts": {s: sum(s in r["failed_stages"] for r in report["results"])
                                            for s in STAGES},
                    "bad_relation_count": sum(not r.get("relation_passed", True)
                                              for r in report["results"]),
                    "trial_count": report["trial_count"]}
    return {"arms": out, "status": "DIAGNOSTIC_RESCUE_NOT_A_CAUSAL_ROOT",
            "limitations": [
                "The Q/E aids intentionally change information, so this is not a fair equal-information benchmark.",
                "No model-context isolation or clinical gold truth is established by the runner.",
                "Rescue patterns are descriptive until blinded independent adjudication and repeated cases.",
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
    c = sub.add_parser("run", help="execute one trusted local adapter per packet (no gold)")
    c.add_argument("--reviewer-dir", type=Path, required=True)
    c.add_argument("--responses", type=Path, required=True)
    c.add_argument("--adapter", type=Path, required=True)
    c.add_argument("--timeout", type=int, default=30)
    c.add_argument("--allow-env", action="append", default=[])
    d = sub.add_parser("prepare-rescue", help="prepare intentionally assisted N/Q/E/QE arms")
    d.add_argument("--spec", type=Path, required=True)
    d.add_argument("--hints", type=Path, required=True)
    d.add_argument("--reviewer-root", type=Path, required=True)
    d.add_argument("--key-root", type=Path, required=True)
    e = sub.add_parser("compare-rescue", help="descriptive paired arm results")
    e.add_argument("--key-root", type=Path, required=True)
    e.add_argument("--response-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            packets = prepare(args.spec, args.reviewer_dir, args.key)
            print(json.dumps({"prepared": len(packets), "case_id": packets[0]["case_id"],
                              "status": "PACKETS_ONLY_NOT_A_MODEL_EVALUATION"}))
            return 0
        if args.command == "run":
            print(json.dumps(run_adapter(args.reviewer_dir, args.responses, args.adapter,
                                         args.timeout, tuple(args.allow_env))))
            return 0
        if args.command == "prepare-rescue":
            manifest = prepare_rescue(args.spec, args.hints, args.reviewer_root, args.key_root)
            print(json.dumps({"arms": list(manifest["arms"]),
                              "status": "RESCUE_PACKETS_ONLY_NOT_A_MODEL_EVALUATION"}))
            return 0
        if args.command == "compare-rescue":
            report = compare_rescue(args.key_root, args.response_root)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0  # Even a wholly failed diagnostic test is valid data.
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
