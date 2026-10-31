"""Synthetic, no Anki/Drive/real learning records: reversible quality quarantine."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

anki = types.ModuleType("ale_anki_readonly")
anki.check_version = lambda: 6
anki.invoke = lambda action, **params: []
anki.ENDPOINT = "http://127.0.0.1:8765"
anki.API_VERSION = 6
drive = types.ModuleType("ale_anki_drive_sync")
drive.BASE = Path("/nonexistent-private-owner")
drive.private_dir = lambda path: None
drive.private_write = lambda path, x: None
drive.load_json = lambda path: {}
flags = types.ModuleType("ale_anki_flag_feedback")
flags.read_flagged_cards = lambda: {}

path = Path(__file__).resolve().parents[1] / "tools" / "ale_anki_quality_quarantine.py"
spec = importlib.util.spec_from_file_location("ale_anki_quality_quarantine", path)
mod = importlib.util.module_from_spec(spec)
with patch.dict(sys.modules, {"ale_anki_readonly": anki, "ale_anki_drive_sync": drive,
                              "ale_anki_flag_feedback": flags}):
    spec.loader.exec_module(mod)

def decision(cid=42):
    card = {"cardId": cid, "note": 9, "question": "Q", "answer": "A", "flags": 0}
    return card, {"anki_card_id":cid, "anki_note_id":9, "decision":"QUALITY_QUARANTINE",
                  "evidence_state":"INDEPENDENTLY_REVIEWED", "evidence_ref":"owner-private:qa-reviewed",
                  "reason_code":"AMBIGUOUS_PROMPT",
                  "content_sha256": mod.card_content_fingerprint(card)}

class TestQuarantine(unittest.TestCase):
    def test_empty_decisions(self):
        self.assertEqual(mod.approved_decisions({}), [])

    def test_ai_self_report_without_independent_review_cannot_suspend(self):
        card, d = decision()
        d["evidence_state"] = "MODEL_GUESS"
        with self.assertRaisesRegex(RuntimeError, "independent"):
            mod.approved_decisions({"schema":1, "decisions":[d]})

    def test_duplicate_ai_decision_rejected(self):
        _, d = decision()
        with self.assertRaisesRegex(RuntimeError, "Duplicate"):
            mod.approved_decisions({"schema":1,"decisions":[d,d]})

    def test_denies_unapproved_api_mutations(self):
        for action in ("unsuspend", "updateNoteFields", "answerCards", "deleteNotes"):
            with self.assertRaises(ValueError):
                mod.write_action(action, cards=[42])

    def test_denies_wrong_flag(self):
        with self.assertRaises(ValueError):
            mod.write_action("setFlag", cards=[42], flag=3)

    def test_first_scan_baselines_existing_flags_no_mutation(self):
        card,_=decision()
        with patch.object(mod.Path,"exists",return_value=True), \
             patch.object(mod,"read_flagged_cards",return_value={"42":9}), \
             patch.object(mod,"check_card",return_value=card), \
             patch.object(mod,"is_suspended",return_value=False), \
             patch.object(mod,"write_action") as writer, \
             patch.object(mod,"private_write") as state:
            self.assertEqual(mod.apply(Path("/unused"),dry_run=False)["applied"],0)
            writer.assert_not_called()
            self.assertEqual(state.call_args.args[1]["flagged_ids"], ["42"])

    def test_owner_flag_eligible_dry_run_zero_writes(self):
        card, _ = decision()
        with patch.object(mod.Path, "exists", return_value=True), \
             patch.object(mod, "read_flagged_cards", return_value={"42":9}), \
             patch.object(mod, "check_card", return_value=card), \
             patch.object(mod, "is_suspended", return_value=False), \
             patch.object(mod, "write_action") as writer:
            self.assertEqual(mod.apply(Path("/unused"), dry_run=True)["eligible_to_quarantine"],1)
            writer.assert_not_called()

    def test_owner_red_flag_apply_suspend_only_exact_card(self):
        card, _ = decision()
        suspended = {"value":False}
        def flag_is_suspended(cid): return suspended["value"]
        def do_write(action, **params):
            self.assertEqual(action, "suspend")
            self.assertEqual(params["cards"], [42])
            suspended["value"] = True
        with patch.object(mod, "read_flagged_cards", return_value={"42":9}), \
             patch.object(mod, "check_card", return_value=card), \
             patch.object(mod, "is_suspended", side_effect=flag_is_suspended), \
             patch.object(mod, "write_action", side_effect=do_write), \
             patch.object(mod, "private_write") as audit:
            self.assertEqual(mod.apply(Path("/unused"), dry_run=False)["applied"],1)
            self.assertGreaterEqual(audit.call_count, 2)
            self.assertEqual(audit.call_args_list[0].args[1]["actions"][0]["reason"],"OWNER_RED_FLAG")

    def test_existing_suspend_not_repeated(self):
        card,_=decision()
        with patch.object(mod,"read_flagged_cards",return_value={"42":9}), \
             patch.object(mod,"check_card",return_value=card), \
             patch.object(mod,"is_suspended",return_value=True), \
             patch.object(mod,"write_action") as writer:
            self.assertEqual(mod.apply(Path("/unused"),dry_run=False)["already_suspended"],1)
            writer.assert_not_called()

    def test_ai_candidate_stale_content_rejected(self):
        card,d=decision()
        d["content_sha256"]="0"*64
        with patch.object(mod,"read_flagged_cards",return_value={}), \
             patch.object(mod,"load_json",side_effect=lambda p: {"schema":1,"decisions":[d]}), \
             patch.object(mod,"check_card",return_value=card), \
             patch.object(mod,"write_action") as writer:
            with self.assertRaisesRegex(RuntimeError,"Stale"):
                mod.apply(Path("/unused"),dry_run=False)
            writer.assert_not_called()

    def test_ai_reviewed_candidate_automatic_flag_and_suspend(self):
        card,d=decision()
        current_flag=0
        suspended=False
        def info(cid,note=None):
            return {**card,"flags":current_flag}
        def is_held(cid): return suspended
        def act(action,**params):
            nonlocal current_flag,suspended
            if action=="setFlag":
                current_flag=1
                self.assertEqual(params,{"cards":[42],"flag":1})
            else:
                self.assertEqual(action,"suspend")
                suspended=True
        def local(path):
            if path.name.endswith("decisions.json"):
                return {"schema":1,"decisions":[d]}
            return {}
        with patch.object(mod,"read_flagged_cards",return_value={}), \
             patch.object(mod,"load_json",side_effect=local), \
             patch.object(mod,"check_card",side_effect=info), \
             patch.object(mod,"is_suspended",side_effect=is_held), \
             patch.object(mod,"write_action",side_effect=act), \
             patch.object(mod,"private_write") as audit:
            self.assertEqual(mod.apply(Path("/unused"),dry_run=False)["applied"],1)
            self.assertEqual(current_flag,1)
            self.assertTrue(suspended)
            self.assertEqual(audit.call_args_list[0].args[1]["actions"][0]["reason"],"AMBIGUOUS_PROMPT")

    def test_identity_mismatch_cannot_apply(self):
        card, d=decision()
        with patch.object(mod,"read_flagged_cards",return_value={"42":123}), \
             patch.object(mod,"load_json",side_effect=lambda p: {"schema":1,"decisions":[d]}):
            with self.assertRaisesRegex(RuntimeError,"collision"):
                mod.apply(Path("/unused"), dry_run=False)

    def test_unreviewed_decision_skipped(self):
        _,d=decision()
        d["decision"]="CANDIDATE_ONLY"
        self.assertEqual(mod.approved_decisions({"schema":1,"decisions":[d]}),[])

if __name__ == "__main__":
    unittest.main()
