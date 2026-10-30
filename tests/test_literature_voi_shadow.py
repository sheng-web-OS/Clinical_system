"""Mechanics only: deliberately synthetic numbers cannot prove agent improvement."""
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = (Path(__file__).resolve().parents[1] /
               "experiments/literature-voi-shadow/voi.py")
spec = importlib.util.spec_from_file_location("literature_voi_pilot", MODULE_PATH)
voi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voi)


def fixture(cost=1):
    return {
        "schema_version": 1, "mode": "shadow", "research_cost": cost,
        "actions": [
            {"id": "fix", "gate": "eligible"},
            {"id": "inspect", "gate": "eligible"},
        ],
        "evidence_outcomes": [
            {"id": "state-a", "probability": 0.5,
             "action_values": {"fix": 10, "inspect": 0}},
            {"id": "state-b", "probability": 0.5,
             "action_values": {"fix": 0, "inspect": 10}},
        ],
    }


class LiteratureValueOfInformationShadowTest(unittest.TestCase):
    def test_research_when_evidence_can_change_best_action(self):
        r = voi.decide(fixture())
        self.assertEqual("SHADOW_SUGGEST_RESEARCH", r["decision"])
        self.assertEqual("4.0", r["hypothetical_net_information_value"])
        self.assertFalse(r["execution_authorized"])
        self.assertEqual(0, r["external_calls"])

    def test_skip_when_evidence_never_changes_action(self):
        p = fixture()
        p["evidence_outcomes"][1]["action_values"] = {"fix": 10, "inspect": 0}
        self.assertEqual("SHADOW_CONTINUE_DIRECT", voi.decide(p)["decision"])

    def test_skip_when_cost_exceeds_information_value(self):
        self.assertEqual("SHADOW_CONTINUE_DIRECT", voi.decide(fixture(6))["decision"])

    def test_zero_cost_and_zero_gain_still_skip(self):
        p = fixture(0)
        p["evidence_outcomes"][1]["action_values"] = {"fix": 10, "inspect": 0}
        self.assertEqual("SHADOW_CONTINUE_DIRECT", voi.decide(p)["decision"])

    def test_held_action_cannot_be_selected(self):
        p = fixture()
        p["actions"][0]["gate"] = "hold"
        r = voi.decide(p)
        self.assertEqual("inspect", r["baseline_action"])
        self.assertEqual("SHADOW_CONTINUE_DIRECT", r["decision"])

    def test_all_held_is_hold(self):
        p = fixture()
        for a in p["actions"]:
            a["gate"] = "hold"
        self.assertEqual("HOLD", voi.decide(p)["decision"])

    def test_unknown_gate_fails_closed(self):
        p = fixture()
        p["actions"][1]["gate"] = "maybe"
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_probability_sum(self):
        p = fixture()
        p["evidence_outcomes"][0]["probability"] = 0.4
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_negative_probability(self):
        p = fixture()
        p["evidence_outcomes"][0]["probability"] = -0.5
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_bool_probability(self):
        p = fixture()
        p["evidence_outcomes"][0]["probability"] = True
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_nonfinite_utility(self):
        p = fixture()
        p["evidence_outcomes"][0]["action_values"]["fix"] = float("nan")
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_missing_action_values(self):
        p = fixture()
        del p["evidence_outcomes"][0]["action_values"]["fix"]
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_duplicate_outcome(self):
        p = fixture()
        p["evidence_outcomes"][1]["id"] = "state-a"
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_duplicate_action(self):
        p = fixture()
        p["actions"][1]["id"] = "fix"
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_never_authorize_active_dispatch(self):
        p = fixture()
        p["mode"] = "active"
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_reject_negative_research_cost(self):
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(fixture(-1))


if __name__ == "__main__":
    unittest.main()
