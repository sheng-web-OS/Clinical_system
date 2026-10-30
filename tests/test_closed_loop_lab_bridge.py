"""Run the isolated, synthetic-only autonomy lab as part of ordinary CI discovery.

The lab cannot access GitHub, real leases, patient data, or platform services.
This file runs its fixed regression tests; it does not activate the dispatcher.
"""
from pathlib import Path
import unittest

LAB = Path(__file__).resolve().parents[1] / "experiments" / "autonomy-shadow" / "closed-loop-lab"


def load_tests(loader, tests, pattern):
    return loader.discover(start_dir=str(LAB), pattern="test_*.py", top_level_dir=str(LAB))
