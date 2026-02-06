# Windows + VMware + Ubuntu 运行手册

这份手册面向只有 Windows 主机、通过 VMware 使用 Ubuntu 虚拟机的场景。

## 一、建议的运行位置

- **推荐：在 Ubuntu 虚拟机中运行**（最稳妥）
  - 项目包含 CMake/C++ 编译与 Python 依赖，Linux 环境配置更直接。
  - 后续若接入真实 RDMA 工具链（如 `ibstat`），也更贴近生产环境。
- 不建议直接在 Windows 原生环境运行当前版本（需额外处理编译链和路径差异）。

## 二、Ubuntu 虚拟机准备

### 1) 安装基础工具

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip build-essential cmake
```

### 2) （可选）安装 Java 以启用 Spark/MLlib

> 若不安装 Java/Spark，程序仍可运行，会自动降级为规则推断模式。

```bash
sudo apt install -y openjdk-17-jre
java -version
```


## 二点五、Ubuntu 22.04 一键命令（推荐）

如果你希望先跑通，再慢慢理解细节，可在仓库根目录执行：

```bash
chmod +x scripts/bootstrap_ubuntu_2204.sh
./scripts/bootstrap_ubuntu_2204.sh
```

该脚本会自动完成：
- 安装 Ubuntu 22.04 需要的基础依赖
- 创建 `python/.venv` 并安装 Python 包
- 执行 Python AI 管线验证
- 编译并运行 C++ 执行器验证

## 三、获取并进入项目

如果你已经把项目放在 VMware 共享目录，可直接 `cd` 到对应路径。

```bash
git clone <你的仓库地址> rdma-ai-hpc-optimizer
cd rdma-ai-hpc-optimizer
```

## 四、运行 Python AI 管线（最小可用）

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m rdma_ai_opt.cli --input sample_metrics.jsonl --report ../reports/latest
```

成功后会在项目根目录下生成：
- `reports/latest/report.json`
- `reports/latest/report.md`

## 五、编译并运行 C++ 执行器

回到项目根目录：

```bash
cd ..
cmake -S cpp -B build
cmake --build build
./build/rdma_optimizer --metrics python/sample_metrics.jsonl --python-script python/rdma_bridge.py
```

## 六、你需要特别确认的 5 个点

1. **Python 版本**：`python3 --version`（建议 3.10+）
2. **CMake 可用**：`cmake --version`
3. **C++ 编译器可用**：`g++ --version`
4. **虚拟机磁盘空间**：至少预留 2GB
5. **网络可访问 PyPI**：`pip install -r requirements.txt` 能成功

## 七、常见问题

### 1) `pyspark` 启动失败 / Java 相关报错
- 原因：未安装 Java 或 `JAVA_HOME` 未正确配置。
- 处理：安装 `openjdk-17-jre` 后重试；若仍失败，可先使用降级模式验证流程。

### 2) C++ 程序运行后提示 Python 文件找不到
- 原因：启动目录不在项目根目录，导致相对路径错误。
- 处理：确保在项目根目录执行 `./build/rdma_optimizer ...` 命令。

### 3) VMware 共享目录权限问题
- 建议先把代码复制到 Ubuntu 本地目录（如 `~/workspace`）再构建，避免共享目录的权限/IO 问题。
