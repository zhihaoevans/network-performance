# network-performance

**网络性能优化中文参考库**：从指标与原理出发，通过观测定位瓶颈，用可复现实验验证优化收益与代价。

面向 Linux 网络/系统开发、DPDK 数据平面、流量检测和高性能服务。既可按路径学习，也可在排障时按症状查阅。

## 快速入口

- 初次使用：[环境准备与开始步骤](GETTING_STARTED.md)
- 查名词：[概念与术语](concepts/README.md)
- 解决问题：[按症状排查](troubleshooting/README.md)
- 查命令：[只读命令速查](observability/commands.md)
- 做实验：[七项实验手册](labs/README.md)
- 用工具：[环境采集与结果汇总](scripts/README.md)

## 内容地图

| 模块 | 主要内容 |
| --- | --- |
| [概念与术语](concepts/README.md) | 吞吐、PPS、P99、BDP、协议与硬件词汇 |
| [基础与方法](fundamentals/README.md) | 目标、假设、证据链、负载模型、统计边界 |
| [Linux 网络栈](linux-networking/README.md) | 收发路径、TCP/UDP、分流、qdisc、参数决策 |
| [网卡与硬件](nic-and-hardware/README.md) | ring、中断合并、offload、NUMA、缓存 |
| [DPDK](dpdk/README.md) | testpmd、mbuf/mempool、burst、多核、检测 |
| [性能观测](observability/README.md) | 命令、perf/eBPF、抓包与计数器 |
| [应用与加密](applications/README.md) | socket I/O、事件循环、背压、TLS/QUIC |
| [虚拟化与云](virtualization/README.md) | 容器路径、配额、conntrack、MTU、VM |
| [高性能路径](advanced/README.md) | socket、XDP、AF_XDP、DPDK、RDMA/RoCE |
| [问题排查](troubleshooting/README.md) | 吞吐不足、分层丢包、尾延迟 |
| [实验](labs/README.md) | 基线、netem、UDP、NUMA、DPDK、批量与检测 |
| [案例](cases/README.md) | 演示证据链与真实案例准入要求 |
| [脚本](scripts/README.md) | 只读采集、iperf3 JSON 汇总、文档检查 |
| [模板](templates/README.md) | 笔记、实验与复盘 |
| [资料](references/README.md) | Linux、DPDK、RFC 与工具官方文档 |

## 按工作目标阅读

| 目标 | 建议路径 |
| --- | --- |
| 查 TCP 为什么跑不满 | 测量设计 → TCP → 吞吐排查 → LAB-001 |
| 做 UDP 小包服务 | UDP → socket I/O → 队列 → LAB-003 |
| 优化 DPDK 转发 | testpmd → 内存/批量 → NUMA → LAB-005 |
| 做安全检测引擎 | DPDK 多核/检测 → 背压 → LAB-007 |
| 排查容器 P99 | 容器网络 → 尾延迟 → perf/eBPF |
| 比较新数据路径 | XDP/AF_XDP → 相同工作量基线 → 功能与运维评估 |

## 使用原则

先定义指标和测量边界，建立基线，再改变一个变量。关注吞吐、尾延迟、失败率和资源成本，不单看峰值。每项变更保存原值，验证后恢复并复测。

正文中的示例 IP、CPU、接口、BDF 和测试值需按环境替换。不存在适合所有机器的 sysctl 参数包。

## 验证状态与边界

本库包含原理参考、实验步骤与演示案例。脚本验证与真实网络性能测试分开：目前尚未收录真实 NIC/DPDK 实测性能数据，演算数值和合成测试不能引用为性能成果。

官方资料集中核对日期：2026-11-01。在线文档和实际运行版本可能不同，详见[版本说明](references/README.md)。本库覆盖主流 Linux/DPDK 优化路径，RDMA 已提供入口参考，但尚未穷尽全部厂商驱动、交换机参数和各云平台实现。

## 维护

```bash
python3 scripts/check_docs.py
python3 -m unittest discover -s tests -v
```

新增内容遵循[维护约定](CONTRIBUTING.md)，状态和下一阶段见[路线图](ROADMAP.md)。
