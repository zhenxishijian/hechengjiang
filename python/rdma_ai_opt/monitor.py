from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


Metric = Dict[str, float]


def load_metrics_jsonl(path: Path) -> List[Metric]:
    records: List[Metric] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records
