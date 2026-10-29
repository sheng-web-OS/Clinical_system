#!/usr/bin/env python3
"""Read public GitHub facts for one allowlisted SHADOW task; never execute it.

The same observer accepts raw JSON fetched by the connected GitHub tools.
Issue/PR prose is never interpreted as instructions. A checkpoint is metadata,
not authenticated evidence of reviewer identity, medical approval or ownership.
"""
import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from tools.dispatch_selector import DispatchError, REPO, load_manifest
from tools.dispatch_runtime import (SHA, artifact_revision, route_checkpoint, task_for,
                                    valid_path, validate_checkpoint)

ROOT = "/repos/" + REPO
START = "<!-- DISPATCH_CHECKPOINT_V1:START -->"
END = "<!-- DISPATCH_CHECKPOINT_V1:END -->"


def require(condition, reason):
    if not condition:
        raise DispatchError(reason)


def checkpoint_from_comments(comments, config, task_id, pr_number, owner):
    """Latest operator-authored marker wins; malformed latest never falls back."""
    require(type(comments) is list, "INVALID_COMMENT_METADATA")
    marked = [c for c in comments if type(c) is dict
              and c.get("user", {}).get("login") == owner
              and type(c.get("body")) is str and START in c["body"]]
    if not marked:
        return None
    require(all(type(c.get("id")) is int for c in marked), "INVALID_COMMENT_ID")
    latest = max(marked, key=lambda c: c["id"])
    body = latest["body"]
    require(body.count(START) == 1 and body.count(END) == 1,
            "AMBIGUOUS_CHECKPOINT_MARKER")
    encoded = body.split(START, 1)[1].split(END, 1)[0].strip()
    require(len(encoded) <= 20000, "CHECKPOINT_TOO_LARGE")
    try:
        checkpoint = json.loads(encoded)
    except ValueError:
        raise DispatchError("INVALID_CHECKPOINT_JSON") from None
    validate_checkpoint(checkpoint, config)
    require(checkpoint["task_id"] == task_id and checkpoint["pr_number"] == pr_number,
            "CHECKPOINT_ASSOCIATION_MISMATCH")
    return {"comment_id": latest["id"], "checkpoint": checkpoint}


