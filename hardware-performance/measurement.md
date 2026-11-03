# 目标机器测量与记录

状态：实验步骤；尚无目标机器实测结果。核对日期：2026-11-03。

## 先记录环境

在 Linux 目标机执行以下只读命令，保留完整输出：

```bash
uname -a
lscpu
lscpu --caches
numactl --hardware
getconf PAGESIZE
perf --version
perf list
```

旧版工具可能不支持部分选项。还需记录 CPU 型号/stepping、微码、BIOS、DIMM 型号/通道/速率、SMT、Turbo、频率策略、SNC/NPS、虚拟化、内核、THP/hugepage、后台负载。cache 拓扑可从 Linux sysfs 的 cpu*/cache/index* 读取，保留 level/type/size/coherency_line_size/shared_cpu_list；CPU0 不一定代表全部核心类型。

## Intel MLC 示例

先阅读下载包自带 README，确认工具版本与 CPU 支持。以下命令会主动分配内存并施加 CPU/内存负载，应在隔离测试窗口运行：

```bash
./mlc --latency_matrix
./mlc --idle_latency
./mlc --loaded_latency
./mlc --bandwidth_matrix
./mlc --c2c_latency
```

Intel 官方说明：工具默认可能通过 MSR 临时关闭硬件预取，完成后恢复；运行权限与具体行为依版本/平台而定。要求保持预取设置时，查本版本的 `-e` 选项，且在结果注明预取状态；不要将两种设置的结果直接比较。正常退出后核对系统设置，异常中断后检查预取及 NUMA balancing 等可能受工具影响的状态，按运行前记录恢复。不要为了运行工具随意修改生产机权限。

以上选项含义依据 [Intel MLC 官方页](https://www.intel.com/content/www/us/en/developer/articles/tool/intelr-memory-latency-checker.html)。输出统计值按工具定义记录；没有延迟分布时不能改写为 P99。

## Cache 与时钟实验

缓存微基准应使用随机、串行依赖的指针追逐，避免编译器删掉加载；将工作集从小于 L1 扩展到超过 LLC，并记录有效容量、页大小、预热与 TLB 状态。顺序扫描易被预取与并行请求影响。只凭工作集大小不能保证所有访问命中指定层，需结合型号对应 PMU 事件解释。

计时开销、指令排序、迁核和时钟语义需专门处理。未验证的 RDTSC 小片段不作为准确时延来源。优先用工具原始 ns 输出，周期换算另附频率与计数器假设。

每组建议至少重复 5 次，保留各次结果、离散程度和失败运行；不要把多次均值的分布当成逐访问 P99。NUMA 实验记录 CPU 与内存绑定策略以及实际页归属。

## 结果记录模板

| 字段 | 内容 |
| --- | --- |
| 状态 | 实测 / 公式推导 / 资料引用 |
| 时间与环境 | 日期、机器标识、CPU/内存/内核/BIOS |
| 工具 | 名称、版本、下载来源、完整命令 |
| 指标 | latency/bandwidth/cycles、单位、统计口径 |
| 配置 | CPU/node、内存 node、页大小、工作集、预取、频率 |
| 负载 | 线程数、访问模式、读写比例、背景流量 |
| 原始数据 | 每次完整输出与失败日志的位置 |
| 结论边界 | 适用机器与条件、未测项目 |
| 恢复 | 运行前后设置对比、恢复结果 |

完整实验使用[仓库实验模板](../templates/experiment.md)。仅凭 VM/Codespaces 的结果不能声明获得宿主机 cache/DRAM 的裸机基线。
