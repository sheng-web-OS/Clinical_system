"""Synthetic-only regression tests for adaptive stage selection."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from ale_adaptive_stages import choose


def packet(**overrides):
    p={"classification":"PUBLIC_SYNTHETIC_ONLY", "concept_id":"example-concept",
       "stages":[{"id":"phenomenon","mode":"MCQ","requires":[]},
                 {"id":"mechanism","mode":"CLOZE","requires":["phenomenon"]},
                 {"id":"transfer","mode":"TRANSFER","requires":["mechanism"]}],
       "evidence":[],"review_day":0}
    p.update(overrides)
    return p


def ev(stage,day=0,item="item-a",outcome="PASS",confidence="CONFIDENT",**flags):
    e={"event_id":f"event-{stage}-{day}-{item}","stage_id":stage,"item_id":item,
       "day_index":day,"outcome":outcome,"confidence":confidence,
       "unhinted":True,"learner_unseen":True,"reasoning_supported":True,
       "source_verified":True,"answer_exposed_before":False}
    e.update(flags)
    return e


class StageSelectionTests(unittest.TestCase):
    def test_first_question_when_no_evidence(self):
        r=choose(packet())
        self.assertEqual(r['decision']['stage_id'],'phenomenon')
        self.assertTrue(all(x['status']=='NOT_OBSERVED' for x in r['stage_states'].values()))

    def test_skip_proven_prerequisite_without_marking_untested_as_pass(self):
        r=choose(packet(evidence=[ev('phenomenon')]))
        self.assertEqual(r['decision']['stage_id'],'mechanism')
        self.assertEqual(r['stage_states']['transfer']['status'],'NOT_OBSERVED')

    def test_failed_transfer_rechecks_unobserved_mechanism_first(self):
        r=choose(packet(evidence=[ev('phenomenon'),ev('transfer',outcome='FAIL')]))
        self.assertEqual(r['decision']['stage_id'],'mechanism')
        self.assertEqual(r['decision']['reason_code'],'CHECK_UNSUPPORTED_PREREQUISITE')

    def test_failed_transfer_after_prereq_pass_rechecks_transfer(self):
        r=choose(packet(evidence=[ev('phenomenon'),ev('mechanism'),ev('transfer',outcome='FAIL')]))
        self.assertEqual(r['decision']['stage_id'],'transfer')

    def test_guessed_correct_not_mastered(self):
        r=choose(packet(evidence=[ev('phenomenon',confidence='GUESS')]))
        self.assertEqual(r['stage_states']['phenomenon']['status'],'WEAK_PASS_NEEDS_DIAGNOSIS')
        self.assertEqual(r['decision']['stage_id'],'phenomenon')

    def test_hint_or_exposed_answer_weakens_correct_answer(self):
        for flags in ({'unhinted':False},{'answer_exposed_before':True},{'source_verified':False},{'reasoning_supported':False}):
            with self.subTest(flags=flags):
                r=choose(packet(evidence=[ev('phenomenon',**flags)]))
                self.assertEqual(r['stage_states']['phenomenon']['status'],'WEAK_PASS_NEEDS_DIAGNOSIS')

    def test_delayed_needs_new_unseen_item_and_elapsed_day(self):
        a=ev('phenomenon',day=0)
        b=ev('phenomenon',day=3,item='item-b')
        r=choose(packet(evidence=[a,b],review_day=3))
        self.assertEqual(r['stage_states']['phenomenon']['status'],'DELAYED_PASS_OBSERVED')
        c=ev('phenomenon',day=3,item='item-c')
        r=choose(packet(evidence=[a,c],review_day=3))
        self.assertEqual(r['stage_states']['phenomenon']['status'],'DELAYED_PASS_OBSERVED')
        r=choose(packet(evidence=[a,ev('phenomenon',day=3,item='item-a')],review_day=3))
        self.assertEqual(r['stage_states']['phenomenon']['status'],'NEAR_PASS_OBSERVED')

    def test_all_near_pass_same_day_deferred(self):
        e=[ev(s) for s in ['phenomenon','mechanism','transfer']]
        r=choose(packet(evidence=e))
        self.assertEqual(r['decision']['action'],'DEFER_TO_ANKI_FSRS')

    def test_next_day_probe_prefers_higher_level(self):
        e=[ev(s) for s in ['phenomenon','mechanism','transfer']]
        r=choose(packet(evidence=e,review_day=1))
        self.assertEqual(r['decision']['stage_id'],'transfer')
        self.assertEqual(r['decision']['reason_code'],'DELAYED_UNSEEN_TRANSFER_PROBE')

    def test_recent_failure_overrides_prior_pass(self):
        events=[ev('phenomenon',day=0),ev('phenomenon',day=1,item='item-b',outcome='FAIL')]
        r=choose(packet(evidence=events,review_day=1))
        self.assertEqual(r['stage_states']['phenomenon']['status'],'OBSERVED_GAP')

    def test_unverified_or_anki_only_event_cannot_be_injected(self):
        bad=packet(evidence=[{'anki_rating':'Hard'}])
        with self.assertRaises(ValueError):choose(bad)
        bad=packet(classification='OWNER_PRIVATE')
        with self.assertRaises(ValueError):choose(bad)

    def test_invalid_dependency_and_duplicate_event_fail_closed(self):
        bad=packet(stages=[{'id':'transfer','mode':'MCQ','requires':['missing']}])
        with self.assertRaises(ValueError):choose(bad)
        with self.assertRaises(ValueError):choose(packet(evidence=[ev('phenomenon'),ev('phenomenon')]))

    def test_future_event_rejected_and_input_immutable(self):
        original=packet(evidence=[ev('phenomenon')]); frozen=copy.deepcopy(original)
        self.assertEqual(choose(original)['anki_or_sheet_mutations'],0)
        self.assertEqual(original,frozen)
        with self.assertRaises(ValueError):choose(packet(evidence=[ev('phenomenon',day=2)]))


if __name__=='__main__':unittest.main()
