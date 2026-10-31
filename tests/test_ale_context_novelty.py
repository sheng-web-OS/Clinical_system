"""Regression tests for public-only, lexical, non-promoting context delta audit."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_context_novelty import compare_texts

ARTICLE = "content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md"


def case(id_, marker, source="pmid_19615844"):
    return {"id": id_, "source_ids": [source],
            "markers": [marker], "hypothesis_status": "UNVERIFIED_CANDIDATE"}


def run(atlas, article, *items):
    packet = {"source_classification": "PUBLIC_SOURCE_LINKED",
              "article_path": ARTICLE, "candidates": list(items)}
    return compare_texts(packet, atlas, article)


class ContextNoveltyTests(unittest.TestCase):
    def test_existing_deep_content_not_called_new_concept(self):
        out = run("SpO2 estimates saturation", "COHb calls for co-oximetry",
                  case("cohb-validity", "COHb"))
        row = out["candidates"][0]
        self.assertEqual(row["status"], "ARTICLE_MENTION_ATLAS_ABSENT")
        self.assertFalse(row["new_concept_proven"])
        self.assertEqual(out["concept_promotions"], 0)

    def test_both_covers_marker_only_not_semantic_equivalence(self):
        out = run("Blood has Hb", "Hb can be measured", case("hemoglobin", "Hb"))
        self.assertEqual(out["candidates"][0]["status"], "BOTH_MENTIONED")
        self.assertFalse(out["candidates"][0]["source_truth_verified"])

    def test_source_only_is_not_proven_to_be_a_gap(self):
        out = run("oxygen", "oxygen", case("brand", "co-oximetry"))
        self.assertEqual(out["candidates"][0]["status"],
                         "SOURCE_ONLY_MARKER_CANDIDATE")
        self.assertFalse(out["candidates"][0]["new_concept_proven"])

    def test_atlas_only_signals_possible_location_mismatch(self):
        out = run("COHb", "oxygen", case("location", "COHb"))
        self.assertEqual(out["candidates"][0]["status"],
                         "ATLAS_MENTION_DEEP_LESSON_ABSENT")

    def test_no_arbitrary_private_path_or_note(self):
        packet = {"source_classification": "PUBLIC_SOURCE_LINKED",
                  "article_path": "../../private.md",
                  "candidates": [case("one", "COHb")]}
        with self.assertRaisesRegex(ValueError, "lesson path"):
            compare_texts(packet, "", "")
        packet["article_path"] = ARTICLE
        packet["private_note"] = "do not process"
        with self.assertRaisesRegex(ValueError, "packet"):
            compare_texts(packet, "", "")

    def test_no_urls_or_free_text_in_markers(self):
        with self.assertRaisesRegex(ValueError, "search markers"):
            run("", "", case("unsafe", "https://docs.google.com/secret"))
        with self.assertRaisesRegex(ValueError, "source IDs"):
            run("", "", case("unsafe", "COHb", "https://my-private-sheet"))

    def test_cannot_declare_medical_validation(self):
        row=case("claim", "COHb")
        row["hypothesis_status"]="VALIDATED"
        with self.assertRaisesRegex(ValueError,"semantic status"):
            run("", "", row)

    def test_determinism_and_no_promotion(self):
        a=run("SpO2", "co-oximetry", case("candidate", "co-oximetry"))
        b=run("SpO2", "co-oximetry", case("candidate", "co-oximetry"))
        self.assertEqual(a,b)
        self.assertFalse(a["modified_public_content"])


if __name__ == "__main__":
    unittest.main()
