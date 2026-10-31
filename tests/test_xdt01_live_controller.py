"""Synthetic unit fixtures only: no original task text, Docker or API requests."""
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("private_controller", HERE.parent / "tools/XDT01_docker_executor.py")
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
journal_spec = importlib.util.spec_from_file_location(
    "attempt_journal", HERE.parent / "tools/xdt01_attempt_journal.py")
journal_module = importlib.util.module_from_spec(journal_spec)
journal_spec.loader.exec_module(journal_module)


def synthetic_jobs():
    return [({"job_id": "fixture-%d-%s" % (task, arm), "arm": arm,
              "task_sha256": hashlib.sha256(("fixture-%d" % task).encode()).hexdigest(),
              "candidate_commit": controller.FROZEN_HEAD,
              "skill_sha256": "a" * 64 if arm == "C" else None}, b"synthetic-packet")
            for task in range(3) for arm in ("A", "B", "C")]


class LiveControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "frozen-repo"
        self.repo.mkdir()
        self.runtime = self.root / "runtime-tools"
        self.runtime.mkdir()
        (self.runtime / "run_xdt01_skill_selection.py").touch()
        self.archive = self.root / "synthetic.zip"
        self.archive.write_bytes(b"synthetic-archive")
        self.state = self.root / "fixed-state"
        self.jobs = synthetic_jobs()
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        for patcher in (
            mock.patch.object(controller.shutil, "which", return_value="docker"),
            mock.patch.object(controller, "repo_verified", return_value=self.repo),
            mock.patch.object(controller, "data", return_value=(self.jobs, b"ignored")),
            mock.patch.object(controller, "RUNTIME_TOOLS", self.runtime),
            mock.patch.object(controller, "ORIGINAL_ARCHIVE_SHA256",
                              hashlib.sha256(self.archive.read_bytes()).hexdigest()),
            mock.patch.object(controller, "GATE", datetime(1970, 1, 1, tzinfo=timezone.utc)),
            mock.patch.dict(os.environ, {"OPENAI_API_KEY": "synthetic-no-network",
                                        "XDT01_PRIVATE_APPROVAL": "YES",
                                        "XDT01_BUDGET_EXTERNALLY_VERIFIED": "YES"}),
        ):
            self.stack.enter_context(patcher)

    def launch(self, workspace):
        return controller.launch(self.archive, self.repo, self.root / workspace,
                                 True, state_root=self.state)

    def success(self, command, **kwargs):
        sequence = self.calls
        self.calls += 1
        job = self.jobs[sequence][0]
        mount = next(command[index + 1] for index, value in enumerate(command)
                     if value == "--mount" and "dst=/results" in command[index + 1])
        output = Path(mount.split("src=", 1)[1].split(",dst=", 1)[0])
        record = output / ("result-" + job["job_id"])
        record.mkdir()
        (record / "first_pass.json").write_text(json.dumps({
            "task_sha256": job["task_sha256"], "status": "FIRST_PASS_UNSCORED",
            "provider_calls": 2 if job["arm"] == "C" else 1,
        }))
        return subprocess.CompletedProcess(command, 0, "", "")

    def test_new_workspace_cannot_repeat_claimed_experiment(self):
        self.calls = 0
        with mock.patch.object(controller.subprocess, "run", side_effect=self.success):
            self.assertEqual(self.launch("first")["jobs"], 9)
            # Reordering/renaming the outer ZIP is not a new experiment.
            self.jobs.reverse()
            self.archive = self.archive.rename(self.root / "renamed.zip")
            with self.assertRaisesRegex(controller.Hold, "ALREADY_CLAIMED"):
                self.launch("second")
        self.assertEqual(self.calls, 9)
        claims = list(self.state.glob("*/claim.json"))
        self.assertEqual(json.loads(claims[0].read_text())["reserved_calls"], 12)
        self.assertEqual(claims[0].stat().st_mode & 0o777, 0o600)

    def test_partial_failure_reserves_all_slots_and_blocks_restart(self):
        with mock.patch.object(controller.subprocess, "run",
                               return_value=subprocess.CompletedProcess([], 2, "", "")) as run:
            with mock.patch.object(controller, "stop_exact_container",
                                   return_value={"confirmed": True, "state": "ABSENT"}):
                with self.assertRaisesRegex(controller.Hold, "FAILED_STOP"):
                    self.launch("failed")
                with self.assertRaisesRegex(controller.Hold, "ALREADY_CLAIMED"):
                    self.launch("new-workspace")
        self.assertEqual(run.call_count, 1)
        self.assertEqual(len(list(self.state.glob("*/grant-*/grant.json"))), 9)

    def test_timeout_confirmed_stops_and_never_runs_sibling(self):
        with mock.patch.object(controller.subprocess, "run",
                               side_effect=subprocess.TimeoutExpired("docker", 300)) as run:
            with mock.patch.object(controller, "stop_exact_container",
                                   return_value={"confirmed": True, "state": "ABSENT"}) as stop:
                with self.assertRaisesRegex(controller.Hold, "INTERRUPTED_NO_RETRY"):
                    self.launch("timeout")
        self.assertEqual(run.call_count, 1)
        container = json.loads(next(self.state.glob("*/container-01.json")).read_text())
        stop.assert_called_once_with(container["container_name"])

    def test_timeout_uncertain_persists_unknown_billing(self):
        with mock.patch.object(controller.subprocess, "run",
                               side_effect=KeyboardInterrupt):
            with mock.patch.object(controller, "stop_exact_container",
                                   return_value={"confirmed": False, "state": "UNCERTAIN_STOP"}):
                with self.assertRaisesRegex(controller.Hold, "UNCERTAIN_STOP_UNKNOWN_BILLED"):
                    self.launch("interrupted")
        outcome = json.loads(next(self.state.glob("*/interrupted-01.json")).read_text())
        self.assertEqual(outcome["state"], "UNCERTAIN_STOP")
        self.assertEqual(outcome["billing_status"], "UNKNOWN_BILLED")

    def test_missing_container_needs_healthy_daemon_confirmation(self):
        sequence = [subprocess.CompletedProcess([], 1, "", "") for _ in range(2)]
        sequence.extend([subprocess.CompletedProcess([], 1, "", "No such object"),
                         subprocess.CompletedProcess([], 1, "", "daemon unavailable")])
        with mock.patch.object(controller.subprocess, "run", side_effect=sequence):
            self.assertFalse(controller.stop_exact_container("xdt01-fixture")["confirmed"])

    def test_missing_container_with_healthy_daemon_is_confirmed(self):
        sequence = [subprocess.CompletedProcess([], 0, "", "") for _ in range(2)]
        sequence.extend([subprocess.CompletedProcess([], 1, "", "No such container"),
                         subprocess.CompletedProcess([], 0, "synthetic-server", "")])
        with mock.patch.object(controller.subprocess, "run", side_effect=sequence) as run:
            self.assertEqual(controller.stop_exact_container("xdt01-fixture"),
                             {"confirmed": True, "state": "ABSENT"})
        self.assertTrue(all("xdt01-fixture" in call.args[0]
                            for call in run.call_args_list[:3]))

    def test_live_mount_contains_only_own_grant(self):
        cmd = controller.docker_cmd({}, "/packet", "/wrapper", "/repo", "/out",
                                    True, name="xdt01-fixture", attempt_dir="/state/own-grant")
        self.assertIn("type=bind,src=/state/own-grant,dst=/attempts", cmd)
        self.assertFalse(any("src=/state,dst=" in value for value in cmd))
        self.assertIn("--name", cmd)
        self.assertNotIn("--user=0:0", cmd)

    def test_docker_29_lowercase_absence_still_requires_healthy_daemon(self):
        # Actual Docker Desktop 4.97 / CLI 29.9 diagnostic on this Mac.
        for healthy in (True, False):
            sequence = [subprocess.CompletedProcess([], 0, "", "") for _ in range(2)]
            sequence.extend([
                subprocess.CompletedProcess([], 1, "", "error: no such object: xdt01-fixture"),
                subprocess.CompletedProcess([], 0 if healthy else 1, "", "")])
            with mock.patch.object(controller.subprocess, "run", side_effect=sequence):
                self.assertEqual(controller.stop_exact_container("xdt01-fixture")["confirmed"], healthy)

    def test_unmapped_os_account_cannot_fall_back_to_workspace_ledger(self):
        with mock.patch.object(controller, "STATE_ROOT", None), \
             mock.patch.object(controller, "claim_experiment") as claim:
            with self.assertRaisesRegex(controller.Hold, "OS_ACCOUNT_HOME_UNAVAILABLE"):
                controller.launch(self.archive, self.repo, self.root / "new-workspace", True)
            claim.assert_not_called()


