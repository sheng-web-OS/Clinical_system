"""Mechanical integrity checks only; never claim that these synthetic records prove reasoning gains."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from compare_skill_transfer import evaluate

HEX = "a" * 64
COMMIT = "b" * 40
ARMS = ("native", "retrieval", "skill")
CASES = (
    ("novel-transfer", "transfer"),
    ("valid-normal", "normal"),
    ("out-of-scope", "boundary"),
)


def fixture():
    suite = {
        "schema_version": 1,
        "id": "synthetic-integrity-fixture",
        "exposure": "development",
        "retrieval_pack_sha256": "d" * 64,
        "candidate_skill_sha256": "e" * 64,
        "cases": [{"id": cid, "role": role, "source_sha256": HEX}
                  for cid, role in CASES],
    }
    records = []
    for cid, role in CASES:
        for arm in ARMS:
            correct = role != "transfer" or arm == "skill"
            records.append({
                "case_id": cid, "arm": arm,
                "source_sha256": HEX, "decision_correct": correct,
                "first_pass": correct, "unsafe": False,
                "hinted": False, "false_alarm": False,
                "article_retrieval_visible": arm != "native",
                "candidate_skill_visible": arm == "skill",
                "retrieval_pack_sha256": None if arm == "native" else "d" * 64,
                "loaded_skill_sha256": "e" * 64 if arm == "skill" else None,
                "skill_applied": role == "transfer" and arm == "skill",
                "worker_context": "writer-" + cid + "-" + arm,
                "reviewer_context": "independent-judge-context",
                "trace_ref": "synthetic-only-" + cid + "-" + arm,
                "model": "fixed-model", "effort": "fixed-effort",
                "tools_scope": "same-frozen-sources",
                "token_budget": "fixed-budget",
                "owner_minutes": 2.0,
            })
    raw = json.dumps(suite, sort_keys=True).encode("utf-8")
    run = {
        "schema_version": 1, "suite_id": suite["id"],
        "suite_sha256": hashlib.sha256(raw).hexdigest(),
        "candidate_commit": COMMIT, "records": records,
    }
    return suite, run


class TransferPilotIntegrity(unittest.TestCase):
    def setUp(self):
        self.suite, self.run = fixture()
        self.hash = self.run["suite_sha256"]

    def report(self):
        return evaluate(self.suite, self.run, self.hash,
                        "d" * 64, "e" * 64)

    def rejects(self, expected):
        with self.assertRaisesRegex(ValueError, expected):
            self.report()

    def test_complete_fixture_is_only_development_not_validated(self):
        report = self.report()
        self.assertEqual("DEVELOPMENT_GAIN_ONLY_NEEDS_INDEPENDENT_HOLDOUT",
                         report["verdict"])
        self.assertFalse(report["promotion_authorized"])
        self.assertFalse(report["clinical_validated"])
        self.assertFalse(report["independent_review_authenticated"])
        self.assertEqual(1, report["arm_metrics"]["skill"]["transfer_first_pass"])
        self.assertEqual(0, report["arm_metrics"]["retrieval"]["transfer_first_pass"])

    def test_real_input_file_digest_mismatch_cannot_be_self_reported(self):
        with self.assertRaisesRegex(ValueError, "actual retrieval pack"):
            evaluate(self.suite, self.run, self.hash, "f" * 64, "e" * 64)
        with self.assertRaisesRegex(ValueError, "actual retrieval pack"):
            evaluate(self.suite, self.run, self.hash, "d" * 64, "f" * 64)

    def test_missing_trials_fail_closed(self):
        self.run["records"].pop()
        self.rejects("missing arm/case")

    def test_duplicate_trials_fail_closed(self):
        self.run["records"].append(copy.deepcopy(self.run["records"][0]))
        self.rejects("unknown or duplicate")

    def test_synthetic_hint_cannot_claim_unprompted_detection(self):
        self.run["records"][0]["hinted"] = True
        self.rejects("hinted trial")

    def test_wrong_source_and_stale_suite_rejected(self):
        self.run["records"][0]["source_sha256"] = "c" * 64
        self.rejects("source mismatch")
        self.suite, self.run = fixture()
        self.run["suite_sha256"] = "c" * 64
        self.rejects("stale answer-key")

    def test_same_context_cannot_be_counted_twice(self):
        self.run["records"][1]["worker_context"] = self.run["records"][0]["worker_context"]
        self.rejects("worker context reused")
        self.suite, self.run = fixture()
        self.run["records"][1]["trace_ref"] = self.run["records"][0]["trace_ref"]
        self.rejects("trace reused")

    def test_reviewer_may_not_overlap_writer(self):
        self.run["records"][0]["reviewer_context"] = self.run["records"][1]["worker_context"]
        self.rejects("reviewer and writer")

    def test_model_effort_and_budget_must_match(self):
        self.run["records"][0]["token_budget"] = "more-budget"
        self.rejects("unequal model")

    def test_skill_metadata_leak_to_baselines_rejected(self):
        next(r for r in self.run["records"] if r["arm"] == "retrieval")["candidate_skill_visible"] = True
        self.rejects("arm contamination")
        self.suite, self.run = fixture()
        next(r for r in self.run["records"] if r["arm"] == "native")["candidate_skill_visible"] = True
        self.rejects("arm contamination")

    def test_article_exposure_mismatch_rejected(self):
        next(r for r in self.run["records"] if r["arm"] == "native")["article_retrieval_visible"] = True
        self.rejects("arm contamination")

    def test_retrieval_pack_mismatch_refused(self):
        next(r for r in self.run["records"] if r["arm"] == "skill")[
            "retrieval_pack_sha256"] = "f" * 64
        self.rejects("article retrieval pack mismatch")

    def test_retrieval_control_cannot_load_candidate_skill(self):
        next(r for r in self.run["records"] if r["arm"] == "retrieval")[
            "loaded_skill_sha256"] = self.suite["candidate_skill_sha256"]
        self.rejects("candidate skill version mismatch")

    def test_wrong_candidate_skill_digest_refused(self):
        next(r for r in self.run["records"] if r["arm"] == "skill")[
            "loaded_skill_sha256"] = "f" * 64
        self.rejects("candidate skill version mismatch")

    def test_boundary_misfire_refused_even_if_output_correct(self):
        next(r for r in self.run["records"] if
             r["arm"] == "skill" and r["case_id"] == "out-of-scope")[
                 "skill_applied"] = True
        self.rejects("non-applicable boundary wrongly activated skill")

    def test_skill_not_used_cannot_claim_incremental_skill_gain(self):
        next(r for r in self.run["records"] if
             r["arm"] == "skill" and r["case_id"] == "novel-transfer")[
                 "skill_applied"] = False
        self.assertEqual("NO_PROMOTABLE_INCREMENT", self.report()["verdict"])

    def test_boundary_false_alarm_is_a_control_failure(self):
        r = next(r for r in self.run["records"] if
                 r["arm"] == "skill" and r["case_id"] == "out-of-scope")
        r["false_alarm"] = True
        r["decision_correct"] = False
        r["first_pass"] = False
        self.assertEqual("HOLD_SAFETY_OR_CONTROL_REGRESSION", self.report()["verdict"])

    def test_stale_suite_skill_digest_refused(self):
        self.suite["candidate_skill_sha256"] = "f" * 64
        self.rejects("candidate skill version mismatch")

    def test_normal_false_alarm_blocks_and_never_promotes(self):
        for r in self.run["records"]:
            if r["case_id"] == "valid-normal" and r["arm"] == "skill":
                r["false_alarm"] = True
                r["decision_correct"] = False
                r["first_pass"] = False
        report = self.report()
        self.assertEqual("HOLD_SAFETY_OR_CONTROL_REGRESSION", report["verdict"])
        self.assertFalse(report["promotion_authorized"])

    def test_any_unsafe_trial_blocks_and_cannot_be_first_pass(self):
        for r in self.run["records"]:
            if r["case_id"] == "novel-transfer" and r["arm"] == "skill":
                r["unsafe"] = True
                r["first_pass"] = False
        self.assertEqual("HOLD_SAFETY_OR_CONTROL_REGRESSION", self.report()["verdict"])
        self.run["records"][0]["unsafe"] = True
        self.run["records"][0]["first_pass"] = True
        self.run["records"][0]["decision_correct"] = True
        self.rejects("first-pass credit contradicts")

    def test_missing_cost_is_not_free_and_no_gain_cannot_pass(self):
        next(r for r in self.run["records"] if r["arm"] == "skill")["owner_minutes"] = None
        self.assertEqual("NO_PROMOTABLE_INCREMENT", self.report()["verdict"])
        self.suite, self.run = fixture()
        for r in self.run["records"]:
            if r["case_id"] == "novel-transfer" and r["arm"] == "skill":
                r["first_pass"] = False
                r["decision_correct"] = False
        self.assertEqual("NO_PROMOTABLE_INCREMENT", self.report()["verdict"])

    def test_bad_cost_boolean_or_negative_fails(self):
        self.run["records"][0]["owner_minutes"] = False
        self.rejects("owner minutes")
        self.run["records"][0]["owner_minutes"] = -1
        self.rejects("owner minutes")

    def test_unexpected_case_role_rejected(self):
        self.suite["cases"][0]["role"] = "interview"
        self.rejects("unknown case role")

    def test_normal_and_boundary_controls_required(self):
        self.suite["cases"][1]["role"] = "transfer"
        self.rejects("controls required")


if __name__ == "__main__":
    unittest.main()
