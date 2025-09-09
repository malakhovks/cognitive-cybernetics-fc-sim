#!/usr/bin/env bash
set -euo pipefail
python -m src.cli run --config config/main.yaml --scenario all --trials 50
python -m src.cli summarize --results results --out reports/summary.csv
python -m src.cli plot --results results --out reports/figures
echo "All done. See reports/ and results/."
