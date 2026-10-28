"""Prevent two simultaneous canonical teaching readings with identical public title.

Immutable historical originals may legitimately share a title with a new integrated
reading; different newly edited lessons may not silently share a canonical title.
"""
import collections
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class UniqueCanonicalReaderTitles(unittest.TestCase):
    def test_identical_nonhistorical_teaching_titles_are_not_published_twice(self):
        pages = json.loads((ROOT / "site/pages.json").read_text(encoding="utf-8"))
        groups = collections.defaultdict(list)
        for row in pages:
            if row.get("kind") == "historical_original":
                continue
            if not ("/lessons/" in row["source"] or row.get("kind") == "ai_integrated"):
                continue
            normalized = re.sub(r"\s+", "", row["title"]).casefold()
            groups[normalized].append(row["source"])
        duplicates = {title: sources for title, sources in groups.items()
                      if len(sources) > 1}
        self.assertFalse(duplicates,
                         "Two canonical lessons reuse the same public title: "
                         + repr(duplicates))


if __name__ == "__main__":
    unittest.main()