def observe_task(config, task_id, pr_number, paths, read_json, worker_id, run_id):
    """Fetch facts twice around the observation to detect a moving PR HEAD.

    read_json takes a fixed GitHub REST path and returns its raw JSON. Callers
    may use connected tools or the bounded GET-only client below. The explicit
    task/PR/path inputs are an observation scope, never execution permission.
    """
    task = task_for(config, task_id)
    require(type(pr_number) is int and pr_number > 0 and
            "pr:" + str(pr_number) not in config["frozen_eval"]["excluded_targets"],
            "PROTECTED_OR_INVALID_PR")
    require(type(paths) is list and 0 < len(paths) <= 40
            and all(valid_path(p) for p in paths) and len(set(paths)) == len(paths),
            "INVALID_OBSERVATION_PATHS")
    repo = read_json(ROOT)
    require(type(repo) is dict and repo.get("full_name") == REPO
            and repo.get("private") is False
            and type(repo.get("owner")) is dict
            and repo["owner"].get("login") == REPO.split("/")[0],
            "REPOSITORY_IDENTITY_OR_VISIBILITY_UNVERIFIED")
    control = read_json(ROOT + "/branches/main")
    require(type(control) is dict and control.get("protected") is True,
            "CONTROL_BRANCH_NOT_PROTECTED")
    main_sha = control.get("commit", {}).get("sha")
    require(type(main_sha) is str and SHA.fullmatch(main_sha), "INVALID_MAIN_SHA")
    issue_number = int(task["target"].split(":")[1])
    issue = read_json(ROOT + "/issues/" + str(issue_number))
    require(type(issue) is dict and issue.get("number") == issue_number
            and issue.get("state") in {"open", "closed"} and "pull_request" not in issue,
            "ISSUE_METADATA_UNVERIFIED")
    pr_path = ROOT + "/pulls/" + str(pr_number)
    pr = read_json(pr_path)
    require(type(pr) is dict and pr.get("number") == pr_number
            and pr.get("state") in {"open", "closed"}
            and type(pr.get("merged")) is bool
            and pr.get("base", {}).get("repo", {}).get("full_name") == REPO
            and pr.get("head", {}).get("repo", {}).get("full_name") == REPO,
            "PR_REPOSITORY_UNVERIFIED")
    head = pr.get("head", {}).get("sha")
    require(type(head) is str and SHA.fullmatch(head), "INVALID_PR_HEAD")
    tree = read_json(ROOT + "/git/trees/" + head + "?recursive=1")
    require(type(tree) is dict and tree.get("truncated") is False
            and type(tree.get("tree")) is list, "TREE_INCOMPLETE")
    blobs = {}
    for path in paths:
        entries = [e for e in tree["tree"] if e.get("path") == path]
        require(len(entries) == 1 and entries[0].get("type") == "blob"
                and entries[0].get("mode") == "100644"
                and type(entries[0].get("sha")) is str
                and SHA.fullmatch(entries[0]["sha"]), "ARTIFACT_NOT_REGULAR_BLOB")
        blobs[path] = entries[0]["sha"]
    runs = read_json(ROOT + "/actions/runs?head_sha=" + head
                     + "&event=pull_request&per_page=100")
    require(type(runs) is dict and type(runs.get("workflow_runs")) is list
            and type(runs.get("total_count")) is int, "CI_METADATA_UNVERIFIED")
    ci = []
    for run in runs["workflow_runs"]:
        if run.get("head_sha") == head and any(
                p.get("number") == pr_number for p in run.get("pull_requests", [])):
            ci.append({key: run.get(key) for key in
                       ("id", "head_sha", "status", "conclusion", "html_url")})
    # Read only the last two pages. A checkpoint older than that is explicitly
    # missing; never traverse unbounded history or invent the current state.
    count = pr.get("comments")
    require(type(count) is int and count >= 0, "COMMENT_COUNT_UNVERIFIED")
    comments = []
    last_page = max(1, (count + 99) // 100)
    for page in range(max(1, last_page - 1), last_page + 1):
        items = read_json(ROOT + "/issues/" + str(pr_number)
                          + "/comments?per_page=100&page=" + str(page))
        require(type(items) is list, "INVALID_COMMENT_METADATA")
        comments.extend(items)
    receipt = checkpoint_from_comments(
        comments, config, task_id, pr_number, repo["owner"].get("login"))
    route = (route_checkpoint(receipt["checkpoint"], config, blobs, worker_id, run_id)
             if receipt else {"next_action": "STRUCTURED_CHECKPOINT_MISSING",
                              "execution_authorized": False})
    if receipt:
        require(receipt["checkpoint"]["observed_head"] == head,
                "CHECKPOINT_HEAD_STALE_RECONCILE_BEFORE_USE")
    if issue["state"] == "closed":
        route["next_action"] = "CLOSED_ISSUE_NO_DISPATCH"
    elif pr["state"] == "closed" and not pr["merged"]:
        route["next_action"] = "CLOSED_PR_NO_DISPATCH"
    elif receipt:
        stage = receipt["checkpoint"]["stage"]
        if stage in {"MERGED_VERIFYING", "VERIFIED_COMPLETE"} and not pr["merged"]:
            route["next_action"] = "HOLD_MERGE_NOT_VERIFIED"
        elif pr["merged"] and stage not in {"MERGED_VERIFYING", "VERIFIED_COMPLETE"}:
            route["next_action"] = "RECONCILE_MERGED_PR_CHECKPOINT"
    after = read_json(pr_path)
    require(after.get("head", {}).get("sha") == head and after.get("state") == pr.get("state")
            and after.get("merged") == pr.get("merged")
            and after.get("comments") == count
            and after.get("updated_at") == pr.get("updated_at"),
            "PR_CHANGED_DURING_OBSERVATION")
    final_control = read_json(ROOT + "/branches/main")
    require(final_control.get("commit", {}).get("sha") == main_sha
            and final_control.get("protected") is True,
            "CONTROL_PLANE_CHANGED_DURING_OBSERVATION")
    return {
        "status": "SHADOW_OBSERVATION_ONLY", "task_id": task_id,
        "target": task["target"], "pr_number": pr_number, "main_sha": main_sha,
        "observed_head": head, "artifact_blobs": blobs,
        "evidence_revision": artifact_revision(blobs),
        "issue_state": issue["state"], "pr_state": pr.get("state"),
        "pr_merged": pr["merged"],
        "ci_runs": ci, "ci_list_complete": runs["total_count"] <= 100,
        "checkpoint_comment_id": receipt["comment_id"] if receipt else None,
        "next_action": route["next_action"],
        "owner_status": "LEASE_NOT_VERIFIED", "review_identity": "NOT_AUTHENTICATED",
        "medical_approval": "NOT_ASSESSED", "execution_authorized": False,
        "model_calls": 0, "write_actions": 0,
        "requires_issue_pr_routing_verification": True,
        "requires_live_source_verification": True,
    }


class GitHubReader:
    """Fixed host, bounded GETs; never log token, URL payloads or API responses."""
    def __call__(self, path):
        require(path.startswith(ROOT), "UNAPPROVED_READ_PATH")
        headers = {"Accept": "application/vnd.github+json",
                   "User-Agent": "clinical-os-dispatch-observe/0.3"}
        if os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
        request = urllib.request.Request("https://api.github.com" + path, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payload = response.read(2000001)
            require(len(payload) <= 2000000, "GITHUB_RESPONSE_TOO_LARGE")
            return json.loads(payload)
        except (OSError, ValueError, urllib.error.HTTPError):
            raise DispatchError("GITHUB_READ_FAILED") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default="ops/dispatch.json")
    parser.add_argument("--task", required=True)
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--paths", nargs="+", required=True)
    parser.add_argument("--worker-id", required=True)
    parser.add_argument("--run-id", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--live", action="store_true")
    source.add_argument("--snapshot", type=Path,
                        help="Raw path-keyed JSON from connected GitHub reads; not a live run")
    args = parser.parse_args()
    try:
        config = load_manifest(args.manifest)
        if args.live:
            reader = GitHubReader()
        else:
            snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
            def reader(path):
                require(path in snapshot, "SNAPSHOT_PATH_MISSING")
                return snapshot[path]
        result = observe_task(config, args.task, args.pr, args.paths, reader,
                              args.worker_id, args.run_id)
        result["input_mode"] = "LIVE_GET_ONLY" if args.live else "SUPPLIED_SNAPSHOT"
    except (DispatchError, OSError, ValueError, TypeError, KeyError, AttributeError):
        # Only fixed dispatch codes are exposed, never response bodies or tokens.
        import sys
        error = sys.exc_info()[1]
        reason = str(error) if isinstance(error, DispatchError) else "INVALID_INPUT"
        print(json.dumps({"status": "HOLD", "reason": reason,
                          "execution_authorized": False}))
        return 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
