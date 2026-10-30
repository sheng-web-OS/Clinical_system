"""Offline regression for the demonstrated root-as-file claim bypass."""
import copy
from pathlib import Path
import unittest

from tools.dispatch_runtime import propose_claim, valid_blobs, valid_path, validate_leases
from tools.dispatch_selector import DispatchError, load_manifest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = load_manifest(ROOT / "ops/dispatch.json")
HEAD = "a" * 40
NOW = "2026-10-30T03:10:00Z"


def claim(state, task, pr, path, run):
    target = next(t["target"] for t in CONFIG["tasks"] if t["id"] == task)
    return propose_claim(
        state, CONFIG, task, run, ["path:" + path, "pr:" + str(pr)],
        state["generation"], NOW,
        binding={"task_id": task, "target": target, "pr_number": pr,
                 "head_sha": HEAD, "changed_paths": [path]},
        expected_head=HEAD)


class RootPathContract(unittest.TestCase):
    def setUp(self):
        self.state = {"schema_version": 1, "generation": 0, "leases": {}}

    def test_root_is_not_an_artifact_file(self):
        self.assertFalse(valid_blobs({".": HEAD}))

    def test_root_claim_cannot_coexist_with_descendant(self):
        with self.assertRaisesRegex(DispatchError, "^INVALID_CLAIM$"):
            first = claim(self.state, "lab-medicine", 214, ".", "root-run-001")
            claim(first["proposed_state"], "public-narrative-audit", 153,
                  "content/example.md", "child-run-001")

    def test_persisted_root_lease_is_rejected(self):
        proposed = claim(self.state, "lab-medicine", 214,
                         "content/a.md", "writer-run-001")["proposed_state"]
        forged = copy.deepcopy(proposed)
        forged["leases"]["lab-medicine"]["resources"] = ["path:.", "pr:214"]
        with self.assertRaisesRegex(DispatchError, "^INVALID_LEASE_VALUES$"):
            validate_leases(forged)

    def test_regular_and_dotfile_paths_remain_valid(self):
        for path in ("AGENTS.md", ".github/workflows/build.yml", "content/a.md"):
            with self.subTest(path=path):
                self.assertTrue(valid_path(path))
                self.assertTrue(valid_blobs({path: HEAD}))

    def test_disjoint_files_remain_non_authorizing_plans(self):
        first = claim(self.state, "lab-medicine", 214,
                      "content/a.md", "writer-run-001")
        second = claim(first["proposed_state"], "public-narrative-audit", 153,
                       "content/b.md", "other-run-001")
        self.assertFalse(first["execution_authorized"])
        self.assertFalse(second["execution_authorized"])
        self.assertEqual(2, len(second["proposed_state"]["leases"]))
        self.assertEqual({}, self.state["leases"])


if __name__ == "__main__":
    unittest.main()
