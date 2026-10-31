"""Adversarial checks for evidence-gated growth diagnostics; public-safe fixture."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
from growth_snapshot import analyze

FIXTURE = json.loads(
    (REPO / "experiments/growth-measurement/selected_pr_shadow_20261031.json").read_text(encoding="utf-8")
)


class TestGrowthSnapshot(unittest.TestCase):
    def test_selected_sample_not_population_success(self):
        r = analyze(deepcopy(FIXTURE))
        self.assertEqual(r["sample_size"], 4)
        self.assertEqual(r["verified_milestone_counts"]["artifact_observed"], 4)
        self.assertEqual(r["verified_milestone_counts"]["engineering_verified"], 1)
        self.assertEqual(r["verified_milestone_counts"]["independently_accepted"], 0)
        self.assertFalse(r["is_population_or_autonomy_success_rate"])

    def test_missing_outcomes_stay_unknown(self):
        r = analyze(deepcopy(FIXTURE))
        self.assertEqual(r["unprompted_accepted_rate"], "NOT_COMPUTABLE")
        self.assertEqual(r["learning_transfer_gain"], "NOT_MEASURED")

    def test_cannot_include_frozen_137(self):
        p = deepcopy(FIXTURE)
        p["tasks"][0]["in_frozen_137"] = True
        with self.assertRaisesRegex(ValueError, "72h"):
            analyze(p)

    def test_no_self_certified_independent_acceptance(self):
        p = deepcopy(FIXTURE)
        p["tasks"][0]["stage_evidence"]["independently_accepted"] = {
            "status": "VERIFIED", "source_url": "https://example.org/untrusted"
        }
        with self.assertRaisesRegex(ValueError, "independent acceptance"):
            analyze(p)

    def test_cannot_skip_engineering_evidence(self):
        p = deepcopy(FIXTURE)
        p["tasks"][1]["stage_evidence"]["independently_accepted"] = {
            "status": "VERIFIED",
            "source_url": "https://example.org/untrusted",
            "independent_acceptance": "untrusted",
        }
        with self.assertRaisesRegex(ValueError, "skip"):
            analyze(p)

    def test_downstream_requires_actual_outcome(self):
        p = deepcopy(FIXTURE)
        p["tasks"][0]["stage_evidence"]["independently_accepted"] = {
            "status": "VERIFIED", "source_url": "https://example.org/test",
            "independent_acceptance": "test"
        }
        p["tasks"][0]["stage_evidence"]["downstream_value_verified"] = {
            "status": "VERIFIED", "source_url": "https://example.org/test",
            "independent_acceptance": "test"
        }
        with self.assertRaisesRegex(ValueError, "downstream outcome"):
            analyze(p)

    def test_unmeasured_owner_minutes_cannot_be_zero(self):
        p = deepcopy(FIXTURE)
        p["tasks"][0]["owner_minutes"] = 0
        with self.assertRaisesRegex(ValueError, "owner minutes"):
            analyze(p)

    def test_duplicate_tasks_rejected(self):
        p = deepcopy(FIXTURE)
        p["tasks"].append(deepcopy(p["tasks"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            analyze(p)

    def test_explicit_stage_evidence_required(self):
        p = deepcopy(FIXTURE)
        del p["tasks"][0]["stage_evidence"]["engineering_verified"]
        with self.assertRaisesRegex(ValueError, "explicitly"):
            analyze(p)

    def test_unverified_source_cannot_claim_verified(self):
        p = deepcopy(FIXTURE)
        p["tasks"][0]["stage_evidence"]["artifact_observed"]["source_url"] = "LOCAL_ONLY"
        with self.assertRaisesRegex(ValueError, "source_url"):
            analyze(p)


    def accepted_fixture(self):
        p = deepcopy(FIXTURE)
        cell = p["tasks"][0]["stage_evidence"]
        cell["independently_accepted"] = {
            "status": "VERIFIED", "source_url": "https://example.org/review",
            "independent_acceptance": "review-receipt/accepted-1"}
        cell["downstream_value_verified"] = {
            "status": "VERIFIED", "source_url": "https://example.org/outcome",
            "independent_acceptance": "review-receipt/accepted-1",
            "outcome_evidence": "outcome-receipt/measured-1"}
        return p

    def test_explicit_missing_evidence_markers_rejected(self):
        for marker in ("NOT_VERIFIED", " not_measured ", "UNKNOWN", "PENDING",
                       "NOT_OBSERVED", "INCONCLUSIVE", "HOLD", "false"):
            for stage, field in (
                ("independently_accepted", "independent_acceptance"),
                ("downstream_value_verified", "independent_acceptance"),
                ("downstream_value_verified", "outcome_evidence")):
                with self.subTest(marker=marker, stage=stage, field=field):
                    p = self.accepted_fixture()
                    p["tasks"][0]["stage_evidence"][stage][field] = marker
                    with self.assertRaises(ValueError):
                        analyze(p)

    def test_evidence_reference_must_be_nonempty_text(self):
        for value in (True, 1, ["receipt"], {"receipt": "present"}, "   "):
            with self.subTest(value=value):
                p = self.accepted_fixture()
                p["tasks"][0]["stage_evidence"]["independently_accepted"][
                    "independent_acceptance"] = value
                with self.assertRaises(ValueError):
                    analyze(p)

    def test_supported_reference_contract_remains_accepted(self):
        r = analyze(self.accepted_fixture())
        self.assertEqual(r["verified_milestone_counts"]["independently_accepted"], 1)
        self.assertEqual(r["verified_milestone_counts"]["downstream_value_verified"], 1)


if __name__ == "__main__":
    unittest.main()
