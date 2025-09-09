PY=python
install:
	$(PY) -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt
run:
	$(PY) -m src.cli run --config config/main.yaml --scenario all --trials 50
summarize:
	$(PY) -m src.cli summarize --results results --out reports/summary.csv
plot:
	$(PY) -m src.cli plot --results results --out reports/figures
