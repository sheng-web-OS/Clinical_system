"""Discover synthetic A02 regressions in the existing PR CI test suite.

Tests live in an isolated experiment; this bridge changes no production code.
"""
import sys
from pathlib import Path

EXPERIMENT = Path(__file__).resolve().parents[1] / "experiments" / "a02-growth-evidence"
sys.path.insert(0, str(EXPERIMENT))
from test_growth_leakage import GrowthLeakageContract  # noqa: E402,F401
