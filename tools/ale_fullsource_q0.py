#!/usr/bin/env python3
"""Read an entire Europe PMC open-access JATS article; propose ONE research Q0.

Public-source-only, bounded, read-only. No predefined tags, concept IDs,
rank labels, user learning data, paid APIs, or knowledge-graph writes.
Selection is a lexical attention baseline, NOT clinical semantic discovery.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from ale_raw_q0_probe import extract, SENTENCES

PMC = re.compile(r"PMC[1-9][0-9]{4,9}\Z")
PMID = re.compile(r"[1-9][0-9]{6,8}\Z")
BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/"
MAX_XML = 3_000_000
SKIP = {"ref-list", "back", "table-wrap", "fig", "disp-formula",
        "supplementary-material", "permissions", "fn-group"}
COEXIST = re.compile(
    r"\b(?:coexist(?:ing|ent|ence)?|simultaneous(?:ly)?|concomitant(?:ly)?|"
    r"confounded by the presence of|mixed mechanisms?|both.{0,85}?and)\b", re.I)
STOP = set("this that when where there with their from have were both also even "
           "these those into between about clinical patient patients findings "
           "results research article methods figure study studies cause caused "
           "would could should using during under while despite which they them "
           "been than then without through after before level levels blood "
           "case cases report reported disease diseases treatment testing".split())


def _tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class _NoExternalRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = urlsplit(newurl)
        if parts.scheme != "https" or parts.hostname != "www.ebi.ac.uk":
            raise ValueError("redirect left Europe PMC origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_oa_xml(pmcid: str) -> bytes:
    if not isinstance(pmcid, str) or not PMC.fullmatch(pmcid):
        raise ValueError("invalid PMCID")
    # Host is not a user-supplied URL. Do not follow a redirect off origin.
    opener = build_opener(_NoExternalRedirect())
    url = BASE + pmcid + "/fullTextXML"
    with opener.open(Request(url, headers={
            "User-Agent": "ClinicalOS-ALE-research-preflight/0.1",
            "Accept": "application/xml"}), timeout=16) as response:
        data = response.read(MAX_XML + 1)
    if len(data) > MAX_XML:
        raise ValueError("source document over size limit")
    return data


def _parse(xml: bytes, requested_pmcid: str) -> tuple[str, list[dict]]:
    if len(xml) > MAX_XML or b"<!DOCTYPE" in xml.upper() or b"<!ENTITY" in xml.upper():
        raise ValueError("oversized or unsafe JATS XML")
    root = ET.fromstring(xml)
    if _tag(root.tag) != "article":
        raise ValueError("expected JATS article XML")
    ids = [x for x in root.iter()
           if _tag(x.tag) == "article-id"]
    pmcids = {("PMC" + "".join(x.itertext()).strip().removeprefix("PMC"))
              for x in ids if x.attrib.get("pub-id-type") in ("pmc", "pmcid")}
    pmids = ["".join(x.itertext()).strip() for x in ids
             if x.attrib.get("pub-id-type") == "pmid"]
    if requested_pmcid not in pmcids:
        raise ValueError("source PMCID did not match requested document")
    if not pmids or not PMID.fullmatch(pmids[0]):
        raise ValueError("missing valid source PMID")
    # An OA endpoint is not in itself a blanket redistribution license.
    # Require explicit machine-readable CC license marker.
    licenses = [x for x in root.iter() if _tag(x.tag) == "license"]
    grants = " ".join(" ".join(x.itertext()) + " " +
                      " ".join(x.attrib.values()) for x in licenses).lower()
    if "creativecommons.org/licenses/" not in grants:
        raise ValueError("no explicit Creative Commons license metadata")
    body = next((x for x in root.iter() if _tag(x.tag) == "body"), None)
    if body is None:
        raise ValueError("article has no full body")
    paragraphs: list[dict] = []
    def walk(element, heading="Body"):
        tag = _tag(element.tag)
        if tag in SKIP:
            return
        if tag == "sec":
            title = next((c for c in element if _tag(c.tag) == "title"), None)
            if title is not None:
                heading = " ".join("".join(title.itertext()).split())[:100] or heading
        if tag == "p":
            text = " ".join("".join(element.itertext()).split())
            if len(text) >= 45:
                paragraphs.append({"section": heading, "paragraph": len(paragraphs)+1,
                                   "text": text[:8000]})
            return
        for child in element:
            walk(child, heading)
    walk(body)
    if not paragraphs:
        raise ValueError("no usable article paragraphs")
    return pmids[0], paragraphs[:350]


def _terms(text: str) -> set[str]:
    return {w.casefold() for w in re.findall(r"[a-zA-Z][a-zA-Z-]{5,40}", text)
            if w.casefold() not in STOP}


def _snippet(text: str, limit_words: int = 12) -> str:
    words = text.split()
    return " ".join(words[:limit_words]) + (" …" if len(words) > limit_words else "")


def scan_fulltext(xml: bytes, pmcid: str, existing_public_context: str = "") -> dict:
    """Scan FULL body; rank article-native, source-anchored questions; never promote.

    Existing-context overlap is only a warning that a medical topic *may* already
    be taught. Lack of lexical overlap is never evidence of semantic novelty.
    """
    pmid, paragraphs = _parse(xml, pmcid)
    if not isinstance(existing_public_context, str):
        raise ValueError("invalid public context")
    existing = _terms(existing_public_context[:400_000])
    candidates: list[dict] = []
    seen: set[str] = set()
    for p in paragraphs:
        body = p["text"]
        # Existing Q0 preflight is capped at 3k chars; walk entire paragraph in
        # bounded overlapping chunks, preserving a stable source location.
        for offset in range(0, len(body), 2400):
            segment = body[offset:offset+2800]
            if len(segment) < 24:
                continue
            try:
                output = extract({"source_classification":"PUBLIC_SOURCE_EXCERPT",
                                  "source_ref":"pmid_"+pmid,"excerpt":segment})
            except ValueError:
                # A source paragraph may contain URLs, emails or raw citations.
                # Reject this chunk rather than drop safety validation.
                continue
            # Coexistence is a candidate reasoning contrast even without the
            # literal markers ('despite', 'however') in the short-excerpt gate.
            # Its generic cue must never be interpreted as semantic proof.
            pool = list(output["candidates"])
            for sent in SENTENCES.finditer(segment):
                sentence = sent.group().strip()
                if (len(sentence.split()) >= 8 and COEXIST.search(sentence)
                        and not any(x["exact_evidence"] == sentence for x in pool)):
                    pool.append({
                        "exact_evidence": sentence, "lexical_attention": 5,
                        "start_char": sent.start() + len(sent.group()) - len(sent.group().lstrip()),
                        "cue": "COEXISTENCE_HYPOTHESIS",
                        "proposed_q0": "Can these mechanisms coexist?",
                    })
            for raw in pool:
                sentence = raw["exact_evidence"]
                key = hashlib.sha256(re.sub(r"\s+"," ",sentence.casefold())
                                     .encode("utf8")).hexdigest()[:16]
                if key in seen:
                    continue
                seen.add(key)
                coexist = bool(COEXIST.search(sentence))
                section = p["section"]
                section_score = (2 if re.search(r"discussion|interpretation|conclusion",
                                               section, re.I)
                                 else 1 if re.search(r"case|result",section,re.I) else 0)
                terms = _terms(sentence)
                overlap = sorted(terms & existing)
                # Restrict evidence to short phrases, trace to source using hash.
                score = raw["lexical_attention"] + section_score + (3 if coexist else 0)
                candidates.append({
                    "pmcid":pmcid, "pmid":pmid, "section":section,
                    "paragraph":p["paragraph"],
                    "sentence_offset":offset+raw["start_char"],
                    "source_sentence_sha256":hashlib.sha256(sentence.encode("utf8")).hexdigest(),
                    "evidence_preview":_snippet(sentence),
                    "cue":"COEXISTENCE_HYPOTHESIS" if coexist else raw["cue"],
                    "score":score,
                    "existing_context_lexical_overlap":overlap[:5],
                    "existing_context_may_cover_topic":bool(overlap),
                    "proposed_q0":(
                        "Can mechanisms currently framed as alternatives coexist, "
                        "and which independent evidence separates their contributions?"
                        if coexist else raw["proposed_q0"]),
                    "requires_q2_q3_source_review":True,
                    "concept_novelty_verified":False,
                })
    candidates.sort(key=lambda r:(-r["score"], r["paragraph"], r["sentence_offset"]))
    return {
        "schema":"ale-fullsource-q0-v0", "source_pmcid":pmcid,"source_pmid":pmid,
        "source_url":f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/",
        "full_body_paragraphs_scanned":len(paragraphs),
        "candidate_count":len(candidates),
        "decision":"REVIEW_ONE_Q0" if candidates else "ABSTAIN_NO_SUPPORTED_CUE",
        "top_candidate":candidates[0] if candidates else None,
        "alternatives":candidates[1:4],
        "method":"LEXICAL_SOURCE_ATTENTION_NOT_SEMANTIC_PROOF",
        "source_rights":"CC_LICENSE_MARKER_PRESENT_NOT_REPUBLICATION_AUTHORIZATION",
        "concept_nodes_created":0,
        "medical_semantics_verified":False,
        "owner_data_accessed":False,
        "public_material_mutated":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pmcid",required=True)
    parser.add_argument("--live-oa",action="store_true",
                        help="fetch exact PMCID from Europe PMC open-access REST only")
    parser.add_argument("--fixture",type=Path,
                        help="offline trusted test source XML, never private content")
    parser.add_argument("--context-file",type=Path,
                        help="optional existing public article for overlap warnings")
    args=parser.parse_args()
    if not PMC.fullmatch(args.pmcid) or args.live_oa == bool(args.fixture):
        parser.error("select exactly one of --live-oa and --fixture with valid PMCID")
    xml=download_oa_xml(args.pmcid) if args.live_oa else args.fixture.read_bytes()
    context=""
    if args.context_file:
        root=Path(__file__).resolve().parents[1]
        candidate=args.context_file.resolve()
        allowed=root / "content" / "xiaoma-internal-medicine"
        atlas=root / "content" / "clinical-os" / "index.md"
        if not ((candidate.is_relative_to(allowed) and candidate.suffix==".md")
                or candidate == atlas.resolve()):
            parser.error("context must be a public article under an allowlisted source path")
        context=candidate.read_text(encoding="utf8")
    print(json.dumps(scan_fulltext(xml,args.pmcid,context),ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
