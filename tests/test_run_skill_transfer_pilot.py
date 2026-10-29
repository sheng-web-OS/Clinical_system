"""No network or live model calls: validate controlled first-pass pilot execution."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.run_skill_transfer_pilot import (
    PilotError, build_plan, clean_cases, digest, extract_output,
    make_request, run,
)

COMMIT = "a" * 40
MARKER = "SYNTHETIC EDUCATIONAL SCENARIO"
CASES = [
    {
        "id": "synthetic-renew",
        "role": "transfer",
        "task": MARKER + ": A fully invented dialysis education task. A learner "
                "reports a low measured pressure despite otherwise stable observations. "
                "Discuss which different mechanisms could explain a discrepancy, "
                "which new information would discriminate them, and how the "
                "conclusion would change under alternative assumptions. No actual "
                "person or medical decisions are involved here.",
    },
    {
        "id": "synthetic-normal",
        "role": "normal",
        "task": MARKER + ": An invented educational primer explicitly asks for a "
                "straightforward account of what a measurement means and how to "
                "read it. The supplied text already contains an adequate "
                "scope qualification. Explain it clearly without manufacturing "
                "a clinical controversy or incorrectly declaring it unsafe.",
    },
    {
        "id": "synthetic-boundary",
        "role": "boundary",
        "task": MARKER + ": A fictional glossary asks students to define "
                "a physiological concept and distinguish it from a neighboring "
                "definition. No patient, diagnostic choice, treatment "
                "comparison, source conflict, or clinical decision point "
                "is provided. Explain definitions without pretending "
                "that a contested clinical choice exists.",
    },
]
SKILL = "---\nname: decision-question-triage\n---\nFollow causal evidence only when applicable."
PACK = "Original authored lesson: distinguish measurement from mechanism."
MODEL = "gpt-5-mini"


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cases = self.root / "cases.json"
        self.pack = self.root / "pack.md"
        self.skill = self.root / "SKILL.md"
        self.cases.write_text(json.dumps({
            "schema_version": 1, "source_class": "synthetic_public_fixture",
            "cases": CASES,
        }), encoding="utf-8")
        self.pack.write_text(PACK, encoding="utf-8")
        self.skill.write_text(SKILL, encoding="utf-8")

    def go(self, mode=False, caller=None):
        return run(self.cases, self.pack, self.skill, self.root / "out",
                   MODEL, COMMIT, execute=mode,
                   key="test-placeholder-not-a-real-key" if mode else None,
                   caller=caller)

    def test_checked_in_synthetic_scenarios_use_real_authored_article_offline(self):
        root = Path(__file__).resolve().parents[1]
        result = run(
            root / "experiments/skill-transfer/fixtures/synthetic-questions.json",
            root / "content/xiaoma-reading/originals/2026-07-14-hcm.md",
            root / ".agents/skills/decision-question-triage/SKILL.md",
            self.root / "checked-in-plan", MODEL, COMMIT)
        self.assertEqual("PLAN_ONLY_NO_MODEL_CALLS", result["status"])
        requests = json.loads((self.root / "checked-in-plan/requests.json").read_text())
        self.assertEqual(9, len(requests))
        self.assertEqual(
            0, sum("Nonobstructive 只回答了一個問題" in x["request"]["instructions"]
                   for x in requests if x["arm"] == "native"))
        self.assertEqual(
            6, sum("Nonobstructive 只回答了一個問題" in x["request"]["instructions"]
                   for x in requests if x["arm"] != "native"))

    def test_plan_only_does_not_touch_model_or_grader(self):
        result = self.go()
        self.assertEqual("PLAN_ONLY_NO_MODEL_CALLS", result["status"])
        self.assertEqual(9, result["planned"])
        self.assertFalse((self.root / "out/first_pass_results.json").exists())
        meta = json.loads((self.root / "out/manifest.json").read_text())
        self.assertEqual("NOT_RUN", meta["results_status"])
        self.assertFalse(meta["learning_effect_validated"])

    def test_request_isolation_and_same_evidence_pack(self):
        self.go()
        reqs = json.loads((self.root / "out/requests.json").read_text())
        self.assertEqual(9, len(reqs))
        for cid in [c["id"] for c in CASES]:
            a = next(r for r in reqs if r["case_id"] == cid and r["arm"] == "native")
            b = next(r for r in reqs if r["case_id"] == cid and r["arm"] == "retrieval")
            c = next(r for r in reqs if r["case_id"] == cid and r["arm"] == "skill")
            self.assertEqual(a["request"]["input"], b["request"]["input"])
            self.assertEqual(b["request"]["input"], c["request"]["input"])
            self.assertNotIn(PACK, a["request"]["instructions"])
            self.assertNotIn(SKILL, a["request"]["instructions"])
            self.assertIn(PACK, b["request"]["instructions"])
            self.assertNotIn(SKILL, b["request"]["instructions"])
            self.assertIn(PACK, c["request"]["instructions"])
            self.assertIn(SKILL, c["request"]["instructions"])
            self.assertFalse(c["request"]["store"])
            self.assertEqual(
                a["request"]["max_output_tokens"], c["request"]["max_output_tokens"])

    def test_actual_mock_executions_have_first_pass_and_blind_packet(self):
        captured = []
        def fake_transport(request, key):
            captured.append(request)
            return {"answer": "first-pass answer " + str(len(captured)),
                    "returned_model": MODEL, "response_id": "mock-" + str(len(captured)),
                    "usage": {"input_tokens": 10, "output_tokens": 20}}
        report = self.go(mode=True, caller=fake_transport)
        self.assertEqual("UNSCORED_EXECUTION", report["status"])
        self.assertEqual("EXECUTION_STARTED_UNSCORED",
                         json.loads((self.root / "out/manifest.json").read_text())
                         ["results_status"])
        self.assertEqual(9, report["completed"])
        self.assertEqual(9, len(captured))
        entries = json.loads((self.root / "out/first_pass_results.json").read_text())
        self.assertEqual(9, len(entries))
        self.assertTrue(all(e["first_pass"] == "NOT_SCORED" for e in entries))
        packets = json.loads((self.root / "out/blind_reviewer_packet.json").read_text())
        self.assertEqual(3, len(packets))
        serialized = json.dumps(packets)
        self.assertNotIn('"arm"', serialized)
        self.assertNotIn(SKILL, serialized)
        self.assertFalse(report["publication_approved"])
        for original in [c["id"] for c in CASES]:
            self.assertNotIn(original, serialized)
        mapping = json.loads(
            (self.root / "out/private_arm_mapping.json").read_text())
        self.assertEqual(9, len(mapping["answer_slots"]))
        self.assertEqual(3, len(mapping["case_aliases"]))

    def test_failed_calls_are_retained_not_dropped(self):
        count = [0]
        def flaky(request, key):
            count[0] += 1
            if count[0] % 2 == 0:
                raise PilotError("MODEL_CALL_FAILED")
            return {"answer": "synthetic answer", "returned_model": MODEL}
        result = self.go(mode=True, caller=flaky)
        self.assertEqual(9, result["attempted"])
        self.assertEqual(5, result["completed"])
        rows = json.loads((self.root / "out/first_pass_results.json").read_text())
        self.assertEqual(4, sum(x["status"] == "FAILED_OR_INCOMPLETE" for x in rows))
        events = [
            json.loads(line)
            for line in (self.root / "out/attempt_events.jsonl").read_text().splitlines()
        ]
        self.assertEqual(18, len(events))
        self.assertEqual(9, sum(e["event"] == "STARTED" for e in events))
        self.assertEqual(4, sum(e["event"] == "FAILED_OR_INCOMPLETE" for e in events))
        self.assertTrue(all(x["adjudication"] == "NOT_DONE" for x in rows))

    def test_live_api_cannot_send_arbitrary_text_merely_marked_synthetic(self):
        with self.assertRaisesRegex(PilotError, "EXACT_PUBLIC_ALLOWLISTED_INPUT_FILES"):
            run(self.cases, self.pack, self.skill, self.root / "untrusted-live",
                MODEL, COMMIT, execute=True, key="synthetic-not-a-real-key",
                caller=None)
        self.assertFalse((self.root / "untrusted-live").exists())

    def test_api_missing_key_fails_before_making_private_directory(self):
        with self.assertRaisesRegex(PilotError, "MODEL_SECRET_NOT_CONFIGURED"):
            run(self.cases, self.pack, self.skill, self.root / "out",
                MODEL, COMMIT, execute=True, key=None)
        self.assertFalse((self.root / "out").exists())

    def test_existing_output_never_overwritten(self):
        self.go()
        before = (self.root / "out/manifest.json").read_bytes()
        with self.assertRaisesRegex(PilotError, "OUTPUT_EXISTS"):
            self.go()
        self.assertEqual(before, (self.root / "out/manifest.json").read_bytes())

    def test_public_repository_output_path_is_denied(self):
        public_output = Path(__file__).resolve().parents[1] / "test-output-should-not-exist"
        with self.assertRaisesRegex(PilotError, "PRIVATE_OUTPUT_MUST_BE_OUTSIDE"):
            run(self.cases, self.pack, self.skill, public_output,
                MODEL, COMMIT)
        self.assertFalse(public_output.exists())

    def test_not_a_patient_or_nonallowlisted_source(self):
        obj = json.loads(self.cases.read_text())
        obj["source_class"] = "real_patient_note"
        self.cases.write_text(json.dumps(obj))
        with self.assertRaisesRegex(PilotError, "SYNTHETIC_SOURCE_ALLOWLIST_ONLY"):
            self.go()

    def test_case_without_synthetic_marker_rejected(self):
        obj = json.loads(self.cases.read_text())
        obj["cases"][0]["task"] = obj["cases"][0]["task"].replace(MARKER, "")
        self.cases.write_text(json.dumps(obj))
        with self.assertRaisesRegex(PilotError, "INVALID_SYNTHETIC_CASE"):
            self.go()

    def test_unexpected_synthetic_count_or_duplicate_roles_refused(self):
        obj = json.loads(self.cases.read_text())
        obj["cases"].pop()
        with self.assertRaisesRegex(PilotError, "EXACTLY_THREE_SYNTHETIC_CASES_REQUIRED"):
            clean_cases(obj)
        obj["cases"] = [dict(c) for c in CASES]
        obj["cases"][2] = dict(obj["cases"][2], role="transfer")
        with self.assertRaisesRegex(PilotError, "REQUIRE_TRANSFER_NORMAL_BOUNDARY"):
            clean_cases(obj)

    def test_bad_commit_and_invalid_model_rejected(self):
        with self.assertRaisesRegex(PilotError, "EXACT_CANDIDATE_COMMIT_REQUIRED"):
            build_plan(CASES, "a" * 64, PACK, "b" * 64, SKILL,
                       "c" * 64, MODEL, "main")
        with self.assertRaisesRegex(PilotError, "INVALID_MODEL_ID"):
            build_plan(CASES, "a" * 64, PACK, "b" * 64, SKILL,
                       "c" * 64, "model;echo secret", COMMIT)

    def test_incomplete_or_refused_response_not_inferred_successful(self):
        with self.assertRaisesRegex(PilotError, "MODEL_NOT_COMPLETED"):
            extract_output({"status": "incomplete", "output": []})
        with self.assertRaisesRegex(PilotError, "EMPTY_MODEL_OUTPUT"):
            extract_output({"status": "completed", "model": MODEL, "output": []})
        with self.assertRaisesRegex(PilotError, "MODEL_ID_MISSING"):
            extract_output({"status": "completed", "output": [
                {"type": "message", "content": [
                    {"type": "output_text", "text": "message"}]}]})

    def test_output_file_permissions_restrict_group_and_world(self):
        self.go()
        if os.name == "posix":
            file_mode = (self.root / "out/requests.json").stat().st_mode & 0o777
            self.assertEqual(0o600, file_mode)

if __name__ == "__main__":
    unittest.main()
