"""CI-discovered bridge readback tests; fully synthetic, no Mac or OAuth needed.

The bridge's own smoke suite is under tools/; include integrity regressions
in the project's standard python -m unittest discover -s tests gate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from test_ale_anki_drive_sync import ContentReadbackTests  # noqa: F401

