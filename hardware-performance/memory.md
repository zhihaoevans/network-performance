# 内存、NUMA 与带宽

状态：公式推导与资料参考；DRAM 访问时延待目标机器实测。核对日期：2026-11-03。

## 可以计算的数据

有效数据位宽为 64 bit（8 B）时，单通道理论数据带宽为：

`带宽(GB/s) = 传输率(MT/s) × 8 / 1000`

| 假设配置 | 理论上限 |
| --- | --- |
| DDR4-2666，单通道，64 bit 有效数据 | 21.328 GB/s |
| DDR4-2666，6 通道全部以该速率工作 | 127.968 GB/s |
| DDR4-2933，单通道，64 bit 有效数据 | 23.464 GB/s |
| DDR4-2933，6 通道全部以该速率工作 | 140.784 GB/s |

GB/s 为十进制；1 GiB/s = 2^30 B/s。表内使用整数 2666/2933 MT/s 演算，标称速率的取整会带来差异。DDR 的 MT/s 表示每秒传输次数，不能把 DDR4-2666 写成 2666 MHz 的 DRAM 时钟。ECC 校验位不作为应用有效数据带宽。

NASA 的 Aitken Xeon Gold 6248 配置为每 socket 六通道、每通道一条 16 GB DIMM，页面公布约 141 GB/s 每 socket，与六通道 DDR4-2933 演算一致。理论值未扣除刷新、命令、读写切换、控制器效率与访问模式影响；读写共享通道，不能把这个值同时作为读和写各自可用的带宽。[配置来源：NASA HECC，Memory Subsystem](https://www.nas.nasa.gov/hecc/support/kb/cascade-lake-processors_579.html)。

## 需要测量的数据

| 指标 | 本目录数值状态 | 必须补充的条件 |
| --- | --- | --- |
| 本地 NUMA 空闲 DRAM 时延 | 待测，ns | CPU/node、内存 node、工作集、预取、页大小 |
| 跨 NUMA DRAM 时延 | 待测，ns | 本地/远端拓扑、SNC/NPS、互连、页实际位置 |
| 带负载 DRAM 时延 | 待测，ns | 带宽负载、读写比例、并发、延迟统计口径 |
| 持续内存带宽 | 待测，GB/s 或 GiB/s | 通道填充、实际速率、线程数、读写比例、工作集 |

DRAM 的 CAS 时序只覆盖部分器件时序；CPU 访问还涉及 cache/TLB、控制器、行状态、互连和排队，因此不能把 CL 换算结果直接写成 CPU 到内存延迟。远端内存也不能按固定“本地的两倍”推算。

[Intel MLC 官方说明](https://www.intel.com/content/www/us/en/developer/articles/tool/intelr-memory-latency-checker.html)提供空闲、负载、NUMA 矩阵与 cache-to-cache 测量入口。具体实验和记录见[测量方法](measurement.md)。
