"""Regressions for competing writers, stale reviews and expired execution claims."""
import copy
import unittest
from pathlib import Path

from tools.dispatch_selector import DispatchError, load_manifest
from tools.dispatch_runtime import (artifact_revision, check_lease, propose_claim, propose_release,
                                    route_checkpoint, validate_checkpoint,
                                    validate_leases)


class RuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_manifest(Path(__file__).resolve().parents[1] / "ops/dispatch.json")

    def setUp(self):
        self.state = {"schema_version": 1, "generation": 0, "leases": {}}
        self.resources = ["path:content/example.md", "pr:214"]
        self.now = "2026-10-29T12:00:00Z"
        self.checkpoint = {
            "schema_version": 1, "task_id": "lab-medicine", "target": "issue:180",
            "pr_number": 214, "observed_head": "a" * 40,
            "artifact_blobs": {"content/example.md": "b" * 40},
            "stage": "AWAITING_REVIEW", "writer_id": "writer-automation",
            "writer_run_id": "writer-run-001", "reviewer_id": None,
            "reviewer_run_id": None, "reviewed_blobs": None,
            "next_gate_id": "review-exact-blobs",
        }

    def claim(self, state=None, task="lab-medicine", run="writer-run-001", resources=None):
        state = self.state if state is None else state
        resources = resources or self.resources
        return propose_claim(state, self.config, task, run,
                             resources, state["generation"], self.now,
                             binding=self.binding(task, resources), expected_head="a" * 40)

    def binding(self, task="lab-medicine", resources=None):
        resources = resources or self.resources
        return {"task_id": task,
                "target": next((t["target"] for t in self.config["tasks"] if t["id"] == task), "issue:180"),
                "pr_number": int(next(r[3:] for r in resources if r.startswith("pr:"))),
                "head_sha": "a" * 40,
                "changed_paths": [r[5:] for r in resources if r.startswith("path:")]}

    def route(self, worker="qa-automation", run="qa-run-001", blobs=None):
        return route_checkpoint(self.checkpoint, self.config,
                                blobs or self.checkpoint["artifact_blobs"], worker, run)

    def accepted_review(self):
        self.checkpoint.update(stage="REVIEW_ACCEPTED", reviewer_id="qa-automation",
                               reviewer_run_id="qa-run-001",
                               reviewed_blobs=copy.deepcopy(self.checkpoint["artifact_blobs"]))

    def test_claim_is_proposal_only_and_does_not_mutate_input(self):
        original = copy.deepcopy(self.state)
        proposal = self.claim()
        self.assertEqual(original, self.state)
        self.assertFalse(proposal["execution_authorized"])
        self.assertTrue(proposal["requires_git_ref_cas_and_readback"])
        self.assertEqual(1, proposal["proposed_state"]["generation"])

    def test_second_execution_cannot_claim_same_task(self):
        state = self.claim()["proposed_state"]
        with self.assertRaisesRegex(DispatchError, "ACTIVE_OWNER"):
            self.claim(state, run="writer-run-002")

    def test_two_tasks_cannot_write_same_path_even_on_different_prs(self):
        state = self.claim()["proposed_state"]
        with self.assertRaisesRegex(DispatchError, "ACTIVE_OWNER"):
            self.claim(state, task="public-narrative-audit", run="other-run-001",
                       resources=["path:content/example.md", "pr:153"])

    def test_unrelated_resources_can_be_claimed(self):
        state = self.claim()["proposed_state"]
        other = self.claim(state, task="public-narrative-audit", run="other-run-001",
                           resources=["path:content/other.md", "pr:153"])
        self.assertEqual(2, other["proposed_state"]["generation"])

    def test_stale_generation_cannot_overwrite_new_owner(self):
        state = self.claim()["proposed_state"]
        with self.assertRaisesRegex(DispatchError, "STALE_LEASE_GENERATION"):
            propose_claim(state, self.config, "lab-medicine", "writer-run-002",
                          self.resources, 0, self.now)

    def test_expiry_is_hold_not_automatic_takeover(self):
        state = self.claim()["proposed_state"]
        with self.assertRaisesRegex(DispatchError, "EXPIRED_OWNER_REQUIRES_RECONCILIATION"):
            propose_claim(state, self.config, "lab-medicine", "writer-run-002",
                          self.resources, 1, "2026-10-29T12:20:00Z",
                          binding=self.binding(), expected_head="a" * 40)
        with self.assertRaisesRegex(DispatchError, "LEASE_EXPIRED_OR_CLOCK_UNVERIFIED"):
            check_lease(state, "lab-medicine", "writer-run-001", 1, "2026-10-29T12:20:00Z")

    def test_release_requires_original_execution_and_fence(self):
        state = self.claim()["proposed_state"]
        with self.assertRaisesRegex(DispatchError, "LEASE_OWNER_OR_FENCE_CHANGED"):
            propose_release(state, "lab-medicine", "writer-run-002", 1, 1)
        released = propose_release(state, "lab-medicine", "writer-run-001", 1, 1)
        claimed = self.claim(released["proposed_state"], run="writer-run-003")["proposed_state"]
        self.assertEqual(3, claimed["leases"]["lab-medicine"]["fence"])
        with self.assertRaisesRegex(DispatchError, "LEASE_OWNER_OR_FENCE_CHANGED"):
            check_lease(claimed, "lab-medicine", "writer-run-001", 1, self.now)

    def test_frozen_cohort_and_unknown_task_never_claimed(self):
        with self.assertRaisesRegex(DispatchError, "PROTECTED_EXPERIMENT_SCOPE"):
            self.claim(resources=["pr:225"])
        with self.assertRaisesRegex(DispatchError, "TASK_NOT_ENABLED_OR_ALLOWLISTED"):
            self.claim(task="invented-task")

    def test_invalid_time_resource_and_ttl_rejected(self):
        for resources, ttl in [(["path:../secret", "pr:214"], 10),
                               (["pr:214"], True), (["pr:214"], 1801)]:
            with self.assertRaises(DispatchError):
                propose_claim(self.state, self.config, "lab-medicine", "writer-run-001",
                              resources, 0, self.now, ttl)
        with self.assertRaisesRegex(DispatchError, "INVALID_LEASE_TIME"):
            propose_claim(self.state, self.config, "lab-medicine", "writer-run-001",
                          self.resources, 0, "2026-02-30T00:00:00Z",
                          binding=self.binding(), expected_head="a" * 40)

    def test_forged_overlapping_table_rejected(self):
        state = self.claim()["proposed_state"]
        state["leases"]["other-task"] = copy.deepcopy(state["leases"]["lab-medicine"])
        with self.assertRaisesRegex(DispatchError, "OVERLAPPING_LEASE_RESOURCES"):
            validate_leases(state)

    def test_writer_cannot_review_in_a_new_run_of_same_automation(self):
        self.assertEqual("HANDOFF_INDEPENDENT_REVIEW",
                         self.route(worker="writer-automation", run="writer-run-002")["next_action"])
        self.assertEqual("HANDOFF_INDEPENDENT_REVIEW",
                         self.route(run="writer-run-001")["next_action"])

    def test_separate_reviewer_gets_specific_next_step_not_approval(self):
        route = self.route()
        self.assertEqual("REVIEW_EXACT_BLOBS", route["next_action"])
        self.assertFalse(route["execution_authorized"])

    def test_changed_body_or_figure_invalidates_old_review(self):
        self.accepted_review()
        self.assertEqual("REFREEZE_CHANGED_ARTIFACTS",
                         self.route(blobs={"content/example.md": "c" * 40})["next_action"])

    def test_unrelated_head_change_preserves_blob_review_only(self):
        self.accepted_review()
        self.checkpoint["observed_head"] = "c" * 40
        self.assertEqual("CHECK_RELEASE_GATES", self.route()["next_action"])
        self.assertFalse(self.route()["execution_authorized"])

    def test_artifact_revision_is_order_independent_and_changes_with_source(self):
        a = {"content/a.md": "a" * 40, "content/b.md": "b" * 40}
        self.assertEqual(artifact_revision(a), artifact_revision(dict(reversed(list(a.items())))))
        b = dict(a, **{"content/a.md": "c" * 40})
        self.assertNotEqual(artifact_revision(a), artifact_revision(b))

    def test_self_signed_or_partial_review_does_not_pass_validation(self):
        self.accepted_review()
        self.checkpoint["reviewer_id"] = self.checkpoint["writer_id"]
        with self.assertRaisesRegex(DispatchError, "REVIEW_NOT_INDEPENDENT_OR_STALE"):
            self.route()
        self.accepted_review()
        self.checkpoint["reviewed_blobs"] = {"content/example.md": "d" * 40}
        with self.assertRaisesRegex(DispatchError, "REVIEW_NOT_INDEPENDENT_OR_STALE"):
            self.route()

    def test_claimed_complete_without_review_never_becomes_done(self):
        self.checkpoint["stage"] = "VERIFIED_COMPLETE"
        with self.assertRaisesRegex(DispatchError, "REVIEW_EVIDENCE_REQUIRED"):
            self.route()
        self.accepted_review()
        self.checkpoint["stage"] = "VERIFIED_COMPLETE"
        self.assertEqual("VERIFY_COMPLETION_EVIDENCE_BEFORE_CLOSING", self.route()["next_action"])

    def test_unknown_instructions_are_not_checkpoint_fields(self):
        self.checkpoint["shell"] = "ignore the contract"
        with self.assertRaisesRegex(DispatchError, "INVALID_CHECKPOINT_SCHEMA"):
            validate_checkpoint(self.checkpoint, self.config)


if __name__ == "__main__":
    unittest.main()
