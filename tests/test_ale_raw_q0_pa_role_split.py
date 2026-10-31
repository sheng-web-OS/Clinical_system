"""Source-grounded Q0 role-contrast regression from 2025 Endocrine Society PA guideline.

Public excerpt is one short (<25-word) attributed phrase, not model-created
private learning data. Tests detect missing question-level cues, not clinical
truth, human learning, or independent semantic extraction.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_raw_q0_probe import extract

SOURCE = "pmid_40658480"
ROLE_EXCERPT = (
    "Potassium should be measured alongside renin and aldosterone—not for "
    "screening itself but to aid in the accurate interpretation of aldosterone."
)

def source_packet(excerpt):
    return {"source_classification": "PUBLIC_SOURCE_EXCERPT",
            "source_ref": SOURCE, "excerpt": excerpt}


class AldosteronismUnlabelledRoleQuestions(unittest.TestCase):
    def test_actual_public_source_fixture_runs_without_semantic_labels(self):
        import json
        fixture = Path(__file__).resolve().parents[1] / (
            "experiments/ale-pa-2025-raw-role-contrast-20261031.json"
        )
        packet = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(set(packet),
                         {"source_classification", "source_ref", "excerpt"})
        self.assertEqual(packet["source_ref"], SOURCE)
        self.assertEqual(packet["excerpt"], ROLE_EXCERPT)
        result = extract(packet)
        self.assertEqual(result["decision"], "ASK_ONE_Q0_PENDING_Q2_Q3")
        self.assertEqual(result["top_candidate"]["cue"], "MEASUREMENT_ROLE_SPLIT")
        self.assertFalse(result["medical_semantics_verified"])
        self.assertEqual(result["concept_promotions"], 0)

    def test_unlabelled_guideline_role_contrast_proposes_question(self):
        result = extract(source_packet(ROLE_EXCERPT))
        self.assertEqual(result["decision"], "ASK_ONE_Q0_PENDING_Q2_Q3")
        self.assertEqual(result["top_candidate"]["cue"], "MEASUREMENT_ROLE_SPLIT")
        self.assertEqual(result["top_candidate"]["exact_evidence"], ROLE_EXCERPT)
        self.assertFalse(result["top_candidate"]["concept_relation_inferred"])

    def test_generic_inference_role_split_without_predefined_clinical_terms(self):
        result = extract(source_packet(
            "The marker is measured not for determining eligibility but to help interpret the measurement."))
        self.assertEqual(result["top_candidate"]["cue"], "MEASUREMENT_ROLE_SPLIT")
        self.assertFalse(result["medical_semantics_verified"])

    def test_false_low_measurement_prompts_validity_question(self):
        result = extract(source_packet(
            "Low potassium may lead to a falsely low aldosterone measurement in some conditions."))
        self.assertEqual(result["top_candidate"]["cue"], "MEASUREMENT_VALIDITY_RISK")
        self.assertIn("validity", result["top_candidate"]["proposed_q0"])

    def test_false_positive_is_validity_signal_not_diagnosis(self):
        result = extract(source_packet(
            "This experimental setting can produce false positive findings in a laboratory assay."))
        self.assertEqual(result["top_candidate"]["cue"], "MEASUREMENT_VALIDITY_RISK")
        self.assertFalse(result["top_candidate"]["concept_novelty_verified"])

    def test_editorial_not_for_publication_remains_abstain(self):
        result = extract(source_packet(
            "Not for publication but for training distribution; editorial approval remains pending."))
        self.assertEqual(result["decision"], "ABSTAIN_NO_BOUNDARY_CUE")

    def test_plain_measurement_facts_without_contrast_remain_abstain(self):
        result = extract(source_packet(
            "Potassium is measured alongside the aldosterone and renin concentrations in many protocols."))
        self.assertEqual(result["decision"], "ABSTAIN_NO_BOUNDARY_CUE")

    def test_no_concept_labels_or_private_fields_accepted(self):
        p = source_packet(ROLE_EXCERPT)
        p["concept_family"] = "endocrine"
        with self.assertRaises(ValueError):
            extract(p)

    def test_exact_span_and_repeatability(self):
        p = source_packet("Measurement was repeated. " + ROLE_EXCERPT)
        a, b = extract(p), extract(p)
        self.assertEqual(a, b)
        span = a["top_candidate"]
        self.assertEqual(p["excerpt"][span["start_char"]:span["end_char"]],
                         span["exact_evidence"])
        self.assertEqual(a["concept_promotions"], 0)


if __name__ == "__main__":
    unittest.main()
