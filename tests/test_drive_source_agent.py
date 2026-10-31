import unittest
from tools.drive_source_agent import (CAPTION, MARKER, execute, gate, validated_context,
                                      verify_synthetic_export_bytes)

BASE = {"task_id": "DEMO-2026-10-29-A",
        "source_class": "synthetic_public_fixture",
        "source_state": "missing", "requires_original": True}


class SelectiveDriveTests(unittest.TestCase):
    def test_utf8_drive_text_export_with_non_ascii_marker(self):
        # Drive text/plain may omit charset, so requests .text can misdecode
        # the em dash. The actual UTF-8 bytes must still match exactly.
        payload = ("Title\n" + MARKER + "\n" + CAPTION + "\n").encode("utf-8")
        self.assertTrue(verify_synthetic_export_bytes(payload))
        self.assertTrue(verify_synthetic_export_bytes(b"\xef\xbb\xbf" + payload))
        self.assertNotEqual(MARKER, MARKER.encode("utf-8").decode("latin-1"))

    def test_invalid_encoding_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "^FIXTURE_ENCODING_INVALID$"):
            verify_synthetic_export_bytes(b"\xff\x80")

    def test_missing_caption_still_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "^FIXTURE_MISMATCH$"):
            verify_synthetic_export_bytes(MARKER.encode("utf-8"))

    def test_missing_marker_still_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "^FIXTURE_MISMATCH$"):
            verify_synthetic_export_bytes(CAPTION.encode("utf-8"))

    def test_fixture_simulation_not_autonomy(self):
        out = execute(BASE, "fixture")
        self.assertEqual(out["decision"], "READ")
        self.assertFalse(out["ai_decision"])
        self.assertFalse(out["drive_read_verified"])

    def test_bounded_model_read_invokes_drive_once(self):
        calls = []
        def model(*_):
            calls.append("model")
            return "READ"
        def drive(_):
            calls.append("drive")
            return True
        out = execute(BASE, "synthetic-read", model_call=model, drive_call=drive)
        self.assertEqual(calls, ["model", "drive"])
        self.assertTrue(out["drive_read_verified"])

    def test_shadow_no_drive_read(self):
        def forbidden(_):
            raise AssertionError("unexpected drive")
        out = execute(BASE, "shadow", model_call=lambda *_: "READ", drive_call=forbidden)
        self.assertFalse(out["drive_read_verified"])

    def test_present_forces_skip_even_if_model_wrong(self):
        out = execute(dict(BASE, source_state="present"), "synthetic-read",
                      model_call=lambda *_: "READ",
                      drive_call=lambda _: (_ for _ in ()).throw(AssertionError()))
        self.assertEqual(out["decision"], "SKIP")

    def test_unknown_forces_hold(self):
        out = execute(dict(BASE, source_state="unknown"), "synthetic-read",
                      model_call=lambda *_: "READ",
                      drive_call=lambda _: (_ for _ in ()).throw(AssertionError()))
        self.assertEqual(out["decision"], "HOLD")

    def test_nonessential_source_forces_hold(self):
        out = execute(dict(BASE, requires_original=False), "synthetic-read",
                      model_call=lambda *_: "READ",
                      drive_call=lambda _: (_ for _ in ()).throw(AssertionError()))
        self.assertEqual(out["decision"], "HOLD")

    def test_private_source_class_rejected(self):
        with self.assertRaises(ValueError):
            execute(dict(BASE, source_class="patient_record"), "fixture")

    def test_nonallowlisted_task_rejected(self):
        with self.assertRaises(ValueError):
            validated_context(dict(BASE, task_id="another"))

    def test_unknown_decision_gate_fails_closed(self):
        self.assertEqual(gate(validated_context(BASE), "PUBLISH"), "HOLD")

    def test_model_failure_never_triggers_read(self):
        def broken(*_):
            raise RuntimeError("MODEL_REQUEST_FAILED")
        with self.assertRaises(RuntimeError):
            execute(BASE, "synthetic-read", model_call=broken,
                    drive_call=lambda _: (_ for _ in ()).throw(AssertionError()))


if __name__ == "__main__":
    unittest.main()
