#!/usr/bin/env python3
"""One-shot, manually authorized, SYNTHETIC-ONLY OpenAI smoke for ETH probe.

This is an API transport / comparative instrument check, NOT a blind clinical
benchmark or evidence of autonomy. Credentials and model answers are never logged.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

from falsification_probe import InvalidProbe, prepare, run_adapter, score

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "experiments/eth-falsification-probe/synthetic-claim-update.json"
ADAPTER = ROOT / "experiments/eth-falsification-probe/openai_model_adapter.py"
VARIANTS = ("native", "clinical_lite")
EXPECTED_PROBES = 4
MAX_REQUESTS = EXPECTED_PROBES * len(VARIANTS)
MODEL = "gpt-5-mini"


class SmokeHold(Exception):
    pass


def plan() -> dict:
    """Fail closed on modified public fixture; no secret or network required."""
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    ids = ["baseline"] + [p["id"] for p in spec["probes"]]
    if (spec.get("case_id") != "synthetic_claim_update_01" or
            len(ids) != EXPECTED_PROBES or len(set(ids)) != EXPECTED_PROBES or
            len(VARIANTS) * len(ids) != MAX_REQUESTS):
        raise SmokeHold("FIXTURE_OR_REQUEST_LIMIT_CHANGED")
    if not ADAPTER.is_file():
        raise SmokeHold("ADAPTER_MISSING")
    return {
        "mode": "SYNTHETIC_ONLY_NOT_BLIND", "model": MODEL,
        "variants": list(VARIANTS), "packets_per_arm": len(ids),
        "max_api_calls": MAX_REQUESTS, "max_output_tokens_per_call": 950,
        "max_theoretical_output_tokens": MAX_REQUESTS * 950,
        "new_model_efficacy": "NOT_VALIDATED",
    }


def authorize(env: dict) -> None:
    """All must hold before the very first paid request."""
    guards = {
        "GITHUB_ACTIONS": "true",
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_REPOSITORY": "sheng-web-OS/Clinical_system",
        "OPENAI_MODEL": MODEL,
    }
    if any(env.get(k) != value for k, value in guards.items()):
        raise SmokeHold("TRUSTED_MAIN_MANUAL_ONLY")
    if not env.get("OPENAI_API_KEY", "").strip():
        raise SmokeHold("API_SECRET_NOT_CONFIGURED")
    if env.get("PROBE_APPROVED_EXTERNAL_DATA") == "true":
        raise SmokeHold("EXTERNAL_DATA_MUST_REMAIN_DISABLED")


def execute(env: dict | None = None) -> dict:
    """Run eight bounded, stateless provider requests from a trusted main job.

    Original model outputs and evaluator keys are ephemeral and never uploaded.
    Arms differ ONLY in instruction, not in packet relabeling or source access.
    """
    env = os.environ if env is None else env
    metadata = plan()
    authorize(env)
    original_variant = os.environ.get("PROBE_VARIANT")
    results = {}
    try:
        with tempfile.TemporaryDirectory(prefix="eth-synthetic-") as td:
            tmp = Path(td)
            reviewer = tmp / "packets"
            key_path = tmp / "coordinator/key.json"
            packets = prepare(SPEC, reviewer, key_path)
            if len(packets) != EXPECTED_PROBES:
                raise SmokeHold("PACKET_NUMBER_CHANGED")
            gold = json.loads(key_path.read_text(encoding="utf-8"))
            for variant in VARIANTS:
                os.environ["PROBE_VARIANT"] = variant
                response_path = tmp / "results" / (variant + ".json")
                done = run_adapter(
                    reviewer, response_path, ADAPTER, timeout=70,
                    allowed_env=("OPENAI_API_KEY", "OPENAI_MODEL", "PROBE_VARIANT"),
                    relabel=False)
                if done.get("executed") != EXPECTED_PROBES:
                    raise SmokeHold("INCOMPLETE_MODEL_ARM")
                raw = json.loads(response_path.read_text(encoding="utf-8"))
                usage = raw.get("provider_usage", {})
                if len(usage) != EXPECTED_PROBES or any(
                        not isinstance(x, dict) or not isinstance(x.get("total_tokens"), int)
                        or x["total_tokens"] <= 0 for x in usage.values()):
                    raise SmokeHold("PROVIDER_USAGE_INCOMPLETE")
                grade = score(gold, raw)
                results[variant] = {
                    "correct_packets": sum(x["passed"] and x.get("relation_passed", True)
                                           for x in grade["results"]),
                    "total_packets": grade["trial_count"],
                    "observed_failed_stages": {s: sum(s in x["failed_stages"]
                        for x in grade["results"]) for s in
                        ("S1_question", "S2_evidence", "S3_decision", "S4_review")},
                    "reported_tokens": sum(x["total_tokens"] for x in usage.values()),
                }
    finally:
        if original_variant is None:
            os.environ.pop("PROBE_VARIANT", None)
        else:
            os.environ["PROBE_VARIANT"] = original_variant
    return {"status": "SYNTHETIC_API_SMOKE_ONLY", "plan": metadata,
            "results": results,
            "cautions": [
                "Public answer-key fixture; NOT an unseen or clinical benchmark.",
                "No independent reviewer; trial results cannot establish skill transfer.",
                "Reported tokens are adapter/provider usage, NOT verified billing charges.",
                "A single paired fixture is not statistical evidence of superiority.",
            ]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true", help="No network or key")
    mode.add_argument("--execute", action="store_true", help="Trusted-main manual only")
    args = parser.parse_args()
    try:
        result = execute() if args.execute else plan()
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (InvalidProbe, SmokeHold, ValueError, OSError, KeyError) as err:
        # Never echo arbitrary exceptions (adapter/output may contain private bytes).
        label = str(err) if isinstance(err, SmokeHold) else "PROBE_HOLD"
        print(json.dumps({"status": "HOLD", "reason": label}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
