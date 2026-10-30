#!/usr/bin/env python3
"""Issue exactly one pinned, neutral task from a private Stage1 archive.

Runs under the examiner identity, NOT the worker identity.  No gold, model
calls, cloud IAM configuration, or public GitHub upload.  This is a mechanical
one-case export, not proof that two runtime identities are isolated.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from zipfile import ZipFile, BadZipFile

from seal_private_case_exam import (
    DIGEST, MAX_CASES, MAX_TASK_BYTES, SealError, TRUSTED_CODE_ROOT,
    check, ensure_safe_output, reject_public_source,
)

SLOT = re.compile(r"H[0-9]{2}\\.md\\Z")
MAX_MANIFEST = 50000
MAX_ARCHIVE = 1000000


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def read_bound(path, max_bytes, expected_hash):
    check(bool(DIGEST.fullmatch(str(expected_hash))), "EXPECTED_SHA256_REQUIRED")
    check(path.is_file() and not path.is_symlink(), "EXAMINER_INPUT_INVALID")
    check(path.stat().st_size <= max_bytes, "EXAMINER_INPUT_OVERSIZED")
    raw = path.read_bytes()
    check(len(raw) <= max_bytes, "EXAMINER_INPUT_OVERSIZED")
    check(digest(raw) == expected_hash, "EXAMINER_INPUT_DIGEST_MISMATCH")
    return raw


def issue_one(stage_root, slot, output_root, *, expected_manifest_sha256,
              expected_archive_sha256, repo_root=TRUSTED_CODE_ROOT):
    stage = Path(stage_root).absolute()
    check(stage.is_dir() and not stage.is_symlink(), "STAGE1_INVALID")
    reject_public_source(stage / "manifest.json", repo_root)
    reject_public_source(stage / "stage1.zip", repo_root)
    check(bool(SLOT.fullmatch(str(slot) + ".md")), "SLOT_INVALID")
    raw_manifest = read_bound(stage / "manifest.json", MAX_MANIFEST,
                              expected_manifest_sha256)
    raw_archive = read_bound(stage / "stage1.zip", MAX_ARCHIVE,
                             expected_archive_sha256)
    try:
        manifest = json.loads(raw_manifest)
    except (UnicodeDecodeError, ValueError) as exc:
        raise SealError("STAGE1_MANIFEST_INVALID") from exc
    check(isinstance(manifest, dict) and set(manifest) ==
          {"version", "status", "actual_model_calls", "source_class", "files"},
          "STAGE1_SCHEMA_INVALID")
    check(manifest["version"] == 2 and manifest["status"] == "PREPARED_NOT_RUN"
          and manifest["actual_model_calls"] == 0 and
          manifest["source_class"] == "private_sealed_holdout_not_validated",
          "STAGE1_NOT_PRISTINE")
    files = manifest["files"]
    check(isinstance(files, list) and 3 <= len(files) <= MAX_CASES,
          "STAGE1_CASE_COUNT_INVALID")
    expected = {}
    for item in files:
        check(isinstance(item, dict) and set(item) == {"path", "bytes", "sha256"},
              "STAGE1_FILE_SCHEMA_INVALID")
        p = item["path"]
        name = p.removeprefix("stage1/") if isinstance(p, str) else ""
        check(p == "stage1/" + name and SLOT.fullmatch(name) is not None and
              name not in expected, "STAGE1_ENTRY_INVALID")
        size = item["bytes"]
        check(type(size) is int and 20 <= size <= MAX_TASK_BYTES and
              bool(DIGEST.fullmatch(str(item["sha256"]))),
              "STAGE1_ENTRY_HASH_INVALID")
        expected[name] = (size, item["sha256"])
    check(slot + ".md" in expected, "SLOT_NOT_FOUND")
    try:
        from io import BytesIO
        with ZipFile(BytesIO(raw_archive)) as z:
            infos = z.infolist()
            check(len(infos) == len(expected) and
                  set(i.filename for i in infos) == set(expected) and
                  len({i.filename for i in infos}) == len(infos),
                  "STAGE1_ZIP_ENTRY_MISMATCH")
            task = None
            for i in infos:
                check(not i.is_dir() and i.file_size == expected[i.filename][0]
                      and i.file_size <= MAX_TASK_BYTES,
                      "STAGE1_ZIP_SIZE_MISMATCH")
                raw = z.read(i)
                check(len(raw) == expected[i.filename][0] and
                      digest(raw) == expected[i.filename][1],
                      "STAGE1_ZIP_DIGEST_MISMATCH")
                if i.filename == slot + ".md":
                    task = raw
    except (BadZipFile, RuntimeError, EOFError) as exc:
        raise SealError("STAGE1_ZIP_INVALID") from exc
    out = ensure_safe_output(output_root, repo_root)
    canonical_stage = stage.resolve(strict=True)
    check(not out.is_relative_to(canonical_stage.parent) and
          not canonical_stage.is_relative_to(out), "WORKER_OUTPUT_OVERLAPS_EXAMINER")
    made = False
    try:
        out.mkdir(mode=0o700)
        made = True
        os.chmod(out, 0o700)
        task_file = out / "task.md"
        with task_file.open("xb") as fp:
            fp.write(task)
        os.chmod(task_file, 0o600)
    except Exception:
        if made:
            shutil.rmtree(out)
        raise
    return {
        "status": "ONE_CASE_EXPORTED_NOT_DELIVERED",
        "task_sha256": digest(task),
        "file_count": 1,
        "model_calls": 0,
        "worker_access_verified": False,
        "gold_exposure_verified": False,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stage-root", type=Path, required=True)
    ap.add_argument("--slot", required=True)
    ap.add_argument("--output-root", type=Path, required=True)
    ap.add_argument("--manifest-sha256", required=True)
    ap.add_argument("--archive-sha256", required=True)
    args = ap.parse_args()
    try:
        print(json.dumps(issue_one(
            args.stage_root, args.slot, args.output_root,
            expected_manifest_sha256=args.manifest_sha256,
            expected_archive_sha256=args.archive_sha256,
        ), sort_keys=True))
        return 0
    except (SealError, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "HOLD", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
