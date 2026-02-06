# RDMA-AI HPC Optimizer

基于 **RDMA + AI + MLlib** 的高性能计算优化工具（C++/Python 混合架构）。

## 目标

利用 AI 分析网络拓扑与数据流模式，自动调优 RDMA 参数，实现更低延迟与更高吞吐。

## 功能

1. **实时监控 RDMA 传输性能**（延迟、吞吐、重传率、队列深度）
2. **AI 驱动参数调优**（动态调整 MTU、QP、CQ moderation、inline size）
3. **预测性负载均衡**（根据时间窗内趋势提前迁移/分配流量）
4. **生成优化报告**（JSON + Markdown 报告）

## 架构

- `cpp/`：高性能采集与执行器（可直接接入 RDMA 运行时）
- `python/`：AI/MLlib 分析与策略决策
- `docs/`：设计文档与数据格式

## 快速开始

### 1) Python 侧（MLlib）

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m rdma_ai_opt.cli --input sample_metrics.jsonl --report ../reports/latest
```

### 2) C++ 侧

```bash
cmake -S cpp -B build
cmake --build build
./build/rdma_optimizer --metrics ../python/sample_metrics.jsonl --python-script ../python/rdma_bridge.py
```

## 说明

- 当前仓库提供的是**可落地扩展的框架实现**，RDMA 实时指标采集点位已预留；可接入 `ibstat` / `perfquery` / 自定义遥测接口。
- 若运行环境未安装 Spark，会自动使用降级策略进行规则推断（便于本地验证）。


## 在 Windows + VMware + Ubuntu 上运行

如果你只有 Windows 电脑，推荐在 **Ubuntu 虚拟机**中运行本项目。完整步骤见：

- `docs/windows_vm_ubuntu_runbook.md`

最短路径如下：

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip build-essential cmake
cd /path/to/repo/python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m rdma_ai_opt.cli --input sample_metrics.jsonl --report ../reports/latest
cd ..
cmake -S cpp -B build
cmake --build build
./build/rdma_optimizer --metrics python/sample_metrics.jsonl --python-script python/rdma_bridge.py
```


### Ubuntu 22.04 一键初始化（可直接复制）

```bash
chmod +x scripts/bootstrap_ubuntu_2204.sh
./scripts/bootstrap_ubuntu_2204.sh
```
