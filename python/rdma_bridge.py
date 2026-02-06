#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from rdma_ai_opt.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="RDMA AI optimizer bridge")
    parser.add_argument("--input", required=True, help="JSONL metrics input path")
    parser.add_argument("--report", required=True, help="Report output directory")
    args = parser.parse_args()

    result = run_pipeline(Path(args.input), Path(args.report))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
