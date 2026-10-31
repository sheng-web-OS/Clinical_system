#!/usr/bin/env python3
"""Read-only evidence-coverage diagnostic; NOT a population success-rate estimator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STAGES = (
    "artifact_observed",
    "engineering_verified",
    "independently_accepted",
    "downstream_value_verified",
)
ALLOWED_TRIGGERS = {"owner_directed", "scheduled_unprompted", "unknown"}
STATUSES = {"VERIFIED", "NOT_VERIFIED"}


def analyze(snapshot: dict[str, Any]) -> dict[str, Any]:
    if snapshot.get("scope") != "SELECTED_PUBLIC_PR_SHADOW":
        raise ValueError("Only selected public PR shadow snapshots are supported")
    if not snapshot.get("observed_on_utc"):
        raise ValueError("Missing observation date")
    tasks = snapshot.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Tasks must be a nonempty list")

    counts = {stage: 0 for stage in STAGES}
    unknown = {stage: 0 for stage in STAGES}
    observations = []
    seen = set()
    for task in tasks:
        task_id = task.get("task_id")
        if not isinstance(task_id, str) or not task_id or task_id in seen:
            raise ValueError("Missing or duplicate task_id")
        seen.add(task_id)
        if task.get("trigger") not in ALLOWED_TRIGGERS:
            raise ValueError(f"{task_id}: unknown trigger")
        if task.get("in_frozen_137") is not False:
            raise ValueError(f"{task_id}: frozen 72h cohort must not be evaluated")
        if task.get("owner_minutes") != "NOT_MEASURED":
            raise ValueError(f"{task_id}: owner minutes require a measured trace")
        if not str(task.get("source_pr", "")).startswith(
            "https://github.com/sheng-web-OS/Clinical_system/pull/"
        ):
            raise ValueError(f"{task_id}: canonical PR link required")
        evidence = task.get("stage_evidence")
        if not isinstance(evidence, dict):
            raise ValueError(f"{task_id}: missing stage evidence")
        last_verified = None
        gap = False
        for stage in STAGES:
            cell = evidence.get(stage)
            if not isinstance(cell, dict) or cell.get("status") not in STATUSES:
                raise ValueError(f"{task_id}: {stage} must explicitly be VERIFIED/NOT_VERIFIED")
            if cell["status"] == "NOT_VERIFIED":
                gap = True
                unknown[stage] += 1
                continue
            if gap:
                raise ValueError(f"{task_id}: cannot skip an unverified prerequisite")
            if not str(cell.get("source_url", "")).startswith("https://"):
                raise ValueError(f"{task_id}: verified stage requires source_url")
            if stage in STAGES[2:] and not cell.get("independent_acceptance"):
                raise ValueError(f"{task_id}: independent acceptance is a hard requirement")
            if stage == STAGES[-1] and not cell.get("outcome_evidence"):
                raise ValueError(f"{task_id}: downstream outcome evidence is required")
            last_verified = stage
            counts[stage] += 1
        observations.append({
            "task_id": task_id,
            "trigger": task["trigger"],
            "highest_verified_stage": last_verified,
            "next_unverified_stage": next(
                (s for s in STAGES if evidence[s]["status"] != "VERIFIED"), None
            ),
            "source_pr": task["source_pr"],
            "owner_minutes": "NOT_MEASURED",
        })
    return {
        "observed_on_utc": snapshot["observed_on_utc"],
        "scope": snapshot["scope"],
        "is_population_or_autonomy_success_rate": False,
        "sample_size": len(tasks),
        "verified_milestone_counts": counts,
        "not_verified_milestone_counts": unknown,
        "task_diagnostics": observations,
        "unprompted_accepted_rate": "NOT_COMPUTABLE",
        "owner_minutes_per_accepted_task": "NOT_MEASURED",
        "learning_transfer_gain": "NOT_MEASURED",
        "cross_task_reliability_gain": "NOT_MEASURED",
        "frozen_72h_experiment_affected": False,
        "interpretation": (
            "Evidence coverage among manually selected PRs only. NOT_VERIFIED is "
            "neither failure nor zero; the sample cannot establish autonomy or growth."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()
    snapshot = json.loads(args.input_json.read_text(encoding="utf-8"))
    print(json.dumps(analyze(snapshot), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
