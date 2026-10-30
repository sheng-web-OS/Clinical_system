"""Deterministic synthetic mechanical tests. No clinical/agent transfer claims."""
import importlib.util
from pathlib import Path
import unittest
import copy
import json

MODULE_PATH = (Path(__file__).resolve().parents[1] /
               "experiments/literature-voi-shadow/voi.py")
spec = importlib.util.spec_from_file_location("literature_voi_pilot", MODULE_PATH)
voi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voi)


def fixture(cost=1):
    return {
        "schema_version": 1, "mode": "shadow", "research_cost": cost,
        "actions": [{"id": "fix", "gate": "eligible"},
                    {"id": "inspect", "gate": "eligible"}],
        "evidence_outcomes": [
            {"id": "state-a", "probability": 0.5,
             "action_values": {"fix": 10, "inspect": 0}},
            {"id": "state-b", "probability": 0.5,
             "action_values": {"fix": 0, "inspect": 10}}],
        "research_signals": [
            {"id": "finding-a",
             "likelihood_by_state": {"state-a": 1, "state-b": 0}},
            {"id": "finding-b",
             "likelihood_by_state": {"state-a": 0, "state-b": 1}}],
    }


class LiteratureValueOfInformationShadowTest(unittest.TestCase):
    def test_perfect_signal_has_evsi_five_net_four(self):
        r = voi.decide(fixture())
        self.assertEqual("SHADOW_SUGGEST_RESEARCH", r["decision"])
        self.assertEqual("5.0", r["evpi_upper_bound"])
        self.assertEqual("5.00", r["hypothetical_evsi"])
        self.assertEqual("4.00", r["hypothetical_net_information_value"])
        self.assertFalse(r["execution_authorized"])
        self.assertFalse(r["information_model_verified"])
        self.assertEqual(0, r["external_calls"])

    def test_zero_information_never_greenlights_search(self):
        p = fixture(0.01)
        for signal in p["research_signals"]:
            signal["likelihood_by_state"] = {"state-a": 0.5, "state-b": 0.5}
        r = voi.decide(p)
        self.assertEqual("SHADOW_CONTINUE_DIRECT", r["decision"])
        self.assertEqual("0.0000", r["hypothetical_evsi"])

    def test_evpi_without_signal_does_not_recommend_search(self):
        p = fixture()
        del p["research_signals"]
        r = voi.decide(p)
        self.assertEqual("SHADOW_NEEDS_SIGNAL_MODEL", r["decision"])
        self.assertEqual("EVPI_ONLY_UPPER_BOUND", r["reason"])

    def test_cost_exceeds_perfect_bound_skip_without_model(self):
        p = fixture(6)
        del p["research_signals"]
        self.assertEqual("SHADOW_CONTINUE_DIRECT", voi.decide(p)["decision"])

    def test_imperfect_signal_worth_small_cost(self):
        p = fixture(0.5)
        p["research_signals"][0]["likelihood_by_state"] = {"state-a": 0.6, "state-b": 0.4}
        p["research_signals"][1]["likelihood_by_state"] = {"state-a": 0.4, "state-b": 0.6}
        r = voi.decide(p)
        self.assertEqual("SHADOW_SUGGEST_RESEARCH", r["decision"])
        self.assertEqual("1.0000", r["hypothetical_evsi"])

    def test_imperfect_signal_not_worth_large_cost(self):
        p = fixture(2)
        p["research_signals"][0]["likelihood_by_state"] = {"state-a": 0.6, "state-b": 0.4}
        p["research_signals"][1]["likelihood_by_state"] = {"state-a": 0.4, "state-b": 0.6}
        self.assertEqual("SHADOW_CONTINUE_DIRECT", voi.decide(p)["decision"])

    def test_skip_when_evidence_never_changes_best_action(self):
        p = fixture()
        p["evidence_outcomes"][1]["action_values"] = {"fix": 10, "inspect": 0}
        self.assertEqual("SHADOW_CONTINUE_DIRECT", voi.decide(p)["decision"])

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

    def test_signals_must_be_normalized_per_state(self):
        p = fixture()
        p["research_signals"][1]["likelihood_by_state"]["state-b"] = 0.5
        with self.assertRaisesRegex(voi.InvalidProposal, "SIGNAL_DISTRIBUTION"):
            voi.decide(p)

    def test_signal_requires_complete_state_distribution(self):
        p = fixture()
        del p["research_signals"][1]["likelihood_by_state"]["state-b"]
        with self.assertRaisesRegex(voi.InvalidProposal, "SIGNAL_LIKELIHOODS"):
            voi.decide(p)

    def test_signal_duplicate_rejected(self):
        p = fixture()
        p["research_signals"][1]["id"] = "finding-a"
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_empty_signal_list_rejected(self):
        p = fixture()
        p["research_signals"] = []
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaises(voi.InvalidProposal):
            json.loads('{"mode":"active","mode":"shadow"}',
                       object_pairs_hook=voi.strict_object)

    def test_json_nonfinite_rejected_by_number(self):
        with self.assertRaises(voi.InvalidProposal):
            voi.number(float("inf"), "utility")

    def test_unbounded_states_rejected(self):
        p = fixture()
        p["evidence_outcomes"] = [copy.deepcopy(p["evidence_outcomes"][0])] * 65
        with self.assertRaises(voi.InvalidProposal):
            voi.decide(p)


if __name__ == "__main__":
    unittest.main()
