# network-performance

网络性能优化知识库，以中文积累原理、测量方法、可复现实验和问题复盘。重点覆盖 Linux 网络栈、网卡与硬件、DPDK 和性能观测。

## 知识导航

| 目录 | 内容 |
| --- | --- |
| [基础与方法](fundamentals/README.md) | 吞吐量、PPS、延迟、基线与实验设计 |
| [Linux 网络栈](linux-networking/README.md) | 收发路径、TCP、软中断、RSS/RPS |
| [网卡与硬件](nic-and-hardware/README.md) | 队列、NUMA、PCIe、offload |
| [DPDK](dpdk/README.md) | PMD、内存池、批处理、多核扩展 |
| [性能观测](observability/README.md) | perf、eBPF、抓包与瓶颈定位 |
| [实验](labs/README.md) | 环境记录、基线与优化对比 |
| [案例](cases/README.md) | 现象、证据、根因、修复与回归 |
| [模板](templates/README.md) | 知识笔记、实验报告、问题复盘 |

## 如何积累

1. 从[积累路线](ROADMAP.md)选择一个问题。
2. 复制[笔记模板](templates/note.md)，整理机制、来源和待验证假设。
3. 从[基线实验](labs/001-network-baseline.md)开始，记录环境和原始结果。
4. 用[实验模板](templates/experiment.md)对比优化前后表现。
5. 将有证据的结论整理为案例，并更新所属目录索引。

## 内容状态

- **待研究**：只有问题或资料线索。
- **待验证**：有解释或方案，尚无本仓库实验支撑。
- **已验证（限定环境）**：有环境、步骤、原始结果与适用范围。
- **已失效**：版本变化或新证据推翻结论，保留原因。

当前是初始框架，主题清单和实验设计不代表已经完成测试。

## 记录约定

- 文件名使用英文小写与短横线，例如 `tcp-retransmission.md`。
- 每篇笔记聚焦一个问题，结论标明资料来源或实验依据。
- 记录内核、驱动、固件和工具版本，调优配置必须说明适用条件。
- 对比时优先只改变一个变量，同时关注吞吐量、尾延迟、丢包和资源开销。
- 资料记录原文链接与自己的理解，不整篇搬运。
- 提交前脱敏，原始抓包和大体积测试产物默认不入库。
- 提交消息示例：`docs: add RSS notes`、`lab: record baseline`、`case: analyze packet loss`。

下一步：完成 LAB-001 的环境记录和基线报告，根据数据选择深入专题。
