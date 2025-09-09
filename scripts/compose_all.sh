#!/usr/bin/env bash
set -euo pipefail
docker compose up --build simulator
docker compose run --rm summarize
docker compose run --rm plot
echo "Done. See reports/ and results/"
