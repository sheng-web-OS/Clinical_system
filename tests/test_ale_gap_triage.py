"""Offline adversarial tests for bounded public-safe gap prioritization."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_gap_triage import triage


def gap(id_, origin="COVERAGE_GAP", impact="TRANSFER", scope="CURRENT",
        families=0, source="PENDING", effort="SMALL"):
    return {"id": id_, "origin": origin, "impact": impact, "scope": scope,
            "source_state": source, "linked_family_count": families,
            "research_effort": effort}


def run(*gaps, capacity=1):
    return triage({"source_classification": "PUBLIC_SYNTHETIC_ONLY",
                   "gaps": list(gaps), "max_active_research": capacity})


class GapTriageTests(unittest.TestCase):
    def test_critical_current_risk_first_and_requires_source_check(self):
        result = run(gap("ordinary", families=2),
                     gap("critical", "SOURCE_CONTRADICTION", "CRITICAL"))
        self.assertEqual(result["decisions"][0]["id"], "critical")
        self.assertEqual(result["decisions"][0]["decision"], "RESEARCH_NOW")
        self.assertEqual(result["decisions"][0]["next_gate"],
                         "REQUIRE_SOURCE_VERIFICATION")
        self.assertFalse(result["decisions"][0]["source_verified_independently"])

    def test_multiple_critical_not_silently_downgraded(self):
        result = run(gap("a", impact="CRITICAL"),
                     gap("b", impact="CRITICAL"), capacity=1)
        self.assertEqual([d["decision"] for d in result["decisions"]],
                         ["RESEARCH_NOW", "CRITICAL_UNRESOLVED_HOLD"])
        self.assertEqual(result["critical_unresolved"], 1)

    def test_zero_capacity_preserves_critical_hold(self):
        self.assertEqual(run(gap("risk", impact="CRITICAL"), capacity=0)
                         ["decisions"][0]["decision"], "CRITICAL_UNRESOLVED_HOLD")

    def test_tag_cannot_create_domain_truth_from_high_impact_label(self):
        result = run(gap("tag", "TAG_ONLY", "CRITICAL"))
        self.assertEqual(result["decisions"][0]["decision"], "DIAGNOSTIC_FIRST")
        self.assertEqual(result["active_research"], 0)

    def test_reading_and_review_button_not_reasoning_diagnosis(self):
        for origin in ("PASSIVE_READING", "REVIEW_RATING_ONLY"):
            self.assertEqual(run(gap("hint", origin, "BLOCKING"))
                             ["decisions"][0]["decision"], "DIAGNOSTIC_FIRST")

    def test_cross_family_value_queued_no_auto_promotion(self):
        result = run(gap("bridge", families=3, source="SOURCE_ATTESTED"))
        self.assertEqual(result["decisions"][0]["decision"], "QUEUE_RESEARCH")
        self.assertEqual(result["concept_promotions"], 0)

    def test_low_value_and_unrelated_preserve_unknown(self):
        for a in (gap("low", impact="LOW"), gap("other", scope="OUT_OF_SCOPE")):
            self.assertEqual(run(a)["decisions"][0]["decision"], "PRESERVE_UNKNOWN")

    def test_critical_out_of_scope_requires_reconciliation(self):
        result = run(gap("mixed", impact="CRITICAL", scope="OUT_OF_SCOPE"))
        self.assertEqual(result["decisions"][0]["decision"], "SCOPE_CONFLICT_HOLD")

    def test_blocking_queued_under_capacity_pressure(self):
        result = run(gap("urgent", impact="CRITICAL"),
                     gap("blocked", impact="BLOCKING"))
        self.assertEqual([d["decision"] for d in result["decisions"]],
                         ["RESEARCH_NOW", "QUEUE_RESEARCH"])

    def test_order_independent(self):
        gaps = [gap("b", impact="BLOCKING"), gap("a", impact="CRITICAL"),
                gap("c", families=5)]
        self.assertEqual(run(*gaps), run(*reversed(gaps)))

    def test_rejects_private_data_or_free_text_fields(self):
        packet = {"source_classification": "OWNER_PRIVATE",
                  "gaps": [gap("one")], "max_active_research": 1}
        with self.assertRaisesRegex(ValueError, "private"):
            triage(packet)
        packet["source_classification"] = "PUBLIC_SYNTHETIC_ONLY"
        packet["gaps"][0]["personal_note"] = "never upload a learner note"
        with self.assertRaisesRegex(ValueError, "unclassified"):
            triage(packet)

    def test_rejects_invalid_or_ambiguous_ids_and_counts(self):
        for variant in (
            [gap("a"), gap("a")],
            [gap("unsafe person name")],
            [dict(gap("a"), linked_family_count=True)],
        ):
            with self.assertRaises(ValueError):
                run(*variant)

    def test_empty_and_unchanging_gap_has_no_work(self):
        result = run()
        self.assertEqual(result["decisions"], [])
        self.assertEqual(result["active_research"], 0)
        self.assertFalse(result["external_research_executed"])


if __name__ == "__main__":
    unittest.main()
