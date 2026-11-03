# Cache 容量与访问时延

状态：资料参考，非本仓库实测。核对日期：2026-11-03。

## 有明确范围的数字

| 范围 | 指标 | 公布值 | 来源与口径 |
| --- | --- | --- | --- |
| Intel Skylake Server | 每核私有 L2 容量 | 1 MiB | S1 §2.6.1.1，原文 1 MB |
| Intel Skylake Server | L2 cache line | 64 B | S1 §2.6.1.1 |
| Intel Skylake Server | L2 相联度 | 16-way | S1 §2.6.1.1 |
| Intel Skylake Server | L2 最小 load-to-use 时延 | 14 cycles | S1 §2.6.1.1 |
| NASA Aitken Xeon Gold 6248 / Cascade Lake | 每核 L1D 容量、行大小 | 32 KiB、64 B | S2 Cache Hierarchy |
| 同上 | L1D 最快时延 | 4 cycles | S2 fastest latency |
| 同上 | 每核 L2 容量、最快时延 | 1 MiB、14 cycles | S2 fastest latency |
| 同上 | 每 socket 共享 L3 容量 | 27.5 MiB，20 核共享 | S2，非 inclusive |
| 同上 | L3 最快时延参考范围 | 50–70 cycles | S2 公布范围，非分位数或本库实测 |

容量按二进制 cache 容量表示（KiB/MiB），S1/S2 原文使用 KB/MB。只摘取与上述指标相关的数据，不据此推断其他型号的容量、相联度或带宽。

按假设恒定 2.5 GHz 换算，4 / 14 / 50–70 cycles 分别对应 1.6 / 5.6 / 20–28 ns；这是演算，不能代表实际 Aitken 运行频率与延迟。L3 同时涉及 uncore/mesh 时钟，实际换算更需核对计时口径。

## 解释与来源冲突

load-to-use 指加载结果可被后续依赖指令使用所需的时间。读取数据所在层、TLB 命中、地址依赖、访问宽度、对齐、cache 一致性状态、排队与频率都会影响观察值。最小时延不能直接相加来估算一次 DRAM miss，也不能用一次访问的时延倒推流式带宽；多个独立请求可以并行。

核对时发现 NASA 的 Skylake 页面将 L2 最快时延列为 12 cycles，与 Intel Skylake Server 手册的 14 cycles 不一致。本目录采用厂商手册中有明确 load-to-use 定义的 14 cycles；不将两者取平均或混用。Cascade Lake 的 NASA 条目也为 14 cycles。其他架构需另建条目，不外推此表。

- S1：[Intel Optimization Reference Manual，248966-050，§2.6.1.1](https://cdrdv2-public.intel.com/821612/248966-Optimization-Reference-Manual-V1-050.pdf)。
- S2：[NASA HECC Cascade Lake Processors，Article 579](https://www.nas.nasa.gov/hecc/support/kb/cascade-lake-processors_579.html)，页面更新 2025-12-18；该集群维护方的型号与配置说明。
- 冲突记录：[NASA HECC Skylake Processors，Article 550](https://www.nas.nasa.gov/hecc/support/kb/skylake-processors_550.html)，页面更新 2026-03-18。

与网络程序的关系：共享可写 cache line 可能产生一致性流量；每核独立队列与合理布局可作为候选方案。对齐或 padding 会增加工作集，需用相同负载比较吞吐、尾延迟与内存占用。测量见[记录方法](measurement.md)。
