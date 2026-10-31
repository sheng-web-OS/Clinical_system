"""Private, immutable per-job provider-attempt reservations.

A reservation without an outcome means UNKNOWN_BILLED and is never reusable.
The operator grants only this job's directory to its worker container.
"""
import json
import os
from pathlib import Path
import re
import uuid
from datetime import datetime, timezone


def _write_once(path, value):
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, ensure_ascii=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


class AttemptJournal:
    def __init__(self, directory, arm, task_sha256, candidate_commit):
        self.directory = Path(directory)
        if not self.directory.is_dir() or self.directory.is_symlink():
            raise ValueError("ATTEMPT_DIRECTORY_INVALID")
        grant_path = self.directory / "grant.json"
        if grant_path.is_symlink():
            raise ValueError("ATTEMPT_GRANT_INVALID")
        self.grant = json.loads(grant_path.read_text(encoding="utf-8"))
        if (arm not in {"A", "B", "C"} or
                self.grant.get("arm") != arm or
                self.grant.get("task_sha256") != task_sha256 or
                self.grant.get("candidate_commit") != candidate_commit or
                self.grant.get("max_calls") != (2 if arm == "C" else 1) or
                not re.fullmatch(r"[0-9a-f]{64}",
                                 self.grant.get("experiment_id", ""))):
            raise ValueError("ATTEMPT_GRANT_MISMATCH")
        self.arm = arm

    def reserve(self, call_index, kind, request_sha256):
        expected_kind = ("selection" if self.arm == "C" and call_index == 1
                         else "answer")
        if (type(call_index) is not int or
                not 1 <= call_index <= self.grant["max_calls"] or
                kind != expected_kind or
                not isinstance(request_sha256, str) or
                not re.fullmatch(r"[0-9a-f]{64}", request_sha256)):
            raise ValueError("ATTEMPT_RESERVATION_INVALID")
        if call_index > 1:
            previous_path = self.directory / "outcome-01.json"
            if not previous_path.is_file() or previous_path.is_symlink():
                raise ValueError("PREVIOUS_ATTEMPT_UNRESOLVED")
            previous = json.loads(previous_path.read_text(encoding="utf-8"))
            if previous.get("evidence", {}).get("state") != "PROVIDER_COMPLETED":
                raise ValueError("PREVIOUS_ATTEMPT_NOT_COMPLETED")
        attempt_id = uuid.uuid4().hex
        try:
            _write_once(self.directory / ("attempt-%02d.json" % call_index), {
                "attempt_id": attempt_id,
                "experiment_id": self.grant["experiment_id"],
                "call_index": call_index, "kind": kind,
                "request_sha256": request_sha256,
                "reserved_at_utc": datetime.now(timezone.utc).isoformat(),
                "billing_status": "UNKNOWN_BILLED",
            })
        except FileExistsError:
            raise ValueError("ATTEMPT_SLOT_ALREADY_RESERVED") from None
        return attempt_id

    def finish(self, call_index, evidence):
        if type(call_index) is not int or not isinstance(evidence, dict):
            raise ValueError("ATTEMPT_OUTCOME_INVALID")
        if not 1 <= call_index <= self.grant["max_calls"]:
            raise ValueError("ATTEMPT_OUTCOME_INVALID")
        attempt_path = self.directory / ("attempt-%02d.json" % call_index)
        if attempt_path.is_symlink():
            raise ValueError("ATTEMPT_RESERVATION_INVALID")
        attempt = json.loads(attempt_path.read_text(encoding="utf-8"))
        try:
            _write_once(self.directory / ("outcome-%02d.json" % call_index), {
                "attempt_id": attempt["attempt_id"],
                "experiment_id": self.grant["experiment_id"],
                "call_index": call_index, "evidence": evidence,
                "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            })
        except FileExistsError:
            raise ValueError("ATTEMPT_OUTCOME_ALREADY_SAVED") from None
