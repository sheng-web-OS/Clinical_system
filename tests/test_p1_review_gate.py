"""Regression fixtures for the actual #171 P1 escape and safe resolution."""
import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "tools/p1_review_gate.py"
spec = importlib.util.spec_from_file_location("p1_review_gate", FILE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

SHA = "a" * 40
NEW_SHA = "b" * 40
PR = {"head": {"sha": SHA}, "user": {"login": "author"}}


def comment(body, *, cid=6442587535, source="issue", who="reporter",
            trusted="COLLABORATOR", created="2026-10-27T13:00:00Z"):
    return {"source": source, "id": cid, "body": body,
            "author_association": trusted, "user": {"login": who},
            "created_at": created, "html_url": "https://github.com/example/repo/pull/171"}


LEGACY_171 = (
    "【出版前去重 P1／已實際核對 main SHA】"
    "與舊文依年度、梯次、科目、題號比對，26 題重疊。"
    "請不要將現有 46 題直接以第二篇完整跨科攻略發佈。"
)


class P1ReviewHardStopTests(unittest.TestCase):
    def test_original_171_p1_warning_would_have_blocked_merge(self):
        self.assertTrue(gate.is_blocker(comment(LEGACY_171)))
        self.assertEqual(len(gate.evaluate(PR, [comment(LEGACY_171)])), 1)

    def test_explicit_marker_always_blocks_for_trusted_reviewer(self):
        self.assertEqual(len(gate.evaluate(PR, [comment(
            "[P1_BLOCK] wrong official answer", cid=10
        )])), 1)

    def test_untrusted_comment_cannot_block_or_unblock(self):
        self.assertEqual(gate.evaluate(PR, [comment(
            "[P1_BLOCK] spam", trusted="NONE"
        )]), [])

    def test_fix_claim_without_structured_clearance_does_not_clear(self):
        records = [
            comment(LEGACY_171),
            comment("P1 已經修好了，不必再阻塞", cid=2,
                    who="reviewer", created="2026-10-27T14:00:00Z"),
        ]
        self.assertEqual(len(gate.evaluate(PR, records)), 1)

    def test_old_sha_review_does_not_unlock_new_head(self):
        clear = f"[P1_RESOLVED source=issue id=6442587535 head={NEW_SHA} evidence=https://github.com/example/repo/pull/171]"
        self.assertEqual(len(gate.evaluate(PR, [
            comment(LEGACY_171),
            comment(clear, cid=12, who="reviewer", created="2026-10-27T14:00:00Z"),
        ])), 1)

    def test_pr_author_cannot_self_sign(self):
        clear = f"[P1_RESOLVED source=issue id=6442587535 head={SHA} evidence=https://github.com/example/repo/pull/171]"
        self.assertEqual(len(gate.evaluate(PR, [
            comment(LEGACY_171),
            comment(clear, cid=12, who="author", created="2026-10-27T14:00:00Z"),
        ])), 1)

    def test_independent_reviewer_must_reference_comment_and_exact_head(self):
        clear = f"[P1_RESOLVED source=issue id=6442587535 head={SHA} evidence=https://github.com/example/repo/actions/runs/123]"
        records = [
            comment(LEGACY_171),
            comment(clear, cid=12, who="reviewer", created="2026-10-27T14:00:00Z"),
        ]
        self.assertEqual(gate.evaluate(PR, records), [])
        self.assertEqual(len(gate.evaluate(
            PR, [comment(LEGACY_171),
                 comment(clear.replace("id=6442587535", "id=999"),
                         cid=12, who="reviewer", created="2026-10-27T14:00:00Z")],
        )), 1)

    def test_resolution_must_be_after_block_and_from_trusted_reviewer(self):
        clear = f"[P1_RESOLVED source=issue id=6442587535 head={SHA} evidence=https://github.com/example/repo/pull/171]"
        for who, trusted, created in [
            ("reviewer", "NONE", "2026-10-27T14:00:00Z"),
            ("reviewer", "COLLABORATOR", "2026-10-27T12:00:00Z"),
        ]:
            with self.subTest(who=who, trusted=trusted, created=created):
                self.assertEqual(len(gate.evaluate(PR, [
                    comment(LEGACY_171),
                    comment(clear, cid=12, who=who, trusted=trusted, created=created),
                ])), 1)

    def test_normal_comment_and_regular_review_do_not_false_block(self):
        self.assertEqual(gate.evaluate(PR, [
            comment("P1 修復已發表，來源附錄記載出版歷程，無阻塞意見", cid=3),
            comment("approved routine proofread", cid=4, source="review"),
        ]), [])

    def test_issue_comment_event_uses_its_pr_number(self):
        self.assertEqual(gate.event_pr_number({
            "issue": {"number": 171, "pull_request": {"url": "https://api.github.com/pulls/171"}}
        }), 171)


if __name__ == "__main__":
    unittest.main()
