#!/usr/bin/env bash
set -euo pipefail
python -m pip install --disable-pip-version-check -r requirements.txt
python tools/validate.py
python tools/check_corpus_inventory.py
python site/visual_quality.py --report /tmp/clinical-os-visual-quality-report.json
python site/build.py
python tools/check_output.py
