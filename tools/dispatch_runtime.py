"""Pure dispatcher checkpoint/lease plans. No network, persistence or authority.

A lease proposal takes effect ONLY after a caller commits it with Git ref CAS
and reads back the resulting revision. These functions cannot authenticate run
identity or clinical review. Existing publication/permission gates still apply.
"""
import copy
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import PurePosixPath

from tools.dispatch_selector import DispatchError

SHA = re.compile(r"[a-f0-9]{40}")
IDENTITY = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{2,159}")
GATE = re.compile(r"[a-z][a-z0-9-]{2,100}")
STAGES = {"WRITING", "AWAITING_REVIEW", "CHANGES_REQUESTED",
          "REVIEW_ACCEPTED", "MERGED_VERIFYING", "VERIFIED_COMPLETE",
          "EXTERNAL_BLOCKED", "SUPERSEDED"}
CHECKPOINT_FIELDS = {
    "schema_version", "task_id", "target", "pr_number", "observed_head",
    "artifact_blobs", "stage", "writer_id", "writer_run_id", "reviewer_id",
    "reviewer_run_id", "reviewed_blobs", "next_gate_id",
}
LEASE_FIELDS = {"execution_id", "resources", "issued_at", "expires_at", "fence"}


def require(condition, reason):
    if not condition:
        raise DispatchError(reason)


def identity(value):
    return type(value) is str and IDENTITY.fullmatch(value) is not None


def task_for(config, task_id):
    matches = [t for t in config["tasks"]
               if t["id"] == task_id and t["enabled"]]
    require(len(matches) == 1, "TASK_NOT_ENABLED_OR_ALLOWLISTED")
    task = matches[0]
    require(task["target"] not in config["frozen_eval"]["excluded_targets"],
            "PROTECTED_EXPERIMENT_SCOPE")
    return task


def valid_path(value):
    return (type(value) is str and 0 < len(value) <= 300
            and re.fullmatch(r"[A-Za-z0-9_./-]+", value) is not None
            and not value.startswith("/")
            and ".." not in value.split("/")
            and str(PurePosixPath(value)) == value)


def valid_blobs(value):
    return (type(value) is dict and 0 < len(value) <= 40
            and all(valid_path(path) and type(sha) is str
                    and SHA.fullmatch(sha) for path, sha in value.items()))


def artifact_revision(blobs):
    """Task-local inputs: unrelated main/PR commits do not trigger rework."""
    require(valid_blobs(blobs), "INVALID_ARTIFACT_BINDING")
    encoded = json.dumps(blobs, sort_keys=True, separators=(",", ":")).encode()
    return "artifacts:" + hashlib.sha256(encoded).hexdigest()


def validate_checkpoint(checkpoint, config):
    require(type(checkpoint) is dict and set(checkpoint) == CHECKPOINT_FIELDS,
            "INVALID_CHECKPOINT_SCHEMA")
    c = checkpoint
    require(type(c["schema_version"]) is int and c["schema_version"] == 1,
            "INVALID_CHECKPOINT_VERSION")
    task = task_for(config, c["task_id"])
    require(c["target"] == task["target"] and type(c["pr_number"]) is int
            and c["pr_number"] > 0 and "pr:" + str(c["pr_number"])
            not in config["frozen_eval"]["excluded_targets"],
            "CHECKPOINT_TARGET_MISMATCH_OR_PROTECTED")
    require(type(c["observed_head"]) is str and SHA.fullmatch(c["observed_head"])
            and valid_blobs(c["artifact_blobs"]), "INVALID_ARTIFACT_BINDING")
    require(type(c["stage"]) is str and c["stage"] in STAGES
            and identity(c["writer_id"]) and identity(c["writer_run_id"])
            and (c["next_gate_id"] is None or
                 (type(c["next_gate_id"]) is str
                  and GATE.fullmatch(c["next_gate_id"]))),
            "INVALID_CHECKPOINT_STATE")
    review = (c["reviewer_id"], c["reviewer_run_id"], c["reviewed_blobs"])
    if any(item is not None for item in review):
        require(identity(c["reviewer_id"]) and identity(c["reviewer_run_id"])
                and c["reviewer_id"] != c["writer_id"]
                and c["reviewer_run_id"] != c["writer_run_id"]
                and c["reviewed_blobs"] == c["artifact_blobs"],
                "REVIEW_NOT_INDEPENDENT_OR_STALE")
    if c["stage"] in {"REVIEW_ACCEPTED", "MERGED_VERIFYING", "VERIFIED_COMPLETE"}:
        require(all(item is not None for item in review),
                "REVIEW_EVIDENCE_REQUIRED")
    return c


def route_checkpoint(checkpoint, config, current_blobs, worker_id, run_id):
    """Suggest the next role, never certify a claimed medical/deployment PASS."""
    c = validate_checkpoint(checkpoint, config)
    require(valid_blobs(current_blobs) and identity(worker_id) and identity(run_id),
            "INVALID_CURRENT_OBSERVATION")
    if current_blobs != c["artifact_blobs"]:
        action = "REFREEZE_CHANGED_ARTIFACTS"
    elif c["stage"] == "AWAITING_REVIEW":
        action = ("HANDOFF_INDEPENDENT_REVIEW" if worker_id == c["writer_id"]
                  or run_id == c["writer_run_id"] else "REVIEW_EXACT_BLOBS")
    else:
        action = {
            "WRITING": "CONTINUE_ORIGINAL_WRITER",
            "CHANGES_REQUESTED": "RETURN_TO_ORIGINAL_WRITER",
            "REVIEW_ACCEPTED": "CHECK_RELEASE_GATES",
            "MERGED_VERIFYING": "VERIFY_PRODUCTION_AND_HTTPS",
            "VERIFIED_COMPLETE": "VERIFY_COMPLETION_EVIDENCE_BEFORE_CLOSING",
            "EXTERNAL_BLOCKED": "WAIT_FOR_DOCUMENTED_UNBLOCK_CONDITION",
            "SUPERSEDED": "FOLLOW_VERIFIED_REPLACEMENT",
        }[c["stage"]]
    return {"next_action": action, "execution_authorized": False,
            "requires_live_source_verification": True}


