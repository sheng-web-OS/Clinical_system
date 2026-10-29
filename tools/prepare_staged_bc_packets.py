#!/usr/bin/env python3
"""Prepare frozen B/C worker *inputs*, not inference or isolated runtimes.

No Stage2, reviewer-only, original outcomes or external network transport.
Only C receives the experimental Skill. Everything written outside public Git.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

HEX64 = re.compile(r"[a-f0-9]{64}\Z")
HEX40 = re.compile(r"[a-f0-9]{40}\Z")
SAFE_ID = re.compile(r"[A-Z][0-9]{2}\Z")
MAX_TASK_BYTES = 50000
MAX_SKILL_BYTES = 30000
COMMON = ("This is an educational, published or fictional development case, not patient-specific advice.\n"
          "Explain the causal possibilities, discriminating evidence, uncertainty, and any justified source request.\n"
          "Do not manufacture clinician motives or facts; never infer causation from a single observation.\n"
          "Finish your FIRST complete answer with exactly one final line:\n"
          "DECISION: RETRIEVE, DECISION: SKIP, or DECISION: HOLD\n"
          "Do not see or use any later-stage original source, reviewer rubric, prior arm output, or answer key.\n"
          "Respond in Traditional Chinese.\n")


class PacketError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise PacketError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_manifest(path, expected_digest):
    require(HEX64.fullmatch(expected_digest or "") is not None, "PIN_MANIFEST_SHA256_REQUIRED")
    require(path.is_file() and not path.is_symlink(), "MANIFEST_INVALID")
    raw = path.read_bytes()
    require(sha(raw) == expected_digest, "MANIFEST_HASH_MISMATCH")
    obj = json.loads(raw)
    require(obj.get("status") == "PREPARED_NOT_RUN" and obj.get("version") == 2
            and obj.get("actual_model_calls") == 0, "UNEXPECTED_PACKET_STATUS")
    files = obj.get("files")
    require(isinstance(files, list) and files, "MANIFEST_FILES_MISSING")
    expected = {}
    for entry in files:
        key = entry.get("path")
        require(isinstance(key, str) and key not in expected
                and type(entry.get("bytes")) is int and entry["bytes"] >= 0
                and HEX64.fullmatch(str(entry.get("sha256", ""))),
                "MANIFEST_FILE_INVALID")
        expected[key] = entry
    return obj, expected


def verify_stage1_archive(path, expected):
    require(path.is_file() and not path.is_symlink(), "STAGE1_ARCHIVE_MISSING")
    needed = {name.removeprefix("stage1/"): meta for name, meta in expected.items()
              if name.startswith("stage1/")}
    require(needed, "STAGE1_FILES_NOT_LISTED")
    seen = {}
    with ZipFile(path, "r") as z:
        all_infos = z.infolist()
        require(len(all_infos) == len(needed), "STAGE1_ARCHIVE_MEMBERS_MISMATCH")
        for info in all_infos:
            name = info.filename
            require(name in needed and name not in seen
                    and not info.is_dir() and not info.flag_bits & 0x1
                    and 10 <= info.file_size <= MAX_TASK_BYTES
                    and (info.external_attr >> 16) & 0o170000 != 0o120000,
                    "STAGE1_ARCHIVE_ENTRY_REJECTED")
            raw = z.read(info)
            require(len(raw) == info.file_size == needed[name]["bytes"]
                    and sha(raw) == needed[name]["sha256"], "STAGE1_ENTRY_HASH_MISMATCH")
            seen[name] = raw
    require(set(seen) == set(needed), "STAGE1_ARCHIVE_MEMBERS_MISMATCH")
    return seen


def prepare(stage1_zip, manifest_path, skill_path, output_dir, *,
            expected_manifest_sha256, expected_skill_sha256,
            candidate_commit, cases=("H01", "S01"), repo_root=None):
    require(HEX40.fullmatch(candidate_commit or "") is not None,
            "EXACT_CANDIDATE_COMMIT_CLAIM_REQUIRED")
    require(HEX64.fullmatch(expected_skill_sha256 or "") is not None,
            "PIN_SKILL_SHA256_REQUIRED")
    require(1 <= len(cases) <= 5 and len(set(cases)) == len(cases)
            and all(SAFE_ID.fullmatch(cid or "") for cid in cases),
            "INVALID_CASE_SELECTION")
    _, manifest_entries = read_manifest(Path(manifest_path), expected_manifest_sha256)
    tasks = verify_stage1_archive(Path(stage1_zip), manifest_entries)
    require(Path(skill_path).is_file() and not Path(skill_path).is_symlink(),
            "SKILL_FILE_INVALID")
    skill_bytes = Path(skill_path).read_bytes()
    require(10 <= len(skill_bytes) <= MAX_SKILL_BYTES
            and sha(skill_bytes) == expected_skill_sha256
            and b"name: decision-question-triage" in skill_bytes,
            "SKILL_BYTES_NOT_PINNED")
    output = Path(output_dir).resolve()
    if repo_root is None:
        repo_root = Path(__file__).resolve().parents[1]
    require(not output.is_relative_to(Path(repo_root).resolve()),
            "PRIVATE_PACKETS_MUST_STAY_OUTSIDE_PUBLIC_REPO")
    require(not output.exists(), "OUTPUT_EXISTS_REFUSE_OVERWRITE")
    for cid in cases:
        require(cid + ".md" in tasks, "CASE_NOT_FROZEN")
    # No output exists until all inputs and exact file hashes pass.
    output.mkdir(mode=0o700, parents=False)
    os.chmod(output, 0o700)
    pairing = []
    instruction_bytes = COMMON.encode("utf-8")
    for cid in cases:
        for arm in ("B", "C"):
            name = f"{cid}_{arm}_stage1.zip"
            dest = output / name
            # Transfer each ZIP individually into a separate worker context;
            # mounting this shared directory would contaminate the B arm.
            with ZipFile(dest, "x", compression=ZIP_DEFLATED) as z:
                z.writestr("task.md", tasks[cid + ".md"])
                z.writestr("instructions.txt", instruction_bytes)
                if arm == "C":
                    z.writestr("candidate_skill.md", skill_bytes)
            os.chmod(dest, 0o600)
            pairing.append({"case_id": cid, "arm": arm, "worker_zip": name,
                            "worker_zip_sha256": sha(dest.read_bytes()),
                            "task_sha256": sha(tasks[cid + ".md"]),
                            "skill_exposure": "EXPLICIT_BYTES" if arm == "C" else "NONE_DECLARED",
                            "worker_execution": "NOT_RUN"})
    receipt = {
        "status": "PACKETS_PREPARED_NO_MODEL_RUN", "source_class": "development_only",
        "candidate_commit_claimed_not_git_verified": candidate_commit,
        "manifest_sha256": expected_manifest_sha256,
        "skill_sha256": expected_skill_sha256,
        "case_ids": list(cases), "worker_context_isolation": "NOT_VERIFIED",
        "provider_model_calls": 0, "actual_cost_usd": None,
        "independent_review": "NOT_DONE", "clinical_transfer_validated": False,
        "stage2_or_review_keys_in_worker_packets": False, "workers": pairing,
    }
    data = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    (output / "facilitator_manifest.json").write_bytes(data)
    os.chmod(output / "facilitator_manifest.json", 0o600)
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--stage1-zip", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--skill", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--manifest-sha256", required=True)
    p.add_argument("--skill-sha256", required=True)
    p.add_argument("--candidate-commit", required=True)
    p.add_argument("--cases", nargs="+", default=["H01", "S01"])
    a = p.parse_args()
    try:
        result = prepare(a.stage1_zip, a.manifest, a.skill, a.output_dir,
                         expected_manifest_sha256=a.manifest_sha256,
                         expected_skill_sha256=a.skill_sha256,
                         candidate_commit=a.candidate_commit, cases=a.cases)
    except (PacketError, OSError, ValueError, KeyError, TypeError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, PacketError) else "PACKET_PREFLIGHT_INVALID"
        print(json.dumps({"status": "HOLD", "reason": reason}))
        return 2
    print(json.dumps({"status": result["status"], "worker_packages": len(result["workers"]),
                      "provider_model_calls": 0, "clinical_transfer_validated": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
