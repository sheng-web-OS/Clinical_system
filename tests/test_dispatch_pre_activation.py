"""Owner-directed offline counterexamples; no network or live lease authority.

The compatibility adapter supplies the proposed binding only if implemented.
On the frozen v0.3 source, the lack of that input is precisely the RED contract.
"""
import copy
import importlib.util
import inspect
import json
from pathlib import Path
import unittest

from tools.dispatch_selector import DispatchError, load_manifest
from tools.dispatch_runtime import propose_claim, validate_leases
from tools.dispatch_observe import START, END

ROOT = Path(__file__).resolve().parents[1]
CONFIG = load_manifest(ROOT / "ops/dispatch.json")
NOW = "2026-10-30T03:00:00Z"
HEAD = "a" * 40


def claim(state, task="lab-medicine", resources=None, binding=None,
          expected_head=HEAD, include_binding=True):
    resources = resources or ["path:content/example.md", "pr:214"]
    kwargs = {}
    if include_binding and "binding" in inspect.signature(propose_claim).parameters:
        kwargs = {"binding": binding or {
            "task_id": task, "target": next(t["target"] for t in CONFIG["tasks"] if t["id"] == task),
            "pr_number": 214, "head_sha": HEAD,
            "changed_paths": [r[5:] for r in resources if r.startswith("path:")],
        }, "expected_head": expected_head}
    return propose_claim(state, CONFIG, task, "probe-run-001", resources,
                         state["generation"], NOW, **kwargs)


class ContractGaps(unittest.TestCase):
    def setUp(self):
        self.state = {"schema_version": 1, "generation": 0, "leases": {}}
        self.binding = {"task_id": "lab-medicine", "target": "issue:180",
                        "pr_number": 214, "head_sha": HEAD,
                        "changed_paths": ["content/example.md"]}

    def test_ancestor_descendant_claim_must_conflict(self):
        first = claim(self.state, resources=["path:content", "pr:214"])["proposed_state"]
        with self.assertRaises(DispatchError):
            claim(first, task="public-narrative-audit", resources=["path:content/a.md", "pr:153"],
                  binding={"task_id": "public-narrative-audit", "target": "issue:152",
                           "pr_number": 153, "head_sha": HEAD, "changed_paths": ["content/a.md"]})

    def test_forged_ancestor_table_must_be_rejected(self):
        state = claim(self.state, resources=["path:content", "pr:214"])["proposed_state"]
        other = copy.deepcopy(state["leases"]["lab-medicine"])
        other["resources"] = ["path:content/a.md", "pr:153"]
        state["leases"]["public-narrative-audit"] = other
        with self.assertRaises(DispatchError):
            validate_leases(state)

    def test_wrong_pr_cannot_use_original_issue_binding(self):
        with self.assertRaises(DispatchError):
            claim(self.state, resources=["path:content/example.md", "pr:999"], binding=self.binding)

    def test_unlisted_changed_path_cannot_be_claimed(self):
        with self.assertRaises(DispatchError):
            claim(self.state, resources=["path:content/unlisted.md", "pr:214"], binding=self.binding)

    def test_stale_bound_head_cannot_be_claimed(self):
        with self.assertRaises(DispatchError):
            claim(self.state, binding=self.binding, expected_head="d" * 40)

    def test_missing_binding_cannot_propose_claim(self):
        with self.assertRaises(DispatchError):
            claim(self.state, include_binding=False)

    def test_marker_end_before_start_must_not_parse(self):
        spec = importlib.util.spec_from_file_location("observer_fixture", ROOT / "tests/test_dispatch_observe.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.ObserverTest.setUpClass()
        fixture = module.ObserverTest("test_exact_blob_checkpoint_routes_to_separate_reviewer")
        fixture.setUp()
        fixture.add_checkpoint()
        body = fixture.snapshot[fixture.comments_path][0]["body"]
        checkpoint = json.loads(body.split(START, 1)[1].split(END, 1)[0])
        fixture.snapshot[fixture.comments_path].append({
            "id": 322, "user": {"login": "sheng-web-OS"},
            "body": END + "\n" + START + json.dumps(checkpoint)})
        with self.assertRaises(DispatchError):
            fixture.observe()


if __name__ == "__main__":
    unittest.main()
