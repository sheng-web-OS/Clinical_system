"""Public-safe synthetic tests for Cloze-first ALE preview (not medical QA)."""
import unittest

from tools.ale_cloze_preview import render_cloze_proposal


def proposal():
    return {
        "concept_family_id": "synthetic_family",
        "concept_node_id": "synthetic_relation",
        "tested_relation": "conditional_dependency",
        "learning_goal": "Retrieve two linked pieces of a fictional machine model.",
        "source_refs": ["synthetic_fixture_v1"],
        "context": "Context: a fictional machine in mode A.",
        "template": "The controller [[first]] so the valve [[second]].",
        "why_together": "One coherent cause-to-effect relation.",
        "slots": [
            {"key": "first", "group": 1, "answer": "activates", "hint": "controller action"},
            {"key": "second", "group": 1, "answer": "opens", "hint": "valve response"},
        ],
    }


class TestClozePreview(unittest.TestCase):
    def test_two_deletions_one_card_same_group(self):
        result = render_cloze_proposal(proposal())
        self.assertEqual(result["note_type"], "Cloze")
        self.assertEqual(result["card_count"], 1)
        self.assertEqual(result["cloze_count"], 2)
        self.assertIn("{{c1::activates::controller action}}", result["text"])
        self.assertIn("{{c1::opens::valve response}}", result["text"])
        self.assertTrue(result["single_card_multi_cloze"])
        self.assertFalse(result["semantic_quality_verified"])
        self.assertFalse(result["source_verified"])
        self.assertFalse(result["anki_mutated"])

    def test_distinct_numbers_create_distinct_cards(self):
        p = proposal()
        p["slots"][1]["group"] = 2
        result = render_cloze_proposal(p)
        self.assertEqual(result["card_count"], 2)
        self.assertEqual(result["card_groups"], [1, 2])
        self.assertFalse(result["single_card_multi_cloze"])

    def test_single_cloze_without_hint_can_be_valid(self):
        p = proposal()
        p["template"] = "The controller [[first]] when mode A starts."
        p["slots"] = [p["slots"][0]]
        p["slots"][0].pop("hint")
        p.pop("why_together")
        self.assertIn("{{c1::activates}}", render_cloze_proposal(p)["text"])

    def test_ambiguous_slot_can_explicitly_require_hint(self):
        p = proposal()
        p["slots"][0]["needs_hint"] = True
        p["slots"][0].pop("hint")
        with self.assertRaisesRegex(ValueError, "hint"):
            render_cloze_proposal(p)

    def test_reject_hint_that_leaks_answer(self):
        p = proposal()
        p["slots"][0]["hint"] = "activates the switch"
        with self.assertRaisesRegex(ValueError, "reveals"):
            render_cloze_proposal(p)

    def test_multi_cloze_requires_shared_concept_rationale(self):
        p = proposal()
        p.pop("why_together")
        with self.assertRaisesRegex(ValueError, "coherence"):
            render_cloze_proposal(p)

    def test_reject_missing_visible_context(self):
        p = proposal()
        p["context"] = ""
        with self.assertRaisesRegex(ValueError, "context"):
            render_cloze_proposal(p)

    def test_reject_unresolved_or_duplicated_slot(self):
        p = proposal()
        p["template"] += " [[unknown]]"
        with self.assertRaisesRegex(ValueError, "once"):
            render_cloze_proposal(p)
        p = proposal()
        p["template"] += " [[first]]"
        with self.assertRaisesRegex(ValueError, "once"):
            render_cloze_proposal(p)

    def test_reject_invalid_group_and_source_omission(self):
        p = proposal()
        p["slots"][0]["group"] = 0
        with self.assertRaisesRegex(ValueError, "positive"):
            render_cloze_proposal(p)
        p = proposal()
        p["source_refs"] = []
        with self.assertRaisesRegex(ValueError, "references"):
            render_cloze_proposal(p)

    def test_reject_context_with_hidden_deletions(self):
        p = proposal()
        p["context"] = "Context: {{c1::mode A}}"
        with self.assertRaisesRegex(ValueError, "visible"):
            render_cloze_proposal(p)

    def test_preview_hides_all_same_group_blanks(self):
        result = render_cloze_proposal(proposal())
        f = result["masked_fronts_for_review"]["1"]
        self.assertIn("[controller action]", f)
        self.assertIn("[valve response]", f)
        self.assertNotIn("activates", f)
        self.assertNotIn("opens", f)
        self.assertIn("fictional machine in mode A", f)

    def test_other_group_remains_readable_in_front(self):
        p = proposal()
        p["slots"][1]["group"] = 2
        result = render_cloze_proposal(p)
        front1 = result["masked_fronts_for_review"]["1"]
        front2 = result["masked_fronts_for_review"]["2"]
        self.assertIn("[controller action]", front1)
        self.assertIn("opens", front1)
        self.assertIn("activates", front2)
        self.assertIn("[valve response]", front2)

    def test_no_hidden_anki_mutation_or_semantic_approval(self):
        r = render_cloze_proposal(proposal())
        self.assertIn("PENDING_SEMANTIC", r["status"])
        self.assertEqual(r["card_count"], 1)


if __name__ == "__main__":
    unittest.main()
