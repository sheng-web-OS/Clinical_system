"""Public synthetic transport-contract tests; not a blinded reasoning benchmark."""
import copy
import unittest
from canary import unique_work


def event(delivery="delivery-1", **changes):
    item = {"repository": "synthetic/example", "pr_number": 7,
            "head_sha": "a" * 40, "next_gate": "engineering-review",
            "evidence_revision": "synthetic-revision-1", "delivery_id": delivery}
    item.update(changes)
    return item


class CanaryContract(unittest.TestCase):
    def test_empty(self):
        self.assertEqual([], unique_work([]))

    def test_same_work_with_different_deliveries_is_one_unit(self):
        a, b = event("delivery-1"), event("delivery-2")
        self.assertEqual([a], unique_work([a, b]))

    def test_distinct_head_with_same_delivery_is_preserved(self):
        a, b = event(), event(head_sha="b" * 40)
        self.assertEqual([a, b], unique_work([a, b]))

    def test_distinct_gate_with_same_delivery_is_preserved(self):
        a, b = event(), event(next_gate="verify-ci")
        self.assertEqual([a, b], unique_work([a, b]))

    def test_changed_evidence_with_same_delivery_is_preserved(self):
        a, b = event(), event(evidence_revision="synthetic-revision-2")
        self.assertEqual([a, b], unique_work([a, b]))

    def test_identical_replay_is_one_unit(self):
        a = event()
        self.assertEqual([a], unique_work([a, copy.deepcopy(a)]))

    def test_first_record_and_order_are_preserved(self):
        a, b = event("delivery-1"), event("delivery-2", pr_number=8)
        self.assertEqual([a, b], unique_work([a, b, copy.deepcopy(a)]))

    def test_inputs_are_not_mutated(self):
        records = [event(), event("delivery-2")]
        original = copy.deepcopy(records)
        unique_work(records)
        self.assertEqual(original, records)


if __name__ == "__main__":
    unittest.main(verbosity=2)
