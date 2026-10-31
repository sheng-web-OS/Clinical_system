"""Offline-only probe: prints booleans, never task or denied-file contents."""
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import socket
import zipfile


def readable(path):
    # Opening proves read capability; no denied-file payload is read, even if
    # the boundary is broken. The positive control uses only a synthetic file.
    try:
        descriptor = os.open(path, os.O_RDONLY)
        os.close(descriptor)
        return True
    except OSError as error:
        if error.errno in (errno.ENOENT, errno.EACCES, errno.EPERM, errno.ENOTDIR):
            return False
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--result-parent", required=True, type=Path)
    parser.add_argument("--blocked-paths", required=True)
    args = parser.parse_args()
    with zipfile.ZipFile(args.packet) as archive:
        names = archive.namelist()
        shape_ok = len(names) == 2 and set(names) == {"task.txt", "job.json"}
        job = json.loads(archive.read("job.json"))
        task = archive.read("task.txt")
        own_task_ok = bool(task) and hashlib.sha256(task).hexdigest() == job["task_sha256"]
        del task, job
    denials = {label: not readable(path)
               for label, path in json.loads(args.blocked_paths).items()}
    status = dict(line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines()
                  if ":" in line)
    # A reserved TEST-NET address proves no route without contacting a provider.
    no_ipv4_routes = len(Path("/proc/net/route").read_text().splitlines()) == 1
    with socket.socket() as connection:
        connection.settimeout(1)
        network_errno = connection.connect_ex(("192.0.2.1", 443))
    root_read_only = any(
        row.split()[1] == "/" and "ro" in row.split()[3].split(",")
        for row in Path("/proc/mounts").read_text().splitlines())
    checks = {
        "non_root": os.getuid() != 0 and os.geteuid() != 0,
        "all_capabilities_dropped": int(status["CapEff"].strip(), 16) == 0,
        "no_new_privileges": status["NoNewPrivs"].strip() == "1",
        "network_none_no_routes_and_enetunreach": no_ipv4_routes and network_errno == errno.ENETUNREACH,
        "root_filesystem_read_only": root_read_only,
        "provider_key_not_in_environment": "OPENAI_API_KEY" not in os.environ,
        "single_packet_mount": sorted(os.listdir("/job")) == ["packet.zip"],
        "exactly_one_task_and_job": shape_ok,
        "own_task_read_and_digest_verified": own_task_ok,
    }
    checks.update(denials)
    outcome = {"status": "PASS" if all(checks.values()) else "BOUNDARY_FAILURE",
               "checks": checks, "provider_calls": 0,
               "uid_evidence": {"uid": os.getuid(), "euid": os.geteuid()},
               "network_evidence": {"no_ipv4_routes": no_ipv4_routes,
                                    "reserved_test_address_connect_errno": network_errno}}
    print(json.dumps(outcome, sort_keys=True))
    return 0 if all(checks.values()) else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        print(json.dumps({"status": "PROBE_ERROR", "provider_calls": 0}))
        raise SystemExit(2) from None
