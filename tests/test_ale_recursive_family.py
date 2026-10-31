"""Regression tests for bounded recursive Concept Family proposal gate."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_recursive_family import dependency_impact, evaluate


def obs(oid, family, pattern="signal_vs_mechanism", role="support",
        checked=True):
    return {"id": oid, "family_id": family, "pattern": pattern,
            "role": role, "source_ref": "public-test-source/" + oid,
            "source_check": "checked" if checked else "unchecked"}


def proposal(**overrides):
    value = {"id": "meta-signal-vs-mechanism", "label": "Signal is not mechanism",
             "pattern": "signal_vs_mechanism",
             "boundary": "Signals can support but do not alone establish mechanism.",
             "support_ids": ["lab", "imaging"],
             "acknowledged_counterexample_ids": []}
    value.update(overrides)
    return value


def packet(**overrides):
    value = {"observations": [obs("lab", "lab-family"), obs("imaging", "image-family")],
             "proposals": [proposal()],
             "dependencies": [{"id": "clinical-inference", "depends_on": ["lab"]},
                              {"id": "downstream-decision", "depends_on": ["clinical-inference"]}]}
    value.update(overrides)
    return value


class RecursiveFamilyTests(unittest.TestCase):
    def test_cross_family_proposal_only_pending_qa(self):
        original = packet()
        frozen = copy.deepcopy(original)
        result = evaluate(original)
        found = result["results"][0]
        self.assertEqual(found["status"], "PROPOSED_PENDING_INDEPENDENT_QA")
        self.assertFalse(found["promotion_authorized"])
        self.assertEqual(len(found["proposed_links"]), 2)
        self.assertEqual([x["claim_id"] for x in found["dependency_recheck"]],
                         ["clinical-inference", "downstream-decision"])
        self.assertEqual(result["mutations_performed"], 0)
        self.assertEqual(original, frozen)

    def test_repeated_examples_of_same_family_cannot_promote(self):
        data = packet(observations=[obs("lab", "same"), obs("imaging", "same")])
        self.assertIn("INSUFFICIENT_DISTINCT_FAMILIES",
                      evaluate(data)["results"][0]["blockers"])

    def test_word_similarity_not_causal_identity(self):
        data = packet(observations=[obs("lab", "lab-family"),
                                    obs("imaging", "image-family", pattern="different_mechanism")])
        self.assertIn("UNRELATED_OR_NEGATIVE_SUPPORT",
                      evaluate(data)["results"][0]["blockers"])

    def test_unverified_source_is_hold(self):
        data = packet(observations=[obs("lab", "lab-family", checked=False),
                                    obs("imaging", "image-family")])
        self.assertIn("SUPPORT_SOURCE_NOT_CHECKED",
                      evaluate(data)["results"][0]["blockers"])

    def test_counterexample_must_be_seen(self):
        data = packet(observations=[obs("lab", "lab-family"), obs("imaging", "image-family"),
                                    obs("edge-case", "other", role="counterexample")])
        found = evaluate(data)["results"][0]
        self.assertEqual(found["status"], "HOLD_REVISION_REQUIRED")
        self.assertEqual(found["unaddressed_counterexamples"], ["edge-case"])

    def test_acknowledged_counterexample_needs_independent_qa(self):
        data = packet(observations=[obs("lab", "lab-family"), obs("imaging", "image-family"),
                                    obs("edge-case", "other", role="counterexample")],
                      proposals=[proposal(acknowledged_counterexample_ids=["edge-case"])])
        found = evaluate(data)["results"][0]
        self.assertEqual(found["status"], "CHALLENGED_PENDING_INDEPENDENT_QA")
        self.assertFalse(found["promotion_authorized"])

    def test_false_acknowledgement_is_rejected(self):
        data = packet(proposals=[proposal(acknowledged_counterexample_ids=["lab"])])
        self.assertIn("INVALID_COUNTEREXAMPLE_ACKNOWLEDGEMENT",
                      evaluate(data)["results"][0]["blockers"])

    def test_missing_case_is_hold_not_exception_or_fake_evidence(self):
        data = packet(proposals=[proposal(support_ids=["lab", "ghost"])])
        self.assertIn("UNKNOWN_EVIDENCE_ID", evaluate(data)["results"][0]["blockers"])

    def test_bounded_recursive_impact_handles_cycles(self):
        nodes = [{"id": "a", "depends_on": ["start", "c"]},
                 {"id": "b", "depends_on": ["a"]},
                 {"id": "c", "depends_on": ["b"]},
                 {"id": "d", "depends_on": ["c"]}]
        impacted = dependency_impact(["start"], nodes, max_depth=3)
        self.assertEqual([x["claim_id"] for x in impacted], ["a", "b", "c"])
        self.assertTrue(all(x["action"] == "RECHECK_NOT_AUTO_INVALIDATE" for x in impacted))

    def test_duplicate_ids_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "duplicate observation"):
            evaluate(packet(observations=[obs("lab", "a"), obs("lab", "b")]))


if __name__ == "__main__":
    unittest.main()
