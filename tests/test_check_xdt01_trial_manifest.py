"""Synthetic adversarial integrity checks only; no real agents are exercised."""
import unittest
from tools.check_xdt01_trial_manifest import check


def manifest():
    digest = "a" * 64
    trials = []
    for domain in ("inventory", "it-incident", "provenance"):
        for arm in ("A", "B", "C"):
            trials.append({"task_id": domain + "-01", "domain": domain, "arm": arm,
                "input_sha256": digest, "model": "same-model", "effort": "same",
                "tool_policy_sha256": digest, "token_cap": 1000,
                "time_cap_s": 600, "first_pass_sha256": digest})
    return {"experiment_id": "XDT-01", "phase": "pilot",
            "protocol_commit": "a" * 40, "skill_sha256": digest, "trials": trials}


class TestXDT01Manifest(unittest.TestCase):
    def test_synthetic_structure(self):
        self.assertEqual(check(manifest()), [])

    def test_missing_arm(self):
        x = manifest()
        x["trials"].pop()
        self.assertTrue(check(x))

    def test_duplicate_arm(self):
        x = manifest()
        x["trials"][1]["arm"] = "A"
        self.assertTrue(check(x))

    def test_mismatched_input(self):
        x = manifest()
        x["trials"][1]["input_sha256"] = "b" * 64
        self.assertTrue(check(x))

    def test_mismatched_budget(self):
        x = manifest()
        x["trials"][1]["token_cap"] = 2000
        self.assertTrue(check(x))

    def test_hidden_gold_leak(self):
        x = manifest()
        x["trials"][0]["gold"] = "hidden-answer"
        self.assertTrue(check(x))

    def test_not_a_real_run_without_receipt(self):
        # A well-formed synthetic manifest must never print VALIDATED; the
        # verifier deliberately checks structure only, not outcome or identity.
        self.assertEqual(check(manifest()), [])


    def test_hidden_case_bundle_at_top_level_fails_closed(self):
        x = manifest()
        x["private_cases"] = [{"text": "unseen hidden source from examiner"}]
        self.assertTrue(check(x))

    def test_unknown_trial_payload_field_fails_closed(self):
        x = manifest()
        x["trials"][0]["unseen_task_text"] = "secret case payload"
        self.assertTrue(check(x))

    def test_unbounded_task_id_fails_closed(self):
        x = manifest()
        for t in x["trials"][:3]:
            t["task_id"] = "a" * 4096
        self.assertTrue(check(x))

    def test_unbounded_model_id_fails_closed(self):
        x = manifest()
        for t in x["trials"][:3]:
            t["model"] = "unknown model " * 900
        self.assertTrue(check(x))



    def test_non_scalar_phase_fails_without_exception(self):
        x = manifest()
        x["phase"] = {"private_text": "hidden"}
        self.assertTrue(check(x))

    def test_non_scalar_arm_fails_without_exception(self):
        x = manifest()
        x["trials"][0]["arm"] = {"hidden": "case"}
        self.assertTrue(check(x))

    def test_non_scalar_domain_fails_without_exception(self):
        x = manifest()
        x["trials"][0]["domain"] = ["hidden"]
        self.assertTrue(check(x))



if __name__ == "__main__":
    unittest.main()
