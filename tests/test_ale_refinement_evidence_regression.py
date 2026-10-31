"""Adversarial RED controls against false recursive concept-scope proposals.

Public synthetic identifiers only. These are deterministic gate invariants,
not evidence of agent learning or independent semantic truth.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_candidate_discovery import discover


def example(name, family, features=("needs_context",), checked="checked", source=True):
    return {
        "id": name,
        "family_id": family,
        "reasoning_signature": {
            "from_role": "measurement",
            "to_role": "inference",
            "missing_bridge_role": "independent_evidence",
        },
        "source_ref": "test-public/" + name if source else None,
        "source_check": checked,
        "context_features": list(features),
    }


class RecursiveScopeEvidenceRegressions(unittest.TestCase):
    def test_same_family_whitespace_cannot_create_orphan_scoped_candidate(self):
        packet = {
            "examples": [example("one", "family_x"), example("two", " family_x ")],
            "challenges": [example("negative", "family_y", ("different_condition",))],
        }
        result = discover(packet)
        self.assertEqual(result["proposal_count"], 0)
        self.assertEqual(result["recursive_scope_refinements"], [],
                         "Scope repair must never exist without a valid parent proposal")

    def test_unverified_support_cannot_generate_scope_repair(self):
        packet = {
            "examples": [example("one", "family_a", checked="unchecked"),
                         example("two", "family_b")],
            "challenges": [example("negative", "family_c", ("different_condition",))],
        }
        result = discover(packet)
        self.assertIn("SUPPORT_SOURCE_NOT_CHECKED", result["gate"]["results"][0]["blockers"])
        self.assertEqual(result["recursive_scope_refinements"], [])

    def test_missing_support_source_cannot_generate_scope_repair(self):
        packet = {
            "examples": [example("one", "family_a", source=False),
                         example("two", "family_b")],
            "challenges": [example("negative", "family_c", ("different_condition",))],
        }
        result = discover(packet)
        self.assertIn("SUPPORT_SOURCE_NOT_CHECKED", result["gate"]["results"][0]["blockers"])
        self.assertEqual(result["recursive_scope_refinements"], [])

    def test_unverified_counterexample_cannot_define_scope_boundary(self):
        packet = {
            "examples": [example("one", "family_a"), example("two", "family_b")],
            "challenges": [example("negative", "family_c",
                                   ("different_condition",), checked="unchecked")],
        }
        result = discover(packet)
        self.assertEqual(result["gate"]["results"][0]["status"], "HOLD_REVISION_REQUIRED")
        self.assertEqual(result["recursive_scope_refinements"], [])

    def test_valid_source_flag_remains_proposal_only(self):
        packet = {
            "examples": [example("one", "family_a"), example("two", "family_b")],
            "challenges": [example("negative", "family_c", ("different_condition",))],
        }
        result = discover(packet)
        self.assertEqual(result["proposal_count"], 1)
        self.assertEqual(len(result["recursive_scope_refinements"]), 1)
        self.assertFalse(result["recursive_scope_refinements"][0]["promotion_authorized"])


if __name__ == "__main__":
    unittest.main()
