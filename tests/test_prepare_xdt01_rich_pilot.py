"""Synthetic-only, zero-provider regressions for rich XDT01 pilot handoff."""
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "tools/prepare_xdt01_rich_pilot.py"
spec = importlib.util.spec_from_file_location("rich", SCRIPT)
rich = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rich)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fixtures():
    c = {"schema_version": 1, "package_id": "xdt-synthetic-unit-001",
         "source_class": "synthetic", "phase": "pilot",
         "instructions": "Use only the provided synthetic evidence. No tool action.",
         "cases": []}
    g = {"schema_version": 1, "package_id": c["package_id"], "keys": []}
    s = {"schema_version": 1, "package_id": c["package_id"],
         "status": "candidate", "method_record": {"authorship": "test double"},
         "general_rules": {"primary": "NOT_DEFINED"}, "cases": []}
    cases = ("inventory", "it-incident", "provenance")
    for i, domain in enumerate(cases, 1):
        evidence = [{"id": "I1", "text": "A synthetic observation, not a gold label."}]
        if domain == "provenance":
            data = "faux source text\n"
            evidence.append({"id": "P4", "object_path": "/objects/fake.txt",
                             "utf8_text": data, "sha256": digest(data.encode())})
        ident = f"xdt-fixture-{i:02d}"
        c["cases"].append({"id": ident, "domain": domain,
                           "task": "Explain the simulated outcome with evidence, including any unknowns.",
                           "evidence": evidence})
        g["keys"].append({"id": ident, "domain": domain,
                          "acceptable_decisions": ["hypothetical decision"],
                          "necessary_conditions": ["reference provided fact"],
                          "must_abstain": False, "critical_failures": [],
                          "unknown_information": ["counterfactual"]})
        s["cases"].append({"id": ident, "expected_skill": "SKIP",
                           "task_items": [f"check-{k}" for k in range(10)],
                           "routing_items": [{"points": 4, "rule": "observe selection"},
                                             {"points": 6, "rule": "do not invent"}]})
    return c, g, s


class RichPilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.repo = self.root / "public-repo"
        self.repo.mkdir()
        self.inputs = self.root / "examiner"
        self.inputs.mkdir()
        self.stage_parent = self.root / "private-stage"
        self.fac_parent = self.root / "private-facilitator"
        self.stage_parent.mkdir()
        self.fac_parent.mkdir()
        self.cases, self.gold, self.scoring = fixtures()

    def apply(self, *, cases=None, gold=None, scoring=None, raw_replacements=None):
        vals = (cases if cases is not None else self.cases,
                gold if gold is not None else self.gold,
                scoring if scoring is not None else self.scoring)
        a = {"repo_root": str(self.repo),
             "candidate_commit": rich.FROZEN_CANDIDATE,
             "skill_sha256": "a" * 64,
             "stage_root": str(self.stage_parent / "stage"),
             "facilitator_root": str(self.fac_parent / "fac")}
        for field, obj in zip(("cases", "gold", "scoring"), vals):
            raw = (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)
                   + "\n").encode()
            if raw_replacements and field in raw_replacements:
                raw = raw_replacements[field]
            path = self.inputs / (field + ".json")
            path.write_bytes(raw)
            a[field + "_file"] = str(path)
            a[field + "_sha256"] = digest(raw)
        return a

    def test_stage_semantic_lossless_evidence_and_private_gold(self):
        a = self.apply()
        result = rich.stage(**a)
        self.assertEqual(result["status"], "OFFLINE_STAGED_REVIEW_HOLD")
        self.assertEqual(result["model_calls"], 0)
        self.assertFalse(result["independent_access_denial_verified"])
        stage = pathlib.Path(a["stage_root"])
        fac = pathlib.Path(a["facilitator_root"])
        self.assertEqual(len(list(stage.glob("H*.txt"))), 3)
        manifest = json.loads((stage / "stage_manifest.json").read_text())
        self.assertEqual(len(manifest["cases"]), 3)
        packets = [json.loads(p.read_bytes()) for p in stage.glob("H*.txt")]
        original = {v["id"]: v for v in self.cases["cases"]}
        for packet in packets:
            self.assertEqual(packet["instructions"], self.cases["instructions"])
            self.assertEqual(packet["case"], original[packet["case"]["id"]])
        stage_bytes = b"".join(p.read_bytes() for p in stage.iterdir())
        self.assertNotIn(b"hypothetical decision", stage_bytes)
        self.assertNotIn(b"check-9", stage_bytes)
        fac_payload = json.loads((fac / "facilitator_only.json").read_text())
        gold = {v["id"]: v for v in self.gold["keys"]}
        scores = {v["id"]: v for v in self.scoring["cases"]}
        for v in fac_payload["case_mapping_and_gold"]:
            self.assertEqual(v["gold"], gold[v["original_id"]])
            self.assertEqual(v["scoring"], scores[v["original_id"]])
        self.assertEqual(fac_payload["primary_binary_endpoint"],
                         "NOT_PREREGISTERED_IN_RICH_RUBRIC")
        self.assertFalse(fac_payload["routing_justification_observable"])

    def test_hash_mismatch_does_not_create_output(self):
        a = self.apply()
        a["scoring_sha256"] = "0" * 64
        with self.assertRaisesRegex(rich.Hold, "INPUT_DIGEST_MISMATCH"):
            rich.stage(**a)
        self.assertFalse(pathlib.Path(a["stage_root"]).exists())

    def test_evidence_object_digest_mismatch(self):
        c, g, s = fixtures()
        c["cases"][2]["evidence"][1]["sha256"] = "0" * 64
        with self.assertRaisesRegex(rich.Hold, "EVIDENCE_OBJECT_HASH_MISMATCH"):
            rich.validate(c, g, s)

    def test_duplicate_evidence_id_rejected(self):
        c, g, s = fixtures()
        c["cases"][0]["evidence"].append(c["cases"][0]["evidence"][0])
        with self.assertRaisesRegex(rich.Hold, "EVIDENCE_ID_INVALID"):
            rich.validate(c, g, s)

    def test_missing_gold_rejected(self):
        c, g, s = fixtures()
        g["keys"].pop()
        with self.assertRaisesRegex(rich.Hold, "GOLD_OR_SCORING_COUNT"):
            rich.validate(c, g, s)

    def test_scoring_mismatched_case_id_rejected(self):
        c, g, s = fixtures()
        s["cases"][0]["id"] = "out-of-sync"
        with self.assertRaisesRegex(rich.Hold, "SCORING_COVERAGE_MISMATCH"):
            rich.validate(c, g, s)

    def test_bad_routing_points_rejected(self):
        c, g, s = fixtures()
        s["cases"][0]["routing_items"][0]["points"] = 7
        with self.assertRaisesRegex(rich.Hold, "ROUTING_TEN_POINTS_REQUIRED"):
            rich.validate(c, g, s)

    def test_only_three_domains_rejected_when_duplicate(self):
        c, g, s = fixtures()
        c["cases"][2]["domain"] = "inventory"
        with self.assertRaisesRegex(rich.Hold, "DOMAIN_DISTRIBUTION_INVALID"):
            rich.validate(c, g, s)

    def test_large_packet_refused(self):
        c, g, s = fixtures()
        c["cases"][0]["evidence"][0]["text"] = "large " * 1400
        c["cases"][0]["evidence"].append({"id": "I2", "text": "extra " * 1400})
        with self.assertRaisesRegex(rich.Hold, "ONE_CASE_TASK_TOO_LARGE"):
            rich.validate(c, g, s)

    def test_no_public_repository_input(self):
        a = self.apply()
        file_inside = self.repo / "cases.json"
        file_inside.write_bytes(pathlib.Path(a["cases_file"]).read_bytes())
        a["cases_file"] = str(file_inside)
        with self.assertRaisesRegex(rich.Hold, "PUBLIC_REPO_INPUT_FORBIDDEN"):
            rich.stage(**a)

    def test_no_public_repository_output(self):
        a = self.apply()
        a["stage_root"] = str(self.repo / "staged")
        with self.assertRaisesRegex(rich.Hold, "PUBLIC_REPO_OUTPUT_FORBIDDEN"):
            rich.stage(**a)

    def test_no_reuse_stage(self):
        a = self.apply()
        pathlib.Path(a["stage_root"]).mkdir()
        with self.assertRaisesRegex(rich.Hold, "TARGET_ALREADY_EXISTS"):
            rich.stage(**a)

    def test_json_duplicate_key_rejected(self):
        with self.assertRaisesRegex(rich.Hold, "DUPLICATE_JSON_KEY"):
            json.loads('{"id": 1, "id": 2}', object_pairs_hook=rich.unique_pairs)

    def test_wrong_frozen_commit_rejected(self):
        a = self.apply()
        a["candidate_commit"] = "0" * 40
        with self.assertRaisesRegex(rich.Hold, "FROZEN_COMMIT_MISMATCH"):
            rich.stage(**a)

    def test_uses_short_evidence_ids(self):
        c, g, s = fixtures()
        self.assertEqual(len(rich.validate(c, g, s)[0]), 3)


if __name__ == "__main__":
    unittest.main()
