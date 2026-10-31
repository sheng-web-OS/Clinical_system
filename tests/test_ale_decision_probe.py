"""Public-safe regression: selectively ask one Q0 or abstain."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from ale_learning_checkpoint import initialize, advance, persist
from ale_decision_probe import probe_next_q0

SIG = {"from_role": "proxy_signal",
       "to_role": "decision_claim",
       "missing_bridge_role": "target_validation"}


def observation(name, family, features):
    return {"id": name, "family_id": family,
            "reasoning_signature": SIG.copy(),
            "source_ref": "public-synthetic/" + name,
            "source_check": "checked", "context_features": features}


def checkpoint(with_guard=True):
    packet = {"classification": "PUBLIC_SYNTHETIC_ONLY",
              "examples": [
                  observation("a", "engineering", ["proxy_only", "needs_context"]),
                  observation("b", "finance", ["proxy_only", "needs_context"])],
              "challenges": []}
    first = initialize(packet)
    if not with_guard:
        return first
    after = copy.deepcopy(packet)
    after["challenges"] = [observation("counter", "other", ["different_target"])]
    return advance(first, packet, after, first["checkpoint_sha256"])


def point():
    return {"source_classification": "PUBLIC_SYNTHETIC_ONLY",
            "phase": "PRE_ACTION", "materiality": "MATERIAL",
            "reasoning_signature": SIG.copy(),
            "original_question_roles": []}


class QuestionGate(unittest.TestCase):
    def test_material_unasked_scope_condition_proposes_one_q0(self):
        r = probe_next_q0(checkpoint(), point())
        self.assertEqual(r["decision"], "PROPOSE_ONE_Q0_SHADOW")
        self.assertEqual(r["unasked_guard_role"], "proxy_only")
        self.assertIn("proxy_only", r["question_q0"])
        self.assertFalse(r["verified"])
        self.assertFalse(r["promotion_authorized"])

    def test_originally_asked_question_is_not_repeated(self):
        p = point()
        p["original_question_roles"] = ["proxy_only", "needs_context"]
        self.assertEqual(probe_next_q0(checkpoint(), p)["decision"], "ABSTAIN")

    def test_no_material_preaction_boundary_abstains(self):
        for k, v in (("phase", "POST_ACTION"), ("materiality", "LOW")):
            with self.subTest(key=k):
                p = point()
                p[k] = v
                self.assertEqual(probe_next_q0(checkpoint(), p)["decision"], "ABSTAIN")

    def test_false_analogy_and_no_scope_abstain(self):
        p = point()
        p["reasoning_signature"]["to_role"] = "different_conclusion"
        self.assertEqual(probe_next_q0(checkpoint(), p)["decision"], "ABSTAIN")
        self.assertEqual(probe_next_q0(checkpoint(False), point())["decision"], "ABSTAIN")

    def test_private_unclassified_input_and_unsafe_roles_rejected(self):
        for classification in ("PRIVATE_LEARNER", None):
            p = point()
            p["source_classification"] = classification
            with self.assertRaises(ValueError):
                probe_next_q0(checkpoint(), p)
        p = point()
        p["original_question_roles"] = ["personal clinical narrative"]
        with self.assertRaises(ValueError):
            probe_next_q0(checkpoint(), p)

    def test_separate_process_can_propose_without_original_packet(self):
        state = checkpoint()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            persist(path / "checkpoint.json", state, None) if state["sequence"] == 0 else (
                path / "checkpoint.json").write_text(json.dumps(state), encoding="utf-8")
            (path / "decision.json").write_text(json.dumps(point()), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "tools" / "ale_decision_probe.py"),
                                     "--checkpoint", str(path / "checkpoint.json"),
                                     "--decision-point", str(path / "decision.json")],
                                    text=True, capture_output=True, check=True)
            r = json.loads(result.stdout)
            self.assertEqual(r["decision"], "PROPOSE_ONE_Q0_SHADOW")
            self.assertEqual(r["checkpoint_sha256"], state["checkpoint_sha256"])


if __name__ == "__main__":
    unittest.main()
