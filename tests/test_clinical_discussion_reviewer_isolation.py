"""Static isolation guards for clinical Discussion reviewer inputs.

These tests verify the prompt/fixture contract only. They do not run an AI,
establish independent judgement, or approve medical content or publication.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
SOP = ROOT / "docs" / "clinical-discussion-depth-sop.md"

def load(path):
    return path.read_text(encoding="utf-8")


class ClinicalDiscussionReviewerIsolation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.common = load(AUDIT / "clinical-discussion-neutral-reviewer-packet.md")
        cls.sop = load(SOP)
        cls.handoff = load(AUDIT / "clinical-discussion-depth-reviewer-handoff.md")
        cls.protocol = load(AUDIT / "clinical-discussion-depth-unhinted-calibration.md")
        cls.frozen = load(AUDIT / "fixtures" / "ba-aneurysm-discussion-202609-frozen.md")

    def test_frozen_historical_source_is_nine_slides(self):
        matches = re.findall(r"^## Slide ([1-9])\b", self.frozen, flags=re.M)
        self.assertEqual(matches, list("123456789"))

    def test_common_packet_does_not_assign_a_specific_arm(self):
        # A baseline must not inadvertently inherit C's reasoning intervention
        # or B's negative presumption.
        for forbidden in (
            "highest-consequence", "most consequential clinical disagreement",
            "before praising", "first identify the most important",
            "Why?", "How do you know?", "This Discussion is poor",
            "your assessment was too generous",
        ):
            self.assertNotIn(forbidden.lower(), self.common.lower())
        self.assertIn("one separate short instruction", self.common)

    def test_common_and_generic_sop_do_not_contain_answer_key(self):
        forbidden = ("BA aneurysm", "78/100", "Slide 2", "Slide 8",
                     "expected RED", "should fail", "historical red label")
        # The common packet references the source path, but must not
        # include its failure labels or the expected clinician critique.
        for word in forbidden:
            if word == "BA aneurysm":
                self.assertNotIn(word, self.sop)
                continue
            self.assertNotIn(word, self.common)
            self.assertNotIn(word, self.sop)
        self.assertIn("Clinical Discussion Depth SOP", self.sop)

    def test_answer_bearing_handoff_is_separate(self):
        self.assertIn("COORDINATOR / EVALUATOR ONLY", self.handoff)
        self.assertIn("DO NOT PROVIDE THIS DOCUMENT TO THE REVIEWER",
                      self.handoff)
        self.assertNotIn("PR #205", self.common)
        self.assertNotIn("issuecomment", self.common)

    def test_protocol_separates_first_pass_and_post_feedback(self):
        for requirement in (
            "Experiment T1", "Experiment T2", "Experiment S",
            "A: neutral", "B: negative cue",
            "C: problem-first independent reconstruction",
            "N (neutral)", "B (negative pressure)", "P (positive pressure)",
            "same original reviewer response",
            "unsupported_flip_rate", "supported_new_detection_rate",
            "valid_claim_reversal_rate", "COUNTERFACTUAL_BRANCHING_NOT_AVAILABLE",
            "MEMORY_EXPOSURE_NOT_VERIFIED", "T2-E expert-attributed negative cue",
            "REPORTED_NOT_INDEPENDENTLY_VERIFIED",
        ):
            self.assertIn(requirement, self.protocol)
        self.assertIn("T1 and T2 answer different causal questions",
                      self.protocol)

    def test_normal_controls_and_uncertainty_are_explicit(self):
        self.assertIn("positive *claim-preservation controls*", self.protocol)
        self.assertIn("GREEN", self.protocol)
        self.assertIn("NOT_MEASURED", self.protocol)
        self.assertIn("NOT_EFFECTIVENESS_VALIDATED", self.protocol)
        self.assertIn("NOT_VERIFIABLE", self.protocol)
        self.assertIn("not an executed experiment", self.protocol)

if __name__ == "__main__":
    unittest.main()
