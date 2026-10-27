"""Source-pinned 3x2x3 original-article packet experiment: engineering only, NO model runs.
The source-Git blob IDs are from immutable source commit c5898a2, verified 2026-10-27.
"""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_COMMIT = "c5898a22636b265da3bc99aec387c346e7f6c386"
PROTOCOL = ROOT / "experiments/autonomy-eval/real-articles-20261027/protocol.json"
SOURCES = {
    "article1": ("content/xiaoma-internal-medicine/lessons/2026-10-21-hypoxemia.md",
                 "be780f1ae3567c60f3a108c8fa489ca8005f39d3"),
    "article2": ("content/xiaoma-internal-medicine/lessons/2026-10-26-copd-emptying.md",
                 "f0b8a501c11e801168f2991d46f21249af1880dd"),
    "article3": ("content/xiaoma-reading/integrated/2026-10-21-dcm.md",
                 "f16eced854467e5c8e43a063ef5d34b93f0d1d15"),
}
spec = importlib.util.spec_from_file_location("quality_lab", ROOT / "tools/autonomy_quality_lab.py")
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def snapshot():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if protocol["source_sha"] != SOURCE_COMMIT:
        raise ValueError("pinned source commit mismatch")
    cases = []
    for ident, (path, git_blob) in SOURCES.items():
        raw = (ROOT / path).read_bytes()
        calculated = hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()
        if calculated != git_blob:
            raise ValueError("source article changed: " + ident)
        cases.append({"id": ident, "path": path, "sha256": hashlib.sha256(raw).hexdigest()})
    return {"schema_version": 1, "exposure": "development",
            "source_commit": SOURCE_COMMIT, "cases": cases,
            "trials": ["t1", "t2", "t3"], "common_instruction": protocol["baseline"],
            "arms": {"baseline": "請依共同品質契約進行審查。",
                     "lite": protocol["treatment_addition"]}}


class OriginalArticlePacketPilot(unittest.TestCase):
    def test_three_real_originals_match_pinned_source_blob(self):
        snap = snapshot()
        self.assertEqual(len(snap["cases"]), 3)
        self.assertEqual(len({x["sha256"] for x in snap["cases"]}), 3)

    def test_18_packets_same_article_across_prompt_conditions_and_all_trials(self):
        snap = snapshot()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "article-qa-packets"
            summary = lab.prepare_packets(ROOT, snap, out)
            self.assertEqual(summary["planned_reviews"], 18)
            self.assertEqual(summary["model_executions"], 0)
            self.assertEqual(summary["article_count"], 3)
            self.assertFalse(summary["clinical_validated"])
            for ident in SOURCES:
                packet = {}
                for trial in ("t1", "t2", "t3"):
                    for arm in ("baseline", "lite"):
                        name = f"{ident}-{trial}-{arm}.json"
                        raw = (out / name).read_bytes()
                        self.assertEqual(hashlib.sha256(raw).hexdigest(), summary["task_sha256"][name])
                        row = json.loads(raw)
                        self.assertEqual(row["evidence_level"], "DEVELOPMENT_ONLY")
                        self.assertNotIn("defect_present", row)
                        self.assertNotIn("known_anchor", row)
                        packet[(trial, arm)] = row
                    self.assertEqual(packet[(trial, "baseline")]["original_full_markdown"],
                                     packet[(trial, "lite")]["original_full_markdown"])
                self.assertEqual(len(set(p["source_sha256"] for p in packet.values())), 1)

    def test_original_preregistration_task_digests_are_not_relabelled(self):
        protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
        old = set(protocol["task_sha256"])
        self.assertEqual(len(old), 6)
        self.assertTrue(all("task.json" in name for name in old))
        with tempfile.TemporaryDirectory() as tmp:
            summary = lab.prepare_packets(ROOT, snapshot(), Path(tmp) / "exploratory")
            self.assertTrue(old.isdisjoint(summary["task_sha256"]))
            self.assertEqual(summary["model_executions"], 0)


if __name__ == "__main__":
    unittest.main()
