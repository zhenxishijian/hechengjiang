from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PredictionResult:
    predicted_latency_us: float
    overload_risk: float


def mllib_predict_latency(metrics: List[Dict[str, float]]) -> PredictionResult:
    """
    使用 Spark MLlib 训练一个轻量模型预测延迟。
    若运行环境缺少 Spark，自动退化为规则近似。
    """
    if not metrics:
        return PredictionResult(predicted_latency_us=0.0, overload_risk=0.0)

    try:
        from pyspark.ml.feature import VectorAssembler
        from pyspark.ml.regression import RandomForestRegressor
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.master("local[*]").appName("rdma-ai-opt").getOrCreate()
        df = spark.createDataFrame(metrics)

        feature_cols = [
            "throughput_gbps",
            "retransmits",
            "queue_depth",
            "cpu_util",
            "hop_count",
            "flow_count",
        ]
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
        ds = assembler.transform(df).select("features", "latency_us")

        model = RandomForestRegressor(
            featuresCol="features", labelCol="latency_us", numTrees=10, maxDepth=4
        ).fit(ds)

        pred = model.transform(ds).selectExpr("avg(prediction) as p").collect()[0]["p"]
        spark.stop()

        overload = min(1.0, pred / 20.0)
        return PredictionResult(predicted_latency_us=float(pred), overload_risk=float(overload))
    except Exception:
        avg_latency = sum(m["latency_us"] for m in metrics) / len(metrics)
        retrans_avg = sum(m["retransmits"] for m in metrics) / len(metrics)
        overload = min(1.0, (avg_latency / 25.0) + (retrans_avg / 20.0))
        return PredictionResult(predicted_latency_us=avg_latency, overload_risk=overload)
