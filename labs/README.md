# 实验手册

| 编号 | 实验 | 要验证的问题 | 前提 |
| --- | --- | --- | --- |
| 001 | [TCP/UDP 双端基线](001-network-baseline.md) | 方向、单流/多流与端点限制 | 两端 Linux、iperf3 |
| 002 | [namespace/netem](002-netns-netem.md) | 延迟注入、恢复与测量边界 | Linux 网络管理权限 |
| 003 | [UDP 包长](003-udp-packet-size.md) | 逐包成本与带宽成本 | 双端基线 |
| 004 | [队列与 NUMA](004-queues-numa.md) | 分流与局部性 | 多队列/可选多 NUMA |
| 005 | [DPDK 转发](005-dpdk-forwarding.md) | 帧长、核数、队列、burst | 实验 NIC 与发包器 |
| 006 | [批处理与延迟](006-batching-latency.md) | 吞吐与 P99 的取舍 | 可配置的被测程序 |
| 007 | [异步检测闭环](007-detection-pipeline.md) | 队列、检测成本与降级 | 自行实现或已有检测程序 |

001–005 提供步骤或配置矩阵，006–007 是依赖被测程序的实验设计。所有实验均未在本仓库取得真实硬件性能结果。

先阅读[环境准备](../GETTING_STARTED.md)。每组使用[实验模板](../templates/experiment.md)，记录原始结果、变更与恢复。合成数据测试只能验证脚本逻辑，不能替代上述性能实验。