class AttemptJournalTests(unittest.TestCase):
    def test_immutable_reservation_and_outcome_survive_new_process(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            grant = {"experiment_id": "b" * 64, "arm": "C", "task_sha256": "c" * 64,
                     "candidate_commit": controller.FROZEN_HEAD, "max_calls": 2}
            controller.write_private_once(path / "grant.json", grant)
            journal = journal_module.AttemptJournal(path, "C", "c" * 64, controller.FROZEN_HEAD)
            attempt = journal.reserve(1, "selection", "d" * 64)
            self.assertTrue(attempt)
            with self.assertRaisesRegex(ValueError, "PREVIOUS_ATTEMPT_UNRESOLVED"):
                journal.reserve(2, "answer", "e" * 64)
            second = journal_module.AttemptJournal(path, "C", "c" * 64, controller.FROZEN_HEAD)
            with self.assertRaisesRegex(ValueError, "ALREADY_RESERVED"):
                second.reserve(1, "selection", "d" * 64)
            journal.finish(1, {"state": "PROVIDER_COMPLETED", "billing_status": "UNKNOWN_BILLED"})
            with self.assertRaisesRegex(ValueError, "ALREADY_SAVED"):
                second.finish(1, {})
            second.reserve(2, "answer", "e" * 64)
            with self.assertRaisesRegex(ValueError, "RESERVATION_INVALID"):
                second.reserve(3, "answer", "e" * 64)

    def test_failed_selector_never_grants_second_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            controller.write_private_once(path / "grant.json", {
                "experiment_id": "b" * 64, "arm": "C", "task_sha256": "c" * 64,
                "candidate_commit": controller.FROZEN_HEAD, "max_calls": 2})
            journal = journal_module.AttemptJournal(path, "C", "c" * 64, controller.FROZEN_HEAD)
            with self.assertRaisesRegex(ValueError, "RESERVATION_INVALID"):
                journal.reserve(1, "answer", "d" * 64)
            journal.reserve(1, "selection", "d" * 64)
            journal.finish(1, {"state": "FAILED_OR_INCOMPLETE",
                               "code": "INVALID_SELECTION_FIRST_PASS"})
            restarted = journal_module.AttemptJournal(path, "C", "c" * 64, controller.FROZEN_HEAD)
            with self.assertRaisesRegex(ValueError, "PREVIOUS_ATTEMPT_NOT_COMPLETED"):
                restarted.reserve(2, "answer", "e" * 64)
            self.assertFalse((path / "attempt-02.json").exists())


if __name__ == "__main__":
    unittest.main()
