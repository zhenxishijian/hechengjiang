#!/usr/bin/env bash
set -euo pipefail

echo "[1/6] Update apt index"
sudo apt update

echo "[2/6] Install base build/runtime deps"
sudo apt install -y \
  ca-certificates curl git \
  python3 python3-venv python3-pip \
  build-essential cmake pkg-config

echo "[3/6] Optional Java runtime for Spark"
sudo apt install -y openjdk-17-jre || true

echo "[4/6] Show tool versions"
python3 --version
pip3 --version
cmake --version
g++ --version || true
java -version || true

echo "[5/6] Prepare python virtual environment"
cd "$(dirname "$0")/.."
python3 -m venv python/.venv
source python/.venv/bin/activate
python -m pip install --upgrade pip
pip install -r python/requirements.txt

echo "[6/6] Quick verification run"
PYTHONPATH=python python -m rdma_ai_opt.cli --input python/sample_metrics.jsonl --report reports/latest
cmake -S cpp -B build
cmake --build build
./build/rdma_optimizer --metrics python/sample_metrics.jsonl --python-script python/rdma_bridge.py

echo "Done. Reports generated under reports/latest"
