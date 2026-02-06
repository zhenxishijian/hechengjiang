# 系统设计

## 数据流

1. 监控模块收集 RDMA 运行指标
2. AI 模型进行延迟预测与参数推荐
3. 执行模块应用推荐参数
4. 报告模块输出优化前后对比

## 输入特征（示例）

- `latency_us`
- `throughput_gbps`
- `retransmits`
- `queue_depth`
- `cpu_util`
- `hop_count`
- `flow_count`

## 输出建议（示例）

- `mtu`
- `qp_count`
- `cq_moderation`
- `inline_size`
- `target_path`
