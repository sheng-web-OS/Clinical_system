#!/usr/bin/env python3
"""Run one original packet using the private patched runtime and frozen source."""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", required=True, type=pathlib.Path)
    parser.add_argument("--repo", required=True, type=pathlib.Path)
    parser.add_argument("--result-parent", required=True, type=pathlib.Path)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    with zipfile.ZipFile(args.packet) as archive:
        if (set(archive.namelist()) != {"task.txt", "job.json"} or
                len(archive.namelist()) != 2):
            raise SystemExit("PACKET_CONTENTS_INVALID")
        job = json.loads(archive.read("job.json"))
        task = archive.read("task.txt")
    if job["task_sha256"] != hashlib.sha256(task).hexdigest():
        raise SystemExit("TASK_SHA_MISMATCH")
    repo = args.repo.resolve(strict=True)
    runner = pathlib.Path("/runtime/run_xdt01_skill_selection.py")
    if not runner.is_file():
        raise SystemExit("RUNNER_NOT_FOUND")
    parent = args.result_parent.resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="xdt01-worker-", dir=parent) as td:
        taskpath = pathlib.Path(td) / "task.txt"
        taskpath.write_bytes(task)
        taskpath.chmod(0o600)
        cmd = [sys.executable, str(runner), "--frozen-repo", str(repo),
               "--arm", job["arm"], "--task-file", str(taskpath),
               "--task-sha256", job["task_sha256"],
               "--candidate-commit", job["candidate_commit"],
               "--output-dir", str(parent / ("result-" + job["job_id"]))]
        if job["arm"] == "C":
            cmd.extend(["--skill-file", str(repo / "experiments/cross-domain-transfer/decision-skill-v0.md"),
                        "--skill-sha256", job["skill_sha256"]])
        if args.live:
            if os.environ.get("XDT01_PRIVATE_APPROVAL") != "YES":
                raise SystemExit("PRIVATE_APPROVAL_NOT_CONFIRMED")
            cmd.extend(["--execute-api", "--budget-authorized",
                        "--attempt-dir", "/attempts"])
        result = subprocess.run(cmd, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
