"""Adversarial tests for decision-before-retrieval development probe. NO API calls."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from selective_retrieval_probe import (validate_fixture, triage_request, validate_triage,
    retrieve_after_triage, answer_request, run_case, execute, digest, build_plan,
    paired_order, PilotError)

FIXTURE = ROOT / "experiments/skill-transfer/fixtures/selective-retrieval-synthetic.json"
DATA = json.loads(FIXTURE.read_text(encoding="utf-8"))
CASES, DOCS = validate_fixture(DATA)
SKILL = "# Synthetic strategy for mock tests; no case facts"


def response(decision="RETRIEVE", gap="missing_primary_evidence",
             source="synthetic-assay-brief", confidence=45):
    return dict(decision=decision, gap_type=gap, source_id=source,
                evidence_question="Which source evidence discriminates interpretations?",
                decision_pivot="What new datum could change our conclusion?",
                provisional_answer="Tentative explanation; not confirmed",
                confidence_percent=confidence)


def fake(values):
    """Deterministic mock; deliberately not a model success or provider receipt."""
    calls = []
    def caller(req):
        calls.append(req)
        if "text" in req:
            return {"answer": json.dumps(values, ensure_ascii=False),
                    "response_id": "MOCK_NOT_PROVIDER", "returned_model": "mock",
                    "usage": None}
        return {"answer": "mock final answer, NOT CLINICALLY REVIEWED",
                "response_id": "MOCK_NOT_PROVIDER", "returned_model": "mock",
                "usage": None}
    return caller, calls


class SelectiveRetrievalProbeTests(unittest.TestCase):
    def test_fixed_balanced_arm_order_is_frozen_before_execution(self):
        plan = build_plan(DATA, SKILL, "gpt-5-mini", "d" * 40)
        order = plan["paired_execution_order"]
        self.assertEqual(len(order), 9)
        self.assertEqual({row["arm"] for row in order[:1] +
                          order[3:4] + order[6:7]}, set(("native", "retrieval", "skill")))
        self.assertEqual([(case["id"], arm) for case, arm in paired_order(CASES)],
                         [(row["case_id"], row["arm"]) for row in order])

    def test_fixture_is_public_development_only(self):
        self.assertEqual(len(CASES), 3)
        self.assertEqual(len(DOCS), 2)
        self.assertEqual(DATA["exposure"], "development_only_public_exposed")

    def test_triage_never_sees_doc_bodies_even_in_skill_arm(self):
        for arm in ("native", "retrieval", "skill"):
            request = triage_request(CASES[0], arm, DOCS, SKILL, "gpt-5-mini")
            raw = json.dumps(request, ensure_ascii=False)
            for doc in DOCS:
                self.assertNotIn(doc["text"], raw)
            if arm == "native":
                self.assertNotIn("synthetic-assay-brief", raw)
            else:
                self.assertIn("synthetic-assay-brief", raw)

    def test_candidate_catalog_same_between_b_and_c(self):
        b = triage_request(CASES[0], "retrieval", DOCS, SKILL, "gpt-5-mini")
        c = triage_request(CASES[0], "skill", DOCS, SKILL, "gpt-5-mini")
        self.assertIn("synthetic-ventilation-brief", b["instructions"])
        self.assertIn("synthetic-ventilation-brief", c["instructions"])
        self.assertIn(SKILL, c["instructions"])
        self.assertNotIn(SKILL, b["instructions"])

    def test_retrieve_allowed_only_after_explicit_first_decision(self):
        p = response()
        doc, verdict = retrieve_after_triage("retrieval", p, DOCS)
        self.assertEqual(verdict, "SOURCE_RETURNED")
        self.assertEqual(doc["id"], "synthetic-assay-brief")

    def test_do_not_retrieve_on_skip(self):
        caller, calls = fake(response("SKIP", "none", ""))
        out = run_case(CASES[2], "skill", DOCS, SKILL, "gpt-5-mini", caller)
        self.assertEqual(out["retrieval_gate"], "MODEL_SKIP")
        self.assertIsNone(out["retrieved_source_id"])
        self.assertEqual(len(calls), 2)
        self.assertNotIn(DOCS[0]["text"], json.dumps(calls, ensure_ascii=False))

    def test_hold_must_not_create_final_answer_or_read(self):
        caller, calls = fake(response("HOLD", "missing_patient_fact", ""))
        out = run_case(CASES[1], "skill", DOCS, SKILL, "gpt-5-mini", caller)
        self.assertEqual(out["retrieval_gate"], "MODEL_HOLD")
        self.assertIsNone(out["answer"])
        self.assertEqual(len(calls), 1)

    def test_missing_patient_fact_blocks_requested_source(self):
        p = response(gap="missing_patient_fact")
        doc, reason = retrieve_after_triage("skill", p, DOCS)
        self.assertIsNone(doc)
        self.assertEqual(reason, "NON_RETRIEVABLE_GAP")

    def test_none_gap_also_blocks_retrieve(self):
        doc, reason = retrieve_after_triage("skill", response(gap="none"), DOCS)
        self.assertIsNone(doc)
        self.assertEqual(reason, "NON_RETRIEVABLE_GAP")

    def test_missing_or_unallowlisted_id_blocks(self):
        doc, reason = retrieve_after_triage("skill", response(source="raw-patient-chart"), DOCS)
        self.assertIsNone(doc)
        self.assertEqual(reason, "SOURCE_NOT_ALLOWLISTED")

    def test_native_cannot_get_article_body(self):
        doc, reason = retrieve_after_triage("native", response(), DOCS)
        self.assertIsNone(doc)
        self.assertEqual(reason, "ARM_NO_SOURCE_ACCESS")

    def test_only_approved_source_enters_second_request(self):
        caller, calls = fake(response())
        out = run_case(CASES[0], "retrieval", DOCS, SKILL, "gpt-5-mini", caller)
        self.assertEqual(out["retrieved_source_sha256"], digest(DOCS[0]["text"]))
        self.assertEqual(len(calls), 2)
        self.assertNotIn(DOCS[0]["text"], json.dumps(calls[0], ensure_ascii=False))
        self.assertIn(DOCS[0]["text"], json.dumps(calls[1], ensure_ascii=False))
        self.assertNotIn(DOCS[1]["text"], json.dumps(calls[1], ensure_ascii=False))

    def test_structured_bad_values_fail_closed(self):
        for bad in (response(confidence=True), response(confidence=101),
                    response(decision="GO"), response(gap="improve_score"),
                    {**response(), "new_unapproved_key": "x"}):
            with self.subTest(bad=bad):
                with self.assertRaises(PilotError):
                    validate_triage(bad)

    def test_duplicate_and_non_synthetic_fixture_rejected(self):
        bad = dict(DATA, source_class="real_patients")
        with self.assertRaises(PilotError):
            validate_fixture(bad)
        duplicate = dict(DATA, documents=[DOCS[0], DOCS[0]])
        with self.assertRaises(PilotError):
            validate_fixture(duplicate)

    def test_offline_plan_makes_no_calls_and_private_only(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "plan"
            got = execute(DATA, SKILL, "gpt-5-mini", "a" * 40, output)
            self.assertEqual(got["status"], "PLAN_ONLY_NO_MODEL_CALLS")
            state = json.loads((output / "manifest.json").read_text())
            self.assertEqual(state["model_calls_made"], 0)
            self.assertFalse(state["clinical_validated"])
            self.assertFalse(state["transfer_validated"])

    def test_offline_and_injected_run_bind_same_frozen_suite(self):
        caller, _ = fake(response("SKIP", "none", ""))
        with tempfile.TemporaryDirectory() as folder:
            plan_dir, run_dir = Path(folder) / "plan", Path(folder) / "run"
            execute(DATA, SKILL, "gpt-5-mini", "e" * 40, plan_dir)
            execute(DATA, SKILL, "gpt-5-mini", "e" * 40, run_dir, caller=caller)
            plan = json.loads((plan_dir / "manifest.json").read_text())
            run_plan = json.loads((run_dir / "manifest.json").read_text())
            receipt = json.loads((run_dir / "run_receipt.json").read_text())
            self.assertEqual(plan["suite_sha256"], run_plan["suite_sha256"])
            self.assertEqual(plan["suite_sha256"], receipt["suite_sha256"])
            self.assertNotEqual(plan["results_status"], "EXECUTION_COMPLETE")
            self.assertEqual(receipt["status"], "DEVELOPMENT_TEST_DOUBLE_ONLY")

    def test_mock_9_case_arm_records_are_not_mislabeled_real(self):
        caller, _ = fake(response("SKIP", "none", ""))
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "mock"
            got = execute(DATA, SKILL, "gpt-5-mini", "b" * 40, output, caller=caller)
            self.assertEqual(got["status"], "DEVELOPMENT_TEST_DOUBLE_ONLY")
            rows = json.loads((output / "first_pass_unscored.json").read_text())
            self.assertEqual(len(rows), 9)
            self.assertTrue(all(row["first_pass_unscored"] for row in rows))
            self.assertTrue(all(row["first_call_receipt"]["response_id"] == "MOCK_NOT_PROVIDER" for row in rows))
            self.assertFalse(got["clinical_validated"])

    def test_blind_reviewer_packet_and_mapping_separated(self):
        caller, _ = fake(response("SKIP", "none", ""))
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "test"
            got = execute(DATA, SKILL, "gpt-5-mini", "c" * 40, output, caller=caller)
            packet = json.loads((output / "blind_reviewer_packet.json").read_text())
            mapping = json.loads((output / "private_arm_mapping.json").read_text())
            receipt = json.loads((output / "run_receipt.json").read_text())
            self.assertEqual(len(packet), 3)
            self.assertEqual(len(mapping), 9)
            self.assertEqual(receipt["model_calls_attempted"], 18)
            self.assertEqual(receipt["completed_pairs"], 9)
            self.assertIsNone(receipt["cost_usd"])
            self.assertIsNone(receipt["owner_minutes"])
            self.assertFalse(receipt["provider_receipt_authenticated"])
            self.assertTrue(all(receipt["per_arm_token_usage"][arm] is None
                                for arm in ("native", "retrieval", "skill")))
            self.assertEqual(receipt["independent_review"], "NOT_DONE")
            self.assertTrue(all("arm" not in str(answer) and "case_id" not in str(answer)
                                for case in packet for answer in case["candidate_answers"]))
            self.assertEqual(got["status"], "DEVELOPMENT_TEST_DOUBLE_ONLY")

    def test_failed_first_stage_remains_incomplete_not_fabricated_review(self):
        def fail_all(request):
            raise PilotError("SYNTHETIC_FAILURE")
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "failed"
            got = execute(DATA, SKILL, "gpt-5-mini", "c" * 40, output, caller=fail_all)
            receipt = json.loads((output / "run_receipt.json").read_text())
            packet = json.loads((output / "blind_reviewer_packet.json").read_text())
            self.assertEqual(got["status"], "HOLD_INCOMPLETE")
            self.assertEqual(receipt["failed_pairs"], 9)
            self.assertEqual(receipt["completed_pairs"], 0)
            self.assertEqual(receipt["model_calls_attempted"], 9)
            self.assertTrue(all(answer["run_status"] == "FAILED_INCOMPLETE"
                                for case in packet for answer in case["candidate_answers"]))
            self.assertTrue(all(answer["answer"] is None
                                for case in packet for answer in case["candidate_answers"]))

    def test_real_api_path_receipt_reuse_fails_closed_using_mock_not_network(self):
        # Uniqueness enforcement is tested by replacing the network transport:
        # no model or provider actually runs, and this MUST NOT be clinical evidence.
        from unittest.mock import patch
        approved = (ROOT / ".agents/skills/decision-question-triage/SKILL.md").read_text()
        def duplicate_provider_receipt(request, key):
            return {"answer": json.dumps(response(), ensure_ascii=False),
                    "response_id": "resp_synthetic_duplicate",
                    "returned_model": "gpt-5-mini",
                    "usage": {"input_tokens": 1, "output_tokens": 2, "total_tokens": 3}}
        with tempfile.TemporaryDirectory() as folder:
            with patch("selective_retrieval_probe.api_call", side_effect=duplicate_provider_receipt):
                output = Path(folder) / "mock_provider"
                got = execute(DATA, approved, "gpt-5-mini", "c" * 40,
                              output, key="synthetic_test_only", live=True)
            self.assertEqual(got["status"], "HOLD_INCOMPLETE")
            receipt = json.loads((output / "run_receipt.json").read_text())
            self.assertGreater(receipt["failed_pairs"], 0)
            self.assertIsNone(receipt["tokens_observed_for_completed_calls"])
            self.assertFalse(receipt["provider_receipt_authenticated"])

    def test_no_write_inside_public_repository(self):
        with self.assertRaises(PilotError):
            execute(DATA, SKILL, "gpt-5-mini", "a" * 40,
                    ROOT / "experiments/skill-transfer/tmp-unsafe")
                    
    def test_live_path_rejects_arbitrary_in_memory_material_even_if_labeled_synthetic(self):
        mutated = json.loads(json.dumps(DATA))
        mutated["cases"][0]["task"] += " Added invisible private source."
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(PilotError, "LIVE_CONTENT_NOT_ALLOWLISTED"):
                execute(mutated, SKILL, "gpt-5-mini", "a" * 40,
                        Path(folder) / "blocked", key="fake_test_key", live=True)

    def test_live_rejects_nonallowlisted_model_before_any_call(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(PilotError, "LIVE_KEY_MODEL_AND_TRANSPORT_REQUIRED"):
                execute(DATA, SKILL, "expensive-unapproved-model", "a" * 40,
                        Path(folder) / "blocked", key="fake_test_key", live=True)

    def test_live_refuses_injected_callable_transport(self):
        caller, _ = fake(response())
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(PilotError):
                execute(DATA, SKILL, "gpt-5-mini", "a" * 40,
                        Path(folder) / "blocked", key="fake_test_key",
                        live=True, caller=caller)

    def test_requires_sha_and_correct_fixture(self):
        with self.assertRaises(PilotError):
            build_plan(DATA, SKILL, "gpt-5-mini", "not-a-sha")


if __name__ == "__main__":
    unittest.main()
