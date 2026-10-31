import copy
import unittest
from ale_graph_policy_bridge import propose

GRAPH = {"classification":"PUBLIC_SYNTHETIC_ONLY","version":1,
         "nodes":[{"id":"interpretation","kind":"INFERENCE","status":"SOURCE_REVIEWED"},
                  {"id":"prerequisite","kind":"INFERENCE","status":"SOURCE_REVIEWED"},
                  {"id":"candidate","kind":"INFERENCE","status":"CANDIDATE"}],
         "edges":[{"from":"interpretation","to":"prerequisite","relation":"REQUIRES","status":"SOURCE_REVIEWED"},
                  {"from":"interpretation","to":"candidate","relation":"RELATED","status":"CANDIDATE"}]}

def obs(finding="INCORRECT_REASONING", basis="COLD_REASONED_ANSWER", target="interpretation", version=1):
    return {"classification":"PUBLIC_SYNTHETIC_ONLY","target_id":target,"graph_version":version,"basis":basis,"finding":finding}

class TestBridge(unittest.TestCase):
    def test_prerequisite_remediation(self):
        x=propose(GRAPH, obs())
        self.assertEqual((x['action'],x['selected_concept_id']),('REPAIR_PREREQUISITE_CANDIDATE','prerequisite'))
        self.assertEqual(x['anki_mutations'],0)
    def test_same_concept_different_observation_card(self):
        self.assertEqual(propose(GRAPH,obs("RETRIEVAL_FAILURE"))['action'],'CARD_CANDIDATE')
    def test_reasoned_pass_requires_transfer(self):
        self.assertEqual(propose(GRAPH,obs("REASONED_PASS"))['action'],'UNSEEN_TRANSFER_TEST')
    def test_transfer_pass_no_card(self):
        self.assertEqual(propose(GRAPH,obs("TRANSFER_PASS"))['action'],'NO_CARD')
    def test_review_and_tag_only_not_semantic_diagnosis(self):
        for basis in ('REVIEW_BUTTON_ONLY','TAG_ONLY'):
            self.assertEqual(propose(GRAPH,obs(basis=basis))['action'],'DIAGNOSTIC_FIRST')
    def test_unverified_node_cannot_be_used(self):
        self.assertEqual(propose(GRAPH,obs(target='candidate'))['action'],'VERIFY_CONCEPT_SOURCE')
    def test_related_is_not_prerequisite(self):
        g=copy.deepcopy(GRAPH);g['edges']=g['edges'][1:]
        self.assertEqual(propose(g,obs())['action'],'DIAGNOSTIC_FIRST')
    def test_graph_change_preserves_evidence(self):
        g=copy.deepcopy(GRAPH);g['version']=2
        self.assertEqual(propose(g,obs())['action'],'RECHECK_VERSIONED_MAPPING')
    def test_unmapped_is_not_forced_to_nearest_tag(self):
        self.assertEqual(propose(GRAPH,obs(target='unknown'))['action'],'UNMAPPED_DIAGNOSTIC_FIRST')
    def test_rejects_private_content_or_extra_fields(self):
        o=obs();o['private_card_html']='<div>content</div>'
        with self.assertRaises(ValueError):propose(GRAPH,o)
        g=copy.deepcopy(GRAPH);g['classification']='OWNER_PRIVATE'
        with self.assertRaises(ValueError):propose(g,obs())
    def test_rejects_dangling_relationship(self):
        g=copy.deepcopy(GRAPH);g['edges'][0]['to']='not_in_graph'
        with self.assertRaises(ValueError):propose(g,obs())
    def test_source_reviewed_role_is_not_independent_medical_qa(self):
        x=propose(GRAPH,obs())
        self.assertFalse(x['caller_evidence_independently_verified'])
        self.assertEqual(x['learner_gain'],'NOT_MEASURED')

if __name__=='__main__':unittest.main()
