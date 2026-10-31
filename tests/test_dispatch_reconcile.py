"""Shadow reconciliation contract tests: no API/models/writes/medical data."""
import copy
import json
import unittest
from pathlib import Path

from tools.dispatch_selector import DispatchError, load_manifest
from tools.dispatch_reconcile import gate_fingerprint, reconcile


class ReconciliationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_manifest(
            Path(__file__).resolve().parents[1] / "ops" / "dispatch.json")

    def setUp(self):
        self.issues = {
            t["target"]: {"number": int(t["target"].split(":")[1]),
                          "state": "open", "is_pr": False}
            for t in self.config["tasks"]
        }
        self.gates = {
            t["target"]: {
                "issue_number": int(t["target"].split(":")[1]),
                "gate_id": "verify-original-gate",
                "evidence_revision": "sha:" + "a" * 40,
                "gate_state": "actionable",
                "owner": "unclaimed",
                "last_receipt": None,
            }
            for t in self.config["tasks"]
        }

    def plan(self):
        return reconcile(self.config, self.issues, self.gates)

    def receipt(self, target="issue:76", status="CONTINUING",
                next_gate_id="write-next-gate"):
        gate = self.gates[target]
        return {
            "gate_id": gate["gate_id"],
            "fingerprint": gate_fingerprint(
                target, gate["gate_id"], gate["evidence_revision"]),
            "status": status, "next_gate_id": next_gate_id,
        }

    def test_baseline_shadow_is_not_execution_authorization(self):
        r = self.plan()
        self.assertEqual("SHADOW_RECONCILED_NO_ACTION", r["status"])
        self.assertFalse(r["execution_authorized"])
        self.assertTrue(r["requires_live_source_verification"])
        self.assertEqual(0, r["model_calls"])
        self.assertEqual(0, r["write_actions"])
        self.assertEqual("ecg-original-evidence", r["selected"][0]["id"])

    def test_unchanged_gate_skips_duplicate_even_if_issue_open(self):
        self.gates["issue:76"]["last_receipt"] = self.receipt()
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])
        self.assertIn({"id": "ecg-original-evidence",
                       "reason": "DUPLICATE_UNCHANGED_GATE"}, r["skipped"])

    def test_completed_receipt_does_not_retrigger(self):
        self.gates["issue:76"]["last_receipt"] = self.receipt(
            status="VERIFIED_COMPLETE", next_gate_id=None)
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])
        self.assertIn({"id": "ecg-original-evidence",
                       "reason": "ALREADY_VERIFIED"}, r["skipped"])

    def test_unblocked_new_pr_revision_makes_gate_eligible_again(self):
        self.gates["issue:76"]["last_receipt"] = self.receipt()
        self.gates["issue:76"]["evidence_revision"] = "sha:" + "b" * 40
        r = self.plan()
        self.assertEqual("ecg-original-evidence", r["selected"][0]["id"])
        self.assertEqual("NEW_GATE", r["selected"][0]["decision"])

    def test_task_local_artifact_revision_avoids_unrelated_head_rework(self):
        self.gates["issue:76"]["evidence_revision"] = "artifacts:" + "a" * 64
        self.gates["issue:76"]["last_receipt"] = self.receipt()
        self.assertEqual("mobile-figure-p0", self.plan()["selected"][0]["id"])

    def test_resume_requires_distinct_next_gate_from_receipt(self):
        self.gates["issue:76"]["last_receipt"] = self.receipt(
            next_gate_id="write-next-gate")
        self.gates["issue:76"]["gate_id"] = "write-next-gate"
        r = self.plan()
        self.assertEqual("ecg-original-evidence", r["selected"][0]["id"])
        self.assertEqual("RESUME_NEXT_GATE", r["selected"][0]["decision"])
        self.assertFalse(r["execution_authorized"])

    def test_active_other_worker_prevents_conflicting_claim(self):
        self.gates["issue:76"]["owner"] = "other_worker"
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])
        self.assertIn({"id": "ecg-original-evidence",
                       "reason": "ACTIVE_OTHER_OWNER"}, r["skipped"])

    def test_waiting_approval_complete_are_not_actionable(self):
        self.gates["issue:76"]["gate_state"] = "waiting"
        self.gates["issue:79"]["gate_state"] = "approval_needed"
        self.gates["issue:152"]["gate_state"] = "complete"
        r = self.plan()
        self.assertEqual("lab-medicine", r["selected"][0]["id"])
        reasons = {i["reason"] for i in r["skipped"]}
        self.assertTrue({"WAITING_NO_NEW_GATE", "APPROVAL_NEEDED",
                         "GATE_COMPLETE"}.issubset(reasons))

    def test_all_gates_waiting_returns_empty_not_false_complete(self):
        for gate in self.gates.values():
            gate["gate_state"] = "waiting"
        r = self.plan()
        self.assertEqual([], r["selected"])
        self.assertEqual(0, r["eligible_count"])
        self.assertEqual("SHADOW_RECONCILED_NO_ACTION", r["status"])

    def test_missing_gate_holds_only_affected_task(self):
        del self.gates["issue:76"]
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])
        self.assertEqual([{"id": "ecg-original-evidence",
                           "reason": "GATE_SNAPSHOT_MISSING"}], r["blocked"])
        self.assertFalse(r["all_tasks_observed"])
        self.assertFalse(r["execution_authorized"])

    def test_missing_issue_does_not_starve_other_tasks(self):
        del self.issues["issue:76"]
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])
        self.assertEqual("SOURCE_METADATA_MISSING_OR_INVALID", r["blocked"][0]["reason"])

    def test_all_unavailable_is_hold_not_empty_success(self):
        self.gates.clear()
        r = self.plan()
        self.assertEqual("HOLD_TASKS_BLOCKED", r["status"])
        self.assertEqual([], r["selected"])
        self.assertEqual(7, len(r["blocked"]))

    def test_global_shape_and_foreign_target_stop_whole_plan(self):
        with self.assertRaisesRegex(DispatchError, "INVALID_ISSUE_SNAPSHOT"):
            reconcile(self.config, None, self.gates)
        with self.assertRaisesRegex(DispatchError, "GATE_SNAPSHOT_MISSING"):
            reconcile(self.config, self.issues, None)
        self.gates["issue:137"] = copy.deepcopy(self.gates["issue:76"])
        with self.assertRaisesRegex(DispatchError, "UNEXPECTED_GATE_TARGET"):
            self.plan()

    def test_bad_receipt_cannot_fake_history(self):
        self.gates["issue:76"]["last_receipt"] = self.receipt()
        self.gates["issue:76"]["last_receipt"]["status"] = "AUTO_APPROVED"
        r = self.plan()
        self.assertEqual("INVALID_RECEIPT_VALUES", r["blocked"][0]["reason"])
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])

    def test_current_gate_receipt_cannot_claim_another_gate(self):
        # Even if a fingerprint matches the active gate, the receipt must
        # actually name that gate before it can suppress any scheduled work.
        # A historical CONTINUING receipt for a *different* fingerprint
        # remains valid for legitimate next-gate resumes (tested above).
        for status, next_gate_id in (
                ("VERIFIED_COMPLETE", None),
                ("CONTINUING", "write-next-gate")):
            with self.subTest(status=status):
                self.setUp()
                receipt = self.receipt(status=status,
                                       next_gate_id=next_gate_id)
                receipt["gate_id"] = "unrelated-gate"
                self.gates["issue:76"]["last_receipt"] = receipt
                r = self.plan()
                self.assertIn(
                    {"id": "ecg-original-evidence",
                     "reason": "INVALID_RECEIPT_VALUES"}, r["blocked"])
                self.assertEqual("mobile-figure-p0",
                                 r["selected"][0]["id"])
                self.assertNotIn("ALREADY_VERIFIED",
                                 [i["reason"] for i in r["skipped"]])
                self.assertFalse(r["execution_authorized"])

    def test_mismatched_issue_gate_fails_closed(self):
        self.gates["issue:76"]["issue_number"] = 137
        self.assertEqual("GATE_TARGET_MISMATCH", self.plan()["blocked"][0]["reason"])

    def test_unverified_evidence_and_arbitrary_field_rejected(self):
        self.gates["issue:76"]["evidence_revision"] = "I said so"
        self.assertEqual("INVALID_EVIDENCE_REVISION", self.plan()["blocked"][0]["reason"])
        self.gates["issue:76"]["evidence_revision"] = "sha:" + "a" * 40
        self.gates["issue:76"]["shell"] = "run arbitrary code"
        self.assertEqual("INVALID_GATE_SCHEMA", self.plan()["blocked"][0]["reason"])

    def test_closed_issue_not_reactivated_by_gate(self):
        self.issues["issue:76"]["state"] = "closed"
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])

    def test_duplicate_same_step_cannot_be_called_resume(self):
        self.gates["issue:76"]["last_receipt"] = self.receipt(
            next_gate_id="verify-original-gate")
        r = self.plan()
        self.assertEqual("mobile-figure-p0", r["selected"][0]["id"])
        self.assertNotEqual("RESUME_NEXT_GATE", r["selected"][0]["decision"])


    def test_resumes_non_p0_before_starting_another_non_p0(self):
        # P0 gates are waiting; a verified next step on a real article should
        # outrank a newly-started high-priority non-P0 audit.
        for target in ("issue:76", "issue:79"):
            self.gates[target]["gate_state"] = "waiting"
        self.gates["issue:180"]["last_receipt"] = self.receipt("issue:180")
        self.gates["issue:180"]["gate_id"] = "write-next-gate"
        result = self.plan()
        self.assertEqual("lab-medicine", result["selected"][0]["id"])
        self.assertEqual("RESUME_NEXT_GATE", result["selected"][0]["decision"])
        self.assertNotIn("public-narrative-audit",
                         [i["id"] for i in result["skipped"]])
        self.assertFalse(result["execution_authorized"])

    def test_resumed_non_p0_never_preempts_actionable_p0(self):
        self.gates["issue:180"]["last_receipt"] = self.receipt("issue:180")
        self.gates["issue:180"]["gate_id"] = "write-next-gate"
        result = self.plan()
        self.assertEqual("ecg-original-evidence", result["selected"][0]["id"])

    def test_two_continuations_keep_original_relative_priority(self):
        for target in ("issue:76", "issue:79"):
            self.gates[target]["gate_state"] = "waiting"
        for target in ("issue:152", "issue:180"):
            self.gates[target]["last_receipt"] = self.receipt(target)
            self.gates[target]["gate_id"] = "write-next-gate"
        result = self.plan()
        self.assertEqual("public-narrative-audit", result["selected"][0]["id"])
        self.assertEqual("RESUME_NEXT_GATE", result["selected"][0]["decision"])


if __name__ == "__main__":
    unittest.main()
