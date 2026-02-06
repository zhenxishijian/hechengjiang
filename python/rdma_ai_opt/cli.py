from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="RDMA AI optimizer CLI")
    parser.add_argument("--input", required=True, help="Metrics JSONL path")
    parser.add_argument("--report", required=True, help="Report output directory")
    args = parser.parse_args()

    result = run_pipeline(Path(args.input), Path(args.report))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
