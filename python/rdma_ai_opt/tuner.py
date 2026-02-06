from __future__ import annotations

from dataclasses import dataclass, asdict

from .model import PredictionResult


@dataclass
class RDMAParams:
    mtu: int
    qp_count: int
    cq_moderation: int
    inline_size: int


@dataclass
class TuningDecision:
    recommended: RDMAParams
    rationale: str

    def to_dict(self) -> dict:
        return {
            "recommended": asdict(self.recommended),
            "rationale": self.rationale,
        }


def recommend_params(pred: PredictionResult) -> TuningDecision:
    if pred.overload_risk > 0.75:
        return TuningDecision(
            recommended=RDMAParams(mtu=2048, qp_count=16, cq_moderation=64, inline_size=256),
            rationale="高风险负载：提高并发队列并增加 CQ moderation 抑制中断开销。",
        )
    if pred.predicted_latency_us > 12:
        return TuningDecision(
            recommended=RDMAParams(mtu=1024, qp_count=12, cq_moderation=32, inline_size=128),
            rationale="中高延迟：采用平衡参数降低排队与重传影响。",
        )
    return TuningDecision(
        recommended=RDMAParams(mtu=4096, qp_count=8, cq_moderation=16, inline_size=64),
        rationale="低负载低延迟：采用大 MTU 提高吞吐并降低包头开销。",
    )
