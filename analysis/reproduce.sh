#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${BONDORA_PYTHON:-python3}"
"$PYTHON_BIN" analysis/test_endpoints.py
"$PYTHON_BIN" analysis/run.py data/Bondora_Estonia_2013_2015.csv.gz \
  --cutoff 2021-07-20 \
  --cutoff-evidence 'ReportAsOfEOD=2021-07-20 in every uploaded row' \
  --default-evidence 'First recorded DefaultDate; source arrears threshold unavailable, no 60/90-day interpretation claimed' \
  --repayment-evidence 'ContractEndDate ONLY for Status=Repaid is a recorded closure proxy, not guaranteed full cash repayment. Financial and LastPaymentOn audit plus stricter closure sensitivity supplied.'
"$PYTHON_BIN" analysis/verify.py data/Bondora_Estonia_2013_2015.csv.gz
"$PYTHON_BIN" analysis/make_report.py
"$PYTHON_BIN" analysis/cumulative_incidence.py
