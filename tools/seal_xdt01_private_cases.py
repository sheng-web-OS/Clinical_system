#!/usr/bin/env python3
"""Offline XDT-01 case handoff; never model-executes, grades, or attests IAM.

Only an external examiner with separately protected input and output roots may
use this tool. Every file it creates is PRIVATE and must stay outside GitHub.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
from collections import Counter
from pathlib import Path

SHA256 = re.compile(r"[0-9a-f]{64}\Z")
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SUITE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{3,64}\Z")
DOMAINS = {"inventory", "it-incident", "provenance"}
PHASE = {"pilot": 1, "exploratory": 4}
MAX_SOURCE_BYTES = 250000
MAX_TASK_BYTES = 12000


class Hold(ValueError):
    pass


def require(ok, code):
    if not ok:
        raise Hold(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_source(path, expected, repo):
    p = Path(path)
    require(bool(SHA256.fullmatch(str(expected))), "INPUT_DIGEST_REQUIRED")
    require(p.is_file() and not p.is_symlink(), "INVALID_PRIVATE_INPUT")
    real = p.resolve(strict=True)
    require(not real.is_relative_to(repo) and
            not p.absolute().is_relative_to(repo), "PUBLIC_GITHUB_INPUT_FORBIDDEN")
    require(real.stat().st_size <= MAX_SOURCE_BYTES, "SOURCE_SIZE_LIMIT")
    raw = p.read_bytes()
    require(len(raw) <= MAX_SOURCE_BYTES and digest(raw) == expected,
            "INPUT_NOT_PREPINNED_OR_MODIFIED")
    try:
        obj = json.loads(raw)
    except (UnicodeError, ValueError) as e:
        raise Hold("INVALID_JSON_INPUT") from e
    require(type(obj) is dict and obj.get("schema_version") == 1,
            "INVALID_SOURCE_SCHEMA")
    return obj


def safe_target(path, repo):
    p = Path(path).absolute()
    require(not p.exists() and not p.is_symlink(), "OUTPUT_MUST_BE_NEW")
    require(p != repo and not p.is_relative_to(repo) and
            not repo.is_relative_to(p), "PUBLIC_GITHUB_OUTPUT_FORBIDDEN")
    # Check every ancestor to reject transparent symlink diversion.
    for a in (p.parent, *p.parent.parents):
        require(not a.is_symlink(), "OUTPUT_SYMLINK_ANCESTOR")
    require(p.parent.is_dir() and not p.parent.resolve().is_relative_to(repo),
            "PRIVATE_OUTPUT_PARENT_REQUIRED")
    require(p.parent.stat().st_mode & 0o002 == 0,
            "WORLD_WRITABLE_PRIVATE_PARENT")
    return p


def validate(cases, gold, phase):
    require(set(cases) == {"schema_version", "source_class", "cases", "phase"},
            "CASES_SCHEMA_EXACT")
    require(set(gold) == {"schema_version", "keys"}, "GOLD_SCHEMA_EXACT")
    require(cases["phase"] == phase, "PHASE_MISMATCH")
    require(cases["source_class"] in {"synthetic", "public_rights_cleared"},
            "SOURCE_CLASS_NOT_ALLOWED")
    rows, keys = cases["cases"], gold["keys"]
    n = PHASE[phase]
    require(type(rows) is list and len(rows) == n * 3,
            "CASE_COUNT_WRONG")
    require(type(keys) is list and len(keys) == len(rows),
            "GOLD_COUNT_WRONG")
    ids, distribution = set(), Counter()
    for row in rows:
        require(type(row) is dict and set(row) == {"id", "domain", "task"},
                "NEUTRAL_CASE_SCHEMA_REQUIRED")
        ident, domain, task = row["id"], row["domain"], row["task"]
        require(type(ident) is str and bool(SUITE.fullmatch(ident))
                and ident not in ids, "CASE_ID_DUPLICATE_OR_INVALID")
        require(domain in DOMAINS, "CASE_DOMAIN_INVALID")
        require(type(task) is str and
                40 <= len(task.encode("utf-8")) <= MAX_TASK_BYTES,
                "CASE_TASK_BYTES_INVALID")
        ids.add(ident)
        distribution[domain] += 1
    require(all(distribution[d] == n for d in DOMAINS),
            "DOMAIN_DISTRIBUTION_INVALID")
    by_key, abstentions = {}, Counter()
    for key in keys:
        require(type(key) is dict and
                set(key) == {"id", "acceptable_decisions", "must_abstain",
                             "rationale", "critical_failures"},
                "GOLD_KEY_SCHEMA_INVALID")
        ident = key["id"]
        require(type(ident) is str and ident not in by_key,
                "DUPLICATE_GOLD_ID")
        require(type(key["acceptable_decisions"]) is list and
                1 <= len(key["acceptable_decisions"]) <= 5 and
                all(type(v) is str and 1 <= len(v) <= 100
                    for v in key["acceptable_decisions"]),
                "GOLD_DECISIONS_INVALID")
        require(type(key["must_abstain"]) is bool and
                type(key["rationale"]) is str and
                len(key["rationale"].strip()) >= 30,
                "GOLD_RATIONALE_INVALID")
        require(type(key["critical_failures"]) is list and
                all(type(v) is str and 3 <= len(v) <= 250
                    for v in key["critical_failures"]),
                "GOLD_CRITICAL_FAILURES_INVALID")
        by_key[ident] = key
    require(set(by_key) == ids, "GOLD_COVERAGE_MISMATCH")
    for row in rows:
        abstentions[row["domain"]] += int(by_key[row["id"]]["must_abstain"])
    if phase == "exploratory":
        require(all(abstentions[d] >= 1 for d in DOMAINS),
                "REQUIRE_UNRESOLVABLE_CASE_PER_DOMAIN")
    return rows, by_key


def seal(*, cases_file, gold_file, cases_sha256, gold_sha256, stage_root,
         facilitator_root, suite_id, phase, candidate_commit, skill_sha256,
         repo_root):
    repo = Path(repo_root).resolve(strict=True)
    require(bool(SUITE.fullmatch(suite_id or "")), "SUITE_ID_INVALID")
    require(phase in PHASE, "PHASE_INVALID")
    require(bool(SHA40.fullmatch(candidate_commit or "")), "EXACT_COMMIT_REQUIRED")
    require(bool(SHA256.fullmatch(skill_sha256 or "")), "SKILL_DIGEST_REQUIRED")
    cases = read_source(cases_file, cases_sha256, repo)
    gold = read_source(gold_file, gold_sha256, repo)
    rows, keymap = validate(cases, gold, phase)
    stage = safe_target(stage_root, repo)
    keys = safe_target(facilitator_root, repo)
    require(stage.parent != keys.parent and stage != keys and
            not stage.is_relative_to(keys) and not keys.is_relative_to(stage),
            "REQUIRE_DISTINCT_PRIVATE_ROOTS")
    order = list(rows)
    secrets.SystemRandom().shuffle(order)
    stage_created = key_created = False
    try:
        stage.mkdir(mode=0o700)
        stage_created = True
        keys.mkdir(mode=0o700)
        key_created = True
        os.chmod(stage, 0o700)
        os.chmod(keys, 0o700)
        case_entries, facilitator_entries = [], []
        for i, row in enumerate(order, 1):
            slot = f"H{i:02d}"
            payload = row["task"].encode("utf-8")
            out = stage / (slot + ".txt")
            # Explicit exclusive creation; all cases remain examiner-only.
            fd = os.open(out, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as h:
                h.write(payload)
            case_entries.append({"slot": slot, "bytes": len(payload),
                                 "sha256": digest(payload)})
            facilitator_entries.append({
                "slot": slot, "original_id": row["id"],
                "domain": row["domain"], "task_sha256": digest(payload),
                "gold": keymap[row["id"]]})
        stage_meta = {
            "status": "STAGED_NOT_DISTRIBUTED", "schema_version": 1,
            "phase": phase, "source_class_claim": cases["source_class"],
            "cases": case_entries, "model_calls": 0,
            "candidate_commit": candidate_commit,
            "skill_sha256": skill_sha256,
        }
        public_info = {
            "status": "STAGED_NOT_DISTRIBUTED", "case_count": len(rows),
            "phase": phase, "model_calls": 0,
            "runtime_iam_verified": False,
            "blinded_review_verified": False, "transfer_validated": False,
        }
        fac = {
            "suite_id": suite_id, "phase": phase,
            "cases_source_sha256": cases_sha256,
            "gold_source_sha256": gold_sha256,
            "case_mapping_and_gold": facilitator_entries,
            "runtime_iam_verified": False,
            "blinded_review_verified": False,
            "actual_model_calls": 0, "transfer_validated": False,
        }
        for dst, obj in ((stage / "stage_manifest.json", stage_meta),
                         (keys / "facilitator_only.json", fac)):
            fd = os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as h:
                json.dump(obj, h, ensure_ascii=False, sort_keys=True, indent=2)
        return public_info
    except Exception:
        if stage_created:
            shutil.rmtree(stage)
        if key_created:
            shutil.rmtree(keys)
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("cases-file", "gold-file", "stage-root", "facilitator-root", "repo-root"):
        p.add_argument("--" + arg, type=Path, required=True)
    for arg in ("cases-sha256", "gold-sha256", "suite-id", "phase",
                "candidate-commit", "skill-sha256"):
        p.add_argument("--" + arg, required=True)
    a = vars(p.parse_args())
    a["repo_root"] = a.pop("repo_root")
    try:
        print(json.dumps(seal(**{k.replace("-", "_"): v for k, v in a.items()})))
        return 0
    except (Hold, OSError, TypeError, KeyError, ValueError) as ex:
        # Never print private case contents or paths, even on unexpected bad data.
        code = str(ex) if isinstance(ex, Hold) else type(ex).__name__
        print(json.dumps({"status": "HOLD", "reason": code}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
