#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ ! -f .env || ! -f prometheus/targets.json ]]; then
  echo "First run: python3 scripts/configure.py VM_IPV4" >&2
  exit 1
fi
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt
docker compose config --quiet
docker compose up -d --build minio prometheus
.venv/bin/python scripts/init-bucket.py
docker compose up -d
docker compose ps
echo "Grafana: http://127.0.0.1:3000/d/linux-lab (admin; password in .env)"
