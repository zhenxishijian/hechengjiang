#!/usr/bin/env bash
set -euo pipefail

echo "[1/8] Update apt index"
sudo apt update

echo "[2/8] Install base build/runtime deps"
sudo apt install -y \
  ca-certificates curl git \
  python3 python3-venv python3-pip \
  build-essential cmake pkg-config

echo "[3/8] Optional Java runtime for Spark"
sudo apt install -y openjdk-17-jre || true

echo "[4/8] Show tool versions"
python3 --version
pip3 --version
cmake --version
g++ --version || true
java -version || true

echo "[5/8] Prepare python virtual environment"
cd "$(dirname "$0")/.."
python3 -m venv python/.venv
source python/.venv/bin/activate
python -m pip install --upgrade pip
pip install --no-cache-dir -r python/requirements.txt



echo "[6/8] Check free disk space before optional Spark install"
FREE_MB=$(df -Pm . | awk 'NR==2 {print $4}')
# pyspark wheel/jars can require significant temp space; use ~8GB as safe threshold
if [ "$FREE_MB" -lt 8192 ]; then
  echo "[WARN] Only ${FREE_MB}MB free; skip optional pyspark install to avoid 'No space left on device'."
  SKIP_SPARK=1
else
  SKIP_SPARK=0
fi

echo "[7/8] Try optional Spark/MLlib dependency (non-blocking)"
if [ "$SKIP_SPARK" -eq 0 ] && ! pip install --no-cache-dir -r python/requirements-ml.txt; then
  echo "[WARN] pyspark install failed; continue with fallback mode (no Spark runtime)."
fi

echo "[8/8] Quick verification run"
PYTHONPATH=python python -m rdma_ai_opt.cli --input python/sample_metrics.jsonl --report reports/latest
cmake -S cpp -B build
cmake --build build
./build/rdma_optimizer --metrics python/sample_metrics.jsonl --python-script python/rdma_bridge.py

echo "Done. Reports generated under reports/latest"
