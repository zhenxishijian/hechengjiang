from __future__ import annotations

from pathlib import Path
from typing import Dict

from .load_balancer import predict_hotspot
from .model import mllib_predict_latency
from .monitor import load_metrics_jsonl
from .report import write_report
from .tuner import recommend_params


def run_pipeline(input_path: Path, report_dir: Path) -> Dict:
    metrics = load_metrics_jsonl(input_path)
    pred = mllib_predict_latency(metrics)
    tuning = recommend_params(pred)
    lb = predict_hotspot(metrics)

    result = {
        "prediction": {
            "predicted_latency_us": pred.predicted_latency_us,
            "overload_risk": pred.overload_risk,
        },
        "tuning": tuning.to_dict(),
        "load_balance": lb,
        "sample_count": len(metrics),
    }

    result = write_report(report_dir, result, metrics)
    write_report(report_dir, result)
    return result
