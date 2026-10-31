import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ale_autonomy_core import persistent_skipped_ids, exact_tag_candidate, choose_next_lesson

EVENT = ['anki-revlog:1700000000000:123', '', '123', '456'] + [''] * 10
CARD = {'cardId': 123, 'note': 456, 'tags': ['ale::concept::renal-mechanism']}

class AutonomyPolicyTests(unittest.TestCase):
    def test_skip_survives_any_catalog_change(self):
        x = {'signature': 'old_catalog', 'skipped_cards': ['123']}
        self.assertEqual(persistent_skipped_ids(x), {'123'})
    def test_corrupt_skip_fails_closed(self):
        with self.assertRaises(ValueError):
            persistent_skipped_ids({'skipped_cards': ['123', None]})
    def test_skip_never_classified_even_if_tag_present(self):
        self.assertIsNone(exact_tag_candidate(EVENT, CARD, {'renal-mechanism'}, {'123'}, set()))
    def test_exact_tag_is_unconfirmed_not_mastery(self):
        r = exact_tag_candidate(EVENT, CARD, {'renal-mechanism'}, set(), set())
        self.assertEqual((r['concept_id'], r['confirmation']), ('renal-mechanism', 'UNCONFIRMED_CANDIDATE'))
    def test_multiple_tags_abstain(self):
        c = dict(CARD, tags=CARD['tags'] + ['ale::concept::ckd-gfr-uacr'])
        self.assertIsNone(exact_tag_candidate(EVENT, c, {'renal-mechanism','ckd-gfr-uacr'},set(),set()))
    def test_no_structured_tag_abstain(self):
        self.assertIsNone(exact_tag_candidate(EVENT, dict(CARD,tags=['Renal']), {'renal-mechanism'},set(),set()))
    def test_invalid_note_never_classified(self):
        event=list(EVENT);event[3]=''
        self.assertIsNone(exact_tag_candidate(event, CARD, {'renal-mechanism'},set(),set()))
    def test_existing_proposal_is_idempotent(self):
        self.assertIsNone(exact_tag_candidate(EVENT,CARD,{'renal-mechanism'},set(),{'123'}))
    def test_preserves_queue_priority_and_source_gate(self):
        concepts=[['ckd-gfr-uacr','renal','','unobserved','','YES','','','','not known']]
        acts=[['1','ckd-gfr-uacr','','original Q02 cold attempt','source check required','','queued'],
              ['2','renal-mechanism','','repair','eligible','','queued']]
        r=choose_next_lesson(concepts,acts)
        self.assertEqual(r['gate'],'VERIFY_SOURCE_BEFORE_COLD_ATTEMPT')
        self.assertEqual(r['learner_gain'],'NOT_MEASURED')
        self.assertEqual(r['status'],'PROPOSED_NOT_COMPLETED')
    def test_observed_reasoning_gap_when_no_queue(self):
        c=[['renal-mechanism','renal','','reasoning_gap','','YES','','','','']]
        self.assertEqual(choose_next_lesson(c,[])['action'],'mechanism_repair_then_unseen_test')
    def test_empty_abstains(self):
        self.assertEqual(choose_next_lesson([],[])['status'],'NO_VERIFIED_NEXT_STEP')

if __name__=='__main__': unittest.main()
