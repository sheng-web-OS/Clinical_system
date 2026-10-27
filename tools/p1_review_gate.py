#!/usr/bin/env python3
"""Fail-closed PR-head status for unresolved trusted P0/P1 review blockers.

This runs ONLY from the protected default-branch workflow. It never checks out
or executes a PR's untrusted version of this program.
"""
import json
import os
import re
import sys
from urllib.request import Request, urlopen

CONTEXT = "p1-review-hold"
TRUSTED = {"OWNER", "MEMBER", "COLLABORATOR"}
BLOCK = re.compile(r"\bP[01][_-]BLOCK\b", re.I)
SEVERITY = re.compile(r"\bP[01]\b", re.I)
LEGACY_LEAD = re.compile(r"出版前|發布前|合併前|阻塞|hard.stop", re.I)
STOP_WORDS = re.compile(r"請不要|不可|不得|不能|不應|暫停|HOLD|do not|must not", re.I)
RESOLVED = re.compile(
    r"\[P1_RESOLVED\s+source=(issue|review|inline)\s+id=(\d+)"
    r"\s+head=([a-f0-9]{40})\s+evidence=(https://[^\s\]]+)\]",
    re.I,
)


def is_blocker(item):
    """Recognize explicit markers and the original #171 pre-merge P1 warning."""
    if item.get("author_association") not in TRUSTED:
        return False
    body = item.get("body") or ""
    if BLOCK.search(body):
        return True
    return (bool(SEVERITY.search(body[:200]))
            and bool(LEGACY_LEAD.search(body[:200]))
            and bool(STOP_WORDS.search(body)))


def evaluate(pr, records):
    """Pure decision logic, scoped to the current HEAD and a separate reviewer."""
    head = pr["head"]["sha"].lower()
    author = pr["user"]["login"].lower()
    active = [i for i in records if is_blocker(i)]
    for blocker in active[:]:
        for item in records:
            if item["source"] == blocker["source"] and item["id"] == blocker["id"]:
                continue
            if item.get("author_association") not in TRUSTED:
                continue
            if (item.get("user") or {}).get("login", "").lower() == author:
                continue  # a PR author cannot self-clear a high-severity blocker
            if (item.get("created_at") or "") < (blocker.get("created_at") or ""):
                continue
            for match in RESOLVED.finditer(item.get("body") or ""):
                source, identifier, sha, _evidence = match.groups()
                if (source.lower(), int(identifier), sha.lower()) == (
                    blocker["source"], blocker["id"], head
                ):
                    active.remove(blocker)
                    break
            if blocker not in active:
                break
    return active


def api(path, token, method="GET", data=None):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = Request(
        "https://api.github.com" + path,
        data=body,
        method=method,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "clinical-os-p1-review-gate",
        },
    )
    with urlopen(req, timeout=25) as response:
        return json.load(response)


def all_pages(path, token):
    out = []
    for page in range(1, 31):
        separator = "&" if "?" in path else "?"
        batch = api(f"{path}{separator}per_page=100&page={page}", token)
        if not isinstance(batch, list):
            raise ValueError("GitHub pagination returned a non-list result")
        out.extend(batch)
        if len(batch) < 100:
            return out
    raise ValueError("Too many PR comments: manual review required (fail closed)")


def tagged(items, source):
    return [
        {**item, "source": source}
        for item in items
        if isinstance(item.get("id"), int)
    ]


def event_pr_number(event):
    if "pull_request" in event:
        return int(event.get("number") or event["pull_request"]["number"])
    if event.get("issue", {}).get("pull_request"):
        return int(event["issue"]["number"])
    return None


def run():
    event_path = os.environ["GITHUB_EVENT_PATH"]
    with open(event_path, encoding="utf-8") as f:
        event = json.load(f)
    n = event_pr_number(event)
    if n is None:
        print("Not a pull request event; no PR status written.")
        return 0
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    base = f"/repos/{repo}"
    pr = api(f"{base}/pulls/{n}", token)
    if pr.get("state") != "open":
        print("Closed pull request; no merge-eligibility status needed.")
        return 0
    head = pr["head"]["sha"]
    run_link = (
        "https://github.com/" + repo + "/actions/runs/"
        + os.environ["GITHUB_RUN_ID"]
    )
    # Invalidate an earlier green status BEFORE reading potentially stale or
    # unavailable comments. A failed API read now leaves required status pending.
    api(
        f"{base}/statuses/{head}", token, method="POST",
        data={"state": "pending", "context": CONTEXT,
              "description": "Rechecking PR discussion for P0/P1 blockers",
              "target_url": run_link},
    )
    rows = (
        tagged(all_pages(f"{base}/issues/{n}/comments", token), "issue")
        + tagged(all_pages(f"{base}/pulls/{n}/reviews", token), "review")
        + tagged(all_pages(f"{base}/pulls/{n}/comments", token), "inline")
    )
    pending = evaluate(pr, rows)
    state = "failure" if pending else "success"
    summary = (
        f"Unresolved P0/P1 review: {len(pending)} item(s); see PR discussion"
        if pending else "No unresolved trusted P0/P1 review blockers"
    )
    # Publish a final SHA-scoped status only after reading all PR evidence.
    api(
        f"{base}/statuses/{head}", token, method="POST",
        data={"state": state, "context": CONTEXT,
              "description": summary[:140], "target_url": run_link},
    )
    for item in pending:
        print(f"BLOCKED {item['source']}:{item['id']} "
              f"{item.get('html_url', '')}")
    print(f"{CONTEXT}: {state} @ {head}")
    return 1 if pending else 0


if __name__ == "__main__":
    try:
        sys.exit(run())
    except Exception as exc:
        # A required status is missing rather than mistakenly green.
        print(f"P1_REVIEW_GATE_ERROR (fail closed): {exc}", file=sys.stderr)
        sys.exit(2)
