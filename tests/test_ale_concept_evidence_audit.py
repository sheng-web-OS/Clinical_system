"""Synthetic-only evidence join checks, no owner data or network."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_concept_evidence_audit import inspect_evidence, inspect_remote, MAP_HEADER

KEY = "anki-revlog:2000000000000:812001"


def event(card="812001", note="910001", family=""):
    return [KEY, "2033-05-18T03:33:20+00:00", card, note, family, "3",
            "UNKNOWN", "NOT_COLLECTED", "", "NOT_DIAGNOSED", "",
            "2000000000000", "SYNCED_READ_ONLY", "2033-05-18T03:33:21+00:00"]


def mapping(card="812001", note="910001", concept="synthetic-concept-1",
            state="OWNER_CONFIRMED_SINGLE_CARD"):
    return ["", note, card, concept, "OWNER_CONFIRMED_LOCAL",
            "TESTS_THIS_CARD_DIRECTION_ONLY", "ACTIVE_MAPPING_PROPOSAL",
            "OWNER_VERIFIED_ANKI_QUESTION_LOCALLY", KEY,
            "2033-05-18T03:33:22+00:00", state]


class EvidenceJoinTests(unittest.TestCase):
    def test_real_identity_only_recall_not_mastery(self):
        r = inspect_evidence([event()], [mapping()], ["synthetic-concept-1"])
        self.assertEqual(r["retrospective_concept_links"], 1)
        self.assertEqual(r["mapped_recall_only"], 0)
        self.assertEqual(r["verified_historical_concept_recall"], 0)
        self.assertEqual(r["unseen_transfer_passes_verified"], 0)
        self.assertEqual(r["causal_diagnoses_verified"], 0)
        self.assertEqual(r["concept_mastery_upgrades"], 0)
        self.assertEqual(r["anki_mutations"], 0)

    def test_unconfirmed_draft_not_linked(self):
        r = inspect_evidence([event()], [mapping(state="YES_FOR_INTERNAL_DRAFT_ONLY")],
                             ["synthetic-concept-1"])
        self.assertEqual(r["unmapped"], 1)
        self.assertEqual(r["mapped_recall_only"], 0)

    def test_confirmed_wrong_card_anchor_is_a_blocking_integrity_error(self):
        with self.assertRaisesRegex(RuntimeError, "wrong source-review anchor"):
            inspect_evidence([event()], [mapping(card="999999")],
                             ["synthetic-concept-1"])

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
        self.assertEqual((r["retrospective_concept_links"], r["unmapped"]), (1, 1))

    def test_deleted_note_is_not_automapped(self):
        with self.assertRaisesRegex(RuntimeError, "anchor note identity mismatch"):
            inspect_evidence([event(note="")], [mapping()],
                             ["synthetic-concept-1"])

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


    def test_owner_local_sheet_adapter_is_read_only(self):
        class FakePrivateSheet:
            def __init__(self):
                self.calls = []
            def verify_schema(self):
                self.calls.append("verify_schema")
            def get(self, a1):
                self.calls.append(a1)
                return {
                    "Error_Events!A2:N": [event()],
                    "Card_Concept_Map!A1:K1": [MAP_HEADER],
                    "Card_Concept_Map!A2:K": [mapping()],
                    "Concepts!A1:J1": [["concept_id", "domain"]],
                    "Concepts!A2:J": [["synthetic-concept-1", "clinical"]],
                }[a1]
        sh = FakePrivateSheet()
        r = inspect_remote(sh)
        self.assertEqual(r["retrospective_concept_links"], 1)
        self.assertEqual(r["mapped_recall_only"], 0)
        self.assertEqual(r["anki_mutations"], 0)
        self.assertEqual(sh.calls.count("Error_Events!A2:N"), 2)
        self.assertFalse(any("append" in c.lower() for c in sh.calls))

    def test_a_card_reused_for_another_review_is_not_assumed_same_question(self):
        older = event()
        older[0] = "anki-revlog:1999999999999:812001"
        older[11] = "1999999999999"
        later = event()
        result = inspect_evidence([older, later], [mapping()], ["synthetic-concept-1"])
        self.assertEqual(result["retrospective_concept_links"], 1)
        self.assertEqual(result["other_review_without_versioned_context"], 1)
        self.assertEqual(result["verified_historical_concept_recall"], 0)

    def test_anchor_must_be_present_in_actual_reviews(self):
        with self.assertRaisesRegex(RuntimeError, "anchor absent"):
            inspect_evidence([], [mapping()], ["synthetic-concept-1"])

    def test_claimed_mapping_source_without_local_attestation_is_rejected(self):
        m = mapping()
        m[7] = "MODEL_GUESSED_FROM_TAGS"
        with self.assertRaisesRegex(RuntimeError, "semantic attestation"):
            inspect_evidence([event()], [m], ["synthetic-concept-1"])

    def test_mapping_before_review_time_is_invalid(self):
        m = mapping()
        m[9] = "2033-05-17T00:00:00+00:00"
        with self.assertRaisesRegex(RuntimeError, "confirmed before"):
            inspect_evidence([event()], [m], ["synthetic-concept-1"])

    def test_review_timestamp_mismatch_rejected(self):
        e = event()
        e[1] = "2033-05-18T00:00:00+00:00"
        with self.assertRaisesRegex(RuntimeError, "timestamp does not match"):
            inspect_evidence([e], [mapping()], ["synthetic-concept-1"])

    def test_mapping_to_a_different_review_event_refused(self):
        m = mapping()
        m[8] = "anki-revlog:2000000000010:812001"
        with self.assertRaisesRegex(RuntimeError, "anchor absent"):
            inspect_evidence([event()], [m], ["synthetic-concept-1"])

    def test_all_identity_ids_stay_out_of_report(self):
        r = inspect_evidence([event()], [mapping()], ["synthetic-concept-1"])
        self.assertNotIn("812001", str(r))
        self.assertNotIn("910001", str(r))
        self.assertNotIn("synthetic-concept-1", str(r))


if __name__ == "__main__":
    unittest.main()
