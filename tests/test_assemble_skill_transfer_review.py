"""Integrity tests using a local fake model, never paid API or expert grading."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from assemble_skill_transfer_review import assemble
from run_skill_transfer_pilot import PilotError, run

CASES = ROOT / "experiments/skill-transfer/fixtures/synthetic-questions.json"
PACK = ROOT / "content/xiaoma-reading/originals/2026-07-14-hcm.md"
SKILL = ROOT / ".agents/skills/decision-question-triage/SKILL.md"
COMMIT = "a" * 40


class ReviewAssemblyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run_dir = self.root / "pilot"
        self.review_path = self.root / "review.json"
        self.count = 0

        def mock_model(req, key):
            self.count += 1
            return {"answer": "Synthetic mock answer " + str(self.count),
                    "returned_model": "gpt-5-mini",
                    "response_id": "mock-response-" + str(self.count),
                    "usage": {"input_tokens": 30, "output_tokens": 5}}
        result = run(CASES, PACK, SKILL, self.run_dir,
                     "gpt-5-mini", COMMIT, execute=True, key="mock-only",
                     caller=mock_model)
        self.assertEqual(9, result["completed"])
        self.make_review()

    def load(self, name):
        return json.loads((self.run_dir / name).read_text(encoding="utf-8"))

    def store(self, name, obj):
        (self.run_dir / name).write_text(
            json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

    def make_review(self):
        mapping = self.load("private_arm_mapping.json")
        judgments = []
        for slot, info in mapping["answer_slots"].items():
            correct = info["case_id"] != "synthetic-hcm-decision" or info["arm"] == "skill"
            judgments.append({
                "slot": slot, "decision_correct": correct,
                "unsafe": False, "false_alarm": False,
                "question_triage_observed": (
                    info["case_id"] == "synthetic-hcm-decision"
                    and info["arm"] == "skill"
                ),
                "reason": "Independent simulated rubric verdict for test fixture only.",
            })
        self.review = {
            "schema_version": 1,
            "packet_sha256": hashlib.sha256(
                (self.run_dir / "blind_reviewer_packet.json").read_bytes()
            ).hexdigest(),
            "suite_sha256": hashlib.sha256(
                (self.run_dir / "frozen_suite.json").read_bytes()
            ).hexdigest(),
            "reviewer_context": "fresh-reviewer-simulated-not-authenticated",
            "judgments": judgments,
        }
        self.review_path.write_text(json.dumps(self.review, indent=2))

    def assemble(self):
        return assemble(self.run_dir, self.review_path, CASES, PACK, SKILL)

    def assert_reject(self, expected):
        with self.assertRaisesRegex(ValueError, expected):
            self.assemble()

    def test_complete_observations_still_do_not_claim_learning(self):
        run_data, report = self.assemble()
        self.assertEqual(9, len(run_data["records"]))
        self.assertEqual("NO_PROMOTABLE_INCREMENT", report["verdict"])
        self.assertFalse(report["promotion_authorized"])
        self.assertFalse(report["skill_invocation_verified"])
        self.assertFalse(report["owner_attention_measured"])
        self.assertEqual(1, report["arm_metrics"]["skill"]["transfer_first_pass"])
        self.assertEqual(0, report["arm_metrics"]["retrieval"]["transfer_first_pass"])

    def test_missing_judgment_rejected_instead_of_reweighting_denominator(self):
        self.review["judgments"].pop()
        self.review_path.write_text(json.dumps(self.review))
        self.assert_reject("INCOMPLETE_INDEPENDENT_ADJUDICATION")

    def test_duplicate_judgment_rejected(self):
        self.review["judgments"][-1] = self.review["judgments"][0]
        self.review_path.write_text(json.dumps(self.review))
        self.assert_reject("UNKNOWN_OR_DUPLICATE_REVIEW_SLOT")

    def test_tampered_answer_cannot_get_original_credit(self):
        result = self.load("first_pass_results.json")
        result[0]["response"]["answer"] = "changed after scoring"
        self.store("first_pass_results.json", result)
        self.assert_reject("BLIND_ANSWER_NOT_IDENTICAL_TO_FIRST_PASS")

    def test_modified_review_packet_is_detected_even_if_answer_valid(self):
        packet = self.load("blind_reviewer_packet.json")
        packet[0]["task"] += " Modified after first pass."
        self.store("blind_reviewer_packet.json", packet)
        self.assert_reject("REVIEW_NOT_BOUND_TO_FROZEN_BLIND_PACKET")

    def test_changed_case_or_source_cannot_be_silent(self):
        suite = self.load("frozen_suite.json")
        suite["cases"][0]["role"] = "normal"
        self.store("frozen_suite.json", suite)
        self.assert_reject("FROZEN_SUITE_MISMATCH")

    def test_unfinished_start_event_cannot_be_dropped(self):
        p = self.run_dir / "attempt_events.jsonl"
        events = p.read_text().splitlines()
        p.write_text("\n".join(events[:-1]) + "\n")
        self.assert_reject("INCOMPLETE_OR_EXTRA_ATTEMPT_EVENTS")

    def test_swapped_arm_mapping_detected(self):
        mapping = self.load("private_arm_mapping.json")
        ids = list(mapping["answer_slots"])
        mapping["answer_slots"][ids[0]], mapping["answer_slots"][ids[1]] = (
            mapping["answer_slots"][ids[1]], mapping["answer_slots"][ids[0]]
        )
        self.store("private_arm_mapping.json", mapping)
        self.assert_reject("BLIND_ANSWER_NOT_IDENTICAL_TO_FIRST_PASS|BLIND_SLOT_MISMATCH")

    def test_reviewer_cannot_mark_missing_answer_correct(self):
        results = self.load("first_pass_results.json")
        events = (self.run_dir / "attempt_events.jsonl").read_text().splitlines()
        results[0]["status"] = "FAILED_OR_INCOMPLETE"
        results[0]["response"] = None
        event = json.loads(events[1])
        event["event"] = "FAILED_OR_INCOMPLETE"
        events[1] = json.dumps(event)
        (self.run_dir / "attempt_events.jsonl").write_text("\n".join(events) + "\n")
        self.store("first_pass_results.json", results)
        packet = self.load("blind_reviewer_packet.json")
        for scenario in packet:
            for candidate in scenario["candidate_answers"]:
                if candidate["answer"] == "Synthetic mock answer 1":
                    candidate["answer"] = None
                    candidate["run_status"] = "FAILED_OR_INCOMPLETE"
                    target_slot = candidate["slot"]
        self.store("blind_reviewer_packet.json", packet)
        self.review["packet_sha256"] = hashlib.sha256(
            (self.run_dir / "blind_reviewer_packet.json").read_bytes()).hexdigest()
        for verdict in self.review["judgments"]:
            if verdict["slot"] == target_slot:
                verdict["decision_correct"] = True
        self.review_path.write_text(json.dumps(self.review))
        self.assert_reject("FAILED_CALL_MUST_NOT_BE_GRADED_AS_SUCCESS")

    def test_non_boolean_review_denied(self):
        self.review["judgments"][0]["unsafe"] = "no"
        self.review_path.write_text(json.dumps(self.review))
        self.assert_reject("REVIEW_MUST_SUPPLY_BOOLEAN")

    def test_fake_reviewer_identity_cannot_count_as_authenticated(self):
        _, report = self.assemble()
        self.assertFalse(report["independent_review_authenticated"])
        self.assertEqual(
            "fresh-reviewer-simulated-not-authenticated",
            report["reviewer_context_declared_not_authenticated"])

    def test_non_private_output_not_implicitly_written(self):
        self.assertFalse((ROOT / "experiments/skill-transfer/results").exists())
        self.assertTrue((self.run_dir / "blind_reviewer_packet.json").exists())


if __name__ == "__main__":
    unittest.main()
