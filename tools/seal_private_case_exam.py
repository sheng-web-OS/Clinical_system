#!/usr/bin/env python3
"""Create an offline, examiner-only sealed case handoff to #225 Stage1.

No network, model calls, external reviewers, security attestation, or medical grading.
Only run in a trusted private environment with ACL-isolated examiner storage.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

DIGEST = re.compile(r"[0-9a-f]{64}\Z")
SUITE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{3,80}\Z")
ROLES = {"transfer", "normal", "boundary"}
MAX_CASES = 12
MAX_TASK_BYTES = 12000


class SealError(ValueError):
    pass


def check(condition, reason):
    if not condition:
        raise SealError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_pinned_json(path, digest):
    check(bool(DIGEST.fullmatch(str(digest))), "PINNED_SHA256_REQUIRED")
    path = Path(path)
    check(path.is_file() and not path.is_symlink(), "PRIVATE_SOURCE_INVALID")
    raw = path.read_bytes()
    check(sha(raw) == digest, "FROZEN_SOURCE_MISMATCH")
    check(len(raw) <= 250000, "PRIVATE_SOURCE_OVERSIZED")
    try:
        obj = json.loads(raw)
    except (UnicodeDecodeError, ValueError) as exc:
        raise SealError("PRIVATE_SOURCE_JSON_INVALID") from exc
    check(isinstance(obj, dict) and obj.get("schema_version") == 1,
          "SOURCE_SCHEMA_INVALID")
    return obj


def ensure_safe_output(path, repo_root):
    path = Path(path).absolute()
    repo = Path(repo_root).resolve(strict=True)
    check(path != repo and not path.is_relative_to(repo) and
          not repo.is_relative_to(path), "PUBLIC_REPO_PATH_FORBIDDEN")
    check(not path.exists() and not path.is_symlink(), "OUTPUT_ALREADY_EXISTS")
    for item in (path.parent, *path.parent.parents):
        check(not item.is_symlink(), "SYMLINK_ANCESTOR_FORBIDDEN")
    check(path.parent.is_dir(), "PRIVATE_PARENT_REQUIRED")
    check(not path.parent.resolve().is_relative_to(repo), "PUBLIC_REPO_PARENT_FORBIDDEN")
    check((path.parent.stat().st_mode & 0o002) == 0,
          "WORLD_WRITABLE_PARENT_FORBIDDEN")
    return path


def validate(cases, gold, suite_id):
    check(SUITE_ID.fullmatch(suite_id or "") is not None, "INVALID_SUITE_ID")
    check(cases.get("source_class") in {"synthetic", "authorized_deidentified"},
          "SOURCE_CLASS_REQUIRED")
    records = cases.get("cases")
    answers = gold.get("keys")
    check(isinstance(records, list) and 3 <= len(records) <= MAX_CASES,
          "INVALID_CASE_COUNT")
    check(isinstance(answers, list), "ANSWER_KEY_REQUIRED")
    by_id = {}
    for row in records:
        check(isinstance(row, dict), "CASE_INVALID")
        ident, role, task = row.get("id"), row.get("role"), row.get("task")
        check(isinstance(ident, str) and SUITE_ID.fullmatch(ident) is not None
              and ident not in by_id, "CASE_ID_INVALID_OR_DUPLICATE")
        check(role in ROLES, "ROLE_INVALID")
        check(isinstance(task, str) and 20 <= len(task.encode("utf-8")) <= MAX_TASK_BYTES,
              "TASK_MISSING_OR_TOO_LARGE")
        check(set(row) == {"id", "role", "task"},
              "ONLY_NEUTRAL_CASE_FIELDS_ALLOWED")
        by_id[ident] = row
    check({r["role"] for r in records} == ROLES,
          "TRANSFER_NORMAL_BOUNDARY_CONTROLS_REQUIRED")
    keymap = {}
    for a in answers:
        check(isinstance(a, dict) and set(a) == {"id", "expected_decision", "clinical_rationale"},
              "KEY_SCHEMA_INVALID")
        ident = a["id"]
        check(isinstance(ident, str) and ident not in keymap, "DUPLICATE_KEY")
        check(isinstance(a["expected_decision"], str) and a["expected_decision"].strip()
              and isinstance(a["clinical_rationale"], str) and a["clinical_rationale"].strip(),
              "KEY_CONTENT_MISSING")
        keymap[ident] = a
    check(set(keymap) == set(by_id), "ANSWER_KEY_COVERAGE_MISMATCH")
    return records, keymap


def seal(cases_file, gold_file, stage1_root, key_root, *,
         expected_cases_sha256, expected_gold_sha256, suite_id, repo_root):
    """Produce separate examiner-only Stage1 and facilitator-only gold directories.

    These are NOT worker contexts. A trusted operator must hand individual
    packets to isolated runners and separately enforce their access controls.
    """
    repo = Path(repo_root).resolve(strict=True)
    for source in (cases_file, gold_file):
        check(not Path(source).absolute().is_relative_to(repo), "PUBLIC_REPO_INPUT_FORBIDDEN")
    cases = read_pinned_json(cases_file, expected_cases_sha256)
    gold = read_pinned_json(gold_file, expected_gold_sha256)
    records, keymap = validate(cases, gold, suite_id)
    stage = ensure_safe_output(stage1_root, repo_root)
    keys = ensure_safe_output(key_root, repo_root)
    check(stage != keys and not stage.is_relative_to(keys) and
          not keys.is_relative_to(stage) and stage.parent != keys.parent,
          "EXAMINER_AND_GOLD_ROOTS_MUST_BE_SEPARATED")
    indices = list(range(len(records)))
    secrets.SystemRandom().shuffle(indices)
    selection = [(f"H{i + 1:02d}", records[k]) for i, k in enumerate(indices)]
    contents = [(slot + ".md", row["task"].encode("utf-8")) for slot, row in selection]
    stage_created = keys_created = False
    try:
        stage.mkdir(mode=0o700)
        stage_created = True
        os.chmod(stage, 0o700)
        keys.mkdir(mode=0o700)
        keys_created = True
        os.chmod(keys, 0o700)
        archive = stage / "stage1.zip"
        with ZipFile(archive, "x", compression=ZIP_DEFLATED) as z:
            for name, data in contents:
                z.writestr(name, data)
        os.chmod(archive, 0o600)
        manifest = {
            "version": 2, "status": "PREPARED_NOT_RUN", "actual_model_calls": 0,
            "source_class": "private_sealed_holdout_not_validated",
            "files": [
                {"path": "stage1/" + name, "bytes": len(data), "sha256": sha(data)}
                for name, data in contents
            ],
        }
        manifest_file = stage / "manifest.json"
        manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
        os.chmod(manifest_file, 0o600)
        facilitator = {
            "schema_version": 1, "suite_id": suite_id,
            "source_class_claim_not_privacy_verified": cases["source_class"],
            "stage1_archive_sha256": sha(archive.read_bytes()),
            "stage1_manifest_sha256": sha(manifest_file.read_bytes()),
            "cases_source_sha256": expected_cases_sha256,
            "gold_source_sha256": expected_gold_sha256,
            "slots": [
                {"slot": slot, "original_id": row["id"], "role": row["role"],
                 "task_sha256": sha(row["task"].encode("utf-8")),
                 "gold": keymap[row["id"]]}
                for slot, row in selection
            ],
            "provider_model_calls": 0,
            "worker_context_isolation": "NOT_VERIFIED",
            "clinical_gold_validated": False,
            "independent_reviewer_authenticated": False,
            "clinical_transfer_validated": False,
        }
        key_file = keys / "facilitator_key.json"
        key_file.write_text(json.dumps(facilitator, ensure_ascii=False, indent=2), encoding="utf-8")
        os.chmod(key_file, 0o600)
    except Exception:
        if stage_created:
            shutil.rmtree(stage)
        if keys_created:
            shutil.rmtree(keys)
        raise
    return {"status": "PREPARED_NOT_RUN", "case_count": len(records),
            "source_class": cases["source_class"], "model_calls": 0,
            "stage1_manifest_sha256": facilitator["stage1_manifest_sha256"],
            "worker_isolation_verified": False, "clinical_validated": False,
            "warning": "Keep examiner Stage1 and facilitator gold entirely separate from workers; source-class attestation is not PHI clearance."}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases-file", type=Path, required=True)
    ap.add_argument("--gold-file", type=Path, required=True)
    ap.add_argument("--stage1-root", type=Path, required=True)
    ap.add_argument("--key-root", type=Path, required=True)
    ap.add_argument("--cases-sha256", required=True)
    ap.add_argument("--gold-sha256", required=True)
    ap.add_argument("--suite-id", required=True)
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    a = ap.parse_args()
    try:
        print(json.dumps(seal(a.cases_file, a.gold_file, a.stage1_root, a.key_root,
                              expected_cases_sha256=a.cases_sha256,
                              expected_gold_sha256=a.gold_sha256,
                              suite_id=a.suite_id, repo_root=a.repo_root),
                         ensure_ascii=False))
        return 0
    except (SealError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
