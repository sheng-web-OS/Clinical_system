"""Negative controls for unlabelled public-source Q0 extraction."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from ale_raw_q0_probe import extract

def packet(text):
    return {"source_classification":"PUBLIC_SOURCE_EXCERPT",
            "source_ref":"pmid_41485812","excerpt":text}

class RawQ0Tests(unittest.TestCase):
    def test_unlabelled_guideline_fragment_proposes_q0_not_concept(self):
        x=extract(packet("Limited available iron for erythropoiesis despite adequate iron stores."))
        self.assertEqual(x["decision"],"ASK_ONE_Q0_PENDING_Q2_Q3")
        self.assertEqual(x["top_candidate"]["cue"],"APPARENT_CONTRAST")
        self.assertIn("despite adequate iron stores",x["top_candidate"]["exact_evidence"])
        self.assertFalse(x["concept_ids_received"])
        self.assertFalse(x["concept_promotions"])
        self.assertFalse(x["top_candidate"]["concept_novelty_verified"])

    def test_routine_descriptive_text_abstains(self):
        x=extract(packet("This figure describes several laboratory measures used to evaluate different states of iron availability."))
        self.assertEqual(x["decision"],"ABSTAIN_NO_BOUNDARY_CUE")
        self.assertIsNone(x["top_candidate"])

    def test_failing_method_but_no_causal_merge(self):
        x=extract(packet("Ferritin alone does not establish the amount of iron available for bone marrow erythropoiesis."))
        self.assertEqual(x["top_candidate"]["cue"],"INFERENCE_BOUNDARY")
        self.assertFalse(x["top_candidate"]["concept_relation_inferred"])

    def test_phrase_not_domain_specific(self):
        x=extract(packet("The algorithm cannot be applied unless the diagnosis and patient population are explicitly defined."))
        self.assertEqual(x["top_candidate"]["cue"],"INFERENCE_BOUNDARY")
        self.assertEqual(x["source_ref"],"pmid_41485812")

    def test_nomenclature_shift_raises_question_not_promotion(self):
        x=extract(packet("The entity was historically termed functional iron deficiency instead of iron restricted erythropoiesis."))
        self.assertEqual(x["top_candidate"]["cue"],"RECLASSIFICATION_SIGNAL")
        self.assertEqual(x["concept_promotions"],0)

    def test_publishing_metadata_false_positive_suppressed(self):
        x=extract(packet("Despite the page count, the report was published online without the supplementary index."))
        self.assertEqual(x["decision"],"ABSTAIN_NO_BOUNDARY_CUE")

    def test_no_label_or_private_data():
        p=packet("Despite variable observations, the laboratory result may not map directly to the diagnostic concept.")
        p["importance"]="CRITICAL"
        with self.assertRaisesRegex(ValueError,"packet"):
            extract(p)
        p.pop("importance")
        p["source_classification"]="OWNER_PRIVATE"
        with self.assertRaisesRegex(ValueError,"private"):
            extract(p)

    def test_reject_pii_hints_urls_and_freeform_credentials(self):
        for text in ("See https://example.com for the evidence.",
                     "The password may be displayed here despite safeguards.",
                     "Patient ID number can be seen despite this." ):
            if len(text)>=24:
                with self.assertRaises(ValueError):extract(packet(text))

    def test_input_exact_span_and_stable_priority(self):
        text=("The team measured red cell indices. "
              "Limited circulating iron availability despite adequate total storage reserves. "
              "Evaluation depends on the clinical population.")
        a=extract(packet(text))
        b=extract(packet(text))
        self.assertEqual(a,b)
        for row in a["candidates"]:
            self.assertEqual(text[row["start_char"]:row["end_char"]],
                             row["exact_evidence"])
        self.assertEqual(a["top_candidate"]["cue"],"APPARENT_CONTRAST")

    def test_no_cue_does_not_force_a_question(self):
        x=extract(packet("Iron is required for the production of functional hemoglobin in circulating red blood cells."))
        self.assertEqual(x["candidates"],[])
        self.assertFalse(x["medical_semantics_verified"])

    def test_reclass_and_contrast_can_coexist_without_overclaim(self):
        x=extract(packet("The old category was historically termed functional deficiency despite adequate iron stores."))
        self.assertEqual(x["top_candidate"]["cue"],"APPARENT_CONTRAST")
        self.assertGreaterEqual(x["top_candidate"]["cue_count"],2)

if __name__ == "__main__":
    unittest.main()
