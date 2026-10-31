"""Structural smoke for public source-linked ALE cross-domain conceptual challenge.

This checks deterministic routing/status only, NOT the external sources' semantic
truth, source independence, model generalization or learner benefit.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from ale_candidate_discovery import discover


class PublicCrossDomainEvidenceProbe(unittest.TestCase):
    def test_proxy_vs_decision_cannot_be_promoted_when_challenged(self):
        path = ROOT / "experiments" / "ale-cross-domain-proxy-vs-decision-20261031.json"
        packet = json.loads(path.read_text(encoding="utf-8"))
        out = discover(packet)
        self.assertEqual(out["proposal_count"], 1)
        self.assertEqual(len(out["candidate_preflight"][0]["families"]), 2)
        candidate = out["gate"]["results"][0]
        self.assertEqual(candidate["status"], "HOLD_REVISION_REQUIRED")
        self.assertEqual(len(candidate["unaddressed_counterexamples"]), 2)
        self.assertFalse(candidate["promotion_authorized"])
        self.assertEqual(out["promotions_performed"], 0)
        self.assertEqual(len(out["recursive_scope_refinements"]), 1)
        refinement = out["recursive_scope_refinements"][0]
        self.assertEqual(refinement["required_context_features"],
                         ["decision_target_requires_context"])
        self.assertFalse(refinement["promotion_authorized"])
        self.assertEqual(out["external_model_calls"], 0)
        self.assertFalse(out["personal_state_accessed"])

    def test_source_link_flags_do_not_claim_independent_attestation(self):
        packet = json.loads((ROOT / "experiments" /
                             "ale-cross-domain-proxy-vs-decision-20261031.json")
                            .read_text(encoding="utf-8"))
        self.assertIn("only the author", packet["source_check_caveat"])
        self.assertIn("not independent", packet["provenance"])


if __name__ == "__main__":
    unittest.main()
