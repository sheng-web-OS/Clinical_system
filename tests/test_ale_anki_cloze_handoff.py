"""Public-safe synthetic checks of graph-preview -> HOLD-only Cloze queue adapter."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ale_anki_import_queue as q
import ale_anki_cloze_handoff as h


def preview():
    text = ("In this decision context, first examine {{c1::alpha::first}} and "
            "{{c1::beta::second}}; then test {{c2::gamma::third}} separately.")
    return {
        "note_type": "Cloze",
        "text": text,
        "card_groups": [1, 2],
        "card_count": 2,
        "masked_fronts_for_review": h.masked_fronts(text, [1, 2]),
        "concept_family_id": "CF_SYNTHETIC",
        "edge_id": "E_SYNTHETIC",
        "scope_boundary_for_reviewer": "This synthetic relation is not medical evidence.",
        "semantic_acceptance": "PENDING_INDEPENDENT_REVIEW",
        "ready_to_import": False,
        "source_verified": False,
        "semantic_quality_verified": False,
    }


def hold(p=None):
    return h.candidate_hold_row(
        preview() if p is None else p,
        card_key="CLOZE-HOLD-01",
        deck="ClinicalOS::ALE",
        tags=["ale::candidate", "synthetic"],
        source_url="https://pubmed.ncbi.nlm.nih.gov/12345678/",
    )


class TestHandoff(unittest.TestCase):
    def test_real_graph_preview_shape_can_create_hold_not_ready(self):
        result = hold()
        self.assertEqual(set(result), set(q.HEADER))
        self.assertEqual((result["qa_status"], result["release_status"],
                          result["import_status"]),
                         ("PENDING_INDEPENDENT_MEDICAL_QA", "HOLD", "HOLD"))
        self.assertEqual(result["content_sha256"],
                         q.digest(result["front_html"], result["back_html"]))
        self.assertEqual(q.note_payload(result["front_html"], result["back_html"])[0],
                         "Cloze")
        with self.assertRaises(ValueError):
            q.validate_ready(result)

    def test_masking_keeps_other_group_visible(self):
        p = preview()
        self.assertIn("[first]", p["masked_fronts_for_review"]["1"])
        self.assertIn("[second]", p["masked_fronts_for_review"]["1"])
        self.assertIn("gamma", p["masked_fronts_for_review"]["1"])
        self.assertIn("[third]", p["masked_fronts_for_review"]["2"])
        self.assertIn("alpha", p["masked_fronts_for_review"]["2"])

    def test_fake_approval_or_missing_graph_rejected(self):
        for key, wrong in (
            ("ready_to_import", True),
            ("semantic_acceptance", "PASS"),
            ("source_verified", True),
            ("concept_family_id", ""),
            ("scope_boundary_for_reviewer", ""),
            ("note_type", "Basic"),
        ):
            p = preview()
            p[key] = wrong
            with self.subTest(key=key), self.assertRaises(ValueError):
                hold(p)

    def test_preview_tampering_or_sibling_mismatch_rejected(self):
        for key, wrong in (
            ("masked_fronts_for_review", {"1": "[...]"}),
            ("card_groups", [1]),
            ("card_count", 1),
        ):
            p = preview()
            p[key] = wrong
            with self.subTest(key=key), self.assertRaises(ValueError):
                hold(p)

    def test_untrusted_source_or_bad_card_key_rejected(self):
        p = preview()
        with self.assertRaises(ValueError):
            h.candidate_hold_row(p, card_key="bad", deck="ClinicalOS::ALE",
                                  tags=["safe"], source_url="https://pubmed.ncbi.nlm.nih.gov/12345678/")
        with self.assertRaises(ValueError):
            h.candidate_hold_row(p, card_key="CLOZE-HOLD-01", deck="ClinicalOS::ALE",
                                  tags=["safe"], source_url="https://evil.example.com/source")

    def test_hold_never_written_by_importer(self):
        # The read-only candidate adapter cannot smuggle a private Draft into
        # the existing opted-in importer by changing only one status field.
        row = hold()
        row["import_status"] = "PENDING"
        with patch.object(q, "local_anki", side_effect=AssertionError("No Anki calls")):
            class MinimalSheet:
                def get(self, a1):
                    if a1 == q.TAB + "!A1:L1": return [q.HEADER]
                    if a1 == q.TAB + "!A2:L": return [[row[k] for k in q.HEADER]]
                    raise AssertionError(a1)
            self.assertEqual(q.process(MinimalSheet()), (0, 0))


if __name__ == "__main__":
    unittest.main()