def utc(value):
    require(type(value) is str and
            re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value),
            "INVALID_LEASE_TIME")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc)
    except ValueError:
        raise DispatchError("INVALID_LEASE_TIME") from None


def timestamp(value):
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def valid_resource(value):
    return (type(value) is str and
            (re.fullmatch(r"pr:[1-9][0-9]*", value) is not None or
             (value.startswith("path:") and valid_path(value[5:]))))


def validate_leases(state):
    require(type(state) is dict and set(state) == {
        "schema_version", "generation", "leases"}
        and type(state["schema_version"]) is int and state["schema_version"] == 1
        and type(state["generation"]) is int and state["generation"] >= 0
        and type(state["leases"]) is dict and len(state["leases"]) <= 30,
        "INVALID_LEASE_TABLE")
    resources_seen = set()
    for task_id, lease in state["leases"].items():
        require(type(task_id) is str and GATE.fullmatch(task_id)
                and type(lease) is dict and set(lease) == LEASE_FIELDS,
                "INVALID_LEASE")
        resources = lease["resources"]
        require(identity(lease["execution_id"]) and type(resources) is list
                and 0 < len(resources) <= 41
                and all(valid_resource(r) for r in resources)
                and resources == sorted(set(resources))
                and type(lease["fence"]) is int
                and 1 <= lease["fence"] <= state["generation"],
                "INVALID_LEASE_VALUES")
        require(not resources_seen.intersection(resources),
                "OVERLAPPING_LEASE_RESOURCES")
        resources_seen.update(resources)
        lifetime = (utc(lease["expires_at"]) - utc(lease["issued_at"])).total_seconds()
        require(0 < lifetime <= 1800, "INVALID_LEASE_LIFETIME")
    return state


def propose_claim(state, config, task_id, execution_id, resources,
                  expected_generation, now, ttl_seconds=1200):
    """Return a CAS proposal. Even active manifests cannot perform writes here."""
    validate_leases(state)
    task_for(config, task_id)
    require(type(expected_generation) is int
            and expected_generation == state["generation"], "STALE_LEASE_GENERATION")
    require(identity(execution_id) and type(ttl_seconds) is int
            and 1 <= ttl_seconds <= 1800 and type(resources) is list
            and 0 < len(resources) <= 41 and all(valid_resource(r) for r in resources)
            and resources == sorted(set(resources)), "INVALID_CLAIM")
    require(any(r.startswith("pr:") for r in resources), "PR_RESOURCE_REQUIRED")
    require(not set(resources).intersection(config["frozen_eval"]["excluded_targets"]),
            "PROTECTED_EXPERIMENT_SCOPE")
    clock = utc(now)
    for held_task, lease in state["leases"].items():
        if held_task == task_id or set(resources).intersection(lease["resources"]):
            require(clock >= utc(lease["issued_at"]), "LEASE_CLOCK_UNVERIFIED")
            reason = ("EXPIRED_OWNER_REQUIRES_RECONCILIATION"
                      if clock >= utc(lease["expires_at"]) else "ACTIVE_OWNER")
            raise DispatchError(reason)
    proposed = copy.deepcopy(state)
    proposed["generation"] += 1
    proposed["leases"][task_id] = {
        "execution_id": execution_id, "resources": resources[:],
        "issued_at": now, "expires_at": timestamp(clock + timedelta(seconds=ttl_seconds)),
        "fence": proposed["generation"],
    }
    validate_leases(proposed)
    return {"proposed_state": proposed, "execution_authorized": False,
            "requires_git_ref_cas_and_readback": True}


def check_lease(state, task_id, execution_id, fence, now):
    validate_leases(state)
    lease = state["leases"].get(task_id)
    require(type(lease) is dict and lease["execution_id"] == execution_id
            and type(fence) is int and lease["fence"] == fence,
            "LEASE_OWNER_OR_FENCE_CHANGED")
    require(utc(lease["issued_at"]) <= utc(now) < utc(lease["expires_at"]),
            "LEASE_EXPIRED_OR_CLOCK_UNVERIFIED")
    return lease


def propose_release(state, task_id, execution_id, fence, expected_generation):
    """Only the recorded owner may release; expiry is never a takeover grant."""
    validate_leases(state)
    require(type(expected_generation) is int
            and expected_generation == state["generation"], "STALE_LEASE_GENERATION")
    lease = state["leases"].get(task_id)
    require(type(lease) is dict and lease["execution_id"] == execution_id
            and type(fence) is int and lease["fence"] == fence,
            "LEASE_OWNER_OR_FENCE_CHANGED")
    proposed = copy.deepcopy(state)
    del proposed["leases"][task_id]
    proposed["generation"] += 1
    return {"proposed_state": proposed, "execution_authorized": False,
            "requires_git_ref_cas_and_readback": True}
