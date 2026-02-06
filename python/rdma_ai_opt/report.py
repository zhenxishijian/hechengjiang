from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


def write_report(output_dir: Path, result: Dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "report.json"
    md_path = output_dir / "report.md"

    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = f"""# RDMA AI 优化报告

## 预测结果
- 预测延迟: {result['prediction']['predicted_latency_us']:.3f} us
- 过载风险: {result['prediction']['overload_risk']:.3f}

## 参数建议
- MTU: {result['tuning']['recommended']['mtu']}
- QP 数量: {result['tuning']['recommended']['qp_count']}
- CQ moderation: {result['tuning']['recommended']['cq_moderation']}
- Inline size: {result['tuning']['recommended']['inline_size']}
- 原因: {result['tuning']['rationale']}

## 负载均衡
- 动作: {result['load_balance']['action']}
- 说明: {result['load_balance']['detail']}
"""
    md_path.write_text(md, encoding="utf-8")
