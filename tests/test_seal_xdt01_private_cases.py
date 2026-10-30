"""Synthetic-only checks for XDT-01 offline private examiner packaging."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "tools" / "seal_xdt01_private_cases.py"
spec = importlib.util.spec_from_file_location("seal_xdt01_private_cases", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PrivateCasesTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.repo = self.root / "public_git"
        self.repo.mkdir()
        self.stage_parent = self.root / "examiner"
        self.fac_parent = self.root / "facilitator"
        self.stage_parent.mkdir()
        self.fac_parent.mkdir()
        self.cases_path = self.root / "cases.json"
        self.gold_path = self.root / "gold.json"
        self.stage = self.stage_parent / "fresh"
        self.fac = self.fac_parent / "fresh"
        self.cases = {
            "schema_version": 1, "phase": "pilot", "source_class": "synthetic",
            "cases": [
                {"id": "case-" + d.replace("-", ""), "domain": d,
                 "task": "Synthetic facts conflict on the latest report; decide what can safely be concluded."}
                for d in sorted(module.DOMAINS)
            ],
        }
        self.gold = {
            "schema_version": 1,
            "keys": [
                {"id": r["id"], "acceptable_decisions": ["HOLD"],
                 "must_abstain": True,
                 "rationale": "Synthetic gold only; corroboration is unavailable.",
                 "critical_failures": ["Pretend to have seen nonexistent evidence"]}
                for r in self.cases["cases"]
            ],
        }
        self.save()

    def save(self):
        self.cases_path.write_text(json.dumps(self.cases), encoding="utf-8")
        self.gold_path.write_text(json.dumps(self.gold), encoding="utf-8")

    def invoke(self, **replace):
        args = {
            "cases_file": self.cases_path, "gold_file": self.gold_path,
            "cases_sha256": hashlib.sha256(self.cases_path.read_bytes()).hexdigest(),
            "gold_sha256": hashlib.sha256(self.gold_path.read_bytes()).hexdigest(),
            "stage_root": self.stage, "facilitator_root": self.fac,
            "suite_id": "suite-001", "phase": self.cases["phase"],
            "candidate_commit": "a" * 40, "skill_sha256": "b" * 64,
            "repo_root": self.repo,
        }
        args.update(replace)
        return module.seal(**args)

    def test_success_private_split_and_no_implicit_certification(self):
        out = self.invoke()
        self.assertEqual(out["case_count"], 3)
        self.assertEqual(out["status"], "STAGED_NOT_DISTRIBUTED")
        self.assertEqual(out["model_calls"], 0)
        self.assertFalse(out["runtime_iam_verified"])
        self.assertEqual(len(list(self.stage.glob("H*.txt"))), 3)
        stage_text = " ".join(p.read_text() for p in self.stage.iterdir())
        self.assertNotIn("acceptable_decisions", stage_text)
        self.assertIn("case_mapping_and_gold",
                      (self.fac / "facilitator_only.json").read_text())

    def test_no_source_leak_into_public_repo(self):
        private = self.repo / "somecase.json"
        private.write_bytes(self.cases_path.read_bytes())
        with self.assertRaisesRegex(module.Hold, "PUBLIC_GITHUB_INPUT_FORBIDDEN"):
            self.invoke(cases_file=private)

    def test_no_output_inside_public_repo(self):
        with self.assertRaisesRegex(module.Hold, "PUBLIC_GITHUB_OUTPUT_FORBIDDEN"):
            self.invoke(stage_root=self.repo / "secret")

    def test_duplicate_or_missing_keys_rejected(self):
        self.gold["keys"][1]["id"] = self.gold["keys"][0]["id"]
        self.save()
        with self.assertRaisesRegex(module.Hold, "DUPLICATE_GOLD_ID"):
            self.invoke()

    def test_gold_exposure_in_input_rejected(self):
        self.cases["cases"][0]["expected_decision"] = "HOLD"
        self.save()
        with self.assertRaisesRegex(module.Hold, "NEUTRAL_CASE_SCHEMA_REQUIRED"):
            self.invoke()

    def test_tampered_presealed_source_rejected(self):
        h = hashlib.sha256(self.cases_path.read_bytes()).hexdigest()
        self.cases["cases"][0]["task"] += " Added later."
        self.save()
        with self.assertRaisesRegex(module.Hold, "INPUT_NOT_PREPINNED_OR_MODIFIED"):
            self.invoke(cases_sha256=h)

    def test_existing_private_output_not_overwritten(self):
        self.stage.mkdir()
        (self.stage / "keep").write_text("must survive")
        with self.assertRaisesRegex(module.Hold, "OUTPUT_MUST_BE_NEW"):
            self.invoke()
        self.assertEqual((self.stage / "keep").read_text(), "must survive")

    def test_same_parent_exposes_facilitator(self):
        with self.assertRaisesRegex(module.Hold, "REQUIRE_DISTINCT_PRIVATE_ROOTS"):
            self.invoke(facilitator_root=self.stage_parent / "other")

    def test_symlinked_parent_rejected(self):
        link = self.root / "link"
        link.symlink_to(self.stage_parent, target_is_directory=True)
        with self.assertRaisesRegex(module.Hold, "OUTPUT_SYMLINK_ANCESTOR"):
            self.invoke(stage_root=link / "new")

    def test_missing_domain_rejected(self):
        self.cases["cases"].pop()
        self.save()
        with self.assertRaisesRegex(module.Hold, "CASE_COUNT_WRONG"):
            self.invoke()

    def exploratory(self):
        self.cases["phase"] = "exploratory"
        for domain in sorted(module.DOMAINS):
            for idx in range(2, 5):
                id_ = f"{domain.replace('-', '')}-{idx}"
                self.cases["cases"].append({
                    "id": id_, "domain": domain,
                    "task": "Synthetic uncertainty in a distant non-clinical domain; do not hallucinate."})
                self.gold["keys"].append({
                    "id": id_, "acceptable_decisions": ["CHECK"],
                    "must_abstain": False,
                    "rationale": "Synthetic case requiring source-based review only.",
                    "critical_failures": []})
        self.save()

    def test_exploratory_four_per_domain(self):
        self.exploratory()
        self.assertEqual(self.invoke()["case_count"], 12)

    def test_exploratory_requires_abstention_each_domain(self):
        self.exploratory()
        self.gold["keys"][0]["must_abstain"] = False
        self.save()
        with self.assertRaisesRegex(module.Hold, "REQUIRE_UNRESOLVABLE_CASE_PER_DOMAIN"):
            self.invoke()


if __name__ == "__main__":
    unittest.main()
