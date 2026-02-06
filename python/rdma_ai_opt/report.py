from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


Metric = Dict[str, float]


def _write_svg_fallback(output_dir: Path, metrics: List[Metric]) -> str:
    """Generate a tiny self-contained SVG chart when matplotlib is unavailable."""
    svg_path = output_dir / "latency_trend.svg"
    if not metrics:
        svg_path.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="240">'
            '<text x="20" y="40" font-size="18">No metrics data</text></svg>',
            encoding="utf-8",
        )
        return svg_path.name

    values = [float(m["latency_us"]) for m in metrics]
    width, height = 640, 240
    margin = 30
    min_v, max_v = min(values), max(values)
    span = (max_v - min_v) if max_v != min_v else 1.0

    points = []
    for i, v in enumerate(values):
        x = margin + (width - margin * 2) * (i / max(1, len(values) - 1))
        y = height - margin - (height - margin * 2) * ((v - min_v) / span)
        points.append(f"{x:.1f},{y:.1f}")

    polyline = " ".join(points)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
  <rect x="0" y="0" width="{width}" height="{height}" fill="white"/>
  <line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="#999"/>
  <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="#999"/>
  <polyline fill="none" stroke="#2a7de1" stroke-width="2" points="{polyline}"/>
  <text x="{margin}" y="20" font-size="14">Latency Trend (fallback SVG)</text>
</svg>'''
    svg_path.write_text(svg, encoding="utf-8")
    return svg_path.name


def generate_visualizations(output_dir: Path, metrics: List[Metric], result: Dict) -> List[str]:
    artifacts: List[str] = []

    try:
        import matplotlib.pyplot as plt

        if metrics:
            xs = list(range(len(metrics)))
            latency = [float(x["latency_us"]) for x in metrics]
            throughput = [float(x["throughput_gbps"]) for x in metrics]

            fig, ax1 = plt.subplots(figsize=(8, 4))
            ax1.plot(xs, latency, marker="o", label="latency_us", color="#2a7de1")
            ax1.set_xlabel("sample_index")
            ax1.set_ylabel("latency (us)", color="#2a7de1")
            ax1.tick_params(axis="y", labelcolor="#2a7de1")

            ax2 = ax1.twinx()
            ax2.plot(xs, throughput, marker="s", linestyle="--", label="throughput_gbps", color="#ef6c00")
            ax2.set_ylabel("throughput (Gbps)", color="#ef6c00")
            ax2.tick_params(axis="y", labelcolor="#ef6c00")

            plt.title("RDMA Latency & Throughput Trend")
            plt.tight_layout()
            p1 = output_dir / "latency_throughput_trend.png"
            plt.savefig(p1, dpi=140)
            plt.close(fig)
            artifacts.append(p1.name)

        params = result["tuning"]["recommended"]
        labels = ["mtu", "qp_count", "cq_moderation", "inline_size"]
        values = [float(params[k]) for k in labels]

        fig2, ax = plt.subplots(figsize=(7, 4))
        ax.bar(labels, values, color=["#6a1b9a", "#2e7d32", "#c62828", "#1565c0"])
        ax.set_title("Recommended RDMA Parameters")
        ax.set_ylabel("value")
        plt.tight_layout()
        p2 = output_dir / "recommended_params.png"
        plt.savefig(p2, dpi=140)
        plt.close(fig2)
        artifacts.append(p2.name)
    except Exception:
        artifacts.append(_write_svg_fallback(output_dir, metrics))

    return artifacts


def write_report(output_dir: Path, result: Dict, metrics: List[Metric]) -> Dict:
from typing import Dict


def write_report(output_dir: Path, result: Dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "report.json"
    md_path = output_dir / "report.md"

    artifacts = generate_visualizations(output_dir, metrics, result)
    result_with_artifacts = dict(result)
    result_with_artifacts["artifacts"] = artifacts

    json_path.write_text(json.dumps(result_with_artifacts, ensure_ascii=False, indent=2), encoding="utf-8")

    artifacts_lines = "\n".join(f"- {name}" for name in artifacts)
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

## 可视化输出
{artifacts_lines}
"""
    md_path.write_text(md, encoding="utf-8")
    return result_with_artifacts
"""
    md_path.write_text(md, encoding="utf-8")
