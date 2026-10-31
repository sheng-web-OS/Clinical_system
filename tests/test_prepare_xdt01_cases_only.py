"""Cases-only staging regressions using synthetic inputs and no provider."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "tools/prepare_xdt01_rich_pilot.py"
spec = importlib.util.spec_from_file_location("cases_only_preparer", SCRIPT)
rich = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rich)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def synthetic_cases():
    text = "  本地 synthetic source\r\n第二行，保留空白。\n"
    return {
        "schema_version": 1, "package_id": "xdt-cases-only-fixture",
        "source_class": "synthetic", "phase": "pilot",
        "instructions": "  共用指示\nUse supplied evidence only.\t",
        "cases": [
            {"id": f"fixture-case-{idx}", "domain": domain,
             "task": f"  合成問題 {idx}\r\nKeep every byte in this value.\n",
             "evidence": [
                 {"id": "E_1", "text": "  證據原文\nsecond line\t"},
                 {"id": "Obj2", "object_path": "/objects/synthetic-來源.txt",
                  "utf8_text": text, "sha256": digest(text.encode("utf-8"))}]}
            for idx, domain in enumerate(("inventory", "it-incident", "provenance"), 1)]}


class CasesOnlyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name).resolve()
        self.repo = self.root / "public-repo"
        self.repo.mkdir()
        self.inputs = self.root / "private-inputs"
        self.inputs.mkdir()
        self.stage_parent = self.root / "private-stage"
        self.stage_parent.mkdir()
        self.cases = synthetic_cases()

    def args(self, raw=None):
        if raw is None:
            raw = (json.dumps(self.cases, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        source = self.inputs / "cases.json"
        source.write_bytes(raw)
        return {"cases_file": str(source), "cases_sha256": digest(raw),
                "repo_root": str(self.repo),
                "stage_root": str(self.stage_parent / "cases-only"),
                "candidate_commit": rich.FROZEN_CANDIDATE,
                "skill_sha256": "a" * 64}

    @staticmethod
    def cli_args(args):
        result = ["--cases-only"]
        for key, value in args.items():
            result.extend(["--" + key.replace("_", "-"), str(value)])
        return result

    def test_roundtrip_and_exact_manifest_without_gold_or_mapping(self):
        args = self.args()
        with patch.object(rich, "read_pinned", wraps=rich.read_pinned) as reader:
            result = rich.stage_cases_only(**args)
        self.assertEqual(reader.call_count, 1)
        self.assertEqual(reader.call_args.args[0], args["cases_file"])
        self.assertEqual(result["status"], "OFFLINE_CASES_ONLY_REVIEW_HOLD")
        self.assertEqual(result["model_calls"], 0)
        stage = pathlib.Path(args["stage_root"])
        self.assertEqual({p.name for p in stage.iterdir()},
                         {"H01.txt", "H02.txt", "H03.txt", "stage_manifest.json"})
        manifest = json.loads((stage / "stage_manifest.json").read_bytes())
        self.assertEqual(set(manifest), {
            "status", "schema_version", "phase", "source_class_claim",
            "candidate_commit", "skill_sha256", "source_sha256", "case_count",
            "cases", "model_calls"})
        self.assertEqual(manifest["source_sha256"], {"cases": args["cases_sha256"]})
        self.assertEqual(manifest["status"], "OFFLINE_CASES_ONLY_REVIEW_HOLD")
        self.assertEqual(manifest["case_count"], 3)
        originals = {case["id"]: case for case in self.cases["cases"]}
        recovered = {}
        for entry in manifest["cases"]:
            self.assertEqual(set(entry), {"slot", "sha256", "bytes", "evidence_count"})
            path = stage / (entry["slot"] + ".txt")
            raw = path.read_bytes()
            self.assertEqual(entry["sha256"], digest(raw))
            self.assertEqual(entry["bytes"], len(raw))
            self.assertLessEqual(len(raw), rich.MAX_PACKET_BYTES)
            packet = json.loads(raw)
            self.assertEqual(set(packet), {"package_id", "instructions", "case"})
            self.assertEqual(packet["package_id"], self.cases["package_id"])
            self.assertEqual(packet["instructions"], self.cases["instructions"])
            case = packet["case"]
            self.assertEqual(case, originals[case["id"]])
            self.assertEqual(entry["evidence_count"], len(case["evidence"]))
            recovered[case["id"]] = case
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(recovered, originals)
        self.assertEqual(stage.stat().st_mode & 0o777, 0o700)
        self.assertEqual((stage / "stage_manifest.json").stat().st_mode & 0o777, 0o600)

    def test_cli_cases_only_needs_no_gold_scoring_or_facilitator(self):
        args = self.args()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = rich.main(self.cli_args(args))
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["model_calls"], 0)

    def test_cli_rejects_each_forbidden_argument_before_reading(self):
        args = self.args()
        for flag in ("gold-file", "gold-sha256", "scoring-file",
                     "scoring-sha256", "facilitator-root"):
            with self.subTest(flag=flag), patch.object(rich, "read_pinned") as reader:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = rich.main(self.cli_args(args) + ["--" + flag, ""])
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(output.getvalue())["reason"],
                                 "CASES_ONLY_FORBIDS_GOLD_SCORING_FACILITATOR_ARGS")
                reader.assert_not_called()
        self.assertFalse(pathlib.Path(args["stage_root"]).exists())

    def test_full_cli_still_requires_all_private_inputs_before_reading(self):
        args = self.args()
        with patch.object(rich, "read_pinned") as reader:
            with contextlib.redirect_stdout(io.StringIO()):
                code = rich.main(self.cli_args(args)[1:])
            self.assertEqual(code, 2)
            reader.assert_not_called()

    def test_raw_source_pin_includes_bom_and_serialization(self):
        raw = b"\xef\xbb\xbf" + json.dumps(self.cases, ensure_ascii=False).encode("utf-8") + b"\r\n"
        args = self.args(raw)
        rich.stage_cases_only(**args)
        manifest = json.loads((pathlib.Path(args["stage_root"]) / "stage_manifest.json").read_bytes())
        self.assertEqual(manifest["source_sha256"]["cases"], digest(raw))
        self.assertEqual(pathlib.Path(args["cases_file"]).read_bytes(), raw)

    def test_wrong_or_nonstring_source_and_skill_pins_fail_closed(self):
        args = self.args()
        for field in ("cases_sha256", "skill_sha256"):
            for value in (None, [], {}, 1, False, "0" * 63):
                bad = dict(args, **{field: value})
                with self.subTest(field=field, value=value):
                    with self.assertRaises(rich.Hold):
                        rich.stage_cases_only(**bad)
        with self.assertRaisesRegex(rich.Hold, "INPUT_DIGEST_MISMATCH"):
            rich.stage_cases_only(**dict(args, cases_sha256="0" * 64))
        self.assertFalse(pathlib.Path(args["stage_root"]).exists())

    def test_malformed_unhashable_domains_and_object_hash_types(self):
        for value in ([], {}, None, 7):
            cases = copy.deepcopy(self.cases)
            cases["cases"][0]["domain"] = value
            with self.subTest(domain=value), self.assertRaisesRegex(rich.Hold, "DOMAIN_DISTRIBUTION_INVALID"):
                rich.validate_cases(cases)
        for value in ([], {}, None, 7):
            cases = copy.deepcopy(self.cases)
            cases["cases"][0]["evidence"][1]["sha256"] = value
            with self.subTest(sha=value), self.assertRaisesRegex(rich.Hold, "EVIDENCE_OBJECT_HASH_MISMATCH"):
                rich.validate_cases(cases)

    def test_blank_and_invalid_unicode_text_fail_without_normalizing(self):
        paths = (("instructions",), ("cases", 0, "task"),
                 ("cases", 0, "evidence", 0, "text"),
                 ("cases", 0, "evidence", 1, "object_path"),
                 ("cases", 0, "evidence", 1, "utf8_text"))
        for path in paths:
            for text in ("", " \t\r\n", "\ud800"):
                cases = copy.deepcopy(self.cases)
                target = cases
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = text
                with self.subTest(path=path, text=repr(text)), self.assertRaises(rich.Hold):
                    rich.validate_cases(cases)

    def test_nonfinite_json_numbers_are_rejected_before_staging(self):
        for number in ("NaN", "Infinity", "-Infinity", "1e999", "-1e999"):
            raw = json.dumps(self.cases).replace('"schema_version": 1',
                                                '"schema_version": ' + number, 1).encode()
            args = self.args(raw)
            with self.subTest(number=number), self.assertRaisesRegex(rich.Hold, "NON_FINITE_JSON_NUMBER"):
                rich.stage_cases_only(**args)
            self.assertFalse(pathlib.Path(args["stage_root"]).exists())

    def test_invalid_json_duplicate_keys_or_utf8_do_not_create_stage(self):
        for raw in (b'{"schema_version":1,"schema_version":1}', b"\xff", b"{"):
            args = self.args(raw)
            with self.subTest(raw=raw), self.assertRaises(rich.Hold):
                rich.stage_cases_only(**args)
            self.assertFalse(pathlib.Path(args["stage_root"]).exists())

    def test_schema_counts_hashes_and_packet_cap_remain_strict(self):
        bad_cases = []
        value = copy.deepcopy(self.cases)
        value["unexpected_gold"] = "must never cross"
        bad_cases.append(value)
        value = copy.deepcopy(self.cases)
        value["cases"].append(copy.deepcopy(value["cases"][0]))
        bad_cases.append(value)
        value = copy.deepcopy(self.cases)
        value["cases"][0]["evidence"][1]["sha256"] = "0" * 64
        bad_cases.append(value)
        value = copy.deepcopy(self.cases)
        value["cases"][0]["evidence"] = [{"id": f"E{i}", "text": "observation"} for i in range(31)]
        bad_cases.append(value)
        value = copy.deepcopy(self.cases)
        value["cases"][0]["task"] = "x" * 10_000
        value["cases"][0]["evidence"][0]["text"] = "y" * 3000
        bad_cases.append(value)
        for cases in bad_cases:
            with self.subTest(case=bad_cases.index(cases)), self.assertRaises(rich.Hold):
                rich.validate_cases(cases)

    def test_public_paths_symlinks_and_existing_stage_are_rejected(self):
        args = self.args()
        self.inputs.joinpath("linked.json").symlink_to(args["cases_file"])
        with self.assertRaisesRegex(rich.Hold, "INPUT_NOT_REGULAR_FILE"):
            rich.stage_cases_only(**dict(args, cases_file=str(self.inputs / "linked.json")))
        public_source = self.repo / "cases.json"
        public_source.write_bytes(pathlib.Path(args["cases_file"]).read_bytes())
        with self.assertRaisesRegex(rich.Hold, "PUBLIC_REPO_INPUT_FORBIDDEN"):
            rich.stage_cases_only(**dict(args, cases_file=str(public_source)))
        traversal = str(self.stage_parent / ".." / "public-repo" / "stage")
        with self.assertRaisesRegex(rich.Hold, "PUBLIC_REPO_OUTPUT_FORBIDDEN"):
            rich.stage_cases_only(**dict(args, stage_root=traversal))
        dangling = self.stage_parent / "dangling"
        dangling.symlink_to(self.stage_parent / "missing")
        with self.assertRaisesRegex(rich.Hold, "TARGET_ALREADY_EXISTS"):
            rich.stage_cases_only(**dict(args, stage_root=str(dangling)))
        pathlib.Path(args["stage_root"]).mkdir()
        with self.assertRaisesRegex(rich.Hold, "TARGET_ALREADY_EXISTS"):
            rich.stage_cases_only(**args)

    def test_failed_manifest_write_cleans_only_new_stage(self):
        args = self.args()
        source = pathlib.Path(args["cases_file"]).read_bytes()
        with patch.object(rich, "exclusive_json", side_effect=OSError("synthetic write failure")):
            with self.assertRaises(OSError):
                rich.stage_cases_only(**args)
        self.assertFalse(pathlib.Path(args["stage_root"]).exists())
        self.assertEqual(pathlib.Path(args["cases_file"]).read_bytes(), source)


if __name__ == "__main__":
    unittest.main()
