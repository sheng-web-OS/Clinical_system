#!/usr/bin/env python3
"""Export an EJE candidate-only input pack. No scoring labels or case metadata."""
import argparse
import json
import re
import subprocess
from pathlib import Path, PurePosixPath


def _git_at(repo, commit, path):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Snapshot must be a pinned 40-character Git commit SHA")
    p = PurePosixPath(path)
    if p.is_absolute() or not p.parts or any(part in ("..", ".") for part in p.parts):
        raise ValueError("Unsafe source path")
    if "labels.json" in p.parts or "cases.json" in p.parts:
        raise ValueError("Case metadata and gold labels may not be exported")
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        check=True, capture_output=True
    )
    return result.stdout


def export_case(cases, case_id, repo, out):
    matches = [c for c in cases["cases"] if c["id"] == case_id]
    if len(matches) != 1:
        raise ValueError("Unknown or duplicate case ID")
    case = matches[0]
    if case["status"] != "replayable":
        raise ValueError("Only frozen replayable cases may be exported")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", case_id):
        raise ValueError("Unsafe case identifier")
    destination = out / case_id
    if destination.exists():
        raise FileExistsError("Refuse to overwrite an existing sealed pack")
    snapshot = case["snapshot"]
    commit = snapshot["commit"]
    # Fetch and validate everything before creating output.
    files = [(p, _git_at(repo, commit, p)) for p in snapshot["paths"]]
    destination.mkdir(parents=True)
    (destination / "TASK.md").write_text(
        "# Independent editorial review\n\n"
        + case["task"] + "\n\n"
        + "Review the supplied snapshot only. Do not browse the case registry, "
          "gold labels, later feedback, or later Git versions. "
          "Report KEEP/local fix/bridge/restructure/HOLD as justified; "
          "do not edit the files in this first-pass round.\n",
        encoding="utf-8",
    )
    for path, raw in files:
        target = destination / "sources" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    # Intentionally omit case type, status, hidden labels and feedback.
    return destination


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case_id")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.cases.read_text(encoding="utf-8"))
    print(export_case(data, args.case_id, args.repo, args.out))


if __name__ == "__main__":
    main()
