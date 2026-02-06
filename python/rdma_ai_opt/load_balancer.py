from __future__ import annotations

from typing import Dict, List


def predict_hotspot(metrics: List[Dict[str, float]]) -> Dict[str, str]:
    if not metrics:
        return {"action": "hold", "detail": "无数据"}

    recent = metrics[-3:]
    lat = [x["latency_us"] for x in recent]
    rising = all(lat[i] <= lat[i + 1] for i in range(len(lat) - 1))

    if rising and lat[-1] > 12:
        return {
            "action": "shift_flows",
            "detail": "检测到延迟持续上升，建议将热点流迁移到低 hop 路径。",
        }
    return {"action": "hold", "detail": "当前负载趋势稳定。"}
