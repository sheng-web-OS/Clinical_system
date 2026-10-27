#!/usr/bin/env bash
set -euo pipefail
python -m pip install --disable-pip-version-check -r requirements.txt
python tools/validate.py
python tools/check_corpus_inventory.py
python site/build.py
python tools/check_output.py
python tools/check_release_security.py
