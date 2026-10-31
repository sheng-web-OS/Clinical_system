"""Only synthetic records; demonstrate provenance ceilings and schema safety."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_attempt_evidence_audit import (
    ATTEMPTS_HEADER, CONCEPTS_HEADER, assess, inspect_remote,
)


def attempt(aid="synthetic-1", response="B", assessment="correct",
            source="assistant-reported key; original not verified",
            official="NO", exposure="initial attempt", quality="provisional"):
    return [aid, "2026-10-31", "session-demo", "local-q-demo", official,
            "domain-demo", response, "B", assessment,
            "synthetic observation", exposure, source, quality, "retest"]


def concept(cid="synthetic-concept-1", retest="YES"):
    return [cid, "demo", "observation", "encountered", "low", retest,
            "high", "retest", "2026-10-31", "not independently validated"]


class ProvenanceAuditTests(unittest.TestCase):
    def test_initial_correct_provisional_answer_is_not_verified_mastery(self):
        report = assess([attempt()], [concept()])
        self.assertEqual(report["observed_response_rows"], 1)
        self.assertEqual(report["independently_verified_item_grades"], 0)
        self.assertEqual(report["mastery_upgrades_authorized"], 0)
        self.assertEqual(report["concept_retest_pending"], 1)

    def test_official_yes_flag_alone_is_not_external_proof(self):
        report = assess([attempt(official="YES")], [])
        self.assertEqual(report["official_identity_claimed_verified_not_external_proof"], 1)
        self.assertEqual(report["independently_verified_item_grades"], 0)

    def test_group_score_not_attributable_to_specific_item(self):
        report = assess([attempt(assessment="group 3/3 reported",
                                 quality="group-level grading")], [])
        self.assertEqual(report["group_grade_nonattributable"], 1)

    def test_unanswered_not_graduated(self):
        report = assess([attempt(response="", assessment="unanswered")], [])
        self.assertEqual(report["answer_missing_rows"], 1)
        self.assertEqual(report["assessment_present_without_independent_receipt"], 0)

    def test_post_remediation_not_unseen(self):
        report = assess([attempt(exposure="after remediation")], [])
        self.assertEqual(report["post_remediation_or_noninitial_exposure"], 1)
        self.assertEqual(report["unseen_transfer_passes_proven_by_this_audit"], 0)

    def test_duplicate_attempt_blocked(self):
        with self.assertRaisesRegex(RuntimeError, "duplicate private attempt"):
            assess([attempt(), attempt()], [])

    def test_duplicate_concept_blocked(self):
        with self.assertRaisesRegex(RuntimeError, "duplicate private concept"):
            assess([], [concept(), concept()])

    def test_trailing_empty_cells_from_sheets_are_allowed(self):
        row = attempt()[:11]
        concept_row = concept()[:6]
        r = assess([row], [concept_row])
        self.assertEqual((r["attempt_rows"], r["concept_nodes"]), (1, 1))

    def test_unrecognized_exam_status_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "Invalid exam identity"):
            assess([attempt(official="MAYBE_PASS")], [])

    def test_read_only_remote_adapter_and_header_validation(self):
        class FakeSheet:
            def __init__(self, bad=False):
                self.calls = []
                self.bad = bad
            def get(self, key):
                self.calls.append(key)
                output = {
                    "Attempts!A1:N1": [ATTEMPTS_HEADER.copy()],
                    "Concepts!A1:J1": [CONCEPTS_HEADER.copy()],
                    "Attempts!A2:N": [attempt()],
                    "Concepts!A2:J": [concept()],
                }
                if self.bad:
                    output["Attempts!A1:N1"] = [["unrecognized"]]
                return output[key]
        sheet = FakeSheet()
        self.assertEqual(inspect_remote(sheet)["concept_nodes"], 1)
        self.assertEqual(len(sheet.calls), 4)
        with self.assertRaisesRegex(RuntimeError, "Attempts header mismatch"):
            inspect_remote(FakeSheet(bad=True))


if __name__ == "__main__":
    unittest.main()
