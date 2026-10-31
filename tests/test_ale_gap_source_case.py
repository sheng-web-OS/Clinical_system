"""Negative controls: public citation IDs are routing hints, not source truth."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ale_gap_source_case import triage_public_sources


def gap(id_, origin="COVERAGE_GAP", impact="TRANSFER", sources=None,
        scope="CURRENT", families=2):
    return {"id":id_, "origin":origin, "impact":impact, "scope":scope,
            "source_state":"PENDING", "linked_family_count":families,
            "research_effort":"SMALL",
            "source_ids": sources or ["pmid_37768662"]}


def packet(*gaps):
    return {"source_classification":"PUBLIC_SOURCE_LINKED",
            "max_active_research":1, "gaps":list(gaps)}


class PublicSourceGapTests(unittest.TestCase):
    def test_real_public_source_ids_are_retained_without_truth_claim(self):
        result=triage_public_sources(packet(
            gap("hyperna", "SOURCE_CONTRADICTION", "CRITICAL",
                ["pmid_37768662","pmid_40152929"]),
            gap("other")
        ))
        self.assertEqual(result["decisions"][0]["decision"], "RESEARCH_NOW")
        self.assertEqual(result["decisions"][0]["source_ids"],
                         ["pmid_37768662","pmid_40152929"])
        self.assertFalse(result["decisions"][0]["same_estimand_confirmed"])
        self.assertFalse(result["decisions"][0]["literature_read_by_program"])
        self.assertEqual(result["concept_promotions"], 0)

    def test_one_citation_does_not_prove_contradiction(self):
        with self.assertRaisesRegex(ValueError,"at least two"):
            triage_public_sources(packet(gap("hyperna",
                "SOURCE_CONTRADICTION","CRITICAL")))

    def test_no_untrusted_links_identifiers_or_private_payload(self):
        for bad in ("https://docs.google.com/private",
                    "pmid_12345678?token=secret", "foo_37768662"):
            with self.assertRaises(ValueError):
                triage_public_sources(packet(gap("secret",sources=[bad])))
        extra=gap("private")
        extra["note_text"]="learner data"
        with self.assertRaisesRegex(ValueError,"private text"):
            triage_public_sources(packet(extra))

    def test_wrong_classification_fails(self):
        req=packet(gap("gap"))
        req["source_classification"]="OWNER_PRIVATE"
        with self.assertRaisesRegex(ValueError,"owner-private"):
            triage_public_sources(req)

    def test_deterministic_priority_preserves_unknown(self):
        gaps=[gap("marginal",impact="LOW",families=0),
              gap("transfer",sources=["pmid_32734201"],families=3)]
        one=triage_public_sources(packet(*gaps))
        two=triage_public_sources(packet(*reversed(gaps)))
        self.assertEqual(one,two)
        self.assertEqual([x["decision"] for x in one["decisions"]],
                         ["QUEUE_RESEARCH","PRESERVE_UNKNOWN"])


if __name__=="__main__":
    unittest.main()
