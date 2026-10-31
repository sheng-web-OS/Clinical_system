#!/usr/bin/env python3
"""GitHub-only synthetic Draft PR writer. No Google/OpenAI credentials in this job."""
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = "sheng-web-OS/Clinical_system"
BRANCH = "bot/synthetic-drive-source-proof"
FILE_PATH = "experiments/autonomy-shadow/results/synthetic-drive-read-proof.md"
BODY = (
    "# Synthetic Google Drive read verified\n\n"
    "This generated file represents **only** the synthetic sandbox marker check. "
    "It contains no real source bytes, Drive file IDs, patient data or "
    "private information.\n\n"
    "Agent requested a source read; the deterministic gate allowed it, "
    "and the expected synthetic source markers were found.\n\n"
    "**No autonomous medical judgment, clinical editorial approval or "
    "production deployment is certified.**\n"
)


def headers():
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise RuntimeError("MISSING_GITHUB_TOKEN")
    return {"Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}


def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("https://api.github.com/repos/" + REPO + "/" + path,
                                 data=data, headers=headers(), method=method)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read(200000))
    except urllib.error.HTTPError as exc:
        raise RuntimeError("GITHUB_API_HTTP_" + str(exc.code)) from None
    except (urllib.error.URLError, ValueError):
        raise RuntimeError("GITHUB_API_FAILED") from None


def plan(verified, repo, ref):
    if verified != "true" or repo != REPO or ref != "refs/heads/main":
        return "HOLD"
    return "PROPOSE_DRAFT_PR"


def main():
    if plan(os.getenv("VERIFIED_SYNTHETIC_READ"), os.getenv("GITHUB_REPOSITORY"),
            os.getenv("GITHUB_REF")) != "PROPOSE_DRAFT_PR":
        print('{"decision":"HOLD"}')
        return 2
    try:
        existing = api("GET", "pulls?state=open&head=" + urllib.parse.quote(
            "sheng-web-OS:" + BRANCH, safe=""))
        if existing:
            print('{"status":"SKIP","reason":"EXISTING_PR"}')
            return 0
        try:
            api("GET", "git/ref/heads/" + BRANCH)
            # Never mutate an unknown pre-existing branch.
            print('{"status":"HOLD","reason":"EXISTING_BRANCH_WITHOUT_PR"}')
            return 2
        except RuntimeError as exc:
            if str(exc) != "GITHUB_API_HTTP_404":
                raise
        main_ref = api("GET", "git/ref/heads/main")
        sha = main_ref["object"]["sha"]
        api("POST", "git/refs", {"ref": "refs/heads/" + BRANCH, "sha": sha})
        api("PUT", "contents/" + FILE_PATH, {
            "message": "test: record verified synthetic Drive source marker",
            "content": base64.b64encode(BODY.encode()).decode(),
            "branch": BRANCH,
        })
        pr = api("POST", "pulls", {
            "title": "[Synthetic][HOLD] Verified Drive source marker",
            "head": BRANCH, "base": "main", "draft": True,
            "body": "Entirely synthetic fixture; no confidential sources. "
                    "Created by authorized read-only Drive agent after synthetic marker check. "
                    "HOLD: no merge, no publication, no medical approval.",
        })
        print(json.dumps({"status": "DRAFT_PR_CREATED", "number": pr["number"]}))
        return 0
    except (RuntimeError, KeyError) as exc:
        # Never print returned data or secrets, only closed-set reason codes.
        allowed = ("MISSING_GITHUB_TOKEN", "GITHUB_API_FAILED",
                   "GITHUB_API_HTTP_403", "GITHUB_API_HTTP_422", "GITHUB_API_HTTP_404",
                   "GITHUB_API_HTTP_401")
        error = str(exc) if str(exc) in allowed else "GITHUB_WRITE_FAILED"
        print(json.dumps({"status": "HOLD", "error": error}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
