"""No external payload is executed; synthetic fixture coverage only."""
import datetime as dt
import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "experiments/external-tech-intake/gate.py"
spec = importlib.util.spec_from_file_location("external_tech_gate", SOURCE)
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate
spec.loader.exec_module(gate)

SHA = "a" * 64
MANIFEST = {"candidate_id": "demo-asset", "artifact_sha256": SHA,
            "source_url": "https://example.org/demo", "source_commit": "a" * 40,
            "license_status": "VERIFIED", "privacy_status": "PUBLIC_CLEARED",
            "risk_tier": "low", "reversible": True}

def receipt():
    cases = []
    for i in range(8):
        cases.append({"id": "unseen-%d" % i, "domain": ["engineering", "knowledge"][i % 2],
                      "period": ["2024", "2025"][i % 2], "split": "unseen_holdout",
                      "baseline_score": .6, "candidate_score": .75,
                      "baseline_cost": 10, "candidate_cost": 11,
                      "severe_regression": False})
    return {"candidate_id": "demo-asset", "artifact_sha256": SHA,
            "prereg_sha256": "b" * 64, "review_sha256": "c" * 64,
            "evaluator_id": "worker-1", "reviewer_id": "reviewer-2",
            "security_review": "PASS", "rights_review": "PASS", "expires_on": "2030-01-01",
            "minimum_cases": 8, "minimum_domains": 2, "minimum_periods": 2,
            "minimum_mean_gain": .08, "maximum_cost_ratio": 1.2, "cases": cases}

class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.m = dict(MANIFEST)
        self.r = receipt()
        self.today = dt.date(2026, 10, 30)

    def d(self):
        return gate.decision(self.m, self.r, today=self.today)["decision"]

    def test_provenance_only_not_automatically_adopted(self):
        self.assertEqual(gate.decision(self.m)["decision"], "READY_FOR_ISOLATED_EVALUATION")

    def test_missing_receipt_pauses_existing_shadow(self):
        self.m["current_state"] = "SHADOW_ADOPTED"
        self.assertEqual(gate.decision(self.m)["decision"], "PAUSE_SHADOW")

    def test_shadow_adopt_is_advisory(self):
        self.assertEqual(self.d(), "ADOPT_SHADOW_CANDIDATE")

    def test_rights_and_privacy_fail_closed(self):
        for k, v in (("license_status", "PENDING"), ("privacy_status", "UNKNOWN")):
            self.m[k] = v
            self.assertEqual(self.d(), "QUARANTINE")
            self.m = dict(MANIFEST)

    def test_risk_reversibility_gate(self):
        self.m["risk_tier"] = "high"
        self.assertEqual(self.d(), "HOLD_RISK")
        self.m["risk_tier"] = "low"
        self.m["reversible"] = False
        self.assertEqual(self.d(), "HOLD_RISK")

    def test_hash_mismatch(self):
        self.r["artifact_sha256"] = "f" * 64
        self.assertEqual(self.d(), "QUARANTINE")

    def test_no_self_review(self):
        self.r["reviewer_id"] = self.r["evaluator_id"]
        self.assertEqual(self.d(), "HOLD_EVIDENCE")

    def test_required_holdout_and_coverage(self):
        self.r["cases"][0]["split"] = "training"
        self.assertEqual(self.d(), "HOLD_EVIDENCE")
        self.r = receipt()
        self.r["cases"] = self.r["cases"][:3]
        self.assertEqual(self.d(), "HOLD_EVIDENCE")
        self.r = receipt()
        for c in self.r["cases"]:
            c["period"] = "2025"
        self.assertEqual(self.d(), "HOLD_EVIDENCE")

    def test_regression_hard_stop(self):
        self.r["cases"][0]["severe_regression"] = True
        self.assertEqual(self.d(), "REJECT")
        self.m["current_state"] = "SHADOW_ADOPTED"
        self.assertEqual(self.d(), "PAUSE_SHADOW")

    def test_cost_and_benefit_fail(self):
        self.r["cases"][0]["candidate_cost"] = 100
        self.assertEqual(self.d(), "REJECT")
        self.m["current_state"] = "SHADOW_ADOPTED"
        self.assertEqual(self.d(), "RETIRE_SHADOW")

    def test_expiry_stops_existing_shadow(self):
        self.r["expires_on"] = "2026-10-29"
        self.m["current_state"] = "SHADOW_ADOPTED"
        self.assertEqual(self.d(), "PAUSE_SHADOW")

    def test_duplicate_case_rejected(self):
        self.r["cases"][0]["id"] = self.r["cases"][1]["id"]
        self.assertEqual(self.d(), "HOLD_EVIDENCE")

    def test_invalid_thresholds(self):
        self.r["minimum_cases"] = 0
        self.assertEqual(self.d(), "HOLD_EVIDENCE")

class ArchiveTests(unittest.TestCase):
    def zip_with(self, items):
        tmp = tempfile.TemporaryDirectory()
        path = Path(tmp.name) / "incoming.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for n, data in items:
                z.writestr(n, data)
        return tmp, path

    def test_benign_zip_is_not_safety_approved(self):
        tmp, path = self.zip_with([("README.md", "hello")])
        with tmp:
            out = gate.preflight_zip(path)
            self.assertEqual(out["decision"], "METADATA_PREFLIGHT_ONLY")
            self.assertEqual(len(out["package_sha256"]), 64)

    def test_path_traversal(self):
        tmp, path = self.zip_with([("../escape", "x")])
        with tmp:
            self.assertEqual(gate.preflight_zip(path)["decision"], "QUARANTINE")

    def test_duplicate_path_normalized(self):
        tmp, path = self.zip_with([("X.txt", "x"), ("x.txt", "y")])
        with tmp:
            self.assertEqual(gate.preflight_zip(path)["decision"], "QUARANTINE")

    def test_secret_filename(self):
        tmp, path = self.zip_with([(".env", "FAKE=only-test")])
        with tmp:
            self.assertEqual(gate.preflight_zip(path)["decision"], "QUARANTINE")

if __name__ == "__main__":
    unittest.main()
