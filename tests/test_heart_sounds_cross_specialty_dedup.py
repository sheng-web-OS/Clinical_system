"""Regression for a published duplicate cross-specialty exam compilation.

Canonical identity is ROC year + sitting + subject + original question number.
This catches reworded copies even when titles and explanations differ.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "content/xiaoma-internal-medicine/lessons/2026-10-27-heart-sounds-cross-discipline-exams.md"
NEW = ROOT / "content/xiaoma-internal-medicine/exams/heart-sounds-cross-specialty-expanded-111-115.md"
SOURCES = ROOT / "content/xiaoma-internal-medicine/exams/heart-sounds-cross-specialty-sources.md"
CORRECTION = ROOT / "archive/national-exam/physician-stage2-2022-2026/extracted/2026-s2-med5/corrected_answer.json"
NEW_SOURCE = "content/xiaoma-internal-medicine/exams/heart-sounds-cross-specialty-expanded-111-115.md"
OLD_SOURCE = "content/xiaoma-internal-medicine/lessons/2026-10-27-heart-sounds-cross-discipline-exams.md"

SUBJECT = {"四": 4, "五": 5, "六": 6}
HEAD = re.compile(r"^###\s*(11[1-5])\s*年?\s*(第一次|第二次|[（(]?[一二12][）)]?)\s*[・\s]*醫學[（(]([四五六])[）)]\s*Q\s*(\d+)", re.M)


def identities(text):
    out = []
    for year, sitting, subject, number in HEAD.findall(text):
        sitting_number = 1 if ("一" in sitting or "1" in sitting) else 2
        out.append((int(year), sitting_number, SUBJECT[subject], int(number)))
    return out


def metadata_ids(row):
    out = []
    for q in row["exam_questions"]:
        out.append((q["year_roc"], q["sitting"], SUBJECT[q["subject"][3]], q["question_number"]))
    return out


def test_published_29_and_extension_20_are_unique():
    old, new = identities(OLD.read_text("utf-8")), identities(NEW.read_text("utf-8"))
    assert len(old) == len(set(old)) == 29
    assert len(new) == len(set(new)) == 20
    assert not (set(old) & set(new)), "same official exam question published twice"


def test_canonical_catalog_29_plus_20():
    pages = json.loads((ROOT / "site/pages.json").read_text("utf-8"))
    by_source = {row["source"]: row for row in pages}
    old = metadata_ids(by_source[OLD_SOURCE])
    new = metadata_ids(by_source[NEW_SOURCE])
    assert len(old) == len(set(old)) == 29
    assert len(new) == len(set(new)) == 20
    assert set(old) == set(identities(OLD.read_text("utf-8")))
    assert set(new) == set(identities(NEW.read_text("utf-8")))
    assert not (set(old) & set(new))
    assert "20" in by_source[NEW_SOURCE]["title"]
    assert "29" in by_source[OLD_SOURCE]["title"]


def test_official_115_s2_med5_q9_correction_is_not_lost():
    extracted = json.loads(CORRECTION.read_text("utf-8"))["pages"][0]["text"]
    assert "第9題答Ｂ或Ｄ或BD者均給分" in extracted
    old = OLD.read_text("utf-8")
    assert "115（二）醫學（五）Q9" in old
    assert "B 或 D" in old or "B／D" in old
    assert (115, 2, 5, 9) not in identities(NEW.read_text("utf-8"))


def test_extension_sources_do_not_advertise_duplicated_46():
    source = SOURCES.read_text("utf-8")
    new = NEW.read_text("utf-8")
    assert "20 道" in source
    assert "20 道" in new
    assert "46 道" not in source + new
