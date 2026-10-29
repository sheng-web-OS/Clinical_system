#!/usr/bin/env python3
"""Export already blinded MedEinst worker packets to PR #225 Stage1 ZIP contract.

Reads ONLY anonymous packet.json files, never a gold key or diagnosis labels.
Zero model calls and no external access. The ZIP is a facilitator input, NOT
one worker's task bundle. Each case must be isolated at the downstream stage.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED

from prepare_medeinst_holdout import HoldoutError, require

ALLOWED_SOURCE_CLASS = (
    "MedEinst_DDXPlus_simulated_research_case",
    "synthetic_fixture_not_medeinst",
)
SHA = re.compile(r"[0-9a-f]{64}\Z")
SLOT = re.compile(r"s_[0-9a-f]{24}\Z")
MAX_CASES = 12
MAX_TASK_BYTES = 48000
CASE_PREFIX = "M"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_packet(path):
    require(path.is_file() and not path.is_symlink(), "INVALID_PACKET_PATH")
    raw = path.read_bytes()
    require(30 <= len(raw) <= MAX_TASK_BYTES, "PACKET_OUT_OF_BOUNDS")
    try:
        obj = json.loads(raw)
    except (UnicodeError, ValueError):
        raise HoldoutError("INVALID_PACKET_JSON") from None
    require(type(obj) is dict and set(obj) == {
        "schema_version", "source_class", "instruction", "case_text"
    }, "PACKET_UNEXPECTED_FIELDS")
    require(obj["schema_version"] == 1
            and obj["source_class"] in ALLOWED_SOURCE_CLASS
            and type(obj["case_text"]) is str
            and 30 <= len(obj["case_text"]) <= 12000
            and type(obj["instruction"]) is str
            and 10 <= len(obj["instruction"]) <= 5000,
            "PACKET_INVALID_CONTENT")
    # Do not pass the source class, benchmark identity, diagnosis, or labels
    # as medical fact. The case is not guaranteed to be expert validated.
    task = (
        "SIMULATED MEDICAL RESEARCH CASE — NOT PATIENT CARE.\n"
        "Use ONLY the clinical description below for a first-pass analysis.\n"
        "Separate observations, differential mechanisms, discriminating evidence,\n"
        "missing patient facts and literature research needs; do not invent motives.\n\n"
        + obj["case_text"] + "\n"
    ).encode("utf-8")
    require(30 <= len(task) <= MAX_TASK_BYTES, "TASK_EXCEEDS_STAGE1_LIMIT")
    return task, sha(raw), obj["source_class"]


def export_stage1(worker_root, output_dir, *, expected_source_class, repo_root=None):
    root = Path(worker_root).expanduser().absolute()
    repo = Path(repo_root or Path(__file__).resolve().parents[1]).resolve()
    require(expected_source_class in ALLOWED_SOURCE_CLASS, "UNRECOGNIZED_SOURCE_CLASS")
    require(root.is_dir() and not root.is_symlink(), "WORKER_ROOT_REQUIRED")
    require(not root.is_relative_to(repo), "WORKER_INPUT_MUST_BE_OUTSIDE_PUBLIC_REPO")
    require(not any(part.is_symlink() for part in (root.parent, *root.parent.parents)),
            "WORKER_ROOT_SYMLINK_ANCESTOR")
    output = Path(output_dir).expanduser().absolute()
    require(not output.exists() and output.parent.is_dir()
            and not output.parent.is_symlink(), "NEW_OUTPUT_ROOT_REQUIRED")
    require(not output.is_relative_to(repo)
            and not output.is_relative_to(root)
            and not root.is_relative_to(output)
            and output != root, "OUTPUT_MUST_BE_SEPARATE")
    require(not any(p.is_symlink() for p in (output.parent, *output.parent.parents)),
            "OUTPUT_SYMLINK_ANCESTOR")

    children = sorted(root.iterdir())
    require(1 <= len(children) <= MAX_CASES, "INVALID_PACKET_COUNT")
    tasks = []
    for child in children:
        require(child.is_dir() and not child.is_symlink()
                and SLOT.fullmatch(child.name)
                and set(p.name for p in child.iterdir()) == {"packet.json"},
                "UNSAFE_OR_UNEXPECTED_WORKER_SLOT")
        task, raw_digest, source_class = read_packet(child / "packet.json")
        require(source_class == expected_source_class, "SOURCE_CLASS_MISMATCH")
        tasks.append((child.name, task, raw_digest))

    # Prepare all contents before making an output directory.
    files = []
    for i, (slot, task, packet_sha) in enumerate(tasks, 1):
        cid = f"{CASE_PREFIX}{i:02d}"
        files.append({
            "case_id": cid, "slot": slot, "packet_sha256": packet_sha,
            "task_filename": cid + ".md", "task_sha256": sha(task),
            "task_bytes": len(task), "task": task,
        })
    output.mkdir(mode=0o700)
    os.chmod(output, 0o700)
    with ZipFile(output / "stage1.zip", "x", compression=ZIP_DEFLATED) as zipout:
        for item in files:
            zipout.writestr(item["task_filename"], item["task"])
    os.chmod(output / "stage1.zip", 0o600)
    manifest = {
        "version": 2, "status": "PREPARED_NOT_RUN",
        "actual_model_calls": 0,
        "files": [{"path": "stage1/" + item["task_filename"],
                   "bytes": item["task_bytes"], "sha256": item["task_sha256"]}
                  for item in files],
    }
    mapping = {
        "source_class": expected_source_class,
        "private_crosswalk_only": True,
        "medical_gold_loaded": False,
        "cases": [{"case_id": x["case_id"], "worker_slot": x["slot"],
                   "packet_sha256": x["packet_sha256"]}
                  for x in files],
    }
    for name, value in (("manifest.json", manifest), ("private_crosswalk.json", mapping)):
        raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
        fd = os.open(output / name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as dst:
            dst.write(raw)
    return {
        "status": "STAGE1_ONLY_NO_MODEL_RUN",
        "packets": len(files),
        "stage1_zip_sha256": sha((output / "stage1.zip").read_bytes()),
        "manifest_sha256": sha((output / "manifest.json").read_bytes()),
        "actual_model_calls": 0,
        "independent_medical_review": "NOT_DONE",
        "clinical_transfer_validated": False,
        "worker_isolation_verified": False,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--worker-root", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--expected-source-class", choices=ALLOWED_SOURCE_CLASS,
                   required=True)
    a = p.parse_args()
    print(json.dumps(export_stage1(a.worker_root, a.output_dir,
                                  expected_source_class=a.expected_source_class),
                     sort_keys=True))


if __name__ == "__main__":
    main()
