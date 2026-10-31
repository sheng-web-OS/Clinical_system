#!/usr/bin/env python3
"""Check nine preflight packet boundaries plus a synthetic leak control.

No gold input is accepted. Private input paths are used only as denied paths;
stdout and the exclusive JSON receipt contain counts/booleans, never paths,
task hashes, job identifiers, commands, or task text.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid

import XDT01_docker_executor as runtime


ROOT = Path(__file__).resolve().parents[1]
BASE_CHECKS = {
    "non_root", "all_capabilities_dropped", "no_new_privileges",
    "network_none_no_routes_and_enetunreach", "root_filesystem_read_only",
    "provider_key_not_in_environment", "single_packet_mount",
    "exactly_one_task_and_job", "own_task_read_and_digest_verified",
}
CANARY = b"SYNTHETIC_CANARY_NO_ANSWER_DATA\n"


def require(ok, code):
    if not ok:
        raise runtime.Hold(code)


def sanitized_outcome(value, blocked):
    require(type(value) is dict and type(value.get("checks")) is dict,
            "PROBE_INVALID_RESULT")
    checks = value["checks"]
    require(set(checks) == BASE_CHECKS | set(blocked) and
            all(type(item) is bool for item in checks.values()), "PROBE_INVALID_CHECKS")
    network = value.get("network_evidence", {})
    uid = value.get("uid_evidence", {})
    require(type(network) is dict and
            type(network.get("no_ipv4_routes")) is bool and
            type(network.get("reserved_test_address_connect_errno")) is int and
            type(uid) is dict and type(uid.get("uid")) is int and
            type(uid.get("euid")) is int, "PROBE_INVALID_EVIDENCE")
    return {
        "status": "PASS" if all(checks.values()) else "BOUNDARY_FAILURE",
        "checks": checks, "provider_calls": 0,
        "uid_evidence": {key: uid[key] for key in ("uid", "euid")},
        "network_evidence": {key: network[key] for key in
                             ("no_ipv4_routes", "reserved_test_address_connect_errno")},
    }


def execute(command, name, blocked):
    environment = {key: value for key, value in os.environ.items()
                   if key not in {"OPENAI_API_KEY", "XDT01_PRIVATE_APPROVAL",
                                  "XDT01_BUDGET_EXTERNALLY_VERIFIED"}}
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=60, env=environment)
    except BaseException:
        try:
            cleanup = runtime.stop_exact_container(name)
        except BaseException:
            cleanup = {"confirmed": False}
        raise runtime.Hold("BOUNDARY_PROBE_INTERRUPTED_STOP_CONFIRMED"
                           if cleanup["confirmed"] else "BOUNDARY_PROBE_UNCERTAIN_STOP") from None
    if result.returncode not in (0, 3):
        cleanup = runtime.stop_exact_container(name)
        raise runtime.Hold("BOUNDARY_PROBE_PROCESS_FAILED"
                           if cleanup["confirmed"] else "BOUNDARY_PROBE_UNCERTAIN_STOP")
    try:
        outcome = sanitized_outcome(json.loads(result.stdout), blocked)
    except (ValueError, TypeError):
        raise runtime.Hold("PROBE_DID_NOT_RETURN_VALID_JSON") from None
    return result.returncode, outcome


def private_file(path, payload):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def verify(*, workspace, stage_root, cases_file, repo, output):
    workspace = Path(workspace).resolve(strict=True)
    stage_root = Path(stage_root).resolve(strict=True)
    cases_file = Path(cases_file).resolve(strict=True)
    output = Path(output).absolute()
    repo = runtime.repo_verified(repo)
    require(workspace.is_dir() and not workspace.is_symlink(), "PREFLIGHT_WORKSPACE_INVALID")
    require(stage_root.is_dir() and not stage_root.is_symlink(), "CASES_STAGE_INVALID")
    require(cases_file.is_file() and not cases_file.is_symlink(), "CASES_SOURCE_INVALID")
    require(not workspace.resolve().is_relative_to(repo) and
            not stage_root.resolve().is_relative_to(repo) and
            not cases_file.resolve().is_relative_to(repo), "PRIVATE_INPUT_INSIDE_PUBLIC_REPO")
    require(not output.exists() and not output.is_symlink(), "OUTPUT_MUST_BE_NEW")
    require(output.parent.is_dir(), "OUTPUT_PARENT_REQUIRED")
    expected = {"task-%02d" % sequence for sequence in range(1, 10)}
    actual = {path.name for path in workspace.iterdir() if path.name.startswith("task-")}
    require(actual == expected, "NINE_PREFLIGHT_PACKETS_REQUIRED")
    probe = Path(__file__).parent / "XDT01_docker_boundary_probe.py"
    root = Path(tempfile.mkdtemp(prefix="xdt01-boundary-", dir=workspace.parent)).resolve()
    root.chmod(0o700)
    canary = root / "synthetic-gold-canary.txt"
    private_file(canary, CANARY)
    if os.geteuid() == 0:
        os.chown(canary, 65532, 65532)
    rows, first = [], None
    for sequence in range(1, 10):
        packet = workspace / ("task-%02d" % sequence) / "packet.zip"
        sibling = workspace / ("task-%02d" % (sequence % 9 + 1)) / "packet.zip"
        require(packet.is_file() and sibling.is_file() and
                not packet.is_symlink() and not sibling.is_symlink(), "PREFLIGHT_PACKET_MISSING")
        target = root / ("probe-%02d" % sequence)
        target.mkdir(mode=0o700)
        if os.geteuid() == 0:
            os.chown(target, 65532, 65532)
        blocked = {
            "synthetic_gold_host_path_denied": str(canary.resolve()),
            "synthetic_gold_worker_path_denied": "/operator/gold-canary.txt",
            "facilitator_unmounted_path_denied": "/facilitator/gold.json",
            "cases_stage_host_path_denied": str(stage_root.resolve()),
            "stage_manifest_host_path_denied": str((stage_root / "stage_manifest.json").resolve()),
            "cases_source_host_path_denied": str(cases_file.resolve()),
            "sibling_packet_host_path_denied": str(sibling.resolve()),
            "sibling_packet_worker_path_denied": "/other-worker/packet.zip",
            "docker_socket_denied": "/var/run/docker.sock",
        }
        name = "xdt01-boundary-" + uuid.uuid4().hex
        command = runtime.docker_cmd({}, packet.resolve(), probe.resolve(), repo,
                                     target, False, name=name)
        command.extend(["--blocked-paths", json.dumps(blocked)])
        code, outcome = execute(command, name, blocked)
        require(code == 0 and outcome["status"] == "PASS", "BOUNDARY_PROBE_FAILED")
        rows.append({"worker_sequence": sequence, "exit_code": code, **outcome})
        if first is None:
            first = (command, blocked)
        print(json.dumps({"worker_sequence": sequence, "status": "PASS", "provider_calls": 0}),
              flush=True)
    # Mount only the new synthetic canary at the denied path. No real gold is
    # accepted, opened, copied, or mounted by this tool or its positive control.
    leaky, blocked = list(first[0]), first[1]
    name = "xdt01-boundary-control-" + uuid.uuid4().hex
    leaky[leaky.index("--name") + 1] = name
    leaky[2:2] = ["--mount", "type=bind,src=%s,dst=/operator/gold-canary.txt,readonly" % canary]
    code, outcome = execute(leaky, name, blocked)
    require(code == 3 and not outcome["checks"]["synthetic_gold_worker_path_denied"],
            "LEAK_CANARY_NOT_DETECTED")
    require(all(value for key, value in outcome["checks"].items()
                if key != "synthetic_gold_worker_path_denied"), "UNEXPECTED_CONTROL_FAILURE")
    receipt = {
        "schema_version": 1, "status": "DOCKER_BOUNDARY_CHECKS_PASS",
        "workers_checked": 9, "own_single_task_read_verified": 9,
        "synthetic_gold_canary_denied": 9, "cases_stage_denied": 9,
        "cases_source_denied": 9, "actual_host_sibling_packet_denied": 9,
        "non_root_verified": 9, "network_none_verified": 9,
        "negative_control": {"synthetic_marker_exposure_detected": True, "exit_code": code},
        "provider_calls": 0, "real_gold_read": False,
        "independent_examiner_identity_verified": False,
        "scientific_non_exposure_verified": False, "worker_results": rows,
    }
    private_file(output, (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps({key: value for key, value in receipt.items() if key != "worker_results"},
                     sort_keys=True))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("workspace", "stage-root", "cases-file", "repo", "output"):
        parser.add_argument("--" + name, required=True, type=Path)
    verify(**vars(parser.parse_args()))


if __name__ == "__main__":
    try:
        main()
    except (runtime.Hold, OSError, ValueError, subprocess.TimeoutExpired) as error:
        code = str(error) if isinstance(error, runtime.Hold) else type(error).__name__.upper()
        print(json.dumps({"status": "HOLD_" + code, "provider_calls": 0}))
        raise SystemExit(2) from None
