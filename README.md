# Feedback-Controlled Knowledge-Production Simulator

A reference implementation of the simulation and controllers described in the project:
**Cognitive Cybernetics of Computer Science Evolution: A Feedback-Driven Environment for Knowledge Production**.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.cli run --config config/main.yaml --scenario all --trials 50
python -m src.cli summarize --results results --out reports/summary.csv
python -m src.cli plot --results results --out reports/figures
```

## Docker Compose

```bash
# optional: copy and adjust env
cp .env.example .env

# build image and run simulator
docker compose up --build simulator

# then summarize and plot
docker compose run --rm summarize
docker compose run --rm plot
```

Bind mounts map `config/`, `results/`, `reports/`, and `data/` into the container.
Adjust `SCENARIO` and `TRIALS` in `.env` as needed.

## Repository Layout
- `src/` — simulation core, controllers, CLI, analysis utilities
- `config/` — YAML configs (experiment parameters)
- `tests/` — pytest unit tests
- `scripts/` — helper shell scripts (e.g., run all / compose)
- `docs/` — technical note & diagrams
- `results/`, `reports/`, `data/` — generated outputs & optional inputs

See **Placement Notes** in this README and the structure tree below.
