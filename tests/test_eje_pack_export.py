#!/usr/bin/env python3
"""Check EJE test input isolation using a disposable local Git fixture."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments" / "editorial-judgment"))
from export_input import export_case


class TestSealedExport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        for args in [
            ["init"], ["config", "user.email", "ci@example.invalid"],
            ["config", "user.name", "CI Fixture"],
        ]:
            subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True)
        (self.repo / "source.md").write_text("Original medical excerpt\n", encoding="utf-8")
        (self.repo / "labels.json").write_text('{"answer": "KEEP"}', encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-m", "fixture"], check=True, capture_output=True)
        self.sha = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"],
                                  check=True, capture_output=True, text=True).stdout.strip()
        self.out = Path(self.temp.name) / "out"

    def cases(self, paths=("source.md",), status="replayable"):
        return {"cases": [{"id": "CASE1", "status": status, "type": "negative-control",
                          "snapshot": {"commit": self.sha, "paths": list(paths)},
                          "task": "Review this material without being told the answer."}]}

    def test_export_omits_type_labels_and_feedback(self):
        dest = export_case(self.cases(), "CASE1", self.repo, self.out)
        self.assertEqual((dest / "sources" / "source.md").read_text(), "Original medical excerpt\n")
        all_content = (dest / "TASK.md").read_text()
        self.assertNotIn("negative-control", all_content)
        self.assertNotIn("KEEP", all_content)
        self.assertFalse((dest / "labels.json").exists())
        self.assertFalse((dest / "cases.json").exists())

    def test_cannot_export_gold_label_file(self):
        with self.assertRaises(ValueError):
            export_case(self.cases(paths=("labels.json",)), "CASE1", self.repo, self.out)

    def test_cannot_export_unfrozen_case(self):
        with self.assertRaises(ValueError):
            export_case(self.cases(status="needs_freeze"), "CASE1", self.repo, self.out)

    def test_does_not_overwrite_pack(self):
        export_case(self.cases(), "CASE1", self.repo, self.out)
        with self.assertRaises(FileExistsError):
            export_case(self.cases(), "CASE1", self.repo, self.out)


if __name__ == "__main__":
    unittest.main()
