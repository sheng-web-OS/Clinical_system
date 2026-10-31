"""Full-source OA JATS baseline: no preselected excerpt, labels or ontology writes."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from ale_fullsource_q0 import scan_fulltext, _parse, download_oa_xml

CC = "https://creativecommons.org/licenses/by/4.0/"
FULL_CASE = (
    "True hyperkalemia due to an acute kidney injury was confounded by the presence "
    "of pseudohyperkalemia due to marked thrombocytosis in the same patient."
)
CAUTION = (
    "Despite clinical improvement, repeat testing showed persistent abnormal "
    "serum potassium results with a different plasma potassium concentration."
)
FILLER = (
    "The care team measured repeat laboratory electrolytes and followed "
    "the person's clinical condition during inpatient observation."
)


def jats(pmc="PMC12513848", pmid="41079794", content=None, license=True):
    content = content if content is not None else (
        '<sec><title>Case Presentation</title><p>'+FILLER+'</p></sec>'
        '<sec><title>Discussion</title><p>'+CAUTION+'</p>'
        '<p>'+FULL_CASE+'</p></sec>'
    )
    lic = ('<permissions><license xlink:href="'+CC+'"/></permissions>'
           if license else '')
    return ('<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<front><article-meta><article-id pub-id-type="pmc">'+pmc.removeprefix("PMC")+'</article-id>'
            '<article-id pub-id-type="pmid">'+pmid+'</article-id>'+lic+
            '</article-meta></front><body>'+content+'</body>'
            '<back><ref-list><p>Despite the administrative discussion, papers were cited.</p>'
            '</ref-list></back></article>').encode("utf8")


class FullSourceQ0Tests(unittest.TestCase):
    def test_full_article_selects_mixed_mechanism_not_only_despite_word(self):
        x=scan_fulltext(jats(),"PMC12513848")
        self.assertEqual(x["decision"],"REVIEW_ONE_Q0")
        self.assertEqual(x["source_pmid"],"41079794")
        self.assertEqual(x["top_candidate"]["cue"],"COEXISTENCE_HYPOTHESIS")
        self.assertIn("Discussion",x["top_candidate"]["section"])
        self.assertEqual(x["concept_nodes_created"],0)
        self.assertFalse(x["medical_semantics_verified"])
        self.assertGreaterEqual(x["full_body_paragraphs_scanned"],3)

    def test_existing_content_is_warning_not_automatic_duplicate_or_new(self):
        x=scan_fulltext(jats(),"PMC12513848",
                        "Pseudohyperkalemia and thrombocytosis are discussed.")
        self.assertTrue(x["top_candidate"]["existing_context_may_cover_topic"])
        self.assertFalse(x["top_candidate"]["concept_novelty_verified"])

    def test_preexisting_coexistence_claim_does_not_auto_promote(self):
        x=scan_fulltext(jats(),"PMC12513848",FULL_CASE)
        self.assertFalse(x["medical_semantics_verified"])
        self.assertEqual(x["concept_nodes_created"],0)

    def test_no_relevant_cue_abstains_even_with_full_article(self):
        x=scan_fulltext(jats(content='<sec><title>Introduction</title>'
                       '<p>'+FILLER+'</p></sec>'),"PMC12513848")
        self.assertEqual(x["decision"],"ABSTAIN_NO_SUPPORTED_CUE")
        self.assertIsNone(x["top_candidate"])

    def test_reference_list_not_mined(self):
        x=scan_fulltext(jats(content='<sec><title>Introduction</title><p>'+
                       FILLER+'</p></sec>'),"PMC12513848")
        self.assertEqual(x["candidate_count"],0)

    def test_pmc_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"PMCID"):
            scan_fulltext(jats(),"PMC12513849")

    def test_source_must_have_explicit_cc_license(self):
        with self.assertRaisesRegex(ValueError,"Creative Commons"):
            scan_fulltext(jats(license=False),"PMC12513848")

    def test_never_parse_entity_or_doctype(self):
        bad=b'<!DOCTYPE article [<!ENTITY exploit "abc">]>'+jats()
        with self.assertRaisesRegex(ValueError,"unsafe"):
            scan_fulltext(bad,"PMC12513848")

    def test_raw_source_cannot_leak_long_copyright_passages(self):
        x=scan_fulltext(jats(),"PMC12513848")
        self.assertLessEqual(len(x["top_candidate"]["evidence_preview"].split()),13)
        self.assertIn("source_sentence_sha256",x["top_candidate"])

    def test_not_domain_specific_and_order_independent(self):
        text=("Independent renal measurements can coexist with mixed assessment mechanisms "
              "when factors affect blood sampling during diagnostic follow-up.")
        xm=scan_fulltext(jats(content='<sec><title>Discussion</title><p>'+
                             text+'</p></sec>'),"PMC12513848")
        self.assertEqual(xm["top_candidate"]["cue"],"COEXISTENCE_HYPOTHESIS")
        self.assertEqual(xm["top_candidate"],scan_fulltext(jats(content=
                         '<sec><title>Discussion</title><p>'+text+
                         '</p></sec>'),"PMC12513848")["top_candidate"])

    def test_invalid_pmcid_is_rejected_without_fetch(self):
        with self.assertRaisesRegex(ValueError,"PMCID"):
            download_oa_xml("https://localhost/private")

    def test_paragraphs_outside_body_are_excluded(self):
        pmid, paragraphs=_parse(jats(),"PMC12513848")
        self.assertEqual(pmid,"41079794")
        self.assertEqual(len(paragraphs),3)
        self.assertNotIn("administrative discussion",
                         " ".join(x["text"] for x in paragraphs))

if __name__ == "__main__":
    unittest.main()
