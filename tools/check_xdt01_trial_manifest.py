#!/usr/bin/env python3
"""Fail-closed STRUCTURAL check for XDT-01 sanitized metadata (not outcome validation).

Run only on a trusted private runner with a sanitized manifest. Never place hidden
prompts, first-pass answers, gold, model secrets, or unblinding map in public GitHub.
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DOMAINS = {"inventory", "it-incident", "provenance"}
ARMS = {"A", "B", "C"}
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
DENOMINATORS = {"pilot": 1, "exploratory": 4}
REQUIRED = ("task_id", "domain", "arm", "input_sha256", "model",
            "effort", "tool_policy_sha256", "token_cap", "time_cap_s",
            "first_pass_sha256")
# A strict exact-key contract is safer than a list of suspicious field names.
# The manifest is metadata ONLY; new fields need independent privacy review.
MANIFEST_KEYS = {"experiment_id", "phase", "protocol_commit",
                 "skill_sha256", "trials"}
TASK_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}\Z")
ATOM = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,99}\Z")


def check(obj):
    errors = []
    if not isinstance(obj, dict):
        return ["Manifest must be an object"]
    if set(obj) != MANIFEST_KEYS:
        errors.append("Unexpected top-level key: manifest must not include any payload")
    if obj.get("experiment_id") != "XDT-01":
        errors.append("Wrong experiment ID")
    phase = obj.get("phase")
    if phase not in DENOMINATORS:
        errors.append("Invalid phase")
    if not HEX40.fullmatch(str(obj.get("protocol_commit", ""))):
        errors.append("Missing or malformed exact protocol commit")
    if not HEX64.fullmatch(str(obj.get("skill_sha256", ""))):
        errors.append("Missing or malformed skill digest")
    trials = obj.get("trials")
    if not isinstance(trials, list):
        return errors + ["trials must be a list"]
    seen = set()
    tasks = defaultdict(list)
    for idx, t in enumerate(trials):
        if not isinstance(t, dict):
            errors.append(f"Trial {idx}: must be object")
            continue
        if set(t) != set(REQUIRED):
            errors.append(f"Trial {idx}: unexpected or missing field; payload forbidden")
        for k in REQUIRED:
            if k not in t:
                errors.append(f"Trial {idx}: missing {k}")
        task_id, arm, domain = t.get("task_id"), t.get("arm"), t.get("domain")
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            errors.append(f"Trial {idx}: invalid bounded task ID")
            continue
        for key in ("model", "effort"):
            if not isinstance(t.get(key), str) or not ATOM.fullmatch(t[key]):
                errors.append(f"Trial {idx}: invalid bounded {key}")
        if arm not in ARMS or domain not in DOMAINS:
            errors.append(f"Trial {idx}: invalid arm/domain")
        if (task_id, arm) in seen:
            errors.append(f"Trial {idx}: duplicate task/arm")
        seen.add((task_id, arm))
        for key in ("input_sha256", "tool_policy_sha256", "first_pass_sha256"):
            if not HEX64.fullmatch(str(t.get(key, ""))):
                errors.append(f"Trial {idx}: invalid digest {key}")
        for key in ("token_cap", "time_cap_s"):
            if type(t.get(key)) is not int or t[key] <= 0:
                errors.append(f"Trial {idx}: invalid {key}")
        tasks[task_id].append(t)
    if phase in DENOMINATORS:
        expected_per_domain = DENOMINATORS[phase]
        task_counts = Counter(v[0].get("domain") for v in tasks.values() if v)
        if set(task_counts) != DOMAINS or any(task_counts[d] != expected_per_domain for d in DOMAINS):
            errors.append(f"Task distribution must be {expected_per_domain} per domain")
        if len(trials) != expected_per_domain * 3 * 3:
            errors.append("Wrong trial denominator")
    # Same-task arms must have the same task packet, model and budget.
    for task_id, group in tasks.items():
        if {x.get("arm") for x in group} != ARMS or len(group) != 3:
            errors.append(f"{task_id}: requires exactly A/B/C")
        for key in ("domain", "input_sha256", "model", "effort",
                    "tool_policy_sha256", "token_cap", "time_cap_s"):
            if len({str(x.get(key)) for x in group}) != 1:
                errors.append(f"{task_id}: unmatched {key}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        obj = json.loads(args.manifest.read_text(encoding="utf-8"))
        problems = check(obj)
    except (OSError, json.JSONDecodeError) as e:
        problems = [f"Unreadable manifest: {e.__class__.__name__}"]
    if problems:
        for p in problems:
            print("HOLD:", p)
        raise SystemExit(2)
    print("STRUCTURE_OK_NOT_VALIDATED — no provider or independent judge attestation")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
