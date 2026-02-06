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

### 1) Python 侧（基础依赖）

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# 可选：如果你想启用 Spark/MLlib 再安装这一行
# pip install -r requirements-ml.txt
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
# 可选：如果你想启用 Spark/MLlib 再安装这一行
# pip install -r requirements-ml.txt
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


### `pyspark` 安装失败（Failed building wheel for pyspark）怎么办

如果你遇到该错误，不会影响本项目基础运行。原因通常是本机构建链或环境限制。

可按下面顺序处理：

```bash
# 1) 先保证基础功能可运行
cd python
source .venv/bin/activate
pip install -r requirements.txt
python -m rdma_ai_opt.cli --input sample_metrics.jsonl --report ../reports/latest

# 2) 再尝试安装可选 MLlib（失败也不阻塞）
pip install -r requirements-ml.txt || true
```

说明：`python/rdma_ai_opt/model.py` 已内置回退逻辑，缺少 Spark 时会自动使用规则推断。


### `pyspark` 安装出现 `No space left on device`

这是磁盘空间不足导致的（`pyspark` 体积较大）。建议：

```bash
# 查看剩余空间
df -h

# 清理 apt 与 pip 缓存
sudo apt clean
rm -rf ~/.cache/pip

# 仅安装基础依赖（先跑通）
cd python
source .venv/bin/activate
pip install -r requirements.txt
python -m rdma_ai_opt.cli --input sample_metrics.jsonl --report ../reports/latest

# 可选 Spark，使用 no-cache 降低磁盘占用（失败也不阻塞）
pip install --no-cache-dir -r requirements-ml.txt || true
```
