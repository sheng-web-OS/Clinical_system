#!/usr/bin/env python3
"""Stage rich XDT-01 pilot cases OFFLINE; preserve full gold/rubric privately.

Code-only adapter for OWNER_AI_FALLBACK. No model/API call, scoring, independent
identity attestation, or live authorization. Never publish private inputs/outputs.
The multi-case stage is FACILITATOR-ONLY: mount one Hxx.txt in a worker.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
from pathlib import Path

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{3,64}\Z")
EVID_ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,31}\Z")
DOMAINS = {"inventory", "it-incident", "provenance"}
MAX_SOURCE_BYTES = 250_000
MAX_PACKET_BYTES = 12_000  # <= frozen #252 sealer and runner task caps
FROZEN_CANDIDATE = "03f29b980ba326ac0509299b9c94292d6a1a5d5a"


class Hold(Exception):
    pass


def require(ok, reason):
    if not ok:
        raise Hold(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def read_pinned(filename, expected, repo):
    p = Path(filename)
    require(bool(HEX64.fullmatch(expected or "")), "SHA256_PIN_REQUIRED")
    require(p.is_file() and not p.is_symlink(), "INPUT_NOT_REGULAR_FILE")
    resolved = p.resolve(strict=True)
    require(not resolved.is_relative_to(repo), "PUBLIC_REPO_INPUT_FORBIDDEN")
    raw = p.read_bytes()
    require(0 < len(raw) <= MAX_SOURCE_BYTES and sha(raw) == expected,
            "INPUT_DIGEST_MISMATCH_OR_SIZE")
    try:
        return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_pairs)
    except (UnicodeError, ValueError) as exc:
        raise Hold("INVALID_UTF8_JSON") from exc


def require_private_target(path, repo):
    p = Path(path).absolute()
    require(not p.exists() and not p.is_symlink(), "TARGET_ALREADY_EXISTS")
    require(not p.is_relative_to(repo) and not repo.is_relative_to(p),
            "PUBLIC_REPO_OUTPUT_FORBIDDEN")
    require(p.parent.is_dir() and not p.parent.is_symlink(),
            "PRIVATE_PARENT_REQUIRED")
    for ancestor in (p.parent, *p.parent.parents):
        require(not ancestor.is_symlink(), "SYMLINK_ANCESTOR_FORBIDDEN")
    require(p.parent.stat().st_mode & 0o002 == 0,
            "WORLD_WRITABLE_PARENT_FORBIDDEN")
    return p


def exact_keys(obj, required, label):
    require(type(obj) is dict and set(obj) == set(required), label + "_SCHEMA")


def valid_text(x, maxbytes):
    return type(x) is str and 0 < len(x.encode("utf-8")) <= maxbytes


def validate(cases, gold, scoring):
    exact_keys(cases, {"schema_version", "package_id", "source_class", "phase",
                       "instructions", "cases"}, "CASES")
    exact_keys(gold, {"schema_version", "package_id", "keys"}, "GOLD")
    exact_keys(scoring, {"schema_version", "package_id", "status",
                         "method_record", "general_rules", "cases"}, "SCORING")
    require(all(type(x.get("schema_version")) is int and x["schema_version"] == 1
                for x in (cases, gold, scoring)), "SCHEMA_VERSION")
    package_id = cases["package_id"]
    require(type(package_id) is str and SAFE_ID.fullmatch(package_id) and
            gold["package_id"] == package_id and
            scoring["package_id"] == package_id, "PACKAGE_ID_MISMATCH")
    require(cases["phase"] == "pilot" and cases["source_class"] == "synthetic",
            "ONLY_SYNTHETIC_PILOT")
    require(valid_text(cases["instructions"], 3000), "INSTRUCTIONS_INVALID")
    records = cases["cases"]
    require(type(records) is list and len(records) == 3, "THREE_CASES_REQUIRED")
    case_by_id = {}
    domains = set()
    packets = {}
    for case in records:
        exact_keys(case, {"id", "domain", "task", "evidence"}, "CASE")
        cid, domain = case["id"], case["domain"]
        require(type(cid) is str and bool(SAFE_ID.fullmatch(cid)) and
                cid not in case_by_id, "CASE_ID_INVALID_OR_DUPLICATE")
        require(domain in DOMAINS and domain not in domains,
                "DOMAIN_DISTRIBUTION_INVALID")
        require(valid_text(case["task"], 10_000), "TASK_TEXT_INVALID")
        evidence = case["evidence"]
        require(type(evidence) is list and 1 <= len(evidence) <= 30,
                "EVIDENCE_LIST_INVALID")
        evid_ids = set()
        for entry in evidence:
            require(type(entry) is dict and set(entry) in
                    ({"id", "text"}, {"id", "object_path", "utf8_text", "sha256"}),
                    "EVIDENCE_ENTRY_SCHEMA")
            eid = entry["id"]
            require(type(eid) is str and bool(EVID_ID.fullmatch(eid)) and
                    eid not in evid_ids, "EVIDENCE_ID_INVALID")
            evid_ids.add(eid)
            if "text" in entry:
                require(valid_text(entry["text"], 10_000), "EVIDENCE_TEXT_INVALID")
            else:
                require(valid_text(entry["object_path"], 500) and
                        type(entry["utf8_text"]) is str and
                        bool(HEX64.fullmatch(entry["sha256"])) and
                        sha(entry["utf8_text"].encode("utf-8")) == entry["sha256"],
                        "EVIDENCE_OBJECT_HASH_MISMATCH")
        # Entire evidence array is serialized into the one-case input, not dropped.
        worker_object = {"package_id": package_id,
                         "instructions": cases["instructions"],
                         "case": case}
        task = (json.dumps(worker_object, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")) + "\n").encode("utf-8")
        require(len(task) <= MAX_PACKET_BYTES, "ONE_CASE_TASK_TOO_LARGE")
        require(json.loads(task)["case"] == case and
                json.loads(task)["instructions"] == cases["instructions"],
                "NON_LOSSLESS_TASK_ENCODING")
        packets[cid] = task
        case_by_id[cid] = case
        domains.add(domain)
    require(domains == DOMAINS, "MISSING_DOMAIN")
    keys = gold["keys"]
    scored = scoring["cases"]
    require(type(keys) is list and len(keys) == 3 and type(scored) is list
            and len(scored) == 3, "GOLD_OR_SCORING_COUNT")
    def index(items, label):
        by_id = {}
        for item in items:
            require(type(item) is dict and type(item.get("id")) is str and
                    item["id"] not in by_id, label + "_IDS_INVALID")
            by_id[item["id"]] = item
        require(set(by_id) == set(case_by_id), label + "_COVERAGE_MISMATCH")
        return by_id
    gold_by_id = index(keys, "GOLD")
    score_by_id = index(scored, "SCORING")
    for cid, case in case_by_id.items():
        key, rubric = gold_by_id[cid], score_by_id[cid]
        require(key.get("domain") == case["domain"], "GOLD_DOMAIN_MISMATCH")
        require(type(key.get("acceptable_decisions")) is list and
                bool(key["acceptable_decisions"]) and
                type(key.get("must_abstain")) is bool and
                type(key.get("critical_failures")) is list and
                type(key.get("necessary_conditions")) is list,
                "GOLD_REQUIRED_FIELDS")
        require(type(rubric.get("task_items")) is list and
                len(rubric["task_items"]) == 10,
                "TEN_SCORING_ITEMS_REQUIRED")
        require(rubric.get("expected_skill") in {"USE", "SKIP", "EITHER"},
                "EXPECTED_SKILL_INVALID")
        route = rubric.get("routing_items")
        require(type(route) is list and
                sum(v["points"] for v in route if type(v) is dict and
                    type(v.get("points")) is int and v["points"] >= 0) == 10 and
                all(type(v) is dict and type(v.get("points")) is int and
                    v["points"] >= 0 and valid_text(v.get("rule"), 2000)
                    for v in route), "ROUTING_TEN_POINTS_REQUIRED")
    return packets, gold_by_id, score_by_id


def exclusive_json(path, obj):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())


def stage(*, cases_file, gold_file, scoring_file, cases_sha256, gold_sha256,
          scoring_sha256, repo_root, stage_root, facilitator_root,
          candidate_commit, skill_sha256):
    repo = Path(repo_root).resolve(strict=True)
    require(repo.is_dir(), "REPO_ROOT_INVALID")
    require(candidate_commit == FROZEN_CANDIDATE, "FROZEN_COMMIT_MISMATCH")
    require(bool(HEX64.fullmatch(skill_sha256 or "")), "SKILL_SHA256_REQUIRED")
    cases = read_pinned(cases_file, cases_sha256, repo)
    gold = read_pinned(gold_file, gold_sha256, repo)
    scoring = read_pinned(scoring_file, scoring_sha256, repo)
    packets, gold_by_id, score_by_id = validate(cases, gold, scoring)
    stage_dir = require_private_target(stage_root, repo)
    fac_dir = require_private_target(facilitator_root, repo)
    require(stage_dir.parent != fac_dir.parent and
            not stage_dir.is_relative_to(fac_dir) and
            not fac_dir.is_relative_to(stage_dir), "SEPARATE_PRIVATE_ROOTS_REQUIRED")
    order = list(packets)
    secrets.SystemRandom().shuffle(order)
    created_stage = created_fac = False
    try:
        stage_dir.mkdir(mode=0o700)
        created_stage = True
        fac_dir.mkdir(mode=0o700)
        created_fac = True
        os.chmod(stage_dir, 0o700)
        os.chmod(fac_dir, 0o700)
        stage_entries = []
        fac_entries = []
        for idx, cid in enumerate(order, 1):
            slot = f"H{idx:02d}"
            task = packets[cid]
            fd = os.open(stage_dir / (slot + ".txt"),
                         os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(task)
                f.flush()
                os.fsync(f.fileno())
            stage_entries.append({"slot": slot, "sha256": sha(task),
                                  "bytes": len(task)})
            fac_entries.append({"slot": slot, "original_id": cid,
                                "domain": next(c["domain"] for c in cases["cases"] if c["id"] == cid),
                                "task_sha256": sha(task),
                                "gold": gold_by_id[cid],
                                "scoring": score_by_id[cid]})
        exclusive_json(stage_dir / "stage_manifest.json", {
            "status": "OFFLINE_STAGED_REVIEW_HOLD", "schema_version": 1,
            "phase": "pilot", "source_class_claim": "synthetic",
            "candidate_commit": candidate_commit, "skill_sha256": skill_sha256,
            "case_count": 3, "cases": stage_entries,
            "model_calls": 0})
        # Full rich gold and scoring retained verbatim in JSON-object semantics.
        # No compressed/truncated gold surrogate, and no gold in stage.
        exclusive_json(fac_dir / "facilitator_only.json", {
            "status": "OFFLINE_STAGED_REVIEW_HOLD",
            "suite_id": cases["package_id"], "phase": "pilot",
            "candidate_commit": candidate_commit, "skill_sha256": skill_sha256,
            "source_sha256": {"cases": cases_sha256, "gold": gold_sha256,
                              "scoring": scoring_sha256},
            "general_rules": scoring["general_rules"],
            "method_record": scoring["method_record"],
            "rubric_status": scoring["status"],
            "case_mapping_and_gold": fac_entries,
            "primary_binary_endpoint": "NOT_PREREGISTERED_IN_RICH_RUBRIC",
            "routing_justification_observable": False,
            "independent_access_denial_verified": False,
            "actual_model_calls": 0})
        return {"status": "OFFLINE_STAGED_REVIEW_HOLD",
                "case_count": 3, "source_sha256_match": True,
                "scoring_contract": "PRIMARY_AND_ROUTING_NEED_REVIEW",
                "model_calls": 0, "independent_access_denial_verified": False}
    except Exception:
        if created_stage:
            shutil.rmtree(stage_dir)
        if created_fac:
            shutil.rmtree(fac_dir)
        raise


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("cases-file", "gold-file", "scoring-file", "repo-root",
                "stage-root", "facilitator-root", "candidate-commit",
                "skill-sha256"):
        p.add_argument("--" + arg, required=True)
    for arg in ("cases-sha256", "gold-sha256", "scoring-sha256"):
        p.add_argument("--" + arg, required=True)
    a = {k.replace("-", "_"): v for k, v in vars(p.parse_args(argv)).items()}
    try:
        print(json.dumps(stage(**a), ensure_ascii=False))
        return 0
    except (Hold, ValueError, TypeError, OSError, KeyError) as exc:
        code = str(exc) if isinstance(exc, Hold) else type(exc).__name__
        print(json.dumps({"status": "HOLD", "reason": code}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
