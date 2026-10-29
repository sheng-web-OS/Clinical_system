#!/usr/bin/env python3
"""Synthetic-only, fail-closed agent gate. Never log source bytes, identifiers or tokens."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

NAME = "Clinical OS — Synthetic Drive Agent Fixture (2026-10-29)"
MARKER = "SYNTHETIC FIXTURE — NO PATIENT DATA OR RESTRICTED MATERIAL"
CAPTION = "Sample size: 12 synthetic observations"
DECISIONS = {"READ", "SKIP", "HOLD"}


def validated_context(raw):
    if not isinstance(raw, dict) or raw.get("source_class") != "synthetic_public_fixture":
        raise ValueError("SOURCE_CLASS_REJECTED")
    if raw.get("task_id") != "DEMO-2026-10-29-A":
        raise ValueError("TASK_NOT_ALLOWLISTED")
    if raw.get("source_state") not in {"missing", "present", "unknown"}:
        raise ValueError("BAD_SOURCE_STATE")
    return {"task_id": raw["task_id"], "source_class": raw["source_class"],
            "source_state": raw["source_state"],
            "requires_original": raw.get("requires_original") is True}


def gate(ctx, decision):
    if decision not in DECISIONS:
        return "HOLD"
    if ctx["source_state"] == "present":
        return "SKIP"
    if ctx["source_state"] != "missing" or not ctx["requires_original"]:
        return "HOLD"
    return decision


def model_decision(ctx, key, model):
    if not key:
        raise RuntimeError("NOT_CONFIGURED_MODEL")
    schema = {
        "type": "object", "additionalProperties": False,
        "properties": {
            "decision": {"type": "string", "enum": ["READ", "SKIP", "HOLD"]},
            "reason_code": {"type": "string",
                            "enum": ["SOURCE_MISSING", "SOURCE_PRESENT", "UNCERTAIN", "OTHER"]},
        },
        "required": ["decision", "reason_code"],
    }
    payload = {
        "model": model, "store": False, "max_output_tokens": 250,
        "instructions": (
            "Decide based only on this public synthetic metadata. "
            "READ only if the original is missing and required. "
            "SKIP if present. HOLD if uncertain. No permissions can be granted."
        ),
        "input": json.dumps(ctx, ensure_ascii=False),
        "text": {"format": {"type": "json_schema", "name": "source_decision",
                            "strict": True, "schema": schema}},
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=55) as response:
            data = json.loads(response.read(200000))
    except (urllib.error.URLError, ValueError, TimeoutError):
        raise RuntimeError("MODEL_REQUEST_FAILED") from None
    chunks = [entry["text"] for item in data.get("output", [])
              if item.get("type") == "message"
              for entry in item.get("content", []) if entry.get("type") == "output_text"]
    try:
        decision = json.loads("".join(chunks))["decision"]
    except (KeyError, ValueError, TypeError):
        raise RuntimeError("MODEL_RESPONSE_INVALID") from None
    return decision if decision in DECISIONS else "HOLD"


def read_synthetic_drive(folder_id):
    if not folder_id or not folder_id.replace("-", "").replace("_", "").isalnum():
        raise RuntimeError("DRIVE_SCOPE_MISSING")
    try:
        import google.auth
        from google.auth.transport.requests import AuthorizedSession
        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/drive.readonly"])
        client = AuthorizedSession(creds)
        result = client.get(
            "https://www.googleapis.com/drive/v3/files",
            params={"q": "'" + folder_id + "' in parents and name = '" + NAME +
                         "' and trashed = false",
                    "fields": "files(id,mimeType),nextPageToken", "page_size": 10},
            timeout=30,
        )
        result.raise_for_status()
        files = result.json().get("files", [])
        if len(files) != 1 or files[0].get("mimeType") != "application/vnd.google-apps.document":
            raise RuntimeError("FIXTURE_NOT_FOUND")
        exported = client.get(
            "https://www.googleapis.com/drive/v3/files/" + files[0]["id"] + "/export",
            params={"mimeType": "text/plain"}, timeout=30)
        exported.raise_for_status()
        if MARKER not in exported.text or CAPTION not in exported.text:
            raise RuntimeError("FIXTURE_MISMATCH")
        return True
    except RuntimeError:
        raise
    except Exception:
        raise RuntimeError("DRIVE_READ_FAILED") from None


def execute(raw, mode, model_call=None, drive_call=None):
    ctx = validated_context(raw)
    if mode == "fixture":
        decision = "READ" if ctx["source_state"] == "missing" and ctx["requires_original"] else "SKIP"
    elif mode in {"shadow", "synthetic-read"}:
        decision = (model_call or model_decision)(
            ctx, os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_MODEL") or "gpt-5-mini")
    else:
        raise ValueError("BAD_MODE")
    decision = gate(ctx, decision)
    read = False
    if decision == "READ" and mode == "synthetic-read":
        read = bool((drive_call or read_synthetic_drive)(os.getenv("DRIVE_FIXTURE_FOLDER_ID")))
    return {"decision": decision, "mode": mode, "ai_decision": mode != "fixture",
            "drive_read_verified": read, "autonomy_certified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fixture", "shadow", "synthetic-read"],
                        default="fixture")
    parser.add_argument("--context", required=True)
    parser.add_argument("--github-output", default=None)
    args = parser.parse_args()
    try:
        with open(args.context, encoding="utf-8") as fh:
            raw = json.load(fh)
        result = execute(raw, args.mode)
        print(json.dumps(result, sort_keys=True))
        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as output:
                output.write("read_verified=" + ("true" if result["drive_read_verified"] else "false") + "\n")
        return 0
    except (RuntimeError, ValueError, KeyError, OSError) as exc:
        known = {"NOT_CONFIGURED_MODEL", "MODEL_REQUEST_FAILED", "MODEL_RESPONSE_INVALID",
                 "DRIVE_SCOPE_MISSING", "FIXTURE_NOT_FOUND", "FIXTURE_MISMATCH",
                 "DRIVE_READ_FAILED", "SOURCE_CLASS_REJECTED", "TASK_NOT_ALLOWLISTED",
                 "BAD_SOURCE_STATE", "BAD_MODE"}
        code = str(exc) if str(exc) in known else "FAIL_CLOSED"
        print(json.dumps({"status": "HOLD", "error": code}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
