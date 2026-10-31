"""Cross-domain adversarial generalization controls for Concept Family discovery.

All records are invented, public-safe structural fixtures, NOT semantic truths.
They test whether an evidence update can change a proposed scope *without* an
automatic claim of mastery, causality, publication, or validated agent learning.

Author-generated cross-domain cases are NOT an independent model-unseen holdout.
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_candidate_discovery import discover


SIG = {"from_role": "observed_signal", "to_role": "causal_explanation",
       "missing_bridge_role": "corroborating_evidence"}


def case(cid, family, *, features=("single_signal", "mechanism_unverified"),
         checked="checked", role=None):
    item = {
        "id": cid, "family_id": family,
        "reasoning_signature": copy.deepcopy(SIG),
        "source_ref": "synthetic-public-logic/" + cid,
        "source_check": checked,
        "context_features": list(features)
    }
    if role:
        item["reasoning_signature"]["missing_bridge_role"] = role
    return item


class CrossDomainConceptUpdateTests(unittest.TestCase):
    def setUp(self):
        self.supports = [
            case("network-latency-alert", "software-observability"),
            case("risk-model-score", "financial-model-diagnostics")
        ]
        self.counter = case("traced-root-cause", "hardware-forensics",
                            features=("corroborated_mechanism",))

    def test_shared_roles_never_mean_semantic_truth_or_auto_promotion(self):
        result = discover({"examples": self.supports})
        self.assertEqual(result["proposal_count"], 1)
        self.assertEqual(result["candidate_preflight"][0]["abstracted_by"],
                         "STRUCTURAL_CLUSTER_NOT_SEMANTIC_PROOF")
        self.assertFalse(result["gate"]["results"][0]["promotion_authorized"])
        self.assertEqual(result["promotions_performed"], 0)

    def test_new_counterexample_forces_reconsideration(self):
        before = discover({"examples": self.supports})
        after = discover({"examples": self.supports, "challenges": [self.counter]})
        self.assertEqual(before["gate"]["results"][0]["status"],
                         "PROPOSED_PENDING_INDEPENDENT_QA")
        self.assertEqual(after["gate"]["results"][0]["status"], "HOLD_REVISION_REQUIRED")
        self.assertIn("UNADDRESSED_COUNTEREXAMPLE",
                      after["gate"]["results"][0]["blockers"])
        self.assertEqual(len(after["recursive_scope_refinements"]), 1)
        self.assertFalse(after["recursive_scope_refinements"][0]["promotion_authorized"])

    def test_new_guard_matching_negative_reverses_earlier_scope_proposal(self):
        old = discover({"examples": self.supports, "challenges": [self.counter]})
        breaking = case("same-conditions-counterexample", "different-domain",
                        features=("single_signal", "mechanism_unverified"))
        revised = discover({"examples": self.supports,
                            "challenges": [self.counter, breaking]})
        self.assertEqual(len(old["recursive_scope_refinements"]), 1)
        self.assertEqual(revised["recursive_scope_refinements"], [],
                         "A newly observed same-guard exception must not be hidden")
        self.assertEqual(revised["promotions_performed"], 0)

    def test_missing_source_of_counterexample_cannot_justify_scope(self):
        contrary = copy.deepcopy(self.counter)
        contrary["source_check"] = "unverified"
        result = discover({"examples": self.supports, "challenges": [contrary]})
        self.assertEqual(result["gate"]["results"][0]["status"],
                         "HOLD_REVISION_REQUIRED")
        self.assertEqual(result["recursive_scope_refinements"], [])

    def test_whitespace_alias_cannot_invent_distinct_family(self):
        examples = [case("source-a", "software-observability"),
                    case("source-b", " software-observability ")]
        result = discover({"examples": examples, "challenges": [self.counter]})
        self.assertEqual(result["proposal_count"], 0)
        self.assertEqual(result["recursive_scope_refinements"], [])

    def test_different_required_bridge_must_not_be_unified(self):
        examples = [self.supports[0], case("risk-model-score",
                    "financial-model-diagnostics", role="out_of_sample_validation")]
        result = discover({"examples": examples})
        self.assertEqual(result["proposal_count"], 0)

    def test_downstream_recheck_is_not_causal_invalidity(self):
        result = discover({
            "examples": self.supports, "challenges": [self.counter],
            "dependencies": [
                {"id": "decision-policy", "depends_on": ["network-latency-alert"]},
                {"id": "retry-strategy", "depends_on": ["decision-policy"]}
            ]
        })
        impacted = result["gate"]["results"][0]["dependency_recheck"]
        # HOLD: no descendants may be automatically invalidated.
        self.assertEqual(impacted, [])
        self.assertEqual(result["promotions_performed"], 0)

    def test_invariance_to_evidence_arrival_order(self):
        packet = {"examples": self.supports, "challenges": [self.counter]}
        backwards = {"examples": list(reversed(self.supports)),
                     "challenges": [self.counter]}
        self.assertEqual(discover(packet), discover(backwards))


if __name__ == "__main__":
    unittest.main()
