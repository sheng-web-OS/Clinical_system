"""S02: adversarial regression tests. All event-causality verdicts fail closed."""
import copy
import unittest
from provenance_probe import assess

EVENT_A = "11111111-1111-4111-8111-111111111111"
EVENT_B = "22222222-2222-4222-8222-222222222222"


class EventProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "github": {
                "repository": "sheng-web-OS/Clinical_system",
                "pr_number": 240,
                "head_sha": "76bb875d23bcccc517c3894d305f728a6919d77b",
                "event_action": "synchronize",
                "event_id": None,
            },
            "platform_run": {
                "id": "a7264387-e8ac-8330-882c-3837b5b69807",
                "task_id": "6ae414b458488191a9b14acf2bb3bfdb",
                "recorded_status": "no_update",
                "chat_ref": None,
                "latest_result": None,
            },
        }

    def verify(self, mutate, verdict, finding=None):
        e = copy.deepcopy(self.case)
        mutate(e)
        result = assess(e)
        self.assertEqual(result.verdict, verdict, result)
        if finding:
            self.assertIn(finding, result.findings)

    def test_s01_real_evidence_remains_inconclusive(self):
        self.verify(lambda e: None, "INCONCLUSIVE", "NO_PLATFORM_EVENT_TO_RUN_BINDING")

    def test_event_without_platform_run(self):
        self.verify(lambda e: e.update(platform_run={}), "GITHUB_EVENT_ONLY")

    def test_missing_github_head(self):
        self.verify(lambda e: e["github"].update(head_sha=None), "INSUFFICIENT_GITHUB_EVIDENCE")

    def test_time_coincidence_not_proof(self):
        self.verify(lambda e: e["platform_run"].update(started_at="2026-10-30T04:52:15Z"), "INCONCLUSIVE")

    def test_self_report_not_proof(self):
        self.verify(lambda e: e.update(processing_receipt={
            "run_id": e["platform_run"]["id"], "nonce": "S01", "provenance": "self_report"
        }), "INCONCLUSIVE", "SELF_REPORTED_RECEIPT_NOT_ATTESTATION")

    def test_perfect_structural_binding_still_not_authenticated(self):
        def mutate(e):
            e["github"]["event_id"] = EVENT_A
            e["platform_event_binding"] = {
                "event_id": EVENT_A, "run_id": e["platform_run"]["id"],
                "task_id": e["platform_run"]["task_id"],
                **{k: e["github"][k] for k in ("repository", "pr_number", "head_sha", "event_action")}
            }
        self.verify(mutate, "INCONCLUSIVE", "STRUCTURAL_BINDING_MATCH_NOT_PROVIDER_AUTHENTICATED")

    def test_wrong_head(self):
        self.verify(lambda e: e.update(processing_receipt={"head_sha": "a" * 40}), "CONFLICT")

    def test_wrong_pr(self):
        self.verify(lambda e: e.update(platform_event_binding={"pr_number": 238}), "CONFLICT")

    def test_wrong_run(self):
        self.verify(lambda e: e.update(processing_receipt={"run_id": EVENT_A}), "CONFLICT")

    def test_wrong_task(self):
        self.verify(lambda e: e.update(processing_receipt={"task_id": EVENT_A}), "CONFLICT")

    def test_wrong_delivery_id(self):
        def mutate(e):
            e["github"]["event_id"] = EVENT_A
            e["platform_event_binding"] = {"event_id": EVENT_B}
        self.verify(mutate, "CONFLICT")

    def test_stale_latest_result_with_receipt(self):
        def mutate(e):
            e["platform_run"]["latest_result"] = {"run_id": EVENT_A}
            e["processing_receipt"] = {"provenance": "platform_result", "nonce": "ARM"}
        self.verify(mutate, "CONFLICT", "PLATFORM_LATEST_RESULT_RUN_MISMATCH")

    def test_platform_result_still_not_event_causality(self):
        def mutate(e):
            e["platform_run"]["latest_result"] = {"run_id": e["platform_run"]["id"]}
            e["processing_receipt"] = {"provenance": "platform_result", "nonce": "ARM"}
        self.verify(mutate, "INCONCLUSIVE", "APPLICATION_PROCESSING_CLAIM_ONLY")

    def test_boolean_pr_number_is_not_integer(self):
        self.verify(lambda e: e["github"].update(pr_number=True), "INVALID_EVIDENCE", "INVALID_GITHUB_PR_NUMBER")

    def test_boolean_action_is_not_action_string(self):
        self.verify(lambda e: e["github"].update(event_action=False), "INVALID_EVIDENCE", "INVALID_GITHUB_EVENT_ACTION")

    def test_boolean_run_id_is_not_id(self):
        self.verify(lambda e: e["platform_run"].update(id=True), "INVALID_EVIDENCE", "INVALID_PLATFORM_ID")

    def test_invalid_head_sha(self):
        self.verify(lambda e: e["github"].update(head_sha="fake"), "INVALID_EVIDENCE", "INVALID_GITHUB_HEAD_SHA")

    def test_fake_delivery_id(self):
        self.verify(lambda e: e["github"].update(event_id="fake"), "INVALID_EVIDENCE", "INVALID_GITHUB_DELIVERY_ID")

    def test_claimed_platform_result_without_observation(self):
        self.verify(lambda e: e.update(processing_receipt={
            "provenance": "platform_result", "nonce": "ARM"
        }), "INCONCLUSIVE", "CLAIMED_PLATFORM_RESULT_WITHOUT_OBSERVED_RESULT")

    def test_stale_result_even_without_receipt(self):
        self.verify(lambda e: e["platform_run"].update(latest_result={"run_id": EVENT_A}),
                    "CONFLICT", "PLATFORM_LATEST_RESULT_RUN_MISMATCH")

    def test_fake_chat_ref(self):
        self.verify(lambda e: e["platform_run"].update(chat_ref="not-an-object"), "INVALID_EVIDENCE", "INVALID_CHAT_REF")

    def test_binding_boolean_pr(self):
        self.verify(lambda e: e.update(platform_event_binding={"pr_number": True}),
                    "INVALID_EVIDENCE", "PLATFORM_EVENT_BINDING_INVALID_PR_NUMBER")

    def test_root_must_be_object(self):
        self.assertEqual(assess([]).verdict, "INVALID_EVIDENCE")

    def test_matching_receipt_still_no_platform_causality(self):
        def mutate(e):
            e["processing_receipt"] = {
                "run_id": e["platform_run"]["id"], "task_id": e["platform_run"]["task_id"],
                "provenance": "platform_result", "nonce": "ARM"}
            e["platform_run"]["latest_result"] = {"run_id": e["platform_run"]["id"]}
        self.verify(mutate, "INCONCLUSIVE")


    def test_status_container_is_invalid_not_exception(self):
        for status in ([], {}, ["a"], {"x": 1}):
            with self.subTest(status=status):
                self.verify(lambda e: e["platform_run"].update(recorded_status=status),
                            "INVALID_EVIDENCE", "INVALID_PLATFORM_RUN_STATUS")

    def test_572_malformed_field_mutations_never_raise(self):
        values = (None, False, True, 0, 1, 1.0, "", [], {}, ["a"], {"x": 1}, "NOT_EXPOSED", "abc")
        fields = ("recorded_status", "id", "task_id", "chat_ref", "latest_result",
                  "repository", "pr_number", "event_id", "head_sha", "event_action", "run_id")
        for section in ("github", "platform_run", "processing_receipt", "platform_event_binding"):
            for field in fields:
                for value in values:
                    with self.subTest(section=section, field=field, value=str(value)):
                        e = copy.deepcopy(self.case)
                        e.setdefault(section, {})[field] = value
                        result = assess(e)
                        self.assertNotEqual(result.verdict, "VERIFIED")
                        self.assertNotEqual(result.verdict, "PASS")


if __name__ == "__main__":
    unittest.main()
