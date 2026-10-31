"""Synthetic-only evidence join checks, no owner data or network."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_concept_evidence_audit import inspect_evidence

KEY = "anki-revlog:2000000000000:812001"


def event(card="812001", note="910001", family=""):
    return [KEY, "2033-05-18T00:00:00+00:00", card, note, family, "3",
            "UNKNOWN", "NOT_COLLECTED", "", "NOT_DIAGNOSED", "",
            "2000000000000", "SYNCED_READ_ONLY", "2033-05-18T00:00:01+00:00"]


def mapping(card="812001", note="910001", concept="synthetic-concept-1",
            state="OWNER_CONFIRMED_SINGLE_CARD"):
    return ["", note, card, concept, "OWNER_CONFIRMED_LOCAL",
            "TESTS_THIS_CARD_DIRECTION_ONLY", "ACTIVE_MAPPING_PROPOSAL",
            "OWNER_VERIFIED_ANKI_QUESTION_LOCALLY", KEY,
            "2033-05-18T00:00:02+00:00", state]


class EvidenceJoinTests(unittest.TestCase):
    def test_real_identity_only_recall_not_mastery(self):
        r = inspect_evidence([event()], [mapping()], ["synthetic-concept-1"])
        self.assertEqual(r["mapped_recall_only"], 1)
        self.assertEqual(r["unseen_transfer_passes_verified"], 0)
        self.assertEqual(r["causal_diagnoses_verified"], 0)
        self.assertEqual(r["concept_mastery_upgrades"], 0)
        self.assertEqual(r["anki_mutations"], 0)

    def test_unconfirmed_draft_not_linked(self):
        r = inspect_evidence([event()], [mapping(state="YES_FOR_INTERNAL_DRAFT_ONLY")],
                             ["synthetic-concept-1"])
        self.assertEqual(r["unmapped"], 1)
        self.assertEqual(r["mapped_recall_only"], 0)

    def test_unmatched_card_refuses_inference(self):
        r = inspect_evidence([event()], [mapping(card="999999")],
                             ["synthetic-concept-1"])
        self.assertEqual(r["recommendation"], "MAPPING_REQUIRED")

    def test_current_note_mismatch_blocks(self):
        with self.assertRaisesRegex(RuntimeError, "conflicts"):
            inspect_evidence([event(note="910002")], [mapping()],
                             ["synthetic-concept-1"])

    def test_conflicting_confirmed_mappings_block(self):
        with self.assertRaisesRegex(RuntimeError, "Conflicting"):
            inspect_evidence([event()], [mapping(),
                                          mapping(concept="synthetic-concept-2")],
                             ["synthetic-concept-1", "synthetic-concept-2"])


    def test_identical_confirmed_duplicate_is_not_two_independent_observations(self):
        with self.assertRaisesRegex(RuntimeError, "Duplicate confirmed"):
            inspect_evidence([event()], [mapping(), mapping()],
                             ["synthetic-concept-1"])

    def test_different_directions_cannot_be_assumed(self):
        second = event(card="812002")
        second[0] = "anki-revlog:2000000000001:812002"
        second[11] = "2000000000001"
        r = inspect_evidence([event(), second], [mapping()],
                             ["synthetic-concept-1"])
        self.assertEqual((r["mapped_recall_only"], r["unmapped"]), (1, 1))

    def test_deleted_note_is_not_automapped(self):
        r = inspect_evidence([event(note="")], [mapping()],
                             ["synthetic-concept-1"])
        self.assertEqual(r["missing_note_identity"], 1)

    def test_legacy_family_cell_not_automatically_equivalent_to_concept(self):
        r = inspect_evidence([event(family="synthetic-parent-family")],
                             [mapping()], ["synthetic-concept-1"])
        self.assertEqual(r["family_relation_needs_verification"], 1)
        self.assertEqual(r["concept_mastery_upgrades"], 0)

    def test_broken_event_identity_refused(self):
        e = event()
        e[11] = "999999"
        with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
            inspect_evidence([e], [mapping()], ["synthetic-concept-1"])

    def test_unknown_taxonomy_concept_refused(self):
        with self.assertRaisesRegex(RuntimeError, "unrecognized concept"):
            inspect_evidence([event()], [mapping(concept="unknown")],
                             ["synthetic-concept-1"])

    def test_all_identity_ids_stay_out_of_report(self):
        r = inspect_evidence([event()], [mapping()], ["synthetic-concept-1"])
        self.assertNotIn("812001", str(r))
        self.assertNotIn("910001", str(r))
        self.assertNotIn("synthetic-concept-1", str(r))


if __name__ == "__main__":
    unittest.main()
