"""Adversarial contract tests for private Clinical_system agent quality instruments."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools/autonomy_quality_lab.py"
spec = importlib.util.spec_from_file_location("autonomy_quality_lab", MODULE)
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


def fixture(tmp):
    root = Path(tmp)
    content = root / "content"
    content.mkdir(exist_ok=True)
    cases = []
    for ident in ("article-a", "normal-b"):
        path = content / (ident + ".md")
        path.write_text("# Clinical case\nPatient observations, mechanism, constraints.\n", encoding="utf8")
        cases.append({"id": ident, "path": "content/" + path.name,
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return {"schema_version": 1, "exposure": "development",
            "source_commit": "a" * 40, "cases": cases, "trials": ["t1", "t2", "t3"],
            "common_instruction": "Find substantive problems and preserve sound reasoning.",
            "arms": {"baseline": "Use common editorial standards.",
                     "lite": "Check adjacent premises, case time course and evidence boundaries."}}


class RealArticlePackets(unittest.TestCase):
    def test_full_original_source_and_matched_nonhinted_packets(self):
        with tempfile.TemporaryDirectory() as root:
            sp = fixture(root)
            out = Path(root) / "experiments/autonomy-eval/private-packets"
            report = lab.prepare_packets(root, sp, out)
            self.assertEqual(report["planned_reviews"], 12)
            self.assertEqual(report["model_executions"], 0)
            a = json.loads((out / "article-a-t1-baseline.json").read_text())
            b = json.loads((out / "article-a-t1-lite.json").read_text())
            self.assertEqual(a["original_full_markdown"], b["original_full_markdown"])
            self.assertEqual(a["source_sha256"], b["source_sha256"])
            self.assertNotIn("defect_present", json.dumps(a))
            self.assertFalse(report["clinical_validated"])
            self.assertEqual(len(report["task_sha256"]), 12)
            for name, digest in report["task_sha256"].items():
                self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(), digest)
            with self.assertRaisesRegex(ValueError, "already exists"):
                lab.prepare_packets(root, sp, out)

    def test_never_write_review_packets_to_public_site(self):
        with tempfile.TemporaryDirectory() as root:
            sp = fixture(root)
            for directory in ("site", "dist", "content/reviews"):
                with self.subTest(directory=directory), self.assertRaisesRegex(ValueError, "private experiments"):
                    lab.prepare_packets(root, sp, Path(root)/directory/"packets")
                self.assertFalse((Path(root)/directory/"packets").exists())

    def test_reject_changed_article_before_any_packets_written(self):
        with tempfile.TemporaryDirectory() as root:
            sp = fixture(root)
            (Path(root)/"content/article-a.md").write_text("altered text")
            out = Path(root)/"experiments/autonomy-eval/private-packets"
            with self.assertRaisesRegex(ValueError, "changed since"):
                lab.prepare_packets(root, sp, out)
            self.assertFalse(out.exists())

    def test_reject_path_traversal_and_private_source(self):
        with tempfile.TemporaryDirectory() as root:
            for path in ("../../secrets.env", "docs/internal.md", "content/../../AGENTS.md"):
                sp = fixture(root)
                sp["cases"][0]["path"] = path
                with self.subTest(path=path), self.assertRaises(ValueError):
                    lab.prepare_packets(root, sp, Path(root)/"experiments/autonomy-eval/out")

    def test_reject_embedded_defect_answer_or_normal_label_in_packet(self):
        with tempfile.TemporaryDirectory() as root:
            sp = fixture(root)
            sp["cases"][0]["defect_present"] = True
            with self.assertRaisesRegex(ValueError, "defect hints"):
                lab.prepare_packets(root, sp, Path(root)/"experiments/autonomy-eval/out")

    def test_reject_duplicate_trials_cases_and_boolean_schema(self):
        for mutate in (lambda s: s.update(schema_version=True),
                       lambda s: s["trials"].__setitem__(2, "t1"),
                       lambda s: s["cases"].__setitem__(1, dict(s["cases"][0])),
                       lambda s: s["arms"].__setitem__("lite", s["arms"]["baseline"])):
            with tempfile.TemporaryDirectory() as root:
                sp = fixture(root)
                mutate(sp)
                with self.assertRaises(ValueError):
                    lab.prepare_packets(root, sp, Path(root)/"experiments/autonomy-eval/out")

    def test_cli_generates_manifest_but_never_pretends_model_ran(self):
        with tempfile.TemporaryDirectory() as root:
            sp = fixture(root)
            base = Path(root)
            (base/"spec.json").write_text(json.dumps(sp), encoding="utf8")
            out = base/"experiments/autonomy-eval/private-packets"
            task = subprocess.run([sys.executable, str(MODULE), "prepare",
                    "--root", root, "--spec", str(base/"spec.json"),
                    "--out", str(out)], capture_output=True, text=True)
            self.assertEqual(task.returncode, 0, task.stderr)
            self.assertEqual(json.loads(task.stdout)["model_executions"], 0)


ISSUE = """# Canonical incident
| F-001 | Broken ECG figure mobile render | Android iPhone image missing |
| F-002 | Metadata in public reader text | Internal Draft/HOLD leaked |
## EVAL-001 — duplicated worker traces
Important: invalid repeated trial attribution; repair independent trace.
"""


class SelectiveMemory(unittest.TestCase):
    def test_real_issue133_incident_cell_with_severity_is_parsed(self):
        text = "| F-001（P0, V/P/G） | Mobile broken diagram image and source |"
        r = lab.select_experiences(text, ["diagram"])
        self.assertEqual(r["selected"][0]["incident_id"], "F-001")

    def test_retrieve_only_relevant_existing_incident(self):
        r = lab.select_experiences(ISSUE, ["Metadata", "Draft/HOLD"])
        self.assertEqual([x["incident_id"] for x in r["selected"]], ["F-002"])
        self.assertEqual(r["selected"][0]["status"], "PROVISIONAL")
        self.assertEqual(r["evidence_level"], "ISSUE_TEXT_RETRIEVAL_ONLY")

    def test_invalidated_experience_never_reused(self):
        state = {"F-002": {"status": "INVALIDATED"}}
        self.assertEqual(lab.select_experiences(ISSUE, ["Metadata"], state)["selected"], [])

    def test_false_validated_without_real_counterexample_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "VALIDATED requires"):
            lab.select_experiences(ISSUE, ["Metadata"], {"F-002": {"status": "VALIDATED"}})

    def test_validated_requires_review_locator_and_normal_control(self):
        state = {"F-002": {"status": "VALIDATED", "verified_case": "case-5",
                           "review_evidence": "github:review-8",
                           "negative_control": "case-6"}}
        self.assertEqual(lab.select_experiences(ISSUE, ["Metadata"], state)
                         ["selected"][0]["status"], "VALIDATED")

    def test_do_not_inject_all_incidents_without_task_match(self):
        self.assertEqual(lab.select_experiences(ISSUE, ["not-present"])["selected"], [])


class FailureTrace(unittest.TestCase):
    def test_earliest_confirmed_not_latest_visible_error(self):
        rows = [{"step": 8, "verdict": "CONFIRMED_FAILURE", "kind": "publishing",
                 "evidence_ref": "run#8", "reviewer_context": "reviewer",
                 "worker_context": "writer"},
                {"step": 2, "verdict": "CONFIRMED_FAILURE", "kind": "source_identity",
                 "evidence_ref": "run#2", "reviewer_context": "reviewer",
                 "worker_context": "writer"},
                {"step": 1, "verdict": "PASS"}]
        result = lab.trace_failure(rows)
        self.assertEqual(result["first_failure_step"], 2)
        self.assertEqual(result["root_cause"], "NOT_ESTABLISHED")

    def test_unknown_traces_do_not_invent_root_cause(self):
        result = lab.trace_failure([{"step": 1, "verdict": "UNKNOWN"}])
        self.assertEqual(result["root_cause"], "NOT_ESTABLISHED")
        self.assertIsNone(result["first_failure_step"])

    def test_same_worker_cannot_mark_own_failure_independent(self):
        with self.assertRaisesRegex(ValueError, "separate reviewer"):
            lab.trace_failure([{"step": 1, "verdict": "CONFIRMED_FAILURE",
                                "evidence_ref": "r", "worker_context": "same",
                                "reviewer_context": "same"}])

    def test_repeated_step_or_unsubstantiated_failure_rejected(self):
        with self.assertRaises(ValueError):
            lab.trace_failure([{"step": 1, "verdict": "PASS"},
                               {"step": 1, "verdict": "UNKNOWN"}])
        with self.assertRaises(ValueError):
            lab.trace_failure([{"step": 1, "verdict": "CONFIRMED_FAILURE"}])


def grades():
    return [{"item_id": "article-a", "candidate_order": ["opaque-x", "opaque-y"],
             "choice": "left", "reviewer_context": "blind-1"},
            {"item_id": "article-a", "candidate_order": ["opaque-y", "opaque-x"],
             "choice": "right", "reviewer_context": "blind-2"}]


class JudgeOrderCalibration(unittest.TestCase):
    def test_consistent_winner_under_reversal_is_not_medical_approval(self):
        r = lab.judge_order_calibration(grades())
        self.assertEqual(r["pairs_stable"], 1)
        self.assertEqual(r["pairs"][0]["winner"], "opaque-x")
        self.assertFalse(r["medical_validation"])
        self.assertFalse(r["publication_approval"])

    def test_left_only_preference_is_flagged(self):
        rows = grades()
        rows[1]["choice"] = "left"
        r = lab.judge_order_calibration(rows)
        self.assertEqual(r["pairs"][0]["state"], "ORDER_SENSITIVE")
        self.assertEqual(r["status"], "NEEDS_REVIEW")

    def test_missing_reverse_grade_is_not_validated(self):
        r = lab.judge_order_calibration(grades()[:1])
        self.assertEqual(r["pairs"][0]["state"], "INCOMPLETE")
        self.assertEqual(r["status"], "NEEDS_REVIEW")

    def test_self_reused_context_or_fake_reversal_rejected(self):
        rows = grades()
        rows[1]["reviewer_context"] = "blind-1"
        with self.assertRaisesRegex(ValueError, "fresh reviewer"):
            lab.judge_order_calibration(rows)
        rows = grades()
        rows[1]["candidate_order"] = ["opaque-x", "opaque-y"]
        with self.assertRaisesRegex(ValueError, "exchange"):
            lab.judge_order_calibration(rows)

    def test_cherry_picked_third_grade_rejected(self):
        rows = grades()
        rows.append(dict(rows[0], reviewer_context="blind-3"))
        with self.assertRaisesRegex(ValueError, "repeated"):
            lab.judge_order_calibration(rows)


if __name__ == "__main__":
    unittest.main()
