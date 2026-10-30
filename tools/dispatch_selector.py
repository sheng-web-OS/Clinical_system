#!/usr/bin/env python3
"""Read-only GitHub issue dispatcher SHADOW plan. Never executes tasks or models."""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "sheng-web-OS/Clinical_system"
ALLOWED_KINDS = {"quality_review", "continue_editorial"}
TASK_KEYS = {"id", "target", "priority", "enabled", "kind", "trigger"}


class DispatchError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise DispatchError(message)


def load_manifest(path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    require(type(config) is dict and set(config) == {
        "schema_version", "repo", "mode", "max_tasks_per_run",
        "frozen_eval", "tasks"}, "INVALID_MANIFEST_SCHEMA")
    require(type(config["schema_version"]) is int and
            config["schema_version"] == 1 and config["repo"] == REPO,
            "INVALID_REPOSITORY_OR_VERSION")
    require(type(config["mode"]) is str and
            config["mode"] in {"shadow", "active"} and
            type(config["max_tasks_per_run"]) is int and
            config["max_tasks_per_run"] == 1,
            "UNAPPROVED_MODE_OR_TASK_BATCH")
    freeze = config["frozen_eval"]
    require(type(freeze) is dict and set(freeze) == {
        "issue", "until_utc", "excluded_targets"}, "INVALID_EVAL_LOCK")
    require(freeze["issue"] == 137 and
            freeze["until_utc"] == "2026-11-01T06:20:15Z",
            "PREREGISTERED_WINDOW_MUST_NOT_CHANGE")
    excluded = freeze["excluded_targets"]
    require(type(excluded) is list and
            all(type(x) is str for x in excluded) and
            len(excluded) == len(set(excluded))
            and {"issue:137", "issue:159", "pr:224", "pr:225",
                 "pr:234", "pr:235"}.issubset(set(excluded)),
            "PROTECTED_EXPERIMENT_SCOPE")
    tasks = config["tasks"]
    require(type(tasks) is list and 0 < len(tasks) <= 30,
            "TASK_COUNT_OUT_OF_SCOPE")
    seen_ids = set()
    seen_targets = set()
    for task in tasks:
        require(type(task) is dict and set(task) == TASK_KEYS,
                "INVALID_TASK_SCHEMA")
        task_id, target = task["id"], task["target"]
        require(type(task_id) is str and
                re.fullmatch(r"[a-z][a-z0-9-]{2,60}", task_id)
                and task_id not in seen_ids, "INVALID_OR_DUPLICATE_TASK_ID")
        require(type(target) is str and
                re.fullmatch(r"issue:[1-9][0-9]*", target)
                and target not in seen_targets and target not in excluded,
                "DISALLOWED_OR_DUPLICATE_TARGET")
        require(type(task["enabled"]) is bool and
                type(task["priority"]) is int and 1 <= task["priority"] <= 100
                and type(task["kind"]) is str and task["kind"] in ALLOWED_KINDS
                and task["trigger"] == "issue_open",
                "INVALID_TASK_POLICY")
        seen_ids.add(task_id)
        seen_targets.add(target)
    return config


def select_tasks(config, snapshot):
    """Snapshot is trusted *metadata* only, never task instructions or case text."""
    require(type(snapshot) is dict, "INVALID_ISSUE_SNAPSHOT")
    eligible, skipped = [], []
    for task in config["tasks"]:
        target = task["target"]
        if not task["enabled"]:
            skipped.append({"id": task["id"], "reason": "DISABLED"})
            continue
        item = snapshot.get(target)
        require(type(item) is dict and
                set(item) == {"number", "state", "is_pr"} and
                type(item["number"]) is int and
                item["number"] == int(target.split(":")[1]) and
                type(item["is_pr"]) is bool and
                type(item["state"]) is str and
                item["state"] in {"open", "closed"},
                "SOURCE_METADATA_MISSING_OR_INVALID")
        if item["is_pr"]:
            raise DispatchError("EXPECTED_ISSUE_GOT_PR")
        if item["state"] != "open":
            skipped.append({"id": task["id"], "reason": "CLOSED"})
            continue
        eligible.append({"id": task["id"], "target": target,
                         "kind": task["kind"], "priority": task["priority"]})
    eligible.sort(key=lambda t: (-t["priority"], t["id"]))
    # The top issue may have an active writer or a pending reviewer even while
    # open. Return the ordered queue so the ChatGPT worker can check every
    # candidate's live PR/owner/last gate and skip it without starving others.
    # Issue-open status alone is NEVER an execution authorization.
    return {"status": ("SHADOW_NO_ACTION" if config["mode"] == "shadow"
                       else "ACTIVE_PLAN_ONLY"),
            "model_calls": 0, "write_actions": 0,
            "execution_authorized": False,
            "selected": eligible[:1],
            "candidates": eligible,
            "selection_requires_live_gate_check": True,
            "other_eligible_count": max(0, len(eligible) - 1),
            "skipped": skipped}


def fetch_open_issue_snapshot(config):
    """Public GitHub metadata-only reads; no credentials printed or mutations."""
    result = {}
    for task in config["tasks"]:
        if not task["enabled"]:
            continue
        target = task["target"]
        number = int(target.split(":")[1])
        url = "https://api.github.com/repos/" + REPO + "/issues/" + str(number)
        headers = {"Accept": "application/vnd.github+json",
                   "User-Agent": "clinical-os-shadow-dispatch/1"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = "Bearer " + token
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=15) as resp:
                raw = resp.read(50000)
            item = json.loads(raw)
        except (OSError, ValueError, urllib.error.HTTPError) as exc:
            raise DispatchError("GITHUB_READ_FAILED") from None
        require(type(item) is dict and
                item.get("number") == number
                and type(item.get("state")) is str and
                item.get("state") in {"open", "closed"},
                "GITHUB_METADATA_UNVERIFIED")
        result[target] = {"number": number, "state": item["state"],
                          "is_pr": "pull_request" in item}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path,
                        default=Path("ops/dispatch.json"))
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument("--live", action="store_true",
                         help="Read public GitHub issue metadata, without writes")
    sources.add_argument("--snapshot", type=Path,
                         help="Use explicit offline JSON issue metadata fixture")
    args = parser.parse_args()
    try:
        config = load_manifest(args.manifest)
        snapshot = (fetch_open_issue_snapshot(config) if args.live else
                    json.loads(args.snapshot.read_text(encoding="utf-8")))
        result = select_tasks(config, snapshot)
    except (DispatchError, OSError, ValueError) as exc:
        error = str(exc) if isinstance(exc, DispatchError) else "INVALID_INPUT"
        print(json.dumps({"status": "HOLD", "reason": error}))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
